acl <- read_tidy("acl_cohort.csv")

test_that("350 reconstructions, followed for at least 2 years unless the graft failed", {
  expect_equal(nrow(acl), 350)
  expect_equal(anyDuplicated(acl$case_id), 0)
  expect_true(all(acl$followup_years >= 2 | acl$graft_failure == 1))
  expect_equal(acl$failure_2y, as.integer(acl$graft_failure == 1 & acl$followup_years <= 2))
})

test_that("graft failure within 2 years is unrelated to hamstring vs BPTB (a true null)", {
  d <- acl[acl$graft %in% c("hamstring", "BPTB"), ]
  expect_gt(stats::fisher.test(table(d$graft, d$failure_2y))$p.value, 0.2)
})

test_that("the hazard of graft failure rises with posterior tibial slope", {
  fit <- survival::coxph(survival::Surv(followup_years, graft_failure) ~ tibial_slope_deg, data = acl)
  hr <- exp(stats::coef(fit))[["tibial_slope_deg"]]
  expect_gt(hr, 1.10)
  expect_lt(hr, 1.35)
  expect_lt(summary(fit)$coefficients["tibial_slope_deg", "Pr(>|z|)"], 0.05)
})

test_that("return to sport at 12 months differs by graft", {
  expect_lt(stats::chisq.test(table(acl$graft, acl$rts_12mo))$p.value, 0.05)
})

test_that("return to sport rises with the pre-injury Tegner level and falls with age", {
  co <- summary(stats::glm(rts_12mo ~ graft + age + sex + tegner_preinjury,
                           family = binomial, data = acl))$coefficients
  expect_gt(co["tegner_preinjury", "Estimate"], 0)
  expect_lt(co["tegner_preinjury", "Pr(>|z|)"], 0.05)
  expect_lt(co["age", "Estimate"], 0)
  expect_lt(co["age", "Pr(>|z|)"], 0.05)
})

test_that("no one returns to sport at 12 months after the graft failed within the first year", {
  expect_true(all(acl$rts_12mo[acl$graft_failure == 1 & acl$followup_years < 1] == 0))
})

test_that("no graft fails in the first 3 months", {
  expect_true(all(acl$followup_years[acl$graft_failure == 1] >= 0.25))
})

test_that("the slope effect meets proportional hazards, as page 14 asks readers to check", {
  fit <- survival::coxph(survival::Surv(followup_years, graft_failure) ~ tibial_slope_deg, data = acl)
  expect_gt(survival::cox.zph(fit)$table["tibial_slope_deg", "p"], 0.05)
})
