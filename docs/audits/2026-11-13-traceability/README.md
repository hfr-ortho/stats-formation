# Audit: can a reader trace every result on the page?

Date: 13.11.2026. Scope: the English pages. Eight review agents each read a group of pages against the same brief ([brief.md](brief.md)) and proposed a fix for every finding. Nothing on the site was changed by the audit.

## The rule

Any time results are presented, the page either calculates them for the reader or ties them directly to test output that shows them. A little more explanation, and clearer explanation, is better than leaving people to guess.

## Severity

| Level | Meaning |
|---|---|
| ERROR | The prose contradicts the output or the data. |
| A | A quoted result appears in no visible output and no derivation is given. Usually it is computed only in a hidden chunk or the Prose guard. |
| B | Traceable only with an unexplained step: another name or scale in the output, unstated rounding or arithmetic, or shown in one language's tab only. |
| C | An explanation a beginner would have to guess at. |

## How to use this list

Work fix by fix. Each finding has an ID (page number, then a counter). The full text of a finding, with its location, the quoted sentence and a concrete proposed fix, is in the file linked from the index below. When a fix is published, change its Status in the index from `open` to `done`.

A fix marked "code: yes" changes R or Python code. It must be copied identically into the German and French pages, and all three pages re-run. A fix marked "code: no" changes prose only, which still has to be translated.

The proposed fixes are proposals. The agents ran most proposed code lines against `data/`, but none was rendered inside a page, so the hidden agreement checks and the Prose guard have not been run against them.

## Counts

| Page | ERROR | A | B | C | Total |
|---|---|---|---|---|---|
| 1 · Tidy data |  | 2 | 4 | 2 | 8 |
| 2 · Demographics (Table 1) |  | 2 | 5 | 1 | 8 |
| 3 · Distributions |  | 1 | 6 | 2 | 9 |
| 4 · Describe one group | 1 | 5 | 8 | 2 | 16 |
| 5 · One group vs a hypothetical value |  | 5 | 6 | 3 | 14 |
| 6 · Two unpaired groups |  | 5 | 11 | 4 | 20 |
| 7 · Two paired groups | 1 | 9 | 5 | 4 | 19 |
| 8 · Three or more unmatched groups |  | 4 | 9 | 3 | 16 |
| 9 · Three or more matched groups | 1 | 5 | 5 | 2 | 13 |
| 10 · Association |  | 3 | 6 | 1 | 10 |
| 11 · Predict from one variable |  | 7 | 11 | 2 | 20 |
| 12 · Predict from several variables |  | 3 | 9 | 1 | 13 |
| 13 · Kaplan-Meier |  | 1 | 10 | 2 | 13 |
| 14 · Cox regression |  | 3 | 5 | 3 | 11 |
| 15 · Post-hoc tests |  | 7 | 6 | 1 | 14 |
| 16 · Mixed models |  | 7 | 4 | 2 | 13 |
| 17 · Agreement | 1 | 1 | 4 | 1 | 7 |
| 18 · Example report |  | 2 | 13 | 4 | 19 |
| How to use this site |  |  | 1 | 2 | 3 |
| Install & set up |  |  |  | 3 | 3 |
| Working with real HFR data |  |  |  | 4 | 4 |
| Choose a test |  |  |  | 1 | 1 |
| **All pages** | **4** | **72** | **128** | **50** | **254** |

No findings: the home page and "Tests A–Z".

## The four errors

All four were rechecked against the page text and the data after the audit.

| ID | What is wrong |
|---|---|
| 04-1 | "9.4 / √600 ≈ 0.39" gives 0.38 as typed; 0.39 comes from the unrounded SD (9.44). |
| 07-1 | "only 22 revisions inform it": only 18 do (14 with implant C, 4 with A), and 14 / 4 is the hazard ratio of 3.5. |
| 09-1 | Counts of `case_id` are called "patients" throughout page 9, including two Results sentences. The 328 complete cases are 299 patients; the 574 pre-op scores are 497 patients. |
| 17-1 | "limits of ±3.7°" where the output gives −2.74° to 3.74°. |

## Themes that one fix can settle on several pages

| Theme | Findings | One fix |
|---|---|---|
| "The 80 patients who had both sides operated on" is repeated on many pages and counted on none | 02-1, 03-1, 04-6, 05-5, 06-5, 07-10, 08-13, 09-13, 10-3, 11-7, 12-3, 13-1, 14-2, 15-7 | Show the count once in visible code on page 2, and make the repeated sentence link to it. |
| R's scientific notation (`1.28e-14`) is printed and never explained | 03-8, 05-6, 06-7, 07-11, 08-9, 08-14, 14-10, 18-9 | Explain it once on "How to use this site" (and in a glossary), and link from each "Read the output". |
| "Read the output" follows R's labels; Python names the same values differently or omits them | 05-7, 06-8, 06-12, 08-10, 08-11, 09-10, 12-12, 13-3, 13-12, 14-6, 15-11 | Give both names in each bullet: "`W` (R) or `U_val` (Python)". |
| A quoted value is printed in one language's tab only | 06-10, 07-12, 07-13, 07-14, 11-8, 11-13, 11-14, 13-4, 13-5, 15-12, 18-10, 18-11 | Print it in the other tab, or say which tab shows it. |
| Percentages and totals quoted from counts, with no visible division or sum | 04-8, 04-13, 05-9, 06-3, 08-5, 08-6, 08-7, 09-8, 10-4, 10-5, 10-9, 11-10, 11-16, 12-8, 14-8, 16-8, 17-5, 18-3, 18-4, 18-5, 18-6 | Add the percentage column to the table already printed. |
| The prose rounds differently from the output, or quotes more digits than R prints | 03-3, 06-13, 11-9, 12-4, 13-2, 13-11, 14-4, 17-3, 18-7, 18-8 | Print the value at the quoted precision, or say how it was rounded. |
| The output gives proportions, the prose percentages | 03-7, 06-9, 12-5, 13-11, 18-12 | One sentence: "multiply by 100". |
| A number has to be read off a plot by eye | 06-15, 11-3, 16-7 | Print it. |
| Printed output that no bullet explains | 03-9, 04-16, 05-14, 06-11, 07-16, 08-15, 09-11, 11-19, 14-9, 15-14 | A bullet for each column that matters, and one line saying which columns to ignore. |
| Terms used without an explanation (glossary candidates) | 06-20 (Wald), 14-7 (SHR), 18-17 (reverse Kaplan-Meier, Aalen-Johansen), 18-19 (small, medium, large), gs-use-2 (Hodges-Lehmann), gs-use-3 (IQR), gs-real-4 (BASEC, REDCap), choose-1 (paired, matched) | A glossary entry and a link at first use. |

## Findings that need facts only Doc has

- gs-real-1 and gs-real-2: where an export of real data may be stored, and what "the secure environment" is.
- gs-setup-1: the wording of the new checks, against a fresh install.

## Index of all findings

| ID | Level | Code | Finding | Details | Status |
|---|---|---|---|---|---|
| 01-1 | A | yes | "The notes miss some revisions" is never counted | [foundations.md](foundations.md) | open |
| 01-2 | A | yes | The make-up of the 126 rows is stated, not shown | [foundations.md](foundations.md) | open |
| 01-3 | B | yes | "All zeros" but R's output hides the fifth check | [foundations.md](foundations.md) | open |
| 01-4 | B | yes | 3,928 survey rows are never explained, and the blank answers are never shown | [foundations.md](foundations.md) | open |
| 01-5 | B | yes | The raw values the text describes are never printed, and the examples are not in the workbook | [foundations.md](foundations.md) | open |
| 01-6 | B | no | Exercise 1's answer points at spellings the output shows differently | [foundations.md](foundations.md) | open |
| 01-7 | C | no | The spot check prints different patients in R and Python, with no explanation | [foundations.md](foundations.md) | open |
| 01-8 | C | no | Step 5's output is never read, and whole numbers print as `2.0` in Python | [foundations.md](foundations.md) | open |
| 02-1 | A | yes | 80 bilateral patients and 520 patients appear in no output | [foundations.md](foundations.md) | done |
| 02-2 | A | yes | R's age SMD of 0.1048 is not in any output | [foundations.md](foundations.md) | open |
| 02-3 | B | no | The quartile box quotes THA numbers the reader has not seen yet | [foundations.md](foundations.md) | open |
| 02-4 | B | no | The SMD sentence drops the minus signs before the box explains them, and the box's sign rule does not fit three of the seven rows | [foundations.md](foundations.md) | open |
| 02-5 | B | no | The SMD's 95% CI column is never explained and exists in R only, yet the exercise answer relies on it | [foundations.md](foundations.md) | open |
| 02-6 | B | no | "Percentages are of the patients with a value" cannot be seen in R, and Python's Missing column is not explained | [foundations.md](foundations.md) | open |
| 02-7 | B | no | The wrong guesses in the ⚠️ box are described, not shown | [foundations.md](foundations.md) | open |
| 02-8 | C | no | Diabetes p-value prints as `>0.999` in R and `1.000` in Python | [foundations.md](foundations.md) | open |
| 03-1 | A | yes | "80 patients appear twice … usually in the same group" has no output behind it | [foundations.md](foundations.md) | done |
| 03-2 | B | no | The three skewness values are printed and never read | [foundations.md](foundations.md) | open |
| 03-3 | B | ? | R's summary shows the upper CI limit as 2.65; the prose says 2.6 | [foundations.md](foundations.md) | open |
| 03-4 | B | no | "About a third of a standard deviation" comes from page 2 | [foundations.md](foundations.md) | open |
| 03-5 | B | no | "The histogram of the pooled values has two humps" but no histogram is drawn | [foundations.md](foundations.md) | open |
| 03-6 | B | no | The satisfaction counts are printed and never mentioned; 98 blanks are unexplained | [foundations.md](foundations.md) | open |
| 03-7 | B | no | "Nearly half" and "17% of patients" are printed as proportions, with the denominator unstated | [foundations.md](foundations.md) | open |
| 03-8 | C | no | Numbers like `9.267769e-11` and `5.341e-05` are never explained | [foundations.md](foundations.md) | open |
| 03-9 | C | no | `W`, `t` and `df` are printed and never explained | [foundations.md](foundations.md) | open |
| 04-1 | ERROR | no | The standard error arithmetic as written gives 0.38, not 0.39 | [catalog-04-05.md](catalog-04-05.md) | done |
| 04-2 | A | yes | "39 of the 194 scores were 48" is computed only in the Prose guard | [catalog-04-05.md](catalog-04-05.md) | done |
| 04-3 | A | yes | "13 scored exactly 42" and "62 of the 194 (32%)" are computed only in the Prose guard | [catalog-04-05.md](catalog-04-05.md) | done |
| 04-4 | A | yes | Exercise 2: the skew, "4 to 6 days" and "0.9 ± 1.1" are shown nowhere | [catalog-04-05.md](catalog-04-05.md) | done |
| 04-5 | A | no | "Every patient was followed for at least 30 days or until death" is checked only in the Prose guard | [catalog-04-05.md](catalog-04-05.md) | done |
| 04-6 | A | yes | "the 80 patients who had both sides operated on" is never counted | [catalog-04-05.md](catalog-04-05.md) | done |
| 04-7 | B | yes | "263 patients at risk" appears only in R's output, and lifelines counts 258 | [catalog-04-05.md](catalog-04-05.md) | done |
| 04-8 | B | no | "13.5% were revised" is not derived, and the summary output is never read | [catalog-04-05.md](catalog-04-05.md) | done |
| 04-9 | B | no | "roughly 47 to 84 years" needs arithmetic the page does not show | [catalog-04-05.md](catalog-04-05.md) | done |
| 04-10 | B | no | The SEM of 0.39 in the Watch-out box is explained only inside a collapsed box | [catalog-04-05.md](catalog-04-05.md) | done |
| 04-11 | B | no | The denominator 1,200 is never printed | [catalog-04-05.md](catalog-04-05.md) | done |
| 04-12 | B | no | R prints a confidence level of 0.9629 under a bullet that says "95% CI" | [catalog-04-05.md](catalog-04-05.md) | done |
| 04-13 | B | yes | Exercise 3: 21.4% is not computed in the Solution | [catalog-04-05.md](catalog-04-05.md) | done |
| 04-14 | B | no | "by 10 years only a handful remain": the table says 21 | [catalog-04-05.md](catalog-04-05.md) | done |
| 04-15 | C | no | The tables under the R and Python plots differ (332 vs 331, 84 vs 83) with no explanation | [catalog-04-05.md](catalog-04-05.md) | done |
| 04-16 | C | no | Printed survival output that is never explained: `n.event`, `std.err`, "519 right-censored" | [catalog-04-05.md](catalog-04-05.md) | done |
| 05-1 | A | yes | Results quote "SD 16.4", which no visible code computes | [catalog-04-05.md](catalog-04-05.md) | done |
| 05-2 | A | yes | Results quote the median 85.8 and IQR 74.7 to 93.9, which no visible code computes | [catalog-04-05.md](catalog-04-05.md) | done |
| 05-3 | A | yes | n = 260, V = 22698.5 and "more patients scored above 80 than below" have no visible source | [catalog-04-05.md](catalog-04-05.md) | done |
| 05-4 | A | yes | The Wilson interval "84.1% to 88.0%" is computed only in the Prose guard | [catalog-04-05.md](catalog-04-05.md) | done |
| 05-5 | A | yes | "the 80 patients who had both sides operated on" is never counted | [catalog-04-05.md](catalog-04-05.md) | done |
| 05-6 | B | no | "p < 0.001" is never tied to the e-notation the output prints | [catalog-04-05.md](catalog-04-05.md) | done |
| 05-7 | B | no | "Read the output" uses R's labels only; Python names the same values differently, or omits them | [catalog-04-05.md](catalog-04-05.md) | done |
| 05-8 | B | no | R prints a 95% CI for the rank-biserial r (0.21 to 0.46) that the page never mentions | [catalog-04-05.md](catalog-04-05.md) | done |
| 05-9 | B | yes | Exercise 3: the percentages 53.5%, 38.3% and 8.2% are not computed in the Solution | [catalog-04-05.md](catalog-04-05.md) | done |
| 05-10 | B | yes | Exercise 1: the R Solution does not print the difference of −0.5 | [catalog-04-05.md](catalog-04-05.md) | done |
| 05-11 | B | no | "about 20 minutes" is 4 × 5.5 = 22, and the page does not show the sum | [catalog-04-05.md](catalog-04-05.md) | done |
| 05-12 | C | no | The rank-biserial r is defined by its end points only; the printed rank sums give it in one line | [catalog-04-05.md](catalog-04-05.md) | done |
| 05-13 | C | no | The chi-square statistic is described, not calculated, although the table above gives every term | [catalog-04-05.md](catalog-04-05.md) | done |
| 05-14 | C | no | pingouin's `CLES  NaN` and `alternative` columns are shown and never explained | [catalog-04-05.md](catalog-04-05.md) | done |
| 06-1 | A | yes | Chi-square p without Yates' correction (0.754) is computed only in the Prose guard | [catalog-06-07.md](catalog-06-07.md) | done |
| 06-2 | A | yes | Exercise 2: "13% with a boot and 17% with a cast scored 24" is not printed anywhere | [catalog-06-07.md](catalog-06-07.md) | done |
| 06-3 | A | yes | Exercise 3: the two percentages and the risk difference are not printed | [catalog-06-07.md](catalog-06-07.md) | done |
| 06-4 | A | yes | "Leaving out any one patient still gives −1" is computed only in the Prose guard | [catalog-06-07.md](catalog-06-07.md) | done |
| 06-5 | A | no | "The 80 patients who had both sides operated on" is shown nowhere, and is not this page's number | [catalog-06-07.md](catalog-06-07.md) | done |
| 06-6 | B | no | Missed-visit counts need a subtraction from numbers the output never shows | [catalog-06-07.md](catalog-06-07.md) | done |
| 06-7 | B | no | p-values are printed in e-notation and the bullets never say how to read them | [catalog-06-07.md](catalog-06-07.md) | done |
| 06-8 | B | no | The mean difference (3.6) is printed only in Python; the bullets use R's labels only | [catalog-06-07.md](catalog-06-07.md) | done |
| 06-9 | B | no | Risk difference −0.8 points is not printed; the CI is printed as proportions | [catalog-06-07.md](catalog-06-07.md) | done |
| 06-10 | B | no | The CI for the rank-biserial r is printed in R only, and nothing says so | [catalog-06-07.md](catalog-06-07.md) | done |
| 06-11 | B | no | Python's `CLES = 0.319411` is printed and never explained | [catalog-06-07.md](catalog-06-07.md) | done |
| 06-12 | B | no | Log-rank bullets describe columns that only R prints | [catalog-06-07.md](catalog-06-07.md) | done |
| 06-13 | B | yes | Exercise 1: R prints the boot arm's SD as 2.75, the Results sentence says 2.7 | [catalog-06-07.md](catalog-06-07.md) | done |
| 06-14 | B | no | The sample odds ratio 0.8311 is not printed, and the formula has no numbers | [catalog-06-07.md](catalog-06-07.md) | done |
| 06-15 | B | yes | "No patient at the floor (0) or the ceiling (24)" can only be read off the histogram | [catalog-06-07.md](catalog-06-07.md) | done |
| 06-16 | B | no | "The estimates agree to five decimals" cannot be checked from the output | [catalog-06-07.md](catalog-06-07.md) | done |
| 06-17 | C | yes | Python's row-percentage table comes out in a different order from R's | [catalog-06-07.md](catalog-06-07.md) | done |
| 06-18 | C | no | `conf.type = "log-log"` and the 5-year table get no explanation in this section | [catalog-06-07.md](catalog-06-07.md) | done |
| 06-19 | C | no | The quartile bullet sits under the wrong output and skips its reasoning | [catalog-06-07.md](catalog-06-07.md) | done |
| 06-20 | C | no | "Wald" is used in the Methods sentence and the Python code without explanation | [catalog-06-07.md](catalog-06-07.md) | done |
| 07-1 | ERROR | yes | "Only 22 revisions inform it": 18 do, and they explain the hazard ratio of exactly 3.5 | [catalog-06-07.md](catalog-06-07.md) | done |
| 07-2 | A | yes | Results sentence: the mean and SD of each view are printed nowhere | [catalog-06-07.md](catalog-06-07.md) | done |
| 07-3 | A | yes | "62 of the 80 hips (78%)" and "56 ... and 48" cam-positive hips are computed only in the Prose guard | [catalog-06-07.md](catalog-06-07.md) | done |
| 07-4 | A | yes | The unpaired p = 0.037 and the "11° spread" are computed only in the Prose guard | [catalog-06-07.md](catalog-06-07.md) | done |
| 07-5 | A | yes | Wilcoxon Results sentence: both IQRs are printed nowhere | [catalog-06-07.md](catalog-06-07.md) | done |
| 07-6 | A | yes | The unstratified hazard ratio 3.60 is computed only in the Prose guard | [catalog-06-07.md](catalog-06-07.md) | done |
| 07-7 | A | yes | Exercise 1: "reads high in hips with little torsion and low in hips with a lot" is shown nowhere | [catalog-06-07.md](catalog-06-07.md) | done |
| 07-8 | A | no | d~av~ "0.33 here" is computed only in the Prose guard | [catalog-06-07.md](catalog-06-07.md) | done |
| 07-9 | A | yes | "A hazard ratio of 3.4997 instead of 3.5" is computed only in the Prose guard | [catalog-06-07.md](catalog-06-07.md) | done |
| 07-10 | A | no | "The 80 patients who had both sides operated on" is shown nowhere, and no example on this page has 80 | [catalog-06-07.md](catalog-06-07.md) | done |
| 07-11 | B | no | p-values: e-notation unexplained, and R and Python print different things for the Wilcoxon test | [catalog-06-07.md](catalog-06-07.md) | done |
| 07-12 | B | no | The CI for d~z~ is printed in R only, and nothing says so | [catalog-06-07.md](catalog-06-07.md) | done |
| 07-13 | B | yes | Exercise 1: R cuts the Budin SD off the table, so "SD 7.6" is visible in Python only | [catalog-06-07.md](catalog-06-07.md) | done |
| 07-14 | B | no | Exercise 3: the Hodges-Lehmann estimate and its CI come from R only | [catalog-06-07.md](catalog-06-07.md) | done |
| 07-15 | B | no | "Of 505 patients seen at both visits" is a sum the output does not show | [catalog-06-07.md](catalog-06-07.md) | done |
| 07-16 | C | no | Python's `CLES = 0.964621` is printed, unexplained, and looks wrong | [catalog-06-07.md](catalog-06-07.md) | done |
| 07-17 | C | yes | The reason for choosing the Wilcoxon test (a ceiling at 1 year) is never shown, and the plot points the other way | [catalog-06-07.md](catalog-06-07.md) | done |
| 07-18 | C | no | The step from the binomial CI to the odds-ratio CI is unexplained | [catalog-06-07.md](catalog-06-07.md) | done |
| 07-19 | C | no | Cox output: three tests with different p-values "test the same thing", and half the table is unexplained | [catalog-06-07.md](catalog-06-07.md) | done |
| 08-1 | A | yes | Welch's ANOVA result appears from nowhere | [catalog-08-09.md](catalog-08-09.md) | done |
| 08-2 | A | yes | Bias-corrected Cramér's V "0.24 here" is never printed | [catalog-08-09.md](catalog-08-09.md) | done |
| 08-3 | A | yes | lifelines' default hazard ratio 0.81713 is never printed | [catalog-08-09.md](catalog-08-09.md) | done |
| 08-4 | A | no | "roughly a one-in-four chance" has no calculation | [catalog-08-09.md](catalog-08-09.md) | done |
| 08-5 | B | yes | "502 of the 600 procedures" and "missing for 98" need unstated sums | [catalog-08-09.md](catalog-08-09.md) | done |
| 08-6 | B | no | Row totals 129, 154 and 67 in the Results are not in the output | [catalog-08-09.md](catalog-08-09.md) | done |
| 08-7 | B | yes | Exercise 3: the percentages 4.7%, 3.9%, 4.5% and the totals are never computed | [catalog-08-09.md](catalog-08-09.md) | done |
| 08-8 | B | no | F = 23.9 is not tied to the Mean Sq column; Python's column names and `np2` are unexplained | [catalog-08-09.md](catalog-08-09.md) | done |
| 08-9 | B | no | ε² = 0.001 is printed by R as `1.35e-03` | [catalog-08-09.md](catalog-08-09.md) | done |
| 08-10 | B | yes | Cox overall test: Python prints neither df nor p, and "the second number" is ambiguous | [catalog-08-09.md](catalog-08-09.md) | done |
| 08-11 | B | no | Chi-square: Python prints three unlabeled numbers, and its percentage table flips the columns | [catalog-08-09.md](catalog-08-09.md) | done |
| 08-12 | B | no | "9,999 random tables" is a scipy default the code never shows | [catalog-08-09.md](catalog-08-09.md) | done |
| 08-13 | B | yes | "the 80 patients who had both sides operated on" is stated, never shown | [catalog-08-09.md](catalog-08-09.md) | done |
| 08-14 | C | no | R's `e` notation is used six times and never explained | [catalog-08-09.md](catalog-08-09.md) | done |
| 08-15 | C | no | Half of R's Cox printout is never mentioned | [catalog-08-09.md](catalog-08-09.md) | done |
| 08-16 | C | yes | Two Results sentences leave out the group figures the page asks for | [catalog-08-09.md](catalog-08-09.md) | done |
| 09-1 | ERROR | comments | The "patients" counted on this page are procedures | [catalog-08-09.md](catalog-08-09.md) | done |
| 09-2 | A | yes | 574 pre-op scores, and the 246 and 43% built on it, are never shown | [catalog-08-09.md](catalog-08-09.md) | done |
| 09-3 | A | yes | "28 of them sit at 57.0" is never shown | [catalog-08-09.md](catalog-08-09.md) | done |
| 09-4 | A | yes | "60 randomized patients" in the boot arm is never shown | [catalog-08-09.md](catalog-08-09.md) | done |
| 09-5 | A | yes | "6 patients score the maximum" is never shown | [catalog-08-09.md](catalog-08-09.md) | done |
| 09-6 | A | yes | "Most patients improved from each visit to the next" has no output behind it | [catalog-08-09.md](catalog-08-09.md) | done |
| 09-7 | B | no | "24.4 percentage points" does not follow from the printed percentages | [catalog-08-09.md](catalog-08-09.md) | done |
| 09-8 | B | yes | Solution 3: the percentages are not computed and the CIs print as an unlabeled matrix | [catalog-08-09.md](catalog-08-09.md) | done |
| 09-9 | B | no | Stratified Cox: the per-implant p-values are skipped, and "13.5" matches the wrong printed line | [catalog-08-09.md](catalog-08-09.md) | done |
| 09-10 | B | no | Python's row and column names are not matched to the bullets | [catalog-08-09.md](catalog-08-09.md) | done |
| 09-11 | C | no | One-sided CIs, Huynh-Feldt columns and "type III" vs "Type I" are printed but never explained | [catalog-08-09.md](catalog-08-09.md) | done |
| 09-12 | C | comments | The Wilson interval line has no comment | [catalog-08-09.md](catalog-08-09.md) | done |
| 09-13 | B | no | "the 80 patients who had both sides operated on" is stated, never shown | [catalog-08-09.md](catalog-08-09.md) | done |
| 10-1 | A | yes | Budin vs CT disagreement figures come only from the Prose guard | [catalog-10-12.md](catalog-10-12.md) | done |
| 10-2 | A | yes | Bias-corrected V = 0.18 is never printed | [catalog-10-12.md](catalog-10-12.md) | done |
| 10-3 | A | no | "the 80 patients who had both sides operated on" is asserted, never counted | [catalog-10-12.md](catalog-10-12.md) | done |
| 10-4 | B | yes | Exercise 3: the percentages and denominators are not in the Solution's output | [catalog-10-12.md](catalog-10-12.md) | done |
| 10-5 | B | yes | "404 procedures" has to be added up from the table | [catalog-10-12.md](catalog-10-12.md) | done |
| 10-6 | B | yes | Which cell has the smallest expected count is not shown | [catalog-10-12.md](catalog-10-12.md) | done |
| 10-7 | B | no | Pearson's C ceiling of 0.71 has no derivation | [catalog-10-12.md](catalog-10-12.md) | done |
| 10-8 | B | yes | Exercise 1: "3.7° higher on average" is not on this page | [catalog-10-12.md](catalog-10-12.md) | done |
| 10-9 | B | no | Row totals 36 and 18 are not printed | [catalog-10-12.md](catalog-10-12.md) | done |
| 10-10 | C | no | p-values: what the two languages print is only half tied to the text | [catalog-10-12.md](catalog-10-12.md) | done |
| 11-1 | A | yes | Logistic ⚠️ box: "97 hours on average" and "17.2% from the model" exist only in the Prose guard | [catalog-10-12.md](catalog-10-12.md) | done |
| 11-2 | A | yes | "An ordinary least-squares line gives 0.43" is never fitted on the page | [catalog-10-12.md](catalog-10-12.md) | done |
| 11-3 | A | yes | LOWESS "from about 70 to about 99" must be read off the plot | [catalog-10-12.md](catalog-10-12.md) | done |
| 11-4 | A | yes | "BMI here runs from 18.0 to 44.5" is never printed | [catalog-10-12.md](catalog-10-12.md) | done |
| 11-5 | A | no | "each knee appears up to four times" is not shown and not even guarded | [catalog-10-12.md](catalog-10-12.md) | done |
| 11-6 | A | yes | Code comment "pre-op visits (1-27 days before surgery)" quotes an unshown range | [catalog-10-12.md](catalog-10-12.md) | done |
| 11-7 | A | no | "the 80 patients who had both sides operated on" | [catalog-10-12.md](catalog-10-12.md) | done |
| 11-8 | B | yes | Half-gain CI "49 to 64 days" is printed in R only, and Python's own CI gives 48 to 64 | [catalog-10-12.md](catalog-10-12.md) | done |
| 11-9 | B | no | Cox CI "1.09 to 1.48" looks wrong against R's printed 1.095 and 1.485 | [catalog-10-12.md](catalog-10-12.md) | done |
| 11-10 | B | yes | "74 of 1,200" and "6.2%" need adding and dividing | [catalog-10-12.md](catalog-10-12.md) | done |
| 11-11 | B | no | "6.8 more minutes (95% CI 5.8 to 7.9)" per 5 kg/m²: the multiplication is not shown | [catalog-10-12.md](catalog-10-12.md) | done |
| 11-12 | B | yes | "5° steeper carries 3.37 times the hazard (95% CI 1.57 to 7.21)": the power is not shown | [catalog-10-12.md](catalog-10-12.md) | done |
| 11-13 | B | yes | Exercise 3: "about 37 days" is printed only in Python, the CIs only in R | [catalog-10-12.md](catalog-10-12.md) | done |
| 11-14 | B | yes | Exercise 1: p < 0.001 is not in the Python output | [catalog-10-12.md](catalog-10-12.md) | done |
| 11-15 | B | yes | Cox: counts and the overall test are not tied to where they are printed | [catalog-10-12.md](catalog-10-12.md) | done |
| 11-16 | B | no | "37 of them (15.0%)": the percentage is not printed | [catalog-10-12.md](catalog-10-12.md) | done |
| 11-17 | B | no | "63% of their eventual gain" after τ days has no derivation | [catalog-10-12.md](catalog-10-12.md) | done |
| 11-18 | B | no | "With 31 failures, this model can take about three terms": the rule is not stated here | [catalog-10-12.md](catalog-10-12.md) | done |
| 11-19 | C | no | Regression summaries: most of the printed output is never explained, and p is quoted in a form neither tab prints | [catalog-10-12.md](catalog-10-12.md) | done |
| 11-20 | C | no | Logistic: "Null and residual deviance (R) or LLR p-value (Python)" leaves the R reader without the link | [catalog-10-12.md](catalog-10-12.md) | done |
| 12-1 | A | yes | Logistic ⚠️ box: "15 of 350" and "all 6 patients whose graft failed in the first year" are never shown | [catalog-10-12.md](catalog-10-12.md) | done |
| 12-2 | A | no | lifelines' default result "0.82915" is computed only in the Prose guard | [catalog-10-12.md](catalog-10-12.md) | done |
| 12-3 | A | no | "the 80 patients who had both sides operated on" | [catalog-10-12.md](catalog-10-12.md) | done |
| 12-4 | B | no | Python prints p = 0.001 for both grafts; the text says p < 0.001 | [catalog-10-12.md](catalog-10-12.md) | done |
| 12-5 | B | yes | Python prints proportions where the text quotes percentages | [catalog-10-12.md](catalog-10-12.md) | done |
| 12-6 | B | yes | "a difference of 19 days (95% CI 11 to 28)": 19 is not printed, and the CI is in R only | [catalog-10-12.md](catalog-10-12.md) | done |
| 12-7 | B | yes | The "before adjustment" numbers (1.37 and 3.07) live on other pages | [catalog-10-12.md](catalog-10-12.md) | done |
| 12-8 | B | no | "173 of 350 reconstructions (49.4%)": total and percentage not printed | [catalog-10-12.md](catalog-10-12.md) | done |
| 12-9 | B | no | Exercise 3: "only 8 of the 74 deaths" and "already predicts the rate after 72 hours" rest on page 11 | [catalog-10-12.md](catalog-10-12.md) | done |
| 12-10 | B | no | Three of five odds-ratio CIs differ in Python; the 🔀 box gives only one | [catalog-10-12.md](catalog-10-12.md) | done |
| 12-11 | B | no | Model-comparison tables: the reported df and χ² are never tied to their columns | [catalog-10-12.md](catalog-10-12.md) | done |
| 12-12 | B | yes | Cox overall test: df and p are in R's output only | [catalog-10-12.md](catalog-10-12.md) | done |
| 12-13 | C | no | The spline is run before it is explained, inside a section about something else | [catalog-10-12.md](catalog-10-12.md) | done |
| 13-1 | A | no | "the 80 patients who had both sides operated on" is never counted | [survival.md](survival.md) | done |
| 13-2 | B | yes | Log-rank p-values and χ² quoted to more digits than R prints | [survival.md](survival.md) | done |
| 13-3 | B | no | Observed and Expected revisions appear in R's output only | [survival.md](survival.md) | done |
| 13-4 | B | yes | Cumulative incidence of death (24.0%, CI 19.3% to 29.0%) is printed in R only | [survival.md](survival.md) | done |
| 13-5 | B | no | Numbers at risk in the prose (332, 84) match R's risk table only | [survival.md](survival.md) | done |
| 13-6 | B | no | Gray's test "df = 2" is not in the printed table | [survival.md](survival.md) | done |
| 13-7 | B | no | Exercise 3 quotes a Gray's test its Solution never runs | [survival.md](survival.md) | done |
| 13-8 | B | no | "99 days" is not in any output | [survival.md](survival.md) | done |
| 13-9 | B | no | "2.7 percentage points" needs a subtraction the page does not show | [survival.md](survival.md) | done |
| 13-10 | B | no | Exercise 2: "100 procedures" and "about a fifth" are left to the reader | [survival.md](survival.md) | done |
| 13-11 | B | no | "5.9% at 2 years" against R's printed 0.0595 | [survival.md](survival.md) | done |
| 13-12 | C | no | Python prints rows of unlabeled numbers; the bullets use R's column names | [survival.md](survival.md) | done |
| 13-13 | C | no | Toy example: the "Year 2" bullet has no row in R's output | [survival.md](survival.md) | done |
| 14-1 | A | yes | The single hazard ratio for approach (1.37, CI 0.72 to 2.61, log 0.31) is never printed | [survival.md](survival.md) | done |
| 14-2 | A | yes | "80 bilateral patients", "only 20 of the 80 had a revision" | [survival.md](survival.md) | done |
| 14-3 | A | yes | "it rests on 16 early revisions" is not shown | [survival.md](survival.md) | done |
| 14-4 | B | yes | Proportional-hazards p-values: prose says 0.359 and 0.106, R prints 0.36 and 0.11, Python has neither | [survival.md](survival.md) | done |
| 14-5 | B | no | "2.85 times as many" cannot be reproduced from the quoted percentages | [survival.md](survival.md) | done |
| 14-6 | B | yes | "Reading the output, line by line" follows R's printout; Python lacks four of the items | [survival.md](survival.md) | done |
| 14-7 | B | no | Fine-Gray output calls the estimate "HR"; the prose calls it SHR | [survival.md](survival.md) | done |
| 14-8 | B | no | "81 of 600 procedures (13.5%)" | [survival.md](survival.md) | done |
| 14-9 | C | no | R's `exp(-coef)` column is printed seven times and never explained | [survival.md](survival.md) | done |
| 14-10 | C | no | The clustered model's p-values are printed in scientific notation and not read | [survival.md](survival.md) | done |
| 14-11 | C | no | The final table's univariable CIs differ from the ones at the top of the page | [survival.md](survival.md) | done |
| 15-1 | A | yes | "About 20%" false-positive chance for four groups | [beyond.md](beyond.md) | done |
| 15-2 | A | yes | Walking-aid use "rose", "fell", "below its pre-op level"; n = 328 | [beyond.md](beyond.md) | done |
| 15-3 | A | yes | "The SDs are similar (8.7 to 9.3 years)" and "the two small classes" | [beyond.md](beyond.md) | done |
| 15-4 | A | yes | F(3, 596) = 23.9 in two Results sentences | [beyond.md](beyond.md) | done |
| 15-5 | A | yes | Overall log-rank χ² = 33.5 (df = 2) | [beyond.md](beyond.md) | done |
| 15-6 | A | yes | "Two of the expected counts are below 5" | [beyond.md](beyond.md) | done |
| 15-7 | A | no | "the 80 patients who had both sides operated on" | [beyond.md](beyond.md) | done |
| 15-8 | B | yes | PROMIS "improved between each visit", "changes this large": no means shown | [beyond.md](beyond.md) | done |
| 15-9 | B | yes | EFAS "rose" with no medians; n = 50 printed in Python only | [beyond.md](beyond.md) | done |
| 15-10 | B | no | Holm's 0.044 and BH's 0.026: the arithmetic is not shown | [beyond.md](beyond.md) | done |
| 15-11 | B | no | Kruskal-Wallis "H = 24.3, df = 3, p < 0.001" not tied to the output | [beyond.md](beyond.md) | done |
| 15-12 | B | no | Overall Fisher p = 0.016 appears in the R tab only | [beyond.md](beyond.md) | done |
| 15-13 | B | no | Implant A vs B hazard ratio is printed but never read | [beyond.md](beyond.md) | done |
| 15-14 | C | no | Tukey and Games-Howell bullets leave columns unexplained | [beyond.md](beyond.md) | done |
| 16-1 | A | yes | Nested model: "patient-level intercept comes out at almost exactly zero", "singular" | [beyond.md](beyond.md) | open |
| 16-2 | A | yes | Complete-case means 49.2 and 84.0 | [beyond.md](beyond.md) | open |
| 16-3 | A | yes | 431 scores, 120 patients, 80 complete (66.7%) | [beyond.md](beyond.md) | open |
| 16-4 | A | yes | "SD 2.9" for the model and "SD 3.2 within each arm" at 3 months | [beyond.md](beyond.md) | open |
| 16-5 | A | yes | Ceiling and missed-visit counts at 12 months | [beyond.md](beyond.md) | open |
| 16-6 | A | yes | "46 of the knee patients had both knees replaced, so 92 of the 330 knees" | [beyond.md](beyond.md) | open |
| 16-7 | A | yes | The curve's "peak of about 89 points at around 8 months" is read off the plot | [beyond.md](beyond.md) | open |
| 16-8 | B | no | 330 knees, 1146 scores, 138 (42%), 58.2%: sums not spelled out | [beyond.md](beyond.md) | open |
| 16-9 | B | no | Residual variance 73.5 and residual SD 8.6: Python calls them "Scale" | [beyond.md](beyond.md) | open |
| 16-10 | B | no | "The undivided statistic, 77.15" | [beyond.md](beyond.md) | open |
| 16-11 | B | no | Exercise 2: page 9's complete-case means are quoted, not shown | [beyond.md](beyond.md) | open |
| 16-12 | C | no | Exercise 3: R gives p = 0.003, Python p = 0.002, no reason given | [beyond.md](beyond.md) | open |
| 16-13 | C | no | The contrast weights `c(-1, 0, 0, 1)` | [beyond.md](beyond.md) | open |
| 17-1 | ERROR | no | "limits of ±3.7°" contradicts the limits shown | [beyond.md](beyond.md) | done |
| 17-2 | A | yes | "`irr::kappa2(weight = "equal")` ... gives 0.63 here instead of 0.73" | [beyond.md](beyond.md) | open |
| 17-3 | B | no | ICC 0.915 reported as 0.91, 0.935 as 0.93, −0.265 as −0.26 | [beyond.md](beyond.md) | open |
| 17-4 | B | no | "0.896 for consistency, and 0.94 for the average of the two raters" | [beyond.md](beyond.md) | open |
| 17-5 | B | no | "40 of the 60 knees" and "48 of 60 knees" are not printed | [beyond.md](beyond.md) | open |
| 17-6 | B | yes | CIs of the limits: Python prints them in a different arrangement | [beyond.md](beyond.md) | open |
| 17-7 | C | yes | Kappa: "some of that would happen by chance" is never quantified | [beyond.md](beyond.md) | open |
| 18-1 | A | yes | The study period in the Methods is printed nowhere | [report-and-front.md](report-and-front.md) | open |
| 18-2 | A | yes | The software versions in the Methods are printed nowhere | [report-and-front.md](report-and-front.md) | open |
| 18-3 | B | yes | How many patients have both scores: 93, 77.5%, 86.8% and 70.1% are never computed | [report-and-front.md](report-and-front.md) | open |
| 18-4 | B | yes | The ceiling percentages 32.6% and 14.9% are never computed | [report-and-front.md](report-and-front.md) | open |
| 18-5 | B | yes | Exercise 3: the four percentages in the Results sentence are never computed; "27" is not derived | [report-and-front.md](report-and-front.md) | open |
| 18-6 | B | yes | Results: 44.2% and 55.8% are never computed | [report-and-front.md](report-and-front.md) | open |
| 18-7 | B | yes | Women: the text says 71.7% and 49.3%, the R table and the manuscript's own Table 1 say 72% and 49% | [report-and-front.md](report-and-front.md) | open |
| 18-8 | B | no | Exercise 1: R prints "p-value = 0.0035", the Results sentence says p = 0.003 | [report-and-front.md](report-and-front.md) | open |
| 18-9 | B | no | Exercise 2: the sign changes from 9.0 to −7.4, the outcome changes, and R prints p as `1.656337e-03` | [report-and-front.md](report-and-front.md) | open |
| 18-10 | B | no | Step 6: the difference of 9.0 points is printed only in the Python tab | [report-and-front.md](report-and-front.md) | open |
| 18-11 | B | yes | Step 7: the numbers at risk (17 at 8 years, 5 at 10) exist only under the R plot | [report-and-front.md](report-and-front.md) | open |
| 18-12 | B | no | Step 7: the output gives proportions, the prose percentages | [report-and-front.md](report-and-front.md) | open |
| 18-13 | B | no | Step 4: "2.9 points higher" is a subtraction the prose doesn't show | [report-and-front.md](report-and-front.md) | open |
| 18-14 | B | no | "They differ in the sixth decimal" cannot be seen in the output | [report-and-front.md](report-and-front.md) | open |
| 18-15 | B | no | "Five spellings of 'missing'", but the visible code lists four | [report-and-front.md](report-and-front.md) | open |
| 18-16 | C | yes | Step 7, Python: the follow-up quartiles are labeled 0.75, 0.50, 0.25, the reverse of R's 25, 50, 75 | [report-and-front.md](report-and-front.md) | open |
| 18-17 | C | no | The Methods name two methods that Step 7 never explains: "reverse Kaplan-Meier" and "Aalen-Johansen" | [report-and-front.md](report-and-front.md) | open |
| 18-18 | C | no | Step 4: the R and Python tables look different, and the 🔀 box explains only the SMDs | [report-and-front.md](report-and-front.md) | open |
| 18-19 | C | no | "Medium-to-large", "small" and "large" are used without the scale | [report-and-front.md](report-and-front.md) | open |
| gs-use-1 | B | yes | The "Try it" answer is a typed comment, not output | [report-and-front.md](report-and-front.md) | open |
| gs-use-2 | C | no | The illustration's medians differ by 2, its "Hodges-Lehmann difference" is 1, and the term is not explained | [report-and-front.md](report-and-front.md) | open |
| gs-use-3 | C | no | "IQR" is used before it is explained | [report-and-front.md](report-and-front.md) | open |
| gs-setup-1 | C | no | "Each step ends with a quick check", but steps 4 to 7 have none, and step 1's check points to a step that doesn't mention R | [report-and-front.md](report-and-front.md) | open |
| gs-setup-2 | C | no | The page never says how to open Terminal or PowerShell | [report-and-front.md](report-and-front.md) | open |
| gs-setup-3 | C | no | "Reading the data without cloning": which steps are still needed, and "any example" needs more than two packages | [report-and-front.md](report-and-front.md) | open |
| gs-real-1 | C | no | "Don't copy them anywhere else", then a repository that reads data from local folders | [report-and-front.md](report-and-front.md) | open |
| gs-real-2 | C | no | "The secure environment" is never defined | [report-and-front.md](report-and-front.md) | open |
| gs-real-3 | C | no | "Before every commit": a data file that `git status` lists as untracked can't be "unstaged" | [report-and-front.md](report-and-front.md) | open |
| gs-real-4 | C | no | BASEC and REDCap are named without saying what they are | [report-and-front.md](report-and-front.md) | open |
| choose-1 | C | no | The rows turn on "paired", "unpaired", "matched" and "unmatched", which the page neither explains nor links; the dashes are unexplained | [report-and-front.md](report-and-front.md) | open |
