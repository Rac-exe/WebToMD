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
    "ui-rationale": (
        "You are a senior product designer and design systems expert. "
        "Below is a raw design style guide extracted from a live website. "
        "Your job is to:\n\n"
        "1. Add a 'Design Rationale' section after the Design Philosophy that explains "
        "the likely reasoning behind the color choices, typography hierarchy, and spacing system. "
        "Discuss what mood or brand personality the palette conveys.\n\n"
        "2. For each color in the palette, add a brief description of its probable role "
        "(e.g. 'Primary CTA background', 'Disabled state text', 'Hover surface').\n\n"
        "3. Add a 'Recommendations' section at the end suggesting:\n"
        "   - Accessibility improvements (contrast ratios that may fail WCAG AA)\n"
        "   - Missing states (hover, focus, active, disabled) to define\n"
        "   - Typography adjustments for better visual hierarchy\n"
        "   - Any inconsistencies in the spacing scale\n\n"
        "4. If the design uses a dark theme, suggest complementary light theme values.\n"
        "   If it uses a light theme, suggest dark mode counterparts.\n\n"
        "Keep the original style guide intact — only ADD new sections and inline annotations. "
        "Use Markdown formatting. Be specific with CSS values, not vague.\n\n"
        "---\n\n{content}"
    ),
}


def build(mode: str, content: str, **kwargs) -> str:
    """Build a prompt string for the given mode."""
    if mode not in PROMPTS:
        raise ValueError(f"Unknown AI mode: {mode!r}. Choose from: {list(PROMPTS)}")
    return PROMPTS[mode].format(content=content, **kwargs)
