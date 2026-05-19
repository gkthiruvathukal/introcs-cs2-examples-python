# Singly Linked List TUI

`data_structures/tui/singly_linked_list_tui.py` is an interactive Textual demo for head-to-tail linked-list behavior.

Run it with:

```bash
make run-sll-tui
```

or:

```bash
.venv/bin/python -m data_structures.tui.singly_linked_list_tui
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
- `/append VALUE [more ...]` — add one or more values at the tail
- `/insert-at INDEX VALUE` — insert before position (0 = new head)
- `/insert-after NODE-ID VALUE` — insert after the node with that id
- `/insert-before NODE-ID VALUE` — insert before the node with that id
- `/remove-value VALUE` — remove the first matching node
- `/remove-at INDEX` — remove the node at position index
- `/remove-node NODE-ID` — remove the node with that id
- `/search VALUE` — search for a value; reports index and node-id when found
- `/at INDEX` — inspect the node at zero-based offset from the head
- `/random N`

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
