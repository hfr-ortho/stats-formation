"""Translated pages teach the same code and quote the same numbers as the English ones (rule 21).

`translated_pages(lang)` yields every French or German page that is no longer a stub ("(en préparation)",
"(in Vorbereitung)"), so these tests pass on stubs and start biting as pages arrive. The rules themselves are tested on small strings
at the bottom, so we know they bite before any page exists."""

import collections
import csv
import functools
import re
import unicodedata

import pytest

from sitelib import ROOT, SITE_ROOT, docx_text
from test_sources import CHUNK, CONTENT_DIRS, EXECUTABLE_CHUNK, KNITR, front_matter

GLOSSARY = ROOT / "docs" / "glossary.csv"
FENCE = re.compile(r"^\s*(```|~~~)")
FENCE_OPEN = re.compile(r"^\s*(`{3,}|~{3,})\s*(.*?)\s*$")
EXEC_INFO = re.compile(r"^\{(r|python)\b")
HTML_ONLY = '::: {.content-visible when-format="html"}'

# The six catalog steps (glossary rows "When to use it" ... "How to report it"), in spec §6 order.
LANGS = ["fr", "de"]
STEPS = {
    "fr": {
        "When to use it": "Quand l'utiliser",
        "Look at the data first": "Regarder d'abord les données",
        "Run it": "Exécuter l'analyse",
        "Read the output": "Lire le résultat",
        "Effect size and 95% CI": "Taille d'effet et IC à 95 %",
        "How to report it": "Rédiger les résultats",
    },
    "de": {
        "When to use it": "Wann verwenden",
        "Look at the data first": "Zuerst die Daten ansehen",
        "Run it": "Analyse durchführen",
        "Read the output": "Ausgabe lesen",
        "Effect size and 95% CI": "Effektstärke und 95%-KI",
        "How to report it": "Resultate formulieren",
    },
}
# Headings and bold leads that legitimately read the same in English and the translation (besides
# glossary rows whose translation is the English term, which are read from docs/glossary.csv). German
# has no "solution": its callout is titled "Lösung".
SAME_AS_ENGLISH = {
    "fr": {"r", "python", "solution", "windows", "mac", "macos", "linux", "git", "positron",
           "kaplan-meier", "cox", "anova", "bonferroni", "holm", "benjamini-hochberg"},
    "de": {"r", "python", "windows", "mac", "macos", "linux", "git", "positron",
           "kaplan-meier", "cox", "anova", "median", "bonferroni", "holm", "benjamini-hochberg",
           "koos jr", "hoos jr"},
}


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


def step_problems(en: str, tr: str, lang="fr") -> list[str]:
    steps = STEPS[lang]
    a, b = sections(en), sections(tr)
    problems = []
    for key in a.keys() & b.keys():
        want = [norm(steps[h]) for h in headings(a[key], 3) if h in steps]
        got = [h for h in headings(b[key], 3) if h in {norm(v) for v in steps.values()}]
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


def same_as_english(lang: str) -> set[str]:
    with GLOSSARY.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    names = {r["en"].strip().lower() for r in rows if r["en"].strip().lower() == r[lang].strip().lower()}
    return names | SAME_AS_ENGLISH[lang]


def untranslated_titles(en: str, tr: str, allowed=None, lang="fr") -> list[str]:
    """Headings and bold leads that read exactly as on the English page. Page 18's manuscript
    (outside the html-only divs) stays English, so its headings are exempt."""
    allowed = same_as_english(lang) if allowed is None else allowed
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
        elif line in ("## R", "## Python", "## Solution", "## Lösung"):
            found.append(("heading", "## Solution" if line == "## Lösung" else line))
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

# The French "Tests de A à Z" table is sorted by the French names (a reader looks for Fisher under F and
# Wilcoxon under W), so its rows no longer sit in English order. That one page compares its numbers and
# inline code as sets of rows; everything outside the table is compared as on any other page.
A_TO_Z = "tests-a-z.qmd"


def table_rows(text: str) -> list[str]:
    return [l for l in text.split("\n") if l.startswith("|")][2:]       # without header and separator


def without_rows(text: str) -> str:
    return "\n".join(l for l in text.split("\n") if not l.startswith("|"))


def row_set_problems(en: str, tr: str) -> list[str]:
    def signature(rows):
        return collections.Counter((tuple(number_tokens(r)), tuple(INLINE.findall(r))) for r in rows)
    a, b = signature(table_rows(en)), signature(table_rows(tr))
    return [] if a == b else [f"rows differ in numbers or inline code: only translation {dict(b - a)}, only English {dict(a - b)}"]


def check_pages(check, lang):
    found = {}
    for en, tr in translated_pages(lang):
        en_text, tr_text = en.read_text(encoding="utf-8"), tr.read_text(encoding="utf-8")
        problems = []
        if tr.name == A_TO_Z and tr.parent.name == lang:
            if check in (code_problems, number_problems):
                problems += row_set_problems(en_text, tr_text)
            en_text, tr_text = without_rows(en_text), without_rows(tr_text)
        problems += check(en_text, tr_text)
        if problems:
            found[str(tr.relative_to(ROOT))] = problems
    assert found == {}


GENERIC = {
    "fr": {"test", "tests", "estimateur", "ajustement", "limites", "courbe", "coefficient", "coefficients"},
    "de": {"test", "tests", "schätzer", "anpassung", "kurve", "koeffizient"},
}
FUNCTION_WORDS = {
    "fr": {"de", "du", "des", "la", "le", "les", "à", "pour", "un", "une", "et"},
    "de": {"der", "die", "das", "des", "für", "von", "nach", "und", "paarweise"},
}
# Names a reader would look up under another word than the rule finds.
SORT_AS = {"Test d'adéquation du khi-deux": "khi-deux", "Vérification des risques proportionnels": "risques proportionnels"}
# German: the Welch t-test is one of the t-tests, so it sits with them, not under "nach Welch".
SORT_AS_DE = {"t-Test nach Welch": "t"}


def sort_key(row: str, generic: set, function_words: set, german: bool = False) -> str:
    """Where a reader looks a row up: the proper name if the name has one (Fisher, Wilcoxon,
    Bland-Altman), otherwise its first word that isn't Test, Estimateur, Ajustement... or a function word
    ("Régression logistique" stays under R, "Test t pour échantillons appariés" under t). Accents and
    umlauts don't count. German capitalizes every noun, so there a proper name is the word after "nach"
    ("Exakter Test nach Fisher"), and a trailing "-Test" or "-Schätzer" is dropped ("Wilcoxon-Rang-Test")."""
    name = row.split("|")[1].strip().split(" (*")[0]
    name = re.sub(r"\s*\([^)]*\)", "", name).replace("\u00a0", " ")
    key = (SORT_AS_DE if german else SORT_AS).get(name)
    if key is None:
        words = [re.sub(r"^[dDlL]['’]", "", w) for w in name.split()]
        if german:
            words = [w.rsplit("-", 1)[0] if "-" in w and w.rsplit("-", 1)[1].lower() in generic else w for w in words]
            after = [words[i + 1] for i, w in enumerate(words[:-1]) if w.lower() == "nach"]
            proper = after[:1] or [w for w in words if w.isalpha() and w.isupper() and len(w) > 2]    # "Einfaktorielle ANOVA" under ANOVA
        else:
            proper = [w for w in words[1:] if w[:1].isupper() and not w.isupper()]
        rest = [w for w in words if w.lower() not in generic | function_words and w]
        key = proper[0] if proper else rest[0]
    decomposed = unicodedata.normalize("NFD", key.casefold())
    return "".join(c for c in decomposed if not unicodedata.combining(c))


@pytest.mark.parametrize("lang", LANGS)
def test_tests_a_z_is_sorted(lang):
    rows = table_rows((ROOT / lang / A_TO_Z).read_text(encoding="utf-8"))
    keys = [sort_key(r, GENERIC[lang], FUNCTION_WORDS[lang], german=lang == "de") for r in rows]
    assert keys == sorted(keys), [(a, b) for a, b in zip(keys, keys[1:]) if a > b]


def test_german_sort_key_finds_the_distinctive_name():
    def key(name):
        return sort_key(f"| {name} | x | y |", GENERIC["de"], FUNCTION_WORDS["de"], german=True)
    assert key("Exakter Test nach Fisher (*Fisher's exact test*)") == "fisher"
    assert key("Wilcoxon-Vorzeichen-Rang-Test (*x*)") == "wilcoxon-vorzeichen-rang"
    assert key("Mann-Whitney-Test (*x*)") == "mann-whitney"
    assert key("t-Test für gepaarte Stichproben (*x*)") == "t"
    assert key("Aalen-Johansen-Schätzer (*x*)") == "aalen-johansen"
    assert key("Äquivalenz der Varianzen (*x*)") == "aquivalenz"
    assert key("Einfaktorielle ANOVA (*x*)") == "anova"
    assert key("ANOVA mit Messwiederholung (*x*)") == "anova"
    assert key("Anteil mit 95%-KI (*x*)") == "anteil"
    assert key("Paarweise Log-Rank-Tests (*x*)") == "log-rank"
    assert key("Paarweise exakte Tests nach Fisher (*x*)") == "fisher"
    assert key("t-Test nach Welch (*Welch's t test*)") == "t"
    assert key("Exakter Test nach Welch (*x*)") == "welch"     # only the listed name is sorted as another


def test_sort_key_finds_the_distinctive_name():
    def key(name):
        return sort_key(f"| {name} | x | y |", GENERIC["fr"], FUNCTION_WORDS["fr"])
    assert key("Test exact de Fisher (*Fisher's exact test*)") == "fisher"
    assert key("Test des rangs signés de Wilcoxon (*x*)") == "wilcoxon"
    assert key("Limites de concordance de Bland-Altman (*x*)") == "bland-altman"
    assert key("Estimateur d'Aalen-Johansen (*x*)") == "aalen-johansen"
    assert key("Test HSD de Tukey (*x*)") == "tukey"
    assert key("Test t pour échantillons appariés (*x*)") == "t"
    assert key("Régression logistique simple (*x*)") == "regression"
    assert key("Test t pour échantillons indépendants (Welch) (*x*)") == "t"
    assert key("Ajustement de Holm (*x*)") == "holm"


def test_row_sets_ignore_order_but_not_numbers():
    en = "| A | b | `x` 1 |\n|---|---|---|\n| c | d | 2 |\n| e | f | `y` |\n"
    assert row_set_problems(en, "| A | b | c |\n|--|--|--|\n| e | f | `y` |\n| g | h | 2 |\n") == []
    assert row_set_problems(en, "| A | b | c |\n|--|--|--|\n| e | f | `y` |\n| g | h | 3 |\n")


@pytest.mark.parametrize("lang", LANGS)
def test_translated_code_matches_english(lang):
    check_pages(code_problems, lang)


@pytest.mark.parametrize("lang", LANGS)
def test_translated_prose_quotes_the_same_numbers(lang):
    check_pages(number_problems, lang)


@pytest.mark.parametrize("lang", LANGS)
def test_methods_and_results_stay_in_english(lang):
    check_pages(reporting_problems, lang)


@pytest.mark.parametrize("lang", LANGS)
def test_page_18_manuscript_stays_in_english(lang):
    for en, tr in translated_pages(lang):
        if tr.name == "18-example-report.qmd":
            assert manuscript_problems(en.read_text(encoding="utf-8"), tr.read_text(encoding="utf-8")) == []


@pytest.mark.parametrize("lang", LANGS)
def test_translated_page_structure_matches_english(lang):
    check_pages(structure_problems, lang)


@pytest.mark.parametrize("lang", LANGS)
def test_catalog_steps_are_in_order(lang):
    for en, tr in translated_pages(lang):
        if tr.parent.name == "catalog":
            problems = step_problems(en.read_text(encoding="utf-8"), tr.read_text(encoding="utf-8"), lang)
            assert problems == [], str(tr.relative_to(ROOT))


@pytest.mark.parametrize("lang", LANGS)
def test_callouts_use_the_glossary_titles(lang):
    check_pages(functools.partial(untranslated_titles, lang=lang), lang)


def test_french_prose_uses_vous():
    found = {str(tr.relative_to(ROOT)): tutoiement(tr.read_text(encoding="utf-8"))
             for _, tr in translated_pages("fr")}
    assert {k: v for k, v in found.items() if v} == {}


@pytest.mark.parametrize("lang", LANGS)
def test_no_page_loses_its_engine(lang):
    check_pages(front_matter_problems, lang)


def test_glossary_has_a_term_for_every_row():
    with GLOSSARY.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) >= 120
    assert [r["en"] for r in rows if not all(r[c].strip() for c in ("en", "fr", "de"))] == []


# ---------------------------------------------------------------- typography and comments

PLAIN_SPACE_BEFORE = re.compile(r" [;:?!%»]")
PLAIN_SPACE_AFTER = re.compile(r"« ")
TABLE_SEPARATOR = re.compile(r"^\|[\s:|-]+\|?\s*$")
TRANSLATED_KEYS = re.compile(r"^(title|subtitle|description):\s*(.*)$")


def typography_lines(tr: str):
    """(line, cleaned text) for each line of translated prose. Code, inline code, URLs, link targets,
    `:::` fences, table separator rows, {attributes}, Methods/Results paragraphs and front-matter keys
    are left out or blanked."""
    reported = {line for p in reported_paragraphs(tr) for line in p.split("\n")}
    lines = [m.group(2) for l in front_matter(tr).split("\n") if (m := TRANSLATED_KEYS.match(l))]
    lines += [l for l in prose_lines(tr) if l not in reported]
    for line in lines:
        if line.startswith(":::") or TABLE_SEPARATOR.match(line):
            continue
        text = re.sub(r"<!--.*?-->", " ", line)
        text = re.sub(r"`[^`\n]*`", "``", text)
        text = re.sub(r"\]\([^)\s]*\)", "]", text)
        text = re.sub(r"<?https?://[^\s>)]*>?", "URL", text)
        text = re.sub(r"\{[^{}\n]*\}", "", text)
        yield line, text


def typography_problems(tr: str) -> list[str]:
    """Plain spaces where French wants a non-breaking one (before ; : ? ! % » and after «), in translated
    prose only."""
    return [f"{line.strip()[:70]!r}" for line, text in typography_lines(tr)
            if PLAIN_SPACE_BEFORE.findall(text) + PLAIN_SPACE_AFTER.findall(text)]


GERMAN_PLAIN_SPACE_BEFORE_PERCENT = re.compile(r" %")
GERMAN_QUOTES = re.compile("[„“”‚‘]")
GUILLEMET_PADDING = re.compile(r"«\s|\s»")


def german_typography_problems(tr: str) -> list[str]:
    """German prose wants a non-breaking space before % (the compound 95%-KI has none), « » quotes as
    in Swiss usage and no space inside them."""
    return [f"{line.strip()[:70]!r}" for line, text in typography_lines(tr)
            if GERMAN_PLAIN_SPACE_BEFORE_PERCENT.search(text) or GERMAN_QUOTES.search(text)
            or GUILLEMET_PADDING.search(text)]


def test_german_typography():
    found = {str(tr.relative_to(ROOT)): german_typography_problems(tr.read_text(encoding="utf-8"))
             for _, tr in translated_pages("de")}
    assert {k: v for k, v in found.items() if v} == {}


GERMAN_KI = re.compile(r"(?<![A-Za-z])KI(?![A-Za-z])")


def ki_unglossed(tr: str) -> bool:
    """True if the prose says KI (or 95%-KI) but never spells out Konfidenzintervall. KI is an odd
    abbreviation for a German beginner, so each page glosses it once (the glossary row)."""
    prose = "\n".join(text for _, text in typography_lines(tr))
    return bool(GERMAN_KI.search(prose)) and "Konfidenzintervall" not in tr


def test_german_pages_gloss_ki():
    found = [str(tr.relative_to(ROOT)) for _, tr in translated_pages("de")
             if ki_unglossed(tr.read_text(encoding="utf-8"))]
    assert found == []


def test_ki_rule_bites_on_an_unglossed_abbreviation():
    head = "---\ntitle: T\n---\n\n"
    assert ki_unglossed(head + "Das 95%-KI ist breit.\n")
    assert ki_unglossed(head + "Das KI ist breit.\n")
    assert not ki_unglossed(head + "Das Konfidenzintervall (KI) ist breit.\n")
    assert not ki_unglossed(head + "Das 95%-KI (Konfidenzintervall) ist breit.\n")
    assert not ki_unglossed(head + "Der Kiosk und `KI` im Code.\n")


def test_french_typography():
    found = {str(tr.relative_to(ROOT)): typography_problems(tr.read_text(encoding="utf-8"))
             for _, tr in translated_pages("fr")}
    assert {k: v for k, v in found.items() if v} == {}


def comment_lines(code: str) -> list[str]:
    return [c for l in code.splitlines() if not l.lstrip().startswith("#|") and (c := split_comment(l)[1])]


def has_words(comment: str) -> bool:
    """False for a comment that holds only numbers or code (`# 69`, `# mean(x)`): those read the same in French."""
    text = re.sub(r"`[^`]*`|[\w.]+\([^)]*\)|[\w.]+\$\w+|[\w.]+::\w+", " ", comment.lstrip("# "))
    return bool(re.search(r"[A-Za-zÀ-ÿ]{3,}", text))


def comment_problems(en: str, tr: str) -> list[str]:
    a, b = fences(en), fences(tr)
    problems = []
    for i, ((i1, b1), (i2, b2)) in enumerate(zip(a, b), 1):
        if i1.startswith("{mermaid") or (EXEC_INFO.match(i1) and is_hidden(split_options(b1)[0])):
            continue
        for x, y in zip(comment_lines(b1), comment_lines(b2)):
            if x == y and has_words(y):
                problems.append(f"block {i}: comment left in English: {y!r}")
    return problems


@pytest.mark.parametrize("lang", LANGS)
def test_visible_comments_are_translated(lang):
    check_pages(comment_problems, lang)


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


def test_typography_rule_wants_non_breaking_spaces_in_prose_only(tmp_path):
    ok = "---\ntitle: \"Un titre\u00a0: oui\"\nengine: knitr\n---\n\nVoici\u00a0: 95\u00a0%, \u00ab\u00a0oui\u00a0\u00bb ?\n"
    ok = ok.replace("oui\u00a0\u00bb ?", "oui\u00a0\u00bb\u00a0?")
    assert typography_problems(ok) == []
    for bad in ["Voici : 5", "Soit 95 % des cas", "dit \u00ab oui\u00a0\u00bb", "dit \u00ab\u00a0oui \u00bb", "Vraiment ?", "Non !", "a ; b"]:
        assert typography_problems(f"---\ntitle: T\n---\n\n{bad}\n") != [], bad
    assert typography_problems('---\ntitle: "Un titre : oui"\n---\n\nx\n') != []


def test_typography_rule_skips_code_urls_fences_and_reporting():
    page = "---\ntitle: T\n---\n\n```r\nx <- 1 : 2   # a : b\n```\n\nVoir `a : b` et <https://x.ch/a> et [lien](a.qmd#x).\n\n::: {.callout-note collapse=\"true\"}\n:::\n\n|------|------|\n\n> **Results:** mean 5 : p = 0.5 ?\n"
    assert typography_problems(page) == []


def test_comment_rule_fails_english_comments_but_not_numbers_or_code():
    en = "```r\nx <- 1   # once\ny <- 2   # 69\nz <- 3   # mean(x)\nw <- 4   # the mean\n```\n"
    fr_bad = "```r\nx <- 1   # once\ny <- 2   # 69\nz <- 3   # mean(x)\nw <- 4   # la moyenne\n```\n"
    fr_good = fr_bad.replace("# once", "# une seule fois")
    assert comment_problems(en, fr_good) == []
    assert len(comment_problems(en, fr_bad)) == 1 and "once" in comment_problems(en, fr_bad)[0]


def test_comment_rule_ignores_hidden_chunks():
    en = "```{r}\n#| include: false\nx <- 1   # once\n```\n"
    assert comment_problems(en, en) == []


# ---------------------------------------------------------------- banned French terms and the Word file

# Calques and wrong terms the glossary and translation guide rule out. One constant, one rule test.
FRENCH_BANNED = {
    "ajuster pour": r"ajuster pour",
    "ajusté pour": r"ajust(?:é|ée|és|ées) pour",
    "test selon lequel": r"\btests? selon lequel",
    "évidence claire": r"évidence claire",
    "botte amovible": r"botte amovible",
    "fracture de la hanche": r"fracture de la hanche",
    "fracture de hanche": r"fracture de hanche",
    "données du cabinet": r"données du cabinet",
    "à égalité": r"à égalité",
    "sans bruit": r"sans bruit",
    "risque de base": r"risque de base",
    "phrase de Results": r"phrase de Results",
    "phrase des résultats": r"(?-i:phrase des résultats)",     # lowercase only: "phrase de Résultats" is right
    "phrase de résultats": r"(?-i:phrase de résultats)",
    "s'accumulent contre": r"s['’]accumulent contre",
}


def banned_terms(tr: str, banned=None) -> list[str]:
    """Banned terms in French (or, with `banned`, German) prose: code, inline code, Methods and Results lines and quoted English
    (inside « » or in italics) are left alone."""
    banned = FRENCH_BANNED if banned is None else banned
    reported = {line for p in reported_paragraphs(tr) for line in p.split("\n")}
    found = []
    for line in prose_lines(tr):
        if line in reported:
            continue
        text = re.sub(r"<!--.*?-->", " ", line).replace("\u00a0", " ")
        text = re.sub(r"`[^`\n]*`", " ", text)
        text = re.sub(r"«[^»]*»", " ", text)
        text = re.sub(r"(?<!\*)\*(?!\*)[^*\n]+(?<!\*)\*(?!\*)", " ", text)     # italics, not **bold**
        text = re.sub(r"\]\([^)\s]*\)", "] ", text)
        found += [name for name, rx in banned.items() if re.search(rx, text, re.IGNORECASE)]
    return found


def test_banned_terms_rule_finds_the_calques_and_spares_the_good_forms():
    for bad in ["Ajustez pour l'âge, ajuster pour le sexe.", "Il est ajusté pour trois tests.",
                "le test selon lequel x", "pas d'évidence claire", "une botte amovible",
                "la fracture de la hanche", "une fracture de hanche", "les données du cabinet",
                "à égalité", "sans bruit", "le risque de base", "la phrase de Results", "s'accumulent contre", "la phrase des résultats", "la phrase de résultats",
                "*italique* puis **gras** ajuster pour"]:
        assert banned_terms(bad), bad
    for good in ["Ajusté sur l'âge, mis en évidence.", "tient compte de toutes les paires", "la phrase de Résultats",
                 "> **Results:** a fracture de hanche, ajusté pour l'âge", "« ajusté pour » est un calque",
                 "le hazard de base", "`ajuster pour`", "```\najuster pour\n```"]:
        assert banned_terms(good) == [], good
    assert set(FRENCH_BANNED) >= {"ajuster pour", "phrase de Results", "s'accumulent contre"}


def test_french_banned_terms():
    found = {str(tr.relative_to(ROOT)): banned_terms(tr.read_text(encoding="utf-8"))
             for _, tr in translated_pages("fr")}
    assert {k: v for k, v in found.items() if v} == {}


@pytest.mark.parametrize("lang", LANGS)
def test_report_docx_has_the_same_text_as_english(site, lang):
    english = SITE_ROOT / "en" / "report" / "18-example-report.docx"
    translated = SITE_ROOT / lang / "report" / "18-example-report.docx"
    assert english.exists() and translated.exists()
    assert docx_text(translated) == docx_text(english)


# ---------------------------------------------------------------- German

# Anglicisms and German-from-Germany terms the glossary and translation guide rule out. False friends
# a pattern can't catch (eventuell, aktuell, konsistent) are in the guide.
GERMAN_BANNED = {
    "Sinn machen": r"\bSinn\s+mach\w*|\bmach(?:t|en|te|ten|e)\s+(?:\w+\s+)?Sinn\b",
    "kontrollieren für": r"kontrollier\w* für",
    "Krankenhaus": r"Krankenhaus",
    "Entlassung": r"Entlassung",
    "Hüftfraktur": r"Hüftfraktur",
    "direkter anteriorer Zugang": r"direkt\w* anterior\w* Zugang",
    "realisieren": r"\brealisier\w*",
    "DAA": r"(?-i:\bDAA\b)",
}
DU = re.compile(r"\b(?:du|dein\w*|dich|dir|euch|euer)\b", re.IGNORECASE)
DU_IMPERATIVE = re.compile(
    r"(?:^|[.!?»]\s+)(?:(?:[-*]|\d+\.)\s+)?(Berechne|Schau|Öffne|Lies|Führe|Nimm|Prüfe|Gib|Starte|Speichere)\b(?![ \s]*:)",
    re.MULTILINE)


def duzen(tr: str) -> list[str]:
    """Informal address in German prose (Methods/Results paragraphs, code and links are not German prose)."""
    prose = "\n".join(prose_lines(tr))
    for p in reported_paragraphs(tr):
        prose = prose.replace(p, " ")
    prose = re.sub(r"`[^`\n]*`", " ", prose)
    prose = re.sub(r"\]\([^)\s]*\)", "] ", prose)
    return DU.findall(prose) + DU_IMPERATIVE.findall(prose)


GENDER_FORMS = re.compile(r"\w[*:]innen\b|\w[*:]in\b|\w[a-zäöü]Innen\b|\w[a-zäöü]In\b|\w_innen\b")


def gender_form_problems(tr: str) -> list[str]:
    """Star, colon, underscore or capital-I forms (Patient*innen, Patient:innen, PatientInnen) in prose.
    The site writes pairs or neutral words. Code and inline code are left alone."""
    prose = "\n".join(prose_lines(tr))
    prose = re.sub(r"`[^`\n]*`", " ", prose)
    prose = re.sub(r"\]\([^)\s]*\)", "] ", prose)
    return GENDER_FORMS.findall(prose)


def test_gender_form_rule_bites_and_spares_pairs_and_code():
    for bad in ["Patient*innen", "Patient:innen", "PatientInnen", "Ärzt*in", "Teilnehmer_innen"]:
        assert gender_form_problems(bad), bad
    for good in ["Patientinnen und Patienten", "Studierende", "`Patient*innen`", "```r\nx <- 1 * innen\n```",
                 "Wir sehen 3 : innen und Innenräume", "Die Ärztinnen, Medizin: in der Praxis"]:
        assert gender_form_problems(good) == [], good


def test_german_pages_use_no_gender_star_colon_or_capital_i():
    found = {str(p.relative_to(ROOT)): gender_form_problems(p.read_text(encoding="utf-8")) for p in german_pages()}
    assert {k: v for k, v in found.items() if v} == {}


def german_pages(root=ROOT):
    return sorted((root / "de").rglob("*.qmd"))


def test_german_decimal_comma_fails():
    assert number_problems("The mean was 0.86.\n", "Der Mittelwert betrug 0,86.\n")


def test_german_ordinals_and_months_compare_like_english():
    assert number_problems("On January 5, 2015, the 1st visit.\n", "Am 5. Januar 2015, der 1. Besuch.\n") == []


def test_loesung_counts_as_solution_in_structure():
    assert structure("## Solution\n") == structure("## Lösung\n")
    assert structure("## Solution\n") != structure("## Antwort\n")


def test_loesung_is_not_an_untranslated_solution_but_solution_is():
    en = "## Solution\n\n## Median\n\n## Run it\n"
    assert untranslated_titles(en, "## Lösung\n\n## Median\n\n## Analyse durchführen\n", lang="de") == []
    assert untranslated_titles(en, en, lang="de") == ["run it", "solution"]


def test_german_steps_compare_through_the_glossary():
    en = "## S {#s}\n### Effect size and 95% CI\n### Run it\n"
    assert step_problems(en, "## S {#s}\n### Effektstärke und 95%-KI\n### Analyse durchführen\n", "de") == []
    assert step_problems(en, "## S {#s}\n### Analyse durchführen\n### Effektstärke und 95%-KI\n", "de")


def test_du_form_is_caught_but_not_sie():
    assert duzen("Berechne deinen Mittelwert.\n")
    assert duzen("Berechnen Sie Ihren Mittelwert.\n") == []
    assert duzen("Du siehst es. Dir hilft das. Schau nach.\n- Lies die Ausgabe.\n") == [
        "Du", "Dir", "Schau", "Lies"]
    assert duzen("Schauen Sie nach. Lesen Sie.\n> **Results:** du dein\n") == []


def test_german_typography_rule():
    assert german_typography_problems("Es sind 12 % der Fälle.\n")                  # plain space
    assert german_typography_problems("Das sogenannte „Modell“.\n")                  # Germany-style quotes
    assert german_typography_problems("Das sogenannte « Modell ».\n")                # space inside « »
    assert german_typography_problems("Es sind 12\u00a0% im «Modell».\n") == []
    assert german_typography_problems("Das 95%-KI reicht von 1 bis 2.\n") == []


def test_german_banned_terms_rule_finds_the_calques_and_spares_the_good_forms():
    for bad in ["Das macht keinen Sinn.", "Es macht Sinn.", "Sinn machen", "für das Alter kontrollieren für",
                "im Krankenhaus", "nach der Entlassung", "eine Hüftfraktur", "der direkte anteriore Zugang",
                "wir realisieren das", "der DAA"]:
        assert banned_terms(bad, GERMAN_BANNED), bad
    for good in ["Das ergibt Sinn.", "im Spital", "nach dem Austritt", "proximale Femurfraktur",
                 "der anteriore Zugang", "«im Krankenhaus» ist deutsch aus Deutschland", "`DAA`",
                 "> **Results:** a Hüftfraktur", "Wir erkennen, dass das stimmt."]:
        assert banned_terms(good, GERMAN_BANNED) == [], good


def test_german_prose_uses_sie():
    # every German page, the home page included: it is exempt only from comparison with English
    found = {str(tr.relative_to(ROOT)): duzen(tr.read_text(encoding="utf-8")) for tr in german_pages()}
    assert {k: v for k, v in found.items() if v} == {}


def test_german_has_no_eszett():
    files = german_pages() + [ROOT / "_quarto.yml"]
    assert [str(f.relative_to(ROOT)) for f in files if "ß" in f.read_text(encoding="utf-8")] == []
    with GLOSSARY.open(encoding="utf-8", newline="") as f:
        assert [r["en"] for r in csv.DictReader(f) if "ß" in r["de"]] == []


def test_german_banned_terms():
    found = {str(tr.relative_to(ROOT)): banned_terms(tr.read_text(encoding="utf-8"), GERMAN_BANNED)
             for tr in german_pages()}
    assert {k: v for k, v in found.items() if v} == {}


def test_german_real_data_uses_the_swiss_law_names():
    text = (ROOT / "de" / "getting-started" / "real-data.qmd").read_text(encoding="utf-8")
    for name in ("Humanforschungsgesetz", "KlinV-Mep", "CER-VD", "BASEC"):
        assert name in text, name


def test_german_names_no_data_protection_officer():
    found = [str(p.relative_to(ROOT)) for p in german_pages()
             if re.search(r"Datenschutz-?beauftragt|Datenschutzberater|Datenschutzverantwortlich", p.read_text(encoding="utf-8"))]
    assert found == []
