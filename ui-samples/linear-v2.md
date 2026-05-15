

OK Converted to Markdown (1081 tokens) via ui (design style guide (markdown) via
Playwright)
# Design Style Guide: Linear ΓÇô The system for product development

> Source: https://linear.app
> Extracted: 2026-05-15 17:03
> Viewport: 1280x720 | Full page: 10314px

## Design Philosophy

- **Mixed theme** ΓÇö uses both light and dark surfaces
- **Dual typeface** ΓÇö Inter Variable (UI) + Berkeley Mono (code/accent)
- **Pill-shaped elements** ΓÇö fully rounded buttons/badges
- **Glassmorphism** ΓÇö backdrop blur effects for depth
- **Generous whitespace** ΓÇö large section gaps for breathing room
- **Accent color** ΓÇö `#eb5757` used for interactive elements

---

## Color Palette

### Backgrounds

**Dark / Base**
- `#0f1011`
- `#000000`
- `#23252a`
- `#08090a`
- `#090a0b`
- `#101112`

**Light / Surface**
- `#e5e5e6`

**Vibrant / Accent**
- `#6366f1`
- `#eb5757`
- `#8b5cf6`

**Semi-transparent**
- `rgba(255, 255, 255, 0.05)` (used 81x)
- `rgba(255, 255, 255, 0.02)` (used 20x)
- `rgba(255, 255, 255, 0.03)` (used 7x)
- `rgba(255, 255, 255, 0.08)`
- `rgba(255, 255, 255, 0.01)`
- `rgba(94, 107, 208, 0.15)`

### Text

**Dark / Base**
- `#08090a`

**Light / Surface**
- `#f7f8f8` (used 873x)
- `#62666d` (used 322x)
- `#d0d6e0` (used 115x)
- `#ffffff` (used 99x)
- `#8a8f98` (used 75x)
- `#e2e4e7`

**Vibrant / Accent**
- `#6d78d5`

### Borders

**Dark / Base**
- `#383b3f`
- `#23252a`
- `#24282c`
- `#323334`

**Light / Surface**
- `#f7f8f8` (used 12x)
- `#e5e5e6`

**Semi-transparent**
- `rgba(255, 255, 255, 0.05)` (used 55x)
- `rgba(255, 255, 255, 0.08)` (used 20x)
- `rgba(255, 255, 255, 0.1)`
- `rgba(255, 255, 255, 0.12)`

**Primary accent**: `#eb5757`


## Typography

**Font stack**: Inter Variable, Berkeley Mono

| Role | Font | Size | Weight | Line Height | Tracking |
|------|------|------|--------|-------------|----------|
| Display / H1 | Inter Variable | 64px | 510 | 64px | -1.408px |
| Display / H1 | Inter Variable | 40px | 510 | 44px | -0.88px |
| H3 | Inter Variable | 20px | 590 | 26.6px | -0.24px |
| Body | Inter Variable | 20px | 400 | 26.6px | -0.24px |
| Body | Inter Variable | 16px | 400 | 24px | normal |
| H4-H6 | Inter Variable | 16px | 590 | 24px | normal |
| Body | Inter Variable | 16px | 510 | 24px | normal |
| Body | Inter Variable | 15px | 400 | 24px | -0.165px |
| Body | Inter Variable | 15px | 510 | 24px | -0.165px |
| Body | Inter Variable | 15px | 590 | 24px | -0.165px |
| Body | Inter Variable | 15px | 300 | 22px | -0.165px |
| Body Small | Inter Variable | 14px | 590 | 21px | -0.182px |
| Body Small | Inter Variable | 14px | 400 | 21px | -0.182px |
| Body Small | Inter Variable | 14px | 510 | 21px | -0.182px |
| Body Small | Berkeley Mono | 14px | 400 | 21px | normal |
| Body Small | Inter Variable | 13.3333px | 400 | normal | normal |
| Body Small | Inter Variable | 13px | 400 | 19.5px | normal |
| Body Small | Inter Variable | 13px | 510 | 32px | normal |
| Body Small | Berkeley Mono | 13px | 400 | 19.5px | normal |
| Code | Berkeley Mono | 12.25px | 400 | 15.925px | -0.182px |
| Caption | Inter Variable | 12px | 510 | 16.8px | normal |
| Caption | Inter Variable | 12px | 400 | 16.8px | normal |
| Caption | Inter Variable | 12px | 590 | 16.8px | normal |
| Caption | Berkeley Mono | 12px | 400 | 16.8px | normal |
| Caption | Inter Variable | 11px | 510 | 15.4px | normal |
| Caption | Inter Variable | 10px | 400 | 15px | -0.15px |
| Caption | Inter Variable | 10px | 510 | 15px | normal |


## Spacing Scale

`1px` ┬╖ `2px` ┬╖ `3px` ┬╖ `4px` ┬╖ `5px` ┬╖ `6px` ┬╖ `7px` ┬╖ `8px` ┬╖ `9px` ┬╖ `10px` ┬╖ `11px` ┬╖ `12px` ┬╖ `14px` ┬╖ `15px` ┬╖ `16px` ┬╖ `17px` ┬╖ `19px` ┬╖ `20px` ┬╖ `21px` ┬╖ `22px` ┬╖ `23px` ┬╖ `24px` ┬╖ `26px` ┬╖ `27px` ┬╖ `28px`


## Borders, Radii & Effects

**Border radius**: `50%`, `1px`, `2px`, `4px`, `6px`, `7px`, `8px`, `12px`

**Shadows**:
- `rgba(0, 0, 0, 0) 0px 8px 2px 0px, rgba(0, 0, 0, 0.01) 0px 5px 2px 0px, rgba(0, 0, 0, 0.04) 0px 3p...`
- `rgba(94, 106, 210, 0) 0px 0px 0px 9.97333px`
- `rgba(0, 0, 0, 0.1) 0px 0px 0px 2px`
- `rgba(0, 0, 0, 0.2) 0px 0px 0px 1px`
- `rgb(35, 37, 42) 0px 0px 0px 1px inset`
- `rgba(0, 0, 0, 0.4) 0px 2px 4px 0px`

**Effects**:
- `backdrop-filter: blur(20px)`
- `filter: blur(0px)`
- `filter: brightness(1)`


## Component Patterns

### Buttons

- **"Product"** (ghost)
  - `background: transparent` ┬╖ `color: #8a8f98`
  - `font: 13px / 400`
  - `padding: 0px 12px` ┬╖ `radius: 9999px`

- **"Sign up"** (filled)
  - `background: #e5e5e6` ┬╖ `color: #08090a`
  - `font: 13px / 510`
  - `padding: 0px 12px` ┬╖ `radius: 9999px`

### Inputs

- **textarea**: bg `rgba(255, 255, 255, 0.02)`, radius `6px`, padding `12px 14px`
- **text**: bg `transparent`, radius `0px`, padding `1px 32px`
- **input**: bg `#3b3b3b`, radius `0px`, padding `0px`

### Navigation

- **9 links**: Customers, Pricing, Now, Contact, Docs, Open app
  - Layout: `flex`, gap: `normal`


## Layout Patterns

### Grid
- `<li>` ΓÇö 1 columns, gap `normal`

### Flexbox
- `<div>`, column, (3 children)
- `<ul>`, row, align: center, gap: 8px, (3 children)
- `<li>`, row, align: center, (5 children)
- `<main>`, column, (2 children)
- `<div>`, row, justify: space-between, align: baseline, (2 children)
- `<header>`, row, justify: space-between, align: center, (2 children)
- `<div>`, row, align: center, gap: 8px, (2 children)


## Assets

27 images, 29 SVG icons detected.

- `1280px ├ù 748px` (no alt) ΓÇö `https://linear.app/cdn-cgi/imagedelivery/fO02fVwohEs9s9UHFwon6A/c7b...`
- `1920px ├ù 891px` (no alt) ΓÇö `https://linear.app/cdn-cgi/imagedelivery/fO02fVwohEs9s9UHFwon6A/660...`
- `1280px ├ù 715px` (no alt) ΓÇö `https://linear.app/cdn-cgi/imagedelivery/fO02fVwohEs9s9UHFwon6A/c7f...`
- `14px ├ù 14px` Avatar of Karri ΓÇö `https://webassets.linear.app/images/ornj730p/production/f79251b06e9...`
- `14px ├ù 14px` Avatar of Karri ΓÇö `https://webassets.linear.app/images/ornj730p/production/f79251b06e9...`
- `14px ├ù 14px` (no alt) ΓÇö `https://linear.app/cdn-cgi/imagedelivery/fO02fVwohEs9s9UHFwon6A/f28...`
- `14px ├ù 14px` (no alt) ΓÇö `https://linear.app/cdn-cgi/imagedelivery/fO02fVwohEs9s9UHFwon6A/f9e...`
- `16px ├ù 16px` (no alt) ΓÇö `https://linear.app/cdn-cgi/imagedelivery/fO02fVwohEs9s9UHFwon6A/f9e...`
- `16px ├ù 16px` (no alt) ΓÇö `https://linear.app/cdn-cgi/imagedelivery/fO02fVwohEs9s9UHFwon6A/f28...`
- `16px ├ù 16px` GitHub Copilot ΓÇö `https://linear.app/cdn-cgi/imagedelivery/fO02fVwohEs9s9UHFwon6A/f9e...`
- `16px ├ù 16px` (no alt) ΓÇö `https://linear.app/cdn-cgi/imagedelivery/fO02fVwohEs9s9UHFwon6A/086...`
- `16px ├ù 16px` (no alt) ΓÇö `https://linear.app/cdn-cgi/imagedelivery/fO02fVwohEs9s9UHFwon6A/302...`
- ... and 15 more

**Named SVG icons**: Linear, Linear logo
