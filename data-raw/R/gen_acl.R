# ACL reconstruction (sports): one row per primary reconstruction. Graft
# failure depends on posterior tibial slope (hazard ratio about 1.22 per
# degree) but not on the graft, so failure within 2 years is a true null for
# hamstring vs BPTB (page 6). Return to sport at 12 months differs by graft and
# rises with the pre-injury Tegner level. Everyone is followed for at least 2
# years unless the graft fails, so failure within 2 years is known for all.
# Rates are tuned for teaching.

make_acl_cohort <- function(seed = 20261103, n = 350) {
  set.seed(seed)
  age   <- as.integer(clamp(round(15 + stats::rgamma(n, shape = 3, scale = 4.5)), 15, 50))
  sex   <- sample(c("Female", "Male"), n, TRUE, prob = c(0.42, 0.58))
  graft <- sample(c("BPTB", "hamstring", "quadriceps"), n, TRUE, prob = c(0.35, 0.45, 0.20))
  tibial_slope_deg <- round(clamp(stats::rnorm(n, 10, 2.5), 4, 18), 1)
  tegner_preinjury <- as.integer(clamp(round(stats::rnorm(n, 6.5 - 0.05 * (age - 28), 1.6)), 1, 10))
  graft_effect <- unname(c(BPTB = 0.5, hamstring = -0.1, quadriceps = -0.6)[graft])
  rts_12mo <- stats::rbinom(n, 1, stats::plogis(
    0.1 + graft_effect + 0.35 * (tegner_preinjury - 6.5) - 0.05 * (age - 28)))

  rate   <- 0.03 * exp(log(1.22) * (tibial_slope_deg - 10) - 0.03 * (age - 28))   # per year
  t_fail <- stats::rexp(n, rate)
  censor <- stats::runif(n, 2, 6)
  graft_failure  <- as.integer(t_fail <= censor)
  followup_years <- pmax(0.01, round(pmin(t_fail, censor), 2))

  tibble::tibble(
    case_id = sprintf("A%04d", seq_len(n)),
    age, sex, graft, tibial_slope_deg, tegner_preinjury, rts_12mo,
    followup_years, graft_failure,
    failure_2y = as.integer(graft_failure == 1 & followup_years <= 2)
  )
}
