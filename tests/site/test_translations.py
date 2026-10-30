"""Translated pages teach the same code and quote the same numbers as the English ones (rule 21).

`translated_pages("fr")` yields every French page that is no longer a "(en préparation)" stub, so these
tests pass on stubs and start biting as pages arrive. The rules themselves are tested on small strings
at the bottom, so we know they bite before any page exists."""

import collections
import csv
import re

from sitelib import ROOT
from test_sources import CHUNK, CONTENT_DIRS, EXECUTABLE_CHUNK, KNITR, front_matter

GLOSSARY = ROOT / "docs" / "glossary.csv"
FENCE = re.compile(r"^\s*(```|~~~)")

# The six catalog steps (glossary rows "When to use it" ... "How to report it"), in spec §6 order.
STEPS = {
    "When to use it": "Quand l'utiliser",
    "Look at the data first": "Regarder d'abord les données",
    "Run it": "Exécuter le test",
    "Read the output": "Lire le résultat",
    "Effect size and 95% CI": "Taille d'effet et IC à 95 %",
    "How to report it": "Comment le rapporter",
}
ENGLISH_CALLOUT_TITLES = ["## ⚠️ Watch out", "## 🔀 R vs Python", "## 🔍 Under the hood", "## 💡 In plain language"]


# ---------------------------------------------------------------- pages

def translated_pages(lang, root=ROOT):
    """(en_path, tr_path) for every page of `lang` that isn't a stub, with its English twin."""
    folders = [root / lang] + [root / lang / d for d in CONTENT_DIRS]
    for folder in folders:
        for tr in sorted(folder.glob("*.qmd")):
            if ".coming-soon" in tr.read_text(encoding="utf-8"):
                continue
            yield root / "en" / tr.relative_to(root / lang), tr


# ---------------------------------------------------------------- code

def strip_comments(code: str) -> str:
    """Code without comments. Leaves `#` inside quoted strings (and `#|` option lines), and drops
    trailing spaces and blank lines. Works for R and Python."""
    kept = []
    for line in code.splitlines():
        if line.lstrip().startswith("#|"):
            kept.append(line.rstrip())
            continue
        quote, i = None, 0
        while i < len(line):
            c = line[i]
            if quote:
                if c == "\\":
                    i += 1
                elif c == quote:
                    quote = None
            elif c in "\"'`":
                quote = c
            elif c == "#":
                line = line[:i]
                break
            i += 1
        line = line.rstrip()
        if line:
            kept.append(line)
    return "\n".join(kept)


def chunks(text: str) -> list[tuple[str, list[str], str]]:
    """Each executable chunk as (language, its `#|` option lines, its code)."""
    found = []
    for lang, body in CHUNK.findall(text):
        lines = body.split("\n")
        n = 0
        while n < len(lines) and lines[n].startswith("#|"):
            n += 1
        found.append((lang, [x.strip() for x in lines[:n]], "\n".join(lines[n:])))
    return found


def is_hidden(options):
    return "#| include: false" in options or "#| echo: false" in options


def code_problems(en: str, tr: str) -> list[str]:
    a, b = chunks(en), chunks(tr)
    if len(a) != len(b):
        return [f"{len(b)} code chunks, English has {len(a)}"]
    problems = []
    for i, ((l1, o1, c1), (l2, o2, c2)) in enumerate(zip(a, b), 1):
        if l1 != l2:
            problems.append(f"chunk {i}: language {l2}, English {l1}")
        elif o1 != o2:
            problems.append(f"chunk {i}: options differ: {o2} vs {o1}")
        elif is_hidden(o1):
            if c1 != c2:
                problems.append(f"chunk {i}: hidden chunk is not byte-identical")
        elif strip_comments(c1) != strip_comments(c2):
            problems.append(f"chunk {i}: code differs (beyond comments)")
    return problems


# ---------------------------------------------------------------- numbers

NUMBER = re.compile(r"\d+(?:[.,]\d+)*")


def prose_lines(text: str):
    """The page without front matter and fenced code (chunks and display code)."""
    text = re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.DOTALL)
    fenced = False
    for line in text.split("\n"):
        if FENCE.match(line):
            fenced = not fenced
        elif not fenced:
            yield line


def numbers(text: str) -> collections.Counter:
    """Number tokens in prose: code blocks, front matter, link targets and {#ids} removed.
    `1,200` and `0.86` are one token each."""
    prose = "\n".join(prose_lines(text))
    prose = re.sub(r"<!--.*?-->", " ", prose, flags=re.DOTALL)
    prose = re.sub(r"`[^`\n]*`", " ", prose)                  # inline code
    prose = re.sub(r"\]\([^)\s]*\)", "] ", prose)              # link targets
    prose = re.sub(r"https?://\S+", " ", prose)
    prose = re.sub(r"\{[^{}\n]*\}", " ", prose)                # {#ids}, {.callout-note ...}
    return collections.Counter(NUMBER.findall(prose))


def sections(text: str) -> dict:
    """Prose split on `## ` headings that carry a {#id}; other headings stay in the section above."""
    parts, key = {"": []}, ""
    for line in prose_lines(text):
        m = re.match(r"^## .*\{#([A-Za-z][\w:.-]*)", line)
        if m:
            key = m.group(1)
            parts.setdefault(key, [])
        parts[key].append(line)
    return {k: "\n".join(v) for k, v in parts.items()}


def number_problems(en: str, tr: str) -> list[str]:
    a, b = sections(en), sections(tr)
    problems = []
    if list(a) != list(b):
        problems.append(f"sections differ: English {list(a)}, translation {list(b)}")
    for key in a.keys() & b.keys():
        if numbers(a[key]) != numbers(b[key]):
            ca, cb = numbers(a[key]), numbers(b[key])
            problems.append(f"section '{key or 'top'}': missing {dict(ca - cb)}, extra {dict(cb - ca)}")
    return problems


# ---------------------------------------------------------------- Methods and Results

def reported_paragraphs(text: str) -> list[str]:
    """The `> **Methods:**` and `> **Results:**` blockquote paragraphs, in order."""
    found, current = [], None
    for line in text.split("\n"):
        if re.match(r"^> \*\*(Methods|Results):\*\*", line):
            current = [line]
            found.append(current)
        elif current is not None and re.match(r"^> \S", line):
            current.append(line)
        else:
            current = None
    return ["\n".join(p) for p in found]


def reporting_problems(en: str, tr: str) -> list[str]:
    a, b = reported_paragraphs(en), reported_paragraphs(tr)
    if a == b:
        return []
    return [f"Methods/Results differ from English ({len(b)} vs {len(a)} paragraphs)"] + \
        [f"  {y[:60]!r} != {x[:60]!r}" for x, y in zip(a, b) if x != y]


# ---------------------------------------------------------------- headings, callouts, register

def headings(text: str, level: int):
    mark = "#" * level + " "
    return [re.sub(r"\s*\{[^}]*\}\s*$", "", l[len(mark):]).strip()
            for l in prose_lines(text) if l.startswith(mark)]


def step_problems(en: str, tr: str) -> list[str]:
    a, b = sections(en), sections(tr)
    problems = []
    for key in a.keys() & b.keys():
        want = [STEPS[h] for h in headings(a[key], 3) if h in STEPS]
        got = [h for h in headings(b[key], 3) if h in STEPS.values()]
        if want != got:
            problems.append(f"section '{key}': steps {got}, expected {want}")
    return problems


def english_leftovers(tr: str) -> list[str]:
    bad = ENGLISH_CALLOUT_TITLES + [f"### {h}" for h in STEPS]
    return [b for b in bad if re.search("^" + re.escape(b), tr, re.MULTILINE)]


TU = re.compile(r"\b(tu|ton|ta|tes)\b", re.IGNORECASE)


def tutoiement(tr: str) -> list[str]:
    """Informal address in prose (Methods/Results paragraphs, code and links are not French prose)."""
    prose = "\n".join(prose_lines(tr))
    for p in reported_paragraphs(tr):
        prose = prose.replace(p, " ")
    prose = re.sub(r"`[^`\n]*`", " ", prose)
    prose = re.sub(r"\]\([^)\s]*\)", "] ", prose)
    return TU.findall(prose)


def front_matter_problems(en: str, tr: str) -> list[str]:
    problems = []
    if EXECUTABLE_CHUNK.search(tr) and not KNITR.search(front_matter(tr)):
        problems.append("code without `engine: knitr`")

    def rest(t):
        return [l for l in front_matter(t).split("\n") if not re.match(r"(title|subtitle|description):", l)]
    if rest(en) != rest(tr):
        problems.append("front matter differs from English beyond title, subtitle and description")
    return problems


# ---------------------------------------------------------------- page tests

def check_pages(check):
    found = {}
    for en, tr in translated_pages("fr"):
        problems = check(en.read_text(encoding="utf-8"), tr.read_text(encoding="utf-8"))
        if problems:
            found[str(tr.relative_to(ROOT))] = problems
    assert found == {}


def test_translated_code_matches_english():
    check_pages(code_problems)


def test_translated_prose_quotes_the_same_numbers():
    check_pages(number_problems)


def test_methods_and_results_stay_in_english():
    check_pages(reporting_problems)


def test_french_catalog_steps_are_in_order():
    for en, tr in translated_pages("fr"):
        if tr.parent.name == "catalog":
            problems = step_problems(en.read_text(encoding="utf-8"), tr.read_text(encoding="utf-8"))
            assert problems == [], str(tr.relative_to(ROOT))


def test_french_callouts_use_the_glossary_titles():
    found = {str(tr.relative_to(ROOT)): english_leftovers(tr.read_text(encoding="utf-8"))
             for _, tr in translated_pages("fr")}
    assert {k: v for k, v in found.items() if v} == {}


def test_french_prose_uses_vous():
    found = {str(tr.relative_to(ROOT)): tutoiement(tr.read_text(encoding="utf-8"))
             for _, tr in translated_pages("fr")}
    assert {k: v for k, v in found.items() if v} == {}


def test_no_page_loses_its_engine():
    check_pages(front_matter_problems)


def test_glossary_has_a_french_term_for_every_row():
    with GLOSSARY.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) >= 120
    assert [r["en"] for r in rows if not r["en"].strip() or not r["fr"].strip()] == []


# ---------------------------------------------------------------- rule tests

PAGE_EN = """---
title: "A page"
engine: knitr
---

Intro with 1,200 patients.

## Section one {#one}

The mean was 0.86 (see [page 3](../foundations/03-distributions.qmd#paired)).

```{r}
x <- c(1, 2)   # a comment
label <- "# not a comment"
mean(x)
```

```{r}
#| include: false
# hidden comment
check_agree(1, 2)
```

> **Results:** The mean was 0.86 (95% CI 0.80 to 0.91).

## Section two {#two}

Another 12 patients.
"""

PAGE_FR = """---
title: "Une page"
engine: knitr
---

Introduction avec 1,200 patients.

## Section un {#one}

La moyenne était de 0.86 (voir [page 3](../foundations/03-distributions.qmd#paired)).

```{r}
x <- c(1, 2)   # un commentaire
label <- "# not a comment"
mean(x)
```

```{r}
#| include: false
# hidden comment
check_agree(1, 2)
```

> **Results:** The mean was 0.86 (95% CI 0.80 to 0.91).

## Section deux {#two}

Encore 12 patients.
"""


def all_problems(en, tr):
    return (code_problems(en, tr) + number_problems(en, tr) + reporting_problems(en, tr)
            + step_problems(en, tr) + english_leftovers(tr) + tutoiement(tr) + front_matter_problems(en, tr))


def test_rule_accepts_a_faithful_translation():
    assert all_problems(PAGE_EN, PAGE_FR) == []


def test_rule_keeps_hash_inside_strings():
    code = 'a <- "x # y"   # real comment\nb <- \'it\\\'s # here\'  # more\n\n# only a comment\n'
    assert strip_comments(code) == 'a <- "x # y"\nb <- \'it\\\'s # here\''
    assert strip_comments("n = 1  # c\n#| echo: false") == "n = 1\n#| echo: false"


def test_rule_catches_changed_code():
    assert code_problems(PAGE_EN, PAGE_FR.replace("c(1, 2)", "c(1, 3)"))
    assert code_problems(PAGE_EN, PAGE_FR.replace("# hidden comment", "# commentaire caché"))
    assert code_problems(PAGE_EN, PAGE_FR.replace("#| include: false", "#| echo: false"))
    assert code_problems(PAGE_EN, PAGE_FR.replace('"# not a comment"', '"pas un commentaire"'))


def test_rule_catches_a_changed_number():
    assert number_problems(PAGE_EN, PAGE_FR.replace("Encore 12", "Encore 21"))
    assert number_problems(PAGE_EN, PAGE_FR.replace("1,200", "1 200"))
    assert number_problems(PAGE_EN, PAGE_FR.replace("0.86 (voir", "0,86 (voir"))
    assert not number_problems(PAGE_EN, PAGE_FR)


def test_numbers_treat_thousands_and_decimals_as_one_token_and_skip_code():
    text = ("---\nn: 99\n---\nWe saw 1,200 patients, 0.86 and 3 more. [link](a/05-x.qmd#sec-7) "
            "https://x.org/2026 `n = 42` {#id-9}\n\n```{r}\nx <- 55\n```\n")
    assert numbers(text) == collections.Counter(["1,200", "0.86", "3"])


def test_rule_catches_changed_reporting_and_register():
    assert reporting_problems(PAGE_EN, PAGE_FR.replace("The mean was", "La moyenne était"))
    assert english_leftovers("## ⚠️ Watch out: x\n") and english_leftovers("### Run it\n")
    assert tutoiement("Si tu veux, ton choix.") == ["tu", "ton"]
    assert front_matter_problems(PAGE_EN, PAGE_FR.replace("engine: knitr\n", ""))
    assert step_problems(
        "## S {#s}\n### Run it\n### Read the output\n", "## S {#s}\n### Lire le résultat\n### Exécuter le test\n")


def test_page_checks_bite_on_a_broken_page(tmp_path):
    for lang, text in [("en", PAGE_EN), ("fr", PAGE_FR.replace("c(1, 2)", "c(9, 9)"))]:
        (tmp_path / lang / "foundations").mkdir(parents=True)
        (tmp_path / lang / "foundations" / "a.qmd").write_text(text, encoding="utf-8")
    (tmp_path / "en" / "foundations" / "b.qmd").write_text(PAGE_EN, encoding="utf-8")
    (tmp_path / "fr" / "foundations" / "b.qmd").write_text(
        '---\ntitle: "b (en préparation)"\n---\n\n::: {.callout-note .coming-soon}\n## x\n:::\n', encoding="utf-8")
    pairs = list(translated_pages("fr", root=tmp_path))
    assert [tr.name for _, tr in pairs] == ["a.qmd"]
    en, tr = pairs[0]
    assert code_problems(en.read_text(encoding="utf-8"), tr.read_text(encoding="utf-8"))
