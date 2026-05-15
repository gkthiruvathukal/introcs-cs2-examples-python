import pytest
from data_structures.stack_demo import StackDemo


ITEMS = [10, 20]
FIRST_ITEM = ITEMS[0]
SECOND_ITEM = ITEMS[1]


@pytest.fixture
def stack():
    return StackDemo()


def test_push_and_peek(stack):
    stack.push(FIRST_ITEM)
    stack.push(SECOND_ITEM)
    assert stack.peek() == SECOND_ITEM


def test_pop(stack):
    stack.push(FIRST_ITEM)
    stack.push(SECOND_ITEM)
    assert stack.pop() == SECOND_ITEM
    assert stack.peek() == FIRST_ITEM


def test_is_empty(stack):
    assert stack.is_empty()
    stack.push(FIRST_ITEM)
    assert not stack.is_empty()


def test_size(stack):
    assert stack.size() == 0
    stack.push(FIRST_ITEM)
    stack.push(SECOND_ITEM)
    assert stack.size() == len(ITEMS)


def test_pop_empty(stack):
    with pytest.raises(IndexError):
        stack.pop()


def test_peek_empty(stack):
    with pytest.raises(IndexError):
        stack.peek()
