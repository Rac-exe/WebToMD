"""AI layer — pluggable multi-provider system.

Usage:
    from webtomd.ai import process_ai
    result = process_ai(markdown, mode="summarize")
"""

from __future__ import annotations

from webtomd.ai.detector import detect, graceful_no_key_message
from webtomd.ai.prompts import build


class AIUnavailableError(Exception):
    """Raised when no AI provider is configured."""


def process_ai(
    markdown: str,
    mode: str,
    provider_override: str | None = None,
    **prompt_kwargs,
) -> str:
    """Apply an AI mode to converted markdown and return the result.

    Raises AIUnavailableError when no provider/key is found so the
    caller can decide whether to show a friendly message or just
    output the raw markdown.
    """
    provider = detect(provider_override=provider_override)
    if provider is None:
        raise AIUnavailableError(graceful_no_key_message())

    prompt = build(mode, content=markdown, **prompt_kwargs)

    try:
        return provider.complete(prompt)
    except ImportError as exc:
        raise AIUnavailableError(
            f"{provider.name} SDK not installed. "
            f"Install with: pip install webtomd[{provider.name.lower()}]"
        ) from exc


VALID_MODES = {"summarize", "tl;dr", "translate", "extract", "qa"}
