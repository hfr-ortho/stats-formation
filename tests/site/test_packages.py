"""The Packages page (spec docs/superpowers/specs/2026-11-16-packages-page-design.md): its two tables
list exactly the R and Python packages that the pages' visible code names, with the pages that use
each one. These tests read the .qmd sources, so they need no built site."""

import functools
import re
import typing

from sitelib import LANGS, PAGES, ROOT
from test_translations import fences, is_hidden, split_options, strip_comments

# Python packages whose install name (the one PyPI and the table use) differs from the import name.
IMPORT_NAMES = {"docx": "python-docx", "scikit_posthocs": "scikit-posthocs"}

BLOCK_LANGUAGE = re.compile(r"^\{?(r|python)\b")
R_LOADED = re.compile(r"\b(?:library|require|requireNamespace)\(\s*[\"']?([A-Za-z][A-Za-z0-9.]*)")
R_NAMESPACE = re.compile(r"(?<![A-Za-z0-9._:])([A-Za-z][A-Za-z0-9.]*):::?(?=[A-Za-z_.`])")
PY_IMPORT = re.compile(r"^\s*import\s+(.+)$", re.MULTILINE)
PY_FROM = re.compile(r"^\s*from\s+([A-Za-z_][A-Za-z0-9_]*)[A-Za-z0-9_.]*\s+import\b", re.MULTILINE)


def packages_in(text: str) -> dict[str, set[str]]:
    """The packages one page's visible code names: `library(x)`, `x::fun`, `import x`, `from x import`,
    in any fenced R or Python block, executed or display-only, that isn't a hidden chunk. Comments and
    inline code in prose don't count. Python packages come back under their install names."""
    found = {"r": set(), "python": set()}
    for info, body in fences(text):
        language = BLOCK_LANGUAGE.match(info)
        options, code = split_options(body)
        if not language or is_hidden(options):
            continue
        code = strip_comments(code)
        if language.group(1) == "r":
            found["r"] |= set(R_LOADED.findall(code)) | set(R_NAMESPACE.findall(code))
        else:
            names = set(PY_FROM.findall(code))
            for imported in PY_IMPORT.findall(code):
                names |= {part.split()[0].split(".")[0] for part in imported.split(",")}
            found["python"] |= {IMPORT_NAMES.get(n, n) for n in names}
    return found


@functools.cache
def used() -> dict[str, dict[str, list[str]]]:
    """Language -> package -> the English pages whose visible code names it, in sidebar order. The three
    languages' code is identical (test_translations.py), so the English pages stand for all."""
    found = {"r": {}, "python": {}}
    for page in [p.replace(".html", ".qmd") for p in PAGES]:
        for language, names in packages_in((ROOT / "en" / page).read_text(encoding="utf-8")).items():
            for name in names:
                found[language].setdefault(name, []).append(page)
    return found


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


# ---------------------------------------------------------------- the page

SECTIONS = ["r", "python"]
PACKAGE_PAGE = {"r": "https://cran.r-project.org/package={}", "python": "https://pypi.org/project/{}/"}
# Packages that come with R or Python: no package page, and a link to the official manual instead.
BUILT_IN = {"r": {"splines"}, "python": {"itertools", "re", "sys"}}
HEADING = {"r": "## R", "python": "## Python"}
LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")


class Row(typing.NamedTuple):
    name: str
    package_page: str | None
    documentation: str | None
    used_on: list[tuple[str, str]]     # (link text, href)


def rows(lang: str, section: str) -> list[Row]:
    """The rows of one language's R or Python table: `| name | package page | documentation | used on |`."""
    lines = (ROOT / lang / "packages.qmd").read_text(encoding="utf-8").split("\n")
    start = lines.index(HEADING[section]) + 1
    end = next((i for i in range(start, len(lines)) if lines[i].startswith("## ")), len(lines))
    found = []
    for line in [l for l in lines[start:end] if l.startswith("|")][2:]:      # without header and separator
        name, package_page, documentation, used_on = [c.strip() for c in line.strip().strip("|").split("|")]

        def url(cell):
            links = LINK.findall(cell)
            return links[0][1] if links else None
        found.append(Row(name.split(" (")[0], url(package_page), url(documentation), LINK.findall(used_on)))
    return found


def page_label(lang: str, page: str) -> str:
    """What "Used on" calls a page: its number for pages 1 to 18, else its title in that language."""
    numbered = re.match(r"(\d+)-", page.split("/")[-1])
    if numbered:
        return str(int(numbered.group(1)))
    return re.search(r'^title:\s*"(.*)"\s*$', (ROOT / lang / page).read_text(encoding="utf-8"), re.MULTILINE).group(1)


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


# ---------------------------------------------------------------- the prose around the tables

# The packages `library(tidyverse)` attaches: `tidyverse:::core` of the locked tidyverse 2.0.0.
TIDYVERSE_CORE = ["dplyr", "forcats", "ggplot2", "lubridate", "purrr", "readr", "stringr", "tibble", "tidyr"]
# "Used on" links stay in the page's language, so only these two kinds of link lead to English pages.
ENGLISH_NOTE = {
    "de": "Die Package-Seiten und die Dokumentationen sind auf Englisch.",
    "fr": "Les pages des packages et leur documentation sont en anglais.",
}
# A row lists the pages that name the package. Pages that only use it through `library(tidyverse)` aren't listed.
USED_ON = {
    "en": "- **Used on** links to the pages whose code names the package.",
    "de": "- **Verwendet auf** führt zu den Seiten, deren Code das Package nennt.",
    "fr": "- **Utilisé sur** renvoie aux pages dont le code nomme le package.",
}


def page_lines(lang: str) -> list[str]:
    return (ROOT / lang / "packages.qmd").read_text(encoding="utf-8").split("\n")


def test_translations_say_which_links_are_in_english():
    for lang, note in ENGLISH_NOTE.items():
        assert any(line.endswith(note) for line in page_lines(lang)), lang


def test_used_on_is_described_as_naming_the_package():
    for lang, bullet in USED_ON.items():
        assert bullet in page_lines(lang), lang


def test_tidyverse_sentence_links_the_core_packages_and_explains_the_readr_row():
    assert set(TIDYVERSE_CORE) & set(used()["r"]) == {"readr"}       # the one core package a page names
    assert used()["r"]["readr"] == ["getting-started/setup.qmd"]
    for lang in LANGS:
        sentence = next(line for line in page_lines(lang) if line.startswith("`library(tidyverse)`"))
        links = LINK.findall(sentence)
        assert links[:9] == [(p, PACKAGE_PAGE["r"].format(p)) for p in TIDYVERSE_CORE], lang
        assert links[9:] == [(page_label(lang, "getting-started/setup.qmd"), "getting-started/setup.qmd")], lang
