import json
import shlex
import subprocess
from pathlib import Path


DEFAULT_SECONDS_PER_FRAME = 5.0
FRAME_FONT_PATH = Path("/System/Library/Fonts/SFNSMono.ttf")
FRAME_CANVAS_SIZE = "1600x1200"
DEFAULT_CAPTURE_DIR = Path.cwd() / ".capture"
DEFAULT_VIDEO_DIR = Path.cwd() / ".video"


def validate_session_name(session_name: str) -> str:
    candidate = session_name.strip()
    if not candidate:
        raise ValueError("Session name must not be empty")
    if any(sep in candidate for sep in ("/", "\\")):
        raise ValueError("Session name must not contain path separators")
    if candidate in (".", ".."):
        raise ValueError("Session name must not be '.' or '..'")
    return candidate


def default_session_name(demo_slug: str) -> str:
    return f"session-{demo_slug}"


def parse_session_arg(arg: str | None) -> str:
    if arg is None:
        raise ValueError("Usage: /session <session-name>")
    parts = shlex.split(arg)
    if len(parts) != 1:
        raise ValueError("Usage: /session <session-name>")
    return validate_session_name(parts[0])


def parse_capture_mode(arg: str | None) -> str:
    if arg is None:
        raise ValueError("Usage: /capture [on|off]")
    parts = shlex.split(arg)
    if len(parts) != 1 or parts[0].lower() not in {"on", "off"}:
        raise ValueError("Usage: /capture [on|off]")
    return parts[0].lower()


def parse_video_args(arg: str | None) -> tuple[str | None, float]:
    if arg is None:
        return None, DEFAULT_SECONDS_PER_FRAME

    parts = shlex.split(arg)
    if len(parts) == 1:
        try:
            seconds_per_frame = float(parts[0])
        except ValueError:
            return validate_session_name(parts[0]), DEFAULT_SECONDS_PER_FRAME
        if seconds_per_frame <= 0:
            raise ValueError("seconds-per-frame must be positive")
        return None, seconds_per_frame

    if len(parts) == 2:
        session_name = validate_session_name(parts[0])
        seconds_per_frame = float(parts[1])
        if seconds_per_frame <= 0:
            raise ValueError("seconds-per-frame must be positive")
        return session_name, seconds_per_frame

    raise ValueError("Usage: /video [session-name] [seconds-per-frame]")


def session_dir(structure_slug: str, session_name: str, capture_dir: Path | None = None) -> Path:
    root = capture_dir if capture_dir is not None else DEFAULT_CAPTURE_DIR
    return root / structure_slug / validate_session_name(session_name)


def frames_dir(structure_slug: str, session_name: str, capture_dir: Path | None = None) -> Path:
    return session_dir(structure_slug, session_name, capture_dir) / "frames"


def metadata_path(structure_slug: str, session_name: str, capture_dir: Path | None = None) -> Path:
    return session_dir(structure_slug, session_name, capture_dir) / "session.json"


def video_output_path(structure_slug: str, session_name: str, video_dir: Path | None = None) -> Path:
    root = video_dir if video_dir is not None else DEFAULT_VIDEO_DIR
    return root / structure_slug / f"{validate_session_name(session_name)}.mp4"


def _initial_metadata(structure_slug: str, session_name: str) -> dict:
    return {
        "structure": structure_slug,
        "session": validate_session_name(session_name),
        "frames": [],
    }


def load_capture_metadata(structure_slug: str, session_name: str, capture_dir: Path | None = None) -> dict:
    path = metadata_path(structure_slug, session_name, capture_dir)
    if not path.exists():
        return _initial_metadata(structure_slug, session_name)
    return json.loads(path.read_text(encoding="utf-8"))


def save_capture_metadata(
    structure_slug: str, session_name: str, payload: dict, capture_dir: Path | None = None
) -> None:
    path = metadata_path(structure_slug, session_name, capture_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def ensure_capture_session(structure_slug: str, session_name: str, capture_dir: Path | None = None) -> dict:
    session_name = validate_session_name(session_name)
    frames_dir(structure_slug, session_name, capture_dir).mkdir(parents=True, exist_ok=True)
    payload = load_capture_metadata(structure_slug, session_name, capture_dir)
    save_capture_metadata(structure_slug, session_name, payload, capture_dir)
    return payload


def next_frame_path(structure_slug: str, session_name: str, capture_dir: Path | None = None) -> tuple[Path, int]:
    payload = ensure_capture_session(structure_slug, session_name, capture_dir)
    next_index = len(payload["frames"]) + 1
    return frames_dir(structure_slug, session_name, capture_dir) / f"frame-{next_index:04d}.png", next_index


def next_frame_paths(
    structure_slug: str, session_name: str, capture_dir: Path | None = None
) -> tuple[Path, Path, int]:
    payload = ensure_capture_session(structure_slug, session_name, capture_dir)
    next_index = len(payload["frames"]) + 1
    frame_base = frames_dir(structure_slug, session_name, capture_dir) / f"frame-{next_index:04d}"
    return frame_base.with_suffix(".txt"), frame_base.with_suffix(".png"), next_index


def render_text_frame_image(text_path: Path, png_path: Path) -> None:
    subprocess.run(
        [
            "magick",
            "-background",
            "#101418",
            "-fill",
            "#e6edf3",
            "-font",
            str(FRAME_FONT_PATH),
            "-pointsize",
            "18",
            f"label:@{text_path}",
            "-gravity",
            "northwest",
            "-extent",
            FRAME_CANVAS_SIZE,
            "-alpha",
            "off",
            "-type",
            "TrueColor",
            "-depth",
            "8",
            str(png_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )


def append_capture_frame(
    structure_slug: str,
    session_name: str,
    *,
    command: str,
    elapsed_ns: int,
    screenshot_path: Path,
    capture_dir: Path | None = None,
) -> dict:
    payload = ensure_capture_session(structure_slug, session_name, capture_dir)
    frame_index = len(payload["frames"]) + 1
    frame_record = {
        "index": frame_index,
        "file": str(Path("frames") / screenshot_path.with_suffix(".png").name),
        "source_text": str(Path("frames") / screenshot_path.with_suffix(".txt").name),
        "command": command,
        "caption": command,
        "elapsed_ns": elapsed_ns,
    }
    payload["frames"].append(frame_record)
    save_capture_metadata(structure_slug, session_name, payload, capture_dir)
    return frame_record


def format_srt_timestamp(total_seconds: float) -> str:
    total_milliseconds = int(round(total_seconds * 1000))
    hours, remainder = divmod(total_milliseconds, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    seconds, milliseconds = divmod(remainder, 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"


def write_concat_manifest(
    structure_slug: str, session_name: str, seconds_per_frame: float, capture_dir: Path | None = None
) -> Path:
    payload = load_capture_metadata(structure_slug, session_name, capture_dir)
    session_path = session_dir(structure_slug, session_name, capture_dir)
    manifest_path = session_path / "frames.txt"
    frames = payload["frames"]
    if not frames:
        raise ValueError("No captured frames are available for this session")

    lines = []
    for frame in frames:
        lines.append(f"file {frame['file']}")
        lines.append(f"duration {seconds_per_frame:.3f}")
    lines.append(f"file {frames[-1]['file']}")
    manifest_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return manifest_path


def write_caption_srt(
    structure_slug: str, session_name: str, seconds_per_frame: float, capture_dir: Path | None = None
) -> Path:
    payload = load_capture_metadata(structure_slug, session_name, capture_dir)
    session_path = session_dir(structure_slug, session_name, capture_dir)
    srt_path = session_path / "captions.srt"
    frames = payload["frames"]
    if not frames:
        raise ValueError("No captured frames are available for this session")

    entries = []
    for index, frame in enumerate(frames, start=1):
        start = (index - 1) * seconds_per_frame
        end = index * seconds_per_frame
        entries.append(
            "\n".join(
                [
                    str(index),
                    f"{format_srt_timestamp(start)} --> {format_srt_timestamp(end)}",
                    frame["caption"],
                ]
            )
        )
    srt_path.write_text("\n\n".join(entries) + "\n", encoding="utf-8")
    return srt_path


def render_capture_video(
    structure_slug: str,
    session_name: str,
    seconds_per_frame: float = DEFAULT_SECONDS_PER_FRAME,
    *,
    capture_dir: Path | None = None,
    video_dir: Path | None = None,
) -> Path:
    if seconds_per_frame <= 0:
        raise ValueError("seconds-per-frame must be positive")

    session_name = validate_session_name(session_name)
    ensure_capture_session(structure_slug, session_name, capture_dir)
    manifest_path = write_concat_manifest(structure_slug, session_name, seconds_per_frame, capture_dir)
    captions_path = write_caption_srt(structure_slug, session_name, seconds_per_frame, capture_dir)
    output_path = video_output_path(structure_slug, session_name, video_dir)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    working_dir = session_dir(structure_slug, session_name, capture_dir)

    try:
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                manifest_path.name,
                "-i",
                captions_path.name,
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                "-c:s",
                "mov_text",
                "-shortest",
                str(output_path),
            ],
            cwd=working_dir,
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as error:
        stderr = error.stderr.strip() if error.stderr else str(error)
        raise RuntimeError(stderr) from error
    return output_path
