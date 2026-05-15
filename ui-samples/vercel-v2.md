

OK Converted to Markdown (1042 tokens) via ui (design style guide (markdown) via
Playwright)
# Design Style Guide: Vercel: Build and deploy the best web experiences with the AI Cloud

> Source: https://vercel.com
> Extracted: 2026-05-15 17:05
> Viewport: 1280x720 | Full page: 2259px

## Design Philosophy

- **Light theme** ΓÇö light/white backgrounds with dark text
- **Dual typeface** ΓÇö Geist (UI) + Geist Mono (code/accent)
- **Pill-shaped elements** ΓÇö fully rounded buttons/badges
- **Generous whitespace** ΓÇö large section gaps for breathing room
- **Accent color** ΓÇö `#0068d6` used for interactive elements

---

## CSS Custom Properties

### Color Tokens

| Variable | Value |
|----------|-------|
| `--accents-1` | `#fafafa` |
| `--accents-2` | `#eaeaea` |
| `--accents-3` | `#999` |
| `--accents-4` | `#888` |
| `--accents-5` | `#666` |
| `--accents-6` | `#444` |
| `--accents-7` | `#333` |
| `--accents-8` | `#111` |
| `--ds-focus-color` | `hsla(212, 100%, 48%, 1)` |
| `--ds-overlay-backdrop-color` | `hsla(0, 0%, 98%, 1)` |
| `--geist-console-text-color-blue` | `#0070f3` |
| `--geist-console-text-color-default` | `#000` |
| `--geist-console-text-color-pink` | `#eb367f` |
| `--geist-console-text-color-purple` | `#7928ca` |
| `--geist-link-color` | `hsla(212, 100%, 48%, 1)` |
| `--geist-selection-text-color` | `hsla(0, 0%, 95%, 1)` |

### Spacing & Size Tokens

| Variable | Value |
|----------|-------|
| `--ds-page-width-with-margin` | `calc(1400px + calc(2 * 24px))` |
| `--geist-gap` | `24px` |
| `--geist-gap-double` | `48px` |
| `--geist-gap-double-negative` | `-48px` |
| `--geist-gap-half` | `12px` |
| `--geist-gap-half-negative` | `-12px` |
| `--geist-gap-negative` | `-24px` |
| `--geist-gap-quarter` | `8px` |
| `--geist-gap-quarter-negative` | `-8px` |
| `--geist-gap-section` | `32px` |
| `--geist-page-margin` | `24px` |
| `--geist-page-width-with-margin` | `calc(1200px + calc(2 * 24px))` |
| `--geist-space-gap` | `24px` |
| `--geist-space-gap-half` | `12px` |
| `--geist-space-gap-half-negative` | `-12px` |
| `--geist-space-gap-negative` | `-24px` |
| `--geist-space-gap-quarter` | `8px` |
| `--geist-space-gap-quarter-negative` | `-8px` |

### Typography Tokens

| Variable | Value |
|----------|-------|
| `--font-mono` | `"Geist Mono", ui-monospace, SFMono-Regular, Roboto Mono, Menlo, Monaco, Liber...` |
| `--font-mono-fallback` | `"Roboto Mono", Menlo, Monaco, Lucida Console, Liberation Mono, DejaVu Sans Mo...` |
| `--font-sans` | `"Geist", Arial, Apple Color Emoji, Segoe UI Emoji, Segoe UI Symbol` |
| `--font-sans-fallback` | `"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", "Oxygen", "...` |
| `--font-space-grotesk` | `Space Grotesk, "Geist", Arial, Apple Color Emoji, Segoe UI Emoji, Segoe UI Sy...` |
| `--geist-form-font` | `.875rem` |
| `--geist-form-large-font` | `1rem` |
| `--geist-form-small-font` | `.875rem` |
| `--geist-text-gradient` | `linear-gradient(180deg, #000c 0%, #000 100%)` |


## Color Palette

### Backgrounds

**Dark / Base**
- `#171717`

**Light / Surface**
- `#ffffff` (used 9x)
- `#fafafa`

**Vibrant / Accent**
- `#f5a623`

### Text

**Dark / Base**
- `#171717` (used 390x)
- `#4d4d4d` (used 383x)
- `#111111`
- `#0068d6`
- `#7820bc`

**Light / Surface**
- `#666666` (used 67x)
- `#ffffff` (used 13x)
- `#8f8f8f` (used 8x)

**Vibrant / Accent**
- `#f5a623`

### Borders

**Dark / Base**
- `#171717` (used 75x)

**Light / Surface**
- `#a8a8a8` (used 8x)
- `#ebebeb` (used 6x)

**Semi-transparent**
- `rgba(0, 0, 0, 0.05)` (used 68x)
- `rgba(0, 0, 0, 0.08)` (used 37x)

**Primary accent**: `#0068d6`


## Typography

**Font stack**: Geist, Geist Mono

| Role | Font | Size | Weight | Line Height | Tracking |
|------|------|------|--------|-------------|----------|
| Display / H1 | Geist | 48px | 600 | 48px | -2.28px |
| Display / H1 | Geist | 32px | 600 | 40px | -1.28px |
| H3 | Geist | 24px | 500 | 32px | -0.96px |
| H2 | Geist | 24px | 600 | 32px | -0.96px |
| Body | Geist | 20px | 400 | 36px | normal |
| Body | Geist | 16px | 400 | 24px | normal |
| Body | Geist | 16px | 500 | 24px | normal |
| Body | Geist | 16px | 600 | 24px | -0.32px |
| Body Small | Geist | 14px | 400 | 14px | normal |
| Body Small | Geist | 14px | 500 | 20px | normal |
| Body Small | Geist Mono | 14px | 400 | 20px | normal |
| Caption | Geist | 12px | 400 | 16px | normal |
| H2 | Geist Mono | 12px | 500 | 12px | normal |
| Caption | Geist Mono | 8px | 600 | 8px | normal |


## Spacing Scale

`1px` ┬╖ `2px` ┬╖ `3px` ┬╖ `4px` ┬╖ `6px` ┬╖ `8px` ┬╖ `10px` ┬╖ `12px` ┬╖ `14px` ┬╖ `16px` ┬╖ `24px` ┬╖ `32px` ┬╖ `40px` ┬╖ `48px` ┬╖ `64px` ┬╖ `85px` ┬╖ `90px`

*Based on a **4px grid** system.*


## Borders, Radii & Effects

**Border radius**: `100%`, `2px`, `4px`, `6px`, `100px`, `9999px`

**Shadows**:
- `rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px ...`
- `rgb(235, 235, 235) 0px 0px 0px 1px`
- `rgba(0, 0, 0, 0.08) 0px 0px 0px 1px, rgba(0, 0, 0, 0.04) 0px 2px 2px 0px, rgb(250, 250, 250) 0px ...`
- `rgba(0, 0, 0, 0.08) 0px 0px 0px 1px, rgb(250, 250, 250) 0px 0px 0px 1px`
- `rgb(235, 235, 235) 0px 0px 0px 1px, rgba(0, 0, 0, 0.05) 0px 1px 2px 0px`


## Component Patterns

### Buttons

- **"Products"** (ghost)
  - `background: transparent` ┬╖ `color: #4d4d4d`
  - `font: 14px / 400`
  - `padding: 8px 12px` ┬╖ `radius: 9999px`

- **"Ask AI"** (filled)
  - `background: #ffffff` ┬╖ `color: #171717`
  - `font: 14px / 500`
  - `padding: 0px 6px` ┬╖ `radius: 6px`

- **"Sign Up"** (filled)
  - `background: #171717` ┬╖ `color: #ffffff`
  - `font: 14px / 500`
  - `padding: 0px 6px` ┬╖ `radius: 6px`

### Navigation

- **41 links**: AI Cloud, AI GatewayOne endpoi, SandboxIsolated, saf, Vercel AgentAn agent, AI SDKThe AI Toolkit, v0Build applications
  - Layout: `flex`, gap: `normal`

- **61 links**: Templates, Supported frameworks, Marketplace, Domains, Next.js on Vercel, Turborepo
  - Layout: `block`, gap: `normal`


## Layout Patterns

### Grid
- `<span>` ΓÇö 1 columns, gap `normal`
- `<section>` ΓÇö 12 columns, gap `normal`

### Flexbox
- `<div>`, row, (2 children)
- `<header>`, row, justify: space-between, align: center, gap: 32px, (2 children)
- `<nav>`, row, align: center, (2 children)
- `<ul>`, row, (3 children)
- `<div>`, column, (4 children)
- `<div>`, column, justify: center, align: center, gap: 32px, (2 children)


## Assets

0 images, 30 SVG icons detected.
