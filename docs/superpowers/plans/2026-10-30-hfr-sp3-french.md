# HFR Sub-project 3 (French Translation) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace all 23 French stub pages with full translations of the English site, keeping every line of code, every output and every number identical to English, with tests that prove it.

**Architecture:** Three preparation tasks come first: the glossary and translation tests, the language-switcher and search fixes, and fixed IDs on headings. Then one task per group of pages follows the same procedure. The last task finishes the home page, the docs and the whole-site check. Each French page runs its own code, so the hidden checks and prose guards run on it too.

**Tech Stack:** Quarto 1.9.37 (knitr engine, R 4.6.0 + Python 3.13 via reticulate, `freeze: auto`); pytest + BeautifulSoup site tests; Node.js for the switcher's tests; lychee; just.

**Spec:** `docs/superpowers/specs/2026-10-06-hfr-stats-formation-design.md` §4.3 and §6. Page conventions: `CLAUDE.md` (rules 2, 3, 7, 11, 13, 21).

## Global Constraints

- Work on branch `sp3-french`, cut from `sp2c-pages-9-17` at `2d38506`, because PR #4 isn't merged yet. Never commit to `main`. No push without Doc's go-ahead.
- **Translate:** prose, headings, callouts, exercises, front-matter `title` and `description`, and comments in visible code.
- **Keep in English, unchanged:** code, variable names, data, outputs, plot labels inside code, every `> **Methods:**` and `> **Results:**` blockquote, and every hidden chunk (`#| include: false` or `#| echo: false`). Page 18's manuscript (everything the .docx holds, including its `#| fig-cap` and `#| tbl-cap`) stays in English.
- **Same file names, same folders, same fixed IDs** (`{#mann-whitney}`). Every explicit `{#id}` on the English page is on the French page.
- **Numbers** are copied exactly: the decimal point and the thousands comma stay as in English (`1,200`, `0.86`), because they sit next to code output and English Results sentences (spec §6).
- **French style:** Swiss Standard French; "vous"; `docs/glossary.csv` decides every listed term. Typography: non-breaking space (U+00A0) before `%`, `:`, `;`, `?`, `!` and inside `« »`, in translated prose only. Audience: beginners in statistics and code; plain, direct sentences, not a word-for-word rendering of the English.
- **Stub rule 7:** a translated page loses "(en préparation)" and its `.coming-soon` callout.
- Every page keeps `engine: knitr` and any `toc-depth` or `format` in its front matter.
- Commit messages: a plain sentence saying what changed, ending with the attribution line from the session's reminder.

## Review Focus

1. A reader switches language in the middle of a page and expects to land on the same section. *Test: `test_toc_headings_have_fixed_ids` (Task 3).*
2. A translator touches a line of code while translating a comment, and the French page teaches different code. *Test: `test_translated_code_matches_english` (Task 1).*
3. A number is mistyped in French prose. Prose guards can't see it, because they run on the data. *Test: `test_translated_prose_quotes_the_same_numbers` (Task 1).*
4. English changes after translation (feedback on PR #4), and the French page silently stops matching. *Tests: both of the above fail on the drift.*
5. Searching from a French page returns English results. *Test: `test_search_index_keeps_only_the_current_language` (Task 2).*

## Rulings (30.10.2026)

- **Thousands stay as `1,200`.** Spec §6 settles the decimal point; the thousands comma follows it, so prose matches the code output and the Results sentences beside it.
- **Hidden chunks stay byte-identical,** including English comments. Readers never see them, and it's what makes the prose guards the same as the English ones.
- **Generic masculine for "patients" and "médecins assistants" in tutorial text;** the home page's doublets stay. It keeps beginners' sentences short.
- **The native-speaker review in spec §6 is a human step** and can't be done here. Task 15 ends the work; merging waits for that review.

---

### Task 1: Glossary, translation guide and translation tests

**Files:**
- Create: `docs/glossary.csv`, `docs/translation-guide.md`, `tests/site/test_translations.py`
- Modify: `Justfile` (the `data` recipe), `CLAUDE.md` (rule 21)
- Create (commit): this plan

**Interfaces:**
- Produces: `translated_pages(lang)` in `tests/site/test_translations.py`, yielding `(en_path, tr_path)` for every page without `.coming-soon`. All tests below use it, so they pass on stubs and start biting as pages arrive.

- [ ] **Step 1: Branch and baseline**

```bash
git checkout sp2c-pages-9-17 && git checkout -b sp3-french
```

- [ ] **Step 2: Write `docs/glossary.csv`**

Columns `en,de,fr,notes`; leave `de` blank. At least 120 rows, from a census of the English pages' terms. These French choices are fixed:

| English | Français |
|------|------|
| 95% CI | IC à 95 % (intervalle de confiance) |
| effect size | taille d'effet |
| SD / IQR | écart-type (ET) / intervalle interquartile (IIQ) |
| p-value; significant | valeur p; significatif |
| odds ratio; hazard ratio | odds ratio (OR); hazard ratio (HR) |
| censored; survival | censuré; survie |
| mixed model; random intercept | modèle mixte; intercept aléatoire |
| tidy data | données ordonnées (*tidy data*) |
| prose: resident | médecin assistant |
| THA / TKA | PTH / PTG in prose; `THA`, `TKA` in code (say so once per page) |
| ACL reconstruction; graft | reconstruction du LCA; greffon |
| BPTB; hamstring | os-tendon rotulien-os (BPTB); ischio-jambiers |
| posterior tibial slope; femoral torsion | pente tibiale postérieure; torsion fémorale |
| hip fracture | fracture de la hanche |
| removable boot; cast | botte amovible; plâtre |
| return to sport | retour au sport |
| osteotomy | ostéotomie |
| anterior approach | voie antérieure |
| PROM | PROM (mesure rapportée par le patient) |

Headings: `When to use it` → `Quand l'utiliser`; `Look at the data first` → `Regarder d'abord les données`; `Run it` → `Exécuter l'analyse`; `Read the output` → `Lire le résultat`; `Effect size and 95% CI` → `Taille d'effet et IC à 95 %`; `How to report it` → `Rédiger les résultats`. Callouts: `⚠️ Attention :`, `🔀 R ou Python :`, `💡`, `🔍 Sous le capot :`. `**The question:**` → `**La question :**`. `Solution` stays. `Exercises` → `Exercices`.

- [ ] **Step 3: Write `docs/translation-guide.md`**

One page: this plan's translate and keep lists, the typography rule, and the page procedure's self-check. It's for sub-project 4 too.

- [ ] **Step 4: Write `tests/site/test_translations.py`**

```python
def strip_comments(code: str) -> str
    """Code without comments. Leaves `#` inside quoted strings, and drops trailing spaces and blank lines."""

def chunks(text: str) -> list[tuple[str, list[str], str]]
    """Each executable chunk as (language, its `#|` option lines, its code)."""

def numbers(text: str) -> collections.Counter
    """Number tokens in prose: code blocks, front matter, link targets and {#ids} removed."""
```

Tests, each over `translated_pages("fr")`:

- `test_translated_code_matches_english`: same chunks in the same order; same options; code equal after `strip_comments`. Chunks with `include: false` or `echo: false` are byte-identical.
- `test_translated_prose_quotes_the_same_numbers`: `numbers()` equal, section by section (split on `## ` headings that carry `{#id}`).
- `test_methods_and_results_stay_in_english`: the lines starting `> **Methods:**` or `> **Results:**` are the same, in the same order.
- `test_french_catalog_steps_are_in_order`: on catalog pages, each section's `###` steps follow Step 2's headings, in order, as in the English page.
- `test_french_callouts_use_the_glossary_titles`: no `## ⚠️ Watch out`, `## 🔀 R vs Python`, `## 🔍 Under the hood` or `### When to use it` remains.
- `test_french_prose_uses_vous`: no `\b(tu|ton|ta|tes)\b` in prose.
- `test_no_page_loses_its_engine`: pages with code declare `engine: knitr`.

Plus rule tests on small strings: `test_rule_keeps_hash_inside_strings`, `test_rule_catches_changed_code`, `test_rule_catches_a_changed_number`.

Also add `test_glossary_has_a_french_term_for_every_row` (no blank `en` or `fr`).

- [ ] **Step 5: Run them**

Run: `uv run pytest tests/site/test_translations.py -q`
Expected: the rule tests and the glossary test pass; page tests pass with nothing to check.

- [ ] **Step 6: Update `Justfile` and `CLAUDE.md`**

`data` also renders `fr/foundations`, `fr/catalog`, `fr/survival`, `fr/beyond`, `fr/report`. Rule 21 gains: "`docs/glossary.csv` and `docs/translation-guide.md` decide terms and style; hidden chunks stay byte-identical."

- [ ] **Step 7: Commit**

```bash
git add docs Justfile CLAUDE.md tests/site/test_translations.py
git commit -m "Glossary, translation guide and tests that keep translated pages' code and numbers identical to English"
```

---

### Task 2: Switcher review items and search by language

**Files:**
- Modify: `lang-switch.html`, `_quarto.yml` (navbar `aria-label`s), `tests/python/test_lang_switch.py`, `tests/site/test_languages.py`

**Interfaces:**
- Produces: `filterIndex(entries, lang)` in `lang-switch.html`, returning the search entries whose `href` starts with `lang + "/"`.

- [ ] **Step 1: Write the failing tests**

```python
def test_search_index_keeps_only_the_current_language():
    assert run(['filterIndex([{href: "fr/a.html"}, {href: "en/a.html"}, {href: "index.html"}], "fr")']) == [[{"href": "fr/a.html"}]]
```

In `tests/site/test_languages.py`: `test_language_links_have_accessible_names` (each top-bar `EN`/`DE`/`FR` link has `aria-label` "English", "Deutsch", "Français").

- [ ] **Step 2: Run them to verify they fail**

Run: `uv run pytest tests/python/test_lang_switch.py tests/site/test_languages.py -q`
Expected: FAIL (`filterIndex` isn't defined; no `aria-label`).

- [ ] **Step 3: Implement**

- `filterIndex()`, and wrap `window.fetch` so that a request ending in `search.json` returns only the current language's entries. `lang-switch.html` loads at the end of the body, before `quarto-search.js` fetches on DOMContentLoaded. Skip the wrap at the site root.
- Narrow the link selector to the top bar: `nav.navbar a.nav-link`, so a link in a page's body reading "FR" isn't rewritten.
- Update the links on `hashchange`, so a middle-click after moving to a section keeps it.
- `aria-label`s in `_quarto.yml`.

- [ ] **Step 4: Render and test**

Run: `just check`
Expected: all pass.

- [ ] **Step 5: Check search by hand**

Run `quarto preview`, open `/fr/index.html`, search "Fisher", and confirm only `/fr/` results appear. Record what you saw in the report. If the preview can't be driven, say so.

- [ ] **Step 6: Commit**

```bash
git add lang-switch.html _quarto.yml tests
git commit -m "The language switcher only touches the top bar and follows the section; search shows the current language; language links have accessible names"
```

---

### Task 3: Fixed IDs on every heading in a table of contents

**Files:**
- Modify: every page in `en/` with an unfixed heading at table-of-contents depth; regenerated `_freeze/`
- Modify: `tests/site/test_anchors.py`

**Interfaces:**
- Produces: `{#id}` on every TOC heading, which the translation tasks copy.

- [ ] **Step 1: Write the failing test**

```python
def test_toc_headings_have_fixed_ids():
    """The switcher keeps #section, so every heading a reader can jump to needs the same ID in every language."""
```

For each page in `en/`: read `toc-depth` from the front matter (default 3; `toc: false` means none). Every `##` and `###` at that depth outside code and callouts carries `{#id}`.

- [ ] **Step 2: Run it to verify it fails**

Run: `uv run pytest tests/site/test_anchors.py -q`
Expected: FAIL, listing the pages.

- [ ] **Step 3: Add the IDs**

Short English kebab-case, unique on the page, matching the auto-generated ID where one exists, so that existing links keep working.

- [ ] **Step 4: Render and test**

Run: `just check`
Expected: all pass, and no number on any page changes.

- [ ] **Step 5: Commit**

```bash
git add en tests _freeze
git commit -m "Every heading in a table of contents has a fixed ID, so the language switcher keeps the section"
```

---

## The page procedure (Tasks 4–14)

For each page in the task, in order:

1. Read `docs/translation-guide.md` and `docs/glossary.csv`.
2. Copy the English `.qmd` over the French stub; translate per the Global Constraints. Change no code, and no text outside what the constraints list.
3. Render: `quarto render fr/<path>.qmd`. Expected: "Output created", with no R error (no `check_agree()` or `stopifnot()` failure) and no Python traceback.
4. Read the French aloud in your head against the English: same teaching, same warnings, nothing added or dropped. Every sentence must read as French written for a beginner, not as English in French words.
5. Add any new term to `docs/glossary.csv`.

Then: `uv run pytest tests/site -q`. Expected: all pass, including every test in `test_translations.py`. Commit one page group with `git add fr docs/glossary.csv _freeze`, and the message `French: <page names>`.

### Task 4: Choose a test, Tests A–Z, Getting started
`choose-a-test`, `tests-a-z`, `getting-started/setup`, `using-this-site`, `real-data`. Test names in A–Z follow the glossary; keep English aliases readers meet in papers and output.

### Task 5: Page 1
`foundations/01-tidy-data`

### Task 6: Pages 2–3
`foundations/02-demographics`, `03-distributions`

### Task 7: Pages 4–5
`catalog/04-describe-one-group`, `05-one-group-vs-hypothetical`

### Task 8: Pages 6–7
`catalog/06-two-unpaired-groups`, `07-two-paired-groups`

### Task 9: Pages 8–9
`catalog/08-three-plus-unmatched`, `09-three-plus-matched`

### Task 10: Pages 10–11
`catalog/10-association`, `11-predict-from-one`

### Task 11: Page 12
`catalog/12-predict-from-several`

### Task 12: Pages 13–14
`survival/13-kaplan-meier`, `14-cox-regression`

### Task 13: Pages 15–16
`beyond/15-post-hoc`, `16-mixed-models`

### Task 14: Pages 17–18
`beyond/17-agreement`, `report/18-example-report`. On page 18, translate the teaching text, which sits inside `::: {.content-visible when-format="html"}`. The manuscript stays in English; say so in one French sentence at its top.

---

### Task 15: Home page, docs, whole-site check

**Files:**
- Modify: `fr/index.qmd`, `CLAUDE.md`, `docs/superpowers/specs/2026-10-06-hfr-stats-formation-design.md` (§4.3's labels, if the glossary changed them), `_quarto.yml` (French sidebar labels, likewise), `tests/site/test_languages.py`

**Interfaces:**
- Consumes: Tasks 1–14.

- [ ] **Step 1: Write the failing test**

```python
def test_french_is_finished(site):
    for page in PAGES:
        assert load_lang("fr", page).select_one(".coming-soon") is None, page
    assert "Traduction en cours" not in text_of(load_lang("fr", "index.html"))
```

- [ ] **Step 2: Update `fr/index.qmd`**

Replace the "Traduction en cours" callout with: `Le code, ses sorties et les phrases Methods et Results restent en anglais, comme dans un article : le texte explique tout en français.`

- [ ] **Step 3: Render and test everything**

Run: `just test && just check`
Expected: all pass; lychee 0 errors; `_freeze/` about 14 MB.

- [ ] **Step 4: Prove the English pages didn't move**

Compare `_freeze/en` with `2d38506`, using `docs/superpowers/plans/2026-10-07-hfr-sp2b-pages-4-8.md` Task 7 Step 5's approach. Expected: only the fixed-ID edits from Task 3.

- [ ] **Step 5: Commit**

```bash
git add fr CLAUDE.md docs _quarto.yml tests _freeze
git commit -m "French is finished: the home page says what stays in English, and no stub remains"
```

---

### Task 16: Native-speaker review and pull request (needs Doc)

**Files:** none.

- [ ] **Step 1: Ask Doc** who reviews the French, and whether to open the pull request once PR #4 has merged. Rebase on `main` first: the commits underneath are the same, so it's clean. Merging publishes.
