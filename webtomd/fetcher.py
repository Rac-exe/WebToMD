"""Fetch layer — HTTP fetch with three-stage fallback chain.

Stage 1: trafilatura  (handles ~80% of pages)
Stage 2: readability  (fallback for unusual layouts)
Stage 3: playwright   (full JS render for SPAs — optional install)
"""

from __future__ import annotations

import httpx
import trafilatura
import typer

from webtomd.utils import is_sparse

# Phase 1
def fetch(url: str, selector: str | None = None) -> str:
    """Fetch URL and return extracted HTML content.

    Escalates through the fallback chain automatically on sparse results.
    """
    _ = selector  # kept for Phase 2 selector-aware extraction path
    raw_html = _download_html(url)
    if is_sparse(raw_html) or raw_html is None:
        raise typer.BadParameter(
            "Could not extract meaningful content from this page. "
            "Fallback chain (readability/playwright) lands in Phase 2."
        )

    content = fetch_trafilatura(url, downloaded_html=raw_html)
    if is_sparse(content) or content is None:
        return raw_html

    # Phase 1.5 quality heuristic:
    # if extraction is disproportionately tiny vs source HTML,
    # prefer raw HTML so conversion keeps more page sections.
    if len(raw_html) > 10_000 and len(content) < int(len(raw_html) * 0.08):
        return raw_html

    return content


def fetch_trafilatura(url: str, downloaded_html: str | None = None) -> str | None:
    """Stage 1 — trafilatura extraction."""
    downloaded = downloaded_html or _download_html(url)
    if not downloaded:
        return None

    return trafilatura.extract(
        downloaded,
        output_format="html",
        include_tables=True,
        include_links=True,
        favor_recall=True,
    )


def _download_html(url: str) -> str | None:
    """Download HTML using trafilatura first, then a browser-like httpx fallback."""
    downloaded = trafilatura.fetch_url(url)
    if downloaded:
        return downloaded

    try:
        response = httpx.get(
            url,
            timeout=20.0,
            follow_redirects=True,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0.0.0 Safari/537.36"
                )
            },
        )
        if response.status_code >= 400:
            return None
        return response.text
    except Exception:
        return None


def fetch_readability(url: str) -> str | None:
    """Stage 2 — readability-lxml fallback."""
    raise NotImplementedError


def fetch_playwright(url: str) -> str | None:
    """Stage 3 — headless Chromium fallback (optional install)."""
    raise NotImplementedError
