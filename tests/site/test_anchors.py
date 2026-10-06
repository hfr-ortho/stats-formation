"""Links into a section use fixed IDs, the same in every language (HFR spec §4.3). The language switcher
keeps the #section when it changes language, so a section must have the same ID in every language."""

import re

from sitelib import LANGS, ROOT

LINK = re.compile(r"\]\(([^)\s]*#[^)\s]+)\)")
FIXED_ID = re.compile(r"\{#([A-Za-z][\w:.-]*)")


def fixed_ids(path):
    return set(FIXED_ID.findall(path.read_text(encoding="utf-8")))


def fragment_links_without_fixed_ids(path):
    """Links on this page whose #section isn't a fixed {#id} on the page they point to."""
    missing = []
    for link in LINK.findall(path.read_text(encoding="utf-8")):
        if "://" in link:
            continue
        file, fragment = link.split("#", 1)
        dest = path if not file else (path.parent / file).resolve()
        if not dest.exists() or fragment not in fixed_ids(dest):
            missing.append(link)
    return missing


def pages(lang):
    return sorted((ROOT / lang).rglob("*.qmd"))


def test_rule_flags_a_link_to_an_auto_generated_id(tmp_path):
    (tmp_path / "a.qmd").write_text("## Mann-Whitney U test\n")
    (tmp_path / "b.qmd").write_text("See [the test](a.qmd#mann-whitney-u-test).\n")
    assert fragment_links_without_fixed_ids(tmp_path / "b.qmd") == ["a.qmd#mann-whitney-u-test"]


def test_rule_accepts_a_link_to_a_fixed_id(tmp_path):
    (tmp_path / "a.qmd").write_text("## Mann-Whitney U test {#mann-whitney}\n")
    (tmp_path / "b.qmd").write_text("See [the test](a.qmd#mann-whitney) and [below](#here).\n\n## Here {#here}\n")
    assert fragment_links_without_fixed_ids(tmp_path / "b.qmd") == []


def test_every_section_link_targets_a_fixed_id():
    found = {str(p.relative_to(ROOT)): fragment_links_without_fixed_ids(p) for lang in LANGS for p in pages(lang)}
    assert {page: links for page, links in found.items() if links} == {}


def test_translated_pages_keep_every_fixed_id():
    for lang in ["de", "fr"]:
        for page in pages(lang):
            if ".coming-soon" in page.read_text(encoding="utf-8"):
                continue    # a stub: nothing translated yet
            missing = fixed_ids(ROOT / "en" / page.relative_to(ROOT / lang)) - fixed_ids(page)
            assert not missing, f"{page.relative_to(ROOT)} lacks {sorted(missing)}"
