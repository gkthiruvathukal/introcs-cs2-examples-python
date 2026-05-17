from data_structures.deque_demo_tui import DequeDemoTUI, DequePanel


def test_deque_tui_prepend_and_append_preserve_ends():
    app = DequeDemoTUI(max_size=6)
    app.append_values(app._convert_many(["2", "3"]))
    app.prepend_values(app._convert_many(["1"]))

    assert app.get_items() == [1, 2, 3]
    assert app.show_state_text() == "front → back: [1, 2, 3]"


def test_deque_tui_restore_snapshot():
    app = DequeDemoTUI()
    app._restore_snapshot({"type": "str", "items": ["a", "b"]})
    assert app.get_items() == ["a", "b"]


def test_deque_panel_labels_show_displacement_from_both_ends():
    assert DequePanel._format_front_label(0, 4) == "front"
    assert DequePanel._format_front_label(2, 4) == "front+2"
    assert DequePanel._format_front_label(3, 4) == "back"
    assert DequePanel._format_back_label(0, 4) == "front"
    assert DequePanel._format_back_label(1, 4) == "back+2"
    assert DequePanel._format_back_label(3, 4) == "back"
