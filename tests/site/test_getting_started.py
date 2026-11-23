import json
import re

from bs4 import BeautifulSoup
from sitelib import LANGS, ROOT, SITE_ROOT, load, text_of

SETUP_COMMANDS = [
    "uv python install 3.13",
    "git clone https://github.com/hfr-ortho/stats-formation.git",
    "renv::restore()",
    "uv sync",
    "Rscript scripts/check_setup.R",
    "uv run python scripts/check_setup.py",
    'source("scripts/check_setup.R")',
    "sudo xcodebuild -license accept",
]


def test_setup_page_shows_every_command_an_ra_types(site):
    text = load("getting-started/setup.html").get_text()
    missing = [c for c in SETUP_COMMANDS if c not in text]
    assert missing == []


def test_setup_page_is_no_longer_a_stub(site):
    assert load("getting-started/setup.html").select_one(".coming-soon") is None




def test_real_data_page_is_no_longer_a_stub(site):
    assert load("getting-started/real-data.html").select_one(".coming-soon") is None


def test_setup_page_shows_how_to_read_data_without_cloning(site):
    text = load("getting-started/setup.html").get_text()
    url = "https://raw.githubusercontent.com/hfr-ortho/stats-formation/main/data/cohort.csv"
    assert url in text




def test_real_data_page_keeps_real_data_out_of_this_folder(site):
    text = load("getting-started/real-data.html").get_text(" ")
    assert "Never copy real data anywhere inside this tutorial folder" in text


def test_setup_page_avoids_cloud_synced_folders(site):
    text = load("getting-started/setup.html").get_text()
    assert "cd ~/Documents" not in text
    assert "mkdir -p ~/projects" in text
    assert "OneDrive" in text and "iCloud" in text


def test_no_clone_instructions_install_packages_and_handle_excel(site):
    text = load("getting-started/setup.html").get_text()
    assert "without steps 5–8" not in text
    assert 'install.packages(c("readr", "readxl"))' in text
    assert "uv run --with pandas --with openpyxl python" in text
    assert 'download.file(url, path, mode = "wb")' in text


def built(lang: str, page: str) -> BeautifulSoup:
    return BeautifulSoup((SITE_ROOT / lang / page).read_text(encoding="utf-8"), "html.parser")


def test_setup_page_says_what_you_need_before_you_start(site):
    """R version (the one renv.lock was made with), disk space and administrator rights, before step 1."""
    locked = json.loads((ROOT / "renv.lock").read_text(encoding="utf-8"))["R"]["Version"]
    major_minor = ".".join(locked.split(".")[:2])
    step_1 = load("getting-started/setup.html").select_one("main section#install-r")
    before = " ".join(el.get_text(" ") for el in step_1.find_previous_siblings())
    assert f"R {major_minor}" in before
    assert "5 GB" in before
    assert "administrator" in before
    assert "HFR IT" in before


def test_setup_page_uses_no_rstudio_menu(site):
    """"Session → Restart R" is RStudio's menu. Positron restarts from the Command Palette."""
    for lang in LANGS:
        text = built(lang, "getting-started/setup.html").get_text(" ")
        assert "Session → Restart R" not in text, lang
        assert "Interpreter: Restart Active Interpreter Session" in text, lang


def test_setup_page_uses_positrons_names(site):
    """Positron's documentation calls the control at the top right the Interpreter picker."""
    text = load("getting-started/setup.html").get_text(" ")
    assert "language picker" not in text
    assert "Interpreter picker" in text and "New Console Session…" in text


def test_setup_page_explains_the_r_version_message(site):
    text = load("getting-started/setup.html").get_text(" ")
    assert "The lockfile was generated with R" in text


def test_setup_page_offers_the_zip_without_git(site):
    page = load("getting-started/setup.html")
    zip_url = "https://github.com/hfr-ortho/stats-formation/archive/refs/heads/main.zip"
    assert any(a.get("href") == zip_url for a in page.select("a"))
    text = page.get_text(" ")
    assert "stats-formation-main" in text and "git pull" in text


SETUP_TIME = {"en": ("30 to 60 minutes", "about an hour"),
              "de": ("30 bis 60 Minuten", "eine Stunde"),
              "fr": ("30 à 60 minutes", "une heure")}


def test_setup_page_says_30_to_60_minutes(site):
    """The site owner's estimate, written as a range with "to"; the earlier "about an hour" is gone."""
    for lang in LANGS:
        text = built(lang, "getting-started/setup.html").select_one("main").get_text(" ")
        now, before = SETUP_TIME[lang]
        assert text.count(now) == 2, lang          # the opening sentence and "Before you start"
        assert before not in text, lang


REPORT_LABEL = {"en": "Report an error", "de": "Fehler melden", "fr": "Signaler une erreur"}
WINDOWS_UNTESTED = {"en": "we haven't run the Windows steps on a Windows PC ourselves yet",
                    "de": "Die Schritte für Windows haben wir selbst noch nicht auf einem Windows-PC ausgeführt",
                    "fr": "nous n'avons pas encore exécuté nous-mêmes les étapes pour Windows sur un PC Windows"}


def test_setup_page_says_the_windows_steps_are_untested(site):
    """Nobody has run the Windows steps yet: "Before you start" says so and points to Report an error."""
    for lang in LANGS:
        step_1 = built(lang, "getting-started/setup.html").select_one("main section#install-r")
        windows = [li for el in step_1.find_previous_siblings() for li in el.select("li")
                   if WINDOWS_UNTESTED[lang] in li.get_text(" ").replace("’", "'")]   # Quarto curls apostrophes
        assert len(windows) == 1, lang
        assert REPORT_LABEL[lang] in windows[0].get_text(" "), lang


HOME_SHORTCUT = {"en": "Shift-Command-H", "de": "Umschalttaste-Befehlstaste-H", "fr": "Maj + Commande + H"}


def test_both_open_folder_sentences_name_the_home_folder_shortcut(site):
    """Positron's Open Folder dialog jumps to the home folder with Shift-Command-H on a Mac."""
    for lang in LANGS:
        section = built(lang, "getting-started/setup.html").select_one("main section#get-this-repository")
        sentences = [el.get_text(" ") for el in section.select("p, li")
                     if "Open Folder" in el.get_text(" ") and not el.select("p, li")]
        assert len(sentences) == 2, (lang, sentences)
        assert all(HOME_SHORTCUT[lang] in s for s in sentences), lang


def test_every_python_block_on_the_setup_page_imports_what_it_uses(site):
    """Readers copy one block at a time, so a block that uses pd imports pandas itself."""
    blocks = load("getting-started/setup.html").select("div.sourceCode pre.python, pre.sourceCode.python")
    assert len(blocks) >= 2, "the selector no longer finds the page's Python blocks"
    for block in blocks:
        code = block.get_text()
        if re.search(r"\bpd\.", code):
            assert "import pandas as pd" in code, code


def test_real_data_page_links_a_git_introduction(site):
    url = "https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository"
    for lang in LANGS:
        commit = built(lang, "getting-started/real-data.html").select_one("section#before-commit")
        assert any(a.get("href") == url for a in commit.select("a")), lang


def test_reporting_conventions_cap_large_p_values(site):
    text = load("getting-started/using-this-site.html").get_text(" ")
    assert "p > 0.999" in text and "p = 1.000" in text


REAL = "getting-started/real-data.html"


def test_real_data_page_states_the_swiss_rules(site):
    text = text_of(load(REAL))
    for phrase in ["Human Research Act", "CER-VD", "BASEC", "cantonal data protection law",
                   "coded", "code key", "general consent", "refused"]:
        assert phrase in text, phrase


def test_real_data_page_says_coded_data_are_never_anonymous(site):
    assert "with a code key are never anonymous" in text_of(load(REAL))


def test_real_data_page_covers_hfr_traps(site):
    text = load(REAL).get_text()  # no separator: keeps highlighted code intact
    for phrase in ["AHV", "patient number", "90 or older", "Quasi-identifiers", "implant", "DICOM", "AI",
                   "git status", "git diff --staged"]:
        assert phrase in text, phrase


def test_real_data_page_warns_about_derived_study_ids(site):
    text = load(REAL).get_text(" ")
    assert "study ID" in text and "initials" in text


def test_real_data_page_names_who_to_tell(site):
    text = text_of(load(REAL))
    assert "Tell your project lead right away" in text
    # HFR has no data protection officer.
    assert "data protection officer" not in text


def test_real_data_page_has_no_us_law(site):
    text = text_of(load(REAL))
    for us in ["HIPAA", "Safe Harbor", "IRB", "ZIP", "Social Security", "PHI"]:
        assert us not in text, us


def test_real_data_page_leaves_the_code_key_to_the_named_person(site):
    text = text_of(load(REAL))
    assert "the person the ethics application names for it" in text
    assert "project lead keeps the code key" not in text and "code key lives only with the project lead" not in text


def test_real_data_page_says_which_studies_general_consent_covers(site):
    text = text_of(load(REAL))
    assert "In a retrospective study" in text
    assert "A prospective study asks each patient for consent to that study" in text


def test_real_data_page_recommends_redcap(site):
    text = text_of(load(REAL))
    assert "Keep study data in the project's REDCap database" in text


def test_real_data_page_puts_code_in_a_private_repository(site):
    text = text_of(load(REAL))
    assert "a private repository in HFR Ortho's GitHub organization" in text
    assert "HFR Ortho's private GitHub organization" not in text


def test_language_heading_says_it_means_r_or_python(site):
    """The site has three human languages too, so "your language" needs saying."""
    headings = [h.get_text(strip=True) for h in load("getting-started/using-this-site.html").select("h2")]
    assert "Pick R or Python once" in headings and "Pick your language once" not in headings
