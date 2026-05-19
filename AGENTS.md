# Repository Guidelines

## Project Structure & Module Organization

This repository contains Python examples for common data structures. Source code lives in `data_structures/`, with one demonstration module per topic, such as `stack_demo.py`, `binary_search_tree_demo.py`, and `trie_demo.py`. Tests live in `tests/` and mirror the module names with `test_<module>.py`. Shared sample input currently lives in `data/`, including `data/words.txt` for trie-related examples. `run_tests.py` delegates to pytest for the full test suite.

## Build, Test, and Development Commands

- `python3 -m venv .venv`: create the local virtual environment.
- `.venv/bin/python -m pip install -r requirements.txt`: install `networkx`, `pytest`, and pytest dependencies.
- `.venv/bin/pytest`: discover and run all tests under `tests/`.
- `.venv/bin/pytest tests/test_stack_demo.py -v`: run one test module with verbose output.
- `.venv/bin/python run_tests.py`: run the compatibility test harness, which invokes pytest.

No separate build step is required.

## Coding Style & Naming Conventions

Use standard Python style with 4-space indentation. Keep modules focused on one data structure or concept. Name implementation files with lowercase snake case ending in `_demo.py` when they are demonstration classes. Class names should use PascalCase, for example `StackDemo` or `GraphDemo`. Test files should use plain pytest functions and fixtures. Prefer clear method names such as `push`, `pop`, `is_empty`, and `size`; avoid abbreviations unless they are conventional.

## Testing Guidelines

The project uses pytest. Add or update tests whenever behavior changes. Match each source module with a corresponding `tests/test_<module>.py` file. Test functions must start with `test_` so discovery finds them. Use `pytest.raises(...)` for expected exceptions, including Python's built-in `RecursionError` where recursive demos can exceed the interpreter recursion limit. Keep tests data-driven with shared constants or helpers when expected sizes and values derive from setup data.

## Commit & Pull Request Guidelines

The current history uses short, direct commit messages such as `Initial commit` and `Initial catalog of data structures`. Continue using concise imperative or descriptive summaries, for example `Add binary search tree demo` or `Fix trie prefix lookup`.

Pull requests should include a brief description, the data structures or tests changed, and the test command run. Link related issues when available. Screenshots are not required for this repository unless future documentation or visual assets are added.

## TUI Architecture

Several data structures have an interactive terminal UI built with [Textual](https://textual.textualize.io). There are two implementation patterns in use.

### Standalone TUI (`stack_demo_tui.py`)

`stack_demo_tui.py` is self-contained: it defines its own `StackDemo` model, panel widget, and full command dispatcher without inheriting from any shared base class. All future shared-base improvements do not automatically reach the stack TUI unless it is later refactored to inherit from `BaseLinearStructureTUI`.

### Base-class TUIs (`tui_common.py`)

All other linear-structure TUIs inherit from `BaseLinearStructureTUI` in `data_structures/tui_common.py`. The base class provides:

- the Textual widget layout (`LinearPanel`, `RichLog`, `Input`, `Header`, `Footer`)
- the shared command dispatcher (`_dispatch`) covering `/random`, `/clear`, `/save`, `/load`, `/undo`, `/redo`, `/show`, `/type`, scroll commands, and `/help`
- per-command timing logged after each submission
- undo/redo via snapshot dicts
- type-constraint enforcement across all push paths

Subclasses override:

- `STRUCTURE_NAME` — display name shown in the panel header
- `START_LABEL` / `END_LABEL` — positional labels for the first and last items
- `get_items()`, `append_values()`, `clear_structure()`, `replace_items()` — structure-specific mutation
- `handle_structure_command()` — returns `True` if the verb was handled, `False` to fall through to the base dispatcher
- `help_lines()` and `placeholder_text()` — structure-specific command hints

### Help Text Conventions

`/help` output is divided into two sections: data-structure-specific commands first (under a `--- <StructureName> ---` heading), then common commands (under `--- Common ---`). Command verbs are wrapped in `[cyan]...[/cyan]` Rich markup. Argument placeholders use plain UPPERCASE names outside the markup span (e.g., `[cyan]/enqueue[/cyan] VALUE`) to avoid Rich's syntax highlighter colorizing them.

### Common Operations Across TUIs

All TUIs support `/search VALUE`, which calls `find()` on the underlying demo object and logs either `found at index N` or `not found`. For linked-list TUIs (`SinglyLinkedListTUI`, `DoublyLinkedListTUI`), `/search` additionally reports the node-id.

The linked-list TUIs also expose positional and node-id–based insert/remove commands:

- `/insert-at INDEX VALUE`, `/insert-after NODE-ID VALUE`, `/insert-before NODE-ID VALUE`
- `/remove-at INDEX`, `/remove-node NODE-ID`, `/remove-value VALUE`

## Agent-Specific Instructions

Keep changes small and educational. Preserve the lightweight pytest workflow unless a task explicitly calls for broader tooling. When adding recursive algorithms, rely on Python's normal recursion behavior and add an explicit-stack iterative alternative when it has teaching value.
