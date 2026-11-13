# Audit findings: en/beyond (pages 15, 16, 17)

Checked against the frozen output in `_freeze/en/beyond/<page>/execute-results/html.json` (dumped to `work-beyond/`). Every hidden number below was recomputed read-only from `data/` in R and, where a Python fix is proposed, in Python; the proposed lines were run and give the values quoted. These pages have no catalog steps, so "step" names the paragraph instead.

Any fix marked "Changes code: yes" adds an R/Python pair, so it also needs a hidden `check_agree()` pair (rule 4), the same change in `de/` and `fr/`, and a re-render of all three pages.

## 15-post-hoc.qmd

### 15-1 · "About 20%" false-positive chance for four groups · A
- **Where:** `en/beyond/15-post-hoc.qmd:86`, section `#why-adjust`, paragraph after the first tabset
- **Text:** "Pairwise comparisons aren't independent, because each group appears in three of the six pairs, so for four groups of equal size the chance is a little lower: about 20%. That's still four times the 5% you meant to allow."
- **Problem:** The printed table gives only the independent-tests figures (0.26, 0.64). Nothing visible produces 20%, and the prose gives no way to get it.
- **Where it really comes from:** Prose guard, line 611: `1 - ptukey(qnorm(0.975) * sqrt(2), nmeans = 4, df = Inf)` = 0.2033.
- **Proposed fix:** Add one line to each tab of the first tabset, after the table, and one sentence ("At least one of the six tests passes p < 0.05 whenever the gap between the highest and the lowest group mean is large enough; the last line computes that chance: 0.20").
  - R: `1 - ptukey(qnorm(0.975) * sqrt(2), nmeans = 4, df = Inf)   # four equal groups, six pairwise tests: chance that at least one gives p < 0.05`
  - Python: `print(1 - stats.studentized_range.cdf(stats.norm.ppf(0.975) * np.sqrt(2), 4, np.inf))   # four equal groups, six pairwise tests: chance that at least one gives p < 0.05`
  - Both print 0.2033 (tested; `stats` and `np` are already imported in that chunk).
- **Changes code:** yes

### 15-2 · Walking-aid use "rose", "fell", "below its pre-op level"; n = 328 · A
- **Where:** `en/beyond/15-post-hoc.qmd:445` and `:493`, section `#after-cochran-q`, intro and paragraph after the tabset
- **Text:** "walking-aid use changed over the year in 328 patients assessed at all four visits" and "Use rose from pre-op to 6 weeks and fell at each visit after that; by 3 months it was already below its pre-op level (adjusted p = 0.005), and by 1 year lower still."
- **Problem:** The output is six McNemar p-values and nothing else. A p-value has no direction, so "rose", "fell" and "below" cannot be traced, and no percentage is given. The 328 is not printed in either tab (the `n1 = 328` three sections earlier is for a different variable). The 0.005 is printed only as `4.66e- 3`.
- **Where it really comes from:** Prose guard, lines 631 to 632: `nrow(aid) == 328` and an ordering check on `colMeans(aid[, c("preop", "3mo", "1yr")])`. The rise from pre-op to 6 weeks is not guarded at all. Actual values: 114, 194, 80 and 34 users, or 34.8%, 59.1%, 24.4% and 10.4%.
- **Proposed fix:** Add two lines to each tab, before the loop, and quote the percentages.
  - R: `nrow(aid)   # patients assessed at all four visits` and `round(100 * colMeans(aid[, c("preop", "6wk", "3mo", "1yr")]), 1)   # % using a walking aid at each visit`
  - Python: `print(len(aid))   # patients assessed at all four visits` and `print((100 * aid[["preop", "6wk", "3mo", "1yr"]].mean()).round(1))   # % using a walking aid at each visit`
  - Prose: "34.8% of patients used a walking aid before surgery, 59.1% at 6 weeks, 24.4% at 3 months and 10.4% at 1 year. Every pair of visits differs after adjustment (the `p_holm` column). The largest adjusted p-value is pre-op vs 3 months: 0.005, printed as `4.66e-3`."
- **Changes code:** yes

### 15-3 · "The SDs are similar (8.7 to 9.3 years)" and "the two small classes" · A
- **Where:** `en/beyond/15-post-hoc.qmd:205`, section `#after-anova`, paragraph after the bullets
- **Text:** "Both CIs include 0, and both comparisons involve one of the two small classes. The SDs are similar (8.7 to 9.3 years), so Games-Howell reaches the same conclusions."
- **Problem:** No SD is printed anywhere on the page, and the class sizes first appear one section later (the Dunn table). The SDs are the reason given for choosing Tukey over Games-Howell, so the reader cannot check the choice.
- **Where it really comes from:** Prose guard, lines 597 and 614: `asa_sd <- tapply(cohort$age, cohort$asa, sd)`.
- **Proposed fix:** Open both tabs with a group summary (this also gives the section a "look at the data first" step).
  - R: `cohort |> group_by(asa) |> summarise(n = n(), mean = mean(age), sd = sd(age))   # look first: group sizes, means and spreads`
  - Python: `print(cohort.groupby("asa")["age"].agg(["count", "mean", "std"]).round(2))   # look first: group sizes, means and spreads`
  - Prints n = 36, 300, 246, 18 and SD = 8.66, 9.08, 8.77, 9.31. Prose: "The SDs are similar (8.7 to 9.3 years, the `sd` column) ... one of the two small classes (ASA 1, n = 36; ASA 4, n = 18)."
- **Changes code:** yes

### 15-4 · F(3, 596) = 23.9 in two Results sentences · A
- **Where:** `en/beyond/15-post-hoc.qmd:209` (section `#after-anova`, Results) and `:587` (section `#planned-comparisons`, Results)
- **Text:** "Across ASA classes, one-way ANOVA gave F(3, 596) = 23.9 (p < 0.001)."
- **Problem:** `age_anova` is fitted in the R tab but never printed, and the Python tab has no ANOVA at all. The number is on page 8, but neither Results sentence says so, and the second one is ten sections away from the only link to page 8.
- **Where it really comes from:** Prose guard, lines 599 and 620: `age_f <- summary(age_anova)[[1]]`.
- **Proposed fix:** Print the table in both tabs, as page 8 does.
  - R: `summary(age_anova)   # the overall test: F on 3 and 596 degrees of freedom`
  - Python: `print(pg.anova(data=cohort, dv="age", between="asa"))   # the overall test: F, with ddof1 = 3 and ddof2 = 596`
  - Cheaper, prose only: a sentence before the first blockquote, "The F statistic in the Results sentence is the overall test from [page 8](../catalog/08-three-plus-unmatched.qmd#one-way-anova)", and the same half-sentence before the second.
- **Changes code:** yes (or no, with the prose-only version)

### 15-5 · Overall log-rank χ² = 33.5 (df = 2) · A
- **Where:** `en/beyond/15-post-hoc.qmd:556`, section `#after-log-rank`, Results
- **Text:** "The log-rank test for revision-free survival across implants gave χ² = 33.5 (df = 2, p < 0.001)."
- **Problem:** The section prints only the three pairwise tests (χ² = 0.414, 20.5, 24.7). The overall statistic is not on the page.
- **Where it really comes from:** Prose guard, line 634: `survdiff(Surv(followup_years, revised) ~ implant, data = cohort)$chisq`. Page 13 prints it.
- **Proposed fix:**
  - R, first line of the chunk: `survdiff(Surv(followup_years, revised) ~ implant, data = cohort)   # the overall log-rank test, as on page 13`
  - Python: import `multivariate_logrank_test` beside `pairwise_logrank_test` in the first chunk, then `overall_logrank = multivariate_logrank_test(cohort["followup_years"], cohort["implant"], cohort["revised"])` and `print(overall_logrank.test_statistic, overall_logrank.p_value)   # chi-square on 2 df, p-value` (prints 33.47, 5.4e-08).
  - Cheaper, prose only: "The overall statistic in the Results sentence is from [page 13](../survival/13-kaplan-meier.qmd#log-rank)."
- **Changes code:** yes (or no, with the prose-only version)

### 15-6 · "Two of the expected counts are below 5" · A
- **Where:** `en/beyond/15-post-hoc.qmd:275`, section `#after-chi-square`, intro
- **Text:** "Two of the expected counts are below 5, too few for the chi-square test (page 8), so the overall test is Fisher's exact test too:"
- **Problem:** Only the observed table is printed. The expected counts, which decide the choice of test, are never shown.
- **Where it really comes from:** Prose guard, line 625: `sum(suppressWarnings(chisq.test(complications))$expected < 5) == 2`. The two are 3.06 (ASA 1) and 1.53 (ASA 4).
- **Proposed fix:** Show them the way page 8's exercise 3 does.
  - R: `chisq.test(complications)$expected   # two expected counts are below 5` (the chunk then needs `#| warning: false`, because R warns "Chi-squared approximation may be incorrect")
  - Python: `print(stats.chi2_contingency(complications).expected_freq.round(2))   # two expected counts are below 5`
  - Prose: "Two of the expected counts are below 5 (3.06 in ASA 1 and 1.53 in ASA 4) ..."
- **Changes code:** yes

### 15-7 · "the 80 patients who had both sides operated on" · A (low priority)
- **Where:** `en/beyond/15-post-hoc.qmd:25`, callout "How this page works"
- **Text:** "the joint replacement examples use every case, including the 80 patients who had both sides operated on."
- **Problem:** A description of the data, not a result, but nothing on the page shows the 80 and there is no link.
- **Where it really comes from:** Prose guard, line 609: `sum(table(cohort$patient_id) == 2) == 80`. Page 3 `#paired` states the same figure.
- **Proposed fix:** Add the link page 8 already uses: "... operated on ([page 3](../foundations/03-distributions.qmd#paired))."
- **Changes code:** no

### 15-8 · PROMIS "improved between each visit", "changes this large": no means shown · B
- **Where:** `en/beyond/15-post-hoc.qmd:366`, section `#after-repeated-measures-anova`, paragraph after the tabset
- **Text:** "PROMIS physical function improved between each visit and the next, from pre-op to 6 weeks (t = 8.0) through to 3 months and 1 year (t = 7.5 for the last step). With 328 patients and changes this large, the adjustment changes nothing."
- **Problem:** The output holds t statistics and p-values only. The direction can be read only from the sign of R's `statistic` (−7.98: group1 minus group2), which the prose never explains, and the box below tells readers to ignore the signs ("Compare their sizes"). "Changes this large" has no number behind it. R prints −7.98 and −7.51; the prose says 8.0 and 7.5 without saying the sign was dropped.
- **Where it really comes from:** The means are on page 9 only (36.1, 39.4, 44.9, 48.2). Line 629 of the guard checks `abs(pf_pairs$statistic[c(1, 6)])`.
- **Proposed fix:** Print the means in both tabs and quote them.
  - R: `pf |> group_by(visit) |> summarise(mean = mean(promis_pf))   # mean score at each visit`
  - Python: `print(pf.groupby("visit")["promis_pf"].mean().round(1)[["preop", "6wk", "3mo", "1yr"]])   # mean score at each visit`
  - Prose: "The mean T-score was 36.1 before surgery, 39.4 at 6 weeks, 44.9 at 3 months and 48.2 at 1 year. Every pair of visits differs (all adjusted p < 0.001; the largest is printed as `5.59e-13`). R's `statistic` is negative because it subtracts the later visit from the earlier one (pre-op minus 6 weeks, t = −7.98); Python subtracts the other way round (7.98)."
- **Changes code:** yes (the sign sentence alone is prose only, but leaves "changes this large" unsupported)

### 15-9 · EFAS "rose" with no medians; n = 50 printed in Python only · B
- **Where:** `en/beyond/15-post-hoc.qmd:375` and `:436`, section `#after-friedman`
- **Text:** "in 50 patients with a boot" and "the EFAS score rose between 6 weeks and 3 months and again between 3 months and 12 months."
- **Problem:** No score per visit is printed, so "rose" rests on reading V = 6, 0 and 16.5 as "almost all differences are negative", which the page does not explain until the R vs Python box, and then only in passing. The 50 is printed by Python (`print(len(efas_wide))`) but not by R.
- **Where it really comes from:** Not computed on the page; medians are 12.5, 17 and 20 (n = 50 at each visit). The 50 is in the guard, line 630.
- **Proposed fix:**
  - R, after building `efas_boot`: `efas_boot |> group_by(visit) |> summarise(n = n(), median = median(efas))   # patients and median score at each visit`
  - Python, after `print(len(efas_wide))`: `print(efas_wide.median())   # median score at each visit`
  - Prose: "The median EFAS score was 12.5 at 6 weeks, 17 at 3 months and 20 at 12 months, and all three pairs differ (adjusted p < 0.001 with either method)."
- **Changes code:** yes

### 15-10 · Holm's 0.044 and BH's 0.026: the arithmetic is not shown · B
- **Where:** `en/beyond/15-post-hoc.qmd:150` to `:151`, section `#adjusting-p-values`, bullets
- **Text:** "Holm, p = 0.044: ... It multiplies the smallest p-value by 6, the next smallest by 5, and so on ... ASA 3 vs 4 has the largest unadjusted p-value (0.030), so it's multiplied by 1, but it takes 0.044 from ASA 1 vs 2, the one before it." and "Benjamini-Hochberg (BH), p = 0.026"
- **Problem:** The bullet follows the ASA 1 vs 2 row but never says which multiplier that row gets. The reader has to work out that 0.022 is the fifth smallest of six and so is multiplied by 2. The Bonferroni bullet gives its multiplier (6); the BH bullet gives no calculation at all. The four smaller p-values print as 0, so the order cannot be read from the table.
- **Where it really comes from:** Output rows "1 vs 2 0.022 0.132 0.0439 0.0263" and "3 vs 4 0.0298 0.179 0.0439 0.0298". 0.02195 × 2 = 0.0439; 0.02195 × 6 / 5 = 0.0263.
- **Proposed fix:** Holm bullet: "ASA 1 vs 2 has the fifth smallest of the six p-values, so it's multiplied by 2: 0.022 × 2 = 0.044. ASA 3 vs 4 has the largest (0.030) and is multiplied by 1, but ..." BH bullet: add "It multiplies each p-value by the number of tests divided by its rank: here 0.022 × 6 / 5 = 0.026."
- **Changes code:** no

### 15-11 · Kruskal-Wallis "H = 24.3, df = 3, p < 0.001" not tied to the output · B
- **Where:** `en/beyond/15-post-hoc.qmd:262`, section `#after-kruskal-wallis`, first bullet
- **Text:** "Kruskal-Wallis H = 24.3, df = 3, p < 0.001: LOS differs somewhere across the classes."
- **Problem:** R prints "Kruskal-Wallis chi-squared = 24.286, df = 3, p-value = 2.177e-05": no "H", and the p in e-notation. Python prints two bare numbers, "24.285994027836807 2.1770634905599066e-05", with no df. Page 8 makes these links; this page does not.
- **Where it really comes from:** The output lines quoted above.
- **Proposed fix:** "**Kruskal-Wallis chi-squared = 24.286** (R) or the first number Python prints: the H statistic, 24.3. **df = 3:** four classes minus one (Python doesn't print it). **p < 0.001** (both print `2.177e-05`): LOS differs somewhere across the classes."
- **Changes code:** no

### 15-12 · Overall Fisher p = 0.016 appears in the R tab only · B
- **Where:** `en/beyond/15-post-hoc.qmd:318` and `:570`, sections `#after-chi-square` and `#overall-test-first`
- **Text:** "The overall Fisher test says the complication rate differs across ASA classes (p = 0.016)."
- **Problem:** R prints "p-value = 0.01587". The Python tab runs only the six pairwise tests, so a Python reader has no overall p-value and no explanation of why.
- **Where it really comes from:** R output of `fisher_overall`.
- **Proposed fix:** Prose only: "(p = 0.016, R's `fisher.test()` output. scipy can only estimate this p-value for a table larger than 2 × 2 ([page 8](../catalog/08-three-plus-unmatched.qmd#chi-square)), so the Python tab runs the pairs only.)" Or add the seeded estimate to Python, as on page 8: `print(stats.fisher_exact(complications, method=stats.PermutationMethod(rng=np.random.default_rng(2026))).pvalue)   # overall test, estimated from random tables`, which prints 0.0169 and needs "(0.017 with this seed)" in the prose.
- **Changes code:** no (yes for the Python line)

### 15-13 · Implant A vs B hazard ratio is printed but never read · B
- **Where:** `en/beyond/15-post-hoc.qmd:554`, section `#after-log-rank`, paragraph after the tabset
- **Text:** "There was no clear evidence of a difference between A and B (p = 0.520). Against implant B, implant C's hazard ratio was 3.75 (95% CI 2.14 to 6.58)"
- **Problem:** The Cox output has two rows. The prose reads only the C row. The A row ("implant_vs_bA 1.223854 0.8170908 0.6676703 2.243351") is the effect size for the pair with p = 0.520 and is not mentioned; R's `exp(-coef)` column is not explained either.
- **Where it really comes from:** Output of `summary(implant_vs_b_model)$conf.int` and the lifelines summary.
- **Proposed fix:** "... between A and B (p = 0.520; hazard ratio for A against B 1.22, 95% CI 0.67 to 2.24, the `implant_vs_bA` row). Against implant B, implant C's hazard ratio was 3.75 (95% CI 2.14 to 6.58, the `implant_vs_bC` row). R's `exp(-coef)` column is the same ratio the other way round (B against A, B against C)."
- **Changes code:** no

### 15-14 · Tukey and Games-Howell bullets leave columns unexplained · C
- **Where:** `en/beyond/15-post-hoc.qmd:201` to `:203`, section `#after-anova`, bullets
- **Text:** "diff / meandiff ... lwr, upr / lower, upper ... p adj / p-adj"
- **Problem:** The bullets name only the Tukey columns. The Games-Howell tables use other names (R: `estimate`, `conf.low`, `conf.high`, `p.adj`; Python: `diff`, `se`, `pval`, and no CI), and statsmodels' `reject` column is never explained. The prose then quotes "p = 0.001 ... in the Games-Howell test" from a table whose columns were not introduced.
- **Where it really comes from:** R row "2 4 10.3 3.93 16.6 0.00114"; Python row "2 4 -10.2700 2.2551 0.0011".
- **Proposed fix:** Add two bullets: "**reject** (Python): True when the adjusted p-value is below 0.05." and "**Games-Howell:** the same three things under other names: `estimate`, `conf.low`/`conf.high` and `p.adj` in R; `diff` and `pval` in Python, which prints the standard error (`se`) in place of a CI."
- **Changes code:** no

## 16-mixed-models.qmd

### 16-1 · Nested model: "patient-level intercept comes out at almost exactly zero", "singular" · A
- **Where:** `en/beyond/16-mixed-models.qmd:386`, section `#bilateral`
- **Text:** "In this cohort the patient-level intercept comes out at almost exactly zero (lme4 warns that the fit is "singular"), so the knee model above is enough."
- **Problem:** A model result is reported, and it decides which model the page uses, but the model is never fitted: there is no code in this section in either language.
- **Where it really comes from:** Not computed anywhere, not even in the Prose guard, so nothing protects the sentence if the data change. Checked by hand: `lmer(prom_score ~ visit + (1 | patient_id/case_id), data = knees)` gives patient SD 0.0005, knee SD 8.837, `isSingular()` TRUE.
- **Proposed fix:** Show the fit.
  - R: `nested_model <- lmer(prom_score ~ visit + (1 | patient_id/case_id), data = knees)   # knees nested in patients`, then `VarCorr(nested_model)   # the patient_id SD is almost exactly 0` and `isSingular(nested_model)   # TRUE: the data can't support the extra intercept`
  - Python: `nested_model = smf.mixedlm("prom_score ~ visit", knees, groups="patient_id", re_formula="1", vc_formula={"case_id": "0 + C(case_id)"}).fit(reml=True)   # knees nested in patients`, then `print(nested_model.cov_re)   # the patient variance: 0`
  - Caution: both fits warn (lme4: "Model failed to converge with 1 negative eigenvalue"; statsmodels: "The MLE may be on the boundary of the parameter space"), so both chunks need the warning silenced to pass the quiet-page test, and the box should quote the warning. Add the patient SD to the guard.
- **Changes code:** yes

### 16-2 · Complete-case means 49.2 and 84.0 · A
- **Where:** `en/beyond/16-mixed-models.qmd:200`, section `#estimated-marginal-means`, paragraph after the bullets
- **Text:** "The 192 knees with all four scores average 49.2 before surgery and 84.0 at 1 year. That's close to the mixed model"
- **Problem:** This is the page's one direct comparison of the mixed model with the complete-case analysis it replaces, and no visible code computes the complete-case side.
- **Where it really comes from:** Prose guard, lines 407 and 434: `complete_means`.
- **Proposed fix:** Add to both tabs, after the contrast.
  - R: `knees |> group_by(case_id) |> filter(n() == 4) |> group_by(visit) |> summarise(knees = n(), mean = mean(prom_score))   # only the knees with all four scores: what repeated-measures ANOVA would use`
  - Python: `complete = knees[knees.groupby("case_id")["prom_score"].transform("size") == 4]   # only the knees with all four scores` and `print(complete.groupby("visit", observed=True)["prom_score"].mean().round(1))   # what repeated-measures ANOVA would use`
  - Prints 49.2, 61.8, 73.8, 84.0 (192 knees).
- **Changes code:** yes

### 16-3 · 431 scores, 120 patients, 80 complete (66.7%) · A
- **Where:** `en/beyond/16-mixed-models.qmd:268` (section `#group-by-time`, intro) and `:398` (section `#reporting`, Results)
- **Text:** "The model uses all 431 EFAS scores from the 120 randomized patients, although only 80 have all four." and "Of 120 randomized patients, 80 (66.7%) had all four scores; all 431 scores were analyzed."
- **Problem:** The model summary is never printed, so no output shows the number of patients, scores or complete cases. The knee section and exercise 1 both count these visibly; this section does not.
- **Where it really comes from:** Prose guard, lines 438 to 439.
- **Proposed fix:** Reuse exercise 1's counting line, right after `trial` is built.
  - R: `c(patients = n_distinct(trial$patient_id), scores = nrow(trial), complete = sum(table(trial$patient_id) == 4))   # patients, scores, patients with all four scores`
  - Python: `print(trial["patient_id"].nunique(), len(trial), (trial.groupby("patient_id").size() == 4).sum())   # patients, scores, patients with all four scores`
  - Prints 120, 431, 80. Intro: "... only 80 have all four (80 / 120 = 66.7%)."
- **Changes code:** yes

### 16-4 · "SD 2.9" for the model and "SD 3.2 within each arm" at 3 months · A
- **Where:** `en/beyond/16-mixed-models.qmd:370`, section `#group-by-time`, paragraph after the bullets
- **Text:** "mostly because the model assumes the same spread at all four visits (SD 2.9), and the 3-month scores spread a little wider (SD 3.2 within each arm)."
- **Problem:** Neither SD is in any output: the variance components of `arm_model` are never printed, and 3.2 is a pooled SD the page never computes. A reader who follows the link finds page 6 quoting SD 2.9 (boot) and 3.4 (cast), which looks like a contradiction of "3.2 within each arm".
- **Where it really comes from:** Prose guard, lines 455 to 456: `sqrt(sum(as.data.frame(VarCorr(arm_model))$vcov))` = 2.92 (patient SD 2.19 and residual SD 1.94 combined) and a hand-coded pooled SD = 3.15.
- **Proposed fix:**
  - R: `VarCorr(arm_model)   # SDs between patients and within a patient`, `sqrt(sum(as.data.frame(VarCorr(arm_model))$vcov))   # both together: the SD of one score, the same at every visit`, `sigma(lm(efas ~ arm, data = filter(trial, visit == "3mo")))   # the 3-month scores alone: SD around each arm's mean`
  - Python: `print(np.sqrt(arm_model.cov_re.iloc[0, 0] + arm_model.scale))   # the SD of one score, the same at every visit` and `print(np.sqrt(smf.ols("efas ~ arm", trial[trial["visit"] == "3mo"]).fit().mse_resid))   # the 3-month scores alone: SD around each arm's mean`
  - Prints 2.92 and 3.15. Prose: "(SD 2.9) ... (SD 3.2 around the arm means; page 6 gives 2.9 with a boot and 3.4 with a cast)."
- **Changes code:** yes

### 16-5 · Ceiling and missed-visit counts at 12 months · A
- **Where:** `en/beyond/16-mixed-models.qmd:370`, section `#group-by-time`, same paragraph
- **Text:** "EFAS scores crowd toward their maximum by 12 months (24 points for 7 of 55 patients with a boot and 8 of 47 with a cast) ... And the cast arm missed more 12-month visits (13 against 5)"
- **Problem:** Six numbers behind the section's two cautions, none of them in any output. The 13 and 5 also need the 60 randomized per arm, which the page never states.
- **Where it really comes from:** Prose guard, lines 415 and 452 to 454.
- **Proposed fix:**
  - R: `trial |> filter(visit == "12mo") |> group_by(arm) |> summarise(scored = n(), missed = 60 - n(), at_maximum = sum(efas == 24))   # 60 patients were randomized to each arm; 24 is the highest EFAS score`
  - Python: `twelve = trial[trial["visit"] == "12mo"]` and `print(twelve.groupby("arm", observed=True)["efas"].agg(scored="size", at_maximum=lambda scores: (scores == 24).sum()))   # 60 were randomized to each arm, so missed = 60 - scored`
  - Prints boot 55 scored, 5 missed, 7 at maximum; cast 47, 13, 8.
- **Changes code:** yes

### 16-6 · "46 of the knee patients had both knees replaced, so 92 of the 330 knees" · A
- **Where:** `en/beyond/16-mixed-models.qmd:384`, section `#bilateral`
- **Text:** "46 of the knee patients had both knees replaced, so 92 of the 330 knees come in pairs."
- **Problem:** No output shows the 46, and the section has no code.
- **Where it really comes from:** Prose guard, lines 408 and 451: `bilateral_knees`.
- **Proposed fix:** Put this before the nested model of finding 16-1.
  - R: `knees |> distinct(patient_id, case_id) |> count(patient_id, name = "knees") |> count(knees, name = "patients")   # patients with one knee, patients with two`
  - Python: `print(knees.groupby("patient_id")["case_id"].nunique().value_counts())   # patients with one knee, patients with two`
  - Prints 238 and 46. Prose: "46 patients had both knees replaced, so 2 × 46 = 92 of the 330 knees come in pairs."
- **Changes code:** yes

### 16-7 · The curve's "peak of about 89 points at around 8 months" is read off the plot · A
- **Where:** `en/beyond/16-mixed-models.qmd:259`, section `#time`, paragraph after the tabset
- **Text:** "the curve invents a peak of about 89 points at around 8 months, then falls."
- **Problem:** Both numbers have to be estimated by eye from the figure. The same sentence quotes 62.7 and 84.1 without saying they are the second and fourth numbers of the unlabeled `on_days` output.
- **Where it really comes from:** Prose guard, line 436: `max(curve$prom_score)` and `which.max`. The peak is 88.6 points on day 247.
- **Proposed fix:**
  - R, after `curve$prom_score <- ...`: `curve[which.max(curve$prom_score), ]   # the highest point of the curve`
  - Python: replace the inline prediction with `curve["prom_score"] = curve_model.predict(curve)`, plot that column, and add `print(curve.loc[curve["prom_score"].idxmax()])   # the highest point of the curve`
  - Prose: "62.7 at 6 weeks and 84.1 at 1 year (the second and fourth numbers printed) ... a peak of 88.6 points on day 247, about 8 months after surgery, then falls."
- **Changes code:** yes

### 16-8 · 330 knees, 1146 scores, 138 (42%), 58.2%: sums not spelled out · B
- **Where:** `en/beyond/16-mixed-models.qmd:86` (section `#why-mixed-models`) and `:392` (section `#reporting`, Results)
- **Text:** "All 330 knees have at least one score, 1146 scores in all, but only 192 knees have all four. Repeated-measures ANOVA would drop the other 138 knees (42%)" and "Of 330 knees, 192 (58.2%) had all four scores"
- **Problem:** The table printed here shows only 4, 28, 106 and 192. The reader has to add four numbers for 330, multiply and add for 1146, and divide for both percentages. 330 and 1146 are confirmed only one section later, in the model summary.
- **Where it really comes from:** Output "1 4 / 2 28 / 3 106 / 4 192"; later "Number of obs: 1146, groups: case_id, 330" (R) and "No. Observations: 1146 ... No. Groups: 330" (Python).
- **Proposed fix:** Prose only: "The knees add up to 4 + 28 + 106 + 192 = 330, and their scores to 4 × 1 + 28 × 2 + 106 × 3 + 192 × 4 = 1146 (the model output below confirms both). Only 192 knees (192 / 330 = 58.2%) have all four; repeated-measures ANOVA would drop the other 4 + 28 + 106 = 138 (138 / 330 = 42%) ..." Or print them, as exercise 1 does: R `c(knees = n_distinct(knees$case_id), scores = nrow(knees))`, Python `print(knees["case_id"].nunique(), len(knees))`.
- **Changes code:** no (yes for the printed version)

### 16-9 · Residual variance 73.5 and residual SD 8.6: Python calls them "Scale" · B
- **Where:** `en/beyond/16-mixed-models.qmd:137` to `:138`, section `#random-intercept`, "Reading the output"
- **Text:** "The scores also vary from visit to visit within a knee with a residual SD of 8.6 points." and "78.1 / (78.1 + 73.5) = 0.52"
- **Problem:** The bullet says where the knee variance is in both outputs, but not the residual. R prints it in the "Residual" row (73.45, 8.570). Python prints it only as "Scale: 73.4507" in the header and never prints 8.6. The "Std.Err." of 1.078 beside Python's `case_id Var` is also left unexplained.
- **Where it really comes from:** R "Residual 73.45 8.570"; Python "Scale: 73.4507".
- **Proposed fix:** "... a residual SD of 8.6 points (R's "Residual" row: variance 73.45, SD 8.570; Python prints only the variance, as "Scale: 73.4507" in the header, and √73.45 = 8.57)." And in the next bullet: "knee variance / (knee variance + residual variance) = 78.1 / (78.1 + 73.5) = 0.52".
- **Changes code:** no

### 16-10 · "The undivided statistic, 77.15" · B
- **Where:** `en/beyond/16-mixed-models.qmd:367`, section `#group-by-time`, first bullet
- **Text:** "visit:arm, F = 25.73 on 3 and 310 df, p < 0.001: the patterns differ. Python's Wald test gives the undivided statistic, 77.15 on 3 degrees of freedom, also p < 0.001."
- **Problem:** "Undivided" is never explained, and a reader who tries the obvious check gets 25.73 × 3 = 77.19, not 77.15. R prints the second df as 309.58 and the p-values appear as `6.924e-15` and `1.25e-16`; none of this is said.
- **Where it really comes from:** R row "visit:arm 290.3 96.75 3 309.58 25.727 6.924e-15"; Python "77.15287791633088 1.252001943749615e-16". The gap is the standard-error difference from the first R vs Python box (hidden comment, lines 361 to 362).
- **Proposed fix:** "**visit:arm, F = 25.73 on 3 and 310 df** (R prints `DenDF` 309.58), **p < 0.001** (`6.924e-15`): the patterns differ. Python's Wald test is a chi-square on 3 degrees of freedom: 77.15 (p < 0.001, printed as `1.25e-16`). R's F is that statistic divided by its 3 degrees of freedom: 77.15 / 3 = 25.72, against R's 25.73, because the two programs' standard errors differ slightly (see the box above)."
- **Changes code:** no

### 16-11 · Exercise 2: page 9's complete-case means are quoted, not shown · B
- **Where:** `en/beyond/16-mixed-models.qmd:540`, section `#exercises`, Solution 2
- **Text:** "Its visit means, 36.1, 39.8, 44.9 and 48.2, are almost the same as page 9's means for those 328 (36.1, 39.4, 44.9 and 48.2)"
- **Problem:** The second set of means and the 328 are not in the solution's output; the reader has to open page 9 and find them in its Results sentence. The solution text has no link.
- **Where it really comes from:** Prose guard, lines 405 to 406 and 464 (`complete_pf`); page 9, line 180.
- **Proposed fix:** Prose only: link it, "[page 9](../catalog/09-three-plus-matched.qmd#repeated-measures-anova)'s means". Better, two lines per tab: R `pf_all |> group_by(case_id) |> filter(n() == 4) |> group_by(visit) |> summarise(joint_replacements = n(), mean = mean(promis_pf))   # page 9's analysis: only those with all four scores`; Python `pf_complete = pf_all[pf_all.groupby("case_id")["promis_pf"].transform("size") == 4]` and `print(pf_complete.groupby("visit", observed=True)["promis_pf"].mean().round(1))`.
- **Changes code:** no (yes for the printed version)

### 16-12 · Exercise 3: R gives p = 0.003, Python p = 0.002, no reason given · C
- **Where:** `en/beyond/16-mixed-models.qmd:569` to `:571`, section `#exercises`, Solution 3
- **Text:** "F(3, 317) = 4.81 (p = 0.003)" and "Python's Wald test gives 14.43 on 3 degrees of freedom, p = 0.002."
- **Problem:** This is the first place the two programs give visibly different p-values for the same test, and the solution does not say why or which to report.
- **Where it really comes from:** R "visit:arm 30.95 10.318 3 316.63 4.8118 0.002723"; Python "14.434304085899631 0.0023698201437420824".
- **Proposed fix:** Add: "14.43 / 3 = 4.81, the same statistic. The p-values differ in the third decimal because R's F test uses Satterthwaite degrees of freedom (317) and Python's chi-square test treats them as infinite, as in the first R vs Python box. Report R's."
- **Changes code:** no

### 16-13 · The contrast weights `c(-1, 0, 0, 1)` · C
- **Where:** `en/beyond/16-mixed-models.qmd:157`, section `#estimated-marginal-means`, R tab
- **Text:** `confint(contrast(knee_means, method = list("1yr - preop" = c(-1, 0, 0, 1))))`
- **Problem:** A beginner has to guess what the four numbers mean; the comment says only "1 year minus pre-op". The Python tab reads the same number from the `visit[T.1yr]` coefficient, which is not said either.
- **Where it really comes from:** n/a (code explanation).
- **Proposed fix:** Extend the contrast bullet: "In R, the four weights go with the four visits in order: −1 for pre-op, 0 for 6 weeks and 3 months, +1 for 1 year, so the contrast is the 1-year mean minus the pre-op mean. In Python the same difference is the `visit[T.1yr]` coefficient, because pre-op is the reference."
- **Changes code:** no

## 17-agreement.qmd

### 17-1 · "limits of ±3.7°" contradicts the limits shown · ERROR (minor)
- **Where:** `en/beyond/17-agreement.qmd:252`, section `#bland-altman`, paragraph after the bullets
- **Text:** "Whether limits of ±3.7° are good enough is a clinical question, not a statistical one."
- **Problem:** The output and the bullet two lines above give limits of −2.74° to 3.74°. They are not symmetric, because the bias is 0.50°, so "±3.7°" overstates the lower limit by a degree.
- **Where it really comes from:** Output "limits1 -2.7376237 limits2 3.7442904".
- **Proposed fix:** "Whether limits of −2.7° to 3.7° are good enough is a clinical question, not a statistical one."
- **Changes code:** no

### 17-2 · "`irr::kappa2(weight = "equal")` ... gives 0.63 here instead of 0.73" · A
- **Where:** `en/beyond/17-agreement.qmd:353`, section `#kappa`, callout "weighted kappa needs the categories in order"
- **Text:** "Some functions sort categories alphabetically ... `irr::kappa2(weight = "equal")` does, and gives 0.63 here instead of 0.73."
- **Problem:** No visible code runs `kappa2()`, so the 0.63 that the warning rests on cannot be reproduced from the page.
- **Where it really comes from:** Prose guard, lines 372 and 394: `irr_weighted`.
- **Proposed fix:** Add one line per tab to the weighted-kappa chunks.
  - R: `irr::kappa2(data.frame(hka_group(cpak$R1), hka_group(cpak$R2)), weight = "equal")$value   # sorts the groups alphabetically: the wrong weights`
  - Python: `alphabetical = pd.crosstab(cpak["R1"].map(hka_group), cpak["R2"].map(hka_group))   # no order given, so pandas sorts alphabetically` and `print(cohens_kappa(alphabetical.to_numpy(), wt="linear").kappa)   # the wrong weights`
  - Both print 0.631. Callout: "... and gives 0.63 here instead of 0.73 (the last line of the code above)."
- **Changes code:** yes

### 17-3 · ICC 0.915 reported as 0.91, 0.935 as 0.93, −0.265 as −0.26 · B
- **Where:** `en/beyond/17-agreement.qmd:365` (section `#reporting`, Results), `:433` (Solution 1, Results), `:461` (Solution 2, Results)
- **Text:** "rater 1's intra-rater ICC 0.91 (95% CI 0.86 to 0.95)"; "The inter-rater ICC(A,1) for the MPTA was 0.93"; "was −0.26° (95% CI −0.65° to 0.12°)"
- **Problem:** R prints "ICC(A,1) = 0.915", "ICC(A,1) = 0.935" and "bias -0.2650000". A reader rounding those gets 0.92, 0.94 and −0.27. The sentences are right only because the unrounded values are 0.9148, 0.9348 and −0.26499…, which only the Python tab shows. Line 171 says 0.915 and the Results say 0.91, with nothing in between.
- **Where it really comes from:** Python output "ICC 0.914844", "ICC 0.934769", "-0.2649999999999987". The guard checks both roundings (line 384).
- **Proposed fix:** Prose only, once after line 171: "R prints the ICC already rounded to three decimals. Before rounding it is 0.9148 (Python's output), so to two decimals it is 0.91, not 0.92." Add the same half-sentence to Solutions 1 ("0.9348, so 0.93") and 2 ("−0.26499…, so −0.26"). Or avoid the trap by quoting three decimals in those Results sentences, as the bullets already do.
- **Changes code:** no

### 17-4 · "0.896 for consistency, and 0.94 for the average of the two raters" · B
- **Where:** `en/beyond/17-agreement.qmd:124`, section `#icc`, callout "always say which ICC"
- **Text:** "here 0.889 for absolute agreement and 0.896 for consistency, and 0.94 for the average of the two raters."
- **Problem:** Both numbers are in Python's six-row table only, under row names the prose never uses. R's output has neither.
- **Where it really comes from:** Python rows "ICC(C,1) 0.896386" and "ICC(A,k) 0.941454". For R, hidden in the Prose guard (lines 370 to 371).
- **Proposed fix:** "... 0.896 for consistency (Python's `ICC(C,1)` row) and 0.94 for the average of the two raters (`ICC(A,k)`). In R, run `irr::icc()` again with `type = "consistency"` or `unit = "average"`."
- **Changes code:** no

### 17-5 · "40 of the 60 knees" and "48 of 60 knees" are not printed · B
- **Where:** `en/beyond/17-agreement.qmd:301` and `:349`, section `#kappa`
- **Text:** "The raters gave the same CPAK class to 40 of the 60 knees (66.7%)" and "The raters agreed on the HKA group for 48 of 60 knees"
- **Problem:** The output gives only the proportion 0.6666667 and, for the second, a 3 × 3 table. The counts need 0.667 × 60 and 16 + 23 + 9, neither spelled out.
- **Where it really comes from:** Output "[1] 0.6666667" and the diagonal of `hka_table`; the guard checks both (lines 389 and 391).
- **Proposed fix:** Prose only: "... to 40 of the 60 knees (the 0.667 printed first: 0.667 × 60 = 40)" and "... for 48 of 60 knees (the diagonal of the table: 16 + 23 + 9), and every disagreement was a near miss: the two corner cells, varus against valgus, are 0."
- **Changes code:** no

### 17-6 · CIs of the limits: Python prints them in a different arrangement · B
- **Where:** `en/beyond/17-agreement.qmd:220` and `:249`, section `#bland-altman`
- **Text:** "The CIs of the limits (−3.48° to −2.00° and 3.00° to 4.48°)"
- **Problem:** R prints one row per limit ("lower -3.477482 -1.997766"). Python prints "[-3.477 3.004] [-1.998 4.484]": the two lower ends, then the two upper ends, so the reader has to pair the first numbers of each bracket. The first Python line is also five unlabeled numbers.
- **Where it really comes from:** Python output lines "0.503 0.076 0.93 1.654 [-2.738 3.744]" and "[-3.477 3.004] [-1.998 4.484]".
- **Proposed fix:** Print one limit per line in Python: `for limit in limits:` / `    print(round(limit, 3), round(limit - t_crit * se_limit, 3), round(limit + t_crit * se_limit, 3))   # each limit with its 95% CI`. Or prose only: "(R: one row per limit. Python: the first bracket holds the lower ends of both CIs, the second the upper ends.)"
- **Changes code:** yes (no for the prose-only version)

### 17-7 · Kappa: "some of that would happen by chance" is never quantified · C
- **Where:** `en/beyond/17-agreement.qmd:256` and `:301`, section `#kappa`
- **Text:** "the agreement between two raters beyond what chance alone would produce" and "40 of the 60 knees (66.7%), but some of that would happen by chance. Kappa = 0.58"
- **Problem:** The page never says how much agreement chance would give or how 66.7% becomes 0.58, so kappa stays a black box. One line would let the reader recompute it.
- **Where it really comes from:** Not computed on the page. Chance agreement is 0.2006, and (0.6667 − 0.2006) / (1 − 0.2006) = 0.583.
- **Proposed fix:**
  - R: `cpak_table <- table(cpak$R1, cpak$R2)`, `by_chance <- sum(rowSums(cpak_table) * colSums(cpak_table)) / sum(cpak_table)^2   # agreement expected if the raters chose classes independently`, `by_chance`
  - Python (after `cpak_table`): `by_chance = (cpak_table.sum(axis=1).to_numpy() * cpak_table.sum(axis=0).to_numpy()).sum() / len(cpak)**2   # agreement expected if the raters chose classes independently` and `print(by_chance)`
  - Prose: "By chance alone the raters would agree on 20.1% of knees. Kappa is the share of the remaining room they used: (0.667 − 0.201) / (1 − 0.201) = 0.58."
- **Changes code:** yes

## Pages with nothing to report

None. All three pages have findings.

## Not checked

- **Figures.** I did not open the rendered images. Page 16's interaction plots and page 17's Bland-Altman plot were judged from their code; the "no trend" reading on page 17 (line 250) is backed only by the guard's `cor.test(...)$p.value > 0.5`.
- **Claims about how the synthetic data were made:** "visits were missed almost entirely at random: by chance, or because follow-up had ended" (page 16, lines 200 and 540) and "at least two weeks apart" (page 17, line 19). These describe the generator in `data-raw/`, which I did not read.
- **Numbers attributed to other pages** were checked against those pages' sources only, not their frozen output: page 8 `#cox` (3.07, 1.85 to 5.09), page 8 `#one-way-anova` (F = 23.9), page 13 `#log-rank` (33.5), page 6 `#unpaired-t` (2.4 to 4.8), page 9 `#repeated-measures-anova` (36.1, 39.4, 44.9, 48.2). All are present there.
- **Python fix for 16-1** was run outside knitr only. Whether reticulate lets statsmodels' boundary warning through to stderr on a rendered page is untested.
- **German and French pages** were not read (out of scope).
