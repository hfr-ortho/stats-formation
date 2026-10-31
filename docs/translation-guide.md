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
- The `:::` fence lines (including `collapse="true"` and `group="language"`), the `## R` / `## Python` / `## Solution` headings (`## Lösung` in German) and the position of every chunk match the English page.

## Numbers

Copy every number exactly as the English has it: the decimal point stays a point (`0.86`) and the thousands comma stays (`1,200`), because they sit beside code output and the English Results sentences. Never round, reformat or "fix" a number; if one looks wrong, tell the controller.

- Keep numbers in the English order within a paragraph. The test compares each paragraph's numbers in sequence, with their sign and any leading `<`, `>`, `≤` or `≥` (`p < 0.05` is not `p > 0.05`; `−2` is not `2`). Keep the English paragraph breaks too: a list item, a heading and a table row each count as a paragraph.
- Dates: month names translate (`January 2015` becomes `janvier 2015`); the day and the year stay. Ordinals keep their digits: `1st` becomes `1er`, `25th` becomes `25e`.
  In German: `January 2015` becomes `Januar 2015`, `1st` becomes `1.`, `25th` becomes `25.`.
- Inline code (`like this`) is compared span by span, in order: copy it exactly.
- Numbers in visible code comments must match the English, in order.

## Style (French)

- Swiss Standard French, "vous", plain direct sentences for beginners in statistics and code. Don't render word for word.
- Generic masculine ("patients", "médecins assistants") in tutorial text.
- Non-breaking space (U+00A0) before `%`, `:`, `;`, `?`, `!` and inside `« »`, in translated prose only (never in code, Methods or Results).
- Use the glossary's headings: `Quand l'utiliser`, `Regarder d'abord les données`, `Exécuter l'analyse`, `Lire le résultat`, `Taille d'effet et IC à 95 %`, `Rédiger les résultats`; `**La question :**`; callouts `⚠️ Attention :`, `🔀 R ou Python :`, `💡`, `🔍 Sous le capot :`; `Exercices`; `Solution` stays.
- THA/TKA are PTH/PTG in prose; say once per page that the code says `THA`, `TKA`.
- Stubs: a translated page loses "(en préparation)" and its `.coming-soon` callout.

## Style (German)

- Swiss Standard German: "ss", never "ß" (Mass, gross, Grösse, Fuss, schliesslich, ausserdem). "Sie" and "Ihr", never "du". Plain, direct sentences for beginners in statistics and code; don't render word for word.
- Gender-fair wording: the pair form ("Patientinnen und Patienten", "Assistenzärztinnen und Assistenzärzte") or a neutral word (Personen, Studierende, Teilnehmende, Forschungsassistierende). Turn singular examples into the plural. Compounds stay (Patientendaten, Patientengruppe). No star, colon or capital-I forms.
- Swiss usage over German-from-Germany usage: Spital, Eintritt, Austritt, Rehospitalisation, Resultate, allfällig.
- Quotation marks are « » with no inner spaces, never „ “. A non-breaking space (U+00A0) goes before `%` in translated prose, except in the compound `95%-KI`. Never in code, Methods or Results.
- Use the glossary's headings: `Wann verwenden`, `Zuerst die Daten ansehen`, `Analyse durchführen`, `Ausgabe lesen`, `Effektstärke und 95%-KI`, `Resultate formulieren`; `**Die Frage:**`; callouts `⚠️ Achtung:`, `🔀 R oder Python:`, `💡`, `🔍 Unter der Haube:`; `Übungen`; the solution callout is titled `Lösung` and the tabset heading is `## Lösung` (the structure test reads it as `## Solution`).
- THA and TKA are Hüft-TP and Knie-TP in prose; say once per page that the code says `THA`, `TKA`.
- Laws use their official Swiss names: Humanforschungsgesetz (HFG), Humanforschungsverordnung (HFV), Verordnung über klinische Versuche (KlinV), KlinV-Mep, Datenschutzgesetz (DSG). HFR has no data protection officer: name none.
- In `tests-a-z`, keep each test's English name in the first cell wherever it differs, in italics in parentheses: "t-Test für gepaarte Stichproben (*paired t test*)". The table is sorted by the distinctive name (Fisher under F, "t-Test für gepaarte Stichproben" under t).
- Stubs: a translated page loses "(in Vorbereitung)" and its `.coming-soon` callout.

## False friends and fixed choices (German)

- Never "Sinn machen": write "Sinn ergeben" ("das ergibt Sinn").
- Never "kontrollieren für": write "adjustiert für" or "unter Berücksichtigung von".
- Never "Krankenhaus" (write "Spital"), "Entlassung" (write "Austritt"), "Hüftfraktur" (write "proximale Femurfraktur"), "realisieren" for to realize (write "erkennen", "merken").
- Never "direkter anteriorer Zugang" or an abbreviation of it: it is "anteriorer Zugang".
- "eventuell" means possibly, not eventually ("schliesslich", "am Ende"); "aktuell" means current, not actual ("tatsächlich"); "konsistent" is for consistent in the sense of firm, not consistent with ("übereinstimmend", "stimmig").
- "signifikant" is reserved for statistical significance. A clinical meaning is "relevant" or "bedeutsam".
- A "Hüft-TP" is a total hip arthroplasty; the code and data say `THA`.
- Numbers keep the English decimal point (`0.86`) and thousands comma (`1,200`), never `0,86` or `1'200`.
- Fixed terms: `Results-Satz` (the sentence after **Results:**), `Eintritt` (admission), `Austritt` (discharge), `Kontrolle` for a visit (`Studienvisite` for the trial on pages 6, 9, 15 and 16, never bare `Visite`), `normalverteilt` for Gaussian, `Hüft-TP`/`Knie-TP`.
- Section names in prose: `im Methodenteil` and `der Resultatteil`, never `Methods-Teil`, `in den Methods`, `in den Methoden` or `Resultate-Abschnitt`. Page 18's manuscript sections stay «Methods und Results».
- The plain-language callout is titled `Einfach erklärt` on every page, never `In einfachen Worten`.
- PROM is masculine (`der PROM`) and the plural is `PROMs`; one value is a `PROM-Score` (`präoperativer PROM-Score`).
- `kontinuierlich` for a continuous variable; `stetig` only as the adverb (steadily).
- Pair forms: Forschungsassistierende, Medizinstudierende, beurteilende Person (plural Beurteilende), Assistenzärztinnen und Assistenzärzte.
- In "Ausgabe lesen", a term the output prints stays bold and verbatim (`95% CI 64.8 to 66.3`); a derived label is German (`95%-KI für den Median 41 bis 43`).
- Gloss at first use, once per page (a test checks KI: `Konfidenzintervall` must appear on every page whose prose uses KI): KI, SD, IQR, HR, OR, PROM, HOOS JR, KOOS JR. The glossary rows give the German form.
- Fedlex's German text decides every law name; the glossary holds the names the project uses.

## False friends and fixed choices (French)

- Never "évidence" for evidence: write "preuve" ("pas de preuve claire").
- Never "valider" for commit: write "faire un commit" ("tout ce qui entre dans un commit").
- Never "détails" for details: write "informations" ("informations sur le patient").
- Never "éventuellement", "consistant", "supporter", "adresser" or "réaliser que" in their English senses (possibly, consistent, to support, to address, to realize).
- "dépôt" only for a repository. A submission (ethics) is a "soumission".
- "significatif" is reserved for statistical significance. A clinical meaning is "important" or "pertinent", and a trivial difference is "négligeable", never "insignifiant".
- "centre" means a hospital: a distribution's center is its "moyenne" or "position".
- "effectif" means the number of subjects, not a count of anything ("un comptage" for a count of days).
- "groupé" means pooled ("regroupé"); clustered data are "en grappes".
- In "Lire le résultat" bullets, name a printed term exactly as the output prints it, in bold, then explain it in French (**mean = 65.5 ans :** la moyenne…).
- A "primary" arthroplasty is "primaire", never "première" (prothèse articulaire primaire).
- Practice data and files are "d'exercice", never "d'entraînement". A PROM takes no plural -s.
- Ethics: "autorisation" and "demande d'autorisation" (LRH, ORH), not "approbation" or "demande d'éthique".
- In `tests-a-z`, keep each test's English name in the first cell wherever it differs from the French, in italics in parentheses: "Test t pour échantillons appariés (*paired t test*)".
- Glosses of abbreviations and instrument names at first use (IC, PROM, HOOS JR, KOOS JR, LCA, IMC) are allowed even though the English doesn't spell them out.
- "the test that X" is never "le test selon lequel X" (that says the test asserts X): write "le test de l'hypothèse que X".
- "ajuster" is for fitting a model ("ajuster un modèle") and for "ajusté sur"; what a variable is modeled by is "modéliser … par" ("modélisez le délai par une spline").
- "the practice's data" and "practice data" are data to practice on: "données d'exercice", never "du cabinet". A clinic ("the practice records it") is "le service".
- A graft's type or tissue is "greffon" (type de greffon, greffon aux ischio-jambiers); the procedure and its failure are "greffe" (échec de la greffe).
- Translate only what the English page says; don't bring in detail from the design spec (the trial's injury is "lésion du médio-pied", not a specific named injury).
- "chez" is for people ("chez les patients"); for things, use "pour" ("pour les prothèses"), never "chez les prothèses".
- "par chance" means luckily; "by chance" is "par hasard".

## Page procedure: self-check before you stop

1. `uv run pytest tests/site/test_translations.py tests/site/test_anchors.py -q` passes (code, numbers, Methods/Results, page 18, structure, steps, headings, "vous", engine).
2. Every `{#id}` of the English page is on yours, on the same `##` headings.
3. Search your page for English leftovers: `Watch out`, `R vs Python`, `Under the hood`, `When to use it`. Never write `tu`, `ton`, `ta`, `tes`, `te`, `toi` or a singular imperative (`Regarde`, `Calcule`).
4. Render the page locally (`quarto render <page>`), commit its `_freeze/` output, and make sure nothing printed to stderr.
