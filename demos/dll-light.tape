# Doubly Linked List — interactive demo (light theme)
# Run from project root:  vhs demos/dll-light.tape

Output demos/dll-light.mp4

Set Theme "Catppuccin Latte"
Set FontSize 16
Set FontFamily "Monaco"
Set Width 1800
Set Height 900
Set Framerate 30
Set Padding 24
Set WindowBar Colorful
Set BorderRadius 8
Set TypingSpeed 50ms
Env TERM xterm-256color

# ── Launch ──────────────────────────────────────────────────────────────────
Type ".venv/bin/python -m data_structures.tui.doubly_linked_list_app"
Enter
Sleep 10s

# ── Build initial list: nodes 1(10) 2(20) 3(30) 4(40) 5(50) ────────────────
Type "/append 10 20 30 40 50"
Enter
Sleep 2s

# ── Inspect ─────────────────────────────────────────────────────────────────
Type "/at 0"
Enter
Sleep 1.5s

Type "/at 2"
Enter
Sleep 1.5s

Type "/show-backward"
Enter
Sleep 2s

# ── Search ──────────────────────────────────────────────────────────────────
Type "/search 30"
Enter
Sleep 1.5s

# ── Insert at head → node 6(5) ──────────────────────────────────────────────
Type "/insert-at 0 5"
Enter
Sleep 2s

# ── Insert after node-1 (data=10) → node 7(15) ──────────────────────────────
Type "/insert-after 1 15"
Enter
Sleep 2s

# ── Insert before node-3 (data=30) → node 8(25) ─────────────────────────────
Type "/insert-before 3 25"
Enter
Sleep 2s

# List is now: 6(5) → 1(10) → 7(15) → 2(20) → 8(25) → 3(30) → 4(40) → 5(50)

# ── Remove by value ─────────────────────────────────────────────────────────
Type "/remove-value 25"
Enter
Sleep 2s

# ── Remove by position (index 0 = node-6) ───────────────────────────────────
Type "/remove-at 0"
Enter
Sleep 2s

# ── Remove by node id (node-7, data=15) ─────────────────────────────────────
Type "/remove-node 7"
Enter
Sleep 2s

# List is now: 1(10) → 2(20) → 3(30) → 4(40) → 5(50)

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
Type "/save /tmp/dll-demo.json"
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

Type "/load /tmp/dll-demo.json"
Enter
Sleep 2s

# ── Quit ────────────────────────────────────────────────────────────────────
Type "/quit"
Enter
Sleep 1s
