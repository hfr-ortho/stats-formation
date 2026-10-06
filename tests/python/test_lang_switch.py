"""The language switcher's logic (HFR spec §4.3), run in Node.js. What it does to a page in the browser
(rewriting the top-bar links, redirecting the root) is checked by hand in a preview."""

import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
NODE = shutil.which("node")
pytestmark = pytest.mark.skipif(NODE is None, reason="Node.js is not installed")


def script():
    html = (ROOT / "lang-switch.html").read_text(encoding="utf-8")
    return re.search(r'<script id="lang-switch">(.*?)</script>', html, re.DOTALL).group(1)


def run(expressions, setup=""):
    """Evaluate JavaScript expressions after loading the switcher outside a browser."""
    probe = setup + script() + f"\nconsole.log(JSON.stringify([{', '.join(expressions)}]));"
    out = subprocess.run([NODE, "-e", probe], capture_output=True, text=True, timeout=30)
    assert out.returncode == 0, out.stderr
    return json.loads(out.stdout)


def test_browser_language_with_a_region_picks_the_site_language():
    assert run(['pickLang(null, ["de-CH", "en"])', 'pickLang(null, ["fr-CH"])', 'pickLang(null, ["it-CH", "en-GB"])',
                'pickLang(null, ["it"])', 'pickLang(null, [])', 'pickLang(null, undefined)']) == \
        ["de", "fr", "en", "en", "en", "en"]


def test_a_stored_choice_wins_over_the_browser():
    assert run(['pickLang("fr", ["de-CH"])', 'pickLang("xx", ["de-CH"])']) == ["fr", "de"]


def test_switching_keeps_the_page_and_section_with_or_without_a_site_prefix():
    assert run(['switchHref("/stats-formation/de/catalog/06-two-unpaired-groups.html", "#mann-whitney", "fr")',
                'switchHref("/de/catalog/06-two-unpaired-groups.html", "#mann-whitney", "en")',
                'switchHref("/stats-formation/en/", "", "de")',
                'switchHref("/stats-formation/", "", "de")']) == \
        ["/stats-formation/fr/catalog/06-two-unpaired-groups.html#mann-whitney",
         "/en/catalog/06-two-unpaired-groups.html#mann-whitney",
         "/stats-formation/de/",
         None]


def test_home_of_the_current_language():
    assert run(['homeHref("/stats-formation/fr/catalog/x.html")', 'homeHref("/en/index.html")']) == \
        ["/stats-formation/fr/index.html", "/en/index.html"]


def test_blocked_storage_never_breaks_the_page():
    blocked = 'globalThis.window = { get localStorage() { throw new Error("blocked"); } };\n'
    assert run(['readChoice()', 'saveChoice("de") === undefined'], setup=blocked) == [None, True]


# ---- the in-page half: the whole script against a stand-in for the browser ----------------------------

PAGE = """
const stored = {};
const replaced = [];
function link(text, href) {
  return { textContent: text, href: href, attrs: {}, listeners: {},
           setAttribute(k, v) { this.attrs[k] = v; }, removeAttribute(k) { delete this.attrs[k]; },
           addEventListener(type, fn) { this.listeners[type] = fn; } };
}
const brand = link("HFR Ortho", "../index.html");
const navLinks = [link("EN", "../en/index.html"), link("DE", "../de/index.html"), link("FR", "../fr/index.html"),
                  link("", "https://github.com/hfr-ortho/stats-formation")];
const storage = %(storage)s;
const define = (name, value) => Object.defineProperty(globalThis, name, { value, configurable: true, writable: true });
define("document", { querySelectorAll: (sel) => sel.includes("navbar-brand") ? [brand]
                                               : sel.includes("nav-link") ? navLinks : [] });
define("navigator", { languages: %(languages)s, language: "en" });
define("window", { location: { pathname: %(path)s, hash: %(hash)s, replace: (url) => replaced.push(url) },
                   get localStorage() { if (storage === "blocked") throw new Error("blocked"); return storage; } });
"""
WORKING_STORAGE = '{ getItem: (k) => stored[k] ?? null, setItem: (k, v) => { stored[k] = v; } }'


def run_page(path, hash="", languages='["en"]', storage=WORKING_STORAGE, after=""):
    """Load the switcher on a stand-in page, then report what it did."""
    setup = PAGE % {"storage": storage, "languages": languages, "path": json.dumps(path), "hash": json.dumps(hash)}
    report = ("{replaced, stored, brand: brand.href, "
              "links: Object.fromEntries(navLinks.map((a) => [a.textContent || 'github', [a.href, a.attrs['aria-current'] || null]]))}")
    probe = setup + script() + "\n" + after + f"\nconsole.log(JSON.stringify({report}));"
    out = subprocess.run([NODE, "-e", probe], capture_output=True, text=True, timeout=30)
    assert out.returncode == 0, out.stderr
    return json.loads(out.stdout)


def test_root_sends_a_swiss_german_browser_to_german_even_with_storage_blocked():
    assert run_page("/stats-formation/", languages='["de-CH", "de"]', storage='"blocked"')["replaced"] == ["de/index.html"]


def test_root_prefers_the_language_chosen_earlier():
    stored_fr = '{ getItem: () => "fr", setItem: () => {} }'
    assert run_page("/stats-formation/", languages='["de-CH"]', storage=stored_fr)["replaced"] == ["fr/index.html"]


def test_page_links_lead_to_the_same_section_in_each_language():
    result = run_page("/stats-formation/de/catalog/06-two-unpaired-groups.html", hash="#mann-whitney")
    assert result["replaced"] == []
    assert result["brand"] == "/stats-formation/de/index.html"
    assert result["links"] == {
        "EN": ["/stats-formation/en/catalog/06-two-unpaired-groups.html#mann-whitney", None],
        "DE": ["/stats-formation/de/catalog/06-two-unpaired-groups.html#mann-whitney", "true"],
        "FR": ["/stats-formation/fr/catalog/06-two-unpaired-groups.html#mann-whitney", None],
        "github": ["https://github.com/hfr-ortho/stats-formation", None],
    }


def test_clicking_takes_the_section_open_now_and_remembers_the_choice():
    click_fr = 'window.location.hash = "#log-rank"; navLinks[2].listeners.click();'
    result = run_page("/en/catalog/06-two-unpaired-groups.html", hash="#mann-whitney", after=click_fr)
    assert result["links"]["FR"][0] == "/fr/catalog/06-two-unpaired-groups.html#log-rank"
    assert result["stored"] == {"hfr-stats-lang": "fr"}


def test_clicking_with_storage_blocked_still_switches():
    click_fr = 'navLinks[2].listeners.click();'
    result = run_page("/en/index.html", storage='"blocked"', after=click_fr)
    assert result["links"]["FR"][0] == "/fr/index.html"
