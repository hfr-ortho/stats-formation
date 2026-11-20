"""Part 4 · Beyond the table: post-hoc tests, mixed models, agreement (spec section 4, pages 15-17).
tests/site/test_free_form.py checks what every free-form page shares."""

import re

import pytest
from bs4 import BeautifulSoup

from sitelib import SITE_ROOT, code_of, load, section, target, text_of

POST_HOC = "beyond/15-post-hoc.html"
MIXED = "beyond/16-mixed-models.html"
AGREEMENT = "beyond/17-agreement.html"


# ---- page 15: post-hoc tests and multiple comparisons ----------------------------

def test_adjustments_are_compared_side_by_side(site):
    found = section(POST_HOC, "adjusting-p-values")
    text = text_of(found)
    for name in ["Bonferroni", "Holm", "Benjamini-Hochberg", "false discovery rate", "family-wise"]:
        assert name in text or name in text_of(section(POST_HOC, "why-adjust")), name
    outputs = [out.get_text() for out in found.select(".cell-output")]
    assert sum(all(column in out for column in ["bonferroni", "holm", "bh"]) for out in outputs) == 2   # R and Python


# Spec section 4, page 15, plus the follow-ups pages 9 and 13 promise.
FOLLOW_UPS = {
    "after-anova": ["TukeyHSD(", "pairwise_tukeyhsd(", "games_howell_test(", "pairwise_gameshowell("],
    "after-kruskal-wallis": ["dunn_test(", "posthoc_dunn("],
    "after-chi-square": ["pairwise_fisher_test(", "fisher_exact("],
    "after-repeated-measures-anova": ["pairwise_t_test(", "pairwise_tests("],
    "after-friedman": ["pairwise_wilcox_test(", "frdAllPairsConoverTest(", "wilcoxon(", "posthoc_conover_friedman("],
    "after-cochran-q": ["mcnemar.test(", "mcnemar("],
    "after-log-rank": ["survdiff(", "pairwise_logrank_test("],
}


@pytest.mark.parametrize("anchor,calls", FOLLOW_UPS.items())
def test_each_overall_test_has_its_follow_up_in_both_languages(site, anchor, calls):
    found = section(POST_HOC, anchor)
    code = code_of(found)
    assert [call for call in calls if call not in code] == []
    assert "holm" in code.lower() or anchor == "after-anova"     # Tukey and Games-Howell adjust themselves


def test_the_overall_test_is_not_a_gate(site):
    """Settles the Phase 3b question: adjusted post-hoc methods don't need a significant overall test first."""
    text = text_of(section(POST_HOC, "overall-test-first"))
    assert "Fisher's least significant difference" in text and "don't need the gate" in text
    assert "p = 0.016" in text                       # the significant-overall, no-significant-pair example


def test_planned_and_exploratory_comparisons_are_distinguished(site):
    text = text_of(section(POST_HOC, "planned-comparisons"))
    assert "pre-specified" in text and "exploratory" in text


# ---- page 16: mixed models ---------------------------------------------------------

def test_mixed_model_page_counts_what_repeated_measures_anova_drops(site):
    text = text_of(section(MIXED, "why-mixed-models"))
    assert "192 knees" in text and "138 knees (138 / 330 = 42%)" in text
    for kind in ["Missing completely at random", "Missing at random", "Missing not at random"]:
        assert kind in text, kind


def test_random_intercept_and_marginal_means_in_both_languages(site):
    code = code_of(section(MIXED, "random-intercept")) + code_of(section(MIXED, "estimated-marginal-means"))
    for call in ["lmer(", "(1 | case_id)", "mixedlm(", "emmeans(", "marginal_means("]:
        assert call in code, call
    assert "Satterthwaite" in text_of(section(MIXED, "random-intercept"))


def test_time_is_shown_as_categories_and_as_a_curve(site):
    code = code_of(section(MIXED, "time"))
    assert "ns(visit_days" in code and "cr(visit_days" in code


def test_group_by_time_tests_the_interaction(site):
    found = section(MIXED, "group-by-time")
    text = text_of(found)
    assert "visit:arm" in text and "efas" in code_of(found)
    warning = text_of(found.select_one("div.callout-warning"))
    assert "doesn't say the boot is better" in warning and "doesn't show the arms are the same" in warning


def test_differences_between_arms_are_adjusted_across_visits(site):
    """emmeans adjusts inside each by group, where there's one contrast, so Holm needs by = NULL."""
    assert 'by = NULL, adjust = "holm"' in code_of(section(MIXED, "group-by-time"))


def test_bilateral_patients_get_a_nested_model_and_a_pointer(site):
    found = section(MIXED, "bilateral")
    assert "(1 | patient_id/case_id)" in text_of(found)
    assert any(a["href"].endswith("survival/14-cox-regression.html#stratified-cox") for a in found.select("a[href]"))


# ---- page 17: agreement and reliability ----------------------------------------------

def test_icc_form_is_named_and_interpreted_with_koo_and_li(site):
    text = text_of(section(AGREEMENT, "icc"))
    for phrase in ["two-way random", "absolute agreement", "single", "Koo and Li", "ICC(A,1)"]:
        assert phrase in text, phrase


def test_icc_box_says_random_and_mixed_give_the_same_number(site):
    """Two-way random and two-way mixed share one formula (Koo and Li 2016); only who the result applies to differs (review A9)."""
    box = next(c for c in section(AGREEMENT, "icc").select("div.callout-warning") if "always say which ICC" in text_of(c))
    assert "give the same number for the same definition and type" in text_of(box)
    assert "each knee is read by a different set of raters" in text_of(section(AGREEMENT, "icc"))
    assert "for every model" not in text_of(load(AGREEMENT))


def test_inter_and_intra_rater_reliability_are_both_measured(site):
    assert "inter-rater" in text_of(section(AGREEMENT, "icc"))
    text = text_of(section(AGREEMENT, "inter-intra-rater"))
    assert "intra-rater" in text.lower() and "0.915" in text


def test_bland_altman_plot_and_limits_in_both_languages(site):
    found = section(AGREEMENT, "bland-altman")
    plotted = [tabset for tabset in found.select("div.panel-tabset")
               if all(pane.select("img") for pane in tabset.select("div.tab-pane"))]
    assert plotted, "the Bland-Altman plot is drawn in both languages"
    assert "limits of agreement" in text_of(found).lower() and "−2.74° to 3.74°" in text_of(found)


def test_kappa_and_weighted_kappa_with_ordered_categories(site):
    found = section(AGREEMENT, "kappa")
    code = code_of(found)
    assert "CohenKappa(" in code and "cohens_kappa(" in code and "Equal-Spacing" in code and 'wt="linear"' in code
    assert "alphabetically" in text_of(found)


# ---- links into pages 15-17 ----------------------------------------------------------

# Where a sentence promises one topic ("compare the visits with paired tests ... page 15"),
# its link lands on that section, not the top of the page.
SECTION_LINKS = {
    "foundations/03-distributions.html": ["beyond/16-mixed-models.html#bilateral"],
    "catalog/07-two-paired-groups.html": ["beyond/16-mixed-models.html#why-mixed-models",
                                          "beyond/17-agreement.html#bland-altman"],
    "catalog/08-three-plus-unmatched.html": ["beyond/15-post-hoc.html#after-anova", "beyond/15-post-hoc.html#after-kruskal-wallis",
                                             "beyond/15-post-hoc.html#after-chi-square", "beyond/15-post-hoc.html#overall-test-first"],
    "catalog/09-three-plus-matched.html": ["beyond/15-post-hoc.html#after-repeated-measures-anova",
                                           "beyond/15-post-hoc.html#after-friedman", "beyond/15-post-hoc.html#after-cochran-q",
                                           "beyond/16-mixed-models.html#why-mixed-models"],
    "catalog/10-association.html": ["beyond/17-agreement.html#bland-altman"],
    "catalog/11-predict-from-one.html": ["beyond/16-mixed-models.html#random-intercept"],
    "catalog/12-predict-from-several.html": ["beyond/16-mixed-models.html#random-intercept"],
    "survival/13-kaplan-meier.html": ["beyond/15-post-hoc.html#after-log-rank"],
}


def beyond_links(page):
    return [target(page, a["href"]) for a in load(page).select("main a[href]") if "beyond/1" in a["href"]]


@pytest.mark.parametrize("page,targets", SECTION_LINKS.items())
def test_links_into_pages_15_to_17_land_on_the_section_they_promise(site, page, targets):
    assert [target for target in targets if target not in beyond_links(page)] == []


@pytest.mark.parametrize("page", SECTION_LINKS)
def test_no_link_into_pages_15_to_17_stops_at_the_top_of_the_page(site, page):
    assert [href for href in beyond_links(page) if "#" not in href] == []


def test_post_hoc_tests_are_no_longer_gated_on_the_overall_test(site):
    """Phase 3b's deferred question, settled on page 15: adjusted post-hoc tests don't need a significant overall test."""
    found = section("catalog/08-three-plus-unmatched.html", "which-groups-differ")
    assert "Only run post-hoc tests when the overall test is significant" not in text_of(found)
    assert "none of them needs a significant overall test first" in text_of(found)
    assert any(a["href"].endswith("beyond/15-post-hoc.html#overall-test-first") for a in found.select("a[href]"))


# ---- final review fixes ----------------------------------------------------------------

def test_page_16_names_its_planned_comparison_instead_of_leaving_three_unadjusted(site):
    found = section(MIXED, "estimated-marginal-means")
    assert 'adjust = "none"' not in code_of(found) and '"1yr - preop" = c(-1, 0, 0, 1)' in code_of(found)
    methods = next(text_of(q) for q in section(MIXED, "reporting").select("blockquote") if "Methods:" in text_of(q))
    assert "The planned comparison was the change from before surgery to 1 year" in methods
    assert "you didn't plan" in text_of(section(POST_HOC, "overall-test-first"))


def test_holm_description_reproduces_the_table_above_it(site):
    text = text_of(section(POST_HOC, "adjusting-p-values"))
    assert "can't be smaller than the one before it" in text and "takes 0.044" in text


def test_bmi_exercise_answer_names_the_least_certain_pairs(site):
    text = text_of(section(POST_HOC, "exercises"))
    assert "The smallest steps" not in text and "least certain" in text
    assert "protects against any false positive" not in text


def test_post_hoc_results_say_where_the_other_pairs_are(site):
    for anchor in ["after-anova", "planned-comparisons"]:
        results = " ".join(text_of(q) for q in section(POST_HOC, anchor).select("blockquote"))
        assert "Table 2 gives all six pairwise comparisons" in results, anchor
    assert "3.07 (95% CI 1.85 to 5.09" in text_of(section(POST_HOC, "after-log-rank"))


def test_mixed_model_page_states_its_arithmetic_and_missingness_correctly(site):
    text = text_of(load(MIXED))
    assert "8.8² = 78.1" not in text and "8.84² = 78.1" in text
    assert "boot led by 3.6 points" in text
    assert "missed completely at random" not in text and "almost entirely at random" in text
    assert "as long as the model describes how a knee's scores are related" in text


def test_agreement_reporting_gives_every_ci_and_says_whose_readings(site):
    found = section(AGREEMENT, "reporting")
    quotes = " ".join(text_of(q) for q in found.select("blockquote"))
    assert "(95% CI −3.48° to −2.00°)" in quotes and "(95% CI 3.00° to 4.48°)" in quotes
    assert "rater 1's intra-rater ICC" in quotes and "each rater's first reading" in quotes
    assert "κ = 0.58 (95% CI 0.44 to 0.73)" in quotes and "weighted κ = 0.73 (95% CI 0.58 to 0.87)" in quotes


def test_scikit_learn_kappa_ordering_trap_is_named(site):
    text = text_of(section(AGREEMENT, "kappa"))
    assert "cohen_kappa_score()" in text and "labels=" in text


# ---- deferred Phase 5 minors ---------------------------------------------------------

def test_conover_p_values_are_printed_in_full_in_both_languages(site):
    """Printing R's test object shows every p-value as "<2e-16", so nobody could see that R and Python agree."""
    shown = " ".join(pre.get_text() for pre in section(POST_HOC, "after-friedman").select(".cell-output pre"))
    assert "<2e-16" not in shown
    assert len(re.findall(r"1\.4[23]\d*e-41", shown)) >= 3   # R's table once, Python's symmetric table twice


def test_post_hoc_follow_ups_pick_up_page_9s_new_examples(site):
    code = code_of(section(POST_HOC, "after-repeated-measures-anova"))
    assert "promis_pf" in code and "vr12" not in code
    found = section(POST_HOC, "after-friedman")
    assert "efas" in code_of(found) and "prom_score" not in code_of(found)
    assert "50 patients" in text_of(found)


def test_false_positive_example_says_pairwise_tests_are_not_independent(site):
    """1 − 0.95^6 = 26% is for six independent tests; six pairwise comparisons of four groups give about 20%."""
    text = text_of(section(POST_HOC, "why-adjust"))
    assert "aren't independent" in text and "about 20%" in text


def test_interaction_results_give_the_marginal_means_with_cis(site):
    """Page 16's ⚠️ box says an interaction is read through the EMMs and their CIs."""
    results = " ".join(text_of(q) for q in section(MIXED, "reporting").select("blockquote"))
    assert "17.3 (95% CI 16.6 to 18.1) with a boot" in results and "13.8 (95% CI 13.0 to 14.5) with a cast" in results
    assert "Holm-adjusted p = 0.898" in results


def test_agreement_example_is_a_systematic_offset(site):
    text = text_of(section(AGREEMENT, "reliability-vs-agreement"))
    assert "for some knees" not in text and "reads every knee 3° higher" in text


def test_dunn_controls_false_positives_only_with_holm(site):
    page_8 = text_of(section("catalog/08-three-plus-unmatched.html", "which-groups-differ"))
    page_15 = text_of(section(POST_HOC, "overall-test-first"))
    assert "Tukey's HSD, Dunn's test and Holm-adjusted" not in page_8
    assert "Dunn's test and any Holm-adjusted" not in page_15
    assert "once Holm's adjustment is applied" in page_8 and "once Holm's adjustment is applied" in page_15


def test_mixed_model_exercise_counts_joint_replacements_not_patients(site):
    before_exercise_3 = text_of(section(MIXED, "exercises")).split("Does pain change differently")[0]
    assert "patients" not in before_exercise_3 and "600 joint replacements" in before_exercise_3


def test_walking_aid_answer_gives_counts_with_percentages(site):
    text = text_of(section(POST_HOC, "exercises"))
    # The counts are procedures (both sides of a bilateral patient count), so the sentence says where an aid "was used".
    assert re.search(r"a walking aid was used in \d+ \(58\.8%\) at 6 weeks, \d+ \(25\.2%\) at 3 months and \d+ \(10\.7%\)", text)


def test_log_rank_box_says_lifelines_needs_a_tighter_convergence_setting(site):
    box = next(text_of(c) for c in section(POST_HOC, "after-log-rank").select(".callout") if "R vs Python" in text_of(c))
    assert "precision" in box and "stops iterating slightly early" in box


def test_after_chi_square_no_longer_points_to_page_8s_old_exercise(site):
    """Page 8's exercise 3 moved to the ACL data; page 15 introduces its ASA example itself."""
    text = text_of(section("beyond/15-post-hoc.html", "after-chi-square"))
    assert "Page 8's exercise 3" not in text
    assert "Take 90-day complications across the four ASA classes" in text


def test_agreement_page_is_framed_as_osteotomy_planning(site):
    text = text_of(load(AGREEMENT))
    assert "osteotomy" in text and "planned correction" in text


def test_post_hoc_box_says_only_joint_replacement_examples_use_every_case(site):
    assert "the joint replacement examples use every case" in text_of(load(POST_HOC))


# ---- content review of 20.11.2026, Task 3.7 ------------------------------------------

def test_tukey_paragraph_says_what_page_8_says_about_welch_and_the_spreads(site):
    """C1: Welch's ANOVA is the safe default; the SD rule is a rule of thumb for a judgment, never a test."""
    text = text_of(section(POST_HOC, "after-anova"))
    assert "When they don't (the largest" not in text
    assert "Welch's ANOVA, the safe default, especially when the group sizes are unequal" in text
    assert "never with a test of the variances" in text and "page 8's rule of thumb" in text
    assert "Two of this example's four classes are under 50 (36 patients in ASA 1 and 18 in ASA 4" in text


def test_dividing_the_threshold_is_the_same_decision_as_multiplying_the_p_value(site):
    """B19: papers often write "significance was set at 0.05/6"; the page shows it is the same decision."""
    text = text_of(section(POST_HOC, "adjusting-p-values"))
    assert "0.05 / 6 = 0.0083" in text and "the same decision" in text


def test_holm_and_tukey_disagreement_on_asa_1_against_2_is_explained(site):
    """B19: p = 0.044 with Holm, 0.096 with Tukey, for the same comparison."""
    text = text_of(section(POST_HOC, "after-anova"))
    assert "Holm and Tukey disagree about ASA 1 vs 2" in text
    assert "treats all six pairs alike" in text and "choose the method before you look at the p-values" in text


def test_dunnetts_test_is_named_apart_from_dunnetts_t3(site):
    """B19: Dunnett's test compares each group with one control (DescTools and PMCMRplus help pages)."""
    text = text_of(section(POST_HOC, "after-anova"))
    assert "Dunnett's test, a different test that compares each group with one control group" in text


def test_repeated_measures_follow_up_points_to_the_mixed_model(site):
    """C13: page 15 keeps only complete cases; page 16 explains why that can bias the result."""
    found = section(POST_HOC, "after-repeated-measures-anova")
    links = [target(POST_HOC, a["href"]) for a in found.select("a[href]")]
    assert "beyond/16-mixed-models.html#why-mixed-models" in links
    assert "beyond/16-mixed-models.html#estimated-marginal-means" in links


def test_hazard_ratio_cis_beside_holm_p_values_are_called_unadjusted(site):
    """B5: the Cox CIs are unadjusted; Holm's adjustment changes only the p-values."""
    assert "These are unadjusted 95% CIs" in text_of(section(POST_HOC, "after-log-rank"))


def test_mixed_model_cis_beside_holm_p_values_are_called_unadjusted(site):
    """B5: confint() prints "Confidence level used: 0.95" with no adjustment line."""
    assert "The CIs of the differences are unadjusted 95% CIs in both tabs" in text_of(section(MIXED, "group-by-time"))
    methods = [text_of(q) for q in section(MIXED, "reporting").select("blockquote") if "Methods:" in text_of(q)]
    assert any("reported with unadjusted 95% CIs and Holm-adjusted p-values" in m for m in methods)


def test_random_intercept_model_states_its_assumptions_and_shows_the_residuals(site):
    """B15: what the model assumes, and one residual plot drawn in both languages."""
    found = section(MIXED, "random-intercept")
    text = text_of(found)
    assert "What the model assumes" in text and "the same spread at every visit" in text
    assert "whichever two visits they come from" in text
    plotted = [tabset for tabset in found.select("div.panel-tabset")
               if all(pane.select("img") for pane in tabset.select("div.tab-pane"))]
    assert plotted, "the residual plot is drawn in both languages"


def test_random_slope_is_defined_and_the_page_says_why_this_model_has_none(site):
    text = text_of(section(MIXED, "random-intercept"))
    assert "random slope" in text and "its own rate of change as well as its own level" in text
    assert "lme4 stops with an error" in text


def test_random_intercept_is_an_overall_level_not_a_baseline(site):
    """The random intercept shifts all four visits, not only the pre-operative score."""
    text = text_of(load(MIXED))
    assert "baseline level" not in text and "its own overall level, at every visit" in text


def test_one_way_icc_does_not_fit_a_design_with_the_same_raters(site):
    """Koo and Li give a two-way model when the same raters measure every subject."""
    text = text_of(section(AGREEMENT, "icc"))
    assert "rarely the right model" not in text and "that design calls for a two-way model" in text


def test_german_one_way_icc_says_each_knee_has_its_own_raters(site):
    page = BeautifulSoup((SITE_ROOT / "de" / AGREEMENT).read_text(encoding="utf-8"), "html.parser")
    assert "von jeweils anderen Beurteilenden" in text_of(page.select_one("section#icc"))


def test_limits_of_agreement_state_the_normality_assumption(site):
    """Bland and Altman 1986: 95% of differences lie between the limits if the differences are normal."""
    text = text_of(section(AGREEMENT, "bland-altman"))
    assert "For 95% of knees" not in text and "for 95% of knees" not in text
    assert "about 95% of knees, if the differences are roughly normal" in text
    assert "3 of the 60 points (5%) lie outside the dashed lines" in text


def test_kappa_box_shows_that_kappa_depends_on_prevalence(site):
    """B11: the same 90% agreement gives kappa 0.80 or 0.44 (Feinstein and Cicchetti 1990, abstract)."""
    found = section(AGREEMENT, "kappa")
    box = next(c for c in found.select("div.callout-warning") if "how common each category is" in text_of(c))
    text = text_of(box)
    assert "kappa is 0.80 in the first and 0.44 in the second" in text
    assert "may not be comparable" in text and "Report the raw agreement and the table beside kappa" in text
    assert "conventions" in text
    assert "DescTools::CohenKappa(common)" in code_of(box) and "cohens_kappa(common)" in code_of(box)
    assert "the same raters reach" not in text and "two made-up pairs of raters" in text


def test_standard_error_of_measurement_and_smallest_detectable_change(site):
    """B20: de Vet et al. 2006: SEM for agreement from the variance components; SDC = 1.96 × √2 × SEM."""
    text = text_of(section(AGREEMENT, "bland-altman"))
    assert "smallest detectable change" in text and "1.96 × √2 × SEM" in text
    assert "SEM = 1.21°" in text and "SDC = 3.36°" in text
    assert "routinely" not in text


# ---- content review of 20.11.2026, Task 3.7, review fix round 1 -------------------------

def test_threshold_sentence_says_what_stays_above_it(site):
    assert "stays above the threshold either way" in text_of(section(POST_HOC, "adjusting-p-values"))


def test_tukey_paragraph_points_to_page_8s_plot(site):
    found = section(POST_HOC, "after-anova")
    assert "judge them from page 8's plot" in text_of(found)
    links = [target(POST_HOC, a["href"]) for a in found.select("a[href]") if "plot" in a.get_text()]
    assert links == ["catalog/08-three-plus-unmatched.html#one-way-anova"]


def test_residual_spread_is_compared_across_visits_not_with_the_model_sd(site):
    text = text_of(section(MIXED, "random-intercept"))
    assert "three assumptions that matter here" in text
    assert "Compare these four with each other, not with the model's residual SD of 8.6" in text


def test_random_slope_box_says_statsmodels_fits_what_lme4_refuses(site):
    found = section(MIXED, "random-intercept")
    box = next(c for c in found.select(".callout") if "a random slope per visit" in text_of(c))
    text = text_of(box)
    assert "number of observations (=1146) <= number of random effects (=1320)" in text
    assert "no reason to trust a random slope" in text


def test_unadjusted_cis_bullet_names_what_each_language_does(site):
    text = text_of(section(MIXED, "group-by-time"))
    assert "± 1.96 × se" in text and "multipletests" in text


def test_cpak_cross_table_is_printed_and_reported(site):
    found = section(AGREEMENT, "kappa")
    first = found.select("div.panel-tabset")[0]
    assert "table(R1 = cpak$R1, R2 = cpak$R2)" in code_of(first) and "print(cpak_table)" in code_of(first)
    results = " ".join(text_of(q) for q in section(AGREEMENT, "reporting").select("blockquote"))
    assert "40 of 60 knees (66.7%)" in results


def test_sem_is_told_apart_from_the_standard_error_of_the_mean(site):
    found = section(AGREEMENT, "bland-altman")
    text = text_of(found)
    assert "not the standard error of the mean" in text
    assert "catalog/04-describe-one-group.html#mean-sd" in [target(AGREEMENT, a["href"]) for a in found.select("a[href]")]
    assert "by different raters" in text and "in the measurement's own units (here degrees)" in text


def test_limits_conclusion_comes_before_the_sem_paragraph(site):
    text = text_of(section(AGREEMENT, "bland-altman"))
    assert text.index("Whether limits of −2.7° to 3.7° are good enough") < text.index("Standard error of measurement and smallest")


def test_sem_and_sdc_are_printed_rounded_in_python(site):
    shown = " ".join(pre.get_text() for pre in section(AGREEMENT, "bland-altman").select(".cell-output pre"))
    assert "1.21284788823662" not in shown and "1.212848 3.361843" in shown
