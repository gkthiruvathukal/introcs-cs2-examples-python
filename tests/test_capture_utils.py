from pathlib import Path

import pytest

from data_structures import capture_utils


def test_parse_capture_args_supports_on_and_off():
    assert capture_utils.parse_capture_mode("on") == "on"
    assert capture_utils.parse_capture_mode("off") == "off"


def test_parse_capture_args_rejects_invalid_values():
    with pytest.raises(ValueError):
        capture_utils.parse_capture_mode(None)
    with pytest.raises(ValueError):
        capture_utils.parse_capture_mode("demo maybe")


def test_parse_session_arg_supports_single_name():
    assert capture_utils.parse_session_arg("demo") == "demo"
    assert capture_utils.parse_session_arg('"my session"') == "my session"


def test_default_session_name_uses_demo_slug():
    assert capture_utils.default_session_name("stack-demo") == "session-stack-demo"


def test_parse_video_args_defaults_and_accepts_custom_seconds():
    assert capture_utils.parse_video_args(None) == (None, 5.0)
    assert capture_utils.parse_video_args("demo") == ("demo", 5.0)
    assert capture_utils.parse_video_args("2.5") == (None, 2.5)
    assert capture_utils.parse_video_args('"my session" 2.5') == ("my session", 2.5)


def test_parse_video_args_rejects_non_positive_seconds():
    with pytest.raises(ValueError):
        capture_utils.parse_video_args("demo 0")
    with pytest.raises(ValueError):
        capture_utils.parse_video_args("0")


def test_append_capture_frame_persists_command_caption_and_frame(tmp_path, monkeypatch):
    monkeypatch.setattr(capture_utils, "DEFAULT_CAPTURE_DIR", tmp_path / ".capture")

    frame_path, _ = capture_utils.next_frame_path("stack", "demo")
    frame_path.parent.mkdir(parents=True, exist_ok=True)
    frame_path.write_text("fake image", encoding="utf-8")

    record = capture_utils.append_capture_frame(
        "stack",
        "demo",
        command="/push 5",
        elapsed_ns=1234,
        screenshot_path=frame_path,
    )
    payload = capture_utils.load_capture_metadata("stack", "demo")

    assert record["caption"] == "/push 5"
    assert payload["frames"][0]["file"] == str(Path("frames") / frame_path.name)


def test_write_manifest_and_captions_use_relative_frame_files(tmp_path, monkeypatch):
    monkeypatch.setattr(capture_utils, "DEFAULT_CAPTURE_DIR", tmp_path / ".capture")
    session_name = "demo"
    structure_slug = "stack"

    first_frame, _ = capture_utils.next_frame_path(structure_slug, session_name)
    first_frame.parent.mkdir(parents=True, exist_ok=True)
    first_frame.write_text("one", encoding="utf-8")
    capture_utils.append_capture_frame(
        structure_slug,
        session_name,
        command="/push 1",
        elapsed_ns=100,
        screenshot_path=first_frame,
    )

    second_frame, _ = capture_utils.next_frame_path(structure_slug, session_name)
    second_frame.write_text("two", encoding="utf-8")
    capture_utils.append_capture_frame(
        structure_slug,
        session_name,
        command="/push 2",
        elapsed_ns=200,
        screenshot_path=second_frame,
    )

    manifest_path = capture_utils.write_concat_manifest(structure_slug, session_name, 3.0)
    captions_path = capture_utils.write_caption_srt(structure_slug, session_name, 3.0)

    manifest_text = manifest_path.read_text(encoding="utf-8")
    captions_text = captions_path.read_text(encoding="utf-8")

    assert "file frames/frame-0001.png" in manifest_text
    assert "duration 3.000" in manifest_text
    assert "/push 1" in captions_text
    assert "00:00:03,000" in captions_text


def test_render_capture_video_invokes_ffmpeg(tmp_path, monkeypatch):
    monkeypatch.setattr(capture_utils, "DEFAULT_CAPTURE_DIR", tmp_path / ".capture")
    monkeypatch.setattr(capture_utils, "DEFAULT_VIDEO_DIR", tmp_path / ".video")
    session_name = "demo"
    structure_slug = "stack"

    frame_path, _ = capture_utils.next_frame_path(structure_slug, session_name)
    frame_path.parent.mkdir(parents=True, exist_ok=True)
    frame_path.write_text("fake image", encoding="utf-8")
    capture_utils.append_capture_frame(
        structure_slug,
        session_name,
        command="/push 5",
        elapsed_ns=500,
        screenshot_path=frame_path,
    )

    calls = []

    def fake_run(cmd, cwd, check, capture_output, text):
        calls.append((cmd, cwd, check, capture_output, text))

    monkeypatch.setattr(capture_utils.subprocess, "run", fake_run)

    output_path = capture_utils.render_capture_video(structure_slug, session_name, 2.0)

    assert output_path.name == "demo.mp4"
    assert calls[0][0][0] == "ffmpeg"
