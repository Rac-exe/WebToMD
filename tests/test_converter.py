"""Tests for HTML → Markdown conversion."""

from pathlib import Path

from webtomd.converter import to_markdown


def _fixture_html() -> str:
    fixture = Path(__file__).parent / "fixtures" / "sample_static.html"
    return fixture.read_text(encoding="utf-8")


def test_to_markdown_preserves_headings() -> None:
    markdown = to_markdown(_fixture_html())
    assert "# Sample Article Title" in markdown
    assert "## Section One" in markdown


def test_to_markdown_preserves_code_blocks() -> None:
    markdown = to_markdown(_fixture_html())
    assert "def hello():" in markdown
    assert 'print("Hello, world!")' in markdown
