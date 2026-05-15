

OK Converted to Markdown (1121 tokens) via ui (design style guide (markdown) via
Playwright)
# Design Style Guide: Tailwind CSS - Rapidly build modern websites without ever leaving your HTML.

> Source: https://tailwindcss.com
> Extracted: 2026-05-15 17:07
> Viewport: 1280x720 | Full page: 11724px

## Design Philosophy

- **Mixed theme** ΓÇö uses both light and dark surfaces
- **Dual typeface** ΓÇö inter (UI) + plexMono (code/accent)
- **Pill-shaped elements** ΓÇö fully rounded buttons/badges
- **Glassmorphism** ΓÇö backdrop blur effects for depth
- **Generous whitespace** ΓÇö large section gaps for breathing room
- **Accent color** ΓÇö `#fb64b6` used for interactive elements

---

## CSS Custom Properties

### Other Tokens

| Variable | Value |
|----------|-------|
| `--lightningcss-dark` | `` |
| `--lightningcss-light` | `initial` |


## Color Palette

### Backgrounds

**Dark / Base**
- `#030712`
- `#000000`

**Light / Surface**
- `#ffffff` (used 23x)

**Vibrant / Accent**
- `#00bcff`
- `#00a6f4`
- `#f6339a`
- `#7c86ff`
- `#c27aff`
- `#fb64b6`

**Semi-transparent**
- `rgba(0, 0, 20, 0.05)` (used 17x)
- `rgba(255, 255, 255, 0.2)` (used 15x)
- `rgba(0, 0, 0, 0.02)` (used 13x)
- `rgba(255, 255, 255, 0.1)` (used 10x)
- `rgba(5, 5, 20, 0.2)` (used 7x)
- `rgba(255, 255, 255, 0.15)` (used 6x)

### Text

**Dark / Base**
- `#030712` (used 1339x)
- `#000000` (used 19x)
- `#4a5565` (used 17x)
- `#1e2939` (used 12x)
- `#00598a` (used 10x)
- `#e60076` (used 6x)

**Light / Surface**
- `#90a1b9` (used 114x)
- `#f8fafc` (used 113x)
- `#cad5e2` (used 88x)
- `#ffffff` (used 17x)
- `#96f7e4` (used 14x)
- `#6a7282` (used 12x)

**Vibrant / Accent**
- `#74d4ff` (used 45x)
- `#fb64b6` (used 42x)
- `#00a6f4` (used 6x)

**Semi-transparent**
- `rgba(0, 0, 0, 0.2)` (used 14x)
- `rgba(4, 8, 18, 0.5)`

### Borders

**Dark / Base**
- `#000000`

**Light / Surface**
- `#ffffff`

**Semi-transparent**
- `rgba(0, 0, 20, 0.05)` (used 54x)
- `rgba(5, 5, 20, 0.2)` (used 8x)
- `rgba(0, 0, 0, 0.05)`
- `rgba(255, 255, 255, 0.05)`
- `rgba(115, 212, 255, 0.6)`

**Primary accent**: `#fb64b6`


## Typography

**Font stack**: inter, plexMono

| Role | Font | Size | Weight | Line Height | Tracking |
|------|------|------|--------|-------------|----------|
| Display / H1 | inter | 96px | 400 | 96px | -4.8px |
| Display / H1 | inter | 40px | 500 | 40px | -2px |
| Display / H1 | inter | 36px | 600 | 48px | normal |
| H2 | inter | 30px | 600 | 36px | normal |
| H3 | inter | 24px | 500 | 40px | normal |
| H3 | inter | 20px | 500 | 40px | normal |
| H3 | inter | 18px | 500 | 28px | normal |
| Body | plexMono | 17px | 500 | 28px | normal |
| Body | inter | 16px | 400 | 24px | normal |
| Body | inter | 16px | 500 | 24px | normal |
| H3 | inter | 16px | 600 | 24px | normal |
| Body Small | inter | 14px | 400 | 24px | normal |
| Body Small | inter | 14px | 600 | 24px | normal |
| Body Small | inter | 14px | 500 | 24px | normal |
| Body Small | inter | 14px | 700 | 24px | normal |
| Code | plexMono | 14px | 500 | 28px | normal |
| Body Small | inter | 13px | 400 | 24px | normal |
| Code | plexMono | 13px | 400 | 24px | normal |
| Caption | inter | 12px | 500 | 20px | normal |
| Caption | inter | 12px | 400 | 16px | normal |
| Caption | plexMono | 12px | 400 | 24px | normal |
| Caption | plexMono | 12px | 600 | 16px | 1.2px |
| Caption | plexMono | 12px | 500 | 16px | normal |


## Spacing Scale

`1px` ┬╖ `2px` ┬╖ `4px` ┬╖ `6px` ┬╖ `8px` ┬╖ `10px` ┬╖ `12px` ┬╖ `16px` ┬╖ `20px` ┬╖ `24px` ┬╖ `28px` ┬╖ `32px` ┬╖ `36px` ┬╖ `40px` ┬╖ `44px` ┬╖ `48px` ┬╖ `57px` ┬╖ `64px` ┬╖ `96px` ┬╖ `160px`

*Based on a **4px grid** system.*


## Borders, Radii & Effects

**Border radius**: `4px`, `8px`, `12px`, `16px`, `24px`, `32px`, `9999px`

**Shadows**:
- `rgba(0, 13, 13, 0.08) 0px 0px 0px 1px inset`
- `rgba(255, 255, 255, 0.1) 0px 0px 0px 1px inset`
- `rgba(0, 0, 0, 0.1) 0px 20px 25px -5px, rgba(0, 0, 0, 0.1) 0px 8px 10px -6px`
- `rgba(0, 0, 20, 0.05) 0px 0px 0px 1px`
- `rgba(255, 255, 255, 0.2) 0px 0px 0px 1px inset, rgba(0, 10, 20, 0.1) 0px 0px 0px 1px, rgba(0, 0, ...`
- `rgba(0, 10, 20, 0.1) 0px 0px 0px 1px inset`

**Effects**:
- `backdrop-filter: blur(12px)`
- `backdrop-filter: blur(8px)`
- `backdrop-filter: brightness(1.5)`
- `backdrop-filter: grayscale(1)`
- `backdrop-filter: contrast(1.5)`
- `backdrop-filter: saturate(2)`


## Component Patterns

### Buttons

- **"v4.3"** (ghost)
  - `background: rgba(0, 0, 20, 0.05)` ┬╖ `color: #030712`
  - `font: 12px / 500`
  - `padding: 2px 6px 2px 10px` ┬╖ `radius: 16px`

- **"Quick search"** (ghost)
  - `background: transparent` ┬╖ `color: rgba(4, 8, 18, 0.5)`
  - `font: 14px / 400`
  - `padding: 8px 16px` ┬╖ `radius: 9999px`

- **"Become a sponsor"** (filled)
  - `background: #000000` ┬╖ `color: #ffffff`
  - `font: 14px / 600`
  - `padding: 8px 16px` ┬╖ `radius: 32px`

- **"Check availability"** (filled)
  - `background: #f6339a` ┬╖ `color: #ffffff`
  - `font: 14px / 700`
  - `padding: 8px 12px` ┬╖ `radius: 8px`

- **"index.html"** (filled)
  - `background: rgba(255, 255, 255, 0.1)` ┬╖ `color: #ffffff`
  - `font: 12px / 400`
  - `padding: 4px 8px` ┬╖ `radius: 4px`

- **"app.css"** (ghost)
  - `background: transparent` ┬╖ `color: #ffffff`
  - `font: 12px / 400`
  - `padding: 4px 8px` ┬╖ `radius: 4px`


## Layout Patterns

### Grid
- `<div>` ΓÇö 3 columns, gap `normal`
- `<button>` ΓÇö 3 columns, gap `4px`
- `<div>` ΓÇö 4 columns, gap `40px`
- `<a>` ΓÇö 1 columns, gap `normal`

### Flexbox
- `<div>`, row, justify: space-between, align: center, gap: 32px, (3 children)
- `<div>`, row, align: flex-end, (7 children)
- `<div>`, column, gap: 8px, (3 children)


## Assets

37 images, 10 SVG icons detected.

- `190px ├ù 192px` (no alt) ΓÇö `https://tailwindcss.com/_next/static/media/cover.0g8-x6e87bh6a.png`
- `372px ├ù 160px` (no alt) ΓÇö `https://tailwindcss.com/_next/static/media/responsive-1.10chodfonif...`
- `182px ├ù 160px` (no alt) ΓÇö `https://tailwindcss.com/_next/static/media/responsive-2.0cdenvbjn04...`
- `182px ├ù 160px` (no alt) ΓÇö `https://tailwindcss.com/_next/static/media/responsive-3.00654hu_8u-...`
- `256px ├ù 256px` (no alt) ΓÇö `https://tailwindcss.com/_next/static/media/filters.17z4w2mm8xht2.png`
- `375px ├ù 621px` (no alt) ΓÇö `https://tailwindcss.com/_next/static/media/dark-mode.light.0tx34lu8...`
- `375px ├ù 621px` (no alt) ΓÇö `https://tailwindcss.com/_next/static/media/dark-mode.dark.11szx9d7s...`
- `192px ├ù 392px` (no alt) ΓÇö `https://tailwindcss.com/_next/static/media/css-grid-1.0c8bc8q87-upx...`
- `192px ├ù 192px` (no alt) ΓÇö `https://tailwindcss.com/_next/static/media/css-grid-2.15b-x2ty8.g~z...`
- `192px ├ù 192px` (no alt) ΓÇö `https://tailwindcss.com/_next/static/media/css-grid-3.08b3dk7gkiatg...`
- `392px ├ù 196px` (no alt) ΓÇö `https://tailwindcss.com/_next/static/media/css-grid-4.0iikpmqc8shsg...`
- `48px ├ù 48px` (no alt) ΓÇö `https://tailwindcss.com/_next/static/media/avatar-4.147155nkju-ki.png`
- ... and 25 more
