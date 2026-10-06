# HFR Sub-project 2: Broaden the Examples — Design Addendum

**Date:** 2026-10-06
**Status:** Approved in brainstorming; awaiting written-spec review
**Parent spec:** `docs/superpowers/specs/2026-10-06-hfr-stats-formation-design.md` (§5 outlined
this sub-project; this addendum replaces that outline)
**Language:** English only. Translation (sub-projects 3–4) starts after this lands.

---

## 1. Purpose

A resident, research assistant or master's student in any HFR Ortho team finds worked
examples built on their own kind of data and questions: trauma, sports & arthroscopy,
joint preservation, and foot & ankle, alongside hip and knee arthroplasty.

**Success looks like:** each of the four new areas is the worked example in at least
three pages' sections; arthroplasty stays the backbone (Table 1, implant survival, the
example report); every moved section meets the same standards as today (R and Python side
by side, agreement checks, prose guards, Results sentences that report numbers only); and
every number on a page that didn't move is unchanged.

## 2. Decisions made in brainstorming

| Topic | Decision |
|------|------|
| Approach | **Swap sections** to the dataset whose question is the more natural example (§4). No new pages; no exercise-only variant. |
| Arthroplasty instruments | **Keep HOOS JR and KOOS JR** (what HFR's PROM databank collects). Replace VR-12 with **PROMIS-29+2 physical function**. Add the **Oxford Hip Score** for THA cases. The parent spec's "Oxford scores and EQ-5D-5L instead of HOOS JR/KOOS JR" is withdrawn. |
| Foot & ankle instrument | **EFAS score** (European Foot and Ankle Society; 6 items scored 0–4, total 0–24, higher is better), as in HFR's databank. Not FAOS. |
| Length of stay | Unchanged (it feeds nine pages); only the discharge labels change. |
| Phases | 2a data, 2b pages 4–8, 2c pages 9–12 and 15–17. Each phase is its own plan and pull request and goes live when merged. |

## 3. Data

All four new datasets are synthetic, modelled loosely on HFR Ortho research lines
(orthogeriatric hip fracture care, the Chopart immobilization RCT, slope-reducing
osteotomy after failed ACL reconstruction, cam morphology and femoral torsion). Each has a
generator `data-raw/R/gen_<name>.R` whose seed is the default argument of its `make_*()`
function, a codebook in `data/codebooks/`, an entry in `codebooks()`, a line in
`data-raw/generate.R`, an allow-list line in `.gitignore`, R tests in
`tests/testthat/test-data-<name>.R` and Python checks in `tests/python/test_data_files.py`.
`write_checksums()` picks the new CSVs up automatically. Each generator uses its own seed,
so no existing dataset changes.

### 3.1 `hip_fracture.csv` (trauma)

One row per patient, about 400 patients aged 65 and over, most over 80.

| Variable | Notes |
|------|------|
| `patient_id` | `H0001` … |
| `age`, `sex`, `asa` | age 65–100 (the codebook notes that real data would group ages ≥ 90) |
| `dementia` | 0/1 |
| `residence` | `home` / `nursing home` |
| `fracture_type` | `femoral neck` / `trochanteric` |
| `treatment` | `hemiarthroplasty` / `nail` / `screws` |
| `hours_to_surgery` | right-skewed; about 85% within 48 hours |
| `surgery_within_48h` | 0/1, derived |
| `los_days` | |
| `death_30d` | 0/1 |
| `followup_days`, `died` | follow-up to death or censoring at 1 year |

### 3.2 `foot_ankle_rct.csv` and `foot_ankle_rct_long.csv` (foot & ankle)

A two-arm RCT of immobilization after a midfoot (Chopart) injury: cast vs removable boot,
about 120 patients randomized 1:1.

- **Wide** (one row per patient): `patient_id` (`F001` …), `arm` (`cast` / `boot`), `age`,
  `sex`, `union_3mo` (0/1).
- **Long** (one row per patient × visit): `patient_id`, `arm`, `visit` (`6wk` / `3mo` /
  `6mo` / `12mo`), `visit_days`, `efas` (0–24, higher is better), `pain_nrs` (0–10, an
  integer). Missed visits rise from about 5% at 6 weeks to about 15% at 12 months.

### 3.3 `acl_cohort.csv` (sports & arthroscopy)

One row per primary ACL reconstruction, about 350.

| Variable | Notes |
|------|------|
| `case_id` | `A0001` … |
| `age`, `sex` | age 15–50 |
| `graft` | `BPTB` / `hamstring` / `quadriceps` |
| `tibial_slope_deg` | posterior tibial slope, about 6–16° |
| `tegner_preinjury` | 0–10 |
| `rts_12mo` | returned to pre-injury sport at 12 months, 0/1 |
| `followup_years`, `graft_failure` | follow-up to graft failure or censoring (up to about 6 years) |
| `failure_2y` | graft failure within 2 years, 0/1 (everyone is followed at least 2 years unless the graft fails), for page 6's Fisher test |

### 3.4 `hip_preservation_imaging.csv` (joint preservation)

One row per hip, about 80 hips in young adults assessed for hip preservation surgery.

`hip_id`, `age`, `sex`, `alpha_dunn45_deg` and `alpha_frogleg_deg` (alpha angle on two
views of the same hip), `torsion_ct_deg` and `torsion_budin_deg` (femoral torsion on CT and
on the modified Budin view), `crossover_sign` (0/1).

### 3.5 Arthroplasty changes (`proms_long.csv`, `cohort.csv`)

- **`promis_pf`**: PROMIS-29+2 physical function T-score, made from the same random draws
  as `vr12_pcs` and rescaled, so no other column changes. During phases 2a–2b both exist;
  phase 2c drops `vr12_pcs` and `vr12_mcs`.
- **`ohs`**: Oxford Hip Score (0–48, higher is better) for THA cases at every visit, blank
  for TKA, drawn from its own seed after everything else, so every existing value is
  unchanged.
- **`discharge`**: `home` / `rehabilitation clinic` (was `home` / `facility`). Labels only.

### 3.6 Built-in effects

`data-raw/validate.R` asserts each one after every regeneration (TJS spec §5.4).

| Dataset | Effect | Teaches | Assertion |
|------|------|------|------|
| hip fracture | 30-day mortality about 7% | proportion, binomial | 5% ≤ rate ≤ 10% |
| hip fracture | about 85% operated within 48 h | binomial vs a 90% target | 80% ≤ share ≤ 89% |
| hip fracture | death rises with hours to surgery and with age | logistic regression | OR per 24 h > 1 with p < 0.05; OR for age > 1 |
| hip fracture | time to surgery right-skewed | describing skewed data | skewness > 1 |
| foot & ankle | boot better EFAS at 3 months | unpaired t | difference 2–4 points, Welch p < 0.01 |
| foot & ankle | boot less pain at 6 weeks | Mann-Whitney | p < 0.05 |
| foot & ankle | arms converge by 12 months | group × time in mixed models | EFAS difference at 12 months < 1 point; interaction p < 0.01 |
| foot & ankle | EFAS rises over time in the boot arm | Friedman | p < 0.001 |
| ACL | graft failure by 2 years unrelated to hamstring vs BPTB | a true null (keeps page 6's lesson) | Fisher p > 0.2 |
| ACL | failure hazard rises with tibial slope | Cox | HR per degree 1.10–1.35, p < 0.05 |
| ACL | return to sport differs by graft | chi-square | p < 0.05 |
| ACL | return to sport rises with Tegner, falls with age | multiple logistic | Tegner OR > 1 and age OR < 1, both p < 0.05 |
| imaging | Dunn 45° alpha angle about 4° above the frog-leg view (the Dunn view profiles the anterosuperior head-neck junction; corrected at the phase 2a review) | paired t | mean difference 3–5°, p < 0.001 |
| imaging | CT and Budin torsion correlate but disagree, more so at high torsion | Pearson; correlation is not agreement | r 0.80–0.92; slope of difference on mean p < 0.05 |
| arthroplasty | PROMIS PF improves before surgery → 1 year | paired tests, mixed models | paired p < 0.001 (inherited from the VR-12 draws) |
| arthroplasty | Oxford Hip Score ceiling at 1 year; tracks HOOS JR | median (IQR), ceilings | ≥ 10% at 48; Spearman ρ with HOOS JR > 0.7 |

Rates are tuned for teaching (enough events and clear effects), and each codebook says so.

## 4. Section mapping

Anchors, decision-table cells and the TJS page anatomy (spec §6: the question, When to use
it, Look at the data first, Run it, Read the output, Effect size and 95% CI, How to report
it, a ⚠️ box, exercises) are unchanged. Each moved section loads its own data, as every
section does now.

| Phase | Page · section (anchor) | Now | New question |
|------|------|------|------|
| 2b | 4 · `#median-iqr` | KOOS JR at 1 year | What's a typical Oxford Hip Score 1 year after THA, and how much do scores vary? |
| 2b | 4 · `#proportion` | 90-day complications | What proportion of hip-fracture patients died within 30 days? |
| 2b | 5 · `#binomial-test` | readmission vs a US state report | Suppose the target is that 90% of hip-fracture patients are operated within 48 hours. Is our proportion different? |
| 2b | 6 · `#unpaired-t` | BMI, TKA vs THA | Is the EFAS score at 3 months different with a boot than with a cast? |
| 2b | 6 · `#mann-whitney` | KOOS JR, men vs women | Is pain 6 weeks after the injury different with a boot than with a cast? |
| 2b | 6 · `#fisher-chi-square` | readmission by sex | Is graft failure within 2 years more common after a hamstring than a BPTB graft? |
| 2b | 7 · `#paired-t` | VR-12 PCS, before vs 1 year | Do the frog-leg and Dunn 45° views give different alpha angles in the same hips? |
| 2b | 8 · `#chi-square` | complications by surgeon | Does return to sport at 12 months differ between BPTB, hamstring and quadriceps grafts? |
| 2c | 9 · `#repeated-measures-anova` | VR-12 PCS over time | Does physical function (PROMIS-29+2) change over the first year after surgery? |
| 2c | 9 · `#friedman` | KOOS JR at 6 weeks, 3 months, 1 year | With a boot, does the EFAS score keep changing between 6 weeks, 3 months and 12 months? |
| 2c | 10 · `#pearson` | operative time vs BMI | How closely does femoral torsion on the modified Budin view track torsion on CT? |
| 2c | 11 · `#logistic-regression` | complication vs age | Does the risk of death within 30 days rise with the time to surgery? |
| 2c | 11 · `#cox` | revision hazard vs age | Does the hazard of ACL graft failure rise with posterior tibial slope? |
| 2c | 12 · `#multiple-logistic-regression` | complication predictors | Which factors predict return to sport at 12 months? |
| 2c | 15, 16 (VR-12 passages) | VR-12 PCS | PROMIS-29+2 physical function |
| 2c | 16 · `#group-by-time` | KOOS JR in knees, men vs women × visit (an interaction with no clear evidence) | Does the boot's advantage in EFAS score change over the year (boot vs cast × visit)? A clear interaction; the section's warning about reading interactions stays, now illustrated by the arms converging at 12 months |
| 2c | 17 | knee alignment | Same `radiographic_reliability.csv`, reframed as osteotomy planning (HKA, MPTA, LDFA) |

Coverage: trauma on pages 4, 5, 11; foot & ankle on 6, 9, 16; sports on 6, 8, 11, 12;
joint preservation on 7, 10, 17.

**Also in each phase:** the page introductions that list examples (such as page 6's "THA vs
TKA, men vs women, implant A vs implant C"), the exercises of every moved section (on the
section's new dataset), and page 3's worked examples that point readers to table cells
(phase 2c).

**Stays arthroplasty:** Table 1 (page 2), every other catalog section, the implant
comparisons and survivorship (pages 6 `#log-rank`, 8 `#cox`, 13, 14), and page 18.

**Content fixes carried from sub-project 1's review (phase 2b):** page 1's "MRN-to-study-ID
crosswalk" becomes the code key / study code wording of the template; the real-data page's
"HFR Ortho's private GitHub organization" becomes "a private repository in HFR Ortho's
GitHub organization"; "Pick your language once" on page 0.2 says it means R or Python.

## 5. Phases

| Phase | Ships | Every existing number |
|------|------|------|
| **2a data** | The four generators, codebooks, tests and effects (§3); `promis_pf`, `ohs`, the discharge labels; `.gitignore` allow-list; `just data` | unchanged (pages re-render only for their data stamps) |
| **2b pages 4–8** | §4's eight 2b sections, their exercises, page introductions, the carried content fixes | unchanged outside the moved sections |
| **2c pages 9–12, 15–17** | §4's 2c sections; PROMIS replaces VR-12 everywhere; page 17's framing; page 3's examples; drop `vr12_pcs`/`vr12_mcs` | unchanged outside the moved sections and the VR-12 passages |

Plans: phase 2a's plan is written after this addendum is approved; 2b's and 2c's after 2a
merges, because their numbers come from the generated data.

## 6. Testing

- **Data:** per dataset, testthat checks structure, allowed values and ranges, missingness,
  privacy (no name- or MRN-shaped values), byte-for-byte reproducibility, and every §3.6
  effect; Python checks the files, codebooks and allow-list.
- **Pages:** every moved section passes the existing source and site tests (knitr engine,
  language tabs, hidden agreement checks, prose guards, Results conventions, catalog
  anatomy, quiet pages). Site tests that pinned a moved section's arthroplasty content are
  rewritten for the new example, never deleted.
- **Unchanged numbers:** after each phase, frozen results of pages and sections that didn't
  move are compared word by word against the previous commit, ignoring clock times and
  gt's random table IDs, as in sub-project 1.
- **Phase 2c:** a test that no page reads `vr12_pcs` or `vr12_mcs`.

## 7. Risks

| Risk | Mitigation |
|------|------|
| Tuning four generators so every effect holds | Prototype each `make_*()` with `validate.R` before committing a seed; never change a seed or loosen an assertion to pass a test (CLAUDE.md rule 9) |
| Moved sections lose quality | Each moved section is rewritten against the same anatomy and conventions, with the same tests, and reviewed phase by phase |
| R and Python disagree on a new model (for example the EFAS mixed model) | The existing `check_agree()` conventions and documented tolerances (CLAUDE.md rules 16–18) |
| Every phase goes live on merge | Each phase is a complete, consistent site on its own |

## 8. Out of scope

- New pages or a subspecialty case-study part.
- Swiss length of stay.
- Hand surgery, spine, shoulder or paediatric examples.
- Translation; the sub-project 1 review items about the switcher, accessibility, the ß test
  and heading IDs (they belong to the preparation for sub-project 3).
