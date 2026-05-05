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
    source_html = html
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
