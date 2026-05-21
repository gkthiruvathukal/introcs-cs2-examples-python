# Demo Video Maintenance

This repo builds the demo videos in two stages:

1. `vhs` renders the raw terminal interaction from a tape in `demos/*.tape`.
2. [`scripts/run_vhs.py`](/Volumes/Work/introcs-cs2-examples-python/scripts/run_vhs.py:1) post-processes that raw video by:
   - selecting a platform-appropriate font
   - trimming the slow launch
   - adding the opening title card and ending card
   - overlaying explanatory captions during the live interaction

The current output style is:
- opening title + credit
- live demo video
- lower-right captions describing the operation being demonstrated
- ending card

For maintainability, the caption wording now lives in the `.tape` files themselves. `run_vhs.py` extracts those caption comments and places them on the video timeline automatically.

## Rebuild Commands

One stack sample:

```bash
make demo-stack-dark   # runs demos/stack.tape --mode dark  → demos/stack-dark.mp4
make demo-stack-light  # runs demos/stack.tape --mode light → demos/stack-light.mp4
make demo-stack        # both
```

All demos:

```bash
make demo-all
```

Override the monospace font used by VHS:

```bash
VHS_FONT_FAMILY="SF Mono" make demo-stack
```

Override the opening credit:

```bash
VHS_CREDIT="George K. Thiruvathukal" make demo-stack
```

## What Controls the Timing

The main timing constants live near the top of [`scripts/run_vhs.py`](/Volumes/Work/introcs-cs2-examples-python/scripts/run_vhs.py:18):

- `INTRO_SECONDS`
  Controls how long the opening title/credit card stays on screen.
- `OUTRO_SECONDS`
  Controls how long the ending card stays on screen.
- `LAUNCH_TRIM_SECONDS`
  Removes some of the slow idle startup time from the raw VHS video before the first real action.
- `ENTER_SECONDS`
  Used when estimating the internal tape timeline from typed commands.

Important:
- the current version does **not** insert full-screen intertitle cards between operations
- so `INTERTITLE_SECONDS` and `LIVE_HOLD_SECONDS` are legacy knobs from the earlier experiment and are not part of the current rendered flow

If you want to speed up or slow down the overall stack video right now, the two most important levers are:
- shorten or lengthen `INTRO_SECONDS`
- shorten or lengthen `LAUNCH_TRIM_SECONDS`

If you want longer pauses on the actual demonstrated operations, the cleanest approach is to increase the `Sleep` durations directly in the `.tape` file for that demo.

## Where the Captions Come From

The live captions come from explicit `# CAPTION:` comments in the `.tape` file.

Example:

```tape
# CAPTION: Push 5 values onto the stack
Type "/push 10 20 30 40 50"
Enter
Sleep 2s
```

That caption is attached to the next typed command and stays visible for that command's observation window.

That path is:

1. `parse_commands(...)`
   Reads the tape and extracts each typed command, its optional `# CAPTION:` text, and its computed end time.
2. `scale_commands(...)`
   Scales those computed command times onto the real rendered video duration.
3. `build_command_caption_cues(...)`
   Turns those commands into timed caption intervals.
4. `burn_captions_into_video(...)`
   Renders the overlays into the final video.

There is still a legacy fallback in [`command_to_intertitle(...)`](/Volumes/Work/introcs-cs2-examples-python/scripts/run_vhs.py:300) for older tapes that do not yet use `# CAPTION:` comments, but new and maintained tapes should prefer explicit caption comments.

## How To Tweak the Caption Descriptions

Edit the `# CAPTION:` comments in the `.tape` file directly.

Example:

```tape
# CAPTION: Peek at the top value
Type "/peek"
Enter
Sleep 1.5s
```

If you want different wording, change only the comment:

```tape
# CAPTION: Read the top value
Type "/peek"
Enter
Sleep 1.5s
```

If you want a command to have no caption, simply omit the `# CAPTION:` line for that command.

## How To Move the Captions

The current lower-right placement is set in [`burn_captions_into_video(...)`](/Volumes/Work/introcs-cs2-examples-python/scripts/run_vhs.py:434).

These two expressions control the position:

```python
x_expr = "main_w-overlay_w-70"
y_expr = "main_h-overlay_h-150"
```

Interpretation:
- `x_expr`
  Keeps the caption box near the right edge.
- `y_expr`
  Keeps the caption box above the command entry area.

Common tweaks:

- move farther right:
  decrease the `70`
- move farther left:
  increase the `70`
- move lower:
  decrease the `150`
- move higher:
  increase the `150`

Example:

```python
x_expr = "main_w-overlay_w-40"
y_expr = "main_h-overlay_h-180"
```

## How To Resize the Caption Box

The box size is built in [`create_caption_overlay(...)`](/Volumes/Work/introcs-cs2-examples-python/scripts/run_vhs.py:406).

The main knobs are:

```python
box_width = max(640, round(width * 0.4))
box_height = max(96, round(height * 0.1))
point_size = max(22, round(height * 0.022))
```

Use these to:
- make the caption box wider or narrower
- make it taller or shorter
- make the caption text larger or smaller

## If You Want More Time To See an Operation

Right now the operation visibility mostly comes from the `Sleep` commands in the tape itself.

That means the simplest way to give an operation more room is to edit the tape:

```tape
Type "/peek"
Enter
Sleep 1.5s
```

Change to:

```tape
Type "/peek"
Enter
Sleep 3s
```

That is the most direct and predictable way to slow down a particular moment.

## Font Selection

The VHS font family is selected by [`choose_font_family(...)`](/Volumes/Work/introcs-cs2-examples-python/scripts/run_vhs.py:45):

- macOS: `Menlo`
- Linux / GitHub Actions: `DejaVu Sans Mono`

The title card font and caption font use separate selectors:
- `choose_title_font_file(...)`
- `choose_caption_font_file(...)`

If you want to change the look of the title cards or caption overlays, those are the places to edit.

## Suggested Workflow

When tuning a demo video:

1. edit the `.tape` file if the interaction timing itself needs to change
2. edit the `# CAPTION:` comments in the tape if the wording needs to change
3. edit `burn_captions_into_video(...)` if the caption position needs to change
4. edit `create_caption_overlay(...)` if the caption size or typography needs to change
5. rebuild one demo first, usually `make demo-stack-dark` (runs `demos/stack.tape --mode dark`)
6. inspect before rebuilding everything
