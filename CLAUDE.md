# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
make install          # create .venv and install dependencies
make test             # full test suite
make test-<name>      # single module, e.g. make test-stack or make test-stack-app
make run-<name>       # import a non-TUI demo module (verifies clean import)
make run-<name>-app   # launch a TUI interactively
make demo-<name>      # produce dark + light mp4s for one TUI (requires vhs, ffmpeg, imagemagick)
make demo-all         # produce all demo videos
```

Valid short `<name>` aliases: `bst`, `deque`, `dict`, `dll`, `graph`, `heap`, `list`, `networkx`, `queue`, `set`, `sll`, `stack`, `trie`, `uint`. App variants: `stack-app`, `queue-app`, `deque-app`, `list-app`, `sll-app`, `dll-app`, `uint-app`.

Single test without make: `.venv/bin/pytest tests/test_stack_demo.py -v`

Font override for demo videos: `VHS_FONT_FAMILY="SF Mono" make demo-stack`

## Architecture

### Data structure modules (`data_structures/`)

One module per topic, named `<topic>_demo.py` or `<topic>.py`. Modules contain only class definitions — no `__main__` block — so `make run-<name>` just verifies a clean import. The exception is TUI apps under `data_structures/tui/`, which are runnable as `python -m data_structures.tui.<app>`.

### TUI layer (`data_structures/tui/`)

Two patterns exist side by side:

- **`stack_app.py`** and **`unsigned_int_app.py`** — standalone, self-contained. Each defines its own model, panel widget, and command dispatcher. Does not inherit from the shared base.
- **All other TUI apps** — inherit from `BaseLinearStructureTUI` in `common.py`. The base provides the Textual widget layout, shared command dispatcher (`/random`, `/clear`, `/save`, `/load`, `/undo`, `/redo`, `/show`, `/type`, scroll, `/help`), undo/redo snapshots, and type-constraint enforcement. Subclasses override `STRUCTURE_NAME`, `START_LABEL`/`END_LABEL`, `get_items()`, `append_values()`, `clear_structure()`, `replace_items()`, `handle_structure_command()`, `help_lines()`, and `placeholder_text()`.

`/help` output convention: structure-specific commands first under `--- <Name> ---`, then common commands under `--- Common ---`. Command verbs use `[cyan]...[/cyan]` Rich markup; argument placeholders stay outside the markup span.

All TUIs support `/search VALUE`. Linked-list TUIs additionally expose positional and node-id–based insert/remove commands.

`unsigned_int_app.py` visualizes a fixed-width unsigned integer as aligned binary/hex/octal box rows (rendered by `render_visualization()` in `data_structures/unsigned_int.py`). Valid sizes: 4, 8, 16, 32, 64. Octal requires phantom bits (⌈size/3⌉×3 − size) shown as `·`; hex has a matching phantom cell. In the binary row, heavy bars (`┃`) mark octal group boundaries (every 3 bits) and double bars (`║`) mark hex group boundaries (every 4 bits). Commands: `/set`, `/random`, `/set-bit`, `/reset-bit`, `/toggle-bit`, `/set-octal`, `/set-hex`, `/size`, `/clear`, `/save`, `/load`, `/undo`, `/redo`.

### Demo video pipeline (`scripts/run_vhs.py`)

Two-stage process:
1. `vhs` renders the raw terminal interaction from a `.tape` file in `demos/`.
2. `run_vhs.py` post-processes the raw video: selects a platform-appropriate font (macOS → `Menlo`, Linux → `DejaVu Sans Mono`), overrides the output path, trims the slow launch, adds an opening title card and ending card (via ImageMagick), and burns lower-right captions from `# CAPTION:` comments in the tape.

Caption pipeline: `parse_commands()` → `scale_commands()` → `build_command_caption_cues()` → `burn_captions_into_video()`.

The timing constants near the top of `run_vhs.py` (`INTRO_SECONDS`, `OUTRO_SECONDS`, `LAUNCH_TRIM_SECONDS`) are the main levers for video pacing. `INTERTITLE_SECONDS` and `LIVE_HOLD_SECONDS` are legacy knobs not currently active.

Each TUI has a single canonical tape file: `demos/<name>.tape`. The `--mode dark|light` flag on `run_vhs.py` does three things: injects `Set Theme` (dark → `TokyoNight`, light → `Catppuccin Latte`), injects `Env TEXTUAL_THEME` (dark → `textual-dark`, light → `textual-light`) so the Textual app itself switches themes, and appends `-dark` or `-light` to the output filename. Individual targets like `make demo-stack-dark` and `make demo-stack-light` are available alongside the combined `make demo-stack`.

On Linux/CI, ImageMagick is installed as `convert` (not `magick`); the release workflow symlinks `/usr/bin/convert` → `/usr/local/bin/magick` to satisfy the script.

### Tests (`tests/`)

One `test_<module>.py` per source module. `conftest.py` adds a `temporary_recursion_limit` fixture and a post-collection summary of test counts per file. `pytest.ini` sets `pythonpath = .` so `data_structures` and `scripts` are importable without installation.
