# Queue — interactive demo
# Run from project root:  vhs demos/queue.tape

Output demos/queue.mp4

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
Type ".venv/bin/python -m data_structures.tui.queue_app"
Enter
Sleep 10s

# ── Build queue: 10 at front, 50 at back ────────────────────────────────────
Type "/enqueue 10 20 30 40 50"
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

# ── Search ──────────────────────────────────────────────────────────────────
Type "/search 30"
Enter
Sleep 1.5s

# ── Dequeue two items ────────────────────────────────────────────────────────
Type "/dequeue"
Enter
Sleep 1.5s

Type "/dequeue"
Enter
Sleep 1.5s

# ── Enqueue more ─────────────────────────────────────────────────────────────
Type "/enqueue 60 70"
Enter
Sleep 2s

# ── Swap and rotate ──────────────────────────────────────────────────────────
Type "/swap"
Enter
Sleep 2s

Type "/rotate"
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
Type "/save /tmp/queue-demo.json"
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

Type "/load /tmp/queue-demo.json"
Enter
Sleep 2s

# ── Quit ────────────────────────────────────────────────────────────────────
Type "/quit"
Enter
Sleep 1s
