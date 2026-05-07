"""Optional AI-assisted filename strategy.

Phase 1.5 scaffold:
- activates only when an AI provider env key is present
- returns an improved title slug heuristic
- never blocks conversion; caller falls back to deterministic naming
"""

from __future__ import annotations

import os
import re

from webtomd.utils import slugify

_PROVIDER_KEYS: list[tuple[str, str]] = [
    ("ANTHROPIC_API_KEY", "anthropic"),
    ("OPENAI_API_KEY", "openai"),
    ("GEMINI_API_KEY", "gemini"),
    ("GROQ_API_KEY", "groq"),
    ("OLLAMA_HOST", "ollama"),
]


def available_provider() -> str | None:
    """Return provider name when any supported AI environment key is set."""
    for key, provider in _PROVIDER_KEYS:
        if os.getenv(key):
            return provider
    return None


def suggest_filename_ai(title_hint: str | None, markdown: str) -> str:
    """Return an AI-style concise filename stem from extracted content.

    This function intentionally avoids network calls in Phase 1.5 and uses
    content heuristics once provider availability is confirmed.
    """
    provider = available_provider()
    if not provider:
        raise RuntimeError("No AI provider configured in environment.")

    text = (title_hint or "").strip()
    if not text:
        for line in markdown.splitlines():
            s = line.strip()
            if s.startswith("# "):
                text = s[2:].strip()
                break

    if not text:
        raise RuntimeError("Unable to derive a filename candidate from content.")

    text = re.sub(r"\s+", " ", text)
    words = [w for w in text.split(" ") if w]
    concise = " ".join(words[:8])
    stem = slugify(concise, max_len=60)
    if not stem:
        raise RuntimeError("Derived AI filename stem was empty.")
    return stem
