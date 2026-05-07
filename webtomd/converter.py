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

    source_html = _fix_tables(source_html)

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


def _fix_tables(html: str) -> str:
    """Normalize HTML tables so markdownify emits proper pipe-tables.

    - Ensures <thead>/<tbody> structure exists
    - Strips block-level tags from cells (collapses to inline text)
    - Converts layout tables (no <th>, used for visual layout) to plain <div> text
    """
    soup = BeautifulSoup(html, "html.parser")
    changed = False

    for table in soup.find_all("table"):
        headers = table.find_all("th")
        rows = table.find_all("tr")

        if not rows:
            continue

        if not headers:
            cell_counts = [len(row.find_all(["td", "th"])) for row in rows]
            all_single_col = all(c <= 1 for c in cell_counts)
            if all_single_col or len(rows) <= 1:
                replacement = soup.new_tag("div")
                for row in rows:
                    for cell in row.find_all(["td", "th"]):
                        p = soup.new_tag("p")
                        p.string = cell.get_text(" ", strip=True)
                        replacement.append(p)
                table.replace_with(replacement)
                changed = True
                continue

            first_row = rows[0]
            first_cells = first_row.find_all("td")
            if first_cells:
                thead = soup.new_tag("thead")
                new_tr = soup.new_tag("tr")
                for td in first_cells:
                    th = soup.new_tag("th")
                    th.string = td.get_text(" ", strip=True)
                    new_tr.append(th)
                thead.append(new_tr)
                first_row.decompose()
                table.insert(0, thead)
                changed = True

        if not table.find("thead"):
            thead_tag = soup.new_tag("thead")
            first_header_row = table.find("tr")
            if first_header_row and first_header_row.find("th"):
                first_header_row.wrap(thead_tag)
                changed = True

        if not table.find("tbody"):
            data_rows = [
                tr for tr in table.find_all("tr", recursive=False)
                if tr.parent.name != "thead"
            ]
            if data_rows:
                tbody = soup.new_tag("tbody")
                for dr in data_rows:
                    tbody.append(dr.extract())
                table.append(tbody)
                changed = True

        for cell in table.find_all(["td", "th"]):
            block_children = cell.find_all(["p", "div", "ul", "ol", "br"])
            if block_children:
                cell.string = cell.get_text(" ", strip=True)
                changed = True

    return str(soup) if changed else html


def _normalize_numbering(markdown: str) -> str:
    """Fix common markdownify/trafilatura numbering glitches.

    Examples:
    - "## 1Getting Started" -> "## 1. Getting Started"
    - "- 1Open app" -> "- 1. Open app"
    - "1Install" -> "1. Install"
    """
    markdown = re.sub(r"(^|\s)(\d+)\.\s+(st|nd|rd|th)-", r"\1\2\3-", markdown, flags=re.IGNORECASE)
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
    doc_text_len = len(soup.get_text(" ", strip=True))
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
            if _should_prune_node(node, has_primary_content=has_primary_content, doc_text_len=doc_text_len):
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
        } and len(text) <= 20:
            tag.decompose()


def _should_prune_node(node, has_primary_content: bool, doc_text_len: int) -> bool:
    """Conservative pruning guardrails to avoid deleting real content sections."""
    text_len = len(node.get_text(" ", strip=True))
    if text_len == 0:
        return True

    # Never remove a container that wraps a canonical content region.
    if node.find(["main", "article", "section"]):
        return False

    heading_count = len(node.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]))
    para_count = len(node.find_all("p"))
    link_count = len(node.find_all("a"))

    if heading_count >= 3 or para_count >= 8:
        return False

    # When page has no explicit main/article, be extra conservative.
    if not has_primary_content:
        if text_len > 600:
            return False
        return link_count >= 4

    # Keep nodes that occupy substantial share of document content.
    if doc_text_len > 0 and text_len >= max(int(doc_text_len * 0.35), 2500):
        return False

    # Drop mostly-link containers (typical nav/sidebar shells).
    if link_count >= 5 and para_count <= 2 and heading_count <= 1:
        return True

    # Otherwise only prune clearly short utility blocks.
    return text_len < 350


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
    link_wall_streak = 0
    for line in markdown.splitlines():
        stripped = line.strip().lower()
        if stripped in noise_tokens:
            continue

        link_count = line.count("](")
        is_link_wall = link_count >= 6 and len(line.strip()) > 120
        if is_link_wall:
            link_wall_streak += 1
        else:
            link_wall_streak = 0

        # Keep at most one line from long runs of link walls.
        if is_link_wall and link_wall_streak >= 2:
            continue

        # Drop isolated huge navigation rows composed almost entirely of links.
        if link_count >= 10 and len(line) > 180:
            continue

        cleaned.append(line)

    reduced = _collapse_duplicate_lines("\n".join(cleaned))
    return _dedupe_adjacent_lines(reduced)


def _dedupe_adjacent_lines(markdown: str) -> str:
    out: list[str] = []
    prev = None
    for line in markdown.splitlines():
        if prev is not None and line.strip() and line.strip() == prev.strip():
            continue
        out.append(line)
        prev = line
    return "\n".join(out)


def _collapse_duplicate_lines(markdown: str) -> str:
    """Remove repeated lines that recur in short proximity."""
    lines = markdown.splitlines()
    recent: list[str] = []
    out: list[str] = []
    for line in lines:
        key = line.strip()
        if key and key in recent:
            continue
        out.append(line)
        if key:
            recent.append(key)
            if len(recent) > 6:
                recent.pop(0)
    return "\n".join(out)
