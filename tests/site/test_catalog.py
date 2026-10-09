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

# Spec section 6, steps 2-7, as h3 headings in this order. Page 4 describes a
# group rather than testing it: its estimate and CI are the result, so it has
# no separate effect-size step.
ANATOMY = ["When to use it", "Look at the data first", "Run it", "Read the output",
           "Effect size and 95% CI", "How to report it"]
DESCRIBE = [step for step in ANATOMY if step != "Effect size and 95% CI"]

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
    assert steps == (DESCRIBE if page.startswith("catalog/04-") else ANATOMY)
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
}


@pytest.mark.parametrize("cell,source", MOVED_SECTIONS.items())
def test_moved_sections_teach_from_their_new_data(site, cell, source):
    dataset, column = source
    code = code_of(section(*cell))
    assert code.count(f'read_csv("{dataset}"') >= 2, f"{cell}: R and Python should both read {dataset}"
    assert column in code, f"{cell}: the code never uses {column}"


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
    found = section("catalog/06-two-unpaired-groups.html", "unpaired-t")
    report = " ".join(text_of(q) for q in found.select("blockquote"))
    assert "n = 57" in report and "n = 55" in report
    assert "112 of the 120 randomized patients" in text_of(found)


def test_wilcoxon_box_describes_page_6s_cis_correctly(site):
    """Page 6's two Hodges-Lehmann CIs agree since it moved to whole-number pain scores."""
    text = text_of(section("catalog/07-two-paired-groups.html", "wilcoxon-signed-rank"))
    assert "on page 6 they differ a little" not in text
    assert "as they do on page 6" in text


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


def test_unmatched_page_counts_procedures_not_patients(site):
    """Cohort rows are procedures (80 patients had both sides operated on), as on pages 4 and 5."""
    page = "catalog/08-three-plus-unmatched.html"
    assert re.findall(r"(?<!–)\b\d+ patients\b", text_of(load(page))) == ["80 patients"]   # not "ASA 3–4 patients"
    assert "Of 600 procedures" in text_of(section(page, "kruskal-wallis"))
    assert "30 of 264 procedures" in text_of(section(page, "exercises"))


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


def test_cox_warning_describes_the_cause_specific_hazard(site):
    """Censoring deaths gives the revision rate among patients still alive; it doesn't hide or create an age effect."""
    warning = text_of(section("catalog/11-predict-from-one.html", "cox").select_one("div.callout-warning"))
    assert "still alive" in warning and "hide an age effect" not in warning


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
    "catalog/12-predict-from-several.html": ["survival/14-cox-regression.html#proportional-hazards"],
}


@pytest.mark.parametrize("page,targets", SECTION_LINKS.items())
def test_links_into_the_survival_pages_land_on_the_section_they_promise(site, page, targets):
    hrefs = {target(page, a["href"]) for a in load(page).select("main a[href]")}
    assert [target for target in targets if target not in hrefs] == []
