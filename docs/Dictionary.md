# Dictionary

## Type of Data Structure

A dictionary is a **dynamic, associative, key-value** data structure. Values are stored and retrieved by unique keys.

## Key Operations and Running Times

| Operation | Method in this repo | Description | Time Complexity |
|---|---|---|---|
| Add/update | `add(key, value)` | Store or replace a key-value pair | `O(1)` average |
| Remove | `remove(key)` | Remove a key-value pair by key | `O(1)` average |
| Get | `get(key)` | Retrieve a value by key | `O(1)` average |
| Keys | `keys()` | Return all keys as a list | `O(n)` |
| Values | `values()` | Return all values as a list | `O(n)` |
| Size | `size()` | Return the number of pairs | `O(1)` |

## Implementation

In this repository, `DictionaryDemo` is implemented using Python's built-in `dict`, a hash table. Hashing gives efficient average-case insertion, lookup, update, and removal by key.

For a language-neutral overview, see [Hash table](https://en.wikipedia.org/wiki/Hash_table).

## When to Use It

Use a dictionary when each value should be found by a meaningful key.

Common examples include:

- mapping usernames to profiles
- counting frequencies
- storing configuration by name
- indexing records by ID
- memoization caches

## When Not to Use It

Do not use a dictionary when you need:

- duplicate keys
- position-based access
- sorted traversal by default
- first-in-first-out processing

For ordered numeric positions, use a list. For unique values without associated data, use a set.

## Testing Strategy

The dictionary tests are in `tests/test_dictionary_demo.py`. They verify add/update behavior, key lookup, removal, key/value views, size tracking, and missing-key errors.

| Behavior Checked | Test Method |
|---|---|
| Added values can be retrieved by key | `test_add_and_get` |
| Adding an existing key updates its value | `test_update_value` |
| Removing a key deletes only that key | `test_remove` |
| `keys()` returns the stored keys | `test_keys` |
| `values()` returns the stored values | `test_values` |
| `size()` reports the number of entries | `test_size` |
| Removing a missing key raises `KeyError` | `test_remove_key_not_found` |
