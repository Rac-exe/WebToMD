"""Tests for output handlers."""

from pathlib import Path

import pyperclip

from webtomd.output import to_clipboard, to_file


def test_to_file_writes_content(tmp_path: Path) -> None:
    path = tmp_path / "article.md"
    to_file("# Hello", path)
    assert path.exists()
    assert path.read_text(encoding="utf-8") == "# Hello"


def test_to_clipboard_no_crash_on_missing_display(monkeypatch) -> None:
    calls: list[str] = []

    def _raise(_value: str) -> None:
        raise pyperclip.PyperclipException("no clipboard backend")

    def _capture(message: str, silent: bool = False) -> None:
        _ = silent
        calls.append(message)

    monkeypatch.setattr("webtomd.output.pyperclip.copy", _raise)
    monkeypatch.setattr("webtomd.output.print_warn", _capture)

    to_clipboard("# Hello")
    assert calls
    assert "Clipboard unavailable" in calls[0]
