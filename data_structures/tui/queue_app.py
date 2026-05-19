from textual.widgets import RichLog

from data_structures.queue_demo import QueueDemo
from .common import (
    BaseLinearStructureTUI,
    build_linear_parser,
    format_value_batch,
    nonnegative_int,
    parse_value_tokens,
)


class QueueDemoTUI(BaseLinearStructureTUI):
    STRUCTURE_NAME = "Queue"
    START_LABEL = "front"
    END_LABEL = "back"

    def __init__(self, **kwargs):
        self.demo = QueueDemo()
        super().__init__(**kwargs)

    def get_items(self) -> list:
        return self.demo.to_list()

    def append_values(self, values) -> None:
        if self.structure_size() + len(values) > self.max_size:
            raise OverflowError(f"Queue overflow: capacity is {self.max_size}")
        for value in values:
            self.demo.enqueue(value)

    def clear_structure(self) -> None:
        self.demo.clear()

    def replace_items(self, items) -> None:
        self.demo = QueueDemo()
        self.append_values(self._convert_many(items))

    def show_state_text(self) -> str:
        return f"front → back: {self.get_items()!r}"

    def placeholder_text(self) -> str:
        return "/help  /enqueue VALUE  /dequeue  /peek  /search VALUE  /at INDEX  /swap  /rotate  /quit"

    def help_lines(self) -> list[str]:
        return [
            "  [cyan]/enqueue[/cyan] VALUE [VALUE ...]   add one or more values at the back",
            "  [cyan]/dequeue[/cyan]                     remove the front value",
            "  [cyan]/peek[/cyan]                        inspect the front value",
            "  [cyan]/search[/cyan] VALUE                search for a value",
            "  [cyan]/at[/cyan] INDEX                    inspect 0,1,2,... relative to the front",
            "  [cyan]/swap[/cyan]                        swap the front two values",
            "  [cyan]/rotate[/cyan]                      rotate the front three values",
        ]

    def handle_structure_command(self, verb: str, arg: str | None, log: RichLog) -> bool:
        if verb == "/enqueue":
            if arg is None:
                log.write("[red]Usage: /enqueue <value> [more values ...][/red]")
                return True
            try:
                self._record_undo_state()
                pushed = self._convert_many(parse_value_tokens(arg, "Usage: /enqueue <value> [more values ...]"))
                self.append_values(pushed)
                self.scroll_offset = 0
                log.write(
                    f"[green]enqueue({len(pushed)} values) added {format_value_batch(pushed)}  "
                    f"{self.show_state_text()}  size={self.structure_size()}[/green]"
                )
            except (OverflowError, TypeError, ValueError) as e:
                label = "Overflow" if isinstance(e, OverflowError) else "TypeError" if isinstance(e, TypeError) else None
                log.write(f"[red]{f'{label}: ' if label else ''}{e}[/red]")
            return True

        if verb == "/dequeue":
            try:
                self._record_undo_state()
                value = self.demo.dequeue()
                self._clamp_scroll_offset()
                log.write(f"[green]dequeue() → {value!r}  size={self.structure_size()}[/green]")
            except IndexError as e:
                log.write(f"[red]Underflow: {e}[/red]")
            return True

        if verb == "/peek":
            try:
                log.write(f"[cyan]peek() → {self.demo.peek()!r}[/cyan]")
            except IndexError as e:
                log.write(f"[red]Underflow: {e}[/red]")
            return True

        if verb == "/swap":
            try:
                self._record_undo_state()
                original_first = self.demo.queue[0]
                original_second = self.demo.queue[1]
                first, second = self.demo.swap()
                log.write(
                    "[green]swap()[/green] "
                    f"→ front two are now {first!r}, {second!r}  size={self.structure_size()}\n"
                    "[dim]"
                    f"Equivalent steps: a = dequeue()  # {original_first!r}; "
                    f"b = dequeue()  # {original_second!r}; "
                    "push_front(a, b) conceptually reorders them as b, a"
                    "[/dim]"
                )
            except IndexError as e:
                log.write(f"[red]Underflow: {e}[/red]")
            return True

        if verb == "/rotate":
            try:
                self._record_undo_state()
                original_first = self.demo.queue[0]
                original_second = self.demo.queue[1]
                original_third = self.demo.queue[2]
                rotated = self.demo.rotate()
                log.write(
                    "[green]rotate()[/green] "
                    f"→ front three are now {rotated!r}  size={self.structure_size()}\n"
                    "[dim]"
                    f"Equivalent steps: a = dequeue()  # {original_first!r}; "
                    f"b = dequeue()  # {original_second!r}; "
                    f"c = dequeue()  # {original_third!r}; "
                    "conceptually reinsert as c, a, b at the front"
                    "[/dim]"
                )
            except IndexError as e:
                log.write(f"[red]Underflow: {e}[/red]")
            return True

        if verb == "/search":
            if arg is None:
                log.write("[red]Usage: /search VALUE[/red]")
                return True
            try:
                value = self._convert_many(parse_value_tokens(arg, "Usage: /search VALUE", 1, 1))[0]
                result = self.demo.find(value)
                if result is None:
                    log.write(f"[cyan]search({value!r}) → not found[/cyan]")
                else:
                    log.write(f"[cyan]search({value!r}) → found at index {result}[/cyan]")
            except TypeError as e:
                log.write(f"[red]TypeError: {e}[/red]")
            return True

        if verb == "/at":
            if arg is None:
                log.write("[red]Usage: /at <non-negative-index>[/red]")
                return True
            try:
                index = nonnegative_int(arg)
                log.write(f"[cyan]at({index}) → {self.demo.at(index)!r}[/cyan]")
            except Exception as e:
                label = "RangeError" if isinstance(e, IndexError) else "Error"
                log.write(f"[red]{label}: {e}[/red]")
            return True

        return False


def main() -> None:
    parser = build_linear_parser("Interactive Queue Demo")
    args = parser.parse_args()
    if args.int_min > args.int_max:
        parser.error("--int-min must be less than or equal to --int-max")
    if args.float_min > args.float_max:
        parser.error("--float-min must be less than or equal to --float-max")
    QueueDemoTUI(
        max_size=args.max_size,
        view_top=args.view_top,
        int_min=args.int_min,
        int_max=args.int_max,
        float_min=args.float_min,
        float_max=args.float_max,
    ).run()


if __name__ == "__main__":
    main()
