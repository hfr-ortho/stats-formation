# Audit findings: page 18 and the front pages

Pages audited: `en/report/18-example-report.qmd`, `en/getting-started/using-this-site.qmd`, `en/getting-started/setup.qmd`, `en/getting-started/real-data.qmd`, `en/index.qmd`, `en/choose-a-test.qmd`, `en/tests-a-z.qmd`.

Notes on these findings:

- No ERROR was found: every number I checked agrees with the output.
- Grading of percentages on page 18: where the prose gives both counts ("15 of the 46 THA patients (32.6%)") and both counts are printed, I graded B, not A. The reader can divide, but no visible code does it, and the only place the page computes the percentage is the hidden Prose guard.
- Every proposed code line was run against `data/` and gives the numbers the prose quotes, except the two version lines in 18-2 and the two solution blocks in gs-use-1, which are standard calls I ran only in part.
- Page 18 says of its manuscript (line 648): "Every number in it comes from the code above". Findings 18-1 to 18-4, 18-6 and 18-7 are the manuscript numbers for which that is not yet true of the *visible* code.

## 18-example-report.qmd

### 18-1 · The study period in the Methods is printed nowhere · A
- **Where:** `en/report/18-example-report.qmd:668`, section `#methods`, "Patients and data"
- **Text:** "We studied 120 primary THAs and TKAs performed at two sites (60 at each) between January 2015 and November 2024."
- **Problem:** No visible chunk prints a surgery date, so the reader cannot find where "January 2015" and "November 2024" come from. Steps 2 and 3 only check the dates against the registry.
- **Where it really comes from:** the hidden Prose guard, line 711: `format(min(study$surgery_date), "%B %Y") == "January 2015"`, `format(max(study$surgery_date), "%B %Y") == "November 2024"`. The actual dates are 2015-01-22 and 2024-11-11.
- **Proposed fix:** print the range in Step 2, in the chunk that joins the registry (after `count(study, procedure)`, line 257, and after the `value_counts()` line, 270).
  R:
  ```r
  range(study$surgery_date)   # the first and the last surgery date, for the Methods
  ```
  Python:
  ```python
  print(study["surgery_date"].min().date(), study["surgery_date"].max().date())   # the first and the last surgery date, for the Methods
  ```
  Then extend line 287: "53 THAs and 67 TKAs. The last line gives the first and the last surgery date: the study period runs from January 2015 to November 2024."
- **Changes code:** yes

### 18-2 · The software versions in the Methods are printed nowhere · A
- **Where:** `en/report/18-example-report.qmd:672`, section `#methods`, "Statistical analysis"
- **Text:** "Analyses used R 4.6 and Python 3.13."
- **Problem:** No visible output shows either version, and the page never says how to find them. (The least important A: these are not results, but they are numbers in the Methods that a reader will have to replace with their own.)
- **Where it really comes from:** the hidden Prose guard, lines 731 to 732 (`R.version$major`, `R.version$minor`, `reticulate::py_config()$version`).
- **Proposed fix:** add a short tabset in Step 8 (inside the html-only block, before line 659), introduced by: "The Methods name the software versions. Ask each language for its own:"
  R:
  ```r
  R.version.string   # the R version, for the Methods
  ```
  Python:
  ```python
  import sys
  print(sys.version.split()[0])   # the Python version, for the Methods
  ```
  On this machine these print `R version 4.6.0 (2026-04-24)` and `3.13.5`. Add: "The manuscript quotes them as R 4.6 and Python 3.13."
  Prose-only alternative (weaker, shows no output): "The versions are what `R --version` and `uv run python --version` print in the terminal."
- **Changes code:** yes (no, for the alternative)

### 18-3 · How many patients have both scores: 93, 77.5%, 86.8% and 70.1% are never computed · B
- **Where:** `en/report/18-example-report.qmd:492`, section `#distributions`; and `:678`, section `#results`, paragraph 2
- **Text:** "93 of the 120 patients have both scores: 46 THA and 47 TKA." / "Both scores were available for 93 patients (77.5%): 46 of 53 after THA (86.8%) and 47 of 67 after TKA (70.1%)."
- **Problem:** The output shows 46 and 47 (Step 5) and 53 and 67 (Step 2). The total 93 and the three percentages are printed nowhere: the reader has to add, then divide numbers from two different steps.
- **Where it really comes from:** the hidden Prose guard, lines 703 and 718 to 719 (`both_counts`, `round(100 * 93 / 120, 1) == 77.5`, `round(100 * both_counts$both / both_counts$n, 1) == c(86.8, 70.1)`).
- **Proposed fix:** add to the Step 5 chunks, after the summary is printed (R line 455, Python line 475).
  R:
  ```r
  # how many patients have both scores: overall, then by procedure
  nrow(analysed)                        # patients with both scores
  100 * nrow(analysed) / nrow(study)    # ... as a percentage of all patients
  study |>
    group_by(procedure) |>
    summarise(n = n(),                                     # all patients
              both = sum(!is.na(prom_1yr - prom_preop)),   # patients with both scores
              pct = 100 * both / n)                        # ... as a percentage
  ```
  Python:
  ```python
  # how many patients have both scores: overall, then by procedure
  print(len(analysed), round(100 * len(analysed) / len(study), 1))   # the count, and as a percentage of all patients
  both = (study["prom_1yr"] - study["prom_preop"]).notna().groupby(study["procedure"])   # True = has both scores
  print(pd.DataFrame({"n": both.size(), "both": both.sum(), "pct": (100 * both.mean()).round(1)}).to_string())
  ```
  Output: 93 and 77.5; THA 53, 46, 86.8; TKA 67, 47, 70.1. Then line 492 can read: "93 of the 120 patients (77.5%) have both scores: 46 of 53 THA patients (86.8%) and 47 of 67 TKA patients (70.1%)."
- **Changes code:** yes

### 18-4 · The ceiling percentages 32.6% and 14.9% are never computed · B
- **Where:** `en/report/18-example-report.qmd:494`, section `#distributions`; and `:678`, section `#results`, paragraph 2
- **Text:** "15 of the 46 THA patients (32.6%) scored the maximum, 100, at 1 year, against 7 of the 47 TKA patients (14.9%)."
- **Problem:** The summary prints the counts (`at_ceiling` 15 and 7) and the group sizes, but not the percentages.
- **Where it really comes from:** the hidden Prose guard, lines 702 and 725 (`ceiling_counts`, `pct = 100 * mean(prom_1yr == 100)`).
- **Proposed fix:** add one column to the summary that is already printed.
  R (lines 452 to 454):
  ```r
  change_summary <- analysed |>
    group_by(procedure) |>
    summarise(n = n(), mean = mean(change), sd = sd(change),
              at_ceiling = sum(prom_1yr == 100),               # patients with the maximum score at 1 year
              pct_at_ceiling = 100 * mean(prom_1yr == 100))    # ... as a percentage of the group
  ```
  Python (lines 473 to 474): add to `.agg(...)`
  ```python
  pct_at_ceiling=("prom_1yr", lambda s: 100 * (s == 100).mean())   # ... as a percentage of the group
  ```
  Both then print 32.6 and 14.9 in the new column. The hidden check and the Prose guard read the other columns by name, so they should be unaffected.
- **Changes code:** yes

### 18-5 · Exercise 3: the four percentages in the Results sentence are never computed; "27" is not derived · B
- **Where:** `en/report/18-example-report.qmd:843` (and the question, `:809`), section `#exercises`, Exercise 3 Solution
- **Text:** "The change score was missing for 7 of 53 THA patients (13.2%) and 20 of 67 TKA patients (29.9%; Fisher's exact test p = 0.046) ... The 1-year score alone was missing for 7 THA patients (13.2%) and 15 TKA patients (22.4%; p = 0.239)." / "27 patients have no change score"
- **Problem:** The solution prints the counts (7, 20, 7, 15) and the two p-values, but none of the percentages, and the denominators 53 and 67 are in Step 2. The 27 in the question is 120 − 93, which is not said.
- **Where it really comes from:** the hidden Prose guard, lines 738 to 741 (`round(100 * c(7 / 53, 20 / 67), 1) == c(13.2, 29.9)`, `round(100 * 15 / 67, 1) == 22.4`).
- **Proposed fix:** question: "27 patients (120 − 93) have no change score". In the solution:
  R, after `table(study$procedure, no_change_score)` (line 819):
  ```r
  round(100 * prop.table(table(study$procedure, no_change_score), margin = 1), 1)   # the same table as row percentages
  ```
  and in the `summarise()` on line 825 add `pct_no_1yr = 100 * mean(is.na(prom_1yr))`.
  Python, after `print(missing_table.to_string())` (line 834):
  ```python
  print(pd.crosstab(study["procedure"], no_change_score, normalize="index").mul(100).round(1).to_string())   # the same table as row percentages
  ```
  and after line 838:
  ```python
  print(study["prom_1yr"].isna().groupby(study["procedure"]).mean().mul(100).round(1).to_string())   # % with no 1-year score
  ```
  These print 13.2 and 29.9, then 13.2 and 22.4.
- **Changes code:** yes

### 18-6 · Results: 44.2% and 55.8% are never computed · B
- **Where:** `en/report/18-example-report.qmd:676`, section `#results`, paragraph 1
- **Text:** "Of the 120 patients, 53 (44.2%) had a THA and 67 (55.8%) a TKA"
- **Problem:** Step 2 prints 53 and 67, and Table 1's header shows N = 53 and N = 67, but no output shows the percentages.
- **Where it really comes from:** the hidden Prose guard, line 712 (`round(100 * 53 / 120, 1) == 44.2`).
- **Proposed fix:** in Step 2.
  R (replace line 257):
  ```r
  count(study, procedure) |>
    mutate(pct = 100 * n / sum(n))   # each procedure as a percentage of all cases
  ```
  Python (add after line 270):
  ```python
  print(study["procedure"].value_counts(normalize=True).sort_index().mul(100).round(1).to_string())   # as percentages
  ```
  Then line 287: "53 THAs (44.2%) and 67 TKAs (55.8%)."
- **Changes code:** yes

### 18-7 · Women: the text says 71.7% and 49.3%, the R table and the manuscript's own Table 1 say 72% and 49% · B
- **Where:** `en/report/18-example-report.qmd:676`, section `#results`, paragraph 1 (compare `:425`, section `#table-1`)
- **Text:** "Women made up 38 of 53 THA patients (71.7%) and 33 of 67 TKA patients (49.3%; SMD 0.47)."
- **Problem:** The one-decimal percentages appear only in the Python tab (`38 (71.7)`, `33 (49.3)`). The R table prints `38 (72%)` and `33 (49%)`, and Step 4's prose uses 72% and 49%. Table 1 of the manuscript is the R table, so it shows 72% and 49% next to a text that says 71.7% and 49.3%.
- **Where it really comes from:** the Python tableone output; in R only the hidden Prose guard, line 715.
- **Proposed fix:** make the R table print one decimal, as the rest of the manuscript does. In `tbl_summary()` (line 382):
  ```r
  digits = list(all_continuous() ~ 1, all_categorical() ~ c(0, 1)),   # 1 decimal for means, SDs and percentages
  ```
  The table then shows `38 (71.7%)` and `33 (49.3%)` (tested), and Step 4's prose can say 71.7% and 49.3% too. Python needs no change.
  Prose-only alternative: write "(72%)" and "(49%)" in the Results, matching Table 1.
- **Changes code:** yes (no, for the alternative)

### 18-8 · Exercise 1: R prints "p-value = 0.0035", the Results sentence says p = 0.003 · B
- **Where:** `en/report/18-example-report.qmd:773`, section `#exercises`, Exercise 1 Solution
- **Text:** "The Hodges-Lehmann difference in the change was 9.5 points (95% CI 3.6 to 15.2; p = 0.003)."
- **Problem:** A reader on the R tab sees `W = 1461.5, p-value = 0.0035` and would round it to 0.004. The sentence is right (the p-value is 0.0034996), but only the Python tab shows enough digits to see that.
- **Where it really comes from:** output line "W = 1461.5, p-value = 0.0035" (R, already rounded); "1461.5 0.0034996103353091236" (Python).
- **Proposed fix:** add to line 775: "R prints the p-value as 0.0035, which it has already rounded; the Python tab shows it is 0.0034996, so to three decimals it is 0.003. The estimate is the `difference in location` line, 9.499948, and the CI is the two numbers under `95 percent confidence interval`." If R readers should see it in their own tab, store the test and add `rank_check$p.value   # the p-value with all its digits` (a code change).
- **Changes code:** no (yes, with the optional R line)

### 18-9 · Exercise 2: the sign changes from 9.0 to −7.4, the outcome changes, and R prints p as `1.656337e-03` · B
- **Where:** `en/report/18-example-report.qmd:804` and `:806`, section `#exercises`, Exercise 2 Solution
- **Text:** "Adjusted for the pre-op score, the difference in the 1-year score between TKA and THA was −7.4 points (95% CI −11.9 to −2.9; p = 0.002)." / "The difference shrinks a little from the unadjusted 9.0 points but doesn't go away"
- **Problem:** Three unexplained steps.
  1. The solution never says which output row to read (`procedureTKA` in R, `procedure[T.TKA]` in Python) or that it is TKA minus THA, the opposite order to Step 6's 9.0 (THA minus TKA). A beginner sees "9.0 shrinks to −7.4".
  2. 9.0 is a difference in the *change*, −7.4 a difference in the *1-year score*; why the two can be compared is not said. The unadjusted difference in the 1-year score itself is 90.6 − 83.9 = 6.7 points, which a reader who checks will find and be confused by.
  3. R prints the p-value as `1.656337e-03`; other pages gloss this notation ("R prints `1.28e-14`"), this one doesn't. Python's CI columns are headed `0` and `1`, unexplained.
- **Where it really comes from:** output lines "procedureTKA -7.3642535 2.2703235 -3.243702 1.656337e-03" and "procedureTKA -11.87464731 -2.8538596" (R); "procedure[T.TKA] -7.364", "procedure[T.TKA] -11.875 -2.854", "procedure[T.TKA] 0.002" (Python).
- **Proposed fix:** replace line 806 with: "Read the `procedureTKA` row (Python: `procedure[T.TKA]`; its CI is in the columns headed `0` and `1`). The coefficient is TKA minus THA, so −7.4 means that, at the same pre-op score, TKA patients scored 7.4 points lower at 1 year. R prints the p-value as `1.656337e-03`, which is 0.001656. Once the pre-op score is in the model, a difference in the 1-year score is also a difference in the change, so compare it with Step 6: there THA minus TKA was 9.0 points, here it is 7.4. The difference shrinks a little but doesn't go away, so the higher starting point explains only part of it."
- **Changes code:** no

### 18-10 · Step 6: the difference of 9.0 points is printed only in the Python tab · B
- **Where:** `en/report/18-example-report.qmd:550`, section `#primary-analysis`, "Reading it"
- **Text:** "THA patients improved by 42.4 points on average and TKA patients by 33.4, a difference of 9.0 points (95% CI 3.5 to 14.6)."
- **Problem:** R's `t.test()` prints the two means (42.42174 and 33.40426) and the CI, but not the difference. Python prints `difference = 9.017...`. A reader on the R tab has to subtract, and isn't told to.
- **Where it really comes from:** Python output line "difference = 9.017483811285857 95% CI 3.480506352222995 to 14.554461270348718"; in R, 42.42174 − 33.40426.
- **Proposed fix:** prose: "... a difference of 9.0 points (95% CI 3.5 to 14.6). R prints the two means under `sample estimates` but not their difference: 42.42 − 33.40 = 9.02. Python prints it on the `difference =` line. The CI is under `95 percent confidence interval` in R."
- **Changes code:** no

### 18-11 · Step 7: the numbers at risk (17 at 8 years, 5 at 10) exist only under the R plot · B
- **Where:** `en/report/18-example-report.qmd:639`, section `#survival`
- **Text:** "The numbers at risk under the R plot show how quickly the data thin out: 17 patients were still followed at 8 years and 5 at 10"
- **Problem:** The prose names the R plot, so R readers can find them (the "At Risk" row reads 120, 102, 77, 41, 17, 5). The Python plot has no risk table and no Python output gives the two numbers.
- **Where it really comes from:** the risk table drawn by `add_risktable()`; the hidden Prose guard, line 727 (`sum(study$followup_years >= 8) == 17`).
- **Proposed fix:** add to the Python chunk, before the plot (line 615):
  ```python
  # the numbers at risk: patients still followed at 0, 2, 4, 6, 8 and 10 years
  print([int((study["followup_years"] >= years).sum()) for years in range(0, 12, 2)])
  ```
  It prints `[120, 102, 77, 41, 17, 5]`, the same as R's row. In the prose: "(the `At Risk` row under the R plot; the list printed before the Python plot)".
- **Changes code:** yes

### 18-12 · Step 7: the output gives proportions, the prose percentages · B
- **Where:** `en/report/18-example-report.qmd:639`, section `#survival` (and `:680`, section `#results`)
- **Text:** "The cumulative incidence of revision was 3.4% (95% CI 1.1% to 7.8%) at 2 years and 12.6% (95% CI 7.0% to 19.8%) at 5 years."
- **Problem:** The outputs print 0.0339, 0.0111, 0.0784 and 0.126, 0.0703, 0.198 (R) and 0.034, 0.011, 0.078 (Python). The step from a proportion to a percentage, and which column is which, is not said.
- **Where it really comes from:** output lines "2 0.0339 0.0111 0.0784" and "5 0.126 0.0703 0.198" (R, columns `estimate`, `conf.low`, `conf.high`; Python `cif`, `low`, `high`).
- **Proposed fix:** add one sentence before it: "The table gives proportions, so multiply by 100: at 2 years the `estimate` (Python: `cif`) is 0.0339, or 3.4%, and its CI runs from 0.0111 to 0.0784."
- **Changes code:** no

### 18-13 · Step 4: "2.9 points higher" is a subtraction the prose doesn't show · B
- **Where:** `en/report/18-example-report.qmd:425`, section `#table-1`
- **Text:** "TKA patients started 2.9 points higher on average"
- **Problem:** 2.9 is not in the table; it is 51.0 − 48.1 from the last row.
- **Where it really comes from:** Table 1 row "Pre-op score (HOOS JR or KOOS JR), points 48.1 (11.5) 51.0 (11.8)"; the hidden Prose guard, line 717.
- **Proposed fix:** "TKA patients started 2.9 points higher on average (51.0 against 48.1, the table's last row)".
- **Changes code:** no

### 18-14 · "They differ in the sixth decimal" cannot be seen in the output · B
- **Where:** `en/report/18-example-report.qmd:556`, section `#primary-analysis`, 🔀 box
- **Text:** "effectsize uses the exact correction, pingouin a close approximation, so with 93 patients they differ in the sixth decimal."
- **Problem:** R prints g as 0.66, Python as 0.6649248297548472. The reader cannot see a sixth-decimal difference. (The claim is true: R's value is 0.66492228.)
- **Where it really comes from:** the hidden check, line 542 (`tol = 1e-5`).
- **Proposed fix:** give both numbers: "so with 93 patients they differ in the sixth decimal: 0.664922 in R (which prints it rounded, as 0.66) and 0.664925 in Python." Or drop the precision: "so they differ far beyond the two decimals you report."
- **Changes code:** no

### 18-15 · "Five spellings of 'missing'", but the visible code lists four · B
- **Where:** `en/report/18-example-report.qmd:48`, section `#tidy`
- **Text:** "five spellings of "missing""
- **Problem:** The code a few lines below has `missing_codes <- c("N/A", "unk", "-", "999")`: four. The fifth is the empty cell, which page 1 says and this page doesn't.
- **Where it really comes from:** page 1, line 97: "`N/A`, `unk`, `-`, `999`, blank | Five ways to say "missing"".
- **Proposed fix:** "five spellings of "missing" (`N/A`, `unk`, `-`, `999` and empty cells)".
- **Changes code:** no

### 18-16 · Step 7, Python: the follow-up quartiles are labeled 0.75, 0.50, 0.25, the reverse of R's 25, 50, 75 · C
- **Where:** `en/report/18-example-report.qmd:601` to `:602`, section `#survival`
- **Text:** output "0.75 4.16 / 0.50 6.05 / 0.25 8.27" against R's "25 50 75 / 4.16 6.05 8.27"; prose (line 639): "The median follow-up was 6.05 years (IQR 4.16 to 8.27)."
- **Problem:** A Python reader sees "0.75 → 4.16" and reads the 75th percentile as 4.16 years. The labels are the share *still followed*, not the percentile; only a code comment hints at it.
- **Where it really comes from:** `qth_survival_times([0.75, 0.5, 0.25], ...)` labels each row with the survival probability.
- **Proposed fix:** relabel before printing (the hidden check reads by position, so it should be unaffected; this line was not run):
  ```python
  follow_up.index = ["25%", "50%", "75%"]   # lifelines labels them by the share still followed: 0.75, 0.50, 0.25
  ```
  Prose-only alternative, after line 639's first sentence: "Python labels the three rows 0.75, 0.50 and 0.25: the share of patients still followed, so 0.75 is the 25th percentile."
- **Changes code:** yes (no, for the alternative)

### 18-17 · The Methods name two methods that Step 7 never explains: "reverse Kaplan-Meier" and "Aalen-Johansen" · C
- **Where:** `en/report/18-example-report.qmd:672`, section `#methods`; Step 7 at `:561`, section `#survival`
- **Text:** "Median follow-up was estimated with the reverse Kaplan-Meier method. The cumulative incidence of revision was estimated with the Aalen-Johansen method"
- **Problem:** In Step 7 "reverse Kaplan-Meier" appears only in a code comment, with no explanation and no link, and "Aalen-Johansen" doesn't appear at all. A reader cannot tie either Methods sentence to the code that did it.
- **Where it really comes from:** page 13, `#follow-up` (line 394) and `#competing-risks` (line 553) explain both.
- **Proposed fix:** in line 561, replace "First, how long were patients followed? Then, what proportion were revised over time?" with: "First, how long were patients followed? The reverse Kaplan-Meier method answers that: it treats the end of follow-up as the event ([page 13](../survival/13-kaplan-meier.qmd#follow-up)). Then, what proportion were revised over time?" Add at the end of the paragraph: "Its estimator is called Aalen-Johansen, the name the Methods use; `survfit()` and `CumIncidenceRight()` both compute it."
- **Changes code:** no

### 18-18 · Step 4: the R and Python tables look different, and the 🔀 box explains only the SMDs · C
- **Where:** `en/report/18-example-report.qmd:393` and `:407`, section `#table-1`; box at `:429`
- **Text:** "Keep a Missing row for every variable that has missing values." (line 369)
- **Problem:** R has a Missing row with a count per group (BMI: 4 and 4); Python has a Missing column with one total (8) and no Missing row. Python also prints a row for each level of the yes/no variables (Diabetes 0 and 1) where R prints one row. A beginner comparing tabs has to work out that these are the same table.
- **Where it really comes from:** the two packages' layouts (gtsummary and tableone).
- **Proposed fix:** add to the 🔀 box: "The layouts differ too. gtsummary adds a Missing row with a count for each group; tableone has a Missing column with the total (BMI: 4 + 4 = 8). For a yes/no variable gtsummary shows only the "yes" row, tableone a row for 0 and a row for 1."
- **Changes code:** no

### 18-19 · "Medium-to-large", "small" and "large" are used without the scale · C
- **Where:** `en/report/18-example-report.qmd:552`, section `#primary-analysis`, "Reading it"
- **Text:** "It's medium-to-large at the point estimate, but the CI runs from a small difference to a large one."
- **Problem:** The reader needs page 6's rule of thumb to see why 0.66 is "medium-to-large" and 0.25 "small"; it isn't on this page.
- **Where it really comes from:** page 6, `#unpaired-t`: "As a rough guide, 0.2 is small, 0.5 medium and 0.8 large."
- **Proposed fix:** "As a rough guide, 0.2 is small, 0.5 medium and 0.8 large ([page 6](../catalog/06-two-unpaired-groups.qmd#unpaired-t)): 0.66 is medium-to-large, but the CI runs from a small difference (0.25) to a large one (1.08)."
- **Changes code:** no

## using-this-site.qmd

### gs-use-1 · The "Try it" answer is a typed comment, not output · B
- **Where:** `en/getting-started/using-this-site.qmd:128` and `:137`, section `#exercises`, Solution
- **Text:** "`median(ages)   # 69`" / "`ages.median()   # 69.0`"
- **Problem:** The two solution blocks are static (` ```r `, ` ```python `), so the page never runs them and the answer is a hand-written comment. It is correct (69), but it is the one solution on my pages whose result is not computed for the reader. CLAUDE.md rule 12 asks for executed solution chunks.
- **Where it really comes from:** not computed anywhere on the page.
- **Proposed fix:** make both blocks executed chunks (`{r}` and `{python}`; the page already has `engine: knitr`), so the page prints the answer.
  R:
  ```r
  ages <- c(64, 71, 58, 69, 75)
  median(ages)   # the middle value when the ages are sorted
  ```
  Python:
  ```python
  import pandas as pd

  ages = pd.Series([64, 71, 58, 69, 75])
  print(ages.median())   # the middle value when the ages are sorted
  ```
- **Changes code:** yes

### gs-use-2 · The illustration's medians differ by 2, its "Hodges-Lehmann difference" is 1, and the term is not explained · C
- **Where:** `en/getting-started/using-this-site.qmd:110`, section `#how-results-are-reported`
- **Text:** "KOOS JR at 1 year was a median of 87 points (IQR 76 to 94) in men and 85 (IQR 73 to 94) in women (Hodges-Lehmann difference 1 point, 95% CI −2 to 4; p = 0.432)."
- **Problem:** On the second page a beginner reads, 87 − 85 = 2 sits next to "difference 1 point". Nothing says that the Hodges-Lehmann difference is not the difference between the medians, the term isn't linked, and "Tests A–Z" has no row for it.
- **Where it really comes from:** an illustration (the numbers appear on no other page).
- **Proposed fix:** add after the blockquote: "The Hodges-Lehmann difference is the median of all the man-minus-woman differences, not the difference between the two medians, so it needn't equal 87 − 85 ([page 6](../catalog/06-two-unpaired-groups.qmd#mann-whitney) explains it)." Or use an illustration with means and a mean difference, which needs no new term.
- **Changes code:** no

### gs-use-3 · "IQR" is used before it is explained · C
- **Where:** `en/getting-started/using-this-site.qmd:101`, section `#how-results-are-reported`
- **Text:** "Continuous, skewed | median (IQR) | length of stay 1 (0 to 2) days"
- **Problem:** SD is spelled out earlier on the page; IQR never is, and the example "1 (0 to 2)" doesn't say which two numbers these are.
- **Where it really comes from:** page 4 has a `#median-iqr` section (link target from the decision table; I did not read it).
- **Proposed fix:** "median (IQR: the interquartile range, from the 25th to the 75th percentile)".
- **Changes code:** no

## setup.qmd

### gs-setup-1 · "Each step ends with a quick check", but steps 4 to 7 have none, and step 1's check points to a step that doesn't mention R · C
- **Where:** `en/getting-started/setup.qmd:6`, `:26`, `:59`, sections `#install-r` to `#install-the-python-packages`
- **Text:** "Each step ends with a quick check." / "**Check:** Positron will find R in step 4."
- **Problem:** Step 4 (Install Positron) says nothing about R, so a Windows reader has no way to check step 1 until step 6. Steps 4, 5, 6 and 7 end without a check, so a beginner can't tell whether `git clone`, `renv::restore()` or `uv sync` worked before running step 8.
- **Where it really comes from:** not applicable (instructions).
- **Proposed fix:** line 26: "**Check:** you'll see R in Positron in step 6." Add checks:
  - Step 5: "**Check:** Positron's file list on the left shows folders such as `data` and `scripts`."
  - Step 6: "**Check:** the R console starts without an error, and `renv::restore()` ends without a line that starts with `Error`."
  - Step 7: "**Check:** `uv sync` ends without an error, and a `.venv` folder appears in the file list."

  The owner should confirm the exact wording against a fresh install (see Not checked). Or change line 6 to "Step 8 checks everything at the end."
- **Changes code:** no

### gs-setup-2 · The page never says how to open Terminal or PowerShell · C
- **Where:** `en/getting-started/setup.qmd:30` and `:36`, section `#install-uv-and-python` (first used at `:26`)
- **Text:** "**Mac:** open Terminal and run:" / "**Windows:** open PowerShell and run:"
- **Problem:** The page is for people who have never coded; many have never opened either app. The "In plain language" box explains R, Python, Positron, Git and uv but not the terminal.
- **Where it really comes from:** not applicable.
- **Proposed fix:** add to the box: "The **terminal** is a window where you type commands: **Terminal** on a Mac (press Cmd+Space, type "Terminal", press Return), **PowerShell** on Windows (open the Start menu, type "PowerShell", press Enter)."
- **Changes code:** no

### gs-setup-3 · "Reading the data without cloning": which steps are still needed, and "any example" needs more than two packages · C
- **Where:** `en/getting-started/setup.qmd:114` and `:142`, section `#reading-the-data-without-cloning`
- **Text:** "You can skip step 5 (cloning) and read the practice data straight from GitHub. You still need the packages, so install them first." / "In any example, replace `"data/"` with ..."
- **Problem:** Steps 6 and 7 install the packages from files inside the clone, so a reader who skips step 5 can't do them. The page installs only readr and readxl (pandas and openpyxl), so an example copied from a tutorial page stops at its first `library()` or `import` line. The reader has to guess which steps apply and which packages to add.
- **Where it really comes from:** not applicable.
- **Proposed fix:** replace line 114 with: "You can skip steps 5 to 8 and read the practice data straight from GitHub, for example to try it in your own project. You still need steps 1 to 4, and the packages below. To run a tutorial page's example this way, also install every package in its `library()` lines (R) or add a `--with` for every package in its `import` lines (Python); cloning installs them all for you."
- **Changes code:** no

## real-data.qmd

### gs-real-1 · "Don't copy them anywhere else", then a repository that reads data from local folders · C
- **Where:** `en/getting-started/real-data.qmd:60` to `:61`, section `#where`
- **Text:** "Keep study data in the project's REDCap database ... Don't copy them anywhere else." / "The repository reads the data at run time from git-ignored folders (`data/raw/`, `db/`, `exports/`)"
- **Problem:** The second bullet describes exactly a copy: an export from REDCap sitting in a folder on a computer. A beginner can't tell whether exporting to their laptop is allowed, on which computer or drive those folders may live, or how the data get there.
- **Where it really comes from:** not applicable; the owner has to supply the rule.
- **Proposed fix:** say in one sentence where an export may be stored and how it gets there, for example: "For the analysis, export only the coded data the protocol allows, into the project's git-ignored `data/raw/` folder on [the owner to name: an HFR computer or drive], and nowhere else." Then change the first bullet's last sentence to "Don't copy them anywhere else than that folder."
- **Changes code:** no

### gs-real-2 · "The secure environment" is never defined · C
- **Where:** `en/getting-started/real-data.qmd:41` and `:63`, sections `#identifiers` and `#where`
- **Text:** "Coarsen them before data leave the secure environment" / "What leaves the secure environment is aggregate"
- **Problem:** Two rules depend on a boundary the page never draws. The reader has to guess whether it means REDCap, the HFR network, an HFR computer, or their own laptop with the private repository.
- **Where it really comes from:** not applicable; the owner has to supply the definition.
- **Proposed fix:** define it at the top of `#where`: "The **secure environment** is [the owner to name: for example REDCap and HFR-managed computers and drives]. Everything else, including personal laptops, email, cloud drives and GitHub, is outside it."
- **Changes code:** no

### gs-real-3 · "Before every commit": a data file that `git status` lists as untracked can't be "unstaged" · C
- **Where:** `en/getting-started/real-data.qmd:79` to `:86`, section `#before-commit`
- **Text:** "Check that no data file, export or screenshot is listed. If you see one, unstage it with `git restore --staged <file>`."
- **Problem:** `git status` lists files in three groups (staged, changed, untracked). The instruction covers only a staged file. If a data file shows under "Untracked files", `git restore --staged` does nothing useful, and the real problem is not mentioned: the file is not ignored, so the next `git add .` will take it. "Staged" is not explained, and the page doesn't say where to run the commands.
- **Where it really comes from:** not applicable.
- **Proposed fix:** "Run these two commands in the project's terminal and read the output. `git status` lists the files git has noticed; `git diff --staged` shows exactly what the next commit will contain ("staged" means marked for the next commit). No data file, export or screenshot may appear in either. If one is listed under "Changes to be committed", take it out with `git restore --staged <file>`. If one is listed under "Untracked files", git is not ignoring it: stop, and ask your project lead to add it to `.gitignore` before you commit anything."
- **Changes code:** no

### gs-real-4 · BASEC and REDCap are named without saying what they are · C
- **Where:** `en/getting-started/real-data.qmd:17` and `:60`, sections `#swiss-rules` and `#where`
- **Text:** "every project gets a BASEC number when it is submitted" / "Keep study data in the project's REDCap database"
- **Problem:** A medical student starting a master's thesis has usually met neither. (HRA, ClinO and CER-VD are explained in the same paragraph.)
- **Where it really comes from:** not applicable.
- **Proposed fix:** "every project gets a BASEC number when it is submitted (BASEC is the Swiss ethics committees' online submission portal)" and "the project's REDCap database (REDCap is a secure web application for collecting and storing study data)".
- **Changes code:** no

## choose-a-test.qmd

### choose-1 · The rows turn on "paired", "unpaired", "matched" and "unmatched", which the page neither explains nor links; the dashes are unexplained · C
- **Where:** `en/choose-a-test.qmd:6` to `:7`, and the table at `:17`, `:22`, `:24`
- **Text:** "Find your **goal** in the left column (for example, *compare two unpaired groups*)."
- **Problem:** Step 2 tells readers where to learn "Gaussian", but step 1 gives no help with paired or matched, although choosing the wrong row is the mistake page 3 calls "one of the most common mistakes in the literature". Four cells hold only "—", with no word on what that means.
- **Where it really comes from:** page 3, `#paired` ("Paired or unpaired? Matched or unmatched?") explains the terms.
- **Proposed fix:** add to step 1: "Not sure whether your groups are paired or unpaired, matched or unmatched? Read [Paired or unpaired?](foundations/03-distributions.qmd#paired) first." Add under the table: "A dash means this site has no test for that combination."
- **Changes code:** no

## Pages with nothing to report

- `en/index.qmd`
- `en/tests-a-z.qmd`. One remark, covered by gs-use-2: effect sizes that appear in Results sentences, such as the Hodges-Lehmann difference and Hedges' g, have no row. The page promises tests and methods, so I did not file it separately.

## Not checked

- **The Word file of page 18.** I read the page source and the html freeze only. The manuscript text is the same source for both formats, so 18-1, 18-2, 18-6 and 18-7 should apply to the .docx too, but I did not open it.
- **The Python figures on page 18** (`unnamed-chunk-22-1.png`, `unnamed-chunk-30-1.png`). I viewed the R histogram and the R cumulative-incidence plot (the "At Risk" row reads 120, 102, 77, 41, 17, 5). For Python I relied on the code, which draws no risk table.
- **Proposed code not fully run.** The R table option in 18-7 was run on a three-column table, not the page's full Table 1. The lines in 18-2 (I printed `R.version.string` and `sys.version`, not the chunks), 18-16 (the relabel) and gs-use-1 (the solution chunks) were not run as written. None was rendered inside the page, so the hidden checks and the Prose guard were not re-run against them.
- **Whether the setup steps work on a clean machine.** I did not install anything. Not verified:
  - the Positron menu and pane names ("language picker at the top right of the Console pane", "Session → Restart R");
  - whether `renv::restore()` needs Rtools on Windows;
  - whether `mkdir -p ~/projects` behaves in PowerShell as in Terminal;
  - the exact success messages of `renv::restore()` and `uv sync`, so the checks proposed in gs-setup-1 need the owner's wording.
- **The legal and institutional content of `real-data.qmd`** (Swiss law, CER-VD, general consent, where HFR stores data). I checked only whether a beginner could follow it. gs-real-1 and gs-real-2 need facts only the owner has. The gloss of BASEC and REDCap in gs-real-4 is from general knowledge, not from the repository.
- **The German and French pages.** Out of scope. Every "Changes code: yes" fix has to be copied into `de/` and `fr/` and all three pages re-rendered.
