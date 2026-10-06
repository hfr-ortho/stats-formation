"""The three languages (HFR spec §4.3): the same pages everywhere, each with its own sidebar and `lang`,
stubs that lead back to English, top-bar language links, and a root page that works without JavaScript."""

from bs4 import BeautifulSoup

from sitelib import LANGS, PAGES, ROOT, SITE_ROOT, target, text_of

STUB_MARK = {"de": "(in Vorbereitung)", "fr": "(en préparation)"}
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


def test_root_page_offers_every_language_without_javascript(site):
    soup = BeautifulSoup((SITE_ROOT / "index.html").read_text(encoding="utf-8"), "html.parser")
    hrefs = {a["href"].removeprefix("./") for a in soup.select("main a[href]")}
    assert {"en/index.html", "de/index.html", "fr/index.html"} <= hrefs
    assert soup.select_one("#quarto-sidebar") is None
