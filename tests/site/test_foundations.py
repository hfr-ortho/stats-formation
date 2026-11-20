"""Part 1 · Foundations: the tidy-data, Table 1 and distributions pages."""

import pytest

from sitelib import FREEZE, load

SECTIONS = {
    "foundations/01-tidy-data.html": [
        "what-tidy-means", "collecting", "tidying", "reshaping", "integrity", "exercises"],
    "foundations/02-demographics.html": [
        "setup", "one-group", "which-summary", "by-group", "smd", "missing", "export", "exercises"],
    "foundations/03-distributions.html": [
        "why", "look", "shapiro", "within-groups", "robustness", "transform", "ordinal",
        "paired", "flowchart", "effect-sizes", "exercises"],
}


@pytest.mark.parametrize("page,sections", SECTIONS.items())
def test_page_is_written_with_all_its_sections(site, page, sections):
    soup = load(page)
    assert soup.select_one(".coming-soon") is None, f"{page} is still a stub"
    ids = {el["id"] for el in soup.select("[id]")}
    assert [s for s in sections if s not in ids] == []


@pytest.mark.parametrize("page", SECTIONS)
def test_page_ends_with_at_least_three_solved_exercises(site, page):
    headers = [h.get_text(strip=True) for h in load(page).select("div.callout .callout-header")]
    assert sum(h.endswith("Solution") for h in headers) >= 3


@pytest.mark.parametrize("page", SECTIONS)
def test_page_runs_code_in_both_languages_and_is_frozen(site, page):
    tabsets = load(page).select("div.panel-tabset")
    executed = [t for t in tabsets if t.select(".cell-output, .cell-output-display")]
    assert len(executed) >= 3
    assert (FREEZE / page.removesuffix(".html")).is_dir()


@pytest.mark.parametrize("page", SECTIONS)
def test_page_shows_no_warnings_or_package_messages(site, page):
    noise = [o.get_text()[:80] for o in load(page).select(".cell-output-stderr")]
    assert noise == []


def test_distributions_page_has_the_flowchart(site):
    assert load("foundations/03-distributions.html").select_one(".mermaid, pre.mermaid-js") is not None


def test_tidy_page_says_to_run_the_steps_in_order(site):
    assert "Run the steps in order" in load("foundations/01-tidy-data.html").get_text(" ")


# ---- review fixes ---------------------------------------------------------

def text_of(page):
    """Page text with smart quotes straightened and runs of whitespace collapsed."""
    return " ".join(load(page).get_text(" ").replace("’", "'").split())


@pytest.mark.parametrize("page", SECTIONS)
def test_outputs_never_dump_raw_arrays_or_run_long(site, page):
    for out in load(page).select(".cell-output"):
        text = out.get_text()
        assert "array(" not in text, f"{page}: raw array printed"
        assert len(text.splitlines()) <= 60, f"{page}: {len(text.splitlines())}-line output"


def test_tidy_page_explains_the_month_first_bug_correctly(site):
    text = text_of("foundations/01-tidy-data.html").replace("`", "")
    assert "month-first (US style" in text
    assert "2015-11-02" in text   # why ISO dates are read on their own
    assert "Never parse a column that mixes formats with one setting" in text
    assert "would quietly change results" not in text


def test_demographics_page_states_smds_and_formats_consistently(site):
    page = "foundations/02-demographics.html"
    text = text_of(page)
    assert "just over 0.1" in text
    assert "Smoking status (0.23)" in text
    assert "always returns an observed value" not in text
    assert "tableone shows both" in text
    assert "not independent" in text
    html = str(load(page))
    assert ">65.5 (9.4)<" in html and ">0.203<" in html     # R table: 1 decimal, 3-decimal p


def test_distributions_page_states_statistics_correctly(site):
    text = text_of("foundations/03-distributions.html")
    assert "unlikely to be pure chance" not in text
    assert "would be unusual if there were really no difference" in text
    assert "bouncing around 0.05" in text
    assert "make no assumption about the shape" not in text
    assert "typical BMI of 30" not in text
    assert "within-patient" in text                       # MCID caveat
    assert "p = 0.173" in text                            # three-decimal p-values
    assert "bilateral" in text and "independent" in text
    # Review B8: p is not the probability of no difference; what the 95% refers to.
    assert "p = 0.03, so there's a 3% chance that there's no difference" in text
    assert "A small p-value means" not in text            # read as the chance of normality
    assert "95 of every 100" in text


def test_flowchart_covers_hypothetical_values_and_matches_the_guidance(site):
    soup = load("foundations/03-distributions.html")
    chart = soup.select_one(".mermaid, pre.mermaid-js").get_text()
    assert "hypothetical value" in chart
    assert "small groups" not in chart


def test_tidy_page_names_the_code_key_like_the_template(site):
    """HFR studies use coded data: a study code, and a code key kept by the person the ethics application names."""
    text = text_of("foundations/01-tidy-data.html")
    assert ("The code key, which links study codes to patient numbers, is kept in a separate, secured file "
            "by the person the ethics application names for it") in text
    assert "crosswalk" not in text


def test_tidy_page_states_what_guessing_and_recoding_really_do(site):
    """Review A10 to A12: guessing keeps the text, forcing a number loses it; which recodes
    fail to missing and which to "no"; the blank survey rows are not all missed visits."""
    text = text_of("foundations/01-tidy-data.html")
    assert "silently turns" not in text
    assert "Forcing a number type is what loses values" in text
    assert "Each recode lists the values it expects" not in text   # the old blanket claim
    assert "so an unknown spelling such as T2DM counts as" in text
    # as.roman() reads Arabic and Roman numerals, so a wrong number such as 12 passes (only 0 goes missing);
    # pandas' recode knows only the Roman numerals I to IV, so a wrong one stops it.
    assert "text it can't read as a class" not in text
    assert "A wrong whole number written in digits" in text and "gets through in both" in text
    assert "A wrong number gets through in both" not in text   # a wrong Roman numeral stops pandas
    assert "564 blank rows: 473 from 72 missed visits and 91 items skipped" in text


def test_bounded_is_not_a_reason_for_the_rank_column(site):
    """Review A13: every PROM is bounded; values piled up at the bound are what send a score to ranks."""
    chart = load("foundations/03-distributions.html").select_one(".mermaid, pre.mermaid-js").get_text()
    assert "bounded" not in chart
    assert "floor or ceiling" in chart
    for page in ["foundations/02-demographics.html", "catalog/07-two-paired-groups.html"]:
        text = text_of(page)
        assert "bounded" not in text, page
        assert "floor or ceiling" in text, page


def test_distributions_page_does_not_say_pearson_compares_means(site):
    """Review A14: Pearson correlation measures a straight-line association; it compares no means."""
    text = text_of("foundations/03-distributions.html")
    assert "Pearson correlation ) compare means" not in text
    assert "Pearson correlation measures a straight-line association" in text


def test_worked_examples_match_the_sections_they_point_to(site):
    text = text_of("foundations/03-distributions.html")
    for phrase in ["Is the EFAS score at 3 months different with a boot than with a cast?",
                   "Is pain 6 weeks after the injury different with a boot than with a cast?",
                   "Does graft failure within 2 years differ between hamstring and BPTB grafts?"]:
        assert phrase in text, phrase


# ---- content review of 20.11.2026, task 3.2 --------------------------------

def test_tidy_page_warns_about_decimal_commas_and_two_digit_years(site):
    """Review B22: the number helpers assume a decimal point; a two-digit year is a guess."""
    soup = load("foundations/01-tidy-data.html")
    text = text_of("foundations/01-tidy-data.html")
    assert "decimal commas" in text
    assert 'locale(decimal_mark = ",")' in text
    assert "a two-digit year is a guess about the century" in text
    code = "".join(c.get_text() for c in soup.select("div.sourceCode code"))
    assert 'value_counts(dropna=False).sort_index()' in code   # step 5: both tabs would show a missing sex
    box = [c.get_text(" ") for c in soup.select("div.callout") if "read differently" in c.get_text()]
    assert box and "check 3" in box[0]                   # step 1's box points to the None box


def test_demographics_page_keeps_length_of_stay_out_of_balance(site):
    """Review C11: length of stay is an outcome, in the tables only as the skewed example."""
    text = text_of("foundations/02-demographics.html")
    assert "Length of stay is an outcome" in text
    assert "Diabetes and length of stay are negligible" not in text
    assert "Smoking status (0.23) and length of stay (0.22" not in text


def test_demographics_page_qualifies_baseline_p_values_and_smds(site):
    """Review B23, B18, C14: trials, how an SMD is computed, chance SMDs above 0.1,
    the sex example per patient, rows against patients, the chi-square test and order."""
    text = text_of("foundations/02-demographics.html")
    assert "Randomized trials" in text and "CONSORT" in text
    assert "always positive" in text                         # SMD for several categories
    assert "proportions" in text and "p(1 − p)" in text      # SMD for a yes/no variable
    assert "chance alone can produce SMDs above it" in text
    assert "p = 0.002 for the 520 patients" in text
    assert "The difference is pure chance." not in text
    assert "both procedures of the 80 bilateral patients" in text
    assert "ignores the order" in text


def test_distributions_page_qualifies_pairs_matching_and_rows(site):
    """Review C12, B10, B18, B5: differences for paired data, individual matching,
    p-values on 600 rows, and a Results-style sentence without a comparison word."""
    text = text_of("foundations/03-distributions.html")
    assert "for paired data, the differences" in text
    chart = load("foundations/03-distributions.html").select_one(".mermaid, pre.mermaid-js").get_text()
    assert "for paired data, the differences" in chart
    assert "Treat matched sets like pairs" not in text
    assert "individually matched" in text
    assert "both procedures of the 80 bilateral patients" in text
    assert "had a higher BMI" not in text
    assert "Mean BMI was 31.2 kg/m² in TKA patients and 29.5 kg/m² in THA patients" in text
