import pytest
from data_structures.queue_demo import QueueDemo


ITEMS = [10, 20]
FIRST_ITEM = ITEMS[0]
SECOND_ITEM = ITEMS[1]


@pytest.fixture
def queue():
    return QueueDemo()


def test_enqueue_and_peek(queue):
    queue.enqueue(FIRST_ITEM)
    queue.enqueue(SECOND_ITEM)
    assert queue.peek() == FIRST_ITEM


def test_dequeue(queue):
    queue.enqueue(FIRST_ITEM)
    queue.enqueue(SECOND_ITEM)
    assert queue.dequeue() == FIRST_ITEM
    assert queue.peek() == SECOND_ITEM


def test_is_empty(queue):
    assert queue.is_empty()
    queue.enqueue(FIRST_ITEM)
    assert not queue.is_empty()


def test_size(queue):
    assert queue.size() == 0
    queue.enqueue(FIRST_ITEM)
    queue.enqueue(SECOND_ITEM)
    assert queue.size() == len(ITEMS)


def test_dequeue_empty(queue):
    with pytest.raises(IndexError):
        queue.dequeue()


def test_peek_empty(queue):
    with pytest.raises(IndexError):
        queue.peek()


def test_at_and_to_list(queue):
    queue.enqueue(FIRST_ITEM)
    queue.enqueue(SECOND_ITEM)
    assert queue.at(0) == FIRST_ITEM
    assert queue.at(1) == SECOND_ITEM
    assert queue.to_list() == ITEMS


def test_clear(queue):
    queue.enqueue(FIRST_ITEM)
    queue.enqueue(SECOND_ITEM)
    queue.clear()
    assert queue.is_empty()
    assert queue.to_list() == []


def test_swap_front_two(queue):
    queue.enqueue(10)
    queue.enqueue(20)
    queue.enqueue(30)
    swapped = queue.swap()
    assert swapped == (20, 10)
    assert queue.to_list() == [20, 10, 30]


def test_swap_requires_two_items(queue):
    queue.enqueue(10)
    with pytest.raises(IndexError):
        queue.swap()


def test_rotate_front_three(queue):
    queue.enqueue(10)
    queue.enqueue(20)
    queue.enqueue(30)
    queue.enqueue(40)
    rotated = queue.rotate()
    assert rotated == [30, 10, 20]
    assert queue.to_list() == [30, 10, 20, 40]


def test_rotate_requires_three_items(queue):
    queue.enqueue(10)
    queue.enqueue(20)
    with pytest.raises(IndexError):
        queue.rotate()
