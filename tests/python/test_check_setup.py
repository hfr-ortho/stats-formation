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


@pytest.mark.skipif(RSCRIPT is None, reason="R is not installed")
def test_r_check_wants_the_lockfiles_r_version(tmp_path):
    """renv::status() complains when R's major.minor differs from renv.lock's, so the check must agree."""
    locked = json.loads((ROOT / "renv.lock").read_text(encoding="utf-8"))["R"]["Version"]
    assert locked.count(".") == 2, locked
    running = subprocess.run([RSCRIPT, "--vanilla", "-e", "cat(as.character(getRversion()))"],
                             capture_output=True, text=True, check=True).stdout
    major, minor, _ = (int(x) for x in running.split("."))

    def line_for(version: str) -> str:
        folder = tmp_path / version
        folder.mkdir()
        (folder / "renv.lock").write_text(json.dumps({"R": {"Version": version}, "Packages": {}}), encoding="utf-8")
        return r_line(folder)

    # Same major.minor, another patch release: fine.
    assert line_for(f"{major}.{minor}.99").endswith("OK")
    # A newer or an older minor version than the lockfile's: a problem that names the lockfile's R.
    for other in [f"{major}.{minor + 1}", f"{major}.{minor - 1}"]:
        line = line_for(f"{other}.0")
        assert "PROBLEM" in line and f"install R {other}" in line, line


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
