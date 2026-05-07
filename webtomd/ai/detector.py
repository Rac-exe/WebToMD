"""Provider auto-detection — reads env vars and returns the right provider."""

from __future__ import annotations

import os

from webtomd.ai.base import AIProvider

PROVIDER_ENV_MAP: list[tuple[str, str]] = [
    ("ANTHROPIC_API_KEY", "anthropic"),
    ("OPENAI_API_KEY", "openai"),
    ("GEMINI_API_KEY", "gemini"),
    ("GROQ_API_KEY", "groq"),
    ("OLLAMA_HOST", "ollama"),
]


def detect(provider_override: str | None = None) -> AIProvider | None:
    """Return the first available provider based on env vars.

    If *provider_override* is given (from config or CLI), try that one first.
    Returns None if no provider is configured.
    """
    if provider_override:
        return _make_provider(provider_override)

    for env_key, slug in PROVIDER_ENV_MAP:
        if os.getenv(env_key):
            return _make_provider(slug)
    return None


def _make_provider(slug: str) -> AIProvider | None:
    from webtomd.ai.providers import (
        AnthropicProvider,
        GeminiProvider,
        GroqProvider,
        OllamaProvider,
        OpenAIProvider,
    )

    registry: dict[str, type[AIProvider]] = {
        "anthropic": AnthropicProvider,
        "openai": OpenAIProvider,
        "gemini": GeminiProvider,
        "groq": GroqProvider,
        "ollama": OllamaProvider,
    }
    cls = registry.get(slug)
    if cls is None:
        return None
    return cls()


def graceful_no_key_message() -> str:
    """Friendly message shown when no AI key is configured."""
    return (
        "\n  AI mode unavailable — no API key configured.\n\n"
        "  To enable --ai features, run:\n\n"
        "    webtomd --configure          <- guided setup\n"
        "    export OPENAI_API_KEY=...    <- environment variable\n\n"
        "  Outputting clean Markdown instead.\n"
    )
