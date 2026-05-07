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
READABILITY_STAGE_TIMEOUT_S = 10.0
PLAYWRIGHT_STAGE_TIMEOUT_S = 20.0
TRAFILATURA_MIN_KEEP_RATIO = 0.08
MIN_ACCEPTABLE_SCORE = 0.18
NAV_TOKEN_PENALTY = (
    "skip to content",
    "cookie settings",
    "accept all cookies",
    "reject all cookies",
    "sign up",
    "open app",
    "loading...",
)


@dataclass
class FetchTrace:
    strategy: str
    note: str


@dataclass
class ExtractCandidate:
    strategy: str
    content: str
    score: float
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

    stage = _resolve_stage_timeouts(url=url, raw_html=raw_html)

    candidates: list[ExtractCandidate] = []
    content = _invoke_timeout_kw(
        fetch_trafilatura,
        url,
        downloaded_html=raw_html,
        timeout_s=stage["extract_timeout_s"],
    )
    _append_candidate(
        candidates,
        strategy="trafilatura",
        content=content,
        source_html=raw_html,
        note="primary extraction",
    )

    if _should_try_readability(raw_html):
        readable = _invoke_timeout_kw(
            fetch_readability,
            url,
            downloaded_html=raw_html,
            timeout_s=stage["readability_timeout_s"],
        )
        _append_candidate(
            candidates,
            strategy="readability",
            content=readable,
            source_html=raw_html,
            note="fallback extraction",
        )

    winner = _pick_best_candidate(candidates)
    if winner is not None:
        _set_trace(winner.strategy, f"{winner.note}; score={winner.score:.3f}")
        return winner.content

    if _looks_js_rendered(raw_html):
        rendered = _invoke_timeout_kw(
            fetch_playwright,
            url,
            timeout_s=stage["playwright_timeout_s"],
        )
        if rendered and not is_sparse(rendered):
            rendered_candidates: list[ExtractCandidate] = []
            rendered_primary = _invoke_timeout_kw(
                fetch_trafilatura,
                url,
                downloaded_html=rendered,
                timeout_s=stage["extract_timeout_s"],
            )
            _append_candidate(
                rendered_candidates,
                strategy="playwright+trafilatura",
                content=rendered_primary,
                source_html=rendered,
                note="rendered trafilatura extraction",
            )

            rendered_readable = _invoke_timeout_kw(
                fetch_readability,
                url,
                downloaded_html=rendered,
                timeout_s=stage["readability_timeout_s"],
            )
            _append_candidate(
                rendered_candidates,
                strategy="playwright+readability",
                content=rendered_readable,
                source_html=rendered,
                note="rendered readability fallback",
            )

            rendered_winner = _pick_best_candidate(rendered_candidates)
            if rendered_winner is not None:
                _set_trace(
                    rendered_winner.strategy,
                    f"{rendered_winner.note}; score={rendered_winner.score:.3f}",
                )
                return rendered_winner.content

            _set_trace("playwright_raw", "rendered candidates too weak; using rendered html")
            return rendered

    _set_trace("raw_html", "all extractor candidates below quality threshold")
    return raw_html


def fetch_trafilatura(
    url: str,
    downloaded_html: str | None = None,
    timeout_s: float = EXTRACT_STAGE_TIMEOUT_S,
) -> str | None:
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
        timeout_s=timeout_s,
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


def fetch_readability(
    url: str,
    downloaded_html: str | None = None,
    timeout_s: float = READABILITY_STAGE_TIMEOUT_S,
) -> str | None:
    """Stage 2 — readability-lxml fallback."""
    downloaded = downloaded_html or _download_html(url, timeout_s=DEFAULT_DOWNLOAD_TIMEOUT_S)
    if not downloaded:
        return None
    return fetch_readability_from_html(downloaded, timeout_s=timeout_s)


def fetch_readability_from_html(
    html: str,
    timeout_s: float = READABILITY_STAGE_TIMEOUT_S,
) -> str | None:
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

    return _run_with_timeout(_extract, timeout_s=timeout_s)


def fetch_playwright(url: str, timeout_s: float = PLAYWRIGHT_STAGE_TIMEOUT_S) -> str | None:
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

    return _run_with_timeout(_render, timeout_s=timeout_s)


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


def _resolve_stage_timeouts(url: str, raw_html: str) -> dict[str, float]:
    """Tune stage budgets for heavy pages to reduce worst-case latency."""
    html_len = len(raw_html)
    script_count = raw_html.lower().count("<script")
    heavy_host = any(h in url.lower() for h in ("minecraft.net",))
    is_heavy = heavy_host or html_len > 450_000 or script_count > 120

    if is_heavy:
        return {
            "extract_timeout_s": 8.0,
            "readability_timeout_s": 7.0,
            "playwright_timeout_s": 12.0,
        }

    return {
        "extract_timeout_s": EXTRACT_STAGE_TIMEOUT_S,
        "readability_timeout_s": READABILITY_STAGE_TIMEOUT_S,
        "playwright_timeout_s": PLAYWRIGHT_STAGE_TIMEOUT_S,
    }


def _invoke_timeout_kw(func, *args, timeout_s: float, **kwargs):
    """Call helper funcs with timeout kw, preserving monkeypatched test signatures."""
    try:
        return func(*args, timeout_s=timeout_s, **kwargs)
    except TypeError:
        return func(*args, **kwargs)


def _append_candidate(
    candidates: list[ExtractCandidate],
    strategy: str,
    content: str | None,
    source_html: str,
    note: str,
) -> None:
    if not content:
        return

    if strategy.endswith("trafilatura") and not _is_good_trafilatura(content, source_html):
        return
    if strategy.endswith("readability") and not _is_good_fallback(content, source_html):
        return
    if strategy not in {"trafilatura", "readability", "playwright+trafilatura", "playwright+readability"}:
        return

    score = _quality_score(content=content, source_html=source_html)
    if score < MIN_ACCEPTABLE_SCORE:
        return
    candidates.append(ExtractCandidate(strategy=strategy, content=content, score=score, note=note))


def _pick_best_candidate(candidates: list[ExtractCandidate]) -> ExtractCandidate | None:
    if not candidates:
        return None
    return max(candidates, key=lambda c: c.score)


def _quality_score(content: str, source_html: str) -> float:
    text = re.sub(r"<[^>]+>", " ", content)
    tokens = text.split()
    token_count = len(tokens)
    if token_count == 0:
        return 0.0

    source_len = max(len(source_html), 1)
    keep_ratio = min(len(content) / source_len, 1.0)
    heading_hits = len(re.findall(r"<h[1-6][^>]*>", content, flags=re.IGNORECASE))
    link_count = len(re.findall(r"<a\b", content, flags=re.IGNORECASE))
    link_density = link_count / max(token_count, 1)

    nav_penalty = 0.0
    lowered = text.lower()
    for marker in NAV_TOKEN_PENALTY:
        if marker in lowered:
            nav_penalty += 0.03

    score = (
        min(token_count / 1200.0, 1.0) * 0.45
        + min(keep_ratio / 0.25, 1.0) * 0.35
        + min(heading_hits / 18.0, 1.0) * 0.2
    )
    score -= min(link_density, 0.35) * 0.3
    score -= nav_penalty
    return max(score, 0.0)
