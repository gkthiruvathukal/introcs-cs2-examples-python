import pytest

from data_structures.binary_search_tree_demo import BinarySearchTreeDemo


TREE_VALUES = [50, 30, 70, 20, 40, 60, 80]
INORDER_VALUES = sorted(TREE_VALUES)
PREORDER_VALUES = [50, 30, 20, 40, 70, 60, 80]
POSTORDER_VALUES = [20, 40, 30, 60, 80, 70, 50]
LEVEL_ORDER_VALUES = TREE_VALUES


@pytest.fixture
def tree():
    tree = BinarySearchTreeDemo()
    for value in TREE_VALUES:
        tree.insert(value)
    return tree


def test_insert_and_search(tree):
    assert tree.search(50)
    assert tree.search(20)
    assert tree.search(80)
    assert not tree.search(90)


def test_insert_ignores_duplicates(tree):
    tree.insert(30)
    assert tree.size() == len(TREE_VALUES)
    assert tree.inorder() == INORDER_VALUES


def test_find_min_and_max(tree):
    assert tree.find_min() == min(TREE_VALUES)
    assert tree.find_max() == max(TREE_VALUES)


def test_find_min_empty_tree():
    tree = BinarySearchTreeDemo()
    with pytest.raises(ValueError):
        tree.find_min()


def test_find_max_empty_tree():
    tree = BinarySearchTreeDemo()
    with pytest.raises(ValueError):
        tree.find_max()


def test_inorder_traversal(tree):
    assert tree.inorder() == INORDER_VALUES


def test_inorder_iterative_matches_recursive_traversal(tree):
    assert tree.inorder_iterative() == tree.inorder()


def test_preorder_traversal(tree):
    assert tree.preorder() == PREORDER_VALUES


def test_preorder_iterative_matches_recursive_traversal(tree):
    assert tree.preorder_iterative() == tree.preorder()


def test_postorder_traversal(tree):
    assert tree.postorder() == POSTORDER_VALUES


def test_postorder_iterative_matches_recursive_traversal(tree):
    assert tree.postorder_iterative() == tree.postorder()


def test_level_order_traversal(tree):
    assert tree.level_order() == LEVEL_ORDER_VALUES


def test_height_balanced_insertion_order(tree):
    assert tree.height() == 3


def test_height_iterative_matches_recursive_height(tree):
    assert tree.height_iterative() == tree.height()


def test_height_sorted_insertion_order_shows_worst_case():
    tree = BinarySearchTreeDemo()
    values = list(range(1, 8))
    for value in values:
        tree.insert(value)

    assert tree.height() == len(values)
    assert tree.level_order() == values


def test_iterative_traversal_handles_deep_sorted_tree():
    tree = BinarySearchTreeDemo()
    values = list(range(1, 1500))
    for value in values:
        tree.insert(value)

    assert tree.inorder_iterative() == values
    assert tree.height_iterative() == len(values)


def test_recursive_traversal_raises_recursion_error_for_deep_tree(
    temporary_recursion_limit,
):
    values = list(range(1, 350))
    tree = BinarySearchTreeDemo()
    for value in values:
        tree.insert(value)

    temporary_recursion_limit(200)
    with pytest.raises(RecursionError):
        tree.inorder()
    assert tree.inorder_iterative() == values


def test_recursive_height_raises_recursion_error_for_deep_tree(
    temporary_recursion_limit,
):
    values = list(range(1, 350))
    tree = BinarySearchTreeDemo()
    for value in values:
        tree.insert(value)

    temporary_recursion_limit(200)
    with pytest.raises(RecursionError):
        tree.height()
    assert tree.height_iterative() == len(values)


def test_empty_tree_traversals():
    tree = BinarySearchTreeDemo()
    assert tree.inorder() == []
    assert tree.inorder_iterative() == []
    assert tree.preorder() == []
    assert tree.preorder_iterative() == []
    assert tree.postorder() == []
    assert tree.postorder_iterative() == []
    assert tree.level_order() == []
    assert tree.height() == 0
    assert tree.height_iterative() == 0


def test_size_counts_inserted_values(tree):
    assert tree.size() == len(TREE_VALUES)
