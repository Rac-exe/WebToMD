"""CLI entry point — all commands and flags defined here."""

from __future__ import annotations

from pathlib import Path
import sys

import typer

from webtomd.ai.naming import suggest_filename_ai
from webtomd import config as app_config
from webtomd.converter import SelectorNotFoundError, extract_title_hint, to_markdown
from webtomd.fetcher import fetch, get_last_fetch_trace
from webtomd.output import open_in_editor, to_clipboard, to_file, to_stdout
from webtomd.renderer import (
    next_witty_message,
    print_error,
    print_markdown_preview,
    print_success,
    print_warn,
    start_spinner,
)
from webtomd.utils import build_output_path, is_valid_url

app = typer.Typer(
    name="webtomd",
    help="Web to Markdown. No garbage.",
    add_completion=False,
)


def _is_interactive_terminal() -> bool:
    """True when command is run in an interactive terminal session."""
    return sys.stdout.isatty()


def _resolve_output_mode(
    explicit_output: str | None,
    force_stdout: bool,
    interactive: bool,
) -> str:
    """Resolve output mode to either 'file' or 'stdout'."""
    if explicit_output:
        return "file"
    if force_stdout:
        return "stdout"
    if interactive:
        return "file"
    return "stdout"


def _format_trace(trace_strategy: str, trace_note: str) -> str:
    if not trace_note:
        return f"via {trace_strategy}"
    brief = trace_note.strip()
    if len(brief) > 90:
        brief = brief[:87].rstrip() + "..."
    return f"via {trace_strategy} ({brief})"


@app.command()
def snap(
    url: str | None = typer.Argument(None, help="URL to convert"),
    output: str = typer.Option(None, "-o", "--output", help="Save to file"),
    stdout: bool = typer.Option(False, "--stdout", help="Force stdout output"),
    name_strategy: str | None = typer.Option(
        None,
        "--name-strategy",
        help="Filename strategy: deterministic | ai",
    ),
    copy: bool | None = typer.Option(None, "--copy/--no-copy", help="Copy to clipboard"),
    silent: bool | None = typer.Option(None, "--silent/--no-silent", help="No animations (pipe-safe)"),
    configure: bool = typer.Option(False, "--configure", help="Interactive AI provider setup"),
    ai: str = typer.Option(None, "--ai", help="AI mode: summarize | tl;dr | translate | extract | qa"),
    batch: str = typer.Option(None, "--batch", help="File of URLs to batch process"),
    selector: str = typer.Option(None, "--selector", help="CSS selector to target specific content"),
    metadata: bool | None = typer.Option(None, "--metadata/--no-metadata", help="Prepend YAML frontmatter"),
    open_after: bool = typer.Option(False, "--open", help="Open output file in default editor"),
) -> None:
    """Convert any URL to clean Markdown."""
    if configure:
        raise typer.BadParameter("`--configure` lands in Phase 3.")

    if not url:
        raise typer.BadParameter("URL is required. Example: webtomd https://example.com")

    cfg = app_config.load()
    cfg = app_config.merge(
        cfg,
        copy=copy,
        silent=silent,
        metadata=metadata,
        name_strategy=name_strategy,
    )

    if cfg.name_strategy not in {"deterministic", "ai"}:
        raise typer.BadParameter("`--name-strategy` must be one of: deterministic, ai")

    if not is_valid_url(url):
        print_error(f"Invalid URL: {url}", silent=bool(cfg.silent))
        raise typer.Exit(1)

    if batch:
        raise typer.BadParameter("`--batch` lands in Phase 2.")
    if ai:
        raise typer.BadParameter("`--ai` lands in Phase 3.")
    if cfg.metadata:
        raise typer.BadParameter("`--metadata` lands in Phase 2.")

    output_mode = _resolve_output_mode(
        explicit_output=output,
        force_stdout=stdout,
        interactive=_is_interactive_terminal(),
    )

    try:
        with start_spinner(next_witty_message(), silent=bool(cfg.silent)):
            html = fetch(url=url, selector=selector)
            title_hint = extract_title_hint(html, selector=selector)
            markdown = to_markdown(html=html, url=url, metadata=False, selector=selector)
    except SelectorNotFoundError as exc:
        raise typer.BadParameter(str(exc)) from exc

    token_count = len(markdown.split())
    trace = get_last_fetch_trace()
    print_success(
        f"Converted to Markdown ({token_count} tokens) {_format_trace(trace.strategy, trace.note)}",
        silent=bool(cfg.silent),
    )

    if output_mode == "file":
        if output:
            output_path = Path(output)
        else:
            base_dir = Path(cfg.output_dir) if cfg.output_dir else Path.cwd()
            chosen_hint = title_hint
            if cfg.name_strategy == "ai":
                try:
                    chosen_hint = suggest_filename_ai(title_hint=title_hint, markdown=markdown)
                except Exception as exc:
                    print_warn(
                        f"AI naming unavailable ({exc}). Falling back to deterministic naming.",
                        silent=bool(cfg.silent),
                    )
            output_path = build_output_path(base_dir, url=url, title_hint=chosen_hint)
        saved_path = to_file(markdown, output_path)
        print_success(f"Saved to {saved_path}", silent=bool(cfg.silent))
        if bool(cfg.copy):
            to_clipboard(markdown)
            print_success("Copied to clipboard", silent=bool(cfg.silent))
        if open_after:
            open_in_editor(saved_path)
        print_markdown_preview(markdown, silent=bool(cfg.silent))
    else:
        to_stdout(markdown)
        if bool(cfg.copy):
            to_clipboard(markdown)
            print_success("Copied to clipboard", silent=bool(cfg.silent))


if __name__ == "__main__":
    app()
