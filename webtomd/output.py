"""Output handler — stdout, file, clipboard."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pyperclip

from webtomd.renderer import print_warn


def to_stdout(markdown: str) -> None:
    """Print markdown to stdout."""
    print(markdown)


def to_file(markdown: str, path: Path) -> Path:
    """Write markdown to a file. Returns the path written."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(markdown, encoding="utf-8")
    return path


def to_clipboard(markdown: str) -> None:
    """Copy markdown to system clipboard. Gracefully warns if unavailable."""
    try:
        pyperclip.copy(markdown)
    except pyperclip.PyperclipException:
        hint = (
            "Clipboard unavailable. On Linux install xclip/xsel; "
            "on headless servers use -o to save a file."
        )
        print_warn(hint)


def open_in_editor(path: Path) -> None:
    """Open a file in the system default editor."""
    if sys.platform.startswith("win"):
        os.startfile(str(path))  # type: ignore[attr-defined]
        return

    if sys.platform == "darwin":
        subprocess.run(["open", str(path)], check=False)
        return

    subprocess.run(["xdg-open", str(path)], check=False)
