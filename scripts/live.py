"""Live SVGs built from your real GitHub data: Contribution City, the stats
dashboard and the daily quote. Dark Industrial style."""
import datetime as dt
import math
import random

from kit import (C, FAMILY, esc, fonts_css, measure, wrap, fmt_num, svg_doc, grad,
                 dot_pattern, ticks, panel, moving_grid, glow_filter)
from cards import line_icon

def _mix(a, b, t):
    a, b = a.lstrip("#"), b.lstrip("#")
    return "#" + "".join(f"{round(int(a[i:i + 2], 16) * (1 - t) + int(b[i:i + 2], 16) * t):02X}" for i in (0, 2, 4))


# window colors, derived from the accent: off -> brightest
LEVEL_COLORS = ["#242424", _mix("#242424", C["orange"], .3), _mix("#242424", C["orange"], .6),
                _mix("#242424", C["orange"], .88), C["orange2"]]


# ── data helpers ────────────────────────────────────────────────────────────
def streaks(days):
    """days: list of (date_str, count) oldest→newest."""
    longest = run = 0
    for _, c in days:
        run = run + 1 if c > 0 else 0
        longest = max(longest, run)
    current = 0
    seq = list(days)
    if seq and seq[-1][1] == 0:      # today may simply not have commits yet
        seq = seq[:-1]
    for _, c in reversed(seq):
        if c > 0:
            current += 1
        else:
            break
    return current, longest


def levels(counts):
    nz = sorted(c for c in counts if c > 0)
    if not nz:
        return lambda c: 0
    q = [nz[max(int(len(nz) * f) - 1, 0)] for f in (0.25, 0.5, 0.75)]

    def lvl(c):
        if c <= 0:
            return 0
        if c <= q[0]:
            return 1
        if c <= q[1]:
            return 2
        if c <= q[2]:
            return 3
        return 4
    return lvl


# ════════════════════════════════════════════════════════════════════════════
# CONTRIBUTION CITY
# ════════════════════════════════════════════════════════════════════════════
def city(data):
    W, H, HZ = 1000, 400, 262
    weeks = data["weeks"]
    days = [d for w in weeks for d in w]
    total = data["total"]
    cur, longest = streaks(days)
    lvl = levels([c for _, c in days])
    busiest = max(days, key=lambda d: d[1]) if days else ("", 0)
    week_tot = [sum(c for _, c in w) for w in weeks]
    mx = max(week_tot) if week_tot and max(week_tot) > 0 else 1

    n = len(weeks)
    x0, x1 = 34, W - 34
    slot = (x1 - x0) / max(n, 1)
    tw = max(slot * 0.72, 4)
    win_h, pitch = 3.3, 5.2
    hmin, hspan = 50, 146

    towers = []
    rnd = random.Random(7)
    top_weeks = set(sorted(range(n), key=lambda i: week_tot[i], reverse=True)[:5]) if total else set()
    for i, w in enumerate(weeks):
        frac = math.sqrt(week_tot[i] / mx) if total else 0
        h = hmin + hspan * frac if week_tot[i] else hmin - 12
        x = x0 + i * slot + (slot - tw) / 2
        y = HZ - h
        wins = []
        ww = max(tw * 0.5, 3)
        wx = x + (tw - ww) / 2
        for d_i, (_, c) in enumerate(w):
            lv = lvl(c)
            wy = y + 7 + d_i * pitch
            delay = 0.9 + i * 0.026 + rnd.uniform(0.1, 0.6)
            wins.append(f'<rect class="{"win lit" if lv else "win"}" x="{wx:.1f}" y="{wy:.1f}" width="{ww:.1f}" height="{win_h}" '
                        f'fill="{LEVEL_COLORS[lv]}" style="animation-delay:{delay:.2f}s"/>')
        cap = antenna = ""
        stroke = "#3A3A3A" if frac > 0.5 else "#2C2C2C"
        if i in top_weeks:
            ax = x + tw / 2
            cap = f'<rect x="{x:.1f}" y="{y - 1:.1f}" width="{tw:.1f}" height="2" fill="{C["orange"]}"/>'
            antenna = (f'<line x1="{ax:.1f}" x2="{ax:.1f}" y1="{y:.1f}" y2="{y - 12:.1f}" stroke="#4A4A4A" stroke-width="1"/>'
                       f'<circle class="beacon" cx="{ax:.1f}" cy="{y - 13:.1f}" r="1.8" fill="{C["orange"]}" style="animation-delay:-{i * 0.3 % 2:.1f}s"/>')
        towers.append(
            f'<g class="tower" style="animation-delay:{0.3 + i * 0.026:.2f}s">'
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{tw:.1f}" height="{h + 2:.1f}" fill="url(#tw)" stroke="{stroke}" stroke-width=".8"/>'
            f'{cap}{antenna}{"".join(wins)}</g>')

    hud = [
        ("bolt", fmt_num(total), "CONTRIBUTIONS / 12 MO"),
        ("flame", f"{cur}d", "CURRENT STREAK"),
        ("flame", f"{longest}d", "LONGEST STREAK"),
        ("calendar", fmt_num(busiest[1]) if busiest[1] else "-",
         "BUSIEST DAY" + (f" · {dt.date.fromisoformat(busiest[0]).strftime('%d %b').upper()}" if busiest[1] else "")),
    ]
    bw, gap, bh = 222, 12, 58
    bx0 = (W - (4 * bw + 3 * gap)) / 2
    by = H - bh - 18
    hud_svg = []
    for j, (ic, v, lab) in enumerate(hud):
        bx = bx0 + j * (bw + gap)
        hud_svg.append(
            f'<g class="hud" style="animation-delay:{1.6 + j * 0.12:.2f}s">'
            f'<rect x="{bx:.1f}" y="{by}" width="{bw}" height="{bh}" rx="10" fill="#0C0C0C" fill-opacity=".94" stroke="{C["line2"]}"/>'
            f'{line_icon(ic, bx + 16, by + 17, 22)}'
            f'<text x="{bx + 50:.1f}" y="{by + 28}" class="hv">{esc(v)}</text>'
            f'<text x="{bx + 50:.1f}" y="{by + 44}" class="hl">{esc(lab)}</text></g>')

    first = dt.date.fromisoformat(days[0][0]).strftime("%b %Y").upper() if days else ""
    last = dt.date.fromisoformat(days[-1][0]).strftime("%b %Y").upper() if days else ""
    empty = ""
    if total == 0:
        empty = (f'<rect x="{W / 2 - 180}" y="76" width="360" height="60" rx="10" fill="#0C0C0C" fill-opacity=".94" stroke="{C["line2"]}"/>'
                 f'<text x="{W / 2}" y="104" text-anchor="middle" class="empty">The city is waiting.</text>'
                 f'<text x="{W / 2}" y="123" text-anchor="middle" class="hl">EVERY COMMIT RAISES A TOWER</text>')

    defs = (dot_pattern("dots", 18, 0.9, "#1A1A1A")
            + f'<linearGradient id="haze" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C["orange"]}" stop-opacity="0"/>'
              f'<stop offset="1" stop-color="{C["orange"]}" stop-opacity=".18"/></linearGradient>'
            + f'<radialGradient id="sunhalo" cx=".5" cy="1" r=".6"><stop offset="0" stop-color="{C["orange"]}" stop-opacity=".22"/>'
              f'<stop offset="1" stop-color="{C["orange"]}" stop-opacity="0"/></radialGradient>'
            + grad("floor", [(0, "#141414"), (1, "#0A0A0A")], 0, 1)
            + grad("tw", [(0, "#1D1D1D"), (1, "#101010")], 0, 1)
            + grad("fade", [(0, "#fff"), (1, "#000")], 0, 1)
            + f'<mask id="reflm"><rect y="{HZ}" width="{W}" height="120" fill="url(#fade)" opacity=".45"/></mask>'
            + f'<clipPath id="frame"><rect width="{W}" height="{H}" rx="20"/></clipPath>'
            + f'<clipPath id="above"><rect width="{W}" height="{HZ}"/></clipPath>'
            + f'<clipPath id="floorclip"><rect y="{HZ}" width="{W}" height="{H - HZ}"/></clipPath>'
            + glow_filter("glh", 2.5, .9))
    css = fonts_css("grotesk-700", "grotesk-500", "smono-400") + f"""
.tower{{animation:rise 1s cubic-bezier(.2,.9,.25,1) both;}}
@keyframes rise{{from{{transform:translateY(230px)}}}}
.lit{{animation:lit .25s steps(2) both;}}
@keyframes lit{{from{{fill:{LEVEL_COLORS[0]}}}}}
.beacon{{animation:bc 1.6s steps(1) infinite;}}@keyframes bc{{50%{{opacity:.15}}}}
.hud{{animation:hud .7s ease-out both;}}@keyframes hud{{from{{opacity:0;transform:translateY(10px)}}}}
.hv{{font-family:{FAMILY['sans']};font-weight:700;font-size:21px;letter-spacing:-.5px;fill:{C['text']};}}
.hl{{font-family:{FAMILY['mono']};font-size:9.5px;fill:{C['dim']};letter-spacing:1.3px;}}
.ttl{{font-family:{FAMILY['sans']};font-weight:500;font-size:17px;fill:{C['text']};letter-spacing:-.2px;}}
.leg{{font-family:{FAMILY['mono']};font-size:9.5px;fill:{C['dim']};letter-spacing:1.3px;}}
.empty{{font-family:{FAMILY['sans']};font-weight:700;font-size:19px;fill:{C['text']};letter-spacing:-.3px;}}"""
    lx_end = W - 34
    more_w = measure("MORE", "smono-400", 9.5, 1.3)
    sq0 = lx_end - more_w - 10 - 5 * 12
    legend = "".join(f'<rect x="{sq0 + k * 12:.1f}" y="27" width="8" height="8" rx="1.5" fill="{LEVEL_COLORS[k]}"/>' for k in range(5))
    body = f"""<g clip-path="url(#frame)">
<rect width="{W}" height="{H}" fill="{C['bg']}"/>
<rect width="{W}" height="{HZ}" fill="url(#dots)"/>
<rect y="{HZ - 130}" width="{W}" height="130" fill="url(#haze)"/>
<ellipse cx="{W / 2}" cy="{HZ}" rx="420" ry="150" fill="url(#sunhalo)"/>
<g clip-path="url(#above)" id="cityg">{''.join(towers)}</g>
<rect y="{HZ}" width="{W}" height="{H - HZ}" fill="url(#floor)"/>
<g clip-path="url(#floorclip)">
<g mask="url(#reflm)" opacity=".35"><use href="#cityg" xlink:href="#cityg" transform="matrix(1 0 0 -1 0 {2 * HZ})"/></g>
{moving_grid(0, W, HZ, H, W / 2, n_h=8, color='#2A2A2A', dur=3.6)}</g>
<rect x="0" y="{HZ - .6}" width="{W}" height="1.2" fill="{C['orange']}" filter="url(#glh)"/>
<rect x="34" y="24" width="7" height="7" fill="{C['orange']}"/>
<text x="50" y="32" class="ttl">Contribution City</text>
<text x="34" y="52" class="leg">1 TOWER = 1 WEEK  ·  1 WINDOW = 1 DAY  ·  TALLER = BUSIER</text>
<text x="{sq0 - 8:.1f}" y="34.5" text-anchor="end" class="leg">LESS</text>{legend}<text x="{lx_end}" y="34.5" text-anchor="end" class="leg">MORE</text>
<text x="34" y="{HZ + 20}" class="leg">{first}</text><text x="{W - 34}" y="{HZ + 20}" text-anchor="end" class="leg">{last}</text>
{empty}
{''.join(hud_svg)}
{ticks(0, 0, W, H, size=11, color=C['orange'], width=1.6, inset=12)}
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="19.5" stroke="{C['line']}"/>"""
    desc = (f"{total} contributions in the last 12 months. Current streak {cur} days, longest streak {longest} days."
            + (f" Busiest day {busiest[0]} with {busiest[1]} contributions." if busiest[1] else ""))
    return svg_doc(W, H, body, css, title="Contribution City", desc=desc, defs=defs)


# ════════════════════════════════════════════════════════════════════════════
# STATS DASHBOARD
# ════════════════════════════════════════════════════════════════════════════
LANG_COLORS = [C["orange"], C["orange2"], C["orange3"], "#A0A0A0", "#6E6E6E", "#474747"]


def stats(data, today):
    W, H = 1000, 300
    pdefs, pbody = panel(W, H, 16, "sd", tick=True)
    s = data["stats"]
    rows = [
        ("star", fmt_num(s["stars"]), "STARS EARNED"),
        ("commit", fmt_num(s["commits"]), "COMMITS / 12 MO"),
        ("pr", fmt_num(s["prs"]), "PULL REQUESTS"),
        ("issue", fmt_num(s["issues"]), "ISSUES"),
        ("repo", fmt_num(s["repos"]), "PUBLIC REPOS"),
        ("people", fmt_num(s["followers"]), "FOLLOWERS"),
    ]
    left = []
    for i, (ic, v, lab) in enumerate(rows):
        col, row = i % 2, i // 2
        x, y = 34, 104 + row * 60
        x += col * 196
        left.append(f'<g class="in" style="animation-delay:{0.2 + i * 0.08:.2f}s">'
                    f'<rect x="{x + .5}" y="{y - 19.5}" width="39" height="39" rx="9" fill="#181818" stroke="{C["line2"]}"/>'
                    f'{line_icon(ic, x + 9, y - 11, 22)}'
                    f'<text x="{x + 54}" y="{y + 3}" class="v">{esc(v)}</text>'
                    f'<text x="{x + 54}" y="{y + 18}" class="l">{esc(lab)}</text></g>')

    days = [d for w in data["weeks"] for d in w]
    active = sum(1 for _, c in days if c > 0)
    span = max(len(days), 1)
    frac = active / span
    rcx, rcy, rr = 528, 158, 64
    circ = 2 * math.pi * rr
    ticks_ring = "".join(
        f'<line x1="{rcx + (rr + 14) * math.cos(a):.1f}" y1="{rcy + (rr + 14) * math.sin(a):.1f}" '
        f'x2="{rcx + (rr + 19) * math.cos(a):.1f}" y2="{rcy + (rr + 19) * math.sin(a):.1f}" stroke="{C["faint"] if k % 3 else C["dim"]}"/>'
        for k, a in enumerate(i * 2 * math.pi / 36 for i in range(36)))
    ring = (f'{ticks_ring}<circle cx="{rcx}" cy="{rcy}" r="{rr}" stroke="#1F1F1F" stroke-width="8"/>'
            + (f'<circle class="ring" cx="{rcx}" cy="{rcy}" r="{rr}" stroke="{C["orange"]}" stroke-width="8" stroke-linecap="round" '
               f'stroke-dasharray="{circ * frac:.1f} {circ:.1f}" transform="rotate(-90 {rcx} {rcy})"/>' if active else "")
            + f'<text x="{rcx}" y="{rcy + 7}" text-anchor="middle" class="rv">{active}</text>'
            f'<text x="{rcx}" y="{rcy + 27}" text-anchor="middle" class="l">ACTIVE DAYS</text>'
            f'<text x="{rcx}" y="{rcy + rr + 46}" text-anchor="middle" class="l">{round(frac * 100)}% OF THE YEAR</text>')

    langs = data["languages"][:6]
    tot = sum(b for _, b in langs) or 1
    lx, lw = 652, 314
    lang_svg = [f'<text x="{lx}" y="60" class="h">Top languages</text>']
    if langs:
        acc = 0
        for i, (name, b) in enumerate(langs):
            seg = lw * b / tot
            lang_svg.append(f'<rect class="seg" x="{lx + acc:.1f}" y="78" width="{max(seg - 2, 1):.1f}" height="8" rx="2" fill="{LANG_COLORS[i]}" style="animation-delay:{0.3 + i * 0.1:.2f}s"/>')
            acc += seg
        for i, (name, b) in enumerate(langs):
            col, row = i % 2, i // 2
            x, y = lx + col * 160, 126 + row * 46
            pct = 100 * b / tot
            lang_svg.append(f'<g class="in" style="animation-delay:{0.5 + i * 0.08:.2f}s">'
                            f'<rect x="{x}" y="{y - 9}" width="9" height="9" rx="2" fill="{LANG_COLORS[i]}"/>'
                            f'<text x="{x + 18}" y="{y}" class="ln">{esc(name)}</text>'
                            f'<text x="{x + 18}" y="{y + 17}" class="l">{pct:.1f}%</text></g>')
    else:
        lang_svg.append(f'<text x="{lx}" y="132" class="ln">No public code yet.</text>'
                        f'<text x="{lx}" y="152" class="l">PUSH A REPO AND THIS FILLS IN</text>')

    css = fonts_css("grotesk-700", "grotesk-500", "smono-400") + f"""
.h{{font-family:{FAMILY['sans']};font-weight:500;font-size:17px;letter-spacing:-.2px;fill:{C['text']};}}
.up{{font-family:{FAMILY['mono']};font-size:9.5px;fill:{C['dim']};letter-spacing:1.3px;}}
.v{{font-family:{FAMILY['sans']};font-weight:700;font-size:22px;letter-spacing:-.5px;fill:{C['text']};}}
.rv{{font-family:{FAMILY['sans']};font-weight:700;font-size:32px;letter-spacing:-1px;fill:{C['text']};}}
.l{{font-family:{FAMILY['mono']};font-size:9.5px;fill:{C['dim']};letter-spacing:1.2px;}}
.ln{{font-family:{FAMILY['sans']};font-weight:500;font-size:14.5px;fill:{C['text']};}}
.in{{animation:in .7s ease-out both;}}@keyframes in{{from{{opacity:0;transform:translateY(8px)}}}}
.ring{{animation:ring 1.8s cubic-bezier(.3,.8,.3,1) both .3s;}}@keyframes ring{{from{{stroke-dasharray:0 {circ:.1f}}}}}
.seg{{animation:seg .8s ease-out both;transform-box:fill-box;transform-origin:left;}}@keyframes seg{{from{{transform:scaleX(0)}}}}"""
    body = f"""{pbody}
<rect x="34" y="38" width="7" height="7" fill="{C['orange']}"/>
<text x="50" y="46" class="h">By the numbers</text>
<text x="34" y="66" class="up">LIVE FROM THE GITHUB API  ·  UPDATED {today.strftime('%d %b %Y').upper()}</text>
{''.join(left)}
<path d="M434.5 40V260M622.5 40V260" stroke="{C['line']}"/>
{ring}
{''.join(lang_svg)}"""
    desc = ", ".join(f"{lab.title()}: {v}" for _, v, lab in rows) + f". Active days: {active}. Languages: " + \
        ", ".join(f"{n} {100 * b / tot:.1f}%" for n, b in langs)
    return svg_doc(W, H, body, css, title="GitHub stats", desc=desc, defs=pdefs)


# ════════════════════════════════════════════════════════════════════════════
# DAILY QUOTE
# ════════════════════════════════════════════════════════════════════════════
QUOTES = [
    ("Talk is cheap. Show me the code.", "Linus Torvalds"),
    ("Programs must be written for people to read, and only incidentally for machines to execute.", "Harold Abelson"),
    ("Simplicity is prerequisite for reliability.", "Edsger W. Dijkstra"),
    ("Any fool can write code that a computer can understand. Good programmers write code that humans can understand.", "Martin Fowler"),
    ("The best way to predict the future is to invent it.", "Alan Kay"),
    ("Make it work, make it right, make it fast.", "Kent Beck"),
    ("All models are wrong, but some are useful.", "George E. P. Box"),
    ("Premature optimization is the root of all evil.", "Donald Knuth"),
    ("Testing shows the presence, not the absence of bugs.", "Edsger W. Dijkstra"),
    ("Debugging is twice as hard as writing the code in the first place.", "Brian Kernighan"),
    ("Artificial intelligence is the new electricity.", "Andrew Ng"),
    ("Software is eating the world.", "Marc Andreessen"),
    ("Release early. Release often. And listen to your customers.", "Eric S. Raymond"),
    ("Given enough eyeballs, all bugs are shallow.", "Eric S. Raymond"),
    ("Walking on water and developing software from a specification are easy if both are frozen.", "Edward V. Berard"),
    ("Simple things should be simple, complex things should be possible.", "Alan Kay"),
    ("The most dangerous phrase in the language is: we've always done it this way.", "Grace Hopper"),
    ("Machine intelligence is the last invention that humanity will ever need to make.", "Nick Bostrom"),
    ("Code is like humor. When you have to explain it, it's bad.", "Cory House"),
    ("Data is the new oil.", "Clive Humby"),
]


def quote(today):
    q, author = QUOTES[today.toordinal() % len(QUOTES)]
    W = 1000
    size = 20
    lines = wrap(q, "grotesk-500", size, 780, 3)
    H = 100 + len(lines) * 29
    pdefs, pbody = panel(W, H, 16, "qt", tick=True)
    css = fonts_css("grotesk-500", "smono-400", "smono-700") + f"""
.q{{font-family:{FAMILY['sans']};font-weight:500;font-size:{size}px;letter-spacing:-.3px;fill:{C['text']};}}
.a{{font-family:{FAMILY['mono']};font-weight:700;font-size:11px;fill:{C['orange']};letter-spacing:2.5px;}}
.lb{{font-family:{FAMILY['mono']};font-size:9.5px;fill:{C['dim']};letter-spacing:2px;}}
.in{{animation:in .8s ease-out both;}}@keyframes in{{from{{opacity:0;transform:translateY(6px)}}}}"""
    qm = (f'<g transform="translate(40 40) scale(1.5)">'
          f'<path d="M2 18c0-7 3-12 9-14l1 3c-3 1.5-4.5 4-4.6 6.5H12V24H2z M16 18c0-7 3-12 9-14l1 3c-3 1.5-4.5 4-4.6 6.5H26V24H16z" fill="{C["orange"]}"/></g>')
    txt = "".join(f'<text x="120" y="{74 + i * 29}" class="q">{esc(l)}</text>' for i, l in enumerate(lines))
    a_text = "— " + author.upper()
    body = f"""{pbody}{qm}
<text x="120" y="38" class="lb">DAILY BYTE  ·  {today.strftime('%d %b %Y').upper()}</text>
<g class="in" style="animation-delay:.2s">{txt}</g>
<g class="in" style="animation-delay:.5s"><text x="{W - 40}" y="{H - 30}" text-anchor="end" class="a">{esc(a_text)}</text></g>"""
    return svg_doc(W, H, body, css, title="Quote of the day", desc=f"“{q}” — {author}", defs=pdefs)
