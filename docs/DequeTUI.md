# Deque TUI

`data_structures/deque_demo_tui.py` is an interactive Textual demo for a double-ended queue.

Run it with:

```bash
make run-deque-tui
```

or:

```bash
.venv/bin/python -m data_structures.deque_demo_tui
```

Key behavior:
- values are displayed from `front` to `back`
- both ends stay visible in capped views
- the shared TUI shell provides `/save`, `/load`, `/undo`, `/redo`, and `/type`

## Deque-specific commands

| Command | Meaning |
|---|---|
| `/push-front VALUE [more ...]` | Add one or more values at the front |
| `/push-back VALUE [more ...]` | Add one or more values at the back |
| `/random N` | Push `N` random values at the back for the current type |
| `/pop-front` | Remove and return the front value |
| `/pop-back` | Remove and return the back value |
| `/peek-front` | Inspect the front value without removing it |
| `/peek-back` | Inspect the back value without removing it |
| `/set-front VALUE` | Replace the front value |
| `/set-back VALUE` | Replace the back value |
| `/search VALUE` | Search for a value; logs the index if found |
| `/at INDEX` | Inspect the value at zero-based offset from the front |

## Shared commands

These are provided by `BaseLinearStructureTUI` and work the same way across all base-class TUIs:

| Command | Meaning |
|---|---|
| `/clear` | Remove all values |
| `/save PATH` | Save current type and contents to a file |
| `/load PATH` | Restore contents from a saved file |
| `/undo` | Restore the previous state |
| `/redo` | Reapply the most recently undone state |
| `/show` / `/print` | Display current contents in the log |
| `/type [int\|float\|str\|bool\|any]` | Get or set the element type constraint |
| `/help` | Show the full command summary |
| `/quit` or `Ctrl+D` | Exit |

The default element type is `int`.
