import pytest

from data_structures.list_demo import ListDemo


ITEMS = [10, 20]
UPDATED_ITEM = 30


@pytest.fixture
def list_demo():
    return ListDemo()


def add_items(list_demo, items):
    for item in items:
        list_demo.add(item)


def test_add_and_get(list_demo):
    add_items(list_demo, ITEMS)
    for index, item in enumerate(ITEMS):
        assert list_demo.get(index) == item


def test_remove_by_value(list_demo):
    add_items(list_demo, ITEMS)
    removed_item = ITEMS[0]
    list_demo.remove(removed_item)
    with pytest.raises(IndexError):
        list_demo.get(len(ITEMS) - 1)
    assert list_demo.get(0) == ITEMS[1]


def test_remove_by_index(list_demo):
    add_items(list_demo, ITEMS)
    assert list_demo.remove_at(0) == ITEMS[0]
    assert list_demo.get(0) == ITEMS[1]


def test_update(list_demo):
    add_items(list_demo, ITEMS)
    list_demo.update(0, UPDATED_ITEM)
    assert list_demo.get(0) == UPDATED_ITEM


def test_size(list_demo):
    add_items(list_demo, ITEMS)
    assert list_demo.size() == len(ITEMS)
    list_demo.remove_at(0)
    assert list_demo.size() == len(ITEMS) - 1


def test_out_of_range_access(list_demo):
    with pytest.raises(IndexError):
        list_demo.get(0)
    with pytest.raises(IndexError):
        list_demo.remove_at(0)


def test_insert_and_to_list(list_demo):
    add_items(list_demo, [ITEMS[0]])
    list_demo.insert(1, ITEMS[1])
    assert list_demo.to_list() == ITEMS


def test_clear(list_demo):
    add_items(list_demo, ITEMS)
    list_demo.clear()
    assert list_demo.size() == 0
    assert list_demo.to_list() == []


# find

def test_find_returns_index_of_existing_item(list_demo):
    add_items(list_demo, [10, 20, 30])
    assert list_demo.find(20) == 1


def test_find_returns_none_when_not_found(list_demo):
    add_items(list_demo, ITEMS)
    assert list_demo.find(99) is None


def test_find_returns_first_match(list_demo):
    add_items(list_demo, [10, 20, 10])
    assert list_demo.find(10) == 0
