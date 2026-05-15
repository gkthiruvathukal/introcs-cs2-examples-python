# List

## Type of Data Structure

A list is a **dynamic, linear, indexed sequence**. Items keep insertion order and can be accessed by position.

## Key Operations and Running Times

| Operation | Method in this repo | Description | Time Complexity |
|---|---|---|---|
| Add | `add(item)` | Append an item to the end | `O(1)` amortized |
| Remove by value | `remove(item)` | Remove the first matching item | `O(n)` |
| Remove by index | `remove_at(index)` | Remove and return the item at an index | `O(n)` |
| Get | `get(index)` | Return the item at an index | `O(1)` |
| Update | `update(index, new_value)` | Replace the item at an index | `O(1)` |
| Size | `size()` | Return the number of items | `O(1)` |

## Implementation

In this repository, `ListDemo` is implemented using Python's built-in `list`, which is a dynamic array. Random access is fast because elements are stored contiguously, while removals can require shifting later elements.

For a language-neutral overview, see [Dynamic array](https://en.wikipedia.org/wiki/Dynamic_array).

## When to Use It

Use a list when you need ordered data, indexed access, and efficient appends.

Common examples include:

- storing sequences of records
- collecting values before processing
- implementing simple arrays
- preserving insertion order

## When Not to Use It

Do not use a list when you need:

- frequent removals from the front
- fast membership tests on large collections
- key-based lookup
- guaranteed sorted insertion

For frequent front operations, use a deque. For fast lookup, use a set or dictionary.

## Testing Strategy

The list tests are in `tests/test_list_demo.py`. They verify indexed access, mutation, removal, size updates, and out-of-range errors.

| Behavior Checked | Test Method |
|---|---|
| Added items can be retrieved by index | `test_add_and_get` |
| Removing by value removes the expected item | `test_remove_by_value` |
| Removing by index returns and removes the expected item | `test_remove_by_index` |
| Updating by index changes the expected item | `test_update` |
| `size()` tracks insertions and removals | `test_size` |
| Empty/out-of-range index access raises `IndexError` | `test_out_of_range_access` |
