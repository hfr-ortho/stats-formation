"""No TJS branding outside the credit and history (HFR spec §4.6).

Allowed: the credit phrase "TJS Statistics Tutorials"; the license files; TJS's and HFR's specs and plans;
README.md and CLAUDE.md, which explain where the repo came from; and the tests that check all this."""

import re
import subprocess
import sys
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parents[2]
TJS = re.compile(r"TJS|Total Joint|tjs-|\bJOA\b")
CREDIT = "TJS Statistics Tutorials"
EXEMPT = ("docs/superpowers/", "LICENSE", "README.md", "CLAUDE.md",
          "tests/python/test_branding.py", "tests/python/test_repo_docs.py")
BINARY = {".png", ".jpg", ".svg", ".xlsx", ".docx", ".zip"}


def tracked(*paths):
    """Files git tracks under these paths (all of them if none), minus the exempt ones."""
    out = subprocess.run(["git", "ls-files", "--", *paths], cwd=ROOT, capture_output=True, text=True, check=True)
    return [p for p in out.stdout.splitlines() if not p.startswith(EXEMPT)]


def offenders(paths):
    """Lines that mention TJS other than in the credit phrase, as "file:line: text"."""
    found = []
    for rel in paths:
        if Path(rel).suffix in BINARY:
            continue
        lines = (ROOT / rel).read_text(encoding="utf-8", errors="ignore").splitlines()
        for number, line in enumerate(lines, 1):
            if TJS.search(line.replace(CREDIT, "")):
                found.append(f"{rel}:{number}: {line.strip()[:100]}")
    return found


def workbook_text(path):
    wb = openpyxl.load_workbook(ROOT / path)
    cells = [str(c.value) for ws in wb.worksheets for row in ws.iter_rows() for c in row if c.value is not None]
    return [wb.properties.creator or ""] + cells


def test_rule_flags_tjs_but_not_the_credit(tmp_path, monkeypatch):
    monkeypatch.setattr(sys.modules[__name__], "ROOT", tmp_path)
    (tmp_path / "a.qmd").write_text("Ask your TJS project lead.\nAdapted from the TJS Statistics Tutorials.\n")
    assert offenders(["a.qmd"]) == ["a.qmd:1: Ask your TJS project lead."]


def test_pages_never_mention_tjs():
    assert offenders(tracked("en", "index.qmd")) == []


def test_data_and_generators_never_mention_tjs():
    assert offenders(tracked("data", "data-raw", "templates", "scripts", "R")) == []
    for workbook in ["data/messy_abstraction_workbook.xlsx", "templates/data-collection-template.xlsx"]:
        assert [t for t in workbook_text(workbook) if TJS.search(t)] == [], workbook
