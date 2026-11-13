"""The glossary tooltips' logic (glossary-terms.html), run in Node.js: which entry a term link points to, and
how an entry's definition is read from the glossary page. Fetching the page and showing the tooltip are checked
by hand in a preview."""

import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
NODE = shutil.which("node")
pytestmark = pytest.mark.skipif(NODE is None, reason="Node.js is not installed")

# A stand-in for the glossary page: one entry with a definition, one whose definition is missing.
GLOSSARY = """
const dd = { tagName: "DD", textContent: "  The middle value\\n   when the values are sorted. " };
const dt = { nextElementSibling: dd };
const lonely = { nextElementSibling: { tagName: "DT", textContent: "next term" } };
const glossary = { getElementById: (id) => ({ median: { closest: () => dt }, orphan: { closest: () => lonely } }[id] || null) };
"""


def run(expressions, setup=""):
    html = (ROOT / "glossary-terms.html").read_text(encoding="utf-8")
    script = re.search(r'<script id="glossary-terms">(.*?)</script>', html, re.DOTALL).group(1)
    probe = setup + script + f"\nconsole.log(JSON.stringify([{', '.join(expressions)}]));"
    out = subprocess.run([NODE, "-e", probe], capture_output=True, text=True, timeout=30)
    assert out.returncode == 0, out.stderr
    return json.loads(out.stdout)


def test_term_id_is_the_part_after_the_hash():
    assert run(['termId("../glossary.html#standard-error")', 'termId("glossary.html")', 'termId(null)',
                'termId("../glossary.html#p-value")']) == ["standard-error", "", "", "p-value"]


def test_definition_is_the_entry_text_on_one_line():
    assert run(['termDefinition(glossary, "median")'], setup=GLOSSARY) == ["The middle value when the values are sorted."]


def test_a_missing_entry_or_definition_gives_nothing():
    assert run(['termDefinition(glossary, "nope")', 'termDefinition(glossary, "orphan")', 'termDefinition(glossary, "")'],
               setup=GLOSSARY) == ["", "", ""]
