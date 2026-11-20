"""Part 2 · Test catalog: one page per row of the decision table, one section per cell."""

import re

import pytest

from sitelib import CELL_ANCHORS, FREEZE, NO_EVIDENCE_AS_NO_DIFFERENCE, code_of, load, section, target, text_of, unreported

# Catalog pages written so far. Later phases add pages 8-12 here.
WRITTEN = [
    "catalog/04-describe-one-group.html",
    "catalog/05-one-group-vs-hypothetical.html",
    "catalog/06-two-unpaired-groups.html",
    "catalog/07-two-paired-groups.html",
    "catalog/08-three-plus-unmatched.html",
    "catalog/09-three-plus-matched.html",
    "catalog/10-association.html",
    "catalog/11-predict-from-one.html",
    "catalog/12-predict-from-several.html",
]

# Spec section 6, steps 2-8, as h3 headings in this order. Page 4 describes a
# group rather than testing it: its estimate and CI are the result, so it has
# no separate effect-size step, and its plain-words step explains a calculation.
ANATOMY = ["When to use it", "What the test really does", "Look at the data first", "Run it", "Read the output",
           "Effect size and 95% CI", "How to report it"]
DESCRIBE = ["When to use it", "What the calculation really does", "Look at the data first", "Run it",
            "Read the output", "How to report it"]


def anatomy(page):
    return DESCRIBE if page.startswith("catalog/04-") else ANATOMY

SECTIONS = [(page, anchor) for page in WRITTEN for anchor in CELL_ANCHORS[page]]

# Survival cells give a short worked example and point to the full treatment.
SURVIVAL_LINKS = {cell: target for cell, target in {
    ("catalog/04-describe-one-group.html", "kaplan-meier"): "survival/13-kaplan-meier.html",
    ("catalog/06-two-unpaired-groups.html", "log-rank"): "survival/14-cox-regression.html",
    ("catalog/07-two-paired-groups.html", "stratified-cox"): "survival/14-cox-regression.html",
    ("catalog/08-three-plus-unmatched.html", "cox"): "survival/14-cox-regression.html",
    ("catalog/09-three-plus-matched.html", "stratified-cox"): "survival/14-cox-regression.html",
    ("catalog/11-predict-from-one.html", "cox"): "survival/14-cox-regression.html",
    ("catalog/12-predict-from-several.html", "cox"): "survival/14-cox-regression.html",
}.items() if cell[0] in WRITTEN}


@pytest.mark.parametrize("page", WRITTEN)
def test_page_is_written_and_frozen(site, page):
    assert load(page).select_one(".coming-soon") is None, f"{page} is still a stub"
    assert (FREEZE / page.removesuffix(".html")).is_dir()


@pytest.mark.parametrize("page,anchor", SECTIONS)
def test_section_follows_the_page_anatomy(site, page, anchor):
    found = section(page, anchor)
    steps = [h.get_text(strip=True) for h in found.select("section.level3 > h3")]
    assert steps == anatomy(page)
    text = text_of(found)
    assert "The question:" in text                                      # step 1
    report = " ".join(text_of(q) for q in found.select("blockquote"))
    assert "Methods:" in report and "Results:" in report                # step 7
    assert found.select("div.callout-warning"), "no ⚠️ Watch out box"   # step 8


@pytest.mark.parametrize("page,anchor", SECTIONS)
def test_section_shows_output_in_both_languages(site, page, anchor):
    ran = [tabset for tabset in section(page, anchor).select("div.panel-tabset")
           if all(pane.select(".cell-output, .cell-output-display")
                  for pane in tabset.select("div.tab-pane"))]
    assert ran, f"{page}#{anchor}: no tabset shows output in both R and Python"


@pytest.mark.parametrize("page", WRITTEN)
def test_page_ends_with_at_least_three_solved_exercises(site, page):
    exercises = load(page).select_one("section#exercises")
    headers = [h.get_text(strip=True) for h in exercises.select("div.callout .callout-header")]
    assert sum(h.endswith("Solution") for h in headers) >= 3


@pytest.mark.parametrize("page", WRITTEN)
def test_page_shows_no_warnings_or_package_messages(site, page):
    assert [out.get_text()[:80] for out in load(page).select(".cell-output-stderr")] == []


@pytest.mark.parametrize("page", WRITTEN)
def test_outputs_are_short_and_never_dump_objects(site, page):
    for out in load(page).select(".cell-output"):
        text = out.get_text()
        assert "array(" not in text and "<matplotlib." not in text, f"{page}: object dumped: {text[:80]}"
        assert len(text.splitlines()) <= 40, f"{page}: {len(text.splitlines())}-line output"


@pytest.mark.parametrize("cell,target", SURVIVAL_LINKS.items())
def test_survival_sections_point_to_the_full_treatment(site, cell, target):
    page, anchor = cell
    hrefs = [a["href"].split("#")[0] for a in section(page, anchor).select("a[href]")]
    assert any(href.endswith(target) for href in hrefs)


def test_log_rank_section_names_the_mantel_haenszel_test(site):
    assert "Mantel-Haenszel" in text_of(section("catalog/06-two-unpaired-groups.html", "log-rank"))


# ---- sub-project 2: sections moved to the dataset whose question fits best (SP2 spec §4) ----

MOVED_SECTIONS = {
    ("catalog/04-describe-one-group.html", "median-iqr"): ("data/proms_long.csv", "ohs"),
    ("catalog/04-describe-one-group.html", "proportion"): ("data/hip_fracture.csv", "death_30d"),
    ("catalog/05-one-group-vs-hypothetical.html", "binomial-test"): ("data/hip_fracture.csv", "surgery_within_48h"),
    ("catalog/06-two-unpaired-groups.html", "unpaired-t"): ("data/foot_ankle_rct_long.csv", "efas"),
    ("catalog/06-two-unpaired-groups.html", "mann-whitney"): ("data/foot_ankle_rct_long.csv", "pain_nrs"),
    ("catalog/06-two-unpaired-groups.html", "fisher-chi-square"): ("data/acl_cohort.csv", "failure_2y"),
    ("catalog/07-two-paired-groups.html", "paired-t"): ("data/hip_preservation_imaging.csv", "alpha_dunn45_deg"),
    ("catalog/08-three-plus-unmatched.html", "chi-square"): ("data/acl_cohort.csv", "rts_12mo"),
    ("catalog/09-three-plus-matched.html", "repeated-measures-anova"): ("data/proms_long.csv", "promis_pf"),
    ("catalog/09-three-plus-matched.html", "friedman"): ("data/foot_ankle_rct_long.csv", "efas"),
    ("catalog/10-association.html", "pearson"): ("data/hip_preservation_imaging.csv", "torsion_budin_deg"),
    ("catalog/11-predict-from-one.html", "logistic-regression"): ("data/hip_fracture.csv", "hours_to_surgery"),
    ("catalog/11-predict-from-one.html", "cox"): ("data/acl_cohort.csv", "tibial_slope_deg"),
    ("catalog/12-predict-from-several.html", "multiple-logistic-regression"): ("data/acl_cohort.csv", "rts_12mo"),
}


@pytest.mark.parametrize("cell,source", MOVED_SECTIONS.items())
def test_moved_sections_teach_from_their_new_data(site, cell, source):
    dataset, column = source
    code = code_of(section(*cell))
    assert code.count(f'read_csv("{dataset}"') >= 2, f"{cell}: R and Python should both read {dataset}"
    assert column in code, f"{cell}: the code never uses {column}"


def test_events_rule_counts_the_smaller_outcome_group(site):
    warning = text_of(section("catalog/12-predict-from-several.html", "multiple-logistic-regression").select_one("div.callout-warning"))
    assert "smaller outcome group" in warning and "15 of 350" in warning


def test_pearson_warning_says_correlation_is_not_agreement(site):
    warning = text_of(section("catalog/10-association.html", "pearson").select_one("div.callout-warning"))
    assert "isn't agreement" in warning and "−10.2° to 7.8°" in warning


def test_friedman_says_how_many_boot_patients_were_analyzed(site):
    """Patients miss trial visits: the reader needs the number analyzed and the number randomized."""
    found = section("catalog/09-three-plus-matched.html", "friedman")
    assert "50 of the 60 patients" in " ".join(text_of(q) for q in found.select("blockquote"))


# ---- review fixes ---------------------------------------------------------

def test_kaplan_meier_section_shows_the_revised_case_it_describes(site):
    outputs = " ".join(o.get_text() for o in section("catalog/04-describe-one-group.html", "kaplan-meier").select(".cell-output"))
    assert outputs.count("C0005") >= 2, "the fifth case should appear in both the R and the Python output"


def test_proportions_name_their_denominator(site):
    for page, anchor, phrase in [("catalog/04-describe-one-group.html", "proportion", "74 of 1,200 patients"),
                                 ("catalog/05-one-group-vs-hypothetical.html", "binomial-test", "1,034 of 1,200 patients")]:
        found = section(page, anchor)
        report = " ".join(text_of(q) for q in found.select("blockquote"))
        assert phrase in report, f"{page}#{anchor}"
        assert "of patients had" not in text_of(found)
    for page, phrase in [("catalog/04-describe-one-group.html", "257 of 1,200 patients"),
                         ("catalog/05-one-group-vs-hypothetical.html", "74 of 1,200 patients")]:
        answers = " ".join(text_of(q) for q in section(page, "exercises").select("blockquote"))
        assert phrase in answers, page


def test_binomial_warning_is_about_choosing_one_sided_after_the_fact(site):
    """A target invites a one-sided test; choosing one after seeing the data makes p too small."""
    warning = text_of(section("catalog/05-one-group-vs-hypothetical.html", "binomial-test").select_one("div.callout-warning"))
    assert "one-sided" in warning and "before the data came in" in warning


def test_log_rank_results_give_each_curve_with_its_ci(site):
    found = section("catalog/06-two-unpaired-groups.html", "log-rank")
    report = " ".join(text_of(q) for q in found.select("blockquote"))
    assert "71.1% (95% CI 61.5% to 78.8%)" in report and "89.9% (95% CI 84.7% to 93.3%)" in report
    outputs = " ".join(o.get_text() for o in found.select(".cell-output"))
    assert "0.7114" in outputs and "0.8986" in outputs   # the code prints what the Results sentence quotes


def test_results_sentences_give_medians_with_their_iqrs(site):
    report = " ".join(text_of(q) for q in section("catalog/06-two-unpaired-groups.html", "mann-whitney").select("blockquote"))
    assert "IQR 3 to 4.75" in report and "IQR 4 to 6" in report
    answer = text_of(section("catalog/07-two-paired-groups.html", "exercises"))
    assert "IQR 65.4 to 81.5" in answer and "IQR 73.6 to 93.8" in answer


def test_tied_pain_scores_are_counted_correctly(site):
    """Whole-number pain scores tie often; the section counts the pairs so readers see why the estimate is a whole number."""
    text = text_of(section("catalog/06-two-unpaired-groups.html", "mann-whitney"))
    assert "less pain in 61%, more in 25%, and 14% were tied" in text


def test_trial_results_say_how_many_were_analyzed(site):
    """Patients miss trial visits: the reader needs the number analyzed in each arm and the number randomized."""
    page = "catalog/06-two-unpaired-groups.html"
    for anchor, counts, analyzed in [("unpaired-t", ["n = 57", "n = 55"], "112 of the 120 randomized patients"),
                                     ("mann-whitney", ["n = 58"], "116 of the 120 randomized patients")]:
        found = section(page, anchor)
        report = " ".join(text_of(q) for q in found.select("blockquote"))
        assert all(n in report for n in counts) and analyzed in text_of(found), anchor
        assert "in the patients seen at that visit" in report, anchor
    answers = text_of(section(page, "exercises"))
    for phrase in ["(SD 2.7; n = 58)", "(SD 2.9; n = 58)", "(IQR 18 to 22; n = 55)", "(IQR 19 to 23; n = 47)",
                   "5 in the boot arm, 13 in the cast arm"]:
        assert phrase in answers, phrase


def test_yates_box_matches_its_own_numbers(site):
    """Yates' correction is meant to move p toward Fisher's, but here it overshoots (0.986 vs Fisher's 0.775)."""
    text = text_of(section("catalog/06-two-unpaired-groups.html", "fisher-chi-square"))
    assert "a little larger (more cautious) and closer to Fisher's" not in text
    assert "it can overshoot" in text


def test_bootstrap_box_gives_the_real_reason_bca_fails(site):
    """BCa fails because every leave-one-out estimate is -1 (its acceleration is 0/0), not because resamples tie."""
    text = text_of(section("catalog/06-two-unpaired-groups.html", "mann-whitney"))
    assert "leaving out any one patient still gives −1" in text


def test_quartile_reading_allows_for_ties(site):
    """62 of 194 Oxford Hip Scores are 39 or less: with ties, "a quarter" is "at least a quarter"."""
    assert "At least a quarter scored 39 or less" in text_of(section("catalog/04-describe-one-group.html", "median-iqr"))


def test_exact_ci_box_does_not_send_readers_to_a_missing_number(site):
    """Page 4 no longer shows the Wilson interval for these 1,034 patients, so page 5 gives it itself."""
    text = text_of(section("catalog/05-one-group-vs-hypothetical.html", "binomial-test"))
    assert "the Wilson interval that page 4 uses" in text


def test_torsion_answer_gives_each_methods_value(site):
    answers = text_of(section("catalog/07-two-paired-groups.html", "exercises"))
    assert "14.5° (SD 8.9) on CT and 13.3° (SD 7.6) on the Budin view" in answers


def test_wilcoxon_box_describes_page_6s_cis_correctly(site):
    """Page 6's two Hodges-Lehmann CIs agree since it moved to whole-number pain scores."""
    text = text_of(section("catalog/07-two-paired-groups.html", "wilcoxon-signed-rank"))
    assert "on page 6 they differ a little" not in text
    assert "as they do on page 6" in text


# ---- content review of 20.11.2026: pages 4 to 6 -------------------------------

def test_describe_page_does_not_give_the_column_median_as_the_follow_up(site):
    """Review A1: revisions and deaths cut followup_years short; page 13's reverse Kaplan-Meier gives 5.62 years."""
    page = "catalog/04-describe-one-group.html"
    found = section(page, "kaplan-meier")
    text = text_of(found)
    assert "with a median follow-up of 4.365 years" not in text
    assert "not the study's median follow-up" in text and "5.62 years" in text
    assert "survival/13-kaplan-meier.html#follow-up" in [target(page, a["href"]) for a in found.select("a[href]")]


def test_describe_page_counts_procedures_not_patients(site):
    """Review A2: cohort rows are procedures; the 263 at risk at 5 years belong to 233 patients."""
    page = "catalog/04-describe-one-group.html"
    found = section(page, "kaplan-meier")
    text = text_of(found)
    assert "263 procedures" in text and "263 patients" not in text
    assert "263 procedures at risk" in " ".join(text_of(q) for q in found.select("blockquote"))
    assert "how many procedures were still being followed" in text   # one word for the rows through the section
    assert "procedures = n()" in code_of(found)   # the count of rows is labeled procedures in the output too
    assert "median_followup" not in code_of(found)   # the column's middle value is not the median follow-up (A1)
    assert "as fewer patients remain" not in text   # review A7: the band widens at revisions, not as patients leave
    assert "widens at each revision" in text
    mean_sd = text_of(section(page, "mean-sd"))
    assert "how precisely 600 cases pin down" in mean_sd
    assert "600 patients" not in mean_sd and "95% of cases lie within 2 SDs" in mean_sd


def test_binomial_box_describes_the_set_it_adds_up(site):
    """Review A3: the p-value adds every result no more likely than 1,034; on the high side that starts at 1,122."""
    text = text_of(section("catalog/05-one-group-vs-hypothetical.html", "binomial-test"))
    assert "no more likely than 1,034" in text and "1,122 or more on the high side" in text
    assert "every result further from 1,080" not in text


def test_describe_pages_do_not_send_bounded_scores_to_ranks(site):
    """Review A13, as on pages 2, 3 and 7: values piled up at a floor or ceiling, not a bounded scale, call for ranks."""
    for page, anchor in [("catalog/04-describe-one-group.html", "median-iqr"),
                         ("catalog/05-one-group-vs-hypothetical.html", "one-sample-t")]:
        assert "bounded" not in text_of(load(page)), page
        assert "floor or ceiling" in text_of(section(page, anchor)), page


def test_three_group_pages_do_not_send_bounded_scores_to_ranks(site):
    """Review A13 on pages 8 and 9: the rank test is for values piled up at a floor or ceiling, not any bounded scale."""
    for page, anchor in [("catalog/08-three-plus-unmatched.html", "one-way-anova"),
                         ("catalog/09-three-plus-matched.html", "repeated-measures-anova")]:
        assert "bounded" not in text_of(load(page)), page
        assert "piles up at a floor or ceiling" in text_of(section(page, anchor)), page


def test_two_odds_ratios_are_close_only_with_large_counts(site):
    """Review A4: for the table 3, 1 / 1, 3 the sample odds ratio is 9 and fisher.test() gives 6.41."""
    text = text_of(section("catalog/06-two-unpaired-groups.html", "fisher-chi-square"))
    assert "always close" not in text and "The two are close unless the counts are small" in text


def test_hodges_lehmann_estimate_can_land_on_half_points(site):
    """Review A5: the median of an even number of whole-number differences (3,364 here) can be a half."""
    text = text_of(section("catalog/06-two-unpaired-groups.html", "mann-whitney"))
    assert "land on whole numbers too" not in text
    assert "its CI can only land on whole or half points (here all three are whole)" in text


# ---- three or more groups -------------------------------------------------

THREE_GROUP_PAGES = [page for page in WRITTEN if page.startswith(("catalog/08-", "catalog/09-"))]
REPORTING_PAGES = [page for page in WRITTEN if page >= "catalog/08-"]   # pages written since the Phase 3b review


@pytest.mark.parametrize("page", THREE_GROUP_PAGES)
def test_three_group_pages_end_with_which_groups_differ(site, page):
    hrefs = [a["href"].split("#")[0] for a in section(page, "which-groups-differ").select("a[href]")]
    assert any(href.endswith("beyond/15-post-hoc.html") for href in hrefs)


def test_matched_page_warns_that_missed_visits_drop_patients(site):
    soup = load("catalog/09-three-plus-matched.html")
    warnings = [box for box in soup.select("div.callout-warning") if "missed visit" in text_of(box)]
    assert warnings, "no warning about missed visits"
    assert any(a["href"].split("#")[0].endswith("beyond/16-mixed-models.html") for a in warnings[0].select("a[href]"))


@pytest.mark.parametrize("page", REPORTING_PAGES)
def test_reports_never_turn_no_evidence_into_no_difference(site, page):
    """A wide CI or a non-significant check is "no evidence of a difference", never "similar" or "held"."""
    reports = [text_of(q) for q in load(page).select("blockquote")] + [text_of(section(page, "exercises"))]
    for text in reports:
        found = NO_EVIDENCE_AS_NO_DIFFERENCE.findall(text)
        assert not found, f"{page}: {found}"


@pytest.mark.parametrize("page", ["catalog/08-three-plus-unmatched.html", "catalog/09-three-plus-matched.html",
                                  "catalog/10-association.html"])
def test_no_results_sentence_reports_a_one_sided_ci(site, page):
    """Review A6, decision D1: effect sizes that can't be negative are reported with a two-sided 95% CI."""
    results = [text_of(p) for p in load(page).select("blockquote p") if text_of(p).startswith("Results:")]
    assert results, f"{page} has no Results sentence"
    for text in results:
        assert "one-sided" not in text and "to 1.00)" not in text, text


def test_unmatched_page_counts_procedures_not_patients(site):
    """Cohort rows are procedures (80 patients had both sides operated on) and ACL rows are reconstructions."""
    page = "catalog/08-three-plus-unmatched.html"
    assert re.findall(r"(?<!–)\b\d+ patients\b", text_of(load(page))) == ["80 patients"]   # not "ASA 3–4 patients"
    assert "Of 600 procedures" in text_of(section(page, "kruskal-wallis"))
    assert "3 of 67 quadriceps reconstructions" in text_of(section(page, "exercises"))


def test_fisher_note_describes_scipys_larger_tables(site):
    text = text_of(section("catalog/08-three-plus-unmatched.html", "chi-square"))
    assert "only handles 2 × 2" not in text and "random resampling" in text


@pytest.mark.parametrize("page", REPORTING_PAGES)
def test_exercise_answers_follow_the_reporting_conventions(site, page):
    """Answers are model Results sentences: effect sizes with a CI, means with SDs, medians with IQRs."""
    for paragraph in section(page, "exercises").select("p"):
        text = text_of(paragraph)
        assert unreported(text) == [], text


# ---- curve fits on repeated scores -------------------------------------------

REPEATED_SCORE_SECTIONS = [cell for cell in [("catalog/11-predict-from-one.html", "nonlinear-regression"),
                                             ("catalog/12-predict-from-several.html", "multiple-nonlinear-regression")]
                           if cell[0] in WRITTEN]


@pytest.mark.parametrize("page,anchor", REPEATED_SCORE_SECTIONS)
def test_curve_fits_warn_that_repeated_scores_make_the_cis_unreliable(site, page, anchor):
    """Each joint contributes up to four scores. That makes least-squares CIs untrustworthy in either
    direction (too wide for within-joint contrasts such as tau), so the warning mustn't promise one."""
    warnings = [box for box in section(page, anchor).select("div.callout-warning") if "can't be trusted" in text_of(box)]
    assert warnings, f"{page}#{anchor}: no warning that the CIs can't be trusted"
    assert "are too narrow" not in text_of(warnings[0])
    assert any(a["href"].split("#")[0].endswith("beyond/16-mixed-models.html") for a in warnings[0].select("a[href]"))
    # Review B2: a resident copies the Methods sentence, not the box, so the Methods say it too.
    methods = [text_of(p) for p in section(page, anchor).select("blockquote p") if text_of(p).startswith("Methods:")]
    assert methods and "treated as independent" in methods[0] and "illustrative only" in methods[0], methods


def test_cox_warning_says_a_slope_is_not_a_treatment(site):
    """Slope isn't assigned, so the hazard ratio doesn't show what an osteotomy would do."""
    found = section("catalog/11-predict-from-one.html", "cox")
    warning = text_of(found.select_one("div.callout-warning"))
    assert "treatment effect" in warning and "osteotomy" in warning


def test_cox_section_keeps_the_cause_specific_lesson(site):
    """Censoring deaths gives the rate among patients still alive; the section says when that matters."""
    assert "still alive" in text_of(section("catalog/11-predict-from-one.html", "cox"))


def test_linear_regression_no_longer_points_to_page_10s_r_squared(site):
    assert "page 10" not in text_of(section("catalog/11-predict-from-one.html", "linear-regression")).lower()


def test_unplanned_findings_are_labeled_in_the_results(site):
    """The adjusted Cox model's sex effect wasn't the question, so the Results sentence says it's exploratory."""
    results = " ".join(text_of(q) for q in section("catalog/12-predict-from-several.html", "cox").select("blockquote"))
    sentence = next(s for s in results.split(". ") if "for men compared with women" in s)
    assert "exploratory" in sentence


# ---- links into the survival pages ----------------------------------------------

# Where a sentence promises one topic ("page 13 covers competing risks"), its link
# lands on that section of pages 13-14, not the top of the page.
SECTION_LINKS = {
    "catalog/04-describe-one-group.html": ["survival/13-kaplan-meier.html#competing-risks"],
    "catalog/06-two-unpaired-groups.html": ["survival/14-cox-regression.html#proportional-hazards",
                                            "survival/13-kaplan-meier.html#competing-risks"],
    "catalog/08-three-plus-unmatched.html": ["survival/14-cox-regression.html#proportional-hazards",
                                             "survival/13-kaplan-meier.html#competing-risks"],
    "catalog/09-three-plus-matched.html": ["survival/14-cox-regression.html#choosing-covariates"],
    "catalog/11-predict-from-one.html": ["survival/13-kaplan-meier.html#competing-risks",
                                         "survival/14-cox-regression.html#fine-gray"],
    "catalog/12-predict-from-several.html": ["survival/14-cox-regression.html#proportional-hazards",
                                             "survival/14-cox-regression.html#choosing-covariates"],   # review B9
}


@pytest.mark.parametrize("page,targets", SECTION_LINKS.items())
def test_links_into_the_survival_pages_land_on_the_section_they_promise(site, page, targets):
    hrefs = {target(page, a["href"]) for a in load(page).select("main a[href]")}
    assert [target for target in targets if target not in hrefs] == []


def test_phase_2b_minors_stay_fixed(site):
    assert "within 30 days of admission" in text_of(section("catalog/04-describe-one-group.html", "proportion"))
    mann_whitney = text_of(section("catalog/06-two-unpaired-groups.html", "mann-whitney"))
    assert "between the 43rd (a 4) and the 44th (a 5)" in mann_whitney and "three-quarters of the way between them" in mann_whitney
    assert "differ between a hamstring graft" in text_of(section("catalog/06-two-unpaired-groups.html", "fisher-chi-square"))
    assert "square root of the average of the two variances" in text_of(load("catalog/07-two-paired-groups.html"))
    assert "prop.test(rts_table, correct = FALSE)$conf.int" in code_of(section("catalog/06-two-unpaired-groups.html", "exercises"))


def test_logistic_warning_does_not_read_the_shape_off_open_ended_bands(site):
    """The over-72-hours band is open-ended, and a straight line already predicts its rate."""
    warning = text_of(section("catalog/11-predict-from-one.html", "logistic-regression").select_one("div.callout-warning"))
    assert "suggests otherwise" not in warning and "17.2% from the model, 18.2% observed" in warning


def test_pearson_warning_gives_the_trend_at_high_torsion(site):
    """Review B13: grouping by CT alone gave 7.0° in 8 hips; Bland and Altman (1995) group by the average of the two methods."""
    warning = text_of(section("catalog/10-association.html", "pearson").select_one("div.callout-warning"))
    assert "averaged 7.0° lower" not in warning
    assert "Grouped by the average of the two readings" in warning
    assert "1.3° lower in the 65 hips from 5° to 25°, and 3.5° lower in the 6 hips over 25°" in warning
    box = section("catalog/10-association.html", "pearson").select_one("div.callout-warning")
    assert "np." not in code_of(box)   # numpy is imported only in the collapsed box, which readers may skip


def test_cox_events_rule_matches_page_14(site):
    warning = text_of(section("catalog/11-predict-from-one.html", "cox").select_one("div.callout-warning"))
    assert "about three terms" in warning
    assert "per coefficient the model estimates" in warning and "too strict" in warning   # review C3


# ---- content review of 20.11.2026: pages 10 to 12 -----------------------------

def test_pearson_warning_says_r_depends_on_the_range(site):
    """Review B13 (Bland and Altman 1986): the same two methods give a lower r in a narrow sample."""
    warning = text_of(section("catalog/10-association.html", "pearson").select_one("div.callout-warning"))
    assert "Over all 80 hips r = 0.86; in the 30 hips with 10° to 20° on CT it is 0.53" in warning
    assert "(the first lines of the code below)" in warning   # golden rule 22: the numbers point to their code
    assert "a lower r in a sample with a narrow range" in warning


def test_expected_count_rule_gives_the_cautious_and_the_usual_version(site):
    """Review B24: "every expected count at least 5" is the cautious rule, not a requirement."""
    text = text_of(section("catalog/10-association.html", "contingency-coefficients"))
    assert "needs every expected count to be at least 5" not in text
    assert "attributed to Cochran" in text and "no more than 20% of the expected counts below 5, and none below 1" in text


def test_linear_regression_shows_the_two_intervals_at_one_bmi(site):
    """Review B14: the CI for the mean at BMI 30 against the prediction interval for one patient."""
    found = section("catalog/11-predict-from-one.html", "linear-regression")
    text, code = text_of(found), code_of(found)
    assert 'interval = "confidence"' in code and 'interval = "prediction"' in code and "get_prediction" in code
    assert "82.7 to 85.1 minutes" in text and "55.0 to 112.7 minutes" in text and "prediction interval" in text
    assert "is estimated to lie" in text   # an interval estimate, not a certainty
    warning = text_of(found.select_one("div.callout-warning"))
    assert "by about 15 minutes either way" not in warning
    assert "the standard deviation of the residuals" in warning and "67.2%" in warning


def test_linear_regressions_check_the_residuals(site):
    """Review B15: page 11 asks for roughly normal residuals, so it shows them; page 12 shows its model's residuals."""
    page_11 = code_of(section("catalog/11-predict-from-one.html", "linear-regression"))
    assert "geom_qq" in page_11 and "probplot" in page_11
    page_12 = code_of(section("catalog/12-predict-from-several.html", "multiple-linear-regression"))
    assert "resid(time_model)" in page_12 and "time_model.resid" in page_12


def test_nonparametric_regression_is_chosen_by_the_residuals(site):
    """Review B15: linear regression assumes normal residuals, not a normal outcome."""
    page = "catalog/11-predict-from-one.html"
    assert "a measurement that isn't normal" not in text_of(load(page))
    assert "residuals around a straight line aren't roughly normal" in text_of(load(page).select_one("main"))
    for anchor in ["linear-regression", "nonparametric-regression"]:
        assert "residuals of a straight-line fit aren't roughly normal" in text_of(section(page, anchor)), anchor


@pytest.mark.parametrize("page,anchors", [
    ("catalog/11-predict-from-one.html", ["logistic-regression", "cox"]),
    ("catalog/12-predict-from-several.html", ["multiple-linear-regression", "multiple-logistic-regression", "cox"]),
])
def test_events_rule_counts_coefficients_as_page_14_does(site, page, anchors):
    """Review C3: page 14 counts about 10 events per coefficient; pages 11 and 12 said per predictor."""
    assert "per predictor" not in text_of(load(page))
    for anchor in anchors:
        text = text_of(section(page, anchor))
        assert "per coefficient the model estimates" in text, anchor
        if anchor != "multiple-linear-regression":   # the abstracts that find it too strict are about logistic and Cox models
            assert "too strict" in text, anchor
    if page.startswith("catalog/12-"):
        logistic = text_of(section(page, "multiple-logistic-regression"))
        assert "about 17 coefficients" in logistic and "about 17 predictors" not in logistic
        assert "allows one coefficient, two at a stretch" in text_of(section(page, "exercises"))


def test_multiple_regression_says_which_coefficients_are_findings(site):
    """Review C4 (Westreich and Greenland 2013): the covariates' coefficients are adjustments, not findings."""
    page = "catalog/12-predict-from-several.html"
    linear = section(page, "multiple-linear-regression")
    assert "adjustments, not findings" in text_of(linear)
    results = [text_of(p) for p in linear.select("blockquote p") if text_of(p).startswith("Results:")]
    assert results and "1.27 minutes" in results[0] and "6.74" not in results[0] and "per year" not in results[0]
    assert "describe prediction, not each factor's own effect" in text_of(section(page, "multiple-logistic-regression"))
    # "When to use it" must not promise each predictor's own effect, which the effect-size step then takes back.
    assert "the effect of each of several predictors" not in text_of(load(page))
    assert "you want the effect of one predictor with the others taken into account" in text_of(linear)
    assert "you want one predictor's hazard ratio" in text_of(section(page, "cox"))


def test_multiple_linear_regression_names_the_equal_slopes_assumption(site):
    """Review B9: the model as written gives BMI one slope for every group; an interaction term lets it differ."""
    page = "catalog/12-predict-from-several.html"
    found = section(page, "multiple-linear-regression")
    assert "the same BMI slope for hips and knees" in text_of(found)
    assert "glossary.html#interaction" in [target(page, a["href"]) for a in found.select("a[href]")]
    # Review B9: the sentence carries page 14's two rules, not just a link to them.
    assert "and not for anything that predictor itself causes" in text_of(found)


def test_adjusted_cox_shift_is_not_read_as_confounding(site):
    """Review C5: a hazard ratio shifts a bit when a strong predictor is added, even without confounding (page 14)."""
    text = text_of(section("catalog/12-predict-from-several.html", "cox"))
    assert "so adjustment shouldn't change much" not in text
    assert "even without confounding" in text and "from 3.07 to 3.19" in text
