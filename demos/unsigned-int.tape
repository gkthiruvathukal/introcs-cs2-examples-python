# UnsignedInt — interactive demo
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

# ── Set a known value ────────────────────────────────────────────────────────
# CAPTION: Set the byte to 85 — alternating 0s and 1s in binary
Type "/set 85"
Enter
Sleep 2s

# ── Explore hex and octal groupings ─────────────────────────────────────────
# CAPTION: Show the value — binary 01010101, hex 0x55, octal 125
Type "/show"
Enter
Sleep 2s

# ── Bit-level manipulation ───────────────────────────────────────────────────
# CAPTION: Set bit 7 (the MSB) to 1 — value jumps to 213
Type "/set-bit 7"
Enter
Sleep 2s

# CAPTION: Reset bit 0 (the LSB) to 0 — value becomes 212
Type "/reset-bit 0"
Enter
Sleep 2s

# CAPTION: Toggle bit 4 to flip it from 1 to 0
Type "/toggle-bit 4"
Enter
Sleep 2s

# ── Octal group manipulation ─────────────────────────────────────────────────
# CAPTION: Clear the value back to zero before exploring octal groups
Type "/clear"
Enter
Sleep 1s

# CAPTION: Set the rightmost octal group (bits 0–2) to 5
Type "/set-octal 0 5"
Enter
Sleep 2s

# CAPTION: Set the middle octal group (bits 3–5) to 2
Type "/set-octal 1 2"
Enter
Sleep 2s

# CAPTION: Set the leftmost octal group (bits 6–7) to 1 — now octal 125
Type "/set-octal 2 1"
Enter
Sleep 2s

# ── Hex group manipulation ───────────────────────────────────────────────────
# CAPTION: Clear and demonstrate hex group manipulation
Type "/clear"
Enter
Sleep 1s

# CAPTION: Set the low nibble (bits 0–3) to hex A
Type "/set-hex 0 10"
Enter
Sleep 2s

# CAPTION: Set the high nibble (bits 4–7) to hex B — now 0xBA
Type "/set-hex 1 11"
Enter
Sleep 2s

# ── Random values ────────────────────────────────────────────────────────────
# CAPTION: Generate a random 8-bit value
Type "/random"
Enter
Sleep 2s

# CAPTION: Generate another random value — full 0–255 range
Type "/random"
Enter
Sleep 2s

# ── Undo / redo ──────────────────────────────────────────────────────────────
# CAPTION: Undo to restore the previous random value
Type "/undo"
Enter
Sleep 2s

# CAPTION: Redo to reapply the undone change
Type "/redo"
Enter
Sleep 2s

# ── Switch to 16-bit representation ─────────────────────────────────────────
# CAPTION: Switch to a 16-bit integer — value resets to 0
Type "/size 16"
Enter
Sleep 2s

# CAPTION: Set a value that shows the wider bit and hex groupings clearly
Type "/set 43981"
Enter
Sleep 2s

# ── Save and quit ────────────────────────────────────────────────────────────
# CAPTION: Save the current session to disk
Type "/save /tmp/uint-demo.json"
Enter
Sleep 2s

# ── Quit ────────────────────────────────────────────────────────────────────
Type "/quit"
Enter
Sleep 1s
