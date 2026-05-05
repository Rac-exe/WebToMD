"""Concrete AI provider implementations.

Each provider is only imported if its SDK is installed.
Missing SDK → ImportError caught gracefully in detector.py.
"""

from __future__ import annotations

from webtomd.ai.base import AIProvider


class AnthropicProvider(AIProvider):
    name = "Anthropic"
    default_model = "claude-sonnet-4-5"

    def complete(self, prompt: str, max_tokens: int = 2048) -> str:
        # Phase 3: implemented
        raise NotImplementedError


class OpenAIProvider(AIProvider):
    name = "OpenAI"
    default_model = "gpt-4o-mini"

    def complete(self, prompt: str, max_tokens: int = 2048) -> str:
        # Phase 3: implemented
        raise NotImplementedError


class GeminiProvider(AIProvider):
    name = "Google Gemini"
    default_model = "gemini-2.0-flash"

    def complete(self, prompt: str, max_tokens: int = 2048) -> str:
        # Phase 3: implemented
        raise NotImplementedError


class GroqProvider(AIProvider):
    name = "Groq"
    default_model = "llama-3.3-70b-versatile"

    def complete(self, prompt: str, max_tokens: int = 2048) -> str:
        # Phase 3: implemented
        raise NotImplementedError


class OllamaProvider(AIProvider):
    name = "Ollama"
    default_model = "llama3.2"

    def complete(self, prompt: str, max_tokens: int = 2048) -> str:
        # Phase 3: implemented
        raise NotImplementedError
