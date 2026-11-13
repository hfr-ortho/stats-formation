# "Report an error" link on every page: design

Date: 13.11.2026. Size: a small change (one script, one config line, a few styles, three prose edits, tests).

## Intent

Doc presents the site to the HFR Ortho learners on Monday 16.11.2026. He wants every page to give them a quick way to report typos and wrong or confusing wording. Most learners have no GitHub account, so the existing "Report an issue" link (Quarto's `repo-actions: [issue]`, a blank GitHub issue form) does not serve them.

## Goals

- Every page in `en/`, `de/` and `fr/` carries a "Report an error" link in the page's language.
- Clicking it opens an email to `josephmichael.schwab@h-fr.ch` that already names the page, the section and any text the learner highlighted. The learner only types what is wrong.
- No account, no outside service. Works on phones.
- Merged and deployed before 16.11.2026.

## Non-goals

- No web form, back end, tracking or analytics.
- No prefilled GitHub issues or issue templates. The existing GitHub link stays as it is.
- No per-paragraph buttons and no pop-up on text selection.

## Anti-goals

- Editing page sources across the site. That would re-run R and Python on every page and change all of `_freeze/` days before the presentation.
- A page that reads worse or breaks when JavaScript is off or the script fails. Without the script the page simply has no email link.
- Anything sent without the learner pressing Send in their own mail app.

## Constraints

- Only whole-project renders use the freeze, and CI never runs R or Python (golden rule 5). The change must render from the existing freeze, except for the three pages whose prose changes.
- Translations change prose only; the three languages keep the same structure (golden rule 21).
- The address is readable in the public source and on a public page. Doc chose his own HFR address knowing this.
- An email link does nothing on a computer with no mail app set up (webmail only), so the address must also appear as plain text somewhere.

## Approaches

1. **One shared script, loaded on every page (chosen by Doc).** A file next to `lang-switch.html`, added to `include-after-body`. No page source changes, no code re-runs, testable in Node like the language switcher. Costs: the labels for the three languages live in the script, and it needs JavaScript, which the site already relies on.
2. **Quarto's `other-links` in each language's `_metadata.yml`, plus a smaller script.** Works as a plain email link without JavaScript, but Quarto places it under the table of contents, the spot that is easy to miss today.
3. **A line in every page's source.** Edits 72 pages and re-runs all of them. Ruled out by the first anti-goal.

## Design

Decided by Doc: prefilled email, approach 1, the address above. The rest are Claude's calls, shown to Doc on 13.11.2026.

**File.** `report-error.html` at the repo root, holding `<script id="report-error">`. `_quarto.yml` lists it after `lang-switch.html` under `include-after-body`. It does not depend on names defined in `lang-switch.html`. It does nothing on the root redirect page.

**Where the link appears.**

- Under "On this page" in the right column, as the first entry of Quarto's `.toc-actions` list, above "Report an issue", with an envelope icon.
- At the end of the page text, above the previous/next links, as one muted line. Phone readers see this one.
- Quarto writes its `.toc-actions` list a second time in the page footer (shown on phones and on pages with no table of contents). The link is the first entry there too, so it appears wherever "Report an issue" does. Added during the build, 13.11.2026.

**Wording.** Native reviewers correct these on the published site like any other text.

| | Right column | End of page | Prompt in the email |
|---|---|---|---|
| en | Report an error | Found a mistake on this page? Report it by email. | What is wrong or confusing: |
| de | Fehler melden | Einen Fehler auf dieser Seite gefunden? Melden Sie ihn per E-Mail. | Was ist falsch oder unklar: |
| fr | Signaler une erreur | Vous avez trouvé une erreur sur cette page ? Signalez-la par e-mail. | Ce qui est faux ou confus : |

**The email.**

```
To:      josephmichael.schwab@h-fr.ch
Subject: HFR Ortho Stats: en/catalog/06-two-unpaired-groups

Page: https://hfr-ortho.github.io/stats-formation/en/catalog/06-two-unpaired-groups.html#mann-whitney
Highlighted text: "…"

What is wrong or confusing:
```

- The subject prefix is the same in every language, so one mail rule catches every report.
- The section is the one that holds the highlighted text; without a highlight, the address's current `#section`; otherwise none.
- Highlighted text has its whitespace collapsed and is cut to 300 characters with an ellipsis. The line is left out when nothing is highlighted.
- The "Page" and "Highlighted text" labels and the prompt follow the page's language; an unknown language falls back to English.

**"Getting help" in `getting-started/using-this-site.qmd`, all three languages.** The first bullet becomes, in English:

> Something on this site is wrong or confusing? Click **Report an error** on that page. It opens an email that already names the page; highlight the sentence first and it is included. No mail app on this computer? Write to josephmichael.schwab@h-fr.ch. With a GitHub account you can [open an issue](https://github.com/hfr-ortho/stats-formation/issues) instead.

German and French follow `docs/glossary.csv` and `docs/translation-guide.md`.

**Tests.**

- `tests/python/test_report_error.py`, in Node like `test_lang_switch.py`: subject and body for each language, the section rules, the 300-character cut, encoding of quotes, accents and line breaks, the English fallback.
- `tests/site/test_languages.py`: every built page includes `id="report-error"`; each language's "How to use this site" shows the address.
- By hand in `just preview`, as for the language switcher: both placements in all three languages, light and dark theme, phone width, and a click with and without highlighted text in at least Chrome and Safari.

**Docs.** A short entry in `CLAUDE.md` (what the file does, where the wording lives, that it must stay out of page sources).

## Left to the builder

- How to keep the highlighted text when the click clears the selection (for example remembering the last non-empty selection inside `main`).
- The exact insertion points in Quarto's HTML, including pages with `toc: false`, and the styles in `styles.css` for both themes.
- French and German typography in the labels (non-breaking spaces before `?` and `:` as the translation guide requires).
- Re-rendering: a whole-project render, committing whatever changes in `_freeze/` for the three edited pages, then `just check`.
- Work on a new branch from `main` (`sp4-german` is already merged and identical to `main`).
