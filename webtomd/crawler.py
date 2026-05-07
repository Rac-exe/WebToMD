"""Same-domain BFS crawler for --depth recursive page discovery."""

from __future__ import annotations

from collections import deque
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

from webtomd.fetcher import _download_html


def crawl(start_url: str, depth: int, max_pages: int = 50) -> list[str]:
    """Discover same-domain links via BFS up to `depth` levels.

    Returns a deduplicated list of URLs including the start URL.
    """
    if depth <= 0:
        return [start_url]

    parsed_start = urlparse(start_url)
    base_domain = parsed_start.netloc.lower()

    visited: set[str] = set()
    queue: deque[tuple[str, int]] = deque([(start_url, 0)])
    result: list[str] = []

    while queue and len(result) < max_pages:
        url, current_depth = queue.popleft()
        normalized = _normalize_url(url)
        if normalized in visited:
            continue
        visited.add(normalized)
        result.append(url)

        if current_depth >= depth:
            continue

        html = _download_html(url)
        if not html:
            continue

        for link in _extract_links(html, url):
            link_parsed = urlparse(link)
            if link_parsed.netloc.lower() != base_domain:
                continue
            if _normalize_url(link) in visited:
                continue
            queue.append((link, current_depth + 1))

    return result


def _extract_links(html: str, base_url: str) -> list[str]:
    """Extract absolute HTTP(S) links from HTML."""
    soup = BeautifulSoup(html, "html.parser")
    links: list[str] = []
    for anchor in soup.find_all("a", href=True):
        href = anchor["href"].strip()
        if href.startswith(("#", "mailto:", "javascript:", "tel:")):
            continue
        absolute = urljoin(base_url, href)
        parsed = urlparse(absolute)
        if parsed.scheme in ("http", "https"):
            links.append(absolute)
    return links


def _normalize_url(url: str) -> str:
    """Normalize URL for deduplication: strip fragment, trailing slash."""
    parsed = urlparse(url)
    path = parsed.path.rstrip("/") or "/"
    return f"{parsed.scheme}://{parsed.netloc.lower()}{path}"
