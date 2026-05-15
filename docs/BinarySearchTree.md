# Binary Search Tree

## Type of Data Structure

A binary search tree is a **dynamic, hierarchical, ordered** data structure. Each node has at most two children, with smaller values on the left and larger values on the right.

## Key Operations and Running Times

| Operation | Method in this repo | Description | Time Complexity |
|---|---|---|---|
| Insert | `insert(data)` | Add a value if it is not already present | `O(h)` |
| Search | `search(data)` | Check whether a value exists | `O(h)` |
| Minimum | `find_min()` | Return the smallest value | `O(h)` |
| Maximum | `find_max()` | Return the largest value | `O(h)` |
| Traversal | `inorder()`, `preorder()`, `postorder()`, `level_order()` | Return values in traversal order | `O(n)` |
| Iterative traversal | `*_iterative()` methods | Traverse using an explicit stack | `O(n)` |
| Height | `height()`, `height_iterative()` | Return longest root-to-leaf path length | `O(n)` |
| Size | `size()` | Return the number of stored values | `O(1)` |

`h` is the tree height. A balanced tree gives `O(log n)` search and insertion. A sorted insertion order can produce height `n`, making these operations `O(n)`.

## Implementation

In this repository, `BinarySearchTreeDemo` is implemented from `TreeNode` objects with `data`, `left`, and `right` references. Duplicate values are ignored. Recursive traversal methods are provided for clarity, and explicit-stack iterative versions are included to show how to avoid Python's recursion limit.

For a language-neutral overview, see [Binary search tree](https://en.wikipedia.org/wiki/Binary_search_tree).

## When to Use It

Use a binary search tree when you want to teach ordered hierarchical search and traversal.

Common examples include:

- ordered symbol tables
- tree traversal practice
- predecessor/successor concepts
- comparing balanced and worst-case tree shapes

## When Not to Use It

Do not use an unbalanced BST when:

- data may arrive already sorted
- guaranteed worst-case `O(log n)` operations are required
- duplicate-heavy data needs special handling
- Python's built-in structures already solve the lookup problem

For production lookup in Python, prefer `dict`, `set`, or a library-backed balanced structure.

## Testing Strategy

The binary search tree tests are in `tests/test_binary_search_tree_demo.py`. They verify ordered behavior, traversal order, height behavior, duplicate handling, recursion-limit behavior, and empty-tree boundaries.

| Behavior Checked | Test Method |
|---|---|
| Inserted values can be found and missing values are absent | `test_insert_and_search` |
| Duplicate inserts do not change size | `test_insert_ignores_duplicates` |
| Minimum and maximum values are found | `test_find_min_and_max` |
| Empty-tree min/max raise `ValueError` | `test_find_min_empty_tree`, `test_find_max_empty_tree` |
| Recursive traversals return expected orders | `test_inorder_traversal`, `test_preorder_traversal`, `test_postorder_traversal`, `test_level_order_traversal` |
| Iterative traversals match recursive traversals | `test_inorder_iterative_matches_recursive_traversal`, `test_preorder_iterative_matches_recursive_traversal`, `test_postorder_iterative_matches_recursive_traversal` |
| Balanced and sorted insertion heights are visible | `test_height_balanced_insertion_order`, `test_height_sorted_insertion_order_shows_worst_case` |
| Iterative methods handle deep sorted trees | `test_iterative_traversal_handles_deep_sorted_tree` |
| Recursive methods raise `RecursionError` for deep trees | `test_recursive_traversal_raises_recursion_error_for_deep_tree`, `test_recursive_height_raises_recursion_error_for_deep_tree` |
| Empty-tree traversal and height results are correct | `test_empty_tree_traversals` |
| `size()` reports inserted value count | `test_size_counts_inserted_values` |
