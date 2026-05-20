# Doubly Linked List — interactive demo (dark theme)
# Run from project root:  vhs demos/dll-dark.tape

Output demos/dll-dark.mp4

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
Type ".venv/bin/python -m data_structures.tui.doubly_linked_list_app"
Enter
Sleep 10s

# ── Build initial list: nodes 1(10) 2(20) 3(30) 4(40) 5(50) ────────────────
# CAPTION: Append 5 values to build the initial doubly linked list
Type "/append 10 20 30 40 50"
Enter
Sleep 2s

# ── Inspect ─────────────────────────────────────────────────────────────────
# CAPTION: Inspect the head node
Type "/at 0"
Enter
Sleep 1.5s

# CAPTION: Inspect a middle node
Type "/at 2"
Enter
Sleep 1.5s

# CAPTION: Traverse the list backward from the tail
Type "/show-backward"
Enter
Sleep 2s

# ── Search ──────────────────────────────────────────────────────────────────
# CAPTION: Search for the value 30
Type "/search 30"
Enter
Sleep 1.5s

# ── Insert at head → node 6(5) ──────────────────────────────────────────────
# CAPTION: Insert a new head node with value 5
Type "/insert-at 0 5"
Enter
Sleep 2s

# ── Insert after node-1 (data=10) → node 7(15) ──────────────────────────────
# CAPTION: Insert 15 after node-1
Type "/insert-after 1 15"
Enter
Sleep 2s

# ── Insert before node-3 (data=30) → node 8(25) ─────────────────────────────
# CAPTION: Insert 25 before node-3
Type "/insert-before 3 25"
Enter
Sleep 2s

# List is now: 6(5) → 1(10) → 7(15) → 2(20) → 8(25) → 3(30) → 4(40) → 5(50)

# ── Remove by value ─────────────────────────────────────────────────────────
# CAPTION: Remove the first node containing 25
Type "/remove-value 25"
Enter
Sleep 2s

# ── Remove by position (index 0 = node-6) ───────────────────────────────────
# CAPTION: Remove the node at index 0
Type "/remove-at 0"
Enter
Sleep 2s

# ── Remove by node id (node-7, data=15) ─────────────────────────────────────
# CAPTION: Remove node-7 by its node id
Type "/remove-node 7"
Enter
Sleep 2s

# List is now: 1(10) → 2(20) → 3(30) → 4(40) → 5(50)

# ── Undo / redo ─────────────────────────────────────────────────────────────
# CAPTION: Undo the previous change
Type "/undo"
Enter
Sleep 1.5s

# CAPTION: Undo one more change
Type "/undo"
Enter
Sleep 1.5s

# CAPTION: Redo the last undone change
Type "/redo"
Enter
Sleep 1.5s

# ── Save current state ───────────────────────────────────────────────────────
# CAPTION: Save the current doubly linked list session
Type "/save /tmp/dll-demo.json"
Enter
Sleep 1.5s

# ── Switch to strings and generate random values ─────────────────────────────
# CAPTION: Clear the list
Type "/clear"
Enter
Sleep 1s

# CAPTION: Switch the list to string values
Type "/type str"
Enter
Sleep 1s

# CAPTION: Generate 5 random string values
Type "/random 5"
Enter
Sleep 2s

# ── Load the saved int session back ─────────────────────────────────────────
# CAPTION: Clear before loading the saved session
Type "/clear"
Enter
Sleep 1s

# CAPTION: Load the saved integer session
Type "/load /tmp/dll-demo.json"
Enter
Sleep 2s

# ── Quit ────────────────────────────────────────────────────────────────────
Type "/quit"
Enter
Sleep 1s
