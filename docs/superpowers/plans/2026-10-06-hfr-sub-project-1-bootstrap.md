# HFR Sub-project 1 (Bootstrap) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn this empty folder into the HFR Ortho Statistics Tutorials repo: the TJS site with its history, rebranded for HFR, adapted to Swiss rules, restructured into `en/`, `de/`, `fr/` with a language switcher, English content complete, German and French home pages translated and every other German/French page a stub, ready to publish at `https://hfr-ortho.github.io/stats-formation/`.

**Architecture:** One Quarto website project. Pages live in `en/`, `de/`, `fr/` with identical file names; each folder's `_metadata.yml` sets `lang`; `_quarto.yml` holds one sidebar per language (Quarto shows the sidebar that contains the page); a small script swaps the language folder in the address. Code still runs from the repo root (`execute-dir: project`), so `data/`, `R/` and renv are untouched. Results stay frozen in `_freeze/`; CI never runs R or Python.

**Tech Stack:** Quarto 1.9.37, R 4.4+ with renv (knitr, reticulate), Python 3.12+ with uv (pandas 3), pytest + BeautifulSoup, testthat, lychee, Node.js (only for the switcher's unit tests; they skip without it), just, gh.

**Spec:** `docs/superpowers/specs/2026-10-06-hfr-stats-formation-design.md` (this plan implements its §4). The tutorial conventions come from the TJS spec, `docs/superpowers/specs/2026-10-05-tjs-stats-tutorials-design.md`, and the golden rules in `CLAUDE.md`. Read both specs and `CLAUDE.md` before starting.

## Global Constraints

- Work in `/Users/docschwab/repos/hfr-ortho/stats-formation`. Run every command from there.
- Quarto **1.9.37** (pinned in CI). Render locally and commit `_freeze/`; CI never runs R or Python.
- Every `CLAUDE.md` golden rule stays in force: synthetic data only; `engine: knitr` on every page with code; never hand-edit `data/` or `templates/` (change `data-raw/`, run `just data`); never loosen a test or change a seed to make a test pass.
- Repo `hfr-ortho/stats-formation` (public). Site `https://hfr-ortho.github.io/stats-formation/`. TJS remote is `tjs`, fetch-only (push URL `DISABLED`).
- Copyright line, verbatim: `HFR adaptations Copyright (c) 2026 HFR Hôpital fribourgeois`. TJS's `Copyright (c) 2026 Total Joint Specialists` stays.
- Credit phrase, verbatim: `Adapted from the TJS Statistics Tutorials`.
- Journal line, verbatim: `reviewers at journals such as JBJS, *The Bone & Joint Journal* and *CORR*`.
- Audience line, verbatim: `HFR Ortho residents, research assistants and medical students doing their master's thesis`.
- Colours: blue `#006DB5`, navy `#103379`, dark-mode links `#5AA9E6`. Every text/background pair ≥ 4.5 : 1.
- Language codes `en`, `de`, `fr`. Stub title marks: `(in Vorbereitung)` and `(en préparation)`. Swiss Standard German: "ss", never "ß". Formal address: "Sie" and "vous".
- In every language, code, variable names, data, outputs and Methods/Results sentences stay in English.
- **Nothing leaves this machine without Doc's explicit go-ahead at that moment:** no `gh repo create`, no `git push`, no Pages settings change. Task 12 asks for each one separately.
- Commit messages: a plain sentence saying what changed (the TJS history's style), ending with:

  ```
  Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
  ```

## Review Focus

1. A Fribourg reader whose browser reports `de-CH` or `fr-CH` (a region tag, not plain `de`/`fr`) opens the site root: they should land in German or French, not English. *Test: `test_browser_language_with_a_region_picks_the_site_language` (Task 10).*
2. The site runs under `/stats-formation/` on GitHub Pages but at `/` in `quarto preview`: the switcher must find the language folder in both. *Test: `test_switching_keeps_the_page_and_section_with_or_without_a_site_prefix` (Task 10).*
3. A browser that blocks `localStorage` (Safari private window, strict privacy settings): switching and the root redirect must still work, with no script error. *Test: `test_blocked_storage_never_breaks_the_page` (Task 10).*
4. A reader halfway down `catalog/06-two-unpaired-groups.html#mann-whitney` switches language: they should land on the same section. *Tests: `test_every_section_link_targets_a_fixed_id` and `test_translated_pages_keep_every_fixed_id` (Task 9), plus the switching test in item 2.*
5. A reader with JavaScript off reaches the site root: plain links to all three languages must be there. *Test: `test_root_page_offers_every_language_without_javascript` (Task 9).*

---

### Task 1: Bring in the TJS history and commit the spec

**Files:**
- Modify (git metadata only): `.git/`
- Commit: `docs/superpowers/specs/2026-10-06-hfr-stats-formation-design.md`, `docs/superpowers/plans/2026-10-06-hfr-sub-project-1-bootstrap.md`

**Interfaces:**
- Consumes: nothing.
- Produces: branch `main` at TJS `94d62e9` plus one HFR commit; remote `tjs` (fetch-only); a working R and Python environment (`renv/library`, `.venv`).

- [ ] **Step 1: Initialise and fetch TJS**

The folder already holds the spec and this plan, so `git clone` (which needs an empty folder) is replaced by:

```bash
git init -b main
git remote add tjs https://github.com/Total-Joint-Specialists/example-stats-analysis.git
git remote set-url --push tjs DISABLED
git fetch tjs
git checkout --no-track -B main tjs/main
```

`--no-track` keeps `main` from tracking TJS, so a bare `git pull` or `git push` never talks to TJS.

- [ ] **Step 2: Check the result**

Run: `git log --oneline -1 && git remote -v && git status --short`
Expected:
```
94d62e9 A welcome page with three ways in ...
tjs	https://github.com/Total-Joint-Specialists/example-stats-analysis.git (fetch)
tjs	DISABLED (push)
?? docs/superpowers/plans/2026-10-06-hfr-sub-project-1-bootstrap.md
?? docs/superpowers/specs/2026-10-06-hfr-stats-formation-design.md
```
If the hash isn't `94d62e9`, TJS has moved on: replace `94d62e9` in the spec's "Derived from" line with the new short hash before Step 5.

- [ ] **Step 3: Set up R and Python**

Run: `just setup`
Expected: renv restores from the global cache, `uv sync` creates `.venv`, both end without errors.

- [ ] **Step 4: Baseline: everything passes before any change**

Run:
```bash
just test
quarto render
uv run pytest tests/site -q
lychee --offline --include-fragments --no-progress _site
```
Expected: all pass. `quarto render` should not execute any code: every page is unchanged, so `_freeze/` is reused (`git status --short _freeze` prints nothing). If anything fails here, stop and report it; it's a problem with the environment, not with HFR changes.

- [ ] **Step 5: Commit the spec and plan**

```bash
git add docs/superpowers/specs/2026-10-06-hfr-stats-formation-design.md docs/superpowers/plans/2026-10-06-hfr-sub-project-1-bootstrap.md
git commit -m "Start the HFR Ortho copy of the TJS tutorials: design spec and the sub-project 1 plan

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 2: HFR identity in the repo documents and package metadata

**Files:**
- Modify: `README.md` (full rewrite), `LICENSE:3`, `LICENSE-CONTENT:1-3`, `pyproject.toml:2-4`, `uv.lock` (regenerated), `DESCRIPTION:2-3`, `CLAUDE.md:1-7` and rule 1, `data/README.md:31`
- Test: `tests/python/test_repo_docs.py`

**Interfaces:**
- Consumes: Task 1's repo.
- Produces: `SITE_URL = "https://hfr-ortho.github.io/stats-formation/"` in `tests/python/test_repo_docs.py` (later tasks don't import it).

- [ ] **Step 1: Write the failing tests**

Replace `tests/python/test_repo_docs.py` with:

```python
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SITE_URL = "https://hfr-ortho.github.io/stats-formation/"
HFR_COPYRIGHT = "HFR adaptations Copyright (c) 2026 HFR Hôpital fribourgeois"
CREDIT = "Adapted from the TJS Statistics Tutorials"


def read(name: str) -> str:
    return (ROOT / name).read_text(encoding="utf-8")


def test_readme_links_the_site_says_synthetic_and_credits_tjs():
    text = read("README.md")
    assert SITE_URL in text
    assert "synthetic" in text.lower()
    assert CREDIT in text
    assert "git clone https://github.com/hfr-ortho/stats-formation.git" in text


def test_licenses():
    assert read("LICENSE").startswith("MIT License")
    assert "Total Joint Specialists" in read("LICENSE")
    assert HFR_COPYRIGHT in read("LICENSE")
    content = read("LICENSE-CONTENT")
    assert "Total Joint Specialists" in content and HFR_COPYRIGHT in content
    assert "adapted from the TJS Statistics Tutorials" in content
    assert "CC BY 4.0" in content
    assert "https://creativecommons.org/licenses/by/4.0/legalcode" in content


def test_package_metadata_names_hfr():
    assert 'name = "hfr-stats-formation"' in read("pyproject.toml")
    assert "HFR Ortho" in read("DESCRIPTION")


def test_claude_md_states_the_golden_rules():
    text = read("CLAUDE.md")
    for rule in ["engine: knitr", "group=\"language\"", "check_agree", "_freeze", "Synthetic data only",
                 "never assign to `_`", "**The question:**", "override-dependencies",
                 'a ceiling of "p > 0.999"', "Bootstrap CIs are seeded", "opts_chunk",
                 "Regression CIs", "CumIncidenceRight", "Mixed models", "Multiple comparisons", "Word output",
                 "report numbers, not interpretation",
                 "deliberate public exception", "fetch-only", "2026-10-06-hfr-stats-formation-design.md"]:
        assert rule in text, rule
```

- [ ] **Step 2: Run them to see them fail**

Run: `uv run pytest tests/python/test_repo_docs.py -q`
Expected: 4 failed (TJS URL in README, no HFR copyright, TJS package name, CLAUDE.md lacks the new strings).

- [ ] **Step 3: Rewrite `README.md`**

````markdown
# HFR Ortho Statistics Tutorials

Tutorials and worked examples that teach HFR Ortho residents, research assistants and medical students doing their master's thesis how to prepare data and run the statistical analyses used in orthopaedic research, in R, Python, or both. The site is in English, German and French.

**Read the site:** https://hfr-ortho.github.io/stats-formation/

> **All data in this repository are synthetic.** No real patient data is ever committed here, and this repository is public.

Adapted from the [TJS Statistics Tutorials](https://total-joint-specialists.github.io/example-stats-analysis/) (CC BY 4.0).

## What's inside

| Part | Topics |
|------|------|
| Getting started | Installing R, Python, Git and Positron; how to use the site; working safely with real HFR data under Swiss rules |
| 1 · Foundations | Tidy data, Table 1, distributions & choosing a test |
| 2 · Test catalog | Every test in the Motulsky decision table, R and Python side by side |
| 3 · Survival analysis | Kaplan-Meier, competing risks, Cox regression |
| 4 · Beyond the table | Post-hoc tests, mixed models, agreement & reliability |
| 5 · Putting it together | A complete example study report |

## Run the examples

```bash
git clone https://github.com/hfr-ortho/stats-formation.git
cd stats-formation
Rscript -e 'renv::restore()'
uv sync
```

Step-by-step instructions for beginners: [Install & set up](https://hfr-ortho.github.io/stats-formation/en/getting-started/setup.html).

## Repository layout

| Path | What it holds |
|------|------|
| `en/`, `de/`, `fr/` | The site's pages, one folder per language, with the same file names in each |
| `index.qmd` | The site root: sends visitors to their language |
| `data/` | Synthetic datasets and codebooks |
| `templates/` | A data-collection template to copy for real projects |
| `R/` | Site helpers (`check_agree()`) |
| `scripts/` | Setup checks you run on your own computer |
| `theme/`, `images/`, `lang-switch.html` | HFR colours and logo, and the language switcher |
| `tests/` | R (testthat), Python (pytest), and built-site tests |
| `_freeze/` | Saved results of every page's code (committed, so the site builds without R or Python) |
| `scratch/` | Your practice space; git ignores everything in it |
| `docs/superpowers/` | Design specs and implementation plans |

## For maintainers

You'll need R, uv, Quarto 1.9.37, [just](https://github.com/casey/just), and [lychee](https://github.com/lycheeverse/lychee).

```bash
just setup     # renv::restore() + uv sync
just test      # R and Python unit tests
just preview   # live preview while writing
just check     # render, then site tests + link check
```

Render locally and commit `_freeze/`. CI builds the site from `_freeze/` without running R or Python, runs the site checks, and publishes `main` to GitHub Pages.

The TJS repository is the `tjs` remote, fetch-only. To carry a TJS fix over: `git fetch tjs`, then `git cherry-pick <commit>`.

## License

Text, figures and synthetic data: [CC BY 4.0](LICENSE-CONTENT). Code: [MIT](LICENSE). Adapted from the TJS Statistics Tutorials, © 2026 Total Joint Specialists.
````

- [ ] **Step 4: Licenses**

In `LICENSE`, replace line 3 `Copyright (c) 2026 Total Joint Specialists` with these two lines:

```
Copyright (c) 2026 Total Joint Specialists
HFR adaptations Copyright (c) 2026 HFR Hôpital fribourgeois
```

In `LICENSE-CONTENT`, replace the first line (`Copyright (c) 2026 Total Joint Specialists`) with:

```
Copyright (c) 2026 Total Joint Specialists
HFR adaptations Copyright (c) 2026 HFR Hôpital fribourgeois

This material is adapted from the TJS Statistics Tutorials
(https://total-joint-specialists.github.io/example-stats-analysis/): rebranded
for HFR Ortho, adapted to Swiss rules, and translated into German and French.
```

- [ ] **Step 5: Package metadata**

In `pyproject.toml`: `name = "hfr-stats-formation"` and `description = "Python environment for the HFR Ortho statistics tutorial site"`. Then run `uv lock` (only the project's own name changes in `uv.lock`).

In `DESCRIPTION`, replace the `Description:` field with:

```
Description: R dependencies for the HFR Ortho statistics tutorial site. Not
    a package; renv reads this file to decide what to lock.
```

`renv.lock` doesn't change (renv reads only `Imports`).

- [ ] **Step 6: `CLAUDE.md` header and rule 1**

Replace everything above `## Golden rules` with:

```markdown
# CLAUDE.md: HFR Ortho Statistics Tutorials

Public Quarto website and repository, in English, German and French. It teaches HFR Ortho residents, research assistants and medical students doing their master's thesis (beginners in both statistics and code) tidy data, Table 1, distribution checks, every test in the Motulsky decision table, survival analysis, and selected extras, in R and Python side by side.

It is an independent copy of the TJS Statistics Tutorials that keeps TJS's git history. The TJS repository is the `tjs` remote, fetch-only (its push URL is `DISABLED`). Carry a TJS fix over with `git fetch tjs` and `git cherry-pick <commit>`; nothing syncs automatically.

- HFR design spec (what HFR changes): `docs/superpowers/specs/2026-10-06-hfr-stats-formation-design.md`
- TJS design spec (the tutorial conventions; "spec section N" below means this one): `docs/superpowers/specs/2026-10-05-tjs-stats-tutorials-design.md`
- Plans: `docs/superpowers/plans/`
```

Replace rule 1's first sentence `1. **Synthetic data only. This repo is public.**` with:

```markdown
1. **Synthetic data only. This repo is public**, a deliberate public exception to the `hfr-ortho` rule that every repo is private.
```

(Keep the rest of rule 1 as it is.)

- [ ] **Step 7: `data/README.md` link**

Replace `https://total-joint-specialists.github.io/example-stats-analysis/foundations/01-tidy-data.html` with `https://hfr-ortho.github.io/stats-formation/en/foundations/01-tidy-data.html`. (`data/CHECKSUMS.md5` covers only CSV files, so this edit doesn't change it.)

- [ ] **Step 8: Run the tests**

Run: `uv run pytest tests/python -q`
Expected: all pass.

- [ ] **Step 9: Commit**

```bash
git add README.md LICENSE LICENSE-CONTENT pyproject.toml uv.lock DESCRIPTION CLAUDE.md data/README.md tests/python/test_repo_docs.py
git commit -m "Name the repo HFR Ortho Statistics Tutorials: README, licenses with the HFR line and TJS credit, package names, CLAUDE.md

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 3: Setup checks move to `scripts/`; pages point at the HFR repo

**Files:**
- Move: `getting-started/check_setup.R` → `scripts/check_setup.R`, `getting-started/check_setup.py` → `scripts/check_setup.py`
- Modify: `scripts/check_setup.R:2-3,14,25`, `scripts/check_setup.py:3,31`, `getting-started/setup.qmd`, `getting-started/using-this-site.qmd:145`, `foundations/01-tidy-data.qmd:104`
- Test: `tests/python/test_check_setup.py:6,27`, `tests/testthat/test-check_setup.R:5`, `tests/site/test_getting_started.py:3-12,43-44`

**Interfaces:**
- Consumes: Task 2.
- Produces: `scripts/check_setup.R` and `scripts/check_setup.py` (same contract as before: print `All good - you are ready.` and exit 0, or `PROBLEM - <fix>` lines and exit 1).

- [ ] **Step 1: Point the tests at the new paths and URLs**

- `tests/python/test_check_setup.py`: `SCRIPT = ROOT / "scripts" / "check_setup.py"`, and in `test_r_check_covers_the_packages_the_pages_call` read `ROOT / "scripts" / "check_setup.R"`.
- `tests/testthat/test-check_setup.R`: `"scripts/check_setup.R"` in place of `"getting-started/check_setup.R"`.
- `tests/site/test_getting_started.py`: set

```python
SETUP_COMMANDS = [
    "uv python install 3.13",
    "git clone https://github.com/hfr-ortho/stats-formation.git",
    "renv::restore()",
    "uv sync",
    "Rscript scripts/check_setup.R",
    "uv run python scripts/check_setup.py",
    'source("scripts/check_setup.R")',
    "sudo xcodebuild -license accept",
]
```

and in `test_setup_page_shows_how_to_read_data_without_cloning`:

```python
    url = "https://raw.githubusercontent.com/hfr-ortho/stats-formation/main/data/cohort.csv"
```

- [ ] **Step 2: Run them to see them fail**

Run: `uv run pytest tests/python/test_check_setup.py -q; Rscript -e 'testthat::test_dir("tests/testthat", filter = "check_setup")'`
Expected: FAIL, file not found.

- [ ] **Step 3: Move the scripts and update every reference**

```bash
mkdir -p scripts
git mv getting-started/check_setup.R getting-started/check_setup.py scripts/
sed -i '' \
  -e 's#Total-Joint-Specialists/example-stats-analysis#hfr-ortho/stats-formation#g' \
  -e 's#getting-started/check_setup#scripts/check_setup#g' \
  -e 's#example-stats-analysis#stats-formation#g' \
  scripts/check_setup.R scripts/check_setup.py getting-started/*.qmd foundations/01-tidy-data.qmd
git grep -n -E "example-stats-analysis|Total-Joint-Specialists|getting-started/check_setup" -- scripts getting-started foundations
```

Expected from the last command: no output. (The sed order matters: the full `Total-Joint-Specialists/…` URL first, then the bare folder name.)

- [ ] **Step 4: Run the unit tests**

Run: `just test`
Expected: all pass.

- [ ] **Step 5: Render and run the site checks**

Run: `just check`
Expected: all pass. `getting-started/using-this-site.qmd` and `foundations/01-tidy-data.qmd` re-execute (their text changed); every other page comes from `_freeze/`.

- [ ] **Step 6: Commit**

```bash
git add -A scripts getting-started foundations _freeze tests
git commit -m "Setup checks move to scripts/; pages link to hfr-ortho/stats-formation and its raw data URLs

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 4: Move every page under `en/`

**Files:**
- Move: `index.qmd`, `choose-a-test.qmd`, `tests-a-z.qmd`, `getting-started/`, `foundations/`, `catalog/`, `survival/`, `beyond/`, `report/` → `en/…`; `_freeze/<same folders>` → `_freeze/en/…`
- Create: `en/_metadata.yml`, `index.qmd` (root page)
- Modify: `_quarto.yml` (full replacement below), `Justfile` (data recipe), `CLAUDE.md` (Layout section, rules 7 and 11)
- Test: `tests/site/sitelib.py`, `tests/site/test_structure.py`, `tests/site/test_home.py`, `tests/site/test_freshness.py`, `tests/site/test_sources.py`, `tests/site/test_catalog.py:46`, `tests/site/test_free_form.py:22`, `tests/site/test_foundations.py:37`, `tests/site/test_conventions.py:60`, `tests/site/test_report.py:23,150,157`, `tests/python/test_gitignore.py`

**Interfaces:**
- Consumes: Task 3.
- Produces, in `tests/site/sitelib.py`: `ROOT`, `SITE_ROOT` (`_site/`), `LANGS = ["en", "de", "fr"]`, `SITE` (`_site/en/`), `SRC` (`en/`), `FREEZE` (`_freeze/en/`), and `target(page: str, href: str, lang: str = "en") -> str`. `load(page)` keeps reading `SITE / page`, i.e. English. `strip_dot` is removed.

- [ ] **Step 1: Update `tests/site/sitelib.py`**

Replace the imports and the `ROOT`/`SITE` lines at the top with:

```python
"""Shared constants and helpers for the built-site tests."""

import html
import posixpath
import re
import zipfile
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[2]
SITE_ROOT = ROOT / "_site"
LANGS = ["en", "de", "fr"]

# The English pages. Every content test reads these; test_languages.py checks German and French.
SITE = SITE_ROOT / "en"
SRC = ROOT / "en"
FREEZE = ROOT / "_freeze" / "en"
```

Replace `strip_dot()` with:

```python
def target(page: str, href: str, lang: str = "en") -> str:
    """Where a link on the built page <lang>/<page> points, as a path inside <lang>/ ("catalog/x.html#id").

    Quarto writes sidebar links as "../en/catalog/x.html" and body links as "catalog/x.html"; both give the
    same answer. A link that leaves the language folder comes back from the site root ("/de/index.html");
    web links come back unchanged."""
    if "://" in href or href.startswith("mailto:"):
        return href
    if href.startswith("#"):
        return page + href
    resolved = posixpath.normpath(posixpath.join(lang, posixpath.dirname(page), href))
    return resolved.removeprefix(f"{lang}/") if resolved.startswith(f"{lang}/") else "/" + resolved
```

- [ ] **Step 2: Update the tests that use paths**

- `tests/site/test_structure.py`: import `CELL_ANCHORS, PAGES, SITE_ROOT, load, target`. In `test_repo_files_are_not_published` use `SITE_ROOT / path`. In `test_sidebar_links_every_page`:

```python
def test_sidebar_links_every_page(site):
    hrefs = {target("index.html", a["href"]) for a in load("index.html").select("#quarto-sidebar a[href]")}
    missing = [p for p in PAGES if p not in hrefs]
    assert missing == []
```

  In the two logo tests use `SITE_ROOT / "images" / …` in place of `site / "images" / …`. Add:

```python
def test_root_page_links_the_english_site(site):
    soup = BeautifulSoup((SITE_ROOT / "index.html").read_text(encoding="utf-8"), "html.parser")
    assert "en/index.html" in {a["href"].removeprefix("./") for a in soup.select("main a[href]")}
    assert soup.select_one("#quarto-sidebar") is None
```

  (add `from bs4 import BeautifulSoup` at the top).
- `tests/site/test_home.py`: import `target` in place of `strip_dot`; `hrefs(page)` becomes `{target(page, a["href"]) for a in load(page).select("main a[href]")}`; in `index_rows()` use `target(A_TO_Z, a["href"])`.
- `tests/site/test_freshness.py`: replace from `CONTENT_DIRS` down to the end of the file with:

```python
CONTENT_DIRS = ["getting-started", "foundations", "catalog", "survival", "beyond", "report"]
READS_DATA = re.compile(r"""["']data/""")


def data_pages():
    """Every built page, in any language, whose code reads data/ (as paths from the site root)."""
    for lang in LANGS:
        for d in CONTENT_DIRS:
            for qmd in sorted((ROOT / lang / d).glob("*.qmd")):
                text = qmd.read_text(encoding="utf-8")
                if "```{r" in text and READS_DATA.search(text):
                    yield qmd.relative_to(ROOT).with_suffix(".html")


def test_pages_that_read_data_were_rendered_from_the_current_data(site):
    current = hashlib.md5((ROOT / "data" / "CHECKSUMS.md5").read_bytes()).hexdigest()
    pages = list(data_pages())
    assert pages, "expected at least one page that reads data/"
    for page in pages:
        html = (SITE_ROOT / page).read_text(encoding="utf-8")
        assert f"<!-- data-checksum: {current} -->" in html, f"{page} was rendered from other data; re-render it"


def test_just_data_re_renders_the_pages_that_read_data():
    justfile = (ROOT / "Justfile").read_text(encoding="utf-8")
    recipe = justfile[justfile.index("\ndata:"):]
    folders = sorted({"/".join(page.parts[:2]) for page in data_pages()})   # e.g. "en/foundations"
    missing = [f for f in folders if not re.search(rf"^\s*quarto render {re.escape(f)}\s*$", recipe, re.MULTILINE)]
    assert missing == [], f"`just data` must re-render: {missing}"
```

  and import `from sitelib import LANGS, ROOT, SITE_ROOT`.
- `tests/site/test_sources.py`: import `CELL_ANCHORS, LANGS, ROOT, SRC`. Replace `qmd_files()` with:

```python
def qmd_files():
    files = sorted(ROOT.glob("*.qmd"))   # the site root's language picker
    for lang in LANGS:
        files += sorted((ROOT / lang).glob("*.qmd"))   # each language's home page, test chooser and A–Z index
        for d in CONTENT_DIRS:
            files += sorted((ROOT / lang / d).glob("*.qmd"))
    return files
```

  In `written_pages()` use `(SRC / d).glob("*.qmd")` (the keys stay `f"{d}/{path.name}"`). Replace the three `ROOT / "foundations" / …` reads with `SRC / "foundations" / …`.
- `tests/site/test_catalog.py`, `test_free_form.py`, `test_foundations.py`: import `FREEZE` and use `FREEZE / page.removesuffix(".html")` in place of `ROOT / "_freeze" / page.removesuffix(".html")`.
- `tests/site/test_conventions.py`: import `FREEZE`; `assert (FREEZE / "getting-started" / "using-this-site").is_dir()`.
- `tests/site/test_report.py`: import `FREEZE, SRC`; `frozen = FREEZE / "report" / "18-example-report"` (both places); `page = (SRC / "report" / "18-example-report.qmd")`. Leave `ROOT / "_freeze" / "site_libs"` as it is: Quarto keeps that folder at the top of `_freeze/`.
- `tests/python/test_gitignore.py`: `"_freeze/en/getting-started/using-this-site/execute-results/html.json"` in place of `"_freeze/getting-started/…"`.

Run: `uv run pytest tests/site -q`
Expected: many failures (the pages aren't under `en/` yet).

- [ ] **Step 3: Move the pages and their frozen results**

```bash
mkdir -p en _freeze/en
git mv index.qmd choose-a-test.qmd tests-a-z.qmd en/
for d in getting-started foundations catalog survival beyond report; do
  git mv "$d" en/
  git mv "_freeze/$d" "_freeze/en/$d"
done
printf 'lang: en\n' > en/_metadata.yml
```

- [ ] **Step 4: The root page**

Create `index.qmd`:

```markdown
---
title: "HFR Ortho Stats"
sidebar: false
toc: false
---

[English](en/index.qmd)
```

(Task 9 adds German and French.)

- [ ] **Step 5: Replace `_quarto.yml`**

```yaml
project:
  type: website
  output-dir: _site
  execute-dir: project
  render:
    - index.qmd
    - en/*.qmd
    - en/getting-started/*.qmd
    - en/foundations/*.qmd
    - en/catalog/*.qmd
    - en/survival/*.qmd
    - en/beyond/*.qmd
    - en/report/*.qmd

# Note: `engine: knitr` does NOT work here or in _metadata.yml. Each page
# with code declares it in its own front matter.
execute:
  freeze: auto

# Quarto ignores `message` under `execute:` for knitr pages; knitr's own chunk
# default hides messages on every page.
knitr:
  opts_chunk:
    message: false

website:
  title: "TJS Statistics Tutorials"
  description: "Tidy data, Table 1, and every common statistical test, in R and Python, for Total Joint Specialists research assistants."
  site-url: "https://total-joint-specialists.github.io/example-stats-analysis/"
  repo-url: "https://github.com/Total-Joint-Specialists/example-stats-analysis"
  repo-actions: [issue]
  search: true
  page-navigation: true
  favicon: images/tjs-icon.png
  navbar:
    left:
      - text: "Home"
        href: en/index.qmd
      - text: "Getting started"
        href: en/getting-started/setup.qmd
      - text: "Choose a test"
        href: en/choose-a-test.qmd
      - text: "Tests A–Z"
        href: en/tests-a-z.qmd
    right:
      - icon: github
        href: "https://github.com/Total-Joint-Specialists/example-stats-analysis"
        aria-label: "GitHub repository"
  sidebar:
    - id: en
      style: docked
      logo:
        light:
          path: images/tjs-logo.png
          alt: "Total Joint Specialists"
        dark:
          path: images/tjs-logo-dark.png
          alt: "Total Joint Specialists"
      contents:
        - text: "Home"
          href: en/index.qmd
        - text: "Choose a test"
          href: en/choose-a-test.qmd
        - text: "Tests A–Z"
          href: en/tests-a-z.qmd
        - section: "Getting started"
          contents:
            - en/getting-started/setup.qmd
            - en/getting-started/using-this-site.qmd
            - en/getting-started/real-data.qmd
        - section: "Part 1 · Foundations"
          contents:
            - en/foundations/01-tidy-data.qmd
            - en/foundations/02-demographics.qmd
            - en/foundations/03-distributions.qmd
        - section: "Part 2 · Test catalog"
          contents:
            - en/catalog/04-describe-one-group.qmd
            - en/catalog/05-one-group-vs-hypothetical.qmd
            - en/catalog/06-two-unpaired-groups.qmd
            - en/catalog/07-two-paired-groups.qmd
            - en/catalog/08-three-plus-unmatched.qmd
            - en/catalog/09-three-plus-matched.qmd
            - en/catalog/10-association.qmd
            - en/catalog/11-predict-from-one.qmd
            - en/catalog/12-predict-from-several.qmd
        - section: "Part 3 · Survival analysis"
          contents:
            - en/survival/13-kaplan-meier.qmd
            - en/survival/14-cox-regression.qmd
        - section: "Part 4 · Beyond the table"
          contents:
            - en/beyond/15-post-hoc.qmd
            - en/beyond/16-mixed-models.qmd
            - en/beyond/17-agreement.qmd
        - section: "Part 5 · Putting it together"
          contents:
            - en/report/18-example-report.qmd
  page-footer:
    left: "Synthetic data only. Never put patient data in a repository."
    right: "Text CC BY 4.0 · Code MIT"

format:
  html:
    theme:
      light: flatly
      dark: darkly
    css: styles.css
    toc: true
    toc-depth: 3
    code-copy: true
    code-overflow: wrap
```

(The TJS branding here is temporary; Task 8 replaces it.)

- [ ] **Step 6: `Justfile` data recipe**

In the `data:` recipe, replace the five `quarto render <folder>` lines with:

```
    quarto render en/foundations
    quarto render en/catalog
    quarto render en/survival
    quarto render en/beyond
    quarto render en/report
```

- [ ] **Step 7: `CLAUDE.md` layout**

Replace the `## Layout` section's first bullet with:

```markdown
- Pages: `en/`, `de/`, `fr/`, one folder per language with the same file names (HFR spec §4.3). In each: `index.qmd` (the welcome page), `choose-a-test.qmd` (the decision table), `tests-a-z.qmd` (every test and method, with aliases; `tests/site/test_home.py` fails if a test section is missing from it), `getting-started/`, `foundations/`, `catalog/` (pages 4–12, one per table row), `survival/`, `beyond/`, `report/`. The root `index.qmd` only sends visitors to a language.
- `scripts/`: `check_setup.R` and `check_setup.py`, the setup checks readers run
- Code on every page runs from the repo root (`execute-dir: project`), so pages read `data/…` and `source("R/check_agree.R")` whatever their folder.
```

- [ ] **Step 8: Render and check that the frozen results were reused**

Run: `quarto render && git status --short _freeze | grep -v '^R ' | head`
Expected: the render succeeds and the second command prints nothing (only renames). If Quarto re-executed some pages anyway, their `_freeze/en/…` JSON shows as modified; that's acceptable as long as Step 9 passes, because the code and seeds are unchanged.

- [ ] **Step 9: Run every check**

Run: `just test && uv run pytest tests/site -q && lychee --offline --include-fragments --no-progress _site`
Expected: all pass.

- [ ] **Step 10: Commit**

```bash
git add -A
git status --short | grep '^??'   # expected: no output (nothing left untracked)
git commit -m "Move every page under en/, with its frozen results; one sidebar with id en; a root page; tests read _site/en

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 5: "Working with real HFR data"

**Files:**
- Modify: `en/getting-started/real-data.qmd` (full rewrite)
- Test: `tests/site/test_getting_started.py`

**Interfaces:**
- Consumes: Task 4 (`load()` reads `_site/en/`).
- Produces: the page's fixed section IDs `swiss-rules`, `coded`, `general-consent`, `identifiers`, `traps`, `where`, `in-code`, `ai`, `before-commit`, `incident` (translations keep them).

- [ ] **Step 1: Replace the TJS tests with Swiss ones**

In `tests/site/test_getting_started.py`, delete `test_real_data_page_lists_all_18_safe_harbor_identifiers`, `test_real_data_page_covers_tjs_traps`, `test_real_data_page_states_the_full_age_over_89_rule` and `test_real_data_page_warns_about_derived_study_ids`, add `text_of` to the import, and add:

```python
REAL = "getting-started/real-data.html"


def test_real_data_page_states_the_swiss_rules(site):
    text = text_of(load(REAL))
    for phrase in ["Human Research Act", "CER-VD", "BASEC", "Federal Act on Data Protection",
                   "coded", "code key", "general consent", "refused"]:
        assert phrase in text, phrase


def test_real_data_page_says_coded_data_are_never_anonymous(site):
    assert "with a code key are never anonymous" in text_of(load(REAL))


def test_real_data_page_covers_hfr_traps(site):
    text = load(REAL).get_text()  # no separator: keeps highlighted code intact
    for phrase in ["AHV", "patient number", "90 or older", "Quasi-identifiers", "implant", "DICOM", "AI",
                   "git status", "git diff --staged"]:
        assert phrase in text, phrase


def test_real_data_page_warns_about_derived_study_ids(site):
    text = load(REAL).get_text(" ")
    assert "study ID" in text and "initials" in text


def test_real_data_page_names_who_to_tell(site):
    assert "data protection officer" in text_of(load(REAL))


def test_real_data_page_has_no_us_law(site):
    text = text_of(load(REAL))
    for us in ["HIPAA", "Safe Harbor", "IRB", "ZIP", "Social Security", "PHI"]:
        assert us not in text, us
```

- [ ] **Step 2: Run them to see them fail**

Run: `quarto render en/getting-started/real-data.qmd && uv run pytest tests/site/test_getting_started.py -q`
Expected: the six new tests fail.

- [ ] **Step 3: Rewrite `en/getting-started/real-data.qmd`**

````markdown
---
title: "Working with real HFR data"
description: "Keeping patient data safe: the Swiss rules, what identifies a patient, where HFR data lives, and the checks to run before every commit."
---

Everything on this site uses invented data. Your real project won't. This page covers the rules that keep patients and HFR safe. Read it before you open any real dataset.

::: {.callout-warning}
## ⚠️ The one rule
**Patient data never goes into a git repository.** That includes private repositories, commits, GitHub issues, screenshots and chat messages. This site's repository is **public**: anything committed here can be read by anyone on the internet, forever. Never copy real data anywhere inside this tutorial folder, including `data/` and `scratch/`.
:::

## The Swiss rules {#swiss-rules}

Two laws apply to every HFR research project that uses patient data:

- **The Human Research Act** (HRA; in German HFG, in French LRH) and its ordinances. Research with health data needs approval from the cantonal ethics committee before anyone touches the data. For HFR that is the CER-VD, and every project gets a BASEC number when it is submitted. Clinical trials, such as randomized trials, also fall under the Clinical Trials Ordinance (ClinO; in German KlinV, in French OClin).
- **The Federal Act on Data Protection** (FADP; in German DSG, in French LPD), revised in 2023. Health data are sensitive personal data under this law.

Your project lead has the approval and the protocol. Read them before you start: they say which data you may use and how.

### Coded, not anonymous {#coded}

HFR studies work with **coded** data. Each patient gets a study code (for example `C0001`), and a separate **code key** links the codes back to the patients. The project lead keeps the code key, apart from the study data and never in a repository.

"Coded" and "anonymous" mean different things in Swiss law. Data are anonymous only when they can no longer be linked back to a person, so data with a code key are never anonymous. Use the word "coded" in everything you write, including emails, protocols and Methods sections.

### General consent {#general-consent}

HFR asks patients for a **general consent** to the use of their data for research. Only patients with a signed general consent go into a study, unless the ethics committee approved something else for your project. Patients who **refused** are never included and never contacted.

## What identifies a patient {#identifiers}

**Direct identifiers** never leave the clinical systems:

- names, initials, date of birth, address, phone numbers, email addresses
- the AHV/AVS number (`756.…`), HFR patient numbers and case numbers
- implant serial and lot numbers
- photographs of patients, and images with names burned in

**Quasi-identifiers** identify patients in combination. In a small cohort, age + sex + surgery date + hospital can point to one person. Coarsen them before data leave the secure environment:

- age in bands, with "90 or older" for the very old
- the surgery month or year, or "days from surgery", instead of the date
- "a Swiss regional hospital" instead of the hospital's name, where the protocol allows it

## HFR traps {#traps}

- **Surgery dates are dates.** Use "days from surgery" or the surgery year instead.
- **Very old patients.** In a small cohort an age of 97 can identify someone. Group them as "90 or older".
- **Study IDs built from patient details.** A study ID made from initials, a patient number or a birth date (like `JS-0412`) is still an identifier. Use arbitrary codes such as `C0001`.
- **Patient numbers hide in file names.** Watch for names like `12345678_xray.png` or `extraction_AHV.xlsx`.
- **Implant stickers.** Lot and serial numbers are device identifiers.
- **Radiographs.** DICOM files carry the patient's name, patient number and dates in their headers, and some images have them burned into the pixels.
- **Free-text "notes" columns.** They collect names, phone numbers and dates.
- **Screenshots of the patient record.** They're patient data too.

## Where HFR data lives {#where}

- Study data stay where your project lead keeps them for the project, for example the project's REDCap database. Don't copy them anywhere else.
- Analysis code lives in a project repository in HFR Ortho's private GitHub organization. The repository reads the data at run time from git-ignored folders (`data/raw/`, `db/`, `exports/`) that are listed in `.gitignore` *before the first commit*.
- The code key lives only with the project lead, never in a repository.
- What leaves the secure environment is aggregate: tables, figures and model results. Your protocol may require hiding small counts.

## How HFR projects handle data in code {#in-code}

These rules come from HFR Ortho project repositories. [Tidy data](../foundations/01-tidy-data.qmd) practices each one.

1. **Read everything as text at first.** Dates arrive in several formats, numbers contain stray text, and lists sit inside single cells. Convert types as a deliberate, recorded step, never silently while reading.
2. **Match columns by name, not position.** Two tabs of the same sheet can have different columns.
3. **Check what you changed.** After every cleaning step, compare row counts and summaries before and after.

## AI tools {#ai}

**Never paste real patient data into an AI chatbot or any website.** That includes ChatGPT, Claude, Copilot and online "data cleaners". The only exception is a tool HFR has approved for patient data; ask your project lead. The synthetic data on this site is fine to paste anywhere.

## Before every commit {#before-commit}

Run these two commands and read the output:

```bash
git status
git diff --staged
```

Check that no data file, export or screenshot is listed. If you see one, unstage it with `git restore --staged <file>`.

## If something goes wrong {#incident}

If patient data reaches a commit, a push or an issue:

1. **Stop.** Don't try to fix it with another commit. Git keeps the history.
2. **Tell your project lead right away.** The data has to be purged from history, and the incident may have to be reported to HFR's data protection officer.

Reporting quickly is always the right call, and nobody will be upset that you did.
````

- [ ] **Step 4: Run the tests**

Run: `quarto render en/getting-started/real-data.qmd && uv run pytest tests/site/test_getting_started.py -q`
Expected: all pass.

- [ ] **Step 5: Full check, then commit**

Run: `just check`
Expected: all pass.

```bash
git add en/getting-started/real-data.qmd tests/site/test_getting_started.py
git commit -m "Working with real HFR data: Swiss law (HRA, FADP), coded not anonymous, general consent, quasi-identifiers, HFR traps

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

Doc reviews this page's wording in Task 11 (spec §4.8), including the storage line under "Where HFR data lives".

---

### Task 6: Swiss day-first dates and HFR labels in the synthetic data

**Files:**
- Modify: `data-raw/R/gen_messy_workbook.R:61-70,165,168,207`, `data-raw/make_template.R:25,29-30`, `en/foundations/01-tidy-data.qmd` (Step 5 date parsing, the 🔀 dates box, "What a failing check looks like", the prose guards)
- Regenerated by `just data`: `data/messy_abstraction_workbook.xlsx`, `templates/data-collection-template.xlsx`, `_freeze/en/**`
- Test: `tests/testthat/test-data-workbook.R:49-57`

**Interfaces:**
- Consumes: Task 4's `Justfile` (`quarto render en/…`).
- Produces: `fmt_date_text(d)` returns `"DD.MM.YY"`, ISO `"YYYY-MM-DD"` or `"D.M.YYYY"`; page 1's `parse_messy_date(x, day_first = TRUE)` (R) and `parse_messy_date(col, dayfirst=True)` (Python).

- [ ] **Step 1: Write the failing R test**

In `tests/testthat/test-data-workbook.R`, replace the test `"text dates use English month names whatever the computer's locale"` with:

```r
test_that("text dates are Swiss day-first or ISO", {
  env <- new.env()
  sys.source(testthat::test_path("..", "..", "data-raw", "R", "gen_messy_workbook.R"), envir = env)
  withr::local_seed(1)
  out <- env$fmt_date_text(rep(as.Date("2024-03-04"), 50))
  expect_setequal(out, c("04.03.24", "2024-03-04", "4.3.2024"))
})
```

Run: `Rscript -e 'testthat::test_dir("tests/testthat", filter = "data-workbook")'`
Expected: FAIL (`"3/4/24"`, `"March 4 2024"` returned).

- [ ] **Step 2: Change the generator**

In `data-raw/R/gen_messy_workbook.R`, replace `fmt_date_text()` with:

```r
fmt_date_text <- function(d) {
  # Swiss sheets write the day first: "04.03.24" or "4.3.2024"; some cells are ISO dates.
  # The same three-way draw as before, so every other random number in data/ stays the same.
  style <- sample(c("dmy_short", "iso", "dmy_long"), length(d), TRUE)
  month <- as.integer(format(d, "%m"))
  day   <- as.integer(format(d, "%d"))
  ifelse(style == "dmy_short",
         sprintf("%02d.%02d.%s", day, month, format(d, "%y")),
         ifelse(style == "iso", format(d, "%Y-%m-%d"),
                sprintf("%d.%d.%s", day, month, format(d, "%Y"))))
}
```

In the same file, `"TJS Outcomes Abstraction - %s (SYNTHETIC DATA - NOT REAL PATIENTS)"` becomes `"HFR Ortho Outcomes Abstraction - %s (SYNTHETIC DATA - NOT REAL PATIENTS)"`, `"Abstractor: RA | Last updated: 1/15/2026 | DO NOT SORT"` becomes `"Abstractor: RA | Last updated: 15.01.2026 | DO NOT SORT"`, and `creator = "TJS synthetic data generator"` becomes `creator = "HFR Ortho synthetic data generator"`.

In `data-raw/make_template.R`: `creator = "TJS stats tutorials"` becomes `creator = "HFR Ortho stats tutorials"`; the README line `"TJS data-collection template"` becomes `"HFR Ortho data-collection template"`; and line 2 of the README becomes:

```r
  "2. Never type patient names or patient numbers here. Use the study code; the project lead keeps the code key (patient number to study code) in a separate, secured file.",
```

Run: `Rscript -e 'testthat::test_dir("tests/testthat", filter = "data-workbook")'`
Expected: PASS.

- [ ] **Step 2b: Regenerate the data files now (no rendering yet)**

Page 1 must be rendered against the new workbook, so write it first:

```bash
Rscript data-raw/generate.R && Rscript data-raw/make_template.R && Rscript data-raw/validate.R
uv run pytest tests/python -q
git status --short data templates
```

Expected: validation and tests pass, and only `data/messy_abstraction_workbook.xlsx` and `templates/data-collection-template.xlsx` changed. If any CSV or `data/CHECKSUMS.md5` changed, the random draws moved: stop and compare `fmt_date_text()` with Step 2.

- [ ] **Step 3: Parse day-first in page 1 (R)**

In `en/foundations/01-tidy-data.qmd`, Step 5's R chunk, replace the comment and `parse_messy_date()` with:

```r
# Dates arrive as Excel serial numbers ("42010"), ISO dates ("2015-04-21"),
# or Swiss day-first text ("13.01.15", "13.1.2015"). Handle the serial
# numbers, then the ISO dates, then read the rest day-first.
parse_messy_date <- function(x, day_first = TRUE) {
  serial <- !is.na(x) & str_detect(x, "^\\d{5}$")
  iso    <- !is.na(x) & str_detect(x, "^\\d{4}-\\d{2}-\\d{2}$")
  rest   <- !is.na(x) & !serial & !iso
  out <- as.Date(rep(NA, length(x)))
  out[serial] <- janitor::excel_numeric_to_date(as.numeric(x[serial]))
  out[iso]    <- ymd(x[iso])
  out[rest]   <- if (day_first) dmy(x[rest], quiet = TRUE) else mdy(x[rest], quiet = TRUE)
  out
}
```

- [ ] **Step 4: Parse day-first in page 1 (Python)**

In Step 5's Python chunk, just above `tidy = pd.DataFrame({`, add:

```python
def parse_messy_date(col, dayfirst=True):
    """Real Excel dates arrive as date-times. Text dates are ISO ("2015-04-21") or Swiss
    day-first ("13.01.15", "13.1.2015"). dayfirst=True would also flip ISO dates, so
    they're read on their own."""
    text = col.where(col.map(type) == str)                 # the text cells; Excel dates become NaN
    iso = text.str.fullmatch(r"\d{4}-\d{2}-\d{2}", na=False)
    excel = pd.to_datetime(col.where(text.isna()))         # the real Excel dates (and empty cells)
    return (excel
            .fillna(pd.to_datetime(text[iso], format="%Y-%m-%d"))
            .fillna(pd.to_datetime(text[text.notna() & ~iso], format="mixed", dayfirst=dayfirst)))
```

and in the `pd.DataFrame({…})` replace the three `pd.to_datetime(step3[…], format="mixed")` calls with `parse_messy_date(step3["dos"])`, `parse_messy_date(step3["prom_preop_date"])` and `parse_messy_date(step3["prom_1yr_date"])`.

- [ ] **Step 5: The 🔀 dates box**

Replace its body with:

```markdown
R needs a separate step for Excel serial numbers (`janitor::excel_numeric_to_date()`). pandas already turned those cells into date-times, so its `parse_messy_date()` only reads the text cells. Both read `"13.01.15"` day-first: Swiss style, which is what HFR sheets use. Both read ISO dates on their own, because pandas' `dayfirst=True` would also flip them (`2015-11-02` would become 11 February).
```

- [ ] **Step 6: "What a failing check looks like": the mistake becomes month-first**

- The opening sentence: `Suppose we had parsed the surgery dates month-first (US style, as many online examples do) by mistake. Nothing crashes. Two checks catch it: a missing count (check 2, applied to the dates) and a new logic check that every pre-op PROM falls within a month before surgery.`
- R chunk: `wrong <- parse_messy_date(step3$dos, day_first = FALSE)   # the mistake`; the names `missing_day_first`/`window_day_first` become `missing_month_first`/`window_month_first`.
- Python chunk:

```python
wrong = parse_messy_date(step3["dos"], dayfirst=False)   # the mistake
preop = parse_messy_date(step3["prom_preop_date"])

def outside_window(surgery):
    days_before = (surgery - preop).dt.days
    return int(((days_before < 0) | (days_before > 31)).sum())

print(pd.Series({
    "missing_correct": tidy["surgery_date"].isna().sum(),
    "missing_month_first": wrong.isna().sum(),
    "window_correct": outside_window(parse_messy_date(step3["dos"])),
    "window_month_first": outside_window(wrong),
}))
```

- [ ] **Step 7: Render page 1 and read the new numbers**

Run: `quarto render en/foundations/01-tidy-data.qmd`
Expected: it fails at a prose guard (the old 37 / 7 / 36 no longer hold) **or** at the hidden answer-key check. If the answer-key check fails, the parsing is wrong: fix Steps 3–4, never the key. When only the prose guards fail, read the four numbers printed by the R chunk and by the Python chunk in `_site/en/foundations/01-tidy-data.html` (or temporarily comment out the guards' `stopifnot`/`assert` lines to get a render). Call them R: `missing_month_first` = **A**, `window_month_first` = **B**; Python: `missing_month_first` = **C**, `window_month_first` = **D**.

- [ ] **Step 8: Update the prose and both guards with A–D**

Replace the two bullets after "With the correct parse, nothing is missing…" (and change "The day-first versions" in that sentence to "The month-first versions"):

```markdown
- **R** can't read dates like `"13.01.15"` month-first (there's no 13th month), so A surgery dates go missing. Others, like `"04.03.24"`, parse "successfully" as 3 April instead of 4 March, and the window check flags B of them.
- **pandas** never returns a missing date here: when month-first is impossible it quietly switches to day-first, so `"13.01.15"` comes out right by luck while `"04.03.24"` becomes 3 April. Only the window check notices: it flags D dates.
```

with the real numbers in place of A, B and D. If C isn't 0, the pandas bullet is wrong: rewrite it to say what C shows. In the ⚠️ box replace its first sentence with `Never parse a column that mixes formats with one setting: read each format on its own, as parse_messy_date() does.` and keep the rest. Prose guards: Python side `assert int(wrong.isna().sum()) == C and outside_window(wrong) == D`; R side `sum(is.na(wrong)) == A,` and `outside_window(wrong) == B,`. Then check for leftovers:

Run: `grep -n -E '1/13/15|February 10|3/4/24|day-first versions|orders = c|format="mixed"\)' en/foundations/01-tidy-data.qmd`
Expected: no output.

- [ ] **Step 9: Re-render everything that reads the data**

Run: `just data`
Expected: the generator (which rewrites the same files as Step 2b), `validate.R`, the Python data tests and the five `quarto render en/…` steps all succeed. This is also the first time every page runs its code from `en/`.

Run: `git status --short data templates`
Expected: the same two `.xlsx` files as in Step 2b, nothing else.

- [ ] **Step 10: Run every check and commit**

Run: `just test && just check`
Expected: all pass.

```bash
git add -A data-raw data templates en _freeze tests
git commit -m "Swiss day-first dates in the messy workbook and page 1 (ISO dates read on their own; the mistake is now month-first); HFR labels in the workbook and template

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 7: HFR wording on the remaining English pages

**Files:**
- Modify: `en/index.qmd:2,8,12,24`, `en/getting-started/using-this-site.qmd:96,146`, `en/getting-started/setup.qmd:173`, `en/foundations/01-tidy-data.qmd:88,154`, `en/foundations/02-demographics.qmd:266`, `en/foundations/03-distributions.qmd:452`
- Create: `tests/python/test_branding.py`
- Test: `tests/site/test_home.py`, `tests/site/test_conventions.py`

**Interfaces:**
- Consumes: Task 6 (page 1's 🔀 box no longer says "TJS").
- Produces: `tests/python/test_branding.py` with `offenders(paths) -> list[str]` and `tracked(*paths) -> list[str]`; Task 8 adds a test to this file.

- [ ] **Step 1: Write the failing tests**

Create `tests/python/test_branding.py`:

```python
"""No TJS branding outside the credit and history (HFR spec §4.6).

Allowed: the credit phrase "TJS Statistics Tutorials"; the license files; TJS's and HFR's specs and plans;
README.md and CLAUDE.md, which explain where the repo came from; and the tests that check all this."""

import re
import subprocess
import sys
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parents[2]
TJS = re.compile(r"TJS|Total Joint|tjs-|\bJOA\b")
CREDIT = "TJS Statistics Tutorials"
EXEMPT = ("docs/superpowers/", "LICENSE", "README.md", "CLAUDE.md",
          "tests/python/test_branding.py", "tests/python/test_repo_docs.py")
BINARY = {".png", ".jpg", ".svg", ".xlsx", ".docx", ".zip"}


def tracked(*paths):
    """Files git tracks under these paths (all of them if none), minus the exempt ones."""
    out = subprocess.run(["git", "ls-files", "--", *paths], cwd=ROOT, capture_output=True, text=True, check=True)
    return [p for p in out.stdout.splitlines() if not p.startswith(EXEMPT)]


def offenders(paths):
    """Lines that mention TJS other than in the credit phrase, as "file:line: text"."""
    found = []
    for rel in paths:
        if Path(rel).suffix in BINARY:
            continue
        lines = (ROOT / rel).read_text(encoding="utf-8", errors="ignore").splitlines()
        for number, line in enumerate(lines, 1):
            if TJS.search(line.replace(CREDIT, "")):
                found.append(f"{rel}:{number}: {line.strip()[:100]}")
    return found


def workbook_text(path):
    wb = openpyxl.load_workbook(ROOT / path)
    cells = [str(c.value) for ws in wb.worksheets for row in ws.iter_rows() for c in row if c.value is not None]
    return [wb.properties.creator or ""] + cells


def test_rule_flags_tjs_but_not_the_credit(tmp_path, monkeypatch):
    monkeypatch.setattr(sys.modules[__name__], "ROOT", tmp_path)
    (tmp_path / "a.qmd").write_text("Ask your TJS project lead.\nAdapted from the TJS Statistics Tutorials.\n")
    assert offenders(["a.qmd"]) == ["a.qmd:1: Ask your TJS project lead."]


def test_pages_never_mention_tjs():
    assert offenders(tracked("en", "index.qmd")) == []


def test_data_and_generators_never_mention_tjs():
    assert offenders(tracked("data", "data-raw", "templates", "scripts", "R")) == []
    for workbook in ["data/messy_abstraction_workbook.xlsx", "templates/data-collection-template.xlsx"]:
        assert [t for t in workbook_text(workbook) if TJS.search(t)] == [], workbook
```

In `tests/site/test_home.py`, add:

```python
def test_home_page_names_hfr_readers_and_journals(site):
    text = main_text(HOME)
    assert "HFR Ortho residents, research assistants and medical students doing their master's thesis" in text
    assert "The Bone & Joint Journal" in text and "CORR" in text
    assert text_of(load(HOME).select_one("h1.title")) == "HFR Ortho Statistics Tutorials"
```

In `tests/site/test_conventions.py`, add:

```python
def test_reporting_rules_name_the_journals(site):
    text = text_of(load("getting-started/using-this-site.html"))
    assert "JBJS, The Bone & Joint Journal and CORR" in text
```

Run: `uv run pytest tests/python/test_branding.py -q; uv run pytest tests/site/test_home.py tests/site/test_conventions.py -q`
Expected: `test_pages_never_mention_tjs`, the home test and the journals test fail. (`test_data_and_generators_never_mention_tjs` already passes after Task 6.)

- [ ] **Step 2: Edit the pages**

| File | Old | New |
|------|------|------|
| `en/index.qmd` | `title: "TJS Statistics Tutorials"` | `title: "HFR Ortho Statistics Tutorials"` |
| `en/index.qmd` | `These tutorials teach Total Joint Specialists research assistants to prepare data, choose the right statistical test, run it, and report it the way JOA and JBJS reviewers expect.` | `These tutorials teach HFR Ortho residents, research assistants and medical students doing their master's thesis to prepare data, choose the right statistical test, run it, and report it the way reviewers at journals such as JBJS, *The Bone & Joint Journal* and *CORR* expect.` |
| `en/index.qmd` (twice) | `Working with real TJS data` | `Working with real HFR data` |
| `en/getting-started/using-this-site.qmd` | `which match what JOA and JBJS reviewers expect.` | `which match what reviewers at journals such as JBJS, *The Bone & Joint Journal* and *CORR* expect.` |
| `en/getting-started/using-this-site.qmd` | `Ask your TJS project lead.` | `Ask your project lead.` |
| `en/getting-started/setup.qmd` | `send it to your TJS project lead.` | `send it to your project lead.` |
| `en/foundations/01-tidy-data.qmd` | `Untidy patterns we see most often in TJS sheets` | `Untidy patterns we see most often in abstraction sheets` |
| `en/foundations/01-tidy-data.qmd` | `copies the problems we see in TJS sheets.` | `copies the problems we see in real abstraction sheets.` |
| `en/foundations/02-demographics.qmd` | `such as TJS's age-80 matched study` | `such as a matched study of patients over 80` |
| `en/foundations/03-distributions.qmd` | `Some worked examples from TJS-style questions:` | `Some worked examples from typical orthopaedic research questions:` |

Then: `git grep -n -E "TJS|Total Joint|JOA" -- en index.qmd`
Expected: no output.

- [ ] **Step 3: Render and run every check**

Run: `just check && uv run pytest tests/python -q`
Expected: all pass. Pages 1–3 and using-this-site re-execute (their text changed).

- [ ] **Step 4: Commit**

```bash
git add -A en _freeze tests
git commit -m "HFR wording: the home page names HFR Ortho readers and JBJS, The Bone & Joint Journal and CORR; no TJS left on any English page

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 8: HFR branding: logo, favicon, colours, footer, site addresses

**Files:**
- Create: `images/hfr-mark-white.svg`, `images/hfr-icon.svg`, `theme/hfr-light.scss`, `theme/hfr-dark.scss`
- Delete: `images/tjs-icon.png`, `images/tjs-logo.png`, `images/tjs-logo-dark.png`
- Modify: `_quarto.yml` (`website:` header lines, `navbar:`, sidebar `logo:`, `page-footer:`, `format: html: theme:`)
- Create test: `tests/python/test_theme.py`
- Test: `tests/site/test_structure.py` (logo, icon, footer), `tests/python/test_branding.py` (whole repo)

**Interfaces:**
- Consumes: Task 7's `tracked()` and `offenders()`.
- Produces: SCSS variables `$primary`, `$link-color`, `$navbar-bg`, `$navbar-fg` (both themes) and `$headings-color` (light); images `images/hfr-mark-white.svg` (top bar) and `images/hfr-icon.svg` (favicon).

- [ ] **Step 1: Write the failing tests**

Create `tests/python/test_theme.py`:

```python
"""HFR colours meet WCAG AA contrast (4.5 : 1) in both themes (HFR spec §4.4)."""

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
WHITE, DARKLY_BODY = "#ffffff", "#222222"   # Flatly's and Darkly's page backgrounds


def variables(name):
    """The theme file's $variables, with references to other variables resolved."""
    text = (ROOT / "theme" / name).read_text(encoding="utf-8")
    raw = dict(re.findall(r"^\$([\w-]+):\s*([^;]+);", text, re.MULTILINE))

    def resolve(value):
        value = value.strip()
        return resolve(raw[value[1:]]) if value.startswith("$") else value

    return {key: resolve(value) for key, value in raw.items()}


def luminance(colour):
    channels = [int(colour.lstrip("#")[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    linear = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast(a, b):
    high, low = sorted([luminance(a), luminance(b)], reverse=True)
    return (high + 0.05) / (low + 0.05)


def test_contrast_matches_known_values():
    assert contrast("#000000", "#ffffff") == pytest.approx(21.0)
    assert contrast("#777777", "#ffffff") == pytest.approx(4.48, abs=0.01)


@pytest.mark.parametrize("theme,background", [("hfr-light.scss", WHITE), ("hfr-dark.scss", DARKLY_BODY)])
def test_text_is_readable(theme, background):
    v = variables(theme)
    assert contrast(v["link-color"], background) >= 4.5
    assert contrast(v["navbar-fg"], v["navbar-bg"]) >= 4.5
    assert contrast("#ffffff", v["primary"]) >= 4.5          # white text on primary buttons
    if "headings-color" in v:
        assert contrast(v["headings-color"], background) >= 4.5


def test_brand_colours_are_hfr():
    light, dark = variables("hfr-light.scss"), variables("hfr-dark.scss")
    assert light["primary"].upper() == "#006DB5" and light["link-color"].upper() == "#006DB5"
    assert light["navbar-bg"].upper() == "#103379" and dark["navbar-bg"].upper() == "#103379"
```

In `tests/site/test_structure.py`, replace `test_every_page_carries_the_tjs_logo_in_both_themes` and `test_the_browser_tab_shows_the_tjs_mark` with:

```python
def test_every_page_carries_the_hfr_mark_in_the_top_bar(site):
    for page in PAGES:
        logos = load(page).select("img.navbar-logo")
        assert logos, page
        assert all(img["src"].endswith("images/hfr-mark-white.svg") for img in logos), page
        assert all(img.get("alt") == "HFR Hôpital fribourgeois" for img in logos), page
    assert (SITE_ROOT / "images" / "hfr-mark-white.svg").exists()


def test_the_browser_tab_shows_the_hfr_mark(site):
    icon = load("index.html").select_one('link[rel="icon"]')
    assert icon is not None and icon["href"].endswith("images/hfr-icon.svg")
    assert (SITE_ROOT / "images" / "hfr-icon.svg").exists()


def test_footer_says_synthetic_in_three_languages_and_credits_tjs(site):
    footer = text_of(load("index.html").select_one("footer"))
    assert "Synthetic data only · Nur synthetische Daten · Données synthétiques uniquement" in footer
    assert "Adapted from the TJS Statistics Tutorials" in footer
```

(import `text_of` too). In `tests/python/test_branding.py`, add:

```python
def test_nothing_in_the_repo_mentions_tjs():
    assert offenders(tracked()) == []
    assert not list((ROOT / "images").glob("tjs-*")), "remove the TJS images"
```

Run: `uv run pytest tests/python/test_theme.py tests/python/test_branding.py -q; quarto render && uv run pytest tests/site/test_structure.py -q`
Expected: FAIL (no theme files, TJS images and config, no navbar logo).

- [ ] **Step 2: Make the logo files from h-fr.ch**

```bash
D=$(mktemp -d)
curl -sL https://www.h-fr.ch/ -o "$D/hfr-home.html"
python3 -I - "$D/hfr-home.html" <<'EOF'
import sys
from pathlib import Path

html = Path(sys.argv[1]).read_text(encoding="utf-8")
start = html.index('class="site-logo')
svg = html[html.index("<svg", start): html.index("</svg>", start) + len("</svg>")]
svg = svg.replace(' class="max-md:w-[50px]"', "")
assert svg.count('fill="#006DB5"') == 4, "the h-fr.ch logo has changed: look at it before using it"
Path("images/hfr-mark-white.svg").write_text(svg.replace('fill="#006DB5"', 'fill="#FFFFFF"') + "\n", encoding="utf-8")
square = svg.replace('width="75" height="48" viewBox="0 0 75 48"', 'width="75" height="75" viewBox="0 -13.5 75 75"')
assert square != svg, "the logo's size changed: adjust the square view box"
Path("images/hfr-icon.svg").write_text(square + "\n", encoding="utf-8")
EOF
git rm images/tjs-icon.png images/tjs-logo.png images/tjs-logo-dark.png
```

Open both SVGs in a browser and check by eye: the white mark (on a dark background) and the blue square icon.

- [ ] **Step 3: Theme files**

`theme/hfr-light.scss`:

```scss
/*-- scss:defaults --*/
// HFR colours (h-fr.ch): blue for links and buttons, navy for the top bar and headings.
$hfr-blue: #006DB5;
$hfr-navy: #103379;

$primary: $hfr-blue;
$link-color: $hfr-blue;
$navbar-bg: $hfr-navy;
$navbar-fg: #ffffff;
$headings-color: $hfr-navy;
```

`theme/hfr-dark.scss`:

```scss
/*-- scss:defaults --*/
// HFR colours on Darkly. #006DB5 is too dark to read as link text on Darkly's #222 page,
// so links use a lighter tint of it; buttons keep the HFR blue under white text.
$hfr-blue: #006DB5;
$hfr-blue-light: #5AA9E6;
$hfr-navy: #103379;

$primary: $hfr-blue;
$link-color: $hfr-blue-light;
$navbar-bg: $hfr-navy;
$navbar-fg: #ffffff;
```

- [ ] **Step 4: `_quarto.yml`**

Replace the lines from `  title: "TJS Statistics Tutorials"` to `  favicon: images/tjs-icon.png` with:

```yaml
  title: "HFR Ortho Stats"
  description: "Tidy data, Table 1, and every common statistical test, in R and Python, in English, German and French, for HFR Ortho residents, research assistants and medical students."
  site-url: "https://hfr-ortho.github.io/stats-formation/"
  repo-url: "https://github.com/hfr-ortho/stats-formation"
  repo-actions: [issue]
  search: true
  page-navigation: true
  favicon: images/hfr-icon.svg
```

Under `navbar:`, add above `left:`:

```yaml
    title: "HFR Ortho"
    logo: images/hfr-mark-white.svg
    logo-alt: "HFR Hôpital fribourgeois"
```

and change the GitHub `href` to `"https://github.com/hfr-ortho/stats-formation"`. Delete the sidebar's whole `logo:` block (seven lines). Replace `page-footer:` with:

```yaml
  page-footer:
    left: "Synthetic data only · Nur synthetische Daten · Données synthétiques uniquement"
    right: "Adapted from the [TJS Statistics Tutorials](https://total-joint-specialists.github.io/example-stats-analysis/) · Text CC BY 4.0 · Code MIT"
```

Replace `theme:` under `format: html:` with:

```yaml
    theme:
      light: [flatly, theme/hfr-light.scss]
      dark: [darkly, theme/hfr-dark.scss]
```

- [ ] **Step 5: Run every check**

Run: `uv run pytest tests/python -q && just check`
Expected: all pass. No page re-executes (only site-wide settings changed).

- [ ] **Step 6: Look at it**

Run: `just preview`, open the address it prints, and check in **both** light and dark mode (the toggle is in the top bar): the white HFR mark and "HFR Ortho" on the navy bar, readable blue links, navy headings in light mode, the favicon in the browser tab, the footer. Stop the preview.

- [ ] **Step 7: Commit**

```bash
git add -A images theme _quarto.yml tests
git commit -m "HFR branding: the HFR mark in white on a navy top bar, HFR blue links, SVG favicon, trilingual footer crediting TJS, HFR site and repo addresses

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 9: German and French: sidebars, home pages, stubs, fixed section IDs

**Files:**
- Create: `de/_metadata.yml`, `fr/_metadata.yml`, `de/index.qmd`, `fr/index.qmd`, 22 stubs in each of `de/` and `fr/` (same paths as `en/`, except `index.qmd`)
- Modify: `index.qmd` (root), `_quarto.yml` (full replacement), `CLAUDE.md` (rule 7, new rule 21)
- Create tests: `tests/site/test_languages.py`, `tests/site/test_anchors.py`
- Modify tests: `tests/site/test_structure.py` (drop `test_root_page_links_the_english_site`), `tests/python/test_repo_docs.py`

**Interfaces:**
- Consumes: `sitelib.LANGS`, `SITE_ROOT`, `ROOT`, `PAGES`, `target(page, href, lang)` (Task 4).
- Produces: `STUB_MARK = {"de": "(in Vorbereitung)", "fr": "(en préparation)"}` in `tests/site/test_languages.py`; `fragment_links_without_fixed_ids(path) -> list[str]` in `tests/site/test_anchors.py`; top-bar links whose text is exactly `EN`, `DE`, `FR` (Task 10's script finds them by that text).

- [ ] **Step 1: Write the failing tests**

Create `tests/site/test_languages.py`:

```python
"""The three languages (HFR spec §4.3): the same pages everywhere, each with its own sidebar and `lang`,
stubs that lead back to English, top-bar language links, and a root page that works without JavaScript."""

from bs4 import BeautifulSoup

from sitelib import LANGS, PAGES, ROOT, SITE_ROOT, target, text_of

STUB_MARK = {"de": "(in Vorbereitung)", "fr": "(en préparation)"}
WARNING = {"en": "SYNTHETIC DATA", "de": "SYNTHETISCHE DATEN", "fr": "DONNÉES SYNTHÉTIQUES"}
HOME_LINKS = {"getting-started/setup.html", "getting-started/using-this-site.html", "getting-started/real-data.html",
              "foundations/01-tidy-data.html", "catalog/04-describe-one-group.html", "survival/13-kaplan-meier.html",
              "beyond/15-post-hoc.html", "report/18-example-report.html", "choose-a-test.html", "tests-a-z.html"}


def load_lang(lang, page):
    return BeautifulSoup((SITE_ROOT / lang / page).read_text(encoding="utf-8"), "html.parser")


def sources(lang):
    return sorted(str(p.relative_to(ROOT / lang)) for p in (ROOT / lang).rglob("*.qmd"))


def test_every_page_exists_in_every_language():
    for lang in ["de", "fr"]:
        assert sources(lang) == sources("en"), lang


def test_every_page_is_built_in_every_language(site):
    for lang in LANGS:
        assert [p for p in PAGES if not (SITE_ROOT / lang / p).exists()] == [], lang


def test_pages_declare_their_language(site):
    for lang in LANGS:
        assert (ROOT / lang / "_metadata.yml").read_text(encoding="utf-8").strip() == f"lang: {lang}"
        for page in PAGES:
            assert load_lang(lang, page).html.get("lang") == lang, f"{lang}/{page}"


def test_each_language_has_its_own_sidebar_in_the_same_order(site):
    def sidebar(lang, page):
        return [target(page, a["href"], lang) for a in load_lang(lang, page).select("#quarto-sidebar a.sidebar-link[href]")]

    english = sidebar("en", "index.html")
    assert set(PAGES) <= set(english)
    for lang in ["de", "fr"]:
        for page in ["index.html", "catalog/06-two-unpaired-groups.html"]:
            assert sidebar(lang, page) == english, f"{lang}/{page}"


def test_untranslated_pages_are_stubs_that_link_to_english(site):
    for lang, mark in STUB_MARK.items():
        for page in PAGES:
            if page == "index.html":
                continue
            soup = load_lang(lang, page)
            box = soup.select_one(".coming-soon")
            assert (mark in soup.title.get_text()) == (box is not None), f"{lang}/{page}"
            if box is not None:
                links = {target(page, a["href"], lang) for a in box.select("a[href]")}
                assert f"/en/{page}" in links, f"{lang}/{page} must link to the English page"


def test_home_pages_are_translated_and_link_the_same_pages(site):
    for lang in LANGS:
        soup = load_lang(lang, "index.html")
        assert soup.select_one(".coming-soon") is None, lang
        assert WARNING[lang] in text_of(soup.select_one("main")), lang
        links = {target("index.html", a["href"], lang) for a in soup.select("main a[href]")}
        assert HOME_LINKS <= links, f"{lang}: {sorted(HOME_LINKS - links)}"


def test_top_bar_links_every_language_home(site):
    for lang in LANGS:
        for page in ["index.html", "catalog/06-two-unpaired-groups.html"]:
            links = {a.get_text(strip=True): target(page, a["href"], lang)
                     for a in load_lang(lang, page).select("nav.navbar a.nav-link[href]")}
            for code in LANGS:
                expected = "index.html" if code == lang else f"/{code}/index.html"
                assert links.get(code.upper()) == expected, (lang, page, code)


def test_root_page_offers_every_language_without_javascript(site):
    soup = BeautifulSoup((SITE_ROOT / "index.html").read_text(encoding="utf-8"), "html.parser")
    hrefs = {a["href"].removeprefix("./") for a in soup.select("main a[href]")}
    assert {"en/index.html", "de/index.html", "fr/index.html"} <= hrefs
    assert soup.select_one("#quarto-sidebar") is None
```

Create `tests/site/test_anchors.py`:

```python
"""Links into a section use fixed IDs, the same in every language (HFR spec §4.3). The language switcher
keeps the #section when it changes language, so a section must have the same ID in every language."""

import re

from sitelib import LANGS, ROOT

LINK = re.compile(r"\]\(([^)\s]*#[^)\s]+)\)")
FIXED_ID = re.compile(r"\{#([A-Za-z][\w:.-]*)")


def fixed_ids(path):
    return set(FIXED_ID.findall(path.read_text(encoding="utf-8")))


def fragment_links_without_fixed_ids(path):
    """Links on this page whose #section isn't a fixed {#id} on the page they point to."""
    missing = []
    for link in LINK.findall(path.read_text(encoding="utf-8")):
        if "://" in link:
            continue
        file, fragment = link.split("#", 1)
        dest = path if not file else (path.parent / file).resolve()
        if not dest.exists() or fragment not in fixed_ids(dest):
            missing.append(link)
    return missing


def pages(lang):
    return sorted((ROOT / lang).rglob("*.qmd"))


def test_rule_flags_a_link_to_an_auto_generated_id(tmp_path):
    (tmp_path / "a.qmd").write_text("## Mann-Whitney U test\n")
    (tmp_path / "b.qmd").write_text("See [the test](a.qmd#mann-whitney-u-test).\n")
    assert fragment_links_without_fixed_ids(tmp_path / "b.qmd") == ["a.qmd#mann-whitney-u-test"]


def test_rule_accepts_a_link_to_a_fixed_id(tmp_path):
    (tmp_path / "a.qmd").write_text("## Mann-Whitney U test {#mann-whitney}\n")
    (tmp_path / "b.qmd").write_text("See [the test](a.qmd#mann-whitney) and [below](#here).\n\n## Here {#here}\n")
    assert fragment_links_without_fixed_ids(tmp_path / "b.qmd") == []


def test_every_section_link_targets_a_fixed_id():
    found = {str(p.relative_to(ROOT)): fragment_links_without_fixed_ids(p) for lang in LANGS for p in pages(lang)}
    assert {page: links for page, links in found.items() if links} == {}


def test_translated_pages_keep_every_fixed_id():
    for lang in ["de", "fr"]:
        for page in pages(lang):
            if ".coming-soon" in page.read_text(encoding="utf-8"):
                continue    # a stub: nothing translated yet
            missing = fixed_ids(ROOT / "en" / page.relative_to(ROOT / lang)) - fixed_ids(page)
            assert not missing, f"{page.relative_to(ROOT)} lacks {sorted(missing)}"
```

In `tests/site/test_structure.py`, delete `test_root_page_links_the_english_site` (replaced by the root-page test above). In `tests/python/test_repo_docs.py`, add `"Three languages"` and `"(in Vorbereitung)"` to the `CLAUDE.md` rule list.

Run: `uv run pytest tests/site/test_languages.py tests/site/test_anchors.py tests/python/test_repo_docs.py -q`
Expected: the language tests and the CLAUDE.md test fail; the anchor tests pass (every link already targets a fixed ID: they guard from now on).

- [ ] **Step 2: Language metadata and the 44 stubs**

```bash
mkdir -p de fr
printf 'lang: de\n' > de/_metadata.yml
printf 'lang: fr\n' > fr/_metadata.yml
python3 - <<'EOF'
from pathlib import Path

TITLES = {  # English page: (Deutsch, Français)
    "choose-a-test.qmd": ("Welchen statistischen Test soll ich verwenden?", "Quel test statistique utiliser ?"),
    "tests-a-z.qmd": ("Tests A–Z", "Tests de A à Z"),
    "getting-started/setup.qmd": ("Installieren & einrichten", "Installer et configurer"),
    "getting-started/using-this-site.qmd": ("So benutzen Sie diese Website", "Comment utiliser ce site"),
    "getting-started/real-data.qmd": ("Mit echten HFR-Daten arbeiten", "Travailler avec de vraies données HFR"),
    "foundations/01-tidy-data.qmd": ("1 · Aufgeräumte Daten (Tidy Data)", "1 · Données ordonnées (tidy data)"),
    "foundations/02-demographics.qmd": ("2 · Demografie (Tabelle 1)", "2 · Données démographiques (tableau 1)"),
    "foundations/03-distributions.qmd": ("3 · Verteilungen & Testwahl", "3 · Distributions et choix du test"),
    "catalog/04-describe-one-group.qmd": ("4 · Eine Gruppe beschreiben", "4 · Décrire un groupe"),
    "catalog/05-one-group-vs-hypothetical.qmd": ("5 · Eine Gruppe mit einem hypothetischen Wert vergleichen",
                                                 "5 · Comparer un groupe à une valeur hypothétique"),
    "catalog/06-two-unpaired-groups.qmd": ("6 · Zwei unverbundene Gruppen vergleichen", "6 · Comparer deux groupes indépendants"),
    "catalog/07-two-paired-groups.qmd": ("7 · Zwei verbundene Gruppen vergleichen", "7 · Comparer deux groupes appariés"),
    "catalog/08-three-plus-unmatched.qmd": ("8 · Drei oder mehr unverbundene Gruppen vergleichen",
                                            "8 · Comparer trois groupes indépendants ou plus"),
    "catalog/09-three-plus-matched.qmd": ("9 · Drei oder mehr verbundene Gruppen vergleichen",
                                          "9 · Comparer trois groupes appariés ou plus"),
    "catalog/10-association.qmd": ("10 · Den Zusammenhang zweier Variablen quantifizieren",
                                   "10 · Quantifier l'association entre deux variables"),
    "catalog/11-predict-from-one.qmd": ("11 · Einen Wert aus einer anderen Variable vorhersagen",
                                        "11 · Prédire une valeur à partir d'une autre variable"),
    "catalog/12-predict-from-several.qmd": ("12 · Einen Wert aus mehreren Variablen vorhersagen",
                                            "12 · Prédire une valeur à partir de plusieurs variables"),
    "survival/13-kaplan-meier.qmd": ("13 · Kaplan-Meier & der Log-Rank-Test", "13 · Kaplan-Meier et le test du log-rank"),
    "survival/14-cox-regression.qmd": ("14 · Cox-Regression (proportionale Hazards)",
                                       "14 · Régression de Cox à risques proportionnels"),
    "beyond/15-post-hoc.qmd": ("15 · Post-hoc-Tests & multiple Vergleiche", "15 · Tests post hoc et comparaisons multiples"),
    "beyond/16-mixed-models.qmd": ("16 · Gemischte Modelle für wiederholte PROMs", "16 · Modèles mixtes pour PROMs répétés"),
    "beyond/17-agreement.qmd": ("17 · Übereinstimmung & Reliabilität", "17 · Concordance et fiabilité"),
    "report/18-example-report.qmd": ("18 · Beispiel-Studienbericht", "18 · Exemple de rapport d'étude"),
}
STUB = {
    "de": ("in Vorbereitung", "Noch nicht übersetzt",
           "Diese Seite wird gerade übersetzt. Bis dahin finden Sie sie [auf Englisch]({link})."),
    "fr": ("en préparation", "Pas encore traduit",
           "Cette page est en cours de traduction. En attendant, vous la trouverez [en anglais]({link})."),
}
english = sorted(str(p.relative_to("en")) for p in Path("en").rglob("*.qmd") if p.name != "index.qmd" or p.parent != Path("en"))
assert sorted(TITLES) == english, set(english) ^ set(TITLES)
for page, titles in TITLES.items():
    link = "../" * (page.count("/") + 1) + "en/" + page
    for lang, title in zip(["de", "fr"], titles):
        assert "ß" not in title
        mark, heading, body = STUB[lang]
        out = Path(lang) / page
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(f'---\ntitle: "{title} ({mark})"\n---\n\n::: {{.callout-note .coming-soon}}\n'
                       f"## {heading}\n{body.format(link=link)}\n:::\n", encoding="utf-8")
print("44 stubs written")
EOF
```

- [ ] **Step 3: The German home page, `de/index.qmd`**

```markdown
---
title: "HFR Ortho Statistik-Tutorials"
subtitle: "Von den Rohdaten bis zum Resultatteil, in R und Python"
toc: false
anchor-sections: false   # the hover anchors would wrap the card titles
---

Diese Tutorials zeigen Assistenzärztinnen und Assistenzärzten, Forschungsassistierenden und Medizinstudierenden, die ihre Masterarbeit an der HFR Orthopädie schreiben, wie man Daten aufbereitet, den passenden statistischen Test wählt, ihn durchführt und so berichtet, wie es Gutachterinnen und Gutachter von Zeitschriften wie JBJS, *The Bone & Joint Journal* und *CORR* erwarten. Sie brauchen keine Erfahrung mit Statistik oder Programmieren: Jede Idee wird von Grund auf erklärt, und jede Codezeile ist kommentiert. Jede Analyse wird in R und in Python nebeneinander gezeigt, so dass Sie die eine oder die andere Sprache lernen können.

::: {.callout-note}
## Übersetzung in Arbeit
Die Tutorials werden zurzeit ins Deutsche übersetzt. Solange eine Seite noch nicht fertig ist, verweist sie auf die englische Fassung.
:::

::: {.callout-important}
## SYNTHETISCHE DATEN
Alle Datensätze auf dieser Website sind erfunden. Keiner beschreibt echte Patientinnen und Patienten, und echte Patientendaten gehören nie in dieses Repository. Bevor Sie mit echten Daten arbeiten, lesen Sie [Mit echten HFR-Daten arbeiten](getting-started/real-data.qmd).
:::

::: {.grid .welcome}

::: {.g-col-12 .g-col-lg-4 .welcome-card}
### Erste Schritte {#getting-started}

Zum ersten Mal hier? Richten Sie R, Python und die Übungsdaten ein, damit Sie auf Ihrem eigenen Computer mitmachen können, und erfahren Sie, wie die Seiten aufgebaut sind.

- [Installieren & einrichten](getting-started/setup.qmd)
- [So benutzen Sie diese Website](getting-started/using-this-site.qmd)
- [Mit echten HFR-Daten arbeiten](getting-started/real-data.qmd)
:::

::: {.g-col-12 .g-col-lg-4 .welcome-card}
### Tutorials & Übungen {#tutorials}

Arbeiten Sie die Teile der Reihe nach durch, oder gehen Sie direkt zu dem, den Sie brauchen. Jede Seite endet mit Übungen und ihren Lösungen.

- [Teil 1 · Grundlagen](foundations/01-tidy-data.qmd): Tidy Data, Tabelle 1, Testwahl
- [Teil 2 · Testkatalog](catalog/04-describe-one-group.qmd): die gängigen Tests, eine Seite pro Ziel
- [Teil 3 · Überlebenszeitanalyse](survival/13-kaplan-meier.qmd): Kaplan-Meier, konkurrierende Risiken, Cox-Regression
- [Teil 4 · Über die Tabelle hinaus](beyond/15-post-hoc.qmd): Post-hoc-Tests, gemischte Modelle, Übereinstimmung
- [Teil 5 · Alles zusammen](report/18-example-report.qmd): eine vollständige Studie, von den Rohdaten bis zum Manuskript
:::

::: {.g-col-12 .g-col-lg-4 .welcome-card}
### Welchen Test soll ich verwenden? {#which-test}

Wählen Sie Ihr Ziel und Ihren Datentyp, und die Tabelle führt Sie zum passenden Test, mit einem durchgerechneten Beispiel in beiden Sprachen.

- [Test auswählen](choose-a-test.qmd)
- Sie kennen den Namen des Tests? [Tests A–Z](tests-a-z.qmd)
:::

:::
```

- [ ] **Step 4: The French home page, `fr/index.qmd`**

```markdown
---
title: "Tutoriels de statistique HFR Ortho"
subtitle: "Des données brutes à la partie Résultats, en R et en Python"
toc: false
anchor-sections: false   # the hover anchors would wrap the card titles
---

Ces tutoriels apprennent aux médecins assistantes et assistants, au personnel de recherche et aux étudiantes et étudiants en médecine qui font leur travail de master à l'HFR Orthopédie à préparer des données, à choisir le bon test statistique, à l'appliquer et à en rapporter les résultats comme l'attendent les relecteurs de revues telles que JBJS, *The Bone & Joint Journal* et *CORR*. Aucune expérience en statistique ou en programmation n'est nécessaire : chaque notion est expliquée depuis le début et chaque ligne de code est commentée. Chaque analyse est présentée en R et en Python, côte à côte, pour que vous puissiez apprendre l'un ou l'autre langage.

::: {.callout-note}
## Traduction en cours
Les tutoriels sont en cours de traduction en français. Tant qu'une page n'est pas prête, elle renvoie à la version anglaise.
:::

::: {.callout-important}
## DONNÉES SYNTHÉTIQUES
Tous les jeux de données de ce site sont inventés. Aucun ne décrit de vrais patients, et de vraies données de patients ne vont jamais dans ce dépôt. Avant de toucher à de vraies données, lisez [Travailler avec de vraies données HFR](getting-started/real-data.qmd).
:::

::: {.grid .welcome}

::: {.g-col-12 .g-col-lg-4 .welcome-card}
### Premiers pas {#getting-started}

Première visite ? Installez R, Python et les données d'exercice pour suivre sur votre propre ordinateur, puis découvrez comment les pages fonctionnent.

- [Installer et configurer](getting-started/setup.qmd)
- [Comment utiliser ce site](getting-started/using-this-site.qmd)
- [Travailler avec de vraies données HFR](getting-started/real-data.qmd)
:::

::: {.g-col-12 .g-col-lg-4 .welcome-card}
### Tutoriels et exercices {#tutorials}

Suivez les parties dans l'ordre, ou allez directement à celle dont vous avez besoin. Chaque page se termine par des exercices et leurs solutions.

- [Partie 1 · Fondements](foundations/01-tidy-data.qmd) : données ordonnées, tableau 1, choix du test
- [Partie 2 · Catalogue des tests](catalog/04-describe-one-group.qmd) : les tests courants, une page par objectif
- [Partie 3 · Analyse de survie](survival/13-kaplan-meier.qmd) : Kaplan-Meier, risques concurrents, régression de Cox
- [Partie 4 · Au-delà du tableau](beyond/15-post-hoc.qmd) : tests post hoc, modèles mixtes, concordance
- [Partie 5 · Synthèse](report/18-example-report.qmd) : une étude complète, des données brutes au manuscrit
:::

::: {.g-col-12 .g-col-lg-4 .welcome-card}
### Quel test utiliser ? {#which-test}

Choisissez votre objectif et votre type de données : le tableau vous mène au bon test, avec un exemple complet dans les deux langages.

- [Choisir un test](choose-a-test.qmd)
- Vous connaissez le nom du test ? [Tests de A à Z](tests-a-z.qmd)
:::

:::
```

- [ ] **Step 5: The root page, `index.qmd`**

```markdown
---
title: "HFR Ortho Stats"
sidebar: false
toc: false
---

- [English](en/index.qmd)
- [Deutsch](de/index.qmd)
- [Français](fr/index.qmd)
```

- [ ] **Step 6: Replace `_quarto.yml`**

```yaml
project:
  type: website
  output-dir: _site
  execute-dir: project
  render:
    - index.qmd
    - en/*.qmd
    - en/getting-started/*.qmd
    - en/foundations/*.qmd
    - en/catalog/*.qmd
    - en/survival/*.qmd
    - en/beyond/*.qmd
    - en/report/*.qmd
    - de/*.qmd
    - de/getting-started/*.qmd
    - de/foundations/*.qmd
    - de/catalog/*.qmd
    - de/survival/*.qmd
    - de/beyond/*.qmd
    - de/report/*.qmd
    - fr/*.qmd
    - fr/getting-started/*.qmd
    - fr/foundations/*.qmd
    - fr/catalog/*.qmd
    - fr/survival/*.qmd
    - fr/beyond/*.qmd
    - fr/report/*.qmd

# Note: `engine: knitr` does NOT work here or in _metadata.yml. Each page
# with code declares it in its own front matter.
execute:
  freeze: auto

# Quarto ignores `message` under `execute:` for knitr pages; knitr's own chunk
# default hides messages on every page.
knitr:
  opts_chunk:
    message: false

website:
  title: "HFR Ortho Stats"
  description: "Tidy data, Table 1, and every common statistical test, in R and Python, in English, German and French, for HFR Ortho residents, research assistants and medical students."
  site-url: "https://hfr-ortho.github.io/stats-formation/"
  repo-url: "https://github.com/hfr-ortho/stats-formation"
  repo-actions: [issue]
  search: true
  page-navigation: true
  favicon: images/hfr-icon.svg
  # Shared by every page, so it must work in every language. The logo lives here, not in the
  # sidebars: Quarto 1.9.37 fixes a sidebar logo's path for the folder depth only in the first sidebar.
  navbar:
    title: "HFR Ortho"
    logo: images/hfr-mark-white.svg
    logo-alt: "HFR Hôpital fribourgeois"
    right:
      - text: "EN"
        href: en/index.qmd
        aria-label: "English"
      - text: "DE"
        href: de/index.qmd
        aria-label: "Deutsch"
      - text: "FR"
        href: fr/index.qmd
        aria-label: "Français"
      - icon: github
        href: "https://github.com/hfr-ortho/stats-formation"
        aria-label: "GitHub repository"
  # One sidebar per language; Quarto shows the one that contains the page.
  sidebar:
    - id: en
      style: docked
      contents:
        - text: "Home"
          href: en/index.qmd
        - text: "Choose a test"
          href: en/choose-a-test.qmd
        - text: "Tests A–Z"
          href: en/tests-a-z.qmd
        - section: "Getting started"
          contents:
            - en/getting-started/setup.qmd
            - en/getting-started/using-this-site.qmd
            - en/getting-started/real-data.qmd
        - section: "Part 1 · Foundations"
          contents:
            - en/foundations/01-tidy-data.qmd
            - en/foundations/02-demographics.qmd
            - en/foundations/03-distributions.qmd
        - section: "Part 2 · Test catalog"
          contents:
            - en/catalog/04-describe-one-group.qmd
            - en/catalog/05-one-group-vs-hypothetical.qmd
            - en/catalog/06-two-unpaired-groups.qmd
            - en/catalog/07-two-paired-groups.qmd
            - en/catalog/08-three-plus-unmatched.qmd
            - en/catalog/09-three-plus-matched.qmd
            - en/catalog/10-association.qmd
            - en/catalog/11-predict-from-one.qmd
            - en/catalog/12-predict-from-several.qmd
        - section: "Part 3 · Survival analysis"
          contents:
            - en/survival/13-kaplan-meier.qmd
            - en/survival/14-cox-regression.qmd
        - section: "Part 4 · Beyond the table"
          contents:
            - en/beyond/15-post-hoc.qmd
            - en/beyond/16-mixed-models.qmd
            - en/beyond/17-agreement.qmd
        - section: "Part 5 · Putting it together"
          contents:
            - en/report/18-example-report.qmd
    - id: de
      style: docked
      contents:
        - text: "Startseite"
          href: de/index.qmd
        - text: "Test auswählen"
          href: de/choose-a-test.qmd
        - text: "Tests A–Z"
          href: de/tests-a-z.qmd
        - section: "Erste Schritte"
          contents:
            - de/getting-started/setup.qmd
            - de/getting-started/using-this-site.qmd
            - de/getting-started/real-data.qmd
        - section: "Teil 1 · Grundlagen"
          contents:
            - de/foundations/01-tidy-data.qmd
            - de/foundations/02-demographics.qmd
            - de/foundations/03-distributions.qmd
        - section: "Teil 2 · Testkatalog"
          contents:
            - de/catalog/04-describe-one-group.qmd
            - de/catalog/05-one-group-vs-hypothetical.qmd
            - de/catalog/06-two-unpaired-groups.qmd
            - de/catalog/07-two-paired-groups.qmd
            - de/catalog/08-three-plus-unmatched.qmd
            - de/catalog/09-three-plus-matched.qmd
            - de/catalog/10-association.qmd
            - de/catalog/11-predict-from-one.qmd
            - de/catalog/12-predict-from-several.qmd
        - section: "Teil 3 · Überlebenszeitanalyse"
          contents:
            - de/survival/13-kaplan-meier.qmd
            - de/survival/14-cox-regression.qmd
        - section: "Teil 4 · Über die Tabelle hinaus"
          contents:
            - de/beyond/15-post-hoc.qmd
            - de/beyond/16-mixed-models.qmd
            - de/beyond/17-agreement.qmd
        - section: "Teil 5 · Alles zusammen"
          contents:
            - de/report/18-example-report.qmd
    - id: fr
      style: docked
      contents:
        - text: "Accueil"
          href: fr/index.qmd
        - text: "Choisir un test"
          href: fr/choose-a-test.qmd
        - text: "Tests de A à Z"
          href: fr/tests-a-z.qmd
        - section: "Premiers pas"
          contents:
            - fr/getting-started/setup.qmd
            - fr/getting-started/using-this-site.qmd
            - fr/getting-started/real-data.qmd
        - section: "Partie 1 · Fondements"
          contents:
            - fr/foundations/01-tidy-data.qmd
            - fr/foundations/02-demographics.qmd
            - fr/foundations/03-distributions.qmd
        - section: "Partie 2 · Catalogue des tests"
          contents:
            - fr/catalog/04-describe-one-group.qmd
            - fr/catalog/05-one-group-vs-hypothetical.qmd
            - fr/catalog/06-two-unpaired-groups.qmd
            - fr/catalog/07-two-paired-groups.qmd
            - fr/catalog/08-three-plus-unmatched.qmd
            - fr/catalog/09-three-plus-matched.qmd
            - fr/catalog/10-association.qmd
            - fr/catalog/11-predict-from-one.qmd
            - fr/catalog/12-predict-from-several.qmd
        - section: "Partie 3 · Analyse de survie"
          contents:
            - fr/survival/13-kaplan-meier.qmd
            - fr/survival/14-cox-regression.qmd
        - section: "Partie 4 · Au-delà du tableau"
          contents:
            - fr/beyond/15-post-hoc.qmd
            - fr/beyond/16-mixed-models.qmd
            - fr/beyond/17-agreement.qmd
        - section: "Partie 5 · Synthèse"
          contents:
            - fr/report/18-example-report.qmd
  page-footer:
    left: "Synthetic data only · Nur synthetische Daten · Données synthétiques uniquement"
    right: "Adapted from the [TJS Statistics Tutorials](https://total-joint-specialists.github.io/example-stats-analysis/) · Text CC BY 4.0 · Code MIT"

format:
  html:
    theme:
      light: [flatly, theme/hfr-light.scss]
      dark: [darkly, theme/hfr-dark.scss]
    css: styles.css
    toc: true
    toc-depth: 3
    code-copy: true
    code-overflow: wrap
```

- [ ] **Step 7: `CLAUDE.md` rules**

Replace rule 7 with:

```markdown
7. **Stub pages** carry a marker in the title and a `.coming-soon` callout: "(coming soon)" in English, "(in Vorbereitung)" in German, "(en préparation)" in French. A German or French stub's callout links to the English page. Remove both when the page is written or translated.
```

Add after rule 20:

```markdown
21. **Three languages, one folder each.** `en/`, `de/` and `fr/` hold the same file names; never add, rename or delete a page in one language only, and add every new page to all three sidebars in `_quarto.yml`. Headings that anything links to carry fixed English IDs (`{#mann-whitney}`), identical in every language, because the language switcher keeps the `#section`. Translations change prose, headings, callouts, exercises and code comments only: code, variable names, data, outputs and Methods/Results sentences stay in English. Swiss Standard German ("ss", never "ß"); "Sie" and "vous". `tests/site/test_languages.py` and `tests/site/test_anchors.py` enforce this.
```

- [ ] **Step 8: Render and run every check**

Run: `just check && uv run pytest tests/python -q`
Expected: all pass. No English page re-executes; the stubs and home pages have no code.

- [ ] **Step 9: Commit**

```bash
git add -A de fr index.qmd _quarto.yml CLAUDE.md tests
git commit -m "German and French: home pages, sidebars and a stub for every other page; root page links all three; fixed section IDs checked in every language

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 10: The language switcher

**Files:**
- Create: `lang-switch.html`, `tests/python/test_lang_switch.py`
- Modify: `_quarto.yml` (`format: html:` adds `include-after-body`)
- Test: `tests/site/test_languages.py` (one test added)

**Interfaces:**
- Consumes: the top-bar links whose text is `EN`, `DE`, `FR` (Task 9); `a.navbar-brand`.
- Produces: global functions in `lang-switch.html`: `langIndex(path) -> number`, `switchHref(path, hash, to) -> string | null`, `homeHref(path) -> string`, `pickLang(stored, browserLangs) -> "en" | "de" | "fr"`, `readChoice() -> string | null`, `saveChoice(lang) -> undefined`; `localStorage` key `hfr-stats-lang`.

- [ ] **Step 1: Write the failing tests**

Create `tests/python/test_lang_switch.py`:

```python
"""The language switcher's logic (HFR spec §4.3), run in Node.js. What it does to a page in the browser
(rewriting the top-bar links, redirecting the root) is checked by hand in Task 10, Step 5."""

import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
NODE = shutil.which("node")
pytestmark = pytest.mark.skipif(NODE is None, reason="Node.js is not installed")


def script():
    html = (ROOT / "lang-switch.html").read_text(encoding="utf-8")
    return re.search(r'<script id="lang-switch">(.*?)</script>', html, re.DOTALL).group(1)


def run(expressions, setup=""):
    """Evaluate JavaScript expressions after loading the switcher outside a browser."""
    probe = setup + script() + f"\nconsole.log(JSON.stringify([{', '.join(expressions)}]));"
    out = subprocess.run([NODE, "-e", probe], capture_output=True, text=True, timeout=30)
    assert out.returncode == 0, out.stderr
    return json.loads(out.stdout)


def test_browser_language_with_a_region_picks_the_site_language():
    assert run(['pickLang(null, ["de-CH", "en"])', 'pickLang(null, ["fr-CH"])', 'pickLang(null, ["it-CH", "en-GB"])',
                'pickLang(null, ["it"])', 'pickLang(null, [])', 'pickLang(null, undefined)']) == \
        ["de", "fr", "en", "en", "en", "en"]


def test_a_stored_choice_wins_over_the_browser():
    assert run(['pickLang("fr", ["de-CH"])', 'pickLang("xx", ["de-CH"])']) == ["fr", "de"]


def test_switching_keeps_the_page_and_section_with_or_without_a_site_prefix():
    assert run(['switchHref("/stats-formation/de/catalog/06-two-unpaired-groups.html", "#mann-whitney", "fr")',
                'switchHref("/de/catalog/06-two-unpaired-groups.html", "#mann-whitney", "en")',
                'switchHref("/stats-formation/en/", "", "de")',
                'switchHref("/stats-formation/", "", "de")']) == \
        ["/stats-formation/fr/catalog/06-two-unpaired-groups.html#mann-whitney",
         "/en/catalog/06-two-unpaired-groups.html#mann-whitney",
         "/stats-formation/de/",
         None]


def test_home_of_the_current_language():
    assert run(['homeHref("/stats-formation/fr/catalog/x.html")', 'homeHref("/en/index.html")']) == \
        ["/stats-formation/fr/index.html", "/en/index.html"]


def test_blocked_storage_never_breaks_the_page():
    blocked = 'globalThis.window = { get localStorage() { throw new Error("blocked"); } };\n'
    assert run(['readChoice()', 'saveChoice("de") === undefined'], setup=blocked) == [None, True]
```

In `tests/site/test_languages.py`, add:

```python
def test_every_page_includes_the_switcher(site):
    pages = sorted(p for p in SITE_ROOT.rglob("*.html") if "site_libs" not in p.parts)
    assert pages
    missing = [str(p.relative_to(SITE_ROOT)) for p in pages if 'id="lang-switch"' not in p.read_text(encoding="utf-8")]
    assert missing == []
```

Run: `uv run pytest tests/python/test_lang_switch.py -q`
Expected: FAIL (`lang-switch.html` doesn't exist).

- [ ] **Step 2: Write `lang-switch.html`**

```html
<script id="lang-switch">
// The language switcher (HFR spec §4.3). Every page lives at <site>/<lang>/<path>, with the same <path>
// in every language, so switching language swaps one segment of the address.
const SITE_LANGS = ["en", "de", "fr"];

// Which segment of a path is the language folder; -1 at the site root.
function langIndex(path) {
  return path.split("/").findIndex((part) => SITE_LANGS.includes(part));
}

// The same page and section in another language; null outside the language folders.
function switchHref(path, hash, to) {
  const i = langIndex(path);
  if (i === -1) return null;
  const parts = path.split("/");
  parts[i] = to;
  return parts.join("/") + hash;
}

// The home page of the language a path is in.
function homeHref(path) {
  return path.split("/").slice(0, langIndex(path) + 1).join("/") + "/index.html";
}

// Where to send a visitor at the site root: their earlier choice, else their browser's language, else English.
// Browsers report region tags ("de-CH"), so only the part before the hyphen counts.
function pickLang(stored, browserLangs) {
  if (SITE_LANGS.includes(stored)) return stored;
  for (const tag of browserLangs || []) {
    const base = String(tag).toLowerCase().split("-")[0];
    if (SITE_LANGS.includes(base)) return base;
  }
  return "en";
}

// localStorage can be missing or blocked (private windows, strict settings); the site works without it.
function readChoice() {
  try { return window.localStorage.getItem("hfr-stats-lang"); } catch (e) { return null; }
}
function saveChoice(lang) {
  try { window.localStorage.setItem("hfr-stats-lang", lang); } catch (e) { /* not remembered */ }
}

if (typeof document !== "undefined") {
  const path = window.location.pathname;
  if (langIndex(path) === -1) {
    // The site root. Its plain links work without JavaScript; with it, go straight to a language.
    window.location.replace(pickLang(readChoice(), navigator.languages || [navigator.language]) + "/index.html");
  } else {
    const current = path.split("/")[langIndex(path)];
    document.querySelectorAll("a.navbar-brand").forEach((a) => { a.href = homeHref(path); });
    document.querySelectorAll("a.nav-link").forEach((a) => {
      const lang = a.textContent.trim().toLowerCase();
      if (!SITE_LANGS.includes(lang)) return;
      a.href = switchHref(path, window.location.hash, lang);
      if (lang === current) a.setAttribute("aria-current", "true");
      else a.removeAttribute("aria-current");
      a.addEventListener("click", () => {
        saveChoice(lang);
        a.href = switchHref(window.location.pathname, window.location.hash, lang);   // the section open now
      });
    });
  }
}
</script>
```

- [ ] **Step 3: Include it on every page**

In `_quarto.yml`, under `format: html:`, add after `css: styles.css`:

```yaml
    include-after-body: lang-switch.html
```

- [ ] **Step 4: Run the tests**

Run: `uv run pytest tests/python/test_lang_switch.py -q && just check`
Expected: all pass.

- [ ] **Step 5: Check it in a browser**

Run `quarto preview --port 4848 --no-browser` in the background, then in Chrome:

1. Open `http://localhost:4848/` → it redirects to your browser's language.
2. Open `http://localhost:4848/en/catalog/06-two-unpaired-groups.html#mann-whitney`, click **DE** → `de/catalog/06-two-unpaired-groups.html#mann-whitney` (the German stub; its "auf Englisch" link leads back).
3. On `en/catalog/06-two-unpaired-groups.html`, click a later section in "On this page", then **FR** → the French page with that section's `#id`.
4. Click **FR**, then open `http://localhost:4848/` again → it goes to French (the choice was remembered).
5. On a German page, click "HFR Ortho" → `de/index.html`.
6. In the browser console, no errors from `lang-switch`.

Stop the preview.

- [ ] **Step 6: Commit**

```bash
git add lang-switch.html _quarto.yml tests
git commit -m "Language switcher: EN · DE · FR keep the page and section, the root sends visitors to their language and remembers a choice; logic tested in Node

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 11: Final verification and Doc's review

**Files:** none changed, unless Doc asks for changes.

**Interfaces:**
- Consumes: everything above.
- Produces: Doc's go-ahead (or changes) for Task 12.

- [ ] **Step 1: Clean build from scratch**

```bash
rm -rf _site .quarto
just test
just check
git status --short
```

Expected: everything passes, and `git status` is clean (the build changed no committed file, so `_freeze/` is up to date).

- [ ] **Step 2: Branding sweep**

Run: `uv run pytest tests/python/test_branding.py -q && git grep -n -i "example-stats-analysis\|total-joint" -- . ':(exclude)docs' ':(exclude)LICENSE*'`
Expected: tests pass; the grep shows only the credit links (`README.md`, `LICENSE-CONTENT` excluded, `_quarto.yml` footer) and the `tjs` remote mention in `README.md`/`CLAUDE.md`.

- [ ] **Step 3: Ask Doc to review**

Start `just preview` and ask Doc to look at, and answer:

1. **"Working with real HFR data"** (`en/getting-started/real-data.html`): is every Swiss rule stated correctly? Does "Study data stay where your project lead keeps them for the project, for example the project's REDCap database" say where HFR study data are stored, or what should it say instead (spec §4.8)? Should HFR's data protection officer read it before the site goes public?
2. **German and French home pages and sidebar labels**: anything to change? (They're provisional; the glossary in sub-projects 3–4 may revise them.)
3. **Branding**: does the top bar look right in light and dark mode? Does HFR communications need to approve the logo before the repo goes public?
4. **Copyright and audience lines**: "HFR adaptations Copyright (c) 2026 HFR Hôpital fribourgeois" and "HFR Ortho residents, research assistants and medical students doing their master's thesis": correct?

Make the changes Doc asks for (each with its test where one applies), re-run Step 1, and commit them.

---

### Task 12: Publish (each step needs Doc's explicit go-ahead)

**Files:** none (GitHub only).

**Interfaces:**
- Consumes: Task 11's approval.
- Produces: `https://github.com/hfr-ortho/stats-formation` (public) and the site at `https://hfr-ortho.github.io/stats-formation/`.

- [ ] **Step 1: Ask, then create the public repo**

Ask Doc: "Create the **public** repo `hfr-ortho/stats-formation` now?" Only on a yes:

```bash
gh repo create hfr-ortho/stats-formation --public \
  --description "HFR Ortho statistics tutorials in R and Python, in English, German and French. Synthetic data only."
git remote add origin https://github.com/hfr-ortho/stats-formation.git
git remote -v
```

Expected: `origin` (fetch and push) and `tjs` (fetch; push `DISABLED`).

- [ ] **Step 2: Ask, then push**

Ask Doc: "Push `main` to `hfr-ortho/stats-formation` now? This makes the code and the full TJS history public there." Only on a yes:

```bash
git push -u origin main
gh run list --repo hfr-ortho/stats-formation --limit 2
gh run watch --repo hfr-ortho/stats-formation --exit-status $(gh run list --repo hfr-ortho/stats-formation --workflow "Publish site" --limit 1 --json databaseId --jq '.[0].databaseId')
```

Expected: "Site checks" and "Publish site" both succeed; a `gh-pages` branch exists.

- [ ] **Step 3: Ask, then turn on GitHub Pages**

Ask Doc: "Turn on GitHub Pages from the `gh-pages` branch now?" Only on a yes:

```bash
gh api -X POST repos/hfr-ortho/stats-formation/pages -f "source[branch]=gh-pages" -f "source[path]=/"
gh api repos/hfr-ortho/stats-formation/pages --jq '.html_url, .status'
```

Wait a minute or two, then:

Run: `curl -sI https://hfr-ortho.github.io/stats-formation/ | head -1 && curl -sI https://hfr-ortho.github.io/stats-formation/de/catalog/06-two-unpaired-groups.html | head -1`
Expected: `HTTP/2 200` for both. Then open `https://hfr-ortho.github.io/stats-formation/` in a browser and repeat Task 10 Step 5's checks 1–3 on the live site (this is where the `/stats-formation/` prefix matters).

- [ ] **Step 4: Tell Doc what to record elsewhere**

The HFR Ortho wiki says every `hfr-ortho` repo is private and maps to a project page. Tell Doc that this repo is the deliberate public exception, so the wiki agent can record it (this plan doesn't edit the wiki).
