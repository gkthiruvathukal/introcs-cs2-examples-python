# Python Data Structures Examples

Educational Python examples for common data structures (CS1/CS2 level). Each data structure has one focused module in `data_structures/`, one test file in `tests/`, and one generated doc in `docs/`.

## Setup

```bash
make install
```

Creates `.venv` and installs dependencies (`pytest`, `networkx`, `textual`).

## Running Tests

```bash
# All tests
make test

# One module (short alias)
make test-stack
```

## Running Demo Modules

```bash
make run-stack
```

The repo includes interactive Textual TUIs for six data structures. Launch any of them with a dedicated `make run-*-app` target:

```bash
make run-stack-app
make run-queue-app
make run-deque-app
make run-list-app
make run-sll-app
make run-dll-app
```

You can also run a TUI directly:

```bash
.venv/bin/python -m data_structures.tui.stack_app
```

Non-TUI demo modules contain only class definitions, so their `make run-<name>` targets verify a clean import but produce no output.

For walkthroughs of the interactive apps, see:
- `docs/StackTUI.md`
- `docs/QueueTUI.md`
- `docs/DequeTUI.md`
- `docs/ListTUI.md`
- `docs/SinglyLinkedListTUI.md`
- `docs/DoublyLinkedListTUI.md`

## Producing Demo Videos

Demo tapes live in `demos/`. Each TUI has a dark-theme tape and a light-theme tape. Generating the videos requires [vhs](https://github.com/charmbracelet/vhs).

Produce videos for one TUI (dark + light):

```bash
make demo-stack
make demo-queue
make demo-deque
make demo-list
make demo-sll
make demo-dll
```

Produce all videos at once:

```bash
make demo-all
```

Individual tape variants are also available, for example `make demo-stack-dark` or `make demo-dll-light`. Generated `.mp4` files are written to `demos/`.

## All Valid Targets

| Target | Description |
|---|---|
| `make install` | Create `.venv` and install dependencies |
| `make test` | Run the full test suite |
| `make run-<name>` | Import a single non-TUI demo module |
| `make run-<name>-app` | Launch a TUI app interactively |
| `make test-<name>` | Run a single test module with verbose output |
| `make demo-<name>` | Produce dark+light demo videos for one TUI (requires [vhs](https://github.com/charmbracelet/vhs)) |
| `make demo-all` | Produce demo videos for all six TUIs |

Valid `<name>` values (short alias or full name both work):

| Short alias | Full name | Source | Test |
|---|---|---|---|
| `bst` | `binary_search_tree_demo` | `data_structures/binary_search_tree_demo.py` | `tests/test_binary_search_tree_demo.py` |
| `deque` | `deque_demo` | `data_structures/deque_demo.py` | `tests/test_deque_demo.py` |
| `dict` | `dictionary_demo` | `data_structures/dictionary_demo.py` | `tests/test_dictionary_demo.py` |
| `dll` | `doubly_linked_list` | `data_structures/doubly_linked_list.py` | `tests/test_doubly_linked_list.py` |
| `graph` | `graph_demo` | `data_structures/graph_demo.py` | `tests/test_graph_demo.py` |
| `heap` | `heap_demo` | `data_structures/heap_demo.py` | `tests/test_heap_demo.py` |
| `list` | `list_demo` | `data_structures/list_demo.py` | `tests/test_list_demo.py` |
| `networkx` | `networkx_graph_demo` | `data_structures/networkx_graph_demo.py` | `tests/test_networkx_graph_demo.py` |
| `queue` | `queue_demo` | `data_structures/queue_demo.py` | `tests/test_queue_demo.py` |
| `queue-app` | `queue_app` | `data_structures/tui/queue_app.py` | `tests/test_queue_app.py` |
| `set` | `set_demo` | `data_structures/set_demo.py` | `tests/test_set_demo.py` |
| `sll` | `singly_linked_list` | `data_structures/singly_linked_list.py` | `tests/test_singly_linked_list.py` |
| `sll-app` | `singly_linked_list_app` | `data_structures/tui/singly_linked_list_app.py` | `tests/test_singly_linked_list_app.py` |
| `stack` | `stack_demo` | `data_structures/stack_demo.py` | `tests/test_stack_demo.py` |
| `stack-app` | `stack_app` | `data_structures/tui/stack_app.py` | `tests/test_stack_app.py` |
| `deque-app` | `deque_app` | `data_structures/tui/deque_app.py` | `tests/test_deque_app.py` |
| `list-app` | `list_app` | `data_structures/tui/list_app.py` | `tests/test_list_app.py` |
| `dll-app` | `doubly_linked_list_app` | `data_structures/tui/doubly_linked_list_app.py` | `tests/test_doubly_linked_list_app.py` |
| `trie` | `trie_demo` | `data_structures/trie_demo.py` | `tests/test_trie_demo.py` |
