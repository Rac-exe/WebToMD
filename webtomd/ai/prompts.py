"""Prompt templates for all --ai modes."""

from __future__ import annotations

PROMPTS: dict[str, str] = {
    "summarize": (
        "Summarize the following article in 3-5 clear, concise paragraphs. "
        "Focus on the key ideas and findings:\n\n{content}"
    ),
    "tl;dr": (
        "Give a 3-bullet TL;DR of the following content. "
        "Each bullet should be one sentence:\n\n{content}"
    ),
    "translate": (
        "Translate the following content to {lang}. "
        "Preserve all Markdown formatting:\n\n{content}"
    ),
    "extract": (
        "Extract all {target} from the following content. "
        "Format as a clean Markdown list:\n\n{content}"
    ),
    "qa": (
        "You are a helpful assistant. The user will ask questions about "
        "the following document. Answer concisely and accurately.\n\n"
        "Document:\n{content}\n\nQuestion: {question}"
    ),
}


def build(mode: str, content: str, **kwargs) -> str:
    """Build a prompt string for the given mode."""
    if mode not in PROMPTS:
        raise ValueError(f"Unknown AI mode: {mode!r}. Choose from: {list(PROMPTS)}")
    return PROMPTS[mode].format(content=content, **kwargs)
