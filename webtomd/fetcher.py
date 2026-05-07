"""Fetch layer — HTTP fetch with staged fallback chain."""

from __future__ import annotations

import httpx
import re
import trafilatura
import typer
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeout
from dataclasses import dataclass

from webtomd.utils import is_sparse


DEFAULT_DOWNLOAD_TIMEOUT_S = 20.0
FETCH_STAGE_TIMEOUT_S = 25.0
EXTRACT_STAGE_TIMEOUT_S = 12.0
TRAFILATURA_MIN_KEEP_RATIO = 0.08


@dataclass
class FetchTrace:
    strategy: str
    note: str


LAST_FETCH_TRACE: FetchTrace = FetchTrace(strategy="none", note="")


def get_last_fetch_trace() -> FetchTrace:
    """Return strategy details from the latest fetch() call."""
    return LAST_FETCH_TRACE


def _set_trace(strategy: str, note: str = "") -> None:
    global LAST_FETCH_TRACE
    LAST_FETCH_TRACE = FetchTrace(strategy=strategy, note=note)


def fetch(url: str, selector: str | None = None) -> str:
    """Fetch URL and return extracted HTML content.

    Escalates through the fallback chain automatically on sparse results.
    """
    raw_html = _download_html(url)
    if is_sparse(raw_html) or raw_html is None:
        raise typer.BadParameter(
            "Could not fetch meaningful content from this page."
        )

    if selector:
        _set_trace("selector_raw_html", "selector mode uses downloaded html")
        return raw_html

    content = fetch_trafilatura(url, downloaded_html=raw_html)
    if _is_good_trafilatura(content, raw_html):
        _set_trace("trafilatura", "primary extraction succeeded")
        return content  # type: ignore[return-value]

    if _should_try_readability(raw_html):
        readable = fetch_readability(url, downloaded_html=raw_html)
        if _is_good_fallback(readable, source_html=raw_html):
            _set_trace("readability", "fallback extraction succeeded")
            return readable  # type: ignore[return-value]

    if _looks_js_rendered(raw_html):
        rendered = fetch_playwright(url)
        if rendered and not is_sparse(rendered):
            rendered_primary = fetch_trafilatura(url, downloaded_html=rendered)
            if _is_good_trafilatura(rendered_primary, rendered):
                _set_trace("playwright+trafilatura", "js-rendered page extracted")
                return rendered_primary  # type: ignore[return-value]

            rendered_readable = fetch_readability(url, downloaded_html=rendered)
            if _is_good_fallback(rendered_readable, source_html=rendered):
                _set_trace("playwright+readability", "js-rendered readability fallback")
                return rendered_readable  # type: ignore[return-value]

            _set_trace("playwright_raw", "using rendered HTML as best effort")
            return rendered

    _set_trace("raw_html", "all extractors sparse; returning downloaded html")
    return raw_html


def fetch_trafilatura(url: str, downloaded_html: str | None = None) -> str | None:
    """Stage 1 — trafilatura extraction."""
    downloaded = downloaded_html or _download_html(url, timeout_s=DEFAULT_DOWNLOAD_TIMEOUT_S)
    if not downloaded:
        return None

    return _run_with_timeout(
        lambda: trafilatura.extract(
            downloaded,
            output_format="html",
            include_tables=True,
            include_links=True,
            favor_recall=True,
        ),
        timeout_s=EXTRACT_STAGE_TIMEOUT_S,
    )


def _download_html(url: str, timeout_s: float = DEFAULT_DOWNLOAD_TIMEOUT_S) -> str | None:
    """Download HTML using trafilatura first, then a browser-like httpx fallback."""
    downloaded = _run_with_timeout(lambda: trafilatura.fetch_url(url), timeout_s=min(timeout_s, FETCH_STAGE_TIMEOUT_S))
    if downloaded:
        return downloaded

    try:
        response = _run_with_timeout(
            lambda: httpx.get(
                url,
                timeout=timeout_s,
                follow_redirects=True,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/124.0.0.0 Safari/537.36"
                    )
                },
            ),
            timeout_s=min(timeout_s + 2.0, FETCH_STAGE_TIMEOUT_S),
        )
        if response is None:
            return None
        if response.status_code >= 400:
            return None
        return response.text
    except Exception:
        return None


def fetch_readability(url: str, downloaded_html: str | None = None) -> str | None:
    """Stage 2 — readability-lxml fallback."""
    downloaded = downloaded_html or _download_html(url, timeout_s=DEFAULT_DOWNLOAD_TIMEOUT_S)
    if not downloaded:
        return None
    return fetch_readability_from_html(downloaded)


def fetch_readability_from_html(html: str) -> str | None:
    """Run readability directly on an HTML string."""
    if not html:
        return None
    try:
        from readability import Document
    except Exception:
        return None

    def _extract() -> str | None:
        doc = Document(html)
        summary = doc.summary(html_partial=True) or ""
        if is_sparse(summary):
            return None
        title = (doc.short_title() or "").strip()
        if title:
            return f"<h1>{title}</h1>\n{summary}"
        return summary

    return _run_with_timeout(_extract, timeout_s=EXTRACT_STAGE_TIMEOUT_S)


def fetch_playwright(url: str) -> str | None:
    """Stage 3 — headless Chromium fallback (optional install)."""
    try:
        from playwright.sync_api import sync_playwright
    except Exception:
        return None

    def _render() -> str | None:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            try:
                page = browser.new_page()
                page.goto(url, wait_until="domcontentloaded", timeout=15_000)
                page.wait_for_timeout(1_500)
                return page.content()
            finally:
                browser.close()

    return _run_with_timeout(_render, timeout_s=20.0)


def _run_with_timeout(func, timeout_s: float):
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(func)
        try:
            return future.result(timeout=timeout_s)
        except FutureTimeout:
            future.cancel()
            return None
        except Exception:
            return None


def _is_good_trafilatura(content: str | None, raw_html: str) -> bool:
    if is_sparse(content) or content is None:
        return False
    if len(raw_html) > 10_000 and len(content) < int(len(raw_html) * TRAFILATURA_MIN_KEEP_RATIO):
        return False
    return True


def _is_good_fallback(content: str | None, source_html: str | None = None) -> bool:
    if not content or is_sparse(content):
        return False
    if source_html and len(source_html) > 8_000 and len(content) < int(len(source_html) * 0.03):
        return False
    return True


def _looks_js_rendered(html: str) -> bool:
    snippet = html.lower()
    if "id=\"__next\"" in snippet or "id=\"root\"" in snippet:
        return True
    script_count = snippet.count("<script")
    body_text = len(" ".join(re.sub(r"<[^>]+>", " ", html).split()))
    return script_count > 25 and body_text < 150


def _should_try_readability(html: str) -> bool:
    """Readability is most helpful when page chrome overwhelms body content."""
    snippet = html.lower()
    chrome_markers = ("<article", "<main", "<nav", "<aside", "<section", "role=\"main\"")
    link_count = snippet.count("<a ")
    return any(marker in snippet for marker in chrome_markers) or link_count > 25
