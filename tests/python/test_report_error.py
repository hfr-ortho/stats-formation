"""The "Report an error" link's logic (spec 2026-11-13-report-error-design.md), run in Node.js: which page an
address names, how highlighted text is trimmed, the prefilled email, and, against a stand-in for the page, where
the links go and what pressing one sends. How a real browser orders a press and the clearing of a highlight is
checked by hand in a preview."""

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
        ["soft-canoes2@icloud.com", "HFR Ortho Stats: ", 300]


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
    assert to == "soft-canoes2@icloud.com"
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


ROOT_PAGE = """
globalThis.window = { location: { pathname: "/stats-formation/index.html", origin: "https://x", hash: "" } };
globalThis.document = new Proxy({}, { get(_, name) { throw new Error("touched document." + String(name)); } });
"""
BARE_PAGE = """
globalThis.window = { location: { pathname: "/stats-formation/en/index.html", origin: "https://x", hash: "" },
                      getSelection: () => null };
globalThis.document = { querySelector: () => null, querySelectorAll: () => [], addEventListener() {},
                        createElement: () => { throw new Error("built a link with nowhere to put it"); } };
"""


def test_script_is_idle_on_the_root_page():
    assert run(["1"], setup=ROOT_PAGE) == [1]


def test_script_survives_a_page_without_its_containers():
    assert run(["1"], setup=BARE_PAGE) == [1]


# Quarto writes its "Report an issue" list twice: beside the text, and in the footer, which comes after this
# script in the page (the only copy on a phone, or on a page with no table of contents).
LATE_PAGE = """
const element = () => { const e = { children: [], classList: { add() {} }, addEventListener() {},
                                    append(...c) { e.children.push(...c); }, prepend(...c) { e.children.unshift(...c); } };
                        return e; };
const lists = [element(), element()];
const main = element();
let ready = null;
globalThis.window = { location: { pathname: "/stats-formation/en/index.html", origin: "https://x", hash: "" },
                      getSelection: () => null };
globalThis.document = { readyState: "loading", createElement: element,
                        addEventListener(name, f) { if (name === "DOMContentLoaded") ready = f; },
                        querySelector: (q) => (q.startsWith("main") ? main : null),
                        querySelectorAll: (q) => (q === ".toc-actions ul" ? lists : []) };
"""


def test_link_joins_every_action_list_once_the_whole_page_is_there():
    counts = "[lists[0].children.length, lists[1].children.length, main.children.length]"
    assert run([counts, f"(ready(), {counts})"], setup=LATE_PAGE) == [[0, 0, 0], [1, 1, 1]]


def test_cut_never_splits_a_character():
    # The callout icons (🔀 💡 🔍) are two UTF-16 units each. Half of one cannot be put in an address:
    # the link would keep its last address and send an earlier highlight.
    text = "a" * 299 + "\U0001F500" + "b" * 50
    assert run([f"trimSelection({json.dumps(text)})"]) == ["a" * 299 + "\U0001F500" + "…"]
    assert 'Highlighted text: "' + "a" * 299 + "\U0001F500" + '…"' in mail(href("en", text))[2]


def test_section_with_an_accent_is_percent_encoded():
    # German and French step headings give ids like "analyse-durchführen-2"; mail apps may end a link at the "ü".
    base = "https://hfr-ortho.github.io/stats-formation/de/x.html"
    assert run([f'reportUrl("{base}", "analyse-durchführen-2", "")', f'reportUrl("{base}", "mann-whitney", "")']) == \
        [base + "#analyse-durchf%C3%BChren-2", base + "#mann-whitney"]


# A page with Quarto's own entry in the list, and a reader who highlights text: `select(node, text)` sets what is
# highlighted, `inside` is in the page text (in the step with id "run-it-1"), `outside` is in the sidebar.
LIVE_PAGE = """
const element = () => { const e = { children: [], listeners: {}, classList: { add() {} },
                                    addEventListener(name, f) { e.listeners[name] = f; },
                                    append(...c) { e.children.push(...c); }, prepend(...c) { e.children.unshift(...c); } };
                        return e; };
const quartoEntry = element();
const list = element(); list.children.push(quartoEntry);
const inside = { nodeType: 1, closest: (q) => (q === "section[id]" ? { id: "run-it-1" } : null) };
const outside = { nodeType: 1, closest: () => null };
const main = element(); main.contains = (node) => node === inside;
let picked = null;
const select = (node, text) => { picked = node ? { isCollapsed: false, anchorNode: node, toString: () => text } : null; };
globalThis.window = { location: { pathname: "/stats-formation/en/catalog/06-two-unpaired-groups.html",
                                  origin: "https://x", hash: "#unpaired-t" }, getSelection: () => picked };
globalThis.document = { readyState: "complete", createElement: element, addEventListener() {},
                        querySelector: (q) => (q.startsWith("main") ? main : null),
                        querySelectorAll: (q) => (q === ".toc-actions ul" ? [list] : []) };
const body = (a) => decodeURIComponent(a.href.split("body=")[1]);
const listLink = () => list.children[0].children[0];
const endLink = () => main.children[0].children[1];
"""
LIVE_URL = "https://x/stats-formation/en/catalog/06-two-unpaired-groups.html"
NO_HIGHLIGHT = f"Page: {LIVE_URL}#unpaired-t\r\n\r\nWhat is wrong or confusing:\r\n"


def test_link_goes_above_quartos_own_entry():
    assert run(["list.children.length", "list.children[1] === quartoEntry"], setup=LIVE_PAGE) == [2, True]


def test_links_work_before_they_are_pressed():
    assert run(["body(listLink())", "body(endLink())"], setup=LIVE_PAGE) == [NO_HIGHLIGHT, NO_HIGHLIGHT]


def test_pressing_a_link_sends_the_highlight_and_its_section():
    quoted = f'Page: {LIVE_URL}#run-it-1\r\nHighlighted text: "the mean"\r\n\r\nWhat is wrong or confusing:\r\n'
    assert run(['(select(inside, "the mean"), listLink().listeners.pointerdown(), body(listLink()))',
                '(select(inside, "the mean"), endLink().listeners.pointerdown(), body(endLink()))',
                '(select(null), select(inside, "the mean"), endLink().listeners.keydown(), body(endLink()))'],
               setup=LIVE_PAGE) == [quoted, quoted, quoted]


def test_a_highlight_outside_the_page_text_or_since_cleared_is_not_sent():
    assert run(['(select(outside, "Tidy data"), endLink().listeners.pointerdown(), body(endLink()))',
                '(select(inside, "the mean"), endLink().listeners.pointerdown(), select(null), '
                'endLink().listeners.pointerdown(), body(endLink()))'], setup=LIVE_PAGE) == [NO_HIGHLIGHT, NO_HIGHLIGHT]
