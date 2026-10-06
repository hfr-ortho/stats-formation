img <- read_tidy("hip_preservation_imaging.csv")

test_that("one row per hip: 80 hips in young adults", {
  expect_equal(nrow(img), 80)
  expect_equal(anyDuplicated(img$hip_id), 0)
  expect_true(all(img$age >= 18 & img$age <= 45))
})

test_that("the frog-leg view reads the alpha angle about 4 degrees higher than Dunn 45", {
  d <- img$alpha_frogleg_deg - img$alpha_dunn45_deg
  expect_gt(mean(d), 3)
  expect_lt(mean(d), 5)
  expect_lt(stats::t.test(img$alpha_frogleg_deg, img$alpha_dunn45_deg, paired = TRUE)$p.value, 0.001)
})

test_that("Budin and CT torsion correlate strongly but disagree more at the extremes", {
  r <- stats::cor(img$torsion_ct_deg, img$torsion_budin_deg)
  expect_gt(r, 0.80)
  expect_lt(r, 0.92)
  difference <- img$torsion_budin_deg - img$torsion_ct_deg
  average <- (img$torsion_budin_deg + img$torsion_ct_deg) / 2
  expect_lt(summary(stats::lm(difference ~ average))$coefficients["average", "Pr(>|t|)"], 0.05)
})
