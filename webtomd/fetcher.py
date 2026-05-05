"""Fetch layer — HTTP fetch with three-stage fallback chain.

Stage 1: trafilatura  (handles ~80% of pages)
Stage 2: readability  (fallback for unusual layouts)
Stage 3: playwright   (full JS render for SPAs — optional install)
"""

from __future__ import annotations

import trafilatura
import typer

from webtomd.utils import is_sparse

# Phase 1
def fetch(url: str, selector: str | None = None) -> str:
    """Fetch URL and return extracted HTML content.

    Escalates through the fallback chain automatically on sparse results.
    """
    _ = selector  # kept for Phase 2 selector-aware extraction path
    content = fetch_trafilatura(url)
    if is_sparse(content):
        raise typer.BadParameter(
            "Could not extract meaningful content from this page. "
            "Phase 1 only supports the primary extraction path. "
            "Fallback chain lands in Phase 2."
        )
    if content is None:
        # Defensive guard for type checkers after sparse check.
        raise typer.BadParameter("No content extracted from URL.")
    return content


def fetch_trafilatura(url: str) -> str | None:
    """Stage 1 — trafilatura extraction."""
    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        return None

    return trafilatura.extract(
        downloaded,
        output_format="html",
        include_tables=True,
        include_links=True,
        favor_recall=True,
    )


def fetch_readability(url: str) -> str | None:
    """Stage 2 — readability-lxml fallback."""
    raise NotImplementedError


def fetch_playwright(url: str) -> str | None:
    """Stage 3 — headless Chromium fallback (optional install)."""
    raise NotImplementedError
