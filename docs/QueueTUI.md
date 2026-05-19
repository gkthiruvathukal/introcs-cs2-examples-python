# Queue TUI

`data_structures/tui/queue_app.py` is an interactive Textual demo for queue behavior.

Run it with:

```bash
make run-queue-app
```

or:

```bash
.venv/bin/python -m data_structures.tui.queue_app
```

Key behavior:
- values are displayed from `front` to `back`
- when the queue is long, the panel keeps both `front` and `back` visible and scrolls the middle rows
- the app supports `/save`, `/load`, `/undo`, `/redo`, and `/type`

Core commands:
- `/enqueue VALUE [more ...]`
- `/dequeue`
- `/peek`
- `/search VALUE`
- `/at INDEX`
- `/swap`
- `/rotate`
- `/random N`
- `/clear`

The default element type is `int`. Use `/type str`, `/type bool`, or `/type any` to switch conversion behavior.
