"""Part 3 · Survival analysis: Kaplan-Meier and Cox regression in full (spec section 4, pages 13-14).
tests/site/test_free_form.py checks what every free-form page shares."""

from sitelib import code_of, load, section, text_of

KM = "survival/13-kaplan-meier.html"
COX = "survival/14-cox-regression.html"


# ---- page 13: Kaplan-Meier and the log-rank test -----------------------------

def test_kaplan_meier_curves_show_numbers_at_risk_and_a_ci_band(site):
    found = section(KM, "kaplan-meier")
    code = code_of(found)
    assert "add_risktable(" in code and "add_confidence_interval()" in code and "add_at_risk_counts(" in code
    panes = found.select("div.panel-tabset div.tab-pane")
    assert len(panes) == 2 and all(pane.select("img") for pane in panes), "the curve is drawn in both languages"


def test_survivorship_is_reported_at_2_5_and_10_years_with_cis_and_numbers_at_risk(site):
    results = " ".join(text_of(q) for q in section(KM, "survivorship").select("blockquote"))
    for years in ["at 2 years", "at 5 years", "at 10 years"]:
        assert years in results, years
    assert results.count("95% CI") >= 3 and "remained at risk" in results


def test_median_follow_up_uses_reverse_kaplan_meier(site):
    found = section(KM, "follow-up")
    assert "reverse Kaplan-Meier" in " ".join(text_of(q) for q in found.select("blockquote"))
    assert "5.62 years" in text_of(found)


def test_log_rank_covers_two_groups_and_three_or_more(site):
    found = section(KM, "log-rank")
    outputs = " ".join(out.get_text() for out in found.select(".cell-output"))
    assert "on 1 degrees of freedom" in outputs and "on 2 degrees of freedom" in outputs
    assert "Mantel-Haenszel" in text_of(found)


def test_competing_risks_compare_the_cumulative_incidence_with_one_minus_km(site):
    text = text_of(section(KM, "competing-risks"))
    for phrase in ["Aalen-Johansen", "1 − Kaplan-Meier", "Gray's test", "Python has no mature implementation of Gray's test"]:
        assert phrase in text, phrase


# ---- page 14: Cox regression ---------------------------------------------------

def test_covariates_are_chosen_in_advance_with_enough_events(site):
    text = text_of(section(COX, "choosing-covariates"))
    assert "chosen before you look" in text and "10 events per term" in text


def test_proportional_hazards_are_checked_on_the_built_in_violation(site):
    found = section(COX, "proportional-hazards")
    assert "Schoenfeld" in text_of(found) and "cox.zph(" in code_of(found)
    plotted = [tabset for tabset in found.select("div.panel-tabset")
               if all(pane.select("img") for pane in tabset.select("div.tab-pane"))]
    assert plotted, "the residual plot is drawn in both languages"
    assert "approach" in code_of(plotted[0])


def test_remedies_cover_stratification_and_a_time_split(site):
    code = code_of(section(COX, "remedies"))
    for call in ["strata(approach)", 'strata=["approach"]', "survSplit(", "CoxTimeVaryingFitter("]:
        assert call in code, call


def test_stratified_cox_covers_matched_sets_and_bilateral_patients(site):
    found = section(COX, "stratified-cox")
    hrefs = [a["href"] for a in found.select("a[href]")]
    for target in ["07-two-paired-groups.html#stratified-cox", "09-three-plus-matched.html#stratified-cox"]:
        assert any(href.endswith(target) for href in hrefs), target
    code = code_of(found)
    assert "cluster = patient_id" in code and 'cluster_col="patient_id"' in code


def test_fine_gray_is_labeled_r_only(site):
    found = section(COX, "fine-gray")
    assert "(R only)" in found.select_one("h2").get_text()
    assert found.select("pre.r") and not found.select("pre.python")
    assert "subdistribution hazard ratio" in text_of(found)


def test_reporting_gives_univariable_and_multivariable_hazard_ratios(site):
    found = section(COX, "reporting")
    table = found.select_one("table")
    assert table is not None and "Univariable" in text_of(table) and "Multivariable" in text_of(table)
    assert "Univariable HR (95% CI)" in " ".join(out.get_text() for out in found.select(".cell-output"))


# ---- final review fixes ------------------------------------------------------

def test_reported_models_all_allow_for_bilateral_patients(site):
    """The Methods promise robust standard errors, so both columns of the table use them."""
    found = section(COX, "reporting")
    table = text_of(found.select_one("table"))
    assert "1.87, 5.04" in table and "1.92, 5.28" in table   # implant C, univariable and multivariable, clustered
    printed = " ".join(out.get_text() for out in found.select(".cell-output"))
    assert "3.07 (1.87 to 5.04)" in printed and "3.19 (1.92 to 5.28)" in printed
    methods = next(text_of(q) for q in found.select("blockquote") if "Methods:" in text_of(q))
    assert "In the Cox models, robust standard errors" in methods


def test_imprecise_estimates_are_not_described_as_effects(site):
    """Explanatory prose follows the same rule as the Results: no clear evidence isn't evidence of none."""
    for page, phrase in [(KM, "does worse early and better later"), (KM, "but the curves crossed"),
                         (COX, "Death doesn't depend on the implant"), (COX, "age barely changes"),
                         (COX, "a later one in the other direction")]:
        assert phrase not in text_of(load(page)), f"{page}: {phrase!r}"


def test_a_moving_hazard_ratio_is_not_proof_of_confounding(site):
    """Hazard ratios shift when a strong predictor is added, even without confounding."""
    text = text_of(section(COX, "univariable-multivariable"))
    assert "the covariates were confounding the unadjusted one" not in text
    assert "even without confounding" in text


def test_results_give_every_estimate_its_ci_and_every_count_its_percentage(site):
    km_results = " ".join(text_of(q) for q in section(KM, "competing-risks").select("blockquote"))
    assert "24.0% (95% CI 19.3% to 29.0%)" in km_results
    cox_results = " ".join(text_of(q) for q in section(COX, "reporting").select("blockquote"))
    assert "81 of 600 procedures (13.5%)" in cox_results


def test_cox_page_never_calls_one_minus_km_the_proportion_revised(site):
    """Page 13 warns never to call 1 − Kaplan-Meier the proportion revised when patients die (review A8)."""
    text = text_of(load(COX))
    assert "had been revised" not in text, "1 − Kaplan-Meier is an estimate with deaths censored, not the share revised"
    # review of Task 1.1: "the estimate of revision" was terse next to "the three risks"
    assert "estimate of the risk of revision (1 − Kaplan-Meier, with deaths censored)" in text
    code = code_of(load(COX))
    assert "revised by 5 years" not in code, "the code comments say what the prose says"
    assert code.count("Kaplan-Meier estimate of the risk of revision by 5 years, deaths censored") == 2


# ---- content review of 20.11.2026: contradictions and missing caveats, pages 13 and 14 ----------

def test_km_band_widens_only_at_revisions_and_most_late(site):
    """Review of Task 1.1: the band opens from zero at the first revisions, so "widens more when few
    remain" needs the middle years as its comparison (the wording page 4 uses)."""
    text = text_of(section(KM, "kaplan-meier"))
    assert "widens more when few procedures remain at risk" not in text
    assert "It widens at each revision and nowhere else" in text
    assert "each revision widens it more than one did in the middle years" in text


def test_km_tail_rule_says_the_page_runs_past_it_on_purpose(site):
    """Review C7 (decision D3): the page states the 10% rule, then reports 10 years with 21 at risk."""
    warning = text_of(section(KM, "kaplan-meier").select_one("div.callout-warning"))
    assert "A common rule of thumb" in warning
    assert "past that point on purpose" in warning
    assert "between 8 years (84 at risk in R's count) and 10 years (21)" in warning   # lifelines shows 83 (fix round 1)
    assert "the 7.9-year estimate carried forward" in warning


def test_km_python_survival_plots_use_the_whole_axis(site):
    """Review B12: R draws survival from 0 to 100%; the Python plots zoomed in on 0.6 to 1. set_ylim()
    returns the limits, and unnamed, reticulate prints them on the page (golden rule 10)."""
    for anchor in ["kaplan-meier", "log-rank"]:
        found = section(KM, anchor)
        assert "y_range = ax.set_ylim(0, 1)" in code_of(found), anchor
        outputs = " ".join(out.get_text() for out in found.select(".cell-output"))
        assert "(0.0, 1.0)" not in outputs, anchor


def test_median_follow_up_methods_say_deaths_were_censored(site):
    """Review B5: censoring deaths in the reverse Kaplan-Meier moves the answer (5.62 against 5.00 years)."""
    found = section(KM, "follow-up")
    methods = " ".join(text_of(q) for q in found.select("blockquote"))
    assert "reverse Kaplan-Meier method, censoring revisions and deaths." in methods
    text = text_of(found)
    assert "is wrong" not in text and "the median is 5.00 years" in text
    assert "misleading as a measure of follow-up" in text
    code = code_of(found)
    assert "event_status != 1" in code and code.count("misleading as follow-up") == 2


def test_approach_time_point_is_fixed_before_the_plot_is_read(site):
    """Review C6: the page says "decide your time points before you look", so the 6-month point is
    fixed in advance, on page 14's clinical grounds, before the reader looks at the plot."""
    text = text_of(section(KM, "log-rank"))
    assert "But look at the plot" not in text
    fixed = text.find("one time point was fixed in advance")
    assert 0 <= fixed < text.find("Now look at the plot")
    assert "the end of the period of highest dislocation risk after hip replacement" in text   # a time point ends a period (fix round 1)


def test_events_per_term_is_a_rule_of_thumb(site):
    """Review B24 (Peduzzi 1995; Vittinghoff and McCulloch 2007): a prudent rule, not a requirement."""
    text = text_of(section(COX, "choosing-covariates"))
    assert "needs about" not in text
    assert "A common rule of thumb is about 10 events per term" in text
    assert "some studies find it too strict" in text


def test_late_period_hazard_ratio_compares_survivors(site):
    """Review B17 (Hernán 2010): a period-specific hazard ratio compares the survivors of the earlier
    period, who are no longer like-for-like groups; Hernán suggests adjusted survival curves."""
    found = section(COX, "remedies")
    text = text_of(found)
    assert "compares only the hips still unrevised at 6 months" in text
    assert "a hazard ratio below 1 can then appear even without any late effect" in text
    # fix round 1: the mechanism is what tends to happen, not a finding about this cohort; the 0.43 rests on
    # 5 and 16 late revisions and its CI includes 1, so the page doesn't attribute it to selection
    assert "has by then lost" not in text
    assert "5 after the posterior approach and 16 after the anterior approach (the second output), and its CI includes 1" in text
    assert "The alternative this site uses is each group's survival at time points fixed in advance" in text
    assert "adjusted survival curves" in text and "Hernán (2010)" in text
    assert "restricted mean" not in text   # no source for it was opened
    hrefs = [a["href"] for a in found.select("a[href]")]
    assert any(href.endswith("13-kaplan-meier.html#log-rank") for href in hrefs)


def test_bilateral_paragraph_gives_the_real_reason(site):
    """Review B18: the practice data have no hidden patient factor linking a patient's two joints; the robust
    standard errors printed are about the same, so "too narrow" needs its condition and a "usually"."""
    text = text_of(section(COX, "stratified-cox"))
    assert "so the pairing matters little in this cohort" not in text
    assert "When a patient's two joints tend to fare alike, treating them as independent usually makes the" in text
    assert "each joint's revision time was drawn separately" in text
    # fix round 1: bilateral patients have two hips or two knees, and only hips get the posterior approach,
    # so "nothing makes a patient's two joints fail together" overstated what the generator does
    assert "nothing makes a patient's two joints fail together" not in text
    assert "no hidden patient factor, such as bone quality" in text
    assert "for implant B it is slightly larger (0.311 against 0.310)" in text
