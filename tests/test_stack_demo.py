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


def test_clear_removes_all_items(stack):
    stack.push(FIRST_ITEM)
    stack.push(SECOND_ITEM)

    stack.clear()

    assert stack.is_empty()
    assert stack.size() == 0


def test_swap_exchanges_top_two_items(stack):
    stack.push(1)
    stack.push(2)
    stack.push(3)

    swapped = stack.swap()

    assert swapped == (3, 2)
    assert stack.stack == [1, 3, 2]


def test_swap_requires_two_items(stack):
    stack.push(FIRST_ITEM)

    with pytest.raises(IndexError):
        stack.swap()


def test_rotate_moves_third_item_to_top(stack):
    stack.push(1)
    stack.push(2)
    stack.push(3)
    stack.push(4)

    rotated = stack.rotate()

    assert rotated == [3, 4, 2]
    assert stack.stack == [1, 3, 4, 2]


def test_rotate_requires_three_items(stack):
    stack.push(FIRST_ITEM)
    stack.push(SECOND_ITEM)

    with pytest.raises(IndexError):
        stack.rotate()


def test_dup_duplicates_top_item(stack):
    stack.push(FIRST_ITEM)

    duplicated = stack.dup()

    assert duplicated == FIRST_ITEM
    assert stack.stack == [FIRST_ITEM, FIRST_ITEM]


def test_dup_requires_one_item(stack):
    with pytest.raises(IndexError):
        stack.dup()
