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
- Include site-specific chrome pruning in Phase 2.
- Keep adding tests locally for validation but do not commit test files.
- Use aggressive normalization for table/list formatting in Phase 2.
- Phase 2 commit preference: granular one-line commits per sub-feature.

## 2026-05-07 21:39:42 +05:30 — Full 5-link command matrix rerun (manual terminal execution)

### User request
- Re-run all currently working commands against the same 5 benchmark URLs.
- Keep `.md` output artifacts for direct manual inspection.
- Provide full analysis of command behavior and content quality.

### Commands executed across all 5 URLs
- `python -m webtomd.cli --silent <url> -o <file>`
- `python -m webtomd.cli --silent --stdout <url>`
- `python -m webtomd.cli --silent <url>` (plain mode in this non-interactive shell, redirected to file)
- `python -m webtomd.cli --silent --name-strategy deterministic <url>` (redirected)
- `python -m webtomd.cli --silent --name-strategy ai <url>` (redirected)
- `python -m webtomd.cli --silent --stdout --copy <url>` (copy-mode status check + captured output)

### Output location
- `eval-runs/five-links-full-20260507-212944/`
  - `explicit/` (clean baseline `-o` files)
  - `stdout/`
  - `plain/`
  - `name-deterministic/`
  - `name-ai/`
  - `logs/timings.csv`
  - `logs/content-summary.json`

### Runtime observations
- 4 URLs consistently complete in ~3–8s across modes.
- Minecraft homepage remains the outlier at ~113–125s due to very heavy page/chrome.

### Quality observations
- `explicit/` outputs are the most reliable representation for manual quality checks.
- Redirected stdout/plain/name-strategy files in PowerShell required UTF-8 normalization for easier viewing.
- Even after normalization, redirected files can show symbol drift on some Unicode characters vs explicit file output.
- Core extracted structure remains present across modes (headings/list counts align closely).

### Site-level quality snapshot from explicit mode
- Minecraft (`www-minecraft-net-en-us.md`): very nav-heavy and large; content present but significant chrome noise.
- Linear My Issues (`linear-app-docs-my-issues.md`): main doc content captured with good headings/lists; some sidebar/menu noise remains.
- Linear Reviews (`linear-app-docs-diffs.md`): strong capture of primary sections; still includes docs shell links.
- Wikipedia Egyptians (`en-wikipedia-org-wiki-egyptians.md`): rich content captured; includes heavy infobox/reference density as expected.
- Claude Skills Overview (`platform-claude-com-docs-en-agents-and-tools-agent-skills-overview.md`): core page captured but retains docs navigation and cookie/settings shell content.

## 2026-05-07 23:07:10 +05:30 — Quality Improvements plan implementation

### Commit-first step completed
- Created focused commit for already-finished changes only:
  - `webtomd/output.py` stdout hardening
  - this worklog benchmark entry
- Commit: `e2832c4`
- Kept `eval-runs/` and `tests/` artifacts uncommitted.

### Code changes implemented
- `webtomd/output.py`
  - Added stdout UTF-8 reconfigure attempt with safe fallback path to avoid Windows encoding crashes.
- `webtomd/fetcher.py`
  - Implemented staged fallback chain with strategy trace:
    1. trafilatura
    2. readability (gated by page-shape heuristic)
    3. playwright (optional, JS-heavy trigger only)
    4. raw HTML best-effort fallback
  - Added timeout wrappers for fetch/extract stages to avoid long stalls.
  - Added `get_last_fetch_trace()` for strategy visibility.
  - Added selector mode behavior to keep raw HTML for CSS selection pass.
- `webtomd/converter.py`
  - Added `SelectorNotFoundError` and strict selector miss handling.
  - Added conservative pre-conversion pruning for cookie/consent/sidebar/boilerplate.
  - Added markdown-level chrome filtering + duplicate-line cleanup.
  - Tightened numbering normalization to avoid `3rd-party` -> `3. rd-party` regression.
- `webtomd/cli.py`
  - Enabled `--selector` (removed Phase-2 guard).
  - Wired selector into fetch/title/markdown conversion path.
  - Added friendly selector-not-found error.
  - Included fetch strategy in conversion success message.

### Validation
- Local tests:
  - `python -m pytest tests/test_fetcher.py tests/test_converter.py tests/test_output.py tests/test_cli_modes.py tests/test_naming.py`
  - Result: `23 passed`.
- Lint diagnostics on edited source files: no linter errors.
- Selector check:
  - `--selector body` succeeds.
  - invalid selector fails with user-friendly `No element matched selector: ...` message.

### Post-change benchmark rerun
- Final benchmark artifacts:
  - `eval-runs/five-links-post-improvements-20260507-230411/`
  - `logs/timings.csv`
  - `logs/content-summary.json`
- Runtime:
  - 4 links complete in typical single-digit seconds.
  - Minecraft remains the slowest link but now finishes with richer output.

### Output quality snapshot (post-change explicit mode)
- Minecraft: `1075` lines, `43` headings, `139` list items (substantially richer than over-pruned intermediate run).
- Linear My Issues: `75` lines, `7` headings, `16` list items (cleaner with reduced shell noise).
- Linear Reviews: `133` lines, `12` headings (retains core content with less docs chrome).
- Wikipedia Egyptians: `1110` lines, `35` headings (strong main-content retention).
- Claude Skills Overview: `305` lines, `31` headings (cookie/loading shell markers removed in this run).

## 2026-05-07 23:28:24 +05:30 — Next-Level Quality phase execution

### Commit sequence executed
- Checkpoint one-line commit:
  - `2faa3f6` — Implement quality fallback, selector support, and benchmark validation
- Granular one-line commits:
  - `677c54d` — Score extraction candidates and pick highest-quality fallback
  - `3c67215` — Add conservative pruning guardrails to avoid over-stripping content
  - `13b4c5c` — Reduce link-wall noise and harden numbering normalization
  - `3369a78` — Tune stage timeouts and failover budgets for heavy pages
  - `146bad1` — Show concise extraction reason in conversion success output

### Code improvements delivered
- `webtomd/fetcher.py`
  - Added candidate scoring for trafilatura/readability/playwright outputs.
  - Added score-based winner selection with thresholding and detailed trace note.
  - Added adaptive per-page stage timeouts (heavy-page aware).
  - Added compatibility wrapper for monkeypatched function signatures in tests.
- `webtomd/converter.py`
  - Strengthened anti-overprune guardrails for structural cleanup.
  - Added stronger markdown cleanup for repeated link-wall lines.
  - Improved numbering normalization around ordinal forms (`3rd-party` cases).
- `webtomd/cli.py`
  - Added concise strategy reason text in success output.

### Validation
- Focused tests:
  - `python -m pytest tests/test_fetcher.py tests/test_converter.py tests/test_output.py tests/test_cli_modes.py tests/test_naming.py`
  - Result: `23 passed`.

### Benchmark rerun
- New artifacts:
  - `eval-runs/five-links-next-phase-20260507-232241/`
  - `logs/timings.csv`
  - `logs/before-after-summary.json`

### Before/after quality snapshot (vs `five-links-post-improvements-20260507-230411`)
- Minecraft:
  - before: `1075` lines / `43` headings / `139` list items
  - after: `1160` lines / `49` headings / `191` list items
  - note: richer retained content after adaptive pruning guardrails.
- Linear My Issues:
  - unchanged at `75` lines / `7` headings / `16` list items.
- Linear Reviews:
  - unchanged at `133` lines / `12` headings.
- Wikipedia Egyptians:
  - reduced to `1039` lines (from `1110`) with headings preserved (`35`).
- Claude Skills Overview:
  - reduced to `295` lines (from `305`) with near-stable structure (`29` headings vs `31`).

### Runtime comparison (explicit mode)
- previous:
  - Minecraft `113.90s`, Linear My Issues `3.22s`, Linear Reviews `3.68s`, Wikipedia `4.26s`, Claude docs `3.90s`
- current:
  - Minecraft `116.52s`, Linear My Issues `3.41s`, Linear Reviews `5.00s`, Wikipedia `5.80s`, Claude docs `3.06s`
- interpretation:
  - quality/guardrail changes improved structural retention and cleanup;
  - latency is still bounded and predictable but not yet materially faster on heavy pages.

## 2026-05-07 23:31:00 +05:30 — Phase 3 implementation (AI + configure + batch + metadata + easter egg)

### Commit sequence
- `c44b9ec` — Implement AI provider runtime with multi-provider support and graceful fallback
- `f1a68e9` — Implement interactive --configure flow with provider setup wizard
- `91c3c72` — Wire --ai, --configure, --batch, and --metadata into CLI lifecycle
- `9287688` — Implement space galaxy shooter easter egg with hidden trigger

### What changed

#### AI Provider Runtime (`webtomd/ai/`)
- `providers.py`: Implemented all 5 provider classes (Anthropic, OpenAI, Gemini, Groq, Ollama) with real SDK calls.
- `detector.py`: Implemented `detect()` with env-var priority chain and optional `provider_override` from config.
- `__init__.py`: Added `process_ai()` entry point and `AIUnavailableError` for graceful degradation.
- `prompts.py`: Already complete from earlier scaffold — builds mode-specific prompts.

#### Interactive Setup (`webtomd/ai/configure.py`)
- Guided terminal wizard using `rich.prompt`:
  - provider selection menu (1-5)
  - key capture (or Ollama host)
  - persists `ai_provider` to `~/.webtomdrc`
  - sets env var for immediate session use
  - security tip for non-Ollama providers

#### CLI Integration (`webtomd/cli.py`)
- Removed Phase 2/3 guardrails for `--ai`, `--configure`, `--batch`, `--metadata`.
- `--configure` triggers wizard and exits.
- `--ai <mode>` validates mode then applies AI post-processing after markdown conversion.
- `--batch <file>` processes URL list sequentially with per-URL error isolation and summary.
- `--metadata` passes through to `to_markdown()` frontmatter builder.
- Refactored into `_convert_single()` for reuse by both single-URL and batch paths.
- Added `_apply_ai()` helper with graceful fallback to raw markdown on any AI failure.

#### Batch Mode
- Reads URL file (one per line, `#` comments supported).
- Per-URL failures are isolated and counted.
- End summary: `N succeeded, M failed`.

#### Metadata Frontmatter
- Already wired from Phase 1 converter logic; Phase 3 just removed the guard.
- End-to-end verified: YAML frontmatter with title, URL, date prepended to output.

#### Easter Egg (`webtomd/easter_egg.py`)
- Full space galaxy shooter game using `rich.Live` + `pynput`.
- Arrow keys move, space shoots, q quits.
- Wave-based enemy spawning with increasing difficulty.
- Score tracking, lives system, game over screen.
- Hidden trigger: `webtomd https://play.webtomd.dev`

### Validation
- **Test suite**: 28 passed, 0 failures.
- **--metadata**: Verified end-to-end with `--stdout --silent` — YAML frontmatter correct.
- **--ai (no key)**: Graceful fallback — warning printed, raw markdown output preserved.
- **--ai (invalid mode)**: Clear error with valid mode list.
- **--batch**: 2-URL test file processed successfully with per-URL status and summary.
- **--configure**: Module imports verified; interactive flow tested at import level.
- **Easter egg**: Module imports verified; game loop structure validated.
- **Lints**: No linter errors in any changed files.

---

## Easter Egg Upgrade — Full Arcade Experience

### Visual Enhancements
- Rich color rendering: cyan player, red/magenta/yellow enemies, green power-ups.
- Explosion effects with animated `*`/`+` particles and color cycling.
- Styled HUD with box-drawing border (Unicode with ASCII fallback).
- ASCII art title screen, controls display, and animated game-over screen.

### Gameplay Mechanics
- Fire rate limiter with normal and rapid-fire cooldowns.
- Four enemy movement patterns: straight, zigzag, dive, fast.
- Enemy HP system — tougher enemies in later waves.
- Boss waves every 5 waves with custom AI: lateral movement + aimed shots.
- Three power-up types: rapid fire, shield, triple shot (each with timers).
- Player shield absorbs one hit; triple shot fires 3 bullets simultaneously.
- High score persistence to `~/.webtomd-highscore`.
- Sound feedback via terminal bell (`\a`) on game events.
- Replay from game-over screen without restarting the CLI.

### Balance Tuning (based on user feedback)
- Reduced `FIRE_COOLDOWN_NORMAL` (4→2) and `FIRE_COOLDOWN_RAPID` (2→1).
- Slowed enemy descent rate: `max(6 - wave//3, 2)` instead of `max(4 - wave//3, 1)`.
- Slowed zigzag and dive enemy lateral/vertical speeds.
- Increased `BOSS_SHOOT_INTERVAL` (8→12) for more forgiving boss fights.
- Doubled player lateral movement speed (1→2 cells/tick).

### Obfuscation
- Renamed `webtomd/easter_egg.py` → `webtomd/_compat.py` with misleading docstring.
- CLI import updated from `webtomd.easter_egg` → `webtomd._compat`.
- Test file renamed `tests/test_easter_egg.py` → `tests/test_compat.py` with misleading docstring.

### Test Coverage
- 36 comprehensive tests covering all game mechanics: spawning, movement patterns, collisions, boss AI, power-ups, shield, triple shot, high score persistence, rendering, screen states, and trigger URL validation.
- All 98 tests passing after full easter egg implementation.

---

## Ship-Readiness + Performance Pass

### Ship-Readiness

#### `__main__.py`
- Created `webtomd/__main__.py` enabling `python -m webtomd` execution.
- One-liner importing and calling `app()` from `cli.py`.

#### README Overhaul
- Complete rewrite with: project tagline, feature list, full install instructions (pip/uv, optional extras, playwright), usage examples for every flag, output defaults table, AI setup section, configuration reference, contributing guide, and license.

#### `--help` Text Polish
- All `typer.Option` help strings reviewed and updated for consistency.
- Capitalization standardized, wording made concise and descriptive.
- Examples: "Save to file" → "Save to a specific file path", "No animations (pipe-safe)" → "Suppress spinners and preview (pipe-safe)".

#### Build Verification
- `uv build` produces clean `webtomd-0.1.0-py3-none-any.whl` and `.tar.gz`.
- All 17 modules included in wheel (core + AI + _compat).
- Entry point `webtomd = webtomd.cli:app` verified via `entry_points.txt`.
- `webtomd --help` and `python -m webtomd --help` both functional.
- `pyproject.toml` metadata complete: classifiers, keywords, URLs, license.

### Performance Pass

#### Heavy Page Optimization (`webtomd/fetcher.py`)
- **HTML size cap**: Pages exceeding 500KB skip trafilatura entirely and go straight to readability (much faster on bloated pages).
- **Parallel extraction**: Trafilatura + readability now run concurrently via `ThreadPoolExecutor(max_workers=2)` instead of sequentially. Playwright post-render extraction also parallelized.
- **Tighter heavy-page thresholds**: Lowered detection from 450KB/120 scripts → 300KB/80 scripts. Tightened budgets: extract 6s, readability 5s, playwright 10s (down from 8s/7s/12s).
- **`_safe_future_result`**: Helper to extract results from futures with safe error handling.

#### Playwright Install UX
- When `fetch_playwright` detects a JS-rendered page but playwright is not installed, prints a one-time friendly hint: install command and `playwright install chromium`.
- Gated by `_PLAYWRIGHT_HINT_SHOWN` module-level flag — only shown once per session.

### 5-URL Benchmark Results

| URL | Time | Words | Strategy |
|---|---|---|---|
| minecraft.net/en-us | 100.9s | 3,536 | raw_html |
| linear.app/docs/my-issues | 3.5s | 412 | raw_html |
| linear.app/docs/diffs | 2.0s | 1,210 | raw_html |
| wikipedia.org/wiki/Egyptians | 4.9s | 21,532 | readability |
| platform.claude.com/agent-skills | 1.9s | 2,218 | readability |

- 4 of 5 URLs complete in under 5 seconds.
- Minecraft.net is an outlier due to slow download phase (heavy CDN/JS page), not extraction.
- Readability strategy is correctly selected for content-rich pages (Wikipedia, Claude docs).
- All 98 tests passing.
