# Set

## Type of Data Structure

A set is a **dynamic, unordered collection of unique values**. It is optimized for membership and mathematical set operations.

## Key Operations and Running Times

| Operation | Method in this repo | Description | Time Complexity |
|---|---|---|---|
| Add | `add(item)` | Add a unique item | `O(1)` average |
| Remove | `remove(item)` | Remove an existing item | `O(1)` average |
| Union | `union(other_set)` | Return all values from both sets | `O(n + m)` |
| Intersection | `intersection(other_set)` | Return values present in both sets | `O(min(n, m))` average |
| Difference | `difference(other_set)` | Return values in this set but not the other | `O(n)` average |
| Subset check | `is_subset(other_set)` | Check whether this set is contained in another | `O(n)` average |
| Size | `size()` | Return the number of values | `O(1)` |

## Implementation

In this repository, `SetDemo` is implemented using Python's built-in `set`, which is hash-table based. Values must be hashable, and duplicates are automatically collapsed.

For a language-neutral overview, see [Set (abstract data type)](https://en.wikipedia.org/wiki/Set_(abstract_data_type)).

## When to Use It

Use a set when uniqueness and membership matter more than order.

Common examples include:

- removing duplicates
- membership filtering
- tracking visited nodes
- comparing groups of values
- implementing union/intersection/difference logic

## When Not to Use It

Do not use a set when you need:

- duplicate values
- stable positional order
- key-value associations
- sorted retrieval without extra work

For key-value associations, use a dictionary. For ordered duplicates, use a list.

## Testing Strategy

The set tests are in `tests/test_set_demo.py`. They verify uniqueness-oriented operations, set algebra, size tracking, subset checks, and missing-item errors.

| Behavior Checked | Test Method |
|---|---|
| Adding values changes the set size | `test_add_and_size` |
| Removing an existing value changes the size | `test_remove` |
| Removing a missing value raises `KeyError` | `test_remove` |
| Union returns all values from both sets | `test_union` |
| Intersection returns shared values | `test_intersection` |
| Difference returns values only in the left set | `test_difference` |
| Subset checks return true and false correctly | `test_is_subset` |
