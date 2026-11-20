# Completeness and learning design in detail

Part of the [content review of 20.11.2026](README.md).

This file measures the site against the brief you gave for this review, which is wider than the site's own stated scope (`CLAUDE.md`: tidy data, Table 1, distribution checks, every test in the decision table, survival analysis and selected extras). So "missing" below means "missing for the three goals you named", not "the site failed to do what it set out to do".

Marks: ✔ = I checked it myself (searches of `en/`, counts from the sources). R = reviewers' judgment or check. Recommendations are proposals for you to decide; nothing was changed.

---

## L1. The three goals against what the site contains ✔

| Your goal | What the site has | What it lacks |
|---|---|---|
| **1. Critically read the literature** | Strong on reading one analysis: what each test does, its output, effect size with CI, and many "⚠️ Watch out" boxes on classic errors (SD against SEM, "no difference" needing a narrow CI, hazard ratio against risk, covariates' coefficients aren't findings, competing risks). | No page on study designs, levels of evidence or bias. No place that teaches reading a paper as a whole. No exercise in which the reader critiques a published-style Methods or Results. The critical-reading lessons are scattered through 18 pages as warning boxes. |
| **2. Understand how a study is designed** | Page 18 step 1 (write the question, the primary outcome and the analysis first). Page 15 on planned comparisons. Page 1 on collecting data. The real-data page on approval and consent. | No sample-size or power section anywhere. No treatment of randomization, blinding, allocation, intention to treat, non-inferiority, choice of comparison group, or how the design decides the analysis. |
| **3. Present results in writing** | The site's strongest side: a Methods and a Results sentence for every test, strict reporting conventions, and page 18's full worked manuscript with a Word file. | No mention of reporting guidelines (STROBE, CONSORT). No flow diagram. Nothing on the Discussion beyond a four-item list on page 18. See accuracy.md B1, B3, B4 for gaps in page 18's model Methods. |

**Evidence (searches of the English sources, glossary excluded):**

| Term | Pages that contain it |
|---|---|
| STROBE, CONSORT, PRISMA, "reporting guideline", "checklist" | 0 |
| blinding, allocation, intention to treat, per protocol, non-inferiority | 0 |
| "level of evidence", meta-analysis, "number needed" | 0 |
| "sample size" as a planning topic, "power calculation" | 0 (the words "sample size" and "power" occur only in passing: "works for any sample size", "more powerful") |
| sensitivity / specificity | 1 mention, not as a topic |
| confound… | 1 page (14) |
| MCID | 3 pages (3, 7, 9) |
| randomized / randomised | 5 pages, as a property of the example trial |

The glossary reviewer listed the terms a resident meets in orthopaedic papers that have **no glossary entry** (each searched): blinding, allocation concealment, intention to treat, per protocol, non-inferiority and equivalence, level of evidence, systematic review, meta-analysis, heterogeneity, forest plot, publication bias, selection bias, recall bias, attrition bias, immortal time bias, confounding by indication, regression to the mean, number needed to treat, incidence against prevalence, sensitivity, specificity, predictive values, ROC curve, case-control study, case series, cross-sectional study, type II error, alpha, MCAR and MNAR, multiple imputation, PASS, SCB, minimal detectable change, median survival, subgroup analysis. Present already: loss to follow-up, registry, propensity score, MCID, randomized trial.

**Recommendation.** Three short concept pages with no code would close most of goal 1 and goal 2, and they would be the pages a read-only learner starts with:

1. **How to read a paper's statistics** (study design in one table: trial, cohort, case-control, case series, and what each can and can't show; the main biases; "what was the primary outcome, was it chosen in advance, how many were lost"; a one-page checklist). It would gather the warning boxes that already exist and link to them.
2. **Planning a study** (question → design → primary outcome → sample size → analysis plan → approval). One worked sample-size calculation for the boot against cast trial would be enough; the data already exist.
3. **Reporting guidelines**, as a section of page 18 or a short page (STROBE for cohorts, CONSORT for trials, where to get the checklist, a flow diagram for the example study).

I don't know whether you want the site to grow in this direction or to stay a statistics-methods site with these topics taught elsewhere in the HFR Ortho program. That is the main decision this review leaves with you.

---

## L2. The pages are long, and nothing tells the reader how long ✔ (counts) / R (times)

Time estimates are the reviewers' judgment from word counts, code chunks and exercises. They were not measured on learners.

| Page | Prose words | Visible code chunks (both languages) | Read only | Hands-on, one language, with exercises |
|---|---|---|---|---|
| 1 · Tidy data | 2,350 | 36 | 30 min | 2 to 2.5 h |
| 2 · Demographics | 1,590 | 18 | 20 min | 1 to 1.25 h |
| 3 · Distributions & choosing a test | 2,950 | 22 | 35 to 40 min | 1.5 h |
| 4 · Describe one group | 3,720 | 30 | 35 to 45 min | 2 to 2.5 h |
| 5 · One group vs a value | 3,720 | 36 | 35 to 45 min | 2 to 2.5 h |
| 6 · Two unpaired groups | 5,060 | 40 | 50 to 60 min | 2.5 to 3 h |
| 7 · Two paired groups | 4,210 | 32 | 40 to 50 min | 2 to 2.5 h |
| 8 · Three or more unmatched | 4,960 | 40 | 45 to 60 min | 2.5 to 3 h |
| 9 · Three or more matched | 4,490 | 36 | 40 to 55 min | 2.5 to 3 h |
| 10 · Association | 2,980 | 30 | 30 min | 1.5 h |
| 11 · Predict from one | 4,850 | 44 | 50 min | 3 h |
| 12 · Predict from several | 4,080 | 34 | 50 to 60 min | 3 h |
| 13 · Kaplan-Meier | 3,710 | 27 | 45 to 55 min | 2 to 2.5 h |
| 14 · Cox regression | 3,820 | 29 | 50 to 60 min | 2.5 to 3 h |
| 15 · Post-hoc tests | 3,580 | 26 | 45 min | 2.5 h |
| 16 · Mixed models | 2,870 | 22 | 45 min | 2 to 2.5 h |
| 17 · Agreement | 2,410 | 22 | 35 min | 1.5 to 2 h |
| 18 · Example report | 3,000 | 24 | 40 min | 2.5 h |
| **All 18** | | | **about 12 to 14 h** | **about 38 to 44 h** |

Against your guardrails:

- **"Digest in a few hours on nights or weekends."** One page fits one evening as reading. The whole site does not, and nothing tells the learner which third to read. The home page says "Work through the parts in order, or go straight to the one you need."
- **No page states** what the reader will be able to do afterwards, how long it takes, or what to read first. Searched: no heading or phrase for objectives, summary, key points, takeaways, checklist or time on any page ✔. Pages 4, 13 and 14 open with a "This page covers" sentence or list, which is the nearest thing.
- **No page ends with a summary.** After 25 screens, page 6 goes straight from the last "How to report it" to the exercises.

**Recommendations (standard practice for self-paced instructional material):**

1. **A box at the top of every numbered page:** "After this page you can…" (three bullets), "Time: 45 min to read, 2.5 h with the exercises", "Read first: page 3". These are advance organizers; they let a learner decide whether to start tonight.
2. **A "Key points" box at the end of every page**, five lines, before the exercises. For the read-only learner it is the page; for the others it is the review.
3. **Mark core against reference** (L3).

---

## L3. The catalog is reference material laid out as a course ✔

Pages 4 to 12 follow the decision table row by row. That is the right structure for "I have data, which test, how do I run it". It is a poor order for learning: page 4 (describe one group) teaches a Kaplan-Meier curve before page 6 teaches a t test; the conditional Cox model for matched pairs (page 7) comes before simple regression (page 11); every page mixes a method residents will use weekly with ones they may never meet (Cochran's Q, nonlinear regression, contingency coefficients).

The site itself half-knows this: page 13 opens by saying pages 4, 6 and 8 "each showed one survival method in a few steps" and then teaches survival again from the start.

**Recommendation: two named paths on the home page, using the pages that exist.**

- **Core path, about 6 evenings** (read, then the exercises you like): page 3's last section (p-value, effect size, CI), then pages 1 → 2 → 3 → 6 (t test, Mann-Whitney, 2 × 2 table) → 7 (paired t test only) → 11 (linear and logistic only) → 12 (linear and logistic) → 13 → 18.
- **Look-up path:** the decision table and Tests A–Z, as now, for everything else.

Sections on the core path can carry a small "core" tag in the sidebar or the page's opening box. Nothing has to move.

**The most important section for goal 1 is hard to find.** "p-values, effect sizes and confidence intervals" is the tenth of ten sections on a page titled "Distributions & choosing a test" (p3:479), after about 2,500 words on normality. Every later page leans on it. It deserves its own short page near the front, or at least the first position on page 3.

---

## L4. Two kinds of learner, one kind of exercise ✔

Your brief names readers who only read and readers who want hands-on practice.

- The 18 numbered pages have 54 exercises. 49 have code in their solution; 5 don't (one on page 1, two each on pages 2 and 3). Page 3's two judgment questions are the closest thing on the site to critical-reading practice.
- There is no quick self-check for the reader who doesn't install anything: no "which of these four statements about this p-value is right", no "spot the problem in this Results sentence".
- The setup takes 60 to 90 minutes and about 5 GB (see usability-and-setup.md U5), and there is no lighter way to try a few lines.

**Recommendations:**

1. **Two or three concept questions per page with collapsed answers**, before the coding exercises. Retrieval practice is among the best-supported techniques in learning research, and these cost no setup. The existing warning boxes supply the material: each one is a misconception that can be turned into a question.
2. **One "read this excerpt" exercise per part:** a short invented Methods and Results paragraph with three planted problems (SEM instead of SD, a baseline p-value in a trial, "no difference" from a wide CI). This is the direct practice for goal 1.
3. Keep the coding exercises as they are. Their three-step progression (same analysis on a new variable, choose the test, write the sentence) is good design, and the solutions are executed code, so they can't go stale.

---

## L5. One-hour workshops: nothing is packaged, and the material divides well

Each reviewer was asked which one-hour hands-on units their pages contain. Merged, they give a series of eight, plus three optional ones. "Needs" lists what does not exist yet.

| # | Workshop | Uses | Hands-on | Needs |
|---|---|---|---|---|
| 0 | Setup clinic (optional, before the series) | setup page | Everyone installs together; ends when both checks print "All good" | The setup fixes in U3 to U5 |
| 1 | What a p-value, an effect size and a CI tell you | p3 `#effect-sizes`, glossary | No code. The BMI example; page 3 exercises 2 and 3; six true/false statements about one result | The concept questions (L4) |
| 2 | Which test? | choose-a-test, p3 `#paired` and `#flowchart`, Tests A–Z | No code. Ten short orthopaedic scenarios: classify goal and data type, name the test, find its other names | The scenarios (ten lines each) |
| 3 | From a messy sheet to Table 1 | p1 checks, p2 | Open the workbook in Excel and list its problems; run the prepared tidying; break it with the month-first mistake; build Table 1; p-value against SMD | Step 5 of page 1 handed out ready-made |
| 4 | Two groups | p6 (t test, Mann-Whitney, 2 × 2), p7 paired t test | Plot, run Welch and Mann-Whitney, rebuild U by counting pairs, 2 × 2 table with risk difference, odds ratio and risk ratio; then the same patients paired and unpaired | Risk ratio on page 6 (B7) |
| 5 | Three or more groups and multiple comparisons | p8 ANOVA, p15 `#why-adjust` to `#after-anova` | Rebuild F by hand; adjust six p-values with Holm by hand; Tukey | — |
| 6 | Regression and what "adjusted" means | p11 linear and logistic, p12 linear | Fit, residual plot, rescale the slope; odds ratio per 24 h; crude against adjusted; sort covariates into confounder, mediator, neither | The confounder sentence on page 12 (B9) |
| 7 | Survival | p13 (censoring to competing risks), p14 hazard ratio | The six-patient table by hand; curve with numbers at risk; 2- and 5-year survivorship; log-rank; 1 − Kaplan-Meier against cumulative incidence; one Cox model | — |
| 8 | From analysis to manuscript | p18 steps 4 to 8 | Start from the tidy file; Table 1; primary analysis; write Methods and Results; mark them against STROBE; answer two reviewer comments (exercises 2 and 3) | STROBE pointer (B3) |
| + | Repeated PROMs with missed visits | p9 opening, p16 | Count completers; random-intercept model; marginal means. R only unless the Python helper is supplied | — |
| + | Can we trust this measurement? | p17 | ICC, Bland-Altman, kappa; exercise 3. Fits one hour as it stands. | — |
| + | Reading a paper | new concept page (L1) | One real paper's Methods and Results, translated term by term | The page, and a paper |

**What would make these usable by someone other than you:** one facilitator page per workshop (aim, the sections to pre-read, a minute-by-minute outline, the exercise, what to say at the end). They could live in the repository without being on the site.

---

## L6. What works well and should be protected in any redesign

- **The fixed seven-step order** of every catalog section (question, when to use it, what the test really does, look at the data first, run it, read the output, effect size, how to report it). Worked examples in a constant format are what beginners need, and the order teaches a habit: look before you test, estimate before you report.
- **"What the test really does" and the "by hand" boxes.** Reviewers singled these out on almost every page (counting pairs for Mann-Whitney, the adjusted coefficient by hand, cumulative incidence built as one changed factor).
- **Honest warning boxes** that show the error happening on the site's own data (Shapiro-Wilk failing both ways; the month-first date mistake that fails differently in R and Python; d_z against d_av at 0.87 and 0.33).
- **Collapsed "Under the hood" boxes and collapsed solutions:** depth is available without being in the way.
- **Machine-checked numbers.** Ten reviewers reading about 130,000 words found no wrong number. That is the prose guards and agreement checks at work.
- **Results sentences that report and don't interpret,** with the interpretation in the surrounding text.

## L7. Smaller learning-design points (R)

- **Page 1, step 5** converts 18 columns in one 40-line chunk of regular expressions, after four steps that are each "small enough to check". Split it into dates, numbers, categories and comorbidities.
- **Page 3** carries ten topics. As one sitting it is too much; reviewers suggest it splits naturally in two (looking at distributions; choosing and interpreting).
- **Page 16's Python tab** hand-builds marginal means with a design matrix that a beginner can't follow from the comments. Say it is a black box that imitates R's emmeans.
- **Page 11** teaches five methods on one page; nonlinear and nonparametric regression are rarely needed by this audience and could be marked as reference.
- **Median survival time** is never explained anywhere on the site, though residents meet it constantly (searched ✔: "median survival" appears on no page).
