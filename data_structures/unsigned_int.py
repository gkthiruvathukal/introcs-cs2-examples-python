import math


VALID_SIZES = (4, 8, 16, 32, 64)


class UnsignedInt:
    """Fixed-width unsigned integer with bit, octal, and hex group manipulation."""

    def __init__(self, size: int = 8, value: int = 0):
        if size not in VALID_SIZES:
            raise ValueError(f"Size must be one of {list(VALID_SIZES)}, got {size}")
        self.size = size
        self._mask = (1 << size) - 1
        self._value = 0
        self.set_value(value)

    @property
    def value(self) -> int:
        return self._value

    def set_value(self, value: int) -> None:
        if not (0 <= value <= self._mask):
            raise ValueError(
                f"Value {value} out of range [0, {self._mask}] for {self.size}-bit unsigned integer"
            )
        self._value = value

    def get_bit(self, pos: int) -> int:
        self._check_bit_pos(pos)
        return (self._value >> pos) & 1

    def set_bit(self, pos: int) -> None:
        self._check_bit_pos(pos)
        self._value |= 1 << pos

    def reset_bit(self, pos: int) -> None:
        self._check_bit_pos(pos)
        self._value &= ~(1 << pos) & self._mask

    def toggle_bit(self, pos: int) -> None:
        self._check_bit_pos(pos)
        self._value ^= 1 << pos

    def set_octal_group(self, group_pos: int, octal_digit: int) -> None:
        """Set octal group at group_pos (0 = rightmost group of 3 bits)."""
        num_groups = math.ceil(self.size / 3)
        if not (0 <= group_pos < num_groups):
            raise ValueError(
                f"Octal group position {group_pos} out of range [0, {num_groups - 1}]"
            )
        if not (0 <= octal_digit <= 7):
            raise ValueError(f"Octal digit must be 0–7, got {octal_digit}")
        if group_pos == num_groups - 1:
            phantom = num_groups * 3 - self.size
            max_digit = (1 << (3 - phantom)) - 1
            if octal_digit > max_digit:
                raise ValueError(
                    f"MSB octal group for {self.size}-bit integer can only hold 0–{max_digit}, got {octal_digit}"
                )
        shift = group_pos * 3
        self._value = (self._value & ~(0b111 << shift)) | (octal_digit << shift)
        self._value &= self._mask

    def set_hex_group(self, group_pos: int, hex_digit: int) -> None:
        """Set hex nibble at group_pos (0 = rightmost nibble)."""
        num_groups = self.size // 4
        if not (0 <= group_pos < num_groups):
            raise ValueError(
                f"Hex group position {group_pos} out of range [0, {num_groups - 1}]"
            )
        if not (0 <= hex_digit <= 15):
            raise ValueError(f"Hex digit must be 0–15 (0x0–0xF), got {hex_digit}")
        shift = group_pos * 4
        self._value = (self._value & ~(0xF << shift)) | (hex_digit << shift)

    def shift_left(self, n: int) -> int:
        """Shift left by n bits. Returns the bits shifted out (0 if none)."""
        if n < 0:
            raise ValueError(f"Shift amount must be non-negative, got {n}")
        if n == 0:
            return 0
        if n >= self.size:
            lost = self._value
            self._value = 0
            return lost
        lost = self._value >> (self.size - n)
        self._value = (self._value << n) & self._mask
        return lost

    def shift_right(self, n: int) -> None:
        """Logical (unsigned) shift right by n bits."""
        if n < 0:
            raise ValueError(f"Shift amount must be non-negative, got {n}")
        self._value = 0 if n >= self.size else self._value >> n

    def rotate_left(self, n: int) -> None:
        """Rotate left by n bits (circular, no overflow)."""
        if n < 0:
            raise ValueError(f"Rotation amount must be non-negative, got {n}")
        n %= self.size
        if n:
            self._value = ((self._value << n) | (self._value >> (self.size - n))) & self._mask

    def rotate_right(self, n: int) -> None:
        """Rotate right by n bits (circular, no overflow)."""
        if n < 0:
            raise ValueError(f"Rotation amount must be non-negative, got {n}")
        n %= self.size
        if n:
            self._value = ((self._value >> n) | (self._value << (self.size - n))) & self._mask

    def complement(self) -> None:
        """Bitwise NOT within the current bit width."""
        self._value = (~self._value) & self._mask

    def bitwise_and(self, other: int) -> None:
        self._check_operand(other)
        self._value &= other

    def bitwise_or(self, other: int) -> None:
        self._check_operand(other)
        self._value |= other

    def bitwise_xor(self, other: int) -> None:
        self._check_operand(other)
        self._value ^= other

    def clear(self) -> None:
        self._value = 0

    def phantom_bit_count(self) -> int:
        return math.ceil(self.size / 3) * 3 - self.size

    def display_bit_width(self) -> int:
        return math.ceil(self.size / 3) * 3

    def bit_list(self) -> list[int]:
        """Real bits only, MSB first, length == size."""
        return [(self._value >> i) & 1 for i in range(self.size - 1, -1, -1)]

    def octal_groups(self) -> list[int]:
        """Octal digits MSB first (including phantom MSB group)."""
        num_groups = math.ceil(self.size / 3)
        return [(self._value >> (i * 3)) & 0b111 for i in range(num_groups - 1, -1, -1)]

    def hex_groups(self) -> list[int]:
        """Hex nibbles MSB first."""
        num_groups = self.size // 4
        return [(self._value >> (i * 4)) & 0xF for i in range(num_groups - 1, -1, -1)]

    def to_bin(self) -> str:
        return f"0b{self._value:0{self.size}b}"

    def to_oct(self) -> str:
        return oct(self._value)

    def to_hex(self) -> str:
        return f"0x{self._value:0{self.size // 4}X}"

    def _check_bit_pos(self, pos: int) -> None:
        if not (0 <= pos < self.size):
            raise ValueError(
                f"Bit position {pos} out of range [0, {self.size - 1}]"
            )

    def _check_operand(self, other: int) -> None:
        if not (0 <= other <= self._mask):
            raise ValueError(
                f"Operand {other} out of range [0, {self._mask}] for {self.size}-bit unsigned integer"
            )



def render_visualization(uint: UnsignedInt, markup: bool = False) -> str:
    """
    Render binary/octal/hex boxes aligned right-to-left.

    Phantom bits (needed so octal groups tile evenly) are shown as '·' on the
    left of the binary row.  The hex phantom cell mirrors this.

    In the binary row, group boundaries are highlighted:
      - octal only  → yellow  heavy verticals (┳ ┃ ┻)
      - hex only    → cyan    double verticals (╥ ║ ╨)
      - both (LCM=12 bits) → magenta heavy verticals
    """
    n_display = uint.display_bit_width()  # total bit columns (incl. phantom)
    n_phantom = uint.phantom_bit_count()
    bits = uint.bit_list()
    oct_groups = uint.octal_groups()
    hex_groups = uint.hex_groups()

    def _sep(i: int) -> tuple[str, str, str]:
        """Return (top, mid, bot) separator chars/markup after cell i."""
        is_oct = (n_display - i - 1) % 3 == 0
        is_hex = (i >= n_phantom) and ((n_display - i - 1) % 4 == 0)
        if markup:
            if is_oct and is_hex:
                return "[bold magenta]┳[/]", "[bold magenta]┃[/]", "[bold magenta]┻[/]"
            if is_oct:
                return "[bold yellow]┳[/]", "[bold yellow]┃[/]", "[bold yellow]┻[/]"
            if is_hex:
                return "[bold cyan]╥[/]", "[bold cyan]║[/]", "[bold cyan]╨[/]"
        else:
            if is_oct:
                return "┳", "┃", "┻"
            if is_hex:
                return "╥", "║", "╨"
        return "┬", "│", "┴"

    # ── binary row ────────────────────────────────────────────────────────────
    all_cells = ["·"] * n_phantom + [str(b) for b in bits]

    top_parts, mid_parts, bot_parts = ["┌"], ["│"], ["└"]
    for i, cell in enumerate(all_cells):
        top_parts.append("───")
        mid_parts.append(f" {cell} ")
        bot_parts.append("───")
        if i < n_display - 1:
            t, m, b = _sep(i)
            top_parts.append(t)
            mid_parts.append(m)
            bot_parts.append(b)
    top_parts.append("┐")
    mid_parts.append("│")
    bot_parts.append("┘")

    bin_top = "".join(top_parts)
    bin_mid = "".join(mid_parts)
    bin_bot = "".join(bot_parts)

    # ── octal row ────────────────────────────────────────────────────────────
    # 3 bit-cells wide → inner = 3*3 + 2 = 11
    inner_oct = 11
    oct_top = "┌" + "┬".join("─" * inner_oct for _ in oct_groups) + "┐"
    oct_mid = "│" + "│".join(str(d).center(inner_oct) for d in oct_groups) + "│"
    oct_bot = "└" + "┴".join("─" * inner_oct for _ in oct_groups) + "┘"

    # ── hex row ──────────────────────────────────────────────────────────────
    # 4 bit-cells wide → inner = 4*3 + 3 = 15
    # A single phantom cell spans the n_phantom bit-columns that have no hex
    # digit.  Its inner width = n_phantom*4 - 1 so the total row stays at
    # 1 + display_bit_width*4 chars (same as the binary and octal rows).
    inner_hex = 15
    phantom_hex = n_phantom * 4 - 1
    hex_top = "┌" + "─" * phantom_hex + "┬" + "┬".join("─" * inner_hex for _ in hex_groups) + "┐"
    hex_mid = "│" + "·".center(phantom_hex) + "│" + "│".join(f"{d:X}".center(inner_hex) for d in hex_groups) + "│"
    hex_bot = "└" + "─" * phantom_hex + "┴" + "┴".join("─" * inner_hex for _ in hex_groups) + "┘"

    return "\n".join([
        "Binary",
        bin_top,
        bin_mid,
        bin_bot,
        "Hex",
        hex_top,
        hex_mid,
        hex_bot,
        "Octal",
        oct_top,
        oct_mid,
        oct_bot,
    ])
