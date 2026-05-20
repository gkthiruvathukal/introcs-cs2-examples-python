#!/usr/bin/env python3
"""Run a VHS tape with platform-aware fonts and post-process the result."""

from __future__ import annotations

import argparse
import os
import platform
import re
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path


DEFAULT_FONT_BY_SYSTEM = {
    "Darwin": "Menlo",
    "Linux": "DejaVu Sans Mono",
}

DEFAULT_CREDIT = "George K. Thiruvathukal"
INTRO_SECONDS = 3.0
OUTRO_SECONDS = 2.5
INTERTITLE_SECONDS = 3.0
LIVE_HOLD_SECONDS = 4.0
LAUNCH_TRIM_SECONDS = 3.0
ENTER_SECONDS = 0.15

FONT_PATTERN = re.compile(r'^Set FontFamily ".*"$', re.MULTILINE)
OUTPUT_PATTERN = re.compile(r"^Output\s+(.+)$", re.MULTILINE)
TYPING_SPEED_PATTERN = re.compile(r"^Set TypingSpeed\s+(.+)$")
TYPE_PATTERN = re.compile(r'^Type(?:@\S+(?:\s+\S+)*)?\s+"(.*)"$')
SLEEP_PATTERN = re.compile(r"^Sleep\s+(.+)$")
SECTION_PATTERN = re.compile(r"^#\s*──\s*(.*?)\s*──+\s*$")
TITLE_PATTERN = re.compile(r"^#\s*(.+?)\s*$")
WIDTH_PATTERN = re.compile(r"^Set Width\s+(\d+)$", re.MULTILINE)
HEIGHT_PATTERN = re.compile(r"^Set Height\s+(\d+)$", re.MULTILINE)

@dataclass
class CaptionCue:
    text: str
    start_seconds: float
    end_seconds: float


@dataclass
class CommandCue:
    text: str
    end_seconds: float


def choose_font_family(system_name: str | None = None) -> str:
    override = os.environ.get("VHS_FONT_FAMILY")
    if override:
        return override
    system_name = system_name or platform.system()
    return DEFAULT_FONT_BY_SYSTEM.get(system_name, "DejaVu Sans Mono")


def choose_title_font_file(system_name: str | None = None) -> str | None:
    system_name = system_name or platform.system()
    candidates_by_system = {
        "Darwin": [
            "/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
            "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf",
        ],
        "Linux": [
            "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
            "/usr/share/fonts/dejavu/DejaVuSerif-Bold.ttf",
        ],
    }
    for candidate in candidates_by_system.get(system_name, []):
        if Path(candidate).exists():
            return candidate
    return None


def choose_caption_font_file(system_name: str | None = None) -> str | None:
    system_name = system_name or platform.system()
    candidates_by_system = {
        "Darwin": [
            "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/System/Library/Fonts/Supplemental/Helvetica.ttc",
        ],
        "Linux": [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/dejavu/DejaVuSans.ttf",
        ],
    }
    for candidate in candidates_by_system.get(system_name, []):
        if Path(candidate).exists():
            return candidate
    return None


def choose_caption_font_argument() -> str:
    return choose_caption_font_file() or "DejaVu-Sans"


def render_tape_text(tape_text: str, font_family: str) -> str:
    replacement = f'Set FontFamily "{font_family}"'
    if FONT_PATTERN.search(tape_text):
        return FONT_PATTERN.sub(replacement, tape_text, count=1)
    return f'{replacement}\n{tape_text}'


def extract_output_path(tape_text: str) -> Path:
    match = OUTPUT_PATTERN.search(tape_text)
    if not match:
        raise ValueError("Tape file must include an Output path")
    return Path(match.group(1).strip())


def replace_output_path(tape_text: str, output_path: Path) -> str:
    replacement = f"Output {output_path.as_posix()}"
    if OUTPUT_PATTERN.search(tape_text):
        return OUTPUT_PATTERN.sub(replacement, tape_text, count=1)
    return f"{replacement}\n{tape_text}"


def extract_title(tape_text: str, tape_path: Path) -> str:
    for line in tape_text.splitlines():
        match = TITLE_PATTERN.match(line)
        if match and not match.group(1).startswith("Run from project root"):
            return match.group(1)
    return tape_path.stem.replace("-", " ").title()


def extract_dimensions(tape_text: str) -> tuple[int, int]:
    width_match = WIDTH_PATTERN.search(tape_text)
    height_match = HEIGHT_PATTERN.search(tape_text)
    width = int(width_match.group(1)) if width_match else 1920
    height = int(height_match.group(1)) if height_match else 1200
    return width, height


def parse_duration_seconds(value: str) -> float:
    tokens = value.strip().split()
    if not tokens:
        return 0.0
    if len(tokens) == 1:
        token = tokens[0].lower()
        if token.endswith("ms"):
            return float(token[:-2]) / 1000.0
        if token.endswith("s"):
            return float(token[:-1])
        return float(token)
    amount = float(tokens[0])
    unit = tokens[1].lower()
    if unit.startswith("ms"):
        return amount / 1000.0
    if unit.startswith("s"):
        return amount
    raise ValueError(f"Unsupported time unit: {value}")


def parse_captions(tape_text: str) -> tuple[list[CaptionCue], float]:
    cues: list[CaptionCue] = []
    elapsed = 0.0
    typing_speed = 0.0
    current_section: str | None = None
    current_start = 0.0

    def close_section(end_time: float) -> None:
        nonlocal current_section, current_start
        if current_section and end_time > current_start:
            cues.append(
                CaptionCue(
                    text=current_section,
                    start_seconds=current_start,
                    end_seconds=end_time,
                )
            )

    for raw_line in tape_text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        section_match = SECTION_PATTERN.match(line)
        if section_match:
            close_section(elapsed)
            current_section = section_match.group(1).strip()
            current_start = elapsed
            continue

        speed_match = TYPING_SPEED_PATTERN.match(line)
        if speed_match:
            typing_speed = parse_duration_seconds(speed_match.group(1))
            continue

        type_match = TYPE_PATTERN.match(line)
        if type_match:
            elapsed += len(type_match.group(1)) * typing_speed
            continue

        if line == "Enter":
            elapsed += ENTER_SECONDS
            continue

        sleep_match = SLEEP_PATTERN.match(line)
        if sleep_match:
            elapsed += parse_duration_seconds(sleep_match.group(1))
            continue

    close_section(elapsed)
    return cues, elapsed


def parse_commands(tape_text: str) -> tuple[list[CommandCue], float]:
    commands: list[CommandCue] = []
    elapsed = 0.0
    typing_speed = 0.0
    active_command: str | None = None

    def close_command(end_time: float) -> None:
        nonlocal active_command
        if active_command:
            commands.append(CommandCue(text=active_command, end_seconds=end_time))
            active_command = None

    for raw_line in tape_text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        speed_match = TYPING_SPEED_PATTERN.match(line)
        if speed_match:
            typing_speed = parse_duration_seconds(speed_match.group(1))
            continue

        type_match = TYPE_PATTERN.match(line)
        if type_match:
            close_command(elapsed)
            active_command = type_match.group(1)
            elapsed += len(active_command) * typing_speed
            continue

        if line == "Enter":
            elapsed += ENTER_SECONDS
            continue

        sleep_match = SLEEP_PATTERN.match(line)
        if sleep_match:
            elapsed += parse_duration_seconds(sleep_match.group(1))
            close_command(elapsed)
            continue

    close_command(elapsed)
    return commands, elapsed


def scale_cues(cues: list[CaptionCue], expected_total: float, actual_total: float) -> list[CaptionCue]:
    if expected_total <= 0 or actual_total <= 0:
        return cues
    scale = actual_total / expected_total
    return [
        CaptionCue(
            text=cue.text,
            start_seconds=cue.start_seconds * scale,
            end_seconds=cue.end_seconds * scale,
        )
        for cue in cues
    ]


def scale_commands(
    commands: list[CommandCue], expected_total: float, actual_total: float
) -> list[CommandCue]:
    if expected_total <= 0 or actual_total <= 0:
        return commands
    scale = actual_total / expected_total
    return [CommandCue(text=command.text, end_seconds=command.end_seconds * scale) for command in commands]


def build_command_caption_cues(
    commands: list[CommandCue], trim_seconds: float = 0.0
) -> list[CaptionCue]:
    cues: list[CaptionCue] = []
    previous_end = 0.0
    for command in commands:
        adjusted_end = command.end_seconds - trim_seconds
        adjusted_start = previous_end - trim_seconds
        previous_end = command.end_seconds
        if adjusted_end <= 0:
            continue
        caption = command_to_intertitle(command.text)
        if not caption:
            continue
        cues.append(
            CaptionCue(
                text=caption,
                start_seconds=max(0.0, adjusted_start),
                end_seconds=max(0.0, adjusted_end),
            )
        )
    return cues


def command_to_intertitle(command_text: str) -> str | None:
    command_text = command_text.strip()
    if not command_text:
        return None
    if not command_text.startswith("/"):
        return None

    parts = command_text.split()
    name = parts[0][1:]
    args = parts[1:]

    if name in {"quit", "exit"}:
        return None
    if name == "push":
        count = len(args)
        return f"Push {count} value{'s' if count != 1 else ''}"
    if name == "peek":
        return "Peek at the top"
    if name == "at" and args:
        return f"Inspect stack index {args[0]}"
    if name == "dup":
        return "Duplicate the top value"
    if name == "pop":
        return "Pop the top value"
    if name == "swap":
        return "Swap the top two values"
    if name == "rotate":
        return "Rotate the top three values"
    if name == "undo":
        return "Undo the previous change"
    if name == "redo":
        return "Redo the last undone change"
    if name == "save":
        return "Save the current session"
    if name == "clear":
        return "Clear the stack"
    if name == "type" and args:
        if args[0] == "str":
            return "Switch to string values"
        if args[0] == "int":
            return "Switch to integer values"
        return f"Switch type to {args[0]}"
    if name == "random" and args:
        return f"Generate {args[0]} random values"
    if name == "load":
        return "Load the saved session"
    return command_text


def format_srt_timestamp(seconds: float) -> str:
    total_ms = max(0, round(seconds * 1000))
    hours, remainder = divmod(total_ms, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, millis = divmod(remainder, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def write_srt(cues: list[CaptionCue], destination: Path, offset_seconds: float = 0.0) -> None:
    lines: list[str] = []
    for index, cue in enumerate(cues, start=1):
        lines.extend(
            [
                str(index),
                f"{format_srt_timestamp(cue.start_seconds + offset_seconds)} --> "
                f"{format_srt_timestamp(cue.end_seconds + offset_seconds)}",
                cue.text,
                "",
            ]
        )
    destination.write_text("\n".join(lines), encoding="utf-8")


def ffprobe_duration_seconds(video_path: Path) -> float:
    completed = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(video_path),
        ],
        capture_output=True,
        check=True,
        text=True,
    )
    return float(completed.stdout.strip())


def create_title_card_image(
    title: str,
    credit: str,
    width: int,
    height: int,
    destination: Path,
    font_file: str | None,
) -> None:
    font = font_file or "Times-New-Roman"
    subprocess.run(
        [
            "magick",
            "-size",
            f"{width}x{height}",
            "xc:#11141a",
            "-font",
            font,
            "-fill",
            "#f3e7c9",
            "-gravity",
            "north",
            "-pointsize",
            "74",
            "-annotate",
            "+0+320",
            title,
            "-fill",
            "#d7c59a",
            "-pointsize",
            "34",
            "-annotate",
            "+0+520",
            "A silent tour through the data structure",
            "-fill",
            "#efe8d8",
            "-pointsize",
            "40",
            "-annotate",
            "+0+700",
            f"Created by {credit}",
            str(destination),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def create_end_card_image(width: int, height: int, destination: Path, font_file: str | None) -> None:
    font = font_file or "Times-New-Roman"
    subprocess.run(
        [
            "magick",
            "-size",
            f"{width}x{height}",
            "xc:#0b0b0b",
            "-font",
            font,
            "-fill",
            "#f6e4b0",
            "-gravity",
            "north",
            "-pointsize",
            "96",
            "-annotate",
            "+0+430",
            "The End",
            "-fill",
            "#ddd4bf",
            "-pointsize",
            "32",
            "-annotate",
            "+0+650",
            "Thanks for watching",
            str(destination),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def create_command_card_image(
    title_text: str,
    command_text: str,
    width: int,
    height: int,
    destination: Path,
    font_file: str | None,
) -> None:
    font = font_file or "Times-New-Roman"
    title_size = max(38, round(height * 0.045))
    command_size = max(24, round(height * 0.025))
    subprocess.run(
        [
            "magick",
            "-size",
            f"{width}x{height}",
            "xc:#120f0a",
            "-font",
            font,
            "-fill",
            "#f2e3bf",
            "-gravity",
            "north",
            "-pointsize",
            str(title_size),
            "-annotate",
            "+0+380",
            title_text,
            "-fill",
            "#ddd4bf",
            "-pointsize",
            str(command_size),
            "-annotate",
            "+0+620",
            command_text,
            str(destination),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def image_to_video(image_path: Path, seconds: float, destination: Path) -> None:
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-loop",
            "1",
            "-t",
            str(seconds),
            "-i",
            str(image_path),
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            str(destination),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def freeze_video_frame(input_video: Path, hold_seconds: float, destination: Path) -> None:
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-sseof",
            "-0.04",
            "-i",
            str(input_video),
            "-frames:v",
            "1",
            "-update",
            "1",
            str(destination),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def trim_video_segment(input_video: Path, start_seconds: float, end_seconds: float, destination: Path) -> None:
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-ss",
            f"{start_seconds:.3f}",
            "-to",
            f"{end_seconds:.3f}",
            "-i",
            str(input_video),
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-an",
            str(destination),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def create_caption_overlay(text: str, width: int, height: int, destination: Path) -> None:
    font = choose_caption_font_argument()
    box_width = max(640, round(width * 0.4))
    box_height = max(96, round(height * 0.1))
    point_size = max(22, round(height * 0.022))
    subprocess.run(
        [
            "magick",
            "-background",
            "rgba(0,0,0,0.55)",
            "-fill",
            "white",
            "-font",
            font,
            "-gravity",
            "center",
            "-size",
            f"{box_width}x{box_height}",
            "-pointsize",
            str(point_size),
            f"caption:{text}",
            str(destination),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def burn_captions_into_video(
    input_video: Path,
    cues: list[CaptionCue],
    width: int,
    height: int,
    output_video: Path,
) -> None:
    x_expr = "main_w-overlay_w-70"
    y_expr = "main_h-overlay_h-150"
    with tempfile.TemporaryDirectory() as overlay_dir_name:
        overlay_dir = Path(overlay_dir_name)
        cmd = ["ffmpeg", "-y", "-i", str(input_video)]
        filter_parts: list[str] = []
        current_stream = "[0:v]"
        for index, cue in enumerate(cues, start=1):
            overlay_path = overlay_dir / f"caption-{index:02d}.png"
            create_caption_overlay(cue.text, width, height, overlay_path)
            cmd.extend(["-loop", "1", "-i", str(overlay_path)])
            next_stream = f"[v{index}]"
            filter_parts.append(
                f"{current_stream}[{index}:v]overlay=x={x_expr}:"
                f"y={y_expr}:shortest=1:eof_action=pass:"
                f"enable='between(t,{cue.start_seconds:.3f},{cue.end_seconds:.3f})'"
                f"{next_stream}"
            )
            current_stream = next_stream
        cmd.extend(
            [
                "-filter_complex",
                ";".join(filter_parts),
                "-map",
                current_stream,
                "-shortest",
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                "-an",
                str(output_video),
            ]
        )
        subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )


def insert_command_intertitles(
    input_video: Path,
    commands: list[CommandCue],
    duration_seconds: float,
    width: int,
    height: int,
    font_file: str | None,
    output_video: Path,
) -> None:
    with tempfile.TemporaryDirectory() as temp_dir_name:
        temp_dir = Path(temp_dir_name)
        parts: list[Path] = []
        current_start = 0.0

        for index, command in enumerate(commands, start=1):
            segment_end = min(command.end_seconds, duration_seconds)
            if segment_end > current_start + 0.01:
                segment_path = temp_dir / f"segment-{index:02d}.mp4"
                trim_video_segment(input_video, current_start, segment_end, segment_path)
                parts.append(segment_path)

            intertitle = command_to_intertitle(command.text)
            if intertitle:
                hold_image = temp_dir / f"hold-{index:02d}.png"
                hold_video = temp_dir / f"hold-{index:02d}.mp4"
                card_image = temp_dir / f"command-{index:02d}.png"
                card_video = temp_dir / f"command-{index:02d}.mp4"
                if segment_end > current_start + 0.01:
                    freeze_video_frame(segment_path, LIVE_HOLD_SECONDS, hold_image)
                    image_to_video(hold_image, LIVE_HOLD_SECONDS, hold_video)
                    parts.append(hold_video)
                create_command_card_image(intertitle, command.text, width, height, card_image, font_file)
                image_to_video(card_image, INTERTITLE_SECONDS, card_video)
                parts.append(card_video)
            current_start = segment_end

        if current_start < duration_seconds - 0.01:
            tail_path = temp_dir / "tail.mp4"
            trim_video_segment(input_video, current_start, duration_seconds, tail_path)
            parts.append(tail_path)

        concat_videos(parts, output_video)


def concat_videos(parts: list[Path], output_path: Path) -> None:
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as handle:
        concat_file = Path(handle.name)
        for part in parts:
            handle.write(f"file '{part.as_posix()}'\n")
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
                str(concat_file),
                "-c",
                "copy",
                str(output_path),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    finally:
        concat_file.unlink(missing_ok=True)


def postprocess_video(
    raw_video: Path,
    output_video: Path,
    tape_text: str,
    tape_path: Path,
    credit: str,
) -> None:
    width, height = extract_dimensions(tape_text)
    title = extract_title(tape_text, tape_path)
    _, expected_total = parse_captions(tape_text)
    actual_total = ffprobe_duration_seconds(raw_video)
    commands, command_expected_total = parse_commands(tape_text)
    scaled_commands = scale_commands(commands, command_expected_total, actual_total)
    trim_seconds = min(LAUNCH_TRIM_SECONDS, actual_total)
    title_font = choose_title_font_file()

    with tempfile.TemporaryDirectory() as temp_dir_name:
        temp_dir = Path(temp_dir_name)
        intro_image = temp_dir / "intro.png"
        intro_video = temp_dir / "intro.mp4"
        trimmed_main_video = temp_dir / "main-trimmed.mp4"
        main_video = temp_dir / "main.mp4"
        outro_image = temp_dir / "outro.png"
        outro_video = temp_dir / "outro.mp4"
        trim_video_segment(raw_video, trim_seconds, actual_total, trimmed_main_video)
        scaled_cues = build_command_caption_cues(scaled_commands, trim_seconds=trim_seconds)

        if scaled_cues:
            burn_captions_into_video(
                trimmed_main_video,
                scaled_cues,
                width=width,
                height=height,
                output_video=main_video,
            )
        else:
            main_video.write_bytes(trimmed_main_video.read_bytes())

        create_title_card_image(title, credit, width, height, intro_image, title_font)
        create_end_card_image(width, height, outro_image, title_font)
        image_to_video(intro_image, INTRO_SECONDS, intro_video)
        image_to_video(outro_image, OUTRO_SECONDS, outro_video)
        output_video.parent.mkdir(parents=True, exist_ok=True)
        concat_videos([intro_video, main_video, outro_video], output_video)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run a VHS tape with an auto-selected font family."
    )
    parser.add_argument("tape", type=Path, help="Path to the source .tape file")
    parser.add_argument(
        "--font-family",
        help="Explicit font family override. Defaults by platform or VHS_FONT_FAMILY.",
    )
    parser.add_argument(
        "--credit",
        default=os.environ.get("VHS_CREDIT", DEFAULT_CREDIT),
        help="Credit line to render on the opening card.",
    )
    parser.add_argument(
        "--print-font",
        action="store_true",
        help="Print the chosen font family and exit.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    font_family = args.font_family or choose_font_family()

    if args.print_font:
        print(font_family)
        return 0

    tape_path = args.tape.resolve()
    original_tape_text = tape_path.read_text(encoding="utf-8")
    output_path = extract_output_path(original_tape_text)

    with tempfile.TemporaryDirectory() as temp_dir_name:
        temp_dir = Path(temp_dir_name)
        raw_output_path = temp_dir / output_path.name
        rendered_text = render_tape_text(original_tape_text, font_family)
        rendered_text = replace_output_path(rendered_text, raw_output_path)

        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", suffix=".tape", delete=False
        ) as handle:
            handle.write(rendered_text)
            temp_tape = Path(handle.name)

        try:
            completed = subprocess.run(
                ["vhs", str(temp_tape)],
                cwd=tape_path.parent.parent,
                check=False,
            )
            if completed.returncode != 0:
                return completed.returncode
            postprocess_video(
                raw_video=raw_output_path,
                output_video=(tape_path.parent.parent / output_path).resolve(),
                tape_text=original_tape_text,
                tape_path=tape_path,
                credit=args.credit,
            )
        finally:
            temp_tape.unlink(missing_ok=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
