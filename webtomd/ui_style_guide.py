"""Build a structured design style guide markdown from extracted UI data."""

from __future__ import annotations

import json
import re
from datetime import datetime
from typing import Any

from webtomd.ui_extractor import UIStyleData


def build_style_guide(data: UIStyleData, *, output_format: str = "markdown") -> str:
    """Turn raw UIStyleData into a formatted output.

    output_format: "markdown" (default), "tokens" (JSON design tokens), "html" (visual report)
    """
    if output_format == "tokens":
        return _build_tokens_json(data)
    if output_format == "html":
        return _build_html_report(data)
    return _build_markdown(data)


# ═══════════════════════════════════════════════════════════
#  MARKDOWN OUTPUT
# ═══════════════════════════════════════════════════════════

def _build_markdown(data: UIStyleData) -> str:
    lines: list[str] = []
    _md_header(lines, data)
    _md_philosophy(lines, data)
    _md_css_variables(lines, data)
    _md_color_palette(lines, data)
    _md_typography(lines, data)
    _md_spacing(lines, data)
    _md_borders_effects(lines, data)
    _md_components(lines, data)
    _md_layouts(lines, data)
    _md_images(lines, data)
    return "\n".join(lines)


def _md_header(lines: list[str], data: UIStyleData) -> None:
    title = data.page_title or _domain(data.url)
    lines.append(f"# Design Style Guide: {title}")
    lines.append("")
    lines.append(f"> Source: {data.url}")
    lines.append(f"> Extracted: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"> Viewport: {data.viewport_width}x{data.viewport_height} | Full page: {data.full_page_height}px")
    lines.append("")


def _md_philosophy(lines: list[str], data: UIStyleData) -> None:
    lines.append("## Design Philosophy")
    lines.append("")

    bg_colors = data.colors.get("background", [])
    dark_count = sum(1 for c in bg_colors if _is_dark(c.get("hex", "") if isinstance(c, dict) else c))
    total = max(len(bg_colors), 1)

    if dark_count > total * 0.6:
        lines.append("- **Dark theme** — dark backgrounds dominate the palette")
    elif dark_count < total * 0.3:
        lines.append("- **Light theme** — light/white backgrounds with dark text")
    else:
        lines.append("- **Mixed theme** — uses both light and dark surfaces")

    fonts = _unique_font_families(data.typography)
    if len(fonts) == 1:
        lines.append(f"- **Single typeface** ({fonts[0]}) — unified, cohesive feel")
    elif len(fonts) == 2:
        lines.append(f"- **Dual typeface** — {fonts[0]} (UI) + {fonts[1]} (code/accent)")
    elif fonts:
        lines.append(f"- **{len(fonts)} typefaces** — {', '.join(fonts[:3])}")

    radii = data.borders.get("radius", [])
    if any(r for r in radii if "9999" in r or "100%" in r or ("px" in r and _px(r) and _px(r) > 50)):
        lines.append("- **Pill-shaped elements** — fully rounded buttons/badges")

    if any("blur" in e for e in data.effects):
        lines.append("- **Glassmorphism** — backdrop blur effects for depth")

    spacing = data.spacing
    if spacing and (isinstance(spacing[-1], int) and spacing[-1] >= 64 or
                    (isinstance(spacing[-1], str) and _px(str(spacing[-1])) and _px(str(spacing[-1])) >= 64)):
        lines.append("- **Generous whitespace** — large section gaps for breathing room")

    accent = _find_accent(data.colors)
    if accent:
        lines.append(f"- **Accent color** — `{accent}` used for interactive elements")

    lines.append("")
    lines.append("---")
    lines.append("")


def _md_css_variables(lines: list[str], data: UIStyleData) -> None:
    if not data.css_variables:
        return
    lines.append("## CSS Custom Properties")
    lines.append("")

    color_vars = {}
    spacing_vars = {}
    font_vars = {}
    other_vars = {}

    for name, val in sorted(data.css_variables.items()):
        lower = name.lower()
        if any(k in lower for k in ["color", "bg", "border-color", "accent", "surface", "text-color"]):
            color_vars[name] = val
        elif any(k in lower for k in ["spacing", "gap", "padding", "margin", "size-"]):
            spacing_vars[name] = val
        elif any(k in lower for k in ["font", "typography", "text-"]):
            font_vars[name] = val
        else:
            other_vars[name] = val

    def _write_var_table(title: str, vars_dict: dict) -> None:
        if not vars_dict:
            return
        lines.append(f"### {title}")
        lines.append("")
        lines.append("| Variable | Value |")
        lines.append("|----------|-------|")
        for n, v in sorted(vars_dict.items()):
            val_display = v if len(v) < 80 else v[:77] + "..."
            lines.append(f"| `{n}` | `{val_display}` |")
        lines.append("")

    _write_var_table("Color Tokens", color_vars)
    _write_var_table("Spacing & Size Tokens", spacing_vars)
    _write_var_table("Typography Tokens", font_vars)
    if len(other_vars) <= 30:
        _write_var_table("Other Tokens", other_vars)
    lines.append("")


def _md_color_palette(lines: list[str], data: UIStyleData) -> None:
    lines.append("## Color Palette")
    lines.append("")

    for category, label in [("background", "Backgrounds"), ("text", "Text"), ("border", "Borders")]:
        colors = data.colors.get(category, [])
        if not colors:
            continue

        lines.append(f"### {label}")
        lines.append("")

        grouped = _group_colors_by_role(colors)
        for role, role_colors in grouped.items():
            if role_colors:
                lines.append(f"**{role}**")
                for c in role_colors[:6]:
                    hex_val = c["hex"] if isinstance(c, dict) else c
                    count = c.get("count", 0) if isinstance(c, dict) else 0
                    usage = f" (used {count}x)" if count > 5 else ""
                    lines.append(f"- `{hex_val}`{usage}")
                lines.append("")

    accent = _find_accent(data.colors)
    if accent:
        lines.append(f"**Primary accent**: `{accent}`")
        lines.append("")
    lines.append("")


def _md_typography(lines: list[str], data: UIStyleData) -> None:
    if not data.typography:
        return
    lines.append("## Typography")
    lines.append("")

    fonts = _unique_font_families(data.typography)
    if fonts:
        lines.append(f"**Font stack**: {', '.join(fonts)}")
        lines.append("")

    lines.append("| Role | Font | Size | Weight | Line Height | Tracking |")
    lines.append("|------|------|------|--------|-------------|----------|")

    seen = set()
    for t in data.typography:
        family = _clean_font(t.get("family", ""))
        size = t.get("size", "")
        weight = t.get("weight", "")
        lh = t.get("lineHeight", "")
        ls = t.get("letterSpacing", "normal")
        tag = t.get("sampleTag", "")
        count = t.get("count", 0)

        key = f"{family}|{size}|{weight}"
        if key in seen:
            continue
        seen.add(key)

        if _px(size) is not None and _px(size) == 0:
            continue
        if count < 2 and _px(size) and _px(size) < 10:
            continue

        role = _guess_type_role(tag, size, weight)
        lines.append(f"| {role} | {family} | {size} | {weight} | {lh} | {ls} |")

    lines.append("")
    lines.append("")


def _md_spacing(lines: list[str], data: UIStyleData) -> None:
    if not data.spacing:
        return
    lines.append("## Spacing Scale")
    lines.append("")

    values = [v for v in data.spacing if isinstance(v, (int, float)) and v > 0]
    if not values:
        return

    lines.append(" · ".join(f"`{v}px`" for v in values[:25]))
    lines.append("")

    base = _detect_grid_base(values)
    if base:
        lines.append(f"*Based on a **{base}px grid** system.*")
        lines.append("")
    lines.append("")


def _md_borders_effects(lines: list[str], data: UIStyleData) -> None:
    radii = data.borders.get("radius", [])
    has_content = radii or data.shadows or data.effects
    if not has_content:
        return

    lines.append("## Borders, Radii & Effects")
    lines.append("")

    if radii:
        clean = sorted(set(radii), key=lambda x: _px(x) or 0)[:8]
        lines.append("**Border radius**: " + ", ".join(f"`{r}`" for r in clean))
        lines.append("")

    if data.shadows:
        clean_shadows = [s for s in data.shadows if not s.startswith("rgba(0, 0, 0, 0) 0px")]
        if clean_shadows:
            lines.append("**Shadows**:")
            for s in clean_shadows[:6]:
                short = s if len(s) < 100 else s[:97] + "..."
                lines.append(f"- `{short}`")
            lines.append("")

    if data.effects:
        lines.append("**Effects**:")
        for e in data.effects[:6]:
            lines.append(f"- `{e}`")
        lines.append("")
    lines.append("")


def _md_components(lines: list[str], data: UIStyleData) -> None:
    if not data.components:
        return
    lines.append("## Component Patterns")
    lines.append("")

    buttons = [c for c in data.components if c.get("type") == "button" and c.get("text")]
    inputs = [c for c in data.components if c.get("type") == "input"]
    navs = [c for c in data.components if c.get("type") == "nav"]

    if buttons:
        lines.append("### Buttons")
        lines.append("")
        seen: set[str] = set()
        for btn in buttons[:8]:
            style_key = f"{btn.get('background')}|{btn.get('borderRadius')}"
            if style_key in seen:
                continue
            seen.add(style_key)
            text = btn["text"]
            bg = btn.get("background", "transparent")
            color = btn.get("color", "inherit")

            variant = "ghost"
            if bg != "transparent" and not bg.startswith("rgba(0"):
                variant = "filled"

            lines.append(f"- **\"{text}\"** ({variant})")
            lines.append(f"  - `background: {bg}` · `color: {color}`")
            lines.append(f"  - `font: {btn.get('fontSize', '')} / {btn.get('fontWeight', '')}`")
            lines.append(f"  - `padding: {btn.get('padding', '')}` · `radius: {btn.get('borderRadius', '')}`")
            lines.append("")

    if inputs:
        lines.append("### Inputs")
        lines.append("")
        seen = set()
        for inp in inputs[:5]:
            key = f"{inp.get('background')}|{inp.get('borderRadius')}"
            if key in seen:
                continue
            seen.add(key)
            lines.append(f"- **{inp.get('inputType', 'text')}**: bg `{inp.get('background')}`, radius `{inp.get('borderRadius')}`, padding `{inp.get('padding')}`")
        lines.append("")

    if navs:
        lines.append("### Navigation")
        lines.append("")
        for nav in navs[:3]:
            texts = nav.get("linkTexts", [])
            lines.append(f"- **{nav.get('linkCount', 0)} links**: {', '.join(texts[:6])}")
            lines.append(f"  - Layout: `{nav.get('display', '')}`, gap: `{nav.get('gap', 'auto')}`")
            lines.append("")
    lines.append("")


def _md_layouts(lines: list[str], data: UIStyleData) -> None:
    if not data.layout_patterns:
        return
    lines.append("## Layout Patterns")
    lines.append("")

    grids = [p for p in data.layout_patterns if p.get("type") == "grid"]
    flexes = [p for p in data.layout_patterns if p.get("type") == "flex"]

    if grids:
        lines.append("### Grid")
        seen: set[str] = set()
        for g in grids[:6]:
            cols = g.get("columns", 0)
            gap = g.get("gap", "")
            key = f"{cols}|{gap}"
            if key in seen:
                continue
            seen.add(key)
            lines.append(f"- `<{g.get('tag', 'div')}>` — {cols} columns, gap `{gap}`")
        lines.append("")

    if flexes:
        lines.append("### Flexbox")
        seen = set()
        for f in flexes[:8]:
            d = f.get("direction", "row")
            j = f.get("justify", "")
            a = f.get("align", "")
            gap = f.get("gap", "")
            tag = f.get("tag", "div")
            key = f"{tag}|{d}|{j}"
            if key in seen:
                continue
            seen.add(key)
            parts = [f"`<{tag}>`", d]
            if j:
                parts.append(f"justify: {j}")
            if a:
                parts.append(f"align: {a}")
            if gap:
                parts.append(f"gap: {gap}")
            parts.append(f"({f.get('children', 0)} children)")
            lines.append(f"- {', '.join(parts)}")
        lines.append("")
    lines.append("")


def _md_images(lines: list[str], data: UIStyleData) -> None:
    if not data.images:
        return
    real = [i for i in data.images if i.get("src") != "[inline SVG]"]
    svgs = [i for i in data.images if i.get("src") == "[inline SVG]"]

    lines.append("## Assets")
    lines.append("")
    lines.append(f"{len(real)} images, {len(svgs)} SVG icons detected.")
    lines.append("")

    if real:
        for img in real[:12]:
            src = img.get("src", "")
            if len(src) > 70:
                src = src[:67] + "..."
            alt = img.get("alt", "")
            dims = f"{img.get('width', '?')} × {img.get('height', '?')}"
            label = alt if alt else "(no alt)"
            lines.append(f"- `{dims}` {label} — `{src}`")
        if len(real) > 12:
            lines.append(f"- ... and {len(real) - 12} more")
        lines.append("")

    named_svgs = [s for s in svgs if s.get("alt") and s["alt"] != "(icon)"]
    if named_svgs:
        lines.append("**Named SVG icons**: " + ", ".join(s["alt"] for s in named_svgs[:10]))
        lines.append("")


# ═══════════════════════════════════════════════════════════
#  JSON DESIGN TOKENS
# ═══════════════════════════════════════════════════════════

def _build_tokens_json(data: UIStyleData) -> str:
    tokens: dict[str, Any] = {"$schema": "https://tr.designtokens.org/format/", "source": data.url}

    # Colors
    color_tokens: dict[str, Any] = {}
    for category in ["background", "text", "border"]:
        colors = data.colors.get(category, [])
        group: dict[str, Any] = {}
        for i, c in enumerate(colors[:10]):
            hex_val = c["hex"] if isinstance(c, dict) else c
            name = f"{category}-{i + 1}"
            group[name] = {"$value": hex_val, "$type": "color"}
        if group:
            color_tokens[category] = group
    accent = _find_accent(data.colors)
    if accent:
        color_tokens["accent"] = {"$value": accent, "$type": "color"}
    tokens["color"] = color_tokens

    # Typography
    font_tokens: dict[str, Any] = {}
    fonts = _unique_font_families(data.typography)
    for i, f in enumerate(fonts):
        font_tokens[f"family-{i + 1}"] = {"$value": f, "$type": "fontFamily"}
    seen_sizes: set[str] = set()
    for t in data.typography:
        size = t.get("size", "")
        if size not in seen_sizes:
            seen_sizes.add(size)
            role = _guess_type_role(t.get("sampleTag", ""), size, t.get("weight", ""))
            font_tokens[f"size-{role.lower().replace(' ', '-').replace('/', '-')}"] = {"$value": size, "$type": "dimension"}
    tokens["typography"] = font_tokens

    # Spacing
    spacing_tokens: dict[str, Any] = {}
    for v in data.spacing:
        val = v if isinstance(v, int) else int(v) if str(v).isdigit() else None
        if val and val > 0:
            spacing_tokens[f"space-{val}"] = {"$value": f"{val}px", "$type": "dimension"}
    tokens["spacing"] = spacing_tokens

    # Border radius
    radius_tokens: dict[str, Any] = {}
    for i, r in enumerate(data.borders.get("radius", [])[:8]):
        radius_tokens[f"radius-{i + 1}"] = {"$value": r, "$type": "dimension"}
    tokens["borderRadius"] = radius_tokens

    # Shadows
    shadow_tokens: dict[str, Any] = {}
    for i, s in enumerate(data.shadows[:6]):
        shadow_tokens[f"shadow-{i + 1}"] = {"$value": s, "$type": "shadow"}
    tokens["shadow"] = shadow_tokens

    # CSS variables passthrough
    if data.css_variables:
        tokens["cssVariables"] = {k: v for k, v in sorted(data.css_variables.items())}

    return json.dumps(tokens, indent=2)


# ═══════════════════════════════════════════════════════════
#  HTML VISUAL REPORT
# ═══════════════════════════════════════════════════════════

def _build_html_report(data: UIStyleData) -> str:
    title = data.page_title or _domain(data.url)

    color_swatches = ""
    for category in ["background", "text", "border"]:
        colors = data.colors.get(category, [])
        if not colors:
            continue
        swatches = ""
        for c in colors[:12]:
            hex_val = c["hex"] if isinstance(c, dict) else c
            count = c.get("count", 0) if isinstance(c, dict) else 0
            border = "1px solid #333" if _is_light(hex_val) else "1px solid transparent"
            swatches += f"""<div class="swatch">
                <div class="swatch-color" style="background:{hex_val};border:{border}"></div>
                <code>{hex_val}</code>
                <small>{count}x</small>
            </div>"""
        color_swatches += f"""<div class="color-group">
            <h3>{category.title()}</h3>
            <div class="swatch-row">{swatches}</div>
        </div>"""

    font_samples = ""
    seen: set[str] = set()
    for t in data.typography[:15]:
        family = _clean_font(t.get("family", ""))
        size = t.get("size", "16px")
        weight = t.get("weight", "400")
        key = f"{family}|{size}|{weight}"
        if key in seen:
            continue
        seen.add(key)
        role = _guess_type_role(t.get("sampleTag", ""), size, weight)
        sample_text = t.get("sampleText", "The quick brown fox") or "The quick brown fox"
        if len(sample_text) > 50:
            sample_text = sample_text[:47] + "..."
        font_samples += f"""<div class="type-sample">
            <div class="type-meta">{role} · {family} · {size} · w{weight}</div>
            <div style="font-family:{t.get('family','sans-serif')};font-size:{size};font-weight:{weight};line-height:{t.get('lineHeight','normal')}">{sample_text}</div>
        </div>"""

    spacing_viz = ""
    for v in data.spacing[:20]:
        px = v if isinstance(v, int) else 0
        if px > 0:
            w = min(px, 300)
            spacing_viz += f"""<div class="space-item">
                <div class="space-bar" style="width:{w}px"></div>
                <code>{px}px</code>
            </div>"""

    btn_cards = ""
    seen_btns: set[str] = set()
    for btn in [c for c in data.components if c.get("type") == "button" and c.get("text")][:6]:
        skey = f"{btn.get('background')}|{btn.get('borderRadius')}"
        if skey in seen_btns:
            continue
        seen_btns.add(skey)
        bg = btn.get("background", "transparent")
        color = btn.get("color", "inherit")
        radius = btn.get("borderRadius", "0")
        padding = btn.get("padding", "8px 16px")
        border_css = btn.get("border", "none")
        if border_css == "none" or "0px none" in str(border_css):
            border_css = "none"
        btn_cards += f"""<div class="btn-demo">
            <button style="background:{bg};color:{color};border-radius:{radius};padding:{padding};border:{border_css};font-size:{btn.get('fontSize','14px')};font-weight:{btn.get('fontWeight','400')};cursor:pointer">{btn['text']}</button>
            <code>bg: {bg}<br>radius: {radius}<br>padding: {padding}</code>
        </div>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>UI Report: {title}</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;background:#0d0d0f;color:#e8e8e8;padding:40px 24px;max-width:1100px;margin:0 auto;line-height:1.6}}
h1{{font-size:2rem;font-weight:700;margin-bottom:8px;letter-spacing:-0.03em}}
h2{{font-size:1.3rem;font-weight:600;margin:48px 0 16px;padding-bottom:12px;border-bottom:1px solid #222}}
h3{{font-size:0.85rem;font-weight:600;color:#888;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:12px}}
.meta{{color:#666;font-size:0.8rem;margin-bottom:32px}}
code{{font-family:"SF Mono",Menlo,monospace;font-size:0.75rem;color:#aaa}}
.swatch-row{{display:flex;flex-wrap:wrap;gap:12px;margin-bottom:24px}}
.swatch{{display:flex;flex-direction:column;align-items:center;gap:6px}}
.swatch-color{{width:64px;height:64px;border-radius:10px}}
.swatch small{{color:#555;font-size:0.65rem}}
.color-group{{margin-bottom:24px}}
.type-sample{{margin-bottom:20px;padding:16px;background:#161618;border-radius:10px;border:1px solid #1a1a1e}}
.type-meta{{font-size:0.7rem;color:#666;margin-bottom:8px;font-family:monospace}}
.space-item{{display:flex;align-items:center;gap:12px;margin-bottom:6px}}
.space-bar{{height:12px;background:linear-gradient(90deg,#5E6AD2,#5E6AD244);border-radius:4px;min-width:2px}}
.btn-demo{{display:inline-flex;flex-direction:column;align-items:flex-start;gap:8px;padding:16px;background:#161618;border-radius:10px;border:1px solid #1a1a1e;margin:0 12px 12px 0}}
.btn-demo button{{min-width:80px}}
.btn-demo code{{display:block;margin-top:4px}}
</style>
</head>
<body>
<h1>Design Style Guide</h1>
<div class="meta">{data.url} · {datetime.now().strftime('%Y-%m-%d')} · {data.viewport_width}×{data.viewport_height}</div>

<h2>Color Palette</h2>
{color_swatches}

<h2>Typography</h2>
{font_samples}

<h2>Spacing Scale</h2>
{spacing_viz}

<h2>Component Patterns</h2>
{btn_cards if btn_cards else '<p style="color:#555">No button components detected.</p>'}

</body>
</html>"""


# ═══════════════════════════════════════════════════════════
#  COLOR HELPERS
# ═══════════════════════════════════════════════════════════

def _group_colors_by_role(colors: list) -> dict[str, list]:
    """Group extracted colors into semantic roles."""
    darks = []
    lights = []
    vibrant = []
    transparent = []

    for c in colors:
        hex_val = c["hex"] if isinstance(c, dict) else c

        if "rgba" in hex_val and re.search(r",\s*0\.\d", hex_val):
            transparent.append(c)
        elif _is_dark(hex_val):
            darks.append(c)
        elif _is_vibrant(hex_val):
            vibrant.append(c)
        else:
            lights.append(c)

    result = {}
    if darks:
        result["Dark / Base"] = darks
    if lights:
        result["Light / Surface"] = lights
    if vibrant:
        result["Vibrant / Accent"] = vibrant
    if transparent:
        result["Semi-transparent"] = transparent
    return result


def _find_accent(colors: dict) -> str | None:
    """Find the most likely accent color across all categories."""
    all_colors = []
    for cat in ["background", "text", "border"]:
        for c in colors.get(cat, []):
            hex_val = c["hex"] if isinstance(c, dict) else c
            count = c.get("count", 0) if isinstance(c, dict) else 0
            all_colors.append((hex_val, count))

    best = None
    best_score = 0
    for hex_val, count in all_colors:
        rgb = _hex_to_rgb(hex_val) if hex_val.startswith("#") else _parse_rgb(hex_val)
        if not rgb:
            continue
        r, g, b = rgb
        max_c, min_c = max(r, g, b), min(r, g, b)
        sat = (max_c - min_c) / max(max_c, 1)
        lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255
        if sat > 0.3 and 0.15 < lum < 0.85:
            score = sat * 0.6 + (count / 50) * 0.4
            if score > best_score:
                best_score = score
                best = hex_val
    return best


def _is_dark(color: str) -> bool:
    rgb = _hex_to_rgb(color) if color.startswith("#") else _parse_rgb(color)
    if not rgb:
        return False
    r, g, b = rgb
    return (0.299 * r + 0.587 * g + 0.114 * b) / 255 < 0.35


def _is_light(color: str) -> bool:
    rgb = _hex_to_rgb(color) if color.startswith("#") else _parse_rgb(color)
    if not rgb:
        return True
    r, g, b = rgb
    return (0.299 * r + 0.587 * g + 0.114 * b) / 255 > 0.7


def _is_vibrant(color: str) -> bool:
    rgb = _hex_to_rgb(color) if color.startswith("#") else _parse_rgb(color)
    if not rgb:
        return False
    r, g, b = rgb
    max_c, min_c = max(r, g, b), min(r, g, b)
    return (max_c - min_c) / max(max_c, 1) > 0.4


def _parse_rgb(color: str) -> tuple[int, int, int] | None:
    m = re.match(r"rgba?\(\s*(\d+),\s*(\d+),\s*(\d+)", color)
    return (int(m.group(1)), int(m.group(2)), int(m.group(3))) if m else None


def _hex_to_rgb(h: str) -> tuple[int, int, int] | None:
    h = h.lstrip("#")
    if len(h) == 3:
        h = h[0]*2 + h[1]*2 + h[2]*2
    if len(h) >= 6:
        return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return None


# ═══════════════════════════════════════════════════════════
#  GENERAL HELPERS
# ═══════════════════════════════════════════════════════════

def _domain(url: str) -> str:
    try:
        from urllib.parse import urlparse
        return urlparse(url).netloc
    except Exception:
        return url


def _clean_font(family: str) -> str:
    if not family:
        return ""
    return family.split(",")[0].strip().strip('"').strip("'")


def _unique_font_families(typo: list) -> list[str]:
    seen: set[str] = set()
    result = []
    for t in typo:
        f = _clean_font(t.get("family", ""))
        if f and f not in seen:
            seen.add(f)
            result.append(f)
    return result


def _px(s: str) -> float | None:
    m = re.match(r"(-?\d+(?:\.\d+)?)px", str(s).strip())
    return float(m.group(1)) if m else None


def _detect_grid_base(values: list) -> int | None:
    int_vals = [int(v) for v in values if isinstance(v, (int, float)) and v > 0]
    for base in [8, 4, 6]:
        if sum(1 for v in int_vals if v % base == 0) >= len(int_vals) * 0.5:
            return base
    return None


def _guess_type_role(tag: str, size: str, weight: str) -> str:
    px_val = _px(size)
    w = int(weight) if str(weight).isdigit() else 400

    if tag in ("h1",) or (px_val and px_val >= 32):
        return "Display / H1"
    if tag in ("h2",) or (px_val and px_val >= 22 and w >= 600):
        return "H2"
    if tag in ("h3",) or (px_val and px_val >= 18 and w >= 500):
        return "H3"
    if tag in ("h4", "h5", "h6"):
        return "H4-H6"
    if tag in ("code", "pre"):
        return "Code"
    if px_val and px_val <= 12:
        return "Caption"
    if px_val and px_val <= 14:
        return "Body Small"
    return "Body"
