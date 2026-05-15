import argparse

from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Input, RichLog, Static


class StackDemo:
    SUPPORTED_TYPES = {"int": int, "float": float, "str": str}

    def __init__(self, max_size=1000):
        self.stack = []
        self.max_size = max_size
        self.element_type = None

    def set_type(self, type_name):
        if type_name in ("any", ""):
            self.element_type = None
        elif type_name in self.SUPPORTED_TYPES:
            self.element_type = self.SUPPORTED_TYPES[type_name]
        else:
            raise ValueError(f"Unknown type '{type_name}'. Use: int, float, str, any")

    def push(self, item):
        if len(self.stack) >= self.max_size:
            raise OverflowError(f"Stack overflow: capacity is {self.max_size}")
        if self.element_type is not None:
            try:
                item = self.element_type(item)
            except (ValueError, TypeError):
                raise TypeError(f"Cannot convert {item!r} to {self.element_type.__name__}")
        self.stack.append(item)
        return item

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


class StackPanel(Static):
    def refresh_stack(self, demo: StackDemo) -> None:
        type_label = demo.element_type.__name__ if demo.element_type else "any"
        header = f"Stack ({demo.size()}/{demo.max_size})  type: {type_label}"

        if demo.is_empty():
            self.update(f"{header}\n  (empty)")
            return

        items = list(reversed(demo.stack))
        cell_w = max(max(len(str(item)) for item in items), 5)
        inner_w = cell_w + 2

        lines = [f"  ┌{'─' * inner_w}┐"]
        for i, item in enumerate(items):
            marker = "  ← top" if i == 0 else ""
            lines.append(f"  │ {str(item):^{cell_w}} │{marker}")
        lines.append(f"  └{'─' * inner_w}┘")
        self.update(header + "\n" + "\n".join(lines))


class StackApp(App):
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

    BINDINGS = [("ctrl+d", "quit", "Quit")]

    def __init__(self, max_size: int = 1000):
        super().__init__()
        self.demo = StackDemo(max_size=max_size)

    def compose(self) -> ComposeResult:
        yield Header()
        yield StackPanel(id="panel")
        yield RichLog(id="log", highlight=True, markup=True)
        yield Input(placeholder="/push <v>  /pop  /peek  /show  /type [int|float|str|any]  /help  /quit")
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
            self._dispatch(raw)
            self._refresh_panel()

    def _dispatch(self, raw: str) -> None:
        log = self.query_one(RichLog)
        parts = raw.split(maxsplit=1)
        verb = parts[0].lower()
        arg = parts[1].strip() if len(parts) > 1 else None

        if verb == "/push":
            if arg is None:
                log.write("[red]Usage: /push <value>[/red]")
                return
            try:
                pushed = self.demo.push(arg)
                log.write(f"[green]push({pushed!r})  size={self.demo.size()}[/green]")
            except OverflowError as e:
                log.write(f"[red]Overflow: {e}[/red]")
            except TypeError as e:
                log.write(f"[red]TypeError: {e}[/red]")

        elif verb == "/pop":
            try:
                val = self.demo.pop()
                log.write(f"[green]pop() → {val!r}  size={self.demo.size()}[/green]")
            except IndexError as e:
                log.write(f"[red]Underflow: {e}[/red]")

        elif verb == "/peek":
            try:
                val = self.demo.peek()
                log.write(f"[cyan]peek() → {val!r}[/cyan]")
            except IndexError as e:
                log.write(f"[red]Underflow: {e}[/red]")

        elif verb in ("/show", "/print"):
            if self.demo.is_empty():
                log.write("[yellow]Stack is empty.[/yellow]")
            else:
                items = list(reversed(self.demo.stack))
                log.write(f"[cyan]top → bottom: {items}[/cyan]")

        elif verb == "/type":
            if arg is None:
                label = self.demo.element_type.__name__ if self.demo.element_type else "any"
                log.write(f"[cyan]Current type constraint: {label}[/cyan]")
            else:
                try:
                    self.demo.set_type(arg.lower())
                    label = self.demo.element_type.__name__ if self.demo.element_type else "any"
                    log.write(f"[green]Type constraint set to: {label}[/green]")
                except ValueError as e:
                    log.write(f"[red]{e}[/red]")

        elif verb in ("/quit", "/exit"):
            self.exit()

        elif verb == "/help":
            log.write(
                "[bold]Commands[/bold]\n"
                "  [cyan]/push <value>[/cyan]               push a value onto the stack\n"
                "  [cyan]/pop[/cyan]                        pop the top value\n"
                "  [cyan]/peek[/cyan]                       inspect the top value\n"
                "  [cyan]/show[/cyan]  [cyan]/print[/cyan]                display stack contents\n"
                "  [cyan]/type [int|float|str|any][/cyan]   get or set element type constraint\n"
                "  [cyan]/help[/cyan]                       show this help\n"
                "  [cyan]/quit[/cyan]  [cyan]Ctrl+D[/cyan]                exit"
            )

        else:
            log.write(f"[red]Unknown command: {verb!r} — type /help[/red]")

    def _refresh_panel(self) -> None:
        self.query_one(StackPanel).refresh_stack(self.demo)


def main() -> None:
    parser = argparse.ArgumentParser(description="Interactive Stack Demo")
    parser.add_argument(
        "--max-size", type=int, default=1000, metavar="N",
        help="Maximum stack capacity (default: 1000)",
    )
    args = parser.parse_args()
    StackApp(max_size=args.max_size).run()


if __name__ == "__main__":
    main()
