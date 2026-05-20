from scripts.run_vhs import choose_font_family, render_tape_text


def test_choose_font_family_prefers_menlo_on_macos(monkeypatch):
    monkeypatch.delenv("VHS_FONT_FAMILY", raising=False)
    assert choose_font_family("Darwin") == "Menlo"


def test_choose_font_family_uses_env_override(monkeypatch):
    monkeypatch.setenv("VHS_FONT_FAMILY", "Courier Prime")
    assert choose_font_family("Darwin") == "Courier Prime"


def test_render_tape_text_replaces_font_family_line():
    tape_text = '\n'.join(
        [
            'Set Theme "TokyoNight"',
            'Set FontSize 16',
            'Set FontFamily "DejaVu Sans Mono"',
            'Set Width 1800',
        ]
    )
    rendered = render_tape_text(tape_text, "Menlo")
    assert 'Set FontFamily "Menlo"' in rendered
    assert 'Set FontFamily "DejaVu Sans Mono"' not in rendered
