"""UI extraction engine — uses Playwright to extract design system data from a live page."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any


@dataclass
class UIStyleData:
    url: str = ""
    page_title: str = ""
    viewport_width: int = 1280
    viewport_height: int = 720
    full_page_height: int = 0
    css_variables: dict[str, str] = field(default_factory=dict)
    colors: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    typography: list[dict[str, Any]] = field(default_factory=list)
    spacing: list[int] = field(default_factory=list)
    borders: dict[str, list[str]] = field(default_factory=dict)
    shadows: list[str] = field(default_factory=list)
    effects: list[str] = field(default_factory=list)
    components: list[dict[str, Any]] = field(default_factory=list)
    layout_patterns: list[dict[str, Any]] = field(default_factory=list)
    images: list[dict[str, str]] = field(default_factory=list)


_JS_EXTRACT = """
() => {
    const MAX_ELEMENTS = 2000;
    const result = {
        cssVariables: {},
        colors: { background: [], text: [], border: [] },
        typography: [],
        spacing: [],
        borders: { radius: [], width: [] },
        shadows: [],
        effects: [],
        components: [],
        layoutPatterns: [],
        images: [],
        fullPageHeight: document.documentElement.scrollHeight,
        pageTitle: document.title || '',
    };

    // ── Helper: convert any CSS color to hex via canvas ──
    const _cvs = document.createElement('canvas');
    _cvs.width = 1; _cvs.height = 1;
    const _ctx = _cvs.getContext('2d');

    function colorToHex(raw) {
        if (!raw || raw === 'transparent' || raw === 'rgba(0, 0, 0, 0)') return null;
        _ctx.clearRect(0, 0, 1, 1);
        _ctx.fillStyle = '#000000';
        _ctx.fillStyle = raw;
        _ctx.fillRect(0, 0, 1, 1);
        const [r, g, b, a] = _ctx.getImageData(0, 0, 1, 1).data;
        if (a === 0) return null;
        if (a < 255) {
            const af = (a / 255).toFixed(2).replace(/0+$/, '').replace(/\\.$/, '');
            return `rgba(${r}, ${g}, ${b}, ${af})`;
        }
        return '#' + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1);
    }

    // ── Helper: round px to nearest int, skip subpixel noise ──
    function roundPx(val) {
        if (!val || val === '0px' || val === 'auto' || val === 'normal') return 0;
        const n = parseFloat(val);
        if (isNaN(n) || n === 0) return 0;
        return Math.round(n);
    }

    // ── Helper: get direct text (not children) ──
    function directText(el) {
        let text = '';
        for (const node of el.childNodes) {
            if (node.nodeType === Node.TEXT_NODE) text += node.textContent;
            else if (node.nodeType === Node.ELEMENT_NODE) {
                const tag = node.tagName.toLowerCase();
                if (['span', 'strong', 'em', 'b', 'i', 'small'].includes(tag)) {
                    text += node.textContent;
                }
            }
        }
        return text.trim().replace(/\\s+/g, ' ').slice(0, 50);
    }

    // ── 1. Extract CSS custom properties ──
    const rootStyles = getComputedStyle(document.documentElement);
    const sheets = Array.from(document.styleSheets);
    for (const sheet of sheets) {
        try {
            const rules = Array.from(sheet.cssRules || []);
            for (const rule of rules) {
                if (rule.selectorText === ':root' || rule.selectorText === 'html' ||
                    rule.selectorText === ':root, :host' || rule.selectorText === '[data-theme]' ||
                    (rule.selectorText && rule.selectorText.includes(':root'))) {
                    const text = rule.cssText;
                    const varMatches = text.matchAll(/--([\\w-]+)\\s*:\\s*([^;]+)/g);
                    for (const m of varMatches) {
                        const name = '--' + m[1].trim();
                        let val = m[2].trim();
                        const computed = rootStyles.getPropertyValue(name).trim();
                        if (computed) val = computed;
                        result.cssVariables[name] = val;
                    }
                }
            }
        } catch(e) {}
    }

    // ── 2. Walk visible elements ──
    const allEls = Array.from(document.querySelectorAll('body *'));
    const els = allEls.slice(0, MAX_ELEMENTS);

    const colorMap = { background: new Map(), text: new Map(), border: new Map() };
    const seenFonts = new Map();
    const spacingSet = new Set();
    const seenRadius = new Set();
    const seenShadows = new Set();
    const seenEffects = new Set();

    function isVisible(el) {
        const r = el.getBoundingClientRect();
        if (r.width === 0 && r.height === 0) return false;
        const s = getComputedStyle(el);
        if (s.display === 'none' || s.visibility === 'hidden' || s.opacity === '0') return false;
        return true;
    }

    function trackColor(category, rawColor, tag) {
        const hex = colorToHex(rawColor);
        if (!hex) return;
        const map = colorMap[category];
        if (map.has(hex)) {
            const entry = map.get(hex);
            entry.count++;
            if (!entry.tags.includes(tag)) entry.tags.push(tag);
        } else {
            map.set(hex, { hex: hex, count: 1, tags: [tag], raw: rawColor });
        }
    }

    function addSpacing(val) {
        const px = roundPx(val);
        if (px > 0 && px <= 200) spacingSet.add(px);
    }

    for (const el of els) {
        if (!isVisible(el)) continue;
        const s = getComputedStyle(el);
        const tag = el.tagName.toLowerCase();

        // Colors — normalize everything to hex/rgba
        trackColor('background', s.backgroundColor, tag);
        trackColor('text', s.color, tag);
        if (s.borderWidth !== '0px') {
            const sides = [s.borderTopColor, s.borderRightColor, s.borderBottomColor, s.borderLeftColor];
            const unique = [...new Set(sides)];
            for (const c of unique) trackColor('border', c, tag);
        }

        // Typography
        const fontKey = `${s.fontFamily}|${s.fontSize}|${s.fontWeight}`;
        if (!seenFonts.has(fontKey)) {
            seenFonts.set(fontKey, {
                family: s.fontFamily,
                size: s.fontSize,
                weight: s.fontWeight,
                lineHeight: s.lineHeight,
                letterSpacing: s.letterSpacing,
                sampleTag: tag,
                sampleText: el.textContent.trim().slice(0, 40),
                count: 1,
            });
        } else {
            seenFonts.get(fontKey).count++;
        }

        // Spacing — round to whole pixels
        addSpacing(s.marginTop); addSpacing(s.marginBottom);
        addSpacing(s.marginLeft); addSpacing(s.marginRight);
        addSpacing(s.paddingTop); addSpacing(s.paddingBottom);
        addSpacing(s.paddingLeft); addSpacing(s.paddingRight);
        addSpacing(s.gap); addSpacing(s.rowGap); addSpacing(s.columnGap);

        // Borders — only clean uniform radius values, skip scientific notation
        const br = s.borderRadius;
        if (br && br !== '0px' && !br.match(/e\\+/)) {
            const parts = br.split(' ');
            if (parts.length === 1) seenRadius.add(br);
            else {
                const unique = [...new Set(parts.filter(p => p !== '0px' && !p.match(/e\\+/)))];
                if (unique.length === 1) seenRadius.add(unique[0]);
                else if (unique.length > 1) seenRadius.add(br);
            }
        }
        // Map huge radius to 9999px (pill shape intent)
        if (br && br.match(/e\\+/) && !seenRadius.has('9999px')) {
            seenRadius.add('9999px');
        }

        // Shadows — normalize oklab/lab inside, skip all-transparent
        const bs = s.boxShadow;
        if (bs && bs !== 'none') {
            const parts = bs.split(/,\\s*(?![^()]*\\))/);
            const meaningful = parts.filter(p => !p.trim().match(/^rgba\\(0,\\s*0,\\s*0,\\s*0\\)\\s+0px/));
            if (meaningful.length > 0) {
                const clean = meaningful.map(p => {
                    return p.replace(/oklab\\([^)]+\\)/g, (m) => colorToHex(m) || m)
                            .replace(/lab\\([^)]+\\)/g, (m) => colorToHex(m) || m);
                }).join(', ');
                seenShadows.add(clean);
            }
        }

        // Effects — skip no-op values
        const bf = s.backdropFilter || s.webkitBackdropFilter;
        if (bf && bf !== 'none' && bf !== 'blur(0px)') seenEffects.add('backdrop-filter: ' + bf);
        const f = s.filter;
        if (f && f !== 'none' && !f.startsWith('url(') &&
            f !== 'blur(0px)' && f !== 'brightness(1)' && f !== 'opacity(1)') {
            seenEffects.add('filter: ' + f);
        }

        // Component detection — buttons
        const isButton = tag === 'button' || el.getAttribute('role') === 'button' ||
            (tag === 'a' && (s.display.includes('flex') || s.display === 'inline-block') &&
             el.textContent.trim().length > 0 && el.textContent.trim().length < 30 &&
             (s.borderRadius !== '0px' || s.backgroundColor !== 'rgba(0, 0, 0, 0)'));

        if (isButton) {
            const text = directText(el);
            if (text.length > 0) {
                const bgHex = colorToHex(s.backgroundColor);
                const textHex = colorToHex(s.color);
                let radius = s.borderRadius;
                if (radius.match(/e\\+/)) radius = '9999px';
                result.components.push({
                    type: 'button',
                    text: text,
                    tag: tag,
                    background: bgHex || 'transparent',
                    color: textHex || 'inherit',
                    fontSize: s.fontSize,
                    fontWeight: s.fontWeight,
                    padding: s.padding,
                    borderRadius: radius,
                    border: s.border !== '0px none rgb(0, 0, 0)' ? s.border : 'none',
                });
            }
        }

        // Inputs
        if (tag === 'input' || tag === 'textarea' || tag === 'select') {
            result.components.push({
                type: 'input',
                inputType: el.getAttribute('type') || tag,
                placeholder: el.getAttribute('placeholder') || '',
                background: colorToHex(s.backgroundColor) || 'transparent',
                color: colorToHex(s.color) || 'inherit',
                fontSize: s.fontSize,
                padding: s.padding,
                borderRadius: s.borderRadius,
            });
        }

        // Navigation
        if (tag === 'nav') {
            const links = Array.from(el.querySelectorAll('a'));
            const linkTexts = links.slice(0, 8).map(a => {
                const firstText = a.querySelector('span') || a;
                let t = '';
                for (const n of firstText.childNodes) {
                    if (n.nodeType === Node.TEXT_NODE) t += n.textContent;
                }
                t = t.trim().replace(/\\s+/g, ' ');
                return t || a.getAttribute('aria-label') || a.textContent.trim().split('\\n')[0].slice(0, 20);
            }).filter(t => t && t.length > 0);
            if (linkTexts.length > 0) {
                result.components.push({
                    type: 'nav',
                    linkCount: links.length,
                    linkTexts: linkTexts,
                    display: s.display,
                    gap: s.gap,
                    background: colorToHex(s.backgroundColor) || 'transparent',
                });
            }
        }

        // Layout — grid
        if (s.display === 'grid' || s.display === 'inline-grid') {
            const cols = s.gridTemplateColumns;
            const colParts = cols.split(' ').length;
            if (colParts >= 2 || tag !== 'div') {
                result.layoutPatterns.push({
                    type: 'grid',
                    tag: tag,
                    columns: colParts,
                    columnDef: cols.length < 80 ? cols : colParts + ' columns',
                    gap: s.gap,
                    width: Math.round(el.getBoundingClientRect().width) + 'px',
                });
            }
        }

        // Layout — flex (only semantic or wide containers)
        if ((s.display === 'flex' || s.display === 'inline-flex') && el.children.length >= 2) {
            const isSemantic = ['header', 'main', 'section', 'footer', 'nav', 'aside'].includes(tag);
            const rect = el.getBoundingClientRect();
            if (isSemantic || rect.width > 600) {
                result.layoutPatterns.push({
                    type: 'flex',
                    tag: tag,
                    direction: s.flexDirection,
                    justify: s.justifyContent !== 'normal' ? s.justifyContent : '',
                    align: s.alignItems !== 'normal' ? s.alignItems : '',
                    gap: s.gap !== 'normal' && s.gap !== '0px' ? s.gap : '',
                    children: el.children.length,
                    width: Math.round(rect.width) + 'px',
                });
            }
        }
    }

    // ── 3. Images ──
    const imgs = Array.from(document.querySelectorAll('img'));
    for (const img of imgs.slice(0, 50)) {
        const rect = img.getBoundingClientRect();
        if (rect.width < 5 && rect.height < 5) continue;
        result.images.push({
            src: img.src || img.getAttribute('data-src') || '',
            alt: img.alt || '',
            width: Math.round(rect.width) + 'px',
            height: Math.round(rect.height) + 'px',
        });
    }
    const svgs = Array.from(document.querySelectorAll('svg'));
    for (const svg of svgs.slice(0, 30)) {
        const rect = svg.getBoundingClientRect();
        if (rect.width < 5 || rect.width > 200) continue;
        const label = svg.getAttribute('aria-label') || svg.closest('[title]')?.getAttribute('title') || '';
        result.images.push({
            src: '[inline SVG]',
            alt: label || '(icon)',
            width: Math.round(rect.width) + 'px',
            height: Math.round(rect.height) + 'px',
        });
    }

    // ── 4. Finalize ──
    for (const cat of ['background', 'text', 'border']) {
        result.colors[cat] = Array.from(colorMap[cat].values())
            .sort((a, b) => b.count - a.count)
            .slice(0, 20);
    }
    result.typography = Array.from(seenFonts.values())
        .sort((a, b) => parseFloat(b.size) - parseFloat(a.size));
    result.spacing = Array.from(spacingSet).sort((a, b) => a - b);
    result.borders.radius = Array.from(seenRadius);
    result.shadows = Array.from(seenShadows).slice(0, 10);
    result.effects = Array.from(seenEffects);

    return JSON.stringify(result);
}
"""


def extract_ui(
    url: str,
    *,
    include_images: bool = False,
    selector: str | None = None,
    viewport_width: int = 1280,
    viewport_height: int = 720,
) -> UIStyleData:
    """Launch Playwright, navigate to URL, extract full design system data."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise RuntimeError(
            "--ui requires Playwright.\n"
            "Install it:  pip install webtomd[playwright] && playwright install chromium"
        )

    data = UIStyleData(url=url, viewport_width=viewport_width, viewport_height=viewport_height)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            page = browser.new_page(viewport={"width": viewport_width, "height": viewport_height})
            page.goto(url, wait_until="domcontentloaded", timeout=20_000)
            page.wait_for_timeout(2000)

            _scroll_full_page(page)

            if selector:
                page.evaluate(f"""
                    () => {{
                        const target = document.querySelector({json.dumps(selector)});
                        if (target) {{
                            document.body.innerHTML = '';
                            document.body.appendChild(target);
                        }}
                    }}
                """)

            raw = page.evaluate(_JS_EXTRACT)
            parsed = json.loads(raw)

            data.page_title = parsed.get("pageTitle", "")
            data.full_page_height = parsed.get("fullPageHeight", 0)
            data.css_variables = parsed.get("cssVariables", {})
            data.colors = parsed.get("colors", {})
            data.typography = parsed.get("typography", [])
            data.spacing = parsed.get("spacing", [])
            data.borders = parsed.get("borders", {})
            data.shadows = parsed.get("shadows", [])
            data.effects = parsed.get("effects", [])
            data.components = parsed.get("components", [])
            data.layout_patterns = parsed.get("layoutPatterns", [])
            data.images = parsed.get("images", [])

        finally:
            browser.close()

    return data


def _scroll_full_page(page) -> None:
    """Scroll down the full page to trigger lazy-loaded elements."""
    page.evaluate("""
        async () => {
            await new Promise((resolve) => {
                let totalHeight = 0;
                const distance = 400;
                const timer = setInterval(() => {
                    window.scrollBy(0, distance);
                    totalHeight += distance;
                    if (totalHeight >= document.documentElement.scrollHeight) {
                        clearInterval(timer);
                        window.scrollTo(0, 0);
                        resolve();
                    }
                }, 100);
                setTimeout(() => { clearInterval(timer); window.scrollTo(0, 0); resolve(); }, 10000);
            });
        }
    """)
    page.wait_for_timeout(500)
