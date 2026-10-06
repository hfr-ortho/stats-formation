# Hip fracture (trauma): one row per patient aged 65 or over, most over 80;
# 1,200 patients, about five years at a regional hospital. Death within 30
# days rises with age, ASA class, dementia and the time to surgery (odds about
# 1.5 times higher per extra day), so page 11's logistic regression has a
# plausible effect to find. About 85% are operated within 48 hours (page 5's
# binomial test against a 90% target). Survivors go home at least 3 days after
# surgery; days count from admission. Survivors of the first 30 days die at a
# lower, still age-dependent rate; follow-up stops at 1 year. Rates are tuned
# for teaching, not taken from a registry.

make_hip_fracture <- function(seed = 20261101, n = 1200) {
  set.seed(seed)
  age <- as.integer(65 + round(35 * stats::rbeta(n, 2.4, 2.0)))
  sex <- sample(c("Female", "Male"), n, TRUE, prob = c(0.72, 0.28))
  asa <- sample(1:4, n, TRUE, prob = c(0.03, 0.27, 0.55, 0.15))
  dementia <- stats::rbinom(n, 1, stats::plogis(-1.6 + 0.08 * (age - 84)))
  residence <- ifelse(stats::rbinom(n, 1, stats::plogis(
    -1.8 + 1.6 * dementia + 0.05 * (age - 84))) == 1, "nursing home", "home")
  fracture_type <- sample(c("femoral neck", "trochanteric"), n, TRUE, prob = c(0.55, 0.45))
  treatment <- ifelse(fracture_type == "trochanteric", "nail",
                      ifelse(stats::runif(n) < 0.85, "hemiarthroplasty", "screws"))
  hours_to_surgery <- round(stats::rlnorm(n, meanlog = log(26), sdlog = 0.6), 1)
  postop_days <- 3L + stats::rnbinom(n, size = 4, mu = 6)          # in hospital after surgery
  los_days <- as.integer(ceiling(hours_to_surgery / 24) + postop_days)

  death_30d <- stats::rbinom(n, 1, stats::plogis(
    -2.85 + 0.06 * (age - 84) + 0.5 * (asa - 3) + 0.4 * dementia + 0.4 * (hours_to_surgery - 30) / 24))
  later <- stats::rexp(n, rate = 0.0007 * exp(0.06 * (age - 84) + 0.4 * dementia))
  death_day <- ifelse(death_30d == 1, sample(2:30, n, TRUE), 30 + ceiling(later))
  death_day <- pmax(death_day, ceiling(hours_to_surgery / 24) + 1)   # deaths come after surgery
  death_30d <- as.integer(death_day <= 30)
  died <- as.integer(death_day <= 365)

  tibble::tibble(
    patient_id         = sprintf("H%04d", seq_len(n)),
    age, sex, asa, dementia, residence, fracture_type, treatment,
    hours_to_surgery,
    surgery_within_48h = as.integer(hours_to_surgery <= 48),
    los_days           = as.integer(pmin(los_days, ifelse(died == 1, death_day, Inf))),
    death_30d,
    followup_days      = as.integer(pmin(death_day, 365)),
    died
  )
}
