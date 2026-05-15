# Design Style Guide: Tailwind CSS - Rapidly build modern websites without ever leaving your HTML.

> Source: https://tailwindcss.com
> Extracted: 2026-05-15 16:41
> Viewport: 1280x720 | Full page height: 11724px

## Design Philosophy

- Light-themed interface
- Dual typeface system: plexMono, inter
- Glassmorphism / backdrop blur effects
- Generous whitespace with large section padding

---

## CSS Custom Properties

| Variable | Value |
|----------|-------|
| `--lightningcss-dark` | `` |
| `--lightningcss-light` | `initial` |


## Color Palette

### Backgrounds
- `rgb(255, 255, 255)` — near-white
- `oklab(0.129999 -0.00404751 -0.027702 / 0.05)`
- `oklab(0.129999 -0.00404751 -0.027702 / 0.02)`
- `oklab(0.745991 -0.0970495 -0.127188 / 0.1)`
- `rgb(0, 0, 0)` — near-black
- `lab(1.90334 0.278696 -5.48866)`
- `oklab(0.999994 0.0000455678 0.0000200868 / 0.2)`
- `oklab(0.999994 0.0000455678 0.0000200868 / 0.1)`
- `oklab(0 0 0 / 0.05)`
- `oklab(0.129999 -0.00404751 -0.027702 / 0.025)`
- `oklab(0.129999 -0.00404751 -0.027702 / 0.2)`
- `lab(56.9303 76.8162 -8.07021)`
- `oklab(0.128998 -0.0038857 -0.0418156 / 0.2)`
- `oklab(0.999994 0.0000455678 0.0000200868 / 0.15)`
- `lab(70.687 -23.6078 -45.9483)`

### Text Colors
- `rgb(0, 0, 0)` — near-black
- `lab(1.90334 0.278696 -5.48866)`
- `lab(47.7841 -0.393182 -10.0268)`
- `lab(35.164 -9.57692 -34.4068)`
- `oklab(0 0 0 / 0.2)`
- `lab(35.6337 -1.58697 -10.8425)`
- `lab(63.3038 -18.433 -51.0407)`
- `rgb(255, 255, 255)` — near-white
- `oklab(0.129999 -0.00404751 -0.027702 / 0.5)`
- `lab(65.5349 -2.25151 -14.5072)`
- `lab(64.5597 64.3615 -12.7988)`
- `lab(84.7652 -1.94535 -7.93337)`
- `lab(80.3307 -20.2945 -31.385)`
- `lab(98.1434 -0.369519 -1.05966)`
- `lab(56.9303 76.8162 -8.07021)`

### Border Colors
- `oklab(0 0 0 / 0.05)`
- `oklab(0.827994 -0.0708814 -0.0854034 / 0.6)`
- `rgb(0, 0, 0) oklab(0 0 0 / 0.05)`
- `oklab(0.129999 -0.00404751 -0.027702 / 0.05)`
- `oklab(0.129999 -0.00404751 -0.027702 / 0.2)`
- `rgb(255, 255, 255) rgb(255, 255, 255) oklab(0.999994 0.0000455678 0.0000200868 / 0.05)`


## Typography

| Role | Font | Size | Weight | Line Height | Letter Spacing |
|------|------|------|--------|-------------|----------------|
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
| Body small | inter | 14px | 400 | 24px | normal |
| Body small | inter | 14px | 600 | 24px | normal |
| Body small | inter | 14px | 500 | 24px | normal |
| Body small | inter | 14px | 700 | 24px | normal |
| Code | plexMono | 14px | 500 | 28px | normal |
| Body small | inter | 13px | 400 | 24px | normal |
| Code | plexMono | 13px | 400 | 24px | normal |
| Caption / Small | inter | 12px | 500 | 20px | normal |
| Caption / Small | inter | 12px | 400 | 16px | normal |
| Caption / Small | plexMono | 12px | 400 | 24px | normal |
| Caption / Small | plexMono | 12px | 600 | 16px | 1.2px |
| Caption / Small | plexMono | 12px | 500 | 16px | normal |

**Font families in use**: inter, plexMono


## Spacing Scale

`1px` · `2px` · `4px` · `6px` · `8px` · `10px` · `12px` · `16px` · `20px` · `24px` · `28px` · `32px` · `36px` · `40px` · `44px` · `48px` · `57px` · `64px` · `96px` · `160px`

*Appears to use a **4px base grid** system.*


## Borders, Radii & Effects

**Border radius values**: `3.35544e+07px`, `0px 0px 16px`, `0px 16px 0px 0px`, `4px`, `8px`, `12px`, `16px`, `16px 0px 0px 16px`, `16px 16px 0px 0px`, `24px`

**Border widths**: `0px 0px 0px 1px`, `0px 0px 1px`, `0px 1px`, `0px 1px 0px 0px`, `1px`

**Box shadows**:
- `rgba(0, 0, 0, 0) 0px 0px 0px 0px, oklab(0.129999 -0.00404751 -0.027702 / 0.08) 0px 0px 0px 1px inset, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px`
- `rgba(0, 0, 0, 0) 0px 0px 0px 0px, oklab(0.999994 0.0000455678 0.0000200868 / 0.1) 0px 0px 0px 1px inset, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px`
- `rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0.1) 0px 20px 25px -5px, rgba(0, 0, 0, 0.1) 0px 8px 10px -6px`
- `rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, oklab(0.129999 -0.00404751 -0.027702 / 0.05) 0px 0px 0px 1px, rgba(0, 0, 0, 0) 0px 0px 0px 0px`
- `rgba(0, 0, 0, 0) 0px 0px 0px 0px, oklab(0.999994 0.0000455678 0.0000200868 / 0.2) 0px 0px 0px 1px inset, rgba(0, 0, 0, 0) 0px 0px 0px 0px, oklab(0.129999 -0.00404751 -0.027702 / 0.1) 0px 0px 0px 1px, rgba(0, 0, 0, 0.1) 0px 1px 3px 0px, rgba(0, 0, 0, 0.1) 0px 1px 2px -1px`
- `rgba(0, 0, 0, 0) 0px 0px 0px 0px, oklab(0.129999 -0.00404751 -0.027702 / 0.1) 0px 0px 0px 1px inset, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px`
- `rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0.1) 0px 1px 3px 0px, rgba(0, 0, 0, 0.1) 0px 1px 2px -1px`
- `rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, oklab(0.745991 -0.0970495 -0.127188 / 0.5) 0px 10px 15px -3px, oklab(0.745991 -0.0970495 -0.127188 / 0.5) 0px 4px 6px -4px`

**Visual effects**:
- `backdrop-filter: blur(12px)`
- `filter: url("#filter0_f_457_1608")`
- `backdrop-filter: blur(8px)`
- `backdrop-filter: brightness(1.5)`
- `backdrop-filter: grayscale(1)`
- `backdrop-filter: contrast(1.5)`
- `backdrop-filter: saturate(2)`
- `backdrop-filter: sepia(1)`


## Component Patterns

### Buttons

- **"v4.3"**
  - Background: `oklab(0.129999 -0.00404751 -0.027702 / 0.05)`
  - Color: `lab(1.90334 0.278696 -5.48866)`
  - Font: 12px 500
  - Padding: `2px 6px 2px 10px`
  - Border radius: `16px`
  - Border: `0px solid lab(1.90334 0.278696 -5.48866)`

- **"⌘KCtrl K"**
  - Background: `oklab(0.129999 -0.00404751 -0.027702 / 0.02)`
  - Color: `rgb(0, 0, 0)`
  - Font: 16px 400
  - Padding: `4px 8px`
  - Border radius: `3.35544e+07px`
  - Border: `0px solid rgb(0, 0, 0)`

- **"Quick search⌘KCtrl K"**
  - Background: `rgba(0, 0, 0, 0)`
  - Color: `oklab(0.129999 -0.00404751 -0.027702 / 0.5)`
  - Font: 14px 400
  - Padding: `8px 16px`
  - Border radius: `3.35544e+07px`
  - Border: `0px solid oklab(0.129999 -0.00404751 -0.027702 / 0.5)`

- **"Become a sponsor"**
  - Background: `rgb(0, 0, 0)`
  - Color: `rgb(255, 255, 255)`
  - Font: 14px 600
  - Padding: `8px 16px`
  - Border radius: `32px`
  - Border: `0px solid rgb(255, 255, 255)`

- **"Check availability"**
  - Background: `lab(56.9303 76.8162 -8.07021)`
  - Color: `rgb(255, 255, 255)`
  - Font: 14px 700
  - Padding: `8px 12px`
  - Border radius: `8px`
  - Border: `0px solid rgb(255, 255, 255)`

- **"index.html"**
  - Background: `oklab(0.999994 0.0000455678 0.0000200868 / 0.1)`
  - Color: `rgb(255, 255, 255)`
  - Font: 12px 400
  - Padding: `4px 8px`
  - Border radius: `4px`
  - Border: `0px solid rgb(255, 255, 255)`

- **"app.css"**
  - Background: `rgba(0, 0, 0, 0)`
  - Color: `rgb(255, 255, 255)`
  - Font: 12px 400
  - Padding: `4px 8px`
  - Border radius: `4px`
  - Border: `0px solid rgb(255, 255, 255)`


## Layout Patterns

### CSS Grid Usage

- `<div>`: columns `40px 1200px 40px`, gap `normal`
- `<div>`: columns `1200px`, gap `160px`
- `<button>`: columns `14px 234.25px 31.75px`, gap `4px`
- `<div>`: columns `400px 400px 400px`, gap `normal`
- `<div>`: columns `270px 270px 270px 270px`, gap `40px`
- `<a>`: columns `254px`, gap `normal`

### Flexbox Usage

- `<div>`: row, justify: space-between, align: center, gap: 32px (3 children)
- `<div>`: row, align: center, gap: 16px (2 children)
- `<div>`: column (2 children)


## Assets Detected

37 images and 10 inline SVG icons detected.

### Images

| Source | Alt | Dimensions |
|--------|-----|------------|
| `https://tailwindcss.com/_next/static/media/cover.0g8-x6e87bh6a.png` |  | 190px × 192px |
| `https://tailwindcss.com/_next/static/media/responsive-1.10chodfonif1e.png` |  | 372px × 160px |
| `https://tailwindcss.com/_next/static/media/responsive-2.0cdenvbjn04n3.png` |  | 182px × 160px |
| `https://tailwindcss.com/_next/static/media/responsive-3.00654hu_8u-c4.png` |  | 182px × 160px |
| `https://tailwindcss.com/_next/static/media/filters.17z4w2mm8xht2.png` |  | 256px × 256px |
| `https://tailwindcss.com/_next/static/media/dark-mode.light.0tx34lu8jwt_1.png` |  | 375px × 621px |
| `https://tailwindcss.com/_next/static/media/dark-mode.dark.11szx9d7s4zjz.png` |  | 375px × 621px |
| `https://tailwindcss.com/_next/static/media/css-grid-1.0c8bc8q87-upx.png` |  | 192px × 392px |
| `https://tailwindcss.com/_next/static/media/css-grid-2.15b-x2ty8.g~z.png` |  | 192px × 192px |
| `https://tailwindcss.com/_next/static/media/css-grid-3.08b3dk7gkiatg.png` |  | 192px × 192px |
| `https://tailwindcss.com/_next/static/media/css-grid-4.0iikpmqc8shsg.png` |  | 392px × 196px |
| `https://tailwindcss.com/_next/static/media/avatar-4.147155nkju-ki.png` |  | 48px × 48px |
| `https://tailwindcss.com/_next/static/media/avatar-5.0hg2xy51~_xab.png` |  | 48px × 48px |
| `https://tailwindcss.com/_next/static/media/avatar-6.03.hh~61qqypr.png` |  | 48px × 48px |
| `https://tailwindcss.com/_next/static/media/avatar-7.0og44ub0nz8ek.png` |  | 48px × 48px |
| `https://tailwindcss.com/_next/static/media/avatar-1.15~cxxh-ptz0r.png` |  | 48px × 48px |
| `https://tailwindcss.com/_next/static/media/avatar-2.12imlx8.m5il..png` |  | 48px × 48px |
| `https://tailwindcss.com/_next/static/media/avatar-3.0co4yvnojd00m.png` |  | 48px × 48px |
| `https://tailwindcss.com/_next/static/media/3d-transforms.02bsrv~jiqeb9.jpeg` |  | 328px × 328px |
| `https://tailwindcss.com/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fopenai.0e...` | OpenAI | 233px × 197px |

### SVG Icons (10 found)

- (icon) — 159px × 20px
- (icon) — 16px × 16px
- (icon) — 16px × 16px
- (icon) — 5px × 5px
- (icon) — 5px × 5px
- (icon) — 5px × 5px
- (icon) — 5px × 5px
- (icon) — 20px × 20px
- (icon) — 16px × 16px
- (icon) — 10px × 10px
