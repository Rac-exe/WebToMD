"""CLI entry point — all commands and flags defined here."""

from __future__ import annotations

from pathlib import Path

import typer

from webtomd import config as app_config
from webtomd.converter import to_markdown
from webtomd.fetcher import fetch
from webtomd.output import open_in_editor, to_clipboard, to_file, to_stdout
from webtomd.renderer import (
    next_witty_message,
    print_error,
    print_markdown_preview,
    print_success,
    start_spinner,
)
from webtomd.utils import is_valid_url, url_to_filename

app = typer.Typer(
    name="webtomd",
    help="Web to Markdown. No garbage.",
    add_completion=False,
)


@app.command()
def snap(
    url: str | None = typer.Argument(None, help="URL to convert"),
    output: str = typer.Option(None, "-o", "--output", help="Save to file"),
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
    cfg = app_config.merge(cfg, copy=copy, silent=silent, metadata=metadata)

    if not is_valid_url(url):
        print_error(f"Invalid URL: {url}", silent=bool(cfg.silent))
        raise typer.Exit(1)

    if batch:
        raise typer.BadParameter("`--batch` lands in Phase 2.")
    if ai:
        raise typer.BadParameter("`--ai` lands in Phase 3.")
    if selector:
        raise typer.BadParameter("`--selector` lands in Phase 2.")
    if cfg.metadata:
        raise typer.BadParameter("`--metadata` lands in Phase 2.")

    output_path: Path | None = None
    if output:
        output_path = Path(output)
    elif cfg.output_dir:
        output_path = Path(cfg.output_dir) / f"{url_to_filename(url)}.md"

    with start_spinner(next_witty_message(), silent=bool(cfg.silent)):
        html = fetch(url=url)
        markdown = to_markdown(html=html, url=url, metadata=False)

    token_count = len(markdown.split())
    print_success(f"Converted to Markdown ({token_count} tokens)", silent=bool(cfg.silent))

    if output_path:
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
