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
FENCE_OPEN = re.compile(r"^\s*(`{3,}|~{3,})\s*(.*?)\s*$")
EXEC_INFO = re.compile(r"^\{(r|python)\b")
HTML_ONLY = '::: {.content-visible when-format="html"}'

# The six catalog steps (glossary rows "When to use it" ... "How to report it"), in spec §6 order.
STEPS = {
    "When to use it": "Quand l'utiliser",
    "Look at the data first": "Regarder d'abord les données",
    "Run it": "Exécuter l'analyse",
    "Read the output": "Lire le résultat",
    "Effect size and 95% CI": "Taille d'effet et IC à 95 %",
    "How to report it": "Rédiger les résultats",
}
# Headings and bold leads that legitimately read the same in English and French (besides glossary
# rows whose French is the English term, which are read from docs/glossary.csv).
SAME_IN_FRENCH = {"r", "python", "solution", "windows", "mac", "macos", "linux", "git", "positron",
                  "kaplan-meier", "cox", "anova", "bonferroni", "holm", "benjamini-hochberg"}


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

def split_comment(line: str) -> tuple[str, str]:
    """(code, comment) for one line: the first `#` outside quotes starts the comment."""
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
            return line[:i], line[i:]
        i += 1
    return line, ""


def strip_comments(code: str) -> str:
    """Code without comments. Leaves `#` inside quoted strings (and `#|` option lines), and drops
    trailing spaces and blank lines. Works for R and Python.

    Line-based: quote state resets at each line, so a `#` inside a string that runs over several lines
    (a triple-quoted Python string, an R string with a newline) is taken for a comment. The pages don't
    have those; if one does, the check fails loudly and the page needs a rule of its own."""
    kept = []
    for line in code.splitlines():
        if not line.lstrip().startswith("#|"):
            line = split_comment(line)[0]
        line = line.rstrip()
        if line:
            kept.append(line)
    return "\n".join(kept)


def split_options(body: str) -> tuple[list[str], str]:
    lines = body.split("\n")
    n = 0
    while n < len(lines) and lines[n].startswith("#|"):
        n += 1
    return [x.strip() for x in lines[:n]], "\n".join(lines[n:])


def chunks(text: str) -> list[tuple[str, list[str], str]]:
    """Each executable chunk as (language, its `#|` option lines, its code)."""
    return [(lang, *split_options(body)) for lang, body in CHUNK.findall(text)]


def fences(text: str) -> list[tuple[str, str]]:
    """Every fenced block, executable or display, as (info string, body)."""
    found, cur = [], None
    for line in text.split("\n"):
        if cur is None:
            m = FENCE_OPEN.match(line)
            if m:
                cur = (m.group(1), m.group(2), [])
        elif re.match(rf"^\s*{re.escape(cur[0][0])}{{{len(cur[0])},}}\s*$", line):
            found.append((cur[1], "\n".join(cur[2])))
            cur = None
        else:
            cur[2].append(line)
    return found


def is_hidden(options):
    return "#| include: false" in options or "#| echo: false" in options


def mask_mermaid_labels(code: str) -> str:
    """A mermaid diagram's structure (ids, arrows) must match; its node and edge labels are prose."""
    code = re.sub(r"\[[^\]\n]*\]", "[]", code)
    code = re.sub(r"\{[^}\n]*\}", "{}", code)
    code = re.sub(r"\|[^|\n]*\|", "||", code)
    return code


def comment_text(code: str) -> str:
    return "\n".join(split_comment(l)[1] for l in code.splitlines() if not l.lstrip().startswith("#|"))


def code_problems(en: str, tr: str) -> list[str]:
    a, b = fences(en), fences(tr)
    if len(a) != len(b):
        return [f"{len(b)} code blocks, English has {len(a)}"]
    problems = []
    for i, ((i1, b1), (i2, b2)) in enumerate(zip(a, b), 1):
        if i1 != i2:
            problems.append(f"block {i}: ```{i2} vs English ```{i1}")
        elif EXEC_INFO.match(i1):
            (o1, c1), (o2, c2) = split_options(b1), split_options(b2)
            if o1 != o2:
                problems.append(f"block {i}: options differ: {o2} vs {o1}")
            elif is_hidden(o1):
                if c1 != c2:
                    problems.append(f"block {i}: hidden chunk is not byte-identical")
            else:
                problems += code_block_problems(i, c1, c2)
        elif i1.startswith("{mermaid"):
            if mask_mermaid_labels(b1) != mask_mermaid_labels(b2):
                problems.append(f"block {i}: diagram structure differs")
        else:
            problems += code_block_problems(i, b1, b2)
    return problems + inline_code_problems(en, tr)


def code_block_problems(i, c1, c2):
    if strip_comments(c1) != strip_comments(c2):
        return [f"block {i}: code differs (beyond comments)"]
    n1, n2 = number_tokens(comment_text(c1)), number_tokens(comment_text(c2))
    return [] if n1 == n2 else [f"block {i}: numbers in comments {n2} vs English {n1}"]


INLINE = re.compile(r"`[^`\n]+`")


def inline_code_problems(en: str, tr: str) -> list[str]:
    a, b = sections(en), sections(tr)
    problems = []
    for key in a.keys() & b.keys():
        x, y = INLINE.findall(a[key]), INLINE.findall(b[key])
        if x != y:
            problems.append(f"section '{key or 'top'}': inline code {y} vs English {x}")
    return problems


# ---------------------------------------------------------------- numbers

# A number is one token with its sign and a leading comparison, so `p < 0.05` and `p > 0.05` differ.
# `1,200` and `0.86` are one token each; a hyphen after a word character ("COVID-19", "1-3") isn't a sign.
NUMBER = re.compile(r"(?:[<>≤≥]\s*)?(?:(?<!\w)[-−])?\d+(?:[.,]\d+)*")
MONTHS = "January|February|March|April|May|June|July|August|September|October|November|December"


def prose_lines(text: str):
    """The page without front matter and fenced code (chunks and display code)."""
    text = re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.DOTALL)
    fenced = False
    for line in text.split("\n"):
        if FENCE.match(line):
            fenced = not fenced
        elif not fenced:
            yield line


def number_tokens(text: str) -> list[str]:
    """Number tokens in order, with code, link targets, URLs and {#ids} removed. Month names don't
    count (they translate): only the day and the year do, in the order of the English sentence."""
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.DOTALL)
    text = re.sub(r"`[^`\n]*`", " ", text)                    # inline code
    text = re.sub(r"\]\([^)\s]*\)", "] ", text)               # link targets
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"\{[^{}\n]*\}", " ", text)                 # {#ids}, {.callout-note ...}
    text = re.sub(rf"\b(?:{MONTHS})\s+(\d{{1,2}}),\s+(\d{{4}})", r"\1 \2", text)    # US style: day, year
    return [re.sub(r"\s+", "", t) for t in NUMBER.findall(text)]


def numbers(text: str) -> collections.Counter:
    """Number tokens in prose: front matter and code blocks removed too."""
    return collections.Counter(number_tokens("\n".join(prose_lines(text))))


def blocks(text: str) -> list[str]:
    """Paragraphs of prose: split on blank lines; each list item, heading and table row is its own block."""
    out, cur = [], []

    def flush():
        if cur:
            out.append(" ".join(cur))
            cur.clear()

    for line in text.split("\n"):
        line = re.sub(r"^(>\s?)+", "", line).rstrip()
        if not line.strip():
            flush()
            continue
        own = line.startswith(("|", ":::")) or re.match(r"^(#{1,6} |\s*[-*+] |\s*\d+[.)] )", line)
        if own:
            flush()
        cur.append(line)
        if own and (line.startswith(("#", "|", ":::"))):
            flush()
    flush()
    return [b for b in out if re.sub(r"\{[^{}\n]*\}|[:\s]", "", b)]


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
    for key in a:
        if key not in b:
            continue
        ba, bb = blocks(a[key]), blocks(b[key])
        if len(ba) != len(bb):
            problems.append(f"section '{key or 'top'}': {len(bb)} paragraphs, English has {len(ba)}")
            continue
        for n, (x, y) in enumerate(zip(ba, bb), 1):
            tx, ty = number_tokens(x), number_tokens(y)
            if tx != ty:
                problems.append(f"section '{key or 'top'}', paragraph {n}: numbers {ty}, English {tx}")
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


# ---------------------------------------------------------------- page 18's manuscript

def split_by_format(text: str) -> tuple[list[str], list[str]]:
    """(lines inside `.content-visible when-format="html"` divs, lines outside them), front matter
    removed. The html div's own opening and closing fences count as outside lines, so they must match."""
    text = re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.DOTALL)
    inside, outside, depth, fenced = [], [], 0, False
    for line in text.split("\n"):
        if FENCE.match(line):
            fenced = not fenced
        div = not fenced and line.startswith(":::")
        if depth == 0:
            outside.append(line)
            if div and line.strip() == HTML_ONLY:
                depth = 1
        else:
            if div and re.match(r"^:{3,}\s*$", line):
                depth -= 1
                if depth == 0:
                    outside.append(line)
                    continue
            elif div:
                depth += 1
            inside.append(line)
    return inside, outside


def manuscript_problems(en: str, tr: str) -> list[str]:
    a, b = split_by_format(en)[1], split_by_format(tr)[1]
    if a == b:
        return []
    diff = [(x, y) for x, y in zip(a, b) if x != y][:2]
    return [f"manuscript differs from English ({len(b)} vs {len(a)} lines): {diff}"]


# ---------------------------------------------------------------- headings, callouts, register

def norm(text: str) -> str:
    """Heading text for comparison: non-breaking spaces become plain spaces, curly apostrophes straight."""
    return text.replace("\u00a0", " ").replace("\u202f", " ").replace("\u2019", "'").strip()


def headings(text: str, level: int):
    mark = "#" * level + " "
    return [norm(re.sub(r"\s*\{[^}]*\}\s*$", "", l[len(mark):]))
            for l in prose_lines(text) if l.startswith(mark)]


def step_problems(en: str, tr: str) -> list[str]:
    a, b = sections(en), sections(tr)
    problems = []
    for key in a.keys() & b.keys():
        want = [norm(STEPS[h]) for h in headings(a[key], 3) if h in STEPS]
        got = [h for h in headings(b[key], 3) if h in {norm(v) for v in STEPS.values()}]
        if want != got:
            problems.append(f"section '{key}': steps {got}, expected {want}")
    return problems


def titles(text: str) -> set[str]:
    """Headings (any level) and bold leads (`**The question:**`) of a page, as comparable strings."""
    found = set()
    for line in prose_lines(text):
        m = re.match(r"^#{1,6}\s+(.*?)\s*(\{[^}]*\})?\s*$", line) or re.match(r"^\*\*([^*]+)\*\*", line)
        if m:
            found.add(re.sub(r"[\s :.]+$", "", m.group(1)).strip().lower())
    return found


def same_in_french() -> set[str]:
    with GLOSSARY.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    names = {r["en"].strip().lower() for r in rows if r["en"].strip().lower() == r["fr"].strip().lower()}
    return names | SAME_IN_FRENCH


def untranslated_titles(en: str, tr: str, allowed=None) -> list[str]:
    """Headings and bold leads that read exactly as on the English page. Page 18's manuscript
    (outside the html-only divs) stays English, so its headings are exempt."""
    allowed = same_in_french() if allowed is None else allowed
    en_visible = "\n".join(split_by_format(en)[0]) if HTML_ONLY in en else en
    return sorted(t for t in titles(tr) & titles(en_visible)
                  if t not in allowed and re.search(r"[a-zà-ÿ]{2,}", t))


TU = re.compile(r"\b(?:[Tt]u|[Tt]on|[Tt]a|[Tt]es|[Tt]e|[Tt]oi)\b|\b[Tt]'")
IMPERATIVE = re.compile(
    r"(?:^|[.!?»]\s+)(?:(?:[-*]|\d+\.)\s+)?(Regarde|Calcule|Lance|Essaie|Ouvre|Lis|Note)\b(?![ \s]*:)",
    re.MULTILINE)


def tutoiement(tr: str) -> list[str]:
    """Informal address in prose (Methods/Results paragraphs, code and links are not French prose).
    Case-sensitive for imperatives, and "TA" (tibial slope... or any acronym) isn't a pronoun."""
    prose = "\n".join(prose_lines(tr))
    for p in reported_paragraphs(tr):
        prose = prose.replace(p, " ")
    prose = re.sub(r"`[^`\n]*`", " ", prose)
    prose = re.sub(r"\]\([^)\s]*\)", "] ", prose)
    return TU.findall(prose) + IMPERATIVE.findall(prose)


def front_matter_problems(en: str, tr: str) -> list[str]:
    problems = []
    if EXECUTABLE_CHUNK.search(tr) and not KNITR.search(front_matter(tr)):
        problems.append("code without `engine: knitr`")

    def rest(t):
        return [l for l in front_matter(t).split("\n") if not re.match(r"(title|subtitle|description):", l)]
    if rest(en) != rest(tr):
        problems.append("front matter differs from English beyond title, subtitle and description")
    return problems


# ---------------------------------------------------------------- structure

def structure(text: str) -> list[tuple[str, str]]:
    """Fenced-div lines (verbatim), section headings by {#id}, the `## R` / `## Python` / `## Solution` headings, and each code
    block's info string, in page order: where the tabsets, solutions and chunks sit."""
    found, fenced = [], False
    for line in text.split("\n"):
        m = FENCE_OPEN.match(line)
        if fenced:
            if FENCE.match(line):
                fenced = False
        elif m:
            found.append(("fence", m.group(2)))
            fenced = True
        elif line.startswith(":::"):
            found.append(("div", line.strip()))
        elif re.match(r"^## .*\{#([A-Za-z][\w:.-]*)", line):
            found.append(("section", re.match(r"^## .*\{#([A-Za-z][\w:.-]*)", line).group(1)))
        elif line in ("## R", "## Python", "## Solution"):
            found.append(("heading", line))
    return found


def structure_problems(en: str, tr: str) -> list[str]:
    a, b = structure(en), structure(tr)
    if a == b:
        return []
    first = next((i for i, (x, y) in enumerate(zip(a, b)) if x != y), min(len(a), len(b)))
    return [f"page structure differs from English at item {first + 1} "
            f"({b[first] if first < len(b) else 'end'} vs {a[first] if first < len(a) else 'end'}); "
            f"{len(b)} items, English has {len(a)}"]


# ---------------------------------------------------------------- page tests

BANNER = re.compile(r"::: \{\.callout-note\}\n## Traduction en cours\n.*?\n:::\n\n?", re.DOTALL)


def without_banner(text: str) -> str:
    """The French home page carries a temporary "Traduction en cours" callout that English hasn't.
    It goes when the last page is translated; until then it isn't compared."""
    return BANNER.sub("", text)


def check_pages(check):
    found = {}
    for en, tr in translated_pages("fr"):
        problems = check(en.read_text(encoding="utf-8"), without_banner(tr.read_text(encoding="utf-8")))
        if problems:
            found[str(tr.relative_to(ROOT))] = problems
    assert found == {}


def test_translated_code_matches_english():
    check_pages(code_problems)


def test_translated_prose_quotes_the_same_numbers():
    check_pages(number_problems)


def test_methods_and_results_stay_in_english():
    check_pages(reporting_problems)


def test_page_18_manuscript_stays_in_english():
    for en, tr in translated_pages("fr"):
        if tr.name == "18-example-report.qmd":
            assert manuscript_problems(en.read_text(encoding="utf-8"), tr.read_text(encoding="utf-8")) == []


def test_translated_page_structure_matches_english():
    check_pages(structure_problems)


def test_french_catalog_steps_are_in_order():
    for en, tr in translated_pages("fr"):
        if tr.parent.name == "catalog":
            problems = step_problems(en.read_text(encoding="utf-8"), tr.read_text(encoding="utf-8"))
            assert problems == [], str(tr.relative_to(ROOT))


def test_french_callouts_use_the_glossary_titles():
    check_pages(untranslated_titles)


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

Intro with 1,200 patients and `n_total`.

## Section one {#one}

The mean was 0.86 (see [page 3](../foundations/03-distributions.qmd#paired)). Then 5, then 7.

**The question:** How old are they?

::: {.panel-tabset group="language"}
## R

```{r}
x <- c(1, 2)   # a comment, 95% of 3
label <- "# not a comment"
mean(x)
```

## Python

```{python}
x = [1, 2]
```
:::

```{r}
#| include: false
# hidden comment
check_agree(1, 2)
```

```bash
uv sync   # takes 2 minutes
```

> **Results:** The mean was 0.86 (95% CI 0.80 to 0.91).

## Section two {#two}

Another 12 patients.
"""

PAGE_FR = """---
title: "Une page"
engine: knitr
---

Introduction avec 1,200 patients et `n_total`.

## Section un {#one}

La moyenne était de 0.86 (voir [page 3](../foundations/03-distributions.qmd#paired)). Puis 5, puis 7.

**La question :** Quel âge ont-ils ?

::: {.panel-tabset group="language"}
## R

```{r}
x <- c(1, 2)   # un commentaire, 95 % de 3
label <- "# not a comment"
mean(x)
```

## Python

```{python}
x = [1, 2]
```
:::

```{r}
#| include: false
# hidden comment
check_agree(1, 2)
```

```bash
uv sync   # prend 2 minutes
```

> **Results:** The mean was 0.86 (95% CI 0.80 to 0.91).

## Section deux {#two}

Encore 12 patients.
"""

REPORT_EN = """---
title: "Report"
---

::: {.content-visible when-format="html"}
Intro with 3 steps.

::: {.callout-note}
## 💡 How this page works
Body.
:::
:::

## Aim {#aim}

To compare 2 groups.

::: {.content-visible when-format="html"}
## Exercises {#exercises}

Do 1 thing.
:::
"""

REPORT_FR = REPORT_EN.replace("Intro with 3 steps.", "Introduction en 3 étapes.").replace(
    "How this page works", "Comment cette page fonctionne").replace("Do 1 thing.", "Faites 1 chose.").replace(
    "Exercises", "Exercices")


def all_problems(en, tr):
    return (code_problems(en, tr) + number_problems(en, tr) + reporting_problems(en, tr)
            + step_problems(en, tr) + untranslated_titles(en, tr, allowed={"r", "python", "solution"}) + tutoiement(tr)
            + front_matter_problems(en, tr) + structure_problems(en, tr))


def test_rule_accepts_a_faithful_translation():
    assert all_problems(PAGE_EN, PAGE_FR) == []
    assert all_problems(REPORT_EN, REPORT_FR) == []


def test_rule_keeps_hash_inside_strings():
    code = 'a <- "x # y"   # real comment\nb <- \'it\\\'s # here\'  # more\n\n# only a comment\n'
    assert strip_comments(code) == 'a <- "x # y"\nb <- \'it\\\'s # here\''
    assert strip_comments("n = 1  # c\n#| echo: false") == "n = 1\n#| echo: false"


def test_strip_comments_is_line_based():
    # the documented limit: a `#` inside a string that spans lines is read as a comment
    assert strip_comments('x <- "a\n# b"') == 'x <- "a'


def test_rule_catches_changed_code():
    assert code_problems(PAGE_EN, PAGE_FR.replace("c(1, 2)", "c(1, 3)"))
    assert code_problems(PAGE_EN, PAGE_FR.replace("# hidden comment", "# commentaire caché"))
    assert code_problems(PAGE_EN, PAGE_FR.replace("#| include: false", "#| echo: false"))
    assert code_problems(PAGE_EN, PAGE_FR.replace('"# not a comment"', '"pas un commentaire"'))


def test_rule_checks_display_fences_inline_code_and_comment_numbers():
    assert code_problems(PAGE_EN, PAGE_FR.replace("uv sync", "uv lock"))
    assert code_problems(PAGE_EN, PAGE_FR.replace("```bash", "```sh"))
    assert code_problems(PAGE_EN, PAGE_FR.replace("`n_total`", "`n_totale`"))
    assert code_problems(PAGE_EN, PAGE_FR.replace("prend 2 minutes", "prend 3 minutes"))
    assert code_problems(PAGE_EN, PAGE_FR.replace("# un commentaire, 95 % de 3", "# un commentaire"))
    assert not code_problems(PAGE_EN, PAGE_FR.replace("prend 2 minutes", "prend 2 minutes de plus"))


def test_mermaid_labels_translate_but_its_structure_does_not():
    en = "```{mermaid}\nflowchart TD\n  A[Goal] -->|No| B{Same?}\n```\n"
    assert not code_problems(en, "```{mermaid}\nflowchart TD\n  A[But] -->|Non| B{Pareil ?}\n```\n")
    assert code_problems(en, "```{mermaid}\nflowchart TD\n  A[But] -->|Non| C{Pareil ?}\n```\n")


def test_rule_catches_a_changed_number():
    assert number_problems(PAGE_EN, PAGE_FR.replace("Encore 12", "Encore 21"))
    assert number_problems(PAGE_EN, PAGE_FR.replace("1,200", "1 200"))
    assert number_problems(PAGE_EN, PAGE_FR.replace("0.86 (voir", "0,86 (voir"))
    assert not number_problems(PAGE_EN, PAGE_FR)


def test_numbers_keep_their_order_within_a_paragraph():
    assert number_problems(PAGE_EN, PAGE_FR.replace("Puis 5, puis 7", "Puis 7, puis 5"))
    # the same numbers in another paragraph of the section don't make up for it
    assert number_problems("## S {#s}\n\nA 1.\n\nB 2.\n", "## S {#s}\n\nA 2.\n\nB 1.\n")


def test_numbers_include_sign_and_comparison():
    assert number_tokens("IC −2 à 4; p < 0.05; n ≥ 30; COVID-19; 1-3") == ["−2", "4", "<0.05", "≥30", "19", "1", "3"]
    assert number_problems("## S {#s}\n\nSo p < 0.05.\n", "## S {#s}\n\nDonc p > 0.05.\n")
    assert number_problems("## S {#s}\n\nCI −2 to 4.\n", "## S {#s}\n\nIC 2 à 4.\n")


def test_a_different_paragraph_count_fails_with_both_counts():
    problems = number_problems("## S {#s}\n\nA 1.\n\nB 2.\n", "## S {#s}\n\nA 1. B 2.\n")
    assert problems == ["section 's': 2 paragraphs, English has 3"]
    assert number_problems("## S {#s}\n\n- a 1\n- b 2\n", "## S {#s}\n\n- a 1 b 2\n")


def test_numbers_treat_thousands_and_decimals_as_one_token_and_skip_code():
    text = ("---\nn: 99\n---\nWe saw 1,200 patients, 0.86 and 3 more. [link](a/05-x.qmd#sec-7) "
            "https://x.org/2026 `n = 42` {#id-9}\n\n```{r}\nx <- 55\n```\n")
    assert numbers(text) == collections.Counter(["1,200", "0.86", "3"])


def test_numbers_ignore_month_names_and_compare_day_and_year():
    assert number_tokens("from January 2015 to 12 November 2024") == ["2015", "12", "2024"]
    assert number_tokens("on November 12, 2024") == number_tokens("le 12 novembre 2024")
    assert number_tokens("the 1st and 25th percentile") == number_tokens("le 1er et le 25e percentile")


def test_rule_catches_changed_reporting_and_register():
    assert reporting_problems(PAGE_EN, PAGE_FR.replace("The mean was", "La moyenne était"))
    assert front_matter_problems(PAGE_EN, PAGE_FR.replace("engine: knitr\n", ""))
    assert step_problems(
        "## S {#s}\n### Run it\n### Read the output\n", "## S {#s}\n### Lire le résultat\n### Exécuter l'analyse\n")


def test_vous_rule_catches_tu_forms_and_imperatives_but_not_acronyms():
    assert tutoiement("Si tu veux, ton choix.") == ["tu", "ton"]
    assert tutoiement("Tes données, ta pente, toi, donne-le-toi, t'aider.") == ["Tes", "ta", "toi", "toi", "t'"]
    assert tutoiement("Regarde le graphique. Puis:\n- Calcule la moyenne.\nLis la sortie. Note que 5.") == [
        "Regarde", "Calcule", "Lis", "Note"]
    assert tutoiement("La TA et le TE se mesurent. Regardez la figure. Note : voir plus bas.") == []


def test_untranslated_headings_and_leads_fail_unless_allowed():
    en = ("## Run it\n\n**The question:** How?\n\n### Look at the data first\n\n## R\n\n## Python\n\n"
          "## Solution\n\n## ⚠️ Watch out: x\n\n**Windows:** run it.\n")
    assert untranslated_titles(en, en) == sorted(
        ["run it", "the question", "look at the data first", "⚠️ watch out: x"])
    fr = ("## Exécuter l'analyse\n\n**La question :** Comment ?\n\n### Regarder d'abord les données\n\n## R\n\n"
          "## Python\n\n## Solution\n\n## ⚠️ Attention : x\n\n**Windows :** lancez-le.\n")
    assert untranslated_titles(en, fr) == []


def test_the_temporary_banner_is_not_compared():
    fr = PAGE_FR.replace("## Section un {#one}", "::: {.callout-note}\n## Traduction en cours\nBientôt 3 pages.\n:::\n\n## Section un {#one}")
    assert all_problems(PAGE_EN, without_banner(fr)) == []
    assert all_problems(PAGE_EN, fr)


def test_page_18_manuscript_rule_bites_and_html_blocks_may_change():
    assert manuscript_problems(REPORT_EN, REPORT_FR) == []
    assert manuscript_problems(REPORT_EN, REPORT_FR.replace("## Aim {#aim}", "## Objectif {#aim}"))
    assert manuscript_problems(REPORT_EN, REPORT_FR.replace("To compare 2 groups.", "Comparer 2 groupes."))
    assert manuscript_problems(REPORT_EN, REPORT_FR.replace(HTML_ONLY, '::: {.content-visible when-format="docx"}'))
    # a manuscript heading identical to the English one is not an untranslated heading
    assert untranslated_titles(REPORT_EN, REPORT_FR, allowed=set()) == []


def test_structure_rule_catches_moved_tabsets_and_changed_fences():
    assert structure_problems(PAGE_EN, PAGE_FR) == []
    assert structure_problems(PAGE_EN, PAGE_FR.replace('group="language"', 'group="langue"'))
    assert structure_problems(PAGE_EN, PAGE_FR.replace("## Python", "## Python\n\n## Solution"))
    moved = PAGE_FR.replace("```{python}\nx = [1, 2]\n```\n:::\n", ":::\n```{python}\nx = [1, 2]\n```\n")
    assert structure_problems(PAGE_EN, moved)


def test_steps_compare_through_non_breaking_spaces_and_curly_apostrophes():
    en = "## S {#s}\n### Effect size and 95% CI\n### Look at the data first\n"
    assert step_problems(en, "## S {#s}\n### Taille d\u2019effet et IC \u00e0 95\u00a0%\n### Regarder d\u2019abord les donn\u00e9es\n") == []
    assert step_problems(en, "## S {#s}\n### Taille d'effet et IC à 95 %\n### Regarder d'abord les données\n") == []
    assert step_problems(en, "## S {#s}\n### Taille d'effet\n### Regarder d'abord les données\n")


def test_structure_notices_a_chunk_moved_across_a_section_heading():
    en = "## One {#one}\n\n```{r}\nx\n```\n\n## Two {#two}\n"
    fr = "## Un {#one}\n\n## Deux {#two}\n\n```{r}\nx\n```\n"
    assert structure_problems(en, fr)
    assert structure_problems(en, en.replace("{#two}", "{#deux}"))
    assert structure_problems(en, en.replace("One", "Un").replace("Two", "Deux")) == []


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
