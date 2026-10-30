# Translation guide

For translating an English page into French (sub-project 3) or German (sub-project 4). Terms come from `docs/glossary.csv` (columns `en,de,fr,notes`); if a term isn't there, add a row before you use it.

## Translate

- Prose, headings, callout titles and bodies, exercises, link text.
- Front-matter `title`, `subtitle` and `description`.
- Comments in visible code (`# the mean` only; the code on the same line is untouched).
- Alt text and captions written in prose. Figure and table captions inside code chunks (`#| fig-cap`) stay English.

## Keep in English, unchanged

- All code, variable names, file names, data, package names, plot labels set inside code, and printed output.
- Every `> **Methods:**` and `> **Results:**` blockquote, including exercise answers. Page 18's manuscript (everything the .docx holds) stays English.
- Every hidden chunk (`#| include: false` or `#| echo: false`), byte for byte, comments included.
- Chunk options, fenced-div attributes, and every explicit `{#id}`. The page keeps its file name, its folder, `engine: knitr`, `toc-depth` and `format`.
- Instrument names (Oxford Hip Score, KOOS JR) and `THA`/`TKA` in code.
- Display code blocks (` ```bash `, ` ```powershell `, ` ```python `, ` ```r `) are identical except for comments. A `{mermaid}` diagram keeps its ids and arrows; its node and edge labels are prose and translate.
- The two results sentences that carry no **Results:** label (`en/foundations/03-distributions.qmd` after "TKA patients had a higher BMI", and `en/getting-started/using-this-site.qmd` after "KOOS JR at 1 year was a median") stay in English too.
- Headings and bold leads must differ from the English ones (`## R`, `## Python`, `## Solution`, and names such as Windows or Kaplan-Meier excepted). Page 18's manuscript headings stay English; everything outside its `.content-visible when-format="html"` blocks is byte-identical to the English page.
- The `:::` fence lines (including `collapse="true"` and `group="language"`), the `## R` / `## Python` / `## Solution` headings and the position of every chunk match the English page.

## Numbers

Copy every number exactly as the English has it: the decimal point stays a point (`0.86`) and the thousands comma stays (`1,200`), because they sit beside code output and the English Results sentences. Never round, reformat or "fix" a number; if one looks wrong, tell the controller.

- Keep numbers in the English order within a paragraph. The test compares each paragraph's numbers in sequence, with their sign and any leading `<`, `>`, `≤` or `≥` (`p < 0.05` is not `p > 0.05`; `−2` is not `2`). Keep the English paragraph breaks too: a list item, a heading and a table row each count as a paragraph.
- Dates: month names translate (`January 2015` becomes `janvier 2015`); the day and the year stay. Ordinals keep their digits: `1st` becomes `1er`, `25th` becomes `25e`.
- Inline code (`like this`) is compared span by span, in order: copy it exactly.
- Numbers in visible code comments must match the English, in order.

## Style (French)

- Swiss Standard French, "vous", plain direct sentences for beginners in statistics and code. Don't render word for word.
- Generic masculine ("patients", "médecins assistants") in tutorial text.
- Non-breaking space (U+00A0) before `%`, `:`, `;`, `?`, `!` and inside `« »`, in translated prose only (never in code, Methods or Results).
- Use the glossary's headings: `Quand l'utiliser`, `Regarder d'abord les données`, `Exécuter l'analyse`, `Lire le résultat`, `Taille d'effet et IC à 95 %`, `Rédiger les résultats`; `**La question :**`; callouts `⚠️ Attention :`, `🔀 R ou Python :`, `💡`, `🔍 Sous le capot :`; `Exercices`; `Solution` stays.
- THA/TKA are PTH/PTG in prose; say once per page that the code says `THA`, `TKA`.
- Stubs: a translated page loses "(en préparation)" and its `.coming-soon` callout.

## Page procedure: self-check before you stop

1. `uv run pytest tests/site/test_translations.py tests/site/test_anchors.py -q` passes (code, numbers, Methods/Results, page 18, structure, steps, headings, "vous", engine).
2. Every `{#id}` of the English page is on yours, on the same `##` headings.
3. Search your page for English leftovers: `Watch out`, `R vs Python`, `Under the hood`, `When to use it`. Never write `tu`, `ton`, `ta`, `tes`, `te`, `toi` or a singular imperative (`Regarde`, `Calcule`).
4. Render the page locally (`quarto render <page>`), commit its `_freeze/` output, and make sure nothing printed to stderr.
