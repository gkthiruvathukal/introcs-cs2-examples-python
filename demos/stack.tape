# Stack — interactive demo
# Run from project root:  vhs demos/stack.tape

Output demos/stack.mp4

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
Type ".venv/bin/python -m data_structures.tui.stack_app"
Enter
Sleep 4s

# ── Build stack: 10 at bottom, 50 at top ────────────────────────────────────
# CAPTION: Push 5 values onto the stack
Type "/push 10 20 30 40 50"
Enter
Sleep 2s

# ── Inspect ─────────────────────────────────────────────────────────────────
# CAPTION: Peek at the top stack value
Type "/peek"
Enter
Sleep 2s

# CAPTION: Inspect the top stack position; equivalent of peek
Type "/at 0"
Enter
Sleep 2s

# CAPTION: Inspect a deeper stack position
Type "/at 2"
Enter
Sleep 2s

# ── Stack manipulation ───────────────────────────────────────────────────────
# CAPTION: Duplicate the top stack value
Type "/dup"
Enter
Sleep 2s

# CAPTION: Pop the top stack value
Type "/pop"
Enter
Sleep 2s

# CAPTION: Swap the top two stack values
Type "/swap"
Enter
Sleep 2s

# CAPTION: Rotate the top three stack values
Type "/rotate"
Enter
Sleep 2s

# ── Pop a couple ─────────────────────────────────────────────────────────────
# CAPTION: Pop the top value again
Type "/pop"
Enter
Sleep 2s

# CAPTION: Pop one more stack value
Type "/pop"
Enter
Sleep 2s

# ── Undo / redo ─────────────────────────────────────────────────────────────
# CAPTION: Undo the previous change
Type "/undo"
Enter
Sleep 2s

# CAPTION: Undo one more change
Type "/undo"
Enter
Sleep 2s

# CAPTION: Redo the last undone change
Type "/redo"
Enter
Sleep 2s

# ── Save current state ───────────────────────────────────────────────────────
# CAPTION: Save the current stack session
Type "/save /tmp/stack-demo.json"
Enter
Sleep 2s

# ── Switch to strings and generate random values ─────────────────────────────
# CAPTION: Clear the stack
Type "/clear"
Enter
Sleep 1s

# CAPTION: Enable the stack to allow string values
Type "/type str"
Enter
Sleep 1s

# CAPTION: Generate 5 random string stack values
Type "/random 5"
Enter
Sleep 2s

# ── Load the saved int session back ─────────────────────────────────────────
# CAPTION: Clear before loading the saved session
Type "/clear"
Enter
Sleep 1s

# CAPTION: Load the saved integer session
Type "/load /tmp/stack-demo.json"
Enter
Sleep 2s

# ── Quit ────────────────────────────────────────────────────────────────────
Type "/quit"
Enter
Sleep 1s
