from sitelib import load, text_of

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
    assert "data protection officer" in text_of(load(REAL))


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
