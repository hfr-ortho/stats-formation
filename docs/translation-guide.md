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
- Instrument names (Oxford Hip Score) and `THA`/`TKA` in code.

## Numbers

Copy every number exactly as the English has it: the decimal point stays a point (`0.86`) and the thousands comma stays (`1,200`), because they sit beside code output and the English Results sentences. Never round, reformat or "fix" a number; if one looks wrong, tell the controller.

## Style (French)

- Swiss Standard French, "vous", plain direct sentences for beginners in statistics and code. Don't render word for word.
- Generic masculine ("patients", "médecins assistants") in tutorial text.
- Non-breaking space (U+00A0) before `%`, `:`, `;`, `?`, `!` and inside `« »`, in translated prose only (never in code, Methods or Results).
- Use the glossary's headings: `Quand l'utiliser`, `Regarder d'abord les données`, `Exécuter le test`, `Lire le résultat`, `Taille d'effet et IC à 95 %`, `Comment le rapporter`; `**La question :**`; callouts `⚠️ Attention :`, `🔀 R ou Python :`, `💡`, `🔍 Sous le capot :`; `Exercices`; `Solution` stays.
- THA/TKA are PTH/PTG in prose; say once per page that the code says `THA`, `TKA`.
- Stubs: a translated page loses "(en préparation)" and its `.coming-soon` callout.

## Page procedure: self-check before you stop

1. `uv run pytest tests/site/test_translations.py tests/site/test_anchors.py -q` passes (code, numbers, Methods/Results, steps, callouts, "vous", engine).
2. Every `{#id}` of the English page is on yours, on the same `##` headings.
3. Search your page for English leftovers: `Watch out`, `R vs Python`, `Under the hood`, `When to use it`.
4. Render the page locally (`quarto render <page>`), commit its `_freeze/` output, and make sure nothing printed to stderr.
