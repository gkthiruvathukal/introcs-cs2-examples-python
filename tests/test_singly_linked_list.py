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
