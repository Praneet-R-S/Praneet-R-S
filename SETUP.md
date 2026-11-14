# Setup guide: Praneet's GitHub profile

Everything on the profile is a hand-built, animated SVG in a dark industrial style
(matte black, graphite and burnt orange #E8590C). A small Python script draws
them from one config file, and a GitHub Action redraws the live parts (Contribution
City, stats, daily quote) every morning from your real GitHub data. No third-party
widget services, so nothing breaks when someone else's server goes down.

```
Praneet-R-S/
├── README.md                     ← the profile page itself
├── profile.config.json           ← the ONLY file you normally edit
├── SETUP.md                      ← this guide
├── .github/workflows/profile.yml ← daily auto-refresh
├── scripts/                      ← renderer (standard-library Python, no installs)
│   ├── render.py   cards.py   live.py   kit.py
│   ├── icons.json                ← brand icons (Simple Icons, CC0)
│   └── font_metrics.json
└── assets/
    ├── header.svg  highlights.svg  about.svg  stack.svg  footer.svg  h-*.svg  btn-*.svg
    ├── projects/                 ← one card per project
    ├── generated/                ← city.svg, stats.svg, quote.svg (rewritten daily)
    └── fonts/                    ← subset fonts embedded into the SVGs (OFL)
```

---

## 1. Create the special profile repository

1. Go to <https://github.com/new>.
2. **Repository name:** `Praneet-R-S`. It must match your username exactly; GitHub
   will say *"You found a secret!"* when it's right.
3. Set it to **Public**. Leave "Add a README" unticked.
4. Click **Create repository**.

## 2. Upload the files

### Option A: with Git (recommended)

Unzip the download, open a terminal inside the `Praneet-R-S` folder, then run:

```bash
git init -b main
git add .
git commit -m "feat: profile README"
git remote add origin https://github.com/Praneet-R-S/Praneet-R-S.git
git push -u origin main
```

### Option B: browser only

1. On the new repo page click **uploading an existing file**.
2. Open the unzipped folder, select **everything inside it** (`README.md`,
   `profile.config.json`, `SETUP.md`, `assets`, `scripts`) and drag it in. Commit.
3. The `.github` folder is hidden on most computers and usually gets skipped, so add
   the workflow by hand: **Add file → Create new file**, type the name
   `.github/workflows/profile.yml`, paste in the contents of that file from the zip,
   and commit.

## 3. Run the Action once

1. Open the repo's **Actions** tab. If GitHub asks, click
   **"I understand my workflows, go ahead and enable them."**
2. Click **Refresh profile → Run workflow → Run workflow**.
3. Wait about 30 seconds for the green check. The bot commits fresh
   `city.svg`, `stats.svg` and `quote.svg`.

Until that first run, the City shows a "The city is waiting." screen and the stats show
zeros. That is expected.

> **If the run fails with a 403 on `git push`:** go to **Settings → Actions → General →
> Workflow permissions**, choose **Read and write permissions**, save, and re-run.

## 4. Look at it

Open <https://github.com/Praneet-R-S> and hard-refresh (**Ctrl + Shift + R**, or
**Cmd + Shift + R** on a Mac). GitHub caches images for a few minutes, so a fresh change can
take a moment to show up.

---

## Everyday edits

Edit **`profile.config.json`** on GitHub (pencil icon) and commit. The Action redraws
every SVG and updates the README automatically within a minute.

| Field | What it controls |
|---|---|
| `name`, `greeting`, `status` | Your name (every "." is drawn in orange), the small "HELLO, I'M" line, and the status at the top right |
| `roles` | The lines that type and delete under your name |
| `specs` | The spec-sheet row at the bottom of the header (label + value pairs) |
| `links.linkedin`, `links.email` | Both rows of buttons. Delete a key to hide that button |
| `highlights` | The four achievement tiles. Icons: `trophy`, `scroll`, `cap`, `people`, `star`, `bolt`, `flame` |
| `about_code` | The animated `praneet.py` window. Token types: `kw`, `cls`, `fn`, `str`, `cm`, `p` |
| `experience` | Work timeline: role, org, period, `current: true` adds the pulsing NOW tag, bullet `points` and `tags` |
| `education` | Degree, school, period and the CGPA bar |
| `community` | Leadership and volunteering entries (icons: `people`, `heart`, `star`, `bolt`) |
| `achievements` | The trophy tiles. Icons: `trophy`, `medal`, `scroll`, `abacus`, `cap`, `star` |
| `projects` | The four big featured cards (see below) |
| `more_projects` | The smaller 'More builds' cards. They use `tags` (tech chips) instead of `metrics` |
| `stack` | Tech grid rows. Brand icon names come from `scripts/icons.json`. Custom ones: `@db`, `@brain`, `@chart`, `@cloud` |
| `hide_languages` | Languages to leave out of Top Languages, e.g. `["Jupyter Notebook"]` |

### When you upload a project

Put the link in that project's `repo` field:

```json
"repo": "https://github.com/Praneet-R-S/sangam",
```

Commit. The card's chip changes from **REPO SOON** to an orange **VIEW REPO** and the card
starts linking to the repo. Until then, cards link to your repositories tab.

`RAP` is marked **COMPANY BUILD** because it's internship work at
Flexidigit, which usually can't be made public. Change `status` if you'd like other wording.

> **Before you upload:** fork `moulishk2205/VetriTamilNadu_SuperApp` to your account
> (open it on GitHub and click **Fork**) so the Vetri Tamil Nadu card's link,
> `github.com/Praneet-R-S/VetriTamilNadu_SuperApp`, works.

### Adding a project

Copy one project block, change the text, and pick a `viz` animation:
`match` (linking nodes), `pulse` (heartbeat), `forecast` (chart drawing itself),
`agents` (agent network), `flow` (process map), `bus` (moving route), `scan` (phone scanner)
or `path` (pathfinding grid). Cards are laid out two per row, so keep an even count.
Add `"no_link": true` to a project that should not be clickable (like Ares Rover).

### Adding a brand icon to the stack

1. Find the icon on <https://simpleicons.org>, open it, and copy the SVG `path` data
   (the long `d="M..."` string).
2. Add it to `scripts/icons.json` as `"name": {"title": "Name", "path": "M..."}`.
3. Use `["name", "Label"]` in `stack`.

### Changing the accent color

All colors live in the `C` dictionary at the top of `scripts/kit.py`. Change `orange`
(and its lighter tints `orange2` and `orange3`), commit, and every card picks it up on the
next run.

### Preview on your own computer (optional)

```bash
python scripts/render.py --demo     # sample numbers, for looking only
python scripts/render.py --empty    # the 'waiting' state
```

Don't commit `--demo` output. If you do by accident, the Action replaces it with real
data on its next run.

---

## Optional: count private contributions

By default, stats only use public activity, so there's nothing extra to set up. To include
private work later:

1. Create a classic token at <https://github.com/settings/tokens> with the `repo` and
   `read:user` scopes.
2. In the profile repo, open **Settings → Secrets and variables → Actions → New repository secret**,
   name it `PROFILE_TOKEN`, and paste the token.
3. Run the workflow again.

## Profile polish checklist

- Use a clear, well-lit **profile photo** (the header is busy, so keep the photo simple).
- **Bio:** `AI/ML Engineer · Full-Stack · B.Tech CSE @ SRM`
- **Location:** Chennai, India. Add LinkedIn under *Social accounts*.
- **Pin 4–6 repos** once they're uploaded. Give each one a description, topics, and its own
  README with a screenshot or GIF.
- Commit regularly. The City grows a tower every week.

## Troubleshooting

| Symptom | Fix |
|---|---|
| Animations don't play | Some apps (and "reduce motion" settings) show the still version. Everything is still readable. Open the page in a desktop browser to see the animations. |
| Fonts look plain | Hard-refresh the page. The fonts are embedded in each SVG. |
| The workflow stopped running | GitHub pauses scheduled workflows in inactive repos. The daily quote commit keeps the repo active, but if it ever pauses, re-enable it in the Actions tab. |
| I want a different refresh time | Edit the `cron` line in `.github/workflows/profile.yml`. The time is in UTC. |

Credits: brand icons from Simple Icons (CC0). Fonts are Space Grotesk and Space Mono,
both under the SIL Open Font License (see `assets/fonts/LICENSE.md`).
