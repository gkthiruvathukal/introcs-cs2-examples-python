# Trie

## Type of Data Structure

A trie is a **dynamic, tree-based string lookup** data structure. It stores strings by sharing common prefixes across paths from the root.

## Key Operations and Running Times

| Operation | Method in this repo | Description | Time Complexity |
|---|---|---|---|
| Insert | `insert(word)` | Add a word to the trie | `O(k)` |
| Search | `search(word)` | Check whether a full word exists | `O(k)` |
| Prefix search | `starts_with(prefix)` | Check whether any word starts with a prefix | `O(k)` |
| Node traversal | `_find_node(prefix)` | Internal helper for word/prefix lookup | `O(k)` |

`k` is the length of the word or prefix being processed.

## Implementation

In this repository, `Trie` is implemented from `TrieNode` objects. Each node stores a `children` dictionary mapping characters to child nodes and an `is_end_of_word` flag.

The implementation is explicit rather than library-backed because tries are useful for teaching prefix sharing and character-by-character traversal.

For a language-neutral overview, see [Trie](https://en.wikipedia.org/wiki/Trie).

## When to Use It

Use a trie when prefix queries are central to the problem.

Common examples include:

- autocomplete
- spell checking
- prefix filtering
- dictionary word lookup
- routing or token prefix tables

## When Not to Use It

Do not use a trie when:

- only exact lookup is needed
- memory usage must be minimal
- strings do not share many prefixes
- sorted full-string operations are more important than prefix operations

For exact lookup only, a set is usually simpler and more memory efficient.

## Testing Strategy

The trie tests are in `tests/test_trie_demo.py`. They build a trie from `data/words.txt` and verify exact word lookup and prefix lookup.

| Behavior Checked | Test Method |
|---|---|
| Common inserted words can be found | `test_search_common_words` |
| Missing words are not reported as present | `test_search_common_words` |
| Existing prefixes are detected | `test_starts_with_prefix` |
| Missing prefixes are rejected | `test_starts_with_prefix` |
