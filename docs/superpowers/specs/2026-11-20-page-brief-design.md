# Goals, time and key points on every numbered page: design

Written 20.11.2026 for Task 4.1 of the content-review fixes (audit findings L2 and U7 in `docs/audits/2026-11-20-content-review/`). Doc decided the titles (D6) and the time rule (D7). The form is piloted on page 6 and waits for Doc's approval before pages 1 to 5 and 7 to 18 follow (Tasks 4.2 to 4.6). Since 23.11.2026 every numbered page has the boxes and alt text: `DONE` equals `NUMBERED`.

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

`::: {.callout-note .page-brief}` with the title `## 🎯 Goals and time`, placed directly after the page's opening paragraph(s) and before the first `## ` heading. It is the first box on the page: on page 6 it comes before the "💡 How every section on this page works" box. On page 18 it sits inside the first html-only block, after the opening paragraph and before the "💡 How this page works" box (see "Page 18").

Three parts, in this order, each with a bold lead-in:

1. **After this page you can:** and exactly three bullets. Each goal is something the reader can do after the page and can check themselves against, with a plain verb (choose, run, write, report, explain, spot), never "understand". Each must be answerable by one of the page's exercises or one of its "How to report it" steps; where a goal is only shown in a solution, the exercise's prompt asks for it (page 6, Exercise 3). Together they serve the site's three aims: reading the literature critically, understanding how a study's analysis is designed, and writing results.
2. **Time:** "about N minutes to read, about X to Y hours with the exercises (an estimate)." N follows the rule below; X to Y is the band from the review's table (`learning-design.md`, L2), or "about X hours" where the band is one number.
3. **Read first:** links, only where the page's own text assumes an earlier page. Left out where nothing is assumed.

### The end box: "📌 Key points"

`::: {.callout-note .key-points}` with the title `## 📌 Key points`, after the last content section, as the last thing a reader sees before `## Exercises`. In the source, only blank lines and hidden chunks come between the box and `## Exercises`, and the page's last `# Prose guard` chunk is among them. On page 6 the guard follows the box directly. Pages 1 and 2 end with several hidden chunks (page 2: an R Prose guard, then a Python one, the last one); the box goes above the whole run, so no hidden chunk ends right above it (a box between page 2's two guards is rejected), and the last Prose guard still sits below it. Page 18 has its own rule (see "Page 18").

Four to six bullets, one sentence each, drawn from the page's own ⚠️ boxes and "When to use it" bullets, and from its other teaching text where a goal would otherwise have no key point (page 6: the odds ratio point, from the Fisher section and Exercise 3). Each goal has a key point. A key point adds no claim the page doesn't already make, agrees with the page as it stands (on page 6: Welch's t test by default, never test the variances first, the Mann-Whitney test isn't a test of medians), and doesn't turn the page's observation into an instruction the page doesn't give. Where it repeats a wording the page warns against, it quotes it as the page does. Points without numbers are preferred; a number from the data is pinned by the Prose guard. No glossary term links: hover text inside a summary box is noise.

**Placement against the catalog anatomy.** On a catalog page the box falls inside the last `##` section in the rendered HTML (on page 6, inside the log-rank section's "How to report it" step, after its ⚠️ and 🔀 boxes). `tests/site/test_catalog.py::test_section_follows_the_page_anatomy` reads only the `###` step headings, and a callout title isn't a heading, so the test accepts it unchanged. The box needs no section of its own, and none was added. If a later page's anatomy test objects, the fix is to teach that test that a `.key-points` callout ends a section, never to weaken the step check.

### Words to minutes (Doc's decision D7)

The reading time is the same number in all three languages and comes from the English source:

- `prose_words(text)` counts the words of the English `.qmd` outside its YAML front matter and outside fenced code blocks, executed or display-only. A fence closes only on the same character repeated at least as often, with nothing after it, so a four-backtick wrapper around a chunk, or a `~~~` fence that holds three backticks, stays code. It drops `:::` div lines, HTML comments, link targets `](...)` and attribute blocks `{...}` (`{.term}`, `{#id}`). Text inside callouts and collapsed solutions counts: it is prose the reader may read. A word is a run of non-space characters with at least one letter or digit, so `##`, `>`, `-`, `|` and `→` don't count.
- The two new boxes are left out of the count. Otherwise writing the time into the box would change the number it states. For counting, a box is found by its class (`.page-brief` or `.key-points`) whatever else its opener says; the placement tests still insist on the exact openers.
- `reading_minutes(words) = max(5, 5 * round(words / 90 / 5))`: 90 words a minute, rounded to 5 minutes, never under 5. Python's `round()` sends an exact half to the even multiple (2,025 words give 20 minutes, 2,475 give 30).
- Page 6: 5,015 words, 55 minutes (5,015 ÷ 90 = 55.7, rounded to 55).
- The rate was 100 words a minute in the pilot's first version. On 23.11.2026 Doc set it to 90: on the corrected text, 90 puts 17 of the 18 pages within 5 minutes of the content reviewers' estimates (page 16 is 10 minutes under, no page is more than 5 over), while 100 left pages 12 to 16 10 to 15 minutes under. The reviewers' figures are judgments, not measurements, and Doc will check the rate with a timed read, so it may change again.

The hands-on time is the band from the review's table, labeled "(an estimate)": the reviewers judged it from word counts, code chunks and exercises, and nobody measured it.

### Alt text

Every chunk that draws a figure carries `#| fig-alt:`, one sentence per figure. The sentence leads with the kind of plot and the pattern the page's text discusses, then gives the detail (panels, scales, bands, tables). Aim for about 250 characters or fewer in English; translations run longer. For example: "Bar charts of pain at 6 weeks: the boot arm's scores (median 4, upper panel) sit lower than the cast arm's (median 5, lower panel); most scores lie between 2 and 6, with one bar per whole score from 0 to 10."

- The writer opens the rendered figure before writing its sentence, and takes every number from the page's own output or text; a number the text doesn't already quote goes into the Prose guard (page 6: the 5-year survival as proportions, 0.899 and 0.711).
- A number says what it counts. `data/cohort.csv` has one row per procedure, so its counts are procedures ("Eingriffe", "interventions"), never patients: 246 rows with implant A are 232 patients.
- The R and Python figures of one tabset each get their own sentence, since they differ in detail (page 6: the Python histograms give each panel its own count scale, the Python Kaplan-Meier plot shows survival as a proportion and adds censored counts).

`fig-alt` reaches both engines under knitr: checked on page 6 on 20.11.2026, the rendered `<img>` of an R chunk and of a Python (reticulate) chunk both carry the `alt` attribute.

Alt text is prose: German and French pages translate it, except the figure inside page 18's manuscript, which keeps its English alt text (see "Page 18"). `tests/site/test_translations.py` compares chunk options across languages; a `#| fig-alt:` line, or each item of a `fig-alt` list, is compared by its numbers and its place among the options only, and every other option and every line of code still has to match exactly.

### The legend

`getting-started/using-this-site.qmd` ("The boxes you'll see", `#the-boxes-youll-see`) shows the two boxes, the 🎯 box first and the 📌 box last, around the four existing kinds. The 🎯 entry says how the times are worked out: the English page's words at 90 words a minute, rounded to 5 minutes, the same in every language; the time with the exercises is an estimate, not a measurement. Its last sentence reads: "Every numbered page has this box and ends with the 📌 Key points box." (German: "Dieser Kasten steht auf jeder nummerierten Seite, und jede endet mit dem Kasten «📌 Das Wichtigste in Kürze»." French: "Chaque page numérotée comporte cet encadré et se termine par l'encadré « 📌 L'essentiel ».")

The legend must be true. During the rollout it said in one sentence that the boxes were being added page by page, starting with page 6, so most numbered pages didn't have them yet ("most" while 9 or more of the 18 pages lack the boxes, "some" below that). Since 23.11.2026 `DONE` equals `NUMBERED` and the legend says every numbered page has them; the page-by-page wording and its test branches remain only for a page added later. `tests/site/test_conventions.py::test_callout_legend_shows_all_six_kinds` checks the six titles, the two classes and the time rule in the English legend; while `DONE` differs from `NUMBERED` it checks the rollout sentence, and once they are equal that the legend says "every numbered page" and not "page by page". `test_page_brief.py::test_legend_tells_the_truth_about_the_rollout` does the same in all three languages: while `DONE` differs from `NUMBERED`, the language's "page by page" (`ROLLOUT`), the word the count calls for (`MOST` or `SOME`) and none of the `EVERY_PAGE` phrases; once they are equal, one of the `EVERY_PAGE` phrases (case ignored, since the sentence may open with it) and no "page by page".

### Styling

Both boxes keep the note style and get one rule in `styles.css`: a 2-pixel frame on all four sides (the left border stays 5 pixels) in `var(--bs-link-color)`, the HFR blue `#006DB5` in light mode and its lighter tint `#5AA9E6` on the dark theme. That sets the page's frame apart from the 💡 notes inside it without a new color.

### Page 18

Page 18 renders to Word too (golden rule 20). Both boxes sit inside its existing `::: {.content-visible when-format="html"}` blocks, so the Word file doesn't change:

- **The top box** is inside the first html-only block (it opens right after the hidden setup chunks), after the opening paragraph and before the "💡 How this page works" box.
- **The key points.** Page 18's Prose guard sits outside the html-only blocks, directly after the manuscript, so the page-wide rule can't hold there. On page 18 the key points are the first thing in the html-only block that follows the Prose guard, and `## Exercises` follows them. `key_points_problems()` accepts exactly that on page 18 and rejects that form on every other page.

The alt text has its own exception on page 18. A figure inside the manuscript (Figure 1, `fig-revision`) keeps its English alt text on the German and French pages: the manuscript stays English there (golden rule 21), and `test_page_18_manuscript_stays_in_english` requires its chunk options to be identical in all three languages. `test_translated_alt_texts_are_not_english` lists the manuscript's figures in `MANUSCRIPT_FIGURES` and asserts that their alt text equals the English page's; `test_manuscript_figures_are_the_listed_ones` fails if a figure outside the html-only blocks is missing from that list. The alt text doesn't reach the Word file: checked on 23.11.2026, `word/document.xml` was byte-identical before and after `fig-alt` was added, and the picture's description stays empty.

`test_report_docx_has_no_brief` checks that the Word file holds neither title.

### Known cases

What the rollout meets, and what the tests do about it:

- **Pages without figures** (1, 2 and 15). `test_every_figure_has_alt_text` compares the number of images on the built page with the number of frozen figures: a page with no figure chunks passes with no images; a page whose source has figure chunks but whose built page shows none fails.
- **Which chunks draw.** The source rule finds a figure chunk by its calls: in R the ggplot family, `ggsurvfit()`, `ggcuminc()` (pages 13 and 18), `emmip()` (page 16) and base graphics; in Python `plt.show()`; and any chunk labeled `fig-...`, which is a figure even when it only prints a stored plot (page 18's `fig-revision`). The truth is the frozen output: knitr names each figure file after its chunk's label, or `unnamed-chunk-N` with N the chunk's place among all executable chunks, the mermaid diagram on page 3 included. `test_drawing_rule_finds_every_frozen_figure` checks, on all 18 English pages, that the rule finds exactly the chunks that produced files under `_freeze/en/<page>/figure-html/`; it holds on all 18 today. `test_every_chunk_that_draws_has_alt_text` asks each such chunk for as many alt texts as it froze figures.
- **A chunk that draws several figures** (page 3: one chunk draws a histogram and a QQ plot) carries a YAML list, one item per figure, in figure order: `#| fig-alt:` followed by one `#|   - "..."` line per figure. `test_translations.py` compares each item by its numbers, so the items translate but their number and their numbers can't change.
- **Page 18**: the placement rules above.
- **Several Prose guards** (pages 1 and 2): the key points come before the run of hidden chunks that ends the page; the page's last Prose guard is in that run.
- **Long fences and box openers with extra classes**: handled by `prose_words()` (see "Words to minutes"), with rule tests, rather than banned.
- **A diagram drawn in the browser.** Page 3's flowchart is a mermaid diagram that the browser draws, so there is no image to carry alt text; the paragraph after it ("In words: …") states the flow in words instead.
- **R and Python figures that differ only in color and marker** may carry the same sentence, but each chunk carries its own `#| fig-alt:` line.
- **"Read first"**: each entry describes what the linked section really teaches, not what its title suggests.

### Glossary rows

`docs/glossary.csv` holds the two titles and the lead-ins in all three languages: "🎯 Goals and time", "📌 Key points", "After this page you can:", "Time:", "about N minutes to read", "about X to Y hours with the exercises", "(an estimate)", "Read first:".

| English | German | French |
|------|------|------|
| 🎯 Goals and time | 🎯 Ziele und Zeitbedarf | 🎯 Objectifs et durée |
| 📌 Key points | 📌 Das Wichtigste in Kürze | 📌 L'essentiel |

### Tests

`tests/site/test_page_brief.py` holds `NUMBERED` (the 18 pages, relative to a language folder), `DONE` (the pages that have their boxes; equal to `NUMBERED` since 23.11.2026, and a page added later joins both lists with its boxes), `TITLES`, `LEAD_INS`, `ESTIMATE`, `HANDS_ON` (the review's bands for all 18 pages), `prose_words()`, `reading_minutes()` and the source rules. Over `DONE` and the three languages:

- `test_page_opens_with_goals_and_time`: one `.page-brief` callout with the language's title, the first box on the page, before the first `## ` heading and outside every section; the goals' lead-in, exactly three goals in one list, the time line and "Read first" (if any), in that order; no glossary term links.
- `test_stated_reading_time_follows_the_rule`: the numbers in the time line are the minutes from `reading_minutes(prose_words(English source))` and the review's band, in every language, and the line ends with the language's "(an estimate)".
- `test_page_ends_with_key_points`: one `.key-points` callout with the language's title, four to six bullets, no `a.term`, after the last `##` heading before Exercises and before `section#exercises`.
- `test_brief_sits_after_the_opening_paragraph` and `test_key_points_sit_above_the_prose_guard`: the source placement rules above, page 18 included.
- `test_every_chunk_that_draws_has_alt_text`: in the source, one alt text per frozen figure in every chunk that draws, so a missing one fails before rendering.
- `test_every_figure_has_alt_text`: the built page shows as many images as were frozen, each with an `alt` of at least 20 characters.
- `test_translated_alt_texts_are_not_english`: no German or French alt text is identical to the English one, except on page 18's manuscript figures (`MANUSCRIPT_FIGURES`), which carry exactly the English page's alt text.
- `test_every_done_page_is_numbered_and_exists_in_every_language`.

Over all 18 pages or all three languages: `test_drawing_rule_finds_every_frozen_figure`, `test_legend_tells_the_truth_about_the_rollout` (see "The legend"), `test_report_docx_has_no_brief` (page 18's Word file contains neither title), and `test_manuscript_figures_are_the_listed_ones` (in each language's page 18 source, the chunks that draw outside the html-only blocks are exactly `MANUSCRIPT_FIGURES`).

Rule tests on small samples: `prose_words()` ignores code (long and tilde fences too), link targets, attributes and the boxes (with extra classes too) and counts callouts and solutions; `reading_minutes(5040) == 55`, with exact halves going to the even multiple (`reading_minutes(4725) == 50`); the brief, key-points (page 18 and several guards included) and drawing rules bite; `alt_count()` reads a list; `test_manuscript_figure_rule_finds_the_figures_outside_the_html_only_blocks`: `manuscript_figures()` finds the drawing chunks outside the html-only blocks, by label or as `unnamed-chunk-N`, and not those inside the blocks, the hidden ones or a table.

### Rollout

Tasks 4.2 to 4.6 added pages to `DONE`; since 23.11.2026 (Task 4.6) `DONE == NUMBERED` and the legend says every numbered page has the boxes. The subset and the page-by-page wording's test branches stay, for a page added later: it joins `NUMBERED` and `DONE` with its boxes, following the steps below. For each page: goals drafted from what its sections and exercises do, each tied to the exercise or "How to report it" that proves it; key points from its own ⚠️ boxes and "When to use it" bullets, one for each goal; one alt text per figure, written after opening the figure. Each pull request carries, for Doc to read without opening the diff, the English goals and key points and two tables: each goal with the exercise or "How to report it" that proves it, and each key point with the page line that already says it.

### CLAUDE.md

Golden rule 24 names the two boxes, their placement, the time rule, alt text and `tests/site/test_page_brief.py`. It was worded by `DONE` during the rollout, so it stayed true while pages were added. Since 23.11.2026 it says that every numbered page has the two boxes, that `DONE` equals `NUMBERED` in `tests/site/test_page_brief.py`, and that a page added later joins both lists with its boxes.

## Left to the builder

- The German and French wording of the boxes, the legend entries and the alt texts. They are Claude's; native reviewers correct them on the published site.
- Which earlier pages a page needs under "Read first".
