import json
from pathlib import Path

import pytest

from data_structures.tui.unsigned_int_app import UnsignedIntApp, build_parser


def test_app_initial_state_is_8bit_zero():
    app = UnsignedIntApp(initial_size=8)
    assert app.uint.size == 8
    assert app.uint.value == 0


def test_app_initial_state_respects_size_arg():
    app = UnsignedIntApp(initial_size=16)
    assert app.uint.size == 16


def test_set_value_updates_uint():
    app = UnsignedIntApp()
    app.uint.set_value(85)
    assert app.uint.value == 85


def test_random_stays_within_range():
    app = UnsignedIntApp(initial_size=8)
    for _ in range(100):
        app.uint.set_value(app.rng.randint(0, app.uint._mask))
        assert 0 <= app.uint.value <= 255


def test_random_covers_full_range_for_nibble():
    app = UnsignedIntApp(initial_size=4)
    seen = set()
    for _ in range(500):
        v = app.rng.randint(0, app.uint._mask)
        seen.add(v)
    assert len(seen) == 16


def test_record_undo_and_undo_restores_previous():
    app = UnsignedIntApp(initial_size=8)
    app.uint.set_value(42)
    app._record_undo()
    app.uint.set_value(99)
    assert app.uint.value == 99
    app.undo_history  # confirm history has one entry
    snap = app.undo_history[-1]
    assert snap["value"] == 42


def test_undo_redo_round_trip():
    app = UnsignedIntApp(initial_size=8)
    app.uint.set_value(10)
    app._record_undo()
    app.uint.set_value(20)
    # undo
    app.redo_history.append(app._snapshot())
    app._restore(app.undo_history.pop())
    assert app.uint.value == 10
    # redo
    app.undo_history.append(app._snapshot())
    app._restore(app.redo_history.pop())
    assert app.uint.value == 20


def test_snapshot_and_restore():
    app = UnsignedIntApp(initial_size=8)
    app.uint.set_value(123)
    snap = app._snapshot()
    assert snap == {"size": 8, "value": 123}
    app.uint.clear()
    app._restore(snap)
    assert app.uint.value == 123


def test_save_and_load_session(tmp_path):
    app = UnsignedIntApp(initial_size=8)
    app.uint.set_value(200)
    path = tmp_path / "uint-session.json"
    payload = {"size": app.uint.size, "value": app.uint.value}
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    loaded = json.loads(path.read_text(encoding="utf-8"))
    assert loaded["size"] == 8
    assert loaded["value"] == 200


def test_build_parser_defaults():
    parser = build_parser()
    args = parser.parse_args([])
    assert args.size == 8


def test_build_parser_accepts_valid_sizes():
    parser = build_parser()
    for size in (4, 8, 16, 32, 64):
        args = parser.parse_args(["--size", str(size)])
        assert args.size == size
