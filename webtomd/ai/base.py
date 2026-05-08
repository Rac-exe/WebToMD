"""Abstract base class for all AI providers."""

from __future__ import annotations

from abc import ABC, abstractmethod


class AIProvider(ABC):
    """Base interface every provider must implement."""

    @abstractmethod
    def complete(self, prompt: str, max_tokens: int = 2048) -> str:
        """Send a prompt and return the completion text."""
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable provider name (e.g. 'OpenAI')."""
        ...

    @property
    @abstractmethod
    def default_model(self) -> str:
        """Default model slug for this provider."""
        ...
