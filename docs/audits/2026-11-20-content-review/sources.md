# Sources behind the findings marked E

Part of the [content review of 20.11.2026](README.md). Task 3.1 of the fix plan (`docs/superpowers/plans/2026-11-20-content-review-fixes.md`). Opened on 20.11.2026.

Several findings in [accuracy.md](accuracy.md) rest on a statistical principle and a reference that was cited from memory. This file records, for each reference, whether its text was opened and what it actually says, so that no correction goes onto the site from memory.

**Status**

- **read:** the text was obtained on 20.11.2026 and the supporting passage was found in it. The quotation is verbatim; its location is given so it can be found again.
- **abstract only:** only the abstract was obtained (PubMed). The quotation is from the abstract, and only what the abstract itself says counts as supported.
- **not obtained:** no text was obtained. What was tried is listed.

**Supports the fix** says whether the passage supports the claim the planned fix needs: yes, partly (the source says something narrower or different), or no.

Typography in quotations: italics are dropped; symbols lost in PDF-to-text conversion are restored in square brackets.

---

## 1. Sjölander & Greenland 2013

- **Citation:** Sjölander A, Greenland S. Ignoring the matching variables in cohort studies – when is it valid and why? Stat Med 2013;32(27):4696–4708. doi:10.1002/sim.5879. PMID 23761197.
- **Findings:** B10 (p7:775 and the code comments at p7:723 and p7:737 call an unstratified Cox model on matched pairs "the wrong model"; p3:440 "Treat matched sets like pairs").
- **Claim the fix needs:** in a matched cohort, an unstratified Cox model (matching ignored) is an accepted analysis, provided the pairs get a cluster-robust standard error; the rule against it comes from matched case-control studies.
- **Status:** read.
- **Passages:**
  - Section 2 "No additional confounders", second-to-last paragraph. The hazard ratio from a Cox model fitted to a matched cohort, ignoring the matching variables, is "a consistent estimator of the causal hazard ratio in a population where the matching variables are distributed as in the matched cohort", provided the model is correct, censoring is noninformative given exposure and the matching variables, and the matching variables are the only confounders. The same paragraph says this unstratified (marginal) ratio is unbiased "for the population effect standardized to the exposed".
  - Section 9 "Conclusion": "we would recommend some adjustment for the matching variables when analyzing matched cohort data, although a matched analyses per se is not needed."
- **Supports the fix:** partly. The paper supports "not wrong": ignoring the matching in a matched cohort gives a valid estimate of the marginal hazard ratio, if the matching variables are the only confounders, and the argument does not carry over to effect estimation in matched case-control studies (abstract). Three points are narrower than the finding: (1) the paper does not discuss cluster-robust standard errors for matched cohorts; the only passage on standard errors (section 3, case-control studies) says a correct p-value must take the correlation within matched sets into account, "for example, by properly adjusting the denominator of the Wald test statistic or by conditioning on the matching variables". (2) The unstratified and the stratified hazard ratios estimate different things (marginal against conditional; the hazard ratio is noncollapsible, section 2). The unstratified one is a population-level hazard ratio: the effect in a population whose matching variables are distributed as in the matched cohort (with matching of unexposed to exposed, the effect standardized to the exposed), not a within-pair effect. (3) The authors' own recommendation is "some adjustment for the matching variables", and adding other covariates while ignoring the matching can leave bias (section 4, conclusion). The paper does not address frequency matching or propensity-score matching by name, so it does not settle the p3:440 part. What this means for the fix: page 7 must describe the unstratified model's hazard ratio as this population-level (marginal) effect, not as the same quantity as the stratified, within-pair hazard ratio.
- **Text from:** Karolinska Institutet, Department of Medical Epidemiology and Biostatistics (the first author's department), course materials: <https://www.meb.ki.se/biostat/cc2024/papers/extras/Sjolander&Greenland_StatMed_2013%20ignoring%20the%20matching%20cohort%20studies.pdf> (publisher's typeset PDF). Citation checked against PubMed and Crossref.
- **Citation check:** "Sjölander & Greenland, Statistics in Medicine 2013" is right.

## 2. Hernán 2010

- **Citation:** Hernán MA. The hazards of hazard ratios. Epidemiology 2010;21(1):13–15. doi:10.1097/EDE.0b013e3181c1ea43. PMID 20010207. PMC3653612.
- **Findings:** B17 (p14:548: the hazard ratio of 0.43 after 6 months, called merely "imprecise").
- **Claim the fix needs:** a hazard ratio for a later period compares only those who survived the earlier period, so the groups are no longer like-for-like; restricted mean survival time and fixed-time differences are alternatives.
- **Status:** read (full text, PMC).
- **Passages:**
  - Paragraph introducing "Problem 2": "This brings us to Problem 2: the period-specific HRs have a built-in selection bias."
  - Same paragraph: "the calculation of the HR during year t was restricted to women who did not develop coronary heart disease—the “survivors”".
- **Supports the fix:** partly. It supports the main point fully: a period-specific hazard ratio is computed among survivors and has a built-in selection bias, so it can fall below 1 "even if hormone therapy has no truly preventive effect in any woman at any time". The alternatives it names are adjusted survival curves (and accelerated failure time models), and "a series of average HRs for increasingly longer periods of follow-up". It does not mention restricted mean survival time; that part of the fix needs another source or should name survival curves or fixed-time differences instead.
- **Text from:** PubMed Central full text, PMC3653612, <https://pmc.ncbi.nlm.nih.gov/articles/PMC3653612/> (first through the PubMed full-text service, which dropped the italic letter t; the quotation was then re-checked against the PMC page itself).
- **Citation check:** "Hernán, Epidemiology 2010" is right.

## 3. Bland & Altman 1986

- **Citation:** Bland JM, Altman DG. Statistical methods for assessing agreement between two methods of clinical measurement. Lancet 1986;1(8476):307–310. PMID 2868172.
- **Findings:** B13 (correlation depends on the range sampled; page 10), B20 (p17:241: limits of agreement cover 95% of differences only if the differences are roughly normal).
- **Claims the fix needs:** (a) r rises and falls with the range of the patients sampled; (b) the 95% coverage of the limits of agreement assumes roughly normal differences.
- **Status:** read.
- **Passages:**
  - Section "Inappropriate use of correlation coefficient", point (3): "Correlation depends on the range of the true quantity in the sample. If this is wide, the correlation will be greater than if it is narrow."
  - Section "Measuring agreement": "If the differences are Normally distributed (Gaussian), 95% of differences will lie between these limits".
- **Supports the fix:** yes, for both. The same section adds that the measurements themselves need not be normal and that the differences can be checked with a histogram.
- **Text from:** the author's full-text copy on Martin Bland's University of York site, <https://www-users.york.ac.uk/~mb55/meas/ba.htm>. Citation checked against PubMed.
- **Citation check:** right.

## 4. Bland & Altman 1995

- **Citation:** Bland JM, Altman DG. Comparing methods of measurement: why plotting difference against standard method is misleading. Lancet 1995;346(8982):1085–1087. doi:10.1016/s0140-6736(95)91748-9. PMID 7564793.
- **Findings:** B13 (p10:181 and p7:910 show a trend by grouping the difference on one method's own value; the fix groups by the mean of the two methods).
- **Claim the fix needs:** relating the difference to one method's own value creates or distorts a trend; relate it to the mean of the two methods.
- **Status:** read.
- **Passages:**
  - Summary: "A plot of the difference against the standard measurement is sometimes suggested, but this will always appear to show a relationship between difference and magnitude when there is none."
  - Summary: "A plot of the difference against the average of the standard and new measurements is unlikely to mislead in this way."
- **Supports the fix:** yes, for the claim as worded above; finding B13's word "exaggerates" should become "can create or distort". It fully supports grouping by the mean of the two methods. "Exaggerates" is narrower than the paper: the paper shows that the artifact's direction depends on which method is used (negative against the standard, positive against the test method: "both plots are liable to be very misleading and any relationship found liable to be an artifact of the method of analysis", section "Plotting difference against standard"). A trend that is really there can therefore be exaggerated or masked. The paper speaks of plots and correlations; the pages use a table grouped by one method, which is the same comparison in tabular form. Safer wording for the fix: "can create or distort a trend".
- **Text from:** the author's full-text copy, <https://www-users.york.ac.uk/~mb55/meas/diffplot.htm>. Citation checked against PubMed. The York text of the summary reads "relationship" where the PubMed abstract reads "relation" ("…appear to show a relation between difference and magnitude…"); the quotation above follows the York text.
- **Citation check:** right. Note: the header of the York copy labels the paper "(1986)"; that is a typo on the host page, the Lancet volume 346 is 1995 (PubMed).

## 5. Feinstein & Cicchetti 1990

- **Citation:** Feinstein AR, Cicchetti DV. High agreement but low kappa: I. The problems of two paradoxes. J Clin Epidemiol 1990;43(6):543–549. doi:10.1016/0895-4356(90)90158-l. PMID 2348207.
- **Findings:** B11 (kappa depends on prevalence; kappas can't be compared across studies with different case mixes; Landis and Koch labels given without this).
- **Claim the fix needs:** with one dominant category, raters can agree on most cases and still get a low kappa, so kappa depends on prevalence and kappas from samples with different case mixes are not comparable.
- **Status:** abstract only.
- **Passage:** Abstract: "In one paradox, a high value of p0 can be drastically lowered by a substantial imbalance in the table's marginal totals either vertically or horizontally."
- **Supports the fix:** partly. The abstract supports high agreement with low kappa when the marginal totals are imbalanced (one category dominates), which is the prevalence effect. It does not itself state that kappas can't be compared across studies with different case mixes; that is a reasonable inference but is not in the abstract. The full text was not obtained.
- **Tried:** PubMed (no PMC copy); the publisher (Elsevier) was not opened because the article is subscription-only.
- **Text from:** PubMed abstract, <https://pubmed.ncbi.nlm.nih.gov/2348207/>.
- **Citation check:** right.

## 6. Cochran 1954

- **Citation:** Cochran WG. Some methods for strengthening the common χ² tests. Biometrics 1954;10(4):417–(last page not confirmed). doi:10.2307/3001616 (Crossref gives the first page only).
- **Findings:** B24 (p8:465, p10:437 state "every expected count should be at least 5"; Cochran's rule for larger tables allows up to 20% of cells below 5).
- **Claim the fix needs:** the usual rule allows up to 20% of expected counts below 5 (and none below 1); "at least 5 in every cell" is the strict version.
- **Status:** not obtained.
- **Tried:** PubMed (not indexed); Crossref (citation only); the article is on JSTOR, subscription-only, and was not downloaded.
- **Alternative source, read:** Bewick V, Cheek L, Ball J. Statistics review 8: Qualitative data – tests of association. Crit Care 2004;8:46–53. doi:10.1186/cc2428. PMID 14975045. PMC420070. Section "Limitations": the rule "attributed to Cochran [5] is that no cell in the table should have an expected frequency of less than one" and that "no more than 20% of the cells should have an expected frequency of less than five." (Its reference 5 is Bland's textbook, not Cochran's paper.) Text from <https://pmc.ncbi.nlm.nih.gov/articles/PMC420070/>.
- **Supports the fix:** partly. The alternative source states the 20% rule and attributes it to Cochran, through a textbook. What Cochran wrote in 1954 was not seen.
- **Citation check:** author, title, journal, year, volume, issue and first page confirmed on Crossref; last page not confirmed.

## 7. Peduzzi et al. 1995

- **Citation:** Peduzzi P, Concato J, Feinstein AR, Holford TR. Importance of events per independent variable in proportional hazards regression analysis. II. Accuracy and precision of regression estimates. J Clin Epidemiol 1995;48(12):1503–1510. doi:10.1016/0895-4356(95)00048-8. PMID 8543964.
- **Findings:** B24 (p14:215 "A Cox model needs about 10 events per term" presented as a requirement), C3 (10 per predictor on p12 against 10 per term on p14).
- **Claims the fix needs:** (a) 10 events per variable is a rule of thumb, not a requirement; (b) whether a "variable" means a predictor or a coefficient.
- **Status:** abstract only.
- **Passage:** Abstract: "Although a single boundary level for avoiding problems is not easy to choose, the value of EPV = 10 seems most prudent."
- **Supports the fix:** partly. It supports (a): the authors present 10 as a prudent choice, not a sharp boundary. It does not settle (b): the abstract counts "events per variable" with "seven predictor variables" and does not say how a predictor with several categories is counted.
- **Tried:** PubMed (no PMC copy); publisher (Elsevier) subscription-only, not opened.
- **Text from:** PubMed abstract, <https://pubmed.ncbi.nlm.nih.gov/8543964/>.
- **Citation check:** right.

## 8. Vittinghoff & McCulloch 2007

- **Citation:** Vittinghoff E, McCulloch CE. Relaxing the rule of ten events per variable in logistic and Cox regression. Am J Epidemiol 2007;165(6):710–718. doi:10.1093/aje/kwk052. PMID 17182981. Published online 20.12.2006.
- **Findings:** B24, C3 (as for Peduzzi).
- **Claims the fix needs:** the 10-events rule is contested and can be relaxed; and what is counted.
- **Status:** abstract only.
- **Passage:** Abstract: "The rule of thumb that logistic and Cox models should be used with a minimum of 10 outcome events per predictor variable (EPV) […] may be too conservative."
- **Supports the fix:** partly. It supports "a contested rule of thumb that may be too conservative" (the abstract also says the rule "can be relaxed"). It does not support the finding's phrase "a rough upper limit"; better wording is "a rule of thumb, which some simulation studies find too strict". On counting, the abstract says "per predictor variable", which does not support the planned "per coefficient".
- **Tried:** PubMed (no PMC copy); the publisher's page and PDF (academic.oup.com) returned a bot check ("Just a moment..."). Copies on SciSpace and a ResearchGate discussion thread were found but not used: they are third-party uploads of a subscription article.
- **Text from:** PubMed abstract, <https://pubmed.ncbi.nlm.nih.gov/17182981/>.
- **Citation check:** right as "2007" (print). Some sources cite it as 2006, the online date (for example Harrell's course notes, below).
- **Alternative source for C3 (counting), read:** Harrell FE. Regression Modeling Strategies, course notes, section 4.4 "Overfitting and Limits on Number of Predictors", <https://hbiostat.org/rmsc/multivar.html> (the same site the glossary already cites). The limit is written p < m/15, where "\(p\) is number of parameters in full model or number of candidate parameters in a stepwise analysis, and \(m\) is the effective sample size". This supports counting coefficients (parameters), not predictors. Note that Harrell's divisor is 15, not 10, and his context is overfitting in prediction models.

## 9. Delacre et al. 2019

- **Citation:** Delacre M, Leys C, Mora YL, Lakens D. Taking parametric assumptions seriously: arguments for the use of Welch's F-test instead of the classical F-test in one-way ANOVA. Int Rev Soc Psychol 2019;32(1):13, 1–12. doi:10.5334/irsp.198.
- **Findings:** C1 (page 6: "Use Welch's test from the start"; pages 8 and 15: classic ANOVA unless the largest SD is more than about twice the smallest). Decision D2.
- **Claim the fix needs:** Welch's ANOVA is the safe default; choosing by checking the spreads first is unreliable.
- **Status:** read (open access).
- **Passages:**
  - Abstract: "Our simulations show that under a range of realistic scenarios, the W-test is a better alternative and we therefore recommend using the W-test by default when comparing means."
  - Section "Recommendations": "tests of the equal variances assumption will often fail to detect differences when these are present".
- **Supports the fix:** yes, for Welch as the safe default; partly for the spread check: the paper's argument is against formal tests of equal variances as a first step ("tests of the equal variances assumption will often fail to detect differences when these are present"); it does not evaluate a judgment of the spreads from a plot, which is what the site's rule is. Two further caveats from the same section: the authors say the classical F-test "should be avoided", which goes further than D2 (keeping the classic example with Welch beside it); and with fewer than 50 observations per group and skewed data, "the W-test will not control Type I error rate". The paper's field is psychology; its argument is from simulations.
- **Text from:** the publisher's article page and PDF, <https://www.rips-irsp.com/article/10.5334/irsp.198/>. Citation checked against the PDF's header and Crossref.
- **Citation check:** right. Note: accuracy.md does not name this paper under C1; it is named only in the plan.

## 10. de Vet et al. 2006

- **Citation:** de Vet HCW, Terwee CB, Knol DL, Bouter LM. When to use agreement versus reliability measures. J Clin Epidemiol 2006;59(10):1033–1039. doi:10.1016/j.jclinepi.2005.10.015. PMID 16980142.
- **Findings:** B20 (the standard error of measurement and the minimal detectable change appear nowhere; "orthopaedic reliability papers report them routinely").
- **Claims the fix needs:** (a) the SEM is the basic agreement measure for continuous measurements, and the minimal detectable change is derived from it; (b) these are reported routinely.
- **Status:** read.
- **Passages:**
  - Section 8 "Typical parameters for agreement and reliability", p. 1038: "the SEM is usually the basic parameter of agreement for measurements on a continuous scale."
  - Section 9 "Clinical interpretation", p. 1038: "The smallest detectable change (SDC) is based on this measurement error, and is defined as 1.96 [×] [√]2 [×] SEM."
- **Supports the fix:** partly. It supports (a), with two details the fix must follow: the paper's term is "smallest detectable change (SDC)" (a footnote adds "smallest detectable difference (SDD)"), not "minimal detectable change", and it distinguishes SEM for agreement (includes systematic differences between raters) from SEM for consistency (excludes them; sections 5 to 7). It contradicts (b) as of 2006: section 4, p. 1035, is titled "Agreement parameters are neglected in medical sciences" and ends "Apparently, agreement parameters have not yet struck root in medical sciences." The claim that orthopaedic papers report them "routinely" needs another source or should be dropped.
- **Text from:** the publisher's PDF on the VU Amsterdam research portal, <https://research.vu.nl/ws/portalfiles/portal/2885021/263494.pdf>. Citation checked against PubMed.
- **Citation check:** right. The glossary already cites this paper's abstract for `agreement`.

## 11. Greenland et al. 2016

- **Citation:** Greenland S, Senn SJ, Rothman KJ, Carlin JB, Poole C, Goodman SN, Altman DG. Statistical tests, P values, confidence intervals, and power: a guide to misinterpretations. Eur J Epidemiol 2016;31(4):337–350. doi:10.1007/s10654-016-0149-3. PMID 27209009. PMC4877414.
- **Findings:** B8 (p > 0.05 is not "no difference"; p is not the chance that there is no difference; p3:169; the CI section never says what "95%" refers to).
- **Claims the fix needs:** (a) p is not the probability that the null hypothesis is true; (b) p > 0.05 does not show absence of an effect; (c) what the 95% of a CI refers to.
- **Status:** read (full text, PMC).
- **Passages:**
  - Section "Common misinterpretations of single P values", misinterpretation 1: "The P value assumes the test hypothesis is true—it is not a hypothesis probability".
  - Same section, misinterpretation 6: "it is a mistake to conclude from P > 0.05 that a study found “no association” or “no evidence” of an effect."
  - Section "Moving from tests to estimates": "If one calculates, say, 95 % confidence intervals repeatedly in valid applications, 95 % of them, on average, will contain (i.e., include or cover) the true effect size."
- **Supports the fix:** yes, for all three. Misinterpretation 19 in the same paper also says a single reported interval does not have a 95% chance of containing the true value, which the CI sentence should respect.
- **Text from:** <https://pmc.ncbi.nlm.nih.gov/articles/PMC4877414/>. Item numbers counted from the article's numbered list.
- **Citation check:** right.

## 12. CONSORT 2010 explanation and elaboration, item 15 (and CONSORT 2025)

- **Citation:** Moher D, Hopewell S, Schulz KF, Montori V, Gøtzsche PC, Devereaux PJ, Elbourne D, Egger M, Altman DG. CONSORT 2010 explanation and elaboration: updated guidelines for reporting parallel group randomised trials. BMJ 2010;340:c869. doi:10.1136/bmj.c869. PMID 20332511. PMC2844943. (Author list as printed on the PMC copy.)
- **Findings:** B23 (page 2's list of who should report baseline p-values leaves out randomized trials).
- **Claim the fix needs:** in a randomized trial, significance tests of baseline differences are uninformative, because any baseline difference is due to chance.
- **Status:** read.
- **Passage:** Item 15 "A table showing baseline demographic and clinical characteristics for each group", Explanation: "we already know that any differences are caused by chance. Tests of baseline differences are not necessarily wrong, just illogical."
- **Supports the fix:** yes.
- **Newer version, read:** CONSORT 2010 has been replaced by CONSORT 2025. Hopewell S, Chan AW, Collins GS, et al. CONSORT 2025 explanation and elaboration: updated guideline for reporting randomised trials. BMJ 2025;389:e081124. doi:10.1136/bmj-2024-081124. PMID 40228832. PMC11995452. The baseline table is now item 25: "Significance testing of baseline differences is not recommended and should not be reported." <https://pmc.ncbi.nlm.nih.gov/articles/PMC11995452/>. The site should cite CONSORT 2025, item 25.
- **Text from:** <https://pmc.ncbi.nlm.nih.gov/articles/PMC2844943/>.
- **Citation check:** "CONSORT 2010 explanation, item 15" is right for 2010 but out of date: the current guideline is CONSORT 2025, where the item is number 25.

## 13. The STROBE statement

- **Citation:** von Elm E, Altman DG, Egger M, Pocock SJ, Gøtzsche PC, Vandenbroucke JP; STROBE Initiative. The Strengthening the Reporting of Observational Studies in Epidemiology (STROBE) statement: guidelines for reporting observational studies. PLoS Med 2007;4(10):e296. doi:10.1371/journal.pmed.0040296. PMID 17941714. PMC2020495. Published simultaneously in other journals (for example Lancet 2007;370:1453, PMID 18064739). Explanation and elaboration: Vandenbroucke JP et al. PLoS Med 2007;4(10):e297. doi:10.1371/journal.pmed.0040297. PMID 17941715. PMC2020496.
- **Findings:** B3 (page 18's model Methods omit the design, selection and eligibility, one joint per patient, assessment windows, ethics approval and consent, sample-size justification, missing data, prespecification, registry completeness, an MCID).
- **Claim the fix needs:** STROBE asks a cohort study's Methods to report these items; a link to the checklist.
- **Status:** read (statement, explanation and elaboration, and the cohort checklist PDF).
- **Passages:**
  - Cohort checklist, items 4, 6(a), 10 and 12(c): "Present key elements of study design early in the paper"; "Give the eligibility criteria, and the sources and methods of selection of participants. Describe methods of follow-up"; "Explain how the study size was arrived at"; "Explain how missing data were addressed".
  - Explanation and elaboration, item 4, Explanation: "We recommend that authors refrain from simply calling a study ‘prospective' or ‘retrospective' because these terms are ill defined".
- **Supports the fix:** partly. STROBE's Methods items (4 to 12) cover the design, setting and dates (which include the assessment windows), eligibility and selection, follow-up, variables, bias, study size, and missing data; item 3 asks for prespecified hypotheses, and item 16(a) asks for unadjusted and confounder-adjusted estimates (relevant to B4). Not STROBE items: ethics approval, consent, an MCID, and the registry's completeness. Those come from journals' own requirements or are good practice, so the "What a real Methods also needs" box (D5) must not attribute them to STROBE. One part of B3 runs against STROBE: it asks for the design "in words (retrospective or prospective cohort)", while STROBE asks authors not simply to use those labels but to describe how and when the data were collected.
- **Checklist link for the site (opened 20.11.2026):** <https://www.strobe-statement.org/checklists/>; cohort checklist PDF <https://www.strobe-statement.org/download/strobe-checklist-cohort-studies-pdf>.
- **Text from:** <https://pmc.ncbi.nlm.nih.gov/articles/PMC2020495/>, <https://pmc.ncbi.nlm.nih.gov/articles/PMC2020496/> and the checklist PDF above.
- **Citation check:** right ("the STROBE statement", 2007).

## 14. Westreich & Greenland 2013

- **Citation:** Westreich D, Greenland S. The table 2 fallacy: presenting and interpreting confounder and modifier coefficients. Am J Epidemiol 2013;177(4):292–298. doi:10.1093/aje/kws412. PMID 23371353. PMC3626058.
- **Findings:** C4 (page 14's warning "the covariates' own hazard ratios aren't findings" against page 12's linear and logistic Results, which report every covariate's coefficient as a finding).
- **Claim the fix needs:** in a model built to estimate one exposure's effect, the other coefficients are not interpretable in the same way and should not be reported as findings.
- **Status:** read.
- **Passages:**
  - Section "Same model, different degrees of confounding": "a model sufficient for estimating the average effect of the primary study exposure can be insufficient to provide an unbiased estimate of secondary effects."
  - Section "Discussion": "the assumption that all estimates reported in Table 2 are for total effects is not warranted."
- **Supports the fix:** yes, with one nuance: the paper says the covariates' coefficients are different kinds of effects (direct rather than total) and may be confounded, not that they are meaningless. Its recommendation is to report only the main exposure's estimates, with the adjustment covariates in a footnote (section "Avoiding Table 2 fallacies"), or to label the other estimates as direct effects. "Not findings about those variables" is a fair plain-words summary; "meaningless" would not be.
- **Text from:** <https://pmc.ncbi.nlm.nih.gov/articles/PMC3626058/>, fetched as a plain HTTP request (curl, with a browser user-agent string) and searched as text; the same route worked again in the fix round on 20.11.2026. The PubMed full-text service returned an empty body for this article. A reader whose browser gets a bot check at PMC should re-open it before the site relies on it.
- **Citation check:** right.

## 15. Greenland, Robins & Pearl 1999

- **Citation:** Greenland S, Robins JM, Pearl J. Confounding and collapsibility in causal inference. Stat Sci 1999;14(1):29–46. doi:10.1214/ss/1009211805.
- **Findings:** C5 (p12:652: the groups are alike, "so adjustment shouldn't change much", for the Cox model; page 14 says a hazard ratio shifts when a strong predictor is added even without confounding).
- **Claim the fix needs:** odds ratios and hazard ratios are noncollapsible: adding a strong predictor of the outcome changes them even when it is not a confounder.
- **Status:** read.
- **Passages:**
  - Section 5.1 "The Divergence", p. 39: "confounding may occur with or without noncollapsibility and noncollapsibility may occur with or without confounding".
  - Same section and page, after Table 2: "the stratum-specific odds ratios must be farther from 1 than the unconditional odds ratio if the latter is not 1".
- **Supports the fix:** yes for the odds ratio; the paper's worked example (Table 2) is an odds ratio and it does not name the hazard ratio. For the hazard ratio, Sjölander & Greenland 2013 (section 1 above, section 2 of that paper) states it directly: "the odds ratio and hazard ratio are noncollapsible, meaning that they may change upon stratification by a perfectly balanced (and thus nonconfounding) factor". Together they support the fix for page 12's Cox section. For a linear model (difference of means) the effect is collapsible, so "shouldn't change much" stays right there.
- **Text from:** the authors' copy, UCLA Cognitive Systems Laboratory Technical Report R-252 (December 1998), listed on Judea Pearl's publication page <https://bayes.cs.ucla.edu/csl_papers.html> and served at <https://ftp.cs.ucla.edu/pub/stat_ser/r252.pdf>. The file is a technical-report cover sheet followed by a scan of the published Statistical Science pages; it has no text layer, so it was read by OCR and the page with both quotations (p. 39) was checked by eye against the scan. A JSTOR copy reposted on a third-party university page, used in the first draft of this file, is no longer the source.
- **Citation check:** right. Crossref and Project Euclid list the authors as Greenland, Pearl, Robins; the printed article reads "Sander Greenland, James M. Robins and Judea Pearl", the order in the brief.

## 16. Little & Rubin

- **Citation:** Little RJA, Rubin DB. Statistical Analysis with Missing Data. 3rd ed. Wiley; 2019. doi:10.1002/9781119482260 (edition, year, publisher and DOI from Crossref; the place of publication was not checked).
- **Findings:** B16 (p16:90: missing at random means "missing depends on things you measured"; the protection holds only for measured things the model includes).
- **Claim the fix needs:** a likelihood-based analysis (here a mixed model) is protected under missing at random only if the variables that predict missingness are in the model.
- **Status:** not obtained.
- **Tried:** a book; no open copy exists from the publisher. Not read.
- **Alternative source, read:** Sterne JAC, White IR, Carlin JB, Spratt M, Royston P, Kenward MG, Wood AM, Carpenter JR. Multiple imputation for missing data in epidemiological and clinical research: potential and pitfalls. BMJ 2009;338:b2393. doi:10.1136/bmj.b2393. PMID 19564179. PMC2714692. Section "Plausibility of missing at random assumption": the assumption "may be reasonable if a variable that is predictive of missing data […] is included in the imputation model, but not if the variable is omitted from the model." Section "Statistical methods to handle missing data": complete-case analysis of a once-measured outcome is unbiased "provided that all variables associated with the outcome being missing can be included as covariates". Text from <https://pmc.ncbi.nlm.nih.gov/articles/PMC2714692/>.
- **Supports the fix:** partly. The alternative source states the principle (the variables that predict missingness must be in the model for the missing-at-random assumption to protect the analysis) for imputation models and for complete-case regression. It mentions random-effects models only as a way to use incomplete data and does not state the principle for mixed models in so many words.

## 17. Altman & Bland 1995

- **Citation:** Altman DG, Bland JM. Absence of evidence is not evidence of absence. BMJ 1995;311(7003):485. doi:10.1136/bmj.311.7003.485. PMID 7647644. PMC2550545.
- **Findings:** B8 (p > 0.05 is not "no difference").
- **Claim the fix needs:** a nonsignificant result does not show there is no difference.
- **Status:** read.
- **Passage:** First paragraph, p. 485: "This term wrongly implies that the study has shown that there is no difference, whereas usually all that has been shown is an absence of evidence of a difference." ("This term" is "negative", for trials without a significant difference.)
- **Supports the fix:** yes.
- **Text from:** PubMed Central, <https://pmc.ncbi.nlm.nih.gov/articles/PMC2550545/>, which shows the article as a scanned image of BMJ page 485 (<https://cdn.ncbi.nlm.nih.gov/pmc/blobs/8360/2550545/a8a7e1236b59/bmj00606-0027.png>). The image was read by OCR and the quotation checked by eye against it. (The first draft used a third-party reproduction of the BMJ page on a University at Buffalo course page; it is no longer the source.)
- **Citation check:** right. Not to be confused with Bland & Altman 1995 (section 4), the same two authors in the other order.

## 18. Newcombe 1998

- **Citation:** Newcombe RG. Interval estimation for the difference between independent proportions: comparison of eleven methods. Stat Med 1998;17(8):873–890. doi:10.1002/(sici)1097-0258(19980430)17:8<873::aid-sim779>3.0.co;2-i. PMID 9595617.
- **Findings:** no finding ID in the plan. It matches the Urgency 4 point at p6:648 (E): "the Wald CI for a risk difference is paired with Fisher's test on 6 events per arm without a caveat".
- **Claim the fix needs:** the simple Wald interval for a difference of two proportions performs poorly with small counts; a score-based interval does better.
- **Status:** abstract only.
- **Passages:** Abstract: "Computationally simpler methods are prone to a variety of aberrations and poor coverage properties." and "A method combining Wilson score intervals for the two proportions to be compared also performs well, and is readily implemented irrespective of sample size."
- **Supports the fix:** partly. The abstract supports "simple methods cover poorly" and names the Wilson-based alternative, but does not name the Wald interval or say at what counts it fails. The full text was not obtained.
- **Tried:** PubMed (no PMC copy); the publisher (Wiley) is subscription-only and was not opened.
- **Text from:** PubMed abstract, <https://pubmed.ncbi.nlm.nih.gov/9595617/>.
- **Citation check:** "Newcombe 1998" is ambiguous: the same issue holds a second paper, Newcombe RG. Two-sided confidence intervals for the single proportion: comparison of seven methods. Stat Med 1998;17(8):857–872 (PMID 9595616), whose abstract says "Simple interval estimate methods for proportions exhibit poor coverage". The risk difference at p6:648 needs the 873–890 paper.

---

## For Doc

The fixes below rest on a reference that was not obtained, was read only as an abstract, or says less than (or something different from) what the finding claims. Until you decide, the plan's later tasks should leave out the part named.

| Finding | Reference | Status | What it means for the fix |
|---|---|---|---|
| B10 | Sjölander & Greenland 2013 | read, partly | "Not the wrong model" for a matched cohort is supported (the unstratified Cox model estimates the marginal hazard ratio if the matching variables are the only confounders). Not supported by this paper: that a cluster-robust standard error makes it "an accepted analysis"; the paper does not discuss robust standard errors for cohorts, and its own recommendation is "some adjustment for the matching variables". It does not address frequency or propensity-score matching (p3:440). Page 7's sentence must describe the unstratified model's hazard ratio as a population-level (marginal) effect, "in a population where the matching variables are distributed as in the matched cohort", not as the within-pair hazard ratio the stratified model gives. The robust-SE wording needs another source or your decision. |
| B17 | Hernán 2010 | read, partly | The survivors' selection bias is supported. Restricted mean survival time is not in the paper; name adjusted survival curves or a series of average hazard ratios over increasingly long follow-up (the paper's alternatives), or find a source for RMST first. |
| B11 | Feinstein & Cicchetti 1990 | abstract only, partly | The prevalence point (high agreement, low kappa with imbalanced marginal totals) is in the abstract. "Kappas can't be compared across studies with different case mixes" is not; word it as a consequence ("so a kappa from a sample with a different case mix may not be comparable") or wait for the full text. |
| B24 | Cochran 1954 | not obtained | The 20% rule is supported only by a secondary source (Bewick et al. 2004, which attributes it to Cochran through a textbook). Cite Bewick, or say "a widely used rule attributed to Cochran", not Cochran 1954 directly. |
| B24, C3 | Peduzzi 1995; Vittinghoff & McCulloch 2007 | abstract only, partly | "A rule of thumb, which some studies find too strict" is supported. "A rough upper limit" is not the abstracts' wording. Neither abstract supports counting "per coefficient": both say "per variable" or "per predictor variable". Harrell's course notes (read) count parameters, with a divisor of 15 in prediction models. Decide whether "per coefficient" rests on Harrell, or keep "per predictor" and add that a categorical predictor uses one coefficient per category beyond the first. |
| B20 | de Vet et al. 2006 | read, partly | SEM and its derived change score are supported, but the paper's term is "smallest detectable change", and it distinguishes SEM for agreement from SEM for consistency. The claim that orthopaedic papers report them "routinely" is contradicted by the paper (2006: "agreement parameters have not yet struck root"); drop it or find a recent source. |
| B3 | STROBE | read, partly | Design, eligibility and selection, follow-up, study size and missing data are STROBE items. Ethics approval, consent, an MCID and registry completeness are not; the D5 box must not attribute them to STROBE. STROBE asks authors not simply to call a study "retrospective" or "prospective"; B3's "design in words (retrospective or prospective cohort)" should become a description of how and when the data were collected. |
| B16 | Little & Rubin | not obtained | The book was not read. Sterne et al. 2009 (read) states the principle for imputation and complete-case models, not for mixed models in so many words. The planned words "and that the model includes" are a small step beyond it; decide whether Sterne is enough, or whether a source on likelihood analysis of longitudinal data under missing at random is needed. |
| C1 | Delacre et al. 2019 | read, partly | Welch's ANOVA as the safe default is supported. The paper argues against formal tests of equal variances as a first step; it does not evaluate judging the spreads from a plot. The page can say the paper recommends Welch by default, but not that the paper endorses (or rejects) the "about twice the smallest SD" rule. |
| p6:648 (Urgency 4) | Newcombe 1998 | abstract only, partly | "Simple methods cover poorly; a Wilson-based interval does better" is supported. That the Wald interval in particular fails at 6 events per arm is not in the abstract. |

Fully supported, no question for you: B13 and B20 by Bland & Altman 1986; B13 by Bland & Altman 1995 (with one wording change: the one-method grouping "can create or distort a trend", not "exaggerates" it); B8 by Greenland et al. 2016 and Altman & Bland 1995; C5 by Greenland, Robins & Pearl 1999 (with Sjölander & Greenland 2013 for the hazard ratio); B23 by CONSORT (cite CONSORT 2025, item 25, instead of 2010, item 15); C4 by Westreich & Greenland 2013.
