import argparse
import json
import random
import shlex
import time
from pathlib import Path

from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Input, RichLog, Static

from ..unsigned_int import VALID_SIZES, UnsignedInt, render_visualization
from .common import format_elapsed_ns, parse_single_path


class UnsignedIntPanel(Static):
    def refresh_display(self, uint: UnsignedInt) -> None:
        header = (
            f"UnsignedInt  size={uint.size}  "
            f"dec={uint.value}  {uint.to_bin()}  {uint.to_oct()}  {uint.to_hex()}"
        )
        vis = render_visualization(uint, markup=True)
        self.update(header + "\n\n" + vis)


class UnsignedIntApp(App):
    CSS = """
    UnsignedIntPanel {
        height: auto;
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
    ]

    PLACEHOLDER = (
        "/help  /set <n>  /random  /set-bit <pos>  /reset-bit <pos>  /toggle-bit <pos>  "
        "/set-octal <grp> <d>  /set-hex <grp> <d>  "
        "/shl <n>  /shr <n>  /rol <n>  /ror <n>  /not  "
        "/and <c>  /or <c>  /xor <c>  "
        "/size <bits>  /clear  /show  /dec  /bin  /oct  /hex  /save <file>  /load <file>  /undo  /redo  /quit"
    )

    def __init__(self, initial_size: int = 8, **kwargs):
        super().__init__(**kwargs)
        self.uint = UnsignedInt(size=initial_size)
        self.undo_history: list[dict] = []
        self.redo_history: list[dict] = []
        self.rng = random.Random()

    # ── lifecycle ─────────────────────────────────────────────────────────────

    def compose(self) -> ComposeResult:
        yield Header()
        yield UnsignedIntPanel(id="panel")
        yield RichLog(id="log", highlight=True, markup=True)
        yield Input(placeholder=self.PLACEHOLDER)
        yield Footer()

    def on_mount(self) -> None:
        self._refresh_panel()
        self.query_one(RichLog).write(
            "[bold]UnsignedInt Demo[/bold] — type [cyan]/help[/cyan] for commands."
        )
        self.query_one(Input).focus()

    # ── command dispatch ──────────────────────────────────────────────────────

    @on(Input.Submitted)
    def handle_command(self, event: Input.Submitted) -> None:
        raw = event.value.strip()
        self.query_one(Input).clear()
        if not raw:
            return
        started = time.perf_counter_ns()
        self._dispatch(raw)
        self._refresh_panel()
        elapsed_ns = time.perf_counter_ns() - started
        self.query_one(RichLog).write(f"[dim]time: {format_elapsed_ns(elapsed_ns)}[/dim]")

    def _dispatch(self, raw: str) -> None:
        log = self.query_one(RichLog)
        parts = raw.split(maxsplit=1)
        verb = parts[0].lower()
        arg = parts[1].strip() if len(parts) > 1 else None

        if verb == "/set":
            if arg is None:
                log.write("[red]Usage: /set <decimal-value>[/red]")
                return
            try:
                new_val = int(arg, 0)
                self._record_undo()
                self.uint.set_value(new_val)
                log.write(f"[green]set({new_val}) → {self.uint.to_bin()}  {self.uint.to_oct()}  {self.uint.to_hex()}[/green]")
            except ValueError as e:
                log.write(f"[red]{e}[/red]")

        elif verb == "/random":
            self._record_undo()
            new_val = self.rng.randint(0, self.uint._mask)
            self.uint.set_value(new_val)
            log.write(
                f"[green]random() → dec={self.uint.value}  "
                f"{self.uint.to_bin()}  {self.uint.to_oct()}  {self.uint.to_hex()}[/green]"
            )

        elif verb == "/set-bit":
            if arg is None:
                log.write("[red]Usage: /set-bit <pos>   (pos 0 = LSB)[/red]")
                return
            try:
                pos = int(arg)
                self._record_undo()
                self.uint.set_bit(pos)
                log.write(f"[green]set-bit({pos}) → {self.uint.to_bin()}[/green]")
            except ValueError as e:
                log.write(f"[red]{e}[/red]")

        elif verb == "/reset-bit":
            if arg is None:
                log.write("[red]Usage: /reset-bit <pos>   (pos 0 = LSB)[/red]")
                return
            try:
                pos = int(arg)
                self._record_undo()
                self.uint.reset_bit(pos)
                log.write(f"[green]reset-bit({pos}) → {self.uint.to_bin()}[/green]")
            except ValueError as e:
                log.write(f"[red]{e}[/red]")

        elif verb == "/toggle-bit":
            if arg is None:
                log.write("[red]Usage: /toggle-bit <pos>   (pos 0 = LSB)[/red]")
                return
            try:
                pos = int(arg)
                self._record_undo()
                self.uint.toggle_bit(pos)
                log.write(f"[green]toggle-bit({pos}) → {self.uint.to_bin()}  dec={self.uint.value}[/green]")
            except ValueError as e:
                log.write(f"[red]{e}[/red]")

        elif verb == "/shl":
            if arg is None:
                log.write("[red]Usage: /shl <n>[/red]")
                return
            try:
                n = int(arg)
                self._record_undo()
                lost = self.uint.shift_left(n)
                result = f"[green]shl({n}) → {self.uint.to_bin()}  dec={self.uint.value}[/green]"
                log.write(result)
                if lost:
                    log.write(f"[yellow]overflow: {n} bit(s) shifted out — lost value 0b{lost:0{n}b}[/yellow]")
            except ValueError as e:
                log.write(f"[red]{e}[/red]")

        elif verb == "/shr":
            if arg is None:
                log.write("[red]Usage: /shr <n>[/red]")
                return
            try:
                n = int(arg)
                self._record_undo()
                self.uint.shift_right(n)
                log.write(f"[green]shr({n}) → {self.uint.to_bin()}  dec={self.uint.value}[/green]")
            except ValueError as e:
                log.write(f"[red]{e}[/red]")

        elif verb == "/rol":
            if arg is None:
                log.write("[red]Usage: /rol <n>[/red]")
                return
            try:
                n = int(arg)
                self._record_undo()
                self.uint.rotate_left(n)
                log.write(f"[green]rol({n}) → {self.uint.to_bin()}  dec={self.uint.value}[/green]")
            except ValueError as e:
                log.write(f"[red]{e}[/red]")

        elif verb == "/ror":
            if arg is None:
                log.write("[red]Usage: /ror <n>[/red]")
                return
            try:
                n = int(arg)
                self._record_undo()
                self.uint.rotate_right(n)
                log.write(f"[green]ror({n}) → {self.uint.to_bin()}  dec={self.uint.value}[/green]")
            except ValueError as e:
                log.write(f"[red]{e}[/red]")

        elif verb == "/not":
            self._record_undo()
            self.uint.complement()
            log.write(f"[green]not() → {self.uint.to_bin()}  dec={self.uint.value}[/green]")

        elif verb in ("/and", "/or", "/xor"):
            if arg is None:
                log.write(f"[red]Usage: {verb} <constant>  (prefix 0b/0o/0x or plain decimal)[/red]")
                return
            try:
                operand = int(arg, 0)
                self._record_undo()
                before = self.uint.value
                if verb == "/and":
                    self.uint.bitwise_and(operand)
                    op_sym = "&"
                elif verb == "/or":
                    self.uint.bitwise_or(operand)
                    op_sym = "|"
                else:
                    self.uint.bitwise_xor(operand)
                    op_sym = "^"
                log.write(
                    f"[green]{verb[1:]}() "
                    f"0b{before:0{self.uint.size}b} {op_sym} 0b{operand:0{self.uint.size}b} "
                    f"→ {self.uint.to_bin()}  dec={self.uint.value}[/green]"
                )
            except ValueError as e:
                log.write(f"[red]{e}[/red]")

        elif verb == "/set-octal":
            tokens = shlex.split(arg) if arg else []
            if len(tokens) != 2:
                log.write("[red]Usage: /set-octal <group-pos> <digit 0-7>   (pos 0 = rightmost)[/red]")
                return
            try:
                grp = int(tokens[0])
                digit = int(tokens[1])
                self._record_undo()
                self.uint.set_octal_group(grp, digit)
                log.write(f"[green]set-octal(group={grp}, digit={digit}) → {self.uint.to_oct()}  dec={self.uint.value}[/green]")
            except ValueError as e:
                log.write(f"[red]{e}[/red]")

        elif verb == "/set-hex":
            tokens = shlex.split(arg) if arg else []
            if len(tokens) != 2:
                log.write("[red]Usage: /set-hex <group-pos> <digit 0-15>   (pos 0 = rightmost)[/red]")
                return
            try:
                grp = int(tokens[0])
                digit = int(tokens[1], 16) if tokens[1].startswith("0x") or tokens[1].startswith("0X") else int(tokens[1])
                self._record_undo()
                self.uint.set_hex_group(grp, digit)
                log.write(f"[green]set-hex(group={grp}, digit=0x{digit:X}) → {self.uint.to_hex()}  dec={self.uint.value}[/green]")
            except ValueError as e:
                log.write(f"[red]{e}[/red]")

        elif verb == "/size":
            if arg is None:
                log.write(f"[cyan]Current size: {self.uint.size} bits.  Valid: {list(VALID_SIZES)}[/cyan]")
                return
            try:
                new_size = int(arg)
                self._record_undo()
                self.uint = UnsignedInt(size=new_size)
                log.write(f"[green]size changed to {new_size} bits, value reset to 0[/green]")
            except ValueError as e:
                log.write(f"[red]{e}[/red]")

        elif verb == "/clear":
            self._record_undo()
            self.uint.clear()
            log.write("[green]clear() → all bits set to 0[/green]")

        elif verb == "/save":
            if arg is None:
                log.write("[red]Usage: /save <path>[/red]")
                return
            try:
                path = parse_single_path(arg, "save")
                payload = {"size": self.uint.size, "value": self.uint.value}
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
                log.write(f"[green]save() wrote size={self.uint.size} value={self.uint.value} to {str(path)!r}[/green]")
            except (OSError, ValueError) as e:
                log.write(f"[red]Save failed: {e}[/red]")

        elif verb == "/load":
            if arg is None:
                log.write("[red]Usage: /load <path>[/red]")
                return
            try:
                path = parse_single_path(arg, "load")
                payload = json.loads(path.read_text(encoding="utf-8"))
                size = int(payload["size"])
                value = int(payload["value"])
                self._record_undo()
                self.uint = UnsignedInt(size=size, value=value)
                log.write(f"[green]load() restored size={size} value={value} from {str(path)!r}[/green]")
            except (OSError, KeyError, ValueError, TypeError) as e:
                log.write(f"[red]Load failed: {e}[/red]")

        elif verb == "/undo":
            if not self.undo_history:
                log.write("[yellow]Nothing to undo.[/yellow]")
                return
            self.redo_history.append(self._snapshot())
            snap = self.undo_history.pop()
            self._restore(snap)
            log.write(f"[green]undo() → size={self.uint.size} dec={self.uint.value}[/green]")

        elif verb == "/redo":
            if not self.redo_history:
                log.write("[yellow]Nothing to redo.[/yellow]")
                return
            self.undo_history.append(self._snapshot())
            snap = self.redo_history.pop()
            self._restore(snap)
            log.write(f"[green]redo() → size={self.uint.size} dec={self.uint.value}[/green]")

        elif verb in ("/show", "/print"):
            log.write(
                f"[cyan]size={self.uint.size}  dec={self.uint.value}  "
                f"{self.uint.to_bin()}  {self.uint.to_oct()}  {self.uint.to_hex()}[/cyan]"
            )

        elif verb == "/dec":
            log.write(f"[cyan]dec={self.uint.value}[/cyan]")

        elif verb == "/bin":
            log.write(f"[cyan]{self.uint.to_bin()}[/cyan]")

        elif verb == "/oct":
            log.write(f"[cyan]{self.uint.to_oct()}[/cyan]")

        elif verb == "/hex":
            log.write(f"[cyan]{self.uint.to_hex()}[/cyan]")

        elif verb in ("/quit", "/exit"):
            self.exit()

        elif verb == "/help":
            log.write("\n".join([
                "[bold]Commands[/bold]",
                "  [bold]--- Value ---[/bold]",
                "  [cyan]/set[/cyan] N                       set integer value (decimal; prefix 0b/0o/0x for other bases)",
                "  [cyan]/random[/cyan]                      set a random value across the full bit range",
                "  [cyan]/clear[/cyan]                       reset all bits to 0",
                "  [cyan]/size[/cyan] 4|8|16|32|64           change bit width (resets value to 0)",
                "",
                "  [bold]--- Bit operations ---[/bold]",
                "  [cyan]/set-bit[/cyan] POS                 set bit at POS to 1  (0=LSB)",
                "  [cyan]/reset-bit[/cyan] POS               set bit at POS to 0",
                "  [cyan]/toggle-bit[/cyan] POS              flip bit at POS",
                "",
                "  [bold]--- Shift, rotate, and logical ---[/bold]",
                "  [cyan]/shl[/cyan] N                       shift left N bits (overflow reported if bits are lost)",
                "  [cyan]/shr[/cyan] N                       logical shift right N bits (zeros fill from left)",
                "  [cyan]/rol[/cyan] N                       rotate left N bits (circular, no overflow)",
                "  [cyan]/ror[/cyan] N                       rotate right N bits (circular, no overflow)",
                "  [cyan]/not[/cyan]                         bitwise complement (flip all bits)",
                "  [cyan]/and[/cyan] CONST                   bitwise AND with constant (0b/0o/0x/decimal)",
                "  [cyan]/or[/cyan] CONST                    bitwise OR with constant",
                "  [cyan]/xor[/cyan] CONST                   bitwise XOR with constant",
                "",
                "  [bold]--- Group operations ---[/bold]",
                "  [cyan]/set-octal[/cyan] GRP DIGIT         set octal group GRP (0=rightmost) to DIGIT (0–7)",
                "  [cyan]/set-hex[/cyan] GRP DIGIT           set hex nibble GRP (0=rightmost) to DIGIT (0–F)",
                "",
                "  [bold]--- Session ---[/bold]",
                "  [cyan]/save[/cyan] PATH                   save current size and value to file",
                "  [cyan]/load[/cyan] PATH                   restore size and value from file",
                "  [cyan]/undo[/cyan]                        undo last change",
                "  [cyan]/redo[/cyan]                        redo last undone change",
                "  [cyan]/show[/cyan]                        display current value in all bases",
                "  [cyan]/dec[/cyan]  [cyan]/bin[/cyan]  [cyan]/oct[/cyan]  [cyan]/hex[/cyan]      display value in one specific base",
                "  [cyan]/help[/cyan]                        show this help",
                "  [cyan]/quit[/cyan]  [cyan]Ctrl+D[/cyan]               exit",
            ]))

        else:
            log.write(f"[red]Unknown command: {verb!r} — type /help[/red]")

    # ── helpers ───────────────────────────────────────────────────────────────

    def _refresh_panel(self) -> None:
        self.query_one(UnsignedIntPanel).refresh_display(self.uint)

    def _snapshot(self) -> dict:
        return {"size": self.uint.size, "value": self.uint.value}

    def _restore(self, snap: dict) -> None:
        self.uint = UnsignedInt(size=snap["size"], value=snap["value"])

    def _record_undo(self) -> None:
        self.undo_history.append(self._snapshot())
        self.redo_history.clear()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Interactive UnsignedInt Demo")
    parser.add_argument(
        "--size",
        type=int,
        default=8,
        choices=list(VALID_SIZES),
        metavar="|".join(str(s) for s in VALID_SIZES),
        help="Initial bit width (default: 8)",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    UnsignedIntApp(initial_size=args.size).run()


if __name__ == "__main__":
    main()
