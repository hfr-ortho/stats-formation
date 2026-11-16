# Packages page: design

Approved by Doc on 16.11.2026. A small change.

## Intent

A reader sees a package in a page's code and wants to read more about it. One page lists every R and Python package the site's code uses and links each to further information.

## Goals, non-goals, anti-goals

- Goal: a page in each language listing the packages, grouped by language (R, then Python) and sorted alphabetically within each.
- Goal: each entry links to its package page (CRAN for R, PyPI for Python) where one exists, and to the package's own documentation site where it has one.
- Goal: each entry says which pages use the package, so the reader can get back to an example.
- Goal: the list can't drift from the pages. A test fails when it does.
- Non-goal: a description of what each package does. It can be added later as one more column.
- Non-goal: versions or citations. `renv.lock` and `uv.lock` hold the versions.
- Non-goal: links to the new page from other pages' text. The sidebar entry is the way in.
- Non-goal: adding patsy to `pyproject.toml`. Two pages import it directly and it arrives with statsmodels; listing it as a dependency is a separate change.
- Anti-goal: a link nobody opened. Every URL is checked before it goes on the page (golden rule 22).
- Anti-goal: executable code on the page, which would bring freeze and re-rendering with it.

## Constraints

- Golden rule 21: the page exists as `en/packages.qmd`, `de/packages.qmd` and `fr/packages.qmd`, and all three sidebars in `_quarto.yml` list it.
- `docs/glossary.csv` keeps "package" in English in German ("Package") and French ("package").
- `just check` runs lychee on internal links only, so nothing re-checks the external URLs after this change.

## Approaches

1. **A hand-written table per language, with links and "used on" (chosen by Doc).** Package names, links and page numbers are the same in every language, so only the intro, the column headings and the "comes with R" notes are translated. A test reads the page sources and keeps the table honest.
2. **The same, plus one line on what each package does.** Friendlier for a beginner, but about 35 sentences in each of three languages, each to be checked and reviewed. Left for later.
3. **A table generated at render from the page sources.** Freeze notices only changes to the page's own file, so the list would go stale without anyone seeing. Dropped.

## Design

**Page.** `packages.qmd` in each language folder, titled "Packages" in all three, with a subtitle in the page's language ("The R and Python packages this site uses, and where to read more"). `toc: false`, no code, no `engine`. In each sidebar it sits directly under Glossary.

**Contents.** A short intro, then `## R` and `## Python`, each a table:

| Package | Package page | Documentation | Used on |
|------|------|------|------|
| effectsize | CRAN | its own site | 5, 6, 7, … |
| splines | comes with R | R manual | 11, 12 |

- "Package page" is `https://cran.r-project.org/package=<name>` or `https://pypi.org/project/<name>/`.
- "Documentation" is the package's own website, where it has one. The cell stays empty where it doesn't.
- "Used on" lists each page that uses the package, as a link: the page number for pages 1 to 18, a short name for Getting started pages.
- Packages that come with R or Python (splines; itertools, re, sys) have no package page: that cell reads "comes with R" or "comes with Python", and Documentation links to the official manual.
- tidyverse has one row. A sentence under the R table names its core packages (ggplot2, dplyr, tidyr, readr, purrr, tibble, stringr, forcats, lubridate), each linked to CRAN, because the pages load them through `library(tidyverse)` and never name them.
- Python rows show the install name; where the import name differs it stands beside it (python-docx, `import docx`; scikit-posthocs, `import scikit_posthocs`).

**What counts as used.** A package named in code a reader can see: a `library()` call, a `pkg::fun()` call, or a Python `import`, in any code block that isn't a hidden chunk (`include: false` or `echo: false`). Packages that only hidden chunks use (the agreement checks, the checksum stamps) stay off the list.

**Test.** A new test reads the `.qmd` sources and fails when:

- a page's visible code names a package the table lacks, or the table holds one no page uses;
- a row's "Used on" doesn't match the pages that use the package;
- a table isn't in alphabetical order (ignoring case);
- the three languages' tables differ in anything but translated text.

The page also joins `PAGES` in `tests/site/sitelib.py` so the existing structure and language tests cover it.

**CLAUDE.md.** The Layout section gains a line on the page, its "what counts as used" rule and its test.

## Left to the builder

- Where the test lives (`tests/site/` next to the other source checks, or `tests/python/`).
- The German and French intro, headings and notes. They are Claude's wording; native reviewers correct them on the published site.
- The exact documentation URL for each package, each opened and confirmed.
