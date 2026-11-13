# "Report an error" Link Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Every page in `en/`, `de/` and `fr/` carries a "Report an error" link that opens an email to Doc already naming the page, the section and any highlighted text.

**Architecture:** One script file, `report-error.html`, loaded on every page through `include-after-body`, next to `lang-switch.html` and independent of it. Its pure functions build the email address and are tested in Node; a small browser-only block inserts two links and fills them in when clicked. No page source changes except the "Getting help" bullet in `getting-started/using-this-site.qmd`, in three languages.

**Tech Stack:** Quarto 1.9.37 website, plain JavaScript (no build step, no dependencies), pytest (`tests/python` runs the script in Node.js, `tests/site` reads the built `_site/`).

**Spec:** `docs/superpowers/specs/2026-11-13-report-error-design.md`

## Global Constraints

- Reports go to `soft-canoes2@icloud.com`.
- Subject prefix, the same in every language: `HFR Ortho Stats: `.
- Highlighted text: whitespace collapsed, cut to 300 characters with `…`.
- No page source edits other than `getting-started/using-this-site.qmd` in `en/`, `de/`, `fr/`. Nothing else may re-run R or Python.
- Without JavaScript, or if the script fails, the page reads exactly as before.
- No web form, back end, tracking, GitHub issue prefilling, per-paragraph buttons or selection pop-up. Quarto's "Report an issue" link stays.
- The script must do nothing on the root redirect page (`_site/index.html` also loads it).
- French prose and French labels on the page: non-breaking space (U+00A0) before `?`, `:` and `;`. Straight apostrophes in sources, as on the existing French pages.
- German: Swiss Standard German, "Sie", no "ß". French: "vous". "E-Mail" (de), "e-mail" (fr), "ticket" for a GitHub issue (fr), "Issue" (de), as in `docs/glossary.csv` and the existing pages.
- Render locally and commit `_freeze/` (CLAUDE.md golden rule 5). Use `just render`, never `quarto render <page>`.
- Work on a new branch `report-error` from `main`. `sp4-german` is merged and identical to `main`.
- Must be merged and deployed before Monday 16.11.2026. A push to `main` publishes the site (`.github/workflows/publish.yml`), so merging needs Doc's go-ahead.

## Review Focus

1. Highlighted text containing `&`, `?`, `#`, `%`, `+`, `"`, accents or line breaks must arrive in the email unchanged, not cut the email short. (Task 1, `test_special_characters_survive_the_address`)
2. A highlight that is only spaces, or that spans several lines and tabs: the first adds no "Highlighted text" line, the second arrives as one line. (Task 1, `test_selection_is_collapsed_and_cut`, `test_body_leaves_out_an_empty_highlight`)
3. Addresses other than the usual one: a folder address ending in `/`, a local preview with no `/stats-formation/` prefix, and the site root. The first two work; the root gives no link. (Task 1, `test_page_is_read_from_the_address`)
4. A page that lacks one of the two insertion points, and the root page: the script must not throw and must not touch the root page. (Task 2, `test_script_is_idle_on_the_root_page`, `test_script_survives_a_page_without_its_containers`)
5. Text highlighted outside the page text (sidebar, top bar): not sent. Covered by hand in Task 2 step 8, because it needs a real browser selection.

---

### Task 1: The email address builder

**Files:**
- Create: `report-error.html`
- Create: `tests/python/test_report_error.py`
- Commit also: `docs/superpowers/specs/2026-11-13-report-error-design.md`, `docs/superpowers/plans/2026-11-13-report-error.md`

**Interfaces:**
- Produces, as top-level names inside `<script id="report-error">`:
  - `REPORT_TO: string`, `REPORT_PREFIX: string`, `REPORT_MAX: number`
  - `REPORT_TEXT: { en, de, fr }`, each `{ link, question, action, page, highlighted, prompt }`
  - `reportPage(pathname: string) -> { lang: string, page: string } | null`
  - `trimSelection(text: string) -> string`
  - `reportUrl(base: string, sectionId: string, hash: string) -> string`
  - `reportHref(lang: string, page: string, url: string, selection: string) -> string`

- [ ] **Step 1: Create the branch**

```bash
git switch -c report-error main
```

- [ ] **Step 2: Write the failing tests in `tests/python/test_report_error.py`**

Copy the module docstring style, `ROOT`, `NODE`, `pytestmark`, `script()` and `run()` from `tests/python/test_lang_switch.py`, reading `report-error.html` and `<script id="report-error">`. Add this helper and these tests:

```python
from urllib.parse import parse_qs, unquote, urlsplit

PAGE_URL = "https://hfr-ortho.github.io/stats-formation/en/catalog/06-two-unpaired-groups.html#mann-whitney"


def mail(href):
    """The parts of a mailto: address, decoded the way a mail app decodes them."""
    parts = urlsplit(href)
    assert parts.scheme == "mailto"
    assert "+" not in parts.query          # spaces must be %20: mail apps keep a "+" as a plus sign
    fields = {k: unquote(v) for k, v in (pair.split("=", 1) for pair in parts.query.split("&"))}
    return parts.path, fields["subject"], fields["body"]


def href(lang, selection, page="en/catalog/06-two-unpaired-groups", url=PAGE_URL):
    return run([f"reportHref({json.dumps(lang)}, {json.dumps(page)}, {json.dumps(url)}, {json.dumps(selection)})"])[0]


def test_constants_are_the_ones_in_the_spec():
    assert run(["REPORT_TO", "REPORT_PREFIX", "REPORT_MAX"]) == \
        ["soft-canoes2@icloud.com", "HFR Ortho Stats: ", 300]


def test_labels_in_every_language():
    en, de, fr = run(["REPORT_TEXT.en", "REPORT_TEXT.de", "REPORT_TEXT.fr"])
    assert en == {"link": "Report an error", "question": "Found a mistake on this page?",
                  "action": "Report it by email.", "page": "Page", "highlighted": "Highlighted text",
                  "prompt": "What is wrong or confusing:"}
    assert de == {"link": "Fehler melden", "question": "Einen Fehler auf dieser Seite gefunden?",
                  "action": "Melden Sie ihn per E-Mail.", "page": "Seite", "highlighted": "Markierter Text",
                  "prompt": "Was ist falsch oder unklar:"}
    assert fr == {"link": "Signaler une erreur", "question": "Vous avez trouvé une erreur sur cette page\u00a0?",
                  "action": "Signalez-la par e-mail.", "page": "Page", "highlighted": "Texte surligné",
                  "prompt": "Ce qui est faux ou confus\u00a0:"}


def test_page_is_read_from_the_address():
    assert run(['reportPage("/stats-formation/en/catalog/06-two-unpaired-groups.html")',
                'reportPage("/de/catalog/06-two-unpaired-groups.html")',
                'reportPage("/stats-formation/fr/")',
                'reportPage("/stats-formation/fr/index.html")',
                'reportPage("/stats-formation/")',
                'reportPage("/stats-formation/index.html")']) == \
        [{"lang": "en", "page": "en/catalog/06-two-unpaired-groups"},
         {"lang": "de", "page": "de/catalog/06-two-unpaired-groups"},
         {"lang": "fr", "page": "fr/index"},
         {"lang": "fr", "page": "fr/index"},
         None, None]


def test_selection_is_collapsed_and_cut():
    long = "é" * 400
    assert run(['trimSelection("  the mean\\n\\t (SD)   was  ")', 'trimSelection("   \\n ")', 'trimSelection("")',
                f'trimSelection("{long}")', f'trimSelection("{"a" * 300}")']) == \
        ["the mean (SD) was", "", "", "é" * 300 + "…", "a" * 300]


def test_section_comes_from_the_highlight_then_the_address():
    base = "https://hfr-ortho.github.io/stats-formation/en/x.html"
    assert run([f'reportUrl("{base}", "mann-whitney", "#unpaired-t")', f'reportUrl("{base}", "", "#unpaired-t")',
                f'reportUrl("{base}", "", "")']) == [base + "#mann-whitney", base + "#unpaired-t", base]


def test_email_names_the_page_and_the_highlight():
    to, subject, body = mail(href("en", "the mean (SD) was"))
    assert to == "soft-canoes2@icloud.com"
    assert subject == "HFR Ortho Stats: en/catalog/06-two-unpaired-groups"
    assert body == f'Page: {PAGE_URL}\r\nHighlighted text: "the mean (SD) was"\r\n\r\nWhat is wrong or confusing:\r\n'


def test_body_leaves_out_an_empty_highlight():
    for selection in ["", "   \n "]:
        assert mail(href("en", selection))[2] == f"Page: {PAGE_URL}\r\n\r\nWhat is wrong or confusing:\r\n"


def test_body_follows_the_page_language_and_falls_back_to_english():
    assert mail(href("de", "x"))[2] == f'Seite: {PAGE_URL}\r\nMarkierter Text: "x"\r\n\r\nWas ist falsch oder unklar:\r\n'
    assert mail(href("fr", "x"))[2] == \
        f'Page\u00a0: {PAGE_URL}\r\nTexte surligné\u00a0: "x"\r\n\r\nCe qui est faux ou confus\u00a0:\r\n'
    assert mail(href("it", "x"))[2] == mail(href("en", "x"))[2]
    assert mail(href("de", "x"))[1] == "HFR Ortho Stats: en/catalog/06-two-unpaired-groups"   # same prefix everywhere


def test_special_characters_survive_the_address():
    selection = 'p < 0.001 & 95% CI? #1 + "médiane" (IQR)'
    assert f'Highlighted text: "{selection}"' in mail(href("en", selection))[2]


def test_long_highlight_is_cut_in_the_email():
    assert 'Highlighted text: "' + "a" * 300 + '…"' in mail(href("en", "a" * 400))[2]
```

- [ ] **Step 3: Run the tests to see them fail**

Run: `uv run pytest tests/python/test_report_error.py -q`
Expected: every test fails (`report-error.html` does not exist).

- [ ] **Step 4: Write `report-error.html` with the constants and the four functions**

One `<script id="report-error">` element, commented in the style of `lang-switch.html`. It must not use any name defined in `lang-switch.html` (its own language list: `["en", "de", "fr"]`). Decisions the tests pin:

- `reportPage`: the first path segment that is a language starts the page name; drop `.html`; a path ending at the language folder is `<lang>/index`; no language segment gives `null`.
- `reportUrl`: `base + "#" + sectionId` when `sectionId` is non-empty, else `base + hash`.
- `reportHref`: `"mailto:" + REPORT_TO + "?subject=" + encodeURIComponent(…) + "&body=" + encodeURIComponent(…)`. Body lines are joined with `"\r\n"`: the page line, the highlight line (only when `trimSelection(selection)` is non-empty, in straight double quotes), an empty line, the prompt, and a final empty string. A label and its value are joined with `": "` in English and German and with `"\u00a0: "` in French; keep that separator in the script next to the labels, not inside `page`/`highlighted`.
- An unknown `lang` uses the English texts.

- [ ] **Step 5: Run the tests to see them pass**

Run: `uv run pytest tests/python/test_report_error.py tests/python/test_lang_switch.py -q`
Expected: all pass.

- [ ] **Step 6: Commit**

```bash
git add report-error.html tests/python/test_report_error.py docs/superpowers/specs/2026-11-13-report-error-design.md docs/superpowers/plans/2026-11-13-report-error.md
git commit -m "Report an error: build the prefilled email address"
```

---

### Task 2: The two links on every page

**Files:**
- Modify: `report-error.html` (add the browser-only block)
- Modify: `_quarto.yml` (`include-after-body`)
- Modify: `styles.css`
- Modify: `tests/python/test_report_error.py`, `tests/site/test_languages.py`

**Interfaces:**
- Consumes: `reportPage`, `reportUrl`, `reportHref`, `REPORT_TEXT` from Task 1.
- Produces: on every language page, `a.report-error-link` twice: inside `.toc-actions ul` (first `<li>`) and inside `p.report-error` (last child of `main#quarto-document-content`). Task 3's prose names the right-column label.

- [ ] **Step 1: Write the failing tests**

In `tests/python/test_report_error.py` (the `run()` helper takes a `setup` string that runs before the script):

```python
ROOT_PAGE = """
globalThis.window = { location: { pathname: "/stats-formation/index.html", origin: "https://x", hash: "" } };
globalThis.document = new Proxy({}, { get(_, name) { throw new Error("touched document." + String(name)); } });
"""
BARE_PAGE = """
globalThis.window = { location: { pathname: "/stats-formation/en/index.html", origin: "https://x", hash: "" },
                      getSelection: () => null };
globalThis.document = { querySelector: () => null, querySelectorAll: () => [], addEventListener() {},
                        createElement: () => { throw new Error("built a link with nowhere to put it"); } };
"""


def test_script_is_idle_on_the_root_page():
    assert run(["1"], setup=ROOT_PAGE) == [1]


def test_script_survives_a_page_without_its_containers():
    assert run(["1"], setup=BARE_PAGE) == [1]
```

In `tests/site/test_languages.py`, after `test_every_page_includes_the_switcher`:

```python
def test_every_page_includes_the_report_link_script(site):
    pages = sorted(p for p in SITE_ROOT.rglob("*.html") if "site_libs" not in p.parts)
    assert pages
    missing = [str(p.relative_to(SITE_ROOT)) for p in pages if 'id="report-error"' not in p.read_text(encoding="utf-8")]
    assert missing == []
```

- [ ] **Step 2: Run them to see the site test fail**

Run: `uv run pytest tests/python/test_report_error.py -q && uv run pytest tests/site/test_languages.py -q -k report_link`
Expected: the two Node tests pass already (there is no browser block yet; they guard the next step), and the site test fails with every page listed.

- [ ] **Step 3: Add the browser-only block to `report-error.html`**

Wrap it in `if (typeof document !== "undefined")`, as `lang-switch.html` does, and return early when `reportPage(window.location.pathname)` is `null`, before reading anything from `document`.

- Right column: prepend `<li><a class="toc-action report-error-link"><i class="bi bi-envelope"></i>LINK</a></li>` to `document.querySelector(".toc-actions ul")`, the same shape as Quarto's own entry.
- End of page: append `<p class="report-error">QUESTION <a class="report-error-link">ACTION</a></p>` to `document.querySelector("main#quarto-document-content")`.
- Skip either one whose container is missing, and create no element for it.
- Each link's `href` is set once at load with no highlight (so right-click and middle-click work), then set again on `pointerdown` and on `keydown`, reading the selection at that moment. Do not track `selectionchange`: a highlight the reader has since cleared must not be sent.
- A selection counts only when its `anchorNode` lies inside `main#quarto-document-content`. Its section is the `id` of the closest `section[id]` ancestor of that node, or `""`.
- The page address is `reportUrl(window.location.origin + window.location.pathname, sectionId, window.location.hash)`.
- Build elements with `createElement` and `textContent`, not `innerHTML` strings.

- [ ] **Step 4: Load the script on every page**

In `_quarto.yml`, under `format: html:`:

```yaml
    include-after-body:
      - lang-switch.html
      - report-error.html
```

- [ ] **Step 5: Style the end-of-page line in `styles.css`**

```css
/* "Report an error" line at the end of every page (report-error.html) */
.report-error {
  margin-top: 2.5rem;
  font-size: 0.875rem;
  color: var(--bs-secondary-color);
}
```

- [ ] **Step 6: Render and run the tests**

Run: `just render`
Expected: no page re-runs its code (no page source changed); `git status --short _freeze` prints nothing.

Run: `uv run pytest tests/python -q && uv run pytest tests/site -q`
Expected: all pass.

- [ ] **Step 7: Check that nothing but the script changed in a built page**

Run: `grep -c 'id="report-error"' _site/en/index.html _site/de/catalog/06-two-unpaired-groups.html _site/fr/report/18-example-report.html _site/index.html`
Expected: `1` for each file.

- [ ] **Step 8: Check by hand in a browser**

Run: `just preview`, then check and note the result of each line:

- `en/catalog/06-two-unpaired-groups.html`: "Report an error" is the first entry under "On this page", above "Report an issue"; the muted line sits at the end of the text, above the previous/next links. Same on the `de` and `fr` pages with their labels.
- `en/index.html` (no table of contents): both links are present and neither looks out of place.
- The root address: no link, and the redirect to a language still works.
- Light and dark theme: the end-of-page line is readable in both.
- Phone width (browser's responsive mode, 390 px): the end-of-page link is visible.
- Chrome and Safari: highlight a sentence under "Mann-Whitney", click each link: the draft names `…#mann-whitney` and quotes the sentence. Click with nothing highlighted: no "Highlighted text" line.
- Highlight a sidebar entry, click the link: no "Highlighted text" line.
- Highlight a sentence, click elsewhere to clear it, then click the link: no "Highlighted text" line.
- Keyboard: Tab to the link with a sentence highlighted, press Enter: the sentence is quoted.

If a real phone is at hand, try the highlight there too. A phone that drops the highlight on tap is acceptable (the page address still arrives); say so in the task report.

- [ ] **Step 9: Commit**

```bash
git add report-error.html _quarto.yml styles.css tests/python/test_report_error.py tests/site/test_languages.py
git commit -m "Report an error: a link under the table of contents and at the end of every page"
```

---

### Task 3: "Getting help" text and docs

**Files:**
- Modify: `en/getting-started/using-this-site.qmd:145`, `de/getting-started/using-this-site.qmd:145`, `fr/getting-started/using-this-site.qmd:145`
- Modify: `tests/site/test_languages.py`
- Modify: `CLAUDE.md`, `README.md:43`
- Commit also: `_freeze/{en,de,fr}/getting-started/using-this-site/`

**Interfaces:**
- Consumes: the right-column labels from Task 1 (`Report an error`, `Fehler melden`, `Signaler une erreur`).

- [ ] **Step 1: Write the failing test in `tests/site/test_languages.py`**

```python
REPORT_LINK = {"en": "Report an error", "de": "Fehler melden", "fr": "Signaler une erreur"}


def test_getting_help_names_the_report_link_and_the_address(site):
    for lang in LANGS:
        help_text = text_of(load_lang(lang, "getting-started/using-this-site.html").select_one("section#getting-help"))
        assert REPORT_LINK[lang] in help_text, lang
        assert "soft-canoes2@icloud.com" in help_text, lang
        assert "github.com/hfr-ortho/stats-formation/issues" in str(
            load_lang(lang, "getting-started/using-this-site.html").select_one("section#getting-help")), lang
```

- [ ] **Step 2: Run it to see it fail**

Run: `uv run pytest tests/site/test_languages.py -q -k getting_help`
Expected: FAIL on `en` (the label is not in the section).

- [ ] **Step 3: Replace the first "Getting help" bullet in each language**

Exact copy. The French line below already has U+00A0 before each `?` and `;`; check they survive the paste (`tests/site/test_translations.py::test_french_typography` fails on a plain space).

`en`:

```markdown
- Something on this site is wrong or confusing? Click **Report an error** on that page. It opens an email that already names the page; highlight the sentence first and it is included. No mail app on this computer? Write to soft-canoes2@icloud.com. With a GitHub account you can [open an issue](https://github.com/hfr-ortho/stats-formation/issues) instead.
```

`de`:

```markdown
- Etwas auf dieser Website ist falsch oder unklar? Klicken Sie auf der betreffenden Seite auf **Fehler melden**. Es öffnet sich eine E-Mail, in der die Seite schon steht; markieren Sie zuerst den Satz, dann steht auch er darin. Kein E-Mail-Programm auf diesem Computer? Schreiben Sie an soft-canoes2@icloud.com. Mit einem GitHub-Konto können Sie stattdessen [ein Issue eröffnen](https://github.com/hfr-ortho/stats-formation/issues).
```

`fr`:

```markdown
- Quelque chose est faux ou confus sur ce site ? Cliquez sur **Signaler une erreur** sur la page concernée. Un e-mail s'ouvre et indique déjà la page ; surlignez d'abord la phrase et elle y figure aussi. Pas de logiciel de messagerie sur cet ordinateur ? Écrivez à soft-canoes2@icloud.com. Avec un compte GitHub, vous pouvez aussi [ouvrir un ticket](https://github.com/hfr-ortho/stats-formation/issues).
```

- [ ] **Step 4: Document the script**

In `CLAUDE.md`, under "Layout", after the `scripts/` line:

```markdown
- `report-error.html`: the "Report an error" link on every page (spec `docs/superpowers/specs/2026-11-13-report-error-design.md`). Loaded through `include-after-body` with `lang-switch.html`; it opens a prefilled email and sends nothing itself. Its labels for the three languages live in the script, and `getting-started/using-this-site.qmd` quotes the right-column label, so change both together. Never move the link into page sources: that would re-run every page. `tests/python/test_report_error.py` checks the email it builds.
```

In `README.md` line 43, change the first cell to `` `theme/`, `images/`, `lang-switch.html`, `report-error.html` `` and the second to `HFR colours and logo, the language switcher, and the "Report an error" link`.

- [ ] **Step 5: Render and run every check**

Run: `just check`
Expected: only the three `using-this-site` pages re-run their code; all site tests pass, including `tests/site/test_translations.py` (typography, "Sie"/"vous", structure); lychee reports no broken links.

Run: `just test`
Expected: all pass.

Run: `git status --short`
Expected: changes only in the three `.qmd` files, their three `_freeze/…/using-this-site/` folders, `tests/site/test_languages.py`, `CLAUDE.md` and `README.md`. If any other `_freeze/` path changed, stop and find out why before committing.

- [ ] **Step 6: Commit**

```bash
git add en/getting-started/using-this-site.qmd de/getting-started/using-this-site.qmd fr/getting-started/using-this-site.qmd _freeze tests/site/test_languages.py CLAUDE.md README.md
git commit -m "Report an error: Getting help says how to report by email, in three languages"
```

---

## After the last task

Open a pull request from `report-error` to `main` and wait for the `checks` workflow. Merging publishes the site, so merge only on Doc's word, and before Monday 16.11.2026. After the deploy, open one page per language on `https://hfr-ortho.github.io/stats-formation/` and click the link once.
