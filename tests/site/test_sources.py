"""Source-level rules for .qmd files (no built site needed)."""

import ast
import builtins
import re

from sitelib import CELL_ANCHORS, LANGS, ROOT, SRC

CONTENT_DIRS = ["getting-started", "foundations", "catalog", "survival", "beyond", "report"]
EXECUTABLE_CHUNK = re.compile(r"^```\{(r|python)[ ,}]", re.MULTILINE)
KNITR = re.compile(r"^engine:\s*knitr\s*$", re.MULTILINE)


def qmd_files():
    files = sorted(ROOT.glob("*.qmd"))   # the site root's language picker
    for lang in LANGS:
        files += sorted((ROOT / lang).glob("*.qmd"))   # each language's home page, test chooser and A–Z index
        for d in CONTENT_DIRS:
            files += sorted((ROOT / lang / d).glob("*.qmd"))
    return files


def front_matter(text: str) -> str:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    return match.group(1) if match else ""


def missing_knitr(text: str) -> bool:
    return bool(EXECUTABLE_CHUNK.search(text)) and not KNITR.search(front_matter(text))


def test_rule_catches_python_page_without_knitr():
    assert missing_knitr("---\ntitle: x\n---\n\n```{python}\nprint(1)\n```\n")


def test_rule_accepts_page_that_declares_knitr():
    assert not missing_knitr("---\ntitle: x\nengine: knitr\n---\n\n```{python}\nprint(1)\n```\n")


def test_rule_ignores_display_only_code():
    assert not missing_knitr("---\ntitle: x\n---\n\n```python\nprint(1)\n```\n")


def test_every_page_with_code_declares_knitr():
    offenders = [str(f.relative_to(ROOT)) for f in qmd_files()
                 if missing_knitr(f.read_text(encoding="utf-8"))]
    assert offenders == [], "Add `engine: knitr` to the front matter of: " + ", ".join(offenders)


CHUNK = re.compile(r"```\{(r|python)\}\n(.*?)\n```", re.DOTALL)


def chunks(text, hidden):
    """(language, code) for each R or Python chunk that is hidden (`#| include: false`
    among its options, in any order) or, with hidden=False, shown on the page."""
    found = []
    for lang, code in CHUNK.findall(text):
        options = []
        for line in code.splitlines():
            if not line.startswith("#|"):
                break
            options.append(line.strip())
        if ("#| include: false" in options) == hidden:
            found.append((lang, code))
    return found


def hidden_chunks(text):
    return chunks(text, hidden=True)


def visible_chunks(text):
    return chunks(text, hidden=False)


def test_chunk_options_can_come_in_any_order():
    text = "```{python}\n#| echo: false\n#| include: false\nchk = 1\n```\n\n```{r}\n#| warning: false\nlibrary(x)\n```\n"
    assert hidden_chunks(text) == [("python", "#| echo: false\n#| include: false\nchk = 1")]
    assert visible_chunks(text) == [("r", "#| warning: false\nlibrary(x)")]


def test_tidy_page_checks_both_answer_keys_in_both_languages():
    """Spec 8.4: page 1's reference solutions must reproduce the answer keys exactly."""
    chunks = hidden_chunks((SRC / "foundations" / "01-tidy-data.qmd").read_text(encoding="utf-8"))
    for key in ["abstraction_workbook_tidy.csv", "survey_items_long.csv"]:
        assert any(lang == "r" and key in code and "stopifnot(isTRUE(all.equal(" in code
                   for lang, code in chunks), f"no hidden R check against {key}"
        assert any(lang == "python" and key in code and "assert_frame_equal" in code
                   for lang, code in chunks), f"no hidden Python check against {key}"


def written_pages(*dirs):
    """Pages in these folders that are no longer "(coming soon)" stubs."""
    for d in dirs:
        for path in sorted((SRC / d).glob("*.qmd")):
            text = path.read_text(encoding="utf-8")
            if "(coming soon)" not in front_matter(text):
                yield f"{d}/{path.name}", text


def test_exercise_solutions_are_executed():
    """Solutions run on every render, so a typo in one can't ship unnoticed."""
    for name, text in written_pages("foundations", "catalog", "survival", "beyond", "report"):
        exercises = text[text.index("## Exercises {#exercises}"):]
        assert "```r\n" not in exercises and "```python\n" not in exercises, name


def test_pages_guard_the_numbers_in_their_prose():
    for name, text in written_pages("foundations", "catalog", "survival", "beyond", "report"):
        chunks = hidden_chunks(text)
        assert any(lang == "r" and "Prose guard" in code and "stopifnot(" in code
                   for lang, code in chunks), name


def section(text, start, end):
    """The source between two markers (tabset "## R" headers make heading-based cuts unreliable)."""
    i = text.index(start)
    return text[i:text.index(end, i)]


def test_recode_cross_tabs_compare_raw_values_with_the_result():
    text = (SRC / "foundations" / "01-tidy-data.qmd").read_text(encoding="utf-8")
    check = section(text, "**3. Cross-tab every recode.**", "**4. Range and logic checks.**")
    assert "left_join(" in check and "merge(" in check
    # Review A11: the comorbidity flags default to 0, so they get a cross-tab too, in both languages.
    for lang, code in visible_chunks(check):
        assert "comorbidities" in code and "sleep_apnea" in code, lang


def test_tidy_recodes_send_unexpected_codes_to_missing():
    text = (SRC / "foundations" / "01-tidy-data.qmd").read_text(encoding="utf-8")
    step5 = section(text, "### Step 5: give every column its real type", "## Reshaping a survey export")
    assert step5.count("case_when(") >= 3      # sex, procedure, side
    assert step5.count("np.select(") >= 2      # procedure, side
    # Review A11: sex matches whole values; a first-letter match turns "Mme" into "Male".
    assert 'regex("^f"' not in step5 and 'regex("^m"' not in step5
    assert '.str[0]' not in step5
    assert '"female"' in step5 and '"male"' in step5


def test_quartile_guard_reads_what_the_libraries_display():
    text = (SRC / "foundations" / "02-demographics.qmd").read_text(encoding="utf-8")
    chunks = hidden_chunks(text)
    assert any(lang == "r" and "table_body" in code and "1 (0–2)" in code for lang, code in chunks)
    assert any(lang == "python" and "1.0 [0.0,1.8]" in code for lang, code in chunks)


# ---- reticulate: never assign to _ ---------------------------------------
# reticulate decides whether to print a statement's value by looking at Python's
# last value, `_`. Code that assigns `_` itself (`_ = ax.hist(...)`) hides
# reticulate's placeholder, and once `_` holds a plot object every later Python
# output on the page is silently dropped. Name the result instead.

PYTHON_CHUNK = re.compile(r"```\{python[^}]*\}\n(.*?)\n```", re.DOTALL)
ASSIGNMENT_TARGET = re.compile(r"^([^=#\n]*?)(?<![=!<>])=(?!=)", re.MULTILINE)
UNDERSCORE_NAME = re.compile(r"(?<![\w.])_(?!\w)")


def assigns_underscore(text):
    return any(UNDERSCORE_NAME.search(target)
               for code in PYTHON_CHUNK.findall(text)
               for target in ASSIGNMENT_TARGET.findall(code))


def test_rule_catches_underscore_assignments():
    assert assigns_underscore("```{python}\n_ = ax.hist(x)\nplt.show()\n```")
    assert assigns_underscore("```{python}\nstat, _ = f(x)\n```")


def test_rule_allows_named_results_and_keyword_arguments():
    assert not assigns_underscore("```{python}\nqq = stats.probplot(x, plot=ax)\nmax_iter = 5\n```")
    assert not assigns_underscore("```{python}\nax.hist(x, bins=30)\n```")


def test_no_python_chunk_assigns_to_underscore():
    offenders = [str(f.relative_to(ROOT)) for f in qmd_files() if assigns_underscore(f.read_text(encoding="utf-8"))]
    assert offenders == [], "Name the result instead of assigning to _ in: " + ", ".join(offenders)


# ---- catalog sections ------------------------------------------------------

CELL_HEADING = re.compile(r"^## .*\{#([a-z0-9-]+)\}\s*$", re.MULTILINE)


def cell_sections(page, text):
    """(anchor, source) for each decision-table cell section of one catalog page, skipping
    other sections such as "Which groups differ?" and the exercises."""
    marks = list(CELL_HEADING.finditer(text))
    for mark, following in zip(marks, marks[1:] + [None]):
        if mark.group(1) in CELL_ANCHORS[page]:
            yield mark.group(1), text[mark.end():following.start() if following else len(text)]


def catalog_sections():
    """(page, anchor, source) for every decision-table section of the written catalog pages."""
    for name, text in written_pages("catalog"):
        for anchor, body in cell_sections(name.replace(".qmd", ".html"), text):
            yield name, anchor, body


def test_cell_sections_skip_sections_that_are_not_table_cells():
    text = "## Cox regression {#cox}\nA\n## Which groups differ? {#which-groups-differ}\nB\n## Exercises {#exercises}\nC\n"
    assert [a for a, _ in cell_sections("catalog/08-three-plus-unmatched.html", text)] == ["cox"]


def test_each_catalog_section_loads_its_own_packages_and_data():
    """Readers arrive from the decision table straight at a section and copy its code."""
    for name, anchor, body in catalog_sections():
        first = {}
        for lang, code in visible_chunks(body):
            first.setdefault(lang, code)
        assert "library(" in first["r"] and 'read_csv("data/' in first["r"], f"{name}#{anchor}: first R block"
        assert "import " in first["python"] and 'read_csv("data/' in first["python"], f"{name}#{anchor}: first Python block"


def test_every_catalog_section_checks_r_against_python():
    for name, anchor, body in catalog_sections():
        hidden = hidden_chunks(body)
        r_checks = sum(lang == "r" and "check_agree(" in code for lang, code in hidden)
        py_values = sum(lang == "python" and "chk = " in code for lang, code in hidden)
        assert r_checks >= 1 and r_checks == py_values, f"{name}#{anchor}: {r_checks} R checks, {py_values} Python chk"


def test_free_form_pages_check_r_against_python():
    """Free-form pages have no cell sections, so count the whole page's checks."""
    for name, text in written_pages("survival", "beyond", "report"):
        hidden = hidden_chunks(text)
        r_checks = sum(lang == "r" and "check_agree(" in code for lang, code in hidden)
        py_values = sum(lang == "python" and "chk = " in code for lang, code in hidden)
        assert r_checks >= 5 and r_checks == py_values, f"{name}: {r_checks} R checks, {py_values} Python chk"


def test_beyond_hidden_checks_reuse_the_printed_results():
    """A hidden check that recomputes its own value can't notice a change in the visible code (Phase 5 review)."""
    for name, text in written_pages("beyond"):
        hidden = "\n".join(code for lang, code in hidden_chunks(text) if "Prose guard" not in code)
        for fresh_call in ["t.test(", "marginal_means(", "1 - 0.95"]:
            assert fresh_call not in hidden, f"{name}: hidden check calls {fresh_call}"


def test_report_hidden_checks_reuse_the_printed_results():
    text = dict(written_pages("report"))["report/18-example-report.qmd"]
    hidden = "\n".join(code for lang, code in hidden_chunks(text) if "Prose guard" not in code)
    for fresh_call in ["t.test(", "hedges_g(", "quantile(", "tidy_survfit(", "qth_survival_times(", "summarise("]:
        assert fresh_call not in hidden, f"hidden check calls {fresh_call}"


def test_beyond_prose_guards_pin_numbers_quoted_from_other_pages():
    guards = {name: next(code for lang, code in hidden_chunks(text) if "Prose guard" in code)
              for name, text in written_pages("beyond")}
    assert "33.5" in guards["beyond/15-post-hoc.qmd"] and "3.07" in guards["beyond/15-post-hoc.qmd"]
    assert "39.4" in guards["beyond/16-mixed-models.qmd"] and "promis_pf" in guards["beyond/16-mixed-models.qmd"]
    assert "ptukey(" in guards["beyond/15-post-hoc.qmd"]   # the 20% for six pairwise comparisons
    assert "16.6, 18.1" in guards["beyond/16-mixed-models.qmd"]   # the 3-month EMMs' CIs in the Results


def calls_of(code, function):
    """The arguments of each call to function(...) in code, up to its matching parenthesis."""
    found = []
    for match in re.finditer(r"(?<![\w.])" + re.escape(function) + r"\(", code):
        depth, quote, i = 1, None, match.end()
        while depth:
            ch = code[i]
            if quote:
                quote = None if ch == quote else quote
            elif ch in "\"'":
                quote = ch
            elif ch in "([":
                depth += 1
            elif ch in ")]":
                depth -= 1
            i += 1
        found.append(code[match.end():i - 1])
    return found


def top_level(args):
    """args split at the commas that aren't inside brackets or strings."""
    parts, depth, quote, start = [], 0, None, 0
    for i, ch in enumerate(args):
        if quote:
            quote = None if ch == quote else quote
        elif ch in "\"'":
            quote = ch
        elif ch in "([":
            depth += 1
        elif ch in ")]":
            depth -= 1
        elif ch == "," and depth == 0:
            parts.append(args[start:i].strip())
            start = i + 1
    return parts + [args[start:].strip()]


def agreement_checks(text):
    """(names, tol) for each check_agree() call in a page's hidden R chunks; tol is None for the default."""
    checks = []
    for lang, code in hidden_chunks(text):
        for call in calls_of(code, "check_agree") if lang == "r" else []:
            parts = top_level(call)
            names = [part.split("=")[0].strip() for part in top_level(calls_of(parts[0], "list")[0])]
            tol = next((part.split("=")[1].strip() for part in parts[1:] if part.startswith("tol")), None)
            checks.append((names, tol))
    return checks


def test_rule_reads_names_and_tolerance_from_each_check():
    text = ('```{r}\n#| include: false\ncheck_agree(list(a = f(x, y)[["(b)"]], se_a = 2), reticulate::py$chk, tol = 1e-3)\n'
            'check_agree(list(c = 3), reticulate::py$chk_c)\n```')
    assert agreement_checks(text) == [(["a", "se_a"], "1e-3"), (["c"], None)]


def test_mixed_model_checks_loosen_the_tolerance_only_where_the_two_methods_differ():
    """lme4 and statsmodels agree on fixed effects and marginal means to about 1e-9, on the random-effect
    SDs to about 1e-6, and on standard errors only to about 1e-4 (Phase 5 review)."""
    checks = agreement_checks(dict(written_pages("beyond"))["beyond/16-mixed-models.qmd"])
    by_tol = {tol: {name for names, t in checks if t == tol for name in names} for tol in [None, "1e-5", "1e-3"]}
    assert by_tol["1e-3"] and all(name.startswith(("se_", "wald")) for name in by_tol["1e-3"]), by_tol["1e-3"]
    assert {"sd_knee", "sd_residual"} <= by_tol["1e-5"] and all(name.startswith("sd_") for name in by_tol["1e-5"]), by_tol["1e-5"]
    assert {"intercept", "visit_1yr", "emm_pre", "emm_1yr", "emm_boot_3mo", "emm_cast_12mo", "diff_3mo", "diff_12mo"} <= by_tol[None]


def test_conover_p_values_are_checked_r_against_python():
    checks = agreement_checks(dict(written_pages("beyond"))["beyond/15-post-hoc.qmd"])
    assert {"log10_p_6wk_12mo", "log10_p_3mo_12mo"} <= {name for names, tol in checks for name in names}


# ---- each section's Python runs on its own -------------------------------

def undefined_names(code):
    """Names the code reads but never imports, assigns or defines (statement order ignored).
    Names made inside a function, lambda or comprehension count only inside it."""
    defined, used = set(dir(builtins)), set()

    def visit(node, local):
        bind = defined if local is None else local
        if isinstance(node, (ast.FunctionDef, ast.Lambda)):
            if isinstance(node, ast.FunctionDef):
                bind.add(node.name)
            inner = set(local or ()) | {arg.arg for arg in ast.walk(node.args) if isinstance(arg, ast.arg)}
            for default in node.args.defaults + [d for d in node.args.kw_defaults if d]:
                visit(default, local)
            for child in (node.body if isinstance(node.body, list) else [node.body]):
                visit(child, inner)
        elif isinstance(node, (ast.ListComp, ast.SetComp, ast.GeneratorExp, ast.DictComp)):
            inner = set(local or ())
            for generator in node.generators:
                visit(generator.iter, local)
                visit(generator.target, inner)
                for condition in generator.ifs:
                    visit(condition, inner)
            for part in ([node.key, node.value] if isinstance(node, ast.DictComp) else [node.elt]):
                visit(part, inner)
        elif isinstance(node, ast.Name):
            if not isinstance(node.ctx, ast.Load):
                bind.add(node.id)
            elif local is None or node.id not in local:
                used.add(node.id)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            bind.update((alias.asname or alias.name).split(".")[0] for alias in node.names)
        else:
            for child in ast.iter_child_nodes(node):
                visit(child, local)

    visit(ast.parse(code), None)
    return used - defined


def test_rule_finds_names_a_section_never_defines():
    assert undefined_names("import pandas as pd\nprint(np.mean(scores))") == {"np", "scores"}
    assert undefined_names("import numpy as np\nx = [1]\nf = lambda v: v + 1\nprint(np.mean(x), f(2))") == set()


def test_rule_keeps_function_and_comprehension_names_inside_them():
    assert undefined_names("f = lambda scores: scores + 1\nprint(scores)") == {"scores"}
    assert undefined_names("squares = [v * v for v in range(3)]\nprint(v)") == {"v"}
    assert undefined_names("def g(a):\n    b = a + 1\n    return b\nprint(g(1), b)") == {"b"}
    assert undefined_names("def g(days):\n    return days * k\nk = 2\nprint(g(1))") == set()


def test_each_catalog_section_python_runs_on_its_own():
    """Every name a section's visible Python uses is created in that section, so it can be copied alone."""
    for name, anchor, body in catalog_sections():
        code = "\n".join(chunk for lang, chunk in visible_chunks(body) if lang == "python")
        assert undefined_names(code) == set(), f"{name}#{anchor} uses {sorted(undefined_names(code))}"


# ---- bootstrap CIs need a seed ---------------------------------------------
# effectsize computes the CIs of these effect sizes by bootstrap (random resampling),
# so without set.seed() the printed CI changes on every render.

BOOTSTRAP_CI_FUNCTIONS = ("rank_epsilon_squared(", "kendalls_w(")
R_CHUNK = re.compile(r"```\{r[^}]*\}\n(.*?)\n```", re.DOTALL)


def unseeded_bootstrap(text):
    for code in R_CHUNK.findall(text):
        seeded = False
        for line in code.splitlines():
            line = line.split("#", 1)[0]   # comments don't count
            seeded = seeded or "set.seed(" in line
            if any(f in line for f in BOOTSTRAP_CI_FUNCTIONS) and "ci = NULL" not in line and not seeded:
                return True
    return False


def test_rule_catches_an_unseeded_bootstrap_ci():
    assert unseeded_bootstrap("```{r}\neffectsize::kendalls_w(y ~ v | id, data = d)\n```")
    assert not unseeded_bootstrap("```{r}\nset.seed(1)\neffectsize::kendalls_w(y ~ v | id, data = d)\n```")
    assert not unseeded_bootstrap("```{r}\neffectsize::kendalls_w(y ~ v | id, data = d, ci = NULL)\n```")
    assert not unseeded_bootstrap("```{r}\n# kendalls_w() warns about ties\nx <- 1\n```")
    assert unseeded_bootstrap("```{r}\n# set.seed(1) is not needed\neffectsize::kendalls_w(y ~ v | id, data = d)\n```")
    assert unseeded_bootstrap("```{r}\nx <- 1  # set.seed(1) later\neffectsize::kendalls_w(y ~ v | id, data = d)\n```")


def test_bootstrap_cis_are_seeded():
    offenders = [str(f.relative_to(ROOT)) for f in qmd_files() if unseeded_bootstrap(f.read_text(encoding="utf-8"))]
    assert offenders == [], "Call set.seed() before (or pass ci = NULL to) a bootstrap CI in: " + ", ".join(offenders)


# ---- effect sizes that can't be negative get two-sided CIs -----------------
# effectsize's default for these is a one-sided CI (upper limit fixed at 1), which
# isn't comparable with the other 95% CIs on the site (review A6, decision D1).

NONNEGATIVE_EFFECT_SIZE = re.compile(
    r"\b(omega_squared|eta_squared|cramers_v|phi|pearsons_c|rank_epsilon_squared|kendalls_w)\(")


def call_arguments(code, start):
    """The text between the opening parenthesis at code[start] and its matching close."""
    depth = 0
    for i in range(start, len(code)):
        depth += {"(": 1, ")": -1}.get(code[i], 0)
        if depth == 0:
            return code[start + 1:i]
    return code[start + 1:]


def one_sided_effect_size_cis(text):
    """Calls that print an effectsize CI without alternative = "two.sided", or a bootstrap CI
    without iterations = 2000, in any R chunk."""
    found = []
    for code in R_CHUNK.findall(text):
        code = "\n".join(line.split("#", 1)[0] for line in code.splitlines())   # comments don't count
        for match in NONNEGATIVE_EFFECT_SIZE.finditer(code):
            args = call_arguments(code, match.end() - 1)
            if "ci = NULL" in args:
                continue
            if 'alternative = "two.sided"' not in args or (
                    match.group(1) in ("rank_epsilon_squared", "kendalls_w") and "iterations = 2000" not in args):
                found.append(f"{match.group(1)}({args})")
    return found


def test_rule_catches_a_one_sided_effect_size_ci():
    assert one_sided_effect_size_cis("```{r}\neffectsize::omega_squared(fit, partial = FALSE)\n```")
    assert one_sided_effect_size_cis("```{r}\nx <- effectsize::eta_squared(aov(y ~ g, data = d),\n  partial = TRUE)\n```")
    assert one_sided_effect_size_cis('```{r}\neffectsize::kendalls_w(y ~ v | id, data = d, alternative = "two.sided")\n```')
    assert one_sided_effect_size_cis('```{r}\neffectsize::phi(tab)   # alternative = "two.sided"\n```')
    assert not one_sided_effect_size_cis('```{r}\neffectsize::cramers_v(tab, adjust = FALSE, alternative = "two.sided")\n```')
    assert not one_sided_effect_size_cis(
        '```{r}\neffectsize::rank_epsilon_squared(y ~ g, data = d, alternative = "two.sided", iterations = 2000)\n```')
    assert not one_sided_effect_size_cis("```{r}\neffectsize::rank_epsilon_squared(y ~ g, data = d, ci = NULL)\n```")
    assert not one_sided_effect_size_cis("```{r}\n# kendalls_w() warns about ties\nx <- 1\n```")


def test_effect_size_cis_are_two_sided():
    offenders = {str(f.relative_to(ROOT)): calls for f in qmd_files()
                 if (calls := one_sided_effect_size_cis(f.read_text(encoding="utf-8")))}
    assert offenders == {}, 'Pass alternative = "two.sided" (and iterations = 2000 to a bootstrap CI): ' + str(offenders)


# ---- jitter is random too ----------------------------------------------------
# geom_jitter() moves each point by a random amount, so an unseeded jitter redraws the
# figure differently on every render and the frozen figure changes for no reason.

JITTER = re.compile(r"\b(geom_jitter|position_jitter)\(([^)]*)\)")


def unseeded_jitter(text):
    """geom_jitter() itself, or position_jitter() without a seed, in any R chunk."""
    for code in R_CHUNK.findall(text):
        for call, args in JITTER.findall(code):
            if call == "geom_jitter" or "seed" not in args:
                return True
    return False


def test_rule_catches_an_unseeded_jitter():
    assert unseeded_jitter("```{r}\nggplot(d, aes(x, y)) + geom_jitter(width = 0.2)\n```")
    assert unseeded_jitter("```{r}\ngeom_point(position = position_jitter(width = 0.2))\n```")
    assert not unseeded_jitter("```{r}\ngeom_point(position = position_jitter(width = 0.2, seed = 2026))\n```")
    assert not unseeded_jitter("```{r}\nggplot(d, aes(x)) + geom_bar()\n```")


def test_jitter_is_seeded():
    offenders = [str(f.relative_to(ROOT)) for f in qmd_files() if unseeded_jitter(f.read_text(encoding="utf-8"))]
    assert offenders == [], "Use geom_point(position = position_jitter(..., seed = 2026)) in: " + ", ".join(offenders)


# ---- per-group CIs use each group's own count ------------------------------

def test_looped_wilson_cis_take_each_groups_own_count():
    """prop.test(k, n) over several groups takes n from the data, never a typed number or the first group's n."""
    fixed_n = re.compile(r"prop\.test\(\s*[A-Za-z_][\w.]*\s*,\s*(\d|[\w.$]+\[1\])")
    for name, text in written_pages("catalog"):
        visible_r = "\n".join(code for lang, code in visible_chunks(text) if lang == "r")
        assert not fixed_n.search(visible_r), f"{name}: {fixed_n.search(visible_r).group(0)}"


# ---- quiet pages -------------------------------------------------------------
# Quarto silently ignores `message` under a page's `execute:` key on knitr pages, so
# messages such as "Waiting for profiling to be done..." reached the page. knitr's own
# chunk default, set once in _quarto.yml, hides them.

PAGE_EXECUTE_MESSAGE = re.compile(r"^execute:\n(?:  .*\n)*?  message:", re.MULTILINE)


def test_rule_catches_a_page_level_message_option():
    assert PAGE_EXECUTE_MESSAGE.search("---\nengine: knitr\nexecute:\n  message: false\n---\n")
    assert not PAGE_EXECUTE_MESSAGE.search("---\nengine: knitr\nexecute:\n  freeze: auto\n---\n")


def test_messages_are_hidden_by_knitr_for_every_page():
    config = (ROOT / "_quarto.yml").read_text(encoding="utf-8")
    assert re.search(r"^knitr:\n  opts_chunk:\n    message: false$", config, re.MULTILINE)
    offenders = [str(f.relative_to(ROOT)) for f in qmd_files() if PAGE_EXECUTE_MESSAGE.search(f.read_text(encoding="utf-8"))]
    assert offenders == [], "Quarto ignores `execute: message`; remove it from: " + ", ".join(offenders)


def test_pages_use_the_swiss_discharge_labels():
    """cohort.csv says "rehabilitation clinic"; code still selecting "facility" would silently match nothing."""
    offenders = [str(f.relative_to(ROOT)) for f in qmd_files() if re.search(r"\bfacilit(?:y|ies)\b", f.read_text(encoding="utf-8"))]
    assert offenders == [], "Use the discharge label 'rehabilitation clinic' in: " + ", ".join(offenders)


def test_no_page_reads_or_names_vr12():
    """Phase 2c dropped vr12_pcs and vr12_mcs (SP2 spec §6); PROMIS-29+2 physical function replaced them."""
    offenders = [str(f.relative_to(ROOT)) for f in qmd_files() if re.search(r"vr12|VR-12", f.read_text(encoding="utf-8"))]
    assert offenders == [], "Still on VR-12: " + ", ".join(offenders)


FENCED = re.compile(r"^```.*?^```", re.DOTALL | re.MULTILINE)
DOWNLOAD = "https://github.com/hfr-ortho/stats-formation/raw/main/"
VIEW = "https://github.com/hfr-ortho/stats-formation/blob/main/"
DATA_FILE_NAMES = sorted(f.name for d in ["data", "data/answer-keys", "templates"]
                         for f in (ROOT / d).glob("*") if f.suffix in {".csv", ".xlsx"})
DATA_FILE_IN_PROSE = re.compile(
    r"(\[)?`((?:[\w.-]+/)*(?:" + "|".join(map(re.escape, DATA_FILE_NAMES)) + r"))`(\]\(([^)]*)\))?")
# using-this-site.qmd explains what a data path is; that mention is an example, not a file to fetch.
PATH_EXAMPLES = {("getting-started/using-this-site.qmd", "data/cohort.csv")}


def unlinked_data_files(text):
    """Data files named in prose that aren't a link to the file's download address.

    The name must be the file's whole path from the repository's top folder, so `cohort.csv` fails too.
    """
    return [m.group(2) for m in DATA_FILE_IN_PROSE.finditer(FENCED.sub("", text))
            if not (m.group(1) and m.group(4) == DOWNLOAD + m.group(2) and (ROOT / m.group(2)).is_file())]


def test_rule_catches_a_data_file_named_without_a_link():
    assert unlinked_data_files("Open `data/cohort.csv` in Excel.") == ["data/cohort.csv"]
    assert unlinked_data_files("Use `cohort.csv`.") == ["cohort.csv"]
    assert unlinked_data_files(f"Use [`cohort.csv`]({DOWNLOAD}cohort.csv).") == ["cohort.csv"]
    assert unlinked_data_files("Open [`data/cohort.csv`](https://example.org/cohort.csv).") == ["data/cohort.csv"]
    assert unlinked_data_files(f"Open [`data/cohort.csv`]({DOWNLOAD}data/cohort.csv).") == []
    assert unlinked_data_files(f"Open [`data/messy_abstraction_workbook.xlsx`]({DOWNLOAD}data/messy_abstraction_workbook.xlsx).") == []
    assert unlinked_data_files('```r\npath <- "data/cohort.csv"  # `data/cohort.csv`\n```\n') == []


def test_every_data_file_named_in_prose_links_to_its_download():
    """A reader of the website has no data/ folder: a data file the text names must be a link to it."""
    for lang in LANGS:
        for path in sorted((ROOT / lang).rglob("*.qmd")):
            page = path.relative_to(ROOT / lang).as_posix()
            found = [name for name in unlinked_data_files(path.read_text(encoding="utf-8"))
                     if (page, name) not in PATH_EXAMPLES]
            assert found == [], f"{lang}/{page}: data file named without a download link"


def test_setup_page_links_every_data_file_and_codebook():
    """The setup page is the one place that lists all the practice data, in every language."""
    files = [f.relative_to(ROOT).as_posix() for d in ["data", "data/answer-keys", "templates"]
             for f in sorted((ROOT / d).glob("*")) if f.suffix in {".csv", ".xlsx"}]
    codebooks = [f.relative_to(ROOT).as_posix() for f in sorted((ROOT / "data" / "codebooks").glob("*.csv"))]
    assert len(files) == 14 and len(codebooks) == 11
    for lang in LANGS:
        text = (ROOT / lang / "getting-started" / "setup.qmd").read_text(encoding="utf-8")
        missing = [f for f in files if f"[`{f}`]({DOWNLOAD}{f})" not in text]
        missing += [c for c in codebooks if f"]({VIEW}{c})" not in text]
        assert missing == [], f"{lang}/getting-started/setup.qmd doesn't link: {missing}"


LIST_ITEM = re.compile(r"^(?:- |\d+\. )")
NOT_PARAGRAPH = re.compile(r"^(?:\s|#|\||:::)")


def list_glued_to_paragraph(text: str) -> list[int]:
    """Line numbers (from 1) of list items that follow a paragraph line with no blank line between.

    Quarto's Markdown then reads the items as more of the paragraph, and the page shows one run-on
    paragraph with literal hyphens. Front matter and fenced code are skipped. A line before an item
    is fine when it is blank, another item, an indented continuation, a heading, a table row or a
    `:::` line.
    """
    lines = text.splitlines()
    start = 0
    if lines and lines[0] == "---":
        start = next((i for i in range(1, len(lines)) if lines[i] == "---"), 0) + 1
    glued, in_code, previous = [], False, ""
    for number, line in enumerate(lines[start:], start=start + 1):
        if line.startswith("```"):
            in_code = not in_code
            previous = line
            continue
        if in_code:
            continue
        if (LIST_ITEM.match(line) and previous.strip() and not LIST_ITEM.match(previous)
                and not NOT_PARAGRAPH.match(previous) and not previous.startswith("```")):
            glued.append(number)
        previous = line
    return glued


def test_rule_catches_a_list_glued_to_its_paragraph():
    assert list_glued_to_paragraph("How to read it:\n- one\n- two\n") == [2]
    assert list_glued_to_paragraph("How to read it:\n\n- one\n- two\n") == []
    assert list_glued_to_paragraph("Steps:\n1. one\n2. two\n") == [2]
    assert list_glued_to_paragraph("---\ntitle: x\n---\n\n## Heading\n- one\n\n::: {.callout}\n- two\n:::\n") == []
    assert list_glued_to_paragraph("Text\n\n```r\nx <- 1\n- 1\n```\n") == []


def test_every_list_is_separated_from_the_paragraph_above():
    """A list needs a blank line above it, or it renders as part of the paragraph (review U1)."""
    offenders = [f"{path.relative_to(ROOT)}:{n}"
                 for lang in LANGS for path in sorted((ROOT / lang).rglob("*.qmd"))
                 for n in list_glued_to_paragraph(path.read_text(encoding="utf-8"))]
    assert offenders == [], "Add a blank line before the list at: " + ", ".join(offenders)
