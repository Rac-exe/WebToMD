"""Conversion layer — HTML to clean Markdown via markdownify."""

from __future__ import annotations

import re
from datetime import date

from bs4 import BeautifulSoup
from markdownify import markdownify as md


class SelectorNotFoundError(ValueError):
    """Raised when a CSS selector does not match any element."""


def extract_title_hint(html: str, selector: str | None = None) -> str | None:
    """Extract a best-effort title from HTML for filename generation."""
    source_html = _sanitize_html(html)
    soup = BeautifulSoup(source_html, "html.parser")

    if selector:
        selected = soup.select_one(selector)
        if selected is not None:
            heading = selected.find(["h1", "h2", "h3"])
            if heading and heading.get_text(strip=True):
                return heading.get_text(strip=True)

    if soup.title and soup.title.get_text(strip=True):
        return soup.title.get_text(strip=True)

    h1 = soup.find("h1")
    if h1 and h1.get_text(strip=True):
        return h1.get_text(strip=True)
    return None


def to_markdown(
    html: str,
    url: str | None = None,
    metadata: bool = False,
    selector: str | None = None,
) -> str:
    """Convert HTML to clean Markdown.

    Args:
        html:      Raw HTML string.
        url:       Source URL (used in YAML frontmatter if metadata=True).
        metadata:  Prepend YAML frontmatter (title, url, date).
        selector:  CSS selector to extract specific element before conversion.

    Returns:
        Clean Markdown string.
    """
    source_html = _sanitize_html(html)
    title = extract_title_hint(source_html, selector=selector) or "Untitled"

    if selector:
        soup = BeautifulSoup(source_html, "html.parser")
        selected = soup.select_one(selector)
        if selected is None:
            raise SelectorNotFoundError(f"No element matched selector: {selector}")
        source_html = str(selected)

    markdown = md(
        source_html,
        heading_style="ATX",
        bullets="-",
        strip=["script", "style", "nav", "footer"],
    )
    markdown = _normalize_numbering(markdown)
    markdown = _drop_css_noise(markdown)
    markdown = _drop_markdown_chrome(markdown)
    markdown = re.sub(r"\n{3,}", "\n\n", markdown).strip()

    if metadata and url:
        return _build_frontmatter(title=title, url=url) + "\n\n" + markdown
    return markdown


def _build_frontmatter(title: str, url: str) -> str:
    """Build YAML frontmatter block."""
    safe_title = title.replace('"', '\\"')
    safe_url = url.replace('"', '\\"')
    today = date.today().isoformat()
    return (
        "---\n"
        f'title: "{safe_title}"\n'
        f'url: "{safe_url}"\n'
        f'date: "{today}"\n'
        "---"
    )


def _normalize_numbering(markdown: str) -> str:
    """Fix common markdownify/trafilatura numbering glitches.

    Examples:
    - "## 1Getting Started" -> "## 1. Getting Started"
    - "- 1Open app" -> "- 1. Open app"
    - "1Install" -> "1. Install"
    """
    lines = markdown.splitlines()
    normalized: list[str] = []

    heading_re = re.compile(r"^(#{1,6}\s+)(\d+)([A-Za-z].*)$")
    list_re = re.compile(r"^(\s*[-*]\s+)(\d+)([A-Za-z].*)$")
    plain_re = re.compile(r"^(\s*)(\d+)([A-Z][A-Za-z].*)$")

    for line in lines:
        m = heading_re.match(line)
        if m:
            normalized.append(f"{m.group(1)}{m.group(2)}. {m.group(3)}")
            continue

        m = list_re.match(line)
        if m:
            normalized.append(f"{m.group(1)}{m.group(2)}. {m.group(3)}")
            continue

        m = plain_re.match(line)
        if m:
            normalized.append(f"{m.group(1)}{m.group(2)}. {m.group(3)}")
            continue

        normalized.append(line)

    return "\n".join(normalized)


def _sanitize_html(html: str) -> str:
    """Remove high-noise tags before markdown conversion."""
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup.find_all(["script", "style", "noscript", "template"]):
        tag.decompose()
    _prune_structural_noise(soup)
    return str(soup)


def _drop_css_noise(markdown: str) -> str:
    """Drop common CSS blobs that can leak through raw HTML conversion."""
    cleaned: list[str] = []
    for line in markdown.splitlines():
        stripped = line.strip()
        if not stripped:
            cleaned.append(line)
            continue

        if stripped.startswith("@import url("):
            continue

        # Heuristic CSS-like line filter.
        if (
            ("{" in stripped and "}" in stripped)
            or stripped.startswith("@keyframes ")
            or stripped.startswith(".")
        ) and ":" in stripped:
            continue

        cleaned.append(line)

    return "\n".join(cleaned)


def _prune_structural_noise(soup: BeautifulSoup) -> None:
    """Drop obvious chrome/sidebar/cookie shells before conversion."""
    has_primary_content = bool(soup.find(["main", "article"]))
    structural_selectors = [
        "footer",
        "aside",
        "[role='navigation']",
        "[class*='sidebar' i]",
        "[id*='sidebar' i]",
        "[class*='breadcrumbs' i]",
        "[id*='breadcrumbs' i]",
    ]
    if has_primary_content:
        structural_selectors.extend(["nav", "header"])

    selector_groups = [
        *structural_selectors,
        "[id*='cookie' i]",
        "[class*='cookie' i]",
        "[id*='consent' i]",
        "[class*='consent' i]",
    ]

    for selector in selector_groups:
        for node in soup.select(selector):
            # Keep unusually large blocks to avoid deleting real page content.
            if len(node.get_text(" ", strip=True)) < 2_000:
                node.decompose()

    for tag in soup.find_all(["a", "button", "span", "div", "p"]):
        text = tag.get_text(" ", strip=True).lower()
        if text in {
            "skip to content",
            "skip to main content",
            "cookie settings",
            "accept all cookies",
            "reject all cookies",
            "loading...",
            "copy page",
            "sign up",
            "open app",
        }:
            tag.decompose()


def _drop_markdown_chrome(markdown: str) -> str:
    """Drop residual markdown lines that are usually site-shell noise."""
    noise_tokens = (
        "skip to content",
        "skip to main content",
        "cookie settings",
        "accept all cookies",
        "reject all cookies",
        "loading...",
        "copy page",
    )
    cleaned: list[str] = []
    for line in markdown.splitlines():
        stripped = line.strip().lower()
        if stripped in noise_tokens:
            continue
        # Drop very long navigation lines composed of many markdown links.
        if line.count("](") >= 10 and len(line) > 180:
            continue
        cleaned.append(line)

    return _dedupe_adjacent_lines("\n".join(cleaned))


def _dedupe_adjacent_lines(markdown: str) -> str:
    out: list[str] = []
    prev = None
    for line in markdown.splitlines():
        if prev is not None and line.strip() and line.strip() == prev.strip():
            continue
        out.append(line)
        prev = line
    return "\n".join(out)
