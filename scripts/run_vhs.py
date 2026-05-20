#!/usr/bin/env python3
"""Run a VHS tape with a platform-appropriate monospace font."""

from __future__ import annotations

import argparse
import os
import platform
import re
import subprocess
import sys
import tempfile
from pathlib import Path


DEFAULT_FONT_BY_SYSTEM = {
    "Darwin": "Menlo",
    "Linux": "DejaVu Sans Mono",
}

FONT_PATTERN = re.compile(r'^Set FontFamily ".*"$', re.MULTILINE)


def choose_font_family(system_name: str | None = None) -> str:
    override = os.environ.get("VHS_FONT_FAMILY")
    if override:
        return override
    system_name = system_name or platform.system()
    return DEFAULT_FONT_BY_SYSTEM.get(system_name, "DejaVu Sans Mono")


def render_tape_text(tape_text: str, font_family: str) -> str:
    replacement = f'Set FontFamily "{font_family}"'
    if FONT_PATTERN.search(tape_text):
        return FONT_PATTERN.sub(replacement, tape_text, count=1)
    return f'{replacement}\n{tape_text}'


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
    tape_text = tape_path.read_text(encoding="utf-8")
    rendered_text = render_tape_text(tape_text, font_family)

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
    finally:
        temp_tape.unlink(missing_ok=True)

    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
