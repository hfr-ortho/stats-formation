# HFR Sub-project 4 (German Translation) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace all 23 German stub pages with full Swiss Standard German translations, keeping every line of code, every output and every number identical to English, with tests that prove it.

**Architecture:** The French work built the machinery: `docs/glossary.csv`, `docs/translation-guide.md` and `tests/site/test_translations.py`. Task 1 extends all three to German and amends the spec. Tasks 2–12 translate page groups by one procedure. Task 13 finishes the home page, search and docs, and Task 14 proves the whole site in a real browser. Each German page runs its own code, so the hidden checks and prose guards run on it too.

**Tech Stack:** Quarto 1.9.37 (knitr engine, R 4.6.0 + Python 3.13 via reticulate, `freeze: auto`); pytest + BeautifulSoup site tests; Node.js for the switcher's tests; lychee; just.

**Spec:** `docs/superpowers/specs/2026-10-06-hfr-stats-formation-design.md` §4.3 and §6. Page conventions: `CLAUDE.md` (rules 2, 3, 6, 7, 11, 13, 21).

## Global Constraints

- Work on branch `sp4-german`, cut from `main` at `e95336b`. Never commit to `main`. No push without Doc's go-ahead.
- **Translate:** prose, headings, callouts, exercises, front-matter `title`, `subtitle` and `description`, and comments in visible code.
- **Keep in English, unchanged:** code, variable names, data, outputs, plot labels inside code, every `> **Methods:**` and `> **Results:**` blockquote, and every hidden chunk (`#| include: false` or `#| echo: false`). Page 18's manuscript (everything the .docx holds, including its `#| fig-cap` and `#| tbl-cap`) stays in English.
- **Same file names, same folders, same fixed IDs.** Every explicit `{#id}` on the English page is on the German page.
- **Numbers** are copied exactly: the decimal point and the thousands comma stay as in English (`0.86`, `1,200`), never `0,86` or `1'200` (spec §6).
- **German style:** Swiss Standard German: "ss", never "ß"; "Sie"; `docs/glossary.csv` decides every listed term. Quotation marks are « » with no inner spaces. A non-breaking space (U+00A0) goes before `%` in translated prose, except in the compound `95%-KI`. Audience: beginners in statistics and code; plain, direct sentences, not a word-for-word rendering of the English.
- **Stub rule 7:** a translated page loses "(in Vorbereitung)" and its `.coming-soon` callout.
- Every page keeps `engine: knitr` and any `toc-depth` or `format` in its front matter.
- No page may name a data protection officer: HFR has none.
- No reviewer's name goes in this public repo.
- "Anterior approach" is "anteriorer Zugang"; never DAA, in any language.
- Commit messages: a plain sentence saying what changed, ending with the attribution line from the session's reminder.

## Review Focus

1. A translator types `0,86` from habit, or `1'200` as Swiss readers write it, and the page disagrees with the output beside it. *Test: `test_translated_prose_quotes_the_same_numbers` over `de` (Task 1), with a rule test that a decimal comma fails.*
2. A "ß" arrives with a German spelling habit or a pasted term. *Test: `test_german_has_no_eszett` (Task 1).*
3. `real-data` uses a loose or German-from-Germany legal name, or brings back a data protection officer. *Tests: `test_german_real_data_uses_the_swiss_law_names`, `test_german_names_no_data_protection_officer` (Task 1), which pass trivially until Task 2 translates the page.*
4. Searching from a German page after translation returns English results, or nothing. *Test: `test_search_index_keeps_only_the_current_language` gains a `de` case (Task 13), and Task 14 checks it in a real browser.*
5. "Solution" becomes "Lösung" (Rule below) and a structure test or the collapsed callout breaks, or an exercise loses its tabset. *Test: `test_translated_page_structure_matches_english` over `de`, with a rule test (Task 1).*

## Rulings (31.10.2026)

- **Review after publishing.** Doc decided this on 31.10.2026, because neither native reviewer uses GitHub. Corrections reach the repo through Doc. Task 1 amends spec §6.
- **Thousands stay as `1,200`,** as in French. A German reader can take that for 1.2, so the German home page says once how numbers are written (Task 13).
- **Gender-fair wording.** The German site already writes "Patientinnen und Patienten" and "Forschungsassistierende", as Swiss public bodies do. Use the pair form or a neutral word (Personen, Studierende, Teilnehmende); turn singular examples into the plural. Compounds stay (Patientendaten, Patientengruppe). No star, colon or capital-I forms. Stiff sentences are a fair cost; a page that reads as Germany-style generic masculine on a Swiss hospital's public site is not.
- **`Solution` becomes `Lösung`.** French could keep the word; German can't. Rule 6 and the guide follow.
- **Swiss usage over German-from-Germany usage:** Spital, Eintritt, Austritt, Rehospitalisation, Resultate, allfällig.
- **Hüft-TP and Knie-TP** (Doc, 31.10.2026), not TEP.
- **Hidden chunks stay byte-identical,** including English comments.

---

### Task 1: Glossary, guide, tests and the spec for German

**Files:**
- Modify: `docs/glossary.csv` (fill `de`), `docs/translation-guide.md`, `tests/site/test_translations.py`, `tests/site/test_getting_started.py` only if a helper is needed, `Justfile`, `CLAUDE.md` (rules 6, 21), `docs/superpowers/specs/2026-10-06-hfr-stats-formation-design.md` §6
- Create (commit): this plan

**Interfaces:**
- Produces: `STEPS[lang]`, `same_as_english(lang)`, `check_pages(check, lang)`, `untranslated_titles(en, tr, allowed=None, lang="fr")`, `step_problems(en, tr, lang="fr")`, and `structure(text)` reading `## Lösung` as `## Solution`. Every page test takes `lang` through `@pytest.mark.parametrize("lang", ["fr", "de"])`, and all of them pass on stubs and start biting as pages arrive.

- [ ] **Step 1: Amend spec §6**

Change the per-page line to: "translate → render → tests; a native speaker reviews the published site and sends corrections to Doc (Doc's decision, 31.10.2026, because the reviewers don't use GitHub)."

- [ ] **Step 2: Fill the glossary's `de` column**

Every row. These choices are fixed:

| English | Deutsch |
|------|------|
| 95% CI; confidence interval | 95%-KI; Konfidenzintervall (KI) |
| effect size | Effektstärke |
| SD; IQR | Standardabweichung (SD); Interquartilsabstand (IQR) |
| p-value; significant | p-Wert; signifikant |
| odds ratio; hazard ratio | Odds Ratio (OR); Hazard Ratio (HR) |
| censored; survival | zensiert; Überleben |
| mixed model; random intercept | gemischtes Modell; zufälliger Achsenabschnitt (Random Intercept) |
| tidy data | aufgeräumte Daten (Tidy Data) |
| resident | Assistenzärztin, Assistenzarzt |
| THA; TKA | Hüft-TP; Knie-TP in prose; `THA`, `TKA` in code (say so once per page) |
| ACL reconstruction; graft | VKB-Rekonstruktion (vorderes Kreuzband); Transplantat |
| BPTB; hamstring | BPTB (Patellarsehne); Hamstrings |
| posterior tibial slope; femoral torsion | posteriorer tibialer Slope; Femurtorsion |
| hip fracture | proximale Femurfraktur (code keeps `hip_fracture`) |
| removable boot; cast | Walker (code keeps `boot`); Gips |
| return to sport | Rückkehr zum Sport |
| length of stay; discharge; admission | Aufenthaltsdauer; Austritt; Eintritt |
| readmission; revision | Rehospitalisation; Revision |
| anterior approach | anteriorer Zugang |
| PROM | PROM (patientenberichtetes Outcome-Mass) |
| Results sentence | Results-Satz |
| foot and ankle | Fuss und Sprunggelenk |

Laws use their official Swiss names: Humanforschungsgesetz (HFG), Humanforschungsverordnung (HFV), Verordnung über klinische Versuche (KlinV), KlinV-Mep, Datenschutzgesetz (DSG). Check each against fedlex.

Headings: `When to use it` → `Wann verwenden`; `Look at the data first` → `Zuerst die Daten ansehen`; `Run it` → `Analyse durchführen`; `Read the output` → `Ausgabe lesen`; `Effect size and 95% CI` → `Effektstärke und 95%-KI`; `How to report it` → `Resultate formulieren`. Callouts: `⚠️ Achtung:`, `🔀 R oder Python:`, `💡`, `🔍 Unter der Haube:`. `**The question:**` → `**Die Frage:**`. `Solution` → `Lösung`. `Exercises` → `Übungen`.

- [ ] **Step 3: Extend `docs/translation-guide.md`**

Add `## Style (German)` and `## False friends and fixed choices (German)`, from this plan's constraints, rulings and Step 4's banned list. Dates: `January 2015` → `Januar 2015`; ordinals: `1st` → `1.`, `25th` → `25.`. In `tests-a-z`, keep each test's English name in the first cell wherever it differs, in italics in parentheses, as in French.

- [ ] **Step 4: Extend `tests/site/test_translations.py`, tests first**

Rule tests (they fail until the code exists):

```python
def test_german_decimal_comma_fails():
    assert number_problems("The mean was 0.86.\n", "Der Mittelwert betrug 0,86.\n")

def test_german_ordinals_and_months_compare_like_english():
    assert number_problems("On January 5, 2015, the 1st visit.\n", "Am 5. Januar 2015, der 1. Besuch.\n") == []

def test_loesung_counts_as_solution_in_structure():
    assert structure("## Solution\n") == structure("## Lösung\n")

def test_du_form_is_caught_but_not_sie():
    assert duzen("Berechne deinen Mittelwert.\n")
    assert duzen("Berechnen Sie Ihren Mittelwert.\n") == []

def test_german_typography_rule():
    assert german_typography_problems("Es sind 12 % der Fälle.\n")        # plain space
    assert german_typography_problems("Das sogenannte „Modell“.\n")       # Germany-style quotes
    assert german_typography_problems("Es sind 12 % im «Modell».\n") == []
    assert german_typography_problems("Das 95%-KI reicht von 1 bis 2.\n") == []
```

Then add `STEPS["de"]` and the Interfaces above, make every page test parametrized, and add:

- `def duzen(tr: str) -> list[str]`: `\b(?:du|dein\w*|dich|dir|euch|euer)\b` (either case) and singular imperatives (`Berechne`, `Schau`, `Öffne`, `Lies`, `Führe`, `Nimm`, `Prüfe`, `Gib`, `Starte`, `Speichere`) in prose, built like `tutoiement()`.
- `def german_typography_problems(tr: str) -> list[str]`: built like `typography_problems()`.
- `test_german_prose_uses_sie`, `test_german_typography`.
- `test_german_has_no_eszett`: no `ß` in any `de/**/*.qmd`, in the `de` column of the glossary, or in `_quarto.yml`.
- `GERMAN_BANNED` and `test_german_banned_terms`, built like `FRENCH_BANNED`: `Sinn machen`, `kontrollieren für`, `Krankenhaus`, `Entlassung`, `Hüftfraktur`, `direkter anteriorer Zugang`, `realisieren`. False friends a pattern can't catch (`eventuell` for eventually, `aktuell` for actual, `konsistent`) go in the guide.
- `test_german_real_data_uses_the_swiss_law_names`: once `de/getting-started/real-data.qmd` isn't a stub, it holds "Humanforschungsgesetz", "KlinV-Mep", "CER-VD" and "BASEC".
- `test_german_names_no_data_protection_officer`: no `Datenschutzbeauftragt` or `Datenschutzberater` in any `de` page.
- `test_german_tests_a_z_is_sorted` and `test_german_report_docx_has_the_same_text_as_english`, the second only once page 18 isn't a stub. `sort_key(row, generic, function_words)` takes the word lists; German `GENERIC` holds Test, Tests, Schätzer, Anpassung, Kurve, Koeffizient; function words der, die, das, des, für, von, nach, und.
- `test_glossary_has_a_term_for_every_row`: no blank `en`, `fr` or `de`.

- [ ] **Step 5: Run them**

Run: `uv run pytest tests/site/test_translations.py -q`
Expected: all pass; German page tests pass with nothing to check.

- [ ] **Step 6: Update `Justfile` and `CLAUDE.md`**

`data` also renders `de/foundations`, `de/catalog`, `de/survival`, `de/beyond`, `de/report`. Rule 6 says the German title is `Lösung`. Rule 21 gains the German test list.

- [ ] **Step 7: Commit**

```bash
git add docs Justfile CLAUDE.md tests
git commit -m "German terms in the glossary and guide, translation tests for German, and native-speaker review after publishing"
```

---

## The page procedure (Tasks 2–12)

For each page in the task, in order:

1. Read `docs/translation-guide.md` and `docs/glossary.csv`.
2. Copy the English `.qmd` over the German stub; translate per the Global Constraints. Change no code, and no text outside what the constraints list.
3. Render: `quarto render de/<path>.qmd`. Expected: "Output created", with no R error (no `check_agree()` or `stopifnot()` failure) and no Python traceback.
4. Read the German against the English: same teaching, same warnings, nothing added or dropped. Every sentence must read as German written for a beginner in Switzerland, not as English in German words.
5. Add any new term to `docs/glossary.csv`.

Then: `uv run pytest tests/site -q`. Expected: all pass, including every test in `test_translations.py`. Commit one page group with `git add de docs/glossary.csv _freeze`, and the message `German: <page names>`.

### Task 2: Choose a test, Tests A–Z, Getting started
`choose-a-test`, `tests-a-z`, `getting-started/setup`, `using-this-site`, `real-data`. Test names in A–Z follow the glossary; keep English aliases readers meet in papers and output. In `real-data`, check every law's name and each article against the German text on fedlex.

### Task 3: Page 1
`foundations/01-tidy-data`

### Task 4: Pages 2–3
`foundations/02-demographics`, `03-distributions`

### Task 5: Pages 4–5
`catalog/04-describe-one-group`, `05-one-group-vs-hypothetical`

### Task 6: Pages 6–7
`catalog/06-two-unpaired-groups`, `07-two-paired-groups`

### Task 7: Pages 8–9
`catalog/08-three-plus-unmatched`, `09-three-plus-matched`

### Task 8: Pages 10–11
`catalog/10-association`, `11-predict-from-one`

### Task 9: Page 12
`catalog/12-predict-from-several`

### Task 10: Pages 13–14
`survival/13-kaplan-meier`, `14-cox-regression`

### Task 11: Pages 15–16
`beyond/15-post-hoc`, `16-mixed-models`

### Task 12: Pages 17–18
`beyond/17-agreement`, `report/18-example-report`. On page 18, translate the teaching text, which sits inside `::: {.content-visible when-format="html"}`. The manuscript stays in English; say so in one German sentence at its top.

---

### Task 13: Home page, search, docs

**Files:**
- Modify: `de/index.qmd`, `lang-switch.html`, `CLAUDE.md`, `_quarto.yml` (German sidebar labels, if the glossary changed them), `tests/site/test_languages.py`, `tests/python/test_lang_switch.py`, spec §4.3's labels (likewise)

**Interfaces:**
- Consumes: Tasks 1–12.

- [ ] **Step 1: Write the failing tests**

```python
def test_german_is_finished(site):
    for page in PAGES:
        assert load_lang("de", page).select_one(".coming-soon") is None, page
    assert "Übersetzung in Arbeit" not in text_of(load_lang("de", "index.html"))
```

In `tests/python/test_lang_switch.py`, `test_search_index_keeps_only_the_current_language` also covers `"de"`.

- [ ] **Step 2: Update `de/index.qmd`**

Replace the "Übersetzung in Arbeit" callout with a sentence in the first paragraph: `Der Code, seine Ausgaben und die Methods- und Results-Sätze bleiben Englisch, wie in einem Artikel: Der Text erklärt alles auf Deutsch. Zahlen stehen wie in der Code-Ausgabe, also mit Dezimalpunkt und mit Komma bei Tausendern.`

- [ ] **Step 3: Search and docs**

Remove `TRANSLATED_LANGS` from `lang-switch.html`, since every language is translated: `filterIndex(entries, lang)`. In `CLAUDE.md`, the opening paragraph and rules 7 and 21 say all three languages are written.

- [ ] **Step 4: Render and test everything**

Run: `just test && just check`
Expected: all pass; lychee 0 errors.

- [ ] **Step 5: Prove the other languages didn't move**

Run: `git diff --stat e95336b -- en fr _freeze/en _freeze/fr`
Expected: nothing.

- [ ] **Step 6: Commit**

```bash
git add de lang-switch.html CLAUDE.md docs _quarto.yml tests _freeze
git commit -m "German is finished: the home page says what stays in English and how numbers are written, search covers every language, and no stub remains"
```

---

### Task 14: Real browser check and cross-page review

**Files:** whatever the review finds.

- [ ] **Step 1: Search in headless Chrome**

Serve `_site` under `/stats-formation/`. Search "Fisher" and "Standardabweichung" from a German page; expected: results, all German. Repeat "Fisher" from English and French; expected: each returns only its own language. Switch language in the middle of a German page; expected: same section.

- [ ] **Step 2: Cross-page review**

One reviewer reads all of `de/` for drift: a glossary term rendered two ways, pair forms that lapse into generic masculine, Germany-style usage, "Results-Satz" variants.

- [ ] **Step 3: Pull request (needs Doc)**

Ask Doc whether to push and open the PR. Merging publishes. The German native-speaker review happens on the published site.
