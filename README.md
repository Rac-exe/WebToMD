# webtomd

> Web to Markdown. No garbage.

A terminal-native CLI that converts any URL into clean, structured Markdown —
with animations, multi-provider AI superpowers, and a hidden easter egg.

```bash
pip install webtomd
```

---

*Demo GIF coming in Phase 4.*

## Usage

```bash
# Basic conversion (interactive terminal: auto-saves a .md file)
webtomd https://example.com/article

# Save to a specific file name
webtomd https://example.com/article -o article.md

# Force stdout output (useful for pipelines)
webtomd https://example.com/article --stdout

# Piped usage automatically stays stdout
webtomd https://example.com/article | rg "##"

# Filename strategy
webtomd https://example.com/article --name-strategy deterministic
webtomd https://example.com/article --name-strategy ai

# Copy to clipboard (works with auto-save or stdout)
webtomd https://example.com/article --copy

# AI summary (auto-detects your API key)
webtomd https://example.com/article --ai summarize

# Batch process
webtomd --batch urls.txt -o ./output/
```

### Output defaults

- Interactive terminal: `webtomd <url>` auto-saves to a generated `.md` file.
- Piped/non-interactive run: `webtomd <url>` prints markdown to stdout.
- `-o/--output` always wins if you provide it.
- `--stdout` always forces stdout.

### Naming defaults

- Default strategy: `deterministic` (title/URL + host slug + collision-safe suffixes).
- Optional strategy: `ai` (opt-in, requires any supported provider key in env).
- If AI naming is requested but unavailable, webtomd falls back to deterministic naming.

## Install

```bash
pip install webtomd

# With AI support (pick your provider)
pip install "webtomd[openai]"
pip install "webtomd[anthropic]"
pip install "webtomd[ai-all]"
```

## License

MIT
