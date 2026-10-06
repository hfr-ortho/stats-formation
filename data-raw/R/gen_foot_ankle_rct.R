# Foot & ankle RCT: cast vs removable boot after a midfoot injury, randomized
# 1:1. The effects are invented for teaching and say nothing about any HFR
# trial. EFAS score (European Foot and Ankle Society; 6 items scored 0-4, total
# 0-24, higher is better) and pain (NRS 0-10) at 6 weeks, 3 months, 6 months
# and 12 months. The boot leads early and the arms converge by 12 months (the
# group x time interaction on page 16). A missed visit keeps its row with every
# measure missing.

make_foot_ankle_rct <- function(seed = 20261102, n = 120) {
  set.seed(seed)
  wide <- tibble::tibble(
    patient_id = sprintf("F%03d", seq_len(n)),
    arm        = sample(rep(c("cast", "boot"), each = n / 2)),
    age        = as.integer(clamp(round(stats::rnorm(n, 42, 14)), 18, 80)),
    sex        = sample(c("Female", "Male"), n, TRUE),
    union_3mo  = stats::rbinom(n, 1, 0.88),
    .ability   = stats::rnorm(n, 0, 2.2)
  )
  visits <- tibble::tibble(
    visit     = c("6wk", "3mo", "6mo", "12mo"),
    nominal   = c(42L, 91L, 182L, 365L),
    jitter    = c(5L, 10L, 14L, 21L),
    p_missing = c(0.05, 0.08, 0.12, 0.15),
    efas_cast = c(9, 14, 18, 20.5),
    efas_boot = c(12, 17, 19, 20.5),
    pain_cast = c(5.0, 3.0, 2.0, 1.0),
    pain_boot = c(3.8, 2.4, 1.8, 1.0)
  )
  grid <- tidyr::expand_grid(wide, visits)
  m <- nrow(grid)
  boot <- grid$arm == "boot"
  efas <- ifelse(boot, grid$efas_boot, grid$efas_cast) + grid$.ability + stats::rnorm(m, 0, 2)
  pain <- ifelse(boot, grid$pain_boot, grid$pain_cast) - 0.3 * grid$.ability + stats::rnorm(m, 0, 1.6)
  visit_days <- grid$nominal + as.integer(round(stats::runif(m, -grid$jitter, grid$jitter)))
  missed <- stats::runif(m) < grid$p_missing

  long <- tibble::tibble(
    patient_id = grid$patient_id,
    arm        = grid$arm,
    visit      = grid$visit,
    visit_days = as.integer(visit_days),
    efas       = as.integer(clamp(round(efas), 0, 24)),
    pain_nrs   = as.integer(clamp(round(pain), 0, 10))
  )
  long[missed, c("visit_days", "efas", "pain_nrs")] <- NA
  list(wide = wide, long = long)
}
