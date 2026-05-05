"""Conversion layer — HTML to clean Markdown via markdownify."""

from __future__ import annotations

import re
from datetime import date

from bs4 import BeautifulSoup
from markdownify import markdownify as md


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
    title = "Untitled"

    if selector:
        soup = BeautifulSoup(source_html, "html.parser")
        selected = soup.select_one(selector)
        if selected is not None:
            source_html = str(selected)
            heading = selected.find(["h1", "h2", "h3"])
            if heading and heading.get_text(strip=True):
                title = heading.get_text(strip=True)
        elif soup.title and soup.title.get_text(strip=True):
            title = soup.title.get_text(strip=True)
    else:
        soup = BeautifulSoup(source_html, "html.parser")
        if soup.title and soup.title.get_text(strip=True):
            title = soup.title.get_text(strip=True)
        else:
            h1 = soup.find("h1")
            if h1 and h1.get_text(strip=True):
                title = h1.get_text(strip=True)

    markdown = md(
        source_html,
        heading_style="ATX",
        bullets="-",
        strip=["script", "style", "nav", "footer"],
    )
    markdown = _normalize_numbering(markdown)
    markdown = _drop_css_noise(markdown)
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
    plain_re = re.compile(r"^(\s*)(\d+)([A-Za-z].*)$")

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
