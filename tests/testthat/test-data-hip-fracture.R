hip <- read_tidy("hip_fracture.csv")
hip$delay_days <- hip$hours_to_surgery / 24

skewness <- function(x) mean((x - mean(x))^3) / stats::sd(x)^3

test_that("one row per patient: 400 patients aged 65 or over, most over 80", {
  expect_equal(nrow(hip), 400)
  expect_equal(anyDuplicated(hip$patient_id), 0)
  expect_true(all(hip$age >= 65 & hip$age <= 100))
  expect_gt(stats::median(hip$age), 80)
})

test_that("derived columns, treatment and timeline are consistent", {
  expect_equal(hip$surgery_within_48h, as.integer(hip$hours_to_surgery <= 48))
  expect_true(all(hip$treatment[hip$fracture_type == "trochanteric"] == "nail"))
  expect_true(all(hip$death_30d <= hip$died))
  expect_true(all(hip$followup_days[hip$death_30d == 1] <= 30))
  expect_true(all(hip$followup_days[hip$died == 0] == 365))
  dead <- hip$died == 1
  expect_true(all(hip$followup_days[dead] * 24 > hip$hours_to_surgery[dead]))   # death after surgery
  expect_true(all(hip$los_days[dead] <= hip$followup_days[dead]))
})

test_that("about 7% die within 30 days and about 85% are operated within 48 hours", {
  expect_gte(mean(hip$death_30d), 0.05)
  expect_lte(mean(hip$death_30d), 0.10)
  expect_gte(mean(hip$surgery_within_48h), 0.80)
  expect_lte(mean(hip$surgery_within_48h), 0.89)
})

test_that("time to surgery is right-skewed", {
  expect_gt(skewness(hip$hours_to_surgery), 1)
})

test_that("death within 30 days rises with the time to surgery and with age", {
  co <- summary(stats::glm(death_30d ~ delay_days + age, family = binomial, data = hip))$coefficients
  expect_gt(co["delay_days", "Estimate"], 0)
  expect_lt(co["delay_days", "Pr(>|z|)"], 0.05)
  expect_gt(co["age", "Estimate"], 0)
})

test_that("the codebook explains why ages of 90 or older are not grouped", {
  cb <- readr::read_csv(data_path("codebooks", "hip_fracture.csv"), show_col_types = FALSE,
                        col_types = readr::cols(.default = "c"))
  expect_match(cb$notes[cb$variable == "age"], "90 or older")
})
