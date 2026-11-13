# Audit findings: catalog pages 10 to 12

Audited: `en/catalog/10-association.qmd`, `en/catalog/11-predict-from-one.qmd`, `en/catalog/12-predict-from-several.qmd`, each against its frozen output (`_freeze/en/catalog/<page>/execute-results/html.json`, dumped to `work-catalog-10-12/`).

How I drew the line between A and B: **A** means the number needs the raw data or a hidden chunk (nothing printed on the page leads to it). **B** means the reader can get there from printed numbers, but only through a step the page does not spell out (arithmetic, a second rounding, a different scale, one language only, another page). No ERROR findings: I found no place where the prose contradicts the output. All proposed code was run read-only against `data/` and gives the quoted numbers.

Every fix marked "Changes code: yes" must be copied identically into `de/` and `fr/` and all three pages re-rendered.

---

## 10-association.qmd

### 10-1 · Budin vs CT disagreement figures come only from the Prose guard · A
- **Where:** `en/catalog/10-association.qmd:130`, section `#pearson`, the ⚠️ box after "How to report it"
- **Text:** "Here r = 0.86, yet the Budin reading was up to 12.9° away from CT, and 95% of the differences would be expected from −10.2° to 7.8°. Even those limits hide a trend: in the 8 hips with 25° or more on CT, the Budin reading averaged 7.0° lower."
- **Problem:** Five numbers (12.9, −10.2, 7.8, 8 hips, 7.0) and no visible code or output for any of them. The printed output gives only r, t, df, p and the CI, none of which lead to them. "Those limits" is also used before the reader is told they are the mean difference ± 1.96 SD. The linked page 17 does not show these torsion numbers either.
- **Where it really comes from:** hidden Prose guard, lines 424 and 432 to 435 (`budin_minus_ct`, `max(abs(...))`, `mean ± 1.96 * sd`, `sum(torsion_ct_deg >= 25)`, mean of the subset).
- **Proposed fix:** Add a tabset inside the box, after the paragraph, and tie the sentence to it ("... the code below computes them"). Also add "(the mean difference ± 1.96 standard deviations)" after "7.8°".

  R:
  ```r
  difference <- imaging$torsion_budin_deg - imaging$torsion_ct_deg   # Budin minus CT, one value per hip
  max(abs(difference))                                  # the largest gap between the two methods
  mean(difference) + c(-1.96, 1.96) * sd(difference)    # where 95% of the differences are expected
  high_ct <- imaging$torsion_ct_deg >= 25               # hips with 25° or more on CT
  sum(high_ct)                                          # how many
  mean(difference[high_ct])                             # their mean difference
  ```
  Python:
  ```python
  difference = imaging["torsion_budin_deg"] - imaging["torsion_ct_deg"]   # Budin minus CT, one value per hip
  print(difference.abs().max())                         # the largest gap between the two methods
  print(difference.mean() - 1.96 * difference.std(), difference.mean() + 1.96 * difference.std())   # where 95% of the differences are expected
  high_ct = imaging["torsion_ct_deg"] >= 25             # hips with 25° or more on CT
  print(high_ct.sum(), difference[high_ct].mean())      # how many, and their mean difference
  ```
  (Outputs: 12.9; −10.19 and 7.81; 8; −6.99.)
- **Changes code:** yes

### 10-2 · Bias-corrected V = 0.18 is never printed · A
- **Where:** `en/catalog/10-association.qmd:412`, section `#contingency-coefficients`, 🔀 box
- **Text:** "effectsize's `cramers_v()` and `phi()` apply a small-sample bias correction by default (here V = 0.18)"
- **Problem:** The page only ever runs `cramers_v(..., adjust = FALSE)` (0.20). The 0.18 appears in no output.
- **Where it really comes from:** Prose guard line 449 (`effectsize::cramers_v(asa_hypertension)$Cramers_v`).
- **Proposed fix:** Add one line to the R tab of "Effect size and 95% CI" (scipy has no counterpart, so R only): `effectsize::cramers_v(asa_hypertension)   # the default, with the small-sample correction` (prints `Cramer's V (adj.) 0.18 [0.10, 1.00]`), and change the box to "(here V = 0.18, the 'adj.' result in the R tab)". Prose-only alternative: drop the number ("a slightly smaller V").
- **Changes code:** yes (R tab only); no for the alternative

### 10-3 · "the 80 patients who had both sides operated on" is asserted, never counted · A
- **Where:** `en/catalog/10-association.qmd:26`, opening 💡 box (the same sentence is at `11-predict-from-one.qmd:26` and `12-predict-from-several.qmd:26`)
- **Text:** "the joint replacement examples use every case, including the 80 patients who had both sides operated on"
- **Problem:** No output on the page shows 80. The linked page 3 `#paired` also states it in prose only (its count sits in that page's Prose guard, line 542).
- **Where it really comes from:** Prose guard line 427 (`sum(table(cohort$patient_id) == 2) == 80`).
- **Proposed fix:** Prose only, same wording on all three pages: "... including the 80 patients who had both sides operated on (`sum(table(cohort$patient_id) == 2)` in R counts them)". Better still, show the count once in visible code on page 3 `#paired` (not one of my pages) and write here "(counted on page 3)".
- **Changes code:** no

### 10-4 · Exercise 3: the percentages and denominators are not in the Solution's output · B
- **Where:** `en/catalog/10-association.qmd:547`, `#exercises`, Solution 3
- **Text:** "Sleep apnea was present in 69 of 257 men (26.8%) and 43 of 343 women (12.5%)"
- **Problem:** The Solution prints only the 2 × 2 counts (300/43, 188/69). The reader must add to get 343 and 257 and divide to get 12.5% and 26.8%. The main section prints row percentages; the Solution does not.
- **Where it really comes from:** Prose guard lines 456 and 457.
- **Proposed fix:** Add the row percentages, as the main section does.
  R, after `apnea`: `round(100 * prop.table(apnea, margin = 1), 1)   # row percentages`
  Python, after `print(apnea)`: `print((100 * pd.crosstab(cohort["sex"], cohort["sleep_apnea"], normalize="index")).round(1))   # row percentages`
  Plus one prose line under the Results: "343 = 300 + 43 women and 257 = 188 + 69 men."
- **Changes code:** yes

### 10-5 · "404 procedures" has to be added up from the table · B
- **Where:** `en/catalog/10-association.qmd:199` and `:274` (Results), section `#spearman`
- **Text:** "404 procedures have both a pre-op and a 1-year score and a satisfaction answer."
- **Problem:** 404 is the sum of the `n` column (14 + 18 + 43 + 131 + 198); nothing prints it. Python even computes `n = len(change)` later without printing it.
- **Where it really comes from:** Prose guard line 437 (`nrow(change) == 404`).
- **Proposed fix:** Add `nrow(change)   # procedures with both scores and a satisfaction answer` to the R chunk and `print(len(change))   # procedures with both scores and a satisfaction answer` to the Python chunk. Prose-only alternative: "404 procedures (the `n` column adds up to 404) have ...".
- **Changes code:** yes; no for the alternative

### 10-6 · Which cell has the smallest expected count is not shown · B
- **Where:** `en/catalog/10-association.qmd:364`, section `#contingency-coefficients`, "Read the output"
- **Text:** "**Smallest expected count 7.83** (ASA 4 without hypertension)"
- **Problem:** The output is the bare number 7.83. Nothing shows that it belongs to the ASA 4, no-hypertension cell, or how an expected count is formed.
- **Where it really comes from:** Prose guard line 446 (`which.min(asa_test$expected) == 4`).
- **Proposed fix:** Print the whole table instead of the minimum: R `round(asa_test$expected, 2)   # expected counts if ASA and hypertension were unrelated`; Python `print(asa_test.expected_freq.round(2))   # expected counts if ASA and hypertension were unrelated`. Then: "Smallest expected count 7.83, in the last row, first column (ASA 4 without hypertension): 18 procedures × 261 without hypertension / 600."
- **Changes code:** yes

### 10-7 · Pearson's C ceiling of 0.71 has no derivation · B
- **Where:** `en/catalog/10-association.qmd:295` ("When to use it") and `:397`
- **Text:** "Its maximum is below 1 and depends on the table's size (0.71 for a table with two columns)" and "its ceiling for this table is 0.71, not 1"
- **Problem:** The reader cannot tell where 0.71 comes from or what it would be for another table.
- **Where it really comes from:** Prose guard line 448 (`sqrt(1 / 2)`).
- **Proposed fix:** Prose: "Its maximum is √((k − 1)/k), where k is the smaller of the number of rows and columns: √(1/2) = 0.71 for a table with two columns."
- **Changes code:** no

### 10-8 · Exercise 1: "3.7° higher on average" is not on this page · B
- **Where:** `en/catalog/10-association.qmd:490`, `#exercises`, Solution 1
- **Text:** "yet the Dunn view read 3.7° higher on average ([page 7](07-two-paired-groups.qmd#paired-t))"
- **Problem:** The Solution prints only the correlation. The 3.7° is on page 7 ("mean difference 3.67"), one click away, but the reader of this Solution cannot check it here.
- **Where it really comes from:** Prose guard line 453; visible on page 7, line 131.
- **Proposed fix:** Add one line per tab: R `mean(imaging$alpha_dunn45_deg - imaging$alpha_frogleg_deg)   # mean difference, Dunn minus frog-leg`; Python `print((imaging["alpha_dunn45_deg"] - imaging["alpha_frogleg_deg"]).mean())   # mean difference, Dunn minus frog-leg` (3.67). Prose-only alternative: "(page 7 computes it: mean difference 3.67)".
- **Changes code:** yes; no for the alternative

### 10-9 · Row totals 36 and 18 are not printed · B (minor)
- **Where:** `en/catalog/10-association.qmd:328` and `:403` (Results), section `#contingency-coefficients`
- **Text:** "from 12 of 36 (33.3%) in ASA 1 to 16 of 18 (88.9%) in ASA 4"
- **Problem:** The table prints 24 and 12, 2 and 16; the reader has to add them to find 36 and 18.
- **Where it really comes from:** Prose guard line 442 (`rowSums`).
- **Proposed fix:** Prose: "from 12 of 36 (24 + 12; 33.3%) in ASA 1 to 16 of 18 (2 + 16; 88.9%) in ASA 4" in the teaching sentence only (not the Results). Code alternative: R `addmargins(asa_hypertension)`, Python `pd.crosstab(..., margins=True)`.
- **Changes code:** no

### 10-10 · p-values: what the two languages print is only half tied to the text · C
- **Where:** `en/catalog/10-association.qmd:113`, `:234`, `:363`
- **Text:** "**p < 0.001** (R prints `< 2.2e-16`)"
- **Problem:** Python prints `pvalue=np.float64(3.0576926692219362e-24)` for the same test, which is not mentioned, and the page never says what `e-16` or `e-05` means. A beginner on the Python tab sees a different number from the one quoted for R.
- **Where it really comes from:** output lines "p-value < 2.2e-16" (R) and "pvalue=np.float64(3.0576926692219362e-24)" (Python).
- **Proposed fix:** Prose, at line 113: "**p < 0.001** (R prints `< 2.2e-16`, Python `3.06e-24`; `e-24` means "move the decimal point 24 places to the left", so both are far below 0.001; R stops printing at 2.2e-16)".
- **Changes code:** no

---

## 11-predict-from-one.qmd

### 11-1 · Logistic ⚠️ box: "97 hours on average" and "17.2% from the model" exist only in the Prose guard · A
- **Where:** `en/catalog/11-predict-from-one.qmd:618`, section `#logistic-regression`, ⚠️ box
- **Text:** "The last band is open-ended: its patients waited 97 hours on average, so a straight line already predicts its higher rate (17.2% from the model, 18.2% observed)."
- **Problem:** This is the argument for why the straight-line model is adequate, and neither 97 nor 17.2% appears in any output. Only 18.2% is in the printed band table. Page 12's exercise 3 leans on the same claim.
- **Where it really comes from:** Prose guard lines 767 (`last_band`), 793 and 794 (`mean(hours_to_surgery[last_band])`, `mean(fitted(delay_model)[last_band])`).
- **Proposed fix:** Add a tabset inside the box after that sentence.

  R:
  ```r
  over_72 <- hip_fracture$hours_to_surgery > 72       # the open-ended last band
  mean(hip_fracture$hours_to_surgery[over_72])        # its mean wait, in hours
  100 * mean(fitted(delay_model)[over_72])            # death rate the model predicts for these patients, %
  100 * mean(hip_fracture$death_30d[over_72])         # death rate observed, %
  ```
  Python:
  ```python
  over_72 = hip_fracture["hours_to_surgery"] > 72     # the open-ended last band
  print(hip_fracture.loc[over_72, "hours_to_surgery"].mean())      # its mean wait, in hours
  print(100 * delay_model.predict(hip_fracture[over_72]).mean())   # death rate the model predicts for these patients, %
  print(100 * hip_fracture.loc[over_72, "death_30d"].mean())       # death rate observed, %
  ```
  (Outputs: 97.3; 17.2; 18.2. In Python use `predict()`, not `fittedvalues`, which is on the log-odds scale.)
- **Changes code:** yes

### 11-2 · "An ordinary least-squares line gives 0.43" is never fitted on the page · A
- **Where:** `en/catalog/11-predict-from-one.qmd:463`, section `#nonparametric-regression`, "Effect size and 95% CI"
- **Text:** "An ordinary least-squares line gives 0.43; the two would differ more if a few unusual patients pulled the least-squares line."
- **Problem:** No visible code fits a least-squares line to `koos_wide`.
- **Where it really comes from:** Prose guard line 760 (`koos_ls <- coef(lm(one_year ~ preop, data = koos_wide))`), checked at line 787.
- **Proposed fix:** Add a small tabset under the sentence. R: `coef(lm(one_year ~ preop, data = koos_wide))   # the least-squares line, for comparison`. Python: `print(stats.linregress(koos_wide["preop"], koos_wide["1yr"]).slope)   # the least-squares slope, for comparison` (0.428). Then "gives 0.43 (the `preop` coefficient)".
- **Changes code:** yes

### 11-3 · LOWESS "from about 70 to about 99" must be read off the plot · A
- **Where:** `en/catalog/11-predict-from-one.qmd:406`, section `#nonparametric-regression`, "Look at the data first"
- **Text:** "The LOWESS curve rises steadily from about 70 to about 99 across the range of pre-op scores."
- **Problem:** The curve's end values are only in the figure; the hidden agreement check and the guard read them from `smooth`, the reader cannot.
- **Where it really comes from:** hidden chunks at lines 396 to 404 and Prose guard line 785 (`smooth$y[1]`, `smooth$y[length(smooth$y)]`).
- **Proposed fix:** Print the two ends in the existing chunks. R: `smooth$y[c(1, length(smooth$y))]   # the curve's height at the lowest and highest pre-op score`. Python: `print(smooth[[0, -1], 1])   # the curve's height at the lowest and highest pre-op score` (70.1 and 98.6).
- **Changes code:** yes

### 11-4 · "BMI here runs from 18.0 to 44.5" is never printed · A
- **Where:** `en/catalog/11-predict-from-one.qmd:165`, section `#linear-regression`, ⚠️ box
- **Text:** "And BMI here runs from 18.0 to 44.5: don't use the line to predict outside that range."
- **Problem:** No output shows the range (Python computes `bmi_range` for the plot but does not print it). It can only be guessed from the x-axis.
- **Where it really comes from:** Prose guard line 774 (`range(cohort$bmi)`).
- **Proposed fix:** In "Look at the data first" add R `range(cohort$bmi)   # lowest and highest BMI in the data` and Python `print(bmi_range)   # lowest and highest BMI in the data` (the variable already exists).
- **Changes code:** yes

### 11-5 · "each knee appears up to four times" is not shown and not even guarded · A
- **Where:** `en/catalog/11-predict-from-one.qmd:316`, section `#nonlinear-regression`, ⚠️ box title (repeated at `12-predict-from-several.qmd:358`: "each joint contributes up to four related scores")
- **Text:** "⚠️ Watch out: each knee appears up to four times"
- **Problem:** The output gives 1146 scores and 330 knees (about 3.5 each), but nothing shows the maximum of four or names the four visits. The Prose guard has no check for it either. (I confirmed it from the data: 192 knees have 4 scores, 106 have 3, 28 have 2, 4 have 1; visits are preop, 6wk, 3mo, 1yr.)
- **Where it really comes from:** not computed anywhere.
- **Proposed fix:** Prose: "Each knee has up to four scores (pre-op, 6 weeks, 3 months and 1 year), so nonlinear least squares treats the 1146 scores ...". Optional code in "Look at the data first": R `count(koos, visit)   # scores at each visit`, Python `print(koos["visit"].value_counts())   # scores at each visit`. Add `max(table(koos$case_id)) == 4` to the guard.
- **Changes code:** no (prose version)

### 11-6 · Code comment "pre-op visits (1-27 days before surgery)" quotes an unshown range · A (minor)
- **Where:** `en/catalog/11-predict-from-one.qmd:200` (R) and `:222` (Python), section `#nonlinear-regression`
- **Text:** "# pre-op visits (1-27 days before surgery) count as day 0"
- **Problem:** The 1 and 27 are in no output. The range also uses a hyphen where the project rule asks for "to".
- **Where it really comes from:** Prose guard line 775 (`range(proms$visit_days[proms$visit == "preop"])`).
- **Proposed fix:** Simplest: shorten the comment to "# pre-op visits have negative days; count them as day 0". Or keep the numbers as "1 to 27 days" and print them: R `range(koos$visit_days[koos$visit == "preop"])`, Python `print(koos.loc[koos["visit"] == "preop", "visit_days"].agg(["min", "max"]))`.
- **Changes code:** yes (a comment is part of the chunk)

### 11-7 · "the 80 patients who had both sides operated on" · A
- **Where:** `en/catalog/11-predict-from-one.qmd:26`, opening 💡 box
- **Text / Problem / Fix:** identical to finding 10-3 (guard line 769 here).
- **Changes code:** no

### 11-8 · Half-gain CI "49 to 64 days" is printed in R only, and Python's own CI gives 48 to 64 · B
- **Where:** `en/catalog/11-predict-from-one.qmd:307` and `:313` (Results), section `#nonlinear-regression`, "Effect size and 95% CI"
- **Text:** "Half of the gain came by about 56 days, 8 weeks (95% CI 49 to 64 days)."
- **Problem:** R prints `log(2) * confint(recovery)["tau", ]` (49.2, 64.1). The Python tab prints only the point estimate 56.05. A Python reader who multiplies the printed τ limits (69.94, 91.79) by ln 2 gets 48.5 and 63.6, so "48 to 64", not the quoted 49. The 🔀 box gives both CIs for τ but not for the half-gain time.
- **Where it really comes from:** R output "49.19974 64.14121" (line 294); Python: not printed.
- **Proposed fix:** Add to the Python chunk after line 303: `print(np.log(2) * (estimates[2] - t_crit * standard_errors[2]), np.log(2) * (estimates[2] + t_crit * standard_errors[2]))   # its 95% CI` (48.5, 63.6), and extend the 🔀 box: "... τ's CI runs from 71.0 to 92.5 days in R and 69.9 to 91.8 in Python, so the half-gain CI is 49 to 64 days in R and 48 to 64 in Python."
- **Changes code:** yes

### 11-9 · Cox CI "1.09 to 1.48" looks wrong against R's printed 1.095 and 1.485 · B
- **Where:** `en/catalog/11-predict-from-one.qmd:728` (also `:735`, `:741`), section `#cox`, "Read the output"
- **Text:** "**lower .95 / upper .95 = 1.09 to 1.48:** the 95% CI"
- **Problem:** R prints `1.095` and `1.485`, already rounded. A reader who rounds those to two decimals gets 1.10 and 1.49 and thinks the page is wrong. The unrounded values (1.0946, 1.4847) are visible only in the Python output. The same applies in a small way to "Concordance = 0.67" from the printed 0.665 (line 731).
- **Where it really comes from:** R output "tibial_slope_deg 1.275 0.7844 1.095 1.485"; Python output "1.094569 1.484728".
- **Proposed fix:** Prose: "**lower .95 / upper .95 = 1.09 to 1.48:** the 95% CI, which excludes 1 (no difference). R prints 1.095 and 1.485, which are 1.0946 and 1.4847 already rounded (the Python output shows more digits), so don't round them a second time."
- **Changes code:** no

### 11-10 · "74 of 1,200" and "6.2%" need adding and dividing · B
- **Where:** `en/catalog/11-predict-from-one.qmd:546`, `:614` (Results), `:618`, `:856` (Solution 2), section `#logistic-regression`
- **Text:** "74 of 1,200 overall." / "Within 30 days, 74 of 1,200 patients died (6.2%)."
- **Problem:** The band table prints four `n` and four `deaths`; 74, 1,200 and 6.2% are their sums and ratio, shown nowhere. (1,200 can be found later as Python's "No. Observations".)
- **Where it really comes from:** Prose guard line 788.
- **Proposed fix:** Add after the band table: R `c(deaths = sum(hip_fracture$death_30d), patients = nrow(hip_fracture), percent = 100 * mean(hip_fracture$death_30d))   # all patients`; Python `print(hip_fracture["death_30d"].sum(), len(hip_fracture), 100 * hip_fracture["death_30d"].mean())   # deaths, patients, percent` (74, 1200, 6.17). Prose-only alternative: "74 of 1,200 overall (the `deaths` and `n` columns added up; 74 / 1,200 = 6.2%)."
- **Changes code:** yes; no for the alternative

### 11-11 · "6.8 more minutes (95% CI 5.8 to 7.9)" per 5 kg/m²: the multiplication is not shown · B
- **Where:** `en/catalog/11-predict-from-one.qmd:155` and `:161` (Results), section `#linear-regression`
- **Text:** "Scale it to a difference that matters clinically: 5 kg/m² of BMI goes with 6.8 more minutes (95% CI 5.8 to 7.9)."
- **Problem:** The page does not say that the slope and both CI limits are multiplied by 5, or that the unrounded values are used (5 × 1.37 = 6.85 would round to 6.9 for some readers; 5 × 1.3680 = 6.84).
- **Where it really comes from:** Prose guard line 773.
- **Proposed fix:** Prose: "Multiply the slope and both ends of its CI by 5: 5 × 1.368 = 6.8 more minutes (95% CI 5 × 1.151 = 5.8 to 5 × 1.585 = 7.9)." Code alternative: R `5 * coef(bmi_model)[["bmi"]]` and `5 * confint(bmi_model)["bmi", ]`; Python `print(5 * bmi_model.params["bmi"], 5 * bmi_model.conf_int().loc["bmi"].values)`.
- **Changes code:** no

### 11-12 · "5° steeper carries 3.37 times the hazard (95% CI 1.57 to 7.21)": the power is not shown · B
- **Where:** `en/catalog/11-predict-from-one.qmd:735`, section `#cox`, "Effect size and 95% CI"
- **Text:** "Hazard ratios multiply: a slope 5° steeper carries 3.37 times the hazard (95% CI 1.57 to 7.21), computed from the unrounded hazard ratio."
- **Problem:** "Multiply" hints at the method but the page never says "raise to the fifth power", and the reader has to go to the Python output for unrounded limits.
- **Where it really comes from:** Prose guard lines 806 and 807 (`exp(5 * coef(slope_cox))`, `exp(5 * confint(slope_cox))`).
- **Proposed fix:** Show it. R: `exp(5 * coef(slope_cox))   # hazard ratio for 5° more slope` and `exp(5 * confint(slope_cox))   # its 95% CI`. Python: `print(slope_cox.summary[["exp(coef)", "exp(coef) lower 95%", "exp(coef) upper 95%"]] ** 5)   # hazard ratio for 5° more slope, with its 95% CI`. Prose-only alternative: "the hazard ratio for 5° is the per-degree ratio to the fifth power: 1.2748⁵ = 3.37 (95% CI 1.0946⁵ = 1.57 to 1.4847⁵ = 7.21)."
- **Changes code:** yes; no for the alternative

### 11-13 · Exercise 3: "about 37 days" is printed only in Python, the CIs only in R · B
- **Where:** `en/catalog/11-predict-from-one.qmd:915`, `#exercises`, Solution 3 (code at `:897` to `:900` and `:910`)
- **Text:** "half of the change was reached at about 37 days (95% CI 33 to 41)" and all three CIs in the sentence
- **Problem:** R prints τ = 53.37 and the CI of the half-gain time but never ln 2 × τ = 37.0. Python prints 36.996 but only standard errors, no CI for anything. Neither tab on its own supports the whole Results sentence.
- **Where it really comes from:** R output "33.06771 41.26295"; Python output "36.996119141613114"; guard lines 815 and 816.
- **Proposed fix:** R: add `log(2) * coef(hip_recovery)[["tau"]]   # days to half of the eventual gain` before the CI line. Python: add the CI lines used in the main section:
  ```python
  hip_errors = np.sqrt(np.diag(hip_covariance))
  t_crit = stats.t.ppf(0.975, df=len(hoos) - 3)   # 3 parameters
  print(hip_estimates - t_crit * hip_errors, hip_estimates + t_crit * hip_errors)   # 95% CIs: plateau, start, tau
  ```
  (these give 86.3 to 89.4, 44.2 to 46.9, and for the half-gain time 33 to 41 after × ln 2, the same as R after rounding), and add "The CIs are R's profile CIs" as Solution 2 does.
- **Changes code:** yes

### 11-14 · Exercise 1: p < 0.001 is not in the Python output · B
- **Where:** `en/catalog/11-predict-from-one.qmd:847`, `#exercises`, Solution 1 (Python code at `:843`)
- **Text:** "(95% CI 0.11 to 0.38; p < 0.001; R² = 0.02)"
- **Problem:** Python prints the coefficients, CI and R² but no p-value. R prints it as `5.910612e-04`, with no hint that this is 0.0006.
- **Where it really comes from:** R output "age 0.2436391 0.07053491 3.454163 5.910612e-04".
- **Proposed fix:** Python: `print(age_time.params, age_time.conf_int(), age_time.pvalues, age_time.rsquared, sep="\n")`. Prose under the Results: "p = 5.9e-04 in the output is 0.00059, so p < 0.001."
- **Changes code:** yes (Python only)

### 11-15 · Cox: counts and the overall test are not tied to where they are printed · B (minor)
- **Where:** `en/catalog/11-predict-from-one.qmd:686`, `:730`, `:741`, section `#cox`
- **Text:** "11 of the 73 reconstructions with a slope of 12° or more failed, and 20 of the 277 with a smaller slope." / "Likelihood ratio test = 10.1 on 1 df, p = 0.002" / "with 31 failures in 350 reconstructions"
- **Problem:** The 11/73 and 20/277 are readable only in the risk table under the plot (At Risk at year 0, Events at year 6), which the sentence does not mention. The 350, 31 and the test's df and p are in R's summary only; the Python tab prints the hazard ratio table and the bare statistic 10.0756.
- **Where it really comes from:** figure risk tables; R output "n= 350, number of events= 31" and "Likelihood ratio test= 10.08 on 1 df, p=0.002".
- **Proposed fix:** Prose at 686: "The table under the plot gives the counts: at year 0, 73 and 277 reconstructions at risk; by year 6, 11 and 20 failures." Python at line 705: `lr_test = slope_cox.log_likelihood_ratio_test()` then `print(lr_test.test_statistic, lr_test.p_value)   # overall likelihood ratio test` and `print(len(acl), acl["graft_failure"].sum())   # reconstructions, failures`.
- **Changes code:** yes (Python); the first part is prose only

### 11-16 · "37 of them (15.0%)": the percentage is not printed · B (minor)
- **Where:** `en/catalog/11-predict-from-one.qmd:406` and `:469` (Results), section `#nonparametric-regression`
- **Text:** "246 knees have both scores, and 37 of them (15.0%) score the maximum of 100 at 1 year."
- **Problem:** Output shows 246 and 37; the division is left to the reader.
- **Where it really comes from:** Prose guard line 784.
- **Proposed fix:** Prose: "37 of them (37 / 246 = 15.0%)" in the teaching sentence.
- **Changes code:** no

### 11-17 · "63% of their eventual gain" after τ days has no derivation · B (minor)
- **Where:** `en/catalog/11-predict-from-one.qmd:184`, section `#nonlinear-regression`, "When to use it"
- **Text:** "After τ days patients have made 63% of their eventual gain, and half of it after τ × ln 2 ≈ 0.69 τ days."
- **Problem:** The half-gain figure is derived (ln 2 ≈ 0.69); the 63% is not.
- **Where it really comes from:** Prose guard line 782 (`1 - exp(-1)`).
- **Proposed fix:** Prose: "After τ days patients have made 63% of their eventual gain (1 − e⁻¹ = 0.63), ..."
- **Changes code:** no

### 11-18 · "With 31 failures, this model can take about three terms": the rule is not stated here · B (minor)
- **Where:** `en/catalog/11-predict-from-one.qmd:745`, section `#cox`, ⚠️ box
- **Text:** "With 31 failures, this model can take about three terms ([page 14](...))."
- **Problem:** The 10-events-per-term rule that turns 31 into 3 is on other pages; this section must stand alone.
- **Where it really comes from:** Prose guard line 796 (`31 %/% 10 == 3`).
- **Proposed fix:** Prose: "At about 10 failures per term, 31 failures allow about three terms (page 14)."
- **Changes code:** no

### 11-19 · Regression summaries: most of the printed output is never explained, and p is quoted in a form neither tab prints · C
- **Where:** `en/catalog/11-predict-from-one.qmd:116` to `:123`, section `#linear-regression`, "Read the output" (the same pattern at `:581` to `:586`)
- **Text:** "**Std. Error 0.11, t = 12.4, p < 0.001:**"
- **Problem:** This is the first full `summary()` on the regression pages. R prints `<2e-16` and Python `0.000`; the bullet says "p < 0.001" without tying it to either. A beginner also faces Residuals quartiles, significance stars, adjusted R², the F-statistic (R) and Omnibus, Durbin-Watson, Jarque-Bera, Cond. No., AIC, BIC (Python) with no word on whether they matter.
- **Where it really comes from:** output lines "bmi 1.3680 0.1105 12.38 <2e-16 ***" and "bmi 1.3680 0.110 12.385 0.000 1.151 1.585".
- **Proposed fix:** Prose: "**Std. Error 0.11, t = 12.4, p < 0.001** (R prints `<2e-16`, Python `0.000`): ..." and one closing bullet: "**Everything else** (R's residual quartiles, stars and F-statistic; Python's Omnibus, Durbin-Watson, Jarque-Bera, AIC and BIC): you can ignore it for a one-predictor model. With one predictor the F test repeats the slope's test."
- **Changes code:** no

### 11-20 · Logistic: "Null and residual deviance (R) or LLR p-value (Python)" leaves the R reader without the link · C
- **Where:** `en/catalog/11-predict-from-one.qmd:586`, section `#logistic-regression`, "Read the output"
- **Text:** "**Null and residual deviance** (R) or **LLR p-value** (Python): how much better the model fits with time to surgery than without it."
- **Problem:** R prints two deviances and no p-value; Python prints a p-value and no deviance. The bullet treats them as the same thing without saying how one becomes the other, so a beginner cannot use either.
- **Where it really comes from:** R output "Null deviance: 555.67 ... Residual deviance: 543.20"; Python output "LLR p-value: 0.0004136".
- **Proposed fix:** Prose: "**Null and residual deviance** (R): the misfit without and with time to surgery. Their difference, 555.67 − 543.20 = 12.47 on 1 degree of freedom, is the likelihood ratio test of the model; Python prints its p-value as **LLR p-value** (0.0004). With one predictor it says the same as the z test above."
- **Changes code:** no

---

## 12-predict-from-several.qmd

### 12-1 · Logistic ⚠️ box: "15 of 350" and "all 6 patients whose graft failed in the first year" are never shown · A
- **Where:** `en/catalog/12-predict-from-several.qmd:488`, section `#multiple-logistic-regression`, ⚠️ box (the 15 is also the premise of exercise 2, `:730`, and its Solution never counts it)
- **Text:** "... but only one or two for graft failure within 2 years (15 of 350; exercise 2). ... all 6 patients whose graft failed in the first year had not returned to sport at 12 months, so a failure can't predict return to sport here, it's part of the outcome."
- **Problem:** Neither 15 nor 6 (nor the "none returned") appears in any output on the page, including the Solution of exercise 2.
- **Where it really comes from:** Prose guard lines 663 to 665.
- **Proposed fix:** Add a tabset inside the box.

  R:
  ```r
  sum(acl$failure_2y)                                                 # grafts that failed within 2 years
  early_failure <- acl$graft_failure == 1 & acl$followup_years <= 1   # failed in the first year
  table(early_failure, returned = acl$rts_12mo)                       # did they return to sport?
  ```
  Python:
  ```python
  print(acl["failure_2y"].sum())                                              # grafts that failed within 2 years
  early_failure = (acl["graft_failure"] == 1) & (acl["followup_years"] <= 1)   # failed in the first year
  print(pd.crosstab(early_failure, acl["rts_12mo"]))                          # did they return to sport?
  ```
  (Outputs: 15; the TRUE row reads 6 and 0.) In Solution 2, also add `sum(acl$failure_2y)` / `print(acl["failure_2y"].sum())` so the "15 events" is visible there.
- **Changes code:** yes

### 12-2 · lifelines' default result "0.82915" is computed only in the Prose guard · A (low priority)
- **Where:** `en/catalog/12-predict-from-several.qmd:611`, section `#cox`, 🔀 box
- **Text:** "lifelines' default convergence rule stops a little early (a hazard ratio of 0.82915 for implant B instead of 0.82912)"
- **Problem:** The page only runs the tightened fit (Python prints 0.829116; R's coefficient table prints 0.82912). The default fit that gives 0.82915 is run nowhere the reader can see.
- **Where it really comes from:** Prose guard line 677 (a `reticulate::py_eval()` of the default fit).
- **Proposed fix:** Prose only: "(a hazard ratio of 0.82915 for implant B instead of the 0.82912 in R's `exp(coef)` column; rerun the Python fit without `fit_options` to see it)". Code alternative, Python tab only: `print(CoxPHFitter().fit(cohort[["followup_years", "revised", "implant", "age_10", "sex", "bmi_5"]], duration_col="followup_years", event_col="revised", formula="implant + age_10 + sex + bmi_5").hazard_ratios_["implant[T.B]"])   # the default: stops a little early`.
- **Changes code:** no (prose version)

### 12-3 · "the 80 patients who had both sides operated on" · A
- **Where:** `en/catalog/12-predict-from-several.qmd:26`, opening 💡 box
- **Text / Problem / Fix:** identical to finding 10-3 (guard line 637 here).
- **Changes code:** no

### 12-4 · Python prints p = 0.001 for both grafts; the text says p < 0.001 · B
- **Where:** `en/catalog/12-predict-from-several.qmd:456`, section `#multiple-logistic-regression`, "Read the output"
- **Text:** "**age_10: p = 0.031**, **tegner_preinjury** and **both grafts: p < 0.001:**"
- **Problem:** R prints 0.000746 and 0.000965, which support "p < 0.001". The statsmodels table rounds both to `0.001`, so a reader on the Python tab sees the text disagree with the output, with no explanation.
- **Where it really comes from:** R output "grafthamstring ... 0.000746", "graftquadriceps ... 0.000965"; Python output "graft[T.hamstring] ... 0.001", "graft[T.quadriceps] ... 0.001".
- **Proposed fix:** Prose: "... **both grafts: p < 0.001** (R prints 0.000746 and 0.000965; Python's table rounds them to 0.001, and `rts_model.pvalues` shows the unrounded values):". Optionally add `print(rts_model.pvalues)   # unrounded p-values` to the Python chunk.
- **Changes code:** no (yes if the optional line is added)

### 12-5 · Python prints proportions where the text quotes percentages · B
- **Where:** `en/catalog/12-predict-from-several.qmd:412` (code `:407`), section `#multiple-logistic-regression`; and `:542` (code `:538`), section `#cox`
- **Text:** "more had a BPTB graft (48.6% against 25.4%)" / "sex (42% to 44% men)"
- **Problem:** R's columns are `bptb_percent` (48.6, 25.4) and `male_percent` (42.7, 42.4, 43.8). Python's are `bptb` (0.4855, 0.2542) and `male` (0.4268, 0.4240, 0.4380): a different scale, never mentioned.
- **Where it really comes from:** Python output "0  30.655367  5.988701  0.254237" and "A  246  25  65.243902  0.426829  30.626016".
- **Proposed fix:** Make Python match R. Line 405: `acl["bptb_percent"] = 100 * (acl["graft"] == "BPTB")   # 100 for BPTB, 0 otherwise: the mean is the percentage` and use `"bptb_percent"` in line 407. Cox section: `cohort["male_percent"] = 100 * (cohort["sex"] == "Male")` and `male_percent=("male_percent", "mean")` in line 538. Prose-only alternative: add "(Python prints these as proportions: 0.486 is 48.6%)" at both places.
- **Changes code:** yes; no for the alternative

### 12-6 · "a difference of 19 days (95% CI 11 to 28)": 19 is not printed, and the CI is in R only · B
- **Where:** `en/catalog/12-predict-from-several.qmd:348`, section `#multiple-nonlinear-regression`, "Effect size and 95% CI" (code `:334` to `:344`)
- **Text:** "Half of the eventual gain took about 37 days after a hip replacement and 56 days after a knee replacement, a difference of 19 days (95% CI 11 to 28)."
- **Problem:** Both tabs print 37.0 and 56.05 but not their difference. R prints the CI of the difference (11.03, 27.83); the Python tab does not print one.
- **Where it really comes from:** R output "11.03455 27.82688"; Prose guard line 651 (`log(2) * tau_diff == 19`).
- **Proposed fix:** R: `log(2) * coef(joint_recovery)[["tau_diff"]]   # difference in days to half the gain` before line 336 (19.05). Python: `print(np.log(2) * estimates[5], np.log(2) * (estimates[5] - t_crit * standard_errors[5]), np.log(2) * (estimates[5] + t_crit * standard_errors[5]))   # the difference and its 95% CI` (19.05, 10.6, 27.5: also 11 to 28 after rounding).
- **Changes code:** yes

### 12-7 · The "before adjustment" numbers (1.37 and 3.07) live on other pages · B
- **Where:** `en/catalog/12-predict-from-several.qmd:134`, section `#multiple-linear-regression`; `:588` and `:589`, section `#cox`
- **Text:** "BMI's coefficient fell only a little after adjustment, from 1.37 minutes per kg/m² on its own ([page 11](...)) to 1.27" / "almost the same as without adjustment (3.07, [page 8](...))" / "imprecise, as before"
- **Problem:** The comparison "adjusted vs unadjusted" is the point of each section, but the unadjusted value is not on this page. A reader who jumped here from the decision table has not seen page 11 or page 8, and "as before" has nothing to refer to. (Both pages do print the values.)
- **Where it really comes from:** Prose guard lines 644 and 627/676 refit the unadjusted models.
- **Proposed fix:** Show the unadjusted fit next to the adjusted one. Linear, under "Effect size and 95% CI": R `coef(lm(op_time_min ~ bmi, data = cohort))   # BMI on its own, for comparison`; Python `print(smf.ols("op_time_min ~ bmi", data=cohort).fit().params)   # BMI on its own, for comparison`. Cox: R `exp(coef(coxph(Surv(followup_years, revised) ~ implant, data = cohort)))   # implant on its own, for comparison`; Python `print(CoxPHFitter().fit(cohort[["followup_years", "revised", "implant"]], duration_col="followup_years", event_col="revised", formula="implant", fit_options={"precision": 1e-9}).hazard_ratios_)   # implant on its own, for comparison`. Replace "imprecise, as before" with "imprecise: the CI runs from about half to one and a half times the hazard". Prose-only alternative: keep the links and add "(the `bmi` row of that page's output)" / "(the `exp(coef)` column there)".
- **Changes code:** yes; no for the alternative

### 12-8 · "173 of 350 reconstructions (49.4%)": total and percentage not printed · B (minor)
- **Where:** `en/catalog/12-predict-from-several.qmd:484` (Results), section `#multiple-logistic-regression`
- **Text:** "At 12 months, 173 of 350 reconstructions (49.4%) were followed by a return to the pre-injury sport."
- **Problem:** The output gives 177 and 173; 350 and 49.4% are left to the reader.
- **Where it really comes from:** Prose guard line 654.
- **Proposed fix:** Prose, in the sentence under the table (line 412): "The 173 who returned (of 177 + 173 = 350; 49.4%) were younger ..."
- **Changes code:** no

### 12-9 · Exercise 3: "only 8 of the 74 deaths" and "already predicts the rate after 72 hours" rest on page 11 · B
- **Where:** `en/catalog/12-predict-from-several.qmd:794`, `#exercises`, Solution 3
- **Text:** "The spline adds nothing clear, because the straight line already predicts the rate after 72 hours. And only 8 of the 74 deaths came that late, too few to pin down a curve."
- **Problem:** Neither 8 nor 74 is in this Solution's output, and "already predicts" is page 11's 17.2% vs 18.2%, which is itself untraceable there (finding 11-1).
- **Where it really comes from:** Prose guard lines 688 and 689; page 11's band table for the 8.
- **Proposed fix:** Prose: "... because the straight line already predicts the rate after 72 hours (17.2% predicted, 18.2% observed; [page 11](11-predict-from-one.qmd#logistic-regression)). And only 8 of the 74 deaths came that late (the band table on page 11), too few to pin down a curve." This holds once 11-1 is fixed.
- **Changes code:** no

### 12-10 · Three of five odds-ratio CIs differ in Python; the 🔀 box gives only one · B (minor)
- **Where:** `en/catalog/12-predict-from-several.qmd:478`, `:484`, `:493`, section `#multiple-logistic-regression`
- **Text:** "With few events the two can differ in the second decimal: for the quadriceps graft, 0.17 to 0.63 in R and 0.17 to 0.64 in Python."
- **Problem:** A Python reader also gets 0.52 to 0.97 for age (text: 0.51 to 0.96) and 1.22 to 1.66 for Tegner (text: 1.22 to 1.67). The box reads as if only the quadriceps CI differs.
- **Where it really comes from:** Python output "age_10 0.707688 0.517341 0.968070", "tegner_preinjury 1.422974 1.220724 1.658731".
- **Proposed fix:** Prose: "... the two can differ in the second decimal. Python gives 0.52 to 0.97 for age, 1.22 to 1.66 for Tegner level and 0.17 to 0.64 for the quadriceps graft; the text above quotes R's."
- **Changes code:** no

### 12-11 · Model-comparison tables: the reported df and χ² are never tied to their columns · B (minor)
- **Where:** `en/catalog/12-predict-from-several.qmd:323` and `:354` (Results), section `#multiple-nonlinear-regression`; `:725` (Solution 1); `:792` (Solution 3)
- **Text:** "**F = 0.58, p = 0.562:**" then "F = 0.58 (df = 2 and 593, p = 0.562)"; "a likelihood ratio χ² of 2.45 (df = 2, p = 0.294)"
- **Problem:** "Read the output" names only F and p. The Results then quote "df = 2 and 593", which come from `Df` and `Res.Df` (R) or `df_diff` and `df_resid` (Python), and in Solution 3 R labels the χ² "Deviance". The second row of each table and the columns `RSS`/`ssr` and `Sum of Sq`/`ss_diff` are not explained.
- **Where it really comes from:** output lines "2 593 118504 2 230.57 0.5769 0.5619" and "2 1196 540.75 2 2.448 0.294".
- **Proposed fix:** Prose at 323: "**F = 0.58, p = 0.562** (second row; `Pr(>F)`): ... The spline uses 2 more degrees of freedom than the straight line (`Df`, or `df_diff` in Python) and leaves 593 (`Res.Df`, `df_resid`): the 'df = 2 and 593' of the Results." In Solution 3: "R calls the likelihood ratio χ² `Deviance`."
- **Changes code:** no

### 12-12 · Cox overall test: df and p are in R's output only · B (minor)
- **Where:** `en/catalog/12-predict-from-several.qmd:592` (Python code `:563`), section `#cox`, "Read the output"
- **Text:** "**Likelihood ratio test = 39.1 on 5 df, p < 0.001:**"
- **Problem:** The Python tab prints only the statistic (39.139). R prints "on 5 df, p=2e-07", and the text does not say that `2e-07` is the p < 0.001.
- **Where it really comes from:** R output "Likelihood ratio test= 39.14 on 5 df, p=2e-07".
- **Proposed fix:** Python: `lr_test = adjusted_cox.log_likelihood_ratio_test()` then `print(lr_test.test_statistic, lr_test.degrees_freedom, lr_test.p_value)   # overall likelihood ratio test`. Prose: "(R prints `p=2e-07`)".
- **Changes code:** yes (Python only)

### 12-13 · The spline is run before it is explained, inside a section about something else · C
- **Where:** `en/catalog/12-predict-from-several.qmd:277` to `:300`, section `#multiple-nonlinear-regression`, "Run it"
- **Text:** "When you don't know the shape, use a spline instead. Here a natural cubic spline lets BMI's effect on operative time bend ..."
- **Problem:** The section's question is "Do hips recover faster than knees?", and halfway through "Run it" it switches to a different dataset and question (BMI and operative time) with no heading or question of its own. The Python line `cr(bmi, knots=bmi_knots, lower_bound=bmi_low, upper_bound=bmi_high, constraints='center')` has four arguments a beginner cannot guess; the 🔀 box explains the knots but nothing explains `constraints='center'` or what `df = 3` buys.
- **Where it really comes from:** n/a (explanation gap).
- **Proposed fix:** Prose before the spline tabset: "**A second question, for the second case (shape unknown):** is BMI's effect on operative time a straight line? `df = 3` gives BMI three coefficients instead of the straight line's one, so the test below has 2 extra degrees of freedom." And one sentence in the 🔀 box: "`constraints='center'` removes one column from patsy's spline so that it doesn't repeat the model's intercept, as `ns()` does by default; both splines then use 3 degrees of freedom."
- **Changes code:** no

---

## Pages with nothing to report

None. Every page has findings.

Sections with nothing to report: page 10 `#spearman` apart from 10-5; page 12 `#multiple-linear-regression` apart from 12-7 (every coefficient, CI, R² and group mean quoted there is printed in both tabs); page 12 exercise 1.

## Not checked

- **Statements read off figures** ("the Budin reading runs a little above CT at low torsion and below it at high torsion", "an even band, with no curve and no funnel shape", "the scores climb steeply over the first 3 months"). I opened only the two Cox risk-table figures on page 11; the other qualitative plot descriptions carry no quoted numbers and were not compared with the images.
- **Claims about software behavior**, which no output on the page can show and which I did not test: R's `cor.test()` exact-test threshold of 1290 (10:283), "deming 1.4-1 misapplies its tie correction; mblm's CI is far too narrow" (11:478), statsmodels' `lowess()` default `delta` (11:480), where `ns(df = 3)` places knots (12:363).
- **Page 3 `#paired`** (for finding 10-3): I only searched its source for `patient_id` and found the count of 80 in its Prose guard, not in visible code. I did not read that page's output.
- **German and French pages**: out of scope; line numbers and fixes refer to the English sources only.
- **Hidden agreement checks** were read to see what they compute, not re-run.
