# Singly Linked List TUI

`data_structures/singly_linked_list_tui.py` is an interactive Textual demo for head-to-tail linked-list behavior.

Run it with:

```bash
make run-sll-tui
```

or:

```bash
.venv/bin/python -m data_structures.singly_linked_list_tui
```

Key behavior:
- the log and `/show` present the structure as `head -> ... -> None`
- the panel renders boxed nodes with `id`, `data`, and `next`
- each node uses a stable label such as `node-3`, so `next` can refer to a specific node
- the panel stays horizontal-only and keeps `head` visible as the list grows
- if the full chain is too wide, the middle collapses behind a `...` gap card
- the log also shows the current horizontal render width and how many nodes are hidden on the left and right
- the shared shell provides `/save`, `/load`, `/undo`, `/redo`, and `/type`

Core commands:
- `/append <value> [more ...]`
- `/random <n>`
- `/remove-value <value>`
- `/search <value>`
- `/at <index>`

The default element type is `int`.

Example panel shape:

```text
                    head
           ┌─────────────────┐ -> ... -> ┌─────────────────┐
           │ id: node-1      │           │ id: node-8      │
           │ data: 10        │           │ data: 80        │
           │ next: node-2    │           │ next: /         │
           └─────────────────┘           └─────────────────┘
```

When the middle is collapsed, scrolling commands move through that hidden middle region while keeping the head-side view anchored.
