import argparse

from textual.widgets import RichLog

from data_structures.list_demo import ListDemo
from data_structures.tui_common import (
    BaseLinearStructureTUI,
    build_linear_parser,
    format_value_batch,
    nonnegative_int,
    parse_value_tokens,
)


class ListDemoTUI(BaseLinearStructureTUI):
    STRUCTURE_NAME = "List"
    START_LABEL = "first"
    END_LABEL = "last"

    def __init__(self, **kwargs):
        self.demo = ListDemo()
        super().__init__(**kwargs)

    def get_items(self) -> list:
        return self.demo.to_list()

    def append_values(self, values) -> None:
        if self.structure_size() + len(values) > self.max_size:
            raise OverflowError(f"List overflow: capacity is {self.max_size}")
        for value in values:
            self.demo.add(value)

    def clear_structure(self) -> None:
        self.demo.clear()

    def replace_items(self, items) -> None:
        self.demo = ListDemo()
        self.append_values(self._convert_many(items))

    def show_state_text(self) -> str:
        return f"index → value: {list(enumerate(self.get_items()))!r}"

    def placeholder_text(self) -> str:
        return "/help  /append VALUE  /insert INDEX VALUE  /remove-value VALUE  /remove-at INDEX  /search VALUE  /get INDEX  /set INDEX VALUE  /quit"

    def format_position_label(self, index: int, item_count: int, start_label: str, end_label: str) -> str:
        return str(index)

    def help_lines(self) -> list[str]:
        return [
            "  [cyan]/append[/cyan] VALUE [VALUE ...]     add one or more values at the end",
            "  [cyan]/insert[/cyan] INDEX VALUE           insert one value at the given index",
            "  [cyan]/remove-value[/cyan] VALUE           remove the first matching value",
            "  [cyan]/remove-at[/cyan] INDEX              remove the value at the given index",
            "  [cyan]/search[/cyan] VALUE                 search for a value",
            "  [cyan]/get[/cyan] INDEX                    inspect the value at the given index",
            "  [cyan]/set[/cyan] INDEX VALUE              replace the value at the given index",
        ]

    def handle_structure_command(self, verb: str, arg: str | None, log: RichLog) -> bool:
        if verb == "/append":
            if arg is None:
                log.write("[red]Usage: /append <value> [more values ...][/red]")
                return True
            try:
                self._record_undo_state()
                values = self._convert_many(parse_value_tokens(arg, "Usage: /append <value> [more values ...]"))
                self.append_values(values)
                self.scroll_offset = 0
                log.write(
                    f"[green]append({len(values)} values) added {format_value_batch(values)}  "
                    f"{self.show_state_text()}  size={self.structure_size()}[/green]"
                )
            except (OverflowError, TypeError, ValueError) as e:
                label = "Overflow" if isinstance(e, OverflowError) else "TypeError" if isinstance(e, TypeError) else None
                log.write(f"[red]{f'{label}: ' if label else ''}{e}[/red]")
            return True

        if verb == "/insert":
            if arg is None:
                log.write("[red]Usage: /insert <index> <value>[/red]")
                return True
            try:
                tokens = parse_value_tokens(arg, "Usage: /insert <index> <value>", min_count=2, max_count=2)
                index = nonnegative_int(tokens[0])
                value = self._convert_many([tokens[1]])[0]
                if self.structure_size() + 1 > self.max_size:
                    raise OverflowError(f"List overflow: capacity is {self.max_size}")
                self._record_undo_state()
                self.demo.insert(index, value)
                self.scroll_offset = 0
                log.write(f"[green]insert({index}, {value!r})  {self.show_state_text()}  size={self.structure_size()}[/green]")
            except (argparse.ArgumentTypeError, ValueError, TypeError, OverflowError, IndexError) as e:
                label = "Overflow" if isinstance(e, OverflowError) else "TypeError" if isinstance(e, TypeError) else None
                log.write(f"[red]{f'{label}: ' if label else ''}{e}[/red]")
            return True

        if verb == "/remove-value":
            if arg is None:
                log.write("[red]Usage: /remove-value <value>[/red]")
                return True
            try:
                tokens = parse_value_tokens(arg, "Usage: /remove-value <value>", min_count=1, max_count=1)
                value = self._convert_many(tokens)[0]
                self._record_undo_state()
                self.demo.remove(value)
                log.write(f"[green]remove-value({value!r})  {self.show_state_text()}  size={self.structure_size()}[/green]")
            except (ValueError, TypeError) as e:
                label = "TypeError" if isinstance(e, TypeError) else None
                log.write(f"[red]{f'{label}: ' if label else ''}{e}[/red]")
            return True

        if verb == "/remove-at":
            if arg is None:
                log.write("[red]Usage: /remove-at <index>[/red]")
                return True
            try:
                index = nonnegative_int(arg)
                self._record_undo_state()
                value = self.demo.remove_at(index)
                self._clamp_scroll_offset()
                log.write(f"[green]remove-at({index}) → {value!r}  size={self.structure_size()}[/green]")
            except (argparse.ArgumentTypeError, ValueError) as e:
                log.write(f"[red]{e}[/red]")
            except IndexError as e:
                log.write(f"[red]RangeError: {e}[/red]")
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

        if verb in {"/get", "/at"}:
            if arg is None:
                log.write(f"[red]Usage: {verb} <index>[/red]")
                return True
            try:
                index = nonnegative_int(arg)
                log.write(f"[cyan]{verb[1:]}({index}) → {self.demo.get(index)!r}[/cyan]")
            except (argparse.ArgumentTypeError, ValueError) as e:
                log.write(f"[red]{e}[/red]")
            except IndexError as e:
                log.write(f"[red]RangeError: {e}[/red]")
            return True

        if verb == "/set":
            if arg is None:
                log.write("[red]Usage: /set <index> <value>[/red]")
                return True
            try:
                tokens = parse_value_tokens(arg, "Usage: /set <index> <value>", min_count=2, max_count=2)
                index = nonnegative_int(tokens[0])
                value = self._convert_many([tokens[1]])[0]
                self._record_undo_state()
                self.demo.update(index, value)
                log.write(f"[green]set({index}, {value!r})  {self.show_state_text()}  size={self.structure_size()}[/green]")
            except (argparse.ArgumentTypeError, ValueError, TypeError) as e:
                label = "TypeError" if isinstance(e, TypeError) else None
                log.write(f"[red]{f'{label}: ' if label else ''}{e}[/red]")
            except IndexError as e:
                log.write(f"[red]RangeError: {e}[/red]")
            return True

        return False


def main() -> None:
    parser = build_linear_parser("Interactive List Demo")
    args = parser.parse_args()
    if args.int_min > args.int_max:
        parser.error("--int-min must be less than or equal to --int-max")
    if args.float_min > args.float_max:
        parser.error("--float-min must be less than or equal to --float-max")
    ListDemoTUI(
        max_size=args.max_size,
        view_top=args.view_top,
        int_min=args.int_min,
        int_max=args.int_max,
        float_min=args.float_min,
        float_max=args.float_max,
    ).run()


if __name__ == "__main__":
    main()
