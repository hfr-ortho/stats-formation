# Content Review Fixes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Correct every Urgency 1 and Urgency 2 finding of the content review of 20.11.2026, and give each of the 18 numbered pages its objectives, time needed and a closing summary, in English, German and French.

**Architecture:** Four phases, each a series of small pull requests that can be published on their own: (1) the inaccurate statements, (2) display and setup faults, (3) misleading sentences, contradictions and missing caveats, (4) a "page brief" box at the top and a "Key points" box at the end of every numbered page, with figure alt text added in the same pass. Every finding keeps its ID from the review, and every fix is pinned by a Prose guard line or a site test so it can't come back.

**Tech Stack:** Quarto with knitr (R and Python through reticulate), pytest (`tests/site`, `tests/python`), `just`, lychee.

**Spec:** `docs/audits/2026-11-20-content-review/` (`README.md` for the list, `accuracy.md`, `usability-and-setup.md` and `learning-design.md` for each finding's quoted sentence, evidence and proposed fix). The design of the page brief is in Phase 4 of this plan and becomes `docs/superpowers/specs/2026-11-20-page-brief-design.md` in Task 4.1.

**Size:** about 20 pull requests. Every numbered page is re-run up to three times (once in Phase 1 or not at all, once in Phase 3, once in Phase 4).

## Decisions for Doc before work starts

Each task below is written for the recommended option. A different answer changes only the tasks named.

| # | Decision | Recommended | Changes |
|---|---|---|---|
| D0 | Does the standing permission to publish verified fix batches cover this review's fixes? | Yes for Phases 1 and 2. Ask before each Phase 3 pull request (new explanations) and each Phase 4 one (new feature). | When a pull request is merged |
| D1 | A6: effect-size CIs on pages 8, 9, 10 | Two-sided (`alternative = "two.sided"`), and 2,000 bootstrap replicates for ε² and Kendall's W. They then read like every other 95% CI on the site and have an upper limit. | Task 1.4 |
| D2 | C1: Welch from the start (page 6) against classic ANOVA (pages 8, 15) | Keep the classic ANOVA example. Say that Welch's ANOVA is the safe default, that the spread rule is a judgment made from the plot and never a test, and show Welch's result for the same data beside it. | Task 3.4 |
| D3 | C7: page 13 reports 10-year survivorship with 21 of 600 at risk, against its own 10% rule | Keep 2, 5 and 10 years (registries report 10). Say that the example goes past the rule on purpose to show the tail, and what the tail is worth (A7). | Tasks 1.1, 3.6 |
| D4 | B1: page 18's primary analysis drops the 7 patients who left follow-up before 1 year | Add a visible step that cross-tabulates "1-year score missing" against "event before 1 year", and put the counts and the handling into the model Methods and Results. | Task 3.8 |
| D5 | B3: ethics and guideline sentences in page 18's model Methods | Add real sentences for design, selection, one joint per patient, assessment windows and missing data. For ethics approval, consent and sample size, add a box "What a real Methods also needs" with bracketed placeholders, not invented approval numbers. Link the STROBE checklist. | Task 3.8 |
| D6 | Titles of the two new boxes | "🎯 Goals and time" and "📌 Key points"; German "🎯 Ziele und Zeitbedarf", "📌 Das Wichtigste in Kürze"; French "🎯 Objectifs et durée", "📌 L'essentiel". | Phase 4 |
| D7 | The times shown | Reading time by one stated rule: English prose words ÷ 100, rounded to 5 minutes (100 words a minute leaves room for the code and output; it reproduces the reviewers' estimates within about 10 minutes). Hands-on time as a band from the review ("about 2 to 3 hours"), labeled as an estimate until the first workshops give real figures. | Phase 4 |
| D8 | U5: a route without Git | Add "Download ZIP" as an alternative to step 3 and step 5, only after it has passed an end-to-end test on a Mac (Task 2.2). Windows stays marked untested until someone runs it on an HFR PC. | Task 2.2 |
| D9 | U3: names of Positron's controls | Doc, or the implementer with Doc watching, reads the names off the Positron window before the page changes. Positron's documentation says "Interpreter picker" and has no "Session → Restart R". | Task 2.2 |

## Global Constraints

- Never commit to `main`. One branch and one pull request per task; `main` is fast-forwarded to the exact reviewed commit. Merging follows D0.
- Three languages together (golden rule 21): every change to an English page is made in the same commit in `de/` and `fr/`. Code, hidden chunks, numbers, Methods and Results sentences are identical in all three; prose is translated following `docs/translation-guide.md` and `docs/glossary.csv` (Swiss Standard German, "Sie", no "ß"; "vous", non-breaking space before `:`).
- New German and French sentences are unreviewed by a native speaker. Each pull request description lists them, by page and section, for the reviewers.
- Accuracy rule (golden rule 22): no number or explanation is published unchecked. Every number a fix adds to the prose gets a line in that page's `# Prose guard` chunk. Every statement about what a function does is run first. A finding marked **E** in `accuracy.md` rests on a reference nobody opened: open it (Task 3.1) or bring the question to Doc; never write it from memory.
- A changed page is re-run and its `_freeze/` output committed (golden rule 5). Run `quarto render <page>` for the page in each language: a single-page render always runs the code.
- Hidden chunks stay byte-identical across languages. Never loosen a `check_agree()` tolerance, change a seed or edit `data/` to make a fix pass (golden rules 9, 15).
- A site test that pins the old wording is updated to pin the corrected wording in the same commit. It is never deleted or weakened.
- Results sentences keep the reporting conventions (golden rule 8): numbers only, "to" for ranges, p to three decimals.
- American spelling. "Anterior approach", never "DAA". Dates in prose as DD.MM.YYYY.
- No reviewer's or learner's name goes into the repository.

## Review Focus

1. A fix that is right in English and drifts in German or French (a reversed comparison, a dropped "not"). `tests/site/test_translations.py` compares numbers and structure, not meaning: each task's reviewer reads the three versions of every changed sentence side by side.
2. A corrected sentence that quotes a number no visible chunk prints. Every task checks its new numbers against the rendered output, not only the Prose guard (golden rule 22).
3. A fix on one page that creates a new contradiction with another page. Task 3.9 is a cross-page read of everything Phases 1 to 3 changed.
4. A page edited in Phase 1 and again in Phase 3 from a stale branch, silently undoing the first fix. Every task starts from the current `main`; Task 3.9 re-runs the Phase 1 tests.
5. A reader on a phone or without a mouse. The decision table (Task 2.1) and the new boxes (Task 4.1) are looked at in a browser at 488 pixels wide and in dark mode, not only tested.

---

## The batch workflow

Every task that changes pages runs these steps. Tasks refer to them as W1 to W9 and list only what is specific to them.

- [ ] **W1: Branch.** `git switch main && git pull && git switch -c review/<task-id>-<slug>`
- [ ] **W2: Write the failing test** named in the task (site test or Prose guard line). Run it and see it fail for the stated reason.
- [ ] **W3: Edit the English page** as the task says. Verify each new number or software claim by running the code on `data/`.
- [ ] **W4: Mirror in `de/` and `fr/`.** Code and hidden chunks copied byte for byte; prose translated.
- [ ] **W5: Re-run the changed pages:** `quarto render en/<folder>/<page>.qmd`, then the same path under `de/` and `fr/`. Expected: no error; the Prose guard and every `check_agree()` pass.
- [ ] **W6: Read the rendered English page** at the changed places (`_site/en/...html`): the sentence, the output it points to, the tab in both languages.
- [ ] **W7: Run every check.** `just check` (expected: `pytest tests/site` passes, lychee 0 errors) and `just test` (expected: pass).
- [ ] **W8: Record.** In `docs/audits/2026-11-20-content-review/README.md`, mark the task's IDs `done` in a Status table (Task 1.1 creates it: columns ID, Task, Status, Pull request).
- [ ] **W9: Commit and open the pull request.** `git add` the three language files, `_freeze/` for those pages, the tests and the audit README. The description lists the IDs fixed and the new German and French sentences. Wait until a check is actually listed (`until gh pr checks <n> | grep -q "pass\|fail"; do sleep 10; done`), then merge as D0 says, and confirm one changed prose phrase on the live page with a bounded `curl | grep` loop.

---

## Phase 1: the inaccurate statements (Urgency 1)

### Task 1.1: Pages 13 to 18: collapsed lists, and the four survival and agreement statements (U1, A7, A8, A9, A15)

**Files:**
- Modify: `en|de|fr/survival/13-kaplan-meier.qmd`, `14-cox-regression.qmd`, `en|de|fr/beyond/15-post-hoc.qmd`, `16-mixed-models.qmd`, `17-agreement.qmd`, `en|de|fr/report/18-example-report.qmd`
- Test: `tests/site/test_sources.py`, `tests/site/test_survival.py`, `tests/site/test_beyond.py`
- Modify: `docs/audits/2026-11-20-content-review/README.md` (Status table)

- [ ] **Step 1 (W2): the list test.** In `tests/site/test_sources.py` add `list_glued_to_paragraph(text: str) -> list[int]`: line numbers, outside fenced code, where a line starting with `- ` or `1. ` follows a non-blank line that is neither a list item, an indented continuation, a heading, a table row, nor a `:::` line. Add `test_rule_catches_a_list_glued_to_its_paragraph()` (a three-line sample fails, the same sample with a blank line passes) and `test_every_list_is_separated_from_the_paragraph_above()` over every `.qmd` under `en/`, `de/`, `fr/`. Expected failure: 15 locations per language on pages 13 to 18.
- [ ] **Step 2: insert the blank line** before each of the 45 lists. Nothing else on those lines changes.
- [ ] **Step 3: A7, page 13.** At the "shaded band" bullet (en line 282): "**The shaded band** is the 95% CI. It widens at each revision, and widens more when few procedures remain at risk. Between revisions its width doesn't change, however many patients leave." After the survivorship table (en lines 337 to 348), replace "The 10-year CI … is the widest" with a sentence that says: no revision happened after 7.9 years, so the 10-year estimate and its CI are the 7.9-year values carried forward, while the number at risk falls from 92 to 21 (R's counts); a flat band is not a precise one. Prose guard: `max(followup_years[revised == 1]) == 7.9`; `n.risk` 92 at 7.9 years and 21 at 10; survival and both CI limits equal at 7.9 and 10 years.
- [ ] **Step 4: A8, page 14** (en line 169). "By 5 years, the Kaplan-Meier estimate of revision (1 − Kaplan-Meier, with deaths censored) was 28.9% for implant C against 10.1% for implant A: a ratio of 2.85, not 3.07". The rest of the paragraph stays. Test in `tests/site/test_survival.py`: `test_cox_page_never_calls_one_minus_km_the_proportion_revised` asserts "had been revised (1 − Kaplan-Meier)" is absent from the page text.
- [ ] **Step 5: A9 and A15, page 17.** Lines 76 to 79: name the three choices as Koo and Li do, with `irr::icc()`'s argument in brackets: **Model** (two-way random or two-way mixed; `model = "twoway"` for both), **Type** (single rater or the mean of several; `unit`), **Definition** (absolute agreement or consistency; `type`). Add one sentence on the one-way model (each knee read by different raters), which is what pingouin's `ICC(1,1)` row is. Line 188: "The same data give a different ICC for each definition and type, and for a one-way model: here 0.889 … Two-way random and two-way mixed give the same number; they differ in who the result applies to." Line 29: "usually between 0 and 1; an estimate or a CI limit below 0, as in exercise 3, means no reliability". Test in `tests/site/test_beyond.py`: `test_icc_box_says_random_and_mixed_give_the_same_number` (the warning box contains "give the same number"; the page text doesn't contain "for every model").
- [ ] **Step 6: W4 to W9.** The German and French list fixes are the same blank lines.

### Task 1.2: Pages 1, 2, 3 and 7: tidy-data claims, "bounded", Pearson (A10 to A14)

**Files:**
- Modify: `en|de|fr/foundations/01-tidy-data.qmd`, `02-demographics.qmd`, `03-distributions.qmd`, `en|de|fr/catalog/07-two-paired-groups.qmd`
- Test: `tests/site/test_sources.py`, `tests/site/test_foundations.py`

- [ ] **Step 1 (W2).** `tests/site/test_foundations.py`: `test_tidy_page_states_what_guessing_and_recoding_really_do` asserts the page text lacks "silently turns" and contains "473" and "91"; `test_bounded_is_not_a_reason_for_the_rank_column` asserts the flowchart text lacks "bounded" and contains "floor or ceiling". Extend `test_tidy_recodes_send_unexpected_codes_to_missing` in `test_sources.py`: step 5 contains no `regex("^f"` and no `regex("^m"`.
- [ ] **Step 2: A10** (page 1, en line 168). Say what guessing does (the BMI column comes back as text in R and as a mix of numbers and text in pandas, and differs between tabs), and that forcing a number type is what turns `32.1 kg/m2` into a missing value. Run both readers on both tabs first and write only what they return. The advice "read everything as text" stays.
- [ ] **Step 3: A11** (page 1, step 5). Code, both languages: the sex recode matches whole values, not the first letter. List the distinct raw values first (`count(step4, sex)`), and use exactly those, lower-cased, in the `case_when()` and its Python twin. The hidden answer-key check must still pass unchanged. Prose (en line 427): the sex, procedure, side and ASA recodes send anything unexpected to missing; the three comorbidity flags are 1 when the abbreviation is found and 0 otherwise, so an unknown spelling counts as "no". Add the comorbidity flags to check 3's cross-tab (raw `comorbidities` text against the three flags, both languages).
- [ ] **Step 4: A12** (page 1, en line 643). "…with the response blank. There are 564 blank rows: 473 from 72 missed visits and 91 single items skipped in a visit that was otherwise answered." Prose guard: the three counts from `items`.
- [ ] **Step 5: A13.** Page 3 flowchart label: "Strongly skewed, piled up at a floor or ceiling, or ordinal". Page 2 (en line 168) and page 7 (en line 43): replace "bounded" with "piled up at a floor or ceiling". Check with `grep -n "bounded" en/` that no other use sends a score to the rank column for being bounded.
- [ ] **Step 6: A14** (page 3, en line 23). "The methods in the first column work with means and SDs of the values themselves: t tests and ANOVA compare means, and Pearson correlation measures a straight-line association. They assume roughly normal data (for t tests and ANOVA, within each group)."
- [ ] **Step 7: W4 to W9.**

### Task 1.3: Pages 4, 5 and 6 (A1 to A5)

**Files:**
- Modify: `en|de|fr/catalog/04-describe-one-group.qmd`, `05-one-group-vs-hypothetical.qmd`, `06-two-unpaired-groups.qmd`
- Test: `tests/site/test_catalog.py`

- [ ] **Step 1 (W2).** `test_describe_page_counts_procedures_not_patients`: in the `kaplan-meier` section of page 4, the text contains "263 procedures" and no "263 patients". `test_binomial_box_describes_the_set_it_adds_up`: page 5's binomial section contains "no more likely than 1,034" and "1,122".
- [ ] **Step 2: A1** (page 4, en line 638). Keep the output. Say that 4.365 is the middle value of the `followup_years` column, that it is not the study's median follow-up because revisions and deaths cut the column short, and link to page 13's "How long were patients followed?", which gives 5.62 years. Prose guard: reverse Kaplan-Meier median rounds to 5.62.
- [ ] **Step 3: A2** (page 4, en lines 697, 698, 751, and 135). "procedures" for "patients" wherever the count is rows of the cohort. The Results sentence becomes "…; 263 procedures at risk)".
- [ ] **Step 4: A3** (page 5, en line 752). "Seeing exactly 1,034 would be very unlikely, and so would every result that is no more likely than 1,034: 1,034 or fewer on the low side, 1,122 or more on the high side. Their probabilities add up to 0.0000268…" Prose guard: the smallest result above 1,080 that is no more likely than 1,034 is 1,122.
- [ ] **Step 5: A4** (page 6, en line 709). "The two are close unless the counts are small; say which you report."
- [ ] **Step 6: A5** (page 6, en line 424). "…so the Hodges-Lehmann estimate and its CI can only land on whole or half points" (keep the rest of the sentence; here all three are whole).
- [ ] **Step 7: W4 to W9.**

### Task 1.4: Pages 8, 9 and 10: effect-size intervals (A6, decision D1)

**Files:**
- Modify: `en|de|fr/catalog/08-three-plus-unmatched.qmd`, `09-three-plus-matched.qmd`, `10-association.qmd`
- Test: `tests/site/test_sources.py`, `tests/site/test_catalog.py`

- [ ] **Step 1 (W2).** `tests/site/test_sources.py`: `test_effect_size_cis_are_two_sided` asserts every `omega_squared(`, `eta_squared(`, `cramers_v(`, `rank_epsilon_squared(` and `kendalls_w(` call that doesn't pass `ci = NULL` passes `alternative = "two.sided"`, and the two bootstrap functions pass `iterations = 2000`. `tests/site/test_catalog.py`: `test_no_results_sentence_reports_a_one_sided_ci` asserts no `**Results:**` paragraph on pages 8 to 10 contains "one-sided" or "to 1.00)".
- [ ] **Step 2: code.** Add the arguments to every such call, visible and hidden, including exercise solutions (`grep -n` the five function names in `en/catalog`). `set.seed(2026)` stays directly before the two bootstrap calls.
- [ ] **Step 3: prose.** Replace each "can't be negative, so only its lower bound is informative" (page 8 line 213, page 10 line 594) and each "R reports a lower bound only" (page 9 lines 239, 473) with: effectsize's default for these effect sizes is a one-sided interval, which mirrors the one-tailed F or chi-square test; `alternative = "two.sided"` asks for the usual interval, comparable with the other 95% CIs on this site. Read each new interval off the rendered output and put it in the sentence and the Results. Values seen in the review, to be confirmed on the render: ω² 0.06 to 0.15; ε² 0.00 to 0.02; Cramér's V 0.14 to 0.35 (page 8) and 0.10 to 0.27 (page 10); partial η² 0.46 to 0.54; Kendall's W about 0.77 to 0.94.
- [ ] **Step 4: page 10's label.** With an upper limit of 0.27 the interval excludes the "medium" benchmark of 0.3; adjust "small-to-medium" to what the interval supports.
- [ ] **Step 5: Prose guard.** Each quoted limit, read from the effectsize object.
- [ ] **Step 6: W4 to W9.** The 🔀 boxes that say Python computes no such CI stay true.

---

## Phase 2: display and setup faults

### Task 2.1: The decision table on a narrow screen (U2)

**Files:**
- Modify: `styles.css`
- Test: `tests/site/test_structure.py`

- [ ] **Step 1 (W2).** `test_decision_table_columns_cannot_collapse`: `styles.css` gives every `.decision-table` cell a `min-width` (a rule on `.decision-table td, .decision-table th`).
- [ ] **Step 2.** In `styles.css`: `min-width: 8.5rem` on every cell of `.decision-table`, keeping 11rem on the first column. The wrapper already scrolls sideways.
- [ ] **Step 3: look.** Serve `_site` (`python3 -m http.server 8765 --bind 127.0.0.1` from `_site/`) and open `/en/choose-a-test.html`, `/de/…`, `/fr/…` at 488 and 1,440 pixels, light and dark. Expected at 488: no cell narrower than its longest word, no row taller than about 150 pixels, the table scrolls sideways. Stop the server.
- [ ] **Step 4: W7 to W9.** No page is re-run (CSS only); `git status` shows nothing under `_freeze/`.

### Task 2.2: The setup page (U3 to U6, decisions D8 and D9)

**Files:**
- Modify: `en|de|fr/getting-started/setup.qmd`, `scripts/check_setup.R`, `README.md`
- Test: `tests/python/test_check_setup.py`, `tests/site/test_getting_started.py`

- [ ] **Step 1: facts first.** (a) D9: record Positron's names for the interpreter control and the restart control from the window. (b) D8: in a fresh folder with `RENV_PATHS_ROOT` set to an empty folder, download the repository ZIP, unzip, open in Positron, run steps 6 to 8. Record whether both checks end "All good". (c) Record the sizes the page will quote (`du -sh` on the installed pieces). If (b) fails, the ZIP route is not added and Doc is told why.
- [ ] **Step 2 (W2).** `tests/python/test_check_setup.py`: `test_r_check_wants_the_lockfiles_r_version` reads `R.Version` from `renv.lock` and asserts `check_setup.R` compares major.minor with it. `tests/site/test_getting_started.py`: `test_setup_page_says_what_you_need_before_you_start` (the page names the R version from `renv.lock`, disk space and administrator rights) and `test_setup_page_uses_no_rstudio_menu` ("Session → Restart R" absent).
- [ ] **Step 3: `scripts/check_setup.R`.** The R line passes only when major.minor equals the lockfile's; its fix text names that version.
- [ ] **Step 4: the page.** A "Before you start" box: R 4.6, about 5 GB free, about an hour, internet, administrator rights for the installers, and what to do on an HFR-managed PC (Doc supplies the sentence, or it says to ask IT). Positron's real control names (step 1a). Step 5: where the `projects` folder is in the Open Folder dialog on each system; the ZIP alternative if step 1b passed, with "no GitHub account needed". Step 4: which Windows installer to choose. Step 6: the message renv prints when the R version differs, added to Troubleshooting. A short "Updating your copy" paragraph (`git pull`, or download the ZIP again). Change "30–45 minutes" to the figure Doc accepts.
- [ ] **Step 5: U6.** Reword "Git … keeps track of changes" to what the reader uses it for here (downloading and updating), and link from the real-data page's commit section to a named Git introduction (open the link before adding it).
- [ ] **Step 6: W4, W6 to W9.** No R or Python runs. Windows statements that were not run are written as instructions Doc has confirmed, or left out.

---

## Phase 3: misleading sentences, contradictions and missing caveats (Urgency 2)

### Task 3.1: Open the references behind the findings marked E

**Files:**
- Create: `docs/audits/2026-11-20-content-review/sources.md`

- [ ] **Step 1.** For each reference named in `accuracy.md` under an E mark, find the paper (PubMed, the publisher, PMC) and record in `sources.md`: the full citation, what passage supports the fix, and "read" or "not obtained". The list: Sjölander & Greenland 2013 (B10); Hernán 2010 (B17); Bland & Altman 1986 and 1995 (B13, B20); Feinstein & Cicchetti 1990 (B11); Cochran 1954 (B24); Peduzzi 1995, Vittinghoff & McCulloch 2007 (B24, C3); Delacre 2019 (C1); de Vet 2006 (B20); Greenland 2016 (B8); the CONSORT 2010 explanation, item 15 (B23); the STROBE statement (B3); Westreich & Greenland 2013 (C4); Greenland, Robins & Pearl 1999 (C5); Little & Rubin (B16); Altman & Bland 1995 (B8); Newcombe 1998.
- [ ] **Step 2.** For every reference "not obtained", list the finding under "For Doc" in `sources.md` and leave its fix out of the later tasks until Doc answers.
- [ ] **Step 3: commit** on `review/3-1-sources` (no page changes).

### Tasks 3.2 to 3.8: page by page

Each task runs W1 to W9. "Guard" names what the Prose guard pins; "Test" names a new site test. Wording is drafted at execution from the fix lines in `accuracy.md`; the decision is what is listed here.

**Task 3.2: Pages 1 to 3** (`foundations/`)
- [ ] B22: a ⚠️ box on page 1 after step 5: the number helpers assume a decimal point ("31,2" becomes 312 in R and 31 in Python), with `locale = locale(decimal_mark = ",")` and the pandas equivalent; a two-digit year is a guess about the century and wrong for birth dates. The box's code is executed in both tabs. Guard: 312 and 31.
- [ ] C11: page 2 says length of stay is an outcome, kept in the table to show a skewed variable, and is left out of every sentence about balance (en lines 28, 293, exercise 1).
- [ ] B23: page 2 adds randomized trials to "Which should you report?" (no baseline p-values); says how an SMD is computed for a yes/no and for a multi-category variable; says that with a few hundred patients values of 0.1 to 0.15 arise by chance; rewords the sex example as a rare fluke and shows the per-patient p-value. Guard: the per-patient p-value.
- [ ] B18 (pages 2, 3): one sentence where each page computes p-values on all 600 rows, saying so and pointing to its own bilateral warning.
- [ ] C12, C14, B10 (page 3): "for paired data, the differences" at en line 234 and in the flowchart; ASA and the chi-square test reconciled in one sentence; "Treat matched sets like pairs" limited to individually matched sets.
- [ ] B8 (page 3): a third misreading in the box ("p = 0.03 does not mean a 3% chance that there is no difference"); en line 169 reworded; the CI section says what 95% refers to. Update `test_distributions_page_states_statistics_correctly` to pin the new bullet.
- [ ] B5 (page 3, en line 529): both means, the difference with its CI, p; no "higher".

**Task 3.3: Pages 4 to 7** (`catalog/`)
- [ ] B5 (page 4): the Kaplan-Meier Methods names the log-log CI; the median's Methods names its CI method; "Survivorship free of revision" as on page 13. B12: the Python Kaplan-Meier plots on page 4 get `ax.set_ylim(0, 1)` so both tabs show the same axis.
- [ ] C2, B6 (pages 5, 7): both signed-rank sections state the symmetry assumption about the values (page 5) or the differences (page 7), say the p-value belongs to the pseudomedian, and offer the sign test when the claim is about the median, with one executed line showing it. Page 7's "when to use it" no longer routes "skewed differences" to the test without that caveat.
- [ ] B7 (page 6): the risk ratio as a third effect size for the 2 × 2 table, in both languages with `check_agree()`; one sentence that the odds ratio lies further from 1 than the risk ratio when the outcome is common, shown on exercise 3 (odds ratio 1.31, risk ratio 1.15). Guard: both.
- [ ] B10, B13 (page 7): the unstratified Cox model described as a different, accepted analysis for a matched cohort when the pairs get a robust standard error, and as wrong for matched case-control data (only if Task 3.1 obtained the reference); the torsion table grouped by the mean of the two methods. Update `test_pearson_warning_gives_the_trend_at_high_torsion` and any page 7 test to the new numbers.
- [ ] C12 (page 7, exercise at en line 917): justified by the differences, with their plot.

**Task 3.4: Pages 8 and 9**
- [ ] C1 (decision D2): page 8's "similar spreads" bullet says Welch's ANOVA is the safe default and the spread rule a judgment from the plot, never a test; page 8 prints Welch's F beside the classic one for the example. Guard: both F values. (Page 15's matching paragraph is in Task 3.7.)
- [ ] B24: "at least 5" presented as the simple cautious rule, with Cochran's version; exercise 3 says "use Fisher's test to be safe", not "isn't reliable". (Page 10's sentence is in Task 3.5.)
- [ ] B21 (page 9): the warning box and the 🔀 box say the page filters to complete cases first because the functions differ, and that `aov()` with `Error()` is valid only on complete data.
- [ ] B5 (page 8, en line 219): all four group means, or a pointer to the table that holds them. B12: the Python survival plot's axis and clipped labels.

**Task 3.5: Pages 10 to 12**
- [ ] B24 (page 10, en line 437): the expected-count rule worded as on page 8 after Task 3.4.
- [ ] B13 (page 10): one sentence, with the two r values (0.86 and 0.53), that r rises and falls with the range of patients sampled; the trend shown against the mean of the two methods. Guard: both r values.
- [ ] B14, B15 (page 11): a visible chunk with `predict(..., interval = "confidence")` and `"prediction"` at one BMI in both languages, and what each means; "±15 minutes" stated as one SD; the nonparametric section's trigger reworded to residuals; a QQ plot of the residuals. `check_agree()` on the two intervals.
- [ ] B2 (pages 11, 12): the nonlinear Methods sentences state that repeated scores from one knee were treated as independent and that the CIs are illustrative. `test_curve_fits_warn_that_repeated_scores_make_the_cis_unreliable` gains an assertion that the Methods paragraph mentions it.
- [ ] B9, C3, C4, C5 (page 12): a link from "choose the predictors before" to page 14's `#choosing-covariates` with one sentence on confounder, mediator and collider; "per coefficient" for the events rule, as a rule of thumb, on pages 11, 12 and 14 (update `test_events_rule_counts_the_smaller_outcome_group` and `test_cox_events_rule_matches_page_14` only if their pinned phrases change); the linear and logistic sections say which coefficient answers the question and that the others are not findings; page 14's sentence on ratios shifting without confounding carried to page 12's Cox section; one sentence each naming interaction (equal slopes) and collinearity. B15 (page 12): a residual-against-fitted plot for the linear model, or a pointer to page 11's check, in both languages.

**Task 3.6: Pages 13 and 14**
- [ ] C6: page 13 says before the plot that 6 months was fixed in advance on clinical grounds (the reason page 14 gives).
- [ ] C7 (decision D3): the 10% sentence says the example runs past it on purpose.
- [ ] B5: the median follow-up Methods says revisions and deaths were both censored in the reverse analysis. B12: Python plots get the 0 to 1 axis.
- [ ] B17, B18, B24 (page 14): the late-period hazard ratio compares survivors of the first 6 months; restricted mean survival time and fixed-time differences named as alternatives; the bilateral paragraph gives the true reason (the practice data have no built-in correlation between a patient's two joints) and says a robust standard error can come out smaller or larger; "needs about 10 events per term" becomes a rule of thumb.

**Task 3.7: Pages 15 to 17**
- [ ] C1 (page 15, en line 214): the Tukey paragraph uses the same wording as page 8 after Task 3.4, and says the example's two small ASA classes fall under the Dunnett's T3 advice it quotes.
- [ ] B19, C13 (page 15): dividing the threshold is the same decision as multiplying the p-value; why Holm and Tukey disagree on ASA 1 against 2; Dunnett's test named apart from T3; the repeated-measures section points to page 16.
- [ ] B16, B5, B15 (page 16): "and that the model includes" for missing at random; "unadjusted 95% CIs" beside the Holm p-values (also page 15's hazard ratios); a short assumptions paragraph with one residual plot; one sentence on random slopes; "its own overall level" for "baseline".
- [ ] B11, B20 (page 17): a ⚠️ box on kappa and prevalence; one paragraph defining the standard error of measurement and the minimal detectable change, computed in both languages; "about 95%, if the differences are roughly normal". New glossary terms follow the glossary rule (source in `docs/glossary-sources.md`, all three languages).

**Task 3.8: Page 18** (decisions D4, D5)
- [ ] B1: the visible cross-tab; Methods and Results state the handling and the counts (22 without a 1-year score: 7 left follow-up before 1 year, of whom 4 were revised and 1 died; 15 not found). Guard: every count.
- [ ] B3, B4, B5: the Methods sentences and the box of D5; the STROBE link (opened first); an adjusted estimate shown beside the crude one, with baseline differences added to the Discussion list; "Analyses used R 4.6" with the main packages.
- [ ] Both formats re-run: commit `execute-results/docx.json` and `figure-docx/` too. `tests/site/test_report.py` and the docx comparison in `test_translations.py` must pass.

### Task 3.9: Glossary, Tests A–Z, decision table, and the cross-page read

**Files:**
- Modify: `en|de|fr/glossary.qmd`, `tests-a-z.qmd`, `choose-a-test.qmd`, `docs/glossary-sources.md`

- [ ] C8: one wording for Mantel-Haenszel everywhere (the log-rank test R and lifelines compute is the Mantel-Haenszel calculation at each event time); the Tests A–Z row notes the stratified 2 × 2 test of the same name. C9: `#t-test` says "Student's" usually means the equal-variance version. C10, B25: `#censored` says "died without the event (see competing risk)" and names the assumption; `#risk`, `#mcid`, `#score-test`, `#odds-ratio`, `#statistical-significance` each get the one sentence listed in `accuracy.md`. One new entry, "False negative (type II error)", with alpha and beta named, sourced as the glossary rule requires.
- [ ] No code: the pages are not re-run. `tests/python/test_glossary_sources.py` and `test_glossary_terms.py` pass.
- [ ] **Cross-page read.** One reviewer reads, in English, every sentence Phases 1 to 3 changed (from the pull request diffs) against the pages it links to, looking only for new contradictions. Then `uv run pytest tests/site -q` on `main`: every Phase 1 test still passes.

---

## Phase 4: goals, time and key points on every numbered page, with figure alt text (L2, U7)

### Design

- **Top of page, directly after the opening paragraph:** a callout `::: {.callout-note .page-brief}` titled "🎯 Goals and time" (D6) with three parts: "After this page you can:" and three bullets, each a thing the reader can do and the page demonstrably teaches; "Time: about N minutes to read, about X hours with the exercises." (D7); "Read first:" with links, only where a page needs an earlier one.
- **End of page, directly before the `# Prose guard` chunk:** a callout `::: {.callout-note .key-points}` titled "📌 Key points" with four to six one-sentence bullets. A key point adds no claim the page doesn't already make. If one quotes a number from the data, the Prose guard below it pins that number. No glossary term links inside it.
- **Page 18:** both boxes sit inside the existing `::: {.content-visible when-format="html"}` blocks, so the Word file doesn't change.
- **Alt text:** every chunk that draws a plot gets `#| fig-alt:` with one sentence saying what the plot shows (kind of plot, variables, the pattern the text discusses). Alt text is prose: translated in `de/` and `fr/`.
- **The legend** on `getting-started/using-this-site.qmd` ("The boxes you'll see") shows the two new boxes, and says how the times are worked out.
- **Glossary rows** in `docs/glossary.csv` for the two titles and for "After this page you can", "Time", "Read first".

### Task 4.1: Spec, tests and the page 6 pilot

**Files:**
- Create: `docs/superpowers/specs/2026-11-20-page-brief-design.md`, `tests/site/test_page_brief.py`
- Modify: `en|de|fr/catalog/06-two-unpaired-groups.qmd`, `en|de|fr/getting-started/using-this-site.qmd`, `docs/glossary.csv`, `tests/site/test_conventions.py`, `CLAUDE.md`

**Interfaces (produced for Tasks 4.2 to 4.6):**
- `NUMBERED = [...]`: the 18 page paths relative to a language folder, with a `DONE` subset that grows by task until it equals `NUMBERED`.
- `prose_words(text: str) -> int`: words of an English `.qmd` outside front matter and fenced code, link targets and `{.term}` attributes removed.
- `reading_minutes(words: int) -> int`: `max(5, 5 * round(words / 100 / 5))`.
- `TITLES = {"en": ("Goals and time", "Key points"), "de": (...), "fr": (...)}` as decided in D6.

- [ ] **Step 1: write the spec** from the Design section above and Doc's answers to D6 and D7.
- [ ] **Step 2: tests** in `tests/site/test_page_brief.py`, parametrized over `DONE` and the three languages: `test_page_opens_with_goals_and_time` (a `.page-brief` callout with the language's title, exactly three goal bullets, before the first `## ` heading); `test_stated_reading_time_follows_the_rule` (the minutes in the brief equal `reading_minutes(prose_words(english source))`, the same number in all three languages); `test_page_ends_with_key_points` (a `.key-points` callout with four to six bullets, after the last section and before Exercises, containing no `a.term`); `test_key_points_sit_above_the_prose_guard` (in each source, the `.key-points` callout comes before the `# Prose guard` chunk); `test_every_figure_has_alt_text` (every `img` inside `main` on the rendered page has an `alt` of at least 20 characters); `test_report_docx_has_no_brief` (page 18's Word text contains neither title). Plus rule tests on small samples: `prose_words` ignores code and link targets; `reading_minutes(5060) == 50`.
- [ ] **Step 3: run them.** Expected: all fail for page 6 (no box yet).
- [ ] **Step 4: page 6 in three languages.** Goals, time, key points, alt text for its seven figures. Check on the rendered page that the `alt` attribute appears on the R **and** the Python figures; if `fig-alt` doesn't reach Python figures under knitr, stop and report before going on.
- [ ] **Step 5: legend and its test.** `test_callout_legend_shows_all_four_kinds` becomes six kinds.
- [ ] **Step 6: look** at page 6 in the browser at 1,440 and 488 pixels, light and dark, in all three languages.
- [ ] **Step 7: `CLAUDE.md`.** A golden rule for the two boxes and alt text, naming the test.
- [ ] **Step 8: W7 to W9, then stop.** Doc reads the pilot page live (or on the branch) and approves the form before the rollout.

### Tasks 4.2 to 4.6: Rollout

One task per group, each W1 to W9, each adding its pages to `DONE`:

- [ ] **4.2** pages 1 to 3
- [ ] **4.3** pages 4, 5, 7 (6 is the pilot)
- [ ] **4.4** pages 8 to 12
- [ ] **4.5** pages 13 to 17
- [ ] **4.6** page 18; then `DONE == NUMBERED` and the test file drops the subset.

For each page: goals drafted from what its sections and exercises actually do (each goal must be answerable by an exercise or a "How to report it" on that page); key points drafted from the page's own ⚠️ boxes and "When to use it" bullets, adding no claim the page doesn't already make; one alt text per figure. Each pull request description carries the English goals and key points as a list so Doc can read them without opening the diff.

---

## Not in this plan

- Urgency 3 items other than L2 (new concept pages, a core path, concept questions, workshops, line length, collapsing the R-against-Python boxes, a glossary index) and Urgency 4.
- The nine claims nobody could verify (end of `accuracy.md`), including page 11's statement about the deming and mblm packages.
- Native-speaker review of the new German and French sentences, which happens on the published site as before.
- Any setup test on Windows or an HFR-managed PC.
