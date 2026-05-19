from data_structures.tui.singly_linked_list_app import (
    SinglyLinkedListTUI,
    build_horizontal_sll_view,
    build_sll_cards,
    build_sll_snapshots,
    estimate_horizontal_width,
    render_horizontal_sll,
)


def test_singly_linked_list_tui_show_state_text():
    app = SinglyLinkedListTUI(max_size=5)
    app.append_values(app._convert_many(["1", "2", "3"]))

    assert app.get_items() == [1, 2, 3]
    assert app.show_state_text() == "head -> 1 -> 2 -> 3 -> None"


def test_singly_linked_list_tui_restore_snapshot():
    app = SinglyLinkedListTUI()
    app._restore_snapshot(
        {
            "type": "bool",
            "nodes": [
                {"node_id": 4, "node_label": "node-4", "data": True, "next_label": "node-9"},
                {"node_id": 9, "node_label": "node-9", "data": False, "next_label": "/"},
            ],
            "items": [True, False],
        }
    )
    assert app.get_items() == [True, False]
    assert app.demo.node_snapshots()[0]["node_label"] == "node-4"


def test_sll_snapshot_builder_inserts_gap_markers():
    snapshots = build_sll_snapshots(
        [
            {"node_id": 1, "node_label": "node-1", "data": 10, "next_label": "node-4"},
            {"node_id": 4, "node_label": "node-4", "data": 40, "next_label": "/"},
        ],
        [0, 3],
        4,
    )

    assert snapshots[0]["kind"] == "node"
    assert snapshots[1] == {"kind": "gap", "hidden_count": 2}
    assert snapshots[2]["kind"] == "node"


def test_horizontal_view_collapses_middle_when_width_is_limited():
    cards = build_sll_cards(
        build_sll_snapshots(
            [
                {"node_id": 1, "node_label": "node-1", "data": 1, "next_label": "node-2"},
                {"node_id": 2, "node_label": "node-2", "data": 2, "next_label": "node-3"},
                {"node_id": 3, "node_label": "node-3", "data": 3, "next_label": "/"},
            ],
            [0, 1, 2],
            3,
        )
    )
    tight_width = estimate_horizontal_width(cards) - 1
    view = build_horizontal_sll_view(
        [
            {"node_id": 1, "node_label": "node-1", "data": 1, "next_label": "node-2"},
            {"node_id": 2, "node_label": "node-2", "data": 2, "next_label": "node-3"},
            {"node_id": 3, "node_label": "node-3", "data": 3, "next_label": "/"},
        ],
        tight_width,
        0,
    )
    assert view["hidden_after"] > 0 or view["hidden_before"] > 0


def test_sll_renderers_show_head_marker_and_forward_arrows():
    cards = build_sll_cards(
        build_sll_snapshots(
            [
                {"node_id": 1, "node_label": "node-1", "data": 1, "next_label": "node-2"},
                {"node_id": 2, "node_label": "node-2", "data": 2, "next_label": "/"},
            ],
            [0, 1],
            2,
        )
    )
    horizontal = render_horizontal_sll(cards)

    assert "head" in horizontal[0]
    assert any(" -> " in line for line in horizontal)
    assert all("<->" not in line for line in horizontal)


def test_horizontal_view_scrolls_hidden_middle():
    items = [
        {
            "node_id": i,
            "node_label": f"node-{i}",
            "data": i,
            "next_label": f"node-{i + 1}" if i < 8 else "/",
        }
        for i in range(1, 9)
    ]
    wide = 120
    view0 = build_horizontal_sll_view(items, wide, 0)
    view1 = build_horizontal_sll_view(items, wide, 1)
    assert view1["scroll_offset"] >= view0["scroll_offset"]
