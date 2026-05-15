# Design Style Guide: Linear – The system for product development

> Source: https://linear.app
> Extracted: 2026-05-15 16:41
> Viewport: 1280x720 | Full page height: 10314px

## Design Philosophy

- Mixed light/dark palette
- Dual typeface system: Berkeley Mono, Inter Variable
- Pill-shaped elements (fully rounded corners)
- Glassmorphism / backdrop blur effects
- Generous whitespace with large section padding

---

## Color Palette

### Backgrounds
- `rgb(8, 9, 10)` — near-black
- `rgb(35, 37, 42)` — dark
- `rgb(229, 229, 230)` — light
- `rgba(94, 106, 210, 0.15)`
- `rgb(9, 10, 11)` — near-black
- `rgb(16, 17, 18)` — near-black
- `rgb(18, 20, 20)` — near-black
- `rgba(255, 255, 255, 0.02)` — near-white
- `rgba(255, 255, 255, 0.04)` — near-white
- `rgb(18, 19, 20)` — near-black
- `rgba(255, 255, 255, 0.05)` — near-white
- `rgba(255, 255, 255, 0.01)` — near-white
- `rgb(22, 23, 24)` — dark
- `rgba(255, 255, 255, 0.03)` — near-white
- `rgb(0, 0, 0)` — near-black

### Text Colors
- `rgb(247, 248, 248)` — near-white
- `rgb(138, 143, 152)` — light gray
- `rgb(8, 9, 10)` — near-black
- `rgb(208, 214, 224)` — light
- `rgb(98, 102, 109)` — neutral gray
- `rgb(255, 255, 255)` — near-white
- `rgb(226, 228, 230)` — light
- `rgb(226, 228, 231)` — light
- `rgb(109, 120, 213)`

### Border Colors
- `rgb(247, 248, 248) rgb(247, 248, 248) rgba(255, 255, 255, 0.08)`
- `rgb(229, 229, 230)`
- `rgba(255, 255, 255, 0.08)`
- `rgb(36, 40, 44)`
- `rgb(247, 248, 248) rgb(247, 248, 248) rgba(255, 255, 255, 0.05)`
- `rgba(255, 255, 255, 0.05)`
- `rgb(247, 248, 248) rgb(247, 248, 248) rgb(247, 248, 248) rgba(255, 255, 255, 0.05)`
- `rgb(35, 37, 42)`
- `rgb(50, 51, 52)`
- `rgb(56, 59, 63)`

**Likely accent color**: `rgb(6, 182, 212)`


## Typography

| Role | Font | Size | Weight | Line Height | Letter Spacing |
|------|------|------|--------|-------------|----------------|
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
| Body small | Inter Variable | 14px | 590 | 21px | -0.182px |
| Body small | Inter Variable | 14px | 400 | 21px | -0.182px |
| Body small | Inter Variable | 14px | 510 | 21px | -0.182px |
| Body small | Berkeley Mono | 14px | 400 | 21px | normal |
| Body small | Inter Variable | 13.3333px | 400 | normal | normal |
| Body small | Inter Variable | 13px | 400 | 19.5px | normal |
| Body small | Inter Variable | 13px | 510 | 32px | normal |
| Body small | Berkeley Mono | 13px | 400 | 19.5px | normal |
| Code | Berkeley Mono | 12.25px | 400 | 15.925px | -0.182px |
| Caption / Small | Inter Variable | 12px | 510 | 16.8px | normal |
| Caption / Small | Inter Variable | 12px | 400 | 16.8px | normal |
| Caption / Small | Inter Variable | 12px | 590 | 16.8px | normal |
| Caption / Small | Berkeley Mono | 12px | 400 | 16.8px | normal |
| Caption / Small | Inter Variable | 11px | 510 | 15.4px | normal |
| Caption / Small | Inter Variable | 10px | 400 | 15px | -0.15px |
| Caption / Small | Inter Variable | 10px | 510 | 15px | normal |

**Font families in use**: Berkeley Mono, Inter Variable


## Spacing Scale

`1px` · `1.225px` · `2px` · `3px` · `4px` · `5px` · `6px` · `7px` · `8px` · `9px` · `10px` · `11px` · `12px` · `14px` · `15px` · `16px` · `17px` · `19px` · `19.2031px` · `20px`


## Borders, Radii & Effects

**Border radius values**: `0px 4px 4px 0px`, `50%`, `1px`, `2px`, `4px`, `4px 0px 0px 4px`, `6px`, `7px`, `8px`, `12px 12px 0px 0px`

**Border widths**: `0px 0px 0px 1px`, `0px 0px 1px`, `0px 1px 0px 0px`, `1px`

**Box shadows**:
- `rgba(0, 0, 0, 0) 0px 8px 2px 0px, rgba(0, 0, 0, 0.01) 0px 5px 2px 0px, rgba(0, 0, 0, 0.04) 0px 3px 2px 0px, rgba(0, 0, 0, 0.07) 0px 1px 1px 0px, rgba(0, 0, 0, 0.08) 0px 0px 1px 0px`
- `rgba(94, 106, 210, 0.004) 0px 0px 0px 9.77857px`
- `rgba(0, 0, 0, 0.1) 0px 0px 0px 2px`
- `rgba(0, 0, 0, 0.2) 0px 0px 0px 1px`
- `rgb(35, 37, 42) 0px 0px 0px 1px inset`
- `rgba(0, 0, 0, 0.4) 0px 2px 4px 0px`
- `rgba(0, 0, 0, 0.03) 0px 1.2px 0px 0px`
- `rgba(0, 0, 0, 0.4) 0px 1px 0px 0px`

**Visual effects**:
- `backdrop-filter: blur(20px)`
- `filter: blur(0px)`
- `filter: url("#filter0_d_3072_54146")`
- `filter: url("#filter0_d_3357_5865")`
- `filter: url("#filter1_d_3357_5865")`
- `filter: url("#filter2_d_3357_5865")`
- `filter: url("#filter3_d_3357_5865")`
- `filter: url("#filter4_d_3357_5865")`


## Component Patterns

### Buttons

- **""**
  - Background: `rgba(0, 0, 0, 0)`
  - Color: `rgb(247, 248, 248)`
  - Font: 16px 400
  - Padding: `0px 8px`
  - Border radius: `6px`
  - Border: `0px none rgb(247, 248, 248)`

- **"Product"**
  - Background: `rgba(0, 0, 0, 0)`
  - Color: `rgb(138, 143, 152)`
  - Font: 13px 400
  - Padding: `0px 12px`
  - Border radius: `9999px`
  - Border: `0px none rgb(138, 143, 152)`

- **"Sign up"**
  - Background: `rgb(229, 229, 230)`
  - Color: `rgb(8, 9, 10)`
  - Font: 13px 510
  - Padding: `0px 12px`
  - Border radius: `9999px`
  - Border: `1px solid rgb(229, 229, 230)`

- **"Linear"**
  - Background: `rgba(0, 0, 0, 0)`
  - Color: `rgb(255, 255, 255)`
  - Font: 13.3333px 400
  - Padding: `0px 4px`
  - Border radius: `4px`
  - Border: `0px none rgb(255, 255, 255)`

### Form Inputs

- **textarea** input
  - Background: `rgba(255, 255, 255, 0.02)`
  - Font size: `13.3333px`
  - Padding: `12px 14px`
  - Border radius: `6px`

- **text** input
  - Background: `rgba(0, 0, 0, 0)`
  - Font size: `16px`
  - Padding: `1px 32px`
  - Border radius: `0px`

- **input** input
  - Background: `rgb(59, 59, 59)`
  - Font size: `13.3333px`
  - Padding: `0px`
  - Border radius: `0px`

### Navigation

- **Nav** with 9 links: , Customers, Pricing, Now, Contact, Docs
  - Layout: `flex`, gap: `normal`

- **Nav** with 0 links: 
  - Layout: `block`, gap: `normal`


## Layout Patterns

### CSS Grid Usage

- `<li>`: columns `72.1094px`, gap `normal`
- `<li>`: columns `88.6562px`, gap `normal`
- `<li>`: columns `90.7031px`, gap `normal`
- `<li>`: columns `66.7031px`, gap `normal`
- `<li>`: columns `52px`, gap `normal`
- `<li>`: columns `72.2812px`, gap `normal`
- `<li>`: columns `61.6094px`, gap `normal`
- `<li>`: columns `72.9219px`, gap `normal`

### Flexbox Usage

- `<div>`: column (3 children)
- `<main>`: column (2 children)
- `<div>`: row, justify: space-between, align: baseline (2 children)
- `<div>`: row, align: center, gap: 12px (3 children)
- `<header>`: row, justify: space-between, align: center (2 children)


## Assets Detected

27 images and 29 inline SVG icons detected.

### Images

| Source | Alt | Dimensions |
|--------|-----|------------|
| `https://linear.app/cdn-cgi/imagedelivery/fO02fVwohEs9s9UHFwon6A/c7b144b7-4ef0...` |  | 1280px × 748px |
| `https://linear.app/cdn-cgi/imagedelivery/fO02fVwohEs9s9UHFwon6A/6600ca96-e49b...` |  | 1920px × 891px |
| `https://linear.app/cdn-cgi/imagedelivery/fO02fVwohEs9s9UHFwon6A/c7fa8f5f-d439...` |  | 1280px × 715px |
| `https://webassets.linear.app/images/ornj730p/production/f79251b06e9edeeacbf28...` | Avatar of Karri | 14px × 14px |
| `https://webassets.linear.app/images/ornj730p/production/f79251b06e9edeeacbf28...` | Avatar of Karri | 14px × 14px |
| `https://linear.app/cdn-cgi/imagedelivery/fO02fVwohEs9s9UHFwon6A/f28b59f4-538c...` |  | 14px × 14px |
| `https://linear.app/cdn-cgi/imagedelivery/fO02fVwohEs9s9UHFwon6A/f9ed2721-1966...` |  | 14px × 14px |
| `https://linear.app/cdn-cgi/imagedelivery/fO02fVwohEs9s9UHFwon6A/f9ed2721-1966...` |  | 16px × 16px |
| `https://linear.app/cdn-cgi/imagedelivery/fO02fVwohEs9s9UHFwon6A/f28b59f4-538c...` |  | 16px × 16px |
| `https://linear.app/cdn-cgi/imagedelivery/fO02fVwohEs9s9UHFwon6A/f9ed2721-1966...` | GitHub Copilot | 16px × 16px |
| `https://linear.app/cdn-cgi/imagedelivery/fO02fVwohEs9s9UHFwon6A/086b510a-f5da...` |  | 16px × 16px |
| `https://linear.app/cdn-cgi/imagedelivery/fO02fVwohEs9s9UHFwon6A/302b16a5-f9ca...` |  | 16px × 16px |
| `https://linear.app/cdn-cgi/imagedelivery/fO02fVwohEs9s9UHFwon6A/1eb8f8b2-3593...` |  | 16px × 16px |
| `https://linear.app/cdn-cgi/imagedelivery/fO02fVwohEs9s9UHFwon6A/6550520e-9e50...` |  | 16px × 16px |
| `https://linear.app/cdn-cgi/imagedelivery/fO02fVwohEs9s9UHFwon6A/4d3381aa-fb2f...` |  | 16px × 16px |
| `https://linear.app/cdn-cgi/imagedelivery/fO02fVwohEs9s9UHFwon6A/7ea107e7-c1a0...` |  | 16px × 16px |
| `https://linear.app/cdn-cgi/imagedelivery/fO02fVwohEs9s9UHFwon6A/c8aeedda-7726...` | didier | 36px × 36px |
| `https://linear.app/cdn-cgi/imagedelivery/fO02fVwohEs9s9UHFwon6A/580cd9c0-2770...` | lena | 36px × 36px |
| `https://linear.app/cdn-cgi/imagedelivery/fO02fVwohEs9s9UHFwon6A/c8aeedda-7726...` | didier | 36px × 36px |
| `https://linear.app/cdn-cgi/imagedelivery/fO02fVwohEs9s9UHFwon6A/22210a73-581d...` | andreas | 36px × 36px |

### SVG Icons (29 found)

- Linear — 88px × 22px
- Linear logo — 13px × 13px
- (icon) — 16px × 16px
- (icon) — 16px × 16px
- (icon) — 16px × 16px
- (icon) — 14px × 14px
- (icon) — 14px × 14px
- (icon) — 14px × 14px
- (icon) — 14px × 14px
- (icon) — 16px × 16px
- (icon) — 14px × 14px
- (icon) — 14px × 14px
- (icon) — 14px × 14px
- (icon) — 16px × 16px
- (icon) — 14px × 14px
