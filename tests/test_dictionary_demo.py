import pytest

from data_structures.dictionary_demo import DictionaryDemo


ITEMS = {"a": 1, "b": 2}
UPDATED_KEY = "a"
UPDATED_VALUE = 10
MISSING_KEY = "non_existing_key"


@pytest.fixture
def dictionary():
    return DictionaryDemo()


def add_items(dictionary, items):
    for key, value in items.items():
        dictionary.add(key, value)


def test_add_and_get(dictionary):
    add_items(dictionary, ITEMS)
    for key, value in ITEMS.items():
        assert dictionary.get(key) == value


def test_update_value(dictionary):
    dictionary.add(UPDATED_KEY, ITEMS[UPDATED_KEY])
    dictionary.add(UPDATED_KEY, UPDATED_VALUE)
    assert dictionary.get(UPDATED_KEY) == UPDATED_VALUE


def test_remove(dictionary):
    add_items(dictionary, ITEMS)
    dictionary.remove(UPDATED_KEY)
    with pytest.raises(KeyError):
        dictionary.get(UPDATED_KEY)
    remaining_key = next(key for key in ITEMS if key != UPDATED_KEY)
    assert dictionary.get(remaining_key) == ITEMS[remaining_key]


def test_keys(dictionary):
    add_items(dictionary, ITEMS)
    assert set(dictionary.keys()) == set(ITEMS)


def test_values(dictionary):
    add_items(dictionary, ITEMS)
    assert set(dictionary.values()) == set(ITEMS.values())


def test_size(dictionary):
    add_items(dictionary, ITEMS)
    assert dictionary.size() == len(ITEMS)


def test_remove_key_not_found(dictionary):
    with pytest.raises(KeyError):
        dictionary.remove(MISSING_KEY)
