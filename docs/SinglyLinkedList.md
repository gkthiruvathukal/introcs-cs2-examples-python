# Singly Linked List

## Type of Data Structure

A singly linked list is a **dynamic, linear, pointer-linked** data structure. Each node stores data and a reference to the next node.

## Key Operations and Running Times

| Operation | Method in this repo | Description | Time Complexity |
|---|---|---|---|
| Insert at tail | `insert(data)` | Add a node to the end of the list | `O(n)` |
| Insert at position | `insert_at(index, data)` | Insert before position (0 = new head) | `O(n)` |
| Insert after node | `insert_after(node_id, data)` | Insert after the node with the given id | `O(n)` |
| Insert before node | `insert_before(node_id, data)` | Insert before the node with the given id | `O(n)` |
| Remove by value | `remove(data)` | Remove the first node with matching data | `O(n)` |
| Remove by position | `remove_at(index)` | Remove the node at zero-based index | `O(n)` |
| Remove by node id | `remove_by_node_id(node_id)` | Remove the node with the given id | `O(n)` |
| Find | `find(data)` | Return `(index, node_id)` of the first match, or `None` | `O(n)` |
| Search | `search(data)` | Check whether a value exists | `O(n)` |
| Size | `size()` | Return the number of nodes | `O(1)` |
| Display | `display()` | Return all values from head to tail | `O(n)` |

## Implementation

In this repository, `SinglyLinkedList` is implemented from simple `Node` objects. Each node has `data` and `next`; the list stores a `head` reference and a cached `_size`.

This implementation is intentionally explicit because linked structures are useful for teaching references, traversal, and node removal.

For a language-neutral overview, see [Linked list](https://en.wikipedia.org/wiki/Linked_list).

## When to Use It

Use a singly linked list when you want to teach or model node-based sequential storage.

Common examples include:

- demonstrating references and traversal
- simple chain-like structures
- low-level implementations of stacks or queues
- insertion/removal when the previous node is already known

## When Not to Use It

Do not use a singly linked list when you need:

- fast indexed access
- cache-friendly iteration
- binary search
- frequent end insertions without a tail reference

In Python application code, a built-in `list` or `collections.deque` is usually a better practical choice.

## Testing Strategy

The singly linked list tests are in `tests/test_singly_linked_list.py`. They verify insertion order, removal, search, positional insert/remove, node-id–based insert/remove, find, and missing-value errors.

| Behavior Checked | Test Method |
|---|---|
| Inserted nodes display in insertion order | `test_insert_and_display` |
| Removing a middle value updates the chain | `test_remove` |
| Existing and missing values are searched correctly | `test_search` |
| `size()` tracks insertions and removals | `test_size` |
| Removing a missing value raises `ValueError` | `test_remove_value_not_found` |
| `remove_at` removes head, tail, and middle nodes | `test_remove_at_*` |
| `remove_by_node_id` removes the correct node | `test_remove_by_node_id_*` |
| `insert_at` inserts at head, tail, and middle | `test_insert_at_*` |
| `insert_after` inserts after middle and tail nodes | `test_insert_after_*` |
| `insert_before` inserts before head and middle nodes | `test_insert_before_*` |
| `find` returns `(index, node_id)` or `None` | `test_find_*` |
