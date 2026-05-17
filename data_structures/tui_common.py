import argparse
import json
import random
import shlex
import time
from pathlib import Path

from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Input, RichLog, Static

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


def parse_value_tokens(arg: str, usage: str, min_count: int = 1, max_count: int | None = None) -> list[str]:
    values = shlex.split(arg)
    if len(values) < min_count:
        raise ValueError(usage)
    if max_count is not None and len(values) > max_count:
        raise ValueError(usage)
    return values


def parse_single_path(arg: str, command_name: str) -> Path:
    parts = shlex.split(arg)
    if len(parts) != 1:
        raise ValueError(f"Usage: /{command_name} <path>")
    return Path(parts[0]).expanduser()


def load_words() -> list[str]:
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


def format_elapsed_ns(elapsed_ns: int) -> str:
    if elapsed_ns < 1_000:
        return f"{elapsed_ns} ns"
    if elapsed_ns < 1_000_000:
        return f"{elapsed_ns / 1_000:.1f} us"
    if elapsed_ns < 1_000_000_000:
        return f"{elapsed_ns / 1_000_000:.1f} ms"
    return f"{elapsed_ns / 1_000_000_000:.3f} s"


def save_session(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def load_session(path: Path, allowed_types: set[str]) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    type_name = payload.get("type", "any")
    items = payload.get("items")
    if type_name not in allowed_types:
        raise ValueError(f"Unsupported session type {type_name!r}")
    if not isinstance(items, list):
        raise ValueError("Session file is missing a valid item list")
    return {"type": type_name, "items": items}


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


def clamp_scroll_offset(item_count: int, view_top, scroll_offset: int) -> int:
    if view_top is None or item_count <= 2:
        return 0

    effective_view_top = max(view_top, 2)
    if item_count <= effective_view_top:
        return 0

    middle_count = item_count - 2
    middle_window_size = max(effective_view_top - 2, 0)
    if middle_window_size <= 0:
        return 0

    max_offset = middle_count - middle_window_size
    return min(max(scroll_offset, 0), max_offset)


def build_linear_view(items, view_top=None, scroll_offset: int = 0):
    ordered = list(items)
    effective_view_top = None if view_top is None else max(view_top, 2)

    if effective_view_top is None or len(ordered) <= effective_view_top:
        return {
            "visible_items": ordered,
            "visible_indices": list(range(len(ordered))),
            "hidden_before": 0,
            "hidden_after": 0,
            "scroll_offset": 0,
            "window_size": max(len(ordered) - 2, 0),
            "item_count": len(ordered),
        }

    if len(ordered) == 1:
        return {
            "visible_items": ordered[:1],
            "visible_indices": [0],
            "hidden_before": 0,
            "hidden_after": 0,
            "scroll_offset": 0,
            "window_size": 0,
            "item_count": 1,
        }

    middle_items = ordered[1:-1]
    window_size = max(effective_view_top - 2, 0)
    offset = clamp_scroll_offset(len(ordered), view_top, scroll_offset)
    visible_middle = middle_items[offset:offset + window_size]
    visible_indices = [0, *(offset + i + 1 for i in range(len(visible_middle))), len(ordered) - 1]

    return {
        "visible_items": [ordered[0], *visible_middle, ordered[-1]],
        "visible_indices": visible_indices,
        "hidden_before": offset,
        "hidden_after": max(len(middle_items) - (offset + len(visible_middle)), 0),
        "scroll_offset": offset,
        "window_size": window_size,
        "item_count": len(ordered),
    }


def default_position_label(index: int, item_count: int, start_label: str, end_label: str) -> str:
    if item_count == 1:
        return f"{start_label}={end_label}"
    if index == 0:
        return start_label
    if index == item_count - 1:
        return end_label
    return f"{start_label}+{index}"


class LinearPanel(Static):
    def refresh_linear(
        self,
        *,
        header: str,
        items,
        view_top=None,
        scroll_offset: int = 0,
        start_label: str,
        end_label: str,
        labeler=None,
    ) -> None:
        view = build_linear_view(items, view_top=view_top, scroll_offset=scroll_offset)
        visible_items = view["visible_items"]
        labeler = labeler or default_position_label

        rendered_header = header
        if view_top is not None:
            rendered_header += f"  view-top: {view_top}"

        middle_indices = [index for index in view["visible_indices"] if 0 < index < view["item_count"] - 1]
        if view["window_size"] > 0 or view["hidden_after"] > 0:
            total_middle = max(view["item_count"] - 2, 0)
            if not middle_indices:
                rendered_header += "  middle: none visible"
            else:
                rendered_header += f"  middle: {middle_indices[0]}-{middle_indices[-1]}/{total_middle}"

        if not visible_items:
            self.update(f"{rendered_header}\n  (empty)")
            return

        labels = [labeler(index, view["item_count"], start_label, end_label) for index in view["visible_indices"]]
        rendered_values = [format_display_value(item) for item in visible_items]
        type_labels = [type(item).__name__ for item in visible_items]

        label_width = max(len("position"), max(len(label) for label in labels))
        value_width = max(len("value"), max(len(rendered) for rendered in rendered_values), 5)
        type_width = max(len("type"), max(len(type_label) for type_label in type_labels))

        lines = []
        if view["hidden_before"] > 0:
            lines.append(f"  ... {view['hidden_before']} hidden near {start_label} ...")

        lines.append(
            f"  ┌{'─' * (label_width + 2)}┬{'─' * (value_width + 2)}┬{'─' * (type_width + 2)}┐"
        )
        lines.append(
            f"  │ {'position':<{label_width}} │ {'value':^{value_width}} │ {'type':<{type_width}} │"
        )
        lines.append(
            f"  ├{'─' * (label_width + 2)}┼{'─' * (value_width + 2)}┼{'─' * (type_width + 2)}┤"
        )
        for label, rendered_value, type_label in zip(labels, rendered_values, type_labels):
            lines.append(
                f"  │ {label:<{label_width}} │ {rendered_value:^{value_width}} │ {type_label:<{type_width}} │"
            )
        lines.append(
            f"  └{'─' * (label_width + 2)}┴{'─' * (value_width + 2)}┴{'─' * (type_width + 2)}┘"
        )

        if view["hidden_after"] > 0:
            lines.append(f"  ... {view['hidden_after']} hidden near {end_label} ...")

        self.update(rendered_header + "\n" + "\n".join(lines))


class BaseLinearStructureTUI(App):
    CSS = """
    LinearPanel {
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
        ("up", "scroll_up", "Forward"),
        ("down", "scroll_down", "Backward"),
        ("pageup", "page_up", "Page forward"),
        ("pagedown", "page_down", "Page backward"),
        ("home", "scroll_home", "Newest"),
    ]

    STRUCTURE_NAME = "Structure"
    START_LABEL = "start"
    END_LABEL = "end"
    DEFAULT_TYPE = "int"
    ENABLE_RANDOM = True
    SUPPORTED_TYPES = {"int": int, "float": float, "str": str, "bool": parse_bool}

    def __init__(
        self,
        *,
        max_size: int = 1000,
        view_top: int = 8,
        int_min: int = INT32_MIN,
        int_max: int = INT32_MAX,
        float_min: float = FLOAT32_MIN,
        float_max: float = FLOAT32_MAX,
    ):
        super().__init__()
        self.max_size = max_size
        self.view_top = view_top
        self.scroll_offset = 0
        self.int_min = int_min
        self.int_max = int_max
        self.float_min = float_min
        self.float_max = float_max
        self.random = random.Random()
        self.words = load_words()
        self.undo_history = []
        self.redo_history = []
        self.element_type = None
        self.set_type(self.DEFAULT_TYPE)

    def compose(self) -> ComposeResult:
        yield Header()
        yield LinearPanel(id="panel")
        yield RichLog(id="log", highlight=True, markup=True)
        yield Input(placeholder=self.placeholder_text())
        yield Footer()

    def on_mount(self) -> None:
        self._refresh_panel()
        self.query_one(RichLog).write(
            f"[bold]{self.STRUCTURE_NAME} Demo[/bold] — type [cyan]/help[/cyan] for commands."
        )

    @on(Input.Submitted)
    def handle_command(self, event: Input.Submitted) -> None:
        raw = event.value.strip()
        self.query_one(Input).clear()
        if raw:
            started = time.perf_counter_ns()
            self._dispatch(raw)
            self._refresh_panel()
            elapsed_ns = time.perf_counter_ns() - started
            self.query_one(RichLog).write(f"[dim]time: {format_elapsed_ns(elapsed_ns)}[/dim]")

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

    def set_type(self, type_name: str) -> None:
        if type_name in ("any", ""):
            self.element_type = None
        elif type_name in self.SUPPORTED_TYPES:
            self.element_type = self.SUPPORTED_TYPES[type_name]
        else:
            raise ValueError(f"Unknown type '{type_name}'. Use: int, float, str, bool, any")

    def get_items(self) -> list:
        raise NotImplementedError

    def append_values(self, values) -> None:
        raise NotImplementedError

    def clear_structure(self) -> None:
        raise NotImplementedError

    def replace_items(self, items) -> None:
        raise NotImplementedError

    def handle_structure_command(self, verb: str, arg: str | None, log: RichLog) -> bool:
        return False

    def help_lines(self) -> list[str]:
        return []

    def show_state_text(self) -> str:
        return repr(self.get_items())

    def placeholder_text(self) -> str:
        return "/help"

    def format_position_label(self, index: int, item_count: int, start_label: str, end_label: str) -> str:
        return default_position_label(index, item_count, start_label, end_label)

    def structure_size(self) -> int:
        return len(self.get_items())

    def is_empty(self) -> bool:
        return self.structure_size() == 0

    def remaining_capacity(self) -> int:
        return self.max_size - self.structure_size()

    def _convert_item(self, item):
        if self.element_type is None:
            return item
        try:
            return self.element_type(item)
        except (ValueError, TypeError):
            raise TypeError(f"Cannot convert {item!r} to {self.element_type.__name__}")

    def _convert_many(self, items):
        return [self._convert_item(item) for item in items]

    def _snapshot_state(self) -> dict:
        return {
            "type": get_type_name(self.element_type),
            "items": list(self.get_items()),
        }

    def _restore_snapshot(self, snapshot: dict) -> None:
        self.set_type(snapshot["type"])
        self.replace_items(snapshot["items"])
        self.scroll_offset = 0

    def _record_undo_state(self) -> None:
        self.undo_history.append(self._snapshot_state())
        self.redo_history.clear()

    def _undo(self) -> None:
        if not self.undo_history:
            raise ValueError("Nothing to undo")
        self.redo_history.append(self._snapshot_state())
        self._restore_snapshot(self.undo_history.pop())

    def _redo(self) -> None:
        if not self.redo_history:
            raise ValueError("Nothing to redo")
        self.undo_history.append(self._snapshot_state())
        self._restore_snapshot(self.redo_history.pop())

    def _page_size(self) -> int:
        if self.view_top is None:
            return 1
        return max(self.view_top - 1, 1)

    def _can_scroll(self) -> bool:
        return self.view_top is not None and self.structure_size() > self.view_top

    def _clamp_scroll_offset(self) -> None:
        self.scroll_offset = clamp_scroll_offset(self.structure_size(), self.view_top, self.scroll_offset)

    def _scroll_by(self, delta: int) -> None:
        if not self._can_scroll():
            return
        self.scroll_offset += delta
        self._clamp_scroll_offset()
        self._refresh_panel()

    def _refresh_panel(self) -> None:
        self._clamp_scroll_offset()
        header = f"{self.STRUCTURE_NAME} ({self.structure_size()}/{self.max_size})  type: {get_type_name(self.element_type)}"
        self.query_one(LinearPanel).refresh_linear(
            header=header,
            items=self.get_items(),
            view_top=self.view_top,
            scroll_offset=self.scroll_offset,
            start_label=self.START_LABEL,
            end_label=self.END_LABEL,
            labeler=self.format_position_label,
        )

    def _dispatch(self, raw: str) -> None:
        log = self.query_one(RichLog)
        parts = raw.split(maxsplit=1)
        verb = parts[0].lower()
        arg = parts[1].strip() if len(parts) > 1 else None

        if self.handle_structure_command(verb, arg, log):
            return

        if verb == "/random" and self.ENABLE_RANDOM:
            if arg is None:
                log.write("[red]Usage: /random <positive-count>[/red]")
                return
            try:
                count = positive_int(arg)
                actual_count = min(count, self.remaining_capacity())
                if actual_count == 0:
                    log.write(f"[yellow]{self.STRUCTURE_NAME} is already full; no random values pushed.[/yellow]")
                    return
                values = build_random_values(
                    count=actual_count,
                    element_type=self.element_type,
                    words=self.words,
                    rng=self.random,
                    int_min=self.int_min,
                    int_max=self.int_max,
                    float_min=self.float_min,
                    float_max=self.float_max,
                )
                self._record_undo_state()
                self.append_values(values)
                self.scroll_offset = 0
                if actual_count < count:
                    log.write(
                        f"[yellow]random({count}) truncated to {actual_count} due to remaining capacity.[/yellow]"
                    )
                log.write(
                    f"[green]random({actual_count}) pushed {len(values)} values {format_value_batch(values)}  "
                    f"{self.show_state_text()}  size={self.structure_size()}[/green]"
                )
            except (argparse.ArgumentTypeError, ValueError) as e:
                log.write(f"[red]{e}[/red]")
            except (OverflowError, TypeError) as e:
                label = "Overflow" if isinstance(e, OverflowError) else "TypeError"
                log.write(f"[red]{label}: {e}[/red]")

        elif verb == "/clear":
            self._record_undo_state()
            previous_size = self.structure_size()
            self.clear_structure()
            self.scroll_offset = 0
            log.write(f"[green]clear() removed {previous_size} values  size={self.structure_size()}[/green]")

        elif verb == "/save":
            if arg is None:
                log.write("[red]Usage: /save <path>[/red]")
                return
            try:
                path = parse_single_path(arg, "save")
                save_session(path, self._snapshot_state())
                log.write(f"[green]save() wrote {self.structure_size()} values to {str(path)!r}[/green]")
            except (OSError, ValueError, TypeError) as e:
                log.write(f"[red]Save failed: {e}[/red]")

        elif verb == "/load":
            if arg is None:
                log.write("[red]Usage: /load <path>[/red]")
                return
            try:
                path = parse_single_path(arg, "load")
                snapshot = load_session(path, {"any", "int", "float", "str", "bool"})
                self._record_undo_state()
                self._restore_snapshot(snapshot)
                log.write(
                    f"[green]load() restored {len(snapshot['items'])} values from {str(path)!r}  size={self.structure_size()}[/green]"
                )
            except (OSError, ValueError, TypeError, OverflowError) as e:
                log.write(f"[red]Load failed: {e}[/red]")

        elif verb == "/undo":
            try:
                self._undo()
                log.write(
                    f"[green]undo() restored previous state  "
                    f"type={get_type_name(self.element_type)}  {self.show_state_text()}  size={self.structure_size()}[/green]"
                )
            except ValueError as e:
                log.write(f"[yellow]{e}[/yellow]")

        elif verb == "/redo":
            try:
                self._redo()
                log.write(
                    f"[green]redo() restored next state  "
                    f"type={get_type_name(self.element_type)}  {self.show_state_text()}  size={self.structure_size()}[/green]"
                )
            except ValueError as e:
                log.write(f"[yellow]{e}[/yellow]")

        elif verb in ("/show", "/print"):
            if self.is_empty():
                log.write(f"[yellow]{self.STRUCTURE_NAME} is empty.[/yellow]")
            else:
                log.write(f"[cyan]{self.show_state_text()}[/cyan]")

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
                log.write(f"[cyan]Current type constraint: {get_type_name(self.element_type)}[/cyan]")
            else:
                try:
                    self._record_undo_state()
                    self.set_type(arg.lower())
                    log.write(f"[green]Type constraint set to: {get_type_name(self.element_type)}[/green]")
                except ValueError as e:
                    log.write(f"[red]{e}[/red]")

        elif verb in ("/quit", "/exit"):
            self.exit()

        elif verb == "/help":
            lines = [
                "[bold]Commands[/bold]",
                *self.help_lines(),
            ]
            if self.ENABLE_RANDOM:
                lines.append("  [cyan]/random <n>[/cyan]                 append n random values for the current type")
            lines.extend(
                [
                    "  [cyan]/clear[/cyan]                      remove all values",
                    "  [cyan]/save <path>[/cyan]                save the current type and contents",
                    "  [cyan]/load <path>[/cyan]                load a saved session into a fresh structure",
                    "  [cyan]/undo[/cyan]                       restore the previous state",
                    "  [cyan]/redo[/cyan]                       restore the next undone state",
                    "  [cyan]/show[/cyan]  [cyan]/print[/cyan]                display current contents",
                    "  [cyan]/up[/cyan]  [cyan]/down[/cyan]                  scroll visible middle rows",
                    "  [cyan]/pageup[/cyan]  [cyan]/pagedown[/cyan]          page through middle rows",
                    "  [cyan]/home[/cyan]                       jump back to the newest visible window",
                    "  [cyan]/type [int|float|str|bool|any][/cyan]  get or set element type constraint",
                    "  [cyan]bool values[/cyan]                 true/false, yes/no, on/off, 1/0",
                    "  [cyan]/help[/cyan]                       show this help",
                    "  [cyan]/quit[/cyan]  [cyan]Ctrl+D[/cyan]                exit",
                ]
            )
            log.write("\n".join(lines))

        else:
            log.write(f"[red]Unknown command: {verb!r} — type /help[/red]")


def build_linear_parser(description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "--max-size", type=int, default=1000, metavar="N",
        help="Maximum structure capacity (default: 1000)",
    )
    parser.add_argument(
        "--view-top",
        type=positive_int,
        default=8,
        metavar="N",
        help="Show at most N visible rows while keeping both ends visible when possible (default: 8)",
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
    return parser
