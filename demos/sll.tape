# Singly Linked List — interactive demo
# Run from project root:  vhs demos/sll.tape

Output demos/sll.mp4

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
Type ".venv/bin/python -m data_structures.tui.singly_linked_list_app"
Enter
Sleep 4s

# ── Build initial list: nodes 1(10) 2(20) 3(30) 4(40) 5(50) ────────────────
# CAPTION: Build a 5-node list by appending values at the tail
Type "/append 10 20 30 40 50"
Enter
Sleep 2s

# ── Inspect ─────────────────────────────────────────────────────────────────
# CAPTION: Inspect the head node of the list
Type "/at 0"
Enter
Sleep 2s

# CAPTION: Inspect the node at index 2
Type "/at 2"
Enter
Sleep 2s

# ── Search ──────────────────────────────────────────────────────────────────
# CAPTION: Search for the node holding value 30
Type "/search 30"
Enter
Sleep 2s

# ── Insert at head → node 6(5) ──────────────────────────────────────────────
# CAPTION: Insert a new head node with value 5
Type "/insert-at 0 5"
Enter
Sleep 2s

# ── Insert after node-1 (data=10) → node 7(15) ──────────────────────────────
# CAPTION: Insert 15 after node-1, splicing into the chain
Type "/insert-after 1 15"
Enter
Sleep 2s

# ── Insert before node-3 (data=30) → node 8(25) ─────────────────────────────
# CAPTION: Insert 25 before node-3, pushing it back one position
Type "/insert-before 3 25"
Enter
Sleep 2s

# List: 6(5) → 1(10) → 7(15) → 2(20) → 8(25) → 3(30) → 4(40) → 5(50)

# ── Remove by value ─────────────────────────────────────────────────────────
# CAPTION: Remove the first node whose value is 25
Type "/remove-value 25"
Enter
Sleep 2s

# ── Remove by position (index 0 = node-6) ───────────────────────────────────
# CAPTION: Remove the head node by its position in the list
Type "/remove-at 0"
Enter
Sleep 2s

# ── Remove by node id (node-7, data=15) ─────────────────────────────────────
# CAPTION: Remove node-7 directly by its unique node id
Type "/remove-node 7"
Enter
Sleep 2s

# ── Undo / redo ─────────────────────────────────────────────────────────────
# CAPTION: Undo the last removal, restoring node-7
Type "/undo"
Enter
Sleep 2s

# CAPTION: Undo one more step, restoring the head node
Type "/undo"
Enter
Sleep 2s

# CAPTION: Redo to reapply the most recently undone removal
Type "/redo"
Enter
Sleep 2s

# ── Save current state ───────────────────────────────────────────────────────
# CAPTION: Save the current list state to a JSON file
Type "/save /tmp/sll-demo.json"
Enter
Sleep 2s

# ── Switch to strings and generate random values ─────────────────────────────
# CAPTION: Clear all nodes from the list
Type "/clear"
Enter
Sleep 1s

# CAPTION: Switch the list to hold string values instead of integers
Type "/type str"
Enter
Sleep 1s

# CAPTION: Populate the list with 5 random words
Type "/random 5"
Enter
Sleep 2s

# ── Load the saved int session back ─────────────────────────────────────────
# CAPTION: Clear before reloading the saved session
Type "/clear"
Enter
Sleep 1s

# CAPTION: Reload the saved integer session from disk
Type "/load /tmp/sll-demo.json"
Enter
Sleep 2s

# ── Quit ────────────────────────────────────────────────────────────────────
Type "/quit"
Enter
Sleep 1s
