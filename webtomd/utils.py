"""Shared utilities — URL validation, filename sanitisation, constants."""

from __future__ import annotations

import re
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


def is_sparse(content: str | None) -> bool:
    """Return True if extracted content is too thin to be useful."""
    if not content:
        return True
    return len(content.strip()) < SPARSE_THRESHOLD
