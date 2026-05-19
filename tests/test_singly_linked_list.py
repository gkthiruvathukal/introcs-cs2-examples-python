import pytest

from data_structures.singly_linked_list import SinglyLinkedList


ITEMS = [10, 20, 30]
REMOVED_ITEM = ITEMS[1]
MISSING_ITEM = 40


@pytest.fixture
def linked_list():
    return SinglyLinkedList()


def insert_items(linked_list, items):
    for item in items:
        linked_list.insert(item)


def test_insert_and_display(linked_list):
    insert_items(linked_list, ITEMS)
    assert linked_list.display() == ITEMS


def test_remove(linked_list):
    insert_items(linked_list, ITEMS)
    linked_list.remove(REMOVED_ITEM)
    assert linked_list.display() == [item for item in ITEMS if item != REMOVED_ITEM]


def test_search(linked_list):
    insert_items(linked_list, ITEMS)
    assert linked_list.search(REMOVED_ITEM)
    assert not linked_list.search(MISSING_ITEM)


def test_size(linked_list):
    inserted_items = ITEMS[:2]
    insert_items(linked_list, inserted_items)
    assert linked_list.size() == len(inserted_items)
    linked_list.remove(inserted_items[0])
    assert linked_list.size() == len(inserted_items) - 1


def test_remove_value_not_found(linked_list):
    linked_list.insert(ITEMS[0])
    with pytest.raises(ValueError):
        linked_list.remove(MISSING_ITEM)


def test_to_list_and_clear(linked_list):
    insert_items(linked_list, ITEMS)
    assert linked_list.to_list() == ITEMS
    linked_list.clear()
    assert linked_list.to_list() == []
    assert linked_list.size() == 0


def test_node_snapshots_include_stable_node_labels_and_links(linked_list):
    insert_items(linked_list, ITEMS[:2])
    assert linked_list.node_snapshots() == [
        {"node_id": 1, "node_label": "node-1", "data": 10, "next_label": "node-2"},
        {"node_id": 2, "node_label": "node-2", "data": 20, "next_label": "/"},
    ]


def test_restore_from_snapshots_preserves_node_ids(linked_list):
    linked_list.restore_from_snapshots(
        [
            {"node_id": 4, "node_label": "node-4", "data": "left", "next_label": "node-9"},
            {"node_id": 9, "node_label": "node-9", "data": "right", "next_label": "/"},
        ]
    )

    assert linked_list.to_list() == ["left", "right"]
    assert linked_list.node_snapshots()[0]["node_label"] == "node-4"


# find

def test_find_returns_index_and_node_id(linked_list):
    insert_items(linked_list, ITEMS)
    result = linked_list.find(ITEMS[1])
    assert result is not None
    index, node_id = result
    assert index == 1
    assert node_id == linked_list.node_snapshots()[1]["node_id"]

def test_find_returns_none_when_not_found(linked_list):
    insert_items(linked_list, ITEMS)
    assert linked_list.find(MISSING_ITEM) is None

def test_find_returns_first_match(linked_list):
    linked_list.insert(10)
    linked_list.insert(20)
    linked_list.insert(10)
    index, node_id = linked_list.find(10)
    assert index == 0


# remove_at

def test_remove_at_head(linked_list):
    insert_items(linked_list, ITEMS)
    linked_list.remove_at(0)
    assert linked_list.to_list() == ITEMS[1:]
    assert linked_list.head.data == ITEMS[1]

def test_remove_at_tail(linked_list):
    insert_items(linked_list, ITEMS)
    linked_list.remove_at(len(ITEMS) - 1)
    assert linked_list.to_list() == ITEMS[:-1]

def test_remove_at_middle(linked_list):
    insert_items(linked_list, ITEMS)
    linked_list.remove_at(1)
    assert linked_list.to_list() == [ITEMS[0], ITEMS[2]]

def test_remove_at_out_of_range(linked_list):
    insert_items(linked_list, ITEMS)
    with pytest.raises(IndexError):
        linked_list.remove_at(len(ITEMS))


# remove_by_node_id

def test_remove_by_node_id_head(linked_list):
    insert_items(linked_list, ITEMS)
    node_id = linked_list.node_snapshots()[0]["node_id"]
    linked_list.remove_by_node_id(node_id)
    assert linked_list.head.data == ITEMS[1]

def test_remove_by_node_id_middle(linked_list):
    insert_items(linked_list, ITEMS)
    node_id = linked_list.node_snapshots()[1]["node_id"]
    linked_list.remove_by_node_id(node_id)
    assert linked_list.to_list() == [ITEMS[0], ITEMS[2]]

def test_remove_by_node_id_not_found(linked_list):
    insert_items(linked_list, ITEMS)
    with pytest.raises(ValueError):
        linked_list.remove_by_node_id(9999)


# insert_at

def test_insert_at_head(linked_list):
    insert_items(linked_list, ITEMS)
    linked_list.insert_at(0, 99)
    assert linked_list.to_list() == [99] + ITEMS
    assert linked_list.head.data == 99

def test_insert_at_tail(linked_list):
    insert_items(linked_list, ITEMS)
    linked_list.insert_at(len(ITEMS), 99)
    assert linked_list.to_list() == ITEMS + [99]

def test_insert_at_middle(linked_list):
    insert_items(linked_list, ITEMS)
    linked_list.insert_at(1, 99)
    assert linked_list.to_list() == [ITEMS[0], 99, ITEMS[1], ITEMS[2]]

def test_insert_at_out_of_range(linked_list):
    insert_items(linked_list, ITEMS)
    with pytest.raises(IndexError):
        linked_list.insert_at(len(ITEMS) + 1, 99)


# insert_after

def test_insert_after_middle_node(linked_list):
    insert_items(linked_list, ITEMS)
    node_id = linked_list.node_snapshots()[0]["node_id"]
    linked_list.insert_after(node_id, 99)
    assert linked_list.to_list() == [ITEMS[0], 99, ITEMS[1], ITEMS[2]]

def test_insert_after_tail_node(linked_list):
    insert_items(linked_list, ITEMS)
    node_id = linked_list.node_snapshots()[-1]["node_id"]
    linked_list.insert_after(node_id, 99)
    assert linked_list.to_list() == ITEMS + [99]

def test_insert_after_not_found(linked_list):
    insert_items(linked_list, ITEMS)
    with pytest.raises(ValueError):
        linked_list.insert_after(9999, 99)


# insert_before

def test_insert_before_head_node(linked_list):
    insert_items(linked_list, ITEMS)
    node_id = linked_list.node_snapshots()[0]["node_id"]
    linked_list.insert_before(node_id, 99)
    assert linked_list.to_list() == [99] + ITEMS
    assert linked_list.head.data == 99

def test_insert_before_middle_node(linked_list):
    insert_items(linked_list, ITEMS)
    node_id = linked_list.node_snapshots()[1]["node_id"]
    linked_list.insert_before(node_id, 99)
    assert linked_list.to_list() == [ITEMS[0], 99, ITEMS[1], ITEMS[2]]

def test_insert_before_not_found(linked_list):
    insert_items(linked_list, ITEMS)
    with pytest.raises(ValueError):
        linked_list.insert_before(9999, 99)
