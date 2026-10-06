# HFR Ortho Statistics Tutorials

Tutorials and worked examples that teach HFR Ortho residents, research assistants and medical students doing their master's thesis how to prepare data and run the statistical analyses used in orthopaedic research, in R, Python, or both. The site is in English, German and French.

**Read the site:** https://hfr-ortho.github.io/stats-formation/

> **All data in this repository are synthetic.** No real patient data is ever committed here, and this repository is public.

Adapted from the [TJS Statistics Tutorials](https://total-joint-specialists.github.io/example-stats-analysis/) (CC BY 4.0).

## What's inside

| Part | Topics |
|------|------|
| Getting started | Installing R, Python, Git and Positron; how to use the site; working safely with real HFR data under Swiss rules |
| 1 · Foundations | Tidy data, Table 1, distributions & choosing a test |
| 2 · Test catalog | Every test in the Motulsky decision table, R and Python side by side |
| 3 · Survival analysis | Kaplan-Meier, competing risks, Cox regression |
| 4 · Beyond the table | Post-hoc tests, mixed models, agreement & reliability |
| 5 · Putting it together | A complete example study report |

## Run the examples

```bash
git clone https://github.com/hfr-ortho/stats-formation.git
cd stats-formation
Rscript -e 'renv::restore()'
uv sync
```

Step-by-step instructions for beginners: [Install & set up](https://hfr-ortho.github.io/stats-formation/en/getting-started/setup.html).

## Repository layout

| Path | What it holds |
|------|------|
| `en/`, `de/`, `fr/` | The site's pages, one folder per language, with the same file names in each |
| `index.qmd` | The site root: sends visitors to their language |
| `data/` | Synthetic datasets and codebooks |
| `templates/` | A data-collection template to copy for real projects |
| `R/` | Site helpers (`check_agree()`) |
| `scripts/` | Setup checks you run on your own computer |
| `theme/`, `images/`, `lang-switch.html` | HFR colours and logo, and the language switcher |
| `tests/` | R (testthat), Python (pytest), and built-site tests |
| `_freeze/` | Saved results of every page's code (committed, so the site builds without R or Python) |
| `scratch/` | Your practice space; git ignores everything in it |
| `docs/superpowers/` | Design specs and implementation plans |

## For maintainers

You'll need R, uv, Quarto 1.9.37, [just](https://github.com/casey/just), and [lychee](https://github.com/lycheeverse/lychee).

```bash
just setup     # renv::restore() + uv sync
just test      # R and Python unit tests
just preview   # live preview while writing
just check     # render, then site tests + link check
```

Render locally and commit `_freeze/`. CI builds the site from `_freeze/` without running R or Python, runs the site checks, and publishes `main` to GitHub Pages.

The TJS repository is the `tjs` remote, fetch-only. To carry a TJS fix over: `git fetch tjs`, then `git cherry-pick <commit>`.

## License

Text, figures and synthetic data: [CC BY 4.0](LICENSE-CONTENT). Code: [MIT](LICENSE). Adapted from the TJS Statistics Tutorials, © 2026 Total Joint Specialists.
