"""The "Report an error" link's logic (spec 2026-11-13-report-error-design.md), run in Node.js: which page an
address names, how highlighted text is trimmed, and the prefilled email. What the script does to a page in the
browser (adding the two links, reading the selection) is checked by hand in a preview."""

import json
import re
import shutil
import subprocess
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit

import pytest

ROOT = Path(__file__).resolve().parents[2]
NODE = shutil.which("node")
pytestmark = pytest.mark.skipif(NODE is None, reason="Node.js is not installed")


def script():
    html = (ROOT / "report-error.html").read_text(encoding="utf-8")
    return re.search(r'<script id="report-error">(.*?)</script>', html, re.DOTALL).group(1)


def run(expressions, setup=""):
    """Evaluate JavaScript expressions after loading the script outside a browser."""
    probe = setup + script() + f"\nconsole.log(JSON.stringify([{', '.join(expressions)}]));"
    out = subprocess.run([NODE, "-e", probe], capture_output=True, text=True, timeout=30)
    assert out.returncode == 0, out.stderr
    return json.loads(out.stdout)


PAGE_URL = "https://hfr-ortho.github.io/stats-formation/en/catalog/06-two-unpaired-groups.html#mann-whitney"


def mail(href):
    """The parts of a mailto: address, decoded the way a mail app decodes them."""
    parts = urlsplit(href)
    assert parts.scheme == "mailto"
    assert "+" not in parts.query          # spaces must be %20: mail apps keep a "+" as a plus sign
    fields = {k: unquote(v) for k, v in (pair.split("=", 1) for pair in parts.query.split("&"))}
    return parts.path, fields["subject"], fields["body"]


def href(lang, selection, page="en/catalog/06-two-unpaired-groups", url=PAGE_URL):
    return run([f"reportHref({json.dumps(lang)}, {json.dumps(page)}, {json.dumps(url)}, {json.dumps(selection)})"])[0]


def test_constants_are_the_ones_in_the_spec():
    assert run(["REPORT_TO", "REPORT_PREFIX", "REPORT_MAX"]) == \
        ["josephmichael.schwab@h-fr.ch", "HFR Ortho Stats: ", 300]


def test_labels_in_every_language():
    en, de, fr = run(["REPORT_TEXT.en", "REPORT_TEXT.de", "REPORT_TEXT.fr"])
    assert en == {"link": "Report an error", "question": "Found a mistake on this page?",
                  "action": "Report it by email.", "page": "Page", "highlighted": "Highlighted text",
                  "prompt": "What is wrong or confusing:"}
    assert de == {"link": "Fehler melden", "question": "Einen Fehler auf dieser Seite gefunden?",
                  "action": "Melden Sie ihn per E-Mail.", "page": "Seite", "highlighted": "Markierter Text",
                  "prompt": "Was ist falsch oder unklar:"}
    assert fr == {"link": "Signaler une erreur", "question": "Vous avez trouvé une erreur sur cette page\u00a0?",
                  "action": "Signalez-la par e-mail.", "page": "Page", "highlighted": "Texte surligné",
                  "prompt": "Ce qui est faux ou confus\u00a0:"}


def test_page_is_read_from_the_address():
    assert run(['reportPage("/stats-formation/en/catalog/06-two-unpaired-groups.html")',
                'reportPage("/de/catalog/06-two-unpaired-groups.html")',
                'reportPage("/stats-formation/fr/")',
                'reportPage("/stats-formation/fr/index.html")',
                'reportPage("/stats-formation/")',
                'reportPage("/stats-formation/index.html")']) == \
        [{"lang": "en", "page": "en/catalog/06-two-unpaired-groups"},
         {"lang": "de", "page": "de/catalog/06-two-unpaired-groups"},
         {"lang": "fr", "page": "fr/index"},
         {"lang": "fr", "page": "fr/index"},
         None, None]


def test_selection_is_collapsed_and_cut():
    long = "é" * 400
    assert run(['trimSelection("  the mean\\n\\t (SD)   was  ")', 'trimSelection("   \\n ")', 'trimSelection("")',
                f'trimSelection("{long}")', f'trimSelection("{"a" * 300}")']) == \
        ["the mean (SD) was", "", "", "é" * 300 + "…", "a" * 300]


def test_section_comes_from_the_highlight_then_the_address():
    base = "https://hfr-ortho.github.io/stats-formation/en/x.html"
    assert run([f'reportUrl("{base}", "mann-whitney", "#unpaired-t")', f'reportUrl("{base}", "", "#unpaired-t")',
                f'reportUrl("{base}", "", "")']) == [base + "#mann-whitney", base + "#unpaired-t", base]


def test_email_names_the_page_and_the_highlight():
    to, subject, body = mail(href("en", "the mean (SD) was"))
    assert to == "josephmichael.schwab@h-fr.ch"
    assert subject == "HFR Ortho Stats: en/catalog/06-two-unpaired-groups"
    assert body == f'Page: {PAGE_URL}\r\nHighlighted text: "the mean (SD) was"\r\n\r\nWhat is wrong or confusing:\r\n'


def test_body_leaves_out_an_empty_highlight():
    for selection in ["", "   \n "]:
        assert mail(href("en", selection))[2] == f"Page: {PAGE_URL}\r\n\r\nWhat is wrong or confusing:\r\n"


def test_body_follows_the_page_language_and_falls_back_to_english():
    assert mail(href("de", "x"))[2] == f'Seite: {PAGE_URL}\r\nMarkierter Text: "x"\r\n\r\nWas ist falsch oder unklar:\r\n'
    assert mail(href("fr", "x"))[2] == \
        f'Page\u00a0: {PAGE_URL}\r\nTexte surligné\u00a0: "x"\r\n\r\nCe qui est faux ou confus\u00a0:\r\n'
    assert mail(href("it", "x"))[2] == mail(href("en", "x"))[2]
    assert mail(href("de", "x"))[1] == "HFR Ortho Stats: en/catalog/06-two-unpaired-groups"   # same prefix everywhere


def test_special_characters_survive_the_address():
    selection = 'p < 0.001 & 95% CI? #1 + "médiane" (IQR)'
    assert f'Highlighted text: "{selection}"' in mail(href("en", selection))[2]


def test_long_highlight_is_cut_in_the_email():
    assert 'Highlighted text: "' + "a" * 300 + '…"' in mail(href("en", "a" * 400))[2]
