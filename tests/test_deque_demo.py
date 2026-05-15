import pytest

from data_structures.deque_demo import DequeDemo


ITEMS = [10, 20]
FRONT_ITEM = ITEMS[0]
BACK_ITEM = ITEMS[1]
UPDATED_FRONT_ITEM = 30
UPDATED_BACK_ITEM = 40


@pytest.fixture
def deque_demo():
    return DequeDemo()


def test_add_to_front_and_back(deque_demo):
    deque_demo.add_to_front(FRONT_ITEM)
    deque_demo.add_to_back(BACK_ITEM)
    assert deque_demo.peek_front() == FRONT_ITEM
    assert deque_demo.peek_back() == BACK_ITEM


def test_remove_from_front_and_back(deque_demo):
    deque_demo.add_to_front(FRONT_ITEM)
    deque_demo.add_to_back(BACK_ITEM)
    assert deque_demo.remove_from_front() == FRONT_ITEM
    assert deque_demo.remove_from_back() == BACK_ITEM


def test_update_front_and_back(deque_demo):
    deque_demo.add_to_front(FRONT_ITEM)
    deque_demo.add_to_back(BACK_ITEM)
    deque_demo.update_front(UPDATED_FRONT_ITEM)
    deque_demo.update_back(UPDATED_BACK_ITEM)
    assert deque_demo.peek_front() == UPDATED_FRONT_ITEM
    assert deque_demo.peek_back() == UPDATED_BACK_ITEM


def test_size(deque_demo):
    deque_demo.add_to_front(FRONT_ITEM)
    deque_demo.add_to_back(BACK_ITEM)
    assert deque_demo.size() == len(ITEMS)


def test_remove_from_empty(deque_demo):
    with pytest.raises(IndexError):
        deque_demo.remove_from_front()
    with pytest.raises(IndexError):
        deque_demo.remove_from_back()


def test_update_empty(deque_demo):
    with pytest.raises(IndexError):
        deque_demo.update_front(1)
    with pytest.raises(IndexError):
        deque_demo.update_back(1)
