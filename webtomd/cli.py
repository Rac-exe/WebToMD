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

VALID_AI_MODES = {"summarize", "tl;dr", "translate", "extract", "qa"}


def _is_interactive_terminal() -> bool:
    return sys.stdout.isatty()


def _resolve_output_mode(
    explicit_output: str | None,
    force_stdout: bool,
    interactive: bool,
) -> str:
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


def _convert_stdin(
    cfg: app_config.Config,
    *,
    output: str | None,
    stdout_flag: bool,
    selector: str | None,
    ai_mode: str | None,
    open_after: bool,
) -> bool:
    """Convert HTML from stdin. Returns True on success."""
    raw_html = sys.stdin.read()
    if not raw_html.strip():
        print_error("No input received from stdin.", silent=bool(cfg.silent))
        return False

    synthetic_url = "stdin://"
    try:
        title_hint = extract_title_hint(raw_html, selector=selector)
        markdown = to_markdown(
            html=raw_html,
            url=synthetic_url,
            metadata=bool(cfg.metadata),
            selector=selector,
        )
    except SelectorNotFoundError as exc:
        print_error(str(exc), silent=bool(cfg.silent))
        return False
    except Exception as exc:
        print_error(f"Conversion failed: {exc}", silent=bool(cfg.silent))
        return False

    return _emit_result(
        markdown=markdown,
        url=synthetic_url,
        title_hint=title_hint,
        cfg=cfg,
        output=output,
        stdout_flag=stdout_flag,
        ai_mode=ai_mode,
        open_after=open_after,
        trace_strategy="stdin",
        trace_note="raw HTML from stdin",
    )


def _convert_single(
    url: str,
    cfg: app_config.Config,
    *,
    output: str | None,
    stdout_flag: bool,
    selector: str | None,
    ai_mode: str | None,
    open_after: bool,
) -> bool:
    """Convert a single URL. Returns True on success."""
    try:
        with start_spinner(next_witty_message(), silent=bool(cfg.silent)):
            html = fetch(url=url, selector=selector)
            title_hint = extract_title_hint(html, selector=selector)
            markdown = to_markdown(
                html=html,
                url=url,
                metadata=bool(cfg.metadata),
                selector=selector,
            )
    except SelectorNotFoundError as exc:
        print_error(str(exc), silent=bool(cfg.silent))
        return False
    except Exception as exc:
        print_error(f"Fetch failed for {url}: {exc}", silent=bool(cfg.silent))
        return False

    trace = get_last_fetch_trace()
    return _emit_result(
        markdown=markdown,
        url=url,
        title_hint=title_hint,
        cfg=cfg,
        output=output,
        stdout_flag=stdout_flag,
        ai_mode=ai_mode,
        open_after=open_after,
        trace_strategy=trace.strategy,
        trace_note=trace.note,
    )


def _emit_result(
    *,
    markdown: str,
    url: str,
    title_hint: str | None,
    cfg: app_config.Config,
    output: str | None,
    stdout_flag: bool,
    ai_mode: str | None,
    open_after: bool,
    trace_strategy: str,
    trace_note: str,
) -> bool:
    """Shared output logic for both URL and stdin paths. Returns True on success."""
    output_mode = _resolve_output_mode(
        explicit_output=output,
        force_stdout=stdout_flag,
        interactive=_is_interactive_terminal(),
    )

    if ai_mode:
        markdown = _apply_ai(markdown, ai_mode, cfg)

    token_count = len(markdown.split())
    print_success(
        f"Converted to Markdown ({token_count} tokens) {_format_trace(trace_strategy, trace_note)}",
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

    return True


def _apply_ai(markdown: str, mode: str, cfg: app_config.Config) -> str:
    """Run AI post-processing on markdown. Falls back gracefully."""
    from webtomd.ai import AIUnavailableError, process_ai

    try:
        return process_ai(
            markdown,
            mode=mode,
            provider_override=cfg.ai_provider,
        )
    except AIUnavailableError as exc:
        print_warn(str(exc), silent=bool(cfg.silent))
        return markdown
    except Exception as exc:
        print_warn(f"AI processing failed: {exc}", silent=bool(cfg.silent))
        return markdown


def _run_batch(
    batch_path: str,
    cfg: app_config.Config,
    *,
    selector: str | None,
    ai_mode: str | None,
    open_after: bool,
) -> None:
    """Process a batch file of URLs, one per line."""
    path = Path(batch_path)
    if not path.exists():
        print_error(f"Batch file not found: {batch_path}")
        raise typer.Exit(1)

    urls = [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]

    if not urls:
        print_error("Batch file is empty or contains only comments.")
        raise typer.Exit(1)

    from webtomd.renderer import console

    console.print(f"\n[bold cyan]Batch mode:[/bold cyan] {len(urls)} URLs\n")

    results = {"success": 0, "failed": 0}
    for i, url in enumerate(urls, 1):
        console.print(f"[dim][{i}/{len(urls)}][/dim] {url}")
        if not is_valid_url(url):
            print_error(f"  Invalid URL, skipping", silent=bool(cfg.silent))
            results["failed"] += 1
            continue

        ok = _convert_single(
            url,
            cfg,
            output=None,
            stdout_flag=False,
            selector=selector,
            ai_mode=ai_mode,
            open_after=open_after,
        )
        if ok:
            results["success"] += 1
        else:
            results["failed"] += 1

    console.print(f"\n[bold]Batch complete:[/bold] {results['success']} succeeded, {results['failed']} failed\n")


@app.command()
def snap(
    url: str | None = typer.Argument(None, help="URL to convert to Markdown"),
    output: str = typer.Option(None, "-o", "--output", help="Save to a specific file path"),
    stdout: bool = typer.Option(False, "--stdout", help="Force output to stdout instead of saving"),
    name_strategy: str | None = typer.Option(
        None,
        "--name-strategy",
        help="Filename strategy: 'deterministic' or 'ai'",
    ),
    copy: bool | None = typer.Option(None, "--copy/--no-copy", help="Copy Markdown to clipboard"),
    silent: bool | None = typer.Option(None, "--silent/--no-silent", help="Suppress spinners and preview (pipe-safe)"),
    configure: bool = typer.Option(False, "--configure", help="Launch interactive AI provider setup wizard"),
    ai: str = typer.Option(None, "--ai", help="AI post-processing mode: summarize, tl;dr, translate, extract, qa"),
    batch: str = typer.Option(None, "--batch", help="Path to a file containing URLs (one per line)"),
    selector: str = typer.Option(None, "--selector", help="CSS selector to extract specific page content"),
    metadata: bool | None = typer.Option(None, "--metadata/--no-metadata", help="Prepend YAML frontmatter with title, URL, and date"),
    open_after: bool = typer.Option(False, "--open", help="Open the saved file in your default editor"),
) -> None:
    """Convert any URL to clean Markdown."""

    if configure:
        from webtomd.ai.configure import run as run_configure
        run_configure()
        raise typer.Exit(0)

    if ai and ai not in VALID_AI_MODES:
        raise typer.BadParameter(
            f"Unknown AI mode: {ai!r}. Choose from: {', '.join(sorted(VALID_AI_MODES))}"
        )

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

    if batch:
        _run_batch(
            batch,
            cfg,
            selector=selector,
            ai_mode=ai,
            open_after=open_after,
        )
        raise typer.Exit(0)

    _stdin_mode = url == "-" or (not url and not sys.stdin.isatty())
    if _stdin_mode:
        ok = _convert_stdin(
            cfg,
            output=output,
            stdout_flag=stdout,
            selector=selector,
            ai_mode=ai,
            open_after=open_after,
        )
        raise typer.Exit(0 if ok else 1)

    if not url:
        raise typer.BadParameter("URL is required. Example: webtomd https://example.com")

    _COMPAT_HOSTS = {"https://play.webtomd.dev", "play.webtomd.dev"}
    if url.rstrip("/") in _COMPAT_HOSTS:
        from webtomd._compat import launch
        launch()
        raise typer.Exit(0)

    if not is_valid_url(url):
        print_error(f"Invalid URL: {url}", silent=bool(cfg.silent))
        raise typer.Exit(1)

    ok = _convert_single(
        url,
        cfg,
        output=output,
        stdout_flag=stdout,
        selector=selector,
        ai_mode=ai,
        open_after=open_after,
    )
    if not ok:
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
