"""The Packages page (spec docs/superpowers/specs/2026-11-16-packages-page-design.md): its two tables
list exactly the R and Python packages that the pages' visible code names, with the pages that use
each one. These tests read the .qmd sources, so they need no built site."""

import functools
import re

from sitelib import PAGES, ROOT
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
