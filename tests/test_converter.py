"""Tests for HTML → Markdown conversion."""

from pathlib import Path

from webtomd.converter import _drop_css_noise, _normalize_numbering, _sanitize_html, to_markdown


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


def test_normalize_numbering_fixes_heading_and_list_tokens() -> None:
    raw = "## 1Getting Started\n- 2Open app\n3Install"
    fixed = _normalize_numbering(raw)
    assert "## 1. Getting Started" in fixed
    assert "- 2. Open app" in fixed
    assert "3. Install" in fixed


def test_sanitize_html_removes_script_and_style() -> None:
    html = "<style>.x{color:red}</style><script>var x=1</script><p>Hello</p>"
    sanitized = _sanitize_html(html)
    assert "<style" not in sanitized
    assert "<script" not in sanitized
    assert "Hello" in sanitized


def test_drop_css_noise_filters_css_lines() -> None:
    raw = "@import url('x');\n.hero { color: red; }\nNormal line"
    cleaned = _drop_css_noise(raw)
    assert "@import" not in cleaned
    assert "color: red" not in cleaned
    assert "Normal line" in cleaned
