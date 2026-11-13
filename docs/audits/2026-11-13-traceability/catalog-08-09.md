# Audit findings: catalog pages 8 and 9

Checked against the frozen output in `_freeze/en/catalog/<page>/execute-results/html.json` (dumped to `work-catalog-08-09/08.md` and `09.md`). Every number below was re-computed read-only from `data/`. The proposed code lines were run once against `data/` and give the values quoted; they were not rendered inside the pages.

## 08-three-plus-unmatched.qmd

### 08-1 · Welch's ANOVA result appears from nowhere · A
- **Where:** `en/catalog/08-three-plus-unmatched.qmd:173`, section `#one-way-anova`, 🔀 box "R vs Python: classic or Welch's ANOVA"
- **Text:** "Here the SDs are similar, and Welch's ANOVA agrees: F = 23.5, p < 0.001."
- **Problem:** No visible chunk runs Welch's ANOVA. The box names the functions, but the reader never sees them run or their output.
- **Where it really comes from:** hidden chunks at lines 176 to 186 (`pg.welch_anova(...)`, `oneway.test(age ~ asa, data = cohort)`); guard line 620.
- **Proposed fix:** Make the two calls visible in a language tabset inside the box, before the third bullet (the hidden pair can keep doing the agreement check):
  - R: `oneway.test(age ~ asa, data = cohort)   # Welch's ANOVA: doesn't assume equal spreads` (prints `F = 23.455, num df = 3.000, denom df = 60.311, p-value = 3.49e-10`)
  - Python: `print(pg.welch_anova(data=cohort, dv="age", between="asa"))   # Welch's ANOVA: doesn't assume equal spreads` (prints `F 23.454811`, `p_unc 3.489598e-10`)
  - Bullet: "Here the SDs are similar, and Welch's ANOVA agrees: F = 23.5 (classic: 23.9), p < 0.001 (R prints `3.49e-10`)."
- **Changes code:** yes

### 08-2 · Bias-corrected Cramér's V "0.24 here" is never printed · A
- **Where:** `en/catalog/08-three-plus-unmatched.qmd:450`, section `#chi-square`, 🔀 box "R vs Python: two versions of Cramér's V"
- **Text:** "effectsize's `cramers_v()` applies a small-sample **bias correction** by default (0.24 here). scipy's `association()` doesn't (0.25)."
- **Problem:** The page only ever runs `cramers_v(rts_table, adjust = FALSE)`, which prints 0.25. The 0.24 is not in any output.
- **Where it really comes from:** Prose guard line 631 (`effectsize::cramers_v(rts_table)$Cramers_v`).
- **Proposed fix:** Add one line to the R tab of "Effect size and 95% CI", after the existing call: `effectsize::cramers_v(rts_table)   # the default, with the bias correction: a little smaller`. It prints `Cramer's V (adj.) 0.24 [0.14, 1.00]`. Then write in the box "(0.24 here, the second R output, headed `Cramer's V (adj.)`)". scipy has no bias-corrected version, so there is no Python line to add; the box already says so. Prose-only alternative: drop "(0.24 here)" and write "which gives a slightly smaller V".
- **Changes code:** yes (R tab only); no for the alternative

### 08-3 · lifelines' default hazard ratio 0.81713 is never printed · A
- **Where:** `en/catalog/08-three-plus-unmatched.qmd:581`, section `#cox`, 🔀 box "R vs Python: convergence and the reference group"
- **Text:** "lifelines' default convergence rule stops a little early here (a hazard ratio of 0.81713 for implant B instead of 0.81709)"
- **Problem:** The visible Python fit already uses the tightened rule and prints 0.817091; R prints 0.8171. The default-rule value 0.81713 appears in no output, and R's 0.81709 is not visible at five decimals either.
- **Where it really comes from:** Prose guard lines 640 to 641 (a `py_eval()` refit without `fit_options`, and `implant_hr["implantB", "exp(coef)"]`).
- **Proposed fix:** Either show it, in the Python tab of "Run it" after the existing lines:
  ```python
  default_cox = CoxPHFitter().fit(
      cohort[["followup_years", "revised", "implant"]],
      duration_col="followup_years", event_col="revised", formula="implant",   # no fit_options: lifelines' default rule
  )
  print(default_cox.hazard_ratios_)   # implant B: 0.817125 instead of 0.817091
  ```
  and in the R tab `exp(coef(implant_cox))   # the hazard ratios to more decimals` (prints `0.8170908 3.0673441`), then write "(0.817125 for implant B with the default rule, 0.817091 once tightened, which is R's 0.8170908)". Or, prose only: remove the two numbers and write "stops a little early here: without `fit_options`, implant B's hazard ratio differs from R's in the fifth decimal".
- **Changes code:** yes; no for the alternative

### 08-4 · "roughly a one-in-four chance" has no calculation · A
- **Where:** `en/catalog/08-three-plus-unmatched.qmd:586`, section `#which-groups-differ`
- **Text:** "with four ASA classes there are six pairs, and six tests at p < 0.05 give roughly a one-in-four chance of at least one false alarm even when nothing is going on."
- **Problem:** Neither the six pairs nor the one-in-four is derived; a beginner cannot reconstruct 1 − 0.95⁶.
- **Where it really comes from:** Prose guard line 642 (`choose(4, 2) == 6`, `round(1 - 0.95^6, 2) == 0.26`). Page 15, `#why-adjust`, shows the calculation in visible code.
- **Proposed fix:** "with four ASA classes there are six pairs (1 vs 2, 1 vs 3, 1 vs 4, 2 vs 3, 2 vs 4, 3 vs 4). Each test at the 5% level has a 95% chance of *not* raising a false alarm, so six independent tests all stay quiet with probability 0.95⁶ = 0.74. That leaves 1 − 0.74 = 0.26, roughly a one-in-four chance of at least one false alarm even when nothing is going on ([page 15](../beyond/15-post-hoc.qmd#why-adjust) works this out in code)."
- **Changes code:** no

### 08-5 · "502 of the 600 procedures" and "missing for 98" need unstated sums · B
- **Where:** `en/catalog/08-three-plus-unmatched.qmd:234`, `:309`, `:313`, section `#kruskal-wallis`, steps "Look at the data first", "How to report it" and the ⚠️ box
- **Text:** "Satisfaction was reported for 502 of the 600 procedures." / "Of 600 procedures, 502 had a satisfaction score at 1 year." / "Satisfaction is missing for 98 procedures."
- **Problem:** The output shows n = 192, 177 and 133 per surgeon. 502 is their sum, never stated; 600 is not printed anywhere in this section; 98 is 600 − 502, never stated.
- **Where it really comes from:** Prose guard lines 603 and 621 (`satisfied_n`, `sum(is.na(cohort$satisfaction_1yr)) == 98`).
- **Proposed fix:** Add one visible line after `satisfied` is made:
  - R: `c(all = nrow(cohort), answered = nrow(satisfied))   # all procedures, and those with a score`
  - Python: `print(len(cohort), len(satisfied))   # all procedures, and those with a score`
  
  Both print 600 and 502. In the ⚠️ box write "Satisfaction is missing for 98 procedures (600 − 502)." Prose-only alternative: "502 of the 600 procedures (192 + 177 + 133, the `n` / `count` column)", which still leaves 600 unshown.
- **Changes code:** yes; no for the alternative

### 08-6 · Row totals 129, 154 and 67 in the Results are not in the output · B
- **Where:** `en/catalog/08-three-plus-unmatched.qmd:441` (and the percentages at `:367`), section `#chi-square`
- **Text:** "84 of 129 BPTB reconstructions (65.1%), 67 of 154 hamstring reconstructions (43.5%) and 22 of 67 quadriceps reconstructions (32.8%)"
- **Problem:** The table prints yes/no counts (84 and 45, and so on) but no row totals; the reader has to add them. The second table prints proportions (0.6511628) under a comment that says "row percentages".
- **Where it really comes from:** Prose guard line 626 (`rowSums(rts_table) == c(129, 154, 67)`).
- **Proposed fix:** Prose only, at line 367: "Each row adds up to that graft's total: 84 + 45 = 129 BPTB, 67 + 87 = 154 hamstring and 22 + 45 = 67 quadriceps reconstructions. The second table divides each count by its row total: 84 / 129 = 0.651, so 65.1% of the BPTB reconstructions, 43.5% of the hamstring and 32.8% of the quadriceps reconstructions were back at their sport." Code alternative: `addmargins(rts_table, margin = 2)   # adds each graft's total` and `pd.crosstab(acl["graft"], acl["rts_12mo"], margins=True)`.
- **Changes code:** no; yes for the alternative

### 08-7 · Exercise 3: the percentages 4.7%, 3.9%, 4.5% and the totals are never computed · B
- **Where:** `en/catalog/08-three-plus-unmatched.qmd:764`, section `#exercises`, Solution 3
- **Text:** "6 of 129 BPTB reconstructions (4.7%), 6 of 154 hamstring reconstructions (3.9%) and 3 of 67 quadriceps reconstructions (4.5%)"
- **Problem:** The solution prints only the counts (6 and 123, and so on). Unlike the main section, it has no row-percentage line, so the reader has to add each row and divide.
- **Where it really comes from:** Prose guard lines 653 to 654 (`ex_failure`, `prop.table(ex_failure, 1)`).
- **Proposed fix:** Add to the solution, after the table is printed, the same line the main section uses:
  - R: `prop.table(failure_table, margin = 1)   # row percentages: failures with each graft` (prints 0.0465, 0.0390, 0.0448 in the `yes` column)
  - Python: `print(pd.crosstab(acl["graft"], acl["failure_2y"], normalize="index"))   # row percentages`
  
  and one sentence: "Each row adds up to the graft's total (6 + 123 = 129)."
- **Changes code:** yes

### 08-8 · F = 23.9 is not tied to the Mean Sq column; Python's column names and `np2` are unexplained · B
- **Where:** `en/catalog/08-three-plus-unmatched.qmd:118` to `:121`, section `#one-way-anova`, step "Read the output"
- **Text:** "**F = 23.9:** the between-group variation divided by the within-group variation, each per degree of freedom." / "**Df = 596** (600 procedures minus four groups)"
- **Problem:** "Each per degree of freedom" is the Mean Sq column (1908.9 and 79.9), which is printed but never named, so the reader cannot see that F is one printed number divided by another. The bullets use R's names only; Python prints `SS`, `DF`, `MS`, `p_unc` and `np2` (0.107), and `np2` is never explained although the next step quotes a different effect size (ω² = 0.10). 600 is not printed; it is the sum of the `n` column.
- **Where it really comes from:** output lines `asa 3 5727 1908.9 23.9 1.28e-14` and `Residuals 596 47599 79.9`; Python `MS 1908.897669` and `79.864206`, `np2 0.107391`.
- **Proposed fix:** Reword the bullets:
  - "**asa row** … **Df = 3** (four groups minus one), **Sum Sq = 5727** (`DF` and `SS` in Python)."
  - "**Residuals** … **Df = 596** (600 procedures, the sum of the `n` column above, minus four groups)."
  - "**Mean Sq** (`MS` in Python): each Sum Sq divided by its Df, 5727 / 3 = 1908.9 between groups and 47599 / 596 = 79.9 within."
  - "**F = 23.9:** the two Mean Sq divided, 1908.9 / 79.9. If the groups had the same mean, F would be close to 1."
  - "**p < 0.001** (R prints `1.28e-14` under `Pr(>F)`, Python under `p_unc`) …"
  - "**np2 = 0.107** (Python only): eta squared, the effect size the next step corrects."
- **Changes code:** no

### 08-9 · ε² = 0.001 is printed by R as `1.35e-03` · B
- **Where:** `en/catalog/08-three-plus-unmatched.qmd:303` (also `:309`, and Solution 2 at `:721`), section `#kruskal-wallis`, step "Effect size and 95% CI"
- **Text:** "ε² = 0.001: surgeon accounts for essentially none of the variation in satisfaction."
- **Problem:** R prints `1.35e-03`, Python `0.0013510047427243259`. A beginner who cannot read `e-03` cannot match the R output to 0.001. The step says ε² "is H divided by (n − 1)" but never puts the numbers in.
- **Where it really comes from:** output line `1.35e-03 | [0.00, 1.00]`; Python `0.00135…`.
- **Proposed fix:** "ε² = 0.001 (R prints `1.35e-03`, its shorthand for 0.00135; Python prints 0.00135): H divided by n − 1 is 0.677 / 501. Surgeon accounts for essentially none of the variation in satisfaction." In Solution 2 add "(R prints `1.22e-03`)".
- **Changes code:** no

### 08-10 · Cox overall test: Python prints neither df nor p, and "the second number" is ambiguous · B
- **Where:** `en/catalog/08-three-plus-unmatched.qmd:561` (code at `:531`, Results at `:572`), section `#cox`, step "Read the output"
- **Text:** "**Likelihood ratio test = 27.6 on 2 df, p < 0.001:** … Python prints it as the second number."
- **Problem:** Python prints a table and then two bare numbers (27.635… and 33.468…). The likelihood ratio statistic is the first of the bare numbers, so "second number" misleads; its df and p-value, both quoted in the Results, appear in R's output only.
- **Where it really comes from:** R line `Likelihood ratio test= 27.64 on 2 df, p=1e-06`; Python line `27.63546691821921`.
- **Proposed fix:** Replace line 531 with
  ```python
  overall = implant_cox.log_likelihood_ratio_test()                         # overall test, all implants
  print(overall.test_statistic, overall.degrees_freedom, overall.p_value)   # chi-square, df, p
  ```
  (prints `27.635… 2 9.98e-07`) and reword: "Python prints it on the line under the table: the statistic, its df and the p-value." For the next bullet: "which Python prints on its last line (33.47; R's score test gives 33.48)".
- **Changes code:** yes (Python tab only). Prose-only minimum: "Python prints the statistic alone, on the first line under the table; its df and p-value are in R's output."

### 08-11 · Chi-square: Python prints three unlabeled numbers, and its percentage table flips the columns · B
- **Where:** `en/catalog/08-three-plus-unmatched.qmd:403` to `:404` (code at `:363` and `:385`), section `#chi-square`, step "Read the output"
- **Text:** "**X-squared = 22.24, df = 2:**" / "**p < 0.001:**"
- **Problem:** The bullets use R's labels. Python prints `22.24081329671966 2 1.4807057268816834e-05` with no labels, and the prose never says which number is which or that `1.48e-05` is the p-value (the ANOVA section does say "R prints `1.28e-14`"). Also, Python's first table puts "yes" first (the code comment says so), but its row-percentage table at line 363 prints column 0 first, so the first number a Python reader sees for BPTB is 0.349, not the 65.1% the prose quotes.
- **Where it really comes from:** the outputs named above.
- **Proposed fix:** Prose: "**X-squared = 22.24, df = 2** (the first two numbers on Python's last line)" and "**p < 0.001** (R prints `p-value = 1.481e-05`; it is Python's third number)". Code, Python tab, line 363: `print(rts_table.div(rts_table.sum(axis=1), axis=0))   # row percentages: each count divided by its row total`, which keeps "yes" first (checked: 0.651163, 0.435065, 0.328358 in column `1`).
- **Changes code:** no for the prose; yes for the column order

### 08-12 · "9,999 random tables" is a scipy default the code never shows · B
- **Where:** `en/catalog/08-three-plus-unmatched.qmd:762`, section `#exercises`, Solution 3
- **Text:** "scipy estimates it from 9,999 random tables (0.9405 with this seed)"
- **Problem:** Nothing in the code or output says 9,999.
- **Where it really comes from:** the default `n_resamples=9999` of `stats.PermutationMethod`.
- **Proposed fix:** "scipy estimates it from 9,999 random tables (the default of `PermutationMethod`; 0.9405 with this seed)".
- **Changes code:** no

### 08-13 · "the 80 patients who had both sides operated on" is stated, never shown · B
- **Where:** `en/catalog/08-three-plus-unmatched.qmd:26`, 💡 box "How every section on this page works" (the same sentence opens pages 4 to 12 and page 15; page 9 is `09-13` below)
- **Text:** "the joint replacement examples use every case, including the 80 patients who had both sides operated on."
- **Problem:** No output on this page shows 80. The link goes to page 3 `#paired`, which also only states it; page 2 states "600 procedures come from 520 patients".
- **Where it really comes from:** Prose guard line 612 (`sum(table(cohort$patient_id) == 2) == 80`).
- **Proposed fix:** Decide once for all pages that carry this sentence. Cheapest: show the count once in visible code where it is first taught (page 2's ⚠️ box or page 3 `#paired`): R `cohort |> count(patient_id, name = "procedures") |> count(procedures)   # 440 patients have one procedure, 80 have two`, Python `print(cohort["patient_id"].value_counts().value_counts())`, and let the boxes link there.
- **Changes code:** yes, on another page; none on this page

### 08-14 · R's `e` notation is used six times and never explained · C
- **Where:** `en/catalog/08-three-plus-unmatched.qmd:121` (first use), every section
- **Text:** "**p < 0.001** (R prints `1.28e-14`)"
- **Problem:** The outputs show `1.28e-14`, `1.284107e-14`, `1.35e-03`, `1.481e-05`, `1.39e-05`, `p=1e-06`, `<2e-16`. A beginner has to guess that `e-14` means "move the decimal point 14 places to the left". A pattern search of `en/` found no page that explains it.
- **Where it really comes from:** printed output.
- **Proposed fix:** At the first use in each section (sections stand alone), one clause: "(R prints `1.28e-14`, shorthand for 1.28 × 10⁻¹⁴: thirteen zeros after the decimal point, then 128)". Or explain it once on page 0.2 and link.
- **Changes code:** no

### 08-15 · Half of R's Cox printout is never mentioned · C
- **Where:** `en/catalog/08-three-plus-unmatched.qmd:556` to `:562`, section `#cox`, step "Read the output"
- **Text:** the five bullets
- **Problem:** `summary(implant_cox)` also prints `n= 600, number of events= 81`, `coef`, `se(coef)`, `z`, `exp(-coef)`, `Concordance= 0.659` and a `Wald test`. None is explained, and the number of revisions (81) is the figure the page 9 ⚠️ box says a Cox model depends on.
- **Where it really comes from:** printed output; page 14 `#hazard-ratio` explains each line.
- **Proposed fix:** Add a first bullet "**n = 600, number of events = 81:** 600 procedures, 81 revisions." and a last one "**The rest** (`coef`, `se(coef)`, `z`, `exp(-coef)`, Concordance, Wald test): explained on [page 14](../survival/14-cox-regression.qmd#hazard-ratio); you don't need them here."
- **Changes code:** no

### 08-16 · Two Results sentences leave out the group figures the page asks for · C
- **Where:** `en/catalog/08-three-plus-unmatched.qmd:309` and `:313` (`#kruskal-wallis`); `:721` (Solution 2)
- **Text:** "Always report how many answered in each group" / "Across the three surgeons, Kruskal-Wallis H = 0.73 (df = 2, p = 0.694; …)"
- **Problem:** The ⚠️ box tells the reader to report how many answered per group, but the section's own Results give only the overall 502 of 600, and no output shows each surgeon's total. Solution 2 reports a test with no data at all: it never looks at length of stay per surgeon, although the question asks "what do you find?".
- **Where it really comes from:** not computed on the page. Read-only check: 192 of 232 (S1), 177 of 211 (S2), 133 of 157 (S3) answered; median length of stay 0 days (IQR 0 to 1) for S1, 1 (IQR 0 to 1) for S2, 0 (IQR 0 to 1) for S3.
- **Proposed fix:** Main section: add `cohort |> group_by(surgeon) |> summarise(procedures = n(), answered = sum(!is.na(satisfaction_1yr)))` and `print(cohort.groupby("surgeon")["satisfaction_1yr"].agg(["size", "count"]))   # procedures, answered`, and start the Results "A satisfaction score at 1 year was available for 192 of 232 procedures by surgeon S1, 177 of 211 by S2 and 133 of 157 by S3." Solution 2: add the section's median/quartile summary for `los_days` in both languages and start the Results "Median length of stay was 0 days (IQR 0 to 1) for surgeon S1, 1 day (IQR 0 to 1) for S2 and 0 days (IQR 0 to 1) for S3 (Kruskal-Wallis H = 0.73, …)".
- **Changes code:** yes

## 09-three-plus-matched.qmd

### 09-1 · The "patients" counted on this page are procedures · ERROR
- **Where:** `en/catalog/09-three-plus-matched.qmd:31`, `:104`, `:149`, `:180`, `:184` (`#repeated-measures-anova`); `:403`, `:482` (`#cochran-q`); `:805`, `:807` (Solution 3); code comments at `:63`, `:67`, `:90`, `:92`, `:376`, `:397`
- **Text:** "574 patients had a pre-op PROMIS physical function score, but only 328 had all four, so the analysis loses 246 patients (43%)" / "328 patients were measured at all four visits" / "981 = 3 × (328 patients − 1)" / "Of 574 patients with a pre-op PROMIS physical function score, 328 had all four measurements." / "Among 328 patients assessed at all four visits" / "Among 345 patients assessed"
- **Problem:** The code counts `case_id`, one per procedure. Because 80 patients had both sides done, these are not patient counts: the 328 complete cases belong to 299 patients, the 574 pre-op scores to 497 patients, and Solution 3's 345 cases to 315 patients. The numbers are right; the unit is wrong. Page 8 says "procedures" for the same cohort, pages 2 and 4 teach "say what the denominator is", and Solution 1 on this page correctly says "136 hip replacements". This is a wording error, not a wrong calculation, but it sits in two Results sentences.
- **Where it really comes from:** `n_distinct(pf$case_id)` at line 67; checked read-only with `n_distinct(pf$patient_id)`.
- **Proposed fix:** Replace "patients" with "procedures" (or "joints") wherever a `case_id` count is quoted, including the code comments ("# procedures with complete data", "# keep procedures measured at all four visits"), and write the Results as "Of 574 procedures with a pre-op PROMIS physical function score, 328 had all four measurements." and "Among 328 procedures assessed at all four visits". The Friedman section (`patient_id`, one ankle per patient) and the matched sets are correct as they stand.
- **Changes code:** comments only (no output changes), but the Results sentences and comments must change identically in German and French

### 09-2 · 574 pre-op scores, and the 246 and 43% built on it, are never shown · A
- **Where:** `en/catalog/09-three-plus-matched.qmd:31` (top ⚠️ box), `:180` (Results), `:184` (⚠️ box), section `#repeated-measures-anova`
- **Text:** "Below, 574 patients had a pre-op PROMIS physical function score, but only 328 had all four, so the analysis loses 246 patients (43%)."
- **Problem:** The box says "Below", but no visible output shows 574. Only 328 is printed. 246 and 43% depend on 574 and their arithmetic is not given.
- **Where it really comes from:** Prose guard lines 641 to 642.
- **Proposed fix:** In "Look at the data first", before the complete-case count:
  - R: `proms |> filter(visit == "preop", !is.na(promis_pf)) |> nrow()   # procedures with a pre-op score`
  - Python: `print(proms.loc[proms["visit"] == "preop", "promis_pf"].notna().sum())   # procedures with a pre-op score`
  
  Both print 574. Then: "574 procedures had a pre-op score and 328 had all four, so the analysis loses 574 − 328 = 246 of them (246 / 574 = 43%)."
- **Changes code:** yes

### 09-3 · "28 of them sit at 57.0" is never shown · A
- **Where:** `en/catalog/09-three-plus-matched.qmd:104`, section `#repeated-measures-anova`, step "Look at the data first"
- **Text:** "At 1 year, 28 of them sit at 57.0, the best the form can record. That's a small share, at one visit, in 328 patients"
- **Problem:** No output counts scores at the ceiling; the boxplot cannot show it.
- **Where it really comes from:** Prose guard line 650.
- **Proposed fix:**
  - R: `sum(pf$promis_pf[pf$visit == "1yr"] == 57)   # how many score the maximum, 57.0, at 1 year`
  - Python: `print((pf.loc[pf["visit"] == "1yr", "promis_pf"] == 57).sum())   # how many score the maximum, 57.0, at 1 year`
  
  Both print 28. Prose: "At 1 year, 28 of the 328 (9%) sit at 57.0".
- **Changes code:** yes

### 09-4 · "60 randomized patients" in the boot arm is never shown · A
- **Where:** `en/catalog/09-three-plus-matched.qmd:207`, `:264`, `:340` (Results), section `#friedman`
- **Text:** "The boot arm of the trial … has 60 randomized patients" / "Among 50 of the 60 patients randomized to a boot"
- **Problem:** The page prints 50 (complete cases) but never 60. The denominator of a Results sentence rests on a number the reader has to take from page 6.
- **Where it really comes from:** Prose guard line 652.
- **Proposed fix:** Before the complete-case filter:
  - R: `trial |> filter(arm == "boot") |> distinct(patient_id) |> nrow()   # patients randomized to a boot`
  - Python: `print(trial.loc[trial["arm"] == "boot", "patient_id"].nunique())   # patients randomized to a boot`
  
  Both print 60.
- **Changes code:** yes

### 09-5 · "6 patients score the maximum" is never shown · A
- **Where:** `en/catalog/09-three-plus-matched.qmd:264`, section `#friedman`, step "Look at the data first"
- **Text:** "by 12 months they're crowding the ceiling of 24: 6 patients score the maximum."
- **Problem:** The output gives quartiles only (q3 = 22 at 12 months); nothing counts scores of 24.
- **Where it really comes from:** Prose guard line 655.
- **Proposed fix:**
  - R: `sum(efas_boot$efas[efas_boot$visit == "12mo"] == 24)   # how many score the maximum, 24, at 12 months`
  - Python: `print((efas_boot.loc[efas_boot["visit"] == "12mo", "efas"] == 24).sum())   # how many score the maximum, 24, at 12 months`
  
  Both print 6. Prose: "6 of the 50 patients score the maximum."
- **Changes code:** yes

### 09-6 · "Most patients improved from each visit to the next" has no output behind it · A
- **Where:** `en/catalog/09-three-plus-matched.qmd:334`, section `#friedman`, step "Effect size and 95% CI"
- **Text:** "W = 0.85: a large effect. Most patients improved from each visit to the next."
- **Problem:** No chunk, visible or hidden, counts patients who improved; even the Prose guard does not check this sentence. The medians rise, but that is not the same claim. The CI printed in R (0.78 to 1.00) is also not mentioned until the Results.
- **Where it really comes from:** not computed anywhere on the page. Read-only check: 45 of 50 scored higher at 3 months than at 6 weeks, 42 of 50 higher at 12 months than at 3 months (37 did both).
- **Proposed fix:** Show it after the W output:
  - R:
    ```r
    efas_wide <- efas_boot |> pivot_wider(names_from = visit, values_from = efas)   # one row per patient, one column per visit
    sum(efas_wide$`3mo` > efas_wide$`6wk`)     # scored higher at 3 months than at 6 weeks
    sum(efas_wide$`12mo` > efas_wide$`3mo`)    # scored higher at 12 months than at 3 months
    ```
  - Python:
    ```python
    efas_wide = efas_boot.pivot(index="patient_id", columns="visit", values="efas")   # one row per patient, one column per visit
    print((efas_wide["3mo"] > efas_wide["6wk"]).sum())     # scored higher at 3 months than at 6 weeks
    print((efas_wide["12mo"] > efas_wide["3mo"]).sum())    # scored higher at 12 months than at 3 months
    ```
  
  Prose: "W = 0.85 (95% CI 0.78 to 1.00 in R): a large effect. 45 of the 50 patients scored higher at 3 months than at 6 weeks, and 42 scored higher at 12 months than at 3 months." Add the two counts to the Prose guard. Prose-only alternative: replace the sentence with the tie to the test, "W is the Friedman chi-squared divided by its largest possible value, n × (visits − 1): 84.94 / (50 × 2) = 0.85."
- **Changes code:** yes; no for the alternative

### 09-7 · "24.4 percentage points" does not follow from the printed percentages · B
- **Where:** `en/catalog/09-three-plus-matched.qmd:476`, section `#cochran-q`, step "Effect size and 95% CI"
- **Text:** "Use rose by 24.4 percentage points from pre-op to 6 weeks, then fell well below its pre-op level by 1 year (24.4 points lower)."
- **Problem:** No subtraction is shown. A reader who subtracts R's printed values gets 59.1 − 34.8 = 24.3, not 24.4 (unrounded: 59.146 − 34.756 = 24.390). The second figure (34.8 − 10.4 = 24.4) does match, and 24.4% is also the 3-month rate, so three identical numbers with different meanings sit close together.
- **Where it really comes from:** Prose guard line 661. Both changes are exactly 80 patients: 194 − 114 and 114 − 34, and 80 / 328 = 24.4%.
- **Proposed fix:** "Use rose from 114 to 194 of the 328 between pre-op and 6 weeks: 80 more, or 80 / 328 = 24.4 percentage points. By 1 year it had fallen to 34, which is 80 fewer than before surgery, again 24.4 points. (Subtracting the rounded percentages, 59.1 − 34.8, gives 24.3; work from the counts.)"
- **Changes code:** no

### 09-8 · Solution 3: the percentages are not computed and the CIs print as an unlabeled matrix · B
- **Where:** `en/catalog/09-three-plus-matched.qmd:805` (code at `:788` to `:790` and `:799` to `:801`), section `#exercises`, Solution 3
- **Text:** "walking-aid use was 58.8% (95% CI 53.6% to 63.9%) at 6 weeks, 25.2% (95% CI 20.9% to 30.1%) at 3 months and 10.7% (95% CI 7.9% to 14.4%) at 1 year"
- **Problem:** The solution prints counts (203, 87, 37 of 345) but no percentages, and the CIs as proportions in a matrix with rows `[1,]`, `[2,]` and columns `[,1]` to `[,3]` (R) or a list of `ConfidenceInterval(low=np.float64(0.5357…` (Python). The reader has to divide, multiply by 100 and work out which cell is which.
- **Where it really comes from:** Prose guard lines 682 to 684.
- **Proposed fix:** Reuse the main section's table:
  - R, replacing line 790:
    ```r
    after_ci <- mapply(function(k, n) prop.test(k, n, correct = FALSE)$conf.int, after_counts$using, after_counts$patients)
    after_counts |>
      mutate(percent = 100 * using / patients, ci_low = 100 * after_ci[1, ], ci_high = 100 * after_ci[2, ])
    ```
  - Python, replacing line 801:
    ```python
    cis = [stats.binomtest(int(k), int(n)).proportion_ci(method="wilson") for k, n in zip(counts["sum"], counts["count"])]
    print(pd.DataFrame({"percent": 100 * counts["sum"] / counts["count"],
                        "ci_low": [100 * ci.low for ci in cis], "ci_high": [100 * ci.high for ci in cis]}))
    ```
- **Changes code:** yes

### 09-9 · Stratified Cox: the per-implant p-values are skipped, and "13.5" matches the wrong printed line · B
- **Where:** `en/catalog/09-three-plus-matched.qmd:580` to `:583` (code at `:557`, Results at `:593`), section `#stratified-cox`, step "Read the output"
- **Text:** "**Likelihood ratio test = 13.5 on 2 df, p = 0.001:** the overall test that implant matters at all. Python prints it last."
- **Problem:** (a) R prints `Likelihood ratio test= 13.48` and, two lines down, `Score (logrank) test = 13.5`; a reader looking for "13.5" lands on the score test. (b) `Pr(>|z|)` (0.3198 for B, 0.0166 for C; column `p` in Python) is printed in both languages and never mentioned, although page 8's Cox section has a bullet for it. (c) Python prints only the statistic (`13.482363098251813`); the df and p = 0.001 quoted in the Results are in R's output only.
- **Where it really comes from:** the output lines quoted; the unrounded p is 0.00118.
- **Proposed fix:** Add a bullet "**Pr(>|z|)** (R) or **p** (Python): the p-value for each implant against A, p = 0.320 for B and p = 0.017 for C." Reword the last bullet: "**Likelihood ratio test = 13.48 on 2 df, p = 0.001** (13.5 in the report; not the score test on the line below, which happens to print 13.5)". In Python replace line 557 with
  ```python
  overall = set_cox.log_likelihood_ratio_test()                             # overall test, all implants
  print(overall.test_statistic, overall.degrees_freedom, overall.p_value)   # chi-square, df, p
  ```
  (prints `13.48… 2 0.00118…`).
- **Changes code:** no for (a) and (b); yes for (c), Python tab only

### 09-10 · Python's row and column names are not matched to the bullets · B
- **Where:** `en/catalog/09-three-plus-matched.qmd:151` (`#repeated-measures-anova`) and `:296` to `:298` (`#friedman`), step "Read the output"
- **Text:** "**Mauchly's test, W = 0.995, p = 0.903:**" / "**df = 2:**" / "**p < 0.001** (R prints "p < 2.2e-16")."
- **Problem:** Other bullets give both languages' names; these give R's only. In Python, Mauchly's test is the rows `W_spher` (0.99515), `p_spher` (0.903231) and `sphericity True`; the Friedman df is `ddof1` and the p-value is `p_unc` (`3.589140e-19`). `sphericity True` is never explained. R actually prints `p-value < 2.2e-16`, and the bullet has no explanation after it, unlike every other p bullet.
- **Where it really comes from:** the pingouin outputs.
- **Proposed fix:** "**Mauchly's test, W = 0.995, p = 0.903** (`W_spher` and `p_spher` in Python, which also sums it up as `sphericity True`)"; "**df = 2** (`ddof1` in Python)"; "**p < 0.001** (R prints `p-value < 2.2e-16`, the smallest it shows; Python's `p_unc` is `3.59e-19`): rankings this consistent would be very unlikely if the scores didn't change between visits." The same for Cochran's Q at line 436 ("Python's `p_unc` is `3.01e-40`").
- **Changes code:** no

### 09-11 · One-sided CIs, Huynh-Feldt columns and "type III" vs "Type I" are printed but never explained · C
- **Where:** `en/catalog/09-three-plus-matched.qmd:152`, `:174`, `:180` (`#repeated-measures-anova`); `:334`, `:340` (`#friedman`)
- **Text:** "η²~p~ = 0.50: a very large effect." / "one-sided 95% CI 0.47 to 1.00" / "Kendall's W = 0.85, one-sided 95% CI 0.78 to 1.00"
- **Problem:** R prints "One-sided CIs: upper bound fixed at [1.00]" three times on this page and the Results quote "one-sided" CIs, but the page never says why they are one-sided (page 8 does, once, in its ANOVA section; sections are meant to stand alone). The teaching prose after each effect size does not mention the CI at all. In the ANOVA output, `HFe 1.007`, `DF[HF]` and `p[HF]` (Huynh-Feldt) get no word, and an epsilon above 1 contradicts "1 means perfect sphericity". rstatix heads its table "type III tests" while effectsize prints "(Type I)" for the same model.
- **Where it really comes from:** printed output.
- **Proposed fix:** Line 174: "η²~p~ = 0.50 (95% CI 0.47 to 1.00): a very large effect. The CI is one-sided: η²~p~ can't be negative, so R reports a lower bound only and fixes the upper bound at 1.00." Line 334: the same clause for W. Line 152, add: "`HFe` and the `[HF]` columns are a second correction, Huynh-Feldt; you can ignore them here. The 'type III' and 'Type I' in the headings are ways of handling several predictors and give the same answer with one."
- **Changes code:** no

### 09-12 · The Wilson interval line has no comment · C
- **Where:** `en/catalog/09-three-plus-matched.qmd:447` (R) and `:457` (Python), section `#cochran-q`, step "Effect size and 95% CI"
- **Text:** `aid_ci <- mapply(function(k, n) prop.test(k, n, correct = FALSE)$conf.int, aid_by_visit$using, aid_by_visit$patients)`
- **Problem:** The densest line on the page has no comment. Nothing says that `prop.test(..., correct = FALSE)` is how R gives the Wilson interval, what `mapply` does, or why the next line reads `aid_ci[1, ]` and `aid_ci[2, ]`. Page 4 comments its version ("# Wilson 95% CI: prop.test() without the continuity correction").
- **Where it really comes from:** visible code.
- **Proposed fix:** Comments only: above line 447 `# Wilson 95% CI for each visit: prop.test() without the continuity correction, once per row` and `# aid_ci has one column per visit: row 1 = lower limit, row 2 = upper limit`; above line 457 `# Wilson 95% CI for each visit, one per row of counts`.
- **Changes code:** comments only (no output changes)

### 09-13 · "the 80 patients who had both sides operated on" is stated, never shown · B
- **Where:** `en/catalog/09-three-plus-matched.qmd:26`, 💡 box "How every section on this page works"
- **Text:** "the joint replacement examples use every case, including the 80 patients who had both sides operated on."
- **Problem:** Same as `08-13`. On this page it matters more, because the counts are then called "patients" (`09-1`).
- **Where it really comes from:** Prose guard line 640.
- **Proposed fix:** As `08-13`: show the count once where it is first taught and link there.
- **Changes code:** none on this page

## Pages with nothing to report

None.

## Not checked

- **Figures.** Statements read from plots ("Implants A and B track each other closely; implant C falls away from both", "Scores rise at each visit") were not checked against the images; the tables beside them support the second.
- **Instrument facts.** "The four-question form in PROMIS-29+2 runs from 22.5 to 57.0" and "The EFAS score adds up six questions … maximum of 24" are facts about the instruments. The guard confirms only that the data stay inside 22.5 to 57.0.
- **"Here lifelines' default convergence matches R exactly"** (`09`:602). The visible outputs agree to the digits printed (0.4330 and 3.9119 in R, 0.432957 and 3.911913 in Python) and the hidden check passes at the default tolerance; "exactly" was not tested further. Noticed in passing, outside this audit: `CLAUDE.md` rule 17 says every Cox fit passes `fit_options={"precision": …}` and stratified fits need `1e-12`; this fit passes none and the box explains why.
- **Whether `e` notation is explained elsewhere** (`08-14`). Only a pattern search of `en/` was done; pages outside my assignment were not read.
- **The proposed code** was run once against `data/` outside the pages and gives the values quoted. It was not rendered in a page, and the site tests were not run against it.
