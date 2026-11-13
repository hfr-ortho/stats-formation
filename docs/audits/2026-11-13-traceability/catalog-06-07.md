# Audit findings: catalog pages 6 and 7

Scope: `en/catalog/06-two-unpaired-groups.qmd` and `en/catalog/07-two-paired-groups.qmd`, top to bottom, exercises and Solutions included.

Notes on method:

- Page 6 was dumped from `_freeze` at the start, before the coordinator's edit landed. Its line numbers below refer to the working file **with** the coordinator's edit to `#mann-whitney` (929 lines; everything after line 311 sits 18 or 19 lines lower than in `HEAD`). Each finding quotes its text so it can be found if lines move again.
- The known finding (61% / 25% / 14%) is not reported. The coordinator's new sentences in that step (r = 0.25 − 0.61; 1,074.5 ÷ 3,364 = 0.32) were read in the source diff, not in rendered output.
- Every proposed code line was run read-only against `data/` and gives the numbers quoted. Scripts and dumps: `/private/tmp/claude-501/-Users-docschwab-repos-hfr-ortho-stats-formation/e86b0746-bdc2-42f9-871b-9e22a905d6cb/scratchpad/audit/work-catalog-06-07/`.
- "Changes code: yes" means the German and French pages need the same change and all three pages a re-render.

## 06-two-unpaired-groups.qmd

### 06-1 · Chi-square p without Yates' correction (0.754) is computed only in the Prose guard · A
- **Where:** `en/catalog/06-two-unpaired-groups.qmd:483`, section `#fisher-chi-square`, step "Read the output", box "Under the hood: Yates' continuity correction"
- **Text:** "without it (`correct = FALSE`, `correction=False`) p = 0.754"
- **Problem:** No visible chunk runs the uncorrected test. `prop.test(failure_table, correct = FALSE)` appears later, but only its `$estimate` and `$conf.int` are printed.
- **Where it really comes from:** Prose guard, `round(chisq.test(failure_table, correct = FALSE)$p.value, 3) == 0.754`.
- **Proposed fix:** Add one line to each "Run it" tab and say "(the last line of the code)" in the box.
  - R: `chisq.test(failure_table, correct = FALSE)$p.value   # the same test without Yates' correction`
  - Python: `print(stats.chi2_contingency(failure_table, correction=False).pvalue)   # the same test without Yates' correction`
  - Both print 0.7536.
- **Changes code:** yes

### 06-2 · Exercise 2: "13% with a boot and 17% with a cast scored 24" is not printed anywhere · A
- **Where:** `en/catalog/06-two-unpaired-groups.qmd:862`, section `#exercises`, exercise 2, Solution
- **Text:** "By 12 months many patients are at or near the ceiling of 24 (13% with a boot and 17% with a cast scored 24), so the **Mann-Whitney test**."
- **Problem:** These two percentages decide the choice of test, but the solution prints only n, median and quartiles. The R tab shows a bar chart (7 and 8 patients at 24, readable only by eye); the Python tab has no plot at all, although the exercise says "Look at the data first".
- **Where it really comes from:** Prose guard, `round(100 * tapply(ex_12mo$efas == 24, ex_12mo$arm, mean)) == c(13, 17)` (7 of 55 and 8 of 47).
- **Proposed fix:** Print the share in both tabs.
  - R: add a column to the existing `summarise()`: `at_24 = mean(efas == 24)   # share scoring the maximum` (prints 0.127 and 0.170).
  - Python: `print(efas_12mo.assign(at_24=efas_12mo["efas"] == 24).groupby("arm")["at_24"].mean())   # share of each arm scoring the maximum, 24`
  - Optionally add the two-panel histogram to the Python tab, as in `#mann-whitney`.
- **Changes code:** yes

### 06-3 · Exercise 3: the two percentages and the risk difference are not printed · A
- **Where:** `en/catalog/06-two-unpaired-groups.qmd:928`, section `#exercises`, exercise 3, Solution (Results)
- **Text:** "81 of 152 reconstructions in women (53.3%) and 92 of 198 in men (46.5%) (risk difference 6.8 percentage points, 95% CI −3.7 to 17.4; ..."
- **Problem:** The solution prints the table (81, 71; 92, 106), the Fisher output and the CI of the difference (−0.0372 to 0.1737), but never 53.3%, 46.5% or 6.8. The reader has to add the rows, divide, subtract and multiply by 100 with no hint. The main section printed these with `prop.table()`; the solution dropped that line.
- **Where it really comes from:** Prose guard (`prop.table(ex_rts, 1)`, `diff(rev(...))`).
- **Proposed fix:**
  - R: add `prop.table(rts_table, margin = 1)   # row percentages: returned to sport, by sex` after `rts_table`.
  - Python: add `print(women_yes / (women_yes + women_no), men_yes / (men_yes + men_no))   # share who returned: women, then men` before the CI line.
  - Add one sentence under the code: "The risk difference is 53.3% − 46.5% = 6.8 percentage points; the CI line prints proportions, so multiply by 100."
- **Changes code:** yes

### 06-4 · "Leaving out any one patient still gives −1" is computed only in the Prose guard · A
- **Where:** `en/catalog/06-two-unpaired-groups.qmd:380`, section `#mann-whitney`, box "R vs Python: Mann-Whitney defaults"
- **Text:** "With whole-number scores the estimate barely moves: leaving out any one patient still gives −1."
- **Problem:** This is a computed result (116 re-estimates) that no visible code produces. It carries the explanation of why scipy's default bootstrap returns `nan`.
- **Where it really comes from:** Prose guard, `jackknife_hl` and `all(jackknife_hl == -1), length(jackknife_hl) == 116`. (The `nan` claim itself is true: checked.)
- **Proposed fix:** Either show it, in the "Effect size and 95% CI" tabs (boot arm only is enough to make the point):
  - R: `boot_scores <- pain_6wk$pain_nrs[pain_6wk$arm == "boot"]`, `cast_scores <- pain_6wk$pain_nrs[pain_6wk$arm == "cast"]`, then `table(sapply(seq_along(boot_scores), function(i) median(outer(boot_scores[-i], cast_scores, "-"))))   # leave each boot patient out in turn: the estimate is −1 all 58 times`
  - Python: `print({float(hodges_lehmann(pain_boot.drop(i), pain_cast)) for i in pain_boot.index})   # leave each boot patient out in turn: always −1`
  - Or, prose only, drop the result and keep the reason: "With whole-number scores the estimate can only land on whole or half points, so it often doesn't change at all when one patient is left out. scipy's default bootstrap method (BCa) needs it to change, so here it returns `nan` with a warning."
- **Changes code:** yes for the first option, no for the second

### 06-5 · "The 80 patients who had both sides operated on" is shown nowhere, and is not this page's number · A
- **Where:** `en/catalog/06-two-unpaired-groups.qmd:26`, box "How every section on this page works"
- **Text:** "the joint replacement example uses every case, including the 80 patients who had both sides operated on."
- **Problem:** No output shows 80. It is also the count for the whole cohort; the implant A vs C comparison on this page has 383 cases from 343 patients, so 40 patients appear twice.
- **Where it really comes from:** Prose guard, `sum(table(cohort$patient_id) == 2) == 80`.
- **Proposed fix:** Prose only: drop the number ("including patients who had both sides operated on"). Or show the page's own number in the `#log-rank` "Look at the data first" chunk and quote that:
  - R: `sum(table(a_vs_c$patient_id) == 2)   # patients with both sides in this comparison` (40)
  - Python: `print((a_vs_c["patient_id"].value_counts() == 2).sum())   # patients with both sides in this comparison`
- **Changes code:** no (first option), yes (second)

### 06-6 · Missed-visit counts need a subtraction from numbers the output never shows · B
- **Where:** `en/catalog/06-two-unpaired-groups.qmd:95` (`#unpaired-t`, "Look at the data first"), `:258` (`#mann-whitney`, same step), `:893` (exercise 2, Solution)
- **Text:** "Eight patients missed the 3-month visit (3 in the boot arm, 5 in the cast arm), so 112 of the 120 randomized patients are analyzed." / "Four patients missed the 6-week visit (2 in each arm), so 116 of the 120" / "18 of the 120 patients missed the 12-month visit, 5 in the boot arm, 13 in the cast arm"
- **Problem:** The output shows only the patients seen (57 and 55; 58 and 58; 55 and 47). The 120 and "60 to each arm" are stated in line 43 but printed nowhere, and the subtraction is not spelled out.
- **Where it really comes from:** Prose guard (`missed_3mo`, `missed_6wk`, `120 - nrow(ex_12mo) == 18`).
- **Proposed fix:** Prose only, for example at line 95: "The table shows 57 + 55 = 112 patients. 60 were randomized to each arm, so 60 − 57 = 3 boot patients and 60 − 55 = 5 cast patients (8 in all) missed the 3-month visit." Same pattern at 258 (60 − 58 = 2 in each arm) and 893 (60 − 55 = 5, 60 − 47 = 13). If the 60 per arm should be visible too: R `trial |> filter(visit == "3mo") |> count(arm, seen = !is.na(efas))`.
- **Changes code:** no

### 06-7 · p-values are printed in e-notation and the bullets never say how to read them · B
- **Where:** `en/catalog/06-two-unpaired-groups.qmd:133` (`#unpaired-t`, "Read the output"), `:651` (`#log-rank`, "Read the output"), and the exercise 1 output
- **Text:** "**p < 0.001:** a difference this large would be very unlikely..." / "**Chisq = 20.5 on 1 degree of freedom, p < 0.001:**"
- **Problem:** The output says `p-value = 2.738e-08`, `p= 6e-06` (Python `5.856248429692094e-06`) and `1.915e-07`. A beginner does not know that `e-08` means "× 10⁻⁸". No English page explains the notation (page 10 is the only one that links a bullet to the printed form).
- **Where it really comes from:** output lines "t = 6.0036, df = 106.05, p-value = 2.738e-08" and "Chisq= 20.5 on 1 degrees of freedom, p= 6e-06".
- **Proposed fix:** Prose only. Line 133: "**p-value = 2.738e-08**, reported as p < 0.001: `e-08` means 'move the decimal point 8 places to the left', so this is 0.00000003. A difference this large would be..." Line 651: "**Chisq = 20.5 on 1 degree of freedom, p = 6e-06** (0.000006), reported as p < 0.001: ..."
- **Changes code:** no

### 06-8 · The mean difference (3.6) is printed only in Python; the bullets use R's labels only · B
- **Where:** `en/catalog/06-two-unpaired-groups.qmd:131` to `:139`, section `#unpaired-t`, steps "Read the output" and "Effect size and 95% CI"
- **Text:** "The **mean difference** with its CI is the effect size readers understand best: 3.6 points (95% CI 2.4 to 4.8)."
- **Problem:** R's `t.test()` prints the two means and the CI, not the difference. Python prints it (`3.585326953748007`) but no bullet mentions that line. The bullets also name things as R does ("t =", "mean in group boot"); Python prints `statistic=`, `pvalue=`, and no group means in this block.
- **Where it really comes from:** R: 17.40351 − 13.81818; Python: first number of the second printed line.
- **Proposed fix:** Prose only. Line 139: "...: 17.40 − 13.82 = 3.59, so 3.6 points (95% CI 2.4 to 4.8). R prints the two means and leaves the subtraction to you; Python's second line prints the difference (3.585) and then the CI." Line 131: "**t = 6.00** (`statistic` in Python)".
- **Changes code:** no

### 06-9 · Risk difference −0.8 points is not printed; the CI is printed as proportions · B
- **Where:** `en/catalog/06-two-unpaired-groups.qmd:536` and `:542`, section `#fisher-chi-square`, steps "Effect size and 95% CI" and "How to report it"; also `:434`
- **Text:** "The failure rate with a hamstring graft was 0.8 percentage points lower (95% CI 5.5 points lower to 4.0 points higher)" / "6 of 154 hamstring grafts (3.9%) and 6 of 129 BPTB grafts (4.7%)"
- **Problem:** Neither language prints the difference. The reader must subtract 0.03896 − 0.04651 and turn −0.0550 and 0.0399 into percentage points. The row totals 154 and 129 are also sums the tables do not show (6 + 148, 6 + 123).
- **Where it really comes from:** output lines "prop 1 0.03896104, prop 2 0.04651163" and "[1] -0.05503361 0.03993243".
- **Proposed fix:** Prose only. Line 536: "The two failure rates are 3.9% and 4.7%, so the risk difference is 3.9 − 4.7 = −0.8 percentage points. The CI line prints proportions (−0.055 to 0.040); times 100, that is −5.5 to 4.0 points. ..." Line 434: "6 of 154 hamstring grafts (6 + 148 in the first row; 3.9%) ...".
- **Changes code:** no

### 06-10 · The CI for the rank-biserial r is printed in R only, and nothing says so · B
- **Where:** `en/catalog/06-two-unpaired-groups.qmd:369` (`#mann-whitney`, "How to report it") and `:891` (exercise 2, Results)
- **Text:** "rank-biserial r = −0.36, 95% CI −0.53 to −0.17" / "rank-biserial r = −0.12, 95% CI −0.33 to 0.10"
- **Problem:** A reader on the Python tab sees `RBC -0.361177` and no CI. The R vs Python box covers the Hodges-Lehmann CI but not this one (the t test section does explain the same situation for Hedges' g).
- **Where it really comes from:** R output "-0.36 | [-0.53, -0.17]" from `effectsize::rank_biserial()`.
- **Proposed fix:** Prose only: add a bullet to the box at line 377: "**The CI for r.** effectsize prints a 95% CI for r. pingouin's `mwu()` gives r (the `RBC` column) without one, so the CI in the Results sentence comes from R."
- **Changes code:** no

### 06-11 · Python's `CLES = 0.319411` is printed and never explained · B
- **Where:** `en/catalog/06-two-unpaired-groups.qmd:293` to `:297`, section `#mann-whitney`, step "Read the output"
- **Text:** output line "MWU  1074.5   two-sided  0.00066 -0.361177  0.319411"; bullets cover `U_val`, `p_val` and `RBC` only
- **Problem:** CLES is exactly the quantity the section is about (the chance that a randomly chosen boot patient reports more pain than a cast patient, ties counted as half), and it equals the "1,074.5 ÷ 3,364 = 0.32" that the coordinator's new sentence derives. The reader is not told the output already shows it. Smaller point in the same bullet list: "a U of 1,682 would mean no tendency either way" does not say 1,682 is half of 3,364.
- **Where it really comes from:** `CLES` column of `pg.mwu()`; U / (n1 × n2).
- **Proposed fix:** Prose only. New bullet: "**CLES = 0.319** (Python): the 'common language effect size', U divided by the number of pairs (1,074.5 ÷ 3,364). It is the chance that a randomly chosen boot patient reports more pain than a randomly chosen cast patient, counting ties as half." And at line 293: "so a U of 1,682 (half of them) would mean no tendency either way."
- **Changes code:** no

### 06-12 · Log-rank bullets describe columns that only R prints · B
- **Where:** `en/catalog/06-two-unpaired-groups.qmd:649` to `:651`, section `#log-rank`, step "Read the output"
- **Text:** "**N:** patients in each group (246 with implant A, 137 with C)." / "**Observed / Expected:** ..."
- **Problem:** Python prints only `20.534618183417702 5.856248429692094e-06`. The bullets are not marked "(R)", unlike the other sections, so a Python reader looks for N, Observed and Expected in vain. R's last two columns, `(O-E)^2/E` and `(O-E)^2/V`, are never mentioned.
- **Where it really comes from:** R's `survdiff()` table.
- **Proposed fix:** Prose only: mark the first two bullets "(R)", add "Python prints only the test statistic (20.53) and the p-value", and one line: "The last column, (O-E)^2/V, is the test statistic again; ignore (O-E)^2/E."
- **Changes code:** no

### 06-13 · Exercise 1: R prints the boot arm's SD as 2.75, the Results sentence says 2.7 · B
- **Where:** `en/catalog/06-two-unpaired-groups.qmd:855`, exercise 1, Solution (Results)
- **Text:** "12.4 points (SD 2.7; n = 58) with a boot"
- **Problem:** The R tibble shows three significant digits (`2.75`), which a reader rounds to 2.8. The value is 2.747 (Python prints `2.747324`), so 2.7 is right, but from the R tab it looks like a mistake. The difference (2.9) is again printed only in Python (`2.931034482758621`).
- **Where it really comes from:** `sd(efas)` = 2.747324.
- **Proposed fix:** Smallest code fix, R tab line 840: `summarise(n = n(), mean = round(mean(efas), 1), sd = round(sd(efas), 1))`. Or prose only, under the tabs: "R's table shows three digits: 2.75 is 2.747 rounded, so the SD is 2.7 to one decimal. The difference is 12.43 − 9.50 = 2.93."
- **Changes code:** yes (first option), no (second)

### 06-14 · The sample odds ratio 0.8311 is not printed, and the formula has no numbers · B
- **Where:** `en/catalog/06-two-unpaired-groups.qmd:551`, section `#fisher-chi-square`, box "R vs Python: two different odds ratios"
- **Text:** "scipy's `fisher_exact()` reports the simple **sample** odds ratio (a × d) / (b × c), 0.8311 here."
- **Problem:** The Python code prints only `failure_fisher.pvalue`, so the reader never sees scipy's 0.8311, and a, b, c, d are not tied to the table.
- **Where it really comes from:** Prose guard, `round(6 * 123 / (148 * 6), 4) == 0.8311`.
- **Proposed fix:** Prose only: "... odds ratio (a × d) / (b × c), here (6 × 123) / (148 × 6) = 0.8311 (`failure_fisher.statistic`)."
- **Changes code:** no

### 06-15 · "No patient at the floor (0) or the ceiling (24)" can only be read off the histogram · B
- **Where:** `en/catalog/06-two-unpaired-groups.qmd:95`, section `#unpaired-t`, step "Look at the data first"
- **Text:** "Both arms are roughly bell-shaped, with no patient at the floor (0) or the ceiling (24)"
- **Problem:** This is the condition "When to use it" sets for treating a score as a measurement, and the summary table prints only n, mean and SD.
- **Where it really comes from:** Prose guard, `all(efas_3mo$efas > 0 & efas_3mo$efas < 24)`. The scores run from 10 to 23 (boot) and 4 to 23 (cast).
- **Proposed fix:** Add `min` and `max` to both summaries and quote them: R `summarise(n = n(), mean = mean(efas), sd = sd(efas), min = min(efas), max = max(efas))`; Python `.agg(["count", "mean", "std", "min", "max"])`. Prose: "... with no patient at the floor (0) or the ceiling (24): the scores run from 4 to 23."
- **Changes code:** yes

### 06-16 · "The estimates agree to five decimals" cannot be checked from the output · B
- **Where:** `en/catalog/06-two-unpaired-groups.qmd:187`, section `#unpaired-t`, box "R vs Python: Student's or Welch's?"
- **Text:** "The estimates agree to five decimals"
- **Problem:** R prints g as `1.13`, Python as `1.130200311478461`. The claim is true (R's full value is 1.1301974) but the reader sees two decimals on one side.
- **Where it really comes from:** hidden `check_agree(..., tol = 1e-5)`.
- **Proposed fix:** Prose only: "The estimates are 1.13020 in both (R's table rounds it to 1.13) and differ only from the sixth decimal: ..."
- **Changes code:** no

### 06-17 · Python's row-percentage table comes out in a different order from R's · C
- **Where:** `en/catalog/06-two-unpaired-groups.qmd:430`, section `#fisher-chi-square`, step "Look at the data first"
- **Text:** `print(pd.crosstab(two_grafts["graft"], two_grafts["failure_2y"], normalize="index"))   # row percentages`
- **Problem:** The counts table is reordered (hamstring first, failed first) but the percentage table is not: Python prints BPTB first and the "0" column first, so 0.953488 sits where R shows 0.03896. A beginner comparing tabs reads the wrong cell.
- **Where it really comes from:** the `.loc[["hamstring", "BPTB"], [1, 0]]` reordering is applied to the first crosstab only.
- **Proposed fix:** Append the same reordering: `print(pd.crosstab(two_grafts["graft"], two_grafts["failure_2y"], normalize="index").loc[["hamstring", "BPTB"], [1, 0]])   # row percentages`
- **Changes code:** yes

### 06-18 · `conf.type = "log-log"` and the 5-year table get no explanation in this section · C
- **Where:** `en/catalog/06-two-unpaired-groups.qmd:581` and `:690` to `:699`, section `#log-rank`
- **Text:** `survfit2(Surv(followup_years, revised) ~ implant, data = a_vs_c, conf.type = "log-log")` / "The Results sentence also gives each implant's revision-free survival at 5 years, with its CI:"
- **Problem:** The section must stand alone, but why R needs `conf.type = "log-log"` is explained only on pages 4 and 13. A reader who leaves it out gets a CI that differs from Python's. The 5-year table (time, n.risk, n.event, survival, std.err, lower/upper 95% CI) is followed directly by the Results sentence, with no line saying which columns become "89.9% (84.7% to 93.3%)".
- **Where it really comes from:** `survival`, `lower 95% CI`, `upper 95% CI` columns (0.8986, 0.8475, 0.9332; 0.7114, 0.6146, 0.7880), times 100.
- **Proposed fix:** Prose only. After the tabset: "Read `survival`, `lower 95% CI` and `upper 95% CI`, times 100: 89.9% (84.7% to 93.3%) with implant A and 71.1% (61.5% to 78.8%) with implant C." In the R vs Python box: "We set `conf.type = "log-log"` in R because that is the CI method lifelines uses ([page 4](04-describe-one-group.qmd#kaplan-meier))."
- **Changes code:** no

### 06-19 · The quartile bullet sits under the wrong output and skips its reasoning · C
- **Where:** `en/catalog/06-two-unpaired-groups.qmd:297`, section `#mann-whitney`, step "Read the output"
- **Text:** "the boot arm's upper quartile is 4.75 because it sits three-quarters of the way between a 4 and a 5."
- **Problem:** The 4.75 is in the "Look at the data first" table, two outputs earlier, not in the test output this step reads. "Three-quarters of the way" is unexplained: with 58 scores in order, the upper quartile falls between the 43rd (a 4) and the 44th (a 5).
- **Where it really comes from:** `quantile()` default: position 1 + 0.75 × 57 = 43.75.
- **Proposed fix:** Prose only: move the sentence to line 258 and write: "The boot arm's upper quartile is 4.75, not a whole score: with the 58 scores in order it falls between the 43rd (a 4) and the 44th (a 5), and both programs place it three-quarters of the way between them."
- **Changes code:** no

### 06-20 · "Wald" is used in the Methods sentence and the Python code without explanation · C
- **Where:** `en/catalog/06-two-unpaired-groups.qmd:540` (Methods) and `:515` (`method="wald"`), section `#fisher-chi-square`
- **Text:** "Effect sizes are reported as risk differences with Wald 95% CIs and as odds ratios with exact 95% CIs."
- **Problem:** The page never says what a Wald CI is or that R's `prop.test(..., correct = FALSE)` gives one. Page 4 defines it only in passing, as the interval not to use for a single proportion.
- **Where it really comes from:** `prop.test(correct = FALSE)$conf.int` and `confint_proportions_2indep(method="wald")`.
- **Proposed fix:** Prose only, before the tabset at line 493: "The CI for the risk difference is the simple 'estimate ± 1.96 standard errors' interval, called a Wald CI: `prop.test(..., correct = FALSE)` in R, `method="wald"` in Python."
- **Changes code:** no

## 07-two-paired-groups.qmd

### 07-1 · "Only 22 revisions inform it": 18 do, and they explain the hazard ratio of exactly 3.5 · ERROR
- **Where:** `en/catalog/07-two-paired-groups.qmd:598`, section `#stratified-cox`, step "Read the output"
- **Text:** "**lower .95 = 1.15, upper .95 = 10.63:** its 95% CI. Wide, because only 22 revisions inform it."
- **Problem:** It contradicts the section's own "When to use it" bullet (line 513): only a revision that happens while the matched partner is still being followed tells the model anything. That is 18 of the 22 (14 with implant C, 4 with implant A); the other 4 happened after the partner's follow-up had ended. A minor error, but the correct numbers also give the reader the derivation the page lacks: 14 / 4 = 3.5.
- **Where it really comes from:** not computed anywhere on the page. Checked against `data/matched_sets.csv`: no pair has tied follow-up times; C first 14, A first 4, uninformative 34 pairs.
- **Proposed fix:** Show the count in "Look at the data first" and use it in the bullet.
  - R: `pairs |> group_by(set_id) |> slice_min(followup_years, n = 1) |> ungroup() |> filter(revised == 1) |> count(implant)   # in each pair, the patient whose follow-up ended first; keep those that ended with a revision`
  - Python: `first = pairs.loc[pairs.groupby("set_id")["followup_years"].idxmin()]   # in each pair, the patient whose follow-up ended first` then `print(first[first["revised"] == 1]["implant"].value_counts())   # keep those that ended with a revision`
  - Bullet: "Wide, because few revisions inform it: of the 22, only the 18 that happened while the matched partner was still being followed count, 14 with implant C and 4 with implant A. With pairs, the hazard ratio is simply 14 / 4 = 3.5."
  - Prose-only alternative: "Wide, because few revisions inform it: 22 in all, and only those that happened while the matched partner was still being followed count."
- **Changes code:** yes (full fix), no (alternative)

### 07-2 · Results sentence: the mean and SD of each view are printed nowhere · A
- **Where:** `en/catalog/07-two-paired-groups.qmd:171`, section `#paired-t`, step "How to report it"
- **Text:** "the mean alpha angle was 61.8° (SD 11.2) on the Dunn 45° view and 58.2° (SD 10.8) on the frog-leg view"
- **Problem:** The visible code prints the number of hips, the missing count, the test and d~z~. No chunk prints either view's mean or SD, in either language.
- **Where it really comes from:** Prose guard, `round(c(mean(imaging$alpha_dunn45_deg), sd(...), mean(imaging$alpha_frogleg_deg), sd(...)), 1) == c(61.8, 11.2, 58.2, 10.8)`.
- **Proposed fix:** Add to "Look at the data first":
  - R: `imaging |> summarise(n = n(), dunn_mean = mean(alpha_dunn45_deg), dunn_sd = sd(alpha_dunn45_deg), frogleg_mean = mean(alpha_frogleg_deg), frogleg_sd = sd(alpha_frogleg_deg))   # each view's mean and SD` (short names, so the tibble is not cut off; prints 61.8, 11.2, 58.2, 10.8)
  - Python: `print(imaging[["alpha_dunn45_deg", "alpha_frogleg_deg"]].agg(["count", "mean", "std"]))   # each view's mean and SD`
- **Changes code:** yes

### 07-3 · "62 of the 80 hips (78%)" and "56 ... and 48" cam-positive hips are computed only in the Prose guard · A
- **Where:** `en/catalog/07-two-paired-groups.qmd:165`, section `#paired-t`, step "Effect size and 95% CI"
- **Text:** "d~z~ = 0.87 is a large effect: 62 of the 80 hips (78%) read higher on the Dunn view. ... With a threshold of 55°, 56 hips count as cam-positive on the Dunn view and 48 on the frog-leg view."
- **Problem:** Four numbers, no visible code. The histogram shows the 62 only by counting bars.
- **Where it really comes from:** Prose guard, `sum(imaging$difference > 0) == 62`, `sum(imaging$alpha_dunn45_deg > 55) == 56`, `sum(imaging$alpha_frogleg_deg > 55) == 48`.
- **Proposed fix:** Add to the effect-size tabs:
  - R: `sum(imaging$difference > 0)   # hips that read higher on the Dunn view`; `mean(imaging$difference > 0)   # ... as a share of the 80 hips`; `sum(imaging$alpha_dunn45_deg > 55)   # cam-positive (above 55°) on the Dunn view`; `sum(imaging$alpha_frogleg_deg > 55)   # ... and on the frog-leg view`
  - Python: `print((imaging["difference"] > 0).sum(), (imaging["difference"] > 0).mean())   # hips that read higher on the Dunn view, and their share`; `print((imaging["alpha_dunn45_deg"] > 55).sum(), (imaging["alpha_frogleg_deg"] > 55).sum())   # cam-positive (above 55°) on each view`
  - Prints 62, 0.775, 56, 48.
- **Changes code:** yes

### 07-4 · The unpaired p = 0.037 and the "11° spread" are computed only in the Prose guard · A
- **Where:** `en/catalog/07-two-paired-groups.qmd:175`, section `#paired-t`, box "Watch out: don't analyze paired data as unpaired"
- **Text:** "Here it gives p = 0.037 instead of p < 0.001: the 3.7° difference between the views is small next to the 11° spread between hips"
- **Problem:** The wrong test is never run in view, and the 11° is the SD of each view, which the page does not print (see 07-2).
- **Where it really comes from:** Prose guard, `round(t.test(imaging$alpha_dunn45_deg, imaging$alpha_frogleg_deg)$p.value, 3) == 0.037` and `round(mean(c(sd(...), sd(...)))) == 11`.
- **Proposed fix:** Add one line per language (end of "Run it", or a small tabset in the box) and point to it:
  - R: `t.test(imaging$alpha_dunn45_deg, imaging$alpha_frogleg_deg)$p.value   # the wrong test: unpaired (see the Watch out box)`
  - Python: `print(stats.ttest_ind(imaging["alpha_dunn45_deg"], imaging["alpha_frogleg_deg"], equal_var=False).pvalue)   # the wrong test: unpaired (see the Watch out box)`
  - Both print 0.0365. In the box: "... next to the spread between hips (each view's SD is about 11°, in the first table)".
- **Changes code:** yes

### 07-5 · Wilcoxon Results sentence: both IQRs are printed nowhere · A
- **Where:** `en/catalog/07-two-paired-groups.qmd:343`, section `#wilcoxon-signed-rank`, step "How to report it"
- **Text:** "Median KOOS JR was 50.0 (IQR 40.8 to 58.2) before surgery and 85.8 (IQR 75.0 to 94.0) at 1 year"
- **Problem:** The visible summary prints n, the number improved and the two medians. The four quartiles appear only in the Prose guard. The pre-op median also looks different in the two tabs (R's tibble `50.0`, Python `49.95`) with no comment.
- **Where it really comes from:** Prose guard, `quantile(koos$koos_preop, c(0.25, 0.75))` and `quantile(koos$koos_1yr, c(0.25, 0.75))`. Exact values: 40.8, 49.95, 58.175 and 74.95, 85.8, 93.975.
- **Proposed fix:** Print the quartiles the way exercise 3 already does:
  - R: `quantile(koos$koos_preop, c(0.25, 0.50, 0.75))   # quartiles before surgery` and `quantile(koos$koos_1yr, c(0.25, 0.50, 0.75))   # quartiles at 1 year`
  - Python: `print(koos[["preop", "1yr"]].quantile([0.25, 0.50, 0.75]))   # quartiles before surgery and at 1 year`
  - Prose under the tabs: "Rounded to one decimal, the medians are 50.0 and 85.8, with IQRs of 40.8 to 58.2 and 75.0 to 94.0."
- **Changes code:** yes

### 07-6 · The unstratified hazard ratio 3.60 is computed only in the Prose guard · A
- **Where:** `en/catalog/07-two-paired-groups.qmd:614`, section `#stratified-cox`, box "Watch out: don't ignore the matching"
- **Text:** "Here it gives a slightly different answer (hazard ratio 3.60)"
- **Problem:** The ordinary Cox model is never fitted in view.
- **Where it really comes from:** Prose guard, `round(exp(coef(coxph(Surv(followup_years, revised) ~ implant, data = pairs))), 2) == 3.60`.
- **Proposed fix:** Add one line per language at the end of "Run it":
  - R: `exp(coef(coxph(Surv(followup_years, revised) ~ implant, data = pairs)))   # the wrong model: matching ignored (see the Watch out box)`
  - Python: `print(CoxPHFitter().fit(pairs[["followup_years", "revised", "implant"]], duration_col="followup_years", event_col="revised", formula="implant", fit_options={"precision": 1e-9}).hazard_ratios_)   # the wrong model: matching ignored`
  - Both print 3.597.
- **Changes code:** yes

### 07-7 · Exercise 1: "reads high in hips with little torsion and low in hips with a lot" is shown nowhere · A
- **Where:** `en/catalog/07-two-paired-groups.qmd:724`, section `#exercises`, exercise 1, Solution
- **Text:** "the Budin view reads high in hips with little torsion and low in hips with a lot, and the two errors cancel in the mean."
- **Problem:** This is the point of the exercise, and no output or plot supports it. The link to page 17 does not help: page 17 does not use the torsion data.
- **Where it really comes from:** Prose guard, `mean(ex_torsion_diff[imaging$torsion_ct_deg < 5]) > 0, mean(ex_torsion_diff[imaging$torsion_ct_deg > 25]) < 0`.
- **Proposed fix:** Add to the solution:
  - R: `imaging |> mutate(ct_torsion = cut(torsion_ct_deg, c(-Inf, 5, 25, Inf), labels = c("under 5°", "5° to 25°", "over 25°"))) |> group_by(ct_torsion) |> summarise(hips = n(), mean_difference = mean(torsion_budin_deg - torsion_ct_deg))   # Budin minus CT, by how much torsion CT shows`
  - Python: `ct_torsion = pd.cut(imaging["torsion_ct_deg"], [-np.inf, 5, 25, np.inf], labels=["under 5°", "5° to 25°", "over 25°"])` then `print(torsion_diff.groupby(ct_torsion, observed=True).agg(["count", "mean"]))   # Budin minus CT, by how much torsion CT shows`
  - Prints 11 hips, +1.45; 61 hips, −0.91; 8 hips, −6.99. Prose: "... reads 1.4° high in the 11 hips with under 5° of torsion on CT and 7.0° low in the 8 hips with over 25°".
- **Changes code:** yes

### 07-8 · d~av~ "0.33 here" is computed only in the Prose guard · A
- **Where:** `en/catalog/07-two-paired-groups.qmd:180`, section `#paired-t`, box "R vs Python: paired effect sizes"
- **Text:** "it returns d~av~ (the mean difference divided by the square root of the average of the two variances), 0.33 here."
- **Problem:** No visible code calls `pg.compute_effsize()` (this section does not even import pingouin), and the two SDs the formula needs are not printed either.
- **Where it really comes from:** Prose guard, `reticulate::py_eval("float(pg.compute_effsize(..., paired=True, eftype='cohen'))")`.
- **Proposed fix:** Prose only, once 07-2 makes the SDs visible: "..., here 3.67 / √((11.2² + 10.8²) / 2) = 3.67 / 11.0 = 0.33."
- **Changes code:** no (depends on 07-2)

### 07-9 · "A hazard ratio of 3.4997 instead of 3.5" is computed only in the Prose guard · A
- **Where:** `en/catalog/07-two-paired-groups.qmd:619`, section `#stratified-cox`, box "R vs Python: strata and convergence"
- **Text:** "lifelines' default convergence rule stops a little early (a hazard ratio of 3.4997 instead of 3.5)"
- **Problem:** The default fit is never run in view.
- **Where it really comes from:** Prose guard, a `py_eval()` of the same fit without `fit_options` (3.49966; checked).
- **Proposed fix:** Lowest priority of the A findings. Either add a Python-only line after the fit, `print(CoxPHFitter().fit(pairs[["followup_years", "revised", "implant", "set_id"]], duration_col="followup_years", event_col="revised", formula="implant", strata=["set_id"]).hazard_ratios_)   # lifelines' default stopping rule: 3.4997`, or keep the prose and say how to see it: "(run the fit without `fit_options` and it prints 3.4997 instead of 3.5)".
- **Changes code:** yes (first option), no (second)

### 07-10 · "The 80 patients who had both sides operated on" is shown nowhere, and no example on this page has 80 · A
- **Where:** `en/catalog/07-two-paired-groups.qmd:26`, box "How every section on this page works"
- **Text:** "the joint replacement examples use every case, including the 80 patients who had both sides operated on."
- **Problem:** Same as 06-5. 80 is the count in the whole PROM file. The KOOS JR example has 28 patients with both sides among its 246 cases; the walking-aid example has 57 among 505.
- **Where it really comes from:** Prose guard, `sum(table(distinct(proms, case_id, patient_id)$patient_id) == 2) == 80`.
- **Proposed fix:** Prose only: drop the number ("including patients who had both sides operated on").
- **Changes code:** no

### 07-11 · p-values: e-notation unexplained, and R and Python print different things for the Wilcoxon test · B
- **Where:** `en/catalog/07-two-paired-groups.qmd:130` (`#paired-t`), `:289` (`#wilcoxon-signed-rank`), `:443` (`#mcnemar`), step "Read the output" in each
- **Text:** "**p < 0.001.**" (lines 289 and 443 have nothing more)
- **Problem:** The outputs read `p-value = 2.724e-11`, `p-value < 2.2e-16` (R) against `4.179101e-42` (Python), and `p-value = 5.36e-14`. The notation is not explained, and for the Wilcoxon test the two tabs visibly disagree with no comment.
- **Where it really comes from:** the output lines quoted. R prints "< 2.2e-16" for any p-value too small for it to show; Python prints the number.
- **Proposed fix:** Prose only. Line 130: "**p-value = 2.724e-11**, reported as p < 0.001: `e-11` means 'move the decimal point 11 places to the left'." Line 289: "**p < 0.001:** R prints `p-value < 2.2e-16`, its way of saying 'too small to show'; Python prints `4.179101e-42`. Both are far below 0.001." Line 443: "**p-value = 5.36e-14**, reported as p < 0.001."
- **Changes code:** no

### 07-12 · The CI for d~z~ is printed in R only, and nothing says so · B
- **Where:** `en/catalog/07-two-paired-groups.qmd:171` (`#paired-t`, Results) and `:722` (exercise 1, Results)
- **Text:** "d~z~ = 0.87, 95% CI 0.61 to 1.12" / "d~z~ = −0.26, 95% CI −0.48 to −0.04"
- **Problem:** The Python tab computes d~z~ by hand (`0.865990584734926`) and has no CI. The R vs Python box talks only about d~av~.
- **Where it really comes from:** R output "0.87 | [0.61, 1.12]" from `effectsize::repeated_measures_d()`.
- **Proposed fix:** Prose only, in the box at line 180: "The Python code gives d~z~ without a CI; the CI in the Results sentence is the one R's effectsize prints."
- **Changes code:** no

### 07-13 · Exercise 1: R cuts the Budin SD off the table, so "SD 7.6" is visible in Python only · B
- **Where:** `en/catalog/07-two-paired-groups.qmd:709` (R code) and `:722` (Results), exercise 1, Solution
- **Text:** "13.3° (SD 7.6) on the Budin view"
- **Problem:** The R tibble is too wide and ends with "# ℹ 1 more variable: torsion_budin_deg_sd <dbl>". The number is hidden in the R tab.
- **Where it really comes from:** Python output "std 8.931075 7.5802".
- **Proposed fix:** Shorter column names so all five fit: `imaging |> summarise(n = n(), ct_mean = mean(torsion_ct_deg), ct_sd = sd(torsion_ct_deg), budin_mean = mean(torsion_budin_deg), budin_sd = sd(torsion_budin_deg))` (prints 14.5, 8.93, 13.3, 7.58).
- **Changes code:** yes (R only; Python unchanged)

### 07-14 · Exercise 3: the Hodges-Lehmann estimate and its CI come from R only · B
- **Where:** `en/catalog/07-two-paired-groups.qmd:786` to `:794`, exercise 3, Solution
- **Text:** "(Hodges-Lehmann estimate of the change 9.9 points, 95% CI 8.2 to 11.6; rank-biserial r = 0.74; p < 0.001)"
- **Problem:** The Python solution prints the test, the counts and the quartiles, but never calls `hodges_lehmann()` or the bootstrap, so two of the reported numbers have no Python source. Also: R prints `9.949962` (its search stops just short of the exact value 9.95), and Python's own method would give 9.95 with a bootstrap CI of 8.25 to 11.6, so the two tabs would round differently. The sentence gives r without the CI R prints (0.66 to 0.80), and 176 + 46 = 222 of 225 leaves 3 unchanged patients unmentioned.
- **Where it really comes from:** R output "(pseudo)median 9.949962", "8.200009 11.600000".
- **Proposed fix:** Prose only is the safe option: under the tabs, "The Hodges-Lehmann estimate and its CI are R's (`(pseudo)median` and the CI above it). In Python, apply `hodges_lehmann()` and the bootstrap from the section above to `later["1yr"] - later["3mo"]`: it prints 9.95 and 8.25 to 11.6, the same result before rounding. Three patients did not change." Adding the Python lines instead would put 9.95 next to a sentence that says 9.9, so the sentence would then need "9.9 (R) or 9.95 (Python)" or a choice of one.
- **Changes code:** no

### 07-15 · "Of 505 patients seen at both visits" is a sum the output does not show · B
- **Where:** `en/catalog/07-two-paired-groups.qmd:410`, section `#mcnemar`, step "Look at the data first"
- **Text:** "Of 505 patients seen at both visits, 134 never used an aid and 108 used one at both times. The other 263 changed"
- **Problem:** The table has four cells and no total; 505 and 263 are left to the reader. Which cell means "started" is explained only two steps later, in a code comment.
- **Where it really comes from:** 134 + 193 + 70 + 108 = 505; 193 + 70 = 263.
- **Proposed fix:** Prose only: "The table holds 134 + 193 + 70 + 108 = 505 patients seen at both visits. 134 never used an aid (row 0, column 0) and 108 used one at both times (row 1, column 1). The other 193 + 70 = 263 changed: **193 started** using an aid (row 0, column 1) and **70 stopped** (row 1, column 0)."
- **Changes code:** no

### 07-16 · Python's `CLES = 0.964621` is printed, unexplained, and looks wrong · C
- **Where:** `en/catalog/07-two-paired-groups.qmd:288` to `:291`, section `#wilcoxon-signed-rank`, step "Read the output"
- **Text:** output line "Wilcoxon    0.0   two-sided  4.179101e-42  1.0  0.964621"
- **Problem:** Every patient improved and r is exactly 1, yet the next column says 0.96. A beginner will wonder what went wrong. pingouin computes CLES as if the two columns were unpaired groups: the share of all 246 × 246 (1-year, pre-op) combinations in which the 1-year score is higher (checked: 0.9646).
- **Where it really comes from:** `CLES` column of `pg.wilcoxon()`.
- **Proposed fix:** Prose only, new bullet: "**CLES = 0.965** (Python): ignore it here. pingouin computes it as if the two columns were two unpaired groups (any patient's 1-year score against any patient's pre-op score), so it is not 1 although every patient improved."
- **Changes code:** no

### 07-17 · The reason for choosing the Wilcoxon test (a ceiling at 1 year) is never shown, and the plot points the other way · C
- **Where:** `en/catalog/07-two-paired-groups.qmd:189`, `:193`, `:214` and `:341`, section `#wilcoxon-signed-rank`
- **Text:** "The 1-year KOOS JR has a ceiling ([page 3](...))." / "If the changes are roughly normal → the [paired t test](#paired-t)." / Methods: "Because 1-year KOOS JR scores showed a ceiling effect"
- **Problem:** The only plot is a histogram of the changes, which looks roughly symmetric. By the section's own last bullet a beginner would now switch to the paired t test. Nothing on the page shows the ceiling that the Methods sentence cites.
- **Where it really comes from:** not shown on this page; 15% of the 246 patients score 100 at 1 year (checked).
- **Proposed fix:** One line per language in "Look at the data first" and one sentence:
  - R: `mean(koos$koos_1yr == 100)   # share of patients at the maximum score at 1 year`
  - Python: `print((koos["1yr"] == 100).mean())   # share of patients at the maximum score at 1 year`
  - Prose at line 250: "The changes look fairly symmetric, but 15% of patients score the maximum of 100 at 1 year: their true improvement is cut off, so we compare ranks."
  - Prose-only alternative: the same sentence without the 15%, pointing to page 3.
- **Changes code:** yes (or no with the alternative)

### 07-18 · The step from the binomial CI to the odds-ratio CI is unexplained · C
- **Where:** `en/catalog/07-two-paired-groups.qmd:447` and `:458` to `:459`, section `#mcnemar`, step "Effect size and 95% CI"
- **Text:** "Its exact CI comes from a binomial test on the discordant pairs." / `ci / (1 - ci)   # turned into a CI for the odds ratio`
- **Problem:** The intermediate CI is never printed and the reader is not told why dividing by (1 − ci) gives an odds ratio.
- **Where it really comes from:** 193 of 263 changers started (0.734, 95% CI 0.676 to 0.786); odds = share / (1 − share).
- **Proposed fix:** Prose only, after line 447: "193 of the 263 patients who changed started using an aid, a share of 0.734. Odds are share / (1 − share): 0.734 / 0.266 = 2.76, the same as 193 / 70. The code does the same to both ends of the share's exact CI (0.676 to 0.786)." Optionally print `ci` on its own line in both tabs so 0.676 and 0.786 are visible.
- **Changes code:** no

### 07-19 · Cox output: three tests with different p-values "test the same thing", and half the table is unexplained · C
- **Where:** `en/catalog/07-two-paired-groups.qmd:596` to `:600`, section `#stratified-cox`, step "Read the output"
- **Text:** "R also prints a likelihood ratio, Wald and score test for the whole model; with one predictor they all test the same thing."
- **Problem:** R prints p = 0.02, 0.03 and 0.02 for them, and the reported p is 0.027. A beginner cannot tell which line the 0.027 belongs to. `coef`, `se(coef)`, `z`, `exp(-coef)` and `Concordance` are never mentioned. The bullets use R's labels only: Python prints `exp(coef) lower 95%`, `exp(coef) upper 95%` and `p`, and does not print n or the number of events.
- **Where it really comes from:** `Pr(>|z|)` is the Wald test: z = 2.21 and 2.21² = 4.88, the "Wald test" line.
- **Proposed fix:** Prose only: "**Pr(>|z|) = 0.027** (`p` in Python): the p-value for implant. It is the Wald test: z = 2.21, and 2.21² = 4.88 is the 'Wald test' line at the bottom, where R rounds the same p to 0.03. The likelihood ratio and score tests ask the same question with slightly different approximations (p = 0.02 here)." Add: "**coef = 1.25** is the log of the hazard ratio; **exp(-coef) = 0.29** is the hazard ratio the other way round, A vs C." Mark the first bullet "(R)".
- **Changes code:** no

## Pages with nothing to report

None. Sections with no A finding: page 6 `#unpaired-t` and `#log-rank`; page 7 `#mcnemar`.

## Not checked

- The rendered output of the coordinator's new `#mann-whitney` code (pair percentages): the `_freeze` snapshot was taken before it landed. The step was skipped as instructed, apart from 06-11, which builds on the new sentence.
- German and French pages (out of scope).
- Plots: only the KOOS change histogram (page 7) and the 12-month EFAS bar chart (page 6) were opened. Statements such as "roughly bell-shaped" and "the gap keeps growing" were not judged.
- Software-default claims in the R vs Python boxes were checked only where a quick run could do it (scipy BCa returns `nan`; `fisher_exact()` statistic 0.8311; lifelines default fit 3.4997; pingouin d~av~ 0.33). Not checked: R's exact-p thresholds for `wilcox.test()`, Efron tie handling, statsmodels' `mcnemar()` default.
- Project rule 17 (every Cox fit passes `fit_options={"precision": 1e-9}`): the `#log-rank` Cox fit on page 6 (line 668) does not, and its printed hazard ratio differs from R's in the sixth decimal (3.039403 against 3.039405). Not a traceability finding, so it is only noted here.
