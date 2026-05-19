# Queue

## Type of Data Structure

A queue is a **dynamic, linear, first-in-first-out (FIFO)** data structure. Elements are added at the back and removed from the front.

## Key Operations and Running Times

| Operation | Method in this repo | Description | Time Complexity |
|---|---|---|---|
| Enqueue | `enqueue(item)` | Add an item to the back of the queue | `O(1)` |
| Dequeue | `dequeue()` | Remove and return the front item | `O(1)` |
| Peek | `peek()` | Return the front item without removing it | `O(1)` |
| Find | `find(item)` | Return the index of the first match, or `None` | `O(n)` |
| At | `at(index)` | Return the value at zero-based offset from the front | `O(1)` |
| Empty check | `is_empty()` | Check whether the queue has no items | `O(1)` |
| Size | `size()` | Return the number of items | `O(1)` |

## Implementation

In this repository, `QueueDemo` is implemented using Python's `collections.deque`.

The back of the queue uses `deque.append(...)`, and the front uses `deque.popleft()`. This avoids the `O(n)` cost of removing from the front of a Python `list`.

For a language-neutral overview, see [Queue (abstract data type)](https://en.wikipedia.org/wiki/Queue_(abstract_data_type)).

## When to Use It

Use a queue when items should be processed in the same order they arrive.

Common examples include:

- task scheduling
- breadth-first search
- print queues
- request handling
- producer-consumer workflows

## When Not to Use It

Do not use a queue when you need:

- last-in-first-out behavior
- indexed access to arbitrary elements
- sorted retrieval
- fast lookup by key

For LIFO behavior, use a stack. For key-based lookup, use a dictionary or hash map.

## Testing Strategy

The queue tests are in `tests/test_queue_demo.py`. They verify FIFO behavior and empty-queue boundary cases.

| Behavior Checked | Test Method |
|---|---|
| Enqueuing items keeps the oldest item at the front | `test_enqueue_and_peek` |
| Dequeuing returns the oldest item first | `test_dequeue` |
| `peek()` returns the new front after a dequeue | `test_dequeue` |
| `is_empty()` is true initially and false after insertion | `test_is_empty` |
| `size()` reports the correct count | `test_size` |
| Dequeuing from an empty queue raises `IndexError` | `test_dequeue_empty` |
| Peeking into an empty queue raises `IndexError` | `test_peek_empty` |
| `find` returns the index of an existing item | `test_find_returns_index_of_existing_item` |
| `find` returns `None` when not found | `test_find_returns_none_when_not_found` |
| `find` returns the first matching index | `test_find_returns_first_match` |
