import argparse
import json
import random
import shlex
import time
from pathlib import Path

from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Input, RichLog, Static

from data_structures.capture_utils import (
    default_session_name,
    ensure_capture_session,
    next_frame_paths,
    parse_capture_mode,
    parse_session_arg,
    parse_video_args,
    render_capture_video,
    append_capture_frame,
    render_text_frame_image,
)
from data_structures.tui_common import format_elapsed_ns

INT32_MIN = -(2 ** 31)
INT32_MAX = 2 ** 31 - 1
FLOAT32_MIN = -3.4028235e38
FLOAT32_MAX = 3.4028235e38
WORDS_PATH = Path(__file__).resolve().parent.parent / "data" / "words.txt"
TRUE_STRINGS = {"true", "t", "1", "yes", "y", "on"}
FALSE_STRINGS = {"false", "f", "0", "no", "n", "off"}
DISPLAY_VALUE_LIMIT = 40


def parse_bool(value) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)) and value in (0, 1):
        return bool(value)

    normalized = str(value).strip().lower()
    if normalized in TRUE_STRINGS:
        return True
    if normalized in FALSE_STRINGS:
        return False
    raise ValueError(f"Cannot interpret {value!r} as bool")


def get_type_name(element_type) -> str:
    if element_type is None:
        return "any"
    if element_type is parse_bool:
        return "bool"
    return element_type.__name__


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


def positive_int(value: str) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("value must be a positive integer")
    return parsed


def nonnegative_int(value: str) -> int:
    parsed = int(value)
    if parsed < 0:
        raise argparse.ArgumentTypeError("value must be a non-negative integer")
    return parsed


def clamp_scroll_offset(stack_size: int, view_top, scroll_offset: int) -> int:
    if view_top is None or stack_size <= 2:
        return 0

    effective_view_top = max(view_top, 2)
    if stack_size <= effective_view_top:
        return 0

    middle_count = stack_size - 2
    middle_window_size = max(effective_view_top - 2, 0)
    if middle_window_size <= 0:
        return 0

    max_offset = middle_count - middle_window_size
    return min(max(scroll_offset, 0), max_offset)


def parse_push_values(arg: str):
    values = shlex.split(arg)
    if not values:
        raise ValueError("Usage: /push <value> [more values ...]")
    return values


def parse_single_path(arg: str, command_name: str) -> Path:
    parts = shlex.split(arg)
    if len(parts) != 1:
        raise ValueError(f"Usage: /{command_name} <path>")
    return Path(parts[0]).expanduser()


def save_session(path: Path, stack: StackDemo) -> None:
    type_name = get_type_name(stack.element_type)
    payload = {
        "type": type_name,
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


def load_words():
    with WORDS_PATH.open(encoding="utf-8") as words_file:
        return [line.strip() for line in words_file if line.strip()]


def format_value_batch(values) -> str:
    if len(values) == 1:
        return repr(values[0])
    return repr(values)


def format_display_value(value) -> str:
    rendered = str(value)
    if len(rendered) > DISPLAY_VALUE_LIMIT:
        return rendered[:DISPLAY_VALUE_LIMIT] + "..."
    return rendered


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


def build_random_values(
    count: int,
    element_type,
    words,
    rng: random.Random,
    int_min: int,
    int_max: int,
    float_min: float,
    float_max: float,
):
    if count <= 0:
        raise ValueError("Usage: /random <positive-count>")

    if element_type is int:
        return [rng.randint(int_min, int_max) for _ in range(count)]

    if element_type is float:
        return [rng.uniform(float_min, float_max) for _ in range(count)]

    if element_type is str:
        return [rng.choice(words) for _ in range(count)]

    if element_type is parse_bool:
        return [rng.choice([True, False]) for _ in range(count)]

    random_builders = (
        lambda: rng.randint(int_min, int_max),
        lambda: rng.uniform(float_min, float_max),
        lambda: rng.choice(words),
        lambda: rng.choice([True, False]),
    )
    return [rng.choice(random_builders)() for _ in range(count)]


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
        type_label = demo.element_type.__name__ if demo.element_type else "any"
        header = f"Stack ({demo.size()}/{demo.max_size})  type: {type_label}"
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


class StackDemoTUI(App):
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

    def __init__(
        self,
        max_size: int = 1000,
        view_top: int = 8,
        int_min: int = INT32_MIN,
        int_max: int = INT32_MAX,
        float_min: float = FLOAT32_MIN,
        float_max: float = FLOAT32_MAX,
        capture_dir: Path | None = None,
        video_dir: Path | None = None,
    ):
        super().__init__()
        self.demo = StackDemo(max_size=max_size)
        self.view_top = view_top
        self.scroll_offset = 0
        self.int_min = int_min
        self.int_max = int_max
        self.float_min = float_min
        self.float_max = float_max
        self.capture_dir = capture_dir if capture_dir is not None else Path.cwd() / ".capture"
        self.video_dir = video_dir if video_dir is not None else Path.cwd() / ".video"
        self.random = random.Random()
        self.words = load_words()
        self.undo_history = []
        self.redo_history = []
        self.capture_session_name = default_session_name("stack-demo")
        self.capture_enabled = False

    def compose(self) -> ComposeResult:
        yield Header()
        yield StackPanel(id="panel")
        yield RichLog(id="log", highlight=True, markup=True)
        yield Input(
            placeholder="/help  /push <v...>  /random <n>  /pop  /peek  /at <index>  /dup  /swap  /rotate  /clear  /session <name>  /capture [on|off]  /video [session] [seconds]  /save <file>  /load <file>  /undo  /redo  /type [int|float|str|bool|any]  /quit"
        )
        yield Footer()

    def on_mount(self) -> None:
        self._refresh_panel()
        self.query_one(RichLog).write(
            "[bold]Stack Demo[/bold] — type [cyan]/help[/cyan] for commands."
        )

    @on(Input.Submitted)
    def handle_command(self, event: Input.Submitted) -> None:
        raw = event.value.strip()
        self.query_one(Input).clear()
        if raw:
            verb = raw.split(maxsplit=1)[0].lower()
            started = time.perf_counter_ns()
            self._dispatch(raw)
            self._refresh_panel()
            elapsed_ns = time.perf_counter_ns() - started
            log = self.query_one(RichLog)
            log.write(f"[dim]time: {format_elapsed_ns(elapsed_ns)}[/dim]")
            if verb not in ("/capture", "/session", "/quit", "/exit"):
                self._maybe_capture_frame(raw, elapsed_ns, log)

    def action_scroll_up(self) -> None:
        self._scroll_by(1)

    def action_scroll_down(self) -> None:
        self._scroll_by(-1)

    def action_page_up(self) -> None:
        self._scroll_by(self._page_size())

    def action_page_down(self) -> None:
        self._scroll_by(-self._page_size())

    def action_scroll_home(self) -> None:
        self.scroll_offset = 0
        self._refresh_panel()

    def _record_undo_state(self) -> None:
        self.undo_history.append(snapshot_stack(self.demo))
        self.redo_history.clear()

    def _can_undo(self) -> bool:
        return len(self.undo_history) > 0

    def _can_redo(self) -> bool:
        return len(self.redo_history) > 0

    def _undo(self) -> None:
        if not self._can_undo():
            raise ValueError("Nothing to undo")
        self.redo_history.append(snapshot_stack(self.demo))
        self.demo = restore_stack(self.undo_history.pop(), self.demo.max_size)
        self.scroll_offset = 0

    def _redo(self) -> None:
        if not self._can_redo():
            raise ValueError("Nothing to redo")
        self.undo_history.append(snapshot_stack(self.demo))
        self.demo = restore_stack(self.redo_history.pop(), self.demo.max_size)
        self.scroll_offset = 0

    def _dispatch(self, raw: str) -> None:
        log = self.query_one(RichLog)
        parts = raw.split(maxsplit=1)
        verb = parts[0].lower()
        arg = parts[1].strip() if len(parts) > 1 else None

        if verb == "/push":
            if arg is None:
                log.write("[red]Usage: /push <value> [more values ...][/red]")
                return
            try:
                self._record_undo_state()
                pushed = self.demo.push_many(parse_push_values(arg))
                self.scroll_offset = 0
                stack_view = list(reversed(self.demo.stack))
                added_text = format_value_batch(pushed)
                log.write(
                    f"[green]push({len(pushed)} values) added {added_text}  "
                    f"stack top → bottom: {stack_view!r}  size={self.demo.size()}[/green]"
                )
            except OverflowError as e:
                log.write(f"[red]Overflow: {e}[/red]")
            except TypeError as e:
                log.write(f"[red]TypeError: {e}[/red]")
            except ValueError as e:
                log.write(f"[red]{e}[/red]")

        elif verb == "/random":
            if arg is None:
                log.write("[red]Usage: /random <positive-count>[/red]")
                return
            try:
                count = positive_int(arg)
                actual_count = min(count, self.demo.remaining_capacity())
                if actual_count == 0:
                    log.write("[yellow]Stack is already full; no random values pushed.[/yellow]")
                    return
                values = build_random_values(
                    count=actual_count,
                    element_type=self.demo.element_type,
                    words=self.words,
                    rng=self.random,
                    int_min=self.int_min,
                    int_max=self.int_max,
                    float_min=self.float_min,
                    float_max=self.float_max,
                )
                self._record_undo_state()
                pushed = self.demo.push_many(values)
                self.scroll_offset = 0
                if actual_count < count:
                    log.write(
                        f"[yellow]random({count}) truncated to {actual_count} due to remaining capacity.[/yellow]"
                    )
                stack_view = list(reversed(self.demo.stack))
                pushed_text = format_value_batch(pushed)
                log.write(
                    f"[green]random({actual_count}) pushed {len(pushed)} values {pushed_text}  "
                    f"stack top → bottom: {stack_view!r}  size={self.demo.size()}[/green]"
                )
            except (argparse.ArgumentTypeError, ValueError) as e:
                log.write(f"[red]{e}[/red]")
            except TypeError as e:
                log.write(f"[red]TypeError: {e}[/red]")

        elif verb == "/pop":
            try:
                self._record_undo_state()
                val = self.demo.pop()
                self._clamp_scroll_offset()
                log.write(f"[green]pop() → {val!r}  size={self.demo.size()}[/green]")
            except IndexError as e:
                log.write(f"[red]Underflow: {e}[/red]")

        elif verb == "/peek":
            try:
                val = self.demo.peek()
                log.write(f"[cyan]peek() → {val!r}[/cyan]")
            except IndexError as e:
                log.write(f"[red]Underflow: {e}[/red]")

        elif verb == "/at":
            if arg is None:
                log.write("[red]Usage: /at <non-negative-index>[/red]")
                return
            try:
                index = nonnegative_int(arg)
                val = self.demo.at(index)
                log.write(f"[cyan]at({index}) → {val!r}[/cyan]")
            except (argparse.ArgumentTypeError, ValueError) as e:
                log.write(f"[red]{e}[/red]")
            except IndexError as e:
                log.write(f"[red]RangeError: {e}[/red]")

        elif verb == "/clear":
            self._record_undo_state()
            previous_size = self.demo.size()
            self.demo.clear()
            self.scroll_offset = 0
            log.write(f"[green]clear() removed {previous_size} values  size={self.demo.size()}[/green]")

        elif verb == "/session":
            try:
                session_name = parse_session_arg(arg)
                self.capture_session_name = session_name
                ensure_capture_session("stack", session_name, self.capture_dir)
                log.write(f"[green]session({session_name!r}) selected for future captures[/green]")
            except ValueError as e:
                log.write(f"[red]{e}[/red]")

        elif verb == "/capture":
            try:
                mode = parse_capture_mode(arg)
                if mode == "on":
                    ensure_capture_session("stack", self.capture_session_name, self.capture_dir)
                    self.capture_enabled = True
                    log.write(
                        f"[green]capture(on)[/green] "
                        f"[dim]session={self.capture_session_name!r}[/dim]"
                    )
                else:
                    self.capture_enabled = False
                    log.write(
                        f"[green]capture(off)[/green] "
                        f"[dim]session remains {self.capture_session_name!r}[/dim]"
                    )
            except ValueError as e:
                log.write(f"[red]{e}[/red]")

        elif verb == "/video":
            try:
                session_name, seconds_per_frame = parse_video_args(arg)
                session_name = session_name or self.capture_session_name
                output_path = render_capture_video(
                    "stack",
                    session_name,
                    seconds_per_frame,
                    capture_dir=self.capture_dir,
                    video_dir=self.video_dir,
                )
                log.write(
                    f"[green]video({session_name!r}) wrote {str(output_path)!r}[/green] "
                    f"[dim]captions default to commands; {seconds_per_frame:g}s per frame[/dim]"
                )
            except (ValueError, OSError, RuntimeError) as e:
                log.write(f"[red]Video failed: {e}[/red]")
            except Exception as e:
                log.write(f"[red]Video failed: {e}[/red]")

        elif verb == "/swap":
            try:
                self._record_undo_state()
                original_top = self.demo.stack[-1]
                original_next = self.demo.stack[-2]
                first, second = self.demo.swap()
                log.write(
                    "[green]swap()[/green] "
                    f"→ top two are now {first!r}, {second!r}  size={self.demo.size()}\n"
                    "[dim]"
                    f"Equivalent steps: a = pop()  # {original_top!r}; "
                    f"b = pop()  # {original_next!r}; "
                    "push(a); push(b)"
                    "[/dim]"
                )
            except IndexError as e:
                log.write(f"[red]Underflow: {e}[/red]")

        elif verb == "/rotate":
            try:
                self._record_undo_state()
                original_top = self.demo.stack[-1]
                original_second = self.demo.stack[-2]
                original_third = self.demo.stack[-3]
                rotated = self.demo.rotate()
                log.write(
                    "[green]rotate()[/green] "
                    f"→ top three are now {rotated!r}  size={self.demo.size()}\n"
                    "[dim]"
                    f"Equivalent steps: a = pop()  # {original_top!r}; "
                    f"b = pop()  # {original_second!r}; "
                    f"c = pop()  # {original_third!r}; "
                    "push(b); push(a); push(c)"
                    "[/dim]"
                )
            except IndexError as e:
                log.write(f"[red]Underflow: {e}[/red]")

        elif verb == "/dup":
            try:
                self._record_undo_state()
                duplicated = self.demo.dup()
                self.scroll_offset = 0
                log.write(
                    "[green]dup()[/green] "
                    f"→ duplicated {duplicated!r}  size={self.demo.size()}\n"
                    "[dim]"
                    f"Equivalent steps: a = peek()  # {duplicated!r}; push(a)"
                    "[/dim]"
                )
            except (IndexError, OverflowError) as e:
                label = "Overflow" if isinstance(e, OverflowError) else "Underflow"
                log.write(f"[red]{label}: {e}[/red]")

        elif verb == "/save":
            if arg is None:
                log.write("[red]Usage: /save <path>[/red]")
                return
            try:
                path = parse_single_path(arg, "save")
                save_session(path, self.demo)
                log.write(f"[green]save() wrote {self.demo.size()} values to {str(path)!r}[/green]")
            except (OSError, ValueError, TypeError) as e:
                log.write(f"[red]Save failed: {e}[/red]")

        elif verb == "/load":
            if arg is None:
                log.write("[red]Usage: /load <path>[/red]")
                return
            try:
                path = parse_single_path(arg, "load")
                type_name, items = load_session(path)
                self._record_undo_state()
                self.demo = restore_stack({"type": type_name, "items": items}, self.demo.max_size)
                self.scroll_offset = 0
                log.write(
                    f"[green]load() restored {len(items)} values from {str(path)!r}  size={self.demo.size()}[/green]"
                )
            except (OSError, ValueError, TypeError, OverflowError) as e:
                log.write(f"[red]Load failed: {e}[/red]")

        elif verb == "/undo":
            try:
                self._undo()
                stack_view = list(reversed(self.demo.stack))
                type_name = get_type_name(self.demo.element_type)
                log.write(
                    f"[green]undo() restored previous state  "
                    f"type={type_name}  stack top → bottom: {stack_view!r}  size={self.demo.size()}[/green]"
                )
            except ValueError as e:
                log.write(f"[yellow]{e}[/yellow]")

        elif verb == "/redo":
            try:
                self._redo()
                stack_view = list(reversed(self.demo.stack))
                type_name = get_type_name(self.demo.element_type)
                log.write(
                    f"[green]redo() restored next state  "
                    f"type={type_name}  stack top → bottom: {stack_view!r}  size={self.demo.size()}[/green]"
                )
            except ValueError as e:
                log.write(f"[yellow]{e}[/yellow]")

        elif verb in ("/show", "/print"):
            if self.demo.is_empty():
                log.write("[yellow]Stack is empty.[/yellow]")
            else:
                items = list(reversed(self.demo.stack))
                log.write(f"[cyan]top → bottom: {items}[/cyan]")

        elif verb == "/up":
            self._scroll_by(1)

        elif verb == "/down":
            self._scroll_by(-1)

        elif verb == "/pageup":
            self._scroll_by(self._page_size())

        elif verb == "/pagedown":
            self._scroll_by(-self._page_size())

        elif verb == "/home":
            self.scroll_offset = 0
            log.write("[cyan]View reset to newest visible window.[/cyan]")

        elif verb == "/type":
            if arg is None:
                label = get_type_name(self.demo.element_type)
                log.write(f"[cyan]Current type constraint: {label}[/cyan]")
            else:
                try:
                    self._record_undo_state()
                    self.demo.set_type(arg.lower())
                    label = get_type_name(self.demo.element_type)
                    log.write(f"[green]Type constraint set to: {label}[/green]")
                except ValueError as e:
                    log.write(f"[red]{e}[/red]")

        elif verb in ("/quit", "/exit"):
            self.exit()

        elif verb == "/help":
            log.write(
                "[bold]Commands[/bold]\n"
                "  [cyan]/push <value> [more ...][/cyan]    push one or more values onto the stack\n"
                "  [cyan]/random <n>[/cyan]                 push n random values for the current type\n"
                "  [cyan]/pop[/cyan]                        pop the top value\n"
                "  [cyan]/peek[/cyan]                       inspect the top value\n"
                "  [cyan]/at <index>[/cyan]                 inspect 0,1,2,... relative to the top\n"
                "  [cyan]/dup[/cyan]                        duplicate the top value\n"
                "  [cyan]/swap[/cyan]                       swap the top two values\n"
                "  [cyan]/rotate[/cyan]                     rotate the top three values\n"
                "  [cyan]/clear[/cyan]                      remove all values from the stack\n"
                "  [cyan]/session <name>[/cyan]              set the session name for future captured frames\n"
                "  [cyan]/capture [on|off][/cyan]            enable or suspend frame capture for the active session\n"
                "  [cyan]/video [session] [seconds][/cyan]  build an mp4 from captured frames; defaults to current session and 5s\n"
                "  [cyan]/save <path>[/cyan]                save the current type and stack contents\n"
                "  [cyan]/load <path>[/cyan]                load a saved session into a fresh stack\n"
                "  [cyan]/undo[/cyan]                       restore the previous stack/type state\n"
                "  [cyan]/redo[/cyan]                       restore the next undone stack/type state\n"
                "  [cyan]/show[/cyan]  [cyan]/print[/cyan]                display stack contents\n"
                "  [cyan]/up[/cyan]  [cyan]/down[/cyan]                  scroll older/newer items\n"
                "  [cyan]/pageup[/cyan]  [cyan]/pagedown[/cyan]          page through older/newer items\n"
                "  [cyan]/home[/cyan]                       jump back to the newest visible window\n"
                "  [cyan]/type [int|float|str|bool|any][/cyan]  get or set element type constraint\n"
                "  [cyan]bool values[/cyan]                 true/false, yes/no, on/off, 1/0\n"
                "  [cyan]/help[/cyan]                       show this help\n"
                "  [cyan]/quit[/cyan]  [cyan]Ctrl+D[/cyan]                exit"
            )

        else:
            log.write(f"[red]Unknown command: {verb!r} — type /help[/red]")

    def _page_size(self) -> int:
        if self.view_top is None:
            return 1
        return max(self.view_top - 1, 1)

    def _can_scroll(self) -> bool:
        return self.view_top is not None and self.demo.size() > self.view_top

    def _clamp_scroll_offset(self) -> None:
        self.scroll_offset = clamp_scroll_offset(
            self.demo.size(),
            self.view_top,
            self.scroll_offset,
        )

    def _scroll_by(self, delta: int) -> None:
        if not self._can_scroll():
            return
        self.scroll_offset += delta
        self._clamp_scroll_offset()
        self._refresh_panel()

    def _refresh_panel(self) -> None:
        self._clamp_scroll_offset()
        self.query_one(StackPanel).refresh_stack(
            self.demo,
            view_top=self.view_top,
            scroll_offset=self.scroll_offset,
        )

    def _maybe_capture_frame(self, raw: str, elapsed_ns: int, log: RichLog) -> None:
        if not self.capture_enabled or not self.capture_session_name:
            return
        try:
            text_path, png_path, _ = next_frame_paths("stack", self.capture_session_name, self.capture_dir)
            text_path.write_text(self._capture_frame_text(), encoding="utf-8")
            render_text_frame_image(text_path, png_path)
            append_capture_frame(
                "stack",
                self.capture_session_name,
                command=raw,
                elapsed_ns=elapsed_ns,
                screenshot_path=text_path,
                capture_dir=self.capture_dir,
            )
            log.write(
                f"[dim]captured frame for session {self.capture_session_name!r}: {png_path.name}[/dim]"
            )
        except Exception as e:
            log.write(f"[red]Capture failed: {e}[/red]")

    def _capture_frame_text(self) -> str:
        panel = self.query_one(StackPanel)
        log = self.query_one(RichLog)
        recent_lines = [line.text for line in log.lines[-8:]]
        sections = [
            "STACK TUI CAPTURE",
            "",
            panel.content,
            "",
            "Recent log:",
            *recent_lines,
        ]
        return "\n".join(sections)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Interactive Stack Demo")
    parser.add_argument(
        "--max-size", type=int, default=1000, metavar="N",
        help="Maximum stack capacity (default: 1000)",
    )
    parser.add_argument(
        "--view-top",
        type=positive_int,
        default=8,
        metavar="N",
        help="Show at most N stack elements while keeping the top visible (default: 8)",
    )
    parser.add_argument(
        "--int-min",
        type=int,
        default=INT32_MIN,
        metavar="N",
        help=f"Minimum random integer for /random under int or any (default: {INT32_MIN})",
    )
    parser.add_argument(
        "--int-max",
        type=int,
        default=INT32_MAX,
        metavar="N",
        help=f"Maximum random integer for /random under int or any (default: {INT32_MAX})",
    )
    parser.add_argument(
        "--float-min",
        type=float,
        default=FLOAT32_MIN,
        metavar="X",
        help=f"Minimum random float for /random under float or any (default: {FLOAT32_MIN})",
    )
    parser.add_argument(
        "--float-max",
        type=float,
        default=FLOAT32_MAX,
        metavar="X",
        help=f"Maximum random float for /random under float or any (default: {FLOAT32_MAX})",
    )
    parser.add_argument(
        "--capture-dir",
        type=Path,
        default=Path.cwd() / ".capture",
        metavar="PATH",
        help="Directory for captured frame sessions (default: ./.capture)",
    )
    parser.add_argument(
        "--video-dir",
        type=Path,
        default=Path.cwd() / ".video",
        metavar="PATH",
        help="Directory for rendered videos (default: ./.video)",
    )
    return parser


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
        capture_dir=args.capture_dir,
        video_dir=args.video_dir,
    ).run()


if __name__ == "__main__":
    main()
