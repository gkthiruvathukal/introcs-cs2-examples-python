# Doubly Linked List TUI

`data_structures/doubly_linked_list_tui.py` is an interactive Textual demo for doubly linked list behavior.

Run it with:

```bash
make run-dll-tui
```

or:

```bash
.venv/bin/python -m data_structures.doubly_linked_list_tui
```

Key behavior:
- the log presents the structure as `None <- ... <-> ... -> None`
- the panel renders boxed nodes with `id`, `data`, `prev`, and `next`
- each node uses a stable label such as `node-3`, so pointer fields can refer to specific nodes
- the panel stays horizontal-only and keeps `head` and `tail` visible when the list grows
- if the full chain is too wide, the middle collapses behind a `...` gap card instead of switching to a vertical layout
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
- `/show-backward` — display values from tail to head
- `/random N`

The default element type is `int`.

Example panel shape:

```text
                     head                                                 tail
           ┌─────────────────┐                           ┌─────────────────┐
           │ id: node-1      │ <-> ... <->              │ id: node-8      │
           │ data: 10        │                           │ data: 80        │
           │ prev: /         │                           │ prev: node-7    │
           │ next: node-2    │                           │ next: /         │
           └─────────────────┘                           └─────────────────┘
```

When the middle is collapsed, scrolling commands move through that hidden middle region while keeping the ends visible.
