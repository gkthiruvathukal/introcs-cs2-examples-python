# Stack — interactive demo (light theme)
# Run from project root:  vhs demos/stack-light.tape

Output demos/stack-light.mp4

Set Theme "Catppuccin Latte"
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
Type ".venv/bin/python -m data_structures.tui.stack_app"
Enter
Sleep 10s

# ── Build stack: 10 at bottom, 50 at top ────────────────────────────────────
Type "/push 10 20 30 40 50"
Enter
Sleep 2s

# ── Inspect ─────────────────────────────────────────────────────────────────
Type "/peek"
Enter
Sleep 1.5s

Type "/at 0"
Enter
Sleep 1.5s

Type "/at 2"
Enter
Sleep 1.5s

# ── Stack manipulation ───────────────────────────────────────────────────────
Type "/dup"
Enter
Sleep 2s

Type "/pop"
Enter
Sleep 1.5s

Type "/swap"
Enter
Sleep 2s

Type "/rotate"
Enter
Sleep 2s

# ── Pop a couple ─────────────────────────────────────────────────────────────
Type "/pop"
Enter
Sleep 1.5s

Type "/pop"
Enter
Sleep 1.5s

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
Type "/save /tmp/stack-demo.json"
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

Type "/load /tmp/stack-demo.json"
Enter
Sleep 2s

# ── Quit ────────────────────────────────────────────────────────────────────
Type "/quit"
Enter
Sleep 1s
