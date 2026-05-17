from data_structures.list_demo_tui import ListDemoTUI


def test_list_tui_append_and_restore_snapshot():
    app = ListDemoTUI(max_size=5)
    app.append_values(app._convert_many(["1", "2"]))

    assert app.get_items() == [1, 2]
    assert app.show_state_text() == "index → value: [(0, 1), (1, 2)]"

    app._restore_snapshot({"type": "int", "items": [4, 5]})
    assert app.get_items() == [4, 5]


def test_list_tui_position_labels_are_indices():
    app = ListDemoTUI()
    assert app.format_position_label(0, 3, "first", "last") == "0"
    assert app.format_position_label(2, 3, "first", "last") == "2"
