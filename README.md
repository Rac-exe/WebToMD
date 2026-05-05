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
# Basic conversion
webtomd https://example.com/article

# Save to file
webtomd https://example.com/article -o article.md

# Copy to clipboard
webtomd https://example.com/article --copy

# AI summary (auto-detects your API key)
webtomd https://example.com/article --ai summarize

# Batch process
webtomd --batch urls.txt -o ./output/
```

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
