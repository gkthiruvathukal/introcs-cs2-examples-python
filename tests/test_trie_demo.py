import pytest

from data_structures.trie_demo import Trie


@pytest.fixture(scope="module")
def trie():
    trie = Trie()
    with open("data/words.txt", "r") as file:
        for word in file.read().splitlines():
            trie.insert(word)
    return trie


def test_search_common_words(trie):
    assert trie.search("apple")
    assert trie.search("banana")
    assert trie.search("orange")
    assert not trie.search("notaword")


def test_starts_with_prefix(trie):
    assert trie.starts_with("app")
    assert trie.starts_with("ban")
    assert not trie.starts_with("xyz")
