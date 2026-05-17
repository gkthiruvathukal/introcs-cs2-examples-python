import asyncio

from textual.widgets import Input

from data_structures.doubly_linked_list_tui import (
    DoublyLinkedListTUI,
    build_dll_cards,
    build_horizontal_dll_view,
    build_dll_snapshots,
    estimate_horizontal_width,
    render_horizontal_dll,
)


def test_doubly_linked_list_tui_show_state_text():
    app = DoublyLinkedListTUI(max_size=5)
    app.append_values(app._convert_many(["1", "2"]))

    assert app.get_items() == [1, 2]
    assert app.show_state_text() == "None <- 1 <-> 2 -> None"


def test_doubly_linked_list_tui_restore_snapshot():
    app = DoublyLinkedListTUI()
    app._restore_snapshot(
        {
            "type": "str",
            "nodes": [
                {"node_id": 4, "node_label": "node-4", "data": "left", "prev_label": "/", "next_label": "node-9"},
                {"node_id": 9, "node_label": "node-9", "data": "right", "prev_label": "node-4", "next_label": "/"},
            ],
            "items": ["left", "right"],
        }
    )
    assert app.get_items() == ["left", "right"]
    assert app.demo.node_snapshots()[0]["node_label"] == "node-4"


def test_dll_snapshot_builder_inserts_gap_markers():
    snapshots = build_dll_snapshots(
        [
            {"node_id": 1, "node_label": "node-1", "data": 10, "prev_label": "/", "next_label": "node-4"},
            {"node_id": 4, "node_label": "node-4", "data": 40, "prev_label": "node-1", "next_label": "/"},
        ],
        [0, 3],
        4,
    )

    assert snapshots[0]["kind"] == "node"
    assert snapshots[1] == {"kind": "gap", "hidden_count": 2}
    assert snapshots[2]["kind"] == "node"


def test_horizontal_view_collapses_middle_when_width_is_limited():
    cards = build_dll_cards(
        build_dll_snapshots(
            [
                {"node_id": 1, "node_label": "node-1", "data": 1, "prev_label": "/", "next_label": "node-2"},
                {"node_id": 2, "node_label": "node-2", "data": 2, "prev_label": "node-1", "next_label": "node-3"},
                {"node_id": 3, "node_label": "node-3", "data": 3, "prev_label": "node-2", "next_label": "/"},
            ],
            [0, 1, 2],
            3,
        )
    )
    tight_width = estimate_horizontal_width(cards) - 1
    view = build_horizontal_dll_view(
        [
            {"node_id": 1, "node_label": "node-1", "data": 1, "prev_label": "/", "next_label": "node-2"},
            {"node_id": 2, "node_label": "node-2", "data": 2, "prev_label": "node-1", "next_label": "node-3"},
            {"node_id": 3, "node_label": "node-3", "data": 3, "prev_label": "node-2", "next_label": "/"},
        ],
        tight_width,
        0,
    )
    assert view["hidden_after"] > 0 or view["hidden_before"] > 0


def test_dll_renderers_show_head_and_tail_markers():
    cards = build_dll_cards(
        build_dll_snapshots(
            [
                {"node_id": 1, "node_label": "node-1", "data": 1, "prev_label": "/", "next_label": "node-2"},
                {"node_id": 2, "node_label": "node-2", "data": 2, "prev_label": "node-1", "next_label": "/"},
            ],
            [0, 1],
            2,
        )
    )
    horizontal = render_horizontal_dll(cards)

    assert "head" in horizontal[0]
    assert "tail" in horizontal[0]
    assert any("<->" in line for line in horizontal)


def test_horizontal_view_scrolls_hidden_middle():
    items = [
        {"node_id": i, "node_label": f"node-{i}", "data": i, "prev_label": f"node-{i-1}" if i > 1 else "/", "next_label": f"node-{i+1}" if i < 8 else "/"}
        for i in range(1, 9)
    ]
    wide = 120
    view0 = build_horizontal_dll_view(items, wide, 0)
    view1 = build_horizontal_dll_view(items, wide, 1)
    assert view1["scroll_offset"] >= view0["scroll_offset"]


def test_doubly_linked_list_tui_append_submitted_once():
    async def scenario():
        app = DoublyLinkedListTUI(max_size=5)
        async with app.run_test() as pilot:
            input_widget = app.query_one(Input)
            input_widget.post_message(Input.Submitted(input_widget, "/append 5"))
            await pilot.pause()
            assert app.get_items() == [5]
            assert len(app.demo.node_snapshots()) == 1

    asyncio.run(scenario())
