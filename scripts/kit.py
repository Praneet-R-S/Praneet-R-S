"""Shared design kit: theme colors, embedded fonts, text measuring, SVG helpers.

Everything here is standard-library Python so the GitHub Action needs no installs.
"""
import base64
import html
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")
FONT_DIR = os.path.join(ASSETS, "fonts")

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "font_metrics.json"), encoding="utf-8") as fh:
    METRICS = json.load(fh)

# ── Dark Industrial palette: matte black, graphite, burnt orange ─────────────
C = {
    "bg": "#0A0A0A",       # matte black
    "panel": "#121212",    # graphite panel
    "panel2": "#181818",   # raised surface
    "line": "#262626",     # hairlines
    "line2": "#343434",
    "dot": "#1E1E1E",      # dot-grid texture
    "orange": "#E8590C",   # burnt orange (primary accent)
    "orange2": "#F27A3A",  # lighter tint for highlights
    "orange3": "#F6A673",  # pale tint
    "text": "#F2F2F2",
    "muted": "#A6A6A6",
    "dim": "#6E6E6E",
    "faint": "#454545",
}

FONTS = {
    "grotesk-400": ("Space Grotesk", 400),
    "grotesk-500": ("Space Grotesk", 500),
    "grotesk-700": ("Space Grotesk", 700),
    "smono-400": ("Space Mono", 400),
    "smono-700": ("Space Mono", 700),
}

FAMILY = {
    "sans": "'Space Grotesk', 'Segoe UI', Helvetica, Arial, sans-serif",
    "mono": "'Space Mono', ui-monospace, 'SFMono-Regular', Consolas, monospace",
}

_font_cache = {}


def font_face(key):
    """@font-face rule with the subset font embedded as a data URI."""
    if key not in _font_cache:
        with open(os.path.join(FONT_DIR, key + ".woff2"), "rb") as fh:
            b64 = base64.b64encode(fh.read()).decode("ascii")
        fam, weight = FONTS[key]
        _font_cache[key] = (
            f"@font-face{{font-family:'{fam}';font-weight:{weight};font-style:normal;"
            f"src:url(data:font/woff2;base64,{b64}) format('woff2');}}"
        )
    return _font_cache[key]


def fonts_css(*keys):
    return "".join(font_face(k) for k in keys)


def measure(text, key, size, spacing=0.0):
    """Approximate rendered width in px of `text` in font `key` at `size`."""
    m = METRICS[key]
    d = m["_default"]
    return sum(m.get(ch, d) for ch in text) * size + spacing * max(len(text) - 1, 0)


def fit_size(text, key, max_w, start, minimum=10, spacing=0.0):
    size = start
    while size > minimum and measure(text, key, size, spacing) > max_w:
        size -= 0.5
    return size


def wrap(text, key, size, max_w, max_lines=None):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if measure(trial, key, size) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        while measure(lines[-1] + "...", key, size) > max_w and " " in lines[-1]:
            lines[-1] = lines[-1].rsplit(" ", 1)[0]
        lines[-1] += "..."
    return lines


def esc(s):
    return html.escape(str(s), quote=True)


def fmt_num(n):
    n = int(n)
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M".replace(".0M", "M")
    if n >= 10_000:
        return f"{n / 1000:.1f}k".replace(".0k", "k")
    return f"{n:,}"


REDUCED_MOTION = "@media (prefers-reduced-motion: reduce){*{animation:none!important;}}"


def svg_doc(w, h, body, css="", title="", desc="", defs=""):
    """Wrap content into a standalone, accessible SVG document."""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t d" fill="none">'
        f'<title id="t">{esc(title)}</title><desc id="d">{esc(desc)}</desc>'
        f"<style>{css}{REDUCED_MOTION}</style>"
        f"<defs>{defs}</defs>{body}</svg>\n"
    )


def grad(gid, stops, x2=1, y2=0, units=""):
    st = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    u = f' gradientUnits="{units}"' if units else ""
    return f'<linearGradient id="{gid}" x1="0" y1="0" x2="{x2}" y2="{y2}"{u}>{st}</linearGradient>'


def dot_pattern(pid="dots", gap=16, r=0.9, color=None, opacity=1):
    color = color or C["dot"]
    return (f'<pattern id="{pid}" width="{gap}" height="{gap}" patternUnits="userSpaceOnUse">'
            f'<circle cx="{gap / 2}" cy="{gap / 2}" r="{r}" fill="{color}" opacity="{opacity}"/></pattern>')


def ticks(x, y, w, h, size=9, color=None, width=1.4, inset=10):
    """Industrial corner registration marks."""
    color = color or C["orange"]
    x0, y0, x1, y1, s = x + inset, y + inset, x + w - inset, y + h - inset, size
    d = (f"M{x0} {y0 + s}V{y0}H{x0 + s} M{x1 - s} {y0}H{x1}V{y0 + s} "
         f"M{x1} {y1 - s}V{y1}H{x1 - s} M{x0 + s} {y1}H{x0}V{y1 - s}")
    return f'<path d="{d}" stroke="{color}" stroke-width="{width}" stroke-linecap="square"/>'


def panel(w, h, rx=16, uid="p", dots=False, tick=True):
    """Graphite panel with hairline border, optional dot texture and corner ticks."""
    defs = grad(f"{uid}-bg", [(0, "#151515"), (1, "#0E0E0E")], 0.3, 1)
    if dots:
        defs += dot_pattern(f"{uid}-dots", 16, 0.9, "#232323")
    body = f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="{rx}" fill="url(#{uid}-bg)"/>'
    if dots:
        body += f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="{rx}" fill="url(#{uid}-dots)"/>'
    body += f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="{rx}" stroke="{C["line"]}"/>'
    if tick:
        body += ticks(0, 0, w, h, color=C["faint"], width=1.2)
    return defs, body


def moving_grid(x0, x1, horizon, bottom, vx, n_h=9, n_v=26, color=None, dur=3.2, spread=2.2, opacity=1.0):
    """Perspective floor. Horizontal lines glide toward the viewer (SMIL)."""
    color = color or C["line2"]
    ys = [horizon + (bottom - horizon + 30) * (i / n_h) ** 2.1 for i in range(n_h + 2)]
    parts = []
    for i in range(n_h + 1):
        a, b = ys[i], ys[i + 1]
        op = min(1.0, 0.2 + i / n_h) * opacity
        parts.append(
            f'<line x1="{x0}" x2="{x1}" y1="{a:.1f}" y2="{a:.1f}" stroke="{color}" stroke-width="1" opacity="{op:.2f}">'
            f'<animate attributeName="y1" values="{a:.1f};{b:.1f}" dur="{dur}s" repeatCount="indefinite"/>'
            f'<animate attributeName="y2" values="{a:.1f};{b:.1f}" dur="{dur}s" repeatCount="indefinite"/></line>'
        )
    width = x1 - x0
    for j in range(n_v + 1):
        bx = x0 - width * (spread - 1) / 2 + width * spread * j / n_v
        parts.append(
            f'<line x1="{vx:.1f}" y1="{horizon}" x2="{bx:.1f}" y2="{bottom + 30}" stroke="{color}" stroke-width="1" opacity="{0.7 * opacity:.2f}"/>'
        )
    return "".join(parts)


def dot_sphere(cx, cy, R, gap=12, cls="ds", sweep=4.2):
    """A dot-matrix sphere: dot size follows the curvature, an orange light sweeps across."""
    base, lit = [], []
    n = int(R // gap) + 1
    for i in range(-n, n + 1):
        for j in range(-n, n + 1):
            x, y = cx + i * gap, cy + j * gap
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5 / R
            if d > 1:
                continue
            z = (1 - d * d) ** 0.5
            r = 0.9 + 2.5 * z
            shade = int(0x26 + (0x52 - 0x26) * z)
            col = f"#{shade:02x}{shade:02x}{shade:02x}"
            delay = (x - (cx - R)) / (2 * R) * (sweep * 0.45) + (y - cy) / R * 0.12
            base.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}" fill="{col}"/>')
            lit.append(f'<circle class="{cls}" cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}" fill="{C["orange"]}" '
                       f'style="animation-delay:{delay:.2f}s"/>')
    css = (f".{cls}{{opacity:0;animation:{cls} {sweep}s ease-in-out infinite;}}"
           f"@keyframes {cls}{{0%,100%{{opacity:0}}12%{{opacity:1}}26%{{opacity:0}}}}")
    return "".join(base) + "".join(lit), css


def glow_filter(fid, std=3.5, opacity=0.8, color=None):
    color = color or C["orange"]
    return (
        f'<filter id="{fid}" x="-30%" y="-60%" width="160%" height="220%">'
        f'<feGaussianBlur in="SourceAlpha" stdDeviation="{std}" result="b"/>'
        f'<feFlood flood-color="{color}" flood-opacity="{opacity}"/><feComposite in2="b" operator="in" result="g"/>'
        f'<feMerge><feMergeNode in="g"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
    )
