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
        if dest.exists() and ".coming-soon" in dest.read_text(encoding="utf-8"):
            continue  # a stub carries no fixed IDs yet: its translation brings them
        if not dest.exists() or fragment not in fixed_ids(dest):
            missing.append(link)
    return missing


def pages(lang):
    return sorted((ROOT / lang).rglob("*.qmd"))


HEADING = re.compile(r"^(#{2,3})\s+(.*?)\s*$")
OPENER = re.compile(r"^(:{3,})\s*(\S.*)?$")


def toc_depth(text):
    """The deepest heading level in the table of contents: 0 when `toc: false`, else `toc-depth` (default 3)."""
    front = re.match(r"---\n(.*?)\n---\n", text, re.S)
    front = front.group(1) if front else ""
    if re.search(r"^toc:\s*false\s*$", front, re.M):
        return 0
    depth = re.search(r"^toc-depth:\s*(\d+)", front, re.M)
    return int(depth.group(1)) if depth else 3


def toc_headings_without_ids(path):
    """`##`/`###` headings that appear in the table of contents (outside code, callouts and tabsets) with no {#id}."""
    text = path.read_text(encoding="utf-8")
    depth = toc_depth(text)
    body = re.sub(r"\A---\n.*?\n---\n", "", text, count=1, flags=re.S)
    missing, in_code, stack = [], False, []
    for line in body.splitlines():
        if line.lstrip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        opener = OPENER.match(line)
        if opener and opener.group(2):
            stack.append(("callout" in opener.group(2) or "panel-tabset" in opener.group(2), len(opener.group(1))))
            continue
        if opener:
            if stack:
                stack.pop()
            continue
        heading = HEADING.match(line)
        if heading and len(heading.group(1)) <= depth and not any(hidden for hidden, _ in stack):
            if not re.search(r"\{[^}]*#[A-Za-z][\w:.-]*", heading.group(2)):
                missing.append(line)
    return missing


def test_rule_finds_unfixed_headings_in_the_table_of_contents(tmp_path):
    page = tmp_path / "a.qmd"
    page.write_text("---\ntoc-depth: 2\n---\n## One\n### Deep\n## Two {#two}\n::: {.callout-tip}\n## Title\n:::\n"
                    "::: {.panel-tabset}\n## R\n:::\n```r\n## code\n```\n")
    assert toc_headings_without_ids(page) == ["## One"]


def test_toc_headings_have_fixed_ids():
    """The switcher keeps #section, so every heading a reader can jump to needs the same ID in every language."""
    found = {str(p.relative_to(ROOT)): toc_headings_without_ids(p) for p in pages("en")}
    assert {page: heads for page, heads in found.items() if heads} == {}


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
