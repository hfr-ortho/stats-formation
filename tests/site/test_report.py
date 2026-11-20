"""Part 5 · Putting it together: the example study report (spec section 4, page 18), on the site and
as a Word manuscript. tests/site/test_free_form.py checks what every free-form page shares."""

import hashlib
import re

import pytest

from sitelib import FREEZE, ROOT, SITE, SRC, code_of, docx_text, docx_xml, load, section, target, text_of

REPORT = "report/18-example-report.html"
WORD = SITE / "report" / "18-example-report.docx"


# ---- the Word version ------------------------------------------------------------------

def test_the_page_offers_the_word_version(site):
    links = [a["href"] for a in load(REPORT).select(".quarto-alternate-formats a[href]")]
    assert links == ["18-example-report.docx"] and WORD.exists()


def test_the_word_version_is_frozen_so_ci_can_rebuild_it_without_r():
    frozen = FREEZE / "report" / "18-example-report"
    assert (frozen / "execute-results" / "docx.json").exists() and (frozen / "figure-docx").is_dir()


def test_the_word_version_is_the_manuscript_only(site):
    text = docx_text(WORD)
    assert text.startswith("Improvement in joint-specific scores") and "Every patient in this report is invented" in text
    assert re.findall(r"^(Aim|Methods|Results)$", text, re.MULTILINE) == ["Aim", "Methods", "Results"]
    for tutorial in ["library(", "import ", "check_agree", "data-checksum", "Exercises", "Tidy the raw workbook"]:
        assert tutorial not in text, tutorial


def test_the_word_version_has_table_1_and_the_revision_figure(site):
    text = docx_text(WORD)
    assert "(Table 1)" in text and "(Figure 1)" in text
    assert "Age, years" in text and "SMD" in text and "Pre-op score (HOOS JR or KOOS JR), points" in text
    assert docx_xml(WORD).count("<w:drawing>") == 1


# ---- the steps ---------------------------------------------------------------------------

def test_the_question_is_written_down_before_the_analysis(site):
    text = text_of(section(REPORT, "question"))
    for part in ["Question:", "Primary outcome:", "Primary analysis:", "Secondary outcome:"]:
        assert part in text, part
    assert "Watch out: two questionnaires" in text


STEP_LINKS = {
    "tidy": "foundations/01-tidy-data.html#tidying",
    "integrity": "foundations/01-tidy-data.html#integrity",
    "table-1": "foundations/02-demographics.html#smd",
    "distributions": "foundations/03-distributions.html",
    "primary-analysis": "catalog/06-two-unpaired-groups.html#unpaired-t",
    "survival": "survival/13-kaplan-meier.html#competing-risks",
}


@pytest.mark.parametrize("anchor,expected", STEP_LINKS.items())
def test_each_step_links_to_the_page_that_explains_it(site, anchor, expected):
    hrefs = [target(REPORT, a["href"]) for a in section(REPORT, anchor).select("a[href]")]
    assert expected in hrefs, hrefs


def test_failed_integrity_checks_stop_the_script(site):
    code = code_of(section(REPORT, "integrity"))
    assert code.count("stopifnot(") >= 4 and code.count("assert ") >= 4
    assert "revised_registry" in code   # the workbook's red fills, checked against the registry


def test_table_1_uses_smds_and_shows_missing_values(site):
    code = code_of(section(REPORT, "table-1"))
    assert 'add_difference(test = everything() ~ "smd")' in code and "smd=True" in code
    assert 'missing_text = "Missing"' in code and "missing=True" in code


def test_the_primary_analysis_is_the_one_planned(site):
    code = code_of(section(REPORT, "primary-analysis"))
    assert "t.test(change ~ procedure" in code and "equal_var=False" in code
    assert "hedges_g(" in code and 'eftype="hedges"' in code


def test_revision_is_a_cumulative_incidence_with_death_competing(site):
    code = code_of(section(REPORT, "survival"))
    assert 'labels = c("censored", "revision", "death")' in code and "CumIncidenceRight(" in code
    assert "event_status == 0" in code   # the reverse Kaplan-Meier follow-up


# ---- the manuscript ----------------------------------------------------------------------

def test_the_manuscript_states_the_caveats_and_the_missing_data(site):
    methods = text_of(section(REPORT, "methods"))
    results = text_of(section(REPORT, "results"))
    assert "points on each joint's own scale" in methods and "treating death as a competing risk" in methods
    assert "Both scores were available for 93 patients (77.5%)" in results


# ---- final review fixes --------------------------------------------------------------------

def test_missing_data_exercise_separates_the_two_reasons_a_score_is_missing(site):
    text = text_of(section(REPORT, "exercises"))
    assert "didn't answer" not in text
    assert "the other 5 TKA patients had no pre-op score" in text and "15 TKA patients (22.4%; p = 0.239)" in text


def test_the_manuscript_does_not_claim_to_update_itself(site):
    text = text_of(section(REPORT, "manuscript"))
    assert "changes every number at once" not in text
    assert "stops the render until every number in the text is updated" in text
    assert "The Discussion is the author's to write" in text


def test_the_methods_give_time_zero_and_censoring(site):
    methods = text_of(section(REPORT, "methods"))
    assert "from the date of surgery to revision" in methods and "(censored)" in methods


def test_the_revision_figure_shows_the_numbers_at_risk(site):
    found = section(REPORT, "survival")
    assert "add_risktable(" in code_of(found) and "17 patients were still followed at 8 years" in text_of(found)


def test_table_1_reports_absolute_smds_without_pooling_the_two_questionnaires(site):
    text = docx_text(WORD)
    assert "absolute standardized mean difference" in text and "Overall" not in text
    assert not re.search(r"(?<![\d.])-0\.\d", text)
    assert not re.search(r"(?<![\d.])-0\.\d", text_of(section(REPORT, "results")))


def test_results_give_the_ceiling_denominators(site):
    assert "15 of 46 THA patients (32.6%)" in text_of(section(REPORT, "results"))


def test_hedges_g_is_read_with_its_ci_in_both_languages(site):
    found = section(REPORT, "primary-analysis")
    assert "runs from a small difference to a large one" in text_of(found) and "compute_esci(" in code_of(found)
    assert "adjusted.pvalues" in code_of(section(REPORT, "exercises"))


def test_the_registry_link_is_checked_on_more_than_revisions(site):
    found = section(REPORT, "integrity")
    code = code_of(found)
    assert "surgery_date_registry" in code and "procedure_registry" in code and "n_distinct(study$patient_id)" in code
    assert "120 different patients" in text_of(found)


def test_the_prose_guard_reads_the_missing_counts_from_the_data():
    page = (SRC / "report" / "18-example-report.qmd").read_text(encoding="utf-8")
    guard = page[page.index("# Prose guard"):page.index("## Exercises {#exercises}")]
    assert "20 + 47 == 67" not in guard and "is.na(study$prom_1yr)" in guard


# ---- content review of 20.11.2026: B1, B3, B4, B5 (task 3.8) -------------------------------

def test_the_word_version_states_the_missing_data_handling_and_the_counts(site):
    """B1: the primary analysis needs both scores, so every early failure is out of it; say so and count."""
    text = docx_text(WORD)
    assert "in patients with both scores (complete-case analysis)" in text
    assert "Patients who were revised or died before 1 year had no 1-year score and were therefore not in this analysis." in text
    assert ("Of the other 27, 5 had no pre-op score (all after TKA) and 22 had no 1-year score; before 1 year, "
            "4 of the 22 had been revised, 1 had died and 2 had reached the end of registry follow-up, "
            "and 15 were still followed.") in text


def test_the_word_version_states_what_the_code_shows_about_design_and_windows(site):
    """B3: only what the code and the data show: design, one joint per patient, windows, prespecification."""
    text = docx_text(WORD)
    assert "In this cohort study, we studied 120 primary THAs" in text
    assert "in 120 patients (one joint per patient)" in text
    assert "within 30 days before surgery and the 1-year score 300 to 425 days after surgery" in text
    assert "The primary outcome and the primary analysis were specified before the outcome data were examined." in text
    assert "censoring revisions and deaths" in text   # what the reverse Kaplan-Meier code does


def test_the_word_version_gives_the_sex_adjusted_difference(site):
    """B4: the adjusted estimate beside the crude one, in the same direction (THA minus TKA)."""
    text = docx_text(WORD)
    assert "In a sensitivity analysis, the difference in the change in score was adjusted for sex by linear regression." in text
    assert "Adjusted for sex, the difference (THA minus TKA) was 9.3 points (95% CI 3.5 to 15.0; p = 0.002)." in text


def test_the_word_version_cites_r_and_the_packages_behind_the_numbers(site):
    """B5: the one program that produced the quoted numbers, with its version and main packages."""
    text = docx_text(WORD)
    assert re.search(r"Analyses used R \d+\.\d+\.\d+ with the packages gtsummary [\d.-]+ and smd [\d.-]+ \(Table 1\), "
                     r"effectsize [\d.-]+ \(Hedges' g\), survival [\d.-]+ \(follow-up and cumulative incidence\) "
                     r"and ggsurvfit [\d.-]+ \(Figure 1\)\.", text)
    assert "Python 3.13" not in text and "R 4.6 and Python" not in text


def test_the_word_version_leaves_out_the_teaching_box(site):
    text = docx_text(WORD)
    for teaching in ["What a real Methods also needs", "STROBE", "CONSORT", "BASEC", "[", "sensitivity analysis checks"]:
        assert teaching not in text, teaching


def test_the_missing_scores_are_cross_tabulated_against_the_first_year(site):
    found = section(REPORT, "missing-scores")
    code, text = code_of(found), text_of(found)
    assert "before_1_year" in code and "addmargins(" in code and "pd.crosstab(" in code
    assert "4 were revised (at 0.19, 0.26, 0.45 and 0.81 years)" in text
    assert "patients whose joint was still in place, and who were still followed, at 1 year" in text
    assert "are what the abstractor couldn't find" not in text_of(section(REPORT, "integrity"))


def test_the_sensitivity_analysis_adjusts_for_sex_and_points_to_exercise_2(site):
    found = section(REPORT, "sensitivity")
    code, text = code_of(found), text_of(found)
    assert "lm(change ~ procedure + sex, data = analysed)" in code and 'smf.ols("change ~ procedure + sex"' in code
    assert "−9.26 points (95% CI −14.99 to −3.54" in text and "exercise 2" in text


def test_the_manuscript_points_to_the_reporting_guidelines(site):
    found = section(REPORT, "manuscript")
    hrefs = [a["href"] for a in found.select("a[href]")]
    assert "https://www.strobe-statement.org/checklists/" in hrefs and "https://www.consort-spirit.org/" in hrefs
    assert any(target(REPORT, h).startswith("getting-started/real-data.html#") for h in hrefs if not h.startswith("http"))
    text = text_of(found)
    assert "What a real Methods also needs" in text and "CONSORT 2025" in text
    assert "CER-VD (BASEC number [" in text and "Not STROBE items" in text
    assert "the baseline differences between the groups" in text   # B4: the Discussion list


def test_the_frozen_word_version_matches_the_current_data_and_ships_flextables_files():
    current = hashlib.md5((ROOT / "data" / "CHECKSUMS.md5").read_bytes()).hexdigest()
    frozen = FREEZE / "report" / "18-example-report" / "execute-results" / "docx.json"
    assert f"data-checksum: {current}" in frozen.read_text(encoding="utf-8")
    assert (ROOT / "_freeze" / "site_libs" / "tabwid-1.1.3").is_dir()
