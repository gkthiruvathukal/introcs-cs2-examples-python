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
