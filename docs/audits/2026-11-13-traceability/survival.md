# Audit findings: survival pages (13, 14)

Checked against `_freeze/en/survival/<page>/execute-results/html.json` (dumped to `work-survival/13-kaplan-meier.md` and `work-survival/14-cox-regression.md`) and the eight frozen figures. Numbers not on the page were confirmed with read-only R and Python snippets on `data/cohort.csv`. No ERROR findings on either page: every quoted number agrees with the data.

## 13-kaplan-meier.qmd

### 13-1 · "the 80 patients who had both sides operated on" is never counted · A
- **Where:** `en/survival/13-kaplan-meier.qmd:35`, callout "💡 How this page works"
- **Text:** "the examples use every case, including the 80 patients who had both sides operated on"
- **Problem:** No visible chunk on the page counts patients with two procedures. The reader cannot tell where 80 comes from.
- **Where it really comes from:** hidden Prose guard, line 689: `sum(table(cohort$patient_id) == 2) == 80`.
- **Proposed fix:** Prose only on this page, once page 14 shows the count (finding 14-2): "…including the 80 patients who had both sides operated on ([page 14](14-cox-regression.qmd#stratified-cox) counts them and shows how to handle them)." If the owner wants it counted here, add one line to each tab of the `#kaplan-meier` chunk, after `cohort` is read:
  - R: `sum(table(cohort$patient_id) == 2)     # patients with two procedures (both sides)`
  - Python: `print((cohort["patient_id"].value_counts() == 2).sum())   # patients with two procedures (both sides)`
- **Changes code:** no (pointer) | yes (if counted here)

### 13-2 · Log-rank p-values and χ² quoted to more digits than R prints · B
- **Where:** `en/survival/13-kaplan-meier.qmd:461`, `:533`, `:537` (Results), section `#log-rank`; and `:757`, exercise 1 Solution
- **Text:** "**Chisq = 0.9 on 1 degree of freedom, p = 0.340:**"; "p < 0.001"; exercise 1: "(log-rank χ² = 0.01, df = 1, p = 0.937)"
- **Problem:** The bullet is written as a quote of R's last line, but R prints `Chisq= 0.9  on 1 degrees of freedom, p= 0.3`. The value 0.340 is only in the Python tab (`0.9116386659614966 0.33968000597546394`, unlabeled). For the implants R prints `p= 5e-08`, which a beginner may not read as "< 0.001". In exercise 1 R prints `Chisq= 0  on 1 degrees of freedom, p= 0.9`, while the Results sentence says χ² = 0.01 and p = 0.937 (Python: `0.006243321559239711 0.9370209370375034`).
- **Where it really comes from:** `approach_logrank$pvalue` (hidden check line 457, guard line 700); exercise values in the guard, line 715. Visible only in the Python output.
- **Proposed fix:** Print the stored values in R, and say what the printout does.
  - R, `#log-rank` two-group chunk, after `approach_logrank`: `approach_logrank$pvalue      # the printout rounds p to one digit; this is the full value`
  - R, exercise 1: 
    ```r
    procedure_logrank <- survdiff(Surv(followup_years, revised) ~ procedure, data = cohort)
    procedure_logrank
    c(procedure_logrank$chisq, procedure_logrank$pvalue)   # the printout rounds both; these are the full values
    ```
  - Python already prints them; no change.
  - Prose, line 461: "**Chisq = 0.9 on 1 degree of freedom:** R's printout rounds p to 0.3; the line below it (and Python's second number) gives p = 0.340. No clear evidence…". Line 533: "p = 5e-08 means 0.00000005, reported as p < 0.001".
- **Changes code:** yes (R only; two added lines and one assignment)

### 13-3 · Observed and Expected revisions appear in R's output only · B
- **Where:** `en/survival/13-kaplan-meier.qmd:460` and `:532`, section `#log-rank`, bullets under each tabset
- **Text:** "the posterior hips had 19 revisions where 16.1 were expected; the anterior hips had 18 where 20.9 were expected"; "implant C had 38 revisions where 16.9 were expected. Implants A (25 vs 34.0) and B (18 vs 30.0)…"
- **Problem:** The Python tab prints only two or three bare numbers (statistic, df, p). A reader on the Python tab cannot find any of the Observed or Expected counts, and the bullets do not say they are R's.
- **Where it really comes from:** R output lines `approach=anterior  145  18  20.9 …`, `approach=posterior 125  19  16.1 …`, `implant=C 137  38  16.9 …`. lifelines does not report them.
- **Proposed fix:** Prose only. Line 460: "**Observed / Expected** (R's table; lifelines prints only the test statistic and the p-value): …". Same words at line 532. Add once: "**N** is the number of procedures in each group."
- **Changes code:** no

### 13-4 · Cumulative incidence of death (24.0%, CI 19.3% to 29.0%) is printed in R only · B
- **Where:** `en/survival/13-kaplan-meier.qmd:635` and `:655` (Results), section `#competing-risks`, "Reading it"
- **Text:** "**The death curve** rises faster: 24.0% of patients had died without a revision by 10 years."; Results: "…when the cumulative incidence of death was 24.0% (95% CI 19.3% to 29.0%)"
- **Problem:** The Python code builds a `death` table but never prints it; its loop prints the revision rows only. A Python reader can only estimate 24% from the plot by eye, and cannot get the CI at all. Also, "rises faster" does not match the first rows R prints: at 2 years death is 0.0530 and revision 0.0595; death is ahead only from about 4 years on.
- **Where it really comes from:** R output row `3 death  10  0.240  0.193  0.290`. Python: computed only in the hidden chunk at lines 612 to 620 (`chk["death_10"]`).
- **Proposed fix:** Print both outcomes in Python by wrapping the existing loop (the hidden chunk still finds `revision`, `death` and `z`):
  ```python
  z = norm.ppf(0.975)
  for outcome, table in [("revision", revision), ("death", death)]:
      for years in [2, 5, 10]:
          row = table.loc[:years].iloc[-1]                                     # last step at or before that time
          spread = np.exp(z * row["se"] / (row["cif"] * np.log(row["cif"])))   # the log-log CI, as in R
          print(outcome, years, round(row["cif"], 3), round(row["cif"] ** (1 / spread), 3), round(row["cif"] ** spread, 3))

  for years in [2, 5, 10]:
      print(years, round(1 - km.survival_function_at_times(years).iloc[0], 3))   # 1 − Kaplan-Meier, for comparison
  ```
  Prose, line 635: "**The death curve** ends higher: 24.0% of patients had died without a revision by 10 years (the `death` row at time 10)." Cheaper prose-only alternative: "(R's `death` rows; in Python, run the same loop on `death`)".
- **Changes code:** yes (Python) | no (prose-only alternative)

### 13-5 · Numbers at risk in the prose (332, 84) match R's risk table only · B
- **Where:** `en/survival/13-kaplan-meier.qmd:281`, section `#kaplan-meier`, "How to read it"
- **Text:** "600 at surgery, 332 at 4 years and 84 at 8 years"
- **Problem:** The table under the Python plot shows 331 at 4 years and 83 at 8 years. The explanation exists, but two callouts further down (line 290), and it does not name these two numbers.
- **Where it really comes from:** R risk table (`At Risk 600 496 332 187 84 21`); Python risk table (`At risk 600 496 331 187 83 21`). Confirmed: one procedure was censored at exactly 4.00 years and one at exactly 8.00.
- **Proposed fix:** Prose only. Line 281: "…600 at surgery, 332 at 4 years and 84 at 8 years in R (lifelines shows 331 and 83; the R vs Python box below explains why)…". Line 290: "…so a patient censored at exactly 4.00 years is in R's count only: here one at 4 years and one at 8."
- **Changes code:** no

### 13-6 · Gray's test "df = 2" is not in the printed table · B
- **Where:** `en/survival/13-kaplan-meier.qmd:651`, `:655` (Results), section `#competing-risks`; repeated at `:830`
- **Text:** "(Gray's test χ² = 31.5, df = 2, p < 0.001)"; "(χ² = 0.97, p = 0.616)"
- **Problem:** The visible `select()` keeps `statistic_1` and `p.value_1` but drops `df_1`, so df = 2 has no source on the page. The output also calls the statistic `statistic_1`/`statistic_2`, not χ², and prints p as `0.000000142`.
- **Where it really comes from:** hidden guard, line 710: `gray$df_1 == 2`.
- **Proposed fix:** Prose only: "…(Gray's test χ² = 31.5, the `statistic_1` column; df = 2, one less than the three implants; p < 0.001)…; …death differed (`statistic_2`: χ² = 0.97, p = 0.616)." Alternative with code: add `df_1` and `df_2` to the `select()`.
- **Changes code:** no (prose) | yes (if `df_1` is added)

### 13-7 · Exercise 3 quotes a Gray's test its Solution never runs · B
- **Where:** `en/survival/13-kaplan-meier.qmd:827` and `:830`, `#exercises`, exercise 3 Solution
- **Text:** "(Gray's test χ² = 31.5, df = 2, p < 0.001)"; "Python has no Gray's test; take it from R."
- **Problem:** The R solution prints only the three cumulative incidences. Nothing in the Solution produces 31.5. The note "take it from R" sits inside the Python tab and points to R code that is not there.
- **Where it really comes from:** `glance(cif_by_implant)` in the main text, line 646 to 648 (the same test, by implant).
- **Proposed fix:** Prose only. Replace the note at line 827 with a sentence above the Results blockquote, outside the tabset: "Gray's test by implant is the one run in the section above (`glance(cif_by_implant)`): χ² = 31.5, p < 0.001. Python has no Gray's test."
- **Changes code:** no

### 13-8 · "99 days" is not in any output · B
- **Where:** `en/survival/13-kaplan-meier.qmd:211`, section `#time-zero`, bullets under the tabset
- **Text:** "**P4** was revised 99 days after surgery, at 0.27 years."
- **Problem:** Both tabs print years only (`0.271`, `0.271047`). The reader has to subtract two dates in the input table or multiply back by 365.25.
- **Where it really comes from:** hidden guard, line 691: `as.numeric(follow_up$end_date[4] - follow_up$surgery_date[4]) == 99`.
- **Proposed fix:** Prose only: "**P4** was revised at 0.27 years: 0.271 × 365.25 = 99 days after surgery."
- **Changes code:** no

### 13-9 · "2.7 percentage points" needs a subtraction the page does not show · B
- **Where:** `en/survival/13-kaplan-meier.qmd:636`, section `#competing-risks`, "Reading it"
- **Text:** "**1 − Kaplan-Meier** says 22.0% by 10 years. It overstates the real proportion revised by 2.7 percentage points"
- **Problem:** The two inputs are printed (`0.21968772` and `0.193`), the difference is not.
- **Where it really comes from:** hidden guard, line 709: `round(100 * (one_minus_km - revision_rows$estimate[3]), 1) == 2.7`.
- **Proposed fix:** Prose only: "…says 22.0% by 10 years, against a cumulative incidence of 19.3%: 22.0 − 19.3 = 2.7 percentage points too many, because it pretends…"
- **Changes code:** no

### 13-10 · Exercise 2: "100 procedures" and "about a fifth" are left to the reader · B
- **Where:** `en/survival/13-kaplan-meier.qmd:796` and `:798`, `#exercises`, exercise 2 Solution
- **Text:** "Of the 100 procedures in patients aged 75 and over, 41 ended in death and 13 in revision."; "1 − Kaplan-Meier overstates the real proportion revised by about a fifth."
- **Problem:** The count table prints 46, 13 and 41 but not their total. "About a fifth" is a relative difference (16.5 / 13.9 = 1.18), while the main text measured the same gap in percentage points; the switch and the division are not shown.
- **Where it really comes from:** hidden guard, line 716 (`nrow(old) == 100`); "a fifth" is not computed anywhere.
- **Proposed fix:** Prose only. Line 798: "1 − Kaplan-Meier (16.5%) is 2.6 percentage points above the cumulative incidence (13.9%): 16.5 / 13.9 = 1.18, so it overstates the real proportion revised by about a fifth." Before the blockquote: "The three counts add up to the 100 procedures (46 + 13 + 41)."
- **Changes code:** no

### 13-11 · "5.9% at 2 years" against R's printed 0.0595 · B
- **Where:** `en/survival/13-kaplan-meier.qmd:634`, section `#competing-risks`, "Reading it"
- **Text:** "5.9% at 2 years, 12.8% at 5 years and 19.3% at 10 years"
- **Problem:** R prints `revision  2  0.0595`, which a reader rounds to 6.0%. Python prints `0.059`. The unrounded value is 0.05949.
- **Where it really comes from:** `revision_rows$estimate[1]` = 0.0594917 (guard line 705).
- **Proposed fix:** Prose only: "5.9% at 2 years (0.0595 in R's table is 0.05949 before rounding), …".
- **Changes code:** no

### 13-12 · Python prints rows of unlabeled numbers; the bullets use R's column names · C
- **Where:** `en/survival/13-kaplan-meier.qmd:311` (read at `:334` to `:337`), `:446`, `:518`, `:605` (read at `:634` to `:636`)
- **Text:** output such as `2 0.939 [0.916, 0.956] 496` and `10 0.193 0.153 0.237 0.22`; bullets headed "**survival:**", "**n.risk:**", "**n.event:**"
- **Problem:** A beginner on the Python tab has to work out from the `print()` call which number is which. "n.event" has no Python counterpart at all, and in the competing-risks row the fifth number (1 − Kaplan-Meier) sits next to the CI without a label.
- **Where it really comes from:** the numbers are all there; only the labels are missing.
- **Proposed fix:** Prose only, one sentence after each bullet list. Line 337: "Python prints the same numbers in one row per time: years, survival, [lower, upper] and the number at risk; it has no n.event." Line 461: "Python prints the test statistic, then p." Line 636: "Python's rows read: years, cumulative incidence of revision, lower and upper CI limit, 1 − Kaplan-Meier."
- **Changes code:** no

### 13-13 · Toy example: the "Year 2" bullet has no row in R's output · C
- **Where:** `en/survival/13-kaplan-meier.qmd:112` to `:116`, section `#censoring`
- **Text:** "Reading the output, one revision at a time: … **Year 2:** B is censored. Nothing happens to the curve, but the at-risk group shrinks to 4."
- **Problem:** R's `summary()` lists only the times with a revision (1, 3, 5), so an R reader finds no year 2 or year 4. Python lists every time, and at 2.0 shows `at_risk 5`, not 4. R also prints `std.err` and a CI whose upper limit is 1 on every row; neither is mentioned.
- **Where it really comes from:** R rows `1 6 1 0.833`, `3 4 1 0.625`, `5 2 1 0.312`; Python `event_table` rows 0.0 to 6.0.
- **Proposed fix:** Prose only. Before the bullets: "R's table has a row only when a revision happens; Python's has a row for every time, with the patients at risk just before it." Year 2 bullet: "…the at-risk group shrinks from 5 to 4 for the next revision." After the bullets: "The CIs are very wide (the upper limit is 1) because there are only six patients."
- **Changes code:** no

## 14-cox-regression.qmd

### 14-1 · The single hazard ratio for approach (1.37, CI 0.72 to 2.61, log 0.31) is never printed · A
- **Where:** `en/survival/14-cox-regression.qmd:360` and `:362`, section `#proportional-hazards`, "Now a real violation"
- **Text:** "…the dashed line, which marks the model's single hazard ratio of 1.37 (log hazard ratio 0.31)."; "That single hazard ratio (1.37, 95% CI 0.72 to 2.61) mixes a large early effect…"
- **Problem:** `approach_model` is fitted in both tabs but its summary is never shown; only the `cox.zph()` test and the plot are. The four numbers appear nowhere in the output. The dashed line can only be read off the plot by eye.
- **Where it really comes from:** hidden guard, line 697: `round(exp(coef(approach_model)), 2) == 1.37, round(exp(confint(approach_model)), 2) == c(0.72, 2.61)`. The 0.31 is not checked anywhere (confirmed: coef = 0.3132).
- **Proposed fix:** Print the model before testing it.
  - R, after the `approach_model <- coxph(...)` line:
    ```r
    coef(approach_model)                   # the log hazard ratio: where the dashed line will sit
    summary(approach_model)$conf.int       # the single hazard ratio the model assumes, with its 95% CI
    ```
  - Python, after the fit:
    ```python
    print(approach_model.summary[["coef", "exp(coef)", "exp(coef) lower 95%",
                                  "exp(coef) upper 95%"]].round(3).to_string())   # log hazard ratio, hazard ratio, 95% CI
    ```
  - Prose, new first bullet: "**The model:** one hazard ratio for the whole follow-up, 1.37 (95% CI 0.72 to 2.61); `coef`, 0.31, is its logarithm." Add `round(coef(approach_model), 2) == 0.31` to the guard.
- **Changes code:** yes

### 14-2 · "80 bilateral patients", "only 20 of the 80 had a revision" · A
- **Where:** `en/survival/14-cox-regression.qmd:31` (callout), `:497` and `:545`, section `#stratified-cox`
- **Text:** "80 patients in the cohort had both sides replaced."; "Only 20 of the 80 bilateral patients had a revision, so the pairing matters little in this cohort."
- **Problem:** No visible code counts bilateral patients or their revisions. The 20 carries the argument for why robust standard errors change so little, and the reader cannot check it.
- **Where it really comes from:** hidden guard, lines 671 and 705: `bilateral <- cohort |> group_by(patient_id) |> filter(n() == 2)`, `n_distinct(bilateral$patient_id) == 80`, `n_distinct(bilateral$patient_id[bilateral$revised == 1]) == 20`.
- **Proposed fix:** Add a short tabset after the "Bilateral patients." paragraph (line 497), before the three choices (both snippets tested: 80 and 20).
  - R:
    ```r
    bilateral <- cohort |>
      group_by(patient_id) |>
      filter(n() == 2) |>                             # patients with two procedures
      summarise(any_revision = any(revised == 1))     # one row per patient: was either joint revised?
    nrow(bilateral)                                   # bilateral patients
    sum(bilateral$any_revision)                       # of them, patients with a revision
    ```
  - Python:
    ```python
    per_patient = cohort.groupby("patient_id")["revised"].agg(["size", "max"])   # procedures and any revision, per patient
    bilateral = per_patient[per_patient["size"] == 2]                             # patients with two procedures
    print(len(bilateral), bilateral["max"].sum())                                 # bilateral patients; of them, with a revision
    ```
  - The guard already defines `bilateral` differently (line 671); rename one of them. Add a hidden agreement check for the two counts.
- **Changes code:** yes

### 14-3 · "it rests on 16 early revisions" is not shown · A
- **Where:** `en/survival/14-cox-regression.qmd:483`, section `#remedies`, text under the split-follow-up tabset
- **Text:** "The CI for the early effect is wide because it rests on 16 early revisions."
- **Problem:** Neither tab prints how many revisions fell in the first 6 months. The count that explains the wide CI even better, 2 anterior against 14 posterior, is not on this page at all (page 13's 6-month table shows it as `n.event`).
- **Where it really comes from:** hidden guard, line 702: `sum(tha$revised == 1 & tha$followup_years <= 0.5) == 16`.
- **Proposed fix:** Add one line to each tab, before the split (both tested):
  - R: `tha |> filter(revised == 1, followup_years <= 0.5) |> count(approach)   # revisions in the first 6 months`
  - Python: `print(tha[(tha["revised"] == 1) & (tha["followup_years"] <= 0.5)]["approach"].value_counts())   # revisions in the first 6 months`
  - Prose: "The CI for the early effect is wide because it rests on 16 early revisions, 14 after the posterior approach and only 2 after the anterior approach." Extend the guard to `c(2, 14)`.
- **Changes code:** yes

### 14-4 · Proportional-hazards p-values: prose says 0.359 and 0.106, R prints 0.36 and 0.11, Python has neither · B
- **Where:** `en/survival/14-cox-regression.qmd:296`, section `#proportional-hazards`, "First, the adjusted model"; repeated in the Results at `:653`
- **Text:** "No predictor's hazard ratio clearly changed over time (global test p = 0.359; BMI had the smallest p-value, 0.106)."; Results: "(test of proportional hazards, global p = 0.359)"
- **Problem:** R prints `bmi_5 2.6106 1 0.11` and `GLOBAL 5.4935 5 0.36`, two digits. The three-digit values are not on the page. The Python tab has no global line and gives BMI `0.100002`; the box that explains the two versions of the test comes one subsection later (line 371) and does not say that lifelines has no global test.
- **Where it really comes from:** hidden guard, lines 692 to 694: `adjusted_zph$table["GLOBAL", "p"]` = 0.3587, `["bmi_5", "p"]` = 0.1062.
- **Proposed fix:**
  - R: print the table behind the printout: `cox.zph(adjusted_model)$table    # one test per predictor, and a global test; $table keeps every digit` (tested: p column shows 0.3026162, 0.7545598, 0.7392927, 0.1061536, 0.3586605). `print(..., digits = 3)` does not help; it still prints 0.36.
  - Prose, line 296: "…(R's `GLOBAL` line: p = 0.359; BMI had the smallest p-value, 0.106). lifelines has no global test, tests implant B and C separately, and uses a slightly different formula, so its BMI p-value is 0.100; the R vs Python box below explains."
- **Changes code:** yes (R, one line)

### 14-5 · "2.85 times as many" cannot be reproduced from the quoted percentages · B
- **Where:** `en/survival/14-cox-regression.qmd:119`, section `#hazard-ratio`, callout "⚠️ Watch out: a hazard ratio isn't a risk ratio"; chunks at `:126` to `:136`
- **Text:** "By 5 years, 28.9% of implant C knees and hips had been revised (1 − Kaplan-Meier), against 10.1% of implant A: 2.85 times as many, not 3.07."
- **Problem:** The division is not shown, and 28.9 / 10.1 = 2.86, not 2.85. The 2.85 comes from the unrounded values. The numbers are also quoted before the output that shows them, and that tabset follows the callout with no sentence to introduce it.
- **Where it really comes from:** output `[1] 0.10143478 0.07591293 0.28862332`; ratio in the hidden guard, line 686: `round(risk_5[3] / risk_5[1], 2) == 2.85`.
- **Proposed fix:** Prose only: "…against 10.1% of implant A (the code below): 0.2886 / 0.1014 = 2.85 times as many, not 3.07." With code instead, R: `risk_5 <- 1 - summary(km_by_implant, times = 5)$surv`, `risk_5`, `risk_5[3] / risk_5[1]   # C against A: the risk ratio`; Python: collect the three risks in a dict and print `risk["C"] / risk["A"]`.
- **Changes code:** no (prose) | yes (if the ratio is computed)

### 14-6 · "Reading the output, line by line" follows R's printout; Python lacks four of the items · B
- **Where:** `en/survival/14-cox-regression.qmd:104` to `:110`, section `#hazard-ratio`
- **Text:** "**n = 600, number of events = 81:**"; "**se(coef), z, Pr(>|z|):** … (p < 0.001 for C…)"; "**lower .95 / upper .95:**"; "the likelihood ratio test (27.6 on 2 df, p < 0.001) … Python prints the concordance and then this test under the table."
- **Problem:** Python prints no n and no number of events, calls the columns `p`, `exp(coef) lower 95%` and `exp(coef) upper 95%`, shows C's p as `0.000`, and prints the likelihood ratio statistic alone (`27.63546691821921`), without df or p. R shows the same p-values as `1.39e-05` and `p=1e-06`.
- **Where it really comes from:** R output lines `n= 600, number of events= 81` and `Likelihood ratio test= 27.64  on 2 df,   p=1e-06`.
- **Proposed fix:** In Python, replace the last line and add one (tested: prints `600 81` and `27.635… 2 9.98e-07`):
  ```python
  print(len(cohort), cohort["revised"].sum())                        # procedures and revisions
  overall = implant_model.log_likelihood_ratio_test()                # overall likelihood ratio test
  print(overall.test_statistic, overall.degrees_freedom, overall.p_value)
  ```
  Prose: name both labels in each bullet ("**Pr(>|z|)** (Python: **p**)", "**lower .95 / upper .95** (Python: **exp(coef) lower 95% / upper 95%**)") and add "1.39e-05 means 0.0000139; Python rounds it to 0.000. Report both as p < 0.001."
- **Changes code:** yes (Python) | no (labels only)

### 14-7 · Fine-Gray output calls the estimate "HR"; the prose calls it SHR · B
- **Where:** `en/survival/14-cox-regression.qmd:572` and `:573`, section `#fine-gray`
- **Text:** "**Implant C:** SHR 3.09 (95% CI 1.86 to 5.14)"; "**Age:** SHR 1.07 per 10 years (95% CI 0.86 to 1.33), against a cause-specific HR of 1.22"
- **Problem:** `crr()` prints a column headed `HR`. The page then warns the reader never to call this number a hazard ratio, without saying that the printout does. The 1.22 it is compared with was printed about 400 lines earlier.
- **Where it really comes from:** output rows `implantC  1.13  0.259  3.09  1.86, 5.14  <0.001` and `age_10  0.067  0.113  1.07  0.86, 1.33  0.55`; 1.22 is `age_10 1.2246225` in the `#univariable-multivariable` output.
- **Proposed fix:** Prose only. Before the bullets: "`crr()` heads the column `HR`; these are the subdistribution hazard ratios. Compare them with the cause-specific model (`adjusted_model`, [above](#univariable-multivariable)):"
- **Changes code:** no

### 14-8 · "81 of 600 procedures (13.5%)" · B
- **Where:** `en/survival/14-cox-regression.qmd:653`, section `#reporting`, Results
- **Text:** "During follow-up, 81 of 600 procedures (13.5%) were revised."
- **Problem:** The percentage is not printed or worked out, and 81 and 600 were last shown at the top of the page, in R's output only.
- **Where it really comes from:** hidden guard, line 677: `round(100 * 81 / 600, 1) == 13.5`.
- **Proposed fix:** Prose only, in the sentence that introduces the blockquote: "The first sentence gives the events: 81 revisions in 600 procedures (the first line of the implant model's output), 81 / 600 = 13.5%."
- **Changes code:** no

### 14-9 · R's `exp(-coef)` column is printed seven times and never explained · C
- **Where:** `en/survival/14-cox-regression.qmd:104` to `:110` (first seen), then the outputs at `:171`, `:385`, `:429`, `:510`, and exercises 1 and 3
- **Text:** output header `exp(coef) exp(-coef) lower .95 upper .95`
- **Problem:** A beginner sees a second "ratio" column next to every hazard ratio (for example `sexMale 0.5065688 1.9740655`) and has to guess what it is. Python has no such column.
- **Where it really comes from:** R's `summary(coxph)$conf.int`.
- **Proposed fix:** Prose only, one bullet at line 108: "**exp(-coef):** the same hazard ratio the other way round (implant A against C: 1 / 3.07 = 0.33). R prints it for convenience; Python doesn't."
- **Changes code:** no

### 14-10 · The clustered model's p-values are printed in scientific notation and not read · C
- **Where:** `en/survival/14-cox-regression.qmd:509` (output), bullets at `:544` to `:545`, section `#stratified-cox`
- **Text:** output column `Pr(>|z|)`: `5.463870e-01`, `6.743766e-06`, `1.006948e-01`, `4.847144e-03`, `7.712846e-01`
- **Problem:** The visible code selects the p-value column, but the bullets never mention it, and `5.463870e-01` is hard for a beginner to read as 0.546. These are the p-values that reappear, rounded, in the final table (0.546, <0.001, 0.101, 0.005, 0.771), so the link is worth making.
- **Where it really comes from:** `summary(clustered_model)$coefficients`.
- **Proposed fix:** Prose only, a third bullet: "**Pr(>|z|):** the p-values, now from the robust standard errors. R prints them in scientific notation: 5.46e-01 is 0.546 and 6.74e-06 is 0.00000674 (p < 0.001). The table in [Reporting](#reporting) shows them rounded." Or wrap the R call in `round(..., 3)`, which changes code.
- **Changes code:** no

### 14-11 · The final table's univariable CIs differ from the ones at the top of the page · C
- **Where:** `en/survival/14-cox-regression.qmd:586`, section `#reporting`, sentence before the table
- **Text:** "Both columns use robust standard errors clustered on patient ([above](#stratified-cox)), so their CIs allow for the bilateral patients."
- **Problem:** The table gives implant C's univariable CI as 1.87 to 5.04 and implant B's p as 0.511; the first section gave 1.85 to 5.09 and 0.514 for the same model. The reason is in the sentence, but the reader is not told the numbers will differ.
- **Where it really comes from:** table rows `C 3.07 1.87, 5.04` and `B 0.82 0.45, 1.49 0.511`; first output `implantC … 1.8502 5.085`, `implantB … 0.514`.
- **Proposed fix:** Prose only, add: "That is why the univariable CI for implant C here (1.87 to 5.04) differs a little from the one at the top of the page (1.85 to 5.09), which used ordinary standard errors."
- **Changes code:** no

## Pages with nothing to report

None.

## Not checked

- The German and French pages (out of scope). Every code-changing fix above (13-2, 13-4, 14-1, 14-2, 14-3, 14-4, optionally 13-1, 13-6, 14-5, 14-6) must be copied to `de/` and `fr/` and all three pages re-rendered.
- The built site in `_site/` and the Word output (not used, as instructed).
- Statements about library internals that no output on the page can confirm: lifelines' default convergence differing "in the fifth or sixth digit" (14, line 114), `AalenJohansenFitter` moving tied times (13, line 668), robust standard errors agreeing exactly without ties (14, hidden comment line 537).
- Qualitative plot readings ("the curves cross", "points near +2 are posterior hips", "the solid line falls below the dashed line") were compared with the frozen figures by eye only.
- Proposed snippets were run stand-alone against `data/cohort.csv` (13-1, 13-2, 13-4, 14-1, 14-2, 14-3, 14-4, 14-6), not inside a page render, so their effect on the hidden agreement checks and the site tests is untested. The code alternatives in 13-6 and 14-5 were not run.
