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

Core commands:
- `/push-front <value> [more ...]`
- `/push-back <value> [more ...]`
- `/random <n>` pushes at the back
- `/pop-front`
- `/pop-back`
- `/peek-front`
- `/peek-back`
- `/set-front <value>`
- `/set-back <value>`
- `/at <index>`

The default element type is `int`.
