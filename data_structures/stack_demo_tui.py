import json
import shlex
from pathlib import Path

from textual.app import ComposeResult
from textual.widgets import Footer, Header, Input, RichLog, Static

from data_structures.tui_common import (
    BaseLinearStructureTUI,
    build_linear_parser,
    build_random_values,
    clamp_scroll_offset,
    format_display_value,
    format_value_batch,
    get_type_name,
    nonnegative_int,
    parse_bool,
    parse_single_path,
    parse_value_tokens,
    INT32_MIN,
    INT32_MAX,
    FLOAT32_MIN,
    FLOAT32_MAX,
)


class StackDemo:
    SUPPORTED_TYPES = {"int": int, "float": float, "str": str, "bool": parse_bool}

    def __init__(self, max_size=1000):
        self.stack = []
        self.max_size = max_size
        self.element_type = int

    def set_type(self, type_name):
        if type_name in ("any", ""):
            self.element_type = None
        elif type_name in self.SUPPORTED_TYPES:
            self.element_type = self.SUPPORTED_TYPES[type_name]
        else:
            raise ValueError(f"Unknown type '{type_name}'. Use: int, float, str, bool, any")

    def push(self, item):
        return self.push_many([item])[0]

    def push_many(self, items):
        converted_items = [self._convert_item(item) for item in items]
        if len(self.stack) + len(converted_items) > self.max_size:
            raise OverflowError(f"Stack overflow: capacity is {self.max_size}")
        self.stack.extend(converted_items)
        return converted_items

    def pop(self):
        if self.is_empty():
            raise IndexError("Pop from an empty stack")
        return self.stack.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("Peek from an empty stack")
        return self.stack[-1]

    def is_empty(self):
        return len(self.stack) == 0

    def size(self):
        return len(self.stack)

    def remaining_capacity(self):
        return self.max_size - len(self.stack)

    def clear(self):
        self.stack.clear()

    def swap(self):
        if self.size() < 2:
            raise IndexError("Swap requires at least two items")
        top = self.stack[-1]
        next_item = self.stack[-2]
        self.stack[-2], self.stack[-1] = top, next_item
        return self.stack[-2], self.stack[-1]

    def rotate(self):
        if self.size() < 3:
            raise IndexError("Rotate requires at least three items")
        third, second, top = self.stack[-3:]
        self.stack[-3:] = [second, top, third]
        return self.stack[-3:]

    def dup(self):
        if self.is_empty():
            raise IndexError("Dup requires at least one item")
        item = self.peek()
        self.push(item)
        return item

    def at(self, index: int):
        if index < 0:
            raise IndexError("At requires a non-negative index")
        if index >= self.size():
            raise IndexError(f"At index {index} is out of range for stack size {self.size()}")
        return self.stack[-1 - index]

    def _convert_item(self, item):
        if self.element_type is None:
            return item
        try:
            return self.element_type(item)
        except (ValueError, TypeError):
            raise TypeError(f"Cannot convert {item!r} to {self.element_type.__name__}")


def parse_push_values(arg: str):
    values = shlex.split(arg)
    if not values:
        raise ValueError("Usage: /push <value> [more values ...]")
    return values


def save_session(path: Path, stack: StackDemo) -> None:
    payload = {
        "type": get_type_name(stack.element_type),
        "items": stack.stack,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def load_session(path: Path):
    payload = json.loads(path.read_text(encoding="utf-8"))
    type_name = payload.get("type", "any")
    items = payload.get("items")
    if type_name not in {"any", "int", "float", "str", "bool"}:
        raise ValueError(f"Unsupported session type {type_name!r}")
    if not isinstance(items, list):
        raise ValueError("Session file is missing a valid item list")
    return type_name, items


def snapshot_stack(stack: StackDemo):
    return {
        "type": get_type_name(stack.element_type),
        "items": list(stack.stack),
    }


def restore_stack(snapshot, max_size: int) -> StackDemo:
    restored = StackDemo(max_size=max_size)
    restored.set_type(snapshot["type"])
    restored.push_many(snapshot["items"])
    return restored


def build_stack_view(stack_items, view_top=None, scroll_offset: int = 0):
    items = list(reversed(stack_items))
    effective_view_top = None if view_top is None else max(view_top, 2)

    if effective_view_top is None or len(items) <= effective_view_top:
        return {
            "visible_items": items,
            "visible_displacements": list(range(len(items))),
            "hidden_newer": 0,
            "hidden_older": 0,
            "scroll_offset": 0,
            "window_size": max(len(items) - 2, 0),
            "stack_size": len(items),
        }

    if len(items) == 1:
        return {
            "visible_items": items[:1],
            "visible_displacements": [0],
            "hidden_newer": 0,
            "hidden_older": 0,
            "scroll_offset": 0,
            "window_size": 0,
            "stack_size": 1,
        }

    middle_items = items[1:-1]
    window_size = max(effective_view_top - 2, 0)
    offset = clamp_scroll_offset(len(items), view_top, scroll_offset)
    visible_middle = middle_items[offset:offset + window_size]
    visible_displacements = [0, *(offset + i + 1 for i in range(len(visible_middle))), len(items) - 1]

    return {
        "visible_items": [items[0], *visible_middle, items[-1]],
        "visible_displacements": visible_displacements,
        "hidden_newer": offset,
        "hidden_older": max(len(middle_items) - (offset + len(visible_middle)), 0),
        "scroll_offset": offset,
        "window_size": window_size,
        "stack_size": len(items),
    }


class StackPanel(Static):
    def refresh_stack(self, demo: StackDemo, view_top=None, scroll_offset: int = 0) -> None:
        header = f"Stack ({demo.size()}/{demo.max_size})  type: {get_type_name(demo.element_type)}"
        view = build_stack_view(demo.stack, view_top=view_top, scroll_offset=scroll_offset)
        items = view["visible_items"]

        if view_top is not None:
            header += f"  view-top: {view_top}"

        older_displacements = [d for d in view["visible_displacements"] if d > 0]
        if view["window_size"] > 0 or view["hidden_older"] > 0:
            total_older = max(demo.size() - 1, 0)
            if not older_displacements:
                header += "  older: none visible"
            else:
                start = older_displacements[0]
                end = older_displacements[-1]
                header += f"  older: {start}-{end}/{total_older}"

        if demo.is_empty():
            self.update(f"{header}\n  (empty)")
            return

        label_width = max(
            len("offset"),
            max(len(self._format_offset_label(displacement, view["stack_size"])) for displacement in view["visible_displacements"]),
        )
        rendered_values = [format_display_value(item) for item in items]
        type_labels = [type(item).__name__ for item in items]
        value_width = max(len("value"), max(len(rendered) for rendered in rendered_values), 5)
        type_width = max(len("type"), max(len(type_label) for type_label in type_labels))

        lines = []
        if view["hidden_newer"] > 0:
            lines.append(f"  ... {view['hidden_newer']} newer hidden ...")

        lines.append(
            f"  ┌{'─' * (label_width + 2)}┬{'─' * (value_width + 2)}┬{'─' * (type_width + 2)}┐"
        )
        lines.append(
            f"  │ {'offset':<{label_width}} │ {'value':^{value_width}} │ {'type':<{type_width}} │"
        )
        lines.append(
            f"  ├{'─' * (label_width + 2)}┼{'─' * (value_width + 2)}┼{'─' * (type_width + 2)}┤"
        )
        for displacement, rendered_value, type_label in zip(view["visible_displacements"], rendered_values, type_labels):
            label = self._format_offset_label(displacement, view["stack_size"])
            lines.append(
                f"  │ {label:<{label_width}} │ {rendered_value:^{value_width}} │ {type_label:<{type_width}} │"
            )
        lines.append(
            f"  └{'─' * (label_width + 2)}┴{'─' * (value_width + 2)}┴{'─' * (type_width + 2)}┘"
        )

        if view["hidden_older"] > 0:
            lines.append(f"  ... {view['hidden_older']} older hidden ...")

        self.update(header + "\n" + "\n".join(lines))

    @staticmethod
    def _format_offset_label(displacement: int, stack_size: int) -> str:
        if stack_size == 1:
            return "top=bottom"
        if displacement == 0:
            return "top"
        if displacement == stack_size - 1:
            return "bottom"
        return f"top-{displacement}"


class StackDemoTUI(BaseLinearStructureTUI):
    STRUCTURE_NAME = "Stack"
    START_LABEL = "bottom"
    END_LABEL = "top"
    DEFAULT_TYPE = "int"

    CSS = """
    StackPanel {
        height: auto;
        min-height: 4;
        border: solid $primary;
        padding: 0 1;
        margin-bottom: 1;
    }
    RichLog {
        height: 1fr;
        border: solid $panel;
    }
    Input {
        margin-top: 1;
    }
    """

    BINDINGS = [
        ("ctrl+d", "quit", "Quit"),
        ("up", "scroll_up", "Older"),
        ("down", "scroll_down", "Newer"),
        ("pageup", "page_up", "Page older"),
        ("pagedown", "page_down", "Page newer"),
        ("home", "scroll_home", "Newest"),
    ]

    def __init__(self, max_size: int = 1000, **kwargs):
        self.demo = StackDemo(max_size=max_size)
        super().__init__(max_size=max_size, **kwargs)

    def set_type(self, type_name: str) -> None:
        super().set_type(type_name)
        self.demo.element_type = self.element_type

    def compose(self) -> ComposeResult:
        yield Header()
        yield StackPanel(id="panel")
        yield RichLog(id="log", highlight=True, markup=True)
        yield Input(placeholder=self.placeholder_text())
        yield Footer()

    def get_items(self) -> list:
        return list(self.demo.stack)

    def append_values(self, values) -> None:
        if self.structure_size() + len(values) > self.max_size:
            raise OverflowError(f"Stack overflow: capacity is {self.max_size}")
        self.demo.push_many(values)

    def clear_structure(self) -> None:
        self.demo.clear()

    def replace_items(self, items) -> None:
        self.demo.clear()
        self.demo.push_many(items)

    def show_state_text(self) -> str:
        return f"stack top → bottom: {list(reversed(self.demo.stack))!r}"

    def placeholder_text(self) -> str:
        return "/help  /push <v...>  /random <n>  /pop  /peek  /at <index>  /dup  /swap  /rotate  /clear  /save <file>  /load <file>  /undo  /redo  /type [int|float|str|bool|any]  /quit"

    def help_lines(self) -> list[str]:
        return [
            "  [cyan]/push[/cyan] VALUE [VALUE ...]      push one or more values onto the stack",
            "  [cyan]/pop[/cyan]                        pop the top value",
            "  [cyan]/peek[/cyan]                       inspect the top value",
            "  [cyan]/at[/cyan] INDEX                   inspect 0,1,2,... relative to the top",
            "  [cyan]/dup[/cyan]                        duplicate the top value",
            "  [cyan]/swap[/cyan]                       swap the top two values",
            "  [cyan]/rotate[/cyan]                     rotate the top three values",
        ]

    def handle_structure_command(self, verb: str, arg: str | None, log: RichLog) -> bool:
        if verb == "/push":
            if arg is None:
                log.write("[red]Usage: /push <value> [more values ...][/red]")
                return True
            try:
                self._record_undo_state()
                pushed = self._convert_many(parse_value_tokens(arg, "Usage: /push <value> [more values ...]"))
                self.append_values(pushed)
                self.scroll_offset = 0
                log.write(
                    f"[green]push({len(pushed)} values) added {format_value_batch(pushed)}  "
                    f"{self.show_state_text()}  size={self.structure_size()}[/green]"
                )
            except OverflowError as e:
                log.write(f"[red]Overflow: {e}[/red]")
            except TypeError as e:
                log.write(f"[red]TypeError: {e}[/red]")
            except ValueError as e:
                log.write(f"[red]{e}[/red]")
            return True

        if verb == "/pop":
            try:
                self._record_undo_state()
                val = self.demo.pop()
                self._clamp_scroll_offset()
                log.write(f"[green]pop() → {val!r}  size={self.structure_size()}[/green]")
            except IndexError as e:
                log.write(f"[red]Underflow: {e}[/red]")
            return True

        if verb == "/peek":
            try:
                log.write(f"[cyan]peek() → {self.demo.peek()!r}[/cyan]")
            except IndexError as e:
                log.write(f"[red]Underflow: {e}[/red]")
            return True

        if verb == "/at":
            if arg is None:
                log.write("[red]Usage: /at <non-negative-index>[/red]")
                return True
            try:
                index = nonnegative_int(arg)
                val = self.demo.at(index)
                log.write(f"[cyan]at({index}) → {val!r}[/cyan]")
            except ValueError as e:
                log.write(f"[red]{e}[/red]")
            except IndexError as e:
                log.write(f"[red]RangeError: {e}[/red]")
            return True

        if verb == "/dup":
            try:
                self._record_undo_state()
                duplicated = self.demo.dup()
                self.scroll_offset = 0
                log.write(
                    "[green]dup()[/green] "
                    f"→ duplicated {duplicated!r}  size={self.structure_size()}\n"
                    "[dim]"
                    f"Equivalent steps: a = peek()  # {duplicated!r}; push(a)"
                    "[/dim]"
                )
            except (IndexError, OverflowError) as e:
                label = "Overflow" if isinstance(e, OverflowError) else "Underflow"
                log.write(f"[red]{label}: {e}[/red]")
            return True

        if verb == "/swap":
            try:
                self._record_undo_state()
                original_top = self.demo.stack[-1]
                original_next = self.demo.stack[-2]
                first, second = self.demo.swap()
                log.write(
                    "[green]swap()[/green] "
                    f"→ top two are now {first!r}, {second!r}  size={self.structure_size()}\n"
                    "[dim]"
                    f"Equivalent steps: a = pop()  # {original_top!r}; "
                    f"b = pop()  # {original_next!r}; "
                    "push(a); push(b)"
                    "[/dim]"
                )
            except IndexError as e:
                log.write(f"[red]Underflow: {e}[/red]")
            return True

        if verb == "/rotate":
            try:
                self._record_undo_state()
                original_top = self.demo.stack[-1]
                original_second = self.demo.stack[-2]
                original_third = self.demo.stack[-3]
                rotated = self.demo.rotate()
                log.write(
                    "[green]rotate()[/green] "
                    f"→ top three are now {rotated!r}  size={self.structure_size()}\n"
                    "[dim]"
                    f"Equivalent steps: a = pop()  # {original_top!r}; "
                    f"b = pop()  # {original_second!r}; "
                    f"c = pop()  # {original_third!r}; "
                    "push(b); push(a); push(c)"
                    "[/dim]"
                )
            except IndexError as e:
                log.write(f"[red]Underflow: {e}[/red]")
            return True

        return False

    def _refresh_panel(self) -> None:
        self._clamp_scroll_offset()
        self.query_one(StackPanel).refresh_stack(
            self.demo,
            view_top=self.view_top,
            scroll_offset=self.scroll_offset,
        )


def build_parser():
    return build_linear_parser("Interactive Stack Demo")


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if args.int_min > args.int_max:
        parser.error("--int-min must be less than or equal to --int-max")
    if args.float_min > args.float_max:
        parser.error("--float-min must be less than or equal to --float-max")
    StackDemoTUI(
        max_size=args.max_size,
        view_top=args.view_top,
        int_min=args.int_min,
        int_max=args.int_max,
        float_min=args.float_min,
        float_max=args.float_max,
    ).run()


if __name__ == "__main__":
    main()
