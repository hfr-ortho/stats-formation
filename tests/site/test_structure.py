import re

from bs4 import BeautifulSoup
from sitelib import CELL_ANCHORS, PAGES, ROOT, SITE_ROOT, load, target


def test_every_page_is_built(site):
    missing = [p for p in PAGES if not (site / p).exists()]
    assert missing == []


def test_repo_files_are_not_published(site):
    for path in ["docs", "tests", "data-raw", "README.html", "CLAUDE.html", "scratch"]:
        assert not (SITE_ROOT / path).exists(), f"{path} must not be in the site"


def test_sidebar_links_every_page(site):
    hrefs = {target("index.html", a["href"]) for a in load("index.html").select("#quarto-sidebar a[href]")}
    missing = [p for p in PAGES if p not in hrefs]
    assert missing == []


def test_catalog_pages_have_every_cell_anchor(site):
    for page, anchors in CELL_ANCHORS.items():
        ids = {el["id"] for el in load(page).select("[id]")}
        missing = [a for a in anchors if a not in ids]
        assert missing == [], f"{page} is missing anchors {missing}"




def test_coming_soon_marking_is_consistent(site):
    for page in PAGES:
        soup = load(page)
        in_title = "(coming soon)" in soup.title.get_text()
        has_box = soup.select_one(".coming-soon") is not None
        assert in_title == has_box, f"{page}: title says {in_title}, box says {has_box}"



def test_every_page_carries_the_hfr_mark_in_the_top_bar(site):
    for page in PAGES:
        logos = load(page).select("img.navbar-logo")
        assert logos, page
        assert all(img["src"].endswith("images/hfr-mark-white.svg") for img in logos), page
        assert all(img.get("alt") == "HFR Hôpital fribourgeois" for img in logos), page
    assert (SITE_ROOT / "images" / "hfr-mark-white.svg").exists()


def test_the_browser_tab_shows_the_hfr_mark(site):
    icon = load("index.html").select_one('link[rel="icon"]')
    assert icon is not None and icon["href"].endswith("images/hfr-icon.svg")
    assert (SITE_ROOT / "images" / "hfr-icon.svg").exists()


# The footer (page-footer in _quarto.yml) holds each of its three parts once per language, in a span that names
# the language. styles.css hides the spans that aren't in the page's language. \u00a0 is the non-breaking space
# French takes before a colon.
FOOTER = {
    "en": ("Synthetic data only", "Last updated: ",
           "Adapted from the TJS Statistics Tutorials · Text CC BY 4.0 · Code MIT"),
    "de": ("Nur synthetische Daten", "Zuletzt aktualisiert: ",
           "Adaptiert nach den TJS Statistics Tutorials · Text CC BY 4.0 · Code MIT"),
    "fr": ("Données synthétiques uniquement", "Dernière mise à jour\u00a0: ",
           "Adapté des TJS Statistics Tutorials · Texte CC BY 4.0 · Code MIT"),
}
# One page per language, and the root page, which only sends visitors to a language and is marked English.
FOOTER_PAGES = {"index.html": "en", "en/index.html": "en", "de/glossary.html": "de",
                "fr/catalog/06-two-unpaired-groups.html": "fr"}
FOOTER_PARTS = ["left", "center", "right"]
# The publish workflow puts the date and time in SITE_UPDATED; a build without it says "local build".
BUILD_STAMP = r"(\d\d\.\d\d\.\d{4}, \d\d:\d\d|local build, not published)"


def footer_soup(page):
    return BeautifulSoup((SITE_ROOT / page).read_text(encoding="utf-8"), "html.parser")


def test_footer_reads_in_the_language_of_the_page(site):
    """What a reader sees: the spans in the page's language, which styles.css leaves showing."""
    for page, lang in FOOTER_PAGES.items():
        soup = footer_soup(page)
        assert soup.html["lang"] == lang, page
        shown = [soup.select_one(f'footer .nav-footer-{part} > p > span[lang="{lang}"]').get_text()
                 for part in FOOTER_PARTS]
        synthetic, updated, credit = FOOTER[lang]
        assert shown[0] == synthetic, page
        assert re.fullmatch(re.escape(updated) + BUILD_STAMP, shown[1]), page
        assert shown[2] == credit, page


def test_footer_holds_every_part_once_per_language_and_nothing_else(site):
    """Text outside a language span would show on every page, whatever its language."""
    for page in FOOTER_PAGES:
        soup = footer_soup(page)
        for part in FOOTER_PARTS:
            paragraphs = soup.select(f"footer .nav-footer-{part} > p")
            assert len(paragraphs) == 1, f"{page} {part}"
            spans = paragraphs[0].find_all("span", attrs={"lang": True}, recursive=False)
            assert [span["lang"] for span in spans] == ["en", "de", "fr"], f"{page} {part}"
            assert paragraphs[0].get_text() == "".join(span.get_text() for span in spans), f"{page} {part}"


def test_footer_credit_links_to_tjs_in_every_language(site):
    soup = footer_soup("en/index.html")
    for lang in FOOTER:
        links = soup.select(f'footer .nav-footer-right span[lang="{lang}"] a')
        assert [(a.get_text(), a["href"]) for a in links] == [
            ("TJS Statistics Tutorials", "https://total-joint-specialists.github.io/example-stats-analysis/")], lang


def test_stylesheet_shows_only_the_footer_in_the_language_of_the_page():
    css = " ".join((ROOT / "styles.css").read_text(encoding="utf-8").split())
    assert ".nav-footer span[lang] { display: none; }" in css
    shown = ", ".join(f'html[lang="{lang}"] .nav-footer span[lang="{lang}"]' for lang in FOOTER)
    assert shown + " { display: inline; }" in css
    # The hiding rule has to come first: the two have different weights, but the order keeps that plain.
    assert css.index(".nav-footer span[lang] { display: none; }") < css.index(shown)
