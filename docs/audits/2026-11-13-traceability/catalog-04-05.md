# Audit findings: catalog pages 04 and 05

Checked against the frozen output in `_freeze/en/catalog/<page>/execute-results/html.json` (dumped to `work-catalog-04-05/04.md` and `05.md`), the frozen figures, and read-only R and Python runs on `data/`. Line numbers refer to the `.qmd` source.

Note for every fix marked "Changes code: yes": the new visible lines only print values the hidden `# Prose guard` already asserts, so no guard change is needed, but the same lines must go into `de/` and `fr/` and all three pages must be re-rendered.

## 04-describe-one-group.qmd

### 04-1 · The standard error arithmetic as written gives 0.38, not 0.39 · ERROR
- **Where:** `en/catalog/04-describe-one-group.qmd:127`, section `#mean-sd`, callout "Under the hood: the CI for a mean" (repeated at line 138, "Watch out: SD or SEM?")
- **Text:** "The **standard error** of the mean is SD / √n = 9.4 / √600 ≈ 0.39 years."
- **Problem:** A reader who types the calculation shown gets 9.4 / √600 = 0.3838, which rounds to 0.38. The quoted 0.39 comes from the unrounded SD (9.4353 / √600 = 0.3852). Minor, a rounding artifact, but the equation on the page is false as printed.
- **Where it really comes from:** hidden Prose guard, line 504: `round(sd(cohort$age) / sqrt(600), 2) == 0.39`. The visible output prints the SD as `9.44` (R tibble and Python).
- **Proposed fix:** Use the SD at the precision the output prints: "The **standard error** of the mean is SD / √n = 9.44 / √600 ≈ 0.39 years." Then close the loop to the printed CI with one more sentence: "Here: 65.52 ± 1.96 × 0.39 = 64.76 to 66.28, the CI printed above." (Checked: 9.44 / √600 = 0.3854; 65.52 ± 0.764 = 64.76 to 66.28.)
- **Changes code:** no

### 04-2 · "39 of the 194 scores were 48" is computed only in the Prose guard · A
- **Where:** `en/catalog/04-describe-one-group.qmd:198`, section `#median-iqr`, step "Look at the data first"
- **Text:** "Scores pile up against the maximum of 48 (a **ceiling**): 39 of the 194 scores were 48."
- **Problem:** Neither number is on the page at this point. The 39 can only be guessed from the height of a histogram bar, and 194 is first printed in the next step ("Run it").
- **Where it really comes from:** hidden Prose guard, line 505: `sum(ohs_1yr == 48) == 39`. `length(ohs_1yr)` is printed later, at line 206.
- **Proposed fix:** Add two lines to the "Look at the data first" chunks, before the plot.
  R (after the `pull(ohs)` line):
  ```r
  length(ohs_1yr)        # how many scores
  sum(ohs_1yr == 48)     # how many of them are the maximum, 48
  ```
  Python (after the `ohs_1yr = ...` line):
  ```python
  print(len(ohs_1yr))              # how many scores
  print((ohs_1yr == 48).sum())     # how many of them are the maximum, 48
  ```
- **Changes code:** yes

### 04-3 · "13 scored exactly 42" and "62 of the 194 (32%)" are computed only in the Prose guard · A
- **Where:** `en/catalog/04-describe-one-group.qmd:243` and `:244`, section `#median-iqr`, step "Read the output"
- **Text:** "With whole-number scores many patients share it (13 scored exactly 42) ..." and "At least a quarter scored 39 or less: with ties, 62 of the 194 (32%) did."
- **Problem:** The printed output gives only n, the three quartiles and the CI. None of 13, 62 or 32% can be recovered from it.
- **Where it really comes from:** hidden Prose guard, lines 505 and 507: `sum(ohs_1yr == 42) == 13`, `sum(ohs_1yr <= 39) == 62`, `round(100 * mean(ohs_1yr <= 39)) == 32`.
- **Proposed fix:** Add three lines to the "Run it" chunks, after the `quantile()` line.
  R:
  ```r
  sum(ohs_1yr == 42)                             # how many scored exactly the median
  sum(ohs_1yr <= 39)                             # how many scored the first quartile or less
  mean(ohs_1yr <= 39)                            # the same as a proportion
  ```
  Python:
  ```python
  print((ohs_1yr == 42).sum())                             # how many scored exactly the median
  print((ohs_1yr <= 39).sum())                             # how many scored the first quartile or less
  print((ohs_1yr <= 39).mean())                            # the same as a proportion
  ```
  The proportion prints as 0.3195876, which the prose rounds to 32%.
- **Changes code:** yes

### 04-4 · Exercise 2: the skew, "4 to 6 days" and "0.9 ± 1.1" are shown nowhere · A
- **Where:** `en/catalog/04-describe-one-group.qmd:563` (question) and `:567` (Solution), section `#exercises`
- **Text:** "... as "0.9 ± 1.1 days"" and "Length of stay is strongly right-skewed (most patients go home on day 0 or 1, a few stay 4 to 6 days)"
- **Problem:** The Solution prints only the three quartiles (0, 1, 1). The reader cannot see the distribution the answer rests on, nor check the resident's mean and SD. The "day 0 or 1" and "4 to 6 days" statements are not even in the Prose guard.
- **Where it really comes from:** mean and SD: hidden Prose guard, line 522. The distribution: not computed anywhere (confirmed on the data: 291, 173, 88, 22, 16, 8 and 2 patients stayed 0 to 6 days).
- **Proposed fix:** Add two lines at the top of each Solution chunk.
  R:
  ```r
  count(cohort, los_days)                                         # how many patients stayed 0, 1, 2 ... days
  cohort |> summarise(mean = mean(los_days), sd = sd(los_days))   # the resident's "0.9 ± 1.1"
  ```
  Python:
  ```python
  print(cohort["los_days"].value_counts().sort_index())           # how many patients stayed 0, 1, 2 ... days
  print(cohort["los_days"].mean(), cohort["los_days"].std())      # the resident's "0.9 ± 1.1"
  ```
  And tie the prose to it: "(464 of the 600 patients went home on day 0 or 1, and 26 stayed 4 to 6 days)". 291 + 173 = 464; 16 + 8 + 2 = 26.
- **Changes code:** yes

### 04-5 · "Every patient was followed for at least 30 days or until death" is checked only in the Prose guard · A
- **Where:** `en/catalog/04-describe-one-group.qmd:276`, section `#proportion`, step "When to use it"
- **Text:** "Here every patient was followed for at least 30 days or until death, so the 30-day proportion is complete."
- **Problem:** This is the fact that justifies using a plain proportion, and nothing visible supports it. The section never shows `followup_days` or `died`.
- **Where it really comes from:** hidden Prose guard, line 512: `all(hip_fracture$followup_days >= 30 | hip_fracture$died == 1)`. The codebook (`data/codebooks/hip_fracture.csv`) defines `followup_days` as "Follow-up to death or 1 year".
- **Proposed fix (prose only):** "Here the codebook says every patient was followed until death or for 1 year (`followup_days`), so nobody's follow-up stops short of 30 days and the 30-day proportion is complete." If a visible check is preferred, add to "Look at the data first": R `count(hip_fracture, died, followup_days >= 30)   # everyone alive was followed for 30 days or more`; Python `print(pd.crosstab(hip_fracture["died"], hip_fracture["followup_days"] >= 30))   # everyone alive was followed for 30 days or more`.
- **Changes code:** no (yes for the optional check)

### 04-6 · "the 80 patients who had both sides operated on" is never counted · A
- **Where:** `en/catalog/04-describe-one-group.qmd:26` (intro callout) and `:363` (section `#proportion`, "Watch out: percent of what?")
- **Text:** "... the joint replacement examples use every case, including the 80 patients who had both sides operated on."
- **Problem:** No visible code on this page counts them. The link goes to page 3 `#paired`, which also only states the number (`en/foundations/03-distributions.qmd:426`) and checks it in its own hidden guard.
- **Where it really comes from:** hidden Prose guard, line 513: `sum(table(cohort$patient_id) == 2) == 80`.
- **Proposed fix:** Show the count once, on page 3 `#paired`, where the link already points (R: `sum(table(cohort$patient_id) == 2)   # patients who appear twice, once per side`; Python: `print((cohort["patient_id"].value_counts() == 2).sum())   # patients who appear twice, once per side`), and here write "the 80 patients who had both sides operated on (page 3 counts them)". The prose-only alternative is to drop the number on this page: "including the patients who had both sides operated on".
- **Changes code:** yes on page 3 (not one of my pages); no on this page

### 04-7 · "263 patients at risk" appears only in R's output, and lifelines counts 258 · B
- **Where:** `en/catalog/04-describe-one-group.qmd:478` and `:484`, section `#kaplan-meier`, steps "Read the output" and "How to report it"
- **Text:** "**At 5 years:** survival 0.863 (95% CI 0.828 to 0.892), with 263 patients still at risk."
- **Problem:** R prints it (`n.risk` column: `5    263      66    0.863 ...`). The Python tab prints only the estimate and CI, and the table under both plots has no column for 5 years (0, 2, 4, 6, 8, 10). A Python reader cannot find 263; lifelines' own convention would give 258, because 5 patients' follow-up ends at exactly 5.00 years.
- **Where it really comes from:** R output line `5    263      66    0.863  0.0162        0.828        0.892`; hidden Prose guard line 518 (`km_5$n.risk == 263`).
- **Proposed fix:** Name the column in the bullet ("263 patients still at risk: the `n.risk` column in R") and add one line to the Python chunk, after the `print(at_5, ...)` line:
  ```python
  print((cohort["followup_years"] >= 5).sum())   # patients still being followed at 5 years (R's n.risk)
  ```
  R needs no new line. See 04-15 for the sentence that explains the two counting rules.
- **Changes code:** yes (Python only, but the page must still be re-rendered in three languages)

### 04-8 · "13.5% were revised" is not derived, and the summary output is never read · B
- **Where:** `en/catalog/04-describe-one-group.qmd:380` (step "When to use it") and `:419` (step "Look at the data first"), section `#kaplan-meier`
- **Text:** "A plain percentage ("13.5% were revised") ignores follow-up time"
- **Problem:** 13.5% is 81 / 600, but the page never says so, and the 81 and 600 are printed only one step later. That printed summary (`600  81  4.36`; Python `600 81 4.365`, unlabelled) is then never mentioned: the prose below it discusses only the first and fifth rows, so the median follow-up of 4.36 years is shown and left unexplained.
- **Where it really comes from:** hidden Prose guard, line 514: `round(100 * mean(cohort$revised), 1) == 13.5`. Visible output: `1      600        81            4.36`.
- **Proposed fix (prose only):** Line 380: "A plain percentage (81 of our 600 cases were revised, 13.5%) ignores follow-up time". Line 419, add: "The second output counts 600 cases and 81 revisions (81 / 600 = 13.5%, the plain percentage above), with a median follow-up of 4.4 years (Python prints the three numbers without labels)."
- **Changes code:** no

### 04-9 · "roughly 47 to 84 years" needs arithmetic the page does not show · B
- **Where:** `en/catalog/04-describe-one-group.qmd:122`, section `#mean-sd`, step "Read the output"
- **Text:** "In a bell-shaped distribution about 95% of patients lie within 2 SDs of the mean, here roughly 47 to 84 years."
- **Problem:** The reader has to work out mean ± 2 × SD alone.
- **Where it really comes from:** hidden Prose guard, line 502. From the printed values: 65.5 − 2 × 9.4 = 46.7 and 65.5 + 2 × 9.4 = 84.3.
- **Proposed fix (prose only):** "... within 2 SDs of the mean, here 65.5 ± 2 × 9.4, roughly 47 to 84 years."
- **Changes code:** no

### 04-10 · The SEM of 0.39 in the Watch-out box is explained only inside a collapsed box · B
- **Where:** `en/catalog/04-describe-one-group.qmd:138`, section `#mean-sd`, "Watch out: SD or SEM?"
- **Text:** "The **standard error of the mean (SEM)** is much smaller than the SD (0.39 vs 9.4 years here)"
- **Problem:** The only place that says how 0.39 arises is the collapsed "Under the hood" box above. A reader who leaves it closed meets 0.39 with no source.
- **Where it really comes from:** line 127 (collapsed callout); hidden Prose guard line 504.
- **Proposed fix (prose only):** "... is much smaller than the SD (SD / √n = 9.44 / √600 ≈ 0.39 years, against an SD of 9.4 years here)". Use 9.44 for the reason given in 04-1.
- **Changes code:** no

### 04-11 · The denominator 1,200 is never printed · B
- **Where:** `en/catalog/04-describe-one-group.qmd:352`, section `#proportion`, step "Read the output"
- **Text:** "**74 of 1,200 = 0.062:** 6.2% of patients died within 30 days of admission."
- **Problem:** The output shows 74, 1126 and 0.06166667. `patients` is assigned and never printed, so 1,200 has to be worked out as 1,126 + 74.
- **Where it really comes from:** visible count table (`0  1126`, `1  74`) plus arithmetic.
- **Proposed fix (prose only):** "**74 of 1,200 = 0.062:** the count above shows 74 deaths and 1,126 survivors, 1,200 patients in all, and 74 / 1,200 = 0.0617, so 6.2% died within 30 days of admission."
- **Changes code:** no

### 04-12 · R prints a confidence level of 0.9629 under a bullet that says "95% CI" · B
- **Where:** `en/catalog/04-describe-one-group.qmd:245`, section `#median-iqr`, step "Read the output" (explained only in the collapsed box at `:249`)
- **Text:** "**95% CI for the median 41 to 43:** how precisely 194 patients pin down the median."
- **Problem:** R's output ends with `attr(,"conf.level") [1] 0.9629381`. The bullets never mention that line; the explanation sits in a collapsed box. Python prints no level at all.
- **Where it really comes from:** R output of `DescTools::MedianCI(ohs_1yr, method = "exact")`.
- **Proposed fix (prose only):** Add to the bullet: "R's last line, `conf.level 0.9629`, is the confidence this interval really has: a little more than the 95% asked for (the box below says why). Python doesn't print it."
- **Changes code:** no

### 04-13 · Exercise 3: 21.4% is not computed in the Solution · B
- **Where:** `en/catalog/04-describe-one-group.qmd:610`, section `#exercises`, Solution 3
- **Text:** "257 of 1,200 patients (21.4%; 95% CI 19.2% to 23.8%)"
- **Problem:** The Solution prints the count (257) and the CI but not the proportion, although the worked section prints `deaths / patients`.
- **Where it really comes from:** hidden Prose guard, line 524: `round(100 * 257 / 1200, 1) == 21.4`.
- **Proposed fix:** One line in each Solution chunk, after `nursing_home` is defined. R: `nursing_home / nrow(hip_fracture)   # the proportion`. Python: `print(nursing_home / len(hip_fracture))   # the proportion`. It prints 0.2141667.
- **Changes code:** yes

### 04-14 · "by 10 years only a handful remain": the table says 21 · B
- **Where:** `en/catalog/04-describe-one-group.qmd:477`, section `#kaplan-meier`, step "Read the output"
- **Text:** "Trust the right-hand end of the curve less: by 10 years only a handful remain."
- **Problem:** The table under both plots gives the number (21 at 10 years); "a handful" hides it and undersells it.
- **Where it really comes from:** the "At risk" row under each plot, last column: 21.
- **Proposed fix (prose only):** "... by 10 years only 21 of the 600 remain (the last column of the "At risk" row)."
- **Changes code:** no

### 04-15 · The tables under the R and Python plots differ (332 vs 331, 84 vs 83) with no explanation · C
- **Where:** `en/catalog/04-describe-one-group.qmd:477` (bullet) and `:491` to `:494` ("R vs Python: the confidence band"), section `#kaplan-meier`
- **Text:** "**The numbers at risk** under the plot show how many patients were still being followed at each time."
- **Problem:** R's table reads 600, 496, 332, 187, 84, 21; lifelines' reads 600, 496, 331, 187, 83, 21. Python's table also has a "Censored" row that R's lacks. A reader who compares the tabs sees two different answers and no reason.
- **Where it really comes from:** R counts patients whose follow-up reaches the time (`followup_years >= t`); lifelines counts those followed beyond it (`> t`). One patient's follow-up ends at exactly 4.00 years and one at exactly 8.00 (five at exactly 5.00, hence 263 vs 258 in 04-7). Confirmed on the data.
- **Proposed fix (prose only):** Add to the 🔀 box: "The tables under the two plots differ by one patient at 4 and at 8 years (332 and 84 in R, 331 and 83 in Python). R counts a patient whose follow-up ends exactly at that time as still at risk; lifelines doesn't. lifelines also adds a row of patients censored so far."
- **Changes code:** no

### 04-16 · Printed survival output that is never explained: `n.event`, `std.err`, "519 right-censored" · C
- **Where:** `en/catalog/04-describe-one-group.qmd:475` to `:478`, section `#kaplan-meier`, step "Read the output"
- **Text:** (no text: the bullets skip these values)
- **Problem:** R's `summary(km, times = 5)` prints `n.event 66` and `std.err 0.0162`; Python's `km.fit()` prints "fitted with 600 total observations, 519 right-censored observations". A beginner will wonder why 66 is not the 81 revisions counted above, and where 519 comes from.
- **Where it really comes from:** 66 = revisions up to 5 years (confirmed on the data); 519 = 600 − 81.
- **Proposed fix (prose only):** Extend the "At 5 years" bullet: "In R's line, `n.event` 66 is the number of revisions up to 5 years (81 over the whole follow-up) and `std.err` is the standard error of the estimate. Python's first line, "600 total observations, 519 right-censored", restates the input: 600 − 81 revisions = 519 censored."
- **Changes code:** no

## 05-one-group-vs-hypothetical.qmd

### 05-1 · Results quote "SD 16.4", which no visible code computes · A
- **Where:** `en/catalog/05-one-group-vs-hypothetical.qmd:161`, section `#one-sample-t`, step "How to report it"
- **Text:** "**Results:** Mean operative time was 84.5 minutes (SD 16.4); the booked time was 90 minutes ..."
- **Problem:** The t test output gives t, df, p, the CI and the mean. The SD is nowhere on the page.
- **Where it really comes from:** hidden Prose guard, line 590: `round(sd(cohort$op_time_min), 1) == 16.4`.
- **Proposed fix:** One line in each "Run it" chunk, after the test is printed.
  R: `sd(cohort$op_time_min)                           # the SD, for the Results sentence`
  Python: `print(cohort["op_time_min"].std())                               # the SD, for the Results sentence`
  It prints 16.43613. Add a bullet: "**SD = 16.4 minutes:** not part of the test output; the Results sentence needs it."
- **Changes code:** yes

### 05-2 · Results quote the median 85.8 and IQR 74.7 to 93.9, which no visible code computes · A
- **Where:** `en/catalog/05-one-group-vs-hypothetical.qmd:324`, section `#wilcoxon-signed-rank`, step "How to report it" (and `:182`, "report both")
- **Text:** "**Results:** The median 1-year KOOS JR was 85.8 points (IQR 74.7 to 93.9); the target was 80 points ..."
- **Problem:** The page prints the pseudomedian (84.35) and never the median or quartiles, although "When to use it" tells the reader to report both. The first numbers of the Results sentence have no source.
- **Where it really comes from:** hidden Prose guard, line 600: `round(median(koos_1yr), 1) == 85.8`, `round(quantile(koos_1yr, c(0.25, 0.75)), 1) == c(74.7, 93.9)`.
- **Proposed fix:** One line in each "Effect size and 95% CI" chunk (first line).
  R: `quantile(koos_1yr, probs = c(0.25, 0.50, 0.75))      # first quartile, median, third quartile`
  Python: `print(np.quantile(koos_1yr, [0.25, 0.50, 0.75]))      # first quartile, median, third quartile`
  It prints 74.700, 85.750, 93.925. Add to the paragraph at line 318: "The median is 85.75 (IQR 74.7 to 93.9), a little above the Hodges-Lehmann estimate, as expected with a ceiling."
- **Changes code:** yes

### 05-3 · n = 260, V = 22698.5 and "more patients scored above 80 than below" have no visible source · A
- **Where:** `en/catalog/05-one-group-vs-hypothetical.qmd:335` ("R vs Python: Wilcoxon defaults"), `:318` (step "Effect size and 95% CI") and `:330` (Watch-out), section `#wilcoxon-signed-rank`
- **Text:** "R reports V ... (22698.5, printed as 22698) ... The two sums always add up to n(n + 1)/2, here 260 × 261 / 2 = 33,930"; "noticeably more patients scored above 80 than below"; "patients who score **exactly** 80 ... are dropped from the test."
- **Problem:** The number of patients is never printed, so 260 appears from nowhere; the counts above and below 80 are never shown; and the page does not say whether anyone scored exactly 80 here (nobody did, which is why n stays 260). 22698.5 cannot be seen in R's output either.
- **Where it really comes from:** hidden Prose guard, lines 593 to 595: `length(koos_1yr) == 260`, `unname(koos_test$statistic) == 22698.5`, `sum(koos_1yr != 80) == 260`. The counts above and below (170 and 90) are not computed anywhere; confirmed on the data.
- **Proposed fix:** Three lines in each "Look at the data first" chunk, before the plot.
  R:
  ```r
  length(koos_1yr)       # how many patients
  sum(koos_1yr > 80)     # how many scored above the target
  sum(koos_1yr < 80)     # how many scored below it
  ```
  Python:
  ```python
  print(len(koos_1yr))              # how many patients
  print((koos_1yr > 80).sum())      # how many scored above the target
  print((koos_1yr < 80).sum())      # how many scored below it
  ```
  Prose after the plot: "260 patients: 170 scored above 80 and 90 below. 170 + 90 = 260, so nobody scored exactly 80 and nobody is dropped from the test." In the 🔀 box, derive the half: "... here 260 × 261 / 2 = 33,930, and 33,930 − 11,231.5 = 22,698.5, which R prints as 22698."
- **Changes code:** yes

### 05-4 · The Wilson interval "84.1% to 88.0%" is computed only in the Prose guard · A
- **Where:** `en/catalog/05-one-group-vs-hypothetical.qmd:579`, section `#binomial-test`, "R vs Python: exact CIs"
- **Text:** "It's a little wider than the Wilson interval that page 4 uses, which for these 1,034 of 1,200 patients runs from 84.1% to 88.0%."
- **Problem:** The page shows only the exact interval. The Wilson figures are on neither this page nor page 4 (page 4 computes Wilson for other counts).
- **Where it really comes from:** hidden Prose guard, line 614: `round(100 * prop.test(within_48h, patients, correct = FALSE)$conf.int, 1) == c(84.1, 88.0)`.
- **Proposed fix:** One line at the end of each "Run it" chunk.
  R: `prop.test(within_48h, patients, correct = FALSE)$conf.int   # the Wilson interval, for comparison`
  Python: `print(surgery_test.proportion_ci(method="wilson"))          # the Wilson interval, for comparison`
  It prints 0.8409757 and 0.8800495, next to the exact 0.8408295 and 0.8807126. The prose-only alternative is to drop the numbers: "It's a little wider than the Wilson interval that page 4 uses."
- **Changes code:** yes (no for the alternative)

### 05-5 · "the 80 patients who had both sides operated on" is never counted · A
- **Where:** `en/catalog/05-one-group-vs-hypothetical.qmd:26`, intro callout
- **Text:** "... including the 80 patients who had both sides operated on."
- **Problem:** Same as 04-6: stated here, linked to page 3, shown on neither.
- **Where it really comes from:** hidden Prose guard, line 587.
- **Proposed fix:** As in 04-6: count it once on page 3 `#paired` and add "(page 3 counts them)" here, or drop the number on this page.
- **Changes code:** yes on page 3; no on this page

### 05-6 · "p < 0.001" is never tied to the e-notation the output prints · B
- **Where:** `en/catalog/05-one-group-vs-hypothetical.qmd:119` (`#one-sample-t`), `:265` (`#wilcoxon-signed-rank`), `:416` (`#chi-square-gof`), `:558` (`#binomial-test`), step "Read the output" in each
- **Text:** "**p < 0.001:** a mean this far from 90 would be very unlikely ..."
- **Problem:** The outputs print `p-value = 1.204e-15`, `2.293e-06` (pingouin: `0.000002`), `5.992e-06` and `2.682e-05`. A beginner who has never seen e-notation cannot match these to "p < 0.001". Pages 8 and 10 already write "(R prints `1.28e-14`)"; this page doesn't, and a search of `en/` found no page that explains the notation.
- **Where it really comes from:** output lines `t = -8.2265, df = 599, p-value = 1.204e-15`; `V = 22698, p-value = 2.293e-06`; `X-squared = 26.964, df = 3, p-value = 5.992e-06`; `number of successes = 1034, number of trials = 1200, p-value = 2.682e-05`.
- **Proposed fix (prose only):** First bullet (line 119): "**p < 0.001** (the output prints `1.204e-15`; "e-15" means "move the decimal point 15 places to the left", so this is 0.000000000000001204): a mean this far from 90 ...". The other three: "**p < 0.001** (the output prints `2.293e-06`, that is 0.000002293)", "(`5.992e-06`, that is 0.000005992)", "(`2.682e-05`, that is 0.00002682)".
- **Changes code:** no

### 05-7 · "Read the output" uses R's labels only; Python names the same values differently, or omits them · B
- **Where:** `en/catalog/05-one-group-vs-hypothetical.qmd:557` to `:560` (`#binomial-test`), `:414` to `:415` (`#chi-square-gof`), `:117` to `:121` (`#one-sample-t`), `:710` (Solution 3)
- **Text:** "**number of successes = 1034, number of trials = 1200**", "**probability of success = 0.862**", "**X-squared = 26.96**", "**df = 3**", "**mean of x = 84.48**"
- **Problem:** The Wilcoxon bullets name both programs' labels; the other three sections name only R's. Worst case: scipy's binomial output reads `BinomTestResult(k=1034, n=1200, ..., statistic=0.8616666666666667, ...)`, where "statistic" is the proportion. scipy's chi-square result (`Power_divergenceResult(statistic=..., pvalue=...)`) has no df at all, so "df = 3" (and "df = 2" in Solution 3) is R-only.
- **Where it really comes from:** R and Python outputs of the "Run it" chunks.
- **Proposed fix (prose only):** Binomial: "**number of successes = 1034, number of trials = 1200** (Python: `k=1034, n=1200`)" and "**probability of success = 0.862** (Python calls it `statistic`)". Chi-square: "**X-squared = 26.96** (Python: `statistic`)" and "**df = 3:** degrees of freedom, the number of categories minus 1 (4 − 1). scipy doesn't print it." t test: "**t = −8.23** (Python: `statistic`)" and "**mean of x = 84.48** (Python: the first number of the second line)". Solution 3: after the Results sentence, "df = 3 categories − 1 = 2; scipy doesn't print it."
- **Changes code:** no

### 05-8 · R prints a 95% CI for the rank-biserial r (0.21 to 0.46) that the page never mentions · B
- **Where:** `en/catalog/05-one-group-vs-hypothetical.qmd:318` and `:324`, section `#wilcoxon-signed-rank`, steps "Effect size and 95% CI" and "How to report it"
- **Text:** "the rank-biserial r of 0.34 is a moderate effect" / "rank-biserial r = 0.34"
- **Problem:** `effectsize::rank_biserial()` prints `0.34 | [0.21, 0.46]` and a footnote, "Deviation from a difference of 80". Neither is explained, the Results sentence gives r without the CI, and the Python tab prints r alone, so the tabs visibly differ.
- **Where it really comes from:** R output of `effectsize::rank_biserial(koos_1yr, mu = 80)`; Python `koos_test["RBC"]` prints 0.337961.
- **Proposed fix (prose only):** Add after line 318: "R's effectsize also prints a 95% CI for r, 0.21 to 0.46 (its footnote just restates the target of 80). pingouin gives r without a CI." Whether the Results sentence should carry that CI (rule 8: a CI with every estimate) is for the owner; if so: "rank-biserial r = 0.34, 95% CI 0.21 to 0.46".
- **Changes code:** no

### 05-9 · Exercise 3: the percentages 53.5%, 38.3% and 8.2% are not computed in the Solution · B
- **Where:** `en/catalog/05-one-group-vs-hypothetical.qmd:710`, section `#exercises`, Solution 3
- **Text:** "Of our patients, 53.5% had never smoked, 38.3% were former and 8.2% current smokers"
- **Problem:** The Solution prints only the counts (321, 230, 49) and the test. The reader must add them up to 600 and divide.
- **Where it really comes from:** hidden Prose guard, line 622.
- **Proposed fix:** One line in each Solution chunk, after the counts are printed. R: `100 * prop.table(smoking)   # the same as percentages`. Python: `print(100 * smoking / smoking.sum())   # the same as percentages`. It prints 53.5, 38.33333 and 8.166667.
- **Changes code:** yes

### 05-10 · Exercise 1: the R Solution does not print the difference of −0.5 · B
- **Where:** `en/catalog/05-one-group-vs-hypothetical.qmd:656`, section `#exercises`, Solution 1
- **Text:** "(difference −0.5 years, 95% CI −1.2 to 0.3; p = 0.213)"
- **Problem:** Python prints `-0.48`; R prints the mean (65.52) and the shifted CI, not the difference, although the worked section prints `op_test$estimate - 90`.
- **Where it really comes from:** R: 65.52 − 66 by hand; Python output `-0.480000000000004 -1.2364948782807943 0.27649487828078634`.
- **Proposed fix:** One line in the R Solution chunk, before `age_test$conf.int - 66`: `age_test$estimate - 66   # mean difference`.
- **Changes code:** yes (R only)

### 05-11 · "about 20 minutes" is 4 × 5.5 = 22, and the page does not show the sum · B
- **Where:** `en/catalog/05-one-group-vs-hypothetical.qmd:155`, section `#one-sample-t`, step "Effect size and 95% CI"
- **Text:** "over a day of four joints, it adds up to about 20 minutes."
- **Problem:** Small, but the reader has to guess the calculation, and it gives 22.
- **Where it really comes from:** 4 × 5.52, from the printed `-5.52`.
- **Proposed fix (prose only):** "over a day of four joints, it adds up to 4 × 5.5 = 22 minutes."
- **Changes code:** no

### 05-12 · The rank-biserial r is defined by its end points only; the printed rank sums give it in one line · C
- **Where:** `en/catalog/05-one-group-vs-hypothetical.qmd:274`, section `#wilcoxon-signed-rank`, step "Effect size and 95% CI"
- **Text:** "The **rank-biserial correlation (r)**: from −1 (every patient below 80) through 0 (balanced) to +1 (every patient above 80)."
- **Problem:** A beginner cannot see what 0.34 measures, and the sentence at line 318 reads it as a count of patients, which it is not: it compares rank sums.
- **Where it really comes from:** (22,698.5 − 11,231.5) / 33,930 = 0.338, from the two rank sums and their total, all quoted in the 🔀 box.
- **Proposed fix (prose only):** Add: "It's the rank sum above 80 minus the rank sum below, as a share of the total: (22,698.5 − 11,231.5) / 33,930 = 0.34." With the counts from 05-3, line 318 can then say what it means: "170 patients scored above 80 and 90 below, and those above tended to be further from it."
- **Changes code:** no

### 05-13 · The chi-square statistic is described, not calculated, although the table above gives every term · C
- **Where:** `en/catalog/05-one-group-vs-hypothetical.qmd:414`, section `#chi-square-gof`, step "Read the output"
- **Text:** "**X-squared = 26.96:** the chi-square statistic, adding up how far each observed count is from its expected count."
- **Problem:** "How far" is left open. The observed and expected counts are printed two steps earlier, so the page can show the sum, and the same sum shows why ASA 3 "makes the biggest difference" (line 461).
- **Where it really comes from:** (36 − 60)² / 60 + (300 − 330)² / 330 + (246 − 198)² / 198 + (18 − 12)² / 12 = 9.60 + 2.73 + 11.64 + 3.00 = 26.96 (confirmed).
- **Proposed fix (prose only):** "**X-squared = 26.96:** the chi-square statistic. For each class, take (observed − expected)² / expected, then add them up: 9.60 + 2.73 + 11.64 + 3.00 = 26.96. ASA 3 contributes most (11.64)."
- **Changes code:** no

### 05-14 · pingouin's `CLES  NaN` and `alternative` columns are shown and never explained · C
- **Where:** `en/catalog/05-one-group-vs-hypothetical.qmd:264` to `:267`, section `#wilcoxon-signed-rank`, step "Read the output"
- **Text:** (no text: the bullets cover `W_val`, `p_val` and `RBC` only)
- **Problem:** The Python output line is `Wilcoxon  11231.5   two-sided  0.000002  0.337961   NaN`. A beginner who sees `NaN` in a result assumes something went wrong.
- **Where it really comes from:** pingouin's "common language effect size", which it fills in only when two samples are passed; here one column of differences is passed.
- **Proposed fix (prose only):** Add a bullet: "**alternative = two-sided, CLES = NaN** (Python): the test is two-sided. CLES is another effect size that pingouin fills in only when it gets two columns of scores; with one column it's empty (`NaN`), which is not an error."
- **Changes code:** no

## Pages with nothing to report

None.

## Not checked

- Both pages' histograms were not opened (age, OHS, operative time, KOOS JR, BMI). The shape statements beside them ("roughly symmetric", "a ceiling at 100 and a long tail to the left") were accepted as qualitative readings of a plot. The two Kaplan-Meier figures on page 4 were opened and read.
- 05-14: the reason pingouin leaves CLES empty for a one-sample call is from my knowledge of pingouin, not confirmed in its source here. The `NaN` itself is in the frozen output.
- General statements with no number from our data were not tested: "For rare events [the Wald interval] can dip below 0%" (04, line 364), "A one-sided test roughly halves the p-value" (05, line 574), "The estimates are identical but the CIs differ slightly" for log vs log-log (04, line 493).
- Whether page 3 `#paired` is being changed to show the 80 bilateral patients (04-6, 05-5) is outside my pages; I only confirmed that it currently states the number without visible code.
- The proposed code lines were not rendered (rendering is off limits). Their values were confirmed with separate read-only R and Python runs; the exact printed form in the page may differ slightly (for example `np.int64` wrappers in Python).
