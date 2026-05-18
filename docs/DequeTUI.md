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
- the shared TUI shell provides `/save`, `/load`, `/undo`, `/redo`, `/type`, and the full capture pipeline

## Deque-specific commands

| Command | Meaning |
|---|---|
| `/push-front <value> [more ...]` | Add one or more values at the front |
| `/push-back <value> [more ...]` | Add one or more values at the back |
| `/random <n>` | Push `n` random values at the back for the current type |
| `/pop-front` | Remove and return the front value |
| `/pop-back` | Remove and return the back value |
| `/peek-front` | Inspect the front value without removing it |
| `/peek-back` | Inspect the back value without removing it |
| `/set-front <value>` | Replace the front value |
| `/set-back <value>` | Replace the back value |
| `/at <index>` | Inspect the value at zero-based offset from the front |

## Shared commands

These are provided by `BaseLinearStructureTUI` and work the same way across all base-class TUIs:

| Command | Meaning |
|---|---|
| `/clear` | Remove all values |
| `/session <name>` | Set the active session name for frame capture |
| `/capture on` | Start capturing one frame after each command |
| `/capture off` | Suspend frame capture |
| `/video [session] [seconds]` | Build an mp4 from captured frames |
| `/save <path>` | Save current type and contents to a file |
| `/load <path>` | Restore contents from a saved file |
| `/undo` | Restore the previous state |
| `/redo` | Reapply the most recently undone state |
| `/show` / `/print` | Display current contents in the log |
| `/type [int\|float\|str\|bool\|any]` | Get or set the element type constraint |
| `/help` | Show the full command summary |
| `/quit` or `Ctrl+D` | Exit |

## Frame capture

The deque TUI uses the slug `"deque"`. Captured frames land under `.capture/deque/<session>/frames/` and rendered videos land under `.video/deque/<session>.mp4`.

See `docs/CapturePipeline.md` for the full capture workflow.

The default element type is `int`.
