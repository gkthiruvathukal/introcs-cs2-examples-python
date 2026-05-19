import asyncio

from textual.widgets import Input, RichLog

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
    assert "/enqueue" in app.placeholder_text()


def test_queue_tui_placeholder_mentions_swap_and_rotate():
    app = QueueDemoTUI()
    placeholder = app.placeholder_text()
    assert "/swap" in placeholder
    assert "/rotate" in placeholder


def test_queue_tui_placeholder_mentions_search():
    app = QueueDemoTUI()
    assert "/search" in app.placeholder_text()


def test_queue_tui_logs_timing_after_submitted_command():
    async def scenario():
        app = QueueDemoTUI(max_size=5)
        async with app.run_test() as pilot:
            input_widget = app.query_one(Input)
            input_widget.post_message(Input.Submitted(input_widget, "/enqueue 5"))
            await pilot.pause()
            log = app.query_one(RichLog)
            assert log.lines[-1].text.startswith("time: ")

    asyncio.run(scenario())


def test_queue_tui_search_found():
    async def scenario():
        app = QueueDemoTUI(max_size=5)
        async with app.run_test() as pilot:
            input_widget = app.query_one(Input)
            input_widget.post_message(Input.Submitted(input_widget, "/enqueue 10 20 30"))
            await pilot.pause()
            input_widget.post_message(Input.Submitted(input_widget, "/search 20"))
            await pilot.pause()
            log = app.query_one(RichLog)
            assert any("found at index 1" in line.text for line in log.lines[-5:])

    asyncio.run(scenario())


def test_queue_tui_search_not_found():
    async def scenario():
        app = QueueDemoTUI(max_size=5)
        async with app.run_test() as pilot:
            input_widget = app.query_one(Input)
            input_widget.post_message(Input.Submitted(input_widget, "/enqueue 10 20"))
            await pilot.pause()
            input_widget.post_message(Input.Submitted(input_widget, "/search 99"))
            await pilot.pause()
            log = app.query_one(RichLog)
            assert any("not found" in line.text for line in log.lines[-5:])

    asyncio.run(scenario())
