# Heap

## Type of Data Structure

A heap is a **dynamic, tree-shaped priority data structure**. This repository uses a min-heap, where the smallest item has the highest priority.

## Key Operations and Running Times

| Operation | Method in this repo | Description | Time Complexity |
|---|---|---|---|
| Insert | `insert(item)` | Add an item to the heap | `O(log n)` |
| Remove minimum | `remove_min()` | Remove and return the smallest item | `O(log n)` |
| Peek minimum | `peek_min()` | Return the smallest item without removing it | `O(1)` |
| Heap sort | `heap_sort(items)` | Return the items in sorted order | `O(n log n)` |
| Size | `size()` | Return the number of items | `O(1)` |

## Implementation

In this repository, `HeapDemo` is implemented using Python's `heapq` module over a list. `heapq` maintains the heap property but does not expose a separate heap object.

For a language-neutral overview, see [Heap (data structure)](https://en.wikipedia.org/wiki/Heap_(data_structure)).

## When to Use It

Use a heap when you repeatedly need the smallest or highest-priority item.

Common examples include:

- priority queues
- scheduling
- Dijkstra-style graph algorithms
- top-k selection
- heap sort

## When Not to Use It

Do not use a heap when you need:

- fast search for arbitrary values
- sorted iteration without removing items
- indexed random access
- key-value lookup

For full sorted order, sort a list. For key-based lookup, use a dictionary.

## Testing Strategy

The heap tests are in `tests/test_heap_demo.py`. They verify min-heap behavior, heap sort, size tracking, and empty-heap errors.

| Behavior Checked | Test Method |
|---|---|
| Insertions expose the smallest item at the top | `test_insert_and_peek_min` |
| Removing the minimum returns the smallest item | `test_remove_min` |
| The next smallest item becomes visible after removal | `test_remove_min` |
| Heap sort returns items in ascending order | `test_heap_sort` |
| `size()` reports inserted item count | `test_size` |
| Removing from an empty heap raises `IndexError` | `test_remove_min_empty` |
| Peeking into an empty heap raises `IndexError` | `test_peek_min_empty` |
