from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SITE_URL = "https://hfr-ortho.github.io/stats-formation/"
HFR_COPYRIGHT = "HFR adaptations Copyright (c) 2026 HFR Hôpital fribourgeois"
CREDIT = "Adapted from the TJS Statistics Tutorials"


def read(name: str) -> str:
    return (ROOT / name).read_text(encoding="utf-8")


def test_readme_links_the_site_says_synthetic_and_credits_tjs():
    text = read("README.md")
    assert SITE_URL in text
    assert "synthetic" in text.lower()
    assert CREDIT in text
    assert "git clone https://github.com/hfr-ortho/stats-formation.git" in text


def test_licenses():
    assert read("LICENSE").startswith("MIT License")
    assert "Total Joint Specialists" in read("LICENSE")
    assert HFR_COPYRIGHT in read("LICENSE")
    content = read("LICENSE-CONTENT")
    assert "Total Joint Specialists" in content and HFR_COPYRIGHT in content
    assert "adapted from the TJS Statistics Tutorials" in content
    assert "CC BY 4.0" in content
    assert "https://creativecommons.org/licenses/by/4.0/legalcode" in content


def test_package_metadata_names_hfr():
    assert 'name = "hfr-stats-formation"' in read("pyproject.toml")
    assert "HFR Ortho" in read("DESCRIPTION")


def test_claude_md_states_the_golden_rules():
    text = read("CLAUDE.md")
    for rule in ["engine: knitr", "group=\"language\"", "check_agree", "_freeze", "Synthetic data only",
                 "never assign to `_`", "**The question:**", "override-dependencies",
                 'a ceiling of "p > 0.999"', "Bootstrap CIs are seeded", "opts_chunk",
                 "Regression CIs", "CumIncidenceRight", "Mixed models", "Multiple comparisons", "Word output",
                 "report numbers, not interpretation",
                 "deliberate public exception", "fetch-only", "2026-10-06-hfr-stats-formation-design.md"]:
        assert rule in text, rule
