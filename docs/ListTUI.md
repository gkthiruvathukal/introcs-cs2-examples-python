# List TUI

`data_structures/list_demo_tui.py` is an interactive Textual demo for indexed list operations.

Run it with:

```bash
make run-list-tui
```

or:

```bash
.venv/bin/python -m data_structures.list_demo_tui
```

Key behavior:
- rows are labeled by numeric index
- long lists keep the first and last rows visible while the middle scrolls
- the shared shell provides `/save`, `/load`, `/undo`, `/redo`, and `/type`

Core commands:
- `/append <value> [more ...]`
- `/insert <index> <value>`
- `/random <n>`
- `/remove-value <value>`
- `/remove-at <index>`
- `/get <index>`
- `/set <index> <value>`

The default element type is `int`.
