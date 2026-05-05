"""Tests for AI provider detection and prompt building."""

import pytest


def test_prompt_build_summarize():
    from webtomd.ai.prompts import build
    prompt = build("summarize", content="Hello world")
    assert "Hello world" in prompt


def test_prompt_build_unknown_mode():
    from webtomd.ai.prompts import build
    with pytest.raises(ValueError):
        build("nonexistent", content="test")


def test_prompt_build_translate():
    from webtomd.ai.prompts import build
    prompt = build("translate", content="Hello", lang="Spanish")
    assert "Spanish" in prompt
