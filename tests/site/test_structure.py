import re

from bs4 import BeautifulSoup
from sitelib import CELL_ANCHORS, PAGES, SITE_ROOT, load, target, text_of


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


def test_footer_says_synthetic_in_three_languages_and_credits_tjs(site):
    footer = text_of(load("index.html").select_one("footer"))
    assert "Synthetic data only · Nur synthetische Daten · Données synthétiques uniquement" in footer
    assert "Adapted from the TJS Statistics Tutorials" in footer


def test_footer_says_when_the_site_was_built(site):
    """The publish workflow puts the date and time in SITE_UPDATED; a build without it says "local build"."""
    stamp = re.compile(r"Last updated · Zuletzt aktualisiert · Dernière mise à jour: "
                       r"(\d\d\.\d\d\.\d{4}, \d\d:\d\d|local build, not published)")
    for page in ["index.html", "en/index.html", "de/glossary.html", "fr/catalog/06-two-unpaired-groups.html"]:
        soup = BeautifulSoup((SITE_ROOT / page).read_text(encoding="utf-8"), "html.parser")
        assert stamp.search(text_of(soup.select_one("footer"))), page
