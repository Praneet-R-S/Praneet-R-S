"""Static (config-driven) SVG components in the Dark Industrial style:
header, buttons, highlights, section headings, the about-me code window,
tech stack, project cards and footer."""
import json
import math
import os

from kit import (C, FAMILY, esc, fonts_css, measure, fit_size, wrap, svg_doc, grad,
                 dot_pattern, ticks, panel, dot_sphere, glow_filter)

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "icons.json"), encoding="utf-8") as fh:
    BRAND = json.load(fh)

# Hand-drawn line icons (24×24, stroke based)
LINE_ICONS = {
    "trophy": "M7 4h10v4a5 5 0 0 1-10 0V4z M7 6H4v1a3 3 0 0 0 3 3 M17 6h3v1a3 3 0 0 1-3 3 M12 13v4 M8 20.5h8 M9.5 17h5v3.5",
    "scroll": "M15 3H6v18h8 M15 3l4 4v8 M15 3v4h4 M9 9h7 M9 12h7 M9 15h3.5 M18 17.2a2.4 2.4 0 1 1-.01 0 M16.6 21.8l1.4-2.2 1.4 2.2",
    "cap": "M2 9.5l10-5 10 5-10 5z M6 11.6v4.6c0 1.6 2.7 3.3 6 3.3s6-1.7 6-3.3v-4.6 M22 9.5v5.5",
    "people": "M9 11a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7z M2.5 20.5c0-3.6 2.9-6.2 6.5-6.2s6.5 2.6 6.5 6.2 M16 4.3a3.5 3.5 0 0 1 0 6.4 M18.2 14.6c2 .8 3.3 3 3.3 5.9",
    "db": "M4 6c0-1.7 3.6-3 8-3s8 1.3 8 3-3.6 3-8 3-8-1.3-8-3z M4 6v12c0 1.7 3.6 3 8 3s8-1.3 8-3V6 M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3",
    "brain": ("M5 6.5L12 4M5 6.5L12 12M5 17.5L12 12M5 17.5L12 20M12 4L19 8M12 12L19 8M12 12L19 16M12 20L19 16 "
              + " ".join(f"M{x + 1.9} {y}a1.9 1.9 0 1 1-3.8 0 1.9 1.9 0 1 1 3.8 0"
                         for x, y in [(5, 6.5), (5, 17.5), (12, 4), (12, 12), (12, 20), (19, 8), (19, 16)])),
    "chart": "M3 3v18h18 M6.5 15.5l4-5 3 3 3.2-4.2 M17 9.3l2.5-3.3 M16.2 6h3.3v3.3",
    "cloud": "M7 18.5h10.5a4.2 4.2 0 0 0 .7-8.35A6.2 6.2 0 0 0 6.2 9.1 4.7 4.7 0 0 0 7 18.5z",
    "mail": "M3 5.5h18v13H3z M3 6.5l9 6.5 9-6.5",
    "star": "M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z",
    "commit": "M12 8a4 4 0 1 0 0 8 4 4 0 0 0 0-8z M2 12h6 M16 12h6",
    "pr": "M6 3a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5z M6 8v8 M6 16a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5z M18 16a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5z M18 16V9a3 3 0 0 0-3-3h-4 M13 3.5L10.5 6 13 8.5",
    "issue": "M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18z M12 7.5v6 M12 16.2v.6",
    "repo": "M5 4.5A1.5 1.5 0 0 1 6.5 3H19v15H6.5A1.5 1.5 0 0 0 5 19.5z M5 19.5A1.5 1.5 0 0 0 6.5 21H19v-3 M9 7h6",
    "flame": "M12 2.8c.9 3 4.6 4.8 4.6 9.4a4.6 4.6 0 0 1-9.2 0c0-2 .9-3.3 2-4.4.2 1.7 1 2.6 2.1 3C11 8.3 10.8 5.6 12 2.8z",
    "bolt": "M13 2L4 14h7l-1 8 9-12h-7z",
    "calendar": "M4 5h16v16H4z M4 10h16 M8 3v4 M16 3v4",
    "arrow": "M7 17L17 7 M9 7h8v8",
    "medal": "M8 2.5h8l-2.5 6h-3z M12 21.5a6 6 0 1 0 0-12 6 6 0 0 0 0 12z M12 12.3l1.1 2.2 2.4.3-1.8 1.6.5 2.4-2.2-1.2-2.2 1.2.5-2.4-1.8-1.6 2.4-.3z",
    "abacus": "M3 3.5h18v17H3z M3 8.5h18 M3 13.5h18 M3 18.5h0 M7 6a1.6 1.6 0 1 0 0 .01 M11 6a1.6 1.6 0 1 0 0 .01 M16 11a1.6 1.6 0 1 0 0 .01 M8 11a1.6 1.6 0 1 0 0 .01 M13 16a1.6 1.6 0 1 0 0 .01 M17 16a1.6 1.6 0 1 0 0 .01",
    "briefcase": "M3 7.5h18v12H3z M8.5 7.5V5a1.5 1.5 0 0 1 1.5-1.5h4A1.5 1.5 0 0 1 15.5 5v2.5 M3 12.5h18 M11 12.5v2h2v-2",
    "pin": "M12 21s-6.5-6.2-6.5-11.2a6.5 6.5 0 0 1 13 0C18.5 14.8 12 21 12 21z M12 12.3a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5z",
    "heart": "M12 20.5s-8-4.9-8-10.6A4.4 4.4 0 0 1 12 7.3a4.4 4.4 0 0 1 8 2.6c0 5.7-8 10.6-8 10.6z",
}


def line_icon(name, x, y, size, stroke=None, width=1.6, cls=""):
    stroke = stroke or C["orange"]
    s = size / 24
    return (f'<g transform="translate({x:.1f},{y:.1f}) scale({s:.3f})" class="{cls}">'
            f'<path d="{LINE_ICONS[name]}" stroke="{stroke}" stroke-width="{width:.2f}" '
            f'stroke-linecap="round" stroke-linejoin="round" fill="none"/></g>')


def brand_icon(name, x, y, size, fill=None):
    fill = fill or C["text"]
    s = size / 24
    return (f'<g transform="translate({x:.1f},{y:.1f}) scale({s:.3f})">'
            f'<path d="{BRAND[name]["path"]}" fill="{fill}"/></g>')


def accent_dots(text, x, y, cls, dot_color=None):
    """Text where every '.' is drawn in the accent color."""
    dot_color = dot_color or C["orange"]
    parts = text.split(".")
    spans = ""
    for i, p in enumerate(parts):
        spans += esc(p)
        if i < len(parts) - 1:
            spans += f'<tspan fill="{dot_color}">.</tspan>'
    return f'<text x="{x}" y="{y}" class="{cls}">{spans}</text>'


FADE = ("@keyframes up{from{opacity:0;transform:translateY(10px)}}"
        ".up{animation:up .9s cubic-bezier(.2,.8,.2,1) both;}")


# ════════════════════════════════════════════════════════════════════════════
# HEADER
# ════════════════════════════════════════════════════════════════════════════
def header(cfg):
    W, H = 1000, 340
    name, roles = cfg["name"], cfg["roles"]
    tx = 48

    name_size = fit_size(name, "grotesk-700", 600, 90, spacing=-2.5)

    # typing roles (SMIL, discrete steps) -------------------------------------
    rsize = 19
    prefix_w = measure("> ", "smono-700", rsize)
    char_t, del_t, hold, pause = 0.075, 0.035, 1.6, 0.35
    slots = [len(r) * (char_t + del_t) + hold + pause for r in roles]
    starts = [sum(slots[:i]) for i in range(len(roles))]
    total = sum(slots)
    role_y = 226
    rx0 = tx + prefix_w
    role_clips, role_texts, cursor_pts = [], [], []
    for i, role in enumerate(roles):
        t0 = starts[i]
        pts = [(t0, 0.0)]
        for k in range(1, len(role) + 1):
            pts.append((t0 + k * char_t, measure(role[:k], "smono-400", rsize)))
        td = t0 + len(role) * char_t + hold
        for j, k in enumerate(range(len(role) - 1, -1, -1), start=1):
            pts.append((td + j * del_t, measure(role[:k], "smono-400", rsize)))
        cursor_pts += pts
        own = ([(0.0, 0.0)] if t0 > 0 else []) + pts + [(total, 0.0)]
        kt = ";".join(f"{t / total:.4f}" for t, _ in own)
        vals = ";".join(f"{wv + (2 if wv else 0):.1f}" for _, wv in own)
        role_clips.append(
            f'<clipPath id="rc{i}"><rect x="{rx0}" y="{role_y - 22}" height="30" width="0">'
            f'<animate attributeName="width" dur="{total:.2f}s" repeatCount="indefinite" calcMode="discrete" '
            f'keyTimes="{kt}" values="{vals}"/></rect></clipPath>')
        role_texts.append(f'<text x="{rx0}" y="{role_y}" clip-path="url(#rc{i})" class="role">{esc(role)}</text>')
    cursor_pts.sort()
    if cursor_pts[0][0] > 0:
        cursor_pts.insert(0, (0.0, 0.0))
    cursor_pts.append((total, 0.0))
    ckt = ";".join(f"{t / total:.4f}" for t, _ in cursor_pts)
    cvals = ";".join(f"{rx0 + wv + 4:.1f}" for _, wv in cursor_pts)
    cursor = (f'<rect class="caret" x="{rx0}" y="{role_y - 16}" width="10" height="20" fill="{C["orange"]}">'
              f'<animate attributeName="x" dur="{total:.2f}s" repeatCount="indefinite" calcMode="discrete" '
              f'keyTimes="{ckt}" values="{cvals}"/></rect>')

    # spec sheet row ------------------------------------------------------------
    specs = cfg.get("specs", [])
    sy = 262
    gap_c = 40
    widths = [max(measure(v, "grotesk-500", 15), measure(l, "smono-400", 10, 2)) for l, v in specs]
    scale = min(1.0, (640 - gap_c * max(len(specs) - 1, 0)) / max(sum(widths), 1))
    spec_svg = []
    x = tx
    for i, (lab, val) in enumerate(specs):
        if i:
            spec_svg.append(f'<path d="M{x - gap_c / 2:.1f} {sy + 12}V{sy + 50}" stroke="{C["line"]}"/>')
        vs = 15 * scale
        spec_svg.append(f'<g class="up" style="animation-delay:{1.2 + i * 0.12:.2f}s">'
                        f'<text x="{x}" y="{sy + 24}" class="lab">{esc(lab)}</text>'
                        f'<text x="{x}" y="{sy + 46}" class="val" style="font-size:{vs:.1f}px">{esc(val)}</text></g>')
        x += widths[i] * scale + gap_c
    spec_svg.insert(0, f'<path d="M{tx} {sy}H{x - gap_c:.1f}" stroke="{C["line"]}"/>')

    # dot-matrix sphere + orbit -------------------------------------------------
    scx, scy, sr = 832, 186, 108
    sphere, sphere_css = dot_sphere(scx, scy, sr, gap=12, cls="ds", sweep=4.6)
    a, b = sr + 26, 30
    orbit = f"M{scx - a} {scy}a{a} {b} 0 1 0 {2 * a} 0a{a} {b} 0 1 0 {-2 * a} 0"

    status = cfg.get("status", "")
    defs = (dot_pattern("dots", 18, 0.9, "#1A1A1A")
            + f'<radialGradient id="halo" cx="{scx / W:.3f}" cy="{scy / H:.3f}" r=".42"><stop offset="0" stop-color="{C["orange"]}" stop-opacity=".16"/>'
              f'<stop offset="1" stop-color="{C["orange"]}" stop-opacity="0"/></radialGradient>'
            + f'<clipPath id="frame"><rect width="{W}" height="{H}" rx="20"/></clipPath>'
            + "".join(role_clips) + glow_filter("gl", 2.5, .7))
    css = (fonts_css("grotesk-700", "grotesk-500", "smono-400", "smono-700") + FADE + sphere_css + f"""
.name{{font-family:{FAMILY['sans']};font-weight:700;font-size:{name_size}px;letter-spacing:-2.5px;fill:{C['text']};}}
.greet{{font-family:{FAMILY['mono']};font-weight:700;font-size:12.5px;letter-spacing:4px;fill:{C['orange']};}}
.role{{font-family:{FAMILY['mono']};font-size:{rsize}px;fill:#D9D9D9;}}
.pre{{font-family:{FAMILY['mono']};font-weight:700;font-size:{rsize}px;fill:{C['orange']};}}
.lab{{font-family:{FAMILY['mono']};font-size:10px;letter-spacing:2px;fill:{C['dim']};}}
.val{{font-family:{FAMILY['sans']};font-weight:500;font-size:15px;fill:{C['text']};}}
.top{{font-family:{FAMILY['mono']};font-size:10.5px;letter-spacing:2px;fill:{C['dim']};}}
.stat{{font-family:{FAMILY['mono']};font-size:10.5px;letter-spacing:2px;fill:{C['muted']};}}
.caret{{animation:blink 1s steps(1) infinite;}}@keyframes blink{{50%{{opacity:0}}}}
.pulse{{animation:pulse 1.8s ease-in-out infinite;}}@keyframes pulse{{50%{{opacity:.25}}}}
.rule{{animation:rule 1s cubic-bezier(.6,0,.2,1) both .3s;transform-box:fill-box;transform-origin:left;}}
@keyframes rule{{from{{transform:scaleX(0)}}}}
""")
    stat_w = measure(status, "smono-400", 10.5, 2)
    body = f"""<g clip-path="url(#frame)">
<rect width="{W}" height="{H}" fill="{C['bg']}"/>
<rect width="{W}" height="{H}" fill="url(#dots)"/>
<rect width="{W}" height="{H}" fill="url(#halo)"/>
<rect x="{tx}" y="31" width="7" height="7" fill="{C['orange']}"/>
<text x="{tx + 16}" y="38.5" class="top">{esc(cfg['name'].upper())}  /  GITHUB.COM/{esc(cfg['username'].upper())}</text>
<circle class="pulse" cx="{W - 48 - stat_w - 14:.1f}" cy="35" r="3.5" fill="{C['orange']}"/>
<text x="{W - 48}" y="38.5" text-anchor="end" class="stat">{esc(status)}</text>
<path d="M{tx} 56H{W - 48}" stroke="{C['line']}"/>
<g class="up" style="animation-delay:.2s"><path class="rule" d="M{tx} 104.5h24" stroke="{C['orange']}" stroke-width="2"/>
<text x="{tx + 36}" y="109" class="greet">{esc(cfg['greeting'])}</text></g>
<g class="up" style="animation-delay:.45s">{accent_dots(name, tx - 3, 186, 'name')}</g>
<g class="up" style="animation-delay:.8s"><text x="{tx}" y="{role_y}" class="pre">&gt;</text>{''.join(role_texts)}{cursor}</g>
{''.join(spec_svg)}
<ellipse cx="{scx}" cy="{scy}" rx="{a}" ry="{b}" stroke="{C['line2']}" stroke-dasharray="2 5" transform="rotate(-14 {scx} {scy})"/>
{sphere}
<g transform="rotate(-14 {scx} {scy})"><circle r="3.5" fill="{C['orange']}" filter="url(#gl)"><animateMotion dur="7s" repeatCount="indefinite" path="{orbit}"/></circle></g>
{ticks(0, 0, W, H, size=11, color=C['orange'], width=1.6, inset=14)}
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="19.5" stroke="{C['line']}"/>"""
    return svg_doc(W, H, body, css, title=f"{cfg['name']} — " + " · ".join(roles),
                   desc=f"{cfg['name']}: {', '.join(roles)}. " + "; ".join(f"{a_}: {b_}" for a_, b_ in specs), defs=defs)


# ════════════════════════════════════════════════════════════════════════════
# BUTTONS
# ════════════════════════════════════════════════════════════════════════════
def button(label, icon, uid):
    W, H = 232, 56
    lab_w = measure(label, "grotesk-500", 16, 0.2)
    total = 24 + 12 + lab_w + 12 + 14
    x0 = (W - total) / 2
    if icon == "linkedin":
        ic = (f'<rect x="{x0}" y="16" width="24" height="24" rx="5" stroke="{C["orange"]}" stroke-width="1.6"/>'
              f'<text x="{x0 + 12}" y="33" text-anchor="middle" class="in">in</text>')
    else:
        ic = line_icon("mail", x0, 16, 24)
    ax = x0 + 36 + lab_w + 12
    defs = (grad("sh", [(0, "#fff0"), (0.5, "#ffffff14"), (1, "#fff0")])
            + f'<clipPath id="c"><rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="14"/></clipPath>')
    css = fonts_css("grotesk-500", "grotesk-700") + f"""
.lab{{font-family:{FAMILY['sans']};font-weight:500;font-size:16px;letter-spacing:.2px;fill:{C['text']};}}
.in{{font-family:{FAMILY['sans']};font-weight:700;font-size:13px;fill:{C['orange']};}}
.sh{{animation:sh 5s ease-in-out infinite;}}
@keyframes sh{{0%,65%{{transform:translateX(-120px)}}100%{{transform:translateX({W + 60}px)}}}}"""
    body = f"""<g clip-path="url(#c)"><rect width="{W}" height="{H}" fill="#111111"/>
<rect class="sh" x="0" y="-10" width="70" height="{H + 20}" fill="url(#sh)" transform="skewX(-20)"/></g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="14" stroke="{C['line2']}"/>
<path d="M24 {H - .5}h28" stroke="{C['orange']}" stroke-width="1.5"/>
{ic}<text x="{x0 + 36}" y="34" class="lab">{esc(label)}</text>
{line_icon('arrow', ax, 21, 14, stroke=C['muted'], width=2)}"""
    return svg_doc(W, H, body, css, title=label, desc=f"{label} button", defs=defs)


# ════════════════════════════════════════════════════════════════════════════
# HIGHLIGHTS STRIP
# ════════════════════════════════════════════════════════════════════════════
def highlights(cfg):
    items = cfg["highlights"]
    W, H, gap = 1000, 176, 14
    n = len(items)
    tw = (W - gap * (n - 1)) / n
    css = fonts_css("grotesk-700", "grotesk-400", "smono-400", "smono-700") + FADE + f"""
.val{{font-family:{FAMILY['sans']};font-weight:700;font-size:36px;letter-spacing:-1px;fill:{C['text']};}}
.lab{{font-family:{FAMILY['mono']};font-weight:700;font-size:10px;letter-spacing:2px;fill:{C['orange']};}}
.sub{{font-family:{FAMILY['sans']};font-size:13px;fill:{C['muted']};}}
.idx{{font-family:{FAMILY['mono']};font-size:10px;fill:{C['faint']};letter-spacing:1px;}}
.bar{{animation:bar 1.1s cubic-bezier(.6,0,.2,1) both;transform-box:fill-box;transform-origin:left;}}
@keyframes bar{{from{{transform:scaleX(0)}}}}"""
    defs = grad("bg", [(0, "#161616"), (1, "#0F0F0F")], 0.3, 1)
    tiles = []
    for i, it in enumerate(items):
        x = i * (tw + gap)
        sub = wrap(it["sub"], "grotesk-400", 13, tw - 40, 2)
        sub_svg = "".join(f'<text x="{x + 20}" y="{140 + j * 17}" class="sub">{esc(s)}</text>' for j, s in enumerate(sub))
        vsize = fit_size(it["value"], "grotesk-700", tw - 40, 36, spacing=-1)
        tiles.append(f"""<g class="up" style="animation-delay:{0.1 + i * 0.12:.2f}s">
<rect x="{x + .5}" y=".5" width="{tw - 1:.1f}" height="{H - 1}" rx="14" fill="url(#bg)" stroke="{C['line']}"/>
<rect class="bar" x="{x + 20}" y="0" width="34" height="2" fill="{C['orange']}" style="animation-delay:{0.5 + i * 0.12:.2f}s"/>
{line_icon(it['icon'], x + 20, 22, 26)}
<text x="{x + tw - 20:.1f}" y="36" text-anchor="end" class="idx">{i + 1:02d}</text>
<text x="{x + 20}" y="98" class="val" style="font-size:{vsize}px">{esc(it['value'])}</text>
<text x="{x + 20}" y="120" class="lab">{esc(it['label'])}</text>{sub_svg}</g>""")
    desc = "; ".join(f"{it['value']} — {it['label']}: {it['sub']}" for it in items)
    return svg_doc(W, H, "".join(tiles), css, title="Highlights", desc=desc, defs=defs)


# ════════════════════════════════════════════════════════════════════════════
# SECTION HEADING
# ════════════════════════════════════════════════════════════════════════════
def heading(num, title, caption):
    W, H = 1000, 64
    tsize = 22
    x_title = 74
    title_w = measure(title, "grotesk-500", tsize, -0.3)
    x_line = x_title + title_w + 24
    cap = caption.upper()
    cap_w = measure(cap, "smono-400", 10.5, 2)
    x_cap_end = W - 26
    line_end = x_cap_end - cap_w - 22
    seg = 44
    css = fonts_css("grotesk-500", "smono-400", "smono-700") + f"""
.num{{font-family:{FAMILY['mono']};font-weight:700;font-size:13px;fill:{C['orange']};letter-spacing:1px;}}
.tt{{font-family:{FAMILY['sans']};font-weight:500;font-size:{tsize}px;letter-spacing:-.3px;fill:{C['text']};}}
.cap{{font-family:{FAMILY['mono']};font-size:10.5px;letter-spacing:2px;fill:{C['dim']};}}
.seg{{animation:seg 4s cubic-bezier(.6,0,.4,1) infinite;}}
@keyframes seg{{0%{{transform:translateX(0)}}50%{{transform:translateX({line_end - x_line - seg:.0f}px)}}100%{{transform:translateX(0)}}}}"""
    body = f"""<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="12" fill="#0F0F0F" stroke="{C['line']}"/>
<text x="26" y="37" class="num">{esc(num)}</text><text x="52" y="37.5" class="cap" style="fill:{C['faint']}">/</text>
<text x="{x_title}" y="40" class="tt">{esc(title)}</text>
<path d="M{x_line:.0f} 32.5H{line_end:.0f}" stroke="{C['line']}"/>
<rect class="seg" x="{x_line:.0f}" y="31.5" width="{seg}" height="2" fill="{C['orange']}"/>
<text x="{x_cap_end}" y="36.5" text-anchor="end" class="cap">{esc(cap)}</text>"""
    return svg_doc(W, H, body, css, title=f"{num} {title}", desc=caption, defs="")


# ════════════════════════════════════════════════════════════════════════════
# ABOUT — animated code window
# ════════════════════════════════════════════════════════════════════════════
def about_code(cfg):
    lines = cfg["about_code"]
    fs, lh = 14, 25
    top = 72
    W = 1000
    H = top + lh * len(lines) + 30
    colors = {"kw": C["orange"], "cls": C["text"], "fn": C["orange2"], "str": "#E4E4E4", "cm": "#5C5C5C", "p": "#959595"}
    cw = measure("M", "smono-400", fs)
    BOLD = ' font-weight="700"'
    rows = []
    for i, toks in enumerate(lines):
        y = top + lh * (i + 1) - 6
        spans = "".join(f'<tspan fill="{colors[k]}"{BOLD if k == "cls" else ""}>{esc(t)}</tspan>' for k, t in toks)
        rows.append(f'<g class="ln" style="animation-delay:{0.3 + i * 0.14:.2f}s">'
                    f'<text x="46" y="{y}" class="no" text-anchor="end">{i + 1:02d}</text>'
                    f'<text x="68" y="{y}" class="code" xml:space="preserve">{spans}</text></g>')
    last_len = sum(len(t) for _, t in lines[-1])
    cy = top + lh * len(lines) - 6
    pdefs, pbody = panel(W, H, 16, "cw", tick=False)
    defs = pdefs + glow_filter("gl", 2.5, .7)
    gx, gy, gr = 872, top + (H - top) / 2 - 10, 80
    css = fonts_css("smono-400", "smono-700") + f"""
.code{{font-family:{FAMILY['mono']};font-size:{fs}px;}}
.no{{font-family:{FAMILY['mono']};font-size:{fs - 3}px;fill:#3E3E3E;}}
.tab{{font-family:{FAMILY['mono']};font-size:12px;fill:{C['text']};}}
.st{{font-family:{FAMILY['mono']};font-size:10px;letter-spacing:1.5px;fill:{C['dim']};}}
.hl{{font-family:{FAMILY['mono']};font-size:9.5px;fill:{C['dim']};letter-spacing:2px;}}
.ln{{animation:ln .5s ease-out both;}}@keyframes ln{{from{{opacity:0;transform:translateX(-8px)}}}}
.caret{{animation:blink 1s steps(1) infinite;}}@keyframes blink{{50%{{opacity:0}}}}
.hfloat{{animation:hf 6s ease-in-out infinite;}}@keyframes hf{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-5px)}}}}"""
    body = f"""{pbody}
<path d="M.5 46H{W - .5}" stroke="{C['line']}"/>
<circle cx="26" cy="23.5" r="5.5" fill="#2A2A2A"/><circle cx="44" cy="23.5" r="5.5" fill="#2A2A2A"/><circle cx="62" cy="23.5" r="5.5" fill="{C['orange']}"/>
<path d="M92 46V17a6 6 0 0 1 6-6h120a6 6 0 0 1 6 6v29" fill="#0B0B0B" stroke="{C['line']}"/>
<path d="M92.5 46h131" stroke="#0B0B0B" stroke-width="2"/>
<rect x="106" y="25" width="7" height="7" fill="{C['orange']}"/>
<text x="122" y="32.5" class="tab">praneet.py</text>
<text x="{W - 24}" y="31" text-anchor="end" class="st">PYTHON 3.12  ·  UTF-8  ·  MAIN</text>
{''.join(rows)}
<rect class="caret" x="{68 + cw * last_len + 4:.1f}" y="{cy - 13}" width="9" height="17" fill="{C['orange']}"/>
{_globe(gx, gy, gr)}"""
    plain = "\n".join("".join(t for _, t in toks) for toks in lines)
    return svg_doc(W, H, body, css, title="About me", desc=plain, defs=defs)


def _globe(cx, cy, r):
    """Wireframe globe: meridians turn (SMIL), a satellite rides the orbit."""
    g = C["line2"]
    parts = [f'<g class="hfloat"><circle cx="{cx}" cy="{cy}" r="{r}" stroke="#3A3A3A" stroke-width="1.2"/>']
    for k in range(1, 4):
        dy = r * k / 4
        rx = (r * r - dy * dy) ** 0.5
        for s in (-1, 1):
            parts.append(f'<ellipse cx="{cx}" cy="{cy + s * dy:.1f}" rx="{rx:.1f}" ry="{rx * 0.16:.1f}" stroke="{g}"/>')
    parts.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="{r * 0.16:.1f}" stroke="#4A4A4A"/>')
    for k in range(6):
        phase = k / 6
        vals = ";".join(f"{abs(r * math.cos(math.pi * (phase + t / 12))):.1f}" for t in range(13))
        parts.append(f'<ellipse cx="{cx}" cy="{cy}" ry="{r}" rx="{r:.1f}" stroke="#3A3A3A">'
                     f'<animate attributeName="rx" values="{vals}" dur="10s" repeatCount="indefinite"/></ellipse>')
    a, b = r + 22, r * 0.32
    orbit = f"M{cx - a} {cy}a{a} {b:.1f} 0 1 0 {2 * a} 0a{a} {b:.1f} 0 1 0 {-2 * a} 0"
    parts.append(f'<g transform="rotate(-16 {cx} {cy})"><path d="{orbit}" stroke="{C["orange"]}" stroke-opacity=".55" stroke-dasharray="2 5"/>'
                 f'<circle r="4" fill="{C["orange"]}" filter="url(#gl)"><animateMotion dur="7s" repeatCount="indefinite" path="{orbit}"/></circle></g>')
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="3.5" fill="{C["orange"]}"/></g>'
                 f'<text x="{cx}" y="{cy + r + 38:.0f}" text-anchor="middle" class="hl">B.TECH CSE  ·  CLASS OF 2027</text>')
    return "".join(parts)


# ════════════════════════════════════════════════════════════════════════════
# TECH STACK
# ════════════════════════════════════════════════════════════════════════════
def stack(cfg):
    groups = cfg["stack"]
    W = 1000
    tile, gap, row_h, top = 82, 14, 112, 30
    label_w = 222
    H = top + row_h * (len(groups) - 1) + tile + top
    pdefs, pbody = panel(W, H, 16, "st", dots=True, tick=True)
    defs = pdefs + grad("tb", [(0, "#1A1A1A"), (1, "#121212")], 0, 1)
    css = fonts_css("grotesk-500", "smono-400") + f"""
.grp{{font-family:{FAMILY['sans']};font-weight:500;font-size:16px;letter-spacing:-.2px;fill:{C['text']};}}
.cnt{{font-family:{FAMILY['mono']};font-size:10px;letter-spacing:2px;fill:{C['dim']};}}
.lb{{font-family:{FAMILY['mono']};font-size:10px;fill:{C['muted']};}}
.t{{animation:pop .6s cubic-bezier(.2,.8,.2,1) both;transform-box:fill-box;transform-origin:center;}}
@keyframes pop{{from{{opacity:0;transform:scale(.85)}}}}
.wave{{opacity:0;animation:wave 5.2s ease-in-out infinite;}}
@keyframes wave{{0%,100%{{opacity:0}}8%{{opacity:1}}22%{{opacity:0}}}}"""
    body = [pbody]
    k = 0
    for gi, g in enumerate(groups):
        y = top + gi * row_h
        cy = y + tile / 2
        body.append(f'<rect x="32" y="{cy - 20:.0f}" width="2" height="16" fill="{C["orange"]}"/>'
                    f'<text x="44" y="{cy - 6:.0f}" class="grp">{esc(g["group"])}</text>'
                    f'<text x="44" y="{cy + 14:.0f}" class="cnt">{len(g["items"]):02d} TOOLS</text>')
        if gi:
            body.append(f'<path d="M28 {y - 15}H{W - 28}" stroke="{C["line"]}"/>')
        for ti, (icon, label) in enumerate(g["items"]):
            x = label_w + ti * (tile + gap)
            if icon.startswith("@"):
                glyph = line_icon(icon[1:], x + tile / 2 - 15, y + 13, 30, stroke="#DADADA", width=1.7)
            else:
                glyph = brand_icon(icon, x + tile / 2 - 15, y + 13, 30, fill="#DADADA")
            lbl = label if measure(label, "smono-400", 10) < tile - 6 else label[:9] + "."
            body.append(f"""<g class="t" style="animation-delay:{0.1 + k * 0.03:.2f}s">
<rect x="{x + .5}" y="{y + .5}" width="{tile - 1}" height="{tile - 1}" rx="12" fill="url(#tb)" stroke="{C['line2']}"/>
<rect class="wave" x="{x + .5}" y="{y + .5}" width="{tile - 1}" height="{tile - 1}" rx="12" stroke="{C['orange']}" stroke-width="1.4" style="animation-delay:{ti * 0.16 + gi * 0.45:.2f}s"/>
{glyph}
<text x="{x + tile / 2}" y="{y + tile - 12}" text-anchor="middle" class="lb">{esc(lbl)}</text></g>""")
            k += 1
    desc = " | ".join(f"{g['group']}: " + ", ".join(lbl for _, lbl in g["items"]) for g in groups)
    return svg_doc(W, H, "".join(body), css, title="Tech stack", desc=desc, defs=defs)


# ════════════════════════════════════════════════════════════════════════════
# PROJECT CARD
# ════════════════════════════════════════════════════════════════════════════
def _viz(kind, x, y, w, h):
    """Small looping illustration in the card's top-right corner."""
    o, o2, g, g2 = C["orange"], C["orange2"], "#4A4A4A", "#2E2E2E"
    if kind == "match":
        L = [(x + 18, y + 14 + i * 21) for i in range(4)]
        R = [(x + w - 18, y + 14 + i * 21) for i in range(4)]
        pairs = [(0, 2), (1, 0), (2, 3), (3, 1)]
        out = []
        for j, (a, b) in enumerate(pairs):
            (x1, y1), (x2, y2) = L[a], R[b]
            d = f"M{x1} {y1}C{x1 + 50} {y1} {x2 - 50} {y2} {x2} {y2}"
            out.append(f'<path d="{d}" stroke="{g2}" stroke-width="1"/>')
            out.append(f'<path class="mline" d="{d}" stroke="{o if j == 2 else "#8A8A8A"}" stroke-width="{1.8 if j == 2 else 1.2}" pathLength="100" '
                       f'stroke-dasharray="100" style="animation-delay:{j * 0.45:.2f}s"/>')
        out += [f'<circle cx="{a}" cy="{b}" r="4.5" fill="#0E0E0E" stroke="#8A8A8A" stroke-width="1.4"/>' for a, b in L]
        out += [f'<rect x="{a - 4.5}" y="{b - 4.5}" width="9" height="9" rx="1.5" fill="#0E0E0E" stroke="{o if i == 3 else "#8A8A8A"}" stroke-width="1.4"/>'
                for i, (a, b) in enumerate(R)]
        bx, by = R[3]
        out.append(f'<text x="{bx - 12}" y="{by + 3.5}" text-anchor="end" class="flag">DUP</text>')
        return "".join(out)
    if kind == "pulse":
        mid = y + h / 2 + 8
        pts = [(0, 0), (.22, 0), (.28, -6), (.33, 0), (.4, 0), (.45, 16), (.5, -34), (.55, 12), (.6, 0), (.7, 0), (.76, -8), (.82, 0), (1, 0)]
        d = "M" + " L".join(f"{x + px * w:.1f} {mid + py:.1f}" for px, py in pts)
        hx, hy = x + w - 20, y + 10
        heart = (f'<path class="beat" d="M{hx} {hy + 6}c-3-5-11-3-11 3 0 5 7 9 11 12 4-3 11-7 11-12 0-6-8-8-11-3z" '
                 f'stroke="{o}" stroke-width="1.5" fill="{o}" fill-opacity=".12"/>')
        return (f'<path d="{d}" stroke="{g2}" stroke-width="1.2"/>'
                f'<path class="ecg" d="{d}" stroke="{o}" stroke-width="1.8" pathLength="100" stroke-dasharray="26 74" stroke-linecap="round"/>'
                + heart)
    if kind == "forecast":
        bx, by = x + 6, y + h - 6
        hist = [(0, .35), (.1, .5), (.2, .42), (.3, .62), (.4, .55), (.5, .72)]
        fut = [(.5, .72), (.62, .66), (.74, .82), (.86, .78), (1, .94)]
        to = lambda px, py: (bx + px * (w - 12), by - py * (h - 18))
        dh = "M" + " L".join(f"{to(a, b)[0]:.1f} {to(a, b)[1]:.1f}" for a, b in hist)
        df = "M" + " L".join(f"{to(a, b)[0]:.1f} {to(a, b)[1]:.1f}" for a, b in fut)
        up = [to(a, b + .05 + (a - .5) * .3) for a, b in fut]
        dn = [to(a, b - .05 - (a - .5) * .3) for a, b in reversed(fut)]
        band = "M" + " L".join(f"{u:.1f} {v:.1f}" for u, v in up + dn) + "Z"
        sx = to(.5, 0)[0]
        return (f'<path d="M{bx} {y + 4}V{by}H{x + w - 4}" stroke="{g2}" stroke-width="1.2"/>'
                f'<path d="M{sx:.1f} {y + 6}V{by}" stroke="{g}" stroke-dasharray="2 3" stroke-width="1"/>'
                f'<path class="band" d="{band}" fill="{o}" fill-opacity=".14"/>'
                f'<path class="draw" d="{dh}" stroke="#CFCFCF" stroke-width="1.8" pathLength="100" stroke-dasharray="100" stroke-linejoin="round"/>'
                f'<path class="draw2" d="{df}" stroke="{o}" stroke-width="1.8" pathLength="100" stroke-dasharray="4 3" stroke-linejoin="round"/>'
                f'<circle class="tip" cx="{to(1, .94)[0]:.1f}" cy="{to(1, .94)[1]:.1f}" r="3.2" fill="{o2}"/>')
    if kind == "agents":
        ccx, ccy, r = x + w / 2, y + h / 2, min(w, h) / 2 - 8
        out = [f'<circle cx="{ccx}" cy="{ccy}" r="{r}" stroke="{g2}" stroke-dasharray="2 4"/>']
        for i in range(9):
            a = -math.pi / 2 + i * 2 * math.pi / 9
            nx, ny = ccx + r * math.cos(a), ccy + r * math.sin(a)
            out.append(f'<line class="flow" x1="{ccx}" y1="{ccy}" x2="{nx:.1f}" y2="{ny:.1f}" stroke="{g}" stroke-dasharray="3 4" style="animation-delay:-{i * 0.13:.2f}s"/>')
            out.append(f'<circle class="node" cx="{nx:.1f}" cy="{ny:.1f}" r="4.5" fill="#0E0E0E" stroke="#8A8A8A" stroke-width="1.4" style="animation-delay:{i * 0.22:.2f}s"/>')
        out.append(f'<circle cx="{ccx}" cy="{ccy}" r="8.5" fill="{o}" fill-opacity=".15" stroke="{o}" stroke-width="1.6"/>'
                   f'<circle cx="{ccx}" cy="{ccy}" r="2.8" fill="{o}"/>')
        return "".join(out)
    if kind == "flow":
        sc, ox, oy = min(w / 164, h / 96), x, y          # drawn at 164x96, scaled to fit
        x, y, w, h = 0, 0, 164, 96
        cy = y + h / 2
        sx, r1, dx, ux, ex = x + 8, x + 24, x + 80, x + 100, x + 156
        main = f"M{sx} {cy}H{dx - 10}V{cy}L{dx} {cy - 10}V{cy - 26}H{ex}V{cy - 7}"
        alt = f"M{sx} {cy}H{dx - 10}L{dx} {cy + 10}V{cy + 26}H{ex}V{cy + 7}"
        out = [f'<path d="M{sx + 6} {cy}H{r1}M{r1 + 34} {cy}H{dx - 11}" stroke="{g}"/>',
               f'<path d="M{dx} {cy - 11}V{cy - 26}H{ux}M{ux + 34} {cy - 26}H{ex}V{cy - 7}M{dx} {cy + 11}V{cy + 26}H{ux}M{ux + 34} {cy + 26}H{ex}V{cy + 7}" stroke="{g}"/>',
               f'<circle cx="{sx}" cy="{cy}" r="6" stroke="#8A8A8A" stroke-width="1.4"/>',
               f'<rect x="{r1}" y="{cy - 11}" width="34" height="22" rx="4" fill="#0E0E0E" stroke="#8A8A8A" stroke-width="1.3"/>',
               f'<path d="M{dx} {cy - 10}L{dx + 10} {cy}L{dx} {cy + 10}L{dx - 10} {cy}Z" fill="#0E0E0E" stroke="{o}" stroke-width="1.4"/>',
               f'<rect x="{ux}" y="{cy - 37}" width="34" height="22" rx="4" fill="#0E0E0E" stroke="#8A8A8A" stroke-width="1.3"/>',
               f'<rect x="{ux}" y="{cy + 15}" width="34" height="22" rx="4" fill="#0E0E0E" stroke="#8A8A8A" stroke-width="1.3"/>',
               f'<circle cx="{ex}" cy="{cy}" r="6" stroke="#8A8A8A" stroke-width="2.6"/>',
               f'<circle r="3.5" fill="{o}"><animateMotion dur="4s" repeatCount="indefinite" path="{main}"/></circle>',
               f'<circle r="3" fill="{o2}" opacity=".8"><animateMotion dur="4s" begin="2s" repeatCount="indefinite" path="{alt}"/></circle>']
        return f'<g transform="translate({ox} {oy}) scale({sc:.3f})">' + "".join(out) + "</g>"
    if kind == "bus":
        pts = [(0, .8), (.22, .8), (.32, .35), (.55, .35), (.66, .7), (.86, .7), (1, .2)]
        P = [(x + px * w, y + py * h) for px, py in pts]
        d = "M" + " L".join(f"{a:.1f} {b:.1f}" for a, b in P)
        out = [f'<path d="{d}" stroke="{g2}" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"/>',
               f'<path d="{d}" stroke="{g}" stroke-width="1.2" stroke-dasharray="3 4" stroke-linejoin="round"/>']
        for a, b in (P[0], P[3], P[5]):
            out.append(f'<circle cx="{a:.1f}" cy="{b:.1f}" r="3.5" fill="#0E0E0E" stroke="#8A8A8A" stroke-width="1.3"/>')
        ex, ey = P[-1]
        out.append(f'<rect x="{ex - 6:.1f}" y="{ey - 6:.1f}" width="12" height="12" rx="2" fill="#0E0E0E" stroke="{o}" stroke-width="1.4"/>')
        out.append(f'<rect x="-6" y="-4" width="12" height="8" rx="2" fill="{o}"><animateMotion dur="5s" repeatCount="indefinite" path="{d}"/></rect>')
        return "".join(out)
    if kind == "scan":
        fw, fh = 46, h - 4
        fx, fy = x + w / 2 - fw / 2 - 14, y + 2
        cx2, cy2 = fx + fw / 2, fy + fh / 2
        out = [f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" rx="8" stroke="#8A8A8A" stroke-width="1.3"/>',
               f'<path d="M{cx2 - 6} {fy + 4}h12" stroke="#5A5A5A" stroke-width="1.6" stroke-linecap="round"/>',
               f'<path d="M{cx2 - 4} {cy2 - 14}h8l2 5v15a2 2 0 0 1-2 2h-8a2 2 0 0 1-2-2v-15z" stroke="#CFCFCF" stroke-width="1.3"/>',
               f'<path d="M{cx2 - 12} {cy2 - 18}v-5h5M{cx2 + 12} {cy2 - 18}v-5h-5M{cx2 - 12} {cy2 + 18}v5h5M{cx2 + 12} {cy2 + 18}v5h-5" stroke="{o}" stroke-width="1.4"/>',
               f'<rect class="scanl" x="{fx + 5}" y="{cy2 - 20}" width="{fw - 10}" height="1.6" fill="{o}"/>',
               f'<text class="cred" x="{fx + fw + 16}" y="{cy2 + 4}">+10</text>']
        return "".join(out)
    if kind == "path":
        cols, rows = 9, 5
        cs = min(w / cols, h / rows)
        gx0, gy0 = x + (w - cols * cs) / 2, y + (h - rows * cs) / 2
        walls = {(2, 0), (2, 1), (2, 2), (5, 2), (5, 3), (5, 4), (7, 0), (7, 1), (4, 0)}
        route = [(0, 4), (1, 4), (2, 4), (3, 4), (3, 3), (3, 2), (3, 1), (4, 1), (5, 1), (6, 1), (6, 2), (7, 2), (8, 2), (8, 1), (8, 0)]
        out = []
        for cx_ in range(cols):
            for cy_ in range(rows):
                fill = "#2E2E2E" if (cx_, cy_) in walls else "#141414"
                out.append(f'<rect x="{gx0 + cx_ * cs + 1:.1f}" y="{gy0 + cy_ * cs + 1:.1f}" width="{cs - 2:.1f}" height="{cs - 2:.1f}" rx="2" fill="{fill}" stroke="#1F1F1F"/>')
        d = "M" + " L".join(f"{gx0 + (a + .5) * cs:.1f} {gy0 + (b + .5) * cs:.1f}" for a, b in route)
        sx, sy = route[0]
        ex, ey = route[-1]
        out.append(f'<path class="draw" d="{d}" stroke="{o}" stroke-width="2" pathLength="100" stroke-dasharray="100" stroke-linejoin="round"/>')
        out.append(f'<circle cx="{gx0 + (sx + .5) * cs:.1f}" cy="{gy0 + (sy + .5) * cs:.1f}" r="3.5" fill="#CFCFCF"/>')
        out.append(f'<rect class="tip" x="{gx0 + (ex + .5) * cs - 4:.1f}" y="{gy0 + (ey + .5) * cs - 4:.1f}" width="8" height="8" fill="{o}"/>')
        return "".join(out)
    return ""


VIZ_CSS = f"""
.flag{{font-family:{FAMILY['mono']};font-weight:700;font-size:8.5px;fill:{C['orange']};animation:blinkf 1.4s steps(1) infinite;}}
@keyframes blinkf{{50%{{opacity:.2}}}}
.mline{{animation:mline 4s ease-in-out infinite both;}}
@keyframes mline{{0%{{stroke-dashoffset:100;opacity:1}}35%,80%{{stroke-dashoffset:0;opacity:1}}100%{{stroke-dashoffset:0;opacity:0}}}}
.ecg{{animation:ecg 2.4s linear infinite;}}
@keyframes ecg{{from{{stroke-dashoffset:100}}to{{stroke-dashoffset:0}}}}
.beat{{animation:beat 1.2s ease-in-out infinite;transform-box:fill-box;transform-origin:center;}}
@keyframes beat{{0%,100%{{transform:scale(1)}}15%{{transform:scale(1.15)}}30%{{transform:scale(1)}}45%{{transform:scale(1.08)}}}}
.draw{{animation:draw 5s ease-out infinite both;}}
@keyframes draw{{0%{{stroke-dashoffset:100}}30%,100%{{stroke-dashoffset:0}}}}
.draw2,.band,.tip{{animation:fade 5s ease-out infinite both;}}
@keyframes fade{{0%,30%{{opacity:0}}50%,100%{{opacity:1}}}}
.flow{{animation:flow 1.2s linear infinite;}}@keyframes flow{{to{{stroke-dashoffset:-14}}}}
.node{{animation:node 2s ease-in-out infinite;}}@keyframes node{{0%,100%{{stroke:#8A8A8A}}20%{{stroke:{C['orange']}}}}}
.scanl{{animation:scan 2.2s ease-in-out infinite alternate;}}@keyframes scan{{to{{transform:translateY(38px)}}}}
.cred{{font-family:{FAMILY['mono']};font-weight:700;font-size:12px;fill:{C['orange']};animation:cred 2.2s ease-out infinite;}}
@keyframes cred{{0%{{opacity:0;transform:translateY(8px)}}30%,70%{{opacity:1;transform:translateY(0)}}100%{{opacity:0;transform:translateY(-8px)}}}}"""


def project_card(p, idx):
    W, H = 490, 344
    pdefs, pbody = panel(W, H, 16, "pc", dots=False, tick=True)
    linked = bool(p.get("repo"))
    chip = "VIEW REPO" if linked else p.get("status", "REPO SOON")
    chip_w = measure(chip, "smono-700", 10, 1.5) + 24 + (16 if linked else 0)
    title_size = fit_size(p["title"], "grotesk-700", W - 52, 30, spacing=-0.8)
    desc = wrap(p["description"], "grotesk-400", 14, W - 52, 3)
    css = fonts_css("grotesk-700", "grotesk-400", "smono-400", "smono-700") + FADE + f"""
.idx{{font-family:{FAMILY['mono']};font-weight:700;font-size:12px;fill:{C['orange']};letter-spacing:1px;}}
.per{{font-family:{FAMILY['mono']};font-size:10px;fill:{C['dim']};letter-spacing:1.5px;}}
.chip{{font-family:{FAMILY['mono']};font-weight:700;font-size:10px;letter-spacing:1.5px;}}
.tt{{font-family:{FAMILY['sans']};font-weight:700;letter-spacing:-.8px;fill:{C['text']};}}
.sub{{font-family:{FAMILY['mono']};font-size:11px;letter-spacing:.5px;fill:{C['orange']};}}
.ds{{font-family:{FAMILY['sans']};font-size:14px;fill:{C['muted']};}}
.mv{{font-family:{FAMILY['sans']};font-weight:700;font-size:22px;letter-spacing:-.5px;fill:{C['text']};}}
.ml{{font-family:{FAMILY['mono']};font-size:9.5px;fill:{C['dim']};letter-spacing:1px;}}
""" + VIZ_CSS
    n = len(p["metrics"])
    col_w = (W - 52) / max(n, 1)
    mets = []
    for j, (v, lab) in enumerate(p["metrics"]):
        mx = 26 + j * col_w
        vs = fit_size(v, "grotesk-700", col_w - 14, 22, spacing=-0.5)
        mets.append(f'<text x="{mx:.1f}" y="298" class="mv" style="font-size:{vs}px">{esc(v)}</text>'
                    f'<rect x="{mx:.1f}" y="309" width="5" height="5" fill="{C["orange"]}"/>'
                    f'<text x="{mx + 11:.1f}" y="315" class="ml">{esc(lab.upper())}</text>')
        if j:
            mets.append(f'<path d="M{mx - 13:.1f} 278V318" stroke="{C["line"]}"/>')
    arrow = line_icon("arrow", 26 + chip_w - 24, 26, 12, stroke=C["bg"], width=2.4) if linked else ""
    chip_rect = (f'<rect x="26" y="22" width="{chip_w:.1f}" height="22" rx="4" fill="{C["orange"]}"/>' if linked else
                 f'<rect x="26.5" y="22.5" width="{chip_w:.1f}" height="21" rx="4" stroke="{C["line2"]}" fill="#161616"/>')
    chip_txt = C["bg"] if linked else C["muted"]
    body = f"""{pbody}
<g class="up">{chip_rect}<text x="38" y="37" class="chip" fill="{chip_txt}">{esc(chip)}</text>{arrow}
<text x="26" y="68" class="idx">{idx:02d}</text><text x="50" y="68" class="per">{esc(p['period'])}</text></g>
{_viz(p.get('viz', ''), 300, 20, 164, 96)}
<g class="up" style="animation-delay:.15s">
<text x="24" y="154" class="tt" style="font-size:{title_size}px">{esc(p['title'])}</text>
<text x="26" y="178" class="sub">{esc(p['subtitle'].upper())}</text>
{''.join(f'<text x="26" y="{208 + j * 20}" class="ds">{esc(l)}</text>' for j, l in enumerate(desc))}
</g>
<path d="M26 266H{W - 26}" stroke="{C['line']}"/>
<g class="up" style="animation-delay:.3s">{''.join(mets)}</g>"""
    return svg_doc(W, H, body, css, title=f"{p['title']} — {p['subtitle']}",
                   desc=p["description"] + " " + "; ".join(f"{v} {l}" for v, l in p["metrics"]), defs=pdefs)


# ════════════════════════════════════════════════════════════════════════════
# FOOTER
# ════════════════════════════════════════════════════════════════════════════
def footer(cfg):
    W, H = 1000, 210
    gap = 14
    cols = int((W - 80) // gap)
    x0 = (W - (cols - 1) * gap) / 2
    strip = []
    for i in range(cols):
        x = x0 + i * gap
        strip.append(f'<circle cx="{x:.1f}" cy="{H - 40}" r="2.2" fill="#2A2A2A"/>'
                     f'<circle class="sw" cx="{x:.1f}" cy="{H - 40}" r="2.2" fill="{C["orange"]}" style="animation-delay:{i * 0.035:.2f}s"/>')
    title = "Thanks for stopping by."
    defs = dot_pattern("dots", 18, 0.9, "#1A1A1A") + f'<clipPath id="frame"><rect width="{W}" height="{H}" rx="20"/></clipPath>'
    css = fonts_css("grotesk-700", "smono-400", "smono-700") + FADE + f"""
.th{{font-family:{FAMILY['sans']};font-weight:700;font-size:44px;letter-spacing:-1.5px;fill:{C['text']};}}
.tg{{font-family:{FAMILY['mono']};font-size:11px;fill:{C['muted']};letter-spacing:3px;}}
.eof{{font-family:{FAMILY['mono']};font-weight:700;font-size:10px;fill:{C['orange']};letter-spacing:3px;}}
.sw{{opacity:0;animation:sw 4.5s ease-in-out infinite;}}
@keyframes sw{{0%,100%{{opacity:0}}6%{{opacity:1}}16%{{opacity:0}}}}"""
    eof_w = measure("END OF FILE", "smono-700", 10, 3)
    body = f"""<g clip-path="url(#frame)"><rect width="{W}" height="{H}" fill="{C['bg']}"/><rect width="{W}" height="{H}" fill="url(#dots)"/>
<path d="M{W / 2 - eof_w / 2 - 50:.0f} 46.5h36 M{W / 2 + eof_w / 2 + 14:.0f} 46.5h36" stroke="{C['line2']}"/>
<text x="{W / 2}" y="50" text-anchor="middle" class="eof">END OF FILE</text>
<g class="up" style="animation-delay:.2s">{accent_dots(title, W / 2, 104, 'th').replace('<text ', '<text text-anchor="middle" ', 1)}</g>
<g class="up" style="animation-delay:.4s"><text x="{W / 2}" y="134" text-anchor="middle" class="tg">LET'S BUILD SOMETHING WORTH SHIPPING</text></g>
{''.join(strip)}
{ticks(0, 0, W, H, size=11, color=C['orange'], width=1.6, inset=14)}</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="19.5" stroke="{C['line']}"/>"""
    return svg_doc(W, H, body, css, title="Thanks for stopping by", desc="Footer", defs=defs)


# ════════════════════════════════════════════════════════════════════════════
# SMALL DIVIDER ("More builds")
# ════════════════════════════════════════════════════════════════════════════
def subheading(label, right):
    W, H = 1000, 44
    lab_w = measure(label.upper(), "smono-700", 11, 3)
    r = right.upper()
    r_w = measure(r, "smono-400", 10, 2)
    css = fonts_css("smono-400", "smono-700") + f"""
.lb{{font-family:{FAMILY['mono']};font-weight:700;font-size:11px;letter-spacing:3px;fill:{C['text']};}}
.rt{{font-family:{FAMILY['mono']};font-size:10px;letter-spacing:2px;fill:{C['dim']};}}"""
    body = f"""<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="10" fill="#0F0F0F" stroke="{C['line']}"/>
<path d="M22 22h10M27 17v10" stroke="{C['orange']}" stroke-width="1.8"/>
<text x="44" y="26" class="lb">{esc(label.upper())}</text>
<path d="M{44 + lab_w + 20:.0f} 21.5H{W - 26 - r_w - 20:.0f}" stroke="{C['line']}" stroke-dasharray="2 4"/>
<text x="{W - 26}" y="25.5" text-anchor="end" class="rt">{esc(r)}</text>"""
    return svg_doc(W, H, body, css, title=label, desc=right, defs="")


def _chips(tags, x, y, max_x, size=9.5):
    out, cx = [], x
    for t in tags:
        t = t.upper()
        w = measure(t, "smono-400", size, 1) + 18
        if cx + w > max_x:
            break
        out.append(f'<rect x="{cx + .5:.1f}" y="{y + .5}" width="{w:.1f}" height="21" rx="4" fill="#161616" stroke="{C["line2"]}"/>'
                   f'<text x="{cx + 9:.1f}" y="{y + 14.5}" class="tag">{esc(t)}</text>')
        cx += w + 8
    return "".join(out)


TAG_CSS = f".tag{{font-family:{FAMILY['mono']};font-size:9.5px;letter-spacing:1px;fill:{C['muted']};}}"


# ════════════════════════════════════════════════════════════════════════════
# COMPACT PROJECT CARD
# ════════════════════════════════════════════════════════════════════════════
def project_mini(p, idx):
    W, H = 490, 236
    pdefs, pbody = panel(W, H, 16, "pm", tick=True)
    linked = bool(p.get("repo"))
    chip = "VIEW REPO" if linked else p.get("status", "REPO SOON")
    chip_w = measure(chip, "smono-700", 10, 1.5) + 24 + (16 if linked else 0)
    cx0 = W - 26 - chip_w
    text_w = 292
    title_size = fit_size(p["title"], "grotesk-700", text_w, 25, spacing=-0.6)
    sub = p["subtitle"].upper()
    sub_size = min(10.5, max(8.5, 10.5 * text_w / max(measure(sub, "smono-400", 10.5, .5), 1)))
    desc = wrap(p["description"], "grotesk-400", 13.5, text_w, 3)
    chip_rect = (f'<rect x="{cx0:.1f}" y="24" width="{chip_w:.1f}" height="22" rx="4" fill="{C["orange"]}"/>' if linked else
                 f'<rect x="{cx0 + .5:.1f}" y="24.5" width="{chip_w:.1f}" height="21" rx="4" stroke="{C["line2"]}" fill="#161616"/>')
    arrow = line_icon("arrow", cx0 + chip_w - 24, 28, 12, stroke=C["bg"], width=2.4) if linked else ""
    css = fonts_css("grotesk-700", "grotesk-400", "smono-400", "smono-700") + FADE + TAG_CSS + f"""
.idx{{font-family:{FAMILY['mono']};font-weight:700;font-size:12px;fill:{C['orange']};letter-spacing:1px;}}
.per{{font-family:{FAMILY['mono']};font-size:10px;fill:{C['dim']};letter-spacing:1.5px;}}
.chip{{font-family:{FAMILY['mono']};font-weight:700;font-size:10px;letter-spacing:1.5px;}}
.tt{{font-family:{FAMILY['sans']};font-weight:700;letter-spacing:-.6px;fill:{C['text']};}}
.sub{{font-family:{FAMILY['mono']};letter-spacing:.5px;fill:{C['orange']};}}
.ds{{font-family:{FAMILY['sans']};font-size:13.5px;fill:{C['muted']};}}""" + VIZ_CSS
    body = f"""{pbody}
<g class="up"><text x="26" y="40" class="idx">{idx:02d}</text><text x="50" y="40" class="per">{esc(p['period'])}</text>
{chip_rect}<text x="{cx0 + 12:.1f}" y="39" class="chip" fill="{C['bg'] if linked else C['muted']}">{esc(chip)}</text>{arrow}</g>
{_viz(p.get('viz', ''), 336, 66, 128, 78)}
<g class="up" style="animation-delay:.15s">
<text x="24" y="92" class="tt" style="font-size:{title_size}px">{esc(p['title'])}</text>
<text x="26" y="114" class="sub" style="font-size:{sub_size:.1f}px">{esc(sub)}</text>
{''.join(f'<text x="26" y="{140 + j * 19}" class="ds">{esc(l)}</text>' for j, l in enumerate(desc))}
</g>
<g class="up" style="animation-delay:.3s">{_chips(p.get('tags', []), 26, H - 44, W - 26)}</g>"""
    return svg_doc(W, H, body, css, title=f"{p['title']} — {p['subtitle']}",
                   desc=p["description"] + " Tech: " + ", ".join(p.get("tags", [])), defs=pdefs)


# ════════════════════════════════════════════════════════════════════════════
# EXPERIENCE + EDUCATION + COMMUNITY
# ════════════════════════════════════════════════════════════════════════════
def experience(cfg):
    W = 1000
    LW, gap = 612, 14
    RX, RW = LW + gap, W - LW - gap
    exp = cfg["experience"]

    # ── left: work timeline ────────────────────────────────────────────────
    items, y = [], 84
    nodes = []
    text_x, wrap_w = 66, LW - 66 - 30
    for i, e in enumerate(exp):
        top = y
        role_w = measure(e["role"], "grotesk-700", 19, -0.4)
        now = (f'<rect x="{text_x + role_w + 12:.1f}" y="{top - 3}" width="40" height="18" rx="4" fill="{C["orange"]}"/>'
               f'<text x="{text_x + role_w + 32:.1f}" y="{top + 9.5}" text-anchor="middle" class="now">NOW</text>') if e.get("current") else ""
        parts = [f'<text x="{text_x}" y="{top + 12}" class="role">{esc(e["role"])}</text>{now}',
                 f'<text x="{LW - 28}" y="{top + 10}" text-anchor="end" class="per">{esc(e["period"])}</text>',
                 f'<text x="{text_x}" y="{top + 33}" class="org">{esc(e["org"].upper())}</text>']
        ly = top + 60
        for pt in e["points"]:
            lines = wrap(pt, "grotesk-400", 13.5, wrap_w - 14)
            parts.append(f'<rect x="{text_x}" y="{ly - 8}" width="4" height="4" fill="{C["orange"]}"/>')
            for j, ln in enumerate(lines):
                parts.append(f'<text x="{text_x + 14}" y="{ly + j * 19}" class="pt">{esc(ln)}</text>')
            ly += len(lines) * 19 + 7
        if e.get("tags"):
            parts.append(_chips(e["tags"], text_x, ly + 2, LW - 28))
            ly += 30
        nodes.append((top + 6, e.get("current")))
        items.append(f'<g class="up" style="animation-delay:{0.2 + i * 0.2:.2f}s">{"".join(parts)}</g>')
        y = ly + 30
    left_h = y - 6

    # ── right: education ───────────────────────────────────────────────────
    ed = cfg["education"]
    deg_lines = wrap(ed["degree"], "grotesk-700", 17, RW - 48)
    ey = 84
    edu = [f'<text x="{RX + 24}" y="{ey + 12 + j * 22}" class="deg">{esc(l)}</text>' for j, l in enumerate(deg_lines)]
    ey += 12 + (len(deg_lines) - 1) * 22
    edu.append(f'<text x="{RX + 24}" y="{ey + 22}" class="org">{esc(ed["school"].upper())}</text>'
               f'<text x="{RX + 24}" y="{ey + 40}" class="per">{esc(ed["period"])}</text>')
    sy = ey + 92
    frac = float(ed["score"]) / float(ed["score_max"])
    score_w = measure(ed["score"], "grotesk-700", 42, -1.5)
    edu.append(f'<text x="{RX + 22}" y="{sy}" class="score">{esc(ed["score"])}</text>'
               f'<text x="{RX + 30 + score_w:.1f}" y="{sy - 4}" class="per">/ {esc(ed["score_max"])}  {esc(ed["score_label"])}</text>'
               f'<rect x="{RX + 24}" y="{sy + 16}" width="{RW - 48}" height="5" rx="2.5" fill="#1F1F1F"/>'
               f'<rect class="bar" x="{RX + 24}" y="{sy + 16}" width="{(RW - 48) * frac:.1f}" height="5" rx="2.5" fill="{C["orange"]}"/>')
    edu_h = sy + 44

    # ── right: community ───────────────────────────────────────────────────
    cy0 = edu_h + gap
    comm = []
    cy = cy0 + 84
    for k, c in enumerate(cfg.get("community", [])):
        note = wrap(c["note"], "grotesk-400", 12.5, RW - 48 - 40)
        comm.append(f'<g class="up" style="animation-delay:{0.5 + k * 0.15:.2f}s">'
                    f'<rect x="{RX + 24.5}" y="{cy - 13.5}" width="29" height="29" rx="7" fill="#181818" stroke="{C["line2"]}"/>'
                    f'{line_icon(c["icon"], RX + 31, cy - 7, 16)}'
                    f'<text x="{RX + 66}" y="{cy}" class="crole">{esc(c["role"])}</text>'
                    f'<text x="{RX + 66}" y="{cy + 18}" class="org">{esc(c["org"].upper())}</text>'
                    f'<text x="{RX + 66}" y="{cy + 34}" class="per">{esc(c["period"])}</text>'
                    + "".join(f'<text x="{RX + 66}" y="{cy + 54 + j * 17}" class="note">{esc(l)}</text>' for j, l in enumerate(note))
                    + '</g>')
        cy += 54 + len(note) * 17 + 22
    right_h = cy - 4

    H = int(max(left_h, right_h))
    comm_h = H - cy0

    # timeline rail
    first_y, last_y = nodes[0][0], nodes[-1][0]
    rail = (f'<path d="M40 {first_y}V{last_y}" stroke="{C["line2"]}" stroke-width="1.5"/>'
            f'<path class="rail" d="M40 {first_y}V{last_y}" stroke="{C["orange"]}" stroke-width="1.5"/>')
    for ny, cur in nodes:
        if cur:
            rail += (f'<circle class="ping" cx="40" cy="{ny}" r="7" stroke="{C["orange"]}" stroke-width="1.5"/>'
                     f'<circle cx="40" cy="{ny}" r="6" fill="{C["orange"]}"/>')
        else:
            rail += f'<circle cx="40" cy="{ny}" r="5.5" fill="#0E0E0E" stroke="#8A8A8A" stroke-width="1.6"/>'

    def box(x, y, w, h, uid):
        return (f'<rect x="{x + .5}" y="{y + .5}" width="{w - 1}" height="{h - 1}" rx="16" fill="url(#bg)" stroke="{C["line"]}"/>'
                + ticks(x, y, w, h, color=C["faint"], width=1.2))

    def head(x, y, icon, title, right=""):
        return (f'{line_icon(icon, x + 24, y + 26, 20)}<text x="{x + 54}" y="{y + 42}" class="ttl">{esc(title)}</text>'
                + (f'<text x="{x + (LW if x == 0 else RW) - 28}" y="{y + 41}" text-anchor="end" class="per">{esc(right)}</text>' if right else "")
                + f'<path d="M{x + 24} {y + 60}H{x + (LW if x == 0 else RW) - 24}" stroke="{C["line"]}"/>')

    css = fonts_css("grotesk-700", "grotesk-500", "grotesk-400", "smono-400", "smono-700") + FADE + TAG_CSS + f"""
.ttl{{font-family:{FAMILY['sans']};font-weight:500;font-size:17px;letter-spacing:-.2px;fill:{C['text']};}}
.role{{font-family:{FAMILY['sans']};font-weight:700;font-size:19px;letter-spacing:-.4px;fill:{C['text']};}}
.crole{{font-family:{FAMILY['sans']};font-weight:700;font-size:15px;letter-spacing:-.2px;fill:{C['text']};}}
.deg{{font-family:{FAMILY['sans']};font-weight:700;font-size:17px;letter-spacing:-.3px;fill:{C['text']};}}
.org{{font-family:{FAMILY['mono']};font-size:10.5px;letter-spacing:1px;fill:{C['orange']};}}
.per{{font-family:{FAMILY['mono']};font-size:9.5px;letter-spacing:1.3px;fill:{C['dim']};}}
.pt{{font-family:{FAMILY['sans']};font-size:13.5px;fill:{C['muted']};}}
.note{{font-family:{FAMILY['sans']};font-size:12.5px;fill:{C['muted']};}}
.now{{font-family:{FAMILY['mono']};font-weight:700;font-size:9px;letter-spacing:1.5px;fill:{C['bg']};}}
.score{{font-family:{FAMILY['sans']};font-weight:700;font-size:42px;letter-spacing:-1.5px;fill:{C['text']};}}
.bar{{animation:bar 1.4s cubic-bezier(.6,0,.2,1) both .4s;transform-box:fill-box;transform-origin:left;}}
@keyframes bar{{from{{transform:scaleX(0)}}}}
.rail{{animation:rail 1.6s cubic-bezier(.6,0,.2,1) both .2s;transform-box:fill-box;transform-origin:top;}}
@keyframes rail{{from{{transform:scaleY(0)}}}}
.ping{{animation:ping 2s ease-out infinite;transform-box:fill-box;transform-origin:center;}}
@keyframes ping{{0%{{transform:scale(1);opacity:.9}}100%{{transform:scale(2.4);opacity:0}}}}"""
    defs = grad("bg", [(0, "#151515"), (1, "#0E0E0E")], 0.3, 1)
    body = (box(0, 0, LW, H, "l") + head(0, 0, "briefcase", "Work experience", f"{len(exp):02d} ROLES") + rail + "".join(items)
            + box(RX, 0, RW, edu_h, "e") + head(RX, 0, "cap", "Education") + f'<g class="up" style="animation-delay:.3s">{"".join(edu)}</g>'
            + box(RX, cy0, RW, comm_h, "c") + head(RX, cy0, "people", "Leadership & community") + "".join(comm))
    desc = " | ".join(f"{e['role']}, {e['org']} ({e['period']}): " + " ".join(e["points"]) for e in exp)
    desc += f" | Education: {ed['degree']}, {ed['school']}, {ed['period']}, {ed['score_label']} {ed['score']}/{ed['score_max']}"
    desc += " | " + " | ".join(f"{c['role']}, {c['org']} ({c['period']}): {c['note']}" for c in cfg.get("community", []))
    return svg_doc(W, H, body, css, title="Experience and education", desc=desc, defs=defs)


# ════════════════════════════════════════════════════════════════════════════
# ACHIEVEMENTS
# ════════════════════════════════════════════════════════════════════════════
def achievements(cfg):
    items = cfg["achievements"]
    W, gap, th = 1000, 14, 142
    tw = (W - gap) / 2
    rows = (len(items) + 1) // 2
    H = rows * th + (rows - 1) * gap
    css = fonts_css("grotesk-700", "grotesk-400", "smono-400", "smono-700") + FADE + f"""
.tt{{font-family:{FAMILY['sans']};font-weight:700;font-size:18px;letter-spacing:-.3px;fill:{C['text']};}}
.meta{{font-family:{FAMILY['mono']};font-size:9.5px;letter-spacing:1.3px;fill:{C['dim']};}}
.tx{{font-family:{FAMILY['sans']};font-size:13px;fill:{C['muted']};}}
.bd{{font-family:{FAMILY['mono']};font-weight:700;font-size:11px;letter-spacing:2px;fill:{C['orange']};}}
.frame{{animation:frame 1.4s cubic-bezier(.6,0,.2,1) both;}}
@keyframes frame{{from{{stroke-dashoffset:256}}}}
.glint{{animation:glint 5s ease-in-out infinite;}}
@keyframes glint{{0%,70%{{transform:translateX(-60px)}}100%{{transform:translateX(90px)}}}}"""
    defs = (grad("bg", [(0, "#151515"), (1, "#0E0E0E")], 0.3, 1)
            + grad("gl", [(0, "#fff0"), (0.5, "#ffffff22"), (1, "#fff0")]))
    tiles = []
    for i, a in enumerate(items):
        col, row = i % 2, i // 2
        x, y = col * (tw + gap), row * (th + gap)
        bx, by = x + 22, y + 22
        txt = wrap(a["text"], "grotesk-400", 13, tw - 108 - 24, 3)
        tiles.append(
            f'<g class="up" style="animation-delay:{0.1 + i * 0.12:.2f}s">'
            f'<rect x="{x + .5:.1f}" y="{y + .5}" width="{tw - 1:.1f}" height="{th - 1}" rx="14" fill="url(#bg)" stroke="{C["line"]}"/>'
            f'<clipPath id="bc{i}"><rect x="{bx}" y="{by}" width="64" height="64" rx="12"/></clipPath>'
            f'<rect x="{bx}" y="{by}" width="64" height="64" rx="12" fill="#161616"/>'
            f'<g clip-path="url(#bc{i})"><rect class="glint" x="{bx - 30}" y="{by}" width="30" height="64" fill="url(#gl)" transform="skewX(-20)" style="animation-delay:{i * 0.6:.1f}s"/></g>'
            f'<rect class="frame" x="{bx + .75}" y="{by + .75}" width="62.5" height="62.5" rx="11.5" stroke="{C["orange"]}" stroke-width="1.5" pathLength="256" stroke-dasharray="256" style="animation-delay:{0.3 + i * 0.12:.2f}s"/>'
            f'{line_icon(a["icon"], bx + 17, by + 17, 30)}'
            f'<text x="{bx + 32}" y="{by + 86}" text-anchor="middle" class="bd">{esc(a["badge"])}</text>'
            f'<text x="{x + 108:.1f}" y="{y + 44}" class="tt">{esc(a["title"])}</text>'
            f'<text x="{x + 108:.1f}" y="{y + 64}" class="meta">{esc((a["org"] + "  ·  " + a["date"]).upper())}</text>'
            + "".join(f'<text x="{x + 108:.1f}" y="{y + 90 + j * 18}" class="tx">{esc(l)}</text>' for j, l in enumerate(txt))
            + '</g>')
    desc = "; ".join(f"{a['title']} ({a['org']}, {a['date']}): {a['text']}" for a in items)
    return svg_doc(W, H, "".join(tiles), css, title="Achievements", desc=desc, defs=defs)
