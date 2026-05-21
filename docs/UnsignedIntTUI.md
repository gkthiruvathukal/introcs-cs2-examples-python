# UnsignedInt TUI

## Purpose

`data_structures/tui/unsigned_int_app.py` is an interactive terminal app for exploring how unsigned integers are represented in binary, hexadecimal, and octal. It lets you manipulate individual bits, shift and rotate, apply logical operations, and immediately see how every change ripples through all three representations simultaneously.

The visualization panel shows three aligned rows — binary, hex, and octal — at all times. Group boundaries in the binary row are colour-coded so you can see where octal groups (every 3 bits) and hex nibbles (every 4 bits) begin and end, including positions where both coincide (every 12 bits).

## Running the App

Install dependencies first:

```bash
make install
```

Run the TUI:

```bash
make run-uint-app
```

You can also run the module directly with an initial bit width:

```bash
.venv/bin/python -m data_structures.tui.unsigned_int_app
.venv/bin/python -m data_structures.tui.unsigned_int_app --size 16
```

## Command-Line Options

### `--size 4|8|16|32|64`

Set the initial bit width (default: `8`). You can also change the width at runtime with `/size`.

## Layout

The interface has three parts:

1. **Visualization panel** (top) — the current value shown as aligned binary, hex, and octal box rows, plus a summary line with the decimal, binary, octal, and hex values.
2. **Log panel** (middle) — records each command's result, overflow warnings, and execution time.
3. **Input box** (bottom) — where commands are entered.

### Boundary colour key

In the binary row:

| Colour | Separator | Meaning |
|---|---|---|
| Yellow | `┃` | Octal group boundary (every 3 bits from the right) |
| Cyan | `║` | Hex group boundary (every 4 bits from the right) |
| Magenta | `┃` | Both coincide (LCM = 12 bits) |

## Commands

### Value

| Command | Description |
|---|---|
| `/set N` | Set the value; accepts decimal, `0b` binary, `0o` octal, or `0x` hex |
| `/random` | Set a random value uniformly across the full bit range |
| `/clear` | Reset all bits to zero |
| `/size 4\|8\|16\|32\|64` | Change the bit width (resets value to zero) |

### Display

| Command | Description |
|---|---|
| `/show` | Display the value in all four bases |
| `/dec` | Display decimal value |
| `/bin` | Display binary value |
| `/oct` | Display octal value |
| `/hex` | Display hexadecimal value |

### Bit operations

| Command | Description |
|---|---|
| `/set-bit POS` | Set the bit at position `POS` to 1 (0 = LSB) |
| `/reset-bit POS` | Set the bit at position `POS` to 0 |
| `/toggle-bit POS` | Flip the bit at position `POS` |

### Shift, rotate, and logical

| Command | Description |
|---|---|
| `/shl N` | Shift left N bits; overflow is reported in yellow if any 1-bits are lost |
| `/shr N` | Logical shift right N bits; zeros fill from the left |
| `/rol N` | Rotate left N bits; bits wrap around, nothing is lost |
| `/ror N` | Rotate right N bits; bits wrap around, nothing is lost |
| `/not` | Bitwise complement (flip all bits within the current width) |
| `/and CONST` | Bitwise AND with a constant |
| `/or CONST` | Bitwise OR with a constant |
| `/xor CONST` | Bitwise XOR with a constant |

Constants for `/and`, `/or`, `/xor` accept any Python-style prefix: `0b101010`, `0o17`, `0xFF`, or plain decimal. The constant must fit within the current bit width.

### Group operations

| Command | Description |
|---|---|
| `/set-octal GRP DIGIT` | Set the octal group at `GRP` (0 = rightmost) to `DIGIT` (0–7) |
| `/set-hex GRP DIGIT` | Set the hex nibble at `GRP` (0 = rightmost) to `DIGIT` (0–15) |

### Session

| Command | Description |
|---|---|
| `/save PATH` | Save the current bit width and value to a JSON file |
| `/load PATH` | Restore the bit width and value from a saved file |
| `/undo` | Restore the previous state |
| `/redo` | Reapply the most recently undone state |
| `/help` | Show the command summary |
| `/quit` or `Ctrl+D` | Exit the app |

## Typical Session

```text
/size 8
/set 0b10110101
/show
/set-bit 0
/toggle-bit 7
/not
/shl 1
/shr 1
/rol 4
/and 0xF0
/or 0x0F
/xor 0xAA
/set-octal 0 7
/set-hex 1 10
/random
/save /tmp/session.json
/undo
/redo
/size 16
/set 0xABCD
/load /tmp/session.json
/quit
```

## Overflow Reporting

`/shl N` checks whether any 1-bits will be lost before shifting. If so, the log records a yellow warning showing how many bits were shifted out and their combined value:

```
shl(1) → 0b01100100  dec=100
overflow: 1 bit(s) shifted out — lost value 0b1
```

Rotate operations (`/rol`, `/ror`) never produce overflow because bits wrap around.

## Errors and Edge Cases

- `/set` raises an error if the value exceeds the current bit width's maximum.
- `/set-bit`, `/reset-bit`, `/toggle-bit` require a position in `[0, size-1]`.
- `/set-octal` validates that the digit fits within the group; the MSB group may have a smaller maximum when phantom bits are present.
- `/set-hex` validates that the digit is in `[0, 15]` and the group index is valid.
- `/and`, `/or`, `/xor` require the constant to fit within the current bit width.
- `/shl` and `/shr` with `N >= size` clear the value (with overflow reported for `/shl` if the value was non-zero).
- `/load` restores both the saved bit width and the saved value, replacing the current configuration.
- Any mutating command after `/undo` clears the redo history.

## Verification

The data structure and rendering logic are covered by `tests/test_unsigned_int.py` (60 tests). TUI-level construction, snapshot, and parser behaviour are covered by `tests/test_unsigned_int_app.py` (11 tests).
