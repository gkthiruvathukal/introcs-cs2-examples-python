# Capture Pipeline

The capture pipeline lets any TUI demo record its state as a series of PNG frames and then assemble them into an MP4 with a subtitle track.

## External dependencies

| Tool | Used for |
|---|---|
| `magick` (ImageMagick) | Rendering `.txt` snapshots to `.png` frames |
| `ffmpeg` | Assembling frames into `.mp4` with embedded `.srt` captions |

Both tools must be available on `PATH`. The TUIs still run normally without them; capture commands will fail with a clear error message if either tool is missing.

## Directory layout

```
.capture/
  <slug>/
    <session>/
      session.json        # metadata: structure, session name, frame list
      frames/
        frame-0001.txt    # raw text snapshot of the TUI state
        frame-0001.png    # rendered PNG (via magick)
        frame-0002.txt
        frame-0002.png
        ...
      frames.txt          # ffmpeg concat manifest (written at /video time)
      captions.srt        # subtitle file (written at /video time)

.video/
  <slug>/
    <session>.mp4
```

The `<slug>` is a short lowercase identifier defined by each TUI class (see below).

## Session lifecycle

1. **`/session <name>`** — selects a named session. Creates the session directory if it does not exist. Future frames go into `.capture/<slug>/<session>/frames/`.
2. **`/capture on`** — enables recording. After each subsequent command, a text snapshot is written and rendered to PNG.
3. **`/capture off`** — suspends recording. The session directory and metadata are preserved; recording can be resumed with `/capture on`.
4. **`/video [session] [seconds-per-frame]`** — builds the video:
   - writes `frames.txt` (ffmpeg concat manifest) and `captions.srt`
   - runs ffmpeg to produce `.video/<slug>/<session>.mp4`
   - the default frame duration is 5 seconds
   - caption text defaults to the command string that produced each frame

Capture commands (`/session`, `/capture`) do not produce a frame themselves. `/quit` and `/exit` are also excluded.

## The `STRUCTURE_SLUG`

Each TUI subclass must define `STRUCTURE_SLUG` as a class attribute to scope its capture output. The base class default is `"structure"`, which is a sentinel value — any subclass that leaves it at the default will share a capture directory with every other unset subclass.

```python
class MyDemoTUI(BaseLinearStructureTUI):
    STRUCTURE_NAME = "My Structure"
    STRUCTURE_SLUG = "my-structure"   # required to isolate capture output
```

See the slug assignment table in `AGENTS.md` for the current status of each TUI.

## How a frame is captured

After each eligible command the base class calls `_maybe_capture_frame()`:

1. Calls `_capture_frame_text()` to produce a plain-text snapshot of the current panel and the last eight log lines.
2. Writes the snapshot to `frame-NNNN.txt`.
3. Calls `magick` to render the `.txt` file to a dark-background `.png` using the system monospace font.
4. Appends a frame record to `session.json` (index, file path, command text, elapsed nanoseconds).

The `_capture_frame_text()` base implementation queries the widget with `id="panel"` and reads `panel.renderable`. Subclasses that use a non-standard panel widget can override `_capture_frame_text()` to produce a richer snapshot.

## Module responsibilities

| Module | Responsibility |
|---|---|
| `data_structures/capture_utils.py` | All I/O: session directories, metadata JSON, text-to-PNG rendering, ffmpeg invocation |
| `data_structures/tui_common.py` | Wires capture into `BaseLinearStructureTUI`: `_maybe_capture_frame`, `_capture_frame_text`, `/session`, `/capture`, `/video` commands |
| `data_structures/stack_demo_tui.py` | Standalone: imports from `capture_utils` directly, does not use the base class |

`capture_utils.py` has no Textual dependency, which keeps it fully testable without a running app. See `tests/test_capture_utils.py`.
