"""Provider auto-detection — reads env vars and returns the right provider.

Priority order:
1. ANTHROPIC_API_KEY  → AnthropicProvider
2. OPENAI_API_KEY     → OpenAIProvider
3. GEMINI_API_KEY     → GeminiProvider
4. GROQ_API_KEY       → GroqProvider
5. OLLAMA_HOST        → OllamaProvider
6. None               → graceful degradation
"""

from __future__ import annotations

import os

from webtomd.ai.base import AIProvider


def detect() -> AIProvider | None:
    """Return the first available provider based on env vars.

    Returns None if no provider is configured — caller handles
    graceful degradation messaging.
    """
    # Phase 3: implemented
    raise NotImplementedError


def graceful_no_key_message() -> str:
    """Return the friendly message shown when no AI key is configured."""
    return (
        "\n  [yellow]✗ AI mode unavailable — no API key configured.[/]\n\n"
        "  To enable --ai features, run:\n\n"
        "    [green]webtomd --configure[/]          ← guided setup\n"
        "    [dim]export OPENAI_API_KEY=...[/]    ← environment variable\n\n"
        "  → Outputting clean Markdown instead.\n"
    )
