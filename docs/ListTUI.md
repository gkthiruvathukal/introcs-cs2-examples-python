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
- `/append VALUE [more ...]`
- `/insert INDEX VALUE`
- `/remove-value VALUE`
- `/remove-at INDEX`
- `/search VALUE`
- `/get INDEX`
- `/set INDEX VALUE`
- `/random N`

The default element type is `int`.
