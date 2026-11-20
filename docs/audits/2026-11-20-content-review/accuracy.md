# Accuracy findings in detail

Part of the [content review of 20.11.2026](README.md). English pages only.

**Locations** are written `p6:709`: page 6, line 709 of its `.qmd` file in `en/`. Page numbers are the ones in the page titles (p1 = `foundations/01-tidy-data.qmd` … p18 = `report/18-example-report.qmd`).

**How each finding was checked**

| Mark | Meaning |
|---|---|
| ✔ | I re-checked it myself after the reviewer reported it: ran the code on `data/`, read the source lines, or read the package's documentation. |
| R | The reviewer ran code or read the package source and reported the output. I read the sentence on the page but did not re-run the check. |
| E | Rests on an established statistical principle. A reference is named where the reviewer gave one; neither of us opened the reference unless it says so. |

No number quoted on any page was found to be wrong. Every finding below is about what a sentence says the numbers mean, or about two pages saying different things.

---

## Urgency 1: inaccurate statements

### A1. Page 4 gives a median follow-up that page 13 calls the wrong calculation ✔

- **Where:** p4:638.
- **Page says:** "…with a median follow-up of 4.365 years (R shows it as 4.36)."
- **Problem:** 4.365 is the plain median of the follow-up column, which mixes real follow-up with times cut short by revision or death. Page 13 (p13:352) introduces the same calculation with "The obvious way to calculate it is wrong" and reports 5.62 years by the reverse Kaplan-Meier method.
- **Evidence:** `median(cohort$followup_years)` = 4.365; reverse Kaplan-Meier median = 5.62.
- **Fix:** drop the median follow-up from page 4's summary, or label it as the plain median and link to p13 `#follow-up`.

### A2. Page 4 counts procedures as patients, including in the Results sentence ✔

- **Where:** p4:697, p4:698, p4:751. The reviewer also flags p4:135 ("600 patients").
- **Page says:** "**Results:** Revision-free survival at 5 years was 86.3% (95% CI 82.8% to 89.2%; 263 patients at risk)."
- **Problem:** the 263 are procedures. They belong to 233 patients. Page 13's Results sentence says "procedures", and page 4's own "percent of what?" box says the rows are procedures.
- **Evidence:** rows with `followup_years >= 5`: 263; distinct `patient_id` among them: 233.
- **Fix:** "263 procedures at risk" at all three places.

### A3. Page 5 describes a different sum from the one that gives the binomial p-value ✔

- **Where:** p5:752 (step 3 at p5:650 is right).
- **Page says:** "Seeing exactly 1,034 would be very unlikely, and so would every result further from 1,080 on either side. Their probabilities add up to 0.0000268…"
- **Problem:** the p-value adds every result *no more likely* than 1,034. On the upper side that starts at 1,122, which is 42 above 1,080, not 46. "Further from 1,080 on either side" is a smaller set.
- **Evidence:** results no more likely than 1,034: 0 to 1,034 and 1,122 to 1,200, sum 2.68 × 10⁻⁵ (the printed p-value). Results at least 46 away on either side: sum 1.63 × 10⁻⁵.
- **Fix:** "and so would every result that is no more likely than 1,034, on either side".

### A4. Page 6: "The two are always close" is not true for small tables ✔

- **Where:** p6:709 (the 🔀 box on the two odds ratios).
- **Problem:** scipy's sample odds ratio and R's conditional maximum-likelihood odds ratio are close only when the counts are reasonably large. Fisher's test is used exactly where they are not.
- **Evidence:** for the table 3, 1 / 1, 3: sample odds ratio 9, `fisher.test()` estimate 6.41.
- **Fix:** "close unless the counts are small".

### A5. Page 6 says two different things about the Hodges-Lehmann estimate, five lines apart ✔

- **Where:** p6:424 ("land on whole numbers too") against p6:429 ("can only land on whole or half points").
- **Problem:** line 429 is right. The median of an even number of whole-number differences (3,364 here) can be a half.
- **Fix:** "whole or half points" in both.

### A6. Pages 8 and 10 give the wrong reason for the one-sided CI, and the Results sentences inherit an interval with no upper limit ✔

- **Where:** p8:213 (ω²), p10:594 (Cramér's V). Carried into Results sentences on pages 8, 9 and 10 (for example p8:446: "ε² = 0.001, one-sided 95% CI 0.00 to 1.00"). Page 9's wording (p9:239, p9:473: "R reports a lower bound only") describes it correctly but has the same reporting consequence.
- **Page says:** "V can't be negative, so only its lower bound is informative."
- **Problem:** the upper bound is informative: it says how large the effect could be. effectsize's documented reason for the one-sided default is that the F and chi-square tests are one-tailed, so a one-sided interval gives the same decision as the test. Two consequences: (1) a "one-sided 95% CI 0.12 to 1.00" has the lower limit of a two-sided 90% CI, so it isn't comparable with the other 95% CIs on the site; (2) for V on page 10 the two-sided interval (0.10 to 0.27) rules out the "medium" 0.3 that the page's own "small-to-medium" label leans on.
- **Evidence:** `help("effectsize_CIs")`, section on one-sided CIs: "In order for a CI to yield the same significance decision it must then by a 1-sided CI, estimating only a lower bound." `cramers_v(tab, adjust = FALSE)`: 0.20 [0.12, 1.00]; with `alternative = "two.sided"`: [0.10, 0.27]; with `ci = 0.90`, two-sided: [0.12, 0.26]. Reviewer's two-sided values for the others (R): ω² 0.10 [0.06, 0.15]; partial η² 0.50 [0.46, 0.54]; Kendall's W 0.85 [0.77, 0.94]; ε² 0.001 [0.00, 0.02].
- **Fix:** either report two-sided intervals (`alternative = "two.sided"`), or keep the one-sided ones, give the real reason, and say the interval can't show how large the effect might be. This is a decision for you: it changes Results sentences on three pages.
- **Related (R):** `rank_epsilon_squared()` and `kendalls_w()` bootstrap with 200 replicates by default; the reviewer saw W's lower bound move between 0.776 and 0.782 with the seed, and effectsize's help says of these bootstrapped CIs that they "should not be used for statistical inference".

### A7. Page 13: the CI band does not widen "as patients leave", and the 10-year figure is the 7.9-year figure ✔

- **Where:** p13:282 ("The shaded band is the 95% CI. It widens as patients leave."); p13:337 to 348 (10-year survivorship and "The 10-year CI … is the widest").
- **Problem:** the band changes only when a revision happens. Censoring alone never widens it. The last revision is at 7.9 years, so from then to the end of the plot the curve and the band are frozen while the number at risk falls from 92 to 21 (at 10 years) and on to 2. The CI therefore does not show how thin the data are in the tail, which is the opposite of what the sentence teaches.
- **Evidence:** `summary(km, times = c(7.9, 10))`: survival 0.7803 (0.7246 to 0.8261) at both times; at risk 92 and 21. Latest revision: 7.9 years.
- **Fix:** say the band widens at each revision, more so when few remain at risk; after the last revision neither moves, so here the "10-year" estimate is the 7.9-year estimate carried forward.
- **Related:** B12 (the page's own 10% rule).

### A8. Page 14 calls 1 − Kaplan-Meier "had been revised", which page 13 says never to do ✔

- **Where:** p14:169 against p13:743.
- **Page 14 says:** "By 5 years, 28.9% of implant C knees and hips had been revised (1 − Kaplan-Meier), against 10.1% of implant A: 2.85 times as many".
- **Page 13 says:** "Never call 1 − Kaplan-Meier 'the proportion of patients revised' when many patients died."
- **Evidence:** at 5 years, implant C: 1 − Kaplan-Meier 28.9%, cumulative incidence 27.3%; implant A: 10.1% and 9.7%.
- **Fix:** word it as the Kaplan-Meier estimate of revision risk with deaths censored, or use the cumulative incidences. The point of the paragraph (a hazard ratio is not a risk ratio) survives either way.

### A9. Page 17: "a different ICC for every model" is wrong for the two models the page presents ✔

- **Where:** p17:188; terminology at p17:76 to 79.
- **Page says:** "The same data give a different ICC for every model, type and unit".
- **Problem:** the only model choice the page describes is two-way random against two-way mixed, and those give the same number. Only the interpretation differs. A reader will conclude that a paper's "two-way mixed" ICC would have differed under "two-way random".
- **Evidence:** Koo & Li 2016 (the page's own source; PMC4913118, fetched and quoted by a summarizing tool, so re-read the wording before citing): "ICC estimates of both the 2-way random- and mixed-effects models are the same because they use the same formula". `irr::icc()` has `model = c("oneway", "twoway")`, with no random/mixed option. The page itself says at p17:198 "The calculation is the same as before".
- **Second problem, same lines:** the page cites Koo & Li for "Model, Type, Unit", but Koo & Li use "Type" for single rater against mean of k raters, and call agreement against consistency the "Definition". The page's words are `irr::icc()`'s argument names. A reader who opens the paper finds "Type" meaning something else.
- **Fix:** say the number changes with one-way against two-way, consistency against absolute agreement, and single against average; random against mixed changes only who the result applies to. Use Koo & Li's three words, with irr's argument names in brackets.

### A10. Page 1: letting the software guess types does not silently produce a missing value ✔

- **Where:** p1:168.
- **Page says:** "If you let the software guess types, it silently turns `32.1 kg/m2` into a missing value, and you never find out."
- **Problem:** neither reader taught on the page does that. With guessing on, the text is kept. A missing value appears only when a number type is forced, and readxl then warns.
- **Evidence:** `read_excel(workbook, sheet = "Site A", skip = 3)` with no `col_types` returns BMI as character, with `"33.5 kg/m2"` intact. Reviewer (R): pandas returns an object column mixing floats and strings; forcing `col_types = "numeric"` warns "Expecting numeric in G9 … got '33.5 kg/m2'".
- **Fix:** say that guessing gives columns of mixed or inconsistent type, and that forcing a number type is what loses the value. The advice to read everything as text stays right.

### A11. Page 1: the recodes do not all "turn anything else into a missing value" ✔

- **Where:** p1:427; code at p1:454 to 460 and the Python twin.
- **Page says:** "Each recode lists the values it expects and turns anything else into a missing value, so a surprise like `U` for sex shows up instead of silently becoming 'Male'."
- **Problem:** sex is matched on its first letter, so "Mme" and "Madame" become "Male". The three comorbidity flags turn anything unrecognized into 0, which reads as "no disease", not missing.
- **Evidence:** the page's `case_when` on "Mme", "Madame", "Monsieur", "U", "w" gives Male, Male, Male, NA, NA. `str_detect(c("T2DM", "NIDDM", "diabetes"), "\\bDM\\b")` gives 0, 0, 0. Reviewer (R): an empty comorbidity cell is NA in R but 0 in pandas; an unexpected ASA value is NA with a warning in R but stops the Python code. None of these values occur in the practice workbook, so the page's numbers are unaffected.
- **Why it matters here:** HFR data are French and German. "Mme" is a likely real value.
- **Fix:** say which recodes fail to missing and which default to "no", match sex on whole expected values, and cross-tabulate the comorbidity recodes as check 3 does for sex and ASA.

### A12. Page 1: the 564 blank rows are not all missed visits ✔

- **Where:** p1:643.
- **Page says:** "A missed visit still has its rows, with the response blank (564 rows here)".
- **Evidence:** in `data/answer-keys/survey_items_long.csv`, 72 visits are wholly blank (473 rows). The other 91 blank rows are single unanswered items inside visits that were otherwise answered.
- **Fix:** "564 unanswered rows: 473 from 72 missed visits and 91 single skipped items".

### A13. Page 3's flowchart sends every bounded score to the rank column, against the page's own examples ✔

- **Where:** p3:463 (flowchart label "Strongly skewed, bounded, or ordinal → Rank column"). Same loose use at p2:168 and p7:43.
- **Problem:** every PROM is bounded. Nine lines later the same page sends the EFAS score (0 to 24) to the Gaussian column (p3:472), and p6:37 says a sum score "can be treated as a measurement when few patients sit at its floor or ceiling". The criterion the site actually uses is values piled up at the bound.
- **Fix:** replace "bounded" with "piled up at a floor or ceiling" in the flowchart and at p2:168 and p7:43.

### A14. Page 3: Pearson correlation does not "compare means" ✔

- **Where:** p3:23.
- **Page says:** "The tests in the first column (t tests, ANOVA, Pearson correlation) compare **means**, and they assume the data within each group follow a roughly bell-shaped, normal distribution."
- **Problem:** right for t tests and ANOVA. Pearson correlation measures a straight-line association between two measurements; it compares no means and has no groups.
- **Fix:** "work with means and SDs of the raw values: t tests and ANOVA compare means, Pearson measures a straight-line association".

### A15. Page 17: the ICC is not always "a number from 0 to 1" ✔

- **Where:** p17:29; the page's own exercise 3 (p17:627) reports "95% CI −0.04 to 0.78" with no comment.
- **Fix:** "usually between 0 and 1; an estimate or CI limit below 0 means no reliability".

---

## Urgency 2: misleading statements, contradictions between pages, missing caveats

### 2b. Model Methods and Results sentences that residents will copy

**B1. Page 18's primary analysis silently leaves out every early failure ✔**
- **Where:** p18:373, p18:727 (Methods), exercise 3.
- **Problem:** the page says the 22 missing 1-year scores "are what the abstractor couldn't find". Seven of them belong to patients whose registry follow-up ended before 1 year: 4 were revised (at 0.19, 0.26, 0.45 and 0.81 years), 1 died (0.93) and 2 were censored (0.04 and 0.16). The Methods never say how patients revised or dead before the 1-year score were handled, and "improvement at 1 year" is reported for survivors with an unrevised joint only.
- **Evidence:** join of `data/answer-keys/abstraction_workbook_tidy.csv` with `data/cohort.csv`; cases C0278, C0557, C0078, C0449, C0477, C0068, C0571.
- **Fix:** cross-tabulate "1-year score missing" against "event before 1 year", state the handling in the Methods, give the counts in the Results. The page already joins both sources.

**B2. Two model Results sentences report CIs that the box directly below says can't be trusted ✔ (read) / R (numbers)**
- **Where:** p11:432 to 438 (nonlinear regression on 1,146 scores from 330 knees) and p12:412 to 418 (the multiple version).
- **Problem:** the Methods sentence does not disclose that repeated scores from one knee were treated as independent; the warning box under it says "these CIs can't be trusted". A resident copies the sentence, not the box.
- **Evidence (R):** a cluster bootstrap over knees gives a time constant of 73.7 to 89.0 days against the page's 71.0 to 92.5.
- **Fix:** put the limitation into the model Methods sentence, or fit on one score per knee, or report a CI that respects the clustering.

**B3. Page 18's model Methods would not pass a reporting-guideline check, and the site never mentions one ✔ (search) / E**
- **Evidence:** "STROBE", "CONSORT", "EQUATOR" and "reporting guideline" appear nowhere in `en/` (searched).
- **Missing from the model Methods (p18:723 to 727), none flagged as omitted:** the design in words (retrospective or prospective cohort); how the 120 were selected and the inclusion and exclusion criteria; one joint per patient (the code checks it at p18:323, the text doesn't state it); the assessment windows (only a code comment at p18:313); an ethics approval and consent statement; a sample-size justification; missing data named as complete-case with its assumption; that the analysis was prespecified; the registry's completeness; an MCID against which to read 9 points.
- **Fix:** add the sentences (they can be invented for the synthetic study), or add a box "what a real Methods also needs" with a link to STROBE.

**B4. Page 18 finds a large baseline imbalance and then reports only the unadjusted result ✔ (read) / R (numbers)**
- **Where:** p18:433 ("71.7% of the THA patients were women against 49.3% of the TKA patients (SMD 0.47)"); the Discussion list at p18:714 omits case mix.
- **Evidence (R):** adjusting for sex gives −9.26 (95% CI −14.99 to −3.54); adding the pre-op score gives −7.35 (−12.02 to −2.68). The result holds.
- **Fix:** add baseline differences to the Discussion list and show or mention the adjusted estimate.

**B5. Smaller points in model sentences**
- p4:749 (R): the Kaplan-Meier Methods sentence omits the CI type, although the code sets `conf.type = "log-log"` and the 🔀 box says "say which you used". Page 13's Methods names it. The median's Methods sentence (p4:393) names no CI method either.
- p13:397 to 401 ✔: "Median follow-up was estimated with the reverse Kaplan-Meier method" does not say deaths were censored like revisions. The choice moves the answer: 5.62 years, against 5.00 if death ends observation.
- p16:363 and p16:564 (R): "95% CIs and Holm-adjusted p-values" pairs unadjusted CIs with adjusted p-values without saying so. Page 15 teaches that Tukey's CIs "are adjusted too". Page 15:658 does the same with hazard ratios.
- p18:727 ✔: "Analyses used R 4.6 and Python 3.13." A manuscript names the one program that produced the quoted numbers, with its main packages.
- p8:219 (R): the model sentence for a four-group ANOVA reports two of the four group means.
- p3:529 (R): the Results-style sentence on the core page uses "higher", which the site's own convention bans. It escapes the test because it has no `**Results:**` label.
- p4:655, p4:751 (E): "Revision-free survival" with deaths censored is implant survivorship. In general usage "X-free survival" counts death as an event. Page 13 says "Survivorship free of revision".

### 2c. Pages that contradict each other

| ID | Topic | One page says | Another says | Check |
|---|---|---|---|---|
| C1 | Welch or classic | p6:229: don't choose by looking at the spreads, "Use Welch's test from the start" | p8:37 and p15:214: use classic ANOVA unless the largest SD is more than about twice the smallest. Page 15 then follows page 8's classic ANOVA with Welch pairwise t tests. | ✔ read |
| C2 | Signed-rank test and skew | p5:232: it tests the pseudomedian, equal to the median only for a symmetric distribution | p7:43: "If the differences are skewed … → the Wilcoxon signed-rank test", with no symmetry caveat. Page 5 itself recommends the test for skewed outcomes (p5:229). See B6. | ✔ read |
| C3 | Events per variable | p12:435, 559: 10 per **predictor** | p14:215: 10 per **term** (coefficient), worded as "needs" | ✔ read |
| C4 | Covariates' own coefficients | p14: a warning box titled "the covariates' own hazard ratios aren't findings" | p12:189, 527, 555: the linear and logistic Results report every covariate's coefficient as a finding | R |
| C5 | Adjustment in balanced groups | p12:652: the groups are alike, "so adjustment shouldn't change much" | p14:259: a hazard ratio shifts when a strong predictor is added, even without confounding. Page 12's own shift (3.07 to 3.19) is this. | ✔ read |
| C6 | Time points | p13:546: "decide your time points before you look" | p13:468: 6 months is picked after "But look at the plot…" and goes into the Results. Page 14 gives the clinical reason page 13 lacks. | R |
| C7 | Where to stop the curve | p13:287: stop once fewer than about 10% (here 60) remain at risk | p13:344 and both plots: 10-year survivorship reported with 21 at risk (3.5%) | ✔ |
| C8 | Mantel-Haenszel | p6:720, p13:405, Tests A–Z: "the same test" as log-rank | glossary `#log-rank-test`: "nearly identical". Reviewer (R): in R the two give the identical statistic (20.5346) on the cohort. | ✔ read |
| C9 | Student's t test | glossary `#t-test`: the t test is "also called Student's t test" | glossary `#equal-variances`, Tests A–Z, p6: Student's is the equal-variance version only | R |
| C10 | Death and censoring | glossary `#censored`: lists "the patient died" as an ordinary reason for censoring | glossary `#competing-risk`: censoring deaths makes 1 − Kaplan-Meier overstate the event | R |
| C11 | Table 1 content | p2:28: Table 1 holds characteristics measured before surgery | p2:41: length of stay, an outcome, is in every Table 1 and its SMD is read as baseline imbalance (p2:293) | ✔ read |
| C12 | Normality with pairs | p3:234: the assumption is about the data "within each group" | p7:41: "about the differences, not about each measurement". p7:917 (exercise) then justifies the paired t test by the measurements. | R |
| C13 | Missed visits | p15:397 to 414 keeps only the 328 procedures seen at all four visits | p16 argues this is wasteful and can be biased; page 15 has no pointer to it | R |
| C14 | ASA class | p3:402: ordinal data "always go in the rank column" | p2: tests ASA with the chi-square test as unordered categories | R |

### 2d. Caveats a resident needs for critical reading, missing or understated

**B6. The signed-rank test's symmetry assumption (E, R).** `help(wilcox.test)` states the null as the distribution being "symmetric about mu" ✔. Reviewer's simulation (R): resampling the page's 260 KOOS scores and testing against the true median, the signed-rank test rejects 36% of the time at n = 260; the sign test rejects 4%. Pages 5 and 7 route skewed data to this test and offer the sign test only for ordinal scales. Fix: name symmetry as the assumption; offer the sign test when the claim is about the median.

**B7. Odds ratio against risk ratio on page 6 ✔.** Page 6 never mentions the risk ratio. Its exercise 3 has a common outcome (return to sport 53.3% against 46.5%) and reports "odds ratio 1.31"; the risk ratio is 1.15. The glossary entry for odds ratio doesn't warn either; the warning sits only under `#risk-ratio`. Fix: one sentence on page 6, shown on exercise 3, and one in the glossary entry.

**B8. "p > 0.05" is not "no difference", and p is not the chance of no difference (R, E).** Page 3's "two classic misreadings" box covers the first for p = 0.20 but the glossary entries for p-value and statistical significance don't, and there is no entry for type II error, false negative, alpha or beta. The misreading "p is the probability that there is no difference" is absent from page 3's box (the glossary has it). p3:169 ("A small p-value means 'probably not'") leans the wrong way.

**B9. What to adjust for (R, E).** Page 12, which defines "adjusted", never says which variables to adjust for. "Confounder" doesn't appear on it; "mediator", "collider", "overfit", "collinear" and "VIF" appear nowhere in `en/` ✔ (searched); "interaction" appears only on page 16 and in the glossary ✔. Page 14 `#choosing-covariates` has the guidance, and page 12 doesn't link to it.

**B10. Matched cohorts: "the wrong model" overstates (E; numbers ✔ on the page).** p7:775 and a code comment call an unstratified Cox model on matched patients wrong. That rule comes from matched case-control studies. In a matched cohort an unstratified model with a cluster-robust standard error is an accepted analysis; the reviewer cites Sjölander & Greenland, Statistics in Medicine 2013 (not opened). p3:440 "Treat matched sets like pairs" has the same over-reach for frequency matching and propensity-score matching.

**B11. Kappa depends on prevalence (E).** "Prevalence" appears nowhere in `en/` ✔. With one dominant category raters can agree on 95% of cases and get a low kappa, so kappas can't be compared across studies with different case mixes. The Landis and Koch labels are given without this.

**B12. Reading the tail of a survival curve (✔).** See A7 and C7. Also (R): the R plots' y-axis runs 0 to 100% and the Python plots' from about 0.72 to 1.00 on pages 4, 8 and 13, so the same curve looks flat in one tab and steep in the other, with no comment. A truncated survival axis is itself something a critical reader should learn to spot.

**B13. Correlation depends on the range sampled (R, E).** Not mentioned on page 10. Reviewer: all 80 hips give r = 0.86; the 30 hips with CT between 10° and 20° give r = 0.53, with the same measurement error. Also p10:181 and p7:910 show a trend by grouping the difference on one method's own value, which Bland and Altman (Lancet 1995) warn exaggerates it; page 17 plots against the mean, the right way.

**B14. Confidence interval for the line against prediction interval for one patient (R).** Page 11 promises regression "lets you predict the outcome for a new patient" but shows neither. "Prediction interval" appears nowhere in `en/` ✔. p11:226 says patients "scatter around it by about 15 minutes either way": that is one SD, covering about two-thirds of patients.

**B15. Residuals, not the outcome (E).** p11:453 says an outcome that isn't normal means "the residuals of a straight line won't be normal". Linear regression assumes normal residuals, as p11:37 correctly says; a skewed outcome can have well-behaved residuals. Page 11 asks the reader to check residual normality but shows only the residual-against-fitted plot (R); page 12 fits four models with no diagnostic (R); page 16 lists no assumptions and shows no residual check (R).

**B16. Missing at random (E).** p16:90: "missing depends on things you measured". The protection holds only for measured things the model includes. Random slopes are never mentioned on the site ✔ (searched), though time-as-a-number models usually need one.

**B17. Period-specific hazard ratios (E).** p14:548 reports a hazard ratio of 0.43 after 6 months as merely "imprecise". It compares only the hips that survived the first 6 months, which are no longer like-for-like groups (reviewer cites Hernán, Epidemiology 2010, not opened). The generator's true late ratio is 1 (R). "Restricted mean survival time" as an alternative when hazards aren't proportional appears nowhere ✔.

**B18. Bilateral joints (R).** p14:625 says pairing matters little because "only 20 of the 80 bilateral patients had a revision". The real reason is that the generator draws each joint's revision time independently. p14:562 says ignoring pairing makes CIs "too narrow", yet the robust standard errors printed are slightly smaller. Also (R): pages 2 and 3 warn about counting bilateral patients twice, then compute every p-value on all 600 rows; for sex the p-value is 0.0002 on rows and 0.002 on the 520 patients.

**B19. Multiple comparisons (R, E).** Page 15 only ever adjusts the p-value; papers very often adjust the threshold instead ("significance was set at 0.05/6"), and only the glossary says the two are the same. The same comparison (age, ASA 1 against 2) is p = 0.044 with Holm in one section and p = 0.096 with Tukey in the next, without comment, right under the warning about choosing the method after seeing the results. Dunnett's test (each group against a control) is absent while "Dunnett's T3" is named.

**B20. Agreement (E).** Standard error of measurement and minimal detectable change appear nowhere ✔; orthopaedic reliability papers report them routinely. p17:241: the limits of agreement cover 95% of differences only if the differences are roughly normal; the assumption isn't stated.

**B21. Complete cases on page 9 (R).** The page's `filter()` step is what makes every function agree. On unfiltered data base R's `aov(... + Error())`, which the page uses for the effect size, drops nobody and returns a different F (467.5 against 326.1) with only a "model is singular" warning. The page doesn't say the filter is what protects the reader.

**B22. Page 1 on Swiss data (✔).** `parse_number("31,2")` returns 312, and the Python helper returns 31. Neither warns. A reader who copies the helpers onto a sheet with decimal commas gets wrong numbers, and R and Python disagree. Two-digit years: `dmy("13.01.45")` returns 2045, which is wrong for a date of birth. Fix: a ⚠️ box saying the helpers assume a decimal point, with `locale(decimal_mark = ",")`.

**B23. Table 1 (R, E).** Page 2's list of who should report p-values leaves out randomized trials, where a baseline p-value is uninformative by construction (CONSORT). Its sex example (p < 0.001, "pure chance", "chance differences turn up") is a fluke of roughly 1 in several hundred, partly produced by counting bilateral patients twice. The 0.1 SMD threshold is presented without saying that with a few hundred patients and multi-category variables, chance alone gives 0.1 to 0.15 (reviewer's shuffle: ASA class exceeds 0.1 in 67% of random splits). The page never says how an SMD is computed for a category.

**B24. Rules of thumb stated as requirements (E).** "Every expected count should be at least 5" (p8:465, p10:437) is the strict version; Cochran's usual rule for larger tables allows up to 20% of cells below 5. Exercise 3 on page 8 calls a chi-square test "not reliable" on a table that meets Cochran's rule (chi-square p = 0.949, exact 0.943). "A Cox model needs about 10 events per term" (p14:215) is contested; it is a rough upper limit, not a requirement.

**B25. Glossary (R).** `#risk` defines risk as events divided by patients at the start, which holds only with complete follow-up. `#mcid` moves from one patient's change to a difference between group means without saying an MCID doesn't transfer automatically. `#score-test`: "equivalent to the log-rank test" is exact only without tied event times (page 8 says "agree to one decimal").

---

## Urgency 4: small points

- p5:446 (R): the box says "scipy doesn't" apply a continuity correction, but the page calls `pg.wilcoxon()`, and pingouin turns it on by default. `method="approx"` is no longer scipy's documented name (`"asymptotic"`).
- p5:334 (R): pingouin's output shows `CLES NaN`, unexplained. A beginner will think something failed.
- p5:767 (E): "It excludes 0, which matches the p-value below 0.05" reads as if the two always match.
- p6:195 (R): `hedges_g()` prints "Estimated using pooled SD" right after the section said to use Welch because it doesn't pool. One sentence would settle it.
- p6:648 (E): the Wald CI for a risk difference is paired with Fisher's test on 6 events per arm without a caveat.
- p6:880 (R): the lifelines fit lacks `fit_options={"precision": 1e-9}`, unlike pages 7 and 8; R and Python print 3.039405 and 3.039403, just inside the agreement tolerance.
- p7:327 (R): the signed-rank example has 246 pairs with symmetric changes, which by the page's own rule is a paired t test case.
- p7:569 (R): the discordant-pair odds ratio isn't explained as a within-patient odds, and the paired risk difference (24.4 points) is omitted.
- p8:410 (R): ε² is the rank counterpart of η², not ω².
- p8:446 (R): medians 4, 5 and 5 with p = 0.713 and no "it isn't a test of medians" note (page 6 has that box).
- p9:298 (R): the 6-month visit is left out without saying so.
- p9:752 (R): the page never prints how many matched sets contain a revision (23 of 52), which is the effective sample size.
- p10:392 (R): "Fisher's z: makes the CI symmetric" (it is symmetric on the z scale only; the printed CI is lopsided).
- p11:757, p11:988 (R): the likelihood-ratio test "says the same as the z test", but the printed p-values differ (0.00016 and 0.00041).
- p11:985 (E): "1.27 times higher" can be read as 127% higher; p11:993 uses the unambiguous "times the hazard".
- p11:258 to 357 (R): the fitted recovery curve is never drawn over the data.
- p13:253 (R): see B12 (Python y-axis).
- p14:368 (R): R's Schoenfeld plot has three dashed lines; the text explains one.
- p17:165 (R): "The first three lines of the code are the mean squares": they are lines 3, 4 and 6.
- p17:412 (E): quadratic weights for kappa are named only as a software option; papers often don't say which they used.
- p3:53 to 115 (R): the age histogram is a comb of spikes (bin width 1.59 on whole years) and the age QQ plot flattens at 85, the dataset's cap, while the text calls it "a textbook bell curve".
- p3:344 (R): the practical guide covers "30 or more" and "under about 15" per group and says nothing for 15 to 30.
- p3:396 (E): leaves the impression that log analyses are uninterpretable; a plain log difference back-transforms to a ratio.
- p3:484: the section that defines the CI never says what "95%" refers to; the glossary does.
- Tests A–Z (R): the English table is sorted by first word, so nothing sits under A for ANOVA, T for t test, L for logistic regression. Methods the site uses have no row: Welch's ANOVA, sign test, Mauchly and Greenhouse-Geisser, Levene's test, odds ratio, risk ratio, Schoenfeld residuals. "Aalen-Johansen estimator: same as the cumulative incidence" confuses the method with what it estimates.
- Decision table (E): "Log-rank (Mantel-Haenszel)" collides with the stratified 2 × 2 test of the same name that residents meet more often; "Mantel-Cox" would avoid it.

## Claims no reviewer could verify

These are statements on the pages that were not confirmed. They are not known to be wrong.

- p11:636: "deming 1.4-1 misapplies its tie correction; mblm's CI is far too narrow". Neither package is in the project library, so the claim wasn't tested. It names two packages as wrong in public.
- p13:287: the source of the "10% at risk" rule. The reviewer recalls Pocock, Clayton & Altman, Lancet 2002, as 10 to 20%, unopened.
- p15:214: GraphPad's recommendation of Dunnett's T3 below 50 per group (the URLs the reviewer tried returned 404).
- p2: "In real arthroplasty cohorts, TKA patients are usually more often female" (a clinical claim with no source on the page).
- p3: the ±0.5 and ±1 skewness cut-offs as "a widely used convention" (already noted in the previous audit as unsourced).
- p13:749, p14:637: "Python has no mature implementation" of Gray's test and Fine-Gray regression.
- p4:404: the SPSS and SAS quartile definitions.
- Whether the decision table matches Motulsky's table cell by cell (the book wasn't opened).
- No glossary definition was compared with its cited source.
