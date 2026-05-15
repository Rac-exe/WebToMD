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

    source_html = _fix_code_blocks(source_html)
    source_html = _fix_tables(source_html)

    markdown = md(
        source_html,
        heading_style="ATX",
        bullets="-",
        strip=["script", "style"],
        code_language_callback=_detect_code_lang,
    )
    markdown = _normalize_numbering(markdown)
    markdown = _drop_css_noise(markdown)
    markdown = _drop_markdown_chrome(markdown)
    markdown = _clean_image_refs(markdown)
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


def _fix_code_blocks(html: str) -> str:
    """Normalize <pre>/<code> blocks so markdownify emits fenced code blocks.

    - Strips line-number <span>s that some syntax highlighters inject
    - Ensures <pre> wraps a single <code> for reliable fencing
    - Preserves language class on the <code> element
    """
    soup = BeautifulSoup(html, "html.parser")
    changed = False

    for pre in soup.find_all("pre"):
        code = pre.find("code")
        if not code:
            raw_text = pre.get_text("\n")
            if len(raw_text.strip()) > 10:
                new_code = soup.new_tag("code")
                new_code.string = raw_text
                pre.clear()
                pre.append(new_code)
                changed = True
            continue

        for line_num_el in code.find_all(
            lambda tag: tag.get("class") and any(
                "line-number" in c or "linenumber" in c or "hljs-ln-n" in c
                for c in tag.get("class", [])
            )
        ):
            line_num_el.decompose()
            changed = True

    return str(soup) if changed else html


def _clean_image_refs(markdown: str) -> str:
    """Clean up broken or data-uri image references."""
    markdown = re.sub(r"!\[[^\]]*\]\(data:image/[^)]+\)", "", markdown)
    markdown = re.sub(r"!\[\]\((?:about:blank|javascript:[^)]*)\)", "", markdown)
    return markdown


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


def _detect_code_lang(el) -> str | None:
    """Try to detect programming language from a <pre>/<code> element's class."""
    classes = el.get("class", []) if hasattr(el, "get") else []
    for cls in classes:
        if isinstance(cls, str):
            m = re.match(r"(?:language|lang|highlight)-(\w+)", cls)
            if m:
                return m.group(1)
    parent = el.parent if hasattr(el, "parent") else None
    if parent:
        parent_classes = parent.get("class", []) if hasattr(parent, "get") else []
        for cls in parent_classes:
            if isinstance(cls, str):
                m = re.match(r"(?:language|lang|highlight)-(\w+)", cls)
                if m:
                    return m.group(1)
    return None


def _drop_css_noise(markdown: str) -> str:
    """Drop common CSS blobs that can leak through raw HTML conversion."""
    cleaned: list[str] = []
    in_code_block = False
    for line in markdown.splitlines():
        stripped = line.strip()

        if stripped.startswith("```"):
            in_code_block = not in_code_block
            cleaned.append(line)
            continue

        if in_code_block:
            cleaned.append(line)
            continue

        if not stripped:
            cleaned.append(line)
            continue

        if stripped.startswith("@import url("):
            continue

        if stripped.startswith("@keyframes "):
            continue

        if (
            "{" in stripped and "}" in stripped
            and ":" in stripped
            and not any(c.isalpha() and c.isupper() for c in stripped[:20])
            and stripped.count(";") >= 2
        ):
            continue

        cleaned.append(line)

    return "\n".join(cleaned)


def _prune_structural_noise(soup: BeautifulSoup) -> None:
    """Drop obvious chrome/sidebar/cookie shells before conversion."""
    has_primary_content = bool(soup.find(["main", "article"]))
    doc_text_len = len(soup.get_text(" ", strip=True))

    # When main/article exists, scope conversion to just that region
    if has_primary_content:
        primary = soup.find("main") or soup.find("article")
        if primary and len(primary.get_text(" ", strip=True)) > max(doc_text_len * 0.25, 200):
            _prune_within_primary(soup, primary, doc_text_len)
            return

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
            if _should_prune_node(
                node, has_primary_content=has_primary_content, doc_text_len=doc_text_len,
            ):
                node.decompose()

    _remove_boilerplate_text(soup)


def _prune_within_primary(soup: BeautifulSoup, primary, doc_text_len: int) -> None:
    """When a <main>/<article> exists, remove everything outside it plus noise inside."""
    body = soup.find("body")
    if body:
        for child in list(body.children):
            if not hasattr(child, "name") or not child.name:
                continue
            if child is primary:
                continue
            try:
                if primary in child.descendants:
                    continue
            except Exception:
                continue
            child.decompose()

    noise_inside = [
        "footer", "aside", "[role='navigation']",
        "[class*='sidebar' i]", "[class*='breadcrumbs' i]",
        "[id*='cookie' i]", "[class*='cookie' i]",
        "[id*='consent' i]", "[class*='consent' i]",
    ]
    for sel in noise_inside:
        for node in primary.select(sel):
            text_len = len(node.get_text(" ", strip=True))
            if text_len < 400:
                node.decompose()

    _remove_boilerplate_text(soup)


def _remove_boilerplate_text(soup: BeautifulSoup) -> None:
    """Remove small boilerplate text elements."""
    exact_kill = {
        "skip to content",
        "skip to main content",
        "cookie settings",
        "accept all cookies",
        "reject all cookies",
        "loading...",
        "copy page",
        "sign up",
        "open app",
        "privacy policy",
        "cookie policy",
        "terms of service",
        "terms of use",
        "terms and conditions",
        "do not share or sell my info",
        "manage cookies",
        "cookie preferences",
        "accept cookies",
        "reject cookies",
        "accessibility help",
        "accessibility statement",
    }
    for tag in soup.find_all(["a", "button", "span", "div", "p"]):
        text = tag.get_text(" ", strip=True).lower()
        if text in exact_kill and len(text) <= 40:
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
        "privacy policy",
        "cookie policy",
        "terms of service",
        "terms of use",
        "manage cookies",
        "cookie preferences",
        "accessibility help",
        "accessibility statement",
    )
    cleaned: list[str] = []
    link_wall_streak = 0
    noise_link_re = re.compile(
        r"^\s*-?\s*\[(" + "|".join(re.escape(t) for t in noise_tokens) + r")\]\([^)]*\)\s*$",
        re.IGNORECASE,
    )
    footer_link_patterns = re.compile(
        r"^\s*-?\s*\[(cookies?|do not share[^]]*|terms[^]]*|privacy[^]]*)\]\([^)]*\)\s*$",
        re.IGNORECASE,
    )

    for line in markdown.splitlines():
        stripped = line.strip().lower()
        if stripped in noise_tokens:
            continue
        if noise_link_re.match(line):
            continue
        if footer_link_patterns.match(line):
            continue

        link_count = line.count("](")
        is_link_wall = link_count >= 6 and len(line.strip()) > 120
        if is_link_wall:
            link_wall_streak += 1
        else:
            link_wall_streak = 0

        if is_link_wall and link_wall_streak >= 2:
            continue

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
