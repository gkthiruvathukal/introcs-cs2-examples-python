# Python Data Structures Examples

Educational Python examples for common data structures (CS1/CS2 level). Each data structure has one focused module in `data_structures/`, one test file in `tests/`, and one generated doc in `docs/`.

## Setup

```bash
make install
```

Creates `.venv` and installs dependencies (`pytest`, `networkx`).

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

`stack_demo_tui` launches an interactive Textual TUI (`make run-stack-tui`). Other demo modules do not yet have a `__main__` block, so their `run-*` targets verify a clean import but produce no output.

## All Valid Targets

| Target | Description |
|---|---|
| `make install` | Create `.venv` and install dependencies |
| `make test` | Run the full test suite |
| `make run-<name>` | Import a single demo module |
| `make test-<name>` | Run a single test module with verbose output |

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
| `set` | `set_demo` | `data_structures/set_demo.py` | `tests/test_set_demo.py` |
| `sll` | `singly_linked_list` | `data_structures/singly_linked_list.py` | `tests/test_singly_linked_list.py` |
| `stack` | `stack_demo` | `data_structures/stack_demo.py` | `tests/test_stack_demo.py` |
| `stack-tui` | `stack_demo_tui` | `data_structures/stack_demo_tui.py` | — |
| `trie` | `trie_demo` | `data_structures/trie_demo.py` | `tests/test_trie_demo.py` |
