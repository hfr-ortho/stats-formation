# Content review: accuracy, completeness, design and ease of use

Date: 20.11.2026. Scope: the English pages (26 pages, about 132,000 words) and the built site at commit 6949255, which is the live version. Nothing on the site was changed. This folder is new and uncommitted.

Every finding has an ID. The one-line version is here; the quoted sentence, the evidence and a proposed fix are in the detail files:

- [accuracy.md](accuracy.md): IDs A, B, C
- [usability-and-setup.md](usability-and-setup.md): IDs U
- [learning-design.md](learning-design.md): IDs L, with reading times per page and a proposed workshop series

## Bottom line

1. **The numbers are right.** Ten reviewers read every page against its printed output and found no wrong number and no wrong definition of a core concept (p-value, confidence interval, hazard, odds ratio). The automatic checks are doing their job.
2. **Fifteen sentences are inaccurate** (urgency 1). They are explanations around correct output, or one page contradicting another. Each was re-checked against the data, the code or the package documentation before it went on this list.
3. **Three things are broken for readers today:** 15 bullet lists per language display as run-on paragraphs on pages 13 to 18; the decision table falls apart on a narrow screen; the setup page has gaps that will stop some beginners.
4. **The site teaches "run and report an analysis" very well, and two of your three goals only in passing.** Critical reading of papers and study design have no pages of their own: nothing on study designs, bias, sample size, or reporting guidelines. The pages are also long (40 to 60 minutes each to read) with no stated objectives, times, summaries or suggested path.

## Status

Where each finding in the fix plan ([`docs/superpowers/plans/2026-11-20-content-review-fixes.md`](../../superpowers/plans/2026-11-20-content-review-fixes.md)) stands. Task is the plan task that fixes it; a finding listed under several tasks is fixed page by page.

| ID | Task | Status | Pull request |
|---|---|---|---|
| A1 | 1.3 | done | #48 |
| A2 | 1.3 | done | #48 |
| A3 | 1.3 | done | #48 |
| A4 | 1.3 | done | #48 |
| A5 | 1.3 | done | #48 |
| A6 | 1.4 | done | #50 |
| A7 | 1.1 | done | #46 |
| A8 | 1.1 | done | #46 |
| A9 | 1.1 | done | #46 |
| A10 | 1.2 | done | #47 |
| A11 | 1.2 | done | #47 |
| A12 | 1.2 | done | #47 |
| A13 | 1.2 | done | #47 |
| A14 | 1.2 | done | #47 |
| A15 | 1.1 | done | #46 |
| U1 | 1.1 | done | #46 |
| U2 | 2.1 | done | #49 |
| U3 | 2.2 | done | pending |
| U4 | 2.2 | done | pending |
| U5 | 2.2 | done | pending |
| U6 | 2.2 | done | pending |
| U7 | 4.1 to 4.6 | open |  |
| B1 | 3.8 | open |  |
| B2 | 3.5 | open |  |
| B3 | 3.8 | open |  |
| B4 | 3.8 | open |  |
| B5 | 3.2, 3.3, 3.4, 3.6, 3.7, 3.8 | partly (3.2 done) | pending |
| B6 | 3.3 | open |  |
| B7 | 3.3 | open |  |
| B8 | 3.2 | partly (3.2 done) | pending |
| B9 | 3.5 | open |  |
| B10 | 3.2, 3.3 | partly (3.2 done) | pending |
| B11 | 3.7 | open |  |
| B12 | 3.3, 3.4, 3.6 | open |  |
| B13 | 3.3, 3.5 | open |  |
| B14 | 3.5 | open |  |
| B15 | 3.5, 3.7 | open |  |
| B16 | 3.7 | open |  |
| B17 | 3.6 | open |  |
| B18 | 3.2, 3.6 | partly (3.2 done) | pending |
| B19 | 3.7 | open |  |
| B20 | 3.7 | open |  |
| B21 | 3.4 | open |  |
| B22 | 3.2 | done | pending |
| B23 | 3.2 | done | pending |
| B24 | 3.4, 3.5, 3.6 | open |  |
| B25 | 3.9 | open |  |
| C1 | 3.4, 3.7 | open |  |
| C2 | 3.3 | open |  |
| C3 | 3.5 | open |  |
| C4 | 3.5 | open |  |
| C5 | 3.5 | open |  |
| C6 | 3.6 | open |  |
| C7 | 3.6 | open |  |
| C8 | 3.9 | open |  |
| C9 | 3.9 | open |  |
| C10 | 3.9 | open |  |
| C11 | 3.2 | done | pending |
| C12 | 3.2, 3.3 | partly (3.2 done) | pending |
| C13 | 3.7 | open |  |
| C14 | 3.2 | done | pending |
| L2 | 4.1 to 4.6 | open |  |

U1: the test that now guards against it (`tests/site/test_sources.py`) found 19 such lists per language on pages 13 to 18, not 15; all 57 are fixed.

## Urgency 1: inaccurate statements (fix first)

| ID | Page | What is wrong |
|---|---|---|
| A1 | 4 | Reports a "median follow-up of 4.365 years" computed the way page 13 calls wrong (page 13 gives 5.62). |
| A2 | 4 | "263 patients at risk", including in the Results sentence: they are 263 procedures in 233 patients. |
| A3 | 5 | The binomial "by hand" text describes a different set of results from the one that adds up to the p-value. |
| A4 | 6 | "The two [odds ratios] are always close": not in small tables (6.4 against 9 in a simple example). |
| A5 | 6 | Says the Hodges-Lehmann estimate lands "on whole numbers", then five lines later "whole or half points". The second is right. |
| A6 | 8, 10 (Results on 8, 9, 10) | Wrong reason for the one-sided CI of ω² and Cramér's V ("only its lower bound is informative"). Results sentences report "95% CI 0.12 to 1.00", which has no upper limit and isn't comparable with the site's other 95% CIs. **Your decision:** report two-sided intervals, or keep one-sided and explain. |
| A7 | 13 | "The band widens as patients leave": it widens only at revisions. The "10-year" survivorship and its CI are the 7.9-year values carried forward while the number at risk falls from 92 to 21. |
| A8 | 14 | Calls 1 − Kaplan-Meier "had been revised", which page 13 says never to do when many patients died. |
| A9 | 17 | "A different ICC for every model": two-way random and two-way mixed give the same number. The page also uses "Type" differently from the paper it cites. |
| A10 | 1 | "If you let the software guess types, it silently turns `32.1 kg/m2` into a missing value": neither reader does that. |
| A11 | 1 | "Each recode … turns anything else into a missing value": "Mme" becomes "Male", and unrecognized comorbidity text becomes "no disease". |
| A12 | 1 | The 564 blank survey rows are called missed visits; 91 of them are single skipped items. |
| A13 | 3 (also 2, 7) | The flowchart sends every "bounded" score to the rank column, which contradicts the page's own examples; the real criterion is values piled at a floor or ceiling. |
| A14 | 3 | Says Pearson correlation "compares means" within groups. |
| A15 | 17 | "The ICC is a number from 0 to 1", while the page's own exercise prints a CI of −0.04 to 0.78. |

The German and French pages carry the same sentences (the site's tests keep the three in step). I did not read them.

## Urgency 2: fix soon

**Broken for readers now** (usability-and-setup.md)

| ID | What |
|---|---|
| U1 | 15 bullet lists per language render as one paragraph with literal hyphens (pages 13 to 18; confirmed on the live site). Cause: no blank line before the list. |
| U2 | Decision table at phone width: the last column shrinks to 31 pixels and its text breaks letter by letter. |
| U3 | Setup page: "Session → Restart R" is an RStudio menu, and the "language picker" isn't Positron's name or location for that control (per Positron's documentation; I did not check the app). |
| U4 | No R version on the setup page; the lockfile says 4.6.0, the check script accepts 4.4. With another R the step 6 check fails while step 8 says "All good". |
| U5 | Setup says 30 to 45 minutes; a reviewer estimates 60 to 90 for a beginner and measured about 5 GB. No mention of disk space, administrator rights or HFR-managed PCs; no route without Git. Windows untested. |
| U6 | Git is introduced only as a download tool, but the real-data page expects safe commits. |
| U7 | No figure on the site has alt text. |

**Model Methods and Results sentences that residents will copy** (accuracy.md, 2b)

| ID | What |
|---|---|
| B1 | Page 18: 7 of the 22 "missing" 1-year scores are patients revised, dead or censored before 1 year. The primary analysis silently drops every early failure, and the Methods don't say so. |
| B2 | Pages 11 and 12: two Results sentences report CIs that the warning box directly below says "can't be trusted". |
| B3 | Page 18's model Methods lacks what a journal requires (design, selection, ethics statement, missing-data handling, sample size), and no reporting guideline is mentioned anywhere on the site. |
| B4 | Page 18 shows a large baseline imbalance (sex, SMD 0.47) and then reports only the unadjusted result. |
| B5 | Seven smaller ones: CI type missing from page 4's Methods; unadjusted CIs beside Holm-adjusted p-values (pages 15, 16); "R 4.6 and Python 3.13" as the software statement; others. |

**Pages that contradict each other** (accuracy.md, 2c): 14 cases, C1 to C14. The ones most likely to confuse: Welch from the start (page 6) against classic ANOVA unless spreads differ (pages 8, 15); the signed-rank test's symmetry assumption (stated on page 5, ignored on page 7); events per predictor (page 12) against per coefficient (page 14); covariates' own coefficients reported as findings (page 12) against "aren't findings" (page 14); page 13 breaking its own two rules on time points and on where to stop the curve.

**Caveats a critical reader needs that are missing or understated** (accuracy.md, 2d): 20 items, B6 to B25. The most important:

- An odds ratio is not a risk ratio (page 6 never says so; its own exercise gives 1.31 against 1.15).
- What to adjust for: confounder, mediator and collider guidance is on page 14 but not on page 12, which defines "adjusted". Collinearity, interaction and prediction intervals appear nowhere.
- Kappa depends on prevalence (page 17).
- The signed-rank test assumes symmetric differences (pages 5, 7).
- Page 1's number and date helpers mishandle decimal commas ("31,2" becomes 312 in R and 31 in Python) and two-digit birth years, with no warning. This matters for Swiss data.

## Urgency 3: structure and design (plan, then do)

| ID | What | Detail |
|---|---|---|
| L1 | Goals 1 and 2 (critical reading, study design) have no pages of their own. Proposal: three short concept pages with no code. **Your decision** whether the site should grow this way. | learning-design.md |
| L2 | No page states objectives, time needed or prerequisites, and none ends with a summary. Reading all 18 pages takes about 12 to 14 hours; working through them about 38 to 44 (reviewers' estimates). | learning-design.md |
| L3 | The catalog is reference material in table order, presented as a course. Proposal: a named core path of nine pages on the home page; the p-value, effect size and CI section moved out of the end of page 3. | learning-design.md |
| L4 | 49 of 54 exercises need code. Read-only learners get no self-checks. Proposal: two or three concept questions per page, and one "critique this excerpt" exercise per part. | learning-design.md |
| L5 | Nothing is packaged as a workshop. The material divides into eight one-hour sessions plus three optional ones; outline in the detail file. | learning-design.md |
| U8 | Text lines are about 140 characters long on a laptop; 45 to 90 is the comfortable range. | usability-and-setup.md |
| U9 | Inside a catalog section (page 6 is 25 screens) nothing shows which of the seven steps you are on. | usability-and-setup.md |
| U10 | All 60 "R vs Python" boxes are open, for readers told to pick one language. | usability-and-setup.md |
| U11 | The glossary is one 30-screen list of 215 entries with no index or filter. | usability-and-setup.md |

## Urgency 4: polish

About 30 small points in accuracy.md ("small points") and usability-and-setup.md (U13, U14). None would mislead a careful reader.

## What I don't know

- **German and French.** Not read. Code and numbers are identical by test; prose findings very likely apply to all three.
- **Swiss law and HFR policy on the real-data page.** Not judged. usability-and-setup.md lists every claim an expert should confirm.
- **Windows and hospital-managed PCs.** No setup step was run on either. No fresh install was run on a Mac in this review either.
- **Phones.** Nothing narrower than 488 pixels was viewed. Whether glossary tooltips work on a touch screen is untested (U12). Safari was not used.
- **The Positron wording (U3)** was checked against Positron's documentation, not the app.
- **Python figures.** Reviewers mostly viewed the R figures. Several noted that Python's survival plots use a different y-axis.
- **Sources.** No glossary definition was compared with its cited reference, and the decision table was not compared with Motulsky's book. References named in the findings (marked E in accuracy.md) were not opened, except Koo & Li 2016 and the R, scipy, effectsize and renv documentation.
- **Nine claims on the pages that nobody could verify** are listed at the end of accuracy.md. The one that matters most: page 11 says two named R packages give wrong results, and neither is installed to test it.
- **Reading times and the setup time** are judgments from word counts, not measurements on learners.
- **Tier 2 evidence.** Findings marked R in the detail files were run by a reviewer and not re-run by me. All of urgency 1 was re-checked.
- **Accessibility** was checked only for alt text and line length, not for contrast, keyboard use or screen readers.
- **The Word file** of page 18 was not opened.

## How the review was done

Nine reviewers each read two or three pages completely, source and rendered output, against one brief (statistical accuracy first, then missing caveats, then clarity for a resident). A tenth walked the setup page as a beginner on Mac and Windows and compared it with the repository. Each finding had to be labeled verified, established or uncertain. I then re-checked every urgency 1 finding and the main urgency 2 findings myself, viewed the built site in a browser at two widths in light and dark, ran an external link check (158 links, all resolve) and searched the sources for the topics your three goals need.
