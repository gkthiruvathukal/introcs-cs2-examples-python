import random

import pytest

from data_structures.tui.common import (
    build_linear_view,
    build_random_values,
    clamp_scroll_offset,
    default_position_label,
    format_elapsed_ns,
    load_session,
    parse_bool,
    parse_single_path,
    parse_value_tokens,
    save_session,
)


WORDS = ["alpha", "beta", "gamma"]


def test_build_linear_view_unlimited_returns_full_order():
    view = build_linear_view([1, 2, 3, 4])

    assert view["visible_items"] == [1, 2, 3, 4]
    assert view["visible_indices"] == [0, 1, 2, 3]
    assert view["hidden_before"] == 0
    assert view["hidden_after"] == 0


def test_build_linear_view_keeps_both_ends_visible():
    view = build_linear_view([1, 2, 3, 4, 5], view_top=3, scroll_offset=1)

    assert view["visible_items"] == [1, 3, 5]
    assert view["visible_indices"] == [0, 2, 4]
    assert view["hidden_before"] == 1
    assert view["hidden_after"] == 1


def test_clamp_scroll_offset_for_linear_view():
    assert clamp_scroll_offset(5, 3, -1) == 0
    assert clamp_scroll_offset(5, 3, 99) == 2


def test_default_position_label_handles_single_and_pinned_ends():
    assert default_position_label(0, 1, "front", "back") == "front=back"
    assert default_position_label(0, 4, "front", "back") == "front"
    assert default_position_label(2, 4, "front", "back") == "front+2"
    assert default_position_label(3, 4, "front", "back") == "back"


def test_parse_value_tokens_supports_quotes():
    assert parse_value_tokens('10 "hello world"', "usage") == ["10", "hello world"]


def test_parse_value_tokens_rejects_wrong_arity():
    with pytest.raises(ValueError):
        parse_value_tokens("", "usage")
    with pytest.raises(ValueError):
        parse_value_tokens("one two", "usage", max_count=1)


def test_parse_single_path_supports_quotes():
    assert str(parse_single_path('"saved sessions/demo.json"', "save")) == "saved sessions/demo.json"


def test_save_and_load_session_round_trip(tmp_path):
    path = tmp_path / "session.json"
    payload = {"type": "int", "items": [1, 2, 3]}

    save_session(path, payload)
    loaded = load_session(path, {"int", "any"})

    assert loaded == payload


def test_build_random_values_for_bool_and_any():
    rng = random.Random(0)
    assert all(isinstance(value, bool) for value in build_random_values(5, parse_bool, WORDS, rng, -1, 1, -1.0, 1.0))

    mixed = build_random_values(10, None, WORDS, rng, -1, 1, -1.0, 1.0)
    assert any(isinstance(value, str) for value in mixed)
    assert any(isinstance(value, bool) for value in mixed)


def test_format_elapsed_ns_scales_units():
    assert format_elapsed_ns(999) == "999 ns"
    assert format_elapsed_ns(1_500) == "1.5 us"
    assert format_elapsed_ns(2_500_000) == "2.5 ms"
    assert format_elapsed_ns(1_250_000_000) == "1.250 s"
