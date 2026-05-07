"""Terminal renderer — all rich UI lives here.

Respects --silent flag for pipe-safe output.
"""

from __future__ import annotations

from contextlib import contextmanager
from itertools import cycle

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax

WITTY_MESSAGES = [
    "Evicting divs and spans...",
    "Negotiating with JavaScript...",
    "Asking the internet nicely...",
    "Stripping the HTML bloat...",
    "Untangling the tag soup...",
    "Persuading the DOM to cooperate...",
    "Filtering out the cookie banners...",
    "Removing 47 tracking scripts...",
]

console = Console()
silent_console = Console(quiet=True)
_witty_cycle = cycle(WITTY_MESSAGES)


def get_console(silent: bool = False) -> Console:
    return silent_console if silent else console


def _safe_symbol(preferred: str, fallback: str) -> str:
    """Return preferred glyph if stream encoding supports it."""
    encoding = getattr(console.file, "encoding", None) or "utf-8"
    try:
        preferred.encode(encoding)
        return preferred
    except Exception:
        return fallback


def next_witty_message() -> str:
    """Return the next witty spinner line in a stable cycle."""
    return next(_witty_cycle)


@contextmanager
def start_spinner(message: str, silent: bool = False):
    """Return a rich Progress spinner context manager."""
    if silent:
        yield None
        return

    with Progress(
        SpinnerColumn(),
        TextColumn("[cyan]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        task_id = progress.add_task(message, total=None)
        yield progress, task_id


def print_success(message: str, silent: bool = False) -> None:
    """Print a green success line."""
    if silent:
        return
    mark = _safe_symbol("✓", "OK")
    console.print(f"[green]{mark} {message}[/green]")


def print_warn(message: str, silent: bool = False) -> None:
    """Print an amber warning line."""
    if silent:
        return
    mark = _safe_symbol("⚠", "WARN")
    console.print(f"[yellow]{mark} {message}[/yellow]")


def print_error(message: str, silent: bool = False) -> None:
    """Print a red error line."""
    if silent:
        return
    mark = _safe_symbol("✗", "ERR")
    console.print(f"[red]{mark} {message}[/red]")


def print_markdown_preview(markdown: str, silent: bool = False) -> None:
    """Syntax-highlight and print the first N lines of markdown."""
    if silent:
        return
    lines = markdown.splitlines()
    preview = "\n".join(lines[:30])
    if len(lines) > 30:
        preview += "\n\n... (truncated)"
    console.print(Syntax(preview, "markdown", theme="monokai", word_wrap=True))


def print_batch_progress(urls: list[str], silent: bool = False):
    """Return a rich Progress bar context manager for batch mode."""
    raise NotImplementedError
