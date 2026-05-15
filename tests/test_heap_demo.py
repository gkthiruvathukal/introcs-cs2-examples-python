import pytest
from data_structures.heap_demo import HeapDemo


ITEMS = [10, 20, 5]
SORT_ITEMS = [42, 7, 19, 3, 28, 11]


@pytest.fixture
def heap():
    return HeapDemo()


def test_insert_and_peek_min(heap):
    for item in ITEMS:
        heap.insert(item)
    assert heap.peek_min() == min(ITEMS)


def test_remove_min(heap):
    for item in ITEMS:
        heap.insert(item)
    assert heap.remove_min() == min(ITEMS)
    assert heap.peek_min() == sorted(ITEMS)[1]


def test_heap_sort(heap):
    assert heap.heap_sort(SORT_ITEMS[:]) == sorted(SORT_ITEMS)


def test_size(heap):
    for item in ITEMS:
        heap.insert(item)
    assert heap.size() == len(ITEMS)


def test_remove_min_empty(heap):
    with pytest.raises(IndexError):
        heap.remove_min()


def test_peek_min_empty(heap):
    with pytest.raises(IndexError):
        heap.peek_min()
