import asyncio

from textual.widgets import Input, RichLog

from data_structures.tui.list_demo_tui import ListDemoTUI


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


def test_list_tui_placeholder_mentions_search():
    app = ListDemoTUI()
    assert "/search" in app.placeholder_text()


def test_list_tui_search_found():
    async def scenario():
        app = ListDemoTUI(max_size=5)
        async with app.run_test() as pilot:
            input_widget = app.query_one(Input)
            input_widget.post_message(Input.Submitted(input_widget, "/append 10 20 30"))
            await pilot.pause()
            input_widget.post_message(Input.Submitted(input_widget, "/search 20"))
            await pilot.pause()
            log = app.query_one(RichLog)
            assert any("found at index 1" in line.text for line in log.lines[-5:])

    asyncio.run(scenario())


def test_list_tui_search_not_found():
    async def scenario():
        app = ListDemoTUI(max_size=5)
        async with app.run_test() as pilot:
            input_widget = app.query_one(Input)
            input_widget.post_message(Input.Submitted(input_widget, "/append 10 20"))
            await pilot.pause()
            input_widget.post_message(Input.Submitted(input_widget, "/search 99"))
            await pilot.pause()
            log = app.query_one(RichLog)
            assert any("not found" in line.text for line in log.lines[-5:])

    asyncio.run(scenario())
