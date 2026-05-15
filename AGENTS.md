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

## Agent-Specific Instructions

Keep changes small and educational. Preserve the lightweight pytest workflow unless a task explicitly calls for broader tooling. When adding recursive algorithms, rely on Python's normal recursion behavior and add an explicit-stack iterative alternative when it has teaching value.
