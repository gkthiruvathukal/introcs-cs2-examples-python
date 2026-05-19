import asyncio
import random
from pathlib import Path

import pytest
from textual.widgets import Input, RichLog

from data_structures.tui import stack_app as stack_tui_module
from data_structures.tui.stack_app import (
    FLOAT32_MAX,
    FLOAT32_MIN,
    INT32_MAX,
    INT32_MIN,
    StackPanel,
    StackDemo,
    StackDemoTUI,
    build_random_values,
    build_parser,
    build_stack_view,
    clamp_scroll_offset,
    load_session,
    parse_bool,
    parse_push_values,
    parse_single_path,
    restore_stack,
    save_session,
    snapshot_stack,
)


STACK_ITEMS = [1, 2, 3, 4, 5]
WORDS = ["alpha", "beta", "gamma"]


def test_build_stack_view_unlimited_returns_full_stack():
    view = build_stack_view(STACK_ITEMS)

    assert view["visible_items"] == [5, 4, 3, 2, 1]
    assert view["visible_displacements"] == [0, 1, 2, 3, 4]
    assert view["hidden_newer"] == 0
    assert view["hidden_older"] == 0
    assert view["scroll_offset"] == 0


def test_build_stack_view_capped_with_fewer_than_limit_items():
    view = build_stack_view([1, 2, 3], view_top=5)

    assert view["visible_items"] == [3, 2, 1]
    assert view["visible_displacements"] == [0, 1, 2]
    assert view["hidden_newer"] == 0
    assert view["hidden_older"] == 0
    assert view["scroll_offset"] == 0


def test_build_stack_view_capped_with_exact_limit_items():
    view = build_stack_view(STACK_ITEMS, view_top=5)

    assert view["visible_items"] == [5, 4, 3, 2, 1]
    assert view["visible_displacements"] == [0, 1, 2, 3, 4]
    assert view["hidden_newer"] == 0
    assert view["hidden_older"] == 0
    assert view["scroll_offset"] == 0


def test_build_stack_view_pins_top_and_bottom_and_shows_newest_middle_items_first():
    view = build_stack_view(STACK_ITEMS, view_top=3, scroll_offset=0)

    assert view["visible_items"] == [5, 4, 1]
    assert view["visible_displacements"] == [0, 1, 4]
    assert view["hidden_newer"] == 0
    assert view["hidden_older"] == 2
    assert view["scroll_offset"] == 0


def test_build_stack_view_scrolls_middle_items_between_pinned_top_and_bottom():
    view = build_stack_view(STACK_ITEMS, view_top=3, scroll_offset=2)

    assert view["visible_items"] == [5, 2, 1]
    assert view["visible_displacements"] == [0, 3, 4]
    assert view["hidden_newer"] == 2
    assert view["hidden_older"] == 0
    assert view["scroll_offset"] == 2


def test_build_stack_view_view_top_one_still_shows_top_and_bottom_when_possible():
    view = build_stack_view(STACK_ITEMS, view_top=1, scroll_offset=3)

    assert view["visible_items"] == [5, 1]
    assert view["visible_displacements"] == [0, 4]
    assert view["hidden_newer"] == 0
    assert view["hidden_older"] == 3
    assert view["scroll_offset"] == 0


def test_build_stack_view_single_item_uses_top_equals_bottom_label():
    view = build_stack_view([7], view_top=3)

    assert view["visible_items"] == [7]
    assert view["visible_displacements"] == [0]


def test_offset_labels_show_top_bottom_and_top_equals_bottom():
    assert StackPanel._format_offset_label(0, 1) == "top=bottom"
    assert StackPanel._format_offset_label(0, 5) == "top"
    assert StackPanel._format_offset_label(2, 5) == "top-2"
    assert StackPanel._format_offset_label(4, 5) == "bottom"


def test_clamp_scroll_offset_clamps_to_valid_bounds():
    assert clamp_scroll_offset(5, 3, -2) == 0
    assert clamp_scroll_offset(5, 3, 10) == 2
    assert clamp_scroll_offset(5, 1, 10) == 0


def test_clamp_scroll_offset_returns_zero_when_scrolling_is_not_needed():
    assert clamp_scroll_offset(3, 3, 1) == 0
    assert clamp_scroll_offset(5, 1, 1) == 0
    assert clamp_scroll_offset(5, None, 1) == 0


def test_parse_push_values_supports_multiple_tokens_and_quotes():
    assert parse_push_values('10 20 "hello world"') == ["10", "20", "hello world"]


def test_parse_push_values_rejects_empty_input():
    with pytest.raises(ValueError):
        parse_push_values("")


def test_parse_single_path_supports_quoted_paths():
    path = parse_single_path('"saved sessions/demo.json"', "save")

    assert path == Path("saved sessions/demo.json")


def test_parse_single_path_requires_one_path():
    with pytest.raises(ValueError):
        parse_single_path("one two", "load")


def test_push_many_converts_all_items_for_current_type():
    stack = StackDemo()
    stack.set_type("int")

    pushed = stack.push_many(["1", "2", "3"])

    assert pushed == [1, 2, 3]
    assert stack.stack == [1, 2, 3]


def test_push_many_converts_bool_values_for_current_type():
    stack = StackDemo()
    stack.set_type("bool")

    pushed = stack.push_many(["true", "0", "yes", "off"])

    assert pushed == [True, False, True, False]
    assert stack.stack == [True, False, True, False]


def test_push_many_is_atomic_when_capacity_would_overflow():
    stack = StackDemo(max_size=2)
    stack.push("1")

    with pytest.raises(OverflowError):
        stack.push_many(["2", "3"])

    assert stack.stack == [1]


def test_clear_removes_all_items_from_tui_stack():
    stack = StackDemo()
    stack.push_many(["1", "2", "3"])

    stack.clear()

    assert stack.stack == []
    assert stack.size() == 0


def test_swap_exchanges_top_two_items_in_tui_stack():
    stack = StackDemo()
    stack.push_many(["1", "2", "3"])

    swapped = stack.swap()

    assert swapped == (3, 2)
    assert stack.stack == [1, 3, 2]


def test_rotate_moves_third_item_to_top_in_tui_stack():
    stack = StackDemo()
    stack.push_many(["1", "2", "3", "4"])

    rotated = stack.rotate()

    assert rotated == [3, 4, 2]
    assert stack.stack == [1, 3, 4, 2]


def test_dup_uses_existing_top_value_in_tui_stack():
    stack = StackDemo()
    stack.set_type("str")
    stack.push("hello")

    duplicated = stack.dup()

    assert duplicated == "hello"
    assert stack.stack == ["hello", "hello"]


def test_dup_respects_capacity_limit_in_tui_stack():
    stack = StackDemo(max_size=1)
    stack.set_type("str")
    stack.push("hello")

    with pytest.raises(OverflowError):
        stack.dup()


def test_at_returns_values_by_zero_based_offset_from_top():
    stack = StackDemo()
    stack.push_many(["10", "20", "30"])

    assert stack.at(0) == 30
    assert stack.at(1) == 20
    assert stack.at(2) == 10


def test_at_rejects_out_of_range_index():
    stack = StackDemo()
    stack.push_many(["10", "20"])

    with pytest.raises(IndexError):
        stack.at(2)


def test_at_rejects_negative_index():
    stack = StackDemo()
    stack.push("10")

    with pytest.raises(IndexError):
        stack.at(-1)


def test_save_and_load_session_round_trip(tmp_path):
    stack = StackDemo(max_size=10)
    stack.set_type("float")
    stack.push_many(["1.5", "2.5"])
    session_path = tmp_path / "session.json"

    save_session(session_path, stack)
    type_name, items = load_session(session_path)

    assert type_name == "float"
    assert items == [1.5, 2.5]


def test_load_session_defaults_type_to_any(tmp_path):
    session_path = tmp_path / "session.json"
    session_path.write_text('{"items": [1, "two"]}\n', encoding="utf-8")

    type_name, items = load_session(session_path)

    assert type_name == "any"
    assert items == [1, "two"]


def test_load_session_rejects_invalid_payload(tmp_path):
    session_path = tmp_path / "session.json"
    session_path.write_text('{"type": "weird", "items": "not-a-list"}\n', encoding="utf-8")

    with pytest.raises(ValueError):
        load_session(session_path)


def test_save_and_load_bool_session_round_trip(tmp_path):
    stack = StackDemo(max_size=10)
    stack.set_type("bool")
    stack.push_many(["true", "false"])
    session_path = tmp_path / "session.json"

    save_session(session_path, stack)
    type_name, items = load_session(session_path)

    assert type_name == "bool"
    assert items == [True, False]


def test_snapshot_and_restore_stack_round_trip():
    stack = StackDemo(max_size=10)
    stack.set_type("bool")
    stack.push_many(["true", "false"])

    snapshot = snapshot_stack(stack)
    restored = restore_stack(snapshot, max_size=10)

    assert snapshot == {"type": "bool", "items": [True, False]}
    assert restored.stack == [True, False]
    assert restored.element_type is parse_bool


def test_build_random_values_for_int_stays_in_configured_range():
    values = build_random_values(
        count=5,
        element_type=int,
        words=WORDS,
        rng=random.Random(7),
        int_min=10,
        int_max=12,
        float_min=FLOAT32_MIN,
        float_max=FLOAT32_MAX,
    )

    assert len(values) == 5
    assert all(10 <= value <= 12 for value in values)


def test_build_random_values_for_float_stays_in_configured_range():
    values = build_random_values(
        count=5,
        element_type=float,
        words=WORDS,
        rng=random.Random(7),
        int_min=INT32_MIN,
        int_max=INT32_MAX,
        float_min=1.5,
        float_max=2.5,
    )

    assert len(values) == 5
    assert all(1.5 <= value <= 2.5 for value in values)


def test_build_random_values_for_str_uses_word_list():
    values = build_random_values(
        count=5,
        element_type=str,
        words=WORDS,
        rng=random.Random(7),
        int_min=INT32_MIN,
        int_max=INT32_MAX,
        float_min=FLOAT32_MIN,
        float_max=FLOAT32_MAX,
    )

    assert len(values) == 5
    assert all(value in WORDS for value in values)


def test_build_random_values_for_bool_uses_boolean_values():
    values = build_random_values(
        count=10,
        element_type=parse_bool,
        words=WORDS,
        rng=random.Random(7),
        int_min=INT32_MIN,
        int_max=INT32_MAX,
        float_min=FLOAT32_MIN,
        float_max=FLOAT32_MAX,
    )

    assert len(values) == 10
    assert all(isinstance(value, bool) for value in values)
    assert set(values) <= {True, False}


def test_build_random_values_for_any_returns_mixed_supported_values():
    values = build_random_values(
        count=10,
        element_type=None,
        words=WORDS,
        rng=random.Random(7),
        int_min=10,
        int_max=12,
        float_min=1.5,
        float_max=2.5,
    )

    assert len(values) == 10
    assert any(isinstance(value, int) for value in values)
    assert any(isinstance(value, float) for value in values)
    assert any(isinstance(value, str) for value in values)
    assert any(isinstance(value, bool) for value in values)


def test_parse_bool_accepts_common_string_forms():
    assert parse_bool("true") is True
    assert parse_bool("YES") is True
    assert parse_bool("0") is False
    assert parse_bool("off") is False


def test_parse_bool_rejects_unknown_values():
    with pytest.raises(ValueError):
        parse_bool("maybe")


def test_undo_restores_previous_snapshot():
    app = StackDemoTUI()
    app.demo.push_many(["1", "2"])
    app._record_undo_state()
    app.demo.push("3")

    app._undo()

    assert app.demo.stack == [1, 2]
    assert app._can_redo()


def test_redo_reapplies_undone_snapshot():
    app = StackDemoTUI()
    app.demo.push_many(["1", "2"])
    app._record_undo_state()
    app.demo.push("3")
    app._undo()

    app._redo()

    assert app.demo.stack == [1, 2, 3]
    assert app._can_undo()


def test_stack_tui_logs_timing_after_submitted_command():
    async def scenario():
        app = StackDemoTUI(max_size=5)
        async with app.run_test() as pilot:
            input_widget = app.query_one(Input)
            input_widget.post_message(Input.Submitted(input_widget, "/push 5"))
            await pilot.pause()
            log = app.query_one(RichLog)
            assert log.lines[-1].text.startswith("time: ")

    asyncio.run(scenario())




def test_record_undo_state_clears_redo_history():
    app = StackDemoTUI()
    app.demo.push("1")
    app._record_undo_state()
    app.demo.push("2")
    app._undo()

    app._record_undo_state()

    assert not app._can_redo()


def test_undo_restores_type_changes():
    app = StackDemoTUI()
    app._record_undo_state()
    app.demo.set_type("bool")

    app._undo()

    assert app.demo.element_type is int


def test_undo_without_history_raises_value_error():
    app = StackDemoTUI()

    with pytest.raises(ValueError):
        app._undo()


def test_redo_without_future_history_raises_value_error():
    app = StackDemoTUI()

    with pytest.raises(ValueError):
        app._redo()


def test_build_random_values_rejects_non_positive_count():
    with pytest.raises(ValueError):
        build_random_values(
            count=0,
            element_type=int,
            words=WORDS,
            rng=random.Random(7),
            int_min=INT32_MIN,
            int_max=INT32_MAX,
            float_min=FLOAT32_MIN,
            float_max=FLOAT32_MAX,
        )


def test_parser_accepts_positive_view_top():
    args = build_parser().parse_args(["--view-top", "5"])

    assert args.view_top == 5


def test_parser_defaults_view_top_to_eight():
    args = build_parser().parse_args([])

    assert args.view_top == 8
    assert args.int_min == INT32_MIN
    assert args.int_max == INT32_MAX
    assert args.float_min == FLOAT32_MIN
    assert args.float_max == FLOAT32_MAX


def test_parser_rejects_zero_view_top():
    with pytest.raises(SystemExit):
        build_parser().parse_args(["--view-top", "0"])


def test_parser_rejects_negative_view_top():
    with pytest.raises(SystemExit):
        build_parser().parse_args(["--view-top", "-1"])
