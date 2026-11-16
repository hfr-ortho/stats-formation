"""Every glossary definition is traceable: each entry of en/glossary.qmd has a section in
docs/glossary-sources.md that names its source, and the sources file lists no entry the glossary lacks."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ENTRY = re.compile(r"^\[[^\]]+\]\{#([a-z0-9-]+)\}", re.MULTILINE)
SECTION = re.compile(r"^### `([a-z0-9-]+)`", re.MULTILINE)


def glossary_ids(lang="en"):
    return ENTRY.findall((ROOT / lang / "glossary.qmd").read_text(encoding="utf-8"))


def source_sections():
    text = (ROOT / "docs" / "glossary-sources.md").read_text(encoding="utf-8")
    parts = SECTION.split(text)[1:]                     # id, body, id, body, ...
    return dict(zip(parts[0::2], parts[1::2]))


def test_glossary_ids_are_unique():
    ids = glossary_ids()
    assert len(ids) == len(set(ids))


def test_every_entry_has_a_source_and_every_source_an_entry():
    assert set(source_sections()) == set(glossary_ids())


def test_every_source_section_names_a_source_and_a_check():
    sections = source_sections()
    assert sections
    missing = [i for i, body in sections.items()
               if not re.search(r"^- \*\*Source:\*\* \S", body, re.MULTILINE)
               or not re.search(r"^- \*\*Checked:\*\* \S", body, re.MULTILINE)]
    assert missing == []
