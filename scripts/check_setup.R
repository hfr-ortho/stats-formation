# Checks that R is ready for the tutorials.
# Run from the repository folder:  Rscript scripts/check_setup.R
# or, in Positron's R console:     source("scripts/check_setup.R")

ok <- TRUE
report <- function(label, pass, fix) {
  cat(sprintf("%-40s %s\n", label, if (pass) "OK" else paste("PROBLEM -", fix)))
  if (!pass) ok <<- FALSE
}

# The project's packages are locked for one R version (renv.lock, "R": {"Version": ...}).
# Read it with base R only: this check runs before any package is installed.
lockfile <- if (file.exists("renv.lock")) paste(readLines("renv.lock", warn = FALSE), collapse = "\n") else ""
found <- regmatches(lockfile, regexec('"R"\\s*:\\s*\\{[^}]*?"Version"\\s*:\\s*"([0-9]+\\.[0-9]+)', lockfile,
                                      perl = TRUE))[[1]]
locked <- if (length(found) == 2) found[2] else NA_character_
running <- as.character(getRversion()[, 1:2])
report(sprintf("R version %s", getRversion()), identical(running, locked),
       if (is.na(locked)) "run this from the stats-formation folder"
       else sprintf("install R %s (any %s.x) from https://cloud.r-project.org", locked, locked))
report("project packages switched on (renv)", nzchar(Sys.getenv("RENV_PROJECT")),
       "start R inside the stats-formation folder")
for (pkg in c("knitr", "rmarkdown", "reticulate", "testthat", "tidyverse", "readxl",
             "tidyxl", "janitor", "gtsummary", "flextable", "smd", "effectsize",
             "DescTools", "survival", "ggsurvfit", "rstatix", "tidycmprsk",
             "broom.helpers", "lme4", "lmerTest", "emmeans", "PMCMRplus", "irr")) {
  report(paste("R package", pkg), requireNamespace(pkg, quietly = TRUE),
         "run renv::restore() in the R console")
}

report("practice data readable (data/cohort.csv)",
       file.exists("data/cohort.csv") && nrow(utils::read.csv("data/cohort.csv")) > 0,
       "run this from the stats-formation folder")

cat(if (ok) "\nAll good - you are ready.\n" else "\nFix the problems above, then run this again.\n")
if (!interactive()) quit(status = if (ok) 0 else 1)
