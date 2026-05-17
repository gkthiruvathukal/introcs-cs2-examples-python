import argparse

from textual.app import ComposeResult
from textual.widgets import Footer, Header, Input, RichLog

from data_structures.deque_demo import DequeDemo
from data_structures.tui_common import (
    BaseLinearStructureTUI,
    LinearPanel,
    build_linear_view,
    build_linear_parser,
    format_display_value,
    format_value_batch,
    get_type_name,
    nonnegative_int,
    parse_value_tokens,
)


class DequePanel(LinearPanel):
    def refresh_deque(self, *, header: str, items, view_top=None, scroll_offset: int = 0) -> None:
        view = build_linear_view(items, view_top=view_top, scroll_offset=scroll_offset)
        visible_items = view["visible_items"]

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

        front_labels = [self._format_front_label(index, view["item_count"]) for index in view["visible_indices"]]
        back_labels = [self._format_back_label(index, view["item_count"]) for index in view["visible_indices"]]
        rendered_values = [format_display_value(item) for item in visible_items]
        type_labels = [type(item).__name__ for item in visible_items]

        front_width = max(len("from front"), max(len(label) for label in front_labels))
        back_width = max(len("from back"), max(len(label) for label in back_labels))
        value_width = max(len("value"), max(len(rendered) for rendered in rendered_values), 5)
        type_width = max(len("type"), max(len(type_label) for type_label in type_labels))

        lines = []
        if view["hidden_before"] > 0:
            lines.append(f"  ... {view['hidden_before']} hidden near front ...")

        lines.append(
            f"  ┌{'─' * (front_width + 2)}┬{'─' * (back_width + 2)}┬{'─' * (value_width + 2)}┬{'─' * (type_width + 2)}┐"
        )
        lines.append(
            f"  │ {'from front':<{front_width}} │ {'from back':<{back_width}} │ {'value':^{value_width}} │ {'type':<{type_width}} │"
        )
        lines.append(
            f"  ├{'─' * (front_width + 2)}┼{'─' * (back_width + 2)}┼{'─' * (value_width + 2)}┼{'─' * (type_width + 2)}┤"
        )
        for front_label, back_label, rendered_value, type_label in zip(front_labels, back_labels, rendered_values, type_labels):
            lines.append(
                f"  │ {front_label:<{front_width}} │ {back_label:<{back_width}} │ {rendered_value:^{value_width}} │ {type_label:<{type_width}} │"
            )
        lines.append(
            f"  └{'─' * (front_width + 2)}┴{'─' * (back_width + 2)}┴{'─' * (value_width + 2)}┴{'─' * (type_width + 2)}┘"
        )

        if view["hidden_after"] > 0:
            lines.append(f"  ... {view['hidden_after']} hidden near back ...")

        self.update(rendered_header + "\n" + "\n".join(lines))

    @staticmethod
    def _format_front_label(index: int, item_count: int) -> str:
        if item_count == 1:
            return "front=back"
        if index == 0:
            return "front"
        if index == item_count - 1:
            return "back"
        return f"front+{index}"

    @staticmethod
    def _format_back_label(index: int, item_count: int) -> str:
        if item_count == 1:
            return "back=front"
        displacement = item_count - 1 - index
        if displacement == 0:
            return "back"
        if index == 0:
            return "front"
        return f"back+{displacement}"


class DequeDemoTUI(BaseLinearStructureTUI):
    STRUCTURE_NAME = "Deque"
    START_LABEL = "front"
    END_LABEL = "back"

    def __init__(self, **kwargs):
        self.demo = DequeDemo()
        super().__init__(**kwargs)

    def compose(self) -> ComposeResult:
        yield Header()
        yield DequePanel(id="panel")
        yield RichLog(id="log", highlight=True, markup=True)
        yield Input(placeholder=self.placeholder_text())
        yield Footer()

    def get_items(self) -> list:
        return self.demo.to_list()

    def append_values(self, values) -> None:
        if self.structure_size() + len(values) > self.max_size:
            raise OverflowError(f"Deque overflow: capacity is {self.max_size}")
        for value in values:
            self.demo.add_to_back(value)

    def prepend_values(self, values) -> None:
        if self.structure_size() + len(values) > self.max_size:
            raise OverflowError(f"Deque overflow: capacity is {self.max_size}")
        for value in reversed(values):
            self.demo.add_to_front(value)

    def clear_structure(self) -> None:
        self.demo.clear()

    def replace_items(self, items) -> None:
        self.demo = DequeDemo()
        self.append_values(self._convert_many(items))

    def show_state_text(self) -> str:
        return f"front → back: {self.get_items()!r}"

    def placeholder_text(self) -> str:
        return "/help  /push-front <v...>  /push-back <v...>  /random <n>  /pop-front  /pop-back  /peek-front  /peek-back  /at <index>  /clear  /save <file>  /load <file>  /undo  /redo  /type [int|float|str|bool|any]  /quit"

    def help_lines(self) -> list[str]:
        return [
            "  [cyan]/push-front <value> [more ...][/cyan]  add one or more values at the front",
            "  [cyan]/push-back <value> [more ...][/cyan]   add one or more values at the back",
            "  [cyan]/pop-front[/cyan]                   remove the front value",
            "  [cyan]/pop-back[/cyan]                    remove the back value",
            "  [cyan]/peek-front[/cyan]                  inspect the front value",
            "  [cyan]/peek-back[/cyan]                   inspect the back value",
            "  [cyan]/set-front <value>[/cyan]           replace the front value",
            "  [cyan]/set-back <value>[/cyan]            replace the back value",
            "  [cyan]/at <index>[/cyan]                  inspect 0,1,2,... relative to the front",
        ]

    def handle_structure_command(self, verb: str, arg: str | None, log: RichLog) -> bool:
        if verb in {"/push-front", "/push-back"}:
            if arg is None:
                log.write(f"[red]Usage: {verb} <value> [more values ...][/red]")
                return True
            try:
                self._record_undo_state()
                values = self._convert_many(parse_value_tokens(arg, f"Usage: {verb} <value> [more values ...]"))
                if verb == "/push-front":
                    self.prepend_values(values)
                else:
                    self.append_values(values)
                self.scroll_offset = 0
                log.write(
                    f"[green]{verb[1:]}({len(values)} values) added {format_value_batch(values)}  "
                    f"{self.show_state_text()}  size={self.structure_size()}[/green]"
                )
            except (OverflowError, TypeError, ValueError) as e:
                label = "Overflow" if isinstance(e, OverflowError) else "TypeError" if isinstance(e, TypeError) else None
                log.write(f"[red]{f'{label}: ' if label else ''}{e}[/red]")
            return True

        if verb in {"/pop-front", "/pop-back"}:
            try:
                self._record_undo_state()
                value = self.demo.remove_from_front() if verb == "/pop-front" else self.demo.remove_from_back()
                self._clamp_scroll_offset()
                log.write(f"[green]{verb[1:]}() → {value!r}  size={self.structure_size()}[/green]")
            except IndexError as e:
                log.write(f"[red]Underflow: {e}[/red]")
            return True

        if verb in {"/peek-front", "/peek-back"}:
            try:
                value = self.demo.peek_front() if verb == "/peek-front" else self.demo.peek_back()
                log.write(f"[cyan]{verb[1:]}() → {value!r}[/cyan]")
            except IndexError as e:
                log.write(f"[red]Underflow: {e}[/red]")
            return True

        if verb in {"/set-front", "/set-back"}:
            if arg is None:
                log.write(f"[red]Usage: {verb} <value>[/red]")
                return True
            try:
                values = parse_value_tokens(arg, f"Usage: {verb} <value>", min_count=1, max_count=1)
                value = self._convert_many(values)[0]
                self._record_undo_state()
                if verb == "/set-front":
                    self.demo.update_front(value)
                else:
                    self.demo.update_back(value)
                log.write(f"[green]{verb[1:]}() → {value!r}  {self.show_state_text()}  size={self.structure_size()}[/green]")
            except (IndexError, TypeError, ValueError) as e:
                label = "Underflow" if isinstance(e, IndexError) else "TypeError" if isinstance(e, TypeError) else None
                log.write(f"[red]{f'{label}: ' if label else ''}{e}[/red]")
            return True

        if verb == "/at":
            if arg is None:
                log.write("[red]Usage: /at <non-negative-index>[/red]")
                return True
            try:
                index = nonnegative_int(arg)
                log.write(f"[cyan]at({index}) → {self.demo.at(index)!r}[/cyan]")
            except (argparse.ArgumentTypeError, ValueError) as e:
                log.write(f"[red]{e}[/red]")
            except IndexError as e:
                log.write(f"[red]RangeError: {e}[/red]")
            return True

        return False

    def _refresh_panel(self) -> None:
        self._clamp_scroll_offset()
        header = f"{self.STRUCTURE_NAME} ({self.structure_size()}/{self.max_size})  type: {get_type_name(self.element_type)}"
        self.query_one(DequePanel).refresh_deque(
            header=header,
            items=self.get_items(),
            view_top=self.view_top,
            scroll_offset=self.scroll_offset,
        )


def main() -> None:
    parser = build_linear_parser("Interactive Deque Demo")
    args = parser.parse_args()
    if args.int_min > args.int_max:
        parser.error("--int-min must be less than or equal to --int-max")
    if args.float_min > args.float_max:
        parser.error("--float-min must be less than or equal to --float-max")
    DequeDemoTUI(
        max_size=args.max_size,
        view_top=args.view_top,
        int_min=args.int_min,
        int_max=args.int_max,
        float_min=args.float_min,
        float_max=args.float_max,
    ).run()


if __name__ == "__main__":
    main()
