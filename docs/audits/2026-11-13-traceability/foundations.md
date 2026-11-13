# Audit findings: foundations pages (01 to 03)

Checked against the frozen output in `_freeze/en/foundations/<page>/execute-results/html.json`. Every number in "Where it really comes from" was confirmed by reading `data/` with a read-only R or Python snippet. The code lines of the main proposed fixes were run against `data/` (outside the pages, with the objects rebuilt the same way) and give the values stated. The two optional alternatives (the demonstration in 02-7 and the plot in 03-5) were not run exactly as written. No ERROR findings on these three pages.

## 01-tidy-data.qmd

### 01-1 · "The notes miss some revisions" is never counted · A
- **Where:** `en/foundations/01-tidy-data.qmd:371`, section `#step-4-recover-the-color-coded-revisions`
- **Text:** "The `Notes` column mentions some revisions ("revised 2021 for loosening"), but not all of them. If we had trusted the notes we would have missed cases. Only the colors were complete."
- **Problem:** The only output in this step is `18`, and the prose never mentions it. Nothing on the page counts how many notes mention a revision, so "not all of them" and "we would have missed cases" cannot be checked. The quoted note "revised 2021 for loosening" is not in the workbook either (the loosening notes are from 2018, 2019, 2024 and 2025).
- **Where it really comes from:** Not computed anywhere, not even in the Prose guard. From the data: 13 of the 18 red-filled cases have a note containing "revised"; 5 do not.
- **Proposed fix:** Add a tabset after the existing one, then rewrite the sentence.

  R:
  ```r
  # Cases whose note mentions a revision
  noted <- step3 |>
    filter(str_detect(notes, "revised")) |>
    pull(study_id) |>
    str_trim()

  length(noted)                         # cases the notes mention
  length(setdiff(revised_ids, noted))   # red-filled cases the notes never mention
  ```
  Python:
  ```python
  # Cases whose note mentions a revision
  has_note = step3["notes"].str.contains("revised", na=False)
  noted = set(step3.loc[has_note, "study_id"].str.strip())

  print(len(noted))                 # cases the notes mention
  print(len(revised_ids - noted))   # red-filled cases the notes never mention
  ```
  Both print 13 and 5. Prose: "The red fill marks 18 revised cases. The `Notes` column mentions a revision ("revised 2019 for loosening") for only 13 of them. If we had trusted the notes we would have missed 5 cases. Only the colors were complete." Add the three numbers to the Prose guard and a hidden agreement check after the pair.
- **Changes code:** yes

### 01-2 · The make-up of the 126 rows is stated, not shown · A
- **Where:** `en/foundations/01-tidy-data.qmd:233`, section `#step-1-read-both-tabs-as-text` (and the unexplained `120` in `#step-2-drop-rows-and-columns-that-arent-data`, line 254)
- **Text:** "126 rows: 60 patients per tab, plus 2 duplicates and a totals row in each."
- **Problem:** The output shows only `126`. Nothing shows 60 patients per tab, 2 duplicates per tab or 1 totals row per tab. Step 2 then prints `120` with no sentence saying why 6 rows went.
- **Where it really comes from:** Not computed in any visible chunk; the Prose guard (line 779) checks only `nrow(raw) == 126`. From the data: 63 rows per tab, 2 `TOTAL` rows in all, 4 exact duplicate rows in all (2 per tab).
- **Proposed fix:** Add three lines to the end of the Step 1 chunks.

  R:
  ```r
  count(raw, site)                            # rows read from each tab
  sum(raw$pt_name == "TOTAL", na.rm = TRUE)   # totals rows
  sum(duplicated(raw))                        # rows that exactly repeat an earlier row
  ```
  Python:
  ```python
  print(raw["site"].value_counts())           # rows read from each tab
  print((raw["pt_name"] == "TOTAL").sum())    # totals rows
  print(raw.duplicated().sum())               # rows that exactly repeat an earlier row
  ```
  They print 63 and 63, then 2, then 4. Prose: "126 rows: 63 from each tab. The 2 totals rows and the 4 duplicated rows (2 on each tab) are not patients, so each tab holds 63 − 1 − 2 = 60 patients." After Step 2's output add: "120 rows are left: 126 − 2 totals rows − 4 duplicates, which is 60 patients per site."
- **Changes code:** yes

### 01-3 · "All zeros" but R's output hides the fifth check · B
- **Where:** `en/foundations/01-tidy-data.qmd:677` (R chunk at 652 to 659), section `#integrity`, check 4
- **Text:** "All zeros: good."
- **Problem:** R prints a one-row tibble too wide for the page. Four checks show 0 and the fifth appears only as "# ℹ 1 more variable: one_year_before_surgery <int>", with no value. Python shows all five. An R reader cannot confirm "all zeros".
- **Where it really comes from:** The value is 0 (Python output line `one_year_before_surgery    0`), but R's printed output cuts it off.
- **Proposed fix:** End the R pipeline with one more step so the checks print one per row:
  ```r
    ) |>
    pivot_longer(everything(), names_to = "check", values_to = "rows")   # one check per line
  ```
  The prose can stay.
- **Changes code:** yes (R only; the German and French pages need the same line)

### 01-4 · 3,928 survey rows are never explained, and the blank answers are never shown · B
- **Where:** `en/foundations/01-tidy-data.qmd:579`, section `#reshaping`
- **Text:** "A KOOS JR patient now has 7 items × 4 visits = 28 rows. A missed visit still has its rows, with the response blank, so "expected but not answered" stays visible."
- **Problem:** The output's headline number is 3,928 rows, which is not a multiple of 28. The page never says the HOOS JR has 6 items, or how many patients answered each instrument, so the reader cannot get from 28 to 3,928. No visible output shows a blank response, so the second sentence cannot be seen either.
- **Where it really comes from:** 82 KOOS JR patients × 28 rows + 68 HOOS JR patients × 24 rows (6 items × 4 visits) = 2,296 + 1,632 = 3,928. 564 responses are blank. Neither is in a visible chunk; the Prose guard (line 782) checks only the 28.
- **Proposed fix:** Add to the end of the chunks:

  R:
  ```r
  items |> distinct(case_id, instrument) |> count(instrument)   # patients per instrument
  sum(is.na(items$response))                                    # rows with no answer
  ```
  Python:
  ```python
  print(items.drop_duplicates("case_id")["instrument"].value_counts())   # patients per instrument
  print(items["response"].isna().sum())                                  # rows with no answer
  ```
  They print 68 HOOS JR and 82 KOOS JR, then 564. Prose: "A KOOS JR patient now has 7 items × 4 visits = 28 rows, and a HOOS JR patient 6 items × 4 visits = 24. With 82 KOOS JR and 68 HOOS JR patients that makes 82 × 28 + 68 × 24 = 3,928 rows. A missed visit still has its rows, with the response blank (564 rows here), so "expected but not answered" stays visible."
- **Changes code:** yes

### 01-5 · The raw values the text describes are never printed, and the examples are not in the workbook · B
- **Where:** `en/foundations/01-tidy-data.qmd:240` (🔀 box, Step 1), `:504` (🔀 box, Step 5), `:744` to `:745` (section `#what-a-failing-check-looks-like`)
- **Text:** "Read as text, R gives the Excel serial number (`42010` means 6 Jan 2015). pandas gives `2015-01-06 00:00:00`." and "R can't read dates like `"13.01.15"` month-first … Others, like `"04.03.24"`, parse "successfully" as 3 April instead of 4 March"
- **Problem:** The page never prints a single raw cell, so the R/Python difference the box describes is not visible in any output. A reader who opens the sheet to look for the examples will not find them: `42010`, 6 Jan 2015, `13.01.15` and `04.03.24` do not occur in the `DOS` column.
- **Where it really comes from:** Illustrative values. The first six `dos` cells really are `"42026" "08.02.15" "14.05.15" "42236" "23.8.2015" "16.10.2015"` in R and `'2015-01-22 00:00:00', '08.02.15', '14.05.15', '2015-08-20 00:00:00', '23.8.2015', '16.10.2015'` in pandas.
- **Proposed fix:** Add one line to the end of the Step 1 chunks:

  R: `head(raw$dos)   # the first six surgery dates, exactly as read`
  Python: `print(raw["dos"].head(6).tolist())   # the first six surgery dates, exactly as read`

  Then use the printed values in the prose. Line 240: "Look at the first date in the two outputs: R gives the Excel serial number `42026` (22 Jan 2015), pandas gives `2015-01-22 00:00:00`." Line 504: replace `2015-01-06 00:00:00` with `2015-01-22 00:00:00`. Lines 744 to 745: replace `"13.01.15"` with `"14.05.15"` (there is no 14th month) and `"04.03.24"` … "3 April instead of 4 March" with `"08.02.15"` … "2 August instead of 8 February". The code comments at lines 381 to 382 and 438 to 439 can keep their generic examples.
- **Changes code:** yes (one line per language; the rest is prose)

### 01-6 · Exercise 1's answer points at spellings the output shows differently · B
- **Where:** `en/foundations/01-tidy-data.qmd:791` and `:815`, section `#exercises`, exercise 1
- **Text:** "every raw spelling should map to one class from 1 to 4" and "`2`, `II` and `ASA 2` all become 2, and the missing codes stay missing."
- **Problem:** The output has no row with a missing code: `step3` already turned the codes into blanks, so the reader sees one row `<NA>  NA  3` (R) or `NaN  NaN  3` (Python) and must work out that this is what "the missing codes stay missing" means. The question says "1 to 4" but the output has classes 1 to 3 only.
- **Where it really comes from:** Output rows `2  2  43`, `ASA 2  2  4`, `II  2  14` and `<NA>  NA  3`.
- **Proposed fix:** Prose only. "`2`, `II` and `ASA 2` all become 2 (43 + 4 + 14 = 61 cases). The last row is the 3 cases with no ASA class: step 3 had already turned their missing codes into blanks, and they stay missing. No one in this sheet has ASA class 4."
- **Changes code:** no

### 01-7 · The spot check prints different patients in R and Python, with no explanation · C
- **Where:** `en/foundations/01-tidy-data.qmd:679` to `:694`, section `#integrity`, check 5
- **Text:** "Pick a few random rows and compare them, by eye, with the workbook."
- **Problem:** R shows cases C0064, C0332 and C0004; Python shows C0353, C0451 and C0557. Everywhere else on the page the two tabs agree, so a beginner will think one of them is wrong.
- **Where it really comes from:** `set.seed(1)` and `random_state=1` fix each language's own draw, but R and Python use different random number generators.
- **Proposed fix:** Prose only, after the tabset: "R and Python draw different rows, because each has its own random number generator. That's fine: any three rows will do. The seed (`set.seed(1)`, `random_state=1`) only makes each language draw the same three rows every time you run it."
- **Changes code:** no

### 01-8 · Step 5's output is never read, and whole numbers print as `2.0` in Python · C
- **Where:** `en/foundations/01-tidy-data.qmd:422` and `:472`, section `#step-5-give-every-column-its-real-type` (the same effect at `:557` and `:811`)
- **Text:** (no prose follows the `glimpse(tidy)` / `tidy.info()` output)
- **Problem:** The longest output on the page gets no explanation. The two tabs also look different: R lists the first values of each column, Python lists counts of non-missing values. In Python, `asa`, `los_days` and the survey `response` are `float64` and later print as `2.0` and `3.0`, while R shows `2` and `3`.
- **Where it really comes from:** pandas stores a whole-number column that has blanks as decimals, because its plain integer type cannot hold a missing value.
- **Proposed fix:** Prose only, after the tabset: "Check the output against what you expect: 120 rows and 18 columns, dates are dates, numbers are numbers. R shows the first few values of each column. Python shows how many values are not missing: `bmi` has 112, which is 120 minus the 8 missing BMIs from step 3." Add a bullet to the 🔀 box at line 503: "**Whole numbers with blanks.** pandas stores a whole-number column that has missing values as decimals, so ASA class 2 prints as `2.0`. The value is the same."
- **Changes code:** no

## 02-demographics.qmd

### 02-1 · 80 bilateral patients and 520 patients appear in no output · A
- **Where:** `en/foundations/02-demographics.qmd:68`, section `#setup`, ⚠️ box; used again at `:440`, section `#exercises`, exercise 3 solution
- **Text:** "80 patients had both sides done, so 600 procedures come from 520 patients." and "We included 600 primary arthroplasties (270 THA and 330 TKA) in 520 patients."
- **Problem:** The setup chunks load the data and print nothing. 600 shows up later in the table headers, but no visible code counts patients. The exercise then tells the reader to "check every number against your own table", and 520 is in no table.
- **Where it really comes from:** Hidden Prose guard, lines 362 to 363 (`n_distinct(cohort$patient_id) == 520`, `sum(table(cohort$patient_id) == 2) == 80`).
- **Proposed fix:** Add to the end of the setup chunks:

  R:
  ```r
  nrow(cohort)                                  # rows: one per procedure
  cohort |>
    count(patient_id, name = "procedures") |>   # how many procedures each patient had
    count(procedures, name = "patients")        # how many patients had 1, how many had 2
  ```
  Python:
  ```python
  print(len(cohort))                                    # rows: one per procedure
  per_patient = cohort["patient_id"].value_counts()     # how many procedures each patient had
  print(per_patient.value_counts())                     # how many patients had 1, how many had 2
  ```
  They print 600, then 440 patients with 1 procedure and 80 with 2. In the box: "440 patients had one procedure and 80 had both sides done: 440 + 80 = 520 patients, and 440 + 2 × 80 = 600 procedures." In the exercise 3 solution add: "The 520 patients come from the count at the top of the page."
- **Changes code:** yes

### 02-2 · R's age SMD of 0.1048 is not in any output · A
- **Where:** `en/foundations/02-demographics.qmd:261`, section `#smd`, 🔀 box
- **Text:** "Age comes out as 0.1048 in R and 0.1046 in Python."
- **Problem:** R's table shows the age SMD as `0.10`. The value 0.1048 exists only inside the gtsummary object. Python's 0.1046 can be traced (`age  -0.104586`), but the prose does not point to it.
- **Where it really comes from:** `smd_r$estimate` in the hidden agreement check at lines 250 to 253. Confirmed: `smd::smd(cohort$age, cohort$procedure)` gives 0.1047628.
- **Proposed fix:** Either (a) show it, with a small tabset inside or just before the box:

  R: `smd::smd(cohort$age, cohort$procedure)   # the function gtsummary calls; its table rounds this to 0.10`
  Python: `print(round(abs(balance.smd_table.loc["age"].iloc[0]), 4))   # the age row from the output above`

  They print 0.1047628 and 0.1046; the pair needs its hidden agreement check with `tol = 0.005`, like the existing one. Or (b) prose only, quoting nothing that is not shown: "R's table rounds to two decimals, so you can't see the difference here: both show 0.10 for age, and Python prints −0.104586. The two packages agree to three decimals and differ after that."
- **Changes code:** (a) yes · (b) no

### 02-3 · The quartile box quotes THA numbers the reader has not seen yet · B
- **Where:** `en/foundations/02-demographics.qmd:138`, section `#which-summary`, 🔀 box
- **Text:** "the THA upper quartile is 2 days in R and 1.8 in Python."
- **Problem:** The only table shown so far is the one-group table, where R and Python agree (`1 (0–1)` and `1.0 [0.0,1.0]`). The THA figures are in the next section's table, and the box does not say so. A reader looking at the output above the box finds no difference.
- **Where it really comes from:** Section `#by-group`: R row `Length of stay, days | … | 1 (0–2)` under THA, Python row `Length of stay, days, median [Q1,Q3] | … | 1.0 [0.0,1.8]`.
- **Proposed fix:** Prose only. "In the table above the two agree (0 to 1 day). In the THA column of the [next table](#by-group) they don't: the upper quartile is 2 days in R (`1 (0–2)`) and 1.8 in Python (`1.0 [0.0,1.8]`)." Or move the box below the by-group table. Also delete the repeated sentence "With whole-number data the results can differ."
- **Changes code:** no

### 02-4 · The SMD sentence drops the minus signs before the box explains them, and the box's sign rule does not fit three of the seven rows · B
- **Where:** `en/foundations/02-demographics.qmd:256` and `:260`, section `#smd`
- **Text:** "Sex (SMD 0.31) and BMI (0.33) are the clear imbalances. Age (0.10) …" and "**Sign.** gtsummary subtracts TKA from THA; tableone subtracts THA from TKA."
- **Problem:** R prints BMI as `-0.33`, Python prints age as `-0.104586` and length of stay as `-0.070965`; the prose quotes them without the sign and does not say so until the box. The box then says the two packages have opposite signs, but sex, ASA class and smoking are positive in both outputs, which the rule does not explain.
- **Where it really comes from:** R column `Difference` (0.10, 0.31, −0.33, 0.12, 0.00, 0.15, 0.07); Python `smd_table` (−0.104586, 0.333603, −0.070965, 0.312714, 0.117597, 0.004631, 0.147952). For a variable entered as a category (sex, ASA class, smoking) both packages compute a distance, which has no direction and is never negative.
- **Proposed fix:** Prose only. Line 256: start with "Ignoring the sign for now (the box below explains it), sex (SMD 0.31) and BMI (0.33) are …". Line 260: "**Sign.** For number columns (age, BMI, diabetes, length of stay) gtsummary subtracts TKA from THA and tableone subtracts THA from TKA, so the signs are opposite. For categories (sex, ASA class, smoking) the SMD has no direction and is positive in both. Report the absolute value, or say which group was subtracted from which."
- **Changes code:** no

### 02-5 · The SMD's 95% CI column is never explained and exists in R only, yet the exercise answer relies on it · B
- **Where:** `en/foundations/02-demographics.qmd:426`, section `#exercises`, exercise 1 solution (the column first appears in the output of the chunk at `:212` to `:223`, section `#smd`)
- **Text:** "Smoking status (0.23) and length of stay (0.22) differ most between sites, and their 95% CIs exclude zero."
- **Problem:** R's table has a `95% CI` column that the main text never mentions. Python's `smd_table` prints no CI at all, so a Python reader cannot check "their 95% CIs exclude zero". The 0.22 for length of stay is `-0.224577` in Python, again quoted without its sign.
- **Where it really comes from:** R output rows `Smoking status | 0.23 | 0.07, 0.39` and `Length of stay, days | 0.22 | 0.06, 0.39`; Python rows `smoker 0.229484`, `los_days -0.224577`.
- **Proposed fix:** Prose only. After line 256 add: "R's table also gives a 95% CI for each SMD; tableone doesn't compute one." In the solution: "Smoking status (0.23) and length of stay (0.22; Python prints −0.22, see the box on signs) differ most between sites. In R's table their 95% CIs (0.07 to 0.39 and 0.06 to 0.39) exclude zero; tableone gives no CI."
- **Changes code:** no

### 02-6 · "Percentages are of the patients with a value" cannot be seen in R, and Python's Missing column is not explained · B
- **Where:** `en/foundations/02-demographics.qmd:315`, section `#missing`
- **Text:** "R adds a "Missing" row under each variable that has any. Python adds a "Missing" column. Either way, the percentages are of the patients with a value, and the reader can see how many were left out."
- **Problem:** R shows ASA class 1 at Site A as `6 (10%)`, which is the same whether the denominator is 60 or 58, so the claim cannot be checked there. The two outputs also look inconsistent: R says 5 and 3 BMIs are missing, Python says 8, and nothing says Python's column counts both sites together.
- **Where it really comes from:** R rows `bmi … Missing | 5 | 3`, `asa … Missing | 2 | 1`, `los_days … Missing | 1 | 2`; Python `Missing` column 8, 3, 3 and `asa 1 | 6 (10.3)`.
- **Proposed fix:** Prose only. "R adds a "Missing" row under each variable that has any, one count per site (BMI: 5 and 3). Python adds a "Missing" column for both sites together (BMI: 8 = 5 + 3). Either way, the percentages are of the patients with a value: at Site A, 6 of the 58 patients with an ASA class are in class 1, which is 10.3% (Python's `6 (10.3)`), not 6 of 60."
- **Changes code:** no

### 02-7 · The wrong guesses in the ⚠️ box are described, not shown · B
- **Where:** `en/foundations/02-demographics.qmd:121` to `:122`, section `#one-group`, ⚠️ box
- **Text:** "**ASA class** looks like a number, so it gets averaged ("mean ASA 2.4")." and "gtsummary treats it as a category and lists "0 days, 1 day, 2 days…"."
- **Problem:** The tables above the box were built with the types already set, so neither wrong result is on the page, and 2.4 is in no output. The first bullet also does not say which software averages: tableone does; gtsummary would list ASA class as a category (it has only four values).
- **Where it really comes from:** Not shown. Confirmed: tableone without `categorical=` prints `asa, mean (SD) | 2.4 (0.7)`; gtsummary without `type =` lists length of stay as 0, 1, 2, … 6 with a count each.
- **Proposed fix:** Cheapest, prose only: "**ASA class** looks like a number, so tableone averages it unless you list it under `categorical` (a "mean ASA class" describes no patient). It's a category." That removes the unshown 2.4. If the owner would rather show it, add a short tabset before the box: R `cohort |> select(los_days) |> tbl_summary()` (length of stay listed as categories), Python `print(TableOne(pd.read_csv("data/cohort.csv"), columns=["asa"]).tabulate(tablefmt="github"))` (ASA averaged to 2.4).
- **Changes code:** no (prose option) · yes (demonstration option)

### 02-8 · Diabetes p-value prints as `>0.999` in R and `1.000` in Python · C
- **Where:** `en/foundations/02-demographics.qmd:164` and `:180` (outputs), section `#by-group`
- **Text:** (output rows `Diabetes | … | >0.999` in R and `Diabetes, n (%) | … | 1.000 | Chi-squared` in Python; the prose at `:196` does not mention it)
- **Problem:** Same test, same data, visibly different p-values, and the site's own convention is "p > 0.999". A beginner pasting the Python table would report p = 1.000.
- **Where it really comes from:** The hidden check confirms both p-values are the same number; gtsummary's `label_style_pvalue(digits = 3)` caps the display at ">0.999", tableone rounds to three decimals.
- **Proposed fix:** Prose only, one sentence after line 196: "For diabetes R prints `>0.999` and Python `1.000`. It is the same p-value: tableone rounds it to three decimals. A p-value is never exactly 1, so write "p > 0.999" in the paper."
- **Changes code:** no

## 03-distributions.qmd

### 03-1 · "80 patients appear twice … usually in the same group" has no output behind it · A
- **Where:** `en/foundations/03-distributions.qmd:426`, section `#paired`
- **Text:** "In our cohort, 80 patients appear twice, once for each side, usually in the same group."
- **Problem:** No visible code on this page counts patients. "Usually in the same group" is not checked anywhere, and "group" is not defined.
- **Where it really comes from:** The 80 is in the hidden Prose guard, line 542. "Usually in the same group" is not computed anywhere. From the data: all 80 had the same procedure on both sides and at the same site.
- **Proposed fix:** Add a tabset after the paragraph's first sentence.

  R:
  ```r
  cohort |>
    count(patient_id, name = "procedures") |>   # how many procedures each patient had
    count(procedures, name = "patients")        # how many patients had 1, how many had 2
  ```
  Python:
  ```python
  per_patient = cohort["patient_id"].value_counts()   # how many procedures each patient had
  print(per_patient.value_counts())                   # how many patients had 1, how many had 2
  ```
  Both print 440 patients with 1 procedure and 80 with 2. Prose: "In our cohort, 80 patients appear twice, once for each side. A bilateral patient's two procedures usually fall in the same comparison group (the same procedure, the same site)." That keeps "usually" as a general statement. If 02-1 is applied, a prose-only version is enough: "(counted on [page 2](02-demographics.qmd#setup))".
- **Changes code:** yes (no, if it links to page 2 after 02-1)

### 03-2 · The three skewness values are printed and never read · B
- **Where:** `en/foundations/03-distributions.qmd:119` to `:144`, section `#look`
- **Text:** "A number for lopsidedness is the **skewness**: 0 for a symmetric shape, positive for a tail to the right, negative for a tail to the left."
- **Problem:** The output gives −0.05, 1.61 and −0.73, and the next thing on the page is a box about package formulas. The prose never ties the numbers to the three shapes, and gives no idea how far from 0 counts as skewed. Later pages and exercise 1 ("skewness about 0.1") lean on this.
- **Where it really comes from:** Output `age -0.05351075   los 1.60890277   prom_1yr -0.72708937`.
- **Proposed fix:** Prose only, after the tabset: "Age: −0.05, practically symmetric. Length of stay: 1.61, a long tail to the right. 1-year PROM: −0.73, a tail to the left. The numbers say what the histograms showed." Optionally add a rough guide (the owner's call): "As a rule of thumb, between −0.5 and 0.5 is close to symmetric, and beyond −1 or 1 is strongly skewed."
- **Changes code:** no

### 03-3 · R's summary shows the upper CI limit as 2.65; the prose says 2.6 · B
- **Where:** `en/foundations/03-distributions.qmd:511` and `:513` (R output of line 482), section `#effect-sizes`
- **Text:** "(mean difference 1.8 kg/m², 95% CI 0.9 to 2.6; p < 0.001)"
- **Problem:** The R tibble prints `ci_high 2.65`, which a reader rounds to 2.7. The true value is 2.647, so 2.6 is right, but an R reader has to find that in the `t.test` printout above, where the interval is printed with the opposite sign (`-2.647347 -0.924101`). The p-value is also printed three ways (`5.341e-05`, `0.0000534`, `0.000053`) and the prose gives a fourth (`p < 0.001`).
- **Where it really comes from:** Python output `ci_high 2.647347`; R `t.test` line `-2.647347 -0.924101`; R tibble rounds to three significant figures.
- **Proposed fix:** Prose only, one sentence before the blockquote: "Rounded to one decimal: the difference is 1.786, so 1.8; the CI runs from 0.924 to 2.647, so 0.9 to 2.6 (R's small table shows 2.65 because it prints three significant figures); and p = 0.00005, which we write as p < 0.001."- **Changes code:** no

### 03-4 · "About a third of a standard deviation" comes from page 2 · B
- **Where:** `en/foundations/03-distributions.qmd:271`, section `#within-groups`
- **Text:** "BMI differs by only about a third of a standard deviation between THA and TKA patients, so pooling barely matters."
- **Problem:** Nothing on this page shows the BMI difference or its SD at this point. The figure is the SMD of 0.33 from page 2, which is not cited.
- **Where it really comes from:** Page 2, section `#smd` (BMI SMD −0.33 in R, 0.333603 in Python). Not in this page's Prose guard.
- **Proposed fix:** Prose only: "BMI differs by only about a third of a standard deviation between THA and TKA patients (the SMD of 0.33 in [Table 1](02-demographics.qmd#smd)), so pooling barely matters."
- **Changes code:** no

### 03-5 · "The histogram of the pooled values has two humps" but no histogram is drawn · B
- **Where:** `en/foundations/03-distributions.qmd:269`, section `#within-groups`
- **Text:** "Pooled, p < 0.001: the histogram of the pooled values has two humps, which is not what a normal distribution looks like."
- **Problem:** The chunk prints two p-values and no plot, on a page whose message is "plot before you test". "4 standard deviations apart" (line 232) is also left for the reader to work out from the code.
- **Where it really comes from:** Not shown. The means are 40 and 60 with SD 5: (60 − 40) / 5 = 4.
- **Proposed fix:** Prose only: line 232 "… each exactly normal, with means of 40 and 60 and an SD of 5, so 4 standard deviations apart." Line 269: "… a histogram of the pooled values would have two humps, one around 40 and one around 60, which is not …". Or draw it: R `ggplot(tibble(value = c(group_a, group_b)), aes(value)) + geom_histogram(bins = 30)`, Python `plt.hist(np.concatenate([group_a, group_b]), bins=30)` then `plt.show()`.
- **Changes code:** no (prose option) · yes (plot option)

### 03-6 · The satisfaction counts are printed and never mentioned; 98 blanks are unexplained · B
- **Where:** `en/foundations/03-distributions.qmd:394` to `:416`, section `#ordinal`
- **Text:** "Report ordinal data as counts and percentages, or as a median (IQR), and compare groups with rank-based tests."
- **Problem:** The output (15, 23, 52, 162, 250 and `NA 98`) is not referred to at all. A beginner is not told what the `NA` row is, and Python labels the scores `1.0` to `5.0` where R shows `1` to `5`.
- **Where it really comes from:** Output of `count(cohort, satisfaction_1yr)`; the hidden check names the two values `very_satisfied` and `no_answer`.
- **Proposed fix:** Prose only, after the tabset: "250 patients chose 5 ("very satisfied") and 15 chose 1. The last row (`NA` in R, `NaN` in Python) is the 98 patients with no answer; say how many are missing when you report the scale. Python prints the scores as `1.0` to `5.0` because the column has blanks."
- **Changes code:** no

### 03-7 · "Nearly half" and "17% of patients" are printed as proportions, with the denominator unstated · B
- **Where:** `en/foundations/03-distributions.qmd:382` and `:384`, section `#transform`
- **Text:** "nearly half the stays are 0 days" and "17% of patients score the maximum at 1 year"
- **Problem:** The output shows `share_zero 0.485` and `ceiling_1yr 0.1696`; the prose turns them into "nearly half" and "17%" without naming the output lines. The 17% is of the patients who have a 1-year score (the code drops the blanks at the top of the page), which the sentence does not say.
- **Where it really comes from:** Output `skew_raw 1.6089028  skew_log 0.5940202  share_zero 0.4850000  ceiling_1yr 0.1696035`.
- **Proposed fix:** Prose only: "… nearly half the stays are 0 days (`share_zero`: 0.485, or 48.5%) …" and "17% of the patients with a 1-year score reach the maximum (`ceiling_1yr`: 0.17) …".
- **Changes code:** no

### 03-8 · Numbers like `9.267769e-11` and `5.341e-05` are never explained · C
- **Where:** `en/foundations/03-distributions.qmd:269` (output of lines 242 and 253), section `#within-groups`; again at `:478`, section `#effect-sizes`
- **Text:** "Each group alone passes easily (p ≈ 1). Pooled, p < 0.001"
- **Problem:** This is the first page where the software prints a p-value in e-notation, and no page in `getting-started/` or `foundations/` explains it. A beginner can read `9.267769e-11` as "about 9.27". Python's `0.999999999999995` against R's `1` for the single group is also left without comment.
- **Where it really comes from:** Outputs `[1] 9.267769e-11` (R) and `9.26776946181564e-11` (Python).
- **Proposed fix:** Prose only, after the tabset at line 255: "`9.267769e-11` is how software writes very small numbers: 9.27 × 10⁻¹¹, a decimal point followed by ten zeros and then 927. Whenever you see `e-` followed by a number of 4 or more, the p-value is below 0.001. For one group alone R rounds the p-value to 1 and Python prints 0.999999999999995."
- **Changes code:** no

### 03-9 · `W`, `t` and `df` are printed and never explained · C
- **Where:** `en/foundations/03-distributions.qmd:173` and `:193` (Shapiro-Wilk), section `#shapiro`; `:478` (Welch), section `#effect-sizes`
- **Text:** "p = 0.001: "not normal"." and "Every test on this site reports three things."
- **Problem:** The output shows `W = 0.99131` (in Python `statistic=np.float64(0.9913…)`) and later `t = -4.0705, df = 580.09`, and the prose reads only the p-value. A beginner cannot tell whether these matter. In Python the reader also has to find the p-value inside `ShapiroResult(statistic=…, pvalue=np.float64(0.00136…))`.
- **Where it really comes from:** Output lines `W = 0.99131, p-value = 0.001361` and `t = -4.0705, df = 580.09, p-value = 5.341e-05`.
- **Proposed fix:** Prose only. After line 183: "The other number, W (`statistic` in Python), is the test statistic: 1 would be a perfect fit to the normal curve. You don't report it; read the p-value (`p-value` in R, `pvalue` in Python)." After the tabset at line 497: "R's printout also shows t and df, the test statistic and its degrees of freedom. [Page 6](../catalog/06-two-unpaired-groups.qmd#unpaired-t) explains them; here we need only the difference, its CI and p."
- **Changes code:** no

## Pages with nothing to report

None. All three pages have findings.

## Not checked

- **Figures.** Statements read off the histograms and QQ plots on page 3 ("piles up at 0 and 1 days", "points curving up at the right end", "the QQ plot is a near-perfect straight line") were not checked against the image files; they are consistent with the printed skewness and counts.
- **Claims about the data generator** on page 2 ("sex was drawn completely independently of procedure", line 202; "site was assigned completely at random", line 426). No page output can show these. I confirmed them in `data-raw/R/gen_cohort.R` (lines 32 to 34: sex, procedure and site are each sampled on their own). Not filed as findings; a link to the generator would let a reader check.
- **Default behavior quoted on page 1** ("If you let the software guess types, it silently turns `32.1 kg/m2` into a missing value", line 168; "Site A rows simply have `mua` missing", line 233). Not demonstrated on the page. I confirmed the second (Site A has no `mua` values); I did not test the first. Note that `32.1 kg/m2` itself is not a value in the workbook (real ones: `33.5 kg/m2`, `29.8 kg/m2`).
- **German and French pages** were not read; fixes marked "Changes code: yes" must be copied into them.
