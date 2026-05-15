# Stack

## Type of Data Structure

A stack is a **dynamic, linear, last-in-first-out (LIFO)** data structure. Elements are added and removed from the same end, usually called the **top**.

## Key Operations and Running Times

| Operation | Method in this repo | Description | Time Complexity |
|---|---|---|---|
| Push | `push(item)` | Add an item to the top of the stack | `O(1)` amortized |
| Pop | `pop()` | Remove and return the top item | `O(1)` |
| Peek | `peek()` | Return the top item without removing it | `O(1)` |
| Empty check | `is_empty()` | Check whether the stack has no items | `O(1)` |
| Size | `size()` | Return the number of items | `O(1)` |

## Implementation

In this repository, `StackDemo` is implemented using Python's built-in `list`.

The top of the stack is the end of the list. `push()` uses `list.append(...)`, and `pop()` uses `list.pop()`. This is the idiomatic Python approach for a simple stack because appending and popping from the end of a list are efficient.

For a language-neutral overview, see [Stack (abstract data type)](https://en.wikipedia.org/wiki/Stack_(abstract_data_type)).

## When to Use It

Use a stack when the most recently added item should be processed first.

Common examples include:

- function call tracking
- undo/redo behavior
- parsing nested expressions
- depth-first search
- matching parentheses or brackets
- backtracking algorithms

## When Not to Use It

Do not use a stack when you need:

- access to arbitrary elements by position
- first-in-first-out behavior
- sorted retrieval
- fast lookup by key
- frequent search through all elements

For FIFO behavior, use a queue. For key-based lookup, use a dictionary or hash map.

## Testing Strategy

The stack tests are in `tests/test_stack_demo.py`. They verify core LIFO behavior and empty-stack boundary cases.

| Behavior Checked | Test Method |
|---|---|
| Pushing items places the newest item on top | `test_push_and_peek` |
| Popping returns the newest item first | `test_pop` |
| `peek()` returns the top item after a pop | `test_pop` |
| `is_empty()` is true initially and false after insertion | `test_is_empty` |
| `size()` reports the correct count | `test_size` |
| Popping from an empty stack raises `IndexError` | `test_pop_empty` |
| Peeking into an empty stack raises `IndexError` | `test_peek_empty` |
