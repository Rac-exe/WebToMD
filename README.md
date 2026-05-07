# webtomd

> Web to Markdown. No garbage.

A fast, terminal-native CLI that converts any URL into clean, structured Markdown. Supports multi-provider AI post-processing, batch conversion, CSS selectors, and YAML frontmatter — all from one command.

Works on **Windows**, **macOS**, and **Linux**.

```bash
pip install webtomd
```

## Features

- **Smart extraction** — trafilatura + readability fallback chain with quality scoring
- **JS-rendered pages** — optional Playwright fallback for SPAs
- **AI modes** — summarize, translate, extract, Q&A via Anthropic / OpenAI / Gemini / Groq / Ollama
- **Batch processing** — convert a file of URLs in one command
- **CSS selectors** — target specific page sections
- **YAML frontmatter** — title, URL, date metadata
- **Auto-save** — interactive terminals save files; piped runs output to stdout
- **Smart filenames** — deterministic or AI-assisted naming
- **Clipboard** — copy output with `--copy`
- **Clean output** — strips nav, sidebars, cookie banners, CSS noise, duplicate content
- **Cross-platform** — Windows, macOS, Linux with encoding-safe output

## Usage

```bash
# Convert a URL (auto-saves .md file in interactive terminals)
webtomd https://example.com/article

# Save to a specific file
webtomd https://example.com/article -o article.md

# Force stdout (useful for pipelines)
webtomd https://example.com/article --stdout

# Pipe-friendly (auto-detects non-interactive terminal)
webtomd https://example.com/article | grep "##"

# Target specific content with CSS selector
webtomd https://example.com --selector "main"

# Add YAML frontmatter
webtomd https://example.com --metadata

# AI summarization (requires API key)
webtomd https://example.com --ai summarize

# Other AI modes
webtomd https://example.com --ai "tl;dr"
webtomd https://example.com --ai translate
webtomd https://example.com --ai extract
webtomd https://example.com --ai qa

# Batch convert from a URL list
webtomd --batch urls.txt

# Copy result to clipboard
webtomd https://example.com --copy

# Open in default editor after saving
webtomd https://example.com --open

# Silent mode (no spinners, no preview — pipe-safe)
webtomd https://example.com --silent -o out.md

# Filename strategy
webtomd https://example.com --name-strategy deterministic
webtomd https://example.com --name-strategy ai
```

## Install

```bash
# Core (no AI)
pip install webtomd

# With a specific AI provider
pip install "webtomd[openai]"
pip install "webtomd[anthropic]"
pip install "webtomd[gemini]"
pip install "webtomd[groq]"

# All AI providers
pip install "webtomd[ai-all]"

# JS-rendered page support
pip install "webtomd[playwright]"
playwright install chromium
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv pip install webtomd
```

**Requires Python 3.11+.**

## AI Setup

Set an environment variable for your provider:

```bash
export OPENAI_API_KEY=sk-...
export ANTHROPIC_API_KEY=sk-ant-...
export GEMINI_API_KEY=...
export GROQ_API_KEY=gsk_...
export OLLAMA_HOST=http://localhost:11434
```

Or use the interactive setup wizard:

```bash
webtomd --configure
```

The first available key is auto-detected in priority order: Anthropic > OpenAI > Gemini > Groq > Ollama.

If no key is configured, `--ai` modes gracefully fall back to plain Markdown output with a friendly message.

## Configuration

Create `~/.webtomdrc` (TOML format) for persistent defaults:

```toml
output_dir = "~/Documents/webtomd"
copy = false
metadata = false
silent = false
name_strategy = "deterministic"
ai_provider = "openai"
```

CLI flags always override config file values.

## Batch Mode

Create a text file with one URL per line (`#` comments supported):

```text
# My reading list
https://example.com/article-1
https://example.com/article-2
https://example.com/article-3
```

```bash
webtomd --batch urls.txt
```

Each URL is processed independently — failures don't abort the batch. A summary is printed at the end.

## Output Defaults

| Context | Behavior |
|---|---|
| Interactive terminal | Auto-saves `.md` file with generated name |
| Piped / non-interactive | Prints Markdown to stdout |
| `-o file.md` | Saves to the specified file |
| `--stdout` | Forces stdout in any context |

## Contributing

```bash
git clone https://github.com/prabhat/webtomd.git
cd webtomd
uv sync --extra dev
uv run pytest
```

Lint with `ruff check .`, type-check with `mypy webtomd/`.

## License

GPL-3.0-or-later
