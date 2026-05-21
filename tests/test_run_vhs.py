from pathlib import Path

from scripts.run_vhs import (
    CaptionCue,
    apply_mode_suffix,
    choose_font_family,
    CommandCue,
    command_to_intertitle,
    extract_dimensions,
    extract_output_path,
    extract_title,
    format_srt_timestamp,
    parse_captions,
    parse_commands,
    render_tape_text,
    render_textual_theme,
    render_theme,
    replace_output_path,
    scale_cues,
)


def test_choose_font_family_prefers_menlo_on_macos(monkeypatch):
    monkeypatch.delenv("VHS_FONT_FAMILY", raising=False)
    assert choose_font_family("Darwin") == "Menlo"


def test_choose_font_family_uses_env_override(monkeypatch):
    monkeypatch.setenv("VHS_FONT_FAMILY", "Courier Prime")
    assert choose_font_family("Darwin") == "Courier Prime"


def test_render_tape_text_replaces_font_family_line():
    tape_text = "\n".join(
        [
            'Set Theme "TokyoNight"',
            "Set FontSize 16",
            'Set FontFamily "DejaVu Sans Mono"',
            "Set Width 1800",
        ]
    )
    rendered = render_tape_text(tape_text, "Menlo")
    assert 'Set FontFamily "Menlo"' in rendered
    assert 'Set FontFamily "DejaVu Sans Mono"' not in rendered


def test_extract_output_and_replace_output_path():
    tape_text = "Output demos/stack-dark.mp4\nSet Width 1920\n"
    assert extract_output_path(tape_text) == Path("demos/stack-dark.mp4")
    replaced = replace_output_path(tape_text, Path("/tmp/raw.mp4"))
    assert 'Output "/tmp/raw.mp4"' in replaced


def test_extract_output_path_accepts_quoted_path():
    tape_text = 'Output "/tmp/raw.mp4"\nSet Width 1920\n'
    assert extract_output_path(tape_text) == Path("/tmp/raw.mp4")


def test_extract_title_and_dimensions():
    tape_text = "\n".join(
        [
            "# Stack — interactive demo (dark theme)",
            "# Run from project root:  vhs demos/stack-dark.tape",
            "Output demos/stack-dark.mp4",
            "Set Width 1920",
            "Set Height 1200",
        ]
    )
    assert extract_title(tape_text, Path("demos/stack-dark.tape")) == "Stack — interactive demo (dark theme)"
    assert extract_dimensions(tape_text) == (1920, 1200)


def test_parse_captions_uses_explicit_caption_comments_and_timing():
    tape_text = "\n".join(
        [
            "Set TypingSpeed 100ms",
            "# CAPTION: Build the initial stack",
            'Type "abc"',
            "Enter",
            "Sleep 2s",
            "# CAPTION: Inspect the top value",
            'Type "/peek"',
            "Enter",
            "Sleep 1s",
        ]
    )
    cues, total = parse_captions(tape_text)
    assert len(cues) == 2
    assert cues[0].text == "Build the initial stack"
    assert cues[0].start_seconds == 0.0
    assert round(cues[0].end_seconds, 2) == 2.45
    assert cues[1].text == "Inspect the top value"
    assert round(total, 2) == 4.10


def test_parse_commands_uses_typed_commands_observation_sleep_and_captions():
    tape_text = "\n".join(
        [
            "Set TypingSpeed 100ms",
            "# CAPTION: Push one value",
            'Type "/push 3"',
            "Enter",
            "Sleep 2s",
            "# CAPTION: Read the top value",
            'Type "/peek"',
            "Enter",
            "Sleep 1.5s",
        ]
    )
    commands, total = parse_commands(tape_text)
    assert [command.text for command in commands] == ["/push 3", "/peek"]
    assert [command.caption for command in commands] == ["Push one value", "Read the top value"]
    assert round(commands[0].end_seconds, 2) == 2.85
    assert round(commands[1].end_seconds, 2) == 5.00
    assert round(total, 2) == 5.00


def test_parse_commands_leaves_caption_none_when_no_caption_comment_exists():
    tape_text = "\n".join(
        [
            "Set TypingSpeed 100ms",
            'Type "/push 3"',
            "Enter",
            "Sleep 2s",
        ]
    )
    commands, _ = parse_commands(tape_text)
    assert commands == [CommandCue(text="/push 3", end_seconds=2.85, caption=None)]


def test_command_to_intertitle_skips_launch_and_prettifies_stack_commands():
    assert command_to_intertitle(".venv/bin/python -m data_structures.tui.stack_app") is None
    assert command_to_intertitle("/push 10 20 30") == "Push 3 values"
    assert command_to_intertitle("/peek") == "Peek at the top"
    assert command_to_intertitle("/quit") is None


def test_scale_cues_and_timestamp_formatting():
    cues = [CaptionCue("Launch", 0.0, 2.0)]
    scaled = scale_cues(cues, expected_total=4.0, actual_total=8.0)
    assert scaled[0].end_seconds == 4.0
    assert format_srt_timestamp(4.125) == "00:00:04,125"


def test_render_theme_replaces_existing_theme():
    tape_text = 'Set Theme "TokyoNight"\nSet FontSize 16\n'
    rendered = render_theme(tape_text, "Catppuccin Latte")
    assert 'Set Theme "Catppuccin Latte"' in rendered
    assert 'Set Theme "TokyoNight"' not in rendered


def test_render_theme_inserts_when_absent():
    tape_text = "Set FontSize 16\nSet Width 1920\n"
    rendered = render_theme(tape_text, "TokyoNight")
    assert 'Set Theme "TokyoNight"' in rendered


def test_apply_mode_suffix_dark():
    assert apply_mode_suffix(Path("demos/stack.mp4"), "dark") == Path("demos/stack-dark.mp4")


def test_apply_mode_suffix_light():
    assert apply_mode_suffix(Path("demos/queue.mp4"), "light") == Path("demos/queue-light.mp4")


def test_render_textual_theme_inserts_after_env_term():
    tape_text = "Set Width 1920\nEnv TERM xterm-256color\nType \"echo hi\"\n"
    result = render_textual_theme(tape_text, "textual-light")
    lines = result.splitlines()
    term_idx = next(i for i, l in enumerate(lines) if l.startswith("Env TERM"))
    assert lines[term_idx + 1] == "Env TEXTUAL_THEME textual-light"


def test_render_textual_theme_replaces_existing():
    tape_text = "Env TERM xterm-256color\nEnv TEXTUAL_THEME textual-dark\n"
    result = render_textual_theme(tape_text, "textual-light")
    assert "Env TEXTUAL_THEME textual-light" in result
    assert "Env TEXTUAL_THEME textual-dark" not in result
