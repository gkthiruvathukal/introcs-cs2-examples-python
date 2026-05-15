import pytest

from data_structures.set_demo import SetDemo


LEFT_ITEMS = {10, 20}
RIGHT_ITEMS = {20, 30}
SUBSET_ITEMS = {10}
REMOVED_ITEM = min(LEFT_ITEMS)
MISSING_ITEM = 100


@pytest.fixture
def sets():
    return SetDemo(), SetDemo()


def add_items(set_demo, items):
    for item in items:
        set_demo.add(item)


def test_add_and_size(sets):
    set1, _ = sets
    add_items(set1, LEFT_ITEMS | RIGHT_ITEMS)
    assert set1.size() == len(LEFT_ITEMS | RIGHT_ITEMS)


def test_remove(sets):
    set1, _ = sets
    add_items(set1, LEFT_ITEMS)
    set1.remove(REMOVED_ITEM)
    assert set1.size() == len(LEFT_ITEMS) - 1
    with pytest.raises(KeyError):
        set1.remove(MISSING_ITEM)


def test_union(sets):
    set1, set2 = sets
    add_items(set1, LEFT_ITEMS)
    add_items(set2, RIGHT_ITEMS)
    assert set1.union(set2) == LEFT_ITEMS | RIGHT_ITEMS


def test_intersection(sets):
    set1, set2 = sets
    add_items(set1, LEFT_ITEMS)
    add_items(set2, RIGHT_ITEMS)
    assert set1.intersection(set2) == LEFT_ITEMS & RIGHT_ITEMS


def test_difference(sets):
    set1, set2 = sets
    add_items(set1, LEFT_ITEMS)
    add_items(set2, RIGHT_ITEMS)
    assert set1.difference(set2) == LEFT_ITEMS - RIGHT_ITEMS


def test_is_subset(sets):
    set1, set2 = sets
    add_items(set1, LEFT_ITEMS)
    add_items(set2, SUBSET_ITEMS)
    assert set2.is_subset(set1)
    assert not set1.is_subset(set2)
