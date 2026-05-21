# UnsignedInt

## Purpose

`data_structures/unsigned_int.py` implements a fixed-width unsigned integer that exposes its internal bit, octal, and hexadecimal structure. It is designed as an educational tool for understanding binary number representation — how the same bit pattern looks different depending on the base used to group and read the bits.

The module provides:

- `UnsignedInt` — the data structure class
- `render_visualization()` — a pure function that produces the aligned multi-row box display

## Supported Sizes

| Size | Bits | Hex digits | Octal digits | Phantom bits |
|---|---|---|---|---|
| nibble | 4 | 1 | 2 | 2 |
| byte | 8 | 2 | 3 | 1 |
| short | 16 | 4 | 6 | 2 |
| int | 32 | 8 | 11 | 1 |
| long | 64 | 16 | 22 | 2 |

*Phantom bits* are extra zero bits added on the left so that octal groups (3 bits each) tile evenly across the full display width.

## Operations

### Value

| Method | Description |
|---|---|
| `set_value(n)` | Set the integer value; raises `ValueError` if out of range |
| `clear()` | Reset to zero |
| `value` | Read-only property returning the current integer value |

### Bit operations

| Method | Description |
|---|---|
| `get_bit(pos)` | Return the bit at position `pos` (0 = LSB) |
| `set_bit(pos)` | Set bit `pos` to 1 |
| `reset_bit(pos)` | Set bit `pos` to 0 |
| `toggle_bit(pos)` | Flip bit `pos` |

### Shift and rotate

| Method | Description |
|---|---|
| `shift_left(n)` | Logical shift left; returns the bits shifted out (non-zero signals overflow) |
| `shift_right(n)` | Logical shift right; zeros fill from the left |
| `rotate_left(n)` | Circular left rotation; no bits lost |
| `rotate_right(n)` | Circular right rotation; no bits lost |

### Logical

| Method | Description |
|---|---|
| `complement()` | Bitwise NOT within the current bit width |
| `bitwise_and(other)` | AND with an unsigned integer constant |
| `bitwise_or(other)` | OR with an unsigned integer constant |
| `bitwise_xor(other)` | XOR with an unsigned integer constant |

### Group operations

| Method | Description |
|---|---|
| `set_octal_group(pos, digit)` | Set the octal group at `pos` (0 = rightmost) to `digit` (0–7) |
| `set_hex_group(pos, digit)` | Set the hex nibble at `pos` (0 = rightmost) to `digit` (0–15) |

### Query

| Method | Description |
|---|---|
| `bit_list()` | List of bits MSB-first, length == `size` |
| `octal_groups()` | List of octal digit values MSB-first (including phantom MSB group) |
| `hex_groups()` | List of hex nibble values MSB-first |
| `phantom_bit_count()` | Number of phantom bits required for octal alignment |
| `display_bit_width()` | Total bit columns shown (real + phantom) |
| `to_bin()` | `"0b..."` string, zero-padded to `size` |
| `to_oct()` | `"0o..."` string |
| `to_hex()` | `"0x..."` string, zero-padded to `size // 4` hex digits |

## Visualization

`render_visualization(uint, markup=False)` returns a multi-line string showing three aligned rows:

```
Binary
┌───┬───┬───┳───┬───╥───┳───┬───┬───┐
│ · │ 0 │ 1 ┃ 0 │ 1 ║ 0 ┃ 1 │ 0 │ 1 │
└───┴───┴───┻───┴───╨───┻───┴───┴───┘
Hex
┌───┬───────────────┬───────────────┐
│ · │       5       │       5       │
└───┴───────────────┴───────────────┘
Octal
┌───────────┬───────────┬───────────┐
│     1     │     2     │     5     │
└───────────┴───────────┴───────────┘
```

All three rows have the same total character width. Alignment rules:

- **Binary row** — one cell per display bit (real bits + phantom `·` on the left)
- **Hex row** — each cell spans 4 bit columns; a phantom cell on the left accounts for unused display columns
- **Octal row** — each cell spans 3 bit columns; always tiles the full display width

### Group boundary indicators

The binary row uses different separator characters to show where groups begin and end:

| Separator | Colour (when `markup=True`) | Meaning |
|---|---|---|
| `┃` / `┳` / `┻` | Yellow | Octal group boundary (every 3 bits from the right) |
| `║` / `╥` / `╨` | Cyan | Hex group boundary (every 4 bits from the right) |
| `┃` / `┳` / `┻` | Magenta | Both coincide (every 12 bits, LCM(3, 4)) |

Pass `markup=True` to get Rich markup colour tags suitable for use in a Textual `Static` widget.
