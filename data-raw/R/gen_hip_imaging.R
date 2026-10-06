# Hip-preservation imaging (joint preservation): one row per hip in young
# adults assessed for hip-preservation surgery. The frog-leg view reads the
# alpha angle about 4 degrees higher than the Dunn 45-degree view of the same
# hip (page 7's paired t test). The modified Budin view tracks CT femoral
# torsion closely (r about 0.88) but compresses it, reading high at low
# torsion and low at high torsion: the two correlate without agreeing (page
# 10, and page 17's point that correlation is not agreement).
# Seed: 20261144, the fifth tried (20261104 + 10k). The Budin view's own noise
# also enters the Bland-Altman average and partly hides the proportional bias,
# so that test passes for only about half of all seeds; the first four missed it.

make_hip_imaging <- function(seed = 20261144, n = 80) {
  set.seed(seed)
  alpha_true <- stats::rnorm(n, 58, 10)
  torsion_ct <- stats::rnorm(n, 15, 9)
  tibble::tibble(
    hip_id            = sprintf("J%03d", seq_len(n)),
    age               = as.integer(round(clamp(stats::rnorm(n, 30, 7), 18, 45))),
    sex               = sample(c("Female", "Male"), n, TRUE, prob = c(0.45, 0.55)),
    alpha_dunn45_deg  = round(alpha_true + stats::rnorm(n, 0, 3), 1),
    alpha_frogleg_deg = round(alpha_true + 4 + stats::rnorm(n, 0, 3), 1),
    torsion_ct_deg    = round(torsion_ct, 1),
    torsion_budin_deg = round(2 + 0.8 * torsion_ct + stats::rnorm(n, 0, 3.8), 1),
    crossover_sign    = stats::rbinom(n, 1, 0.3)
  )
}
