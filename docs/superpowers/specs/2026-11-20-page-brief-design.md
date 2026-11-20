# Goals, time and key points on every numbered page: design

Written 20.11.2026 for Task 4.1 of the content-review fixes (audit findings L2 and U7 in `docs/audits/2026-11-20-content-review/`). Doc decided the titles (D6) and the time rule (D7). The form is piloted on page 6 and waits for Doc's approval before pages 1 to 5 and 7 to 18 follow (Tasks 4.2 to 4.6).

## Intent

A reader opening a numbered page can't tell what it will teach, how long it takes or what to read first, and after 25 screens the page goes straight to the exercises. A screen-reader user gets nothing from any figure. Each numbered page gets a box at the top that says what the reader will be able to do, how long it takes and what to read first, a box at the end with the page's key points, and a text alternative for every figure.

## Goals, non-goals, anti-goals

- Goal: one box at the top of each of the 18 numbered pages, "🎯 Goals and time": three goals, the time, and the pages to read first where the page needs them.
- Goal: one box at the end of each numbered page, "📌 Key points": four to six one-sentence points, for the reader who reads only the box and as a review for the others.
- Goal: every figure on a numbered page has alt text (WCAG 2, success criterion 1.1.1, level A).
- Goal: the form can't drift. A test checks each box, the stated time against the rule, and every figure's alt text.
- Non-goal: boxes on the unnumbered pages (home, Getting started, the decision table, Tests A–Z, the glossary, Packages).
- Non-goal: measuring how long learners take. The hands-on time is the reviewers' estimate and says so.
- Non-goal: marking core against reference material (L3), concept questions or a core path. They are separate findings.
- Anti-goal: a key point that says something the page doesn't. A summary is where a careless claim would be read most.
- Anti-goal: a goal the page doesn't teach. Each goal must be provable by one of the page's exercises or one of its "How to report it" steps.
- Anti-goal: alt text written without looking at the figure, or quoting a number that isn't on the page.

## Constraints

- Golden rule 21: the boxes and alt texts exist in `en/`, `de/` and `fr/` with the same structure; code and hidden chunks stay identical. A box adds the same number of lines in each language, so the three files keep the same line count.
- Golden rule 22: every number in a box or an alt text is one the page already prints or states, and the Prose guard pins any number from the data.
- Golden rule 20: page 18's Word file holds only the manuscript.
- `fig-alt` is a chunk option, so adding it re-runs the page (golden rule 5).
- Catalog pages set `toc-depth: 2`; the boxes must not add a table-of-contents entry.

## Approaches

1. **Two callouts with classes, a time rule in a test, `fig-alt` on each chunk (chosen).** The boxes are ordinary callouts, so they look like the site's other boxes and need no new machinery; a class (`.page-brief`, `.key-points`) lets tests and styles find them.
2. **Level-2 sections ("## Key points") instead of callouts.** They would show in the table of contents and break the catalog anatomy (each `##` is one test). Dropped.
3. **A Quarto filter that writes the time into the page.** It would need the words counted at render time, and freeze would not notice a changed rule. Dropped: the time is written by hand and a test checks it.

## Design

### The top box: "🎯 Goals and time"

`::: {.callout-note .page-brief}` with the title `## 🎯 Goals and time`, placed directly after the page's opening paragraph(s) and before the first `## ` heading. It is the first box on the page: on page 6 it comes before the "💡 How every section on this page works" box.

Three parts, in this order, each with a bold lead-in:

1. **After this page you can:** and exactly three bullets. Each goal is something the reader can do after the page and can check themselves against, with a plain verb (choose, run, write, report, explain, spot), never "understand". Each must be answerable by one of the page's exercises or one of its "How to report it" steps. Together they serve the site's three aims: reading the literature critically, understanding how a study's analysis is designed, and writing results.
2. **Time:** "about N minutes to read, about X to Y hours with the exercises (an estimate)." N follows the rule below; X to Y is the band from the review's table (`learning-design.md`, L2), or "about X hours" where the band is one number.
3. **Read first:** links, only where the page's own text assumes an earlier page. Left out where nothing is assumed.

### The end box: "📌 Key points"

`::: {.callout-note .key-points}` with the title `## 📌 Key points`, after the last content section and directly before the hidden `# Prose guard` chunk, which itself sits before `## Exercises`. Four to six bullets, one sentence each, drawn from the page's own ⚠️ boxes and "When to use it" bullets. A key point adds no claim the page doesn't already make, and agrees with the page as it stands (on page 6: Welch's t test by default, never test the variances first, the Mann-Whitney test isn't a test of medians). Points without numbers are preferred; a number from the data is pinned by the Prose guard below. No glossary term links: hover text inside a summary box is noise.

**Placement against the catalog anatomy.** On a catalog page the box falls inside the last `##` section in the rendered HTML (on page 6, inside the log-rank section's "How to report it" step, after its ⚠️ and 🔀 boxes). `tests/site/test_catalog.py::test_section_follows_the_page_anatomy` reads only the `###` step headings, and a callout title isn't a heading, so the test accepts it unchanged. The box needs no section of its own, and none was added. If a later page's anatomy test objects, the fix is to teach that test that a `.key-points` callout ends a section, never to weaken the step check.

### Words to minutes (Doc's decision D7)

The reading time is the same number in all three languages and comes from the English source:

- `prose_words(text)` counts the words of the English `.qmd` outside its YAML front matter and outside fenced code blocks (``` and ~~~ fences, executed or display-only). It drops `:::` div lines, HTML comments, link targets `](...)` and attribute blocks `{...}` (`{.term}`, `{#id}`). Text inside callouts and collapsed solutions counts: it is prose the reader may read. A word is a run of non-space characters with at least one letter or digit, so `##`, `>`, `-`, `|` and `→` don't count.
- The two new boxes are left out of the count. Otherwise writing the time into the box would change the number it states.
- `reading_minutes(words) = max(5, 5 * round(words / 100 / 5))`: 100 words a minute, rounded to 5 minutes, never under 5. Python's `round()` sends an exact half to the even multiple (2,250 words give 20 minutes, 2,750 give 30).
- Page 6: 4,940 words, 50 minutes (the review counted about 5,060 on an earlier version of the page, which gives the same 50).

The hands-on time is the band from the review's table, labeled "(an estimate)": the reviewers judged it from word counts, code chunks and exercises, and nobody measured it.

### Alt text

Every chunk that draws a figure carries `#| fig-alt:` with one sentence: the kind of plot, its variables, and the pattern the page's text discusses (for example "Bar charts of pain at 6 weeks on the 0 to 10 scale, one bar per whole score, boot arm above and cast arm below: most scores lie between 2 and 6, and the boot arm's scores sit lower (median 4) than the cast arm's (median 5)."). The writer opens the rendered figure before writing its sentence and takes every number from the page's own output or text. The R and Python figures of one tabset each get their own sentence, since they differ in detail (page 6: the Python histograms give each panel its own count scale, the Python Kaplan-Meier plot shows survival as a proportion and adds censored counts).

`fig-alt` reaches both engines under knitr: checked on page 6 on 20.11.2026, the rendered `<img>` of an R chunk and of a Python (reticulate) chunk both carry the `alt` attribute.

Alt text is prose: German and French pages translate it. `tests/site/test_translations.py` compares chunk options across languages; a `#| fig-alt:` line is compared by its numbers and its place among the options only, and every other option and every line of code still has to match exactly.

Known cases for the rollout: a chunk that draws two figures (page 3, two `ggplot()` calls in one chunk) needs one alt text per figure (knitr takes a list), and page 18's labeled figure chunk (`fig-revision`) needs checking against its caption.

### The legend

`getting-started/using-this-site.qmd` ("The boxes you'll see", `#the-boxes-youll-see`) shows the two boxes, the 🎯 box first and the 📌 box last, around the four existing kinds. The 🎯 entry says how the times are worked out: the English page's words at 100 words a minute, rounded to 5 minutes, the same in every language; the time with the exercises is an estimate, not a measurement. `tests/site/test_conventions.py::test_callout_legend_shows_all_six_kinds` (formerly "four kinds") checks the six titles, the two classes and the time rule.

### Styling

Both boxes keep the note style and get one rule in `styles.css`: a 2-pixel frame on all four sides (the left border stays 5 pixels) in `var(--bs-link-color)`, the HFR blue `#006DB5` in light mode and its lighter tint `#5AA9E6` on the dark theme. That sets the page's frame apart from the 💡 notes inside it without a new color.

### Page 18

Page 18 renders to Word too (golden rule 20). Its two boxes sit inside its existing `::: {.content-visible when-format="html"}` blocks, so the Word file doesn't change. `test_report_docx_has_no_brief` checks that the Word file holds neither title.

### Glossary rows

`docs/glossary.csv` holds the two titles and the lead-ins in all three languages: "🎯 Goals and time", "📌 Key points", "After this page you can:", "Time:", "about N minutes to read", "about X to Y hours with the exercises", "(an estimate)", "Read first:".

| English | German | French |
|------|------|------|
| 🎯 Goals and time | 🎯 Ziele und Zeitbedarf | 🎯 Objectifs et durée |
| 📌 Key points | 📌 Das Wichtigste in Kürze | 📌 L'essentiel |

### Tests

`tests/site/test_page_brief.py` holds `NUMBERED` (the 18 pages, relative to a language folder), `DONE` (the pages that have their boxes; page 6 now), `TITLES`, `LEAD_INS`, `HANDS_ON` (the review's bands for all 18 pages), `prose_words()` and `reading_minutes()`. Over `DONE` and the three languages:

- `test_page_opens_with_goals_and_time`: one `.page-brief` callout with the language's title, the first box on the page, before the first `## ` heading and outside every section, with the goals and time lead-ins, exactly three goal bullets and no glossary term links.
- `test_stated_reading_time_follows_the_rule`: the numbers in the time line are the minutes from `reading_minutes(prose_words(English source))` and the review's band, in every language.
- `test_page_ends_with_key_points`: one `.key-points` callout with the language's title, four to six bullets, no `a.term`, after the last `##` heading before Exercises and before `section#exercises`.
- `test_key_points_sit_above_the_prose_guard`: in the source, the box closes and the hidden `# Prose guard` chunk follows directly.
- `test_every_figure_has_alt_text`: every `img` inside `main` has an `alt` of at least 20 characters.
- `test_every_chunk_that_draws_has_alt_text`: in the source, every visible chunk that draws (`ggplot()` and base graphics in R, `plt.show()` in Python) has `#| fig-alt:`, so a missing one fails before rendering.
- `test_every_done_page_is_numbered_and_exists_in_every_language`.
- `test_report_docx_has_no_brief`: page 18's Word file, in each language, contains neither title. It passes trivially until page 18 gets its boxes (Task 4.6).

Rule tests on small samples: `prose_words()` ignores code, link targets, attributes and the boxes and counts callouts and solutions; `reading_minutes(5060) == 50`; the key-points and drawing rules bite.

### Rollout

Tasks 4.2 to 4.6 add pages to `DONE`; Task 4.6 makes `DONE == NUMBERED` and drops the subset. For each page: goals drafted from what its sections and exercises do, each tied to the exercise or "How to report it" that proves it; key points from its own ⚠️ boxes and "When to use it" bullets; one alt text per figure, written after opening the figure. Each pull request lists the English goals and key points so Doc can read them without opening the diff.

### CLAUDE.md

A golden rule names the two boxes, their placement, the time rule, alt text and `tests/site/test_page_brief.py`.

## Left to the builder

- The German and French wording of the boxes, the legend entries and the alt texts. They are Claude's; native reviewers correct them on the published site.
- Which earlier pages a page needs under "Read first".
