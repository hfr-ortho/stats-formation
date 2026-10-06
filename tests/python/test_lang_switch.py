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
