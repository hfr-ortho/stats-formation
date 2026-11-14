"""renv.lock must install without a compiler.

CRAN keeps a ready-built (binary) package only for each package's newest version. A lockfile that reads from
CRAN therefore goes stale within weeks: `renv::restore()` then compiles the older versions on the learner's
computer, which fails without a Fortran compiler (Mac) or Rtools (Windows). A dated Posit Package Manager
snapshot keeps the binaries of the versions that were current on its date."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOCK = json.loads((ROOT / "renv.lock").read_text(encoding="utf-8"))
SNAPSHOT = re.compile(r"https://packagemanager\.posit\.co/cran/\d{4}-\d{2}-\d{2}")


def test_lockfile_reads_from_one_dated_snapshot():
    repos = LOCK["R"]["Repositories"]
    assert [r["Name"] for r in repos] == ["CRAN"], repos
    assert SNAPSHOT.fullmatch(repos[0]["URL"]), repos[0]["URL"]


def test_every_package_comes_from_that_snapshot():
    """A record that names another repository (Positron's default is .../cran/latest) is installed from there,
    and "latest" moves on."""
    elsewhere = {name: (p.get("Source"), p.get("Repository")) for name, p in LOCK["Packages"].items()
                 if p.get("Source") != "Repository" or p.get("Repository") != "CRAN"}
    assert not elsewhere, elsewhere
