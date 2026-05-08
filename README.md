# webtomd

> Web to Markdown. No garbage.

Convert any URL into clean, structured Markdown. In seconds, from your terminal.

```bash
pip install webtomd
webtomd https://example.com/article
```

That's it. Clean `.md` file, saved to your current directory.

## Who is this for?

- **Developers** building RAG pipelines, training datasets, or knowledge bases from web content
- **Technical writers** pulling reference material from docs, wikis, and blogs into Markdown
- **Researchers** archiving web articles in a portable, version-controllable format
- **AI engineers** feeding clean web content into LLM prompts without HTML noise
- **Anyone** who's ever done "view source, copy, clean up for 20 minutes" and wished there was a better way

## Why webtomd?

Most web-to-markdown tools give you a wall of nav links, cookie banners, and broken formatting. webtomd doesn't.

- **Actually clean output** ➜ not just converted HTML, but intelligently extracted content with navs, sidebars, and ads stripped out
- **Works on real websites** ➜ handles JS-rendered SPAs, paywalled layouts, complex tables, and nested lists
- **One command, zero config** ➜ no browser extensions, no copy-paste, no manual cleanup
- **Plugs into your workflow** ➜ pipes, batch files, stdin, clipboard, AI post-processing, all from the terminal
- **Your AI provider, your choice** ➜ works with OpenAI, Anthropic, Gemini, Groq, or local Ollama

Works on **Windows**, **macOS**, and **Linux**. Python 3.11+.

## Install

### pip (all platforms)

```bash
pip install webtomd
```

### uv (recommended, faster)

```bash
uv pip install webtomd
```

### pipx (isolated global install)

```bash
pipx install webtomd
```

### Optional extras

```bash
# AI provider support
pip install "webtomd[openai]"
pip install "webtomd[anthropic]"
pip install "webtomd[gemini]"
pip install "webtomd[groq]"
pip install "webtomd[ai-all]"

# JS-rendered page support (SPAs, React/Vue/Next.js sites)
pip install "webtomd[playwright]"
playwright install chromium
```

### Verify installation

```bash
webtomd --help
```

If `webtomd` isn't found in your PATH, you can always run it as a module:

```bash
python -m webtomd --help
```

## Features

- **Smart extraction**: trafilatura + readability fallback chain with quality scoring
- **JS-rendered pages**: optional Playwright fallback for SPAs
- **AI modes**: summarize, translate, extract, Q&A via Anthropic / OpenAI / Gemini / Groq / Ollama
- **Batch processing**: convert a file of URLs in one command with progress bar
- **CSS selectors**: target specific page sections
- **YAML frontmatter**: title, URL, date metadata
- **Auto-save**: interactive terminals save files; piped runs output to stdout
- **Smart filenames**: deterministic or AI-assisted naming
- **Clipboard**: copy output with `--copy`
- **stdin support**: pipe HTML directly
- **Recursive crawl**: `--depth N` discovers and converts same-domain linked pages
- **Clean output**: strips nav, sidebars, cookie banners, CSS noise, duplicate content
- **Cross-platform**: Windows, macOS, Linux with encoding-safe output

## Usage

### Basic conversion

```bash
# Auto-saves .md file in interactive terminals
webtomd https://example.com/article

# Save to a specific file
webtomd https://example.com/article -o article.md

# Force output to terminal
webtomd https://example.com/article --stdout
```

### Selectors and metadata

```bash
# Extract only content inside a CSS selector
webtomd https://example.com --selector "main"
webtomd https://example.com --selector "article .content"

# Add YAML frontmatter (title, url, date)
webtomd https://example.com --metadata
```

### AI post-processing

```bash
webtomd https://example.com --ai summarize
webtomd https://example.com --ai "tl;dr"
webtomd https://example.com --ai translate
webtomd https://example.com --ai extract
webtomd https://example.com --ai qa
```

### Batch and crawl

```bash
# Batch: convert a list of URLs
webtomd --batch urls.txt

# Crawl: recursively discover and convert same-domain links
webtomd https://example.com --depth 2
```

### Stdin (pipe HTML directly)

**macOS / Linux:**

```bash
curl -s https://example.com | webtomd - --stdout
curl -s https://example.com | webtomd --stdout
```

**Windows (PowerShell):**

```powershell
(Invoke-WebRequest https://example.com).Content | python -m webtomd - --stdout
```

### Other options

```bash
# Copy result to clipboard
webtomd https://example.com --copy

# Open in default editor after saving
webtomd https://example.com --open

# Silent mode (no spinners, no preview, pipe-safe)
webtomd https://example.com --silent -o out.md

# Filename strategy
webtomd https://example.com --name-strategy deterministic
webtomd https://example.com --name-strategy ai
```

## AI Setup

Set your provider's API key as an environment variable.

**macOS / Linux (bash/zsh):**

```bash
export OPENAI_API_KEY=sk-...
export ANTHROPIC_API_KEY=sk-ant-...
export GEMINI_API_KEY=...
export GROQ_API_KEY=gsk_...
export OLLAMA_HOST=http://localhost:11434
```

**Windows (PowerShell):**

```powershell
$env:OPENAI_API_KEY = "sk-..."
$env:ANTHROPIC_API_KEY = "sk-ant-..."
$env:GEMINI_API_KEY = "..."
$env:GROQ_API_KEY = "gsk_..."
$env:OLLAMA_HOST = "http://localhost:11434"
```

**Windows (Command Prompt):**

```cmd
set OPENAI_API_KEY=sk-...
set ANTHROPIC_API_KEY=sk-ant-...
```

To persist across sessions, add these to your shell profile (`~/.bashrc`, `~/.zshrc`) or set them via Windows System Environment Variables.

Or use the interactive setup wizard (writes to `~/.webtomdrc`):

```bash
webtomd --configure
```

The first available key is auto-detected in priority order: Anthropic > OpenAI > Gemini > Groq > Ollama.

If no key is configured, `--ai` modes gracefully fall back to plain Markdown output with a friendly message. Nothing breaks.

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

**Location:** `~/.webtomdrc` resolves to:
- macOS/Linux: `/home/yourname/.webtomdrc`
- Windows: `C:\Users\YourName\.webtomdrc`

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

Each URL is processed independently with a live progress bar. Failures don't abort the batch. A summary is printed at the end.

## Output Defaults

| Context | Behavior |
|---|---|
| Interactive terminal | Auto-saves `.md` file with generated name |
| Piped / non-interactive | Prints Markdown to stdout |
| `-o file.md` | Saves to the specified file |
| `--stdout` | Forces stdout in any context |

## Troubleshooting

**`webtomd` command not found:**
- Ensure your Python `Scripts` (Windows) or `bin` (macOS/Linux) directory is in your PATH
- Alternative: `python -m webtomd`

**Encoding errors on Windows:**
- webtomd handles UTF-8 output automatically, but if your terminal shows garbled characters, run `chcp 65001` first or use Windows Terminal (recommended over cmd.exe)

**Playwright not installing:**
- Run `playwright install chromium` after installing the playwright extra
- On Linux, you may need system deps: `playwright install-deps chromium`

**Clipboard not working:**
- macOS: works out of the box (`pbcopy`)
- Linux: install `xclip` or `xsel` (`sudo apt install xclip`)
- Windows: works out of the box

**Slow conversion on certain sites:**
- Some sites throttle or block automated requests. This is network-bound, not a tool issue
- Try `--selector "main"` to skip heavy page processing

## Contributing

```bash
git clone https://github.com/MrRaccooon/WebToMD.git
cd WebToMD
```

**Setup (all platforms):**

```bash
pip install uv         # if you don't have uv
uv sync --extra dev
uv run pytest
```

**Run lints:**

```bash
uv run ruff check .
```

**Run type checks:**

```bash
uv run mypy webtomd/
```

## License

GPL-3.0-or-later
