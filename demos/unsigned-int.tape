# Unsigned Integer Bit Set — interactive demo
# Run from project root:  vhs demos/unsigned-int.tape

Output demos/unsigned-int.mp4

Set Theme "TokyoNight"
Set FontSize 16
Set FontFamily "DejaVu Sans Mono"
Set Width 1920
Set Height 1200
Set Framerate 30
Set Padding 24
Set WindowBar Colorful
Set BorderRadius 8
Set TypingSpeed 29ms
Env TERM xterm-256color

# ── Launch ──────────────────────────────────────────────────────────────────
Type ".venv/bin/python -m data_structures.tui.unsigned_int_app"
Enter
Sleep 4s

# ════════════════════════════════════════════════════════════════════════════
# 4-BIT section
# ════════════════════════════════════════════════════════════════════════════

# CAPTION: Start with a 4-bit integer — the smallest supported size
Type "/size 4"
Enter
Sleep 2s

# CAPTION: Set the value using a binary literal — 0b1010 is decimal 10
Type "/set 0b1010"
Enter
Sleep 2s

# CAPTION: Show the value in all four bases at once
Type "/show"
Enter
Sleep 2s

# CAPTION: Set bit 0 (the LSB) — value becomes 11
Type "/set-bit 0"
Enter
Sleep 2s

# CAPTION: Toggle bit 3 (the MSB) from 1 to 0 — value becomes 3
Type "/toggle-bit 3"
Enter
Sleep 2s

# CAPTION: Complement flips every bit within the 4-bit width — value becomes 12
Type "/not"
Enter
Sleep 2s

# CAPTION: Shift left 1 bit — the MSB is 1, so overflow is reported
Type "/shl 1"
Enter
Sleep 2s

# CAPTION: Rotate right 2 — bits wrap around, no bits are lost
Type "/ror 2"
Enter
Sleep 2s

# ════════════════════════════════════════════════════════════════════════════
# 8-BIT section
# ════════════════════════════════════════════════════════════════════════════

# CAPTION: Switch to 8-bit — the classic byte representation
Type "/size 8"
Enter
Sleep 2s

# CAPTION: Set 85 — alternating bits 01010101 in binary
Type "/set 85"
Enter
Sleep 2s

# CAPTION: Display just the binary representation
Type "/bin"
Enter
Sleep 2s

# CAPTION: Display the octal representation
Type "/oct"
Enter
Sleep 2s

# CAPTION: Display the hexadecimal representation
Type "/hex"
Enter
Sleep 2s

# CAPTION: Set bit 7 (the MSB) to 1 — value jumps from 85 to 213
Type "/set-bit 7"
Enter
Sleep 2s

# CAPTION: Reset bit 0 (the LSB) to 0 — value becomes 212
Type "/reset-bit 0"
Enter
Sleep 2s

# CAPTION: Shift left 1 — the MSB was 1, so one bit is lost to overflow
Type "/shl 1"
Enter
Sleep 2s

# CAPTION: Logical shift right 3 — zeros fill in from the left
Type "/shr 3"
Enter
Sleep 2s

# CAPTION: Rotate left 4 — the high nibble and low nibble swap
Type "/rol 4"
Enter
Sleep 2s

# CAPTION: Rotate right 4 — restores the previous arrangement
Type "/ror 4"
Enter
Sleep 2s

# CAPTION: Set the rightmost octal group (bits 0–2) to 7
Type "/set-octal 0 7"
Enter
Sleep 2s

# CAPTION: Set the middle octal group (bits 3–5) to 5
Type "/set-octal 1 5"
Enter
Sleep 2s

# CAPTION: Set the high hex nibble (bits 4–7) to hex A
Type "/set-hex 1 10"
Enter
Sleep 2s

# CAPTION: AND with 0b11110000 — clears the low nibble, keeps the high
Type "/and 0b11110000"
Enter
Sleep 2s

# CAPTION: OR with 0x0F — fills the low nibble with all 1s
Type "/or 0x0F"
Enter
Sleep 2s

# CAPTION: XOR with 0xAA — flips every other bit
Type "/xor 0xAA"
Enter
Sleep 2s

# CAPTION: Generate a random 8-bit value across the full 0–255 range
Type "/random"
Enter
Sleep 2s

# CAPTION: Save this session to disk for reloading later
Type "/save /tmp/uint-demo.json"
Enter
Sleep 2s

# CAPTION: Undo the random — restores the previous value
Type "/undo"
Enter
Sleep 2s

# CAPTION: Redo to reapply the random value
Type "/redo"
Enter
Sleep 2s

# ════════════════════════════════════════════════════════════════════════════
# 16-BIT section
# ════════════════════════════════════════════════════════════════════════════

# CAPTION: Switch to 16-bit — hex and octal groups multiply; notice the coloured boundary bars
Type "/size 16"
Enter
Sleep 2s

# CAPTION: Set 0xABCD — a value that shows all hex digits clearly
Type "/set 0xABCD"
Enter
Sleep 2s

# CAPTION: Display the decimal equivalent
Type "/dec"
Enter
Sleep 2s

# CAPTION: Shift left 4 bits — the top hex digit overflows
Type "/shl 4"
Enter
Sleep 2s

# CAPTION: Shift right 4 to restore the lower three hex digits
Type "/shr 4"
Enter
Sleep 2s

# CAPTION: Rotate left 8 — swaps the high byte and low byte
Type "/rol 8"
Enter
Sleep 2s

# CAPTION: AND with 0xFF00 — masks out the low byte, isolates the high byte
Type "/and 0xFF00"
Enter
Sleep 2s

# CAPTION: OR with 0x00FF — fills the low byte back with all 1s
Type "/or 0x00FF"
Enter
Sleep 2s

# CAPTION: Complement the entire 16-bit value
Type "/not"
Enter
Sleep 2s

# CAPTION: Generate a random 16-bit value
Type "/random"
Enter
Sleep 2s

# ════════════════════════════════════════════════════════════════════════════
# 32-BIT section
# ════════════════════════════════════════════════════════════════════════════

# CAPTION: Switch to 32-bit — the magenta bars now mark every 12-bit LCM boundary
Type "/size 32"
Enter
Sleep 2s

# CAPTION: Set a well-known 32-bit pattern — 0xDEADBEEF
Type "/set 0xDEADBEEF"
Enter
Sleep 2s

# CAPTION: Shift right 16 — isolates the upper word in the lower 16 bits
Type "/shr 16"
Enter
Sleep 2s

# CAPTION: Rotate left 16 — swaps the upper and lower 16-bit halves
Type "/rol 16"
Enter
Sleep 2s

# CAPTION: XOR with 0xFFFFFFFF — equivalent to a full complement
Type "/xor 0xFFFFFFFF"
Enter
Sleep 2s

# CAPTION: Generate a random 32-bit value
Type "/random"
Enter
Sleep 2s

# CAPTION: Reload the 8-bit session saved earlier — size and value both restore
Type "/load /tmp/uint-demo.json"
Enter
Sleep 2s

# ── Quit ────────────────────────────────────────────────────────────────────
Type "/quit"
Enter
Sleep 1s
