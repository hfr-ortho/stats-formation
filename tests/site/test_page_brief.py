"""Every numbered page opens with "🎯 Goals and time" and ends with "📌 Key points", and every figure has a
text alternative (spec docs/superpowers/specs/2026-11-20-page-brief-design.md; audit findings L2 and U7).

The boxes arrive page by page: `DONE` lists the pages that have them, and the page tests run on those
pages only. When `DONE` equals `NUMBERED`, drop the subset. The rules themselves are tested on small
strings at the bottom, so we know they bite before a page relies on them."""

import re

import pytest
from bs4 import BeautifulSoup

from sitelib import LANGS, ROOT, SITE_ROOT, docx_text, text_of

# The 18 numbered pages, relative to a language folder.
NUMBERED = [
    "foundations/01-tidy-data.qmd",
    "foundations/02-demographics.qmd",
    "foundations/03-distributions.qmd",
    "catalog/04-describe-one-group.qmd",
    "catalog/05-one-group-vs-hypothetical.qmd",
    "catalog/06-two-unpaired-groups.qmd",
    "catalog/07-two-paired-groups.qmd",
    "catalog/08-three-plus-unmatched.qmd",
    "catalog/09-three-plus-matched.qmd",
    "catalog/10-association.qmd",
    "catalog/11-predict-from-one.qmd",
    "catalog/12-predict-from-several.qmd",
    "survival/13-kaplan-meier.qmd",
    "survival/14-cox-regression.qmd",
    "beyond/15-post-hoc.qmd",
    "beyond/16-mixed-models.qmd",
    "beyond/17-agreement.qmd",
    "report/18-example-report.qmd",
]

# The pages that have their boxes and alt texts. Tasks 4.2 to 4.6 add theirs.
DONE = [
    "catalog/06-two-unpaired-groups.qmd",
]

# The box titles, without their emoji (Doc's decision D6). The emoji are 🎯 and 📌 in every language.
TITLES = {
    "en": ("Goals and time", "Key points"),
    "de": ("Ziele und Zeitbedarf", "Das Wichtigste in Kürze"),
    "fr": ("Objectifs et durée", "L'essentiel"),
}
EMOJI = ("🎯", "📌")

# The lead-ins of the top box's parts (docs/glossary.csv). "Read first" appears only where a page needs one.
LEAD_INS = {
    "en": ("After this page you can:", "Time:", "Read first:"),
    "de": ("Nach dieser Seite können Sie:", "Zeitbedarf:", "Vorher lesen:"),
    "fr": ("Après cette page, vous saurez :", "Durée :", "À lire d'abord :"),
}

# Hands-on time with the exercises, in hours: the band from the review's table (learning-design.md, L2),
# the reviewers' estimate, not a measurement. The brief states it as "about X to Y hours" ("about X hours"
# where the band is one number).
HANDS_ON = {
    "foundations/01-tidy-data.qmd": (2, 2.5),
    "foundations/02-demographics.qmd": (1, 1.25),
    "foundations/03-distributions.qmd": (1.5,),
    "catalog/04-describe-one-group.qmd": (2, 2.5),
    "catalog/05-one-group-vs-hypothetical.qmd": (2, 2.5),
    "catalog/06-two-unpaired-groups.qmd": (2.5, 3),
    "catalog/07-two-paired-groups.qmd": (2, 2.5),
    "catalog/08-three-plus-unmatched.qmd": (2.5, 3),
    "catalog/09-three-plus-matched.qmd": (2.5, 3),
    "catalog/10-association.qmd": (1.5,),
    "catalog/11-predict-from-one.qmd": (3,),
    "catalog/12-predict-from-several.qmd": (3,),
    "survival/13-kaplan-meier.qmd": (2, 2.5),
    "survival/14-cox-regression.qmd": (2.5, 3),
    "beyond/15-post-hoc.qmd": (2.5,),
    "beyond/16-mixed-models.qmd": (2, 2.5),
    "beyond/17-agreement.qmd": (1.5, 2),
    "report/18-example-report.qmd": (2.5,),
}

BRIEF_OPEN = re.compile(r"^::: \{\.callout-note \.page-brief\}\s*$")
KEY_POINTS_OPEN = re.compile(r"^::: \{\.callout-note \.key-points\}\s*$")
FENCE = re.compile(r"^\s*(```|~~~)")
DIV_CLOSE = re.compile(r"^:{3,}\s*$")
CHUNK = re.compile(r"^```\{(r|python)\}\n(.*?)\n```", re.DOTALL | re.MULTILINE)
# Calls that draw a figure. R: the ggplot family and base graphics. Python: every figure on the site ends
# with plt.show(). A chunk that draws must carry `#| fig-alt:`.
R_DRAWS = re.compile(r"\bggplot\(|\bggsurvfit\(|\bggsurvplot\(|(?<![\w.])plot\(|\bhist\(|\bboxplot\(|\bbarplot\(|\bqqnorm\(")
PY_DRAWS = re.compile(r"\bplt\.show\(\)")


def html(page: str) -> str:
    return page.removesuffix(".qmd") + ".html"


def source(lang: str, page: str) -> str:
    return (ROOT / lang / page).read_text(encoding="utf-8")


def built(lang: str, page: str) -> BeautifulSoup:
    return BeautifulSoup((SITE_ROOT / lang / html(page)).read_text(encoding="utf-8"), "html.parser")


# ---------------------------------------------------------------- the reading-time rule

def without_boxes(lines):
    """The lines outside the two new boxes (a box counting its own words would change its own number)."""
    depth = 0
    for line in lines:
        if depth:
            if DIV_CLOSE.match(line):
                depth -= 1
            elif line.startswith(":::"):
                depth += 1
            continue
        if BRIEF_OPEN.match(line) or KEY_POINTS_OPEN.match(line):
            depth = 1
            continue
        yield line


def prose_words(text: str) -> int:
    """The words a reader reads on a page: the English .qmd without its front matter, fenced code blocks
    (executed or display-only), `:::` div lines, HTML comments, link targets `](...)`, attribute blocks
    `{...}` and the two boxes themselves. Text in callouts and collapsed solutions counts. A word is a run
    of non-space characters with at least one letter or digit, so `##`, `>`, `-`, `|` and `→` don't count."""
    text = re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.DOTALL)
    kept, fenced = [], False
    for line in without_boxes(text.split("\n")):
        if FENCE.match(line):
            fenced = not fenced
        elif not fenced and not line.lstrip().startswith(":::"):
            kept.append(line)
    prose = "\n".join(kept)
    prose = re.sub(r"<!--.*?-->", " ", prose, flags=re.DOTALL)
    prose = re.sub(r"\]\([^)\s]*\)", "] ", prose)
    prose = re.sub(r"\{[^{}\n]*\}", " ", prose)
    return sum(1 for word in prose.split() if re.search(r"[^\W_]", word))


def reading_minutes(words: int) -> int:
    """English prose words ÷ 100 words a minute, rounded to 5 minutes, never under 5 (Doc's decision D7).
    Python's round() sends an exact half to the even multiple: 2,250 words give 20 minutes, 2,750 give 30."""
    return max(5, 5 * round(words / 100 / 5))


# ---------------------------------------------------------------- the built pages

def box(soup, cls):
    found = soup.select(f"main div.callout.{cls}")
    assert len(found) == 1, f"{len(found)} .{cls} boxes"
    return found[0]


def title_of(callout) -> str:
    """The title a reader sees: without the screen-reader-only label ("Note") Quarto puts before it."""
    container = callout.select_one(".callout-title-container")
    hidden = " ".join(text_of(span) for span in container.select(".screen-reader-only"))
    return text_of(container).removeprefix(hidden).strip()


def body_of(callout):
    return callout.select_one(".callout-body-container") or callout


def position(soup):
    """Each element's place in document order."""
    return {id(el): i for i, el in enumerate(soup.find_all(True))}


def time_paragraph(callout, lang):
    lead = LEAD_INS[lang][1]
    found = [p for p in body_of(callout).select("p") if text_of(p).startswith(lead)]
    assert len(found) == 1, f"no paragraph starting with {lead!r}"
    return text_of(found[0])


def numbers_in(text: str) -> list[float]:
    return [float(n) for n in re.findall(r"\d+(?:\.\d+)?", text)]


PAGES = [(lang, page) for page in DONE for lang in LANGS]


def test_every_done_page_is_numbered_and_exists_in_every_language():
    assert set(DONE) <= set(NUMBERED) and len(NUMBERED) == 18 and set(HANDS_ON) == set(NUMBERED)
    for page in DONE:
        for lang in LANGS:
            assert (ROOT / lang / page).exists(), f"{lang}/{page}"


@pytest.mark.parametrize("lang,page", PAGES)
def test_page_opens_with_goals_and_time(site, lang, page):
    soup = built(lang, page)
    brief = box(soup, "page-brief")
    assert title_of(brief) == f"{EMOJI[0]} {TITLES[lang][0]}"
    assert soup.select("main div.callout")[0] is brief, "the brief is not the first box on the page"
    assert brief.find_parent("section") is None, "the brief sits inside a section"
    first_h2 = soup.select_one("main h2")
    assert first_h2 is not None and position(soup)[id(brief)] < position(soup)[id(first_h2)], "the brief comes after a ## heading"
    text = text_of(body_of(brief))
    assert LEAD_INS[lang][0] in text and LEAD_INS[lang][1] in text
    goals = body_of(brief).select(":scope ul > li")
    assert len(goals) == 3, f"{len(goals)} goals"
    assert brief.select("a.term") == [], "glossary term links in the brief"


@pytest.mark.parametrize("lang,page", PAGES)
def test_stated_reading_time_follows_the_rule(site, lang, page):
    """Read the minutes and the hands-on band in the brief: the same numbers in every language, the minutes
    from the English source by the rule, the band from the review's table."""
    minutes = reading_minutes(prose_words(source("en", page)))
    stated = numbers_in(time_paragraph(box(built(lang, page), "page-brief"), lang))
    assert stated == [minutes, *HANDS_ON[page]], f"stated {stated}, the rule gives {minutes} minutes and {HANDS_ON[page]} hours"


@pytest.mark.parametrize("lang,page", PAGES)
def test_page_ends_with_key_points(site, lang, page):
    soup = built(lang, page)
    points = box(soup, "key-points")
    assert title_of(points) == f"{EMOJI[1]} {TITLES[lang][1]}"
    bullets = body_of(points).select(":scope ul > li")
    assert 4 <= len(bullets) <= 6, f"{len(bullets)} key points"
    assert points.select("a.term") == [], "glossary term links in the key points"
    where = position(soup)
    exercises = soup.select_one("main section#exercises")
    assert exercises is not None and where[id(points)] < where[id(exercises)], "the key points come after Exercises"
    last_h2 = [h for h in soup.select("main h2") if where[id(h)] < where[id(exercises)]][-1]
    assert where[id(last_h2)] < where[id(points)], "a section starts after the key points"


@pytest.mark.parametrize("lang,page", PAGES)
def test_key_points_sit_above_the_prose_guard(lang, page):
    """In the source, the key points close and the hidden `# Prose guard` chunk follows directly."""
    assert key_points_problems(source(lang, page)) == []


@pytest.mark.parametrize("lang,page", PAGES)
def test_every_figure_has_alt_text(site, lang, page):
    images = built(lang, page).select("main img")
    assert images, "no figures"
    short = [(img.get("src"), img.get("alt")) for img in images if len((img.get("alt") or "").strip()) < 20]
    assert short == []


@pytest.mark.parametrize("lang,page", PAGES)
def test_every_chunk_that_draws_has_alt_text(lang, page):
    """Source level, so a missing alt text fails before the page is rendered."""
    assert drawing_chunks_without_alt(source(lang, page)) == []


@pytest.mark.parametrize("lang", LANGS)
def test_report_docx_has_no_brief(site, lang):
    """Page 18's boxes sit inside its html-only blocks, so the Word file shows neither. Until page 18 gets
    its boxes (Task 4.6) this passes trivially; it is here so the rollout can't break the Word file."""
    text = docx_text(SITE_ROOT / lang / "report" / "18-example-report.docx")
    for title in TITLES[lang] + TITLES["en"]:
        assert title not in text.replace("’", "'"), title


# ---------------------------------------------------------------- source rules

def key_points_problems(text: str) -> list[str]:
    lines = text.split("\n")
    opens = [i for i, line in enumerate(lines) if KEY_POINTS_OPEN.match(line)]
    if len(opens) != 1:
        return [f"{len(opens)} key-points boxes"]
    i = opens[0] + 1
    while i < len(lines) and not DIV_CLOSE.match(lines[i]):
        if lines[i].startswith(":::"):
            return ["a div inside the key points"]
        i += 1
    i += 1
    while i < len(lines) and not lines[i].strip():
        i += 1
    chunk = "\n".join(lines[i:i + 3])
    if not (chunk.startswith("```{r}\n#| include: false\n") and "# Prose guard" in chunk):
        return [f"the key points are followed by {lines[i] if i < len(lines) else 'the end'!r}, not the Prose guard chunk"]
    return []


def drawing_chunks_without_alt(text: str) -> list[str]:
    missing = []
    for lang, body in CHUNK.findall(text):
        options = [line.strip() for line in body.split("\n") if line.startswith("#|")]
        if "#| include: false" in options:
            continue
        draws = R_DRAWS.search(body) if lang == "r" else PY_DRAWS.search(body)
        if draws and not any(o.startswith("#| fig-alt:") for o in options):
            missing.append(f"{lang}: {body.split(chr(10))[len(options)][:60]!r}")
    return missing


# ---------------------------------------------------------------- the rules, on small samples

SAMPLE = """---
title: "A page"
engine: knitr
---

Two words [linked](../glossary.qmd#mean){.term} here <!-- not this -->.

::: {.callout-note .page-brief}
## 🎯 Goals and time
These words don't count.
:::

```{r}
x <- c(1, 2, 3)   # code doesn't count
```

```python
print("display code doesn't count either")
```

::: {.callout-warning}
## ⚠️ Watch out
Callouts count → too.
:::

::: {.callout-note .key-points}
## 📌 Key points
- Nor do these.
:::
"""


def test_prose_words_ignores_code_link_targets_attributes_and_the_boxes():
    # "Two words linked here" (4), "⚠️ Watch out" (2: the emoji has no letter), "Callouts count too." (3)
    assert prose_words(SAMPLE) == 9


def test_prose_words_counts_text_inside_callouts_and_solutions():
    assert prose_words("::: {.callout-tip collapse=\"true\"}\n## Solution\nRead this answer.\n:::\n") == 4


def test_reading_minutes_rounds_to_five():
    assert reading_minutes(5060) == 50
    assert reading_minutes(4940) == 50
    assert reading_minutes(4740) == 45
    assert reading_minutes(120) == 5
    assert reading_minutes(0) == 5


def test_key_points_rule_wants_the_prose_guard_next():
    guard = "```{r}\n#| include: false\n# Prose guard: numbers\nstopifnot(TRUE)\n```\n"
    box_ = "::: {.callout-note .key-points}\n## 📌 Key points\n- One.\n:::\n\n"
    assert key_points_problems(box_ + guard) == []
    assert key_points_problems(guard + box_)
    assert key_points_problems(box_ + "Some prose.\n\n" + guard)
    assert key_points_problems(guard)


def test_drawing_rule_finds_plots_without_alt_text():
    r_plot = "```{r}\n#| fig-height: 4\nggplot(d, aes(x)) + geom_bar()\n```\n"
    py_plot = "```{python}\nfig, ax = plt.subplots()\nplt.show()\n```\n"
    assert len(drawing_chunks_without_alt(r_plot + py_plot)) == 2
    with_alt = r_plot.replace("#| fig-height: 4", "#| fig-height: 4\n#| fig-alt: \"Bar chart of x.\"")
    assert drawing_chunks_without_alt(with_alt) == []
    assert drawing_chunks_without_alt("```{r}\nmean(x)\n```\n```{r}\n#| include: false\nplot(x)\n```\n") == []
