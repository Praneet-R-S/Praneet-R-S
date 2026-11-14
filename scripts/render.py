#!/usr/bin/env python3
"""Renders every SVG on the profile and refreshes the generated README blocks.

    python scripts/render.py           # real data (needs GITHUB_TOKEN or PROFILE_TOKEN)
    python scripts/render.py --demo    # sample data, handy for previewing locally

Edit profile.config.json, push, and the GitHub Action does the rest.
"""
import datetime as dt
import json
import os
import random
import re
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import ROOT, ASSETS  # noqa: E402
import cards  # noqa: E402
import live  # noqa: E402

GEN = os.path.join(ASSETS, "generated")
PROJ = os.path.join(ASSETS, "projects")

QUERY = """
query($login: String!, $cursor: String) {
  user(login: $login) {
    followers { totalCount }
    pullRequests { totalCount }
    issues { totalCount }
    repositories(ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC, first: 100, after: $cursor) {
      totalCount
      pageInfo { hasNextPage endCursor }
      nodes {
        name
        stargazerCount
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name } } }
      }
    }
    contributionsCollection {
      totalCommitContributions
      contributionCalendar { totalContributions weeks { contributionDays { date contributionCount } } }
    }
  }
}"""


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def gql(token, variables):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json",
                 "User-Agent": "profile-renderer"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        out = json.load(r)
    if out.get("errors"):
        raise RuntimeError(out["errors"])
    return out["data"]["user"]


def fetch(username, token, hide=()):
    user, cursor, repos = None, None, []
    while True:
        u = gql(token, {"login": username, "cursor": cursor})
        user = user or u
        repos += u["repositories"]["nodes"]
        page = u["repositories"]["pageInfo"]
        if not page["hasNextPage"]:
            break
        cursor = page["endCursor"]
    langs = {}
    for r in repos:
        if r["name"].lower() == username.lower():      # skip this profile repo itself
            continue
        for e in r["languages"]["edges"]:
            if e["node"]["name"] in hide:
                continue
            langs[e["node"]["name"]] = langs.get(e["node"]["name"], 0) + e["size"]
    cal = user["contributionsCollection"]["contributionCalendar"]
    weeks = [[(d["date"], d["contributionCount"]) for d in w["contributionDays"]] for w in cal["weeks"]]
    return {
        "total": cal["totalContributions"],
        "weeks": weeks,
        "languages": sorted(langs.items(), key=lambda kv: kv[1], reverse=True),
        "stats": {
            "stars": sum(r["stargazerCount"] for r in repos),
            "commits": user["contributionsCollection"]["totalCommitContributions"],
            "prs": user["pullRequests"]["totalCount"],
            "issues": user["issues"]["totalCount"],
            "repos": user["repositories"]["totalCount"],
            "followers": user["followers"]["totalCount"],
        },
    }


def demo_data(today):
    """Plausible fake activity, only for local previews."""
    rnd = random.Random(2026)
    start = today - dt.timedelta(days=364 + (today.weekday() + 1) % 7)
    days, d = [], start
    while d <= today:
        i = (d - start).days
        burst = 1.6 if 120 < i < 170 or 250 < i < 300 else 1.0
        weekend = 0.55 if d.weekday() >= 5 else 1.0
        c = 0 if rnd.random() < 0.28 else int(rnd.expovariate(1 / (4.5 * burst * weekend)))
        days.append((d.isoformat(), c))
        d += dt.timedelta(days=1)
    weeks = [days[i:i + 7] for i in range(0, len(days), 7)]
    return {
        "total": sum(c for _, c in days), "weeks": weeks,
        "languages": [("Python", 61000), ("TypeScript", 24000), ("JavaScript", 9000), ("C++", 6000), ("Jupyter Notebook", 4200), ("HTML", 2100)],
        "stats": {"stars": 48, "commits": 612, "prs": 37, "issues": 21, "repos": 14, "followers": 63},
    }


def empty_data(today):
    start = today - dt.timedelta(days=364 + (today.weekday() + 1) % 7)
    days = [((start + dt.timedelta(days=i)).isoformat(), 0) for i in range((today - start).days + 1)]
    return {"total": 0, "weeks": [days[i:i + 7] for i in range(0, len(days), 7)], "languages": [],
            "stats": {k: 0 for k in ("stars", "commits", "prs", "issues", "repos", "followers")}}


def replace_block(text, tag, content):
    pat = re.compile(rf"(<!-- {tag}:START -->)(.*?)(<!-- {tag}:END -->)", re.S)
    return pat.sub(lambda m: m.group(1) + "\n" + content + "\n" + m.group(3), text)


def readme_blocks(cfg, featured_files, more_files):
    fallback = f"https://github.com/{cfg['username']}?tab=repositories"

    def cell(p, f):
        img = f'<img src="assets/projects/{f}" width="49%" alt="{p["title"]} — {p["subtitle"]}">'
        if p.get("no_link"):
            return "  " + img
        return f'  <a href="{p.get("repo") or fallback}">{img}</a>'

    def grid(projects, files):
        cells = [cell(p, f) for p, f in zip(projects, files)]
        return ["<p align=\"center\">\n" + "\n".join(cells[i:i + 2]) + "\n</p>" for i in range(0, len(cells), 2)]

    rows = grid(cfg["projects"], featured_files)
    if more_files:
        rows.append('<p align="center">\n  <img src="assets/h-more.svg" width="100%" alt="More builds">\n</p>')
        rows += grid(cfg.get("more_projects", []), more_files)
    links = cfg["links"]
    btns = []
    if links.get("linkedin"):
        btns.append(f'  <a href="{links["linkedin"]}"><img src="assets/btn-linkedin.svg" height="48" alt="LinkedIn"></a>')
    if links.get("email"):
        btns.append(f'  <a href="mailto:{links["email"]}"><img src="assets/btn-email.svg" height="48" alt="Email"></a>')
    return "\n".join(rows), "<p align=\"center\">\n" + "\n&nbsp;\n".join(btns) + "\n</p>"


def main():
    demo = "--demo" in sys.argv
    empty = "--empty" in sys.argv
    with open(os.path.join(ROOT, "profile.config.json"), encoding="utf-8") as fh:
        cfg = json.load(fh)
    today = dt.datetime.now(dt.timezone.utc).date()

    # static, config-driven pieces
    write(os.path.join(ASSETS, "header.svg"), cards.header(cfg))
    write(os.path.join(ASSETS, "highlights.svg"), cards.highlights(cfg))
    write(os.path.join(ASSETS, "about.svg"), cards.about_code(cfg))
    write(os.path.join(ASSETS, "stack.svg"), cards.stack(cfg))
    write(os.path.join(ASSETS, "footer.svg"), cards.footer(cfg))
    write(os.path.join(ASSETS, "btn-linkedin.svg"), cards.button("LinkedIn", "linkedin", "li"))
    write(os.path.join(ASSETS, "btn-email.svg"), cards.button("Email me", "mail", "em"))
    write(os.path.join(ASSETS, "experience.svg"), cards.experience(cfg))
    write(os.path.join(ASSETS, "achievements.svg"), cards.achievements(cfg))
    for num, title, cap, fname in [
        ("01", "About me", "who i am", "h-about"),
        ("02", "Experience & education", "where i've worked and studied", "h-experience"),
        ("03", "Achievements", "wins and recognition", "h-achievements"),
        ("04", "Featured builds", "things i've shipped", "h-projects"),
        ("05", "Tech arsenal", "what i build with", "h-stack"),
        ("06", "GitHub signal", "live · refreshed daily", "h-signal"),
        ("07", "Let's connect", "say hello", "h-connect"),
    ]:
        write(os.path.join(ASSETS, f"{fname}.svg"), cards.heading(num, title, cap))

    featured_files, more_files = [], []
    for i, p in enumerate(cfg["projects"], start=1):
        f = f"{i:02d}-{slug(p['title'])}.svg"
        write(os.path.join(PROJ, f), cards.project_card(p, i))
        featured_files.append(f)
    more = cfg.get("more_projects", [])
    for i, p in enumerate(more, start=len(featured_files) + 1):
        f = f"{i:02d}-{slug(p['title'])}.svg"
        write(os.path.join(PROJ, f), cards.project_mini(p, i))
        more_files.append(f)
    if more:
        write(os.path.join(ASSETS, "h-more.svg"), cards.subheading("More builds", f"{len(more):02d} projects"))
    for old in os.listdir(PROJ):                       # drop cards of removed projects
        if old.endswith(".svg") and old not in featured_files + more_files:
            os.remove(os.path.join(PROJ, old))

    # live pieces
    token = os.environ.get("PROFILE_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if demo:
        data = demo_data(today)
    elif empty:
        data = empty_data(today)
    elif token:
        data = fetch(cfg["username"], token, set(cfg.get("hide_languages", [])))
    else:
        data = None
        print("No GITHUB_TOKEN set: skipped live cards (use --demo for a local preview).")
    if data is not None:
        write(os.path.join(GEN, "city.svg"), live.city(data))
        write(os.path.join(GEN, "stats.svg"), live.stats(data, today))
    write(os.path.join(GEN, "quote.svg"), live.quote(today))

    # README generated blocks
    rp = os.path.join(ROOT, "README.md")
    with open(rp, encoding="utf-8") as fh:
        text = fh.read()
    proj_html, links_html = readme_blocks(cfg, featured_files, more_files)
    text = replace_block(text, "PROJECTS", proj_html)
    text = replace_block(text, "LINKS", links_html)
    write(rp, text)
    print("Rendered profile assets for", cfg["username"], "(demo)" if demo else "")


if __name__ == "__main__":
    main()
