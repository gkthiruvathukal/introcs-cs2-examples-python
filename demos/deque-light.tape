# Deque — interactive demo (light theme)
# Run from project root:  vhs demos/deque-light.tape

Output demos/deque-light.mp4

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
Type ".venv/bin/python -m data_structures.tui.deque_app"
Enter
Sleep 10s

# ── Build deque from both ends → [10, 20, 30, 40, 50] front to back ─────────
Type "/push-back 20 30 40"
Enter
Sleep 2s

Type "/push-front 10"
Enter
Sleep 1.5s

Type "/push-back 50"
Enter
Sleep 1.5s

# ── Inspect ─────────────────────────────────────────────────────────────────
Type "/peek-front"
Enter
Sleep 1.5s

Type "/peek-back"
Enter
Sleep 1.5s

Type "/at 2"
Enter
Sleep 1.5s

# ── Search ──────────────────────────────────────────────────────────────────
Type "/search 30"
Enter
Sleep 1.5s

# ── Modify front and back values ─────────────────────────────────────────────
Type "/set-front 5"
Enter
Sleep 2s

Type "/set-back 55"
Enter
Sleep 2s

# ── Pop from both ends ───────────────────────────────────────────────────────
Type "/pop-front"
Enter
Sleep 1.5s

Type "/pop-back"
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
Type "/save /tmp/deque-demo.json"
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

Type "/load /tmp/deque-demo.json"
Enter
Sleep 2s

# ── Quit ────────────────────────────────────────────────────────────────────
Type "/quit"
Enter
Sleep 1s
