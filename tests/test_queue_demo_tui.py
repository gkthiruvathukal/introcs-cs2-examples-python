from data_structures.queue_demo_tui import QueueDemoTUI


def test_queue_tui_append_snapshot_and_restore():
    app = QueueDemoTUI(max_size=5)
    app.append_values(app._convert_many(["1", "2"]))

    snapshot = app._snapshot_state()
    assert snapshot == {"type": "int", "items": [1, 2]}

    app._restore_snapshot({"type": "int", "items": [3, 4]})
    assert app.get_items() == [3, 4]
    assert app.show_state_text() == "front → back: [3, 4]"


def test_queue_tui_placeholder_mentions_enqueue():
    app = QueueDemoTUI()
    assert "/enqueue <v...>" in app.placeholder_text()


def test_queue_tui_placeholder_mentions_swap_and_rotate():
    app = QueueDemoTUI()
    placeholder = app.placeholder_text()
    assert "/swap" in placeholder
    assert "/rotate" in placeholder
