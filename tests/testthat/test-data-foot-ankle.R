fa  <- read_tidy("foot_ankle_rct.csv")
fal <- read_tidy("foot_ankle_rct_long.csv")
seen_at <- function(v) fal[fal$visit == v & !is.na(fal$efas), ]

test_that("120 patients randomized 1:1, each with four visits", {
  expect_equal(nrow(fa), 120)
  expect_equal(anyDuplicated(fa$patient_id), 0)
  expect_equal(as.vector(table(fa$arm)[c("boot", "cast")]), c(60, 60))
  expect_equal(nrow(fal), 4 * 120)
  expect_equal(nrow(dplyr::distinct(fal, patient_id, visit)), nrow(fal))
  j <- dplyr::left_join(fal, fa[, c("patient_id", "arm")], by = "patient_id", suffix = c("", "_wide"))
  expect_equal(j$arm, j$arm_wide)
})

test_that("a missed visit has every measure missing, and misses rise to about 15%", {
  missed <- is.na(fal$efas)
  expect_equal(missed, is.na(fal$pain_nrs))
  expect_equal(missed, is.na(fal$visit_days))
  miss <- tapply(missed, fal$visit, mean)
  expect_lt(miss[["6wk"]], 0.10)
  expect_gt(miss[["12mo"]], 0.08)
  expect_lt(miss[["12mo"]], 0.25)
})

test_that("the boot gives a better EFAS score at 3 months, by 2 to 4 points", {
  d <- seen_at("3mo")
  diff <- mean(d$efas[d$arm == "boot"]) - mean(d$efas[d$arm == "cast"])
  expect_gt(diff, 2)
  expect_lt(diff, 4)
  expect_lt(stats::t.test(efas ~ arm, data = d)$p.value, 0.01)
})

test_that("the boot gives less pain at 6 weeks", {
  d <- fal[fal$visit == "6wk" & !is.na(fal$pain_nrs), ]
  expect_lt(mean(d$pain_nrs[d$arm == "boot"]), mean(d$pain_nrs[d$arm == "cast"]))
  expect_lt(stats::wilcox.test(pain_nrs ~ arm, data = d, exact = FALSE)$p.value, 0.05)
})

test_that("the arms converge by 12 months: a group x time interaction", {
  d <- seen_at("12mo")
  expect_lt(abs(mean(d$efas[d$arm == "boot"]) - mean(d$efas[d$arm == "cast"])), 1)
  fit <- lmerTest::lmer(efas ~ arm * visit + (1 | patient_id), data = fal)
  expect_lt(stats::anova(fit)["arm:visit", "Pr(>F)"], 0.01)
})

test_that("with a boot, the EFAS score keeps changing over the year (Friedman)", {
  b <- fal[fal$arm == "boot" & fal$visit %in% c("6wk", "3mo", "12mo"), c("patient_id", "visit", "efas")]
  w <- tidyr::pivot_wider(b, names_from = visit, values_from = efas)
  w <- w[stats::complete.cases(w), ]
  expect_lt(stats::friedman.test(as.matrix(w[, c("6wk", "3mo", "12mo")]))$p.value, 0.001)
})
