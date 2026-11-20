"""The three languages (HFR spec §4.3): the same pages everywhere, each with its own sidebar and `lang`,
stubs that lead back to English, top-bar language links, and a root page that works without JavaScript."""

from bs4 import BeautifulSoup

from sitelib import LANGS, PAGES, ROOT, SITE_ROOT, target, text_of

STUB_MARK = {"de": "(in Vorbereitung)", "fr": "(en préparation)"}   # kept for pages added later
WARNING = {"en": "SYNTHETIC DATA", "de": "SYNTHETISCHE DATEN", "fr": "DONNÉES SYNTHÉTIQUES"}
HOME_LINKS = {"getting-started/setup.html", "getting-started/using-this-site.html", "getting-started/real-data.html",
              "foundations/01-tidy-data.html", "catalog/04-describe-one-group.html", "survival/13-kaplan-meier.html",
              "beyond/15-post-hoc.html", "report/18-example-report.html", "choose-a-test.html", "tests-a-z.html"}


def load_lang(lang, page):
    return BeautifulSoup((SITE_ROOT / lang / page).read_text(encoding="utf-8"), "html.parser")


def sources(lang):
    return sorted(str(p.relative_to(ROOT / lang)) for p in (ROOT / lang).rglob("*.qmd"))


def test_every_page_exists_in_every_language():
    for lang in ["de", "fr"]:
        assert sources(lang) == sources("en"), lang


def test_every_page_is_built_in_every_language(site):
    for lang in LANGS:
        assert [p for p in PAGES if not (SITE_ROOT / lang / p).exists()] == [], lang


def test_pages_declare_their_language(site):
    for lang in LANGS:
        assert (ROOT / lang / "_metadata.yml").read_text(encoding="utf-8").strip() == f"lang: {lang}"
        for page in PAGES:
            assert load_lang(lang, page).html.get("lang") == lang, f"{lang}/{page}"


def test_each_language_has_its_own_sidebar_in_the_same_order(site):
    def sidebar(lang, page):
        return [target(page, a["href"], lang) for a in load_lang(lang, page).select("#quarto-sidebar a.sidebar-link[href]")]

    english = sidebar("en", "index.html")
    assert set(PAGES) <= set(english)
    for lang in ["de", "fr"]:
        for page in ["index.html", "catalog/06-two-unpaired-groups.html"]:
            assert sidebar(lang, page) == english, f"{lang}/{page}"


def test_untranslated_pages_are_stubs_that_link_to_english(site):
    for lang, mark in STUB_MARK.items():
        for page in PAGES:
            if page == "index.html":
                continue
            soup = load_lang(lang, page)
            box = soup.select_one(".coming-soon")
            assert (mark in soup.title.get_text()) == (box is not None), f"{lang}/{page}"
            if box is not None:
                links = {target(page, a["href"], lang) for a in box.select("a[href]")}
                assert f"/en/{page}" in links, f"{lang}/{page} must link to the English page"


def test_french_is_finished(site):
    for page in PAGES:
        assert load_lang("fr", page).select_one(".coming-soon") is None, page
    assert "Traduction en cours" not in text_of(load_lang("fr", "index.html"))


def test_german_is_finished(site):
    for page in PAGES:
        assert load_lang("de", page).select_one(".coming-soon") is None, page
        assert "(in Vorbereitung)" not in load_lang("de", page).title.get_text(), page
    assert "Übersetzung in Arbeit" not in text_of(load_lang("de", "index.html"))


def test_home_pages_are_translated_and_link_the_same_pages(site):
    for lang in LANGS:
        soup = load_lang(lang, "index.html")
        assert soup.select_one(".coming-soon") is None, lang
        assert WARNING[lang] in text_of(soup.select_one("main")), lang
        links = {target("index.html", a["href"], lang) for a in soup.select("main a[href]")}
        assert HOME_LINKS <= links, f"{lang}: {sorted(HOME_LINKS - links)}"


def test_top_bar_links_every_language_home(site):
    for lang in LANGS:
        for page in ["index.html", "catalog/06-two-unpaired-groups.html"]:
            links = {a.get_text(strip=True): target(page, a["href"], lang)
                     for a in load_lang(lang, page).select("nav.navbar a.nav-link[href]")}
            for code in LANGS:
                expected = "index.html" if code == lang else f"/{code}/index.html"
                assert links.get(code.upper()) == expected, (lang, page, code)


def test_language_links_have_accessible_names(site):
    # Quarto keeps `aria-label` off text links in the navbar, so the switcher sets it in the browser
    # (its logic is tested in tests/python/test_lang_switch.py); here: every page ships the names.
    for lang in LANGS:
        html = (SITE_ROOT / lang / "index.html").read_text(encoding="utf-8")
        assert 'LANG_NAMES = { en: "English", de: "Deutsch", fr: "Français" }' in html, lang
        assert len(load_lang(lang, "index.html").select("nav.navbar a.nav-link")) >= 3


def test_root_page_offers_every_language_without_javascript(site):
    soup = BeautifulSoup((SITE_ROOT / "index.html").read_text(encoding="utf-8"), "html.parser")
    hrefs = {a["href"].removeprefix("./") for a in soup.select("main a[href]")}
    assert {"en/index.html", "de/index.html", "fr/index.html"} <= hrefs
    assert soup.select_one("#quarto-sidebar") is None


def test_every_page_includes_the_switcher(site):
    pages = sorted(p for p in SITE_ROOT.rglob("*.html") if "site_libs" not in p.parts)
    assert pages
    missing = [str(p.relative_to(SITE_ROOT)) for p in pages if 'id="lang-switch"' not in p.read_text(encoding="utf-8")]
    assert missing == []


def test_every_page_includes_the_glossary_script(site):
    pages = sorted(p for p in SITE_ROOT.rglob("*.html") if "site_libs" not in p.parts)
    missing = [str(p.relative_to(SITE_ROOT)) for p in pages if 'id="glossary-terms"' not in p.read_text(encoding="utf-8")]
    assert missing == []


def test_every_term_link_points_to_an_entry_of_its_own_language(site):
    for lang in LANGS:
        entries = {span["id"] for span in load_lang(lang, "glossary.html").select("dl dt span[id]")}
        assert entries, lang
        for page in PAGES:
            for a in load_lang(lang, page).select("a.term"):
                target, _, entry = a["href"].partition("#")
                assert target.endswith("glossary.html") and f"/{lang}/" in "/" + target.replace("../", ""), f"{lang}/{page}: {a['href']}"
                assert entry in entries, f"{lang}/{page}: no glossary entry '{entry}'"



def definition(lang, entry):
    """An entry's definition on a language's glossary page: the text the hover shows."""
    dt = load_lang(lang, "glossary.html").select_one(f"dl dt:has(span#{entry})")
    assert dt is not None, f"{lang}: no glossary entry '{entry}'"
    return text_of(dt.find_next_sibling("dd"))


# Words each corrected entry must carry in every language (content review of 20.11.2026, task 3.9).
CORRECTED_ENTRIES = {
    "log-rank-test": {"en": "Mantel-Haenszel calculation", "de": "Mantel-Haenszel-Rechnung", "fr": "calcul de Mantel-Haenszel"},
    "t-test": {"en": "on this site", "de": "auf dieser Website", "fr": "sur ce site"},
    "censored": {"en": "Competing risk", "de": "Konkurrierendes Risiko", "fr": "Risque concurrent"},
    "risk": {"en": "Kaplan-Meier", "de": "Kaplan-Meier", "fr": "Kaplan-Meier"},
    "score-test": {"en": "exact method", "de": "exakten Methode", "fr": "méthode exacte"},
    "odds-ratio": {"en": "not a risk ratio", "de": "kein relatives Risiko", "fr": "pas un risque relatif"},
    "statistical-significance": {"en": "confidence interval", "de": "Konfidenzintervall", "fr": "intervalle de confiance"},
    "false-negative": {"en": "beta", "de": "Beta", "fr": "bêta"},
    "reverse-kaplan-meier": {"en": "loss to follow-up", "de": "verloren", "fr": "perdu de vue"},
}


def test_corrected_glossary_entries_say_the_same_in_every_language(site):
    for entry, words in CORRECTED_ENTRIES.items():
        for lang, word in words.items():
            assert word in definition(lang, entry), (lang, entry, word)


def test_log_rank_entry_says_what_r_computes_and_what_the_source_says(site):
    """R's survdiff() and mantelhaen.test() on the event-time 2 x 2 tables give the same statistic (C8)."""
    text = definition("en", "log-rank-test")
    assert "R and lifelines compute it as the Mantel-Haenszel calculation" in text
    assert "nearly identical" in text and "(the Mantel-Haenszel test for survival data is nearly identical)" not in text


def test_t_test_entry_says_how_this_site_uses_students(site):
    text = definition("en", "t-test")
    assert "on this site it means the unpaired t test that assumes equal variances" in text, "C9"
    assert "Welch's" in text


def test_censored_entry_puts_death_with_the_competing_risk_and_names_the_assumption(site):
    text = definition("en", "censored")
    assert "or the patient died." not in text, "C10: death is censored only when it isn't the event studied"
    assert "died without the event, when death is not the event studied" in text
    assert "the same chance of a later event as those still being followed" in text


def test_risk_entry_says_when_the_simple_count_works(site):
    assert "only when every patient was followed for the whole period" in definition("en", "risk"), "B25"


def test_score_test_entry_says_when_it_equals_the_log_rank_test(site):
    text = definition("en", "score-test")
    assert "it is equivalent to the log-rank test." not in text, "B25: exact only without tied event times"
    assert "when no two events happen at the same time" in text


def test_odds_ratio_entry_warns_it_is_not_a_risk_ratio(site):
    assert "An odds ratio is not a risk ratio: it lies further from 1" in definition("en", "odds-ratio"), "B7"


def test_significance_entry_says_non_significance_is_not_no_difference(site):
    text = definition("en", "statistical-significance")
    assert "not statistically significant does not show that there is no difference" in text, "B8"
    assert "the significance level or alpha" in text


def test_false_negative_entry_names_beta_and_power(site):
    text = definition("en", "false-negative")
    assert "type II error" in text and "power is 1 minus beta" in text


def test_reverse_kaplan_meier_entry_leaves_the_deaths_to_the_methods(site):
    text = definition("en", "reverse-kaplan-meier")
    assert "being censored counts as the event" not in text, "page 13 censors deaths in the reverse analysis too"
    assert "a death can count either way" in text

def test_every_page_includes_the_report_link_script(site):
    pages = sorted(p for p in SITE_ROOT.rglob("*.html") if "site_libs" not in p.parts)
    assert pages
    missing = [str(p.relative_to(SITE_ROOT)) for p in pages if 'id="report-error"' not in p.read_text(encoding="utf-8")]
    assert missing == []


REPORT_LINK = {"en": "Report an error", "de": "Fehler melden", "fr": "Signaler une erreur"}


def test_getting_help_names_the_report_link_and_the_address(site):
    for lang in LANGS:
        help_text = text_of(load_lang(lang, "getting-started/using-this-site.html").select_one("section#getting-help"))
        assert REPORT_LINK[lang] in help_text, lang
        assert "soft-canoes2@icloud.com" in help_text, lang
        assert "github.com/hfr-ortho/stats-formation/issues" in str(
            load_lang(lang, "getting-started/using-this-site.html").select_one("section#getting-help")), lang
