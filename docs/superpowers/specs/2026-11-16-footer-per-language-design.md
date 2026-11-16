# Footer in the page's language: design

Approved by Doc on 16.11.2026. A small change.

## Intent

The footer showed all three languages at once ("Synthetic data only · Nur synthetische Daten · Données synthétiques uniquement"). A reader has chosen one language and should see the footer in that language only.

## Goals, non-goals, anti-goals

- Goal: every page shows the three footer parts (synthetic data, last updated, credit and licenses) in its own language.
- Goal: the credit and licenses, until now English only, are translated too.
- Non-goal: changing what the footer says, or Quarto's own "Report an issue" entry, which Quarto already translates.
- Anti-goal: editing page sources. That would re-run R and Python on every page (golden rule 5).
- Anti-goal: a footer in the wrong language when JavaScript is off or slow.

## Constraints

- Quarto 1.9.37 reads `page-footer` from `_quarto.yml` only (`websiteConfig("page-footer", …)` in its code), so a language folder's `_metadata.yml` cannot set its own footer.
- Every page already carries its language: `en/`, `de/` and `fr/` set `lang` in `_metadata.yml`, and Quarto writes it to `<html lang="…">`. `tests/site/test_languages.py` checks this.

## Approaches

1. **All three versions in the footer, shown by a style rule (chosen).** Each part holds its text once per language in a span that names the language; `styles.css` hides the spans that don't match `<html lang>`. No script, nothing flashes, no page source changes. Cost: the page's HTML still holds the two hidden versions, and a page whose stylesheet fails to load shows all three run together.
2. **A script that swaps the text**, as `report-error.html` does for its link. German and French pages would show English first, and only English with scripts off. Ruled out by the second anti-goal.
3. **A footer per language folder.** Quarto doesn't read one (see Constraints).

## Design

**Footer** (`page-footer` in `_quarto.yml`). Each of `left`, `center` and `right` is three spans in the order en, de, fr, with nothing outside them:

| | left | center | right |
|---|---|---|---|
| en | Synthetic data only | Last updated: *build time* | Adapted from the TJS Statistics Tutorials · Text CC BY 4.0 · Code MIT |
| de | Nur synthetische Daten | Zuletzt aktualisiert: *build time* | Adaptiert nach den TJS Statistics Tutorials · Text CC BY 4.0 · Code MIT |
| fr | Données synthétiques uniquement | Dernière mise à jour : *build time* | Adapté des TJS Statistics Tutorials · Texte CC BY 4.0 · Code MIT |

The French colon takes a non-breaking space. The German and French credit lines are new and are Claude's wording: native reviewers correct them on the published site like any other text.

**Style rule** (`styles.css`). `.nav-footer span[lang]` is hidden; `html[lang="en"] .nav-footer span[lang="en"]`, and the same for `de` and `fr`, are shown.

**Claude's calls.**

- The build time's fallback, "local build, not published", stays English: it appears only in local renders and the pull-request check, never on the published site.
- The root page, which only sends visitors to a language, is marked English by Quarto and shows the English footer.

**Tests** (`tests/site/test_structure.py`). The footer's shown spans match the table above on one page per language and on the root page; each part holds exactly one span per language and no other text; each language's credit links to TJS; `styles.css` holds the two rules. No test runs a browser, so the style rule was also checked by hand in a headless browser on 16.11.2026 (English, German and French pages, and a French page at phone width).
