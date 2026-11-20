# Display, usability and setup findings in detail

Part of the [content review of 20.11.2026](README.md).

**What was looked at.** The local build in `_site/` (commit 6949255, the same commit as the live site, whose footer reads "Last updated: 18.11.2026, 17:04"), in the Dia browser at 1,440 and 488 pixels wide, light and dark. The browser extension is not allowed to open the github.io address, so the live site itself was checked only by fetching one page's HTML. The setup page was read step by step by a reviewer acting as a beginner; nothing was installed.

Marks: ✔ = I checked it myself. R = a reviewer checked it and reported how; I did not repeat the check.

---

## Urgency 2: broken for readers now

### U1. Fifteen bullet lists per language display as one run-on paragraph ✔

- **Where:** pages 13 to 18, all three languages (15 in English, 15 in German, 15 in French). Confirmed on the live site.
- **What the reader sees:** "How to read it: - **The steps:** the curve starts at 100%… - **The ticks** mark censored patients… - **The shaded band**…" as a single block of text with literal hyphens. These are the "Reading the output" passages, the most important teaching text on those pages.
- **Cause:** the list starts on the line directly after a paragraph line, with no blank line between. Quarto's Markdown then reads the bullets as a continuation of the paragraph. Example: p13:279 to 282.
- **English locations (rendered pages):** page 13: 5 lists; page 14: 2; page 15: 2; page 16: 2; page 17: 3; page 18: 1.
- **Fix:** a blank line before each list. It is a source change in prose, so each page re-renders. A site test could catch it: no rendered `<p>` should contain " - <strong>".

### U2. The decision table is unusable below about 500 pixels wide ✔

- **Where:** `choose-a-test.html`, at a window 488 pixels wide (the narrowest Dia allows; a phone is about 390, not tested).
- **What the reader sees:** the last column, "Survival time", is squeezed to 31 pixels. Its text breaks one or two letters per line ("K / a / pl / a / n-"), which stretches the rows to 430 and 500 pixels tall. The row "Describe one group" fills most of a screen with white space.
- **Cause:** `styles.css` gives the first column a minimum width of 11 rem and the other columns none; the table scrolls sideways but the columns shrink first.
- **Why it matters:** this page is one of the three entry points on the home page and the tool a resident opens on a phone between cases.
- **Fix (best practice for wide tables on small screens):** give every column a minimum width so the table scrolls sideways instead of collapsing, or below a breakpoint turn each goal into a card listing its four tests.

### U3. The setup page names Positron controls that Positron's documentation doesn't have (R; one check ✔)

- **Where:** `getting-started/setup.qmd` lines 26, 79, 97, 206 ("the language picker at the top right of the Console pane"); line 202 ("Restart R (Session → Restart R)").
- **Positron's documentation** (the "Managing interpreters" page, read through a summarizing fetch ✔): the control is the "Interpreter picker", "located in the top right" of the window; you "choose New Console Session…". Restart is an icon in the Console action bar, or the command "Interpreter: Restart Active Interpreter Session". A "Session" menu is not mentioned; "Session → Restart R" is RStudio's menu.
- **Not known:** I did not look at the Positron window itself. The setup wording was confirmed on a fresh clone on 14.11.2026 according to the last audit, so the picker instruction may work in practice even if the name differs. The "Session → Restart R" row is the more likely real problem.
- **Fix:** use Positron's names and say where on screen; replace the restart instruction.

### U4. The page states no R version; the lockfile, the check script and the step 6 check disagree ✔

- **Facts:** `renv.lock` records R 4.6.0. `scripts/check_setup.R` passes any R from 4.4 and says "install R 4.4 or newer". The setup page states no version. renv's `renv_status_check_version` compares major.minor: with any R other than 4.6.x, `renv::status()` prints "The lockfile was generated with R 4.6.0, but you're using R …" instead of the sentence the page promises at line 87 ("No issues found…").
- **Effect:** today CRAN serves R 4.6.2, so a new install matches. A reader with an older R, and every reader once R 4.7 is out, fails the step 6 check while step 8 says "All good".
- **Not known:** whether the package snapshot has a ready-built package for every locked version under R 4.4, 4.5 or 4.7.
- **Fix:** state "R 4.6" on the page, make the check script agree, add the "lockfile was generated with R…" message to Troubleshooting.

### U5. What a beginner is not told before starting (R)

Measured on this Mac by the reviewer:

| Component | Size |
|---|---|
| Positron | 881 MB download, 2.3 GB installed |
| Apple Command Line Tools (for Git) | 1.3 GB installed |
| R packages (215) | 649 MB |
| Python 3.13 and 46 packages | about 420 MB |
| R, repository | about 280 MB |
| **Total** | **about 5 GB** |

- The page says "30–45 minutes". The reviewer's estimate for a true beginner on a private Mac, when nothing fails, is 60 to 90 minutes. That is a judgment, not a measurement.
- Not on the page (searched): disk space, administrator rights, what to do on an HFR-managed PC, proxy or certificate errors, macOS 14 or newer for the current Apple silicon R installer.
- **No route without Git.** The page offers no "Download ZIP", and doesn't say that no GitHub account is needed. Step 3 on a Mac installs 1.3 GB of tools for one `git clone`. The reviewer confirmed the ZIP address returns 200 and that the environment files are tracked; the ZIP route was **not** tested end to end.
- **No route for R only or Python only**, although the page tells readers to pick one language.
- **Step 5:** the reader isn't told where `~/projects` is in Positron's Open Folder dialog (the home folder on a Mac, `C:\Users\<name>` on Windows). The reviewer rates this as the step most likely to stop a beginner.
- **Step 4:** Positron's Windows download offers user or system install and x64 or ARM64, with no recommendation on the page.
- **Step 8:** the R check prints an unexplained three-line "Registered S3 method overwritten by 'lme4'" message mid-list (seen on this Mac).
- **Troubleshooting:** "Anything else → your project lead" gives a reader without a project lead no contact.
- **Not tested at all:** Windows, a hospital-managed PC, a fresh Mac. Whether PowerShell's script policy, `mkdir -p`, or `Rscript` on PATH work on an HFR PC is unknown.

### U6. Git is introduced as a download tool, but the real-data page expects commits (R)

`setup.qmd` says Git "keeps track of changes". No English page contains `git add`, `commit`, `pull` or `push`. Nothing says how to update the local copy when the site changes. `real-data.qmd` lines 79 to 88 expect the trainee to stage and commit safely.

### U7. No figure has a text alternative ✔

- **Facts:** no `.qmd` in `en/` sets `fig-alt` (searched: 0). On the rendered pages the figures have no `alt` attribute (page 6: 0 of 7; page 13: 0 of 6).
- **Why it matters:** a screen-reader user gets nothing from any plot, and the site teaches "look at the data first". WCAG 2 success criterion 1.1.1 (level A) requires a text alternative for informative images.
- **Fix:** `#| fig-alt:` on each plot chunk, one sentence saying what the plot shows. It is a chunk option, so pages re-render; the alt text needs translating.

---

## Urgency 3: design and usability improvements

### U8. Lines of text are about 140 characters long on a laptop screen ✔

Measured on page 6 at a 1,440-pixel window: the text column is 905 pixels wide at 17 pixels, about 140 characters per line. Typographic guidance puts comfortable reading at roughly 45 to 90 characters; WCAG 2 criterion 1.4.8 (level AAA) sets a maximum of 80. Long lines make dense explanatory prose harder to track, and these pages are dense. Fix: cap the prose column (for example `max-width: 75ch` on paragraphs and lists) and let code blocks, outputs and tables keep the full width.

### U9. Inside a catalog section the reader has no map ✔

Catalog pages set `toc-depth: 2`, so the right-hand list shows only the four or five tests. Page 6 is 25 screens tall with 28 third-level headings that repeat the same seven steps per test. Within a test, nothing shows which step you are on or how many remain. Options: show the current section's steps in the right-hand list (depth 3, collapsed to the active section), or put a one-line step bar at the top of each test section. The fixed step order itself is a strength and should stay.

### U10. The sixty R-against-Python boxes are always open ✔

There are 60 "🔀 R vs Python" boxes in `en/`, none collapsed. They explain differences between two languages to readers who were told to pick one. For a beginner in one language they are extra material of exactly the kind the coherence principle in multimedia learning (Mayer) says to remove or defer. Option: collapse them by default, like the "Under the hood" boxes, and keep open only the few that change what the reader must type (Welch against Student, `np.std`).

### U11. The glossary is one 30-screen list with no index ✔

215 entries, no letter index, no filter, an empty right-hand list. A reader who arrives from the sidebar (not from a tooltip) has to scroll or use the browser's find. Fix: letter headings (which also fill the right-hand list) or a filter box.

### U12. Tooltips on touch screens: not tested

The glossary tooltips appear on hover or keyboard focus (confirmed on hover ✔). On a phone or tablet there is no hover. Whether a tap shows the definition, or just follows the link to the glossary page and loses the reader's place, was not tested. There are about 100 term links per page, so this decides how the pages feel on a phone.

### U13. Many dotted underlines

A typical "When to use it" bullet has four to six dotted-underlined terms; page 14 has 149 term links. The rule "first use in a section" is already applied. This is a judgment call: the tooltips are useful, and the density makes ordinary links (solid underline) harder to pick out. If you want fewer, link a term once per page for the 30 or so most basic terms (mean, median, SD, CI, p-value).

### U14. Smaller display points

- **Mobile sidebar** ✔: at 488 pixels the slide-out menu clips long page titles ("5 · Compare one group to a hypoth") instead of wrapping.
- **Flowchart on page 3** ✔: 13 boxes drawn at about 11.5 pixels effective text size on a laptop; smaller on a phone. No text alternative.
- **R and Python plots differ** (R): Python Kaplan-Meier plots start the y-axis near 0.6 to 0.72 where R's start at 0%; on page 8 the Python plot's axis labels are clipped. On page 3, R orders the three panels alphabetically while the text and Python use age, length of stay, PROM.
- **Tests A–Z in English** (R): sorted by first word; see accuracy.md, small points.
- **Home page** ✔: the first card says "First time here? Set up R, Python and the practice data", which steers readers who only want to read toward a 5 GB install. The "Just want to read?" note is on the setup page, one click too late.
- **RStudio link** (R): `posit.co/download/rstudio-desktop/` now lands on the RStudio User Guide, not a download page.
- **Excel example on the setup page** (R): the Python block at lines 164 to 166 uses `pd` without importing it.

## What works well and should be protected

- Consistent, calm visual design; code, output and prose are clearly separated; dark mode works, with plots kept on white.
- The language tabs remember the choice across pages.
- Search works and groups hits by page and section.
- Every page has "Report an error" and previous/next links.
- All 158 distinct external links on the English pages resolved on 20.11.2026 (lychee; 51 through redirects).
- The home page's three cards map to the three ways people arrive.

## The real-data page: claims for an expert to confirm

I did not judge any legal or HFR-policy statement. The reviewer listed the claims on `getting-started/real-data.qmd` that rest on Swiss law or HFR policy and cite no source on the page (line numbers of the English file):

- 10: patient data never in any git repository, private ones included.
- 17: the HRA names; approval "before anyone touches the data"; CER-VD as the committee for HFR; every project gets a BASEC number; trials fall under ClinO, device trials under ClinO-MD.
- 18: health data as sensitive personal data; Fribourg cantonal data protection law applies to HFR.
- 24, 64: HFR studies use coded data; the key holder is named in the ethics application and isn't involved in the project.
- 26: the definitions of "coded" and "anonymous".
- 30: general consent; who may be included in a retrospective study.
- 34 to 53: the list of direct identifiers; the coarsening rules; where "90 or older" comes from.
- 60 to 65: the secure environment; Tresorit; REDCap; what may leave.
- 77: an "HFR-approved" AI tool.
- 95: who decides whether an incident is reported.

Doc decided several of these himself on 31.10.2026 and 14.11.2026. The list is here so they can be ticked off, not because any is known to be wrong.

**Practical gaps a trainee still has after reading it (R):** no order of steps; no contact other than "your project lead"; no route to REDCap, Tresorit or the GitHub organization; no way to check a patient's general-consent status; no links to BASEC, CER-VD or the laws; the page puts exports on HFR-managed drives while the setup page says network drives break Git and the environments, and neither says where to run the analysis.
