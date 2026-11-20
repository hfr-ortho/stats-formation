import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "check_setup.py"
R_SCRIPT = ROOT / "scripts" / "check_setup.R"
RSCRIPT = shutil.which("Rscript")


def run(python: str) -> subprocess.CompletedProcess:
    return subprocess.run([python, str(SCRIPT)], cwd=ROOT, capture_output=True, text=True)


def r_line(folder: Path) -> str:
    """The R version line that check_setup.R prints when run in `folder` (with no packages to find)."""
    (folder / "lib").mkdir(exist_ok=True)
    result = subprocess.run([RSCRIPT, "--vanilla", str(R_SCRIPT)], cwd=folder, capture_output=True, text=True,
                            env={"PATH": "/usr/bin:/bin", "R_LIBS_USER": str(folder / "lib")}, timeout=120)
    return next(line for line in result.stdout.splitlines() if line.startswith("R version"))


def running_r() -> tuple[int, int]:
    out = subprocess.run([RSCRIPT, "--vanilla", "-e", "cat(as.character(getRversion()))"],
                         capture_output=True, text=True, check=True).stdout
    major, minor, _ = (int(x) for x in out.split("."))
    return major, minor


def line_for_lockfile(folder: Path, text: str) -> str:
    folder.mkdir()
    (folder / "renv.lock").write_text(text, encoding="utf-8")
    return r_line(folder)


needs_r = pytest.mark.skipif(RSCRIPT is None, reason="R is not installed")


@needs_r
def test_r_check_wants_the_lockfiles_r_version(tmp_path):
    """renv::status() complains when R's major.minor differs from renv.lock's, so the check must agree."""
    major, minor = running_r()

    def line_for(version: str) -> str:
        return line_for_lockfile(tmp_path / version, json.dumps({"R": {"Version": version}, "Packages": {}}))

    # Same major.minor, another patch release: fine.
    assert line_for(f"{major}.{minor}.99").endswith("OK")
    # A newer minor, a newer major and an older major than the running R's: a problem that names the lockfile's R.
    for other in [f"{major}.{minor + 1}", f"{major + 1}.{minor}", f"{major - 1}.{minor}"]:
        line = line_for(f"{other}.0")
        assert "PROBLEM" in line and f"install R {other}" in line, line


@needs_r
def test_r_check_reads_the_real_lockfile(tmp_path):
    """The repository's own renv.lock, in whatever layout renv wrote it, gives the check its R version."""
    locked = json.loads((ROOT / "renv.lock").read_text(encoding="utf-8"))["R"]["Version"]
    locked_major_minor = ".".join(locked.split(".")[:2])
    line = line_for_lockfile(tmp_path / "real", (ROOT / "renv.lock").read_text(encoding="utf-8"))
    if ".".join(map(str, running_r())) == locked_major_minor:
        assert line.endswith("OK"), line
    else:
        assert "PROBLEM" in line and f"install R {locked_major_minor}" in line, line


@needs_r
def test_r_check_reads_the_version_whatever_the_key_order(tmp_path):
    """JSON keys have no fixed order: "Repositories" may come before "Version" in the "R" block."""
    major, minor = running_r()
    lockfile = {"R": {"Repositories": [{"Name": "CRAN", "URL": "https://packagemanager.posit.co/cran/2026-10-06"}],
                      "Version": f"{major}.{minor}.0"},
                "Packages": {"x": {"Package": "x", "Version": "0.0.1"}}}
    assert line_for_lockfile(tmp_path / "indented", json.dumps(lockfile, indent=2)).endswith("OK")
    assert line_for_lockfile(tmp_path / "one-line", json.dumps(lockfile)).endswith("OK")


@needs_r
def test_r_check_without_a_lockfile_says_where_to_run_it(tmp_path):
    folder = tmp_path / "elsewhere"
    folder.mkdir()
    line = r_line(folder)
    assert "PROBLEM" in line and "the folder that holds renv.lock" in line, line


@needs_r
def test_r_check_says_when_it_cannot_read_the_lockfile(tmp_path):
    line = line_for_lockfile(tmp_path / "broken", json.dumps({"R": {"Repositories": []}, "Packages": {}}))
    assert "PROBLEM" in line and "couldn't read the R version in renv.lock" in line, line


def test_passes_inside_the_project_environment():
    result = run(sys.executable)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "All good - you are ready." in result.stdout


def test_flags_a_python_outside_the_project_environment():
    base_python = Path(sys.base_prefix) / "bin" / "python3"
    result = run(str(base_python))
    assert result.returncode == 1
    assert "PROBLEM" in result.stdout


def test_r_check_covers_the_packages_the_pages_call():
    script = (ROOT / "scripts" / "check_setup.R").read_text(encoding="utf-8")
    for pkg in ["tidyverse", "readxl", "tidyxl", "janitor", "gtsummary", "flextable", "smd",
                "effectsize", "DescTools", "survival", "ggsurvfit", "rstatix", "tidycmprsk",
                "broom.helpers", "lme4", "lmerTest", "emmeans", "PMCMRplus", "irr"]:
        assert f'"{pkg}"' in script, pkg


def test_python_check_covers_the_packages_the_pages_import():
    script = SCRIPT.read_text(encoding="utf-8")
    for name in ["pandas", "numpy", "matplotlib", "scipy", "statsmodels", "pingouin", "lifelines", "scikit_posthocs"]:
        assert f'"{name}"' in script, name


def test_project_python_uses_pandas_3():
    """The pages are written for pandas 3. lifelines declares pandas<3, so pyproject.toml overrides it."""
    import pandas

    assert int(pandas.__version__.split(".")[0]) >= 3, pandas.__version__
