# Packages Page Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A "Packages" page in English, German and French that lists every R and Python package named in the site's visible code, with links to read more and the pages that use each one.

**Architecture:** Three hand-written pages (`en/`, `de/`, `fr/packages.qmd`) with the same two tables and no code. A new source-level test scans the English pages' visible code and fails when the tables and the code disagree.

**Tech Stack:** Quarto markdown, pytest (`tests/site/`, run with `uv run pytest`).

**Spec:** `docs/superpowers/specs/2026-11-16-packages-page-design.md`

## Global Constraints

- The page exists under the same name in `en/`, `de/` and `fr/`, and all three sidebars in `_quarto.yml` list it directly under Glossary (golden rule 21). Never commit it in one language only.
- No executable code on the page: no `{r}` or `{python}` chunk, no `engine`.
- Title "Packages" in all three languages (`docs/glossary.csv` keeps the word English). `toc: false`.
- A package is "used" when visible code names it: `library(x)`, `require(x)`, `requireNamespace("x")`, `x::fun` in an R block, or `import x` / `from x import` in a Python block. Visible means any fenced block, executed (`{r}`) or display-only (`r`), whose options hold neither `#| include: false` nor `#| echo: false`. Inline code in prose and comments inside code don't count.
- Package page URLs are exactly `https://cran.r-project.org/package=<name>` and `https://pypi.org/project/<name>/`.
- Every external URL on the page is one of those listed in this plan (each returned HTTP 200 on 16.11.2026) or is opened and confirmed before it goes in (golden rule 22).
- German: Swiss Standard German, "Sie", no "ß". French: "vous", non-breaking space before `:`. American spelling in English.
- Don't touch any existing page source: editing a page with code re-runs it.

## Review Focus

1. A package named only in a display-only block (`renv::restore()` on the setup page) must count. Pinned in Task 1's rule test.
2. A package only hidden chunks use (`tools`, `reticulate`) must not demand a row. Pinned in Task 1's rule test.
3. A Python import name that differs from the install name (`docx`, `scikit_posthocs`) must match the row under its install name. Pinned in Task 1's rule test.
4. `import os, sys` and `import a.b as c` must yield every top-level name. Pinned in Task 1's rule test.
5. A later page that names a package that comes with R (`stats::`) will fail the list test until it gets a "comes with R" row. That is the wanted behavior; Task 2's link test covers such rows through `BUILT_IN`, which then needs the name added.

Not tested by design: the external links after today. `just check` runs lychee offline.

---

### Task 1: The scanner

**Files:**
- Create: `tests/site/test_packages.py`

**Interfaces:**
- Consumes: `fences(text) -> list[(info, body)]`, `split_options(body) -> (options, code)`, `is_hidden(options) -> bool` and `strip_comments(code) -> str` from `tests/site/test_translations.py`; `ROOT`, `PAGES`, `LANGS` from `tests/site/sitelib.py`.
- Produces:
  - `IMPORT_NAMES = {"docx": "python-docx", "scikit_posthocs": "scikit-posthocs"}`
  - `packages_in(text: str) -> dict[str, set[str]]`: keys `"r"` and `"python"`; the packages one page's visible code names, Python names as install names.
  - `used() -> dict[str, dict[str, list[str]]]`: language key → package → the English pages that use it, as paths relative to `en/` (`"catalog/06-two-unpaired-groups.qmd"`), in `PAGES` order.

- [ ] **Step 1: Write the failing rule test**

````python
RULE_PAGE = """---
title: x
---

```{r}
#| warning: false
library(survival)
d <- effectsize::cohens_d(a, b)   # not rstatix::cohens_d
# library(commented)
```

```{r}
#| include: false
tools::md5sum("f")
```

```{python}
#| echo: false
import hidden_pkg
```

```{python}
import numpy as np
import os, sys
from scipy import stats
import statsmodels.formula.api as smf
from docx import Document
import scikit_posthocs as sp
```

```r
renv::restore()
```

```bash
uv sync
```

Prose names `rms::rcs()` only.
"""


def test_scanner_reads_visible_code_only():
    assert packages_in(RULE_PAGE) == {
        "r": {"survival", "effectsize", "renv"},
        "python": {"numpy", "os", "sys", "scipy", "statsmodels", "python-docx", "scikit-posthocs"},
    }


def test_scanner_finds_the_pages_that_use_a_package():
    assert used()["r"]["irr"] == ["beyond/17-agreement.qmd"]
    assert used()["python"]["python-docx"] == ["foundations/02-demographics.qmd"]
    assert used()["r"]["readxl"] == ["getting-started/setup.qmd", "foundations/01-tidy-data.qmd",
                                     "report/18-example-report.qmd"]
    assert "tools" not in used()["r"] and "reticulate" not in used()["r"] and "rms" not in used()["r"]
````

- [ ] **Step 2: Run it to see it fail**

Run: `uv run pytest tests/site/test_packages.py -q`
Expected: FAIL, `NameError: name 'packages_in' is not defined`

- [ ] **Step 3: Implement `packages_in()` and `used()` in `tests/site/test_packages.py`**

A block's language comes from its fence info: `{r}` or `r`, `{python}` or `python`; every other block is skipped. Strip comments with `strip_comments()` before matching. `used()` reads `ROOT / "en"` only (the three languages' code is identical, which `test_translations.py` enforces) and may be cached with `functools.cache`.

- [ ] **Step 4: Run it to see it pass**

Run: `uv run pytest tests/site/test_packages.py -q`
Expected: 2 passed

- [ ] **Step 5: Compare with the expected list**

Run: `uv run python -c "import sys; sys.path.insert(0, 'tests/site'); import test_packages as t; print(sorted(t.used()['r'], key=str.lower)); print(sorted(t.used()['python'], key=str.lower))"`
Expected, exactly:

```
['DescTools', 'effectsize', 'emmeans', 'flextable', 'ggsurvfit', 'gtsummary', 'irr', 'janitor', 'lmerTest', 'PMCMRplus', 'readr', 'readxl', 'renv', 'rstatix', 'smd', 'splines', 'survival', 'tidycmprsk', 'tidyverse', 'tidyxl']
['itertools', 'lifelines', 'matplotlib', 'numpy', 'openpyxl', 'pandas', 'patsy', 'pingouin', 'python-docx', 're', 'scikit-posthocs', 'scipy', 'statsmodels', 'sys', 'tableone']
```

A difference means the scanner or this plan is wrong: find out which before going on.

- [ ] **Step 6: Commit**

```bash
git add tests/site/test_packages.py docs/superpowers/specs/2026-11-16-packages-page-design.md docs/superpowers/plans/2026-11-16-packages-page.md
git commit -m "Packages page: spec, plan and the scanner that finds the packages pages use"
```

---

### Task 2: The three pages, their sidebar entries and their tests

**Files:**
- Create: `en/packages.qmd`, `de/packages.qmd`, `fr/packages.qmd`
- Modify: `_quarto.yml` (after each of the three Glossary entries, lines 79–80, 123–124, 167–168)
- Modify: `tests/site/sitelib.py` (`PAGES`: add `"packages.html"` after `"glossary.html"`)
- Modify: `tests/site/test_packages.py`
- Modify: `CLAUDE.md` (Layout), `README.md` (if it lists the top-level pages)

**Interfaces:**
- Consumes: `packages_in()`, `used()`, `IMPORT_NAMES` from Task 1.
- Produces:
  - `BUILT_IN = {"r": {"splines"}, "python": {"itertools", "re", "sys"}}`
  - `rows(lang: str, section: str) -> list[Row]`, `section` being `"r"` or `"python"`; `Row` has `name: str`, `package_page: str | None` (the URL), `documentation: str | None` (the URL), `used_on: list[tuple[str, str]]` (link text, href).

**Row format** (the tests parse it; one row per package, four cells; the "Used on" cells here are shortened):

```
| effectsize | [CRAN](https://cran.r-project.org/package=effectsize) | [easystats.github.io/effectsize](https://easystats.github.io/effectsize/) | [5](catalog/05-one-group-vs-hypothetical.qmd), [6](catalog/06-two-unpaired-groups.qmd) |
| splines | comes with R | [R manual](https://stat.ethz.ch/R-manual/R-devel/library/splines/html/00Index.html) | [12](catalog/12-predict-from-several.qmd) |
| python-docx (`import docx`) | [PyPI](https://pypi.org/project/python-docx/) | [python-docx.readthedocs.io](https://python-docx.readthedocs.io/) | [2](foundations/02-demographics.qmd) |
```

- Cell 1: the package name as plain text. `Row.name` is the text before any ` (`.
- Cell 2: `[CRAN](…)` or `[PyPI](…)`; for a built-in, the words "comes with R" / "comes with Python" and no link.
- Cell 3: the documentation link, its text the address without `https://` and without a trailing `/` or `/index.html`; for a built-in, the text "R manual" / "Python manual". Empty where the table below says "none".
- Cell 4: one link per page from `used()`, in that order, joined by `, `. Text: the page number without a leading zero for pages 1 to 18; for a Getting started page, that page's `title:` in the same language.

**Documentation URLs** (from each package's own CRAN or PyPI record, or the README of the repository that record names; "none" where the package names no site of its own):

| R package | Documentation |
|------|------|
| DescTools | `https://andrisignorell.github.io/DescTools/` |
| effectsize | `https://easystats.github.io/effectsize/` |
| emmeans | `https://rvlenth.github.io/emmeans/` |
| flextable | `https://davidgohel.github.io/flextable/` |
| ggsurvfit | `https://www.danieldsjoberg.com/ggsurvfit/` |
| gtsummary | `https://www.danieldsjoberg.com/gtsummary/` |
| irr | none |
| janitor | `https://sfirke.github.io/janitor/` |
| lmerTest | none |
| PMCMRplus | none |
| readr | `https://readr.tidyverse.org/` |
| readxl | `https://readxl.tidyverse.org/` |
| renv | `https://rstudio.github.io/renv/` |
| rstatix | `https://rpkgs.datanovia.com/rstatix/` |
| smd | `https://bsaul.github.io/smd/` |
| splines | `https://stat.ethz.ch/R-manual/R-devel/library/splines/html/00Index.html` |
| survival | none |
| tidycmprsk | `https://mskcc-epi-bio.github.io/tidycmprsk/` |
| tidyverse | `https://tidyverse.tidyverse.org/` |
| tidyxl | `https://nacnudus.github.io/tidyxl/` |

| Python package | Documentation |
|------|------|
| itertools | `https://docs.python.org/3/library/itertools.html` |
| lifelines | `https://lifelines.readthedocs.io/` |
| matplotlib | `https://matplotlib.org/` |
| numpy | `https://numpy.org/doc/` |
| openpyxl | `https://openpyxl.readthedocs.io/` |
| pandas | `https://pandas.pydata.org/docs/` |
| patsy | `https://patsy.readthedocs.io/` |
| pingouin | `https://pingouin-stats.org/` |
| python-docx (`import docx`) | `https://python-docx.readthedocs.io/` |
| re | `https://docs.python.org/3/library/re.html` |
| scikit-posthocs (`import scikit_posthocs`) | `https://scikit-posthocs.readthedocs.io/` |
| scipy | `https://docs.scipy.org/doc/scipy/` |
| statsmodels | `https://www.statsmodels.org/stable/` |
| sys | `https://docs.python.org/3/library/sys.html` |
| tableone | `https://tableone.readthedocs.io/` |

`https://www.statsmodels.org/stable/` and `https://openpyxl.readthedocs.io/` were checked only as `…/stable/index.html` and `…/en/stable/`: confirm these two shorter forms open before using them, or use the checked forms.

**English copy** (German and French translate it; `docs/glossary.csv` and `docs/translation-guide.md` decide the terms):

```markdown
---
title: "Packages"
subtitle: "The R and Python packages this site uses, and where to read more"
toc: false
---

Every R and Python package named in this site's code is listed here, so you can read more about any of them.

- **Package page** is the package's entry in CRAN, the public archive of R packages, or in PyPI, the public archive of Python packages.
- **Documentation** is the package's own website, where it has one.
- **Used on** links to the pages whose code uses the package.

## R

| Package | Package page | Documentation | Used on |
|------|------|------|------|
…

`library(tidyverse)` loads these packages together: [dplyr](https://cran.r-project.org/package=dplyr), [forcats](…), [ggplot2](…), [lubridate](…), [purrr](…), [readr](…), [stringr](…), [tibble](…) and [tidyr](…). The pages use their functions without loading each one by name, so most of them have no row of their own.

## Python

Where a package is imported under another name than it is installed under, the import follows in parentheses.

| Package | Package page | Documentation | Used on |
|------|------|------|------|
…
```

The nine tidyverse packages are `tidyverse:::core` of the locked tidyverse 2.0.0 (read on 16.11.2026); each links to `https://cran.r-project.org/package=<name>` (all nine returned 200).

**Translated fixed strings:**

| | en | de | fr |
|---|---|---|---|
| built-in, R | comes with R | in R enthalten | fourni avec R |
| built-in, Python | comes with Python | in Python enthalten | fourni avec Python |
| manual, R | R manual | R-Handbuch | manuel de R |
| manual, Python | Python manual | Python-Handbuch | manuel de Python |
| sidebar text | Packages | Packages | Packages |

`## R` and `## Python` stay as they are in every language (`SAME_AS_ENGLISH` in `test_translations.py` already allows them).

- [ ] **Step 1: Write the failing page tests** in `tests/site/test_packages.py`

```python
SECTIONS = ["r", "python"]
PACKAGE_PAGE = {"r": "https://cran.r-project.org/package={}", "python": "https://pypi.org/project/{}/"}


def test_tables_list_exactly_the_packages_in_visible_code():
    for s in SECTIONS:
        assert {r.name for r in rows("en", s)} == set(used()[s]), s


def test_tables_are_alphabetical():
    for lang in LANGS:
        for s in SECTIONS:
            names = [r.name for r in rows(lang, s)]
            assert names == sorted(names, key=str.lower), f"{lang} {s}"


def test_used_on_links_the_pages_that_use_each_package():
    for lang in LANGS:
        for s in SECTIONS:
            for r in rows(lang, s):
                assert [href for _, href in r.used_on] == used()[s][r.name], f"{lang} {r.name}"
                assert [text for text, _ in r.used_on] == [page_label(lang, p) for p in used()[s][r.name]], f"{lang} {r.name}"


def test_package_page_links():
    for s in SECTIONS:
        for r in rows("en", s):
            if r.name in BUILT_IN[s]:
                assert r.package_page is None and r.documentation is not None, r.name
            else:
                assert r.package_page == PACKAGE_PAGE[s].format(r.name), r.name


def test_python_rows_show_a_differing_import_name():
    text = (ROOT / "en" / "packages.qmd").read_text(encoding="utf-8")
    for import_name, install_name in IMPORT_NAMES.items():
        assert f"| {install_name} (`import {import_name}`) |" in text


def test_three_languages_carry_the_same_rows():
    def signature(lang, s):
        return [(r.name, r.package_page, r.documentation, [h for _, h in r.used_on]) for r in rows(lang, s)]
    for s in SECTIONS:
        for lang in ["de", "fr"]:
            assert signature(lang, s) == signature("en", s), f"{lang} {s}"
```

`page_label(lang: str, page: str) -> str` returns `str(int(prefix))` for a file named `NN-….qmd`, else the `title:` of `ROOT / lang / page`.

- [ ] **Step 2: Run them to see them fail**

Run: `uv run pytest tests/site/test_packages.py -q`
Expected: the six new tests FAIL (`NameError` for `rows`, then `FileNotFoundError` for `en/packages.qmd` once `rows` exists); the two from Task 1 pass.

- [ ] **Step 3: Implement `BUILT_IN`, `rows()` and `page_label()`**

`rows()` reads the table lines between the section's `## R` / `## Python` heading and the next `##` heading or the end of the file, skipping the header and separator lines.

- [ ] **Step 4: Write `en/packages.qmd`**

Use the English copy, the row format and the documentation table above. Take each row's "Used on" pages from `used()`.

- [ ] **Step 5: Write `de/packages.qmd` and `fr/packages.qmd`**

Same tables, row for row. Translate the subtitle, the intro, the three bullets, the two sentences, the column headings and the fixed strings. Getting started link texts are those pages' German and French titles.

- [ ] **Step 6: Add the page to the three sidebars and to `PAGES`**

In `_quarto.yml`, after each Glossary entry:

```yaml
        - text: "Packages"
          href: en/packages.qmd
```

(`de/packages.qmd` and `fr/packages.qmd` in the other two.) In `tests/site/sitelib.py`, add `"packages.html"` to `PAGES` after `"glossary.html"`.

- [ ] **Step 7: Run the package tests**

Run: `uv run pytest tests/site/test_packages.py -q`
Expected: 8 passed

- [ ] **Step 8: Open every external link on the page**

Run: `grep -ohE "https://[^)]+" en/packages.qmd | sort -u | while read u; do curl -s -o /dev/null -L -A "Mozilla/5.0" --max-time 20 -w "%{http_code} $u\n" "$u"; done`
Expected: every line starts with `200`. Then `diff <(grep -ohE "https://[^)]+" en/packages.qmd | sort) <(grep -ohE "https://[^)]+" de/packages.qmd | sort)` and the same for `fr`: no output.

- [ ] **Step 9: Document the page**

`CLAUDE.md`, Layout section, a new bullet after the `glossary.qmd` one: the page, what counts as used (the Global Constraints wording), that a new package on a page needs a row on all three pages, that documentation URLs come from the package's own CRAN or PyPI record and are opened before they go in, and that `tests/site/test_packages.py` checks it. Also add `packages.qmd` to the page list in the "Pages:" bullet. `README.md`: add the page wherever the top-level pages are listed; if they aren't, leave it.

- [ ] **Step 10: Render and run every check**

Run: `just check`
Expected: the render runs no R or Python (only the three new pages and the sidebar change), `pytest tests/site` passes with no failure, lychee reports 0 errors. `git status` shows no change under `_freeze/`.

Run: `just test`
Expected: pass.

If `test_translations.py` reports the new German or French page (typography, "Sie"/"vous", numbers, structure), fix the page, not the test.

- [ ] **Step 11: Look at the built pages**

Open `_site/en/packages.html`, `_site/de/packages.html` and `_site/fr/packages.html`: the sidebar shows "Packages" under Glossary, both tables render with four columns, the EN/DE/FR switch moves between the three pages, and the footer and "Report an error" link read in the page's language.

- [ ] **Step 12: Commit**

```bash
git add en/packages.qmd de/packages.qmd fr/packages.qmd _quarto.yml tests/site/sitelib.py tests/site/test_packages.py CLAUDE.md README.md
git commit -m "Packages page: every R and Python package the site's code uses, with links, in three languages"
```
