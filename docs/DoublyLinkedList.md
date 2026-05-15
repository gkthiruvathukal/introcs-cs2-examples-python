# Doubly Linked List

## Type of Data Structure

A doubly linked list is a **dynamic, linear, bidirectionally linked** data structure. Each node stores data plus references to both the next and previous nodes.

## Key Operations and Running Times

| Operation | Method in this repo | Description | Time Complexity |
|---|---|---|---|
| Insert | `insert(data)` | Add a node to the end of the list | `O(1)` |
| Remove | `remove(data)` | Remove the first node with matching data | `O(n)` |
| Search | `search(data)` | Check whether a value exists | `O(n)` |
| Size | `size()` | Return the number of nodes | `O(1)` |
| Display forward | `display_forward()` | Return values from head to tail | `O(n)` |
| Display backward | `display_backward()` | Return values from tail to head | `O(n)` |

## Implementation

In this repository, `DoublyLinkedList` is implemented from `Node` objects. Each node has `data`, `next`, and `prev`; the list stores `head`, `tail`, and a cached `_size`.

The `tail` reference makes end insertion constant time, and `prev` links make reverse traversal straightforward.

For a language-neutral overview, see [Doubly linked list](https://en.wikipedia.org/wiki/Doubly_linked_list).

## When to Use It

Use a doubly linked list when bidirectional traversal or efficient end insertion is important.

Common examples include:

- browser history models
- undo/redo chains
- ordered navigation in both directions
- teaching node removal with previous links

## When Not to Use It

Do not use a doubly linked list when you need:

- fast random access by index
- compact memory usage
- cache-friendly scans
- key-based lookup

Doubly linked lists use extra references per node, so they are often less practical than arrays or deques in high-level Python code.

## Testing Strategy

The doubly linked list tests are in `tests/test_doubly_linked_list.py`. They verify forward and backward traversal, removal, search, size tracking, and missing-value errors.

| Behavior Checked | Test Method |
|---|---|
| Inserted nodes display from head to tail | `test_insert_and_display_forward` |
| Inserted nodes display from tail to head | `test_display_backward` |
| Removing a middle value updates the list | `test_remove` |
| Existing and missing values are searched correctly | `test_search` |
| `size()` tracks insertions and removals | `test_size` |
| Removing a missing value raises `ValueError` | `test_remove_value_not_found` |
