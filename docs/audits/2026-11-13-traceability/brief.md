# Audit brief: can a reader trace every result on the page?

## The site and its readers

`/Users/docschwab/repos/hfr-ortho/stats-formation` is a public Quarto website that teaches statistics to orthopaedic residents, research assistants and medical students who are beginners in both statistics and code. Every analysis is shown in R and Python side by side. Read `CLAUDE.md` at the repo root first: it explains how pages are built (language tabsets, hidden agreement checks, the hidden `# Prose guard` chunk at the end of each page, Methods/Results blockquotes, collapsed exercise solutions).

You audit only the English pages you were assigned. This is a read-only audit: do not edit, create or delete anything in the repository, and do not render (`quarto render`, `just render`, `just check` are off limits). Write only to the findings file named in your task.

## The rule the owner wants

> Any time results are presented, we should either calculate them for the reader or tie them back directly to test output that shows them. A little more explanation, and clearer explanation, is better than leaving people to guess.

## The example that started this

Page 6, section `#mann-whitney`, said: "Of all 3,364 (boot, cast) pairs, the boot patient reported less pain in 61%, more in 25%, and 14% were tied." The figures are correct, but no visible code on the page produces them. They were computed only in the hidden `# Prose guard` chunk at the bottom of the source (`pain_diffs <- outer(...)`, then `stopifnot(... == c(61, 25, 14))`). The printed output gives U = 1074.5 and r = −0.361, which cannot be turned back into the three percentages. A careful reader could not find where the numbers came from. (This one is already being fixed; do not report it.)

## What to look for

Go through each assigned page from top to bottom. For every number or result quoted in prose (teaching text, "Read the output" bullets, callouts, Methods and Results blockquotes, exercise questions and the text inside collapsed Solutions), decide which of these it is:

1. **Shown:** a visible chunk on the page prints it, at the precision the prose quotes or one that plainly rounds to it. Fine; no finding.
2. **Derived, with the derivation shown:** the prose says how to get it from printed output (for example "58 × 58 = 3,364 pairs"). Fine.
3. **Untraceable (severity A):** no visible output shows it and the prose gives no derivation. Typical causes: it is computed only in a hidden chunk (`#| include: false`, `#| echo: false`, the agreement checks, the `# Prose guard`), or it needs a calculation the page never shows. The Prose guard is a good index: each `stopifnot()` item names a number the prose quotes, and an item computed from an object the visible code never prints is a candidate.
4. **Traceable only with an unexplained step (severity B):** the output shows it under another name or scale (R prints "W", the prose says "U"); it is rounded or transformed without saying so; it appears in only one language's output although both tabs are shown; the reader must combine two outputs or do arithmetic that is not spelled out; or a printed value that matters is never mentioned in "Read the output".
5. **Wrong (severity ERROR):** the prose contradicts the output. Report these first.

Also report **unclear explanations (severity C)** where a beginner would have to guess: a term used before it is explained, a leap in reasoning, a piece of output shown but never explained, R and Python outputs that visibly differ with no explanation, a sentence that is hard to follow. Report only the ones that would really stop a beginner; a few well-chosen C findings per page beat a long list.

Out of scope: typos, style preferences, translations, page design, the choice of statistical methods. If you happen to see a factual or statistical error, report it as ERROR.

## How to check

- Page source: `en/<folder>/<page>.qmd`. Line numbers in your findings refer to this file.
- What the page actually prints: the executed page, with every chunk's output, is stored in `_freeze/en/<folder>/<page>/execute-results/html.json` under `["result"]["markdown"]`. Dump it to a text file in your scratch folder and read it, for example:
  `python3 -c "import json,sys; print(json.load(open(sys.argv[1]))['result']['markdown'])" _freeze/en/catalog/06-two-unpaired-groups/execute-results/html.json > <scratch>/06.md`
  Hidden chunks leave no output there, so if a number is not in that text, the reader does not see it. Do not use `_site/`: it may be mid-rebuild.
- Before you call a number untraceable, search the dumped output for it in the forms it could take (`0.36`, `-0.361`, `36%`, `.361`). Before you call it traceable, find the output line. Quote that line in the finding when it helps.
- Tables and figures count as output. A number readable from a printed table is shown; a number that has to be read off a plot by eye is not.
- You may run small read-only R or Python snippets from the repo root to confirm what a number is (`Rscript -e '...'`, `uv run python -c '...'`), reading `data/`. Never write into the repo.

## Proposed fixes

For each finding propose the smallest fix that satisfies the rule, concretely enough to apply:

- Prefer showing the calculation: the visible code lines to add, in **both** R and Python (R tab first), using the objects the section already defines, in the page's style (short lines, a comment on each line that explains it in plain words).
- Where the number is already in the output, propose the sentence that ties the prose to it ("the `estimate` line", "the `RBC` column").
- Keep to the project rules in `CLAUDE.md`: Results blockquotes report numbers only, no interpretation; each catalog section must stand alone; ranges use "to"; any random step is seeded.
- Say whether the fix changes code. A fix that changes code must be copied identically into the German and French pages, and all three pages re-run, so it costs more than a prose-only fix.

## Findings file format

Write your findings to the file named in your task, as markdown, most severe first within each page:

```
## <page file name>

### <NN>-<k> · <short title> · <ERROR|A|B|C>
- **Where:** `en/<folder>/<page>.qmd:<line>`, section `#<anchor>`, step "<step heading>"
- **Text:** "<the sentence or phrase, quoted>"
- **Problem:** <what the reader cannot trace or understand, in one or two sentences>
- **Where it really comes from:** <hidden chunk at line N / output line "..." / not computed anywhere>
- **Proposed fix:** <the sentence and/or the R and Python lines to add>
- **Changes code:** yes | no
```

`<NN>` is the page number (01 to 18; use `gs`, `home`, `choose`, `az` for unnumbered pages) and `<k>` counts findings on that page from 1.

End the file with a short `## Pages with nothing to report` list if any, and a `## Not checked` list for anything you could not verify, with the reason.

## What to send back

Your final message is read by the coordinator, not the site owner. Keep it under 200 words: the path of your findings file, the number of findings per page by severity, and the three findings you consider most important, by ID with one line each. Nothing else.
