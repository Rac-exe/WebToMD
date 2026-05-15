# Design Style Guide: Vercel: Build and deploy the best web experiences with the AI Cloud

> Source: https://vercel.com
> Extracted: 2026-05-15 16:41
> Viewport: 1280x720 | Full page height: 2259px

## Design Philosophy

- Light-themed interface
- Dual typeface system: Geist Mono, Geist
- Pill-shaped elements (fully rounded corners)
- Glassmorphism / backdrop blur effects
- Generous whitespace with large section padding

---

## CSS Custom Properties

| Variable | Value |
|----------|-------|
| `--banner-height` | `0px` |
| `--banner-min-height` | `64px` |
| `--font-mono` | `"Geist Mono", ui-monospace, SFMono-Regular, Roboto Mono, Menlo, Monaco, Liberation Mono, DejaVu Sans Mono, Courier New, monospace, Apple Color Emoji, Segoe UI Emoji, Segoe UI Symbol` |
| `--font-sans` | `"Geist", Arial, Apple Color Emoji, Segoe UI Emoji, Segoe UI Symbol` |
| `--vh100-offset` | `calc(64px + 0px)` |


## Color Palette

### Backgrounds
- `rgb(255, 255, 255)` — near-white
- `rgb(23, 23, 23)` — dark
- `rgb(250, 250, 250)` — near-white
- `rgb(245, 166, 35)`

### Text Colors
- `rgb(23, 23, 23)` — dark
- `rgb(77, 77, 77)` — neutral gray
- `rgb(255, 255, 255)` — near-white
- `rgb(0, 104, 214)`
- `rgb(120, 32, 188)`
- `rgb(102, 102, 102)` — neutral gray
- `rgb(245, 166, 35)`
- `rgb(17, 17, 17)` — near-black
- `rgb(143, 143, 143)` — light gray

### Border Colors
- `rgba(0, 0, 0, 0.08)`
- `rgb(168, 168, 168)`
- `rgb(235, 235, 235)`
- `rgb(23, 23, 23) rgba(0, 0, 0, 0.05) rgba(0, 0, 0, 0.05) rgb(23, 23, 23)`
- `rgb(23, 23, 23) rgb(23, 23, 23) rgba(0, 0, 0, 0.05)`
- `rgb(23, 23, 23) rgba(0, 0, 0, 0.05) rgb(23, 23, 23) rgb(23, 23, 23)`
- `rgb(23, 23, 23) rgb(235, 235, 235) rgb(23, 23, 23) rgb(23, 23, 23)`
- `rgb(23, 23, 23)`

**Likely accent color**: `rgb(0, 104, 214)`


## Typography

| Role | Font | Size | Weight | Line Height | Letter Spacing |
|------|------|------|--------|-------------|----------------|
| Display / H1 | Geist | 48px | 600 | 48px | -2.28px |
| Display / H1 | Geist | 32px | 600 | 40px | -1.28px |
| H3 | Geist | 24px | 500 | 32px | -0.96px |
| H2 | Geist | 24px | 600 | 32px | -0.96px |
| Body | Geist | 20px | 400 | 36px | normal |
| Body | Geist | 16px | 400 | 24px | normal |
| Body | Geist | 16px | 500 | 24px | normal |
| Body | Geist | 16px | 600 | 24px | -0.32px |
| Body small | Geist | 14px | 400 | 14px | normal |
| Body small | Geist | 14px | 500 | 20px | normal |
| Body small | Geist Mono | 14px | 400 | 20px | normal |
| Caption / Small | Geist | 12px | 400 | 16px | normal |
| H2 | Geist Mono | 12px | 500 | 12px | normal |
| Caption / Small | Geist Mono | 8px | 600 | 8px | normal |

**Font families in use**: Geist, Geist Mono


## Spacing Scale

`1px` · `2px` · `3px` · `4px` · `6px` · `8px` · `10px` · `12px` · `14px` · `16px` · `24px` · `32px` · `40px` · `48px` · `64px` · `84.5px` · `90px`

*Appears to use a **4px base grid** system.*


## Borders, Radii & Effects

**Border radius values**: `100%`, `2px`, `4px`, `6px`, `100px`, `9999px`

**Border widths**: `0px 0px 1px`, `0px 1px 0px 0px`, `0px 1px 1px 0px`, `1px`

**Box shadows**:
- `rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgb(235, 235, 235) 0px 0px 0px 1px`
- `rgb(235, 235, 235) 0px 0px 0px 1px`
- `rgba(0, 0, 0, 0.08) 0px 0px 0px 1px, rgba(0, 0, 0, 0.04) 0px 2px 2px 0px, rgb(250, 250, 250) 0px 0px 0px 1px`
- `rgba(0, 0, 0, 0.08) 0px 0px 0px 1px, rgb(250, 250, 250) 0px 0px 0px 1px`
- `rgb(235, 235, 235) 0px 0px 0px 1px, rgba(0, 0, 0, 0.05) 0px 1px 2px 0px`

**Visual effects**:
- `filter: blur(0px)`


## Component Patterns

### Buttons

- **""**
  - Background: `rgba(0, 0, 0, 0)`
  - Color: `rgb(23, 23, 23)`
  - Font: 16px 400
  - Padding: `0px`
  - Border radius: `0px`
  - Border: `0px solid rgb(235, 235, 235)`

- **"Products"**
  - Background: `rgba(0, 0, 0, 0)`
  - Color: `rgb(77, 77, 77)`
  - Font: 14px 400
  - Padding: `8px 12px`
  - Border radius: `9999px`
  - Border: `0px none rgb(77, 77, 77)`

- **"AI GatewayOne endpoint, all your models"**
  - Background: `rgba(0, 0, 0, 0)`
  - Color: `rgb(77, 77, 77)`
  - Font: 14px 400
  - Padding: `12px`
  - Border radius: `6px`
  - Border: `0px solid rgb(235, 235, 235)`

### Navigation

- **Nav** with 41 links: AI Cloud, AI GatewayOne endpoint, all yo, SandboxIsolated, safe code exe, Vercel AgentAn agent that know, AI SDKThe AI Toolkit for TypeS, v0Build applications with AI
  - Layout: `flex`, gap: `normal`

- **Nav** with 61 links: Templates, Supported frameworks, Marketplace, Domains, Next.js on Vercel, Turborepo
  - Layout: `block`, gap: `normal`


## Layout Patterns

### CSS Grid Usage

- `<span>`: columns `16px`, gap `normal`
- `<div>`: columns `32px`, gap `normal`

### Flexbox Usage

- `<div>`: row (2 children)
- `<header>`: row, justify: space-between, align: center, gap: 32px (2 children)
- `<div>`: row, justify: flex-end, align: center, gap: 12px (2 children)
- `<div>`: column (4 children)
- `<div>`: column, justify: center, align: center, gap: 32px (2 children)
- `<div>`: column, justify: flex-start, align: center, gap: 24px (2 children)
- `<div>`: row, justify: center, align: stretch, gap: 24px (2 children)


## Assets Detected

0 images and 30 inline SVG icons detected.

### SVG Icons (30 found)

- (icon) — 90px × 18px
- (icon) — 14px × 14px
- (icon) — 16px × 16px
- (icon) — 16px × 16px
- (icon) — 16px × 16px
- (icon) — 16px × 16px
- (icon) — 16px × 16px
- (icon) — 16px × 16px
- (icon) — 16px × 16px
- (icon) — 16px × 16px
- (icon) — 16px × 16px
- (icon) — 16px × 16px
- (icon) — 16px × 16px
- (icon) — 16px × 16px
- (icon) — 16px × 16px
