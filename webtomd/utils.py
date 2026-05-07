"""Shared utilities — URL validation, filename sanitisation, constants."""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import urlparse

SPARSE_THRESHOLD = 200  # characters — below this triggers fallback escalation


def is_valid_url(url: str) -> bool:
    """Return True if the string is a valid HTTP/HTTPS URL."""
    try:
        parsed = urlparse(url)
        return parsed.scheme in ("http", "https") and bool(parsed.netloc)
    except Exception:
        return False


def url_to_filename(url: str) -> str:
    """Convert a URL into a safe, readable filename without extension.

    Example:
        https://stripe.com/docs/api  →  stripe-com-docs-api
    """
    parsed = urlparse(url)
    raw = f"{parsed.netloc}{parsed.path}".strip("/")
    safe = re.sub(r"[^\w\-]", "-", raw)
    safe = re.sub(r"-{2,}", "-", safe).strip("-")
    return safe[:80] or "output"


def slugify(text: str, max_len: int = 80) -> str:
    """Convert arbitrary text into a filename-safe slug."""
    slug = text.strip().lower()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"-{2,}", "-", slug).strip("-")
    return (slug[:max_len] or "output").strip("-")


def host_slug(url: str) -> str:
    """Return a compact host token for context in generated filenames."""
    netloc = (urlparse(url).netloc or "").lower()
    netloc = re.sub(r"^www\.", "", netloc)
    primary = netloc.split(":")[0]
    return slugify(primary, max_len=40) or "site"


def unique_path(directory: Path, stem: str, suffix: str = ".md") -> Path:
    """Return a non-colliding path by appending -2, -3, ... when needed."""
    directory.mkdir(parents=True, exist_ok=True)
    candidate = directory / f"{stem}{suffix}"
    if not candidate.exists():
        return candidate

    idx = 2
    while True:
        candidate = directory / f"{stem}-{idx}{suffix}"
        if not candidate.exists():
            return candidate
        idx += 1


def build_output_path(directory: Path, url: str, title_hint: str | None = None) -> Path:
    """Build a deterministic, collision-safe output path for a URL."""
    host = host_slug(url)
    base = slugify(title_hint or "", max_len=60) if title_hint else ""
    if not base:
        base = url_to_filename(url)

    if host not in base:
        stem = f"{base}-{host}"
    else:
        stem = base

    return unique_path(directory=directory, stem=stem, suffix=".md")


def is_sparse(content: str | None) -> bool:
    """Return True if extracted content is too thin to be useful."""
    if not content:
        return True
    return len(content.strip()) < SPARSE_THRESHOLD
