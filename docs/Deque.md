# Deque

## Type of Data Structure

A deque is a **dynamic, linear, double-ended queue**. Items can be added, removed, inspected, or updated at both the front and the back.

## Key Operations and Running Times

| Operation | Method in this repo | Description | Time Complexity |
|---|---|---|---|
| Add front | `add_to_front(item)` | Add an item to the front | `O(1)` |
| Add back | `add_to_back(item)` | Add an item to the back | `O(1)` |
| Remove front | `remove_from_front()` | Remove and return the front item | `O(1)` |
| Remove back | `remove_from_back()` | Remove and return the back item | `O(1)` |
| Peek front | `peek_front()` | Return the front item without removing it | `O(1)` |
| Peek back | `peek_back()` | Return the back item without removing it | `O(1)` |
| Update front | `update_front(new_item)` | Replace the front item | `O(1)` |
| Update back | `update_back(new_item)` | Replace the back item | `O(1)` |
| Find | `find(item)` | Return the index of the first match, or `None` | `O(n)` |
| At | `at(index)` | Return the value at zero-based offset from the front | `O(1)` |
| Size | `size()` | Return the number of items | `O(1)` |

## Implementation

In this repository, `DequeDemo` is implemented using Python's `collections.deque`.

The implementation uses `appendleft(...)` and `popleft()` for front operations, and `append(...)` and `pop()` for back operations. This is the standard Python choice when efficient operations are needed at both ends.

For a language-neutral overview, see [Double-ended queue](https://en.wikipedia.org/wiki/Double-ended_queue).

## When to Use It

Use a deque when work may arrive or leave from either end.

Common examples include:

- sliding-window algorithms
- undo/redo history with bounded ends
- implementing both stacks and queues
- palindrome checks
- schedulers that need front and back priority adjustments

## When Not to Use It

Do not use a deque when you need:

- frequent random access by index
- sorted retrieval
- key-based lookup
- stable table-like records

For indexed random access, use a list. For key-based access, use a dictionary.

## Testing Strategy

The deque tests are in `tests/test_deque_demo.py`. They verify both front and back operations, updates, size reporting, and empty-deque errors.

| Behavior Checked | Test Method |
|---|---|
| Adding to both ends preserves front/back positions | `test_add_to_front_and_back` |
| Removing from both ends returns the correct items | `test_remove_from_front_and_back` |
| Updating both ends changes the expected endpoints | `test_update_front_and_back` |
| `size()` reports the correct count | `test_size` |
| Removing from an empty deque raises `IndexError` | `test_remove_from_empty` |
| Updating an empty deque raises `IndexError` | `test_update_empty` |
| `find` returns the index of an existing item | `test_find_returns_index_of_existing_item` |
| `find` returns `None` when not found | `test_find_returns_none_when_not_found` |
| `find` returns the first matching index | `test_find_returns_first_match` |
