# HFR Sub-project 2, Phase 2a (Data) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the synthetic data that phases 2b and 2c will teach from — four new datasets (hip fracture, foot & ankle RCT, ACL cohort, hip-preservation imaging) and the arthroplasty changes (PROMIS physical function, Oxford Hip Score, Swiss discharge labels) — without changing any number on any existing page.

**Architecture:** Each dataset gets its own generator in `data-raw/R/` (seeded `make_*()` function), its own codebook entry, its own testthat file asserting its built-in effects, and an allow-list line in `.gitignore`. Existing generators change only by adding deterministic columns (no new random draws in their streams), so every existing value stays byte-identical. One final task re-renders the site and proves no page number moved.

**Tech Stack:** R 4.4+ (tibble, tidyr, dplyr, readr, withr, survival, lmerTest, testthat) via renv; Python 3.12+ (pandas, pytest) via uv; Quarto 1.9.37; just.

**Spec:** `docs/superpowers/specs/2026-10-06-hfr-sp2-broaden-examples-design.md` (§3 data, §3.6 effects, §5 phase 2a, §6 testing). Parent spec: `docs/superpowers/specs/2026-10-06-hfr-stats-formation-design.md`. Repo rules: `CLAUDE.md`.

## Global Constraints

- Work on branch `sp2-broaden-examples` in `/Users/docschwab/repos/hfr-ortho/stats-formation`. Never commit to `main` (a push to `main` publishes the live site).
- Synthetic data only. Never hand-edit `data/` or `templates/`: change `data-raw/`, then regenerate.
- Seeds (the default argument of each `make_*()`): `make_hip_fracture` 20261101, `make_foot_ankle_rct` 20261102, `make_acl_cohort` 20261103, `make_hip_imaging` 20261104, Oxford Hip Score noise 20261105.
- **Choosing a seed is allowed only for a new generator, during this phase** (the TJS spec: "fixed seed, chosen in prototyping so every assertion passes"). If one of a new dataset's effect tests fails: first confirm the generator matches this plan character for character; then try that generator's seed + 10, + 20, … in order, take the first that passes every one of its tests, and record the chosen seed and the number tried in the generator's header comment and in the ledger. Never loosen an assertion, never change an effect size to pass, never change an existing generator's seed.
- Existing datasets must stay byte-identical except: `cohort.csv` (discharge label), `proms_long.csv` (two new columns). `data/CHECKSUMS.md5` changes as a result.
- Column names, value labels and ranges exactly as written in this plan (they implement spec §3).
- Tasks 1–6 regenerate data, which leaves the built site stale on purpose (the freshness test fails until Task 7 re-renders). In Tasks 1–6 run the R and Python tests, not `just check`.
- R tests: `Rscript -e 'testthat::test_dir("tests/testthat", filter = "<name>", stop_on_failure = TRUE)'`. All data tests: `Rscript data-raw/validate.R`.
- Commit messages: a plain sentence saying what changed, ending with:

  ```
  Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
  ```

- No push, no pull request, no merge without Doc's explicit go-ahead at that moment (Task 8).

## Review Focus

1. A reader copies a page's code and regenerates the data on their own machine: every CSV must come out byte for byte the same. *Test: each dataset's entry in `tests/testthat/test-data-reproducible.R` (Tasks 1, 3–6).*
2. The hip-fracture data show real ages up to 100, while "Working with real HFR data" tells readers to group ages of 90 or older: the codebook must say why. *Test: `the codebook explains why ages of 90 or older are not grouped` (Task 3).*
3. A page that still selects `discharge == "facility"` would silently get zero rows after the relabel, not an error. *Test: `test_pages_use_the_swiss_discharge_labels` (Task 2).*
4. A missed foot & ankle visit with an EFAS score but no pain score (or the reverse) would make the two outcomes disagree on who was seen. *Test: `a missed visit has every measure missing, and misses rise to about 15%` (Task 4).*
5. A number on an existing page changes because a generator's random stream moved. *Test: the frozen-results comparison in Task 7, Step 3, plus the reproducibility test (Task 1).*

---

### Task 1: PROMIS physical function and the Oxford Hip Score in `proms_long.csv`

**Files:**
- Modify: `data-raw/R/gen_proms.R` (`make_proms_long()`)
- Modify: `data-raw/R/codebooks.R` (`proms_long` entry)
- Test: `tests/testthat/test-data-proms.R`
- Regenerated: `data/proms_long.csv`, `data/codebooks/proms_long.csv`, `data/CHECKSUMS.md5`

**Interfaces:**
- Consumes: `clamp(x, lo, hi)` from `data-raw/R/gen_cohort.R`.
- Produces: `make_proms_long(cohort, seed = 20261008, ohs_seed = 20261105)`; `proms_long.csv` columns in this order: `case_id, patient_id, visit, visit_days, instrument, prom_score, ohs, vr12_pcs, vr12_mcs, promis_pf, walking_aid`.

- [ ] **Step 1: Write the failing tests**

In `tests/testthat/test-data-proms.R`, replace the test `"a missed visit has every measure missing"` with:

```r
test_that("a missed visit has every measure missing", {
  missed <- is.na(proms$prom_score)
  expect_true(all(is.na(proms$visit_days[missed])))
  expect_true(all(is.na(proms$vr12_pcs[missed])))
  expect_true(all(is.na(proms$promis_pf[missed])))
  expect_true(all(is.na(proms$ohs[missed])))
  expect_true(all(is.na(proms$walking_aid[missed])))
})
```

and append:

```r
test_that("PROMIS physical function is VR-12 PCS rescaled and improves from pre-op to 1 year", {
  expect_equal(is.na(proms$promis_pf), is.na(proms$vr12_pcs))
  expect_gt(stats::cor(proms$promis_pf, proms$vr12_pcs, use = "complete.obs"), 0.99)
  expect_true(all(proms$promis_pf >= 10 & proms$promis_pf <= 80, na.rm = TRUE))
  w <- wide("promis_pf")
  expect_lt(stats::t.test(w$`1yr`, w$preop, paired = TRUE)$p.value, 0.001)
})

test_that("the Oxford Hip Score is for THA only, has a ceiling at 1 year and tracks HOOS JR", {
  expect_true(all(is.na(proms$ohs[proms$instrument == "KOOS JR"])))
  hips <- proms[proms$instrument == "HOOS JR", ]
  expect_equal(is.na(hips$ohs), is.na(hips$prom_score))
  yr1 <- hips[hips$visit == "1yr" & !is.na(hips$ohs), ]
  expect_gte(mean(yr1$ohs == 48), 0.10)
  expect_gt(stats::cor(yr1$ohs, yr1$prom_score, method = "spearman"), 0.7)
})
```

- [ ] **Step 2: Run them to see them fail**

Run: `Rscript -e 'testthat::test_dir("tests/testthat", filter = "data-proms", stop_on_failure = TRUE)'`
Expected: FAIL (`promis_pf` and `ohs` don't exist).

- [ ] **Step 3: Add the columns to the generator**

In `data-raw/R/gen_proms.R`:

1. Change the signature to `make_proms_long <- function(cohort, seed = 20261008, ohs_seed = 20261105) {`.
2. In the `out <- tibble::tibble(` call, add after `vr12_mcs    = round(clamp(mcs, 0, 100), 1),`:

```r
    # PROMIS-29+2 physical function (T-score): VR-12 PCS rescaled, no new draws.
    promis_pf   = round(clamp(0.9 * pcs + 8, 10, 80), 1),
```

3. Change the `measures` line to:

```r
  measures <- c("visit_days", "prom_score", "vr12_pcs", "vr12_mcs", "promis_pf", "walking_aid")
```

4. Replace the final `out` (the function's last line) with:

```r
  # Oxford Hip Score (0-48, higher is better) for THA cases, tracking HOOS JR.
  # Its noise comes from its own seed after every other draw, so no other value
  # in this file (or any later dataset) changes.
  noise <- withr::with_seed(ohs_seed, stats::rnorm(nrow(out), 0, 2.5))
  out$ohs <- ifelse(out$instrument == "HOOS JR",
                    as.integer(clamp(round(0.48 * out$prom_score + noise), 0, 48)),
                    NA_integer_)
  dplyr::relocate(out, ohs, .after = prom_score)
```

Also update the header comment's first line to: `# PROMs in long format: one row per case x visit (preop, 6wk, 3mo, 1yr): HOOS JR or KOOS JR, the Oxford Hip Score (THA), VR-12 and PROMIS-29+2 physical function, walking aid.`

- [ ] **Step 4: Update the codebook**

In `data-raw/R/codebooks.R`, in the `proms_long = cb(` entry, add after the `"prom_score", …` row:

```r
      "ohs", "Oxford Hip Score (THA only)", "integer", "points", "0..48", "Higher = better; blank for TKA and for missed visits",
```

and after the `"vr12_mcs", …` row:

```r
      "promis_pf", "PROMIS-29+2 physical function", "numeric", "T-score", "10..80", "Mean 50, SD 10 in the reference population; higher = better",
```

- [ ] **Step 5: Regenerate and run the tests**

Run:
```bash
Rscript data-raw/generate.R && Rscript data-raw/validate.R && uv run pytest tests/python -q
git status --short data
```
Expected: all tests pass. `git status` shows only `data/proms_long.csv`, `data/codebooks/proms_long.csv` and `data/CHECKSUMS.md5` changed. Then confirm no existing value moved, by comparing the old file with the new one minus its two new columns:

```bash
uv run python - <<'EOF'
import io, subprocess
import pandas as pd
old = pd.read_csv(io.StringIO(subprocess.run(["git", "show", "HEAD:data/proms_long.csv"], capture_output=True, text=True).stdout))
new = pd.read_csv("data/proms_long.csv").drop(columns=["ohs", "promis_pf"])
pd.testing.assert_frame_equal(old, new)
print("every existing value unchanged")
EOF
```

Expected: `every existing value unchanged`.

- [ ] **Step 6: Commit**

```bash
git add data-raw/R/gen_proms.R data-raw/R/codebooks.R tests/testthat/test-data-proms.R data
git commit -m "PROMIS-29+2 physical function and the Oxford Hip Score (THA) in proms_long.csv; every existing value unchanged

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 2: Swiss discharge labels (`home` / `rehabilitation clinic`)

**Files:**
- Modify: `data-raw/R/gen_cohort.R` (discharge line), `data-raw/R/codebooks.R` (`cohort` entry)
- Modify: `en/catalog/05-one-group-vs-hypothetical.qmd`, `en/catalog/11-predict-from-one.qmd`, `en/catalog/12-predict-from-several.qmd`, `en/beyond/15-post-hoc.qmd`
- Test: `tests/testthat/test-data-cohort.R`, `tests/site/test_sources.py`
- Regenerated: `data/cohort.csv`, `data/codebooks/cohort.csv`, `data/CHECKSUMS.md5`

**Interfaces:**
- Consumes: nothing new.
- Produces: `cohort.csv` `discharge` values `home` / `rehabilitation clinic`.

- [ ] **Step 1: Write the failing tests**

Append to `tests/testthat/test-data-cohort.R`:

```r
test_that("discharge is home or to a rehabilitation clinic", {
  expect_setequal(unique(cohort$discharge), c("home", "rehabilitation clinic"))
})
```

Append to `tests/site/test_sources.py`:

```python
def test_pages_use_the_swiss_discharge_labels():
    """cohort.csv says "rehabilitation clinic"; code still selecting "facility" would silently match nothing."""
    offenders = [str(f.relative_to(ROOT)) for f in qmd_files() if re.search(r"facilit", f.read_text(encoding="utf-8"))]
    assert offenders == [], "Use the discharge label 'rehabilitation clinic' in: " + ", ".join(offenders)
```

Run: `Rscript -e 'testthat::test_dir("tests/testthat", filter = "data-cohort", stop_on_failure = TRUE)'; uv run pytest tests/site/test_sources.py -q -k discharge`
Expected: both FAIL.

- [ ] **Step 2: Relabel in the generator and codebook**

In `data-raw/R/gen_cohort.R`, in the `cases$discharge <- ifelse(…` call, change `"facility", "home")` to `"rehabilitation clinic", "home")`. In `data-raw/R/codebooks.R`, the cohort row `"discharge", "Discharge destination", "categorical", "", "home|facility", "",` becomes `"discharge", "Discharge destination", "categorical", "", "home|rehabilitation clinic", "",`.

- [ ] **Step 3: Relabel on the four pages**

```bash
uv run python - <<'EOF'
from pathlib import Path
files = [Path(p) for p in ["en/catalog/05-one-group-vs-hypothetical.qmd", "en/catalog/11-predict-from-one.qmd",
                           "en/catalog/12-predict-from-several.qmd", "en/beyond/15-post-hoc.qmd"]]
pairs = [   # identifiers first, then the label, then the prose
    ("ex_facility", "ex_rehab"),
    ("facility_model", "rehab_model"),
    ("facility_ors", "rehab_ors"),
    ('cohort["facility"]', 'cohort["rehab"]'),
    ('"facility ~', '"rehab ~'),
    ("mutate(facility =", "mutate(rehab ="),
    ("facility = fisher.test", "rehab = fisher.test"),
    ('"complication_90d", "facility"', '"complication_90d", "rehab"'),
    ('"facility"', '"rehabilitation clinic"'),
    ("A state report says 90% of joint replacement patients go home rather than to a facility.",
     "Suppose a national registry reports that 90% of joint replacement patients go home rather than to a rehabilitation clinic."),
    ("(facility or home)", "(rehabilitation clinic or home)"),
    ("to a facility", "to a rehabilitation clinic"),
]
texts = {f: f.read_text(encoding="utf-8") for f in files}
for old, new in pairs:
    hits = sum(t.count(old) for t in texts.values())
    assert hits > 0, f"not found: {old}"
    texts = {f: t.replace(old, new) for f, t in texts.items()}
for f, t in texts.items():
    f.write_text(t, encoding="utf-8")
print("relabelled")
EOF
git grep -n -i "facilit" -- en
```

Expected: `relabelled`, then no output from `git grep`. If a line remains, edit it by hand in the same spirit (identifier → `rehab`, label → `rehabilitation clinic`, prose → "rehabilitation clinic").

- [ ] **Step 4: Regenerate, test, and render the four pages**

Run:
```bash
Rscript data-raw/generate.R && Rscript data-raw/validate.R && uv run pytest tests/python -q
uv run pytest tests/site/test_sources.py -q
git status --short data
quarto render en/catalog/05-one-group-vs-hypothetical.qmd && quarto render en/catalog/11-predict-from-one.qmd && quarto render en/catalog/12-predict-from-several.qmd && quarto render en/beyond/15-post-hoc.qmd
```

Expected: all tests pass; `data/cohort.csv`, `data/codebooks/cohort.csv`, `data/CHECKSUMS.md5` changed; the four pages render (their prose guards still hold: 30 patients went to a rehabilitation clinic, OR 2.06, and so on). Then confirm only the label changed:

```bash
uv run python - <<'EOF'
import io, subprocess
import pandas as pd
old = pd.read_csv(io.StringIO(subprocess.run(["git", "show", "HEAD:data/cohort.csv"], capture_output=True, text=True).stdout))
new = pd.read_csv("data/cohort.csv")
old["discharge"] = old["discharge"].replace({"facility": "rehabilitation clinic"})
pd.testing.assert_frame_equal(old, new)
print("only the discharge label changed")
EOF
```

Expected: `only the discharge label changed`.

- [ ] **Step 5: Commit**

```bash
git add data-raw/R/gen_cohort.R data-raw/R/codebooks.R tests/testthat/test-data-cohort.R tests/site/test_sources.py data en _freeze
git commit -m "Discharge home or to a rehabilitation clinic (was facility), in the data and on pages 5, 11, 12 and 15; no number changes

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 3: `hip_fracture.csv` (trauma)

**Files:**
- Create: `data-raw/R/gen_hip_fracture.R`, `tests/testthat/test-data-hip-fracture.R`
- Modify: `data-raw/R/codebooks.R`, `data-raw/generate.R`, `.gitignore`, `tests/testthat/test-data-codebooks.R`, `tests/testthat/test-data-reproducible.R`, `tests/python/test_gitignore.py`, `data/README.md`
- Generated: `data/hip_fracture.csv`, `data/codebooks/hip_fracture.csv`

**Interfaces:**
- Consumes: `clamp()`.
- Produces: `make_hip_fracture(seed = 20261101, n = 400)` returning a tibble with columns `patient_id, age, sex, asa, dementia, residence, fracture_type, treatment, hours_to_surgery, surgery_within_48h, los_days, death_30d, followup_days, died`.

- [ ] **Step 1: Write the failing tests**

Create `tests/testthat/test-data-hip-fracture.R`:

```r
hip <- read_tidy("hip_fracture.csv")
hip$delay_days <- hip$hours_to_surgery / 24

skewness <- function(x) mean((x - mean(x))^3) / stats::sd(x)^3

test_that("one row per patient: 400 patients aged 65 or over, most over 80", {
  expect_equal(nrow(hip), 400)
  expect_equal(anyDuplicated(hip$patient_id), 0)
  expect_true(all(hip$age >= 65 & hip$age <= 100))
  expect_gt(stats::median(hip$age), 80)
})

test_that("derived columns, treatment and timeline are consistent", {
  expect_equal(hip$surgery_within_48h, as.integer(hip$hours_to_surgery <= 48))
  expect_true(all(hip$treatment[hip$fracture_type == "trochanteric"] == "nail"))
  expect_true(all(hip$death_30d <= hip$died))
  expect_true(all(hip$followup_days[hip$death_30d == 1] <= 30))
  expect_true(all(hip$followup_days[hip$died == 0] == 365))
  dead <- hip$died == 1
  expect_true(all(hip$followup_days[dead] * 24 > hip$hours_to_surgery[dead]))   # death after surgery
  expect_true(all(hip$los_days[dead] <= hip$followup_days[dead]))
})

test_that("about 7% die within 30 days and about 85% are operated within 48 hours", {
  expect_gte(mean(hip$death_30d), 0.05)
  expect_lte(mean(hip$death_30d), 0.10)
  expect_gte(mean(hip$surgery_within_48h), 0.80)
  expect_lte(mean(hip$surgery_within_48h), 0.89)
})

test_that("time to surgery is right-skewed", {
  expect_gt(skewness(hip$hours_to_surgery), 1)
})

test_that("death within 30 days rises with the time to surgery and with age", {
  co <- summary(stats::glm(death_30d ~ delay_days + age, family = binomial, data = hip))$coefficients
  expect_gt(co["delay_days", "Estimate"], 0)
  expect_lt(co["delay_days", "Pr(>|z|)"], 0.05)
  expect_gt(co["age", "Estimate"], 0)
})

test_that("the codebook explains why ages of 90 or older are not grouped", {
  cb <- readr::read_csv(data_path("codebooks", "hip_fracture.csv"), show_col_types = FALSE,
                        col_types = readr::cols(.default = "c"))
  expect_match(cb$notes[cb$variable == "age"], "90 or older")
})
```

In `tests/testthat/test-data-codebooks.R`, add `"hip_fracture.csv"` to the `expect_setequal(books, c(…))` list. In `tests/testthat/test-data-reproducible.R`, add to the `fresh` list:

```r
    "hip_fracture.csv"                          = env$make_hip_fracture(),
```

In `tests/python/test_gitignore.py`, add `"data/hip_fracture.csv"` and `"data/codebooks/hip_fracture.csv"` to `test_project_files_are_not_ignored`'s list.

Run: `Rscript -e 'testthat::test_dir("tests/testthat", filter = "data-(hip-fracture|codebooks|reproducible)", stop_on_failure = TRUE)'; uv run pytest tests/python/test_gitignore.py -q`
Expected: FAIL (no file, no generator, path ignored).

- [ ] **Step 2: Write the generator**

Create `data-raw/R/gen_hip_fracture.R`:

```r
# Hip fracture (trauma): one row per patient aged 65 or over, most over 80.
# Death within 30 days rises with age, ASA class and the time to surgery, so
# page 11's logistic regression has an effect to find. About 85% are operated
# within 48 hours (page 5's binomial test against a 90% target). Survivors of
# the first 30 days die at a lower, still age-dependent rate; follow-up stops
# at 1 year. Rates are tuned for teaching, not taken from a registry.

make_hip_fracture <- function(seed = 20261101, n = 400) {
  set.seed(seed)
  age <- as.integer(pmin(100, round(65 + stats::rgamma(n, shape = 6, scale = 3.2))))
  sex <- sample(c("Female", "Male"), n, TRUE, prob = c(0.72, 0.28))
  asa <- sample(1:4, n, TRUE, prob = c(0.03, 0.27, 0.55, 0.15))
  dementia <- stats::rbinom(n, 1, stats::plogis(-1.6 + 0.08 * (age - 84)))
  residence <- ifelse(stats::rbinom(n, 1, stats::plogis(
    -1.8 + 1.6 * dementia + 0.05 * (age - 84))) == 1, "nursing home", "home")
  fracture_type <- sample(c("femoral neck", "trochanteric"), n, TRUE, prob = c(0.55, 0.45))
  treatment <- ifelse(fracture_type == "trochanteric", "nail",
                      ifelse(stats::runif(n) < 0.85, "hemiarthroplasty", "screws"))
  hours_to_surgery <- round(stats::rlnorm(n, meanlog = log(26), sdlog = 0.6), 1)
  los_days <- as.integer(4 + stats::rnbinom(n, size = 4, mu = 7))

  death_30d <- stats::rbinom(n, 1, stats::plogis(
    -2.75 + 0.07 * (age - 84) + 0.5 * (asa - 3) + 0.9 * (hours_to_surgery - 30) / 24))
  later <- stats::rexp(n, rate = 0.0007 * exp(0.06 * (age - 84) + 0.4 * dementia))
  death_day <- ifelse(death_30d == 1, sample(2:30, n, TRUE), 30 + ceiling(later))
  death_day <- pmax(death_day, ceiling(hours_to_surgery / 24) + 1)   # deaths come after surgery
  death_30d <- as.integer(death_day <= 30)
  died <- as.integer(death_day <= 365)

  tibble::tibble(
    patient_id         = sprintf("H%04d", seq_len(n)),
    age, sex, asa, dementia, residence, fracture_type, treatment,
    hours_to_surgery,
    surgery_within_48h = as.integer(hours_to_surgery <= 48),
    los_days           = as.integer(pmin(los_days, ifelse(died == 1, death_day, Inf))),
    death_30d,
    followup_days      = as.integer(pmin(death_day, 365)),
    died
  )
}
```

- [ ] **Step 3: Codebook, generate.R, .gitignore, README**

In `data-raw/R/codebooks.R`, add to the `books <- list(` (after `survey_items_long = cb(…)`, with a comma after its closing parenthesis):

```r
    hip_fracture = cb(
      "patient_id", "Patient ID", "id", "", "", "One row per patient aged 65 or over with a hip fracture",
      "age", "Age at fracture", "integer", "years", "65..100", "Real ages, because the data are invented; with real data, group ages of 90 or older (see Working with real HFR data)",
      "sex", "Sex", "categorical", "", "Female|Male", "",
      "asa", "ASA physical status class", "integer", "", "1|2|3|4", "Ordinal",
      "dementia", "Dementia", "binary", "", "0|1", "1 = yes",
      "residence", "Residence before the fracture", "categorical", "", "home|nursing home", "",
      "fracture_type", "Fracture type", "categorical", "", "femoral neck|trochanteric", "",
      "treatment", "Treatment", "categorical", "", "hemiarthroplasty|nail|screws", "Trochanteric fractures are nailed",
      "hours_to_surgery", "Time from admission to surgery", "numeric", "hours", "0..400", "Right-skewed",
      "surgery_within_48h", "Operated within 48 hours", "binary", "", "0|1", "1 = yes; from hours_to_surgery",
      "los_days", "Length of hospital stay", "integer", "days", "1..60", "",
      "death_30d", "Died within 30 days", "binary", "", "0|1", "1 = yes; rates are tuned for teaching",
      "followup_days", "Follow-up to death or 1 year", "integer", "days", "1..365", "",
      "died", "Died during follow-up", "binary", "", "0|1", "1 = yes; 0 = alive at 1 year"
    )
```

In `data-raw/generate.R`, after `write_tidy(items, "data/answer-keys/survey_items_long.csv")` add:

```r
write_tidy(make_hip_fracture(), "data/hip_fracture.csv")
```

In `.gitignore`, under `# --- ... except these named synthetic files`, add `!/data/hip_fracture.csv` (after `!/data/messy_survey_export.csv`) and `!/data/codebooks/hip_fracture.csv` (after the last `!/data/codebooks/…` line).

In `data/README.md`, add a row to the "Tidy datasets" table:

```markdown
| `hip_fracture.csv` | hip-fracture patient aged 65 or over (400) | trauma examples: a proportion, a binomial test, logistic regression |
```

- [ ] **Step 4: Generate and run the tests**

Run:
```bash
Rscript data-raw/generate.R && Rscript data-raw/validate.R && uv run pytest tests/python -q
git status --short data
```

Expected: all tests pass (seed rule in Global Constraints if an effect test fails); only `data/hip_fracture.csv`, `data/codebooks/hip_fracture.csv` and `data/CHECKSUMS.md5` are new or changed.

- [ ] **Step 5: Commit**

```bash
git add data-raw tests .gitignore data
git commit -m "hip_fracture.csv: 400 synthetic hip-fracture patients, 30-day death rising with age and time to surgery, about 85% operated within 48 hours

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 4: `foot_ankle_rct.csv` and `foot_ankle_rct_long.csv` (foot & ankle)

**Files:**
- Create: `data-raw/R/gen_foot_ankle_rct.R`, `tests/testthat/test-data-foot-ankle.R`
- Modify: `data-raw/R/codebooks.R`, `data-raw/generate.R`, `.gitignore`, `tests/testthat/test-data-codebooks.R`, `tests/testthat/test-data-reproducible.R`, `tests/python/test_gitignore.py`, `data/README.md`
- Generated: `data/foot_ankle_rct.csv`, `data/foot_ankle_rct_long.csv`, their codebooks

**Interfaces:**
- Consumes: `clamp()`.
- Produces: `make_foot_ankle_rct(seed = 20261102, n = 120)` returning `list(wide = <tibble>, long = <tibble>)`; wide columns `patient_id, arm, age, sex, union_3mo` (plus the dropped latent `.ability`); long columns `patient_id, arm, visit, visit_days, efas, pain_nrs`.

- [ ] **Step 1: Write the failing tests**

Create `tests/testthat/test-data-foot-ankle.R`:

```r
fa  <- read_tidy("foot_ankle_rct.csv")
fal <- read_tidy("foot_ankle_rct_long.csv")
seen_at <- function(v) fal[fal$visit == v & !is.na(fal$efas), ]

test_that("120 patients randomized 1:1, each with four visits", {
  expect_equal(nrow(fa), 120)
  expect_equal(anyDuplicated(fa$patient_id), 0)
  expect_equal(as.vector(table(fa$arm)[c("boot", "cast")]), c(60, 60))
  expect_equal(nrow(fal), 4 * 120)
  expect_equal(nrow(dplyr::distinct(fal, patient_id, visit)), nrow(fal))
  j <- dplyr::left_join(fal, fa[, c("patient_id", "arm")], by = "patient_id", suffix = c("", "_wide"))
  expect_equal(j$arm, j$arm_wide)
})

test_that("a missed visit has every measure missing, and misses rise to about 15%", {
  missed <- is.na(fal$efas)
  expect_equal(missed, is.na(fal$pain_nrs))
  expect_equal(missed, is.na(fal$visit_days))
  miss <- tapply(missed, fal$visit, mean)
  expect_lt(miss[["6wk"]], 0.10)
  expect_gt(miss[["12mo"]], 0.08)
  expect_lt(miss[["12mo"]], 0.25)
})

test_that("the boot gives a better EFAS score at 3 months, by 2 to 4 points", {
  d <- seen_at("3mo")
  diff <- mean(d$efas[d$arm == "boot"]) - mean(d$efas[d$arm == "cast"])
  expect_gt(diff, 2)
  expect_lt(diff, 4)
  expect_lt(stats::t.test(efas ~ arm, data = d)$p.value, 0.01)
})

test_that("the boot gives less pain at 6 weeks", {
  d <- fal[fal$visit == "6wk" & !is.na(fal$pain_nrs), ]
  expect_lt(mean(d$pain_nrs[d$arm == "boot"]), mean(d$pain_nrs[d$arm == "cast"]))
  expect_lt(stats::wilcox.test(pain_nrs ~ arm, data = d, exact = FALSE)$p.value, 0.05)
})

test_that("the arms converge by 12 months: a group x time interaction", {
  d <- seen_at("12mo")
  expect_lt(abs(mean(d$efas[d$arm == "boot"]) - mean(d$efas[d$arm == "cast"])), 1)
  fit <- lmerTest::lmer(efas ~ arm * visit + (1 | patient_id), data = fal)
  expect_lt(stats::anova(fit)["arm:visit", "Pr(>F)"], 0.01)
})

test_that("with a boot, the EFAS score keeps changing over the year (Friedman)", {
  b <- fal[fal$arm == "boot" & fal$visit %in% c("6wk", "3mo", "12mo"), c("patient_id", "visit", "efas")]
  w <- tidyr::pivot_wider(b, names_from = visit, values_from = efas)
  w <- w[stats::complete.cases(w), ]
  expect_lt(stats::friedman.test(as.matrix(w[, c("6wk", "3mo", "12mo")]))$p.value, 0.001)
})
```

Add `"foot_ankle_rct.csv", "foot_ankle_rct_long.csv"` to the books list in `test-data-codebooks.R`. In `test-data-reproducible.R`, add `fa <- env$make_foot_ankle_rct()` just before `fresh <- list(` and add to `fresh`:

```r
    "foot_ankle_rct.csv"                        = fa$wide,
    "foot_ankle_rct_long.csv"                   = fa$long,
```

In `tests/python/test_gitignore.py`, add `"data/foot_ankle_rct.csv"`, `"data/foot_ankle_rct_long.csv"`, `"data/codebooks/foot_ankle_rct.csv"`, `"data/codebooks/foot_ankle_rct_long.csv"` to the not-ignored list.

Run: `Rscript -e 'testthat::test_dir("tests/testthat", filter = "data-(foot-ankle|codebooks|reproducible)", stop_on_failure = TRUE)'; uv run pytest tests/python/test_gitignore.py -q`
Expected: FAIL.

- [ ] **Step 2: Write the generator**

Create `data-raw/R/gen_foot_ankle_rct.R`:

```r
# Foot & ankle RCT: cast vs removable boot after a midfoot (Chopart) injury,
# randomized 1:1. EFAS score (European Foot and Ankle Society; 6 items scored
# 0-4, total 0-24, higher is better) and pain (NRS 0-10) at 6 weeks, 3 months,
# 6 months and 12 months. The boot leads early and the arms converge by 12
# months (the group x time interaction on page 16). A missed visit keeps its
# row with every measure missing.

make_foot_ankle_rct <- function(seed = 20261102, n = 120) {
  set.seed(seed)
  wide <- tibble::tibble(
    patient_id = sprintf("F%03d", seq_len(n)),
    arm        = sample(rep(c("cast", "boot"), each = n / 2)),
    age        = as.integer(clamp(round(stats::rnorm(n, 42, 14)), 18, 80)),
    sex        = sample(c("Female", "Male"), n, TRUE),
    union_3mo  = stats::rbinom(n, 1, 0.88),
    .ability   = stats::rnorm(n, 0, 2.2)
  )
  visits <- tibble::tibble(
    visit     = c("6wk", "3mo", "6mo", "12mo"),
    nominal   = c(42L, 91L, 182L, 365L),
    jitter    = c(5L, 10L, 14L, 21L),
    p_missing = c(0.05, 0.08, 0.12, 0.15),
    efas_cast = c(9, 14, 18, 20.5),
    efas_boot = c(12, 17, 19, 20.5),
    pain_cast = c(5.0, 3.0, 2.0, 1.0),
    pain_boot = c(3.8, 2.4, 1.8, 1.0)
  )
  grid <- tidyr::expand_grid(wide, visits)
  m <- nrow(grid)
  boot <- grid$arm == "boot"
  efas <- ifelse(boot, grid$efas_boot, grid$efas_cast) + grid$.ability + stats::rnorm(m, 0, 2)
  pain <- ifelse(boot, grid$pain_boot, grid$pain_cast) - 0.3 * grid$.ability + stats::rnorm(m, 0, 1.6)
  visit_days <- grid$nominal + as.integer(round(stats::runif(m, -grid$jitter, grid$jitter)))
  missed <- stats::runif(m) < grid$p_missing

  long <- tibble::tibble(
    patient_id = grid$patient_id,
    arm        = grid$arm,
    visit      = grid$visit,
    visit_days = as.integer(visit_days),
    efas       = as.integer(clamp(round(efas), 0, 24)),
    pain_nrs   = as.integer(clamp(round(pain), 0, 10))
  )
  long[missed, c("visit_days", "efas", "pain_nrs")] <- NA
  list(wide = wide, long = long)
}
```

- [ ] **Step 3: Codebooks, generate.R, .gitignore, README**

Add to `codebooks()`'s list:

```r
    foot_ankle_rct = cb(
      "patient_id", "Patient ID", "id", "", "", "One row per randomized patient (cast vs boot after a midfoot injury)",
      "arm", "Randomized arm", "categorical", "", "cast|boot", "1:1",
      "age", "Age at injury", "integer", "years", "18..80", "",
      "sex", "Sex", "categorical", "", "Female|Male", "",
      "union_3mo", "Radiographic union at 3 months", "binary", "", "0|1", "1 = yes"
    ),
    foot_ankle_rct_long = cb(
      "patient_id", "Patient ID", "id", "", "", "One row per patient x visit; links to foot_ankle_rct.csv",
      "arm", "Randomized arm", "categorical", "", "cast|boot", "",
      "visit", "Scheduled visit", "categorical", "", "6wk|3mo|6mo|12mo", "",
      "visit_days", "Days from injury to the visit", "integer", "days", "30..400", "Blank = visit missed",
      "efas", "EFAS score", "integer", "points", "0..24", "European Foot and Ankle Society score; higher = better",
      "pain_nrs", "Pain, numeric rating scale", "integer", "points", "0..10", "0 = no pain"
    )
```

In `data-raw/generate.R`, after the hip-fracture line add:

```r
fa <- make_foot_ankle_rct()
write_tidy(fa$wide, "data/foot_ankle_rct.csv")
write_tidy(fa$long, "data/foot_ankle_rct_long.csv")
```

`.gitignore` allow-list: `!/data/foot_ankle_rct.csv`, `!/data/foot_ankle_rct_long.csv`, `!/data/codebooks/foot_ankle_rct.csv`, `!/data/codebooks/foot_ankle_rct_long.csv`. `data/README.md` row:

```markdown
| `foot_ankle_rct.csv`, `foot_ankle_rct_long.csv` | randomized patient (120); patient × visit | foot & ankle RCT (cast vs boot, EFAS score): two-group tests, Friedman, mixed models |
```

- [ ] **Step 4: Generate and run the tests**

Run:
```bash
Rscript data-raw/generate.R && Rscript data-raw/validate.R && uv run pytest tests/python -q
git status --short data
```

Expected: all pass (seed rule if an effect fails); only the four new files and `CHECKSUMS.md5` new or changed.

- [ ] **Step 5: Commit**

```bash
git add data-raw tests .gitignore data
git commit -m "foot_ankle_rct (wide and long): 120 synthetic patients, cast vs boot, EFAS and pain at four visits; the boot leads early and the arms converge by 12 months

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 5: `acl_cohort.csv` (sports & arthroscopy)

**Files:**
- Create: `data-raw/R/gen_acl.R`, `tests/testthat/test-data-acl.R`
- Modify: `data-raw/R/codebooks.R`, `data-raw/generate.R`, `.gitignore`, `tests/testthat/test-data-codebooks.R`, `tests/testthat/test-data-reproducible.R`, `tests/python/test_gitignore.py`, `data/README.md`, `docs/superpowers/specs/2026-10-06-hfr-sp2-broaden-examples-design.md` (§3.3: add `failure_2y`)
- Generated: `data/acl_cohort.csv`, `data/codebooks/acl_cohort.csv`

**Interfaces:**
- Consumes: `clamp()`.
- Produces: `make_acl_cohort(seed = 20261103, n = 350)`; columns `case_id, age, sex, graft, tibial_slope_deg, tegner_preinjury, rts_12mo, followup_years, graft_failure, failure_2y`.

- [ ] **Step 1: Write the failing tests**

Create `tests/testthat/test-data-acl.R`:

```r
acl <- read_tidy("acl_cohort.csv")

test_that("350 reconstructions, followed for at least 2 years unless the graft failed", {
  expect_equal(nrow(acl), 350)
  expect_equal(anyDuplicated(acl$case_id), 0)
  expect_true(all(acl$followup_years >= 2 | acl$graft_failure == 1))
  expect_equal(acl$failure_2y, as.integer(acl$graft_failure == 1 & acl$followup_years <= 2))
})

test_that("graft failure within 2 years is unrelated to hamstring vs BPTB (a true null)", {
  d <- acl[acl$graft %in% c("hamstring", "BPTB"), ]
  expect_gt(stats::fisher.test(table(d$graft, d$failure_2y))$p.value, 0.2)
})

test_that("the hazard of graft failure rises with posterior tibial slope", {
  fit <- survival::coxph(survival::Surv(followup_years, graft_failure) ~ tibial_slope_deg, data = acl)
  hr <- exp(stats::coef(fit))[["tibial_slope_deg"]]
  expect_gt(hr, 1.10)
  expect_lt(hr, 1.35)
  expect_lt(summary(fit)$coefficients["tibial_slope_deg", "Pr(>|z|)"], 0.05)
})

test_that("return to sport at 12 months differs by graft", {
  expect_lt(stats::chisq.test(table(acl$graft, acl$rts_12mo))$p.value, 0.05)
})

test_that("return to sport rises with the pre-injury Tegner level and falls with age", {
  co <- summary(stats::glm(rts_12mo ~ graft + age + sex + tegner_preinjury,
                           family = binomial, data = acl))$coefficients
  expect_gt(co["tegner_preinjury", "Estimate"], 0)
  expect_lt(co["tegner_preinjury", "Pr(>|z|)"], 0.05)
  expect_lt(co["age", "Estimate"], 0)
  expect_lt(co["age", "Pr(>|z|)"], 0.05)
})
```

Add `"acl_cohort.csv"` to `test-data-codebooks.R`'s list; add `"acl_cohort.csv" = env$make_acl_cohort(),` to `fresh`; add `"data/acl_cohort.csv"`, `"data/codebooks/acl_cohort.csv"` to `test_gitignore.py`'s not-ignored list.

Run: `Rscript -e 'testthat::test_dir("tests/testthat", filter = "data-(acl|codebooks|reproducible)", stop_on_failure = TRUE)'; uv run pytest tests/python/test_gitignore.py -q`
Expected: FAIL.

- [ ] **Step 2: Write the generator**

Create `data-raw/R/gen_acl.R`:

```r
# ACL reconstruction (sports): one row per primary reconstruction. Graft
# failure depends on posterior tibial slope (hazard ratio about 1.22 per
# degree) but not on the graft, so failure within 2 years is a true null for
# hamstring vs BPTB (page 6). Return to sport at 12 months differs by graft and
# rises with the pre-injury Tegner level. Everyone is followed for at least 2
# years unless the graft fails, so failure within 2 years is known for all.
# Rates are tuned for teaching.

make_acl_cohort <- function(seed = 20261103, n = 350) {
  set.seed(seed)
  age   <- as.integer(clamp(round(15 + stats::rgamma(n, shape = 3, scale = 4.5)), 15, 50))
  sex   <- sample(c("Female", "Male"), n, TRUE, prob = c(0.42, 0.58))
  graft <- sample(c("BPTB", "hamstring", "quadriceps"), n, TRUE, prob = c(0.35, 0.45, 0.20))
  tibial_slope_deg <- round(clamp(stats::rnorm(n, 10, 2.5), 4, 18), 1)
  tegner_preinjury <- as.integer(clamp(round(stats::rnorm(n, 6.5 - 0.05 * (age - 28), 1.6)), 1, 10))
  graft_effect <- unname(c(BPTB = 0.5, hamstring = -0.1, quadriceps = -0.6)[graft])
  rts_12mo <- stats::rbinom(n, 1, stats::plogis(
    0.1 + graft_effect + 0.35 * (tegner_preinjury - 6.5) - 0.05 * (age - 28)))

  rate   <- 0.03 * exp(log(1.22) * (tibial_slope_deg - 10) - 0.03 * (age - 28))   # per year
  t_fail <- stats::rexp(n, rate)
  censor <- stats::runif(n, 2, 6)
  graft_failure  <- as.integer(t_fail <= censor)
  followup_years <- pmax(0.01, round(pmin(t_fail, censor), 2))

  tibble::tibble(
    case_id = sprintf("A%04d", seq_len(n)),
    age, sex, graft, tibial_slope_deg, tegner_preinjury, rts_12mo,
    followup_years, graft_failure,
    failure_2y = as.integer(graft_failure == 1 & followup_years <= 2)
  )
}
```

- [ ] **Step 3: Codebook, generate.R, .gitignore, README, spec**

Add to `codebooks()`'s list:

```r
    acl_cohort = cb(
      "case_id", "Reconstruction (case) ID", "id", "", "", "One row per primary ACL reconstruction",
      "age", "Age at surgery", "integer", "years", "15..50", "",
      "sex", "Sex", "categorical", "", "Female|Male", "",
      "graft", "Graft", "categorical", "", "BPTB|hamstring|quadriceps", "BPTB = bone-patellar tendon-bone",
      "tibial_slope_deg", "Posterior tibial slope", "numeric", "degrees", "4..18", "",
      "tegner_preinjury", "Tegner activity level before the injury", "integer", "", "1..10", "Ordinal; higher = more demanding sport",
      "rts_12mo", "Returned to pre-injury sport at 12 months", "binary", "", "0|1", "1 = yes",
      "followup_years", "Follow-up to graft failure or censoring", "numeric", "years", "0.01..6", "At least 2 years unless the graft failed",
      "graft_failure", "Graft failure during follow-up", "binary", "", "0|1", "1 = failed; rates are tuned for teaching",
      "failure_2y", "Graft failure within 2 years", "binary", "", "0|1", "1 = yes; known for everyone"
    )
```

`data-raw/generate.R`: `write_tidy(make_acl_cohort(), "data/acl_cohort.csv")`. `.gitignore`: `!/data/acl_cohort.csv`, `!/data/codebooks/acl_cohort.csv`. `data/README.md` row:

```markdown
| `acl_cohort.csv` | primary ACL reconstruction (350) | sports examples: Fisher's exact test, chi-square, Cox and logistic regression |
```

In the sub-project 2 spec §3.3 table, add a row after `followup_years`, `graft_failure`: `| failure_2y | graft failure within 2 years, 0/1 (everyone is followed at least 2 years unless the graft fails), for page 6's Fisher test |`.

- [ ] **Step 4: Generate and run the tests**

Run:
```bash
Rscript data-raw/generate.R && Rscript data-raw/validate.R && uv run pytest tests/python -q
git status --short data
```

Expected: all pass (seed rule if an effect fails); only the two new files and `CHECKSUMS.md5`.

- [ ] **Step 5: Commit**

```bash
git add data-raw tests .gitignore data docs/superpowers/specs/2026-10-06-hfr-sp2-broaden-examples-design.md
git commit -m "acl_cohort.csv: 350 synthetic ACL reconstructions; graft failure rises with tibial slope, not with the graft; return to sport differs by graft and Tegner level

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 6: `hip_preservation_imaging.csv` (joint preservation)

**Files:**
- Create: `data-raw/R/gen_hip_imaging.R`, `tests/testthat/test-data-hip-imaging.R`
- Modify: `data-raw/R/codebooks.R`, `data-raw/generate.R`, `.gitignore`, `tests/testthat/test-data-codebooks.R`, `tests/testthat/test-data-reproducible.R`, `tests/python/test_gitignore.py`, `data/README.md`
- Generated: `data/hip_preservation_imaging.csv`, `data/codebooks/hip_preservation_imaging.csv`

**Interfaces:**
- Consumes: `clamp()`.
- Produces: `make_hip_imaging(seed = 20261104, n = 80)`; columns `hip_id, age, sex, alpha_dunn45_deg, alpha_frogleg_deg, torsion_ct_deg, torsion_budin_deg, crossover_sign`.

- [ ] **Step 1: Write the failing tests**

Create `tests/testthat/test-data-hip-imaging.R`:

```r
img <- read_tidy("hip_preservation_imaging.csv")

test_that("one row per hip: 80 hips in young adults", {
  expect_equal(nrow(img), 80)
  expect_equal(anyDuplicated(img$hip_id), 0)
  expect_true(all(img$age >= 18 & img$age <= 45))
})

test_that("the frog-leg view reads the alpha angle about 4 degrees higher than Dunn 45", {
  d <- img$alpha_frogleg_deg - img$alpha_dunn45_deg
  expect_gt(mean(d), 3)
  expect_lt(mean(d), 5)
  expect_lt(stats::t.test(img$alpha_frogleg_deg, img$alpha_dunn45_deg, paired = TRUE)$p.value, 0.001)
})

test_that("Budin and CT torsion correlate strongly but disagree more at the extremes", {
  r <- stats::cor(img$torsion_ct_deg, img$torsion_budin_deg)
  expect_gt(r, 0.80)
  expect_lt(r, 0.92)
  difference <- img$torsion_budin_deg - img$torsion_ct_deg
  average <- (img$torsion_budin_deg + img$torsion_ct_deg) / 2
  expect_lt(summary(stats::lm(difference ~ average))$coefficients["average", "Pr(>|t|)"], 0.05)
})
```

Add `"hip_preservation_imaging.csv"` to `test-data-codebooks.R`'s list; `"hip_preservation_imaging.csv" = env$make_hip_imaging(),` to `fresh`; `"data/hip_preservation_imaging.csv"`, `"data/codebooks/hip_preservation_imaging.csv"` to `test_gitignore.py`.

Run: `Rscript -e 'testthat::test_dir("tests/testthat", filter = "data-(hip-imaging|codebooks|reproducible)", stop_on_failure = TRUE)'; uv run pytest tests/python/test_gitignore.py -q`
Expected: FAIL.

- [ ] **Step 2: Write the generator**

Create `data-raw/R/gen_hip_imaging.R`:

```r
# Hip-preservation imaging (joint preservation): one row per hip in young
# adults assessed for hip-preservation surgery. The frog-leg view reads the
# alpha angle about 4 degrees higher than the Dunn 45-degree view of the same
# hip (page 7's paired t test). The modified Budin view tracks CT femoral
# torsion closely (r about 0.88) but compresses it, reading high at low
# torsion and low at high torsion: the two correlate without agreeing (page
# 10, and page 17's point that correlation is not agreement).

make_hip_imaging <- function(seed = 20261104, n = 80) {
  set.seed(seed)
  alpha_true <- stats::rnorm(n, 58, 10)
  torsion_ct <- stats::rnorm(n, 15, 9)
  tibble::tibble(
    hip_id            = sprintf("J%03d", seq_len(n)),
    age               = as.integer(round(clamp(stats::rnorm(n, 30, 7), 18, 45))),
    sex               = sample(c("Female", "Male"), n, TRUE, prob = c(0.45, 0.55)),
    alpha_dunn45_deg  = round(alpha_true + stats::rnorm(n, 0, 3), 1),
    alpha_frogleg_deg = round(alpha_true + 4 + stats::rnorm(n, 0, 3), 1),
    torsion_ct_deg    = round(torsion_ct, 1),
    torsion_budin_deg = round(2 + 0.8 * torsion_ct + stats::rnorm(n, 0, 3.8), 1),
    crossover_sign    = stats::rbinom(n, 1, 0.3)
  )
}
```

- [ ] **Step 3: Codebook, generate.R, .gitignore, README**

Add to `codebooks()`'s list:

```r
    hip_preservation_imaging = cb(
      "hip_id", "Hip ID", "id", "", "", "One row per hip assessed for hip-preservation surgery",
      "age", "Age", "integer", "years", "18..45", "",
      "sex", "Sex", "categorical", "", "Female|Male", "",
      "alpha_dunn45_deg", "Alpha angle, Dunn 45-degree view", "numeric", "degrees", "20..100", "",
      "alpha_frogleg_deg", "Alpha angle, frog-leg lateral view", "numeric", "degrees", "20..100", "Same hip as the Dunn view",
      "torsion_ct_deg", "Femoral torsion on CT", "numeric", "degrees", "-25..55", "",
      "torsion_budin_deg", "Femoral torsion on the modified Budin view", "numeric", "degrees", "-25..55", "",
      "crossover_sign", "Crossover sign on the AP pelvis", "binary", "", "0|1", "1 = present"
    )
```

`data-raw/generate.R`: `write_tidy(make_hip_imaging(), "data/hip_preservation_imaging.csv")`. `.gitignore`: `!/data/hip_preservation_imaging.csv`, `!/data/codebooks/hip_preservation_imaging.csv`. `data/README.md` row:

```markdown
| `hip_preservation_imaging.csv` | hip (80) | joint preservation: a paired t test (two views), correlation vs agreement (CT vs Budin torsion) |
```

- [ ] **Step 4: Generate and run the tests**

Run:
```bash
Rscript data-raw/generate.R && Rscript data-raw/validate.R && uv run pytest tests/python -q
git status --short data
```

Expected: all pass (seed rule if an effect fails); only the two new files and `CHECKSUMS.md5`.

- [ ] **Step 5: Commit**

```bash
git add data-raw tests .gitignore data
git commit -m "hip_preservation_imaging.csv: 80 synthetic hips; alpha angle on two views, CT vs modified Budin torsion that correlate without agreeing

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 7: Re-render, prove no number moved, full checks

**Files:**
- Modify: `_freeze/**` (re-rendered), `data/README.md` (the `proms_long.csv` row)
- Test: everything

**Interfaces:**
- Consumes: Tasks 1–6.
- Produces: a branch whose site is fresh and fully tested.

- [ ] **Step 1: Update the `proms_long.csv` README row**

In `data/README.md`, the `proms_long.csv` row's "One row per" cell becomes `case × visit (pre-op, 6 wk, 3 mo, 1 yr): HOOS JR / KOOS JR, Oxford Hip Score (THA), VR-12, PROMIS-29+2 physical function`.

- [ ] **Step 2: Re-render every page that reads data**

Run: `just data`
Expected: succeeds (generator, validation, Python data tests, and `quarto render en/foundations|catalog|survival|beyond|report`).

- [ ] **Step 3: Prove no existing number changed**

```bash
uv run python - <<'EOF'
import re, subprocess
# Against main, so the four pages Task 2 re-rendered are compared too.
changed = subprocess.run(["git", "diff", "--name-only", "main", "--", "_freeze"], capture_output=True, text=True).stdout.split()
clock = re.compile(r"^\d{2}:\d{2}:\d{2}$")
gt_id = re.compile(r"[a-z]{10}")
flagged = {}
for path in [p for p in changed if p.endswith(".json")]:
    diff = subprocess.run(["git", "diff", "--word-diff=porcelain", "main", "--", path], capture_output=True, text=True).stdout
    removed = [l[1:] for l in diff.splitlines() if l.startswith("-") and not l.startswith("---")]
    numeric = [t for t in removed if re.search(r"\d", t) and not clock.match(t) and not gt_id.search(t)]
    if numeric:
        flagged[path] = numeric[:12]
for path, tokens in flagged.items():
    print(path, tokens)
print("checked", len(changed), "frozen files;", len(flagged), "with removed numbers")
EOF
```

Expected: `0 with removed numbers`, or only tokens explained by this phase: page code lines that changed in Task 2 (no numbers), printed column lists or counts that grew by `ohs` and `promis_pf`. Record every flagged token and its explanation in the ledger; any other changed number is a bug (a generator's random stream moved): stop and debug.

- [ ] **Step 4: Full checks**

Run: `just test && just check`
Expected: all pass, including `test_freshness` and lychee.

- [ ] **Step 5: Commit**

```bash
git add data/README.md _freeze en
git commit -m "Re-render every page from the phase 2a data; no existing number changed

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 8: Pull request (needs Doc's go-ahead)

**Files:** none (GitHub only).

**Interfaces:**
- Consumes: Task 7's branch.
- Produces: a PR `sp2-broaden-examples` → `main`.

- [ ] **Step 1: Ask Doc**

Ask: "Push `sp2-broaden-examples` and open a pull request into `main`? Merging it later publishes the new data files on the live site's repository (pages don't change in this phase except the discharge wording on pages 5, 11, 12 and 15)." Only on a yes:

```bash
git push -u origin sp2-broaden-examples
cat > "${TMPDIR:-/tmp}/sp2a-pr.md" <<'BODY'
Phase 2a of sub-project 2 (design: `docs/superpowers/specs/2026-10-06-hfr-sp2-broaden-examples-design.md`): the data the next two phases teach from. No existing number changes.

- New synthetic datasets, each with a seeded generator, a codebook, tests for every built-in effect, and byte-for-byte reproducibility: `hip_fracture.csv` (trauma), `foot_ankle_rct.csv` + `foot_ankle_rct_long.csv` (cast vs boot, EFAS score), `acl_cohort.csv` (sports), `hip_preservation_imaging.csv` (joint preservation).
- `proms_long.csv` gains `promis_pf` (PROMIS-29+2 physical function, VR-12 PCS rescaled) and `ohs` (Oxford Hip Score, THA). VR-12 stays until phase 2c.
- Discharge is now home or to a rehabilitation clinic; pages 5, 11, 12 and 15 use the new label (same numbers).
- Every page re-rendered; a word-level comparison of the frozen results against `main` found no changed number.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
BODY
gh pr create --repo hfr-ortho/stats-formation --base main --head sp2-broaden-examples \
  --title "Sub-project 2, phase 2a: new synthetic datasets for trauma, foot & ankle, sports and joint preservation" \
  --body-file "${TMPDIR:-/tmp}/sp2a-pr.md"
gh pr checks --repo hfr-ortho/stats-formation --watch
```

Expected: the PR exists and its checks pass. Merging is a separate go-ahead (it publishes).
