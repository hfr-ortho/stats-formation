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
# JSON keys have no fixed order, so take the whole "R" block, drop what is nested in it
# (the "Repositories" list), and look for "Version" in what is left.
lockfile_r_version <- function(path) {
  if (!file.exists(path)) return(NA_character_)
  json <- paste(readLines(path, warn = FALSE), collapse = "\n")
  start <- regexpr('"R"\\s*:\\s*\\{', json, perl = TRUE)
  if (start < 0) return("")
  chars <- strsplit(substring(json, start + attr(start, "match.length") - 1), "")[[1]]
  end <- which(cumsum((chars == "{") - (chars == "}")) == 0)[1]
  if (is.na(end)) return("")
  block <- paste(chars[2:(end - 1)], collapse = "")
  repeat {
    flat <- gsub("\\[[^][]*\\]|\\{[^{}]*\\}", "", block, perl = TRUE)
    if (identical(flat, block)) break
    block <- flat
  }
  found <- regmatches(block, regexec('"Version"\\s*:\\s*"([0-9]+\\.[0-9]+)', block, perl = TRUE))[[1]]
  if (length(found) == 2) found[2] else ""
}
folder <- "the folder that holds renv.lock (stats-formation or stats-formation-main)"
locked <- lockfile_r_version("renv.lock")
running <- as.character(getRversion()[, 1:2])
report(sprintf("R version %s", getRversion()), identical(running, locked),
       if (is.na(locked)) paste("run this from", folder)
       else if (!nzchar(locked)) "couldn't read the R version in renv.lock: get a fresh copy of the repository (setup page, step 5)"
       else sprintf("install R %s (any %s.x) from https://cloud.r-project.org", locked, locked))
report("project packages switched on (renv)", nzchar(Sys.getenv("RENV_PROJECT")),
       paste("start R inside", folder))
for (pkg in c("knitr", "rmarkdown", "reticulate", "testthat", "tidyverse", "readxl",
             "tidyxl", "janitor", "gtsummary", "flextable", "smd", "effectsize",
             "DescTools", "survival", "ggsurvfit", "rstatix", "tidycmprsk",
             "broom.helpers", "lme4", "lmerTest", "emmeans", "PMCMRplus", "irr")) {
  report(paste("R package", pkg), requireNamespace(pkg, quietly = TRUE),
         "run renv::restore() in the R console")
}

report("practice data readable (data/cohort.csv)",
       file.exists("data/cohort.csv") && nrow(utils::read.csv("data/cohort.csv")) > 0,
       paste("run this from", folder))

cat(if (ok) "\nAll good - you are ready.\n" else "\nFix the problems above, then run this again.\n")
if (!interactive()) quit(status = if (ok) 0 else 1)
