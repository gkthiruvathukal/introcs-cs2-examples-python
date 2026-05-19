# List — interactive demo (light theme)
# Run from project root:  vhs demos/list-light.tape

Output demos/list-light.mp4

Set Theme "Catppuccin Latte"
Set FontSize 16
Set FontFamily "DejaVu Sans Mono"
Set Width 1800
Set Height 900
Set Framerate 30
Set Padding 24
Set WindowBar Colorful
Set BorderRadius 8
Set TypingSpeed 29ms
Env TERM xterm-256color

# ── Launch ──────────────────────────────────────────────────────────────────
Type ".venv/bin/python -m data_structures.tui.list_app"
Enter
Sleep 10s

# ── Build list ───────────────────────────────────────────────────────────────
Type "/append 10 20 30 40 50"
Enter
Sleep 2s

# ── Search ──────────────────────────────────────────────────────────────────
Type "/search 30"
Enter
Sleep 1.5s

# ── Insert at index 2 → [10, 20, 25, 30, 40, 50] ────────────────────────────
Type "/insert 2 25"
Enter
Sleep 2s

# ── Set value at index 0 → [5, 20, 25, 30, 40, 50] ──────────────────────────
Type "/set 0 5"
Enter
Sleep 2s

# ── Remove by value ─────────────────────────────────────────────────────────
Type "/remove-value 25"
Enter
Sleep 2s

# ── Remove by position ───────────────────────────────────────────────────────
Type "/remove-at 4"
Enter
Sleep 2s

# ── Undo / redo ─────────────────────────────────────────────────────────────
Type "/undo"
Enter
Sleep 1.5s

Type "/undo"
Enter
Sleep 1.5s

Type "/redo"
Enter
Sleep 1.5s

# ── Save current state ───────────────────────────────────────────────────────
Type "/save /tmp/list-demo.json"
Enter
Sleep 1.5s

# ── Switch to strings and generate random values ─────────────────────────────
Type "/clear"
Enter
Sleep 1s

Type "/type str"
Enter
Sleep 1s

Type "/random 5"
Enter
Sleep 2s

# ── Load the saved int session back ─────────────────────────────────────────
Type "/clear"
Enter
Sleep 1s

Type "/load /tmp/list-demo.json"
Enter
Sleep 2s

# ── Quit ────────────────────────────────────────────────────────────────────
Type "/quit"
Enter
Sleep 1s
