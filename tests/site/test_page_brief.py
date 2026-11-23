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
    "foundations/01-tidy-data.qmd",
    "foundations/02-demographics.qmd",
    "foundations/03-distributions.qmd",
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

# Each language's words for the time line's "(an estimate)", and for the legend's sentence that says the boxes
# arrive page by page. While DONE != NUMBERED the legend must say so and must not claim every page has them.
ESTIMATE = {"en": "(an estimate)", "de": "(eine Schätzung)", "fr": "(estimation)"}
ROLLOUT = {"en": "page by page", "de": "Seite für Seite", "fr": "page par page"}
EVERY_PAGE = {"en": ("each numbered page", "every numbered page"), "de": ("jeder nummerierten Seite",),
              "fr": ("chaque page numérotée",)}
# How many pages still lack the boxes: "most" while half or more do, then "some".
MOST = {"en": "most numbered pages", "de": "die meisten nummerierten Seiten", "fr": "la plupart des pages numérotées"}
SOME = {"en": "some numbered pages", "de": "einige nummerierte Seiten", "fr": "certaines pages numérotées"}

# Page 18 renders to Word too: its boxes sit inside html-only blocks (spec, "Page 18").
REPORT = "report/18-example-report.qmd"
HTML_ONLY = '::: {.content-visible when-format="html"}'

BRIEF_OPEN = re.compile(r"^::: \{\.callout-note \.page-brief\}\s*$")
# For counting words, a box is found by its class whatever else its opener says (the placement tests insist
# on the exact openers above).
ANY_BOX_OPEN = re.compile(r"^:{3,}\s*\{[^}]*\.(?:page-brief|key-points)(?![\w-])[^}]*\}\s*$")
FENCE_OPEN = re.compile(r"^\s*(`{3,}|~{3,})")
KEY_POINTS_OPEN = re.compile(r"^::: \{\.callout-note \.key-points\}\s*$")
FENCE = re.compile(r"^\s*(```|~~~)")
DIV_CLOSE = re.compile(r"^:{3,}\s*$")
EXERCISES = "## Exercises {#exercises}"
EXERCISES_HEADING = re.compile(r"^## .*\{#exercises\}\s*$")   # translated in de/ and fr/
# Every executable chunk, in page order. knitr numbers them all, mermaid included, for "unnamed-chunk-N".
CHUNK = re.compile(r"^```\{(\w+)[^}\n]*\}\n(.*?)\n```", re.DOTALL | re.MULTILINE)
CHUNK_START = re.compile(r"^```\{(\w+)[^}\n]*\}\s*$")
# Calls that draw a figure. R: the ggplot family (with ggsurvfit's ggcuminc() and emmeans' emmip()) and base
# graphics; a chunk labeled `fig-...` is a figure even when it only prints a stored plot (page 18). Python:
# every figure on the site ends with plt.show(). test_drawing_rule_finds_every_frozen_figure keeps the rule
# exact against the frozen figures of all 18 pages. A chunk that draws must carry `#| fig-alt:`.
R_DRAWS = re.compile(r"\bggplot\(|\bggsurvfit\(|\bggsurvplot\(|\bggcuminc\(|\bemmip\(|(?<![\w.])plot\(|\bhist\("
                     r"|\bboxplot\(|\bbarplot\(|\bqqnorm\(")
FIGURE_LABEL = re.compile(r"^#\| label: fig-")
PY_DRAWS = re.compile(r"\bplt\.show\(\)")
FIG_ALT = re.compile(r"^#\| fig-alt:\s*(.*)$")
ALT_ITEM = re.compile(r"^#\|\s+- ")


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
        if ANY_BOX_OPEN.match(line):
            depth = 1
            continue
        yield line


def outside_code(lines):
    """The lines outside fenced code. A fence closes only on the same character repeated at least as often
    with nothing after it, so a ```` wrapper around a chunk, or a ~~~ fence holding ```, stays code."""
    fence = None
    for line in lines:
        if fence is None:
            m = FENCE_OPEN.match(line)
            if m:
                fence = m.group(1)
            else:
                yield line
        elif re.match(rf"^\s*{re.escape(fence[0])}{{{len(fence)},}}\s*$", line):
            fence = None


def prose_words(text: str) -> int:
    """The words a reader reads on a page: the English .qmd without its front matter, fenced code blocks
    (executed or display-only), `:::` div lines, HTML comments, link targets `](...)`, attribute blocks
    `{...}` and the two boxes themselves. Text in callouts and collapsed solutions counts. A word is a run
    of non-space characters with at least one letter or digit, so `##`, `>`, `-`, `|` and `→` don't count."""
    text = re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.DOTALL)
    kept = [line for line in outside_code(without_boxes(text.split("\n"))) if not line.lstrip().startswith(":::")]
    prose = "\n".join(kept)
    prose = re.sub(r"<!--.*?-->", " ", prose, flags=re.DOTALL)
    prose = re.sub(r"\]\([^)\s]*\)", "] ", prose)
    prose = re.sub(r"\{[^{}\n]*\}", " ", prose)
    return sum(1 for word in prose.split() if re.search(r"[^\W_]", word))


def reading_minutes(words: int) -> int:
    """English prose words ÷ 90 words a minute, rounded to 5 minutes, never under 5 (Doc's decision D7;
    the rate is Doc's decision of 23.11.2026, replacing 100).
    Python's round() sends an exact half to the even multiple: 2,025 words give 20 minutes, 2,475 give 30."""
    return max(5, 5 * round(words / 90 / 5))


# ---------------------------------------------------------------- chunks and figures

def options_of(body: str) -> list[str]:
    options = []
    for line in body.split("\n"):
        if not line.startswith("#|"):
            break
        options.append(line.rstrip())
    return options


def executable_chunks(text: str) -> list[tuple[str, list[str], str]]:
    """(engine, its `#|` option lines, its body) for every executable chunk, in page order."""
    return [(engine, options_of(body), body) for engine, body in CHUNK.findall(text)]


def is_hidden(options) -> bool:
    return "#| include: false" in options


def alt_count(options) -> int:
    """How many alt texts a chunk carries: 1 for `#| fig-alt: "..."`, n for a YAML list of n items
    (`#| fig-alt:` followed by `#|   - "..."` lines, one per figure)."""
    for i, option in enumerate(options):
        m = FIG_ALT.match(option)
        if m:
            if m.group(1).strip():
                return 1
            n = 0
            for item in options[i + 1:]:
                if not ALT_ITEM.match(item):
                    break
                n += 1
            return n
    return 0


def drawing_chunks(text: str) -> set[int]:
    """The chunks (numbered from 1, as knitr does) that the source rule says draw a figure."""
    found = set()
    for i, (engine, options, body) in enumerate(executable_chunks(text), 1):
        if is_hidden(options):
            continue
        if any(FIGURE_LABEL.match(o) for o in options) or (engine == "r" and R_DRAWS.search(body)) \
                or (engine == "python" and PY_DRAWS.search(body)):
            found.add(i)
    return found


def frozen_figures(lang: str, page: str) -> dict[int, int]:
    """The truth: for each chunk that produced figure files in _freeze/<lang>/<page>/figure-html/, how many.
    Files are named after the chunk's label, or "unnamed-chunk-N" with N its place among all chunks."""
    chunks = executable_chunks(source(lang, page))
    labels = {}
    for i, (_, options, _) in enumerate(chunks, 1):
        label = next((o.split(":", 1)[1].strip() for o in options if o.startswith("#| label:")), f"unnamed-chunk-{i}")
        labels[label] = i
    folder = ROOT / "_freeze" / lang / page.removesuffix(".qmd") / "figure-html"
    counts = {}
    for png in sorted(folder.glob("*.png")) if folder.is_dir() else []:
        label = re.sub(r"-\d+\.png$", "", png.name)
        assert label in labels, f"{lang}/{page}: {png.name} matches no chunk"
        counts[labels[label]] = counts.get(labels[label], 0) + 1
    return counts


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


def lead_paragraph(callout, lead):
    found = [p for p in body_of(callout).select("p") if text_of(p).startswith(lead)]
    return found[0] if len(found) == 1 else None


def time_paragraph(callout, lang):
    found = lead_paragraph(callout, LEAD_INS[lang][1])
    assert found is not None, f"no paragraph starting with {LEAD_INS[lang][1]!r}"
    return text_of(found)


def numbers_in(text: str) -> list[float]:
    return [float(n) for n in re.findall(r"\d+(?:\.\d+)?", text)]


PAGES = [(lang, page) for page in DONE for lang in LANGS]
TRANSLATED = [(lang, page) for page in DONE for lang in LANGS if lang != "en"]


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
    where = position(soup)
    first_h2 = soup.select_one("main h2")
    assert first_h2 is not None and where[id(brief)] < where[id(first_h2)], "the brief comes after a ## heading"
    # the three parts, in order: the goals' lead-in, exactly three goals, the time line, then "Read first" if any
    goals_lead = lead_paragraph(brief, LEAD_INS[lang][0])
    time_line = lead_paragraph(brief, LEAD_INS[lang][1])
    assert goals_lead is not None and time_line is not None, "a lead-in is missing"
    lists = body_of(brief).select(":scope > ul")
    assert len(lists) == 1 and len(lists[0].select(":scope > li")) == 3, "not exactly three goals in one list"
    order = [where[id(goals_lead)], where[id(lists[0])], where[id(time_line)]]
    read_first = lead_paragraph(brief, LEAD_INS[lang][2])
    if read_first is not None:
        order.append(where[id(read_first)])
    assert order == sorted(order), "the parts are out of order"
    assert brief.select("a.term") == [], "glossary term links in the brief"


@pytest.mark.parametrize("lang,page", PAGES)
def test_stated_reading_time_follows_the_rule(site, lang, page):
    """Read the minutes and the hands-on band in the brief: the same numbers in every language, the minutes
    from the English source by the rule, the band from the review's table, and the band called an estimate."""
    minutes = reading_minutes(prose_words(source("en", page)))
    line = time_paragraph(box(built(lang, page), "page-brief"), lang)
    stated = numbers_in(line)
    assert stated == [minutes, *HANDS_ON[page]], f"stated {stated}, the rule gives {minutes} minutes and {HANDS_ON[page]} hours"
    assert line.endswith(ESTIMATE[lang] + "."), f"the time line doesn't end with {ESTIMATE[lang]!r}"


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
def test_brief_sits_after_the_opening_paragraph(lang, page):
    """In the source: the page's first box, after the opening paragraph, before the first section heading
    (on page 18, inside the first html-only block)."""
    assert brief_problems(source(lang, page), page) == []


@pytest.mark.parametrize("lang,page", PAGES)
def test_key_points_sit_above_the_prose_guard(lang, page):
    """In the source: after the key points, only hidden chunks (the page's last `# Prose guard` among them)
    come before Exercises; on page 18, the key points open the html-only block that follows the Prose guard."""
    assert key_points_problems(source(lang, page), page) == []


@pytest.mark.parametrize("page", NUMBERED)
def test_drawing_rule_finds_every_frozen_figure(page):
    """The source rule against the truth, the figures the last render froze, on all 18 English pages."""
    assert drawing_chunks(source("en", page)) == set(frozen_figures("en", page))


@pytest.mark.parametrize("lang,page", PAGES)
def test_every_chunk_that_draws_has_alt_text(lang, page):
    """Source level, so a missing alt text fails before the page is rendered: one alt text per figure."""
    text = source(lang, page)
    frozen = frozen_figures(lang, page)
    chunks = executable_chunks(text)
    wrong = {i: (alt_count(chunks[i - 1][1]), frozen.get(i, 1)) for i in drawing_chunks(text) | set(frozen)
             if alt_count(chunks[i - 1][1]) != frozen.get(i, 1)}
    assert wrong == {}, "chunk: (alt texts, figures)"


@pytest.mark.parametrize("lang,page", PAGES)
def test_every_figure_has_alt_text(site, lang, page):
    """Every figure the render froze appears with an alt text of at least 20 characters. A page without
    figure chunks passes with no images; a page whose source draws but whose built page shows nothing fails."""
    images = built(lang, page).select("main img")
    expected = sum(frozen_figures(lang, page).values())
    assert len(images) == expected, f"{len(images)} images on the page, {expected} frozen figures"
    if drawing_chunks(source(lang, page)):
        assert images, "the source draws figures but the page shows none"
    short = [(img.get("src"), img.get("alt")) for img in images if len((img.get("alt") or "").strip()) < 20]
    assert short == []


@pytest.mark.parametrize("lang,page", TRANSLATED)
def test_translated_alt_texts_are_not_english(site, lang, page):
    english = [img.get("alt") for img in built("en", page).select("main img")]
    translated = [img.get("alt") for img in built(lang, page).select("main img")]
    assert len(translated) == len(english)
    assert [a for a, b in zip(translated, english) if a == b] == [], "alt text left in English"


@pytest.mark.parametrize("lang", LANGS)
def test_legend_tells_the_truth_about_the_rollout(site, lang):
    """Until every numbered page has its boxes, the legend says they arrive page by page and never that
    every numbered page has them. Task 4.6 turns this round."""
    legend = text_of(built(lang, "getting-started/using-this-site.qmd").select_one("section#the-boxes-youll-see"))
    if set(DONE) != set(NUMBERED):
        assert ROLLOUT[lang] in legend
        assert [p for p in EVERY_PAGE[lang] if p in legend] == []
        missing = len(NUMBERED) - len(DONE)
        assert (MOST if missing >= len(NUMBERED) / 2 else SOME)[lang] in legend, f"{missing} of 18 pages lack the boxes"
    else:
        assert ROLLOUT[lang] not in legend


@pytest.mark.parametrize("lang", LANGS)
def test_report_docx_has_no_brief(site, lang):
    """Page 18's boxes sit inside its html-only blocks, so the Word file shows neither. Until page 18 gets
    its boxes (Task 4.6) this passes trivially; it is here so the rollout can't break the Word file."""
    text = docx_text(SITE_ROOT / lang / "report" / "18-example-report.docx")
    for title in TITLES[lang] + TITLES["en"]:
        assert title not in text.replace("’", "'"), title


# ---------------------------------------------------------------- source rules

def chunk_end(lines, start):
    """The index of the line that closes the chunk opening at `start`."""
    j = start + 1
    while j < len(lines) and lines[j].rstrip() != "```":
        j += 1
    return j


def chunk_starts(lines):
    """Indices of the lines that open an executable chunk."""
    i = 0
    while i < len(lines):
        if CHUNK_START.match(lines[i]):
            yield i
            i = chunk_end(lines, i)
        i += 1


def is_guard(lines, start):
    options = options_of("\n".join(lines[start + 1:chunk_end(lines, start)]))
    first_code = lines[start + 1 + len(options)] if start + 1 + len(options) < len(lines) else ""
    return is_hidden(options) and first_code.startswith("# Prose guard")


def next_nonblank(lines, i):
    while i < len(lines) and not lines[i].strip():
        i += 1
    return i


def previous_nonblank(lines, i):
    while i >= 0 and not lines[i].strip():
        i -= 1
    return i


def top_level(lines):
    """Indices of lines outside fenced code."""
    fenced = False
    for i, line in enumerate(lines):
        if FENCE.match(line):
            fenced = not fenced
            continue
        if not fenced:
            yield i


def brief_problems(text: str, page: str = "") -> list[str]:
    lines = text.split("\n")
    opens = [i for i in top_level(lines) if BRIEF_OPEN.match(lines[i])]
    if len(opens) != 1:
        return [f"{len(opens)} page-brief boxes"]
    at = opens[0]
    problems = []
    before = lines[previous_nonblank(lines, at - 1)]
    if not before.strip() or before.startswith(("```", ":::", "#", "---")):
        problems.append(f"the brief follows {before[:40]!r}, not the opening paragraph")
    first_section = next((i for i in top_level(lines) if re.match(r"^## .*\{#", lines[i])), len(lines))
    other_box = next((i for i in top_level(lines) if lines[i].startswith("::: {.callout") and i != at), len(lines))
    if not at < min(first_section, other_box):
        problems.append("the brief isn't the first box before the first section")
    html_only = [i for i in top_level(lines) if lines[i].strip() == HTML_ONLY]
    if page == REPORT:
        if not html_only or not html_only[0] < at or any(
                DIV_CLOSE.match(lines[i]) and depth_at(lines, html_only[0], i) == 0 for i in range(html_only[0] + 1, at)):
            problems.append("on page 18 the brief belongs inside the first html-only block")
    elif html_only and html_only[0] < at:
        problems.append("the brief sits after an html-only block")
    return problems


def depth_at(lines, start, i):
    """Div depth just after line i, counting from the div that opens at `start` (depth 1)."""
    depth = 1
    for line in lines[start + 1:i + 1]:
        if DIV_CLOSE.match(line):
            depth -= 1
        elif line.startswith(":::"):
            depth += 1
    return depth


def key_points_problems(text: str, page: str = "") -> list[str]:
    """Where the key points sit in the source. Everywhere but page 18: the box sits above the whole run of
    hidden chunks that ends the page (pages 1 and 2 end with several), so no hidden chunk ends right above it;
    after it only blank lines and hidden chunks come before `## Exercises`, the page's last `# Prose guard` among them. Page 18: the guard sits in the manuscript region, so the box is
    the first thing in the html-only block that follows the guard, and `## Exercises` comes next."""
    lines = text.split("\n")
    opens = [i for i in top_level(lines) if KEY_POINTS_OPEN.match(lines[i])]
    if len(opens) != 1:
        return [f"{len(opens)} key-points boxes"]
    start = opens[0]
    end = start + 1
    while end < len(lines) and not DIV_CLOSE.match(lines[end]):
        if lines[end].startswith(":::"):
            return ["a div inside the key points"]
        end += 1
    guards = [i for i in chunk_starts(lines) if is_guard(lines, i)]
    if not guards:
        return ["no Prose guard chunk"]
    last_guard = guards[-1]
    if page == REPORT:
        problems = []
        opener = previous_nonblank(lines, start - 1)
        if lines[opener].strip() != HTML_ONLY or previous_nonblank(lines, opener - 1) != chunk_end(lines, last_guard):
            problems.append("on page 18 the key points open the html-only block right after the Prose guard")
        following = next_nonblank(lines, end + 1)
        if following >= len(lines) or not EXERCISES_HEADING.match(lines[following]):
            problems.append("on page 18 `## Exercises` follows the key points")
        return problems
    # the box sits above the whole trailing run of hidden chunks: no hidden chunk ends right above it
    above = previous_nonblank(lines, start - 1)
    if any(chunk_end(lines, s) == above and is_hidden(options_of("\n".join(lines[s + 1:above]))) for s in chunk_starts(lines)):
        return ["the key points sit inside the run of hidden chunks that ends the page; put them above it"]
    j = next_nonblank(lines, end + 1)
    while j < len(lines) and not EXERCISES_HEADING.match(lines[j]):
        if not (CHUNK_START.match(lines[j]) and is_hidden(options_of("\n".join(lines[j + 1:chunk_end(lines, j)])))):
            return [f"{lines[j][:50]!r} comes between the key points and Exercises"]
        j = next_nonblank(lines, chunk_end(lines, j) + 1)
    if j >= len(lines):
        return ["no `## Exercises` after the key points"]
    if not end < last_guard < j:
        return ["the page's last Prose guard chunk isn't between the key points and Exercises"]
    return []


def drawing_chunks_without_alt(text: str) -> list[int]:
    chunks = executable_chunks(text)
    return sorted(i for i in drawing_chunks(text) if alt_count(chunks[i - 1][1]) == 0)


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


def test_prose_words_handles_long_and_tilde_fences_and_boxes_with_more_classes():
    wrapped = "One.\n\n````markdown\n```{r}\nnot counted at all\n```\nstill code\n````\n\nTwo.\n"
    assert prose_words(wrapped) == 2
    assert prose_words("One.\n\n~~~\ncode ``` here\nmore code\n~~~\n\nTwo.\n") == 2
    assert prose_words("One.\n\n::: {.callout-note .page-brief .extra}\n## 🎯 Goals and time\nNot these.\n:::\n") == 1


def test_reading_minutes_rounds_to_five():
    # 5 minutes at 90 words a minute is 450 words, so minutes = 5 * round(words / 450).
    assert reading_minutes(5040) == 55  # 5040 / 450 = 11.2 -> 11 -> 55 (one minute above 4,950 words = 55)
    assert reading_minutes(4860) == 55  # 4860 / 450 = 10.8 -> 11 -> 55 (one minute below)
    assert reading_minutes(4710) == 50  # 4710 / 450 = 10.47 -> 10 -> 50 (the next multiple down)
    assert reading_minutes(120) == 5  # 120 / 450 = 0.27 -> 0 -> floor of 5
    assert reading_minutes(0) == 5
    # exact halves go to the even multiple: 4725 / 450 = 10.5 -> 10 -> 50; 5175 / 450 = 11.5 -> 12 -> 60
    assert reading_minutes(4725) == 50
    assert reading_minutes(5175) == 60


GUARD = "```{r}\n#| include: false\n# Prose guard: numbers\nstopifnot(TRUE)\n```\n"
PY_GUARD = "```{python}\n#| include: false\n# Prose guard (Python side): more\nassert True\n```\n"
HIDDEN = "```{r}\n#| include: false\ncheck_agree(1, 1)\n```\n"
POINTS = "::: {.callout-note .key-points}\n## 📌 Key points\n- One.\n:::\n\n"
EXERCISE_HEADING = EXERCISES + "\n\nText.\n"


def test_key_points_rule_wants_only_hidden_chunks_and_the_last_guard_before_exercises():
    assert key_points_problems(POINTS + GUARD + "\n" + EXERCISE_HEADING) == []
    assert key_points_problems(POINTS + GUARD + "\n" + PY_GUARD + "\n" + EXERCISE_HEADING) == []   # page 2
    assert key_points_problems(GUARD + "\n" + POINTS + PY_GUARD + "\n" + EXERCISE_HEADING)          # between page 2's guards
    assert key_points_problems(HIDDEN + "\n" + POINTS + GUARD + "\n" + EXERCISE_HEADING)            # inside the hidden run
    assert key_points_problems(POINTS + HIDDEN + "\n" + GUARD + "\n" + EXERCISE_HEADING) == []     # page 1
    assert key_points_problems(GUARD + "\n" + POINTS + EXERCISE_HEADING)                           # guard above
    assert key_points_problems(POINTS + "Some prose.\n\n" + GUARD + "\n" + EXERCISE_HEADING)       # prose between
    assert key_points_problems(POINTS + "```{r}\nplot(x)\n```\n\n" + GUARD + "\n" + EXERCISE_HEADING)   # visible chunk
    assert key_points_problems(GUARD + "\n" + EXERCISE_HEADING)                                    # no box


def test_key_points_rule_on_page_18_wants_the_html_only_block_after_the_guard():
    good = GUARD + "\n" + HTML_ONLY + "\n" + POINTS + EXERCISE_HEADING + ":::\n"
    assert key_points_problems(good, REPORT) == []
    assert key_points_problems(good.replace(HTML_ONLY + "\n" + POINTS, HTML_ONLY + "\n"), REPORT)   # no box
    assert key_points_problems(POINTS + GUARD + "\n" + HTML_ONLY + "\n" + EXERCISE_HEADING + ":::\n", REPORT)
    assert key_points_problems(GUARD + "\n" + POINTS + HTML_ONLY + "\n" + EXERCISE_HEADING + ":::\n", REPORT)
    assert key_points_problems(good)     # the page 18 form is wrong on any other page


BRIEF = "::: {.callout-note .page-brief}\n## 🎯 Goals and time\n- A goal.\n:::\n\n"
OTHER_BOX = "::: {.callout-note}\n## 💡 How every section on this page works\nText.\n:::\n\n"
SECTION = "## A test {#a-test}\n\nText.\n"


def test_brief_rule_wants_the_first_box_after_the_opening_paragraph():
    assert brief_problems("Opening paragraph.\n\n" + BRIEF + OTHER_BOX + SECTION) == []
    assert brief_problems("Opening paragraph.\n\n" + OTHER_BOX + BRIEF + SECTION)          # not the first box
    assert brief_problems("Opening paragraph.\n\n" + SECTION + BRIEF)                      # after a section
    assert brief_problems(BRIEF + "Opening paragraph.\n\n" + SECTION)                      # before the paragraph
    on_18 = HTML_ONLY + "\nOpening paragraph.\n\n" + BRIEF + OTHER_BOX + ":::\n\n" + SECTION
    assert brief_problems(on_18, REPORT) == []
    assert brief_problems(on_18)                                                           # elsewhere: no
    outside = HTML_ONLY + "\nOpening paragraph.\n\n" + OTHER_BOX + ":::\n\nParagraph.\n\n" + BRIEF + SECTION
    assert brief_problems(outside, REPORT)


def test_drawing_rule_finds_plots_and_counts_alt_texts():
    r_plot = "```{r}\n#| fig-height: 4\nggplot(d, aes(x)) + geom_bar()\n```\n"
    py_plot = "```{python}\nfig, ax = plt.subplots()\nplt.show()\n```\n"
    assert drawing_chunks_without_alt(r_plot + py_plot) == [1, 2]
    with_alt = r_plot.replace("#| fig-height: 4", "#| fig-height: 4\n#| fig-alt: \"Bar chart of x.\"")
    assert drawing_chunks_without_alt(with_alt) == []
    assert drawing_chunks_without_alt("```{r}\nmean(x)\n```\n```{r}\n#| include: false\nplot(x)\n```\n") == []
    for call in ["cif |>\n  ggcuminc(outcome = 'revision')", "emmip(model, arm ~ visit)"]:
        assert drawing_chunks(f"```{{r}}\n{call}\n```\n") == {1}
    assert drawing_chunks("```{r}\n#| echo: false\n#| label: fig-revision\nrevision_plot\n```\n") == {1}
    assert drawing_chunks("```{mermaid}\nflowchart TD\n```\n\n```{r}\nhist(x)\n```\n") == {2}   # knitr counts mermaid
    two = ["#| fig-alt:", '#|   - "First figure."', '#|   - "Second figure."', "#| fig-height: 3"]
    assert alt_count(two) == 2 and alt_count(['#| fig-alt: "One."']) == 1 and alt_count(["#| echo: false"]) == 0
