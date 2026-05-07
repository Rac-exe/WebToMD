# webtomd Session Worklog

This file is a running record of what I changed, why I changed it, and what was verified.
I will keep appending to this file as work continues in this session.

## 2026-05-05 22:44:55 +05:30 — Initialization + Phase 1 Build complete

### 1) Project framing and naming decisions (from planning artifacts)
- Reviewed `mdsnap-pitch.html` and `mdsnap-sepm.md` to extract initial product scope.
- Renamed planning docs to `webtomd-pitch.html` and `webtomd-sepm.md`.
- Updated both planning docs to align with decisions:
  - working name: `webtomd`
  - package manager: `uv` (instead of Poetry)
  - easter egg: space shooter
  - no telemetry in v1
  - defer `--depth` to v2
  - AI behavior: graceful degradation when unavailable

Why:
- Keep requirements, messaging, and implementation direction in sync before writing code.

### 2) Repository scaffolding
- Created baseline structure:
  - package: `webtomd/` (+ `webtomd/ai/`)
  - tests: `tests/` (+ fixtures)
  - support dirs: `scripts/`, `docs/`
- Added root files:
  - `.gitignore`
  - `.python-version`
  - `pyproject.toml`
  - `README.md`
  - `LICENSE`

Why:
- Establish a clean, implementable skeleton before feature work.

### 3) Git ignore updates requested by user
- Added these two files to `.gitignore`:
  - `webtomd-pitch.html`
  - `webtomd-sepm.md`
- Verified with `git check-ignore` that both are ignored.

Why:
- User explicitly requested planning docs not be tracked in git.

### 4) Commit attribution guardrail
- Added project rule: `.cursor/rules/git-commits.mdc`
- Rule explicitly forbids adding `Co-authored-by` lines.

Why:
- User requested no co-author attribution in commit messages.

### 5) Phase 1 implementation work (completed)

#### `webtomd/renderer.py`
- Implemented:
  - `start_spinner(...)` using `rich.progress.Progress`
  - `print_success(...)`, `print_warn(...)`, `print_error(...)`
  - `print_markdown_preview(...)` with truncation at 30 lines
  - witty message cycling (`next_witty_message()`)

Why:
- Needed user-visible progress, status messaging, and markdown preview for CLI UX.

#### `webtomd/fetcher.py`
- Implemented Stage-1 fetch flow:
  - `fetch_trafilatura(url)`
  - `fetch(url, selector=None)` coordinator
- Wired sparse-content detection through `webtomd.utils.is_sparse`.
- If extraction is too sparse, raises a clear Phase-1 limitation error.

Why:
- Phase 1 scope is primary extractor only; fallback chain is Phase 2.

#### `webtomd/converter.py`
- Implemented HTML -> Markdown conversion via `markdownify`.
- Added optional CSS selector pre-extraction (`BeautifulSoup`).
- Added cleanup: trim output + collapse excessive blank lines.
- Implemented YAML frontmatter helper `_build_frontmatter(...)`.

Why:
- Core product value is clean Markdown conversion from extracted HTML.

#### `webtomd/output.py`
- Implemented:
  - `to_stdout(...)`
  - `to_file(...)`
  - `to_clipboard(...)` with graceful failure warning
  - `open_in_editor(...)` cross-platform

Why:
- Phase 1 requires stdout/file/clipboard output modes.

#### `webtomd/cli.py`
- Wired Phase-1 execution path end-to-end:
  - config load + merge
  - URL validation
  - spinner around fetch+convert
  - output routing (stdout/file/copy/open)
  - markdown preview
- Adjusted interface so direct invocation works:
  - `webtomd <url> [flags]`
- Added explicit guardrails for out-of-scope flags:
  - `--batch`, `--selector`, `--metadata` => Phase 2
  - `--ai`, `--configure` => Phase 3

Why:
- Provide a working user path now while clearly signaling phased feature rollout.

### 6) Tests added/updated
- Updated converter tests in `tests/test_converter.py`:
  - heading preservation
  - code block preservation
- Updated output tests in `tests/test_output.py`:
  - file writing works
  - clipboard failure is graceful (mocked)
- Existing utility/config/prompt tests retained.

Why:
- Ensure implemented behavior is covered and regressions are less likely.

### 7) Environment + verification
- `uv` was not installed initially; installed with `python -m pip install uv`.
- Synced dependencies and dev extras:
  - `python -m uv sync`
  - `python -m uv sync --extra dev`
- Added direct dependency needed by converter:
  - `python -m uv add beautifulsoup4`
- Smoke checks:
  - CLI help works.
  - Real conversion test works:
    - `.venv\\Scripts\\python -m webtomd.cli --silent https://docs.python.org/3/`
- Tests:
  - `.venv\\Scripts\\python -m pytest tests/`
  - Result: `15 passed`.
- Lint diagnostics checked for changed files: no linter issues reported.

Why:
- Validate that Phase-1 implementation is runnable and stable.

### 8) Current repo state snapshot
- `git status --short` currently shows only untracked files/directories (fresh scaffold + implementation).
- No commit created in this session.

---

## Update policy for this file
- I will append a new timestamped section for each substantial block of work.
- Each section will include:
  1. what changed,
  2. why it changed,
  3. what was verified.

## 2026-05-05 22:54:51 +05:30 — User extraction question (no code changes)

### What happened
- User asked whether two URLs from the same site can be extracted.
- Clarified that Phase 1 supports single-URL runs (one command per URL), while true multi-URL batch extraction is Phase 2.

### Why this clarification was needed
- Current CLI intentionally guards `--batch` as out-of-scope for Phase 1.
- Prevents confusion when users try multiple URLs at once.

### Verification
- Behavior already validated earlier in session:
  - single URL extraction works,
  - phased guardrails are active for not-yet-built flags.

## 2026-05-05 23:11:54 +05:30 — Output quality review (tryprmpt pages)

### What happened
- Reviewed extracted outputs:
  - `tryprmpt-home.md`
  - `tryprmpt-help.md`
- Compared output structure/quality against expected content layout for the source pages.

### Findings
- `tryprmpt-home.md` is too sparse and misses large sections from the page (high severity quality issue).
- `tryprmpt-help.md` is mostly complete but has markdown formatting defects:
  - numbered list items emitted as `1Text` instead of `1. Text`,
  - table sections degraded into line pairs (header/body not preserved),
  - shortcut blocks rendered as fenced inline fragments rather than a proper table/list.

### Why this matters
- Home page sparsity directly lowers trust in extraction quality for marketing pages.
- Help page formatting issues reduce readability and reduce usefulness for downstream RAG/chunking.

### Suggested next-step improvements
- Add markdown post-processing normalization:
  - fix numbered list tokenization (`^(\d+)([A-Za-z])` -> `$1. $2`),
  - detect 2-column table patterns and rebuild markdown tables.
- Tighten main-content targeting on landing pages:
  - optional extraction heuristic to prioritize repeated heading/section containers.

## 2026-05-05 23:23:29 +05:30 — Phase 1.5 implementation and verification

### What changed
- Implemented Phase 1.5 extraction quality improvements in `webtomd/fetcher.py`:
  - Added `_download_html()` fallback path:
    - try `trafilatura.fetch_url()` first,
    - then fallback to `httpx.get()` with browser-like user-agent if primary fetch fails.
  - Added quality heuristic in `fetch()`:
    - if trafilatura extraction is disproportionately short compared to source HTML, use raw HTML for conversion.
- Implemented Phase 1.5 markdown cleanup in `webtomd/converter.py`:
  - `_normalize_numbering()` now fixes broken tokens like:
    - `## 1Getting Started` -> `## 1. Getting Started`
    - `- 1Open` -> `- 1. Open`
  - `_sanitize_html()` removes noisy tags (`script`, `style`, `noscript`, `template`) before conversion.
  - `_drop_css_noise()` removes leaked CSS lines in markdown output.
- Extended tests:
  - `tests/test_fetcher.py`:
    - fallback to `httpx` when trafilatura fetch returns `None`,
    - prefer raw HTML when extracted content is too short.
  - `tests/test_converter.py`:
    - numbering normalization checks,
    - sanitize-html checks,
    - CSS noise filtering checks.

### Why these changes were required
- Real-world extraction on `tryprmpt.com` showed two issues:
  1. homepage was either too sparse or over-trimmed,
  2. docs page had broken numbered list formatting.
- The fallback fetch + quality heuristic improved coverage without waiting for full Phase 2 fallback chain.
- Post-processing normalization significantly improved readability for docs-style content.

### Verification performed
- Test suite run after changes:
  - `21 passed`.
- Re-ran same real-site extraction commands:
  - `https://www.tryprmpt.com/`
  - `https://www.tryprmpt.com/help`
- Result comparison:
  - `tryprmpt-home.md`: improved from **55 lines** to **105 lines** with much better section coverage.
  - `tryprmpt-help.md`: line count unchanged (**234**) but numbering quality improved (`1Getting` -> `1. Getting`, `- 1Open` -> `- 1. Open`).
- Remaining known gap:
  - some two-column table-like sections in help output still flatten into line pairs; table reconstruction remains future work.

## 2026-05-07 20:17:23 +05:30 — Auto-save and naming UX implementation

### What changed
- Implemented output-mode resolver in `webtomd/cli.py`:
  - explicit `-o/--output` -> file
  - `--stdout` -> stdout
  - interactive terminal -> auto-save
  - piped/non-interactive -> stdout
- Added deterministic filename generation in `webtomd/utils.py`:
  - `slugify(...)`
  - `host_slug(...)`
  - `unique_path(...)` with `-2`, `-3`, ... collision handling
  - `build_output_path(...)` as the final resolver
- Added title hint extraction in `webtomd/converter.py`:
  - `extract_title_hint(...)`
- Added naming config/flag support:
  - `name_strategy` field in `webtomd/config.py` (default: `deterministic`)
  - `--name-strategy` and `--stdout` in CLI
- Added AI naming opt-in scaffold:
  - new file `webtomd/ai/naming.py`
  - checks provider env keys
  - generates concise filename stem
  - non-blocking fallback to deterministic naming with warning
- Updated docs in `README.md` for new defaults and flags.

### Why these changes were required
- Better UX goal: plain `webtomd <url>` should usually produce a ready-to-use file without requiring `-o`.
- Preserve CLI power behavior by keeping stdout for piped/non-interactive runs.
- Add predictable naming that avoids collisions and supports future smarter naming.

### Verification plan
- Run full tests.
- Validate:
  - interactive auto-save,
  - piped stdout behavior,
  - `--stdout` override,
  - deterministic naming,
  - AI naming fallback path.

### Verification results (2026-05-07 20:20:26 +05:30)
- Test suite: `28 passed`.
- Manual checks:
  - `--stdout` emitted markdown to stdout successfully.
  - Plain piped run (`webtomd <url> | ...`) produced stdout and created **0 files** in a temp folder.
  - Deterministic naming generated host-aware filename stem (`example-title-examplecom.md`).
  - `--name-strategy ai --stdout` executed without failure and stayed non-blocking.
- Additional robustness fix:
  - On Windows CP1252 terminals, Unicode status glyphs caused render errors.
  - Added encoding-safe status symbols in `webtomd/renderer.py` (`OK/WARN/ERR` fallback).

## 2026-05-07 20:40:02 +05:30 — Multi-link method verification and output quality audit

### Scope
- Verified behavior against these links:
  - `https://www.minecraft.net/en-us`
  - `https://linear.app/docs/my-issues`
  - `https://linear.app/docs/diffs`
  - `https://en.wikipedia.org/wiki/Egyptians`
  - `https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview`

### What was run
- Quick reachability check with `httpx` for all links (all returned HTTP 200 quickly).
- Guardrail command checks:
  - `--batch` (Phase 2 message),
  - `--selector` (Phase 2 message),
  - `--ai` (Phase 3 message).
- Full extraction audit via internal conversion pipeline (same converter + naming logic), writing outputs under:
  - `eval-runs/2026-05-07-internal-eval`

### Key findings
- Core extraction quality differs by site type:
  - Linear docs pages: generally good content fidelity; minor nav/header noise remains.
  - Claude docs page: high nav/footer chrome noise; actual article mixed with doc shell.
  - Wikipedia page: substantial sidebar/nav clutter overwhelms article body.
  - Minecraft marketing page: highly noisy due mega-menu/navigation-heavy layout.
- AI naming path currently acts as an opt-in scaffold and may produce same filename as deterministic when title is already high quality.
- Important runtime note:
  - direct CLI runs on some of these links can stall at `trafilatura.fetch_url` before fallback kicks in; this needs a timeout/short-circuit hardening pass.

### Output metrics snapshot (internal eval)
- Minecraft: 1171 lines, 26 headings, 191 list items (very noisy)
- Linear My Issues: 118 lines, 7 headings (good)
- Linear Reviews: 181 lines, 12 headings (good)
- Wikipedia Egyptians: 1497 lines, 37 headings, 664 table markers (heavy chrome)
- Claude Skills Overview: 521 lines, 39 headings, 10 code fences (content present but shell-heavy)

### Recommended follow-ups
- Add extraction-time timeout around trafilatura primary fetch.
- Add doc-shell pruning heuristics for known doc portals (Linear, Claude docs, Wikipedia).
- Add readability fallback before raw-html conversion for nav-heavy pages.

## 2026-05-07 20:50:08 +05:30 — Commits created and Phase 2 planning kickoff

### Commits completed
- `84e5716` — Add auto-save defaults and pluggable filename strategies
- `e49bcf2` — Document new output defaults and naming behavior

### Commit constraints honored
- Did not include `tests/` in these commits.
- Did not include converted URL outputs in these commits.
- Left evaluation artifacts and generated outputs untracked.

### Phase 2 planning decisions captured
- `--selector` should be implemented in next coding step (not deferred).
- Phase 2 priority order:
  1. fallback chain (readability + playwright),
  2. stdin/batch features afterward.
- Playwright install UX direction:
  - trigger install on first actual playwright fallback need.
