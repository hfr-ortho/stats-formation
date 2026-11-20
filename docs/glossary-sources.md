# Glossary sources

Where each definition on the glossary pages (`en/glossary.qmd`, `de/glossary.qmd`, `fr/glossary.qmd`) comes from, so that it can be verified or improved. One section per entry, in the order of the English glossary; the heading is the entry's id.

- **Source** is the reference the definition was written from, and **Supports** is what its passage says.
- **Checked** says whether the passage was opened and read when the entry was written ("passage read"), or whether only the citation could be confirmed.
- A definition is the source's content in plain words for beginners, not a quotation. German and French entries are translations of the English one.
- To change a definition: check the new wording against the source (or a better one), update this file, and change all three glossary pages. `tests/python/test_glossary_sources.py` fails if an entry has no section here.
- Not used as sources: Wikipedia, blogs, Q&A sites and AI-generated text.

### `aalen-johansen`

**Aalen-Johansen estimator.** A method for estimating the probability of being in each of several states (for example unrevised, revised, or dead without revision) at each time. With competing risks it gives the cumulative incidence. With a single type of event it gives the same result as the Kaplan-Meier method.

- **Source:** Therneau T, Crowson C, Atkinson E. Multi-state models and competing risks. Vignette of the R survival package (CRAN; PDF dated 09.09.2026); section 2.1 Aalen-Johansen estimate
- **URL:** <https://cran.r-project.org/web/packages/survival/vignettes/compete.pdf>
- **Supports:** The Aalen-Johansen estimate gives the probability of being in each state at time t; it reproduces the Kaplan-Meier for two states and the cumulative incidence for competing risks.
- **Also:** Therneau T. R survival package, help page survfit.formula ("For ordinary (single event) survival this reduces to the Kaplan-Meier estimate"; "for competing risks data the AJ reduces to the cumulative incidence (CI) estimator"), https://stat.ethz.ch/R-manual/R-devel/library/survival/html/survfit.formula.html. Original paper (not opened; details from reference lists found by web search, not from the publisher): Aalen OO, Johansen S. An empirical transition matrix for non-homogeneous Markov chains based on censored observations. Scand J Stat 1978;5(3):141–150.
- **Checked:** 16.11.2026, passage read
- **Notes:** The states in the example are the site's (revision and death). The original paper's volume and pages are not confirmed at the publisher (no Crossref record found); treat that citation as unverified. The vignette PDF on CRAN is rebuilt with each release, so its date changes. Primary source read in full text.

### `adjustment`

**Adjusted (for other variables).** Estimated while accounting for the effect of other variables, usually by putting them into a regression model together with the variable of interest. An implant's hazard ratio adjusted for age and sex is the effect of the implant that is left once the effects of age and sex have been taken out. An unadjusted estimate leaves the other variables out.

- **Source:** Harrell FE. Glossary of Statistical Terms. Vanderbilt University School of Medicine, Department of Biostatistics, 26.04.2025; entry "adjusting or controlling for a variable"
- **URL:** <https://hbiostat.org/glossary/>
- **Supports:** Harrell: "Assessing the effect of one variable while accounting for the effect of another (confounding) variable", by stratifying or by a regression model that subtracts out that effect; "Adjustment results in adjusted odds ratios, adjusted hazard ratios, adjusted slopes".
- **Checked:** 16.11.2026, passage read
- **Notes:** Only the sense 'adjusted for other variables'. Not for p-value adjustment (multiple comparisons), adjusted R-squared, or effectsize's 'Cramer's V (adj.)' bias correction, as the scope note says. Harrell also names stratification as a way to adjust; the definition says 'usually' a regression model because that is what the site's pages do.

### `agreement`

**Agreement.** How close repeated measurements of the same patient are to each other, for example by how many degrees two raters' readings of the same knee differ. It is not the same as correlation: two raters' readings can be perfectly correlated while one always reads higher. For continuous measurements it is shown with Bland-Altman limits of agreement.

- **Source:** de Vet HCW, Terwee CB, Knol DL, Bouter LM. When to use agreement versus reliability measures. J Clin Epidemiol 2006;59(10):1033–1039; abstract
- **URL:** <https://doi.org/10.1016/j.jclinepi.2005.10.015>
- **Supports:** "Agreement parameters assess how close the results of the repeated measurements are, by estimating the measurement error in repeated measurements."
- **Also:** Bland JM, Altman DG. Statistical methods for assessing agreement between two methods of clinical measurement. Lancet 1986;i:307–310 (author's full-text copy) ("r measures the strength of a relation between two variables, not the agreement between them"; perfect correlation needs only that the points lie along any straight line), https://www-users.york.ac.uk/~mb55/meas/ba.htm; Koo TK, Li MY. A Guideline of Selecting and Reporting Intraclass Correlation Coefficients for Reliability Research. J Chiropr Med 2016;15(2):155–163 ("paired t test and Bland-Altman plot are methods for analyzing agreement"), https://pmc.ncbi.nlm.nih.gov/articles/PMC4913118/
- **Checked:** 16.11.2026, passage read
- **Notes:** Of de Vet et al. only the abstract was read. Defined for agreement between raters or methods on a continuous measurement (page 17's sense). Page 17 also speaks of 'agreement on CPAK class', measured with kappa; the kappa entry covers that. The internal check_agree() helper is unrelated.

### `anova`

**ANOVA (analysis of variance).** A test that compares the means of three or more groups at once. It compares the variation between the group means with the variation among patients within the groups; their ratio is the F statistic. One-way ANOVA has a single grouping variable, such as implant type, and a small p-value says that at least one group mean differs, not which one.

- **Source:** GraphPad Software. GraphPad Prism 11 Statistics Guide; page 'Interpreting results: One-way ANOVA'
- **URL:** <https://www.graphpad.com/guides/prism/latest/statistics/f_ratio_and_anova_table_(one-way_anova).htm>
- **Supports:** ANOVA compares the means of three or more groups by comparing the variation within groups with the variation among group means; a tiny P value indicates only that at least one mean probably differs.
- **Also:** Bewick V, Cheek L, Ball J. Statistics review 9: One-way analysis of variance. Crit Care 2004;8(2):130-136. doi:10.1186/cc2836; sections 'Introduction' and 'One-way analysis of variance' (F = between-treatments mean square divided by error mean square), https://pmc.ncbi.nlm.nih.gov/articles/PMC420045/
- **Checked:** 16.11.2026, passage read
- **Notes:** Repeated-measures ANOVA has its own entry. Welch's ANOVA is covered in the Welch entry.

### `association`

**Association.** Two variables are associated when they show some relationship with each other, for example when patients with a higher BMI tend to have longer operations. In a positive association the two tend to rise together; in a negative one, one tends to fall as the other rises. An association does not by itself show that one causes the other.

- **Source:** Çetinkaya-Rundel M, Hardin J. Introduction to Modern Statistics, 2nd edition. OpenIntro, 2024; section 1.2.3, "Relationships between variables", and section 1.2.5
- **URL:** <https://openintro-ims.netlify.app/data-hello>
- **Supports:** OpenIntro: "When two variables show some connection with one another, they are called associated variables"; a downward trend is a negative association, an upward one positive; "association does not imply causation".
- **Also:** CDC. Principles of Epidemiology in Public Health Practice, 3rd edition; Glossary, "association" ("the statistical relation between two or more events, characteristics, or other variables"). https://archive.cdc.gov/www_cdc_gov/csels/dsepd/ss1978/glossary.html
- **Checked:** 16.11.2026, passage read
- **Notes:** The BMI example is an illustration written for this site, not from the source (OpenIntro's examples are US county data). The book's welcome page gives 'Copyright 2024. Second Edition. Version date: March 31, 2026'. The CDC textbook is not on the brief's list but is an official standard reference with free access. Altman and Krzywinski's 'Association, correlation and causation' (Nat Methods 2015;12:899) is paywalled and was not read.

### `assumption`

**Assumption.** A condition that a test or model takes for granted about the data, for example that patients are independent of each other, that the values follow a normal distribution or that groups have equal variances. The p-value and confidence interval can be trusted only as far as the assumptions hold, so they need to be checked.

- **Source:** NIST/SEMATECH e-Handbook of Statistical Methods. National Institute of Standards and Technology; section 4.2.1, "What are the typical underlying assumptions in process modeling?"; accessed 16.11.2026
- **URL:** <https://www.itl.nist.gov/div898/handbook/pmd/section2/pmd21.htm>
- **Supports:** NIST: "Successful use of these methods in any particular application hinges on the validity of the underlying assumptions"; the list includes constant standard deviation and normally distributed random errors, and the Handbook gives methods for checking them.
- **Also:** NIST/SEMATECH e-Handbook of Statistical Methods. National Institute of Standards and Technology; section 1.2.2, "Importance"; accessed 16.11.2026 (if the assumptions are not valid, the conclusions are not valid). https://www.itl.nist.gov/div898/handbook/eda/section2/eda22.htm Also Motulsky HJ. "The need for independent samples". GraphPad Statistics Guide (Prism 11). GraphPad Software; accessed 16.11.2026 ("Statistical tests are based on the assumption that each subject ... was sampled independently of the rest"). https://www.graphpad.com/guides/prism/latest/statistics/the_need_for_independent_samples.htm
- **Checked:** 16.11.2026, passage read
- **Notes:** NIST writes about measurement processes and models in general; the three examples in the definition are the assumptions the site's pages name, each confirmed in a source read this session (independence: GraphPad; normal distribution: GraphPad 'Key concepts: Nonparametric tests'; equal variances: NIST 1.3.5.10).

### `at-risk`

**At risk.** Still being followed, and not yet having had the event, at a given moment.

- **Source:** GraphPad Software. GraphPad Prism 11 Statistics Guide (the guide the brief lists as Motulsky's); page "The mathematics of Kaplan-Meier survival analysis"
- **URL:** <https://www.graphpad.com/guides/prism/latest/statistics/stat_kaplan-meier_mathematics.htm>
- **Supports:** Patients who had the event or were censored at one time "are no longer included in the number at risk for any subsequent time points".
- **Also:** Goel MK, Khanna P, Kishore J. Understanding survival analysis: Kaplan-Meier estimate. Int J Ayurveda Res 2010;1(4):274 to 278; section on the Kaplan-Meier estimate ("Subjects who have died, dropped out, or move out are not counted as 'at risk'"). https://doi.org/10.4103/0974-7788.76794 . Also Harrell FE. Glossary of Statistical Terms. Vanderbilt University School of Medicine, Department of Biostatistics, version of 26.04.2025, entry "risk set" ("The set of patients in the study at a specified time"). https://hbiostat.org/glossary/
- **Checked:** 16.11.2026, passage read
- **Notes:** Fully supported. Detail the definition leaves out and the pages state ("still being followed just before it"): GraphPad counts a patient who has the event, or is censored, at time t as still at risk at time t, and drops them only from later times.

### `baseline`

**Baseline.** The starting point of a study: when the patient enters it, before the treatment being studied. Baseline characteristics are what was recorded then, such as age, sex and the score before surgery. A later measurement minus the baseline measurement is the change from baseline.

- **Source:** Cochrane Community. Glossary. Cochrane; archived copy of community.cochrane.org/glossary (Internet Archive snapshot of 01.07.2019); entry "Baseline characteristics"
- **URL:** <https://web.archive.org/web/20190701142620/https://community.cochrane.org/glossary>
- **Supports:** "Values of demographic, clinical and other variables collected for each participant at the beginning of a trial, before the intervention is administered."
- **Also:** Higgins JPT, Li T, Deeks JJ (editors). Chapter 6: Choosing effect measures and computing estimates of effect. In: Cochrane Handbook for Systematic Reviews of Interventions, version 6.5. Cochrane, 2024; section 6.5.1 (measured "at baseline, that is, before interventions are administered"; change from baseline is the difference between the two measurements). https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-06
- **Checked:** 16.11.2026, passage read
- **Notes:** Cochrane has retired its glossary page (community.cochrane.org/glossary now redirects to resources.cochrane.org, which points readers to archive.org), so the entry was read in the Internet Archive snapshot of 01.07.2019. Defines the before-treatment sense only. Not for "baseline hazard" or "baseline risk" (pages 7 and 14) or a knee's "own baseline level" (page 16, the random intercept), which mean a reference level, not a time point.

### `benjamini-hochberg`

**Benjamini-Hochberg adjustment.** A way of adjusting p-values that controls the false discovery rate instead of the family-wise error rate. That is a less strict standard, so it usually misses fewer real differences than Holm's or Bonferroni's adjustment. Often shortened to BH.

- **Source:** R Core Team. p.adjust {stats}: Adjust P-values for Multiple Comparisons. R documentation (stats version 4.6.0), Details
- **URL:** <https://stat.ethz.ch/R-manual/R-devel/library/stats/html/p.adjust.html>
- **Supports:** The BH method controls the false discovery rate, "a less stringent condition than the family-wise error rate, so it is typically more powerful than the others".
- **Also:** Benjamini Y, Hochberg Y. Controlling the False Discovery Rate: A Practical and Powerful Approach to Multiple Testing. J R Stat Soc B 1995;57(1):289–300; summary (a simple sequential Bonferroni-type procedure controls the false discovery rate, with a substantial gain in power), https://academic.oup.com/jrsssb/article/57/1/289/7035855
- **Checked:** 16.11.2026, passage read
- **Notes:** Of the original paper only the summary was read. Page 15's rule (p times number of tests divided by its rank) matches the body of R's p.adjust() (pmin(1, cummin(n/i * p[o]))). Page 15's advice that BH 'suits screening many outcomes for leads, not confirming a claim' is not stated in the sources I opened and is left to the page.

### `bias`

**Bias.** A systematic error: something in the design, conduct or analysis of a study that pushes an estimate away from the true value in one direction. Unlike the play of chance, it would still be there on average if the study were repeated many times. In a Bland-Altman analysis, the bias is the mean difference between the two methods or raters.

- **Source:** Harrell FE. Glossary of Statistical Terms. Vanderbilt University School of Medicine, Department of Biostatistics, 26.04.2025; entry "bias"
- **URL:** <https://hbiostat.org/glossary/>
- **Supports:** Harrell: "A systematic error ... Bias typically pertains to the discrepancy between the average of many estimates over repeated sampling and the true value of a parameter."
- **Also:** ICH Harmonised Tripartite Guideline E9: Statistical Principles for Clinical Trials. ICH, 05.02.1998; Glossary, "Bias (Statistical & Operational)" (the systematic tendency of factors in the design, conduct, analysis and evaluation of a trial to make the estimate deviate from its true value). https://database.ich.org/sites/default/files/E9_Guideline.pdf For the Bland-Altman sense: Bland JM, Altman DG. Statistical methods for assessing agreement between two methods of clinical measurement. Lancet 1986;i: pages 307 to 310 ("the bias, estimated by the mean difference"), author copy at https://www-users.york.ac.uk/~mb55/meas/ba.htm
- **Checked:** 16.11.2026, passage read
- **Notes:** Covers both senses in the scope note: systematic error ('bias', 'biased', 'unbiased') and the Bland-Altman bias on page 17. ICH E9 speaks of a treatment effect; the definition says 'an estimate'. The site's 'small-sample bias correction' (Cramer's V, page 10) is the same statistical sense: an estimate that is off on average.

### `binary`

**Binary (yes/no) outcome.** An outcome with only two possible values, such as revised or not revised. It is summarized as a proportion: the share of patients in whom the answer is yes.

- **Source:** Higgins JPT, Li T, Deeks JJ (eds). Chapter 6: Choosing effect measures and computing estimates of effect. In: Cochrane Handbook for Systematic Reviews of Interventions, version 6.5. Cochrane, 2024; sections 6.1.1 and 6.4.1
- **URL:** <https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-06>
- **Supports:** "Dichotomous (binary) outcome data arise when the outcome for every participant is one of two possibilities, for example, dead or alive".
- **Also:** Harrell FE. Biostatistics for Biomedical Research. hbiostat.org; section 4.1, Distributions (a binary variable is characterized by the proportion of "yes" in a sample). https://hbiostat.org/bbr/descript ; also Bland & Altman 2000 (see odds), which writes binary ("yes or no") variables.
- **Checked:** 16.11.2026, passage read
- **Notes:** Sources also call this "dichotomous"; the site's English pages do not use that word, so I left it out.

### `binomial-test`

**Binomial test.** An exact test that compares one group's proportion of a yes/no outcome with a hypothetical proportion. It uses the binomial distribution, which gives the probability of each possible number of patients with the outcome (0, 1, 2 and so on) out of a fixed number of patients, when each patient has the same chance of it.

- **Source:** GraphPad Software. GraphPad Prism 11 Statistics Guide; page 'The binomial test'
- **URL:** <https://www.graphpad.com/guides/prism/latest/statistics/stat_binomial.htm>
- **Supports:** The binomial test is an exact test that compares the observed with the expected distribution when there are only two categories; the chi-square test is only an approximation there.
- **Also:** Binomial distribution: NIST/SEMATECH e-Handbook of Statistical Methods, section 1.3.6.6.18 'Binomial Distribution' (used with exactly two mutually exclusive outcomes, to obtain the probability of x successes in N trials with a fixed probability of success), https://www.itl.nist.gov/div898/handbook/eda/section3/eda366i.htm ; R Core Team. R documentation, stats::binom.test ('an exact test of a simple null hypothesis about the probability of success in a Bernoulli experiment'), https://stat.ethz.ch/R-manual/R-devel/library/stats/html/binom.test.html
- **Checked:** 16.11.2026, passage read
- **Notes:** The entry also has to cover 'binomial distribution' (pages 4 and 5), so the second sentence defines it. GraphPad describes three ways to build the two-sided p-value; the site's page 5 uses the one GraphPad calls the method of small P values.

### `bland-altman`

**Bland-Altman limits of agreement.** A way of showing how far apart two measurements of the same thing can be, such as readings by two raters or two methods. The differences between the paired measurements are plotted against their means: the mean difference is the bias, and about 95% of the differences fall within the limits of agreement (the bias plus and minus 1.96 standard deviations of the differences). Whether the limits are narrow enough is a clinical judgment, not a statistical one.

- **Source:** Bland JM, Altman DG. Statistical methods for assessing agreement between two methods of clinical measurement. Lancet 1986;i:307–310 (author's full-text copy)
- **URL:** <https://www-users.york.ac.uk/~mb55/meas/ba.htm>
- **Supports:** Plot the difference between the methods against their mean; the bias is the mean difference d, and if the differences are Normally distributed 95% of them lie between d - 1.96s and d + 1.96s, the "limits of agreement".
- **Also:** Giavarina D. Understanding Bland Altman analysis. Biochem Med (Zagreb) 2015;25(2):141–151 (the plot "does not say whether those limits are acceptable or not. Acceptable limits must be defined a priori, based on clinical necessity"), https://pmc.ncbi.nlm.nih.gov/articles/PMC4470095/
- **Checked:** 16.11.2026, passage read
- **Notes:** Read on Martin Bland's own website, which hosts the Lancet text. Agrees with page 17. The '95%' holds if the differences are roughly normally distributed (Bland & Altman say so); the definition says 'about 95%'. 'Bias' here means the mean difference between the two raters, a narrower sense than the glossary's general 'bias' entry (batch S2).

### `bonferroni`

**Bonferroni correction.** The simplest adjustment for multiple comparisons: every p-value is multiplied by the number of tests, which is the same as dividing the 0.05 threshold by that number. It controls the family-wise error rate, but it is strict, so real differences are missed more easily. Holm's adjustment gives the same protection and is never stricter.

- **Source:** R Core Team. p.adjust {stats}: Adjust P-values for Multiple Comparisons. R documentation (stats version 4.6.0), Details
- **URL:** <https://stat.ethz.ch/R-manual/R-devel/library/stats/html/p.adjust.html>
- **Supports:** "the Bonferroni correction ... in which the p-values are multiplied by the number of comparisons"; it gives strong control of the family-wise error rate and "is dominated by Holm's method".
- **Also:** Perneger TV. What's wrong with Bonferroni adjustments. BMJ 1998;316(7139):1236–1238 (the adjusted level is approximated by alpha/n; type II errors increase, "so that truly important differences are deemed non-significant"), https://pmc.ncbi.nlm.nih.gov/articles/PMC1112991/. Standard reference, not opened: Bland JM, Altman DG. Multiple significance tests: the Bonferroni method. BMJ 1995;310(6973):170, https://doi.org/10.1136/bmj.310.6973.170
- **Checked:** 16.11.2026, passage read
- **Notes:** Bland & Altman's Statistics Note (the obvious reference) is a scanned page on PubMed Central and bmj.com returned 403, so it was not read. Page 15 calls Bonferroni 'the strictest' of the three adjustments it shows; the definition says only 'strict', because R's documentation notes that another method (BY) can be stricter still.

### `bootstrap`

**Bootstrap.** A way to get a confidence interval without a formula. The computer draws many new samples of the same size from the data themselves, so that some patients appear more than once and others not at all, and recalculates the estimate on each. The spread of those estimates gives the interval; the percentile method and BCa are two ways of reading it off.

- **Source:** Harrell FE. Glossary of Statistical Terms. Vanderbilt University School of Medicine, Department of Biostatistics, 26.04.2025; entry "bootstrap"
- **URL:** <https://hbiostat.org/glossary/>
- **Supports:** Harrell: random samples with replacement from the original dataset, each with the same number of observations; some subjects are omitted and some sampled more than once; used to compute standard deviations and confidence limits without assuming a model.
- **Also:** SciPy v1.18.0 Manual, scipy.stats.bootstrap (resample with replacement, compute the statistic for each resample, read the interval from the bootstrap distribution; 'percentile', 'basic' and 'BCa', bias-corrected and accelerated, differ in that last step). https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html Also NIST/SEMATECH e-Handbook of Statistical Methods. National Institute of Standards and Technology; section 1.3.3.4, "Bootstrap Plot"; accessed 16.11.2026 (sorted bootstrap values give the confidence limits). https://www.itl.nist.gov/div898/handbook/eda/section3/bootplot.htm
- **Checked:** 16.11.2026, passage read
- **Notes:** Covers 'bootstrap', 'bootstrapped', 'resampling', 'BCa' and 'percentile method'. BCa stands for bias-corrected and accelerated (SciPy); the sources call the drawing 'with replacement', and the bootstrap also gives standard errors (Harrell). Not verified here: page 6's description of how BCa works (it 'looks at how much the estimate changes when each patient is left out in turn'); the SciPy page only names the method. That detail is in Efron (1987) and the SciPy source code, neither opened. Bland and Altman's BMJ note 'Bootstrap resampling methods' (2015;350:h2622) returned 403.

### `bounded-scale`

**Bounded scale.** A scale whose values cannot go below a lowest or above a highest possible value, such as a score from 0 to 100. Values on such a scale often pile up at one end or at both, so the distribution is often skewed and rank-based (nonparametric) methods are commonly used.

- **Source:** Lesaffre E, Rizopoulos D, Tsonaka S. The logistic-transform for bounded outcome scores. IAP Statistics Network Technical Report 0448, 2004 (published in Biostatistics, 2007;8(1):72 to 85); Introduction
- **URL:** <https://sites.uclouvain.be/IAP-Stat-Phase-V-VI/PhaseV/publications_2004/TR/TR0448.pdf>
- **Supports:** "Bounded outcome scores are measurements that are restricted to a finite interval"; their distributions range from unimodal to J- and U-shaped, which "often necessitates the use of non-parametric methods".
- **Also:** Deeks JJ, Higgins JPT, Altman DG, McKenzie JE, Veroniki AA, Simmonds M (editors). Chapter 10: Analysing data and undertaking meta-analyses (last updated November 2026). In: Cochrane Handbook for Systematic Reviews of Interventions Version 6.5.1. Cochrane, 2026; section 10.5.3 (a check for skew that applies to "scale outcomes with minimum or maximum scores"). https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-10
- **Checked:** 16.11.2026, passage read
- **Notes:** Read as the freely available technical report (pages 1 and 2); the journal version at academic.oup.com was not opened, so its volume and pages come from a search result, not from the article. "Pile up at one end or at both" is my plain wording of "J- and U-shaped". The source says "bounded outcome score"; the site says "bounded" and "a bounded score". Altman and Bland's Statistics Note on detecting skewness (BMJ 1996;313:1200), which Cochrane cites for the check, could not be opened.

### `boxplot`

**Boxplot.** A plot that sums up a variable's values, usually with one box per group. The box runs from the first to the third quartile, so it holds the middle half of the values, and a line inside it marks the median. Lines called whiskers reach to the lowest and highest values within 1.5 times the IQR of the box; values beyond them are drawn as separate points.

- **Source:** NIST/SEMATECH e-Handbook of Statistical Methods. National Institute of Standards and Technology, 2012; section 1.3.3.7, Box Plot
- **URL:** <https://www.itl.nist.gov/div898/handbook/eda/section3/boxplot.htm>
- **Supports:** A box is drawn between the lower and upper quartiles (the middle 50% of the data) with a line at the median and lines out to the extremes; a variant draws far points individually.
- **Also:** ggplot2 reference, geom_boxplot (whiskers extend to the most extreme value no further than 1.5 * IQR from the hinge; data beyond are plotted individually). https://ggplot2.tidyverse.org/reference/geom_boxplot.html ; matplotlib documentation, pyplot.boxplot (same rule). https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.boxplot.html ; Çetinkaya-Rundel M, Hardin J. Introduction to Modern Statistics, 2nd ed. OpenIntro, 2024, section 5.5. https://openintro-ims.netlify.app/explore-numerical
- **Checked:** 16.11.2026, passage read
- **Notes:** The whisker rule is the documented default of the two functions the site's pages call (geom_boxplot and ax.boxplot), both opened and read; NIST describes it as the "box plots with fences" variant and its basic box plot runs the lines to the minimum and maximum. Label follows master.tsv; NIST and IMS write "box plot".

### `categorical-variable`

**Categorical variable.** A variable whose values are categories, not measured numbers, such as sex, graft type or ASA class. The possible categories are called its levels. When the levels have a natural order, the variable is ordinal.

- **Source:** Çetinkaya-Rundel M, Hardin J. Introduction to Modern Statistics, 2nd ed. OpenIntro, 2024; section 1.2.2, Types of variables
- **URL:** <https://openintro-ims.netlify.app/data-hello>
- **Supports:** "Because the responses themselves are categories, state is called a categorical variable, and the possible values (states) are called the variable's levels"; with a natural ordering it is ordinal.
- **Also:** Harrell FE. Glossary of Statistical Terms. Vanderbilt University School of Medicine, Department of Biostatistics, 2025 (hbiostat.org); entry "categorical variable". https://hbiostat.org/glossary/
- **Checked:** 16.11.2026, passage read
- **Notes:** Usage differs between sources: Harrell's glossary reserves "categorical" for categories with no logical order and lists ordinal separately, while IMS (and the site, which calls a yes/no outcome and ASA class categorical) uses it for both. The definition follows IMS and the site. I left out the word "nominal" (unordered) because the site does not use it.

### `ceiling-effect`

**Ceiling (or floor) effect.** Many patients score the best (or worst) value a scale allows, so the scale cannot show how much better (or worse) they really are.

- **Source:** Hamilton DF, Giesinger JM, MacDonald DJ, Simpson AHRW, Howie CR, Giesinger K. Responsiveness and ceiling effects of the Forgotten Joint Score-12 following total hip arthroplasty. Bone Joint Res 2016;5(3):87 to 91; Introduction and Discussion
- **URL:** <https://doi.org/10.1302/2046-3758.53.2000480>
- **Supports:** "A ceiling effect means that several patients score the highest possible score"; if the patient continues to improve, "the test does not capture that improvement".
- **Also:** Wamper KE, Sierevelt IN, Poolman RW, Bhandari M, Haverkamp D. The Harris hip score: Do ceiling effects limit its usefulness in orthopedics? A systematic review. Acta Orthop 2010;81(6):703 to 707; Introduction ("A floor effect occurs when several of the patients score the lowest possible score, whereas a ceiling effect occurs when several of the patients score the highest possible score"). https://doi.org/10.3109/17453674.2010.537808 (PDF read at https://actaorthop.org/actao/article/download/11132/14895)
- **Checked:** 16.11.2026, passage read
- **Notes:** Fully supported. Both papers say "several" patients where the glossary says "many", and both add a cut-off the glossary rightly leaves out (more than 15% of patients at the best or worst score, citing Terwee et al. 2007, which I could not open). The papers spell out the consequence only for the ceiling (further improvement is not captured); the floor half of "how much worse they really are" follows by symmetry and is not stated in either paper.

### `censored`

**Censored.** Followed for a while without having the event, then no longer observed: the study ended, the patient moved away, or the patient died without the event, when death is not the event studied (see the entry Competing risk). All we know is that the event had not happened by then. The usual methods assume that censored patients have the same chance of a later event as those still being followed.

- **Source:** Clark TG, Bradburn MJ, Love SB, Altman DG. Survival analysis part I: basic concepts and first analyses. Br J Cancer 2003;89(2):232 to 238; section "Censoring makes survival analysis different"
- **URL:** <https://doi.org/10.1038/sj.bjc.6601118>
- **Supports:** Censoring arises when a patient has not had the event by the close of the study, is lost to follow-up, or has a different event that makes further follow-up impossible. The assumption, section "Summary": "It is assumed that those patients who are censored have the same survival prospects as those who continue to be followed, that is, the censoring is uninformative"; section "Uninformative censoring": those censored "should be as likely to have a subsequent event as those individuals who remain in the study".
- **Also:** GraphPad Software. GraphPad Prism 11 Statistics Guide (the guide the brief lists as Motulsky's); page "Censored Data" (a participant who dropped out or reached the end of the study without the event is censored; "it must occur after the last time that each of them was last observed"). https://www.graphpad.com/guides/prism/latest/statistics/stat_censored_data.htm
- **Checked:** 16.11.2026, passage read; 20.11.2026, the sections "Censoring makes survival analysis different", "Uninformative censoring" and "Summary" re-read in full text (Europe PMC, PMC2394262)
- **Notes:** Fully supported for the way the site uses it (event = revision or graft failure). "The patient died" is Clark's third case, a different event that ends follow-up; the paper's ovarian example censors deaths from other causes. It holds only when death is not the event being studied, and censoring deaths has the competing-risk cost that pages 4 and 13 already explain. Reworded on 20.11.2026 (content review C10): the definition listed "the patient died" as an ordinary reason, while the competing-risk entry says censoring deaths makes 1 minus Kaplan-Meier overstate the event; it now says "died without the event, when death is not the event studied" and names the competing-risk entry in words (entries do not link to each other). The last sentence, the assumption, is Clark's own summary.

### `central-limit-theorem`

**Central limit theorem.** A mathematical result: when samples are large enough, the means of repeated samples follow a normal distribution even if the individual values do not. This is why tests on means, such as the t test and ANOVA, still work for values that are not normally distributed, provided the sample is large enough.

- **Source:** Motulsky HJ. "The Central Limit Theorem of statistics". GraphPad Statistics Guide (Prism 11). GraphPad Software; accessed 16.11.2026
- **URL:** <https://www.graphpad.com/guides/prism/latest/statistics/the_central_limit_theorem_of_statistics.htm>
- **Supports:** Motulsky: "if your samples are large enough, the distribution of means will follow a Gaussian distribution even if the population is not Gaussian", which lets tests such as the t test and ANOVA work well.
- **Also:** Penn State Department of Statistics. STAT 200: Elementary Statistics (online course notes), Lesson 7; section 7.4, "Central Limit Theorem"; accessed 16.11.2026 (Definition 7.2: with a sufficiently large sample the sampling distribution is approximately normal for means, proportions, differences, slopes and correlations). https://online.stat.psu.edu/stat200/Lesson07.html
- **Checked:** 16.11.2026, passage read
- **Notes:** SITE VS SOURCE (rule of thumb only): page 3 says averages of 'about 30 or more values' are close to normal; Motulsky says 'a sample size of 10 or so is generally enough' unless the population has a really unusual distribution, and that the number depends on how far the population is from normal; Penn State only says 'sufficiently large'. The definition gives no number.

### `change-score`

**Change score.** A patient's score after treatment minus the same patient's score before it (at baseline), so each patient contributes one number: how much they changed. Say which score is subtracted from which, because that sets the sign.

- **Source:** Higgins JP, Li T, Deeks JJ (editors). Chapter 6: Choosing effect measures and computing estimates of effect [last updated August 2023]. In: Cochrane Handbook for Systematic Reviews of Interventions version 6.5. Cochrane, 2024; section 6.5.1
- **URL:** <https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-06>
- **Supports:** With "change from baseline (also called a change score)", "a single measurement is created for each participant" by subtracting the baseline from the post-intervention measurement or the other way round.
- **Also:** Vickers AJ, Altman DG. Analysing controlled trials with baseline and follow up measurements. BMJ, 2001;323(7321):1123 to 1124 ("a change score can be calculated by subtracting the follow up score from the baseline score"). https://doi.org/10.1136/bmj.323.7321.1123
- **Checked:** 16.11.2026, passage read
- **Notes:** Cochrane read as page text; Vickers and Altman read through the PubMed Central page (PMC1121605) with a fetch tool that returns short quotes. The two sources subtract in opposite directions, hence the second sentence; the site computes 1-year score minus pre-op score (page 18). For information, not a conflict: Vickers and Altman, and Cochrane section 10.5.2, prefer adjusting for the baseline score in a regression (ANCOVA) over comparing change scores between the arms of a randomized trial; page 18 compares change scores between two procedures in an observational example.

### `chi-square-statistic`

**Chi-square (χ²) statistic.** A test statistic that adds up how far the observed counts are from the expected counts: each difference is squared and divided by the expected count. The larger it is, the further the data are from the null hypothesis. The chi-square distribution, whose shape depends on the degrees of freedom, turns it into a p-value, and some other tests, such as Kruskal-Wallis, use that distribution too.

- **Source:** Motulsky HJ. "How the chi-square goodness of fit test works". GraphPad Statistics Guide (Prism 11). GraphPad Software; accessed 16.11.2026
- **URL:** <https://www.graphpad.com/guides/prism/latest/statistics/stat_the_chi-square_goodness_of_fit.htm>
- **Supports:** Motulsky: for each category take the difference between observed and expected counts, square it, divide by the expected count and add them up, the sum of (O-E)2/E; the P value is the probability of so large a discrepancy or larger.
- **Also:** NIST/SEMATECH e-Handbook of Statistical Methods. National Institute of Standards and Technology; section 1.3.6.6.6, "Chi-Square Distribution"; accessed 16.11.2026 (one shape parameter, the degrees of freedom; typically used to develop hypothesis tests and confidence intervals). https://www.itl.nist.gov/div898/handbook/eda/section3/eda3666.htm Kruskal-Wallis: Motulsky HJ. "Interpreting results: Kruskal-Wallis test". GraphPad Statistics Guide (Prism 11). GraphPad Software; accessed 16.11.2026 (the statistic H approximates a chi-square distribution). https://www.graphpad.com/guides/prism/latest/statistics/how_the_kruskal-wallis_test_works.htm
- **Checked:** 16.11.2026, passage read
- **Notes:** Defines the statistic and its distribution, not the chi-square test of a table (own entry, chi-square-test). The site also meets chi-square statistics in the log-rank, likelihood ratio and Wald tests; only Kruskal-Wallis was confirmed in a source this session, so only it is named.

### `chi-square-test`

**Chi-square test.** A test for counts in categories that compares the counts observed with the expected counts. For a contingency table, these are the counts expected if the two variables had nothing to do with each other; in the goodness-of-fit version, they are the counts that hypothetical proportions predict for one group. Its p-value is an approximation that needs reasonably large expected counts.

- **Source:** Bewick V, Cheek L, Ball J. Statistics review 8: Qualitative data - tests of association. Crit Care 2004;8(1):46-53. doi:10.1186/cc2428; section 'chi-squared test of association'
- **URL:** <https://pmc.ncbi.nlm.nih.gov/articles/PMC420070/>
- **Supports:** The test compares observed frequencies with those expected under no association; large differences suggest an association, and the chi-square distribution is an approximation that depends on reasonably large expected frequencies.
- **Also:** Goodness of fit: GraphPad Software. GraphPad Prism 11 Statistics Guide; page 'How the chi-square goodness of fit test works' (null hypothesis: the observed data are sampled from a population with the expected frequencies), https://www.graphpad.com/guides/prism/latest/statistics/stat_the_chi-square_goodness_of_fit.htm ; SciPy documentation, scipy.stats.chi2_contingency (guideline of at least 5 in each cell), https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chi2_contingency.html
- **Checked:** 16.11.2026, passage read
- **Notes:** Covers both senses on the site: the test on a contingency table (pages 6 and 8) and the goodness-of-fit test (page 5). The 'at least 5' rule is left to the pages.

### `clopper-pearson`

**Clopper-Pearson interval.** A confidence interval for a proportion, also called the exact interval, calculated from the exact probabilities of each possible count (the binomial distribution) instead of from an approximation. It is guaranteed to capture the true proportion at least as often as stated, which makes it conservative: usually a little wider than it needs to be.

- **Source:** R Core Team. R documentation, stats::binom.test (R 4.6); Details
- **URL:** <https://stat.ethz.ch/R-manual/R-devel/library/stats/html/binom.test.html>
- **Supports:** "This guarantees that the confidence level is at least conf.level, but in general does not give the shortest-length confidence intervals."
- **Also:** SciPy documentation, BinomTestResult.proportion_ci (method "exact": "Use the Clopper-Pearson exact method"): https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats._result_classes.BinomTestResult.proportion_ci.html . NIST/SEMATECH e-Handbook, section 7.2.4.1 ("An exact method based on the binomial distribution"): https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm . Original, not opened (as cited by R and SciPy): Clopper CJ, Pearson ES. The use of confidence or fiducial limits illustrated in the case of the binomial. Biometrika 1934;26(4):404–413.
- **Checked:** 16.11.2026, passage read
- **Notes:** "Conservative" is my word for R's "at least conf.level ... does not give the shortest-length confidence intervals"; the site uses the same word (page 4) and "conservative" is a planned glossary entry.

### `clustered-data`

**Clustered data.** Data in which observations come in groups (clusters) whose members are more alike than members of different groups: patients of one hospital, repeated scores of one patient, or the two knees of one patient. An analysis that ignores the clustering makes the results look more precise than they are. Clusters inside larger clusters, such as knees within patients, are called nested.

- **Source:** Higgins JPT, Li T, Deeks JJ (editors). Chapter 6: Choosing effect measures and computing estimates of effect [last updated August 2023]. Cochrane Handbook for Systematic Reviews of Interventions version 6.5. Cochrane, 2024; sections 6.2.1, 6.2.7 and MECIR Box 6.2.a
- **URL:** <https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-06>
- **Supports:** With measurements on multiple body parts the "participants are the 'clusters'"; failing to account for clustering is likely to overestimate precision, giving "confidence intervals that are too narrow".
- **Also:** Schober P, Vetter TR. Repeated Measures Designs and Analysis of Longitudinal Data: If at First You Do Not Succeed—Try, Try Again. Anesth Analg 2018;127(2):569–575 (observations from the same family or hospital "are likely more similar to each other than to observations of subjects from another cluster"), https://pmc.ncbi.nlm.nih.gov/articles/PMC6072386/; Bates D, Mächler M, Bolker B, Walker S. Fitting Linear Mixed-Effects Models Using lme4. J Stat Softw 2015;67(1) (read as the lme4 package vignette), https://cran.r-project.org/web/packages/lme4/vignettes/lmer.pdf, section 2.2 and Table 2 (nested grouping factors, g2 within g1)
- **Checked:** 16.11.2026, passage read
- **Notes:** The Cochrane example of body parts is eyes; 'two knees of one patient' is the site's own (pages 3, 14, 16) application of the same point. 'Nested' is supported by the lme4 paper's wording for (1 | g1/g2), the formula page 16 uses.

### `cochran-q-test`

**Cochran's Q test.** A test for a yes/no outcome measured three or more times in the same patients, or once in each member of a matched set. It asks whether the proportion answering yes is the same at every visit, and extends McNemar's test to more than two measurements.

- **Source:** statsmodels developers. statsmodels documentation, statsmodels.stats.contingency_tables.cochrans_q; Notes
- **URL:** <https://www.statsmodels.org/stable/generated/statsmodels.stats.contingency_tables.cochrans_q.html>
- **Supports:** Cochran's Q is a k-sample extension of the McNemar test, equivalent to it with two groups; it tests that the probability of success is the same for every group.
- **Also:** Pingouin documentation, pingouin.cochran ('a non-parametric test for ANOVA with repeated measures where the dependent variable is binary'), https://pingouin-stats.org/generated/pingouin.cochran.html ; original paper as cited there, not opened: Cochran WG. The comparison of percentages in matched samples. Biometrika 1950;37:256-266. doi:10.1093/biomet/37.3-4.256
- **Checked:** 16.11.2026, passage read
- **Notes:** Sourced from official software documentation (list 3) because no list 1 source that could be opened covers this test; BMJ's Statistics at Square One returned HTTP 403. The site's statement that patients with the same answer at every visit drop out of the calculation is not stated in these two pages and is not part of the definition.

### `coefficient`

**Coefficient.** The number a regression model estimates for a predictor: how much the outcome changes, on average, when that predictor goes up by one unit and the other predictors stay the same. For a categorical predictor it is the difference from the reference group. In logistic and Cox regression the coefficient is on a logarithm scale, and software converts it into an odds ratio or a hazard ratio.

- **Source:** Penn State Eberly College of Science. STAT 501: Regression Methods (online course notes); Lesson 5, section 5.3 (The multiple linear regression model), and Lesson 13, section 13.2, 'Odds, log odds, and odds ratio'
- **URL:** <https://online.stat.psu.edu/stat501/Lesson05.html>
- **Supports:** Each coefficient is the change in the mean outcome per one-unit increase in its predictor when all the other predictors are held constant; in logistic regression the odds are multiplied by exp(coefficient) per unit.
- **Also:** Cox: R survival package, help page summary.coxph ('the coefficient, the hazard ratio exp(coef), standard error, Wald statistic, and P value') (https://stat.ethz.ch/R-manual/R-devel/library/survival/html/summary.coxph.html). Categorical predictors and the reference category: Schneider A, Hommel G, Blettner M. Linear regression analysis: part 14 of a series on evaluation of scientific publications. Dtsch Arztebl Int, 2010;107(44):776–782 (https://pmc.ncbi.nlm.nih.gov/articles/PMC2992018/). Logistic: https://online.stat.psu.edu/stat501/Lesson13.html
- **Checked:** 16.11.2026, passage read
- **Notes:** Defined for regression coefficients only, as the scope note asks; 'correlation coefficient' belongs to the correlation entries.

### `cohens-d`

**Cohen's d.** An effect size for the difference between two means: the difference divided by the standard deviation of the two groups, pooled into one. It counts the difference in standard deviations instead of points, so effects measured on different scales can be compared. For paired data, Cohen's dz divides the mean change by the standard deviation of the changes.

- **Source:** Lakens D. Calculating and reporting effect sizes to facilitate cumulative science: a practical primer for t-tests and ANOVAs. Frontiers in Psychology, 2013;4:863; sections "Cohen's d in between-subjects designs" and "Cohen's d in one-sample or correlated samples comparisons"
- **URL:** <https://pmc.ncbi.nlm.nih.gov/articles/PMC3840331/>
- **Supports:** The numerator is the difference between the two group means and the denominator the pooled standard deviation; for dz the denominator is the standard deviation of the difference scores.
- **Also:** effectsize documentation, cohens_d() ("the estimated the standardized difference between the means of two populations"): https://easystats.github.io/effectsize/reference/cohens_d.html . Original, not opened: Cohen J. Statistical Power Analysis for the Behavioral Sciences, 2nd ed. Routledge, 1988.
- **Checked:** 16.11.2026, passage read
- **Notes:** Both senses used on the site are covered: d for two groups (page 18) and dz for paired data (page 7). No cut-offs given. Possible disagreement with the site: page 7 says the usual 0.2/0.5/0.8 guide "applies" to dz; Lakens says those benchmarks are arbitrary, and that dz depends on the correlation between the paired measurements (larger than the other paired d versions when r > 0.5), so it is not on the same footing as a between-group d.

### `kappa`

**Cohen's kappa (κ).** A measure of how well two raters agree when they sort the same patients into categories, after allowing for the agreement expected by chance alone. It is 1 for perfect agreement and 0 for agreement no better than chance. Weighted kappa is the version for ordered categories: a near miss counts as a smaller disagreement than a big miss.

- **Source:** McHugh ML. Interrater reliability: the kappa statistic. Biochem Med (Zagreb) 2012;22(3):276–282; section 'Cohen's kappa'
- **URL:** <https://pmc.ncbi.nlm.nih.gov/articles/PMC3900052/>
- **Supports:** Kappa accounts for chance agreement: "0 represents the amount of agreement that can be expected from random chance, and 1 represents perfect agreement between the raters"; kappa = (observed - chance) / (1 - chance).
- **Also:** Tang W, Hu J, Zhang H, Wu P, He H. Kappa coefficient: a popular measure of rater agreement. Shanghai Arch Psychiatry 2015;27(1):62–67; section 5 (for ordered categories "a weighted kappa coefficient is computed that takes into consideration the different levels of disagreement between categories"), https://pmc.ncbi.nlm.nih.gov/articles/PMC4372765/. Originals, not opened: Cohen J. A coefficient of agreement for nominal scales. Educ Psychol Meas 1960;20(1):37–46; Cohen J. Weighted kappa: nominal scale agreement with provision for scaled disagreement or partial credit. Psychol Bull 1968;70(4):213–220, https://doi.org/10.1037/h0026256
- **Checked:** 16.11.2026, passage read
- **Notes:** Cohen's two papers were not opened. Kappa can be negative (McHugh: possible but unlikely in practice); left out for brevity. Landis and Koch's labels are left to page 17. Agrees with page 17's wording and by-hand box.

### `cohort`

**Cohort.** A defined group of patients who are followed over time, such as everyone who had a hip replacement at one hospital during given years. In a cohort study, what happens to them is recorded, and subgroups, such as patients with different implants, are often compared.

- **Source:** Cochrane Community. Glossary. Cochrane; archived copy of community.cochrane.org/glossary (Internet Archive snapshot of 01.07.2019); entry "Cohort study"
- **URL:** <https://web.archive.org/web/20190701142620/https://community.cochrane.org/glossary>
- **Supports:** "An observational study in which a defined group of people (the cohort) is followed over time"; outcomes of subsets of the cohort are compared.
- **Also:** Vandenbroucke JP, von Elm E, Altman DG, et al. Strengthening the Reporting of Observational Studies in Epidemiology (STROBE): Explanation and Elaboration. PLoS Med, 2007;4(10):e297; Box 1 ("In cohort studies, the investigators follow people over time"). https://doi.org/10.1371/journal.pmed.0040297
- **Checked:** 16.11.2026, passage read
- **Notes:** Cochrane has retired its glossary page (community.cochrane.org/glossary now redirects to resources.cochrane.org, which points readers to archive.org), so the entry was read in the Internet Archive snapshot of 01.07.2019. The site mostly uses "cohort" loosely for the patients of one dataset ("the joint replacement cohort", "this synthetic cohort"), and that cohort's rows are procedures, not people (80 patients appear twice), whereas the sources define a cohort as a group of people. Harrell's glossary defines a cohort study differently ("all subjects meeting the entry criteria are included"); the hospital example follows that idea.

### `cles`

**Common language effect size (CLES).** The probability that a randomly chosen patient from one group has a higher value than a randomly chosen patient from the other group, with a tie counted as half. It is also called the probability of superiority. A value of 0.5 means that higher and lower are equally likely.

- **Source:** Vallat R. pingouin documentation, pingouin.mwu(); Notes
- **URL:** <https://pingouin-stats.org/generated/pingouin.mwu.html>
- **Supports:** "The common language effect size is the proportion of pairs where x is higher than y"; pingouin computes P(X > Y) + 0.5 × P(X = Y).
- **Also:** Lakens D. Calculating and reporting effect sizes to facilitate cumulative science: a practical primer for t-tests and ANOVAs. Frontiers in Psychology, 2013;4:863; section "Cohen's d in between-subjects designs" ("also known as the probability of superiority"; the probability that a randomly sampled person from one group has a higher observed measurement than a randomly sampled person from the other): https://pmc.ncbi.nlm.nih.gov/articles/PMC3840331/ . Originals, not opened (as cited by pingouin): McGraw KO, Wong SP. A common language effect size statistic. Psychological Bulletin 1992;111(2):361–365; Vargha A, Delaney HD. Journal of Educational and Behavioral Statistics 2000;25(2):101–132.
- **Checked:** 16.11.2026, passage read
- **Notes:** Defined as pingouin computes it (counting pairs, ties as half), which is what pages 6 and 7 print. McGraw and Wong's original version, described by Lakens, works it out from the means and SDs assuming normal distributions. The 0.5 sentence is not a quote: it follows by arithmetic from the formula (equal shares of higher and lower pairs give 0.5).

### `competing-risk`

**Competing risk.** An event that makes the event of interest impossible. A patient who dies can never have a revision, so death is a competing risk for revision. Counting such patients as censored makes 1 minus the Kaplan-Meier estimate overstate how many patients will have the event.

- **Source:** Austin PC, Lee DS, Fine JP. Introduction to the analysis of survival data in the presence of competing risks. Circulation 2016;133(6):601–609. doi:10.1161/CIRCULATIONAHA.115.017719; introduction and section "Estimating Crude Incidence"
- **URL:** <https://pmc.ncbi.nlm.nih.gov/articles/PMC4741409/>
- **Supports:** "A competing risk is an event whose occurrence precludes the occurrence of the primary event of interest."
- **Also:** Clark TG, Bradburn MJ, Love SB, Altman DG. Survival analysis part IV: further concepts and methods in survival analysis. Br J Cancer 2003;89(5):781–786. doi:10.1038/sj.bjc.6601117 (with competing risks "the Kaplan–Meier method, in particular, tends to overestimate the proportion of subjects experiencing each event"). https://pmc.ncbi.nlm.nih.gov/articles/PMC2394469/
- **Checked:** 16.11.2026, passage read
- **Notes:** The source's example is death from another cause when the outcome is cardiovascular death; revision and death is the site's example of the same thing. Covers "competing event". Primary source read in full text.

### `complete-case-analysis`

**Complete-case analysis.** An analysis that uses only the patients who have a value for every variable it needs and leaves out everyone else. It loses precision because fewer patients are analyzed, and it can be biased when the patients left out differ from those kept.

- **Source:** Sterne JAC, White IR, Carlin JB, et al. Multiple imputation for missing data in epidemiological and clinical research: potential and pitfalls. BMJ, 2009;338:b2393; "Consequences of missing data"
- **URL:** <https://pmc.ncbi.nlm.nih.gov/articles/PMC2714692/>
- **Supports:** Complete cases are "those individuals who have no missing data in any of the variables required for that analysis"; results can be biased and lose precision.
- **Also:** Vandenbroucke JP, von Elm E, Altman DG, et al. Strengthening the Reporting of Observational Studies in Epidemiology (STROBE): Explanation and Elaboration. PLoS Med, 2007;4(10):e297; Box 6 (bias arises if individuals with missing data are not typical of the whole sample; inefficiency from the reduced sample size). https://doi.org/10.1371/journal.pmed.0040297
- **Checked:** 16.11.2026, passage read
- **Notes:** The English pages never use the term itself; they say "dropping incomplete cases" (page 16) and describe repeated-measures ANOVA dropping knees without all four scores, which is a complete-case analysis.

### `concordance`

**Concordance (C-index).** How often a model ranks two patients in the right order: of all the pairs that can be compared, the share in which the patient the model rated at higher risk was the one who had the event sooner. A value of 0.5 is what random guessing would give, and 1 is a perfect ranking. It is also called the C-index or c statistic.

- **Source:** Therneau T, Atkinson E. Concordance (vignette). R package survival, CRAN, 09.09.2026; section 1.1
- **URL:** <https://cran.r-project.org/web/packages/survival/vignettes/concordance.pdf>
- **Supports:** C is the fraction of concordant pairs, pairs in which prediction and outcome go in the same direction; it ranges from 0 to 1, and 1/2 corresponds to a random guess.
- **Also:** lifelines documentation, CoxPHFitter: 'the concordance score (also known as the c-index)' (https://lifelines.readthedocs.io/en/latest/fitters/regression/CoxPHFitter.html). Harrell FE. Glossary of Statistical Terms. Vanderbilt University, 26.04.2025; entry 'ROC curve': c is the concordance probability (https://hbiostat.org/glossary/)
- **Checked:** 16.11.2026, passage read
- **Notes:** Written for the survival use on pages 11 and 14. For a yes/no outcome the vignette says it equals the area under the ROC curve; left out because ROC is not a glossary term. Tied predictions count as half in R; left out. The vignette calls values of 0.5 to 0.55 'not very impressive'; no cut-off was put in the definition.

### `confidence-interval`

**Confidence interval (CI).** A range of values for the true effect that fit the data. A 95% CI comes from a method that captures the true value in 95 of 100 repeated studies.

- **Source:** Greenland S, Senn SJ, Rothman KJ, Carlin JB, Poole C, Goodman SN, Altman DG. Statistical tests, P values, confidence intervals, and power: a guide to misinterpretations. Eur J Epidemiol 2016;31(4):337 to 350; section "Moving from tests to estimates" and misinterpretation 19
- **URL:** <https://doi.org/10.1007/s10654-016-0149-3>
- **Supports:** A 95% CI is the range of effect sizes more compatible with the data; "95 % of them, on average, will contain (i.e., include or cover) the true effect size".
- **Also:** Harrell FE. Glossary of Statistical Terms. Vanderbilt University School of Medicine, Department of Biostatistics, version of 26.04.2025, entry "confidence limits" ("0.95 of similarly constructed confidence limits in repeated samples from the same population would contain the unknown quantity"; "better called compatibility intervals"). https://hbiostat.org/glossary/ . Also GraphPad Software. GraphPad Prism 11 Statistics Guide (the guide the brief lists as Motulsky's); page "Interpreting a confidence interval of a mean". https://www.graphpad.com/guides/prism/latest/statistics/stat_more_about_confidence_interval.htm
- **Checked:** 16.11.2026, passage read
- **Notes:** Fully supported. Two qualifiers in Greenland that the definition leaves out: the 95% holds "on average" over very many studies (not exactly 95 of every 100), and only "if all the assumptions used to compute the intervals were correct". The first sentence says "true effect"; GraphPad notes a CI can be computed for almost any value (a mean, a proportion), which the second sentence's "true value" covers.

### `confounding`

**Confounding.** A distortion of a comparison between groups, caused by a third factor (the confounder) that is related both to the group a patient is in and to the outcome. If older patients more often receive one implant and also have more complications, age confounds the comparison of the implants. Adjusting for the confounder in the analysis reduces the distortion.

- **Source:** Vandenbroucke JP, von Elm E, Altman DG, et al. Strengthening the Reporting of Observational Studies in Epidemiology (STROBE): explanation and elaboration. PLoS Medicine, 2007;4(10):e297; Box 5, "Confounding"
- **URL:** <https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.0040297>
- **Supports:** STROBE: a seeming association (or lack of one) is due to another factor that determines the outcome and is also associated with the exposure, the confounder; stratification or multivariable analysis reduces its effect.
- **Also:** Harrell FE. Glossary of Statistical Terms. Vanderbilt University School of Medicine, Department of Biostatistics, 26.04.2025; entry "confounder" (a variable that is a common cause of, or just associated with, the response and the exposure, and that can explain away an apparent association). https://hbiostat.org/glossary/ Also CDC. Principles of Epidemiology in Public Health Practice, 3rd edition; Glossary, "confounding" ("the distortion of the association between an exposure and a health outcome by a third variable that is related to both"). https://archive.cdc.gov/www_cdc_gov/csels/dsepd/ss1978/glossary.html
- **Checked:** 16.11.2026, passage read
- **Notes:** 'Exposure' is replaced by 'the group a patient is in' to avoid a word that has no glossary entry. The implant and age example is this site's analog of STROBE's contraceptive and blood pressure example (page 14 uses the same idea); it is an illustration, not from the source. Harrell adds that a confounder is measured before the exposure, which separates it from a mediator (own entry elsewhere).

### `conover-test`

**Conover's test.** A post-hoc test used after the Friedman test to compare the visits or conditions in pairs. It works on the same kind of ranks as the Friedman test, and its p-values are then adjusted for multiple comparisons.

- **Source:** Pohlert T. PMCMRplus package (version 1.9.10) documentation, frdAllPairsConoverTest(): Conover's All-Pairs Comparisons Test for Unreplicated Blocked Data
- **URL:** <https://search.r-project.org/CRAN/refmans/PMCMRplus/html/frdAllPairsConoverTest.html>
- **Supports:** "Performs Conover's all-pairs comparisons tests of Friedman-type ranked data"; p-values come from the t distribution with any p.adjust method, or from the studentized range distribution.
- **Also:** scikit-posthocs documentation, posthoc_conover_friedman() ("usually conducted post hoc after significant results of the Friedman test"), https://scikit-posthocs.readthedocs.io/en/latest/generated/scikit_posthocs.posthoc_conover_friedman.html. Underlying reference, not opened: Conover WJ. Practical Nonparametric Statistics, 3rd edition. Wiley, 1999
- **Checked:** 16.11.2026, passage read
- **Notes:** UNCONFIRMED site claim: page 15 says Conover's test 'is often more powerful' than pairwise Wilcoxon tests; neither documentation page says so, and I could not open Conover's book or another source that does. The definition leaves it out. Also note that 'Conover's test' can mean the Conover-Iman test after Kruskal-Wallis; the site means the version after Friedman, which is what is defined.

### `conservative`

**Conservative.** Erring on the side of caution. A conservative test or correction gives p-values that are, if anything, too large. A conservative confidence interval is, if anything, wider than necessary: it captures the true value at least as often as it claims.

- **Source:** Motulsky HJ. "Options for Contingency table analyses". GraphPad Statistics Guide (Prism 11). GraphPad Software; accessed 16.11.2026
- **URL:** <https://www.graphpad.com/guides/prism/latest/statistics/stat_chi-square_or_fishers_test.htm>
- **Supports:** Motulsky: the Yates correction over corrects, so it "gives a P value that is too large (too 'conservative')".
- **Also:** statsmodels 0.15.0 documentation, statsmodels.stats.proportion.proportion_confint, Notes ("the Clopper-Pearson exact interval has coverage at least 1-alpha, but is in general conservative"). https://www.statsmodels.org/stable/generated/statsmodels.stats.proportion.proportion_confint.html Also R help for binom.test (the Clopper-Pearson procedure guarantees at least the stated confidence level but in general does not give the shortest intervals). https://stat.ethz.ch/R-manual/R-devel/library/stats/html/binom.test.html
- **Checked:** 16.11.2026, passage read
- **Notes:** DOUBTFUL as a general definition: no acceptable source that could be opened defines 'conservative' in general. The definition is assembled from two documented uses, each read this session (a p-value that is too large; an interval whose coverage is at least the nominal level); the opening phrase 'erring on the side of caution' is a gloss of mine. Not stated because unverified: that a conservative method has less power (the site says of Bonferroni that it 'often throws away real differences').

### `contingency-coefficient`

**Contingency coefficient.** A number that says how strongly two categorical variables in a contingency table are linked, calculated from the chi-square statistic: 0 means no link, and larger values mean a stronger link. Phi and Cramér's V are the common ones. Pearson's contingency coefficient (C) is another, whose largest possible value is below 1 and depends on the size of the table.

- **Source:** The SciPy community. scipy.stats.contingency.association. SciPy v1.18.0 Manual; summary and Notes
- **URL:** <https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.contingency.association.html>
- **Supports:** The function "calculates degree of association between two nominal variables" as Cramer's V, Tschuprow's T or Pearson's Contingency Coefficient; 0.0 means no association and 1.0 perfect association.
- **Also:** Ben-Shachar MS, Makowski D, Lüdecke D, et al. Convert chi-square to phi and other correlation-like effect sizes. effectsize 1.0.3.1 reference, Details (formulas that compute phi, Cramér's V and Pearson's C from chi-square and n). https://easystats.github.io/effectsize/reference/chisq_to_phi.html . Signorell A, et al. Cramer's V, Pearson's Contingency Coefficient and Phi Coefficient. DescTools reference, Details (the contingency coefficient goes from 0 to the square root of (k minus 1) divided by k, with k the smaller of the numbers of rows and columns). https://search.r-project.org/CRAN/refmans/DescTools/html/CramerV.html . Motulsky H. Choosing a statistical test (chapter 37 of Intuitive Biostatistics, 1995), table row "Quantify association between two variables": "Contingency coefficients". https://www.graphpad.com/support/faqid/1790/
- **Checked:** 16.11.2026, passage read
- **Notes:** Two senses, both covered: the site (page 10 and the decision table) follows Motulsky and uses "contingency coefficients" for the whole family (phi, Cramér's V, Pearson's C), while the software documentation keeps the name "contingency coefficient" for Pearson's C alone. All four pages read in this session. The site's maximum for C (page 10) agrees with DescTools. Not confirmed from an opened source: the site's remark that Pearson's C "is older", so the entry leaves it out. DescTools notes that phi can exceed 1 on tables larger than 2 × 2; the site uses phi only for 2 × 2 tables, where this does not arise.

### `contingency-table`

**Contingency table.** A table of counts that sorts patients by two categorical variables: one variable defines the rows, the other the columns, and each cell holds the number of patients with that combination. Also called a cross-tabulation. A 2 × 2 table has two rows and two columns, for example graft type by failure (yes or no).

- **Source:** Bewick V, Cheek L, Ball J. Statistics review 8: Qualitative data - tests of association. Crit Care 2004;8(1):46-53. doi:10.1186/cc2428; section 'Introduction'
- **URL:** <https://pmc.ncbi.nlm.nih.gov/articles/PMC420070/>
- **Supports:** Categorical data are summarized as counts of patients in each category, and for two variables these frequencies 'can be presented in a two-way, or contingency, table'.
- **Also:** R Core Team. R documentation, base::table ('a contingency table of the counts at each combination of factor levels'), https://stat.ethz.ch/R-manual/R-devel/library/base/html/table.html , and stats::xtabs (titled 'Cross Tabulation'), https://stat.ethz.ch/R-manual/R-devel/library/stats/html/xtabs.html ; GraphPad Software. GraphPad Prism 11 Statistics Guide; page 'Key concepts: Contingency tables', https://www.graphpad.com/guides/prism/latest/statistics/introduction_to_contingency_tables.htm
- **Checked:** 16.11.2026, passage read
- **Notes:** Sources differ on paired data: GraphPad's McNemar page says a table of matched pairs 'is not a contingency table' in the usual sense, while R's mcnemar.test help calls it a two-dimensional contingency table. The site's page 7 says 'cross-tabulate the two answers', which fits the definition. Page 1's 'cross-tab' (raw value against recoded value) is the same kind of table.

### `continuity-correction`

**Continuity correction (Yates).** A small adjustment that software makes when it uses a chi-square or normal approximation for counts or ranks: it moves the observed value half a unit closer to the expected value before calculating the test statistic. This usually makes the p-value a little larger. Yates' correction is the version for a 2 × 2 table.

- **Source:** R Core Team. R documentation, package stats version 4.6.0: chisq.test, "Pearson's Chi-squared Test for Count Data", argument correct
- **URL:** <https://stat.ethz.ch/R-manual/R-devel/library/stats/html/chisq.test.html>
- **Supports:** R help: continuity correction for 2 by 2 tables means "one half is subtracted from all |O - E| differences"; SciPy describes Yates' correction as adjusting each observed value by 0.5 towards the expected value.
- **Also:** Motulsky HJ. "Options for Contingency table analyses". GraphPad Statistics Guide (Prism 11). GraphPad Software; accessed 16.11.2026 (the Yates continuity correction is designed to make the chi-square approximation better but over corrects, giving a P value that is too large; with large samples it makes little difference). https://www.graphpad.com/guides/prism/latest/statistics/stat_chi-square_or_fishers_test.htm For ranks: R help for wilcox.test, argument correct (continuity correction in the normal approximation for the p-value), https://stat.ethz.ch/R-manual/R-devel/library/stats/html/wilcox.test.html and SciPy v1.18.0 Manual, scipy.stats.mannwhitneyu (z = (U - mn - d) / se, with d the continuity correction of 1/2).
- **Checked:** 16.11.2026, passage read
- **Notes:** With large samples the correction makes little difference (Motulsky). Unconfirmed and therefore left out: WHY the correction exists (counts move in whole steps while the approximating distribution is smooth). That is the textbook reason, but no acceptable source stating it could be opened (BMJ Statistics at Square One returns 403). 'Usually' because Motulsky notes the rare case where observed and expected values are within 0.25 and the correction lowers the p-value; R caps the correction so that cannot happen there. Yates's original 1934 paper was not opened.

### `continuous-variable`

**Continuous variable.** A variable measured on a numeric scale that can take any value within a range, such as age, BMI or operative time. Scores with many possible values are usually analyzed the same way.

- **Source:** Higgins JPT, Li T, Deeks JJ (eds). Chapter 6: Choosing effect measures and computing estimates of effect. In: Cochrane Handbook for Systematic Reviews of Interventions, version 6.5. Cochrane, 2024; section 6.5.1
- **URL:** <https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-06>
- **Supports:** "The term 'continuous' in statistics conventionally refers to a variable that can take any value in a specified range"; in practice the same methods are used for measurement scales.
- **Also:** Harrell FE. Glossary of Statistical Terms. Vanderbilt University School of Medicine, Department of Biostatistics, 2025 (hbiostat.org); entry "continuous variable" (a variable with at least about 10 possible values can be treated as continuous). https://hbiostat.org/glossary/
- **Checked:** 16.11.2026, passage read
- **Notes:** The site often says "measurement" for this type (decision table column "Measurement"); Cochrane 6.1.1 defines continuous data as "a measurement of a numerical quantity", which matches.

### `contrast`

**Contrast.** A comparison between means, written as a sum in which each mean is multiplied by a weight and the weights add up to zero. The simplest contrast is the difference between two means, such as the mean score at 1 year minus the mean score before surgery.

- **Source:** NIST/SEMATECH e-Handbook of Statistical Methods, section 7.4.2.6 Assessing the response from any factor combination; 'Definition and estimation of contrasts'
- **URL:** <https://www.itl.nist.gov/div898/handbook/prc/section4/prc426.htm>
- **Supports:** "A contrast is a linear combination of 2 or more factor level means with coefficients that sum to zero"; simple contrasts include the difference between two factor means.
- **Also:** Lenth RV. emmeans vignette 'Comparisons and contrasts in emmeans' (pairwise comparisons are linear functions of EMMs with coefficients such as 1 and -1), https://rvlenth.github.io/emmeans/articles/comparisons.html
- **Checked:** 16.11.2026, passage read
- **Notes:** Defined for the site's use: contrasts between model-based means (page 16's weights -1, 0, 0, +1). The loose sense in page 8's table ('contrasts between groups') is the same idea.

### `convergence`

**Convergence.** Many models have no formula for their estimates, so software starts from a first guess and improves it in repeated steps, called iterations. The fit has converged when a further step makes virtually no difference. If the software reports that a model did not converge, the search stopped before reaching that point.

- **Source:** GraphPad Software. GraphPad Prism 11 Curve Fitting Guide; 'How nonlinear regression works'
- **URL:** <https://www.graphpad.com/guides/prism/latest/curve-fitting/how_regression_works2.htm>
- **Supports:** Start with initial values, adjust the parameters again and again to bring the curve closer to the points, and stop when the adjustments make virtually no difference.
- **Also:** NIST/SEMATECH e-Handbook of Statistical Methods. National Institute of Standards and Technology; section 4.1.4.2: iterative procedures need starting values, and with poor ones 'the optimization procedure may not converge' (https://www.itl.nist.gov/div898/handbook/pmd/section1/pmd142.htm). R help pages glm.control and coxph.control: iteration continues until the relative change is below a tolerance, up to a maximum number of iterations (https://stat.ethz.ch/R-manual/R-devel/library/stats/html/glm.control.html)
- **Checked:** 16.11.2026, passage read
- **Notes:** Covers 'converge', 'iterations', 'stops iterating'. The definition does not say what to do after a failed convergence or that the estimates are then unusable: none of the sources I opened states that in plain words.

### `correlation`

**Correlation.** A measure of how closely two variables move together. The correlation coefficient runs from −1 (as one rises the other falls, perfectly) through 0 (no correlation) to 1 (they rise together, perfectly). It says nothing about whether one causes the other.

- **Source:** Penn State Department of Statistics. STAT 200: Elementary Statistics (online course notes), Lesson 3; section 3.4, "Two Quantitative Variables"; accessed 16.11.2026
- **URL:** <https://online.stat.psu.edu/stat200/Lesson03.html>
- **Supports:** Penn State, Definition 3.5: "A measure of the direction and strength of the relationship between two variables"; r lies between -1 and +1, the sign gives the direction, and "Correlation does NOT equal causation".
- **Also:** Motulsky HJ. "Key concepts: Correlation". GraphPad Statistics Guide (Prism 11). GraphPad Software; accessed 16.11.2026 (the coefficient ranges from -1, a perfect inverse relationship, to 1, a perfect positive relationship; zero means no correlation at all). https://www.graphpad.com/guides/prism/latest/statistics/stat_key_concepts_correlation.htm
- **Checked:** 16.11.2026, passage read
- **Notes:** Generic sense; Pearson and Spearman have their own entries. For Pearson's r, 0 means no straight-line relationship (Penn State cautions that r is only for linear relationships); that refinement belongs in the Pearson entry. The 'intraclass correlation' on pages 16 and 17 is a related but different quantity (own entry, icc).

### `cox-regression`

**Cox regression.** A regression model for time-to-event data, also called the Cox proportional hazards model. It relates the hazard to one or more predictors at once and gives a hazard ratio for each, without assuming how the hazard itself changes over time. It does assume proportional hazards.

- **Source:** Bradburn MJ, Clark TG, Love SB, Altman DG. Survival analysis part II: multivariate data analysis – an introduction to concepts and methods. Br J Cancer 2003;89(3):431–436. doi:10.1038/sj.bjc.6601119; sections "The need for multivariate statistical modelling", "The Cox ('semi-parametric') proportional hazards model" and Discussion
- **URL:** <https://pmc.ncbi.nlm.nih.gov/articles/PMC2394368/>
- **Supports:** The Cox model "describes the relation between the event incidence, as expressed by the hazard function and a set of covariates".
- **Also:** Original paper (not opened; bibliographic details checked in Crossref): Cox DR. Regression models and life-tables. J R Stat Soc Series B 1972;34(2):187–202 (with discussion to page 220). https://doi.org/10.1111/j.2517-6161.1972.tb00899.x
- **Checked:** 16.11.2026, passage read
- **Notes:** "Without assuming how the hazard changes" paraphrases: the baseline hazard is estimated nonparametrically, so "the survival times are not assumed to follow a particular statistical distribution". The source says "covariates"; the entry says "predictors" (glossary id predictor). Primary source read in full text.

### `cramers-v`

**Cramér's V.** An effect size for the association between two categorical variables in a contingency table, from 0 (no association) to 1 (perfect association). It is calculated from the chi-square statistic, the number of observations and the number of rows or columns, whichever is smaller. For a 2 × 2 table it is the same as phi (φ).

- **Source:** Ben-Shachar MS, Lüdecke D, Makowski D, et al. effectsize: Indices of Effect Size (R package documentation), phi() / cramers_v() help page; Details
- **URL:** <https://easystats.github.io/effectsize/reference/phi.html>
- **Supports:** Phi and Cramér's V are effect sizes for tests of independence in contingency tables, identical for 2-by-2 tables, ranging between 0 (no dependence) and 1 (perfect dependence).
- **Also:** Tomczak M, Tomczak E. The need to report effect size estimates revisited. An overview of some recommended measures of effect size. Trends in Sport Sciences, 2014;1(21):19–25; p. 24 (phi for 2 × 2 tables, Cramér's V for larger ones; V is the square root of chi-square ÷ (n × df of the smaller of rows and columns); both from 0 to 1): https://www.wbc.poznan.pl/Content/325867/5_Trends_Vol21_2014_%20no1_20.pdf . SciPy documentation, scipy.stats.contingency.association ("1.0 indicates perfect association, and 0.0 means the variables have no association"): https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.contingency.association.html
- **Checked:** 16.11.2026, passage read
- **Notes:** Covers phi as the 2 × 2 case, as the scope note asks. The site's "equals φ (without its sign)" (page 10) is consistent: effectsize reports phi between 0 and 1. No original paper opened (Cramér H. Mathematical Methods of Statistics, 1946 is the usual attribution; I did not see it cited in the opened pages, so it is not in the citation). No cut-offs given.

### `cumulative-incidence`

**Cumulative incidence.** The probability that a given event has happened by a given time. With competing risks, the cumulative incidence function (CIF) is the probability of having the event by that time and before any competing event; 1 minus the Kaplan-Meier estimate overstates it. Without competing risks the two are the same.

- **Source:** Austin PC, Lee DS, Fine JP. Introduction to the analysis of survival data in the presence of competing risks. Circulation 2016;133(6):601–609. doi:10.1161/CIRCULATIONAHA.115.017719; section "Estimating Crude Incidence"
- **URL:** <https://pmc.ncbi.nlm.nih.gov/articles/PMC4741409/>
- **Supports:** The CIF "denotes the probability of experiencing the kth event before time t and before the occurrence of a different type of event".
- **Also:** Clark TG, Bradburn MJ, Love SB, Altman DG. Survival analysis part I: basic concepts and first analyses. Br J Cancer 2003;89(2):232–238. doi:10.1038/sj.bjc.6601118; section "Survival function of the ovarian data" ("The cumulative incidence at a time point is simply one minus the survival probability", with a single event). https://pmc.ncbi.nlm.nih.gov/articles/PMC2394262/
- **Checked:** 16.11.2026, passage read
- **Notes:** Two senses, both covered: with a single event, cumulative incidence is 1 minus survival (Clark et al.; Austin et al.); with competing risks it is the CIF. The site uses the word almost only in the competing-risks sense and sets it against 1 − Kaplan-Meier, which is correct there. Austin et al. say the Kaplan-Meier complement is "generally" too high. Primary source read in full text.

### `degrees-of-freedom`

**Degrees of freedom (df).** Roughly, the number of independent pieces of information behind a part of a calculation. For the noise, it is the sample size minus the number of quantities already estimated; for a comparison, it is the number of groups or categories minus 1 (in a table: rows minus 1, times columns minus 1). Software uses it to pick the reference distribution for a test statistic.

- **Source:** Harrell FE. Glossary of Statistical Terms. Vanderbilt University School of Medicine, Department of Biostatistics, version of 26.04.2025, entry "degrees of freedom"
- **URL:** <https://hbiostat.org/glossary/>
- **Supports:** "Denominator d.f. is also called error d.f. and is the sample size minus the number of parameters needing to be estimated"; a 4-group comparison has 3 d.f.
- **Also:** GraphPad Software. GraphPad Prism 11 Statistics Guide (the guide the brief lists as Motulsky's); pages "Computing the SD" (knowing the mean and all but one value fixes the last one: "there are n-1 degrees of freedom"), "How Prism computes P values from statistical ratios" (P from t and df, from F and two df, from chi-square and df) and "How the chi-square goodness of fit test works" (df = number of categories minus 1). https://www.graphpad.com/guides/prism/latest/statistics/stat_computing_the_sd.htm . Also Çetinkaya-Rundel M, Hardin J. Introduction to Modern Statistics, 2nd ed. OpenIntro; section 18.1.4 (two-way table: df = (rows minus 1) × (columns minus 1)). https://openintro-ims.netlify.app/inference-tables
- **Checked:** 16.11.2026, passage read
- **Revised:** this entry existed before the source check; its wording was changed on that date to match the source.
- **Notes:** The definition describes only one kind of df: Harrell's "denominator" or "error" d.f. (sample size minus the number of quantities estimated), which is right for a t test (page 5: df = n − 1) and for the second df of an F test. Harrell says d.f. "has somewhat different meanings depending on the context" and names a second kind, the number of parameters being tested (4 groups: 3 d.f.). The site links this entry for that second kind too: page 8 ("the number of groups minus 1"; chi-square with (3 − 1) × (2 − 1) = 2), page 5 (categories minus 1), page 15 (Kruskal-Wallis df = 3). For those, "sample size minus the quantities already estimated" gives the wrong number. The last sentence (software uses df to pick the reference distribution) is supported. "Independent pieces of information" is the glossary's own gloss; the sources say "free floating" parameters (Harrell) and "all but one of the values" (GraphPad).

### `deviance`

**Deviance.** A measure of how badly a model fitted by maximum likelihood fits the data: the smaller, the better the fit, and a model that fitted perfectly would have 0. The null deviance belongs to a model with no predictors and the residual deviance to the fitted model. The drop from one to the other is the likelihood ratio test statistic.

- **Source:** R Core Team. R: Fitting Generalized Linear Models (help page glm, stats package); section Value
- **URL:** <https://stat.ethz.ch/R-manual/R-devel/library/stats/html/glm.html>
- **Supports:** Deviance is, up to a constant, minus twice the maximized log-likelihood, with the constant chosen so that a saturated model has deviance zero; the null deviance is that of the null model.
- **Also:** Penn State Eberly College of Science. STAT 501: Regression Methods (online course notes); Lesson 13, section 13.2 (deviance table: the null model has no predictors; the statistic is the null deviance minus the fitted model's deviance) and Topic 3, section T.3.1 (a saturated model is a perfect fit) (https://online.stat.psu.edu/stat501/Lesson13.html)
- **Checked:** 16.11.2026, passage read
- **Notes:** 'The smaller, the better' is my reading of 'minus twice the maximized log-likelihood' (a higher likelihood gives a lower deviance), not a quoted sentence. Matches page 11's 'the misfit of the model without and with time to surgery'.

### `distribution`

**Distribution.** The pattern of how a variable's values are spread out: where their center lies, how widely they vary and whether the shape is symmetric or skewed. A histogram shows it. Named distributions, such as the normal or the binomial, are mathematical models of such a pattern that give the probability of each range of values.

- **Source:** NIST/SEMATECH e-Handbook of Statistical Methods. National Institute of Standards and Technology, 2012; section 1.3.3.14, Histogram, and section 1.3.6.1, What is a Probability Distribution
- **URL:** <https://www.itl.nist.gov/div898/handbook/eda/section3/histogra.htm>
- **Supports:** A histogram summarizes "the distribution of a univariate data set": its center, spread, skewness, outliers and modes; a probability function gives the probability of values or intervals (section 1.3.6.1).
- **Also:** Harrell FE. Biostatistics for Biomedical Research. hbiostat.org; section 4.1 ("The distribution of a random variable X is a profile of its variability and other tendencies"; for a sample it is shown by a histogram). https://hbiostat.org/bbr/descript ; NIST section 1.3.6.1: https://www.itl.nist.gov/div898/handbook/eda/section3/eda361.htm
- **Checked:** 16.11.2026, passage read
- **Notes:** None of the acceptable sources I opened gives a one-line beginner definition of "distribution"; this one is assembled from NIST's list of what a histogram shows about a distribution and Harrell's "profile of its variability". Every part is supported, but the wording is mine. The third sentence covers the site's second sense (binomial, chi-square, "reference distribution"); drop it if only the data sense is wanted.

### `dunn-test`

**Dunn's test.** A post-hoc test used after the Kruskal-Wallis test to compare the groups in pairs. It compares the groups' mean ranks, with the ranks taken from all the values together and not worked out again for each pair. The p-values are then adjusted for multiple comparisons, for example with Holm's method.

- **Source:** GraphPad Software. GraphPad Prism 11 Statistics Guide; page 'How the Dunn method for nonparametric comparisons works'
- **URL:** <https://www.graphpad.com/guides/prism/latest/statistics/stat_how_the_dunn_method_for_nonpar.htm>
- **Supports:** Dunn's test compares the mean ranks of two groups, and "the ranks are those for all the values": ranks are not created again for just the two groups being compared.
- **Also:** Kassambara A. rstatix documentation, dunn_test() ("The mean rank of the different groups is compared. Used for post-hoc test following Kruskal-Wallis test"; pairwise Wilcoxon tests fail "to retain the dependent ranking that produced the Kruskal-Wallis test statistic"), https://rpkgs.datanovia.com/rstatix/reference/dunn_test.html. Original, not opened: Dunn OJ. Multiple comparisons using rank sums. Technometrics 1964;6(3):241–252
- **Checked:** 16.11.2026, passage read
- **Notes:** Dunn's 1964 paper was not opened. GraphPad's own adjustment for Dunn's test is Bonferroni-style (multiply by the number of comparisons); rstatix and scikit-posthocs let you choose, and page 15 chooses Holm. GraphPad also applies Dunn's test after the Friedman test; the site uses it after Kruskal-Wallis only, and the definition follows the site. GraphPad's reference gives Technometrics volume 5; rstatix and scikit-posthocs give volume 6, used here.

### `effect-size`

**Effect size.** A number that says how large a difference or an association is. The p-value doesn't say that.

- **Source:** GraphPad Software. GraphPad Prism 11 Statistics Guide (the guide the brief lists as Motulsky's); page "Understanding ANOVA Effect Sizes", section "Effect Sizes and P values: different interpretations, both important"
- **URL:** <https://www.graphpad.com/guides/prism/latest/statistics/stat_anova_effect_sizes.htm>
- **Supports:** "effect sizes describe how large that effect is"; a P value "says nothing about the magnitude or practical importance of the effect itself".
- **Also:** Greenland S, Senn SJ, Rothman KJ, Carlin JB, Poole C, Goodman SN, Altman DG. Statistical tests, P values, confidence intervals, and power: a guide to misinterpretations. Eur J Epidemiol 2016;31(4):337 to 350; section "Common misinterpretations of single P values" ("Lack of statistical significance indicates that the effect size is small. No!"; the authors use "effect" for "association or effect"). https://doi.org/10.1007/s10654-016-0149-3
- **Checked:** 16.11.2026, passage read
- **Notes:** Fully supported, for differences and for associations (GraphPad: an effect size "quantifies the strength of the relationship"). Could not open Sullivan and Feinn 2012 (J Grad Med Educ 4:279), the usual citation; PubMed Central and the journal site blocked automated access. Cochrane Handbook 6.5.1.2 notes that in the social sciences "effect size" often means the standardized mean difference only; the glossary and the pages use the general sense (a slope or a hazard ratio is an effect size on page 11).

### `efron-method`

**Efron's method (tied times).** A way for Cox regression to handle ties: events recorded at exactly the same time. R's survival package and Python's lifelines both use it. It is more accurate than the simpler Breslow method when there are many ties; when there are no ties, the methods give the same result.

- **Source:** Therneau T. R survival package, help page coxph, version 3.8-6; argument ties and Details
- **URL:** <https://stat.ethz.ch/R-manual/R-devel/library/survival/html/coxph.html>
- **Supports:** "The Efron option is more accurate if there are a large number of ties, and it is the default option here."
- **Also:** lifelines documentation, CoxPHFitter ("Ties are handled using Efron's method"), https://lifelines.readthedocs.io/en/latest/fitters/regression/CoxPHFitter.html. Original paper (not opened; bibliographic details checked in Crossref): Efron B. The efficiency of Cox's likelihood function for censored data. J Am Stat Assoc 1977;72(359):557–565. https://doi.org/10.1080/01621459.1977.10480613
- **Checked:** 16.11.2026, passage read
- **Notes:** The help page also says: "If there are no tied death times all the methods are equivalent." "Simpler" renders the help page's "The Breslow approximation is the easiest to program". Two cautions: R's default switches to Breslow for multi-state Cox models only; and lifelines also uses the name "Breslow's method" for how it estimates the baseline hazard, which is a different thing from tie handling. What the method does arithmetically is not described in any source opened, so the entry does not say. Read through the fetch tool's quotes of the page, not as full text.

### `epsilon-squared`

**Epsilon squared (ε²).** An effect size for the Kruskal-Wallis test: the test statistic H divided by the number of observations minus 1. It runs from 0 to 1, and larger values mean larger differences between the groups.

- **Source:** Tomczak M, Tomczak E. The need to report effect size estimates revisited. An overview of some recommended measures of effect size. Trends in Sport Sciences, 2014;1(21):19–25; p. 24
- **URL:** <https://www.wbc.poznan.pl/Content/325867/5_Trends_Vol21_2014_%20no1_20.pdf>
- **Supports:** After a Kruskal-Wallis test, epsilon squared is H divided by (n² − 1)/(n + 1), which is n − 1; it runs from 0 (no relationship) to 1 (perfect relationship).
- **Also:** Ben-Shachar MS, Lüdecke D, Makowski D, et al. effectsize: Indices of Effect Size (R package documentation), rank_epsilon_squared() help page; Details ("Values range from 0 to 1, with larger values indicating larger differences between groups"): https://easystats.github.io/effectsize/reference/rank_epsilon_squared.html
- **Checked:** 16.11.2026, passage read
- **Notes:** This is the rank epsilon squared that accompanies Kruskal-Wallis, not the Greenhouse-Geisser epsilon (own entry). Page 8 also calls it "the share of the variation in the ranks that the groups account for" and "the rank-based counterpart of omega squared". Neither opened source says the first in words; it does follow by algebra from H ÷ (n − 1), which is my own derivation and not from a source (H is 12 × the between-group sum of squares of the ranks ÷ (n(n + 1)), and the total sum of squares of the ranks is n(n² − 1) ÷ 12), so I left it out of the definition rather than cite it. On the second: H ÷ (n − 1) is the uncorrected share, so it corresponds to eta squared on the ranks, not to the bias-corrected omega squared; the sources call it epsilon squared all the same.

### `equal-variances`

**Equal variances.** The assumption that the values are spread out equally in every group being compared, that is, that the groups have the same variance (and so the same standard deviation) in the population. The ordinary (Student's) t test and ANOVA assume it; Welch's test does not. In regression the matching assumption is that the residuals have the same spread throughout (constant variance).

- **Source:** NIST/SEMATECH e-Handbook of Statistical Methods. National Institute of Standards and Technology; section 1.3.5.10, "Levene Test for Equality of Variances"; accessed 16.11.2026
- **URL:** <https://www.itl.nist.gov/div898/handbook/eda/section3/eda35a.htm>
- **Supports:** NIST: "Equal variances across samples is called homogeneity of variance. Some statistical tests, for example the analysis of variance, assume that variances are equal across groups or samples."
- **Also:** Motulsky HJ. "The unequal variance Welch t test". GraphPad Statistics Guide (Prism 11). GraphPad Software; accessed 16.11.2026 (the standard unpaired test assumes both groups come from populations with the same variance; the Welch test does not). https://www.graphpad.com/guides/prism/latest/statistics/stat_the_unequal_variance_welch_t_t.htm Regression: NIST/SEMATECH e-Handbook of Statistical Methods. National Institute of Standards and Technology; section 4.2.1, "What are the typical underlying assumptions in process modeling?"; accessed 16.11.2026 ("The random errors have a constant standard deviation"). https://www.itl.nist.gov/div898/handbook/pmd/section2/pmd21.htm
- **Checked:** 16.11.2026, passage read
- **Notes:** Covers 'equal variance(s)', 'unequal variances', 'homogeneity of variance' and 'constant variance'. The site's advice not to pick the t test by a preliminary variance test matches Motulsky's Welch page ('this is not a good plan').

### `estimate`

**Estimate (point estimate).** A number calculated from the sample that stands in for an unknown true value in the population, such as a mean, a difference between two means or a regression coefficient. A point estimate is that single number, as opposed to the confidence interval around it. An estimator is the method that produces it, such as the Kaplan-Meier estimator.

- **Source:** Harrell FE. Glossary of Statistical Terms. Vanderbilt University School of Medicine, Department of Biostatistics, 26.04.2025; entries "estimate" and "nonparametric estimator"
- **URL:** <https://hbiostat.org/glossary/>
- **Supports:** Harrell: "A statistical estimate of a parameter based on the data ... Examples include the sample mean, sample median, and estimated regression coefficients"; a nonparametric estimator is "a method for estimating a parameter", for example the Kaplan-Meier estimator.
- **Also:** Penn State Department of Statistics. STAT 200: Elementary Statistics (online course notes), Lesson 4; section 4.2, "Introduction to Confidence Intervals"; accessed 16.11.2026 (Definition 4.5: point estimate, the "sample statistic that serves as the best estimate for a population parameter", at the center of a confidence interval). https://online.stat.psu.edu/stat200/Lesson04.html
- **Checked:** 16.11.2026, passage read
- **Notes:** Covers 'estimate', 'point estimate' and 'estimator'. Harrell defines an estimate through the word parameter (own entry in this batch); the definition says 'unknown true value' instead to stay plain.

### `estimated-marginal-means`

**Estimated marginal means.** The mean outcome that a fitted model predicts for each group or visit, averaged evenly over the other predictors in the model. They come from the model and not straight from the raw data, so a different model gives different values. Also called EMMs or least-squares means.

- **Source:** Lenth RV. emmeans package (version 2.0.5), vignette 'Basics of estimated marginal means'; sections 'Estimated marginal means' and 'Summary of main points'
- **URL:** <https://rvlenth.github.io/emmeans/articles/basics.html>
- **Supports:** A reference grid of all factor combinations is formed, model predictions are obtained on it, and EMMs are equally weighted marginal averages of those predictions; "EMMs are derived from a model. A different model for the same data may lead to different EMMs."
- **Also:** emmeans package website: "Estimated marginal means (EMMs, also known as least-squares means in the context of traditional regression models)", https://rvlenth.github.io/emmeans/
- **Checked:** 16.11.2026, passage read
- **Notes:** Page 16 adds that the EMMs use every knee, including those with missed visits; that is a property of the mixed model, not of EMMs, and is left to the page.

### `eta-squared`

**Eta squared (η²).** An effect size for ANOVA: the share of the total variation in the outcome that goes with group membership. Partial eta squared sets aside the variation due to other factors, such as the differences between patients in a repeated-measures design; generalized eta squared keeps those differences between patients in, so that different study designs can be compared. Omega squared is eta squared corrected for its tendency to come out too high in a sample.

- **Source:** Lakens D. Calculating and reporting effect sizes to facilitate cumulative science: a practical primer for t-tests and ANOVAs. Frontiers in Psychology, 2013;4:863; section "Eta-squared in between and within-subjects comparisons"
- **URL:** <https://pmc.ncbi.nlm.nih.gov/articles/PMC3840331/>
- **Supports:** Eta squared "measures the proportion of the variation in Y that is associated with membership of the different groups defined by X"; partial, generalized and omega squared are described as paraphrased.
- **Also:** Ben-Shachar MS, Lüdecke D, Makowski D, et al. effectsize: Indices of Effect Size (R package documentation), eta_squared() help page (the indices estimate "how much variance in the response variables is accounted for by the explanatory variable(s)"; omega and epsilon squared correct the bias, "especially important is small samples"): https://easystats.github.io/effectsize/reference/eta_squared.html . Original for generalized eta squared, not opened: Olejnik S, Algina J. Generalized eta and omega squared statistics: measures of effect size for some common research designs. Psychological Methods 2003;8:434–447 (as cited by Lakens).
- **Checked:** 16.11.2026, passage read
- **Notes:** One entry covers eta squared, partial and generalized eta squared and omega squared, as the scope note asks. No cut-offs given. Possible disagreement with the site: page 9 applies the 0.01/0.06/0.14 guide to partial eta squared from a repeated-measures ANOVA; Lakens (citing Olejnik and Algina) says using Cohen's benchmarks for partial eta squared in designs with repeated measures "is not consistent with the considerations upon which the benchmarks were based", and that they fit generalized eta squared only as a last resort.

### `event`

**Event.** What a time-to-event analysis waits for: something that happens at one moment, such as revision of an implant, failure of a graft or death. A study has to say exactly what counts as the event and when the clock starts.

- **Source:** Clark TG, Bradburn MJ, Love SB, Altman DG. Survival analysis part I: basic concepts and first analyses. Br J Cancer 2003;89(2):232–238. doi:10.1038/sj.bjc.6601118; sections Introduction and "Types of 'event' in cancer studies"
- **URL:** <https://pmc.ncbi.nlm.nih.gov/articles/PMC2394262/>
- **Supports:** "It is important to state what the event is and when the period of observation starts and finishes."
- **Also:** Austin PC, Lee DS, Fine JP. Introduction to the analysis of survival data in the presence of competing risks. Circulation 2016;133(6):601–609. doi:10.1161/CIRCULATIONAHA.115.017719; introduction ("time to the occurrence of the event of interest"). https://pmc.ncbi.nlm.nih.gov/articles/PMC4741409/
- **Checked:** 16.11.2026, passage read
- **Notes:** The source's examples are death and cancer relapse; the orthopaedic examples (revision, graft failure) are the site's own events, put in their place. Altman & Bland, Time to event (survival) data, BMJ 1998;317:468, would be the shortest citation but could not be opened (BMJ and Europe PMC refused the fetch), so it is not cited. Primary source read in full text.

### `exact-test`

**Exact (and approximate) method.** An exact method works out a p-value or confidence interval from the probability of every result the data could have given, so it is valid at any sample size; Fisher's exact test and the binomial test are examples. An approximate method (software also says asymptotic or large-sample) uses a normal or chi-square distribution as a shortcut and is accurate only when the sample is large enough.

- **Source:** Motulsky HJ. "Options for Contingency table analyses". GraphPad Statistics Guide (Prism 11). GraphPad Software; accessed 16.11.2026
- **URL:** <https://www.graphpad.com/guides/prism/latest/statistics/stat_chi-square_or_fishers_test.htm>
- **Supports:** Motulsky: "The chi-square test is only an approximation", not accurate with small samples; Fisher's exact test "always gives an exact P value and works fine with small sample sizes".
- **Also:** Motulsky HJ. "Interpreting results: Mann-Whitney test". GraphPad Statistics Guide (Prism 11). GraphPad Software; accessed 16.11.2026 (the exact P value tabulates every possible way to shuffle the data; the approximate method converts the statistic to a z value and uses a Gaussian distribution, accurate with large samples). https://www.graphpad.com/guides/prism/latest/statistics/how_the_mann-whitney_test_works.htm Also SciPy v1.18.0 Manual, scipy.stats.mannwhitneyu, parameter method ('asymptotic' compares the standardized statistic against the normal distribution; 'exact' uses the exact distribution of U under the null hypothesis). https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mannwhitneyu.html
- **Checked:** 16.11.2026, passage read
- **Notes:** Covers 'exact test', 'exact p-value', 'exact interval', 'asymptotic', 'approximation', 'large-sample' and 'normal approximation'. 'Large-sample' as a synonym rests on the examples in R's wilcox.test help (exact = FALSE is commented 'large sample approximation'), NIST 1.3.5.15 (the chi-square approximation needs a sufficient sample size) and R's chisq.test help ('asymptotic chi-squared distribution'). Two caveats left out of the definition: Motulsky notes that some statisticians think Fisher's test answers a slightly different question, and exact intervals (Clopper-Pearson) are conservative (see that entry). SITE VS SOURCE: pages 5, 6 and 7 say R computes an exact Wilcoxon or Mann-Whitney p-value only 'without ties'. The R 4.6.0 help for wilcox.test says an exact p-value is computed whenever the samples hold fewer than 50 values, and that with ties exact inference uses the permutation distribution; a test run in R 4.6.0 with tied values returned 'Wilcoxon rank sum exact test' without a warning. The pages' explicit exact = FALSE keeps their numbers right, but the sentences describe older R behavior.

### `expected-count`

**Expected count.** The count a table cell would hold if the null hypothesis were true. In a table of groups by outcome, that means the outcome has nothing to do with the group: row total × column total ÷ grand total. When one group is compared with given proportions, it is the total × the category's proportion.

- **Source:** Çetinkaya-Rundel M, Hardin J. Introduction to Modern Statistics, 2nd ed. OpenIntro; section 18.1.1, Expected counts in two-way tables
- **URL:** <https://openintro-ims.netlify.app/inference-tables>
- **Supports:** Expected counts are what the cells would hold "if there was no difference between the groups": (row total × column total) ÷ table total.
- **Also:** GraphPad Software. GraphPad Prism 11 Statistics Guide (the guide the brief lists as Motulsky's); pages "How the chi-square goodness of fit test works" and "How to: Compare observed and expected distributions" (expected values come from a theory: "Multiply that fraction by the total number"). https://www.graphpad.com/guides/prism/latest/statistics/stat_compareoande.htm
- **Checked:** 16.11.2026, passage read
- **Revised:** this entry existed before the source check; its wording was changed on that date to match the source.
- **Notes:** Correct, formula included, for a table of groups by outcome of any size (pages 6, 8, 10 and 15). It does not cover the second use the site links to this entry: the chi-square goodness-of-fit test on page 5 ("the total number of patients × that category's hypothetical proportion"), where there are no groups and no row or column totals. GraphPad defines those expected counts as the theory's proportion times the total.

### `f-statistic`

**F statistic.** A test statistic that is the ratio of two variances. In ANOVA it is the variation between the group means divided by the variation within the groups: close to 1 when the groups do not differ, and larger when they do. The F distribution, which has two degrees-of-freedom values (one for each variance), turns it into a p-value.

- **Source:** Motulsky HJ. "Interpreting results: One-way ANOVA". GraphPad Statistics Guide (Prism 11). GraphPad Software; accessed 16.11.2026; section "The F statistic (F ratio)"
- **URL:** <https://www.graphpad.com/guides/prism/latest/statistics/f_ratio_and_anova_table_(one-way_anova).htm>
- **Supports:** Motulsky: "The F statistic for ANOVA is the ratio of the mean square for the between groups divided by the mean square within groups"; if the null hypothesis is true you expect F close to 1.0, otherwise greater.
- **Also:** NIST/SEMATECH e-Handbook of Statistical Methods. National Institute of Standards and Technology; section 7.4.3.3, "The ANOVA table and tests of hypotheses about means"; accessed 16.11.2026 (F = MST / MSE, compared with the F distribution on the two degrees of freedom). https://www.itl.nist.gov/div898/handbook/prc/section4/prc433.htm Also NIST/SEMATECH e-Handbook of Statistical Methods. National Institute of Standards and Technology; section 1.3.5.9, "F-Test for Equality of Two Variances"; accessed 16.11.2026 (F is the ratio of two sample variances). https://www.itl.nist.gov/div898/handbook/eda/section3/eda359.htm
- **Checked:** 16.11.2026, passage read
- **Notes:** Covers 'F', 'F statistic' and 'F test'. The site also uses F tests in regression, mixed models and the ICC; those are ratios of variances of the same kind, but only the ANOVA and two-variance cases were read in a source.

### `false-discovery-rate`

**False discovery rate.** Of all the results called significant in a set of tests, the expected share that are false positives. Controlling it, as the Benjamini-Hochberg adjustment does, is a less strict standard than controlling the family-wise error rate.

- **Source:** R Core Team. p.adjust {stats}: Adjust P-values for Multiple Comparisons. R documentation (stats version 4.6.0), Details
- **URL:** <https://stat.ethz.ch/R-manual/R-devel/library/stats/html/p.adjust.html>
- **Supports:** BH and BY "control the false discovery rate, the expected proportion of false discoveries amongst the rejected hypotheses"; the FDR "is a less stringent condition than the family-wise error rate".
- **Also:** Benjamini Y, Hochberg Y. Controlling the False Discovery Rate: A Practical and Powerful Approach to Multiple Testing. J R Stat Soc B 1995;57(1):289–300; summary ("controlling the expected proportion of falsely rejected hypotheses — the false discovery rate"), https://academic.oup.com/jrsssb/article/57/1/289/7035855; GraphPad Software. GraphPad Prism 11 Statistics Guide, 'What is a family of comparisons?', https://www.graphpad.com/guides/prism/latest/statistics/stat_comparison_family.htm
- **Checked:** 16.11.2026, passage read
- **Notes:** Of the original paper only the summary was read (through the fetch tool; the PDF is a scan without text). Agrees with page 15's wording.

### `false-negative`

**False negative (type II error).** A result that is not statistically significant when there truly is a difference: chance made the sample look as if there were none. For a true difference of a given size, its probability is called beta, and power is 1 minus beta. Statisticians call it a type II error.

- **Source:** Motulsky HJ. "Type I, II (and III) errors". GraphPad Statistics Guide (Prism 11). GraphPad Software; accessed 20.11.2026
- **URL:** <https://www.graphpad.com/guides/prism/latest/statistics/type_i_ii_and_iii_errors.htm>
- **Supports:** Motulsky: "You've made a type II error when there really is a difference (association, correlation) overall, but random sampling caused your data to not show a statistically significant difference."
- **Also:** Greenland S, Senn SJ, Rothman KJ, Carlin JB, Poole C, Goodman SN, Altman DG. Statistical tests, P values, confidence intervals, and power: a guide to misinterpretations. Eur J Epidemiol 2016;31(4):337 to 350. doi:10.1007/s10654-016-0149-3; section "Common misinterpretations of power": "The corresponding pre-study probability of failing to reject the test hypothesis when the alternative is correct is one minus the power, also known as the Type-II or beta error rate"; misinterpretation 24 calls this error "a false negative". <https://pmc.ncbi.nlm.nih.gov/articles/PMC4877414/>
- **Checked:** 20.11.2026, passage read (GraphPad page and Greenland et al. in full text, Europe PMC)
- **Notes:** Added in the content review of 20.11.2026 (B8) as the counterpart of `false-positive`. "For a true difference of a given size" follows Greenland: beta is defined for a particular alternative (the one used to compute power), so it is a probability given that difference, not the chance that a non-significant result is wrong (Greenland's misinterpretation 24). Power is 1 minus beta by Greenland's sentence; the `power` entry's own sources agree on what power is.

### `false-positive`

**False positive (type I error).** A statistically significant result when there is truly no difference: chance alone made the sample look as if there were one. A test at the 0.05 significance level gives a false positive in 5% of studies in which there is truly no difference. Statisticians call it a type I error.

- **Source:** Motulsky HJ. "Type I, II (and III) errors". GraphPad Statistics Guide (Prism 11). GraphPad Software; accessed 16.11.2026
- **URL:** <https://www.graphpad.com/guides/prism/latest/statistics/type_i_ii_and_iii_errors.htm>
- **Supports:** Motulsky: a type I error is made when there really is no difference overall, but random sampling caused your data to show a statistically significant difference.
- **Also:** Penn State Department of Statistics. STAT 200: Elementary Statistics (online course notes), Lesson 6; section 6.1, "Type I and Type II Errors"; accessed 16.11.2026 (Definition 6.1: rejecting H0 when H0 is really true; its probability is alpha, commonly set at .05). https://online.stat.psu.edu/stat200/Lesson06.html The wording "false positives" for significant results without a real effect is used in Motulsky HJ. "The false discovery rate and statistical significance". GraphPad Statistics Guide (Prism 11). GraphPad Software; accessed 16.11.2026. https://www.graphpad.com/guides/prism/latest/statistics/a_bayesian_perspective_on_interpreting_statistical_significance.htm
- **Checked:** 16.11.2026, passage read
- **Notes:** Also covers 'false alarm' (the site's informal synonym; not found in the sources). Caution from Harrell's glossary (entry 'type I assertion probability'): alpha is 'frequently confusingly labeled as a false positive probability'; it is the chance of a significant result GIVEN no effect, not the chance that a significant result is false. The site's sentence on page 15 is conditional in the right way. Harrell also notes the 5% holds only when one p-value is computed and the test's assumptions are true.

### `family-wise-error-rate`

**Family-wise error rate.** The chance of at least one false positive across a whole set (family) of tests when there are truly no differences. Adjustments such as Holm's and Bonferroni's keep it at or below the chosen level, usually 5%.

- **Source:** GraphPad Software. GraphPad Prism 11 Statistics Guide; page 'What is a family of comparisons?'
- **URL:** <https://www.graphpad.com/guides/prism/latest/statistics/stat_comparison_family.htm>
- **Supports:** FWER methods are designed so that, if all null hypotheses in the family are true, the probability of "even one spuriously significant result across the entire family stays at or below alpha".
- **Also:** R Core Team. p.adjust {stats}: Adjust P-values for Multiple Comparisons. R documentation (stats version 4.6.0), Details (Bonferroni, Holm, Hochberg and Hommel "are designed to give strong control of the family-wise error rate"), https://stat.ethz.ch/R-manual/R-devel/library/stats/html/p.adjust.html; Perneger TV. What's wrong with Bonferroni adjustments. BMJ 1998;316(7139):1236–1238 (20 independent tests give a 0.64 chance of at least one significant result), https://pmc.ncbi.nlm.nih.gov/articles/PMC1112991/
- **Checked:** 16.11.2026, passage read
- **Notes:** Agrees with page 15, including its 1 - 0.95^k formula (Perneger gives the same formula and the same 64% for 20 tests). GraphPad spells it 'familywise'; the label follows master.tsv.

### `fine-gray`

**Fine-Gray regression.** A regression model for competing risks that relates predictors to the cumulative incidence of one event. Its results are subdistribution hazard ratios, which are not ordinary hazard ratios: patients who have had a competing event stay in the at-risk group. It suits the question of how many patients will have the event.

- **Source:** Austin PC, Lee DS, Fine JP. Introduction to the analysis of survival data in the presence of competing risks. Circulation 2016;133(6):601–609. doi:10.1161/CIRCULATIONAHA.115.017719; section "Hazard Function Regression" and Discussion
- **URL:** <https://pmc.ncbi.nlm.nih.gov/articles/PMC4741409/>
- **Supports:** The subdistribution hazard model estimates the effect of covariates on the cumulative incidence function, and its risk set keeps subjects who have had a competing event.
- **Also:** Original paper (not opened; bibliographic details checked in Crossref): Fine JP, Gray RJ. A proportional hazards model for the subdistribution of a competing risk. J Am Stat Assoc 1999;94(446):496–509. https://doi.org/10.1080/01621459.1999.10474144. Also Therneau T, Crowson C, Atkinson E. Multi-state models and competing risks. Vignette of the R survival package (CRAN; PDF dated 09.09.2026); section 4 Fine-Gray model, https://cran.r-project.org/web/packages/survival/vignettes/compete.pdf
- **Checked:** 16.11.2026, passage read
- **Notes:** Covers "subdistribution hazard". Austin et al. recommend the model "when the focus is on estimating incidence or predicting prognosis" and the cause-specific Cox model for questions of cause. The site's warning that the subdistribution hazard ratio shows only the direction of the effect on the cumulative incidence (page 14) goes a little further than the source opened here; it is what Austin and Fine's later paper on reporting Fine-Gray analyses (Stat Med 2017) is known for, but that paper was not opened and its citation is from memory, so check it before citing. Primary source read in full text.

### `fisher-exact-test`

**Fisher's exact test.** An exact test of whether two categorical variables in a contingency table, most often a 2 × 2 table, are associated. It keeps the row and column totals fixed and adds up the exact probabilities of the tables at least as extreme as the one observed, so it also works when the counts are small.

- **Source:** Bewick V, Cheek L, Ball J. Statistics review 8: Qualitative data - tests of association. Crit Care 2004;8(1):46-53. doi:10.1186/cc2428; section 'Fisher's exact test'
- **URL:** <https://pmc.ncbi.nlm.nih.gov/articles/PMC420070/>
- **Supports:** The exact P value comes from all tables with the same row and column totals as the original that are as or more extreme in their departure from the null hypothesis.
- **Also:** GraphPad Software. GraphPad Prism 11 Statistics Guide; page 'Options for Contingency table analyses' (Fisher's test 'always gives an exact P value and works fine with small sample sizes'), https://www.graphpad.com/guides/prism/latest/statistics/stat_chi-square_or_fishers_test.htm ; R Core Team. R documentation, stats::fisher.test ('independence of rows and columns in a contingency table with fixed marginals'), https://stat.ethz.ch/R-manual/R-devel/library/stats/html/fisher.test.html
- **Checked:** 16.11.2026, passage read
- **Notes:** 'At least as extreme' is defined in more than one way for the two-sided p-value: the site's page 6, GraphPad and R add up the tables that are no more likely than the observed one, while the Critical Care review doubles the one-sided value. The definition's wording covers both. GraphPad also reports the view that fixed row and column totals rarely match the study design, a nuance the site does not mention.

### `fixed-effect`

**Fixed effect.** The part of a mixed model that describes the effect of a predictor of interest, such as treatment or visit, on the average patient. A fixed effect is the same for every patient, unlike a random effect.

- **Source:** Schober P, Vetter TR. Repeated Measures Designs and Analysis of Longitudinal Data: If at First You Do Not Succeed—Try, Try Again. Anesth Analg 2018;127(2):569–575; section 'Mixed-Effect Models'
- **URL:** <https://pmc.ncbi.nlm.nih.gov/articles/PMC6072386/>
- **Supports:** Effects of covariates of specific scientific interest (treatment groups, age, sex) "are referred to as fixed effects"; the fixed effect of time estimates the average change across the subjects.
- **Also:** statsmodels documentation, Linear Mixed Effects Models, https://www.statsmodels.org/stable/mixed_linear.html (the "fixed effects parameters" are "shared by all subjects")
- **Checked:** 16.11.2026, passage read

### `follow-up`

**Follow-up.** The time during which a patient is observed in a study, from the starting point (such as the date of surgery) until the event or the last date on which their status is known. A patient who is lost to follow-up stopped being observed before the study ended, and is censored at the last date known.

- **Source:** Clark TG, Bradburn MJ, Love SB, Altman DG. Survival analysis part I: basic concepts and first analyses. Br J Cancer 2003;89(2):232–238. doi:10.1038/sj.bjc.6601118; sections "Types of 'event' in cancer studies", "Censoring makes survival analysis different", "Illustrative studies" and "Length of follow-up"
- **URL:** <https://pmc.ncbi.nlm.nih.gov/articles/PMC2394262/>
- **Supports:** Censoring arises when "a patient is lost to follow-up during the study period"; patients without the event are censored at "the date of last follow-up".
- **Also:** Clark TG, Bradburn MJ, Love SB, Altman DG. Survival analysis part IV: further concepts and methods in survival analysis. Br J Cancer 2003;89(5):781–786. doi:10.1038/sj.bjc.6601117 (informative censoring: patients "lost to follow-up for reasons that may relate to their (unknown) outcome"). https://pmc.ncbi.nlm.nih.gov/articles/PMC2394469/
- **Checked:** 16.11.2026, passage read
- **Notes:** Clark et al. use the word throughout but never define it in one sentence; the entry is put together from their uses ("period of observation", "end of follow-up", "date of last follow-up", "lost to follow-up"). The Cochrane glossary's one-line definition could not be opened (the page has moved), so it is not cited. Primary source read in full text.

### `friedman-test`

**Friedman test.** A rank-based (nonparametric) test for three or more measurements on the same patients, or on matched sets. It ranks each patient's own values from lowest to highest and asks whether some visits tend to rank higher than others, so differences between patients do not affect it.

- **Source:** GraphPad Software. GraphPad Prism 11 Statistics Guide; page 'Interpreting results: Friedman test'
- **URL:** <https://www.graphpad.com/guides/prism/latest/statistics/how_the_friedman_test_works.htm>
- **Supports:** The Friedman test is a nonparametric test for three or more matched groups: it ranks the values within each matched set separately and compares the rank sums, so factors that shift all of a subject's values do not affect it.
- **Also:** Bewick V, Cheek L, Ball J. Statistics review 10: Further nonparametric methods. Crit Care 2004;8(3):196-199. doi:10.1186/cc2857; section 'The Friedman Test' (ranking within each patient 'automatically removing differences between patients'), https://pmc.ncbi.nlm.nih.gov/articles/PMC468904/
- **Checked:** 16.11.2026, passage read

### `games-howell`

**Games-Howell test.** A post-hoc test that compares every pair of group means without assuming that the groups have similar spreads. It is a version of Tukey's HSD that uses Welch's correction, and its p-values are already adjusted for multiple comparisons.

- **Source:** Kassambara A. rstatix package (version 1.1.0) documentation, games_howell_test(): Games Howell Post-hoc Tests
- **URL:** <https://rpkgs.datanovia.com/rstatix/reference/games_howell_test.html>
- **Supports:** Used "when the assumption of homogeneity of variances is violated"; "based on Welch's degrees of freedom correction and uses Tukey's studentized range distribution"; "no need to apply additional p-value corrections".
- **Also:** Lee S, Lee DK. What is the proper way to apply the multiple comparison test? Korean J Anesthesiol 2018;71(5):353–360, https://pmc.ncbi.nlm.nih.gov/articles/PMC6193594/ ("an improved version of the Tukey-Kramer method ... applicable in cases where the equivalence of variance assumption is violated"); GraphPad Software. GraphPad Prism 11 Statistics Guide, 'How the Dunnett T3, Games and Howell, and Tamhane T2 tests work', https://www.graphpad.com/guides/prism/latest/statistics/stat_multiple-comparisons-without-a.htm. Original, not opened: Games & Howell 1976 (full citation not confirmed in this session)
- **Checked:** 16.11.2026, passage read
- **Notes:** Possible divergence from the site: GraphPad (Motulsky) and Lee & Lee both recommend Dunnett's T3 over Games-Howell when groups have fewer than 50 members, and Lee & Lee say Games-Howell needs at least six per group. Page 15 recommends Games-Howell whenever the SDs differ, and its example has groups of 36 and 18. The original paper was not opened and I could not confirm its full citation.

### `gray-test`

**Gray's test.** A test that compares the cumulative incidence of an event between two or more groups when there are competing risks. It does for cumulative incidence curves what the log-rank test does for survival curves.

- **Source:** Gray RJ. R cmprsk package, help page cuminc (Cumulative Incidence Analysis)
- **URL:** <https://search.r-project.org/CRAN/refmans/cmprsk/html/cuminc.html>
- **Supports:** cuminc() will "Estimate cumulative incidence functions from competing risks data and test equality across groups", citing Gray (1988).
- **Also:** tidycmprsk documentation, cuminc() ("The p-values reported in cuminc() ... are Gray's test as described in Gray RJ (1988)"), https://mskcc-epi-bio.github.io/tidycmprsk/reference/cuminc.html. Therneau T, Crowson C, Atkinson E. Multi-state models and competing risks. Vignette of the R survival package (CRAN; PDF dated 09.09.2026); section 4, https://cran.r-project.org/web/packages/survival/vignettes/compete.pdf. Original paper (not opened: the Project Euclid page came back empty; bibliographic details checked in Crossref): Gray RJ. A class of K-sample tests for comparing the cumulative incidence of a competing risk. Ann Stat 1988;16(3):1141–1154. https://doi.org/10.1214/aos/1176350951
- **Checked:** 16.11.2026, passage read
- **Notes:** The comparison with the log-rank test rests on Therneau's vignette: a Fine-Gray model with one two-level predictor "reduces to Gray's test ... in the same way that a coxph fit with a single categorical predictor is equivalent to the log-rank test". No opened source describes how the test statistic is calculated, so the entry does not say. Read through the fetch tool's quotes of the page, not as full text.

### `greenhouse-geisser`

**Greenhouse-Geisser correction.** A correction for repeated-measures ANOVA when sphericity cannot be assumed. It reduces the degrees of freedom according to a number called epsilon, which is 1 when sphericity holds and smaller the more it is violated, and the smaller degrees of freedom give a larger p-value. The Huynh-Feldt correction is a less conservative alternative.

- **Source:** GraphPad Software. GraphPad Prism 11 Statistics Guide; page 'Sphericity and compound symmetry' (section 'Repeated measures ANOVA without assuming sphericity') and 'Quantifying violations of sphericity with epsilon'
- **URL:** <https://www.graphpad.com/guides/prism/latest/statistics/stat_epsilon.htm>
- **Supports:** Epsilon is at most 1.0, which denotes no violation of sphericity, and gets smaller with more violation; the correction only reduces the degrees of freedom, which increases the P value.
- **Also:** Pingouin documentation, pingouin.epsilon (Greenhouse-Geisser, Huynh-Feldt and lower-bound epsilon), https://pingouin-stats.org/generated/pingouin.epsilon.html ; GraphPad page https://www.graphpad.com/guides/prism/latest/statistics/stat_sphericity_and_compound_symmet.htm
- **Checked:** 16.11.2026, passage read
- **Notes:** Doubtful wording in the source: GraphPad says the Greenhouse-Geisser method 'might be a bit conservative' and that Huynh-Feldt 'tends to go too far in the other direction'; 'less conservative' in the definition rests on that sentence and on Pingouin's formula, in which the Huynh-Feldt epsilon is built from the Greenhouse-Geisser one. The sources say the correction reduces the degrees of freedom but do not spell out that they are multiplied by epsilon, so the definition does not say so either. The original papers (Greenhouse and Geisser 1959; Huynh and Feldt 1976) were not opened and are not cited.

### `hazard`

**Hazard.** The moment-to-moment risk of the event among those still at risk: the rate at which events are happening at a given time. It can rise or fall over time. The baseline hazard of a Cox regression is the hazard when every predictor is zero, which the hazard ratios then multiply.

- **Source:** Clark TG, Bradburn MJ, Love SB, Altman DG. Survival analysis part I: basic concepts and first analyses. Br J Cancer 2003;89(2):232–238. doi:10.1038/sj.bjc.6601118; section "Survival and hazard"
- **URL:** <https://pmc.ncbi.nlm.nih.gov/articles/PMC2394262/>
- **Supports:** The hazard "represents the instantaneous event rate for an individual who has already survived to time t".
- **Also:** Bradburn MJ, Clark TG, Love SB, Altman DG. Survival analysis part II: multivariate data analysis – an introduction to concepts and methods. Br J Cancer 2003;89(3):431–436. doi:10.1038/sj.bjc.6601119; section "The Cox ('semi-parametric') proportional hazards model" (baseline hazard = "the value of the hazard if all the x are equal to zero"; "the hazard may (and probably will) vary over time"; covariates "act multiplicatively on the hazard"). https://pmc.ncbi.nlm.nih.gov/articles/PMC2394368/ Also Austin et al. 2016 ("instantaneous rate of occurrence of the event of interest in subjects who are still at risk"), https://pmc.ncbi.nlm.nih.gov/articles/PMC4741409/
- **Checked:** 16.11.2026, passage read
- **Notes:** Wording kept in line with the existing hazard-ratio entry ("moment-to-moment risk of the event among those still at risk"). "Hazard rate" is the same quantity (Clark et al. use both words). Clark et al. first call the hazard a probability and then, "put another way", a rate; the entry uses the rate reading, as the site does on page 14. Primary source read in full text.

### `hazard-ratio`

**Hazard ratio (HR).** One group's hazard divided by the other's. The hazard is the moment-to-moment risk of the event among those still at risk, so a hazard ratio of 2 means the event is twice as likely at any moment.

- **Source:** Harrell FE. Glossary of Statistical Terms. Vanderbilt University School of Medicine, Department of Biostatistics, version of 26.04.2025, entries "hazard ratio" and "hazard rate"
- **URL:** <https://hbiostat.org/glossary/>
- **Supports:** Hazard ratio: "The ratio of hazard rates at a single time t, for two types of subjects"; hazard rate: the instantaneous risk of the event, given it has not yet occurred.
- **Also:** Clark TG, Bradburn MJ, Love SB, Altman DG. Survival analysis part I: basic concepts and first analyses. Br J Cancer 2003;89(2):232 to 238; section "Survival and hazard" (the hazard is "the instantaneous event rate for an individual who has already survived to time t"). https://doi.org/10.1038/sj.bjc.6601118 . Also GraphPad Software. GraphPad Prism 11 Statistics Guide (the guide the brief lists as Motulsky's); page "Cox regression models proportional hazards" (under the model "the hazard ratio for any two individuals in a population is constant at all times"). https://www.graphpad.com/guides/prism/latest/statistics/stat_cox_regression_models_prop_hazards.htm
- **Checked:** 16.11.2026, passage read
- **Notes:** Fully supported. "At any moment" is true when the hazard ratio is the same at all times, which is what the Cox model assumes (GraphPad) and what Harrell words as "When the hazard ratio is independent of t"; the pages cover that assumption. Harrell also warns that a hazard ratio is not a risk ratio: "twice as likely" applies to the moment-to-moment risk among patients still at risk, as the definition says, not to the overall chance of the event. Could not open Spruance et al. 2004 (hazard ratio in clinical trials); PubMed Central blocked automated access.

### `hedges-g`

**Hedges' g.** Cohen's d with a small correction. Cohen's d tends to come out a little too large in small samples, and Hedges' g removes that bias; in larger samples the two are almost the same.

- **Source:** Ben-Shachar MS, Lüdecke D, Makowski D, et al. effectsize: Indices of Effect Size (R package documentation), cohens_d() / hedges_g() help page; Description
- **URL:** <https://easystats.github.io/effectsize/reference/cohens_d.html>
- **Supports:** "Hedges' g provides a correction for small-sample bias (using the exact method) to Cohen's d."
- **Also:** Lakens D. Calculating and reporting effect sizes to facilitate cumulative science: a practical primer for t-tests and ANOVAs. Frontiers in Psychology, 2013;4:863; section "Cohen's d in between-subjects designs" (sample-based d overestimates the population effect, especially in small samples; the corrected effect size is Hedges' g): https://pmc.ncbi.nlm.nih.gov/articles/PMC3840331/ . Also Cochrane Handbook 6.5, section 6.5.1.2 (the SMD used in Cochrane reviews is Hedges' adjusted g). Original, not opened: Hedges LV, Olkin I. Statistical Methods for Meta-Analysis. Academic Press, 1985 (as cited by effectsize).
- **Checked:** 16.11.2026, passage read
- **Notes:** The direction of the bias (too large) is from Lakens: estimates based on sample averages "overestimate the true population effect". The site's wording (page 18: "Cohen's d shrunk slightly to correct for small samples") agrees.

### `histogram`

**Histogram.** A plot that shows the distribution of one variable. The range of values is cut into intervals of equal width, called bins, and a bar over each bin shows how many values fall in it.

- **Source:** NIST/SEMATECH e-Handbook of Statistical Methods. National Institute of Standards and Technology, 2012; section 1.3.3.14, Histogram
- **URL:** <https://www.itl.nist.gov/div898/handbook/eda/section3/histogra.htm>
- **Supports:** The range of the data is split into equal-sized bins and the number of points in each bin is counted; the plot summarizes the distribution of a univariate data set.
- **Also:** Çetinkaya-Rundel M, Hardin J. Introduction to Modern Statistics, 2nd ed. OpenIntro, 2024; section 5.3 ("Higher bars represent where the data are relatively more common"). https://openintro-ims.netlify.app/explore-numerical
- **Checked:** 16.11.2026, passage read

### `hodges-lehmann`

**Hodges-Lehmann estimate.** A rank-based estimate that goes with the Wilcoxon and Mann-Whitney tests. For one group (or one set of paired differences) it is the median of the averages of every pair of values, also called the pseudomedian, which equals the median when the distribution is symmetric. For two groups it is the median of the differences between every value in one group and every value in the other, not the difference between the two medians.

- **Source:** R Core Team. R documentation, stats::wilcox.test (R 4.6); Details
- **URL:** <https://stat.ethz.ch/R-manual/R-devel/library/stats/html/wilcox.test.html>
- **Supports:** The pseudomedian is the median of the distribution of (u + v)/2; it coincides with the median if the distribution is symmetric; the two-sample estimator is not the difference in medians.
- **Also:** Motulsky H. GraphPad Prism Statistics Guide, "Interpreting results: Mann-Whitney test" ("The Hodges-Lehmann estimate is the median of this set of differences" between each value in one group and each value in the other): https://www.graphpad.com/guides/prism/latest/statistics/how_the_mann-whitney_test_works.htm . DescTools documentation, HodgesLehmann() (one sample: the median of the data points and their pairwise (Walsh) averages): https://search.r-project.org/CRAN/refmans/DescTools/html/HodgesLehmann.html . Original, not opened (as cited by GraphPad and DescTools): Hodges JL, Lehmann EL. Estimates of location based on rank tests. Annals of Mathematical Statistics 1963;34:598–611.
- **Checked:** 16.11.2026, passage read
- **Notes:** Covers "pseudomedian" (page 5) and both the one-sample and two-sample estimates (pages 5, 6, 7). R's help defines the pseudomedian for the population distribution; that the sample estimate is the median of the pairwise averages is from DescTools (which says "Walsh averages" without defining the term). The site's wording agrees with the sources.

### `holm`

**Holm adjustment.** A way of adjusting p-values for multiple comparisons. The smallest p-value is multiplied by the number of tests, the next smallest by one fewer, and so on, and no adjusted p-value may be smaller than the one before it. It controls the family-wise error rate as the Bonferroni correction does but is never stricter, so it is preferred.

- **Source:** R Core Team. p.adjust {stats}: Adjust P-values for Multiple Comparisons. R documentation (stats version 4.6.0), Details, and the function's source code
- **URL:** <https://stat.ethz.ch/R-manual/R-devel/library/stats/html/p.adjust.html>
- **Supports:** "There seems no reason to use the unmodified Bonferroni correction because it is dominated by Holm's method, which is also valid under arbitrary assumptions." The code multiplies the sorted p-values by n, n-1, ..., 1 and takes a running maximum.
- **Also:** Original, not opened: Holm S. A simple sequentially rejective multiple test procedure. Scand J Stat 1979;6(2):65–70. Also: Aickin M, Gensler H. Adjusting for multiple testing when reporting research results: the Bonferroni vs Holm methods. Am J Public Health 1996;86(5):726–728; abstract (Holm's procedure "is uniformly better"), https://doi.org/10.2105/ajph.86.5.726; statsmodels multipletests documentation ("holm : step-down method using Bonferroni adjustments"), https://www.statsmodels.org/stable/generated/statsmodels.stats.multitest.multipletests.html
- **Checked:** 16.11.2026, passage read
- **Notes:** Holm's 1979 paper is paywalled (JSTOR) and was not opened; of Aickin & Gensler only the PubMed abstract was read. The step-by-step rule was checked against the body of R's p.adjust() (printed in this session: pmin(1, cummax((n + 1 - i) * p[o]))), which matches page 15's description and worked example.

### `hypothetical-value`

**Hypothetical value.** The fixed number that a one-sample test compares your group's mean, median or proportion with, such as a target or a published figure. It comes from outside your data, from theory or from earlier studies, and is not calculated from the data being tested. Also called the comparison value.

- **Source:** GraphPad Software. One sample t test. GraphPad QuickCalcs; Introduction and Overview
- **URL:** <https://www.graphpad.com/quickcalcs/onesamplet1/>
- **Supports:** "A one sample t test compares the mean with a hypothetical value", which comes from theory or previous data and "does not come from the data itself, but is an external value chosen for scientific reasons".
- **Also:** GraphPad Software. GraphPad Prism 11 Statistics Guide; "Experimental design tab" for one-sample tests (the t test compares a mean against "a hypothetical mean that you provide", the Wilcoxon signed rank test a median against "a hypothetical median"). https://www.graphpad.com/guides/prism/latest/statistics/stat_experimental-design-tab-1samplet.htm . Motulsky H. Choosing a statistical test (chapter 37 of Intuitive Biostatistics, 1995), table row "Compare one group to a hypothetical value" (one-sample t test; Wilcoxon test; chi-square or binomial test). https://www.graphpad.com/support/faqid/1790/
- **Checked:** 16.11.2026, passage read
- **Notes:** "Proportion" rests on Motulsky's table, which lists the chi-square or binomial test in this row. "Comparison value" is the site's own synonym (page 5, once); the sources do not use it. The site's English pages never say "reference value", so the entry does not list it. The target and published-figure examples are the site's (page 5); GraphPad's example is a blood pressure from a previous study.

### `independence`

**Independent observations.** Observations are independent when whatever makes one value higher or lower by chance affects that value only. Two hips of the same patient, or several scores from the same knee, are not independent, because what affects one is likely to affect the other. Most tests assume independent observations; when values are related, the analysis has to account for it.

- **Source:** Motulsky HJ. "The need for independent samples". GraphPad Statistics Guide (Prism 11). GraphPad Software; accessed 16.11.2026
- **URL:** <https://www.graphpad.com/guides/prism/latest/statistics/the_need_for_independent_samples.htm>
- **Supports:** Motulsky: "Data are independent when any random factor that causes a value to be too high or too low affects only that one value"; three measurements in one animal are not three independent values.
- **Also:** Motulsky HJ. "Analysis checklist: Mann-Whitney test". GraphPad Statistics Guide (Prism 11). GraphPad Software; accessed 16.11.2026 (the results only make sense when whatever caused a value to be too high or too low affects only that one value). https://www.graphpad.com/guides/prism/latest/statistics/stat_checklist_mannwhitney.htm
- **Checked:** 16.11.2026, passage read
- **Notes:** The hip and knee examples are this site's analog of Motulsky's example (repeated measurements in the same animal); they are not in the source. Does not cover 'independent variable' (a predictor), as the scope note asks. 'Independent tests' on page 15 is the same idea applied to tests. Altman and Bland's BMJ note 'Units of analysis' (1997) would be the classic second source but could not be opened (BMJ returns 403).

### `interaction`

**Interaction.** Two predictors interact when the effect of one on the outcome depends on the value of the other: for example, when the difference between two treatments is not the same at every visit. A model allows for this with an interaction term.

- **Source:** Penn State Eberly College of Science. STAT 501: Regression Methods (online course notes); Lesson 8, section 8.6 (Interaction effects)
- **URL:** <https://online.stat.psu.edu/stat501/Lesson08.html>
- **Supports:** Two predictors interact if the effect on the response variable of one predictor depends on the value of the other.
- **Also:** Harrell FE. Regression Modeling Strategies (course notes). hbiostat.org; chapter 2, section 2.3.2 (Interactions): the effect of X1 on Y depends on the level of X2, described by adding the product of the two to the model (https://hbiostat.org/rmsc/genreg.html)
- **Checked:** 16.11.2026, passage read
- **Notes:** The treatment by visit example is the site's own use (page 16); the source's example is age by treatment.

### `intercept`

**Intercept.** The value a regression model predicts for the outcome when every predictor is 0; for a categorical predictor, 0 means the reference group. It often has no practical meaning of its own, because a predictor such as BMI is never 0.

- **Source:** Penn State Eberly College of Science. STAT 501: Regression Methods (online course notes); Lesson 1, section 1.2 (What is the best fitting line?), and Lesson 5, section 5.3
- **URL:** <https://online.stat.psu.edu/stat501/Lesson01.html>
- **Supports:** The intercept is the predicted mean outcome when x = 0 if the data include x = 0, and otherwise is not meaningful; in multiple regression it is the mean outcome when all predictors are zero.
- **Also:** Reference group = all indicator variables zero: Penn State Eberly College of Science. STAT 501: Regression Methods (online course notes); Lesson 8, section 8.4 (https://online.stat.psu.edu/stat501/Lesson08.html). Schneider A, Hommel G, Blettner M. Linear regression analysis: part 14 of a series on evaluation of scientific publications. Dtsch Arztebl Int, 2010;107(44):776–782 calls it the y-intersect of the line (https://pmc.ncbi.nlm.nih.gov/articles/PMC2992018/)
- **Checked:** 16.11.2026, passage read
- **Notes:** 'Random intercept' is left to the random-effect entry. The BMI example is mine (the source uses a height of 0 inches). On page 16 the site uses 'the intercept' for the pre-op mean, which is the reference-group case.

### `iqr`

**Interquartile range (IQR).** The range that holds the middle half of the values, from the 25th percentile to the 75th.

- **Source:** Harrell FE. Glossary of Statistical Terms. Vanderbilt University School of Medicine, Department of Biostatistics, version of 26.04.2025, entry "inter-quartile range"
- **URL:** <https://hbiostat.org/glossary/>
- **Supports:** "The range between the outer quartiles (25th and 75th percentiles) ... a central interval containing half the sample."
- **Also:** NIST/SEMATECH e-Handbook of Statistical Methods; section 1.3.5.6, Measures of Scale. https://www.itl.nist.gov/div898/handbook/eda/section3/eda356.htm
- **Checked:** 16.11.2026, passage read
- **Notes:** Fully supported as the interval the site reports ("1 (0 to 2) days"). NIST, GraphPad ("Quartiles and the interquartile range") and Introduction to Modern Statistics 5.5 define the IQR as one number, the 75th percentile minus the 25th. Both uses are standard; the pages never print the single number, so no rewording is needed.

### `icc`

**Intraclass correlation coefficient (ICC).** A measure of reliability, usually between 0 and 1: the share of the total variation in the measurements that comes from real differences between patients, the rest being measurement error. Values close to 1 mean the measurement tells patients apart well. In a mixed model the same share describes how alike repeated measurements from one patient are.

- **Source:** Koo TK, Li MY. A Guideline of Selecting and Reporting Intraclass Correlation Coefficients for Reliability Research. J Chiropr Med 2016;15(2):155–163; introduction and Table 1
- **URL:** <https://pmc.ncbi.nlm.nih.gov/articles/PMC4913118/>
- **Supports:** "reliability represents a ratio of true variance over true variance plus error variance"; it "ranges between 0 and 1, with values closer to 1 representing stronger reliability"; the ICC is such an index.
- **Also:** Harrison XA, Donaldson L, Correa-Cano ME, et al. A brief introduction to mixed effects modelling and multi-model inference in ecology. PeerJ 2018;6:e4794 (the among-individual variance and the residual variance of a random-intercept model give an "intra-class correlation coefficient" that measures repeatability), https://pmc.ncbi.nlm.nih.gov/articles/PMC5970551/; de Vet HCW, Terwee CB, Knol DL, Bouter LM. When to use agreement versus reliability measures. J Clin Epidemiol 2006;59(10):1033–1039; abstract (reliability: whether persons "can be distinguished from each other, despite measurement errors"), https://doi.org/10.1016/j.jclinepi.2005.10.015
- **Checked:** 16.11.2026, passage read
- **Notes:** Covers both site senses: rater reliability (page 17) and the between-knee share of variance in a mixed model (page 16). Not in the definition, for length: there are several forms of ICC (Koo & Li count 10) and a report must say which; page 17 has a warning box on this. Koo & Li give the range as 0 to 1; software estimates and their CIs can fall below 0 (page 17's exercise 3 shows a CI from -0.04). The 2017 erratum to Koo & Li only corrects a formula in Table 3. Benchmark cut-offs are left to the page.

### `kaplan-meier`

**Kaplan-Meier method.** A way to estimate survival over time when some patients are censored, also called the product-limit method. At each time an event happens, it takes the share of the patients at risk who get past that time without the event, and multiplies these shares together. Each patient counts for as long as they were followed, and the curve steps down only at an event.

- **Source:** Clark TG, Bradburn MJ, Love SB, Altman DG. Survival analysis part I: basic concepts and first analyses. Br J Cancer 2003;89(2):232–238. doi:10.1038/sj.bjc.6601118; section "Kaplan–Meier survival estimate"
- **URL:** <https://pmc.ncbi.nlm.nih.gov/articles/PMC2394262/>
- **Supports:** Survival is estimated from censored and uncensored times by the KM (product-limit) method: interval survival probabilities are multiplied; the estimate is a step function changing only at events.
- **Also:** Original paper (not opened; bibliographic details checked in Crossref): Kaplan EL, Meier P. Nonparametric estimation from incomplete observations. J Am Stat Assoc 1958;53(282):457–481. https://doi.org/10.1080/01621459.1958.10501452
- **Checked:** 16.11.2026, passage read
- **Notes:** The source says each patient contributes "for as long as they are known to be event-free". Bland & Altman, Survival probabilities (the Kaplan-Meier method), BMJ 1998;317:1572, could not be opened and is not cited. Primary source read in full text.

### `kendalls-w`

**Kendall's W.** An effect size for the Friedman test: the Friedman statistic rescaled to run from 0 to 1. It measures how closely the patients agree in the order in which they rank the repeated measurements (for example the visits): 0 means no agreement and 1 means complete agreement.

- **Source:** Ben-Shachar MS, Lüdecke D, Makowski D, et al. effectsize: Indices of Effect Size (R package documentation), rank_epsilon_squared() / kendalls_w() help page; Details
- **URL:** <https://easystats.github.io/effectsize/reference/rank_epsilon_squared.html>
- **Supports:** Kendall's W accompanies the Friedman test and is also a measure of agreement of rankings between raters (blocks); values range from 0 to 1, larger meaning higher agreement.
- **Also:** Tomczak M, Tomczak E. The need to report effect size estimates revisited. An overview of some recommended measures of effect size. Trends in Sport Sciences, 2014;1(21):19–25; p. 24 (W is the Friedman statistic divided by N(k − 1); from 0, no relationship, to 1, a perfect relationship): https://www.wbc.poznan.pl/Content/325867/5_Trends_Vol21_2014_%20no1_20.pdf . pingouin.friedman() calls W "Kendall's coefficient of concordance": https://pingouin-stats.org/generated/pingouin.friedman.html . Original, not opened (as cited by effectsize): Kendall MG. Rank Correlation Methods. Griffin, 1948.
- **Checked:** 16.11.2026, passage read
- **Notes:** The end points are paraphrased: Tomczak says 0 indicates "no relationship" and 1 "a perfect relationship"; effectsize says larger values mean "higher agreement between raters". The site's formula (Friedman statistic ÷ n(k − 1), page 9) matches Tomczak. No cut-offs given; the page quotes 0.1/0.3/0.5, which neither source gives.

### `kruskal-wallis-test`

**Kruskal-Wallis test.** A rank-based (nonparametric) test that compares three or more unpaired groups. It ranks all the values together, ignoring the groups, and asks whether the groups' ranks differ more than chance would explain. It extends the Mann-Whitney test to more than two groups.

- **Source:** GraphPad Software. GraphPad Prism 11 Statistics Guide; page 'Interpreting results: Kruskal-Wallis test'
- **URL:** <https://www.graphpad.com/guides/prism/latest/statistics/how_the_kruskal-wallis_test_works.htm>
- **Supports:** The Kruskal-Wallis test is a nonparametric test that compares three or more unmatched groups: all values are ranked together and the discrepancies among the rank sums are combined into one statistic.
- **Also:** Bewick V, Cheek L, Ball J. Statistics review 10: Further nonparametric methods. Crit Care 2004;8(3):196-199. doi:10.1186/cc2857; section 'Kruskal-Wallis test' ('an extension of the Mann-Whitney test for more than two independent samples'), https://pmc.ncbi.nlm.nih.gov/articles/PMC468904/ ; original paper as cited in the SciPy documentation for scipy.stats.kruskal, not opened: Kruskal WH, Wallis WW. Use of ranks in one-criterion variance analysis. J Am Stat Assoc 1952;47(260):583-621
- **Checked:** 16.11.2026, passage read
- **Notes:** The author initials of the 1952 paper are given as SciPy prints them (W. W. Wallis) and were not checked against the paper. The two sources state the null hypothesis differently: the Critical Care review and SciPy say equal population medians, while GraphPad says the test compares mean ranks and is a test of medians only if the distributions have the same shape. The definition follows GraphPad and the site's wording (whether values in some groups tend to be larger).

### `least-squares`

**Least squares.** The usual way to fit a regression line or curve: choose the one for which the sum of the squared residuals is as small as possible. For linear regression a formula gives the answer directly (ordinary least squares); for nonlinear regression software has to search for it in repeated steps (nonlinear least squares).

- **Source:** Penn State Eberly College of Science. STAT 501: Regression Methods (online course notes); Lesson 1, section 1.2 (What is the best fitting line?)
- **URL:** <https://online.stat.psu.edu/stat501/Lesson01.html>
- **Supports:** The least squares criterion says to minimize the sum of the squared prediction errors; formulas give the intercept and slope of the line that does so.
- **Also:** NIST/SEMATECH e-Handbook of Statistical Methods. National Institute of Standards and Technology; section 4.1.4.2, Nonlinear least squares regression: linear least squares estimates can always be obtained analytically, nonlinear ones need iterative procedures and starting values (https://www.itl.nist.gov/div898/handbook/pmd/section1/pmd142.htm). Harrell FE. Glossary of Statistical Terms. Vanderbilt University, 26.04.2025; entries 'least squares estimate' and 'linear regression model' (OLS) (https://hbiostat.org/glossary/)
- **Checked:** 16.11.2026, passage read

### `levene-test`

**Levene's test.** A test of whether two or more groups have equal variances. A small p-value is evidence that the variances differ.

- **Source:** NIST/SEMATECH e-Handbook of Statistical Methods. National Institute of Standards and Technology; section 1.3.5.10, "Levene Test for Equality of Variances"; accessed 16.11.2026
- **URL:** <https://www.itl.nist.gov/div898/handbook/eda/section3/eda35a.htm>
- **Supports:** NIST: "Levene's test (Levene 1960) is used to test if k samples have equal variances"; the alternative hypothesis is that at least one pair of variances differs.
- **Also:** Original, as listed in the NIST Handbook's references (section 1.4.3) but not opened: Levene H. In: Olkin I, et al., editors. Contributions to Probability and Statistics: Essays in Honor of Harold Hotelling. Stanford University Press, 1960; pages 278 to 292. https://www.itl.nist.gov/div898/handbook/eda/section4/eda43.htm
- **Checked:** 16.11.2026, passage read
- **Notes:** NIST presents the test as a way to verify the equal-variance assumption; the site (page 6) advises against using it to choose between Student's and Welch's t test, in line with Motulsky's Welch page. The definition takes no side. NIST's reference list gives the 1960 chapter without its title, so the title is left out here.

### `likelihood-ratio-test`

**Likelihood ratio test.** A test that compares two models, one with and one without the predictors being tested, by how likely each makes the observed data. A small p-value says the fuller model makes the data more likely than chance alone would explain. In logistic regression its test statistic is the drop in deviance between the two models.

- **Source:** Penn State Eberly College of Science. STAT 501: Regression Methods (online course notes); Lesson 13, section 13.2, 'Likelihood ratio (or deviance) test'
- **URL:** <https://online.stat.psu.edu/stat501/Lesson13.html>
- **Supports:** The statistic compares the log-likelihood of the full model with that of the reduced model set by the null hypothesis, has a chi-square distribution, and equals deviance (reduced) minus deviance (full).
- **Also:** Harrell FE. Regression Modeling Strategies (course notes). hbiostat.org; chapter 9 (Overview of maximum likelihood estimation, by Chiara Di Gravio), sections 9.2 and 9.3: LR = -2 log(L at H0 / L at MLE); 'LR is the best statistic followed by S and W' (https://hbiostat.org/rmsc/mle.html)
- **Checked:** 16.11.2026, passage read
- **Notes:** Page 14's remark that the likelihood ratio test is the most reliable of the three agrees with Harrell.

### `likert-scale`

**Likert scale.** A survey question answered by picking one of a few ordered choices, typically 5 or 7, classically to say how much one agrees or disagrees with a statement. The answers are ordinal: they can be ranked, but the distance from one choice to the next is not necessarily equal.

- **Source:** Sullivan GM, Artino AR Jr. Analyzing and interpreting data from Likert-type scales. J Grad Med Educ 2013;5(4):541 to 542
- **URL:** <https://pmc.ncbi.nlm.nih.gov/articles/PMC3886444/>
- **Supports:** "a 5- or 7-point ordinal scale used by respondents to rate the degree to which they agree or disagree with a statement"; responses can be ranked but distances are not measurable.
- **Also:** Not opened (original method): Likert R. A technique for the measurement of attitudes. Archives of Psychology 1932;22(140):1 to 55.
- **Checked:** 16.11.2026, passage read
- **Notes:** SITE DISAGREES WITH THIS SOURCE ON ANALYSIS. Page 3 (en/foundations/03-distributions.qmd, section #ordinal) says: "Never compute a t test on Likert scores, however many patients you have." Sullivan & Artino's bottom line is the opposite: "parametric tests can be used to analyze Likert scale responses" (citing Norman 2010), while agreeing that medians and frequencies describe such data better than means. The stricter view the site takes is also in the literature (Jamieson 2004, cited by the same paper, not opened). The definition stays out of the dispute; Doc may want to soften page 3 or cite the stricter source. Sullivan & Artino also note that several Likert-type items are often summed into a scale score. The wording "a few ordered choices" is kept broad because the site's example is a satisfaction rating from 1 to 5, not agreement; the source likewise mentions frequency-response versions (always, often, sometimes).

### `linear-regression`

**Linear regression.** A model that describes a continuous outcome as a straight-line function of one predictor (simple linear regression) or of several predictors added together (multiple linear regression). It gives a coefficient for each predictor and is fitted by least squares.

- **Source:** Penn State Eberly College of Science. STAT 501: Regression Methods (online course notes); Lesson 1, section 1.1 (What is simple linear regression?)
- **URL:** <https://online.stat.psu.edu/stat501/Lesson01.html>
- **Supports:** Simple linear regression studies one predictor variable; multiple linear regression studies two or more.
- **Also:** Harrell FE. Glossary of Statistical Terms. Vanderbilt University, 26.04.2025; entry 'linear regression model': also called ordinary least squares, regression for a continuous dependent variable (https://hbiostat.org/glossary/). Schneider A, Hommel G, Blettner M. Linear regression analysis: part 14 of a series on evaluation of scientific publications. Dtsch Arztebl Int, 2010;107(44):776–782: Y = a + b1 X1 + b2 X2 + ..., one regression coefficient for each independent variable (https://pmc.ncbi.nlm.nih.gov/articles/PMC2992018/)
- **Checked:** 16.11.2026, passage read
- **Notes:** Also meant for 'regression' where a page means linear regression.

### `linear-relationship`

**Linear relationship.** A relationship in which the outcome changes, on average, by the same amount for each one-unit increase in the predictor, so the points on a scatter plot follow a straight line with some scatter around it. Linear regression and the Pearson correlation measure only this kind of relationship: they can show nothing even when two variables are closely related along a curve.

- **Source:** Penn State Eberly College of Science. STAT 501: Regression Methods (online course notes); Lesson 1, objectives and sections 1.1, 1.2 and 1.6, and Lesson 4, section 4.1
- **URL:** <https://online.stat.psu.edu/stat501/Lesson01.html>
- **Supports:** R-squared and r are measures of linear association and can be 0 even if there is a perfect nonlinear association; linearity means the mean of the response is a linear function of x.
- **Also:** Schneider A, Hommel G, Blettner M. Linear regression analysis: part 14 of a series on evaluation of scientific publications. Dtsch Arztebl Int, 2010;107(44):776–782: the linear regression model describes the dependent variable with a straight line (https://pmc.ncbi.nlm.nih.gov/articles/PMC2992018/)
- **Checked:** 16.11.2026, passage read
- **Notes:** Covers 'straight-line relationship' and 'linearity' (the assumption checked on pages 12 and 14).

### `log-log-interval`

**Log-log confidence interval.** A confidence interval for a Kaplan-Meier survival probability that is worked out on a transformed scale (the logarithm of minus the logarithm of the survival probability) and then converted back. Because of the transformation, the limits cannot fall below 0% or above 100%, as the plain interval of the estimate plus and minus about 2 standard errors can. In R it is conf.type = "log-log" in survfit(); lifelines uses it for its Kaplan-Meier intervals.

- **Source:** Therneau TM. R documentation, survival::survfit.formula (survival 3.8-6); argument conf.type
- **URL:** <https://stat.ethz.ch/R-manual/R-devel/library/survival/html/survfit.formula.html>
- **Supports:** "The log-log option bases the intervals on the log hazard or log(-log(survival))".
- **Also:** SAS Institute. SAS/STAT 15.1 User's Guide, The LIFETEST Procedure, "Survivor Function" under pointwise confidence limits (untransformed limits "might include impossible values outside the range [0,1]"; a transformation with unrestricted range, such as the log-log function, avoids this): https://support.sas.com/documentation/onlinedoc/stat/151/lifetest.pdf . Therneau TM. A package for survival analysis in R (vignette) (direct intervals "do not behave well, particularly near 0 and 1"): https://cran.r-project.org/web/packages/survival/vignettes/survival.pdf . lifelines documentation, KaplanMeierFitter ("Uses Greenwood's Exponential formula (\"log-log\" in R)"): https://lifelines.readthedocs.io/en/latest/fitters/univariate/KaplanMeierFitter.html . Original, not opened (as cited by SAS): Kalbfleisch JD, Prentice RL. The Statistical Analysis of Failure Time Data. Wiley, 1980.
- **Checked:** 16.11.2026, passage read
- **Notes:** The claim that the limits stay within 0% to 100% rests on the SAS guide, which says so for transformations whose range is unrestricted and names log-log among them; R's own help and vignette describe the transformation but do not state the bound. SAS is not software the site uses; it is cited as official documentation of the method. The site's wording (page 4: "Log-log keeps the CI between 0% and 100%") agrees.

### `log-rank-test`

**Log-rank test.** A test of whether the survival curves of two or more groups differ, also called the Mantel-Cox test. At each time an event happens, it works out how many events each group would be expected to have if the groups did not differ, then compares the totals observed and expected. For two groups, R and lifelines compute it as the Mantel-Haenszel calculation on the 2 × 2 table of each event time, so there it is the same test as the Mantel-Haenszel test for survival data; one statistics guide calls the two nearly identical, differing only in how they handle events at the same time. It gives a p-value but no effect size.

- **Source:** Clark TG, Bradburn MJ, Love SB, Altman DG. Survival analysis part I: basic concepts and first analyses. Br J Cancer 2003;89(2):232–238. doi:10.1038/sj.bjc.6601118; section "Nonparametric tests comparing survival"
- **URL:** <https://pmc.ncbi.nlm.nih.gov/articles/PMC2394262/>
- **Supports:** At each event time the logrank test calculates the events expected in each group if the groups did not differ, sums them, and compares observed with expected.
- **Also:** Bland JM, Altman DG. The logrank test. BMJ 2004;328(7447):1073. doi:10.1136/bmj.328.7447.1073, https://pmc.ncbi.nlm.nih.gov/articles/PMC403858/ (null hypothesis of no difference in the probability of an event; "cannot provide an estimate of the size of the difference between the groups"). Names: GraphPad, FAQ 1079, How do the three methods compare to survival curves (log-rank, Mantel-Haenszel, Gehan-Breslow-Wilcoxon) differ?, https://www.graphpad.com/support/faq/how-do-the-three-methods-compare-to-survival-curves-log-rank-mantel-haenszel-gehan-wilcoxon-differ/ and GraphPad Prism 5 Help, Interpreting results: Comparing two survival curves, https://www.graphpad.com/guides/prism/5/user-guide/curve_comparison.htm
- **Checked:** 16.11.2026, passage read; 20.11.2026, computation on `data/cohort.csv` (R 4.6.0, survival 3.8.12, lifelines 0.30.3): implants A and C, revision as the event. `survdiff(Surv(followup_years, revised) ~ implant)` gives chi-square 20.53461818; `mantelhaen.test(tables, correct = FALSE)` on the 59 2 × 2 tables (implant by revised or not, among the patients at risk) at the 59 distinct revision times, 4 of them tied, gives 20.53461818, difference 0; lifelines' `logrank_test()` gives 20.534618183417702.
- **Notes:** Names: GraphPad calls it "the log-rank (Mantel-Cox) test" and says the Mantel-Haenszel method is "nearly identical", the two differing "only in how they deal with two subjects with the same time of death". The site (pages 6 and 13) says it is "the same test" as Mantel-Haenszel. Reworded on 20.11.2026 (content review C8) so that both facts stand: in R and lifelines, for two groups, the log-rank statistic is the Mantel-Haenszel calculation on the event-time 2 × 2 tables (computation above, ties included), and GraphPad, the recorded source, calls the two nearly identical. The definition claims nothing about other programs. Only two groups were checked, so the sentence says "for two groups". The Bland & Altman note was read through the fetch tool's short quotes only, not as full text. The sources spell it "logrank"; the label keeps the site's "log-rank". Primary source read in full text.

### `logarithm`

**Logarithm (log scale).** The power to which a base must be raised to give a number: the log to base 10 of 100 is 2. In statistics, log usually means the natural log, whose base is e, about 2.718. Equal steps on a log scale mean equal ratios, which pulls in a long right tail, so skewed data and ratios are often analyzed there; zero and negative numbers have no logarithm.

- **Source:** Bland M. Clinical Biostatistics: Logarithms (background notes for the MSc course). University of York, 2006
- **URL:** <https://www-users.york.ac.uk/~mb55/msc/clinbio/background/logarithms.htm>
- **Supports:** 10 to the power 2 is 100, so 2 is the log of 100 to base 10; log in statistics is the natural log (e = 2.718...); equal distances mean equal ratios; log of 0 "does not exist".
- **Also:** Not opened: Bland JM, Altman DG. Statistics Notes: Logarithms. BMJ 1996;312:700, https://doi.org/10.1136/bmj.312.7032.700 ; opened: Çetinkaya-Rundel M, Hardin J. Introduction to Modern Statistics, 2nd ed. OpenIntro, 2024, section 5.7 (a log transformation makes strongly right-skewed data more symmetric). https://openintro-ims.netlify.app/explore-numerical ; Higgins JPT, Li T, Deeks JJ (eds). Chapter 6: Choosing effect measures and computing estimates of effect. In: Cochrane Handbook for Systematic Reviews of Interventions, version 6.5. Cochrane, 2024, section 6.1.2.1 (ratio measures are analyzed on the natural log scale, that is log base e, written ln). https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-06
- **Checked:** 16.11.2026, passage read
- **Notes:** The BMJ Statistics Note is the citation of record, but bmj.com refused the request and PubMed Central holds only a scanned page, so I could not read it. Every claim was instead checked against Martin Bland's own course notes on the University of York site (same author, same content, opened and read in full), plus IMS and Cochrane. Whether an author's course notes meet the brief's source list is Doc's call; if not, treat this entry as verified against IMS and Cochrane only for the skew and ratio claims, and the base/power, natural log and log(0) claims as resting on Bland's notes. Consistent with the site (page 3: "log(0) doesn't exist"). To undo a natural log, software uses exp(), as page 11 does.

### `logistic-regression`

**Logistic regression.** A regression model for a yes/no outcome, such as revised or not revised. It estimates the probability of the outcome from one or more predictors and gives each predictor's effect as an odds ratio.

- **Source:** Harrell FE. Glossary of Statistical Terms. Vanderbilt University, 26.04.2025; entry 'logistic regression model'
- **URL:** <https://hbiostat.org/glossary/>
- **Supports:** The binary logistic model predicts the probability of an event as a function of several variables; logistic models are used to estimate adjusted odds ratios as well as probabilities.
- **Also:** Penn State Eberly College of Science. STAT 501: Regression Methods (online course notes); Lesson 13, section 13.2: binary logistic regression is used when the response has two possible outcomes; the odds are multiplied by exp(coefficient) for every one-unit increase (https://online.stat.psu.edu/stat501/Lesson13.html)
- **Checked:** 16.11.2026, passage read
- **Notes:** Defines binary logistic regression, the only kind on the site; the sources also describe ordinal and nominal versions. 'Simple' and 'multiple' logistic regression differ only in the number of predictors.

### `long-format`

**Long and wide format.** Two ways to lay out repeated measurements. Wide format has one row per patient, with each repeated measurement in a column of its own; long format has one row per measurement, so a patient with several visits has several rows. Reshaping turns one layout into the other.

- **Source:** R Core Team. R documentation: reshape {stats}, Reshape Grouped Data; Description
- **URL:** <https://stat.ethz.ch/R-manual/R-devel/library/stats/html/reshape.html>
- **Supports:** "'wide' format (with repeated measurements in separate columns of the same row) and 'long' format (with the repeated measurements in separate rows)"
- **Also:** pandas development team. pandas user guide: Reshaping and pivot tables (wide: typically one row for each subject; long: multiple rows for each subject). https://pandas.pydata.org/docs/user_guide/reshaping.html
- **Checked:** 16.11.2026, passage read
- **Notes:** The row need not be a patient: page 7 has one row per patient (wide), page 17 one row per knee, rater and session (long). In the tidyr pivoting vignette Wickham writes that it makes no sense to call a dataset "long form", because length is relative; the site, R's reshape() and pandas all use the terms, so the entry keeps them. Do not link "wide" where it describes a CI.

### `lowess`

**LOWESS (LOESS).** A smoothing method that draws a curve through a scatter plot without assuming any formula for its shape. For each point it fits a small regression to the nearby points only, giving the closest ones the most weight, and joins the results into a smooth curve.

- **Source:** NIST/SEMATECH e-Handbook of Statistical Methods. National Institute of Standards and Technology; section 4.1.4.4, LOESS (aka LOWESS)
- **URL:** <https://www.itl.nist.gov/div898/handbook/pmd/section1/pmd144.htm>
- **Supports:** At each point a low-degree polynomial is fitted to the nearby subset of the data by weighted least squares, giving more weight to near points; no global function has to be specified.
- **Also:** R Core Team. R: Scatter Plot Smoothing (help page lowess, stats package) (https://stat.ethz.ch/R-manual/R-devel/library/stats/html/lowess.html). statsmodels documentation, lowess: 'LOWESS (Locally Weighted Scatterplot Smoothing)' (https://www.statsmodels.org/stable/generated/statsmodels.nonparametric.smoothers_lowess.lowess.html). Original method: Cleveland WS. Robust locally weighted regression and smoothing scatterplots. J Am Stat Assoc, 1979;74(368):829–836 (reference as printed on the R help page; the paper itself was not opened)
- **Checked:** 16.11.2026, passage read
- **Notes:** Also meant for 'smoother' and 'smoothed trend'. Page 11 expands LOWESS as 'locally weighted smoothing'; statsmodels spells it 'Locally Weighted Scatterplot Smoothing' and NIST describes it as locally weighted polynomial regression. A shortening, not an error. NIST treats LOESS and LOWESS as one method; in R, loess() is a newer function than lowess() with different defaults (lowess help page). Cleveland 1979 itself was not opened.

### `main-effect`

**Main effect.** The effect of one variable in a model on its own, averaged over the levels of the other variables: for example, the difference between two treatment arms averaged over all visits. When there is an interaction, the effect of one variable depends on the level of the other, so a main effect on its own can mislead.

- **Source:** GraphPad Software. GraphPad Prism 11 Statistics Guide; "ANOVA Key Concepts"
- **URL:** <https://www.graphpad.com/guides/prism/latest/statistics/stat_anova_key_concepts.htm>
- **Supports:** "Main effects: compares groups within a single specified factor, averaged across all other factors"; with an interaction, "the effect of one factor depends on the value (or level) of another factor".
- **Also:** Penn State Eberly College of Science. STAT 502: Analysis of Variance and Design of Experiments; Lesson 5 Multi-Factor ANOVA, section 5.1 ("The main effect of factor A is the effect of A on the response ignoring the effect of all other factors"; if the interaction is significant, "do NOT interpret the main effects individually"). https://online.stat.psu.edu/stat502/Lesson05 . NIST/SEMATECH e-Handbook of Statistical Methods, section 5.7 A Glossary of DOE Terminology, entry "Effect" ("The effect of a single factor is also called a main effect"). https://www.itl.nist.gov/div898/handbook/pri/section7/pri7.htm
- **Checked:** 16.11.2026, passage read
- **Notes:** All three read in this session (Penn State as the downloaded page; its server certificate fails verification in the fetch tool). The sources say "factor"; the entry says "variable" because "factor" is not a glossary term. The arm and visit example is the site's (page 16), where "the main effect of arm alone only compares the average levels". Penn State states the rule more strongly than the entry ("of no consequence" when the interaction is significant).

### `mann-whitney-test`

**Mann-Whitney test.** A rank-based (nonparametric) test that compares two unpaired groups. It asks whether values in one group tend to be larger than in the other: if the groups did not differ, a patient picked at random from one group would have the higher value half the time. Also called the Wilcoxon rank-sum test.

- **Source:** GraphPad Software. GraphPad Prism 11 Statistics Guide; page 'Interpreting results: Mann-Whitney test'
- **URL:** <https://www.graphpad.com/guides/prism/latest/statistics/how_the_mann-whitney_test_works.htm>
- **Supports:** The Mann-Whitney test, also called the Wilcoxon rank sum test, is a nonparametric test that compares two unpaired groups by ranking all values; under the null a random value from one population exceeds one from the other with 50% probability.
- **Also:** Whitley E, Ball J. Statistics review 6: Nonparametric methods. Crit Care 2002;6(6):509-513. doi:10.1186/cc1820; section 'The Wilcoxon rank sum or Mann-Whitney test', https://pmc.ncbi.nlm.nih.gov/articles/PMC153434/ ; original paper as cited in the SciPy documentation for scipy.stats.mannwhitneyu, not opened: Mann HB, Whitney DR. On a test of whether one of two random variables is stochastically larger than the other. Ann Math Stat 1947;18:50-60
- **Checked:** 16.11.2026, passage read
- **Notes:** GraphPad has a separate page, 'The Mann-Whitney test doesn't really compare medians' (read): it compares mean ranks, and is a test of medians only if both distributions have the same shape. The definition therefore avoids 'compares medians', as the site does.

### `matched`

**Matched.** Chosen to resemble each other: each patient in one group is picked to be like a patient in the other in characteristics such as age and sex. Groups are also called matched when the same patients are measured several times. Matched data need methods for matched sets, not methods for independent groups.

- **Source:** GraphPad Software (Motulsky H). GraphPad Prism 11 Statistics Guide; Experimental design tab: One-way ANOVA
- **URL:** <https://www.graphpad.com/guides/prism/latest/statistics/stat_choosing_test_one-way_anova.htm>
- **Supports:** Data are matched when each subject is measured several times or subjects are recruited as matched groups (age, disease severity); then choose a repeated-measures test.
- **Also:** Cochrane Community. Glossary. Cochrane; archived copy of community.cochrane.org/glossary (Internet Archive snapshot of 01.07.2019); entries "Matching" (controls chosen for each case by variables such as age and sex) and "Paired design". https://web.archive.org/web/20190701142620/https://community.cochrane.org/glossary . Vandenbroucke JP, von Elm E, Altman DG, et al. Strengthening the Reporting of Observational Studies in Epidemiology (STROBE): Explanation and Elaboration. PLoS Med, 2007;4(10):e297; Box 2 and item 12d. https://doi.org/10.1371/journal.pmed.0040297
- **Checked:** 16.11.2026, passage read
- **Notes:** Cochrane has retired its glossary page (community.cochrane.org/glossary now redirects to resources.cochrane.org, which points readers to archive.org), so the entry was read in the Internet Archive snapshot of 01.07.2019. Covers both senses on the site: page 3 (patients chosen to resemble each other) and the decision table's "matched groups", which include repeated visits of the same patients. One doubt about the last sentence and about page 3's "Treat matched sets like pairs": it holds for the site's matched cohorts (Haukoos and Lewis, JAMA 2015: compare "using methods that account for the paired nature of the data"), but for matched case-control studies Pearce (BMJ 2016;352:i969, abstract read) says a matched design does not always need a matched analysis; adjusting for the matching factors can be enough. Bland JM, Altman DG. Matching. BMJ 1994;309:1128 could not be opened (scanned PDF), so it is not cited.

### `maximum-likelihood`

**Maximum likelihood.** A method for estimating a model's numbers: software picks the values under which the observed data were most likely to occur. The likelihood is that probability of the observed data, which changes with the values tried. It is the standard method for logistic and Cox regression.

- **Source:** Harrell FE. Glossary of Statistical Terms. Vanderbilt University, 26.04.2025; entries 'maximum likelihood estimate' and 'likelihood function'
- **URL:** <https://hbiostat.org/glossary/>
- **Supports:** A maximum likelihood estimate is the value of a parameter making the data most likely to have been observed; it is the standard method for logistic and Cox regression.
- **Also:** Penn State Eberly College of Science. STAT 501: Regression Methods (online course notes); Lesson 13, section 13.2: maximizing the likelihood has no closed-form solution, so an iterative technique finds the estimates (https://online.stat.psu.edu/stat501/Lesson13.html)
- **Checked:** 16.11.2026, passage read
- **Notes:** Covers plain 'likelihood' too. The likelihood ratio test and REML have their own entries. For Cox regression the quantity maximized is the partial likelihood (R help coxph.control); Harrell's glossary does not make that distinction and neither does the definition.

### `mcnemar-test`

**McNemar's test.** A test for a yes/no outcome measured twice in the same patients, or once in each member of a matched pair. It uses only the discordant pairs, those whose two answers differ, and asks whether changes in one direction are as common as changes in the other.

- **Source:** Bewick V, Cheek L, Ball J. Statistics review 8: Qualitative data - tests of association. Crit Care 2004;8(1):46-53. doi:10.1186/cc2428; sections 'Matched samples' and 'McNemar's test'
- **URL:** <https://pmc.ncbi.nlm.nih.gov/articles/PMC420070/>
- **Supports:** For matched pairs with a categorical outcome, the null hypothesis implies that the two kinds of discordant pairs are equally frequent; the statistic is built from those two counts only.
- **Also:** GraphPad Software. GraphPad Prism 11 Statistics Guide; page 'McNemar's test' (pairs in which both members agree 'provide no information'; the binomial test on the two discordant counts is the exact version), https://www.graphpad.com/guides/prism/latest/statistics/stat_how_to_mcnemars_test.htm ; statsmodels documentation, statsmodels.stats.contingency_tables.mcnemar, https://www.statsmodels.org/stable/generated/statsmodels.stats.contingency_tables.mcnemar.html
- **Checked:** 16.11.2026, passage read
- **Notes:** The site's rule of thumb of about 10 discordant pairs for the chi-square version was not found in these sources and is not part of the definition.

### `mean`

**Mean.** The average: add up the values and divide by how many there are.

- **Source:** NIST/SEMATECH e-Handbook of Statistical Methods; section 1.3.5.1, Measures of Location
- **URL:** <https://www.itl.nist.gov/div898/handbook/eda/section3/eda351.htm>
- **Supports:** "the mean is the sum of the data points divided by the number of data points"; it is the value "most commonly referred to as the average".
- **Also:** Harrell FE. Glossary of Statistical Terms. Vanderbilt University School of Medicine, Department of Biostatistics, version of 26.04.2025, entry "mean" ("Arithmetic average, i.e., the sum of all the values divided by the number of observations"). https://hbiostat.org/glossary/
- **Checked:** 16.11.2026, passage read
- **Notes:** Fully supported.

### `mean-difference`

**Mean difference.** The mean of one group minus the mean of the other, in the units of the measurement, such as points or degrees. It says how much higher or lower one group is on average. For paired data it is the mean of the differences within the pairs, and in a one-sample test it is the group's mean minus the hypothetical value.

- **Source:** Higgins JP, Li T, Deeks JJ (editors). Chapter 6: Choosing effect measures and computing estimates of effect [last updated August 2023]. In: Cochrane Handbook for Systematic Reviews of Interventions version 6.5. Cochrane, 2024; section 6.5.1.1
- **URL:** <https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-06>
- **Supports:** The mean difference ("more correctly, 'difference in means'") "measures the absolute difference between the mean value in two groups" and estimates the average change in the outcome.
- **Also:** GraphPad Software. GraphPad Prism 11 Statistics Guide; "Interpreting results: Paired t" (the paired t test works with "the mean of these differences") and "Interpreting results: One-sample t test" (CI "for the difference between the actual and hypothetical mean"). https://www.graphpad.com/guides/prism/latest/statistics/interpretingpairedttests.htm
- **Checked:** 16.11.2026, passage read
- **Notes:** The site uses the term in three settings (two groups on page 6, pairs on pages 7 and 17, one sample against a fixed number on page 5), so the entry covers all three. Cochrane defines it for the two groups of a randomized trial and notes that "difference in means" is the more correct name; the site uses both. "In the units of the measurement" paraphrases Cochrane's "absolute difference" (as opposed to the standardized mean difference).

### `measurement-error`

**Measurement error.** The difference between a measured value and the true value. Because of it, repeated readings of the same knee differ a little from each other although the knee has not changed. It can be a steady shift (bias) or random scatter; reliability statistics such as the ICC compare it with the real differences between patients.

- **Source:** NIST/SEMATECH. e-Handbook of Statistical Methods. National Institute of Standards and Technology, 2012; sections 2.1.1.3 Bias and Accuracy and 2.1.1.4 Variability
- **URL:** <https://www.itl.nist.gov/div898/handbook/mpc/section1/mpc114.htm>
- **Supports:** Bias is the difference between the average of measurements on the same object and its true value; variability is the tendency "to produce slightly different measurements on the same test item".
- **Also:** Koo TK, Li MY. A Guideline of Selecting and Reporting Intraclass Correlation Coefficients for Reliability Research. Journal of Chiropractic Medicine, 2016 ("reliability represents a ratio of true variance over true variance plus error variance"; its Table 1 lists each subject's error as measured minus true value). https://doi.org/10.1016/j.jcm.2016.02.012
- **Checked:** 16.11.2026, passage read
- **Notes:** NIST read as page text (bias: https://www.itl.nist.gov/div898/handbook/mpc/section1/mpc113.htm). NIST never uses the two words "measurement error" as a defined term; the definition combines its bias and variability, and Koo and Li's table supplies "measured minus true". Koo and Li read through the PubMed Central page (PMC4913118) with a fetch tool that paraphrased Table 1, so that detail is less firmly checked than the quoted sentence. Page 17 uses the term in the narrower sense of random error: what is left of the spread of the readings after real differences between knees and the steady difference between raters are taken out. The natural source, Bland JM, Altman DG. Measurement error. BMJ 1996;313:744, could not be opened (scanned article, no text on PubMed Central; bmj.com refuses the fetch tool).

### `median`

**Median.** The middle value when the values are sorted: half lie below it and half above.

- **Source:** NIST/SEMATECH e-Handbook of Statistical Methods; section 1.3.5.1, Measures of Location
- **URL:** <https://www.itl.nist.gov/div898/handbook/eda/section3/eda351.htm>
- **Supports:** "the median is the value of the point which has half the data smaller than that point and half the data larger than that point".
- **Also:** GraphPad Software. GraphPad Prism 11 Statistics Guide (the guide the brief lists as Motulsky's); page "Interpreting results: Quartiles and the interquartile range" ("Half the values are higher; half are lower. Rank the values from low to high."). https://www.graphpad.com/guides/prism/latest/statistics/stat_percentiles_and_the_median.htm . Also Harrell FE. Glossary of Statistical Terms. Vanderbilt University School of Medicine, Department of Biostatistics, version of 26.04.2025, entry "median". https://hbiostat.org/glossary/
- **Checked:** 16.11.2026, passage read
- **Notes:** Fully supported. Detail left out: with an even number of values there is no single middle value, and NIST, GraphPad and Introduction to Modern Statistics take the average of the two middle values. The latter still sums the median up as "the number in the middle".

### `mcid`

**Minimal clinically important difference (MCID).** The smallest change in a score, such as a PROM, that patients perceive as beneficial. A difference can be statistically significant and still be smaller than the MCID. Published MCIDs for the same score differ with the patients studied and the method used to work them out.

- **Source:** Maltenfort M, Díaz-Ledezma C. Statistics in Brief: Minimum clinically important difference — availability of reliable estimates. Clinical Orthopaedics and Related Research, 2017;475(4):933–946
- **URL:** <https://pmc.ncbi.nlm.nih.gov/articles/PMC5339150/>
- **Supports:** Quoting Jaeschke: "the smallest difference in score in the domain of interest which patients perceive as beneficial"; estimates differ with patients' characteristics and with the calculation method.
- **Also:** Leopold SS, Porcher R. Editorial: The minimum clinically important difference — the least we can do. Clinical Orthopaedics and Related Research, 2017;475(4):929–932 (a tiny p-value attached to an effect smaller than the MCID is a difference a patient is unlikely to call important): https://pmc.ncbi.nlm.nih.gov/articles/PMC5339159/ . Original, abstract only read on PubMed: Jaeschke R, Singer J, Guyatt GH. Measurement of health status: ascertaining the minimal clinically important difference. Controlled Clinical Trials 1989;10(4):407–415: https://doi.org/10.1016/0197-2456(89)90005-6
- **Checked:** 16.11.2026, passage read
- **Notes:** PMC blocked a direct download, so both CORR articles were read through the fetch tool's answers to targeted questions (short quotes), not as full text; treat the wording of the support quote as checked but the surrounding context as less thoroughly read than for the other entries. CORR writes "minimum", the site and Jaeschke "minimal"; label kept as in master.tsv. Possible disagreement with the site: page 3 and page 7 call the MCID "a within-patient threshold for one person's change". Neither CORR article says this explicitly, and Jaeschke's abstract says the values help interpret scores "both in individuals and in groups of patients". The editorial does support the site's caution that a mean difference below the MCID does not rule out benefit in a subset of patients. Content review of 20.11.2026 (B25) asked to add that an MCID derived for one patient's change does not transfer automatically to a difference between group means. Neither CORR article says so (both re-asked through the fetch tool on 20.11.2026; Maltenfort and Díaz-Ledezma only report, after Katz et al., that "averaging across groups could be misleading, if only a few patients change substantially"), and a web search found sources that disagree on whether an MCID is an individual or a group threshold. Definition left unchanged; the question is with Doc.

### `missing-data`

**Missing data.** Values that were never recorded, such as an unanswered question or a missed visit. R shows a missing value as NA and pandas as NaN. Whether they bias a result depends on why they are missing; missing at random means that the chance a value is missing depends only on things that were measured, not on the missing value itself.

- **Source:** Sterne JAC, White IR, Carlin JB, et al. Multiple imputation for missing data in epidemiological and clinical research: potential and pitfalls. BMJ, 2009;338:b2393; "Consequences of missing data" and Box 1
- **URL:** <https://pmc.ncbi.nlm.nih.gov/articles/PMC2714692/>
- **Supports:** The risk of bias depends on why data are missing; missing at random: systematic differences between missing and observed values are explained by observed data.
- **Also:** Vandenbroucke JP, von Elm E, Altman DG, et al. Strengthening the Reporting of Observational Studies in Epidemiology (STROBE): Explanation and Elaboration. PLoS Med, 2007;4(10):e297; Box 6 (missing at random: given the observed data, the probability of being missing is independent of the missing values). https://doi.org/10.1371/journal.pmed.0040297 . R Core Team. R documentation: NA {base}. https://stat.ethz.ch/R-manual/R-devel/library/base/html/NA.html . pandas user guide: Working with missing data. https://pandas.pydata.org/docs/user_guide/missing_data.html
- **Checked:** 16.11.2026, passage read
- **Notes:** Page 16's three definitions (missing completely at random, at random, not at random) agree with Sterne's Box 1. Elsewhere page 16 says visits "were missed almost entirely at random" in the everyday sense, which is the technical "completely at random"; a link from that phrase to this entry could confuse. The examples in the first sentence follow Sterne (missed clinic appointments) and Hayes-Larson 2019 (non-response; see table-1). pandas also has NaT and pd.NA; page 3 names only NA and NaN. Page 13 notes that censoring is not missing data.

### `mixed-model`

**Mixed model.** A model for data in which several measurements belong together, such as scores from the same patient at several visits. It combines fixed effects, which describe the average effect of predictors such as treatment or visit, with random effects, which allow each patient their own level.

- **Source:** Schober P, Vetter TR. Repeated Measures Designs and Analysis of Longitudinal Data: If at First You Do Not Succeed—Try, Try Again. Anesth Analg 2018;127(2):569–575; section 'Mixed-Effect Models'
- **URL:** <https://pmc.ncbi.nlm.nih.gov/articles/PMC6072386/>
- **Supports:** "The name mixed-effect models arises from the fact that they include both fixed and random effects"; random effects control for the variation coming from different subjects.
- **Also:** statsmodels documentation, Linear Mixed Effects Models, https://www.statsmodels.org/stable/mixed_linear.html ("used for regression analyses involving dependent data ... multiple observations are made on each subject"); Bates D, Mächler M, Bolker B, Walker S. Fitting Linear Mixed-Effects Models Using lme4. J Stat Softw 2015;67(1) (read as the lme4 package vignette), https://cran.r-project.org/web/packages/lme4/vignettes/lmer.pdf, section 1
- **Checked:** 16.11.2026, passage read
- **Notes:** Covers 'mixed model', 'linear mixed model', 'mixed-effects model'. Page 16's main selling point (a mixed model uses every score, including patients with missed visits) is NOT in the definition: none of the sources I opened states it, so it is left to the page. Schober & Vetter only say that repeated-measures ANOVA drops a subject with any missing observation.

### `model`

**Model.** A short mathematical description of how an outcome depends on one or more predictors, plus a part for the chance variation that is left over. Fitting a model means having software find the values of its unknown numbers that match the data best; the result is the fitted model.

- **Source:** NIST/SEMATECH e-Handbook of Statistical Methods. National Institute of Standards and Technology; section 4.1.1, What is process modeling?
- **URL:** <https://www.itl.nist.gov/div898/handbook/pmd/section1/pmd11.htm>
- **Supports:** Modeling is the concise description of the variation in one quantity by a mathematical function of other quantities plus a random component that follows a probability distribution.
- **Also:** Harrell FE. Glossary of Statistical Terms. Vanderbilt University, 26.04.2025; entry 'statistical model' (https://hbiostat.org/glossary/). For 'fit': Penn State Eberly College of Science. STAT 501: Regression Methods (online course notes); Lesson 1, section 1.2: the line that fits best is the one whose prediction errors are as small as possible (https://online.stat.psu.edu/stat501/Lesson01.html)
- **Checked:** 16.11.2026, passage read
- **Notes:** Covers 'model', 'statistical model', 'fit a model' and 'fitted'. Harrell's entry is more technical (identified parameters, a probability distribution for the data); the NIST wording was used because it is plainer. 'Fitted values' (the model's predictions) are named in the residual entry as 'the value the model predicts'.

### `multiple-comparisons`

**Multiple comparisons.** Running several tests in one study, for example comparing every pair of groups or testing many outcomes. The more tests, the greater the chance that at least one gives a false positive. An adjustment makes each test stricter by raising its p-value (to an adjusted p-value), so that the overall chance stays at the chosen level.

- **Source:** Harrell FE. Glossary of Statistical Terms. hbiostat.org; entry 'multiple comparisons'
- **URL:** <https://hbiostat.org/glossary/>
- **Supports:** When multiple tests are done, the chance that at least one asserts an effect when there are no effects increases with the number of tests; to control the overall probability, "individual P-values can be adjusted upward".
- **Also:** ICH Harmonised Tripartite Guideline E9, Statistical Principles for Clinical Trials (1998), section 5.6 (multiplicity "may necessitate an adjustment to the type I error"), https://database.ich.org/sites/default/files/E9_Guideline.pdf; GraphPad Software. GraphPad Prism 11 Statistics Guide, 'What is a family of comparisons?', https://www.graphpad.com/guides/prism/latest/statistics/stat_comparison_family.htm
- **Checked:** 16.11.2026, passage read
- **Notes:** Covers 'multiple comparisons', 'multiple testing', 'multiplicity', 'adjusted p-value(s)'. Note the glossary id 'adjustment' (batch S2) is about adjusting for confounders, so this entry explains the p-value adjustment in its own words.

### `multivariable`

**Multivariable model.** A model with several predictors at once, also called multiple regression, so that each predictor's effect is estimated with the others held fixed: adjusted for them. A univariable model has only one predictor.

- **Source:** Schneider A, Hommel G, Blettner M. Linear regression analysis: part 14 of a series on evaluation of scientific publications. Dtsch Arztebl Int, 2010;107(44):776–782; sections 'Univariable linear regression' and 'Multivariable linear regression'
- **URL:** <https://pmc.ncbi.nlm.nih.gov/articles/PMC2992018/>
- **Supports:** Univariable regression studies the relationship between the outcome and a single independent variable; multivariable regression studies several at once, with their coefficients adjusted for each other.
- **Also:** Harrell FE. Glossary of Statistical Terms. Vanderbilt University, 26.04.2025; entry 'multivariable model': relates multiple predictor variables to a single response (https://hbiostat.org/glossary/). Hidalgo B, Goodman M. Multivariate or multivariable regression? Am J Public Health, 2013;103(1):39–40 (https://pmc.ncbi.nlm.nih.gov/articles/PMC3518362/)
- **Checked:** 16.11.2026, passage read
- **Notes:** Not the same as 'multivariate', which Harrell's glossary and Hidalgo and Goodman reserve for models with more than one outcome; left out of the definition to keep it short, worth adding if a page ever says 'multivariate'. Hidalgo and Goodman was read through the fetch tool's quotes, the other two directly.

### `nonlinear-regression`

**Nonlinear regression.** Regression that fits a curve whose formula you choose, such as a recovery curve that rises quickly and then levels off, where a straight line cannot describe the relationship. The program starts from rough guesses that you supply and improves them step by step until the curve fits the data best (least squares); with poor starting guesses it may fail to find an answer.

- **Source:** NIST/SEMATECH. e-Handbook of Statistical Methods. National Institute of Standards and Technology, 2012; section 4.1.4.2 Nonlinear Least Squares Regression
- **URL:** <https://www.itl.nist.gov/div898/handbook/pmd/section1/pmd142.htm>
- **Supports:** Nonlinear least squares fits "a much larger and more general class of functions", needs "iterative optimization procedures" and user-provided starting values, and with poor ones "the optimization procedure may not converge".
- **Checked:** 16.11.2026, passage read
- **Notes:** Read as page text. NIST's example is a process that "increases quickly at first and then levels off", which linear models "do not describe ... very well"; the recovery curve is the site's (page 11). Strictly, NIST defines a nonlinear model as one that is not linear in its unknown parameters, which is narrower than "any curve": a curve such as a spline is still fitted by linear regression. Page 11 uses the term in NIST's sense. Page 12's heading "Multiple nonlinear regression" also covers splines, and the page itself says they fit inside an ordinary linear model, so there is no conflict, only a looser heading.

### `nonparametric`

**Nonparametric (rank-based) test.** A test that does not assume the values follow a normal distribution. Most nonparametric tests work on the ranks of the values instead of the values themselves; the Mann-Whitney, Wilcoxon signed-rank, Kruskal-Wallis and Friedman tests are examples. Also called distribution-free.

- **Source:** Harrell FE. Glossary of Statistical Terms. Vanderbilt University School of Medicine, Department of Biostatistics, 26.04.2025; entry "nonparametric tests"
- **URL:** <https://hbiostat.org/glossary/>
- **Supports:** Harrell: a test that makes minimal assumptions about the distribution of the data; such tests for ordinal or continuous variables "are typically based on the ranks of the data values"; "Distribution-free is perhaps a better term".
- **Also:** Motulsky HJ. "Key concepts: Nonparametric tests". GraphPad Statistics Guide (Prism 11). GraphPad Software; accessed 16.11.2026 (values are ranked from low to high and the analyses are based on the distribution of ranks; fewer assumptions about the distribution of the data). https://www.graphpad.com/guides/prism/latest/statistics/parametricornonparametric.htm The list of tests is from Motulsky HJ. "Nonparametric tests". GraphPad Statistics Guide (Prism 11). GraphPad Software; accessed 16.11.2026. https://www.graphpad.com/guides/prism/latest/statistics/stat_nonparametric_tests.htm
- **Checked:** 16.11.2026, passage read
- **Notes:** Harrell adds that these tests are not assumption-free (the log-rank test assumes proportional hazards, for instance); left to the pages. The site's 'nonparametric regression' (page 11) uses the word more loosely (no assumed straight line or normal residuals); the definition is about tests, as the label says.

### `normal-distribution`

**Normal (Gaussian) distribution.** A symmetric, bell-shaped distribution: values pile up around the mean and thin out evenly on both sides. It is fully described by its mean and standard deviation, and about 95% of values lie within 2 standard deviations of the mean. Many tests assume that the data follow it.

- **Source:** Harrell FE. Glossary of Statistical Terms. Vanderbilt University School of Medicine, Department of Biostatistics, 2025 (hbiostat.org); entry "normal distribution"
- **URL:** <https://hbiostat.org/glossary/>
- **Supports:** "A symmetric, bell-shaped distribution ... Also called the Gaussian distribution"; a measurement falls within 1.96 standard deviations of the mean with probability 0.95.
- **Also:** Çetinkaya-Rundel M, Hardin J. Introduction to Modern Statistics, 2nd ed. OpenIntro, 2024; section 13.2.1 ("the mean and standard deviation describe a normal distribution exactly") and 13.3.1 (about 95% within 2 standard deviations). https://openintro-ims.netlify.app/foundations-mathematical ; NIST/SEMATECH e-Handbook of Statistical Methods. National Institute of Standards and Technology, 2012, section 1.3.6.6.1 ("Many classical statistical tests are based on the assumption that the data follow a normal distribution"). https://www.itl.nist.gov/div898/handbook/eda/section3/eda3661.htm ; not opened: Altman DG, Bland JM. Statistics Notes: The normal distribution. BMJ 1995;310:298, https://doi.org/10.1136/bmj.310.6975.298
- **Checked:** 16.11.2026, passage read
- **Notes:** The Altman & Bland note is the natural citation but could not be opened (bmj.com refused the request; PubMed Central holds only a scanned page), so it is listed as not opened and nothing rests on it. Harrell adds a caution worth knowing: the normal distribution "cannot be relied upon to approximate the distribution of raw data"; the site's page 3 teaches readers to check, so no conflict.

### `null-hypothesis`

**Null hypothesis.** The assumption a test starts from: that there is no difference or no association. The p-value is calculated as if it were true.

- **Source:** Greenland S, Senn SJ, Rothman KJ, Carlin JB, Poole C, Goodman SN, Altman DG. Statistical tests, P values, confidence intervals, and power: a guide to misinterpretations. Eur J Epidemiol 2016;31(4):337 to 350; sections "Statistical tests, P values, and confidence intervals: a caustic primer" and "Common misinterpretations of single P values"
- **URL:** <https://doi.org/10.1007/s10654-016-0149-3>
- **Supports:** When the tested effect size is "a 'null' value representing zero effect", the test hypothesis is called the null hypothesis; "The P value assumes the test hypothesis is true".
- **Also:** GraphPad Software. GraphPad Prism 11 Statistics Guide (the guide the brief lists as Motulsky's); page "What is a P value?" ("The first step is to state the null hypothesis, that really the treatment does not affect the outcome"). https://www.graphpad.com/guides/prism/latest/statistics/what_is_a_p_value.htm . Also Harrell FE. Glossary of Statistical Terms. Vanderbilt University School of Medicine, Department of Biostatistics, version of 26.04.2025, entry "null hypothesis". https://hbiostat.org/glossary/
- **Checked:** 16.11.2026, passage read
- **Notes:** Fully supported. Harrell qualifies it: "Customarily but not necessarily a hypothesis of no effect"; a test can start from another value. The site has such tests: page 5 (the true mean is 90 minutes, the rate is 7%: no difference from a stated value) and Shapiro-Wilk on page 3 (the data come from a normal distribution). Greenland reserves "null" for the no-effect case, so the definition stands; adding "usually" before "that there is no difference" would cover the others.

### `observational-study`

**Observational study.** A study in which the researchers do not assign the treatment; they record which treatment each patient got and what happened afterwards. Patients who got one treatment can differ from those who got another, for example in age or health, so a difference in outcome may not be due to the treatment (confounding).

- **Source:** Cochrane Community. Glossary. Cochrane; archived copy of community.cochrane.org/glossary (Internet Archive snapshot of 01.07.2019); entries "Observational study" and "Cohort study"
- **URL:** <https://web.archive.org/web/20190701142620/https://community.cochrane.org/glossary>
- **Supports:** "A study in which the investigators do not seek to intervene, and simply observe the course of events"; unallocated groups need adjusted analysis for confounders.
- **Also:** Harrell FE. Glossary of Statistical Terms. Vanderbilt University, 26.04.2025; entry "observational study" (no treatment is manipulated by the investigator, randomization is not used; limited for therapeutic comparisons because of unknown confounders). https://hbiostat.org/glossary/
- **Checked:** 16.11.2026, passage read
- **Notes:** Cochrane has retired its glossary page (community.cochrane.org/glossary now redirects to resources.cochrane.org, which points readers to archive.org), so the entry was read in the Internet Archive snapshot of 01.07.2019.

### `odds`

**Odds.** The probability that an event happens divided by the probability that it does not: in a group, the number of patients with the event divided by the number without it. Odds of 0.1 mean 1 patient with the event for every 10 without, a risk of about 9%. The log odds, the logarithm of the odds, can take any value and are the scale on which logistic regression works.

- **Source:** Higgins JPT, Li T, Deeks JJ (eds). Chapter 6: Choosing effect measures and computing estimates of effect. In: Cochrane Handbook for Systematic Reviews of Interventions, version 6.5. Cochrane, 2024; section 6.4.1.1, Risk and odds
- **URL:** <https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-06>
- **Supports:** Odds are "the ratio of the probability that a particular event will occur to the probability that it will not occur"; with odds of 0.1 the risk is 0.091.
- **Also:** Bland JM, Altman DG. Statistics Notes: The odds ratio. BMJ 2000;320:1468 (odds: "the ratio of the probability that the event of interest occurs to the probability that it does not"). https://pmc.ncbi.nlm.nih.gov/articles/PMC1127651/ ; Harrell FE. Regression Modeling Strategies. hbiostat.org; section 10.1 (the logistic model is linear in the log odds, logit(P) = log(P / (1 - P))). https://hbiostat.org/rmsc/lrm
- **Checked:** 16.11.2026, passage read
- **Notes:** Agrees with the site (page 11: "the risk divided by 1 minus the risk"; existing odds-ratio entry: number with divided by number without). "Can take any value" is not a verbatim source statement for the log odds: Cochrane 6.4.1.1 says odds run from zero to infinity, Cochrane 6.1.2.1 says the log of 0 is minus infinity and the log of infinity is infinity, and Bland & Altman say it of the log odds ratio; the claim follows from those.

### `odds-ratio`

**Odds ratio.** The odds of the outcome in one group divided by the odds in the other. The odds are the number with the outcome divided by the number without it. An odds ratio is not a risk ratio: it lies further from 1, and the two differ most when the outcome is common, so reading an odds ratio as a risk ratio overstates the effect.

- **Source:** Higgins JPT, Li T, Deeks JJ (editors). Chapter 6: Choosing effect measures and computing estimates of effect. In: Cochrane Handbook for Systematic Reviews of Interventions, version 6.5. Cochrane, 2024; sections 6.4.1.1 (Risk and odds) and 6.4.1.2
- **URL:** <https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-06>
- **Supports:** Odds in health care "is the ratio of the number of people with the event to the number without"; the odds ratio "is the ratio of the odds of an event" in the two groups.
- **Also:** Harrell FE. Glossary of Statistical Terms. Vanderbilt University School of Medicine, Department of Biostatistics, version of 26.04.2025, entries "odds" and "odds ratio" ("the odds of the event occurring for group A divided by the odds that it occurs for group B"). https://hbiostat.org/glossary/ . Also GraphPad Software. GraphPad Prism 11 Statistics Guide (the guide the brief lists as Motulsky's); page "Interpreting results: Odds ratio" (worked example 688/21 against 650/59). https://www.graphpad.com/guides/prism/latest/statistics/stat_interpreting_results_odds_rati.htm
- **Checked:** 16.11.2026, passage read; 20.11.2026, section 6.4.1.3 "Warning: OR and RR are not the same" read ("For interventions that increase the chances of events, the odds ratio will be larger than the risk ratio ... especially when events are common"; "For interventions that reduce the chances of events, the odds ratio will be smaller than the risk ratio, so that, again, misinterpretation overestimates the effect"). Computation on `data/acl_cohort.csv` (R 4.6.0), page 6's example, return to sport by sex: women 81 of 152 (0.533), men 92 of 198 (0.465); risk ratio 1.147, sample odds ratio 1.314 (Fisher's conditional estimate 1.313, the 1.31 page 6 prints), so the odds ratio is further from 1.
- **Notes:** Fully supported. The last sentence was added on 20.11.2026 (content review B7) from Cochrane section 6.4.1.3; "further from 1" is Cochrane's "larger" and "smaller" put together, and is also arithmetic for one 2 × 2 table: the odds ratio is the risk ratio times (1 minus the risk in the second group) divided by (1 minus the risk in the first), a factor above 1 exactly when the first risk is the higher. The risk-ratio entry carries the same warning. Harrell defines odds with probabilities (probability of the event ÷ probability of no event), which is the same number as the count with ÷ the count without. Could not open Bland and Altman's Statistics Note "The odds ratio" (BMJ 2000;320:1468); bmj.com and PubMed Central blocked automated access.

### `ordinal`

**Ordinal.** Describes data whose values are categories with a natural order, such as mild, moderate and severe, or satisfaction from 1 to 5. The order has meaning, but the steps between neighboring categories are not necessarily equal.

- **Source:** Higgins JPT, Li T, Deeks JJ (eds). Chapter 6: Choosing effect measures and computing estimates of effect. In: Cochrane Handbook for Systematic Reviews of Interventions, version 6.5. Cochrane, 2024; section 6.6.1
- **URL:** <https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-06>
- **Supports:** "Ordinal outcome data arise when each participant is classified in a category and when the categories have a natural order", for example mild, moderate or severe.
- **Also:** Harrell FE. Glossary of Statistical Terms. Vanderbilt University School of Medicine, Department of Biostatistics, 2025 (hbiostat.org); entry "ordinal variable" ("Spacings between codes are not important"). https://hbiostat.org/glossary/ ; Sullivan GM, Artino AR Jr. Analyzing and interpreting data from Likert-type scales. J Grad Med Educ 2013;5(4):541 to 542 (differences between responses "are not necessarily equal"). https://pmc.ncbi.nlm.nih.gov/articles/PMC3886444/
- **Checked:** 16.11.2026, passage read
- **Notes:** I did not put the site's analysis rule ("ordinal data always go in the rank column") into the definition: the sources differ on it. Cochrane 6.6.1 says ordinal scales with many categories are often analyzed as continuous, and Sullivan & Artino conclude parametric tests can be used; see the note under likert-scale.

### `outcome`

**Outcome.** The variable a study sets out to explain, predict or change with a treatment, such as a score 1 year after surgery or whether a hip was revised. Also called the dependent variable, the response or the end point.

- **Source:** Harrell FE. Glossary of Statistical Terms. Vanderbilt University School of Medicine, Department of Biostatistics, 2025 (hbiostat.org); entry "dependent, response, outcome, endpoint variable"
- **URL:** <https://hbiostat.org/glossary/>
- **Supports:** A binary, categorical, ordinal, continuous or time-to-event variable "that is considered to be the target of prediction or the target of an intervention".
- **Also:** Penn State Eberly College of Science. STAT 200: Elementary Statistics (online notes), Lesson 1: Collecting Data; section 1.1.2, Definition 1.7 (response variable, "also known as the dependent or outcome variable"; its variation is explained by the explanatory variable). https://online.stat.psu.edu/stat200/Lesson01
- **Checked:** 16.11.2026, passage read
- **Notes:** Defined in the scope note's sense (the outcome variable). The site also writes "patients with the outcome" and "two possible outcomes", meaning one result of a yes/no variable (close to "event"); that sense is not covered here. If wanted, a third sentence could be: For a yes/no outcome, "patients with the outcome" are those in whom it happened (Penn State STAT 200 Lesson 2, Definition 2.5 uses "number with the outcome" this way). Harrell spells it "endpoint"; I kept "end point" from master.tsv.

### `outlier`

**Outlier.** A value that lies far from the rest of the values. Look into it before deciding what to do: it may be a recording error, or it may be real and informative.

- **Source:** NIST/SEMATECH e-Handbook of Statistical Methods. National Institute of Standards and Technology, 2012; section 7.1.6, What are outliers in the data?
- **URL:** <https://www.itl.nist.gov/div898/handbook/prc/section1/prc16.htm>
- **Supports:** "An outlier is an observation that lies an abnormal distance from other values"; outliers should be investigated carefully, may hold valuable information, and are often bad data points.
- **Also:** Çetinkaya-Rundel M, Hardin J. Introduction to Modern Statistics, 2nd ed. OpenIntro, 2024; section 5.5 ("An outlier is an observation that appears extreme relative to the rest of the data"; may flag data entry errors). https://openintro-ims.netlify.app/explore-numerical
- **Checked:** 16.11.2026, passage read
- **Notes:** No cut-off is given on purpose. NIST and IMS both mention the boxplot convention (beyond 1.5 times the IQR from the box) but say what counts as abnormal is the analyst's call; the site says "extreme outliers" without a rule.

### `overall-test`

**Overall (omnibus) test.** A single test of whether there is any difference at all among three or more groups, such as the F test of an ANOVA. A small p-value says that some difference exists somewhere, but not which groups differ. Also called an omnibus or global test.

- **Source:** Lenth RV. emmeans package (version 2.0.5), vignette 'Basics of estimated marginal means'; section 'P values, significance, and recommendations'
- **URL:** <https://rvlenth.github.io/emmeans/articles/basics.html>
- **Supports:** Of the "omnibus F test": a small P value "suggests that there is some effect, somewhere", and does not even necessarily imply that any two means differ.
- **Also:** Schober P, Vetter TR. Repeated Measures Designs and Analysis of Longitudinal Data: If at First You Do Not Succeed—Try, Try Again. Anesth Analg 2018;127(2):569–575 (ANOVA "gives an overall P value" but "does not identify which group means are equal or not"), https://pmc.ncbi.nlm.nih.gov/articles/PMC6072386/; NIST/SEMATECH e-Handbook of Statistical Methods, section 7.4.7 How can we make multiple comparisons?, https://www.itl.nist.gov/div898/handbook/prc/section4/prc47.htm; survival package documentation, cox.zph ("a global chi-square test ... in addition to the per-variable or per-term tests"), https://stat.ethz.ch/R-manual/R-devel/library/survival/html/cox.zph.html
- **Checked:** 16.11.2026, passage read
- **Notes:** The sources describe the ANOVA F test; that Kruskal-Wallis, chi-square and log-rank tests across three or more groups are overall tests in the same sense is the site's usage (page 15) and is not stated in a source I opened. 'Global test' on page 14 (cox.zph) is one test across all the model's terms, a slightly different use of the same idea; the definition's wording about groups does not cover it literally.

### `p-hacking`

**p-hacking (data dredging).** Trying different analyses, outcome definitions or subgroups, or adding more data, until a result becomes statistically significant, and then reporting only that result. The chance of a false positive is then higher than the 5% a single planned test allows. Also called data dredging.

- **Source:** GraphPad Software. GraphPad Prism 11 Statistics Guide; page 'Advice: Don't P-Hack'
- **URL:** <https://www.graphpad.com/guides/prism/latest/statistics/stat_advice_dont_p-hack.htm>
- **Supports:** Collecting more data or trying other analyses until the result is significant means that, even with no real effect, "the chance of finding a 'statistically significant' result exceeds 5%".
- **Also:** Head ML, Holman L, Lanfear R, Kahn AT, Jennions MD. The Extent and Consequences of P-Hacking in Science. PLoS Biol 2015;13(3):e1002106 (researchers "try out several statistical analyses and/or data eligibility specifications and then selectively report those that produce significant results"), https://pmc.ncbi.nlm.nih.gov/articles/PMC4359000/; American Statistical Association, press release on the Statement on Statistical Significance and P-Values, 7 March 2016 ("practices called by such names as 'p-hacking' and 'data dredging'"), https://www.amstat.org/asa/files/pdfs/p-valuestatement.pdf
- **Checked:** 16.11.2026, passage read
- **Notes:** The ASA statement itself (Wasserstein & Lazar 2016) could not be opened (403); the press release that accompanies it was read. Page 15 uses 'p-hacking' for choosing the adjustment after seeing the p-values and page 14 'data dredging' for trying several cut points; both fit the definition.

### `p-value`

**p-value.** The probability of a result at least as extreme as yours if there were truly no difference. A small p-value means the data would be surprising if there were no difference. It is not the probability that there is no difference.

- **Source:** Greenland S, Senn SJ, Rothman KJ, Carlin JB, Poole C, Goodman SN, Altman DG. Statistical tests, P values, confidence intervals, and power: a guide to misinterpretations. Eur J Epidemiol 2016;31(4):337 to 350; sections "Statistical tests, P values, and confidence intervals: a caustic primer" and "Common misinterpretations of single P values" (misinterpretation 1)
- **URL:** <https://doi.org/10.1007/s10654-016-0149-3>
- **Supports:** The P value is the probability the test statistic "would have been at least as large as its observed value if every model assumption were correct, including the test hypothesis".
- **Also:** Harrell FE. Glossary of Statistical Terms. Vanderbilt University School of Medicine, Department of Biostatistics, version of 26.04.2025, entry "P-value" ("as or more extreme than the observed statistic had H0 been true"; "The P-value is not the probability that the null hypothesis is true"). https://hbiostat.org/glossary/ . Also GraphPad Software. GraphPad Prism 11 Statistics Guide (the guide the brief lists as Motulsky's); page "What is a P value?". https://www.graphpad.com/guides/prism/latest/statistics/what_is_a_p_value.htm
- **Checked:** 16.11.2026, passage read
- **Notes:** Fully supported, all three sentences (the third is Greenland's misinterpretation 1: the P value "is not a hypothesis probability"). Greenland's wording is stricter in one respect: the P value assumes every assumption of the test is correct, not only "no difference". As for the null hypothesis, "no difference" is the usual case, not the only one.

### `paired`

**Paired.** Two measurements that belong together: the same patient before and after surgery, or the left and right hip of one person.

- **Source:** Harrell FE. Glossary of Statistical Terms. Vanderbilt University School of Medicine, Department of Biostatistics, version of 26.04.2025, entry "paired data"
- **URL:** <https://hbiostat.org/glossary/>
- **Supports:** "When each subject has two response measurements, there is a natural pairing to the data and the two responses are correlated."
- **Also:** GraphPad Software. GraphPad Prism 11 Statistics Guide (the guide the brief lists as Motulsky's); page "Experimental design tab: t tests" (paired when "values on the same row are related to each other": before and after an intervention, subjects recruited as matched pairs, twins). https://www.graphpad.com/guides/prism/latest/statistics/stat_choosing_a_t_test.htm
- **Checked:** 16.11.2026, passage read
- **Notes:** Fully supported. GraphPad's list also counts two different people matched to each other (matched pairs, twins) as paired. The definition's two examples are both within one person, but "belong together" covers the matched pairs the site analyzes on page 7.

### `pairwise-comparison`

**Pairwise comparison.** A comparison of two groups at a time. With three or more groups, comparing every pair means several tests (four groups make six pairs), so the p-values need an adjustment for multiple comparisons.

- **Source:** NIST/SEMATECH e-Handbook of Statistical Methods, section 7.4.7 How can we make multiple comparisons?
- **URL:** <https://www.itl.nist.gov/div898/handbook/prc/section4/prc47.htm>
- **Supports:** "Doing pairwise comparison procedures over and over again for all possible pairs will not, in general, work", because the overall significance level is not as specified for a single pair comparison.
- **Also:** Lenth RV. emmeans vignette 'Comparisons and contrasts in emmeans', section 'Pairwise comparisons', https://rvlenth.github.io/emmeans/articles/comparisons.html; PMCMRplus documentation, frdAllPairsConoverTest (k groups give k(k-1)/2 pairs), https://search.r-project.org/CRAN/refmans/PMCMRplus/html/frdAllPairsConoverTest.html
- **Checked:** 16.11.2026, passage read
- **Notes:** 'Four groups make six pairs' is k(k-1)/2 with k = 4, the example page 15 uses.

### `prom`

**Patient-reported outcome measure (PROM).** A questionnaire that patients answer themselves about their own health, such as symptoms, function or quality of life. The answers come straight from the patient, without a clinician interpreting them, and are often combined into a score.

- **Source:** Johnston BC, Patrick DL, Devji T, et al. Chapter 18: Patient-reported outcomes. In: Cochrane Handbook for Systematic Reviews of Interventions, version 6.5. Cochrane, 2024; section 18.1.1
- **URL:** <https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-18>
- **Supports:** PROMs "are instruments that are used to measure the PROs, most often self-report questionnaires"; a PRO comes directly from the patient without interpretation.
- **Checked:** 16.11.2026, passage read
- **Notes:** The Cochrane chapter quotes the FDA's 2009 guidance for the definition of a patient-reported outcome; the FDA document itself was not opened. "Often combined into a score" rests on a weaker passage of the same chapter (section 18.2: instruments may "yield a single indicator or index number, or a profile"), so drop that clause if it should be backed more firmly.

### `pearson-correlation`

**Pearson correlation (r).** A number, r, from −1 to +1 that says how closely two measurements follow a straight line. Close to +1, one rises as the other rises; close to −1, one falls as the other rises; close to 0, there is no straight-line relationship, though there may still be a curved one.

- **Source:** Bewick V, Cheek L, Ball J. Statistics review 7: Correlation and regression. Crit Care 2003;7(6):451-459. doi:10.1186/cc2401; section on the scatter diagram and the correlation coefficient
- **URL:** <https://pmc.ncbi.nlm.nih.gov/articles/PMC374386/>
- **Supports:** The Pearson (product moment) correlation coefficient always lies between -1 and +1; values near +1 or -1 indicate a strong positive or negative linear relationship, and near 0 no linear relationship, although a nonlinear one could exist.
- **Also:** SciPy documentation, scipy.stats.pearsonr ('measures the linear relationship between two datasets'), https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.pearsonr.html ; GraphPad Software. GraphPad Prism 11 Statistics Guide; page 'Interpreting results: Correlation', https://www.graphpad.com/guides/prism/latest/statistics/stat_interpreting_results_correlati.htm
- **Checked:** 16.11.2026, passage read
- **Notes:** No strength labels given, as the brief asks. The source also warns that correlation does not imply causation; left to the pages.

### `percentage-point`

**Percentage point.** The unit for the plain difference between two percentages. A fall from 4% to 3% is a fall of 1 percentage point, although relative to the starting 4% it is a fall of 25%.

- **Source:** Schünemann HJ, Vist GE, Higgins JPT, et al. Chapter 15: Interpreting results and drawing conclusions. In: Cochrane Handbook for Systematic Reviews of Interventions, version 6.5. Cochrane, 2024; section 15.4.1
- **URL:** <https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-15>
- **Supports:** Reducing the relative risk of death by 25% and reducing the risk by 1 percentage point can be the same benefit, "a reduction in risk from 4% to 3%".
- **Also:** Bland JM, Altman DG. Statistics Notes: The odds ratio. BMJ 2000;320:1468 (difference between proportions "0.187 (or 18.7 percentage points)"). https://pmc.ncbi.nlm.nih.gov/articles/PMC1127651/ ; Eurostat. Statistics Explained, Glossary: Percentage point ("used when comparing two different percentages"). https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Glossary:Percentage_point
- **Checked:** 16.11.2026, passage read
- **Notes:** The example is Cochrane's own. Eurostat is an official statistical glossary, not on the brief's named list, given as a third confirmation only.

### `percentile`

**Percentile.** The value below which a given percentage of the values lie. A quarter of the values lie below the 25th percentile.

- **Source:** NIST/SEMATECH e-Handbook of Statistical Methods; section 7.2.6.2, Percentiles
- **URL:** <https://www.itl.nist.gov/div898/handbook/prc/section2/prc262.htm>
- **Supports:** Percentiles estimate the proportions of the data that fall above and below a given value: "70 % of the data should fall below the 70th percentile."
- **Also:** Çetinkaya-Rundel M, Hardin J. Introduction to Modern Statistics, 2nd ed. OpenIntro; section 5.5 (the first quartile is "the 25th percentile, i.e., 25% of the data fall below this value"). https://openintro-ims.netlify.app/explore-numerical
- **Checked:** 16.11.2026, passage read
- **Notes:** Fully supported. NIST's formal wording is "at most" that percentage below, and NIST and GraphPad note that programs compute percentiles in several slightly different ways, so in a small sample the share below the 25th percentile is close to a quarter, not exactly a quarter.

### `planned-comparison`

**Planned comparison.** A comparison chosen when the study was designed, before any data were seen, because it answers the research question. A few planned comparisons need a milder adjustment for multiple comparisons than comparing every pair, and a single one needs none.

- **Source:** GraphPad Software. GraphPad Prism 11 Statistics Guide; page 'Lingo: Multiple comparison tests'
- **URL:** <https://www.graphpad.com/guides/prism/latest/statistics/terminology_post-hoc_mutplie_c_2_2.htm>
- **Supports:** Planned comparisons focus on a few scientifically sensible comparisons; "You can't decide which comparisons to do after looking at the data"; they must "be chosen when you design the experiment".
- **Also:** GraphPad Software. GraphPad Prism 11 Statistics Guide, 'What is a family of comparisons?' (fewer comparisons mean a less strict correction; a family of one comparison needs no correction), https://www.graphpad.com/guides/prism/latest/statistics/stat_comparison_family.htm; NIST/SEMATECH e-Handbook of Statistical Methods, section 7.4.7 How can we make multiple comparisons? (contrasts should be "determined in advance of observing the experimental results"), https://www.itl.nist.gov/div898/handbook/prc/section4/prc47.htm
- **Checked:** 16.11.2026, passage read
- **Notes:** Agrees with page 15 ('If you planned three comparisons, adjust for three') and page 16 (one planned comparison, no adjustment).

### `population`

**Population.** The whole group that a study wants to draw conclusions about, such as all patients who have a hip replacement. It can rarely be measured in full, so a study measures a sample and uses it to estimate the population's true values, such as the true mean.

- **Source:** Çetinkaya-Rundel M, Hardin J. Introduction to Modern Statistics, 2nd ed. OpenIntro, 2024; sections 2.1.1 and 2.1.2
- **URL:** <https://openintro-ims.netlify.app/data-design>
- **Supports:** Each research question refers to a target population; it is often not feasible to collect data for every case, so a sample is used to estimate the population average (a population parameter).
- **Also:** Penn State Eberly College of Science. STAT 200: Elementary Statistics (online notes), Lesson 1: Collecting Data; section 1.2, Definition 1.8 ("The entire set of possible cases") and Definition 1.11 (parameter: a measure concerning a population). https://online.stat.psu.edu/stat200/Lesson01
- **Checked:** 16.11.2026, passage read
- **Notes:** The sources say "population parameter" where the site says "true mean" or "true value"; the NIST handbook (section 3.3.3.3) uses "true mean" in the same sense. I kept the site's wording so that the entry covers "true mean/true value" and "patients like ours". "Parameter" has its own entry in another batch.

### `post-hoc-test`

**Post-hoc test.** A follow-up test run after an overall test, such as ANOVA, to find out which groups differ from which. It usually compares the groups in pairs, and because that means several tests, the p-values are adjusted for multiple comparisons. Some authors use the term only for comparisons chosen after looking at the data, as opposed to planned comparisons.

- **Source:** Schober P, Vetter TR. Repeated Measures Designs and Analysis of Longitudinal Data: If at First You Do Not Succeed—Try, Try Again. Anesth Analg 2018;127(2):569–575; section 'Repeated-Measures ANOVA'
- **URL:** <https://pmc.ncbi.nlm.nih.gov/articles/PMC6072386/>
- **Supports:** ANOVA gives an overall P value but "does not identify which group means are equal or not"; post hoc tests are pairwise comparisons of selected or all means, and need an adjusted significance criterion.
- **Also:** Lee S, Lee DK. What is the proper way to apply the multiple comparison test? Korean J Anesthesiol 2018;71(5):353–360, https://pmc.ncbi.nlm.nih.gov/articles/PMC6193594/ (the multiple comparison test "is sometimes also called a 'post-hoc test'"); GraphPad Software. GraphPad Prism 11 Statistics Guide, 'Lingo: Multiple comparison tests' ("Post-hoc test is used for situations where you decide which comparisons you want to make after looking at the data"), https://www.graphpad.com/guides/prism/latest/statistics/terminology_post-hoc_mutplie_c_2_2.htm
- **Checked:** 16.11.2026, passage read
- **Notes:** Two senses, both covered. The site (page 15) uses 'post-hoc' for any pairwise follow-up, including comparisons planned in advance; Motulsky's GraphPad guide reserves it for comparisons decided after seeing the data. Also: NIST 7.4.7 treats the ANOVA F test as a 'preliminary test' that decides whether to go on, which is the gate page 15 (#overall-test-first) argues is not needed; the emmeans vignette sides with the page.

### `power`

**Power.** The probability that a study finds a difference statistically significant when a difference of a given size truly exists. It grows with the sample size and with the size of the true difference. An underpowered study is likely to miss a real difference.

- **Source:** Harrell FE. Glossary of Statistical Terms. Vanderbilt University School of Medicine, Department of Biostatistics, 26.04.2025; entry "power"
- **URL:** <https://hbiostat.org/glossary/>
- **Supports:** Harrell: the probability of rejecting the null hypothesis for a set value of the unknown effect; it increases when the sample size and true effect increase and when the inter-subject variability decreases.
- **Also:** Motulsky HJ. "Key concepts: Statistical Power". GraphPad Statistics Guide (Prism 11). GraphPad Software; accessed 16.11.2026 ("The power of a test is the probability that you will reject the null hypothesis when it is false"; depends on effect size, sample size and variability). https://www.graphpad.com/guides/prism/latest/statistics/stat_key_concepts_statistical_power.htm
- **Checked:** 16.11.2026, passage read
- **Notes:** Harrell adds that power falls when the values vary more between patients (left out for brevity). The word 'underpowered' does not occur in the passages read; the last sentence follows from the definition of power (low probability of rejecting a false null hypothesis). 'Powerful' as used on the site (a more powerful test) is the same sense.

### `precision`

**Precision.** How little an estimate is affected by the play of chance (random error). A narrow confidence interval or a small standard error means a precise estimate; a wide interval means an imprecise one. Precision improves as the sample size grows.

- **Source:** Harrell FE. Glossary of Statistical Terms. Vanderbilt University School of Medicine, Department of Biostatistics, 26.04.2025; entry "precision"
- **URL:** <https://hbiostat.org/glossary/>
- **Supports:** Harrell: "Degree of absence of random error ... Precision can be quantified by the width of a confidence (compatibility) interval and sometimes by ... (standard error)"; it increases with the sample size.
- **Also:** Harrell FE. Glossary of Statistical Terms. Vanderbilt University School of Medicine, Department of Biostatistics, 26.04.2025; entry "standard error" ("Standard errors describe the precision of a statistical summary, not the variability across subjects"). https://hbiostat.org/glossary/
- **Checked:** 16.11.2026, passage read
- **Notes:** Statistical sense only. The site's code argument fit_options={"precision": ...} (lifelines) is a numerical tolerance, a different meaning, and should not be linked to this entry.

### `predictor`

**Predictor (covariate).** A variable used to explain or predict the outcome, such as age, sex or implant type. Also called a covariate, an explanatory variable or an independent variable.

- **Source:** Harrell FE. Glossary of Statistical Terms. Vanderbilt University School of Medicine, Department of Biostatistics, 2025 (hbiostat.org); entry "predictor, explanatory variable, risk factor, covariate, covariable, independent variable"
- **URL:** <https://hbiostat.org/glossary/>
- **Supports:** Harrell lists these names as one entry: "quantities which may be associated with better or worse outcome".
- **Also:** Penn State Eberly College of Science. STAT 200: Elementary Statistics (online notes), Lesson 1: Collecting Data; section 1.1.2, Definition 1.6 (explanatory variable, "also known as the independent or predictor variable, it explains variations in the response variable"). https://online.stat.psu.edu/stat200/Lesson01
- **Checked:** 16.11.2026, passage read
- **Notes:** Both sources treat the four names as synonyms, and so does the definition. "Independent variable" here has nothing to do with independent (unpaired) groups or the independence assumption, which have their own entries; the linker should not link "independent" alone to this entry.

### `prespecified`

**Prespecified (and exploratory) analysis.** A prespecified analysis is described in the study protocol before the data are seen: which outcome, which comparison, which method. An exploratory analysis is chosen after looking at the data; its results suggest questions for later studies and should be labeled as exploratory. The primary analysis is the prespecified analysis of the study's main outcome.

- **Source:** ICH Harmonised Tripartite Guideline E9, Statistical Principles for Clinical Trials (Step 4, 5 February 1998); sections 2.1.3, 2.2.2, 5.1 and 5.7
- **URL:** <https://database.ich.org/sites/default/files/E9_Guideline.pdf>
- **Supports:** The principal features of the analysis should be described in the protocol (5.1); exploratory analyses may use data-dependent hypotheses, serve "for suggesting further hypotheses for later research" (2.1.3) and should be clearly identified as such (5.7).
- **Also:** Moher D, Hopewell S, Schulz KF, et al. CONSORT 2010 Explanation and Elaboration. BMJ 2010;340:c869; item 18 ("Analyses that were prespecified in the trial protocol ... are much more reliable than those suggested by the data"), https://pmc.ncbi.nlm.nih.gov/articles/PMC2844943/
- **Checked:** 16.11.2026, passage read
- **Notes:** Covers 'prespecified', 'pre-specified', 'specified in advance', 'exploratory' and 'primary analysis'. ICH E9 speaks of the 'primary variable' and the 'confirmatory analysis of the primary variable(s)'; 'primary analysis' is the site's (and common) shorthand for that. Both sources are about trials; the site applies the idea to observational studies too.

### `primary-outcome`

**Primary outcome.** The one outcome that a study names in advance as its most important. It answers the study's main question, and the sample size calculation is usually based on it. The other outcomes of interest are secondary outcomes; the primary outcome is also called the primary end point.

- **Source:** Moher D, Hopewell S, Schulz KF, et al. CONSORT 2010 Explanation and Elaboration: updated guidelines for reporting parallel group randomised trials. BMJ, 2010;340:c869; item 6a
- **URL:** <https://doi.org/10.1136/bmj.c869>
- **Supports:** The primary outcome is "the pre-specified outcome considered to be of greatest importance to relevant stakeholders" and usually the one used in the sample size calculation; other outcomes of interest are secondary.
- **Also:** ICH Harmonised Tripartite Guideline. Statistical Principles for Clinical Trials E9. International Conference on Harmonisation, 05.02.1998; section 2.2.2 Primary and Secondary Variables (the primary variable, or "primary endpoint", gives the evidence "directly related to the primary objective of the trial"; "There should generally be only one"). https://database.ich.org/sites/default/files/E9_Guideline.pdf
- **Checked:** 16.11.2026, passage read
- **Notes:** CONSORT read in full text through PubMed Central (PMC2844943); ICH E9 read as the PDF (pages 5 and 6). Both are written for randomized trials; the site applies the term to an observational report (page 18), where it means the same. CONSORT allows that some trials have more than one primary outcome but does not recommend it, so "the one outcome" follows ICH E9's "generally only one". The site writes "end point" as two words.

### `probability`

**Probability.** A number from 0 to 1, often written as a percentage, that says how likely an event is. A probability of 0.25, or a 25% chance, means the event would happen in about 25 of 100 cases in the long run.

- **Source:** Harrell FE. Glossary of Statistical Terms. Vanderbilt University School of Medicine, Department of Biostatistics, 2025 (hbiostat.org); entry "probability"
- **URL:** <https://hbiostat.org/glossary/>
- **Supports:** A probability is "a number between 0 and 1 inclusive"; in the frequentist school it is the long-term fraction of occurrences of the event.
- **Also:** Penn State Eberly College of Science. STAT 200: Elementary Statistics (online notes), Lesson 2: Describing Data, Part 1; section 2.1.3 (probabilities "are typically written in decimal form but may also be translated to percentages"; 0.25 is "a 25% chance"). https://online.stat.psu.edu/stat200/Lesson02
- **Checked:** 16.11.2026, passage read
- **Notes:** Harrell notes that probability can also mean a degree of belief; the definition gives the long-run frequency reading, which is the one the site's p-value and confidence interval entries use.

### `profile-interval`

**Profile-likelihood confidence interval.** A confidence interval for a model coefficient, found by trying one candidate value after another, refitting the rest of the model each time, and keeping the candidates for which the model fits the data not significantly worse than at the best estimate. It need not be symmetric around the estimate, and in small samples it can be more accurate than the Wald interval. R's confint() gives it for glm() and nls() models.

- **Source:** Cole SR, Chu H, Greenland S. Maximum likelihood, profile likelihood, and penalized likelihood: a primer. American Journal of Epidemiology, 2014;179(2):252–260; section "Profile likelihood"
- **URL:** <https://pmc.ncbi.nlm.nih.gov/articles/PMC3873110/>
- **Supports:** Fix the coefficient at each value in turn, maximize over the rest; the limits are where a likelihood ratio test gives P = 0.05. With small samples they can give more accurate coverage and tend to be asymmetric.
- **Also:** R Core Team. R documentation, stats::confint (R 4.6) ("Methods for classes \"glm\" and \"nls\" call the appropriate profile method"; confint.default() is "based on asymptotic normality"): https://stat.ethz.ch/R-manual/R-devel/library/stats/html/confint.html
- **Checked:** 16.11.2026, passage read
- **Notes:** "Fits the data not significantly worse" stands for the likelihood ratio test at the 5% level (for a 95% interval), to avoid the undefined word "likelihood"; "maximum likelihood" and "likelihood-ratio test" are planned entries the editor may want to link. The site's wording (page 11: moves each number away from its estimate "until the fit gets significantly worse") agrees. PMC shows the article as published online in 2013; volume 179(2) is the 2014 print issue.

### `propensity-score`

**Propensity score.** A patient's estimated probability of receiving one treatment instead of the other, calculated from characteristics recorded at baseline. In an observational study, patients are matched on this score, or weighted by it (a weighted cohort), so that the treatment groups become alike in those characteristics. It cannot balance characteristics that were not recorded.

- **Source:** Austin PC. An Introduction to Propensity Score Methods for Reducing the Effects of Confounding in Observational Studies. Multivariate Behav Res, 2011;46(3):399; abstract and the sections on the propensity score, matching and weighting
- **URL:** <https://pmc.ncbi.nlm.nih.gov/articles/PMC3144483/>
- **Supports:** "The propensity score is the probability of treatment assignment conditional on observed baseline characteristics"; matching or weighting on it balances measured covariates.
- **Also:** Haukoos JS, Lewis RJ. The Propensity Score (JAMA Guide to Statistics and Methods). JAMA, 2015;314(15):1637 (confounding may remain if unmeasured factors influenced the choice of treatment). https://doi.org/10.1001/jama.2015.13480
- **Checked:** 16.11.2026, passage read
- **Notes:** Haukoos and Lewis was read through the PubMed full-text service (PMC4866501). Both sources also describe stratifying on the score and adjusting for it; the definition names only matching and weighting, the two the site mentions (page 2). Agrees with page 2's advice to show SMDs for matched or weighted cohorts: both sources recommend standardized differences to check balance.

### `proportion`

**Proportion.** A part divided by the whole: the number of patients with a characteristic divided by the total number of patients. It lies between 0 and 1 and is often written as a percentage, so 30 of 200 patients is 0.15, or 15%.

- **Source:** Penn State Eberly College of Science. STAT 200: Elementary Statistics (online notes), Lesson 2: Describing Data, Part 1; section 2.1.1, One Categorical Variable
- **URL:** <https://online.stat.psu.edu/stat200/Lesson02>
- **Supports:** Proportion = number in the category divided by the total number; "A proportion must be between 0 and 1.00".
- **Also:** Centers for Disease Control and Prevention. Principles of Epidemiology in Public Health Practice, 3rd ed.; Lesson 3, Section 1 ("A proportion is the comparison of a part to the whole ... may be expressed as a decimal, a fraction, or a percentage"). https://archive.cdc.gov/www_cdc_gov/csels/dsepd/ss1978/lesson3/section1.html
- **Checked:** 16.11.2026, passage read
- **Notes:** The CDC textbook is not on the brief's named list; it is an official, freely available standard reference and is used only as the second source. The 30 of 200 example is my own arithmetic (30 / 200 = 0.15).

### `proportional-hazards`

**Proportional hazards.** The assumption behind Cox regression that one group's hazard is a constant multiple of another's, so that the hazard ratio stays the same over the whole follow-up. The hazards themselves may change over time. The assumption needs to be checked, for example with Schoenfeld residuals.

- **Source:** Bradburn MJ, Clark TG, Love SB, Altman DG. Survival analysis part II: multivariate data analysis – an introduction to concepts and methods. Br J Cancer 2003;89(3):431–436. doi:10.1038/sj.bjc.6601119; section "The Cox ('semi-parametric') proportional hazards model"
- **URL:** <https://pmc.ncbi.nlm.nih.gov/articles/PMC2394368/>
- **Supports:** "the hazard of the event in any group is a constant multiple of the hazard in any other".
- **Also:** Bellera CA, MacGrogan G, Debled M, Tunon de Lara C, Brouste V, Mathoulin-Pélissier S. Variables with time-varying effects and the Cox model: some statistical concepts illustrated with a prognostic factor study in breast cancer. BMC Med Res Methodol 2010;10:20. doi:10.1186/1471-2288-10-20 ("the hazard ratio HR is constant; this is the assumption of proportional hazards"). https://pmc.ncbi.nlm.nih.gov/articles/PMC2846954/ Checking: Bradburn MJ, Clark TG, Love SB, Altman DG. Survival analysis part III: multivariate data analysis – choosing a model and assessing its adequacy and fit. Br J Cancer 2003;89(4):605–611. doi:10.1038/sj.bjc.6601120; section "Assessing whether PH is appropriate". https://pmc.ncbi.nlm.nih.gov/articles/PMC2376927/
- **Checked:** 16.11.2026, passage read
- **Notes:** That the assumption must be checked: Bradburn et al. part II ("it is important to verify that it holds") and part III ("should be verified"). Primary source read in full text.

### `qq-plot`

**Q-Q plot.** A plot for checking whether data follow a normal distribution: the sorted values are plotted against the values a normal distribution would give. If the data are roughly normal, the points lie close to a straight line; bends in the line or stray points at its ends show skew or outliers.

- **Source:** NIST/SEMATECH e-Handbook of Statistical Methods. National Institute of Standards and Technology, 2012; section 1.3.3.21, Normal Probability Plot
- **URL:** <https://www.itl.nist.gov/div898/handbook/eda/section3/normprpl.htm>
- **Supports:** The data are plotted against a theoretical normal distribution so that the points should form an approximate straight line; departures from the line indicate departures from normality.
- **Also:** NIST/SEMATECH e-Handbook of Statistical Methods. National Institute of Standards and Technology, 2012; section 1.3.3.24, Quantile-Quantile Plot (a probability plot is a q-q plot against the quantiles of a theoretical distribution; outliers can be detected). https://www.itl.nist.gov/div898/handbook/eda/section3/qqplot.htm ; R Core Team. R documentation, stats::qqnorm ("produces a normal QQ plot"). https://stat.ethz.ch/R-manual/R-devel/library/stats/html/qqnorm.html
- **Checked:** 16.11.2026, passage read
- **Notes:** Defined in the sense the site uses: the normal Q-Q plot, which NIST calls a normal probability plot. In general a Q-Q plot can compare any two distributions (NIST 1.3.3.24). The site writes "QQ plot"; master.tsv's label "Q-Q plot" is kept, and R's manual uses both spellings.

### `quartile`

**Quartile.** One of the three values that split the sorted values into four equal parts. The first quartile (Q1) is the 25th percentile, the second is the median, and the third (Q3) is the 75th percentile.

- **Source:** Harrell FE. Glossary of Statistical Terms. Vanderbilt University School of Medicine, Department of Biostatistics, 2025 (hbiostat.org); entry "quartiles"
- **URL:** <https://hbiostat.org/glossary/>
- **Supports:** The quartiles are the 25th and 75th percentiles and the median; the three values divide a variable's distribution into four intervals containing equal numbers of observations.
- **Also:** Çetinkaya-Rundel M, Hardin J. Introduction to Modern Statistics, 2nd ed. OpenIntro, 2024; section 5.5 (first quartile = 25th percentile and third quartile = 75th percentile, often labeled Q1 and Q3). https://openintro-ims.netlify.app/explore-numerical ; not opened: Altman DG, Bland JM. Statistics Notes: Quartiles, quintiles, centiles, and other quantiles. BMJ 1994;309:996, https://doi.org/10.1136/bmj.309.6960.996
- **Checked:** 16.11.2026, passage read
- **Notes:** NIST section 7.1.6 uses the same Q1 and Q3 labels. The Altman & Bland note could not be opened (scanned page only) and nothing rests on it.

### `r-squared`

**R-squared (R²).** The share of the variation in the outcome that a regression model accounts for, from 0 (none) to 1 (all of it). With one predictor it equals the Pearson correlation squared. Adding predictors can only raise it, so the adjusted R-squared applies a penalty for the number of predictors.

- **Source:** Penn State Eberly College of Science. STAT 501: Regression Methods (online course notes); Lesson 1, sections 1.5 and 1.6, and Lesson 10, section 10.3
- **URL:** <https://online.stat.psu.edu/stat501/Lesson01.html>
- **Supports:** R-squared is the regression sum of squares divided by the total sum of squares, a proportion between 0 and 1, read as the share of the variation in y explained by x; r is its square root.
- **Also:** Adjusted R-squared: Penn State Eberly College of Science. STAT 501: Regression Methods (online course notes); Lesson 10, section 10.3: R-squared can only increase as variables are added, and the adjusted value 'makes us pay a penalty for adding more predictors' (https://online.stat.psu.edu/stat501/Lesson10.html). Schneider A, Hommel G, Blettner M. Linear regression analysis: part 14 of a series on evaluation of scientific publications. Dtsch Arztebl Int, 2010;107(44):776–782 (https://pmc.ncbi.nlm.nih.gov/articles/PMC2992018/)
- **Checked:** 16.11.2026, passage read
- **Notes:** No cut-offs given: the source says what counts as large depends on the research area. The source warns that 'explained' does not mean caused; 'accounts for' was chosen for that reason and matches page 11's wording.

### `random-effect`

**Random effect.** The part of a mixed model that lets each patient, knee or other group differ from the average. With a random intercept, all of a patient's measurements are shifted up or down by that patient's own amount, and the model estimates how much these amounts vary between patients (a variance component).

- **Source:** statsmodels documentation, Linear Mixed Effects Models; opening section
- **URL:** <https://www.statsmodels.org/stable/mixed_linear.html>
- **Supports:** "Random intercepts models, where all responses in a group are additively shifted by a value that is specific to the group."
- **Also:** Schober P, Vetter TR. Repeated Measures Designs and Analysis of Longitudinal Data: If at First You Do Not Succeed—Try, Try Again. Anesth Analg 2018;127(2):569–575 (subject effects modeled "as if they randomly came from a probability distribution (random effects)"), https://pmc.ncbi.nlm.nih.gov/articles/PMC6072386/; Bates D, Mächler M, Bolker B, Walker S. Fitting Linear Mixed-Effects Models Using lme4. J Stat Softw 2015;67(1) (read as the lme4 package vignette), https://cran.r-project.org/web/packages/lme4/vignettes/lmer.pdf, section 2.2 (each level of the grouping factor has its own random intercept; the mean and standard deviation of these intercepts are estimated); Harrison XA, Donaldson L, Correa-Cano ME, et al. A brief introduction to mixed effects modelling and multi-model inference in ecology. PeerJ 2018;6:e4794 (random effects "allow the estimation of variance in the response variable within and among these groups"), https://pmc.ncbi.nlm.nih.gov/articles/PMC5970551/
- **Checked:** 16.11.2026, passage read
- **Notes:** Covers 'random effect(s)', 'random intercept' and 'variance component'. Random slopes are not mentioned because the site fits random intercepts only.

### `randomized-trial`

**Randomized trial.** A study in which chance, not the surgeon or the patient, decides which treatment each patient gets. Each treatment group is called an arm. Because of the random assignment the arms are alike on average at the start, even in characteristics nobody measured, so their outcomes can be compared directly to estimate the effect of the treatment.

- **Source:** Cochrane Community. Glossary. Cochrane; archived copy of community.cochrane.org/glossary (Internet Archive snapshot of 01.07.2019); entries "Randomised controlled trial", "Randomisation" and "Arm"
- **URL:** <https://web.archive.org/web/20190701142620/https://community.cochrane.org/glossary>
- **Supports:** Interventions are compared by being randomly allocated to participants; an arm is "a group of participants allocated a particular treatment".
- **Also:** Harrell FE. Glossary of Statistical Terms. Vanderbilt University, 26.04.2025; entry "clinical trial" (treatment choice is outside the control of physician and patient; randomization avoids selection bias from known and unknown factors). https://hbiostat.org/glossary/
- **Checked:** 16.11.2026, passage read
- **Notes:** Cochrane has retired its glossary page (community.cochrane.org/glossary now redirects to resources.cochrane.org, which points readers to archive.org), so the entry was read in the Internet Archive snapshot of 01.07.2019. "Alike on average" follows Haukoos and Lewis, JAMA 2015, and "compared directly" follows Austin 2011 (both cited under propensity-score, both read): random allocation leaves treatment unconfounded with measured and unmeasured baseline characteristics, so outcomes can be compared directly. The CONSORT 2010 explanation paper (BMJ 2010;340:c869) could not be opened (bmj.com refuses automated access), so it is not cited.

### `rank`

**Rank.** A value's position when all the values are sorted from lowest to highest. Tied values share the average of their positions.

- **Source:** GraphPad Software. GraphPad Prism 11 Statistics Guide (the guide the brief lists as Motulsky's); page "Interpreting results: Mann-Whitney test", sections "How it works" and "Tied values in the Mann-Whitney test"
- **URL:** <https://www.graphpad.com/guides/prism/latest/statistics/how_the_mann-whitney_test_works.htm>
- **Supports:** Values are ranked from low to high, the smallest getting rank 1; tied values "both are assigned the average of the two (or more) ranks for which they tie".
- **Also:** NIST/SEMATECH e-Handbook of Statistical Methods; section 7.2.6.2, "Definitions of order statistics and ranks" (the rank is a value's position in the data ordered by increasing magnitude). https://www.itl.nist.gov/div898/handbook/prc/section2/prc262.htm
- **Checked:** 16.11.2026, passage read
- **Notes:** Fully supported.

### `rank-biserial`

**Rank-biserial correlation.** An effect size for rank-based tests (Mann-Whitney, Wilcoxon signed-rank), from −1 to +1. For two groups, pair every patient in one group with every patient in the other: it is the share of pairs in which the first group's value is higher minus the share in which it is lower. For paired data, the changes are ranked by size, and it is the share of the rank total that belongs to the increases minus the share that belongs to the decreases.

- **Source:** Ben-Shachar MS, Lüdecke D, Makowski D, et al. effectsize: Indices of Effect Size (R package documentation), rank_biserial() help page; Details
- **URL:** <https://easystats.github.io/effectsize/reference/rank_biserial.html>
- **Supports:** "the correlation represents the difference between the proportion of favorable and unfavorable pairs / signed ranks (Kerby, 2014)"; values range from −1 to +1 (complete dominance of one sample).
- **Also:** Vallat R. pingouin documentation, pingouin.mwu(), Notes ("the difference between the proportion of favorable evidence minus the proportion of unfavorable evidence. Values range from -1 to 1"): https://pingouin-stats.org/generated/pingouin.mwu.html . Originals, not opened (as cited by effectsize): Cureton EE. Rank-biserial correlation. Psychometrika 1956;21(3):287–290; Kerby DS. The simple difference formula: an approach to teaching nonparametric correlation. Comprehensive Psychology 2014;3:11-IT.
- **Checked:** 16.11.2026, passage read
- **Notes:** Covers both site uses: two groups (page 6) and one sample or pairs (pages 5 and 7, where effectsize calls it the matched-pairs rank-biserial correlation). No cut-offs given; the pages quote 0.1/0.3/0.5, which neither opened source gives.

### `reference-group`

**Reference group.** The category of a categorical predictor that all the other categories are compared with, such as the standard implant or the control group. A model reports each other category's result relative to the reference group, so say which one it is.

- **Source:** Penn State Eberly College of Science. STAT 501: Regression Methods (online course notes); Lesson 8, section 8.4 (Coding qualitative variables)
- **URL:** <https://online.stat.psu.edu/stat501/Lesson08.html>
- **Supports:** Choose one group to be the reference group, such as a control group or the largest group; it has the value zero for all the indicator variables.
- **Also:** Schneider A, Hommel G, Blettner M. Linear regression analysis: part 14 of a series on evaluation of scientific publications. Dtsch Arztebl Int, 2010;107(44):776–782: 'the reference category should be defined first, and all other categories are to be considered in relation to this category' (https://pmc.ncbi.nlm.nih.gov/articles/PMC2992018/). R help page relevel: treatment contrasts 'take the first level as the reference' (https://stat.ethz.ch/R-manual/R-devel/library/stats/html/relevel.html)
- **Checked:** 16.11.2026, passage read
- **Notes:** Covers 'reference level' and 'reference category'. The pages' statement that R and Python take the first category alphabetically was not put in the definition: I confirmed only that R takes the first level (relevel help), not the alphabetical default or Python's rule. 'So say which one it is' follows the site (page 8) and Schneider's 'should be defined first'.

### `registry`

**Registry.** A systematic collection of data on the patients who have a certain kind of operation, such as joint replacement, kept by a hospital, a region or a country. A joint (arthroplasty) registry records the patient, the operation and the implant, and whether the joint is later revised. Registries are used for research, for improving quality and for finding implants that fail more often than others.

- **Source:** Hughes RE, Batra A, Hallstrom BR. Arthroplasty registries around the world: valuable sources of hip implant revision risk data. Current Reviews in Musculoskeletal Medicine, 2017;10(2):240 to 252; Introduction and "Registry concepts"
- **URL:** <https://doi.org/10.1007/s12178-017-9408-5>
- **Supports:** A registry is "a systematic collection of data on patient demographics, procedures, devices used, and outcomes"; arthroplasty registries "commonly use revision as an endpoint" and serve research, quality improvement and device surveillance.
- **Checked:** 16.11.2026, passage read
- **Notes:** Read through the PubMed Central page (PMC5435639) with a fetch tool that returns short quotes; the abstract was also read through PubMed. The source describes national, regional and institutional arthroplasty registries. It does not define disease registries, so the entry stays with operations. The standard general definition (Gliklich RE, Dreyer NA, Leavy MB, editors. Registries for Evaluating Patient Outcomes: A User's Guide. AHRQ) could not be opened (NCBI Bookshelf and the AHRQ site refused the fetch tool), so it is not cited. The source does not describe how a revision is linked to the first operation, so the entry does not say.

### `reliability`

**Reliability.** How well a measurement can tell patients apart despite measurement error: the real differences between patients compared with the differences between repeated readings. It depends on how varied the patients in the sample are, and is usually reported as an ICC. Inter-rater reliability compares different raters, intra-rater reliability the same rater on different occasions, and test-retest reliability the same measurement repeated under the same conditions.

- **Source:** de Vet HCW, Terwee CB, Knol DL, Bouter LM. When to use agreement versus reliability measures. J Clin Epidemiol 2006;59(10):1033–1039; abstract
- **URL:** <https://doi.org/10.1016/j.jclinepi.2005.10.015>
- **Supports:** "Reliability parameters assess whether study objects, often persons, can be distinguished from each other, despite measurement errors" and "are highly dependent on the heterogeneity of the study sample".
- **Also:** Koo TK, Li MY. A Guideline of Selecting and Reporting Intraclass Correlation Coefficients for Reliability Research. J Chiropr Med 2016;15(2):155–163; Table 2 (definitions of interrater, test-retest and intrarater reliability) and abstract (ICC as "a widely used reliability index"), https://pmc.ncbi.nlm.nih.gov/articles/PMC4913118/
- **Checked:** 16.11.2026, passage read
- **Notes:** Of de Vet et al. only the abstract was read (through PubMed); the full text is paywalled. SITE VS SOURCE: page 17 writes 'Intra-rater (test-retest) reliability' as if the two were the same. Koo & Li, the guide the page itself cites, define them separately: intra-rater is one rater across two or more trials; test-retest is one instrument on the same subject under the same conditions, typically where no rater is involved (a self-report questionnaire). Koo & Li also define reliability more loosely ('the extent to which measurements can be replicated'); the definition follows de Vet, which matches page 17's reliability-versus-agreement distinction.

### `reml`

**REML (restricted maximum likelihood).** The recommended way to fit a linear mixed model, and the default in R's lmer and in statsmodels. It is a variant of maximum likelihood that gives less biased estimates of the variances, such as how much patients differ from each other.

- **Source:** Harrison XA, Donaldson L, Correa-Cano ME, et al. A brief introduction to mixed effects modelling and multi-model inference in ecology. PeerJ 2018;6:e4794; section 'Stability of variance components and testing significance of random effects'
- **URL:** <https://pmc.ncbi.nlm.nih.gov/articles/PMC5970551/>
- **Supports:** REML (restricted/residual maximum likelihood) should be used to estimate the variance components of random effects in Gaussian models because it "produces less biased estimates compared to maximum likelihood".
- **Also:** lme4 documentation, lmer(): usage shows REML = TRUE as the default ("Fit a linear mixed-effects model (LMM) to data, via REML or maximum likelihood"), https://search.r-project.org/CRAN/refmans/lme4/html/lmer.html; statsmodels documentation, Linear Mixed Effects Models, https://www.statsmodels.org/stable/mixed_linear.html (the default fit prints "Method: REML")
- **Checked:** 16.11.2026, passage read
- **Notes:** The explanatory source is an ecology tutorial in a peer-reviewed journal (PeerJ, on PubMed Central); I found no medical tutorial that I could open which states the 'less biased variances' point. The lme4 paper (Bates et al. 2015) derives the REML criterion but does not give a plain-words reason. Agrees with page 16 ('the standard choice').

### `repeated-measures`

**Repeated measures.** The same outcome measured several times in the same patients, such as a score before surgery and at each follow-up visit. Measurements from one patient are more alike than measurements from different patients, so they are not independent and need a method that allows for this.

- **Source:** Schober P, Vetter TR. Repeated Measures Designs and Analysis of Longitudinal Data: If at First You Do Not Succeed—Try, Try Again. Anesth Analg 2018;127(2):569–575; abstract and introduction
- **URL:** <https://pmc.ncbi.nlm.nih.gov/articles/PMC6072386/>
- **Supports:** "values repeatedly measured in the same individual are usually more similar to each other than values from different individuals—and therefore are not independent"; appropriate analysis requires specific techniques.
- **Also:** Higgins JPT, Li T, Deeks JJ (editors). Chapter 6: Choosing effect measures and computing estimates of effect. Cochrane Handbook for Systematic Reviews of Interventions version 6.5 (2024); sections 6.2.1 and 6.2.4, https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-06
- **Checked:** 16.11.2026, passage read
- **Notes:** Defines the data structure only; 'repeated-measures ANOVA' has its own entry (batch S3).

### `repeated-measures-anova`

**Repeated-measures ANOVA.** ANOVA for three or more measurements on the same patients, such as a score at several visits, or on matched sets. It first sets aside the differences between patients, so that each patient serves as their own control, and then compares the means of the visits. It assumes sphericity and can use only patients measured at every visit.

- **Source:** GraphPad Software. GraphPad Prism 11 Statistics Guide; page 'Interpreting results: Repeated measures one-way ANOVA', with the pages 'What is repeated measures experimental design?' and 'Missing values in repeated measures ANOVA'
- **URL:** <https://www.graphpad.com/guides/prism/latest/statistics/anova_table.htm>
- **Supports:** Repeated-measures ANOVA compares the means of three or more matched groups and separates between-subject from within-subject variability; with a missing value, none of that subject's data can be used.
- **Also:** Pingouin documentation, pingouin.rm_anova; Notes (total variation split into effect, subjects and error; subjects with a missing value are removed), https://pingouin-stats.org/generated/pingouin.rm_anova.html ; GraphPad pages https://www.graphpad.com/guides/prism/latest/statistics/stat_what-is-repated-measures_.htm and https://www.graphpad.com/guides/prism/latest/statistics/stat_missing-values-in-repeated-mea.htm
- **Checked:** 16.11.2026, passage read
- **Notes:** Sphericity is its own entry. GraphPad notes that the same analysis is called a randomized block design when treatments are assigned within matched sets.

### `residual`

**Residual.** The difference between a patient's observed value and the value the model predicts for that patient: what is left over after the prediction. A residual plot shows the residuals against the predicted values to check the model's assumptions. The residual standard error estimates the standard deviation of the residuals: how far, typically, the observed values lie from the predictions.

- **Source:** Penn State Eberly College of Science. STAT 501: Regression Methods (online course notes); Lesson 1, sections 1.2 and 1.4, and Lesson 4, sections 4.1 and 4.2
- **URL:** <https://online.stat.psu.edu/stat501/Lesson01.html>
- **Supports:** The prediction error (residual) is the observed response minus the predicted response; S, the square root of the mean squared error, estimates sigma and is known as the residual standard error.
- **Also:** Residual plot: Penn State Eberly College of Science. STAT 501: Regression Methods (online course notes); Lesson 4: a residuals versus fits plot is used to detect non-linearity, unequal error variances and outliers (https://online.stat.psu.edu/stat501/Lesson04.html). Harrell FE. Glossary of Statistical Terms. Vanderbilt University, 26.04.2025; entry 'residual' (https://hbiostat.org/glossary/)
- **Checked:** 16.11.2026, passage read
- **Notes:** Schoenfeld residuals have their own entry. 'Typically' rests on the site's own SD entry (the typical distance of a value from the mean); the source says S estimates sigma, the SD of the errors around the line. 'Residual variance' on page 16 is the square of the same quantity; 'residual deviance' is in the deviance entry.

### `retrospective-study`

**Retrospective (and prospective) study.** A retrospective study uses data that already exist, such as records from routine care: the outcomes have already happened when the study starts. A prospective study is planned first, and the patients are then enrolled and followed forward in time. Both words are used in more than one way, so a paper should say how and when its data were collected.

- **Source:** Cochrane Community. Glossary. Cochrane; archived copy of community.cochrane.org/glossary (Internet Archive snapshot of 01.07.2019); entries "Retrospective study", "Prospective study" and "Cohort study"
- **URL:** <https://web.archive.org/web/20190701142620/https://community.cochrane.org/glossary>
- **Supports:** Retrospective: the outcomes have occurred before the study commenced, subjects identified from past records; prospective: people are followed forwards through time.
- **Also:** Harrell FE. Glossary of Statistical Terms. Vanderbilt University, 26.04.2025; entries "prospective study" (first designed, then subjects enrolled; intentional data collection) and "retrospective study". https://hbiostat.org/glossary/ . Vandenbroucke JP, von Elm E, Altman DG, et al. Strengthening the Reporting of Observational Studies in Epidemiology (STROBE): Explanation and Elaboration. PLoS Med, 2007;4(10):e297; item 4 (the terms are "ill defined"; authors should describe exactly how and when data collection took place). https://doi.org/10.1371/journal.pmed.0040297
- **Checked:** 16.11.2026, passage read
- **Notes:** Cochrane has retired its glossary page (community.cochrane.org/glossary now redirects to resources.cochrane.org, which points readers to archive.org), so the entry was read in the Internet Archive snapshot of 01.07.2019. The site's only use (getting-started/real-data.qmd: a retrospective study "uses data already collected during care") matches the usage STROBE lists second (timing of data collection relative to when the study was conceived). STROBE itself avoids both words; the third sentence reflects that.

### `reverse-kaplan-meier`

**Reverse Kaplan-Meier method (median follow-up).** A way to calculate the median follow-up, that is, how long patients were followed. It runs the Kaplan-Meier method with the roles swapped: a patient's observation ending without the event, at the close of the study or through loss to follow-up, counts as the event, and patients who had the event count as censored. When death is not the event studied, a death can count either way, as censored or as the end of follow-up; the two give different medians, so the Methods section says which was used. The plain median of all follow-up times comes out too short, because patients with an early event stop being followed early.

- **Source:** Clark TG, Bradburn MJ, Love SB, Altman DG. Survival Analysis Part I: Basic concepts and first analyses. British Journal of Cancer, 2003; section "Length of follow-up"
- **URL:** <https://doi.org/10.1038/sj.bjc.6601118>
- **Supports:** The reverse KM estimator is "the KM method with the event indicator reversed so that the outcome of interest becomes being censored"; the median follow-up of all patients tends to underestimate follow-up.
- **Also:** Schemper M, Smith TL. A note on quantifying follow-up in studies of failure time. Controlled Clinical Trials, 1996;17(4):343 to 346 (the original paper, cited by Clark et al.; not opened, no abstract on PubMed). https://doi.org/10.1016/0197-2456(96)00075-x . Betensky RA. Measures of follow-up in time-to-event studies: Why provide them and what should they be? Clinical Trials, 2015 (the median time to censoring "is not equivalent to the median observation time of all subjects"). https://doi.org/10.1177/1740774515586176
- **Checked:** 16.11.2026, passage read; 20.11.2026, Clark et al. section "Length of follow-up" re-read in full text (Europe PMC, PMC2394262), with section "Censoring makes survival analysis different" for what being censored means (close of the study, loss to follow-up, a different event). Computation on `data/cohort.csv` (R 4.6.0, survival 3.8.12): reverse Kaplan-Meier median 5.62 years with revisions and deaths censored (`event_status == 0` as the event), 5.00 years with a death counting as the end of follow-up (`event_status != 1` as the event), as page 13 prints.
- **Notes:** Clark et al. and Betensky read in full text through PubMed Central (PMC2394262, PMC4506242); Schemper and Smith could not be opened, so the method is described as Clark et al. describe it. Not confirmed by the opened sources: both describe a single event (death). The site (pages 13 and 18) also treats deaths as censored when the event of interest is revision; whether a death should count as censored or as the end of follow-up in the reverse analysis is not addressed in what I read, so I could not check the site's choice. Betensky adds that more than half of the trial reports surveyed gave a median follow-up without saying how it was calculated, which supports the site's advice to name the method. Reworded on 20.11.2026: "being censored counts as the event" read, on a revision analysis that censors deaths, as making deaths events too, which gives page 13's 5.00 years, not the 5.62 years page 13 reports. The definition now names the two kinds of censoring Clark et al. list besides a different event (close of the study, loss to follow-up) and says a death can count either way. That a death can count either way, and that the medians differ, rests on the computation above, not on a source; that the Methods should say which was used rests on Betensky (name how follow-up was calculated) and on page 13. Which choice is right is still not settled by the sources read.

### `risk`

**Risk.** The probability that an event, such as a revision or a death, happens within a stated period. It is estimated as the number of patients who had the event in that period divided by the number of patients at its start. That count gives the risk only when every patient was followed for the whole period: patients who left early are counted as if they never had the event. Otherwise the risk is estimated with the Kaplan-Meier method (1 minus the survival probability) or, with competing risks, as the cumulative incidence.

- **Source:** Higgins JPT, Li T, Deeks JJ (eds). Chapter 6: Choosing effect measures and computing estimates of effect. In: Cochrane Handbook for Systematic Reviews of Interventions, version 6.5. Cochrane, 2024; section 6.4.1.1, Risk and odds
- **URL:** <https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-06>
- **Supports:** "Risk describes the probability with which a health outcome will occur", usually written as a decimal between 0 and 1 or as a percentage.
- **Also:** Centers for Disease Control and Prevention. Principles of Epidemiology in Public Health Practice, 3rd ed.; Lesson 3, Section 2 (incidence proportion or risk: new cases "during a specified ... period of time" divided by the population at the start of the period). https://archive.cdc.gov/www_cdc_gov/csels/dsepd/ss1978/lesson3/section2.html ; Penn State Eberly College of Science. STAT 200: Elementary Statistics (online notes), Lesson 2: Describing Data, Part 1, Definition 2.5. https://online.stat.psu.edu/stat200/Lesson02
- **Checked:** 16.11.2026, passage read; 20.11.2026, CDC Lesson 3 Section 2 re-read ("The incidence proportion underestimates the true rate because it ignores persons lost to follow-up, and assumes that they remained disease-free for all four years"; person-time "can accommodate persons coming into and leaving the study"). For the methods named: Clark TG, Bradburn MJ, Love SB, Altman DG. Survival analysis part I. Br J Cancer 2003;89(2):232–238, sections "Kaplan–Meier survival estimate" (survival estimated from censored and uncensored times) and "Survival function of the ovarian data" ("The cumulative incidence at a time point is simply one minus the survival probability"), https://pmc.ncbi.nlm.nih.gov/articles/PMC2394262/ ; Austin PC, Lee DS, Fine JP. Circulation 2016;133(6):601–609 (with competing risks, the cumulative incidence function), https://pmc.ncbi.nlm.nih.gov/articles/PMC4741409/ , as recorded under `kaplan-meier` and `cumulative-incidence`
- **Notes:** The "within a stated period" part comes from the CDC text, not from Cochrane. Harrell's glossary gives a different strict meaning (probability of an adverse event times the severity of the loss) while noting that risk is often used as another name for probability; the site and Cochrane use the probability sense, so I defined that. The simple formula ignores censoring; where follow-up differs between patients the site uses Kaplan-Meier or cumulative incidence instead. Since 20.11.2026 (content review B25) the definition says so: the CDC passage supports that the count treats patients lost to follow-up as event-free; Clark et al. and Austin et al. support the two estimates named.

### `risk-difference`

**Risk difference.** The risk in one group minus the risk in the other, where each risk is the proportion of patients in that group who have the event. It can be written as a proportion or in percentage points.

- **Source:** Higgins JPT, Li T, Deeks JJ (editors). Chapter 6: Choosing effect measures and computing estimates of effect. In: Cochrane Handbook for Systematic Reviews of Interventions, version 6.5. Cochrane, 2024; section 6.4.1.4 "Measure of absolute effect: the risk difference"
- **URL:** <https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-06>
- **Supports:** "The risk difference is the difference between the observed risks (proportions of individuals with the outcome of interest) in the two groups".
- **Checked:** 16.11.2026, passage read
- **Notes:** Cochrane writes a risk difference as "0.02 (or 2%)"; the site reports it in percentage points, which is the same quantity. The scope note's "difference in proportions" is covered by the wording.

### `risk-ratio`

**Risk ratio (relative risk).** The risk in one group divided by the risk in the other. A risk ratio of 1 means the two risks are equal, and 3 means the event is three times as likely in the first group. It is not the same as an odds ratio; the two differ when the event is common.

- **Source:** Higgins JPT, Li T, Deeks JJ (editors). Chapter 6: Choosing effect measures and computing estimates of effect. In: Cochrane Handbook for Systematic Reviews of Interventions, version 6.5. Cochrane, 2024; sections 6.4.1.2 "Measures of relative effect: the risk ratio and odds ratio" and 6.4.1.3 "Warning: OR and RR are not the same"
- **URL:** <https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-06>
- **Supports:** "The risk ratio (RR, or relative risk) is the ratio of the risk of an event in the two groups"; a risk ratio of 3 means events are three times more likely.
- **Checked:** 16.11.2026, passage read
- **Notes:** The site also warns that a hazard ratio isn't a risk ratio (page 14). Cochrane chapter 6 does not make that comparison, so the definition mentions only the odds ratio; the hazard-ratio entry can carry the other warning.

### `robust`

**Robust.** Little affected by outliers or by data that do not quite meet a method's assumptions. The median is robust to a few extreme values and the mean is not; the t test and ANOVA are fairly robust to mild departures from a normal distribution, especially in large samples.

- **Source:** NIST/SEMATECH e-Handbook of Statistical Methods. National Institute of Standards and Technology; section 1.3.5.1, "Measures of Location"; accessed 16.11.2026
- **URL:** <https://www.itl.nist.gov/div898/handbook/eda/section3/eda351.htm>
- **Supports:** NIST: "robustness is a lack of susceptibility to the effects of nonnormality"; "Extreme values in the tails distort the mean. However, these extreme values do not distort the median".
- **Also:** Motulsky HJ. "Interpreting results: Normality tests". GraphPad Statistics Guide (Prism 11). GraphPad Software; accessed 16.11.2026 ("Statistical tests tend to be quite robust to mild violations of the Gaussian assumption"). https://www.graphpad.com/guides/prism/latest/statistics/stat_interpreting_results_normality.htm Also Motulsky HJ. "Analysis checklist: One-way ANOVA". GraphPad Statistics Guide (Prism 11). GraphPad Software; accessed 16.11.2026 (ANOVA is fairly robust to violations of a Gaussian distribution with large samples). https://www.graphpad.com/guides/prism/latest/statistics/stat_checklist_1wayanova.htm
- **Checked:** 16.11.2026, passage read
- **Notes:** Does not cover 'robust standard errors' (page 14, clustered Cox model), which is the name of a specific technique; link that phrase elsewhere or not at all. Harrell's glossary uses 'robust' in a third sense too (a result that survives a different analysis), not used on the site.

### `robust-standard-error`

**Robust standard error.** A standard error calculated in a way that stays valid when the observations are not independent, for example two joints from the same patient. Ordinary standard errors are then too small. The robust version, also called a sandwich or cluster-robust standard error, corrects this and leaves the estimate itself unchanged.

- **Source:** Naimi AI, Whitcomb BW. Simple Approaches for Dealing With Correlated Data. American Journal of Epidemiology, 2023;192(4):507 to 509
- **URL:** <https://doi.org/10.1093/aje/kwac221>
- **Supports:** "One key consequence of correlated outcomes is systematic underestimation of the standard errors"; "One simple way to account for clustering is to use robust standard errors", which gave the same estimate with a larger standard error.
- **Also:** Therneau TM. coxph: Fit Proportional Hazards Regression Model. R survival package help (a non-unique id "identifies clusters of correlated observations"; the robust variance is "known as the Huber sandwich estimator"). https://stat.ethz.ch/R-manual/R-devel/library/survival/html/coxph.html . Davidson-Pilon C. CoxPHFitter. lifelines documentation (robust: "the Huber sandwich estimator"; cluster_col "forces the sandwich estimator (robust variance estimator) to be used"). https://lifelines.readthedocs.io/en/latest/fitters/regression/CoxPHFitter.html
- **Checked:** 16.11.2026, passage read
- **Notes:** Naimi and Whitcomb read through the PubMed Central page (PMC10893847) with a fetch tool that returns short quotes; its volume and page numbers come from that tool's reading of the page. The article does not use the word "sandwich"; that name comes from the two software pages, which are the functions the site calls (page 14). Robust standard errors also protect against other wrong assumptions about the variance; the entry covers only the use the site makes of them, clustered observations. The tutorial I looked for first (Mansournia MA, et al. Reflection on modern methods: demystifying robust standard errors for epidemiologists. Int J Epidemiol 2021;50(1):346 to 351) could not be opened.

### `sample`

**Sample.** The patients (or hips, knees or measurements) that a study actually collected data on. They are one part of a larger population, and what is found in the sample is used to estimate what is true in that population.

- **Source:** Çetinkaya-Rundel M, Hardin J. Introduction to Modern Statistics, 2nd ed. OpenIntro, 2024; section 2.1.1, Populations and samples
- **URL:** <https://openintro-ims.netlify.app/data-design>
- **Supports:** Collecting data on a whole population is rarely feasible, so a sample is taken; "A sample is the data you have", and it is used to estimate the population average.
- **Also:** Penn State Eberly College of Science. STAT 200: Elementary Statistics (online notes), Lesson 1: Collecting Data; section 1.2, Definition 1.9 ("A subset of the population from which data are collected"). https://online.stat.psu.edu/stat200/Lesson01
- **Checked:** 16.11.2026, passage read
- **Notes:** Both sources opened and read. Sullivan & Artino 2013 (see likert-scale) says the same in one sentence. Defined for the scope note's sense only (the group studied), not "sample size" or code samples.

### `sample-size`

**Sample size (n).** The number of patients (or hips, knees or measurements) in a study or in one of its groups, written n. The larger the sample size, the more precise the estimates.

- **Source:** NIST/SEMATECH e-Handbook of Statistical Methods. National Institute of Standards and Technology, 2012; section 3.3.3.3, Selecting Sample Sizes
- **URL:** <https://www.itl.nist.gov/div898/handbook/ppc/section3/ppc333.htm>
- **Supports:** The variance of an estimate is proportional to the variability of the population divided by the sample size n; enough observations are needed for reasonably precise estimates.
- **Also:** Penn State Eberly College of Science. STAT 200: Elementary Statistics (online notes), Lesson 2: Describing Data, Part 1; section 2.1.1 ("n is the sample size"). https://online.stat.psu.edu/stat200/Lesson02 ; also Çetinkaya-Rundel M, Hardin J. Introduction to Modern Statistics, 2nd ed. OpenIntro, 2024, section 5.2 footnote ("The sample size was n = 50"). https://openintro-ims.netlify.app/explore-numerical
- **Checked:** 16.11.2026, passage read
- **Notes:** All three passages opened and read. No source states "patients, hips or knees"; that is the site's unit of counting, added as an example.

### `satterthwaite`

**Satterthwaite degrees of freedom.** A method for approximating the degrees of freedom of the t and F tests on a mixed model's fixed effects. In a mixed model these test statistics do not exactly follow a t or F distribution, so the method finds the degrees of freedom of one that comes close. R's lmerTest package uses it to give p-values.

- **Source:** Kuznetsova A, Brockhoff PB, Christensen RHB. lmerTest Package: Tests in Linear Mixed Effects Models. J Stat Softw 2017;82(13):1–26; abstract and section 2
- **URL:** <https://www.jstatsoft.org/article/view/v082i13>
- **Supports:** "Generally the t-statistic does not follow a t distribution"; a t distribution that approximates it is found with Satterthwaite's approximation to the degrees of freedom, which lmerTest implements for the t and F tests.
- **Also:** lmerTest package documentation (p-values "via Satterthwaite's degrees of freedom method"), https://search.r-project.org/CRAN/refmans/lmerTest/html/lmerTest-package.html. Original, not opened: Satterthwaite FE. An approximate distribution of estimates of variance components. Biometrics Bulletin 1946;2(6):110–114 (citation taken from the lmerTest paper's reference list)
- **Checked:** 16.11.2026, passage read
- **Notes:** The original 1946 paper was not opened; the definition rests on the lmerTest paper. Agrees with page 16 ('an approximation to how much information the estimate rests on').

### `scatter-plot`

**Scatter plot.** A plot of two variables against each other, one along each axis, with one point per patient. It shows whether and how the two are related, and whether any point lies far from the rest.

- **Source:** NIST/SEMATECH e-Handbook of Statistical Methods. National Institute of Standards and Technology, 2012; section 1.3.3.26, Scatter Plot
- **URL:** <https://www.itl.nist.gov/div898/handbook/eda/section3/scatterp.htm>
- **Supports:** "A scatter plot is a plot of the values of Y versus the corresponding values of X"; it reveals relationships between two variables and can show outliers.
- **Also:** Çetinkaya-Rundel M, Hardin J. Introduction to Modern Statistics, 2nd ed. OpenIntro, 2024; section 5.1 ("In any scatterplot, each point represents a single case"). https://openintro-ims.netlify.app/explore-numerical
- **Checked:** 16.11.2026, passage read

### `schoenfeld-residuals`

**Schoenfeld residuals.** Numbers used to check proportional hazards in a Cox regression. For each event and each predictor, the residual is the predictor's value in the patient who had the event minus the value the model expected. Plotted against time, after Grambsch and Therneau's rescaling, they should show no trend; a trend means the hazard ratio changes over time.

- **Source:** Bellera CA, MacGrogan G, Debled M, Tunon de Lara C, Brouste V, Mathoulin-Pélissier S. Variables with time-varying effects and the Cox model: some statistical concepts illustrated with a prognostic factor study in breast cancer. BMC Med Res Methodol 2010;10:20. doi:10.1186/1471-2288-10-20; Methods, section on Schoenfeld residuals
- **URL:** <https://pmc.ncbi.nlm.nih.gov/articles/PMC2846954/>
- **Supports:** "They are defined as the covariate value for the individual that failed minus its expected value"; a non-random pattern against time is evidence of non-proportionality.
- **Also:** Therneau T. R survival package, help page cox.zph, https://stat.ethz.ch/R-manual/R-devel/library/survival/html/cox.zph.html (scaled Schoenfeld residuals; the plot estimates the coefficient over time, a horizontal line if the assumption holds; score test for slope = 0). Original papers (not opened; bibliographic details checked in Crossref): Schoenfeld D. Partial residuals for the proportional hazards regression model. Biometrika 1982;69(1):239–241. https://doi.org/10.1093/biomet/69.1.239; Grambsch PM, Therneau TM. Proportional hazards tests and diagnostics based on weighted residuals. Biometrika 1994;81(3):515–526. https://doi.org/10.1093/biomet/81.3.515
- **Checked:** 16.11.2026, passage read
- **Notes:** Covers the surface form "Grambsch-Therneau": their paper is the reference the cox.zph help page gives for the scaled residuals and the test. Harrell's Regression Modeling Strategies course notes (hbiostat.org/rmsc/cox.html, section 20.6.2) say the same: "Grambsch and Therneau scale to yield estimates of β(t)". Also consistent with Bradburn et al. part III. Bellera et al. define the residual against "its expected value"; the site (page 14) describes this as comparing the revised patient with everyone still at risk, which matches but was not found word for word in an opened source. Read through the fetch tool's quotes of the page, not as full text.

### `scientific-notation`

**Scientific notation.** How software prints very small or very large numbers. 2.7e-08 means 2.7 with the decimal point moved 8 places to the left: 0.000000027.

- **Source:** Python Software Foundation. The Python Language Reference (Python 3.15), chapter 2, Lexical analysis; section "Floating-point literals"
- **URL:** <https://docs.python.org/3/reference/lexical_analysis.html#floating-point-literals>
- **Supports:** "The e or E represents 'times ten raised to the power of'": 1.166e-5 represents 1.166×10⁻⁵, or 0.00001166.
- **Also:** R Core Team. R documentation, help page "options" (base), entry scipen: R prints in "fixed or exponential notation" and prefers fixed "unless it is more than scipen digits wider". https://stat.ethz.ch/R-manual/R-devel/library/base/html/options.html . Also Python Software Foundation, The Python Standard Library, "Format Specification Mini-Language" ("the letter 'e' separating the coefficient from the exponent"). https://docs.python.org/3/library/string.html#format-specification-mini-language
- **Checked:** 16.11.2026, passage read
- **Notes:** Fully supported. Arithmetic checked: 2.7 × 10⁻⁸ = 0.000000027 (seven zeros after the decimal point, then 27). The sources say the software switches to this notation when the plain form would be longer, which is the case for very small and very large numbers.

### `score-test`

**Score test.** One of three standard tests of a model's coefficients, with the likelihood ratio test and the Wald test. It is calculated at the no-effect values of the coefficients, so it does not need the fitted estimates. For a Cox model that compares groups, it gives the same number as the log-rank test when no two events happen at the same time; with tied event times the two differ slightly, unless the Cox model handles ties with the exact method.

- **Source:** Therneau T. A package for survival analysis in R (vignette). R package survival, CRAN, 09.09.2026; section 2.6 (Differences in survival) and section 3.5.2 (Score tests)
- **URL:** <https://cran.r-project.org/web/packages/survival/vignettes/survival.pdf>
- **Supports:** The log-rank test is equivalent to the score test from a Cox model with the group as a factor variable.
- **Also:** R survival package, help page coxph.object: 'value of the efficient score test, at the initial value of the coefficients' (the default initial value is zero, help page coxph) (https://stat.ethz.ch/R-manual/R-devel/library/survival/html/coxph.object.html). Harrell FE. Regression Modeling Strategies (course notes). hbiostat.org; chapter 9 (by Chiara Di Gravio), sections 9.2 and 9.3: the likelihood ratio and Wald tests need all the parameters estimated (https://hbiostat.org/rmsc/mle.html)
- **Checked:** 16.11.2026, passage read; 20.11.2026, computation on `data/cohort.csv` (R 4.6.0, survival 3.8.12, lifelines 0.30.3). Implants A and C: `survdiff()` 20.53461818; `coxph()` score test 20.54045499 with `ties = "efron"` (R's default), 20.52666185 with `"breslow"`, 20.53461818 with `"exact"`. All three implants: `survdiff()` 33.46861907; score test 33.47853886 (Efron), 33.45548345 (Breslow), 33.46861907 (exact). With the A and C times made distinct (each repeated time shifted by a different millionth of a year): `survdiff()` and all three score tests 20.54680681. Vignette section "Tied times" (survival.Rnw in the installed package) describes the three methods.
- **Notes:** Page 8 says the Cox score test and the log-rank test agree to one decimal, not exactly, because they handle tied times differently. The vignette says 'equivalent' with no caveat about ties; I found no passage in the sources I opened that confirms or contradicts the page's explanation. Reworded on 20.11.2026 (content review B25) from the computation above: the score test equals the log-rank statistic with no tied event times and with the exact method, and differs slightly with Efron's or Breslow's method when times are tied. This is a statement about what R's survival package computes, checked on the site's data, not a quotation. That the score test needs no fitted estimates is drawn from two passages together (computed at the initial values; only LR and Wald are said to need the estimates), not from one sentence.

### `sensitivity-analysis`

**Sensitivity analysis.** A repeat of the main analysis with one choice changed, such as another method, another definition of the outcome or another way of handling missing data. If the result stays about the same, it does not depend on that choice.

- **Source:** Deeks JJ, Higgins JPT, Altman DG, et al (editors). Chapter 10: Analysing data and undertaking meta-analyses. In: Cochrane Handbook for Systematic Reviews of Interventions, version 6.5.1. Cochrane, 2026; section 10.14
- **URL:** <https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-10>
- **Supports:** "a repeat of the primary analysis ... in which alternative decisions or ranges of values are substituted for decisions that were arbitrary or unclear"
- **Also:** Vandenbroucke JP, von Elm E, Altman DG, et al. Strengthening the Reporting of Observational Studies in Epidemiology (STROBE): Explanation and Elaboration. PLoS Med, 2007;4(10):e297; items 12e and 17 (whether the main results are consistent with those from alternative analysis strategies or assumptions; examples include definitions of exposures or outcomes and the handling of missing data). https://doi.org/10.1371/journal.pmed.0040297
- **Checked:** 16.11.2026, passage read
- **Notes:** The Cochrane passage is written for systematic reviews; STROBE gives the same meaning for a single study. Fits the site's one use (page 14: a Fine-Gray model fitted as a sensitivity analysis). The sources call a result that survives "robust"; the definition avoids the word because the glossary's own "robust" entry is about methods.

### `shapiro-wilk-test`

**Shapiro-Wilk test.** A test of whether a sample could have come from a normal distribution. A small p-value is evidence that it did not. A large p-value does not prove that the data are normal: in small samples the test has little power to detect departures.

- **Source:** NIST/SEMATECH e-Handbook of Statistical Methods. National Institute of Standards and Technology; section 7.2.1.3, "Anderson-Darling and Shapiro-Wilk tests"; accessed 16.11.2026
- **URL:** <https://www.itl.nist.gov/div898/handbook/prc/section2/prc213.htm>
- **Supports:** NIST: the Shapiro-Wilk test "calculates a W statistic that tests whether a random sample ... comes from (specifically) a normal distribution. Small values of W are evidence of departure from normality".
- **Also:** Motulsky HJ. "Interpreting results: Normality tests". GraphPad Statistics Guide (Prism 11). GraphPad Software; accessed 16.11.2026 (a normality test cannot prove the data were sampled from a Gaussian distribution; with smaller data sets the tests don't have much power). https://www.graphpad.com/guides/prism/latest/statistics/stat_interpreting_results_normality.htm Original paper, as listed in the NIST Handbook's references (section 7.5) but not opened: Shapiro SS, Wilk MB. An analysis of variance test for normality (complete samples). Biometrika 1965;52(3 and 4): pages 591 to 611.
- **Checked:** 16.11.2026, passage read
- **Notes:** The second and third sentences come from Motulsky's page on normality tests in general (Prism's set includes Shapiro-Wilk). Page 3's other point, that in large samples the test flags departures too small to matter, is only hinted at by Motulsky ('The distribution could be close to Gaussian (with large data sets)') and is left to the page.

### `sign-test`

**Sign test.** A simple test for one group compared with a hypothetical value, or for two paired measurements, that uses only the direction of each difference: it counts the values above and the values below, and drops those exactly equal. If nothing differed, about half would fall on each side; a binomial test says how surprising the observed split is.

- **Source:** Whitley E, Ball J. Statistics review 6: Nonparametric methods. Crit Care 2002;6(6):509-513. doi:10.1186/cc1820; section 'The sign test'
- **URL:** <https://pmc.ncbi.nlm.nih.gov/articles/PMC153434/>
- **Supports:** The sign test gives each observation a + or - according to whether it is above or below a hypothesized value, drops exact ties, and takes exact P values from the Binomial distribution; it can also be used for paired data.
- **Also:** GraphPad Software. GraphPad Prism 11 Statistics Guide; page 'The binomial test' ('When the expected probability is 0.5, then the binomial test is the same as the sign test'), https://www.graphpad.com/guides/prism/latest/statistics/stat_binomial.htm ; statsmodels documentation, statsmodels.stats.descriptivestats.sign_test, https://www.statsmodels.org/stable/generated/statsmodels.stats.descriptivestats.sign_test.html
- **Checked:** 16.11.2026, passage read
- **Notes:** The site names the sign test on pages 5 and 7 as a binomial test on the counts above and below (or up and down) for ordinal scales; the source describes it the same way. The source also notes that the sign test has less power than the Wilcoxon signed-rank test because it ignores the size of the differences.

### `skewed`

**Skewed.** Lopsided: most values sit at one end and a long tail stretches out to the other.

- **Source:** NIST/SEMATECH e-Handbook of Statistical Methods; section 1.3.5.11, Measures of Skewness and Kurtosis
- **URL:** <https://www.itl.nist.gov/div898/handbook/eda/section3/eda35b.htm>
- **Supports:** Skewness is lack of symmetry; "skewed right means that the right tail is long relative to the left tail".
- **Also:** Çetinkaya-Rundel M, Hardin J. Introduction to Modern Statistics, 2nd ed. OpenIntro; section 5.3, Histograms and shape (most values are low and "only a handful" high: when a distribution "trails off to the right in this way and has a longer right tail, the shape is said to be right skewed"). https://openintro-ims.netlify.app/explore-numerical
- **Checked:** 16.11.2026, passage read
- **Notes:** Fully supported.

### `slope`

**Slope.** The steepness of a regression line: how much the outcome changes, on average, for each one-unit increase in the predictor. A positive slope means the outcome rises as the predictor rises, and a negative slope means it falls.

- **Source:** Penn State Eberly College of Science. STAT 501: Regression Methods (online course notes); Lesson 1, section 1.2 (What is the best fitting line?)
- **URL:** <https://online.stat.psu.edu/stat501/Lesson01.html>
- **Supports:** We can expect the mean response to increase or decrease by the slope for every one-unit increase in x; a positive trend gives a positive slope and a negative trend a negative slope.
- **Also:** Schneider A, Hommel G, Blettner M. Linear regression analysis: part 14 of a series on evaluation of scientific publications. Dtsch Arztebl Int, 2010;107(44):776–782: the slope of the regression line is the regression coefficient; a falling line has b < 0, a rising line b > 0 (https://pmc.ncbi.nlm.nih.gov/articles/PMC2992018/)
- **Checked:** 16.11.2026, passage read
- **Notes:** Regression slope only (also fits the Theil-Sen slope on page 11); the posterior tibial slope is anatomy and must not be linked.

### `cohen-benchmarks`

**Small, medium and large effects (Cohen's benchmarks).** Labels that call an effect size small, medium (or moderate) or large by comparing it with conventional cut-offs; the best known were proposed by Cohen. They are rules of thumb, not laws: Cohen meant them for use only when nothing better is known, and what counts as a large effect depends on the field and on what matters to patients.

- **Source:** Lakens D. Calculating and reporting effect sizes to facilitate cumulative science: a practical primer for t-tests and ANOVAs. Frontiers in Psychology, 2013;4:863; sections "Interpreting Cohen's d" and on eta squared
- **URL:** <https://doi.org/10.3389/fpsyg.2013.00863>
- **Supports:** The benchmarks suggested by Cohen "are arbitrary and should not be interpreted rigidly"; the only reason to use them is that findings cannot be compared with related findings (attributed to Cohen 1988).
- **Also:** Brydges CR. Effect Size Guidelines, Sample Size Calculations, and Statistical Power in Gerontology. Innovation in Aging, 2019 (Cohen "stated that these guidelines should only be used if estimates specific to the research area of interest are unknown"). https://doi.org/10.1093/geroni/igz036 . Ben-Shachar MS, Makowski D, Lüdecke D, et al. Automated Interpretation of Indices of Effect Size. effectsize package vignette ("such rules of thumb are just suggestions and there is nothing universal about them"). https://easystats.github.io/effectsize/articles/interpret.html . Schünemann HJ, Vist GE, Higgins JP, et al. Chapter 15: Interpreting results and drawing conclusions [last updated August 2023]. In: Cochrane Handbook for Systematic Reviews of Interventions version 6.5. Cochrane, 2024; section 15.5.3.1 ("patient importance of a finding is context-dependent"). https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-15
- **Checked:** 16.11.2026, passage read
- **Notes:** All four passages read in this session. Cohen's book (Statistical Power Analysis for the Behavioral Sciences, 2nd ed., 1988) could not be opened, so his caution is reported as Lakens and Brydges report it; his often quoted words ("much diffidence, qualifications, and invitations not to employ them if possible") turned up only in a search snippet and are not used. No cut-offs are given, as instructed. Three points where the site's pages go beyond what the opened sources attribute to Cohen: (1) page 9 applies 0.01, 0.06 and 0.14 to partial eta squared from a repeated-measures ANOVA, and Lakens says that using the benchmarks in designs with repeated measures "is not consistent with the considerations upon which the benchmarks were based"; (2) pages 5 and 9 apply 0.1, 0.3 and 0.5 to the rank-biserial correlation and to Kendall's W, for which I found no Cohen benchmark (the effectsize vignette labels Kendall's W with Landis and Koch's agreement scale and does not cover the rank-biserial correlation); (3) the effectsize vignette's own rule for omega squared (Cohen 1992: 0.02, 0.13, 0.26) differs from the site's 0.01, 0.06, 0.14, which match what Lakens gives as Cohen's eta squared benchmarks. The pages call all of these "a rough guide", which fits the sources.

### `spearman-correlation`

**Spearman correlation (ρ).** A rank-based correlation, ρ (rho), from −1 to +1: the Pearson correlation calculated on the ranks of the values instead of the values themselves. It says how consistently one variable rises (or falls) as the other rises, even along a curve, and it suits ordinal data and data that are not normally distributed.

- **Source:** R Core Team. R documentation, stats::cor (Correlation, Variance and Covariance); Details
- **URL:** <https://stat.ethz.ch/R-manual/R-devel/library/stats/html/cor.html>
- **Supports:** Spearman's rho is a rank-based measure of association, recommended when the data need not be bivariate normal; 'spearman' basically computes cor(R(x), R(y)), where R is the rank.
- **Also:** SciPy documentation, scipy.stats.spearmanr ('a nonparametric measure of the monotonicity of the relationship between two datasets', from -1 to +1), https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.spearmanr.html ; GraphPad Software. GraphPad Prism 11 Statistics Guide; page 'Interpreting results: Correlation' (same range as r; 'sometimes denoted by the Greek letter rho'), https://www.graphpad.com/guides/prism/latest/statistics/stat_interpreting_results_correlati.htm
- **Checked:** 16.11.2026, passage read
- **Notes:** Sourced from official software documentation (list 3): the Critical Care review on correlation does not cover Spearman, and BMJ's Statistics at Square One (chapter 11) returned HTTP 403. 'Even along a curve' paraphrases SciPy's 'monotonic'.

### `sphericity`

**Sphericity.** An assumption of repeated-measures ANOVA: the differences between any two visits have the same variance, whichever pair of visits you take. Mauchly's test checks it, and a small p-value suggests the assumption is violated. If it is violated and nothing is done about it, the p-value of the ANOVA comes out too small.

- **Source:** GraphPad Software. GraphPad Prism 11 Statistics Guide; page 'Sphericity and compound symmetry'
- **URL:** <https://www.graphpad.com/guides/prism/latest/statistics/stat_sphericity_and_compound_symmet.htm>
- **Supports:** Sphericity states that the variance of the differences between any two treatments is the same for every pair; if it is violated and not accounted for, the repeated measures ANOVA P value will be too small.
- **Also:** Mauchly's test: rstatix documentation, anova_test (sphericity is met when 'Mauchly's test is not significant, p > 0.05'), https://rpkgs.datanovia.com/rstatix/reference/anova_test.html ; Pingouin documentation, pingouin.sphericity ('Mauchly and JNS test for sphericity'), https://pingouin-stats.org/generated/pingouin.sphericity.html ; original paper as cited there, not opened: Mauchly JW. Significance test for sphericity of a normal n-variate distribution. Ann Math Stat 1940;11(2):204-209
- **Checked:** 16.11.2026, passage read
- **Notes:** Point of difference with the site: GraphPad (following Maxwell and Delaney) advises against using a test or the value of epsilon to decide whether to correct, and recommends not assuming sphericity at all for measurements repeated over time. The site's page 9 Methods sentence plans the Greenhouse-Geisser correction only if Mauchly's test shows a violation. The definition itself is neutral on this.

### `spline`

**Spline.** A flexible curve built from short curved pieces that join smoothly at points called knots. Putting a predictor into a model as a spline lets its effect bend where a single coefficient would force a straight line. A natural cubic spline, also called a restricted cubic spline, is kept straight beyond the outermost knots.

- **Source:** Harrell FE. Regression Modeling Strategies (course notes). hbiostat.org; chapter 2, sections 2.4.3 to 2.4.5
- **URL:** <https://hbiostat.org/rmsc/genreg.html>
- **Supports:** A spline function is a piecewise polynomial; cubic splines are smooth at the knots, where the pieces are joined; restricted cubic splines are constrained to be linear in the tails.
- **Also:** Natural = restricted: R package Hmisc, help page rcspline.eval: 'restricted cubic spline (natural spline)' (https://search.r-project.org/CRAN/refmans/Hmisc/html/rcspline.eval.html). R splines package, help page ns: 'natural cubic spline' (https://stat.ethz.ch/R-manual/R-devel/library/splines/html/ns.html)
- **Checked:** 16.11.2026, passage read
- **Notes:** 'Short curved pieces' stands for the source's piecewise (cubic) polynomials, to avoid 'polynomial'. Matches page 12's wording.

### `spread`

**Spread.** How far apart the values in a set of data lie, also called variability. The standard deviation, the interquartile range and the range (the largest value minus the smallest) each put a number on it.

- **Source:** NIST/SEMATECH. e-Handbook of Statistical Methods. National Institute of Standards and Technology, 2012; section 1.3.5.6 Measures of Scale
- **URL:** <https://www.itl.nist.gov/div898/handbook/eda/section3/eda356.htm>
- **Supports:** "A fundamental task in many statistical analyses is to characterize the spread, or variability, of a data set"; the measures listed include variance, standard deviation, range and interquartile range.
- **Checked:** 16.11.2026, passage read
- **Notes:** NIST treats "spread" and "variability" as the same thing, which matches the site ("similar spread", "share of the variation"). NIST does not use the word "variation"; the ANOVA pages use it for the same idea, measured as sums of squares. The definition names the range because NIST lists it; the site reports SD and IQR.

### `standard-deviation`

**Standard deviation (SD).** The typical distance of a value from the mean. A small SD means the values sit close together.

- **Source:** Çetinkaya-Rundel M, Hardin J. Introduction to Modern Statistics, 2nd ed. OpenIntro; section 5.4, Variance and standard deviation
- **URL:** <https://openintro-ims.netlify.app/explore-numerical>
- **Supports:** "The standard deviation represents the typical deviation of observations from the mean"; it "roughly describes how far away the typical observation is from the mean".
- **Also:** NIST/SEMATECH e-Handbook of Statistical Methods; section 1.3.5.6, Measures of Scale ("the standard deviation is the square root of the variance", and the variance is "roughly the arithmetic average of the squared distance from the mean"). https://www.itl.nist.gov/div898/handbook/eda/section3/eda356.htm . Also GraphPad Software. GraphPad Prism 11 Statistics Guide (the guide the brief lists as Motulsky's); page "The SD and SEM are not the same" (the SD "quantifies scatter — how much the values vary from one another"). https://www.graphpad.com/guides/prism/latest/statistics/stat_semandsdnotsame.htm
- **Checked:** 16.11.2026, passage read
- **Notes:** Fully supported; the source uses the same word, "typical". What a statistician would add: the SD is not the plain average distance from the mean but the square root of the average squared distance (NIST), which weights far-off values more; the source hedges with "roughly", the glossary does not.

### `standard-error`

**Standard error.** How much an estimate, such as a mean or a difference between two means, would vary from one sample to the next. It shrinks as the sample grows. It is not the SD, which describes how spread out the patients are.

- **Source:** Harrell FE. Glossary of Statistical Terms. Vanderbilt University School of Medicine, Department of Biostatistics, version of 26.04.2025, entry "standard error"
- **URL:** <https://hbiostat.org/glossary/>
- **Supports:** "The standard deviation of a statistical estimator"; standard errors describe precision, "not the variability across subjects", and go to zero as the sample size grows.
- **Also:** GraphPad Software. GraphPad Prism 11 Statistics Guide (the guide the brief lists as Motulsky's); pages "Key concepts: SEM" and "The SD and SEM are not the same" ("The SEM gets smaller as your samples get larger"; a standard error exists "for almost any parameter computed from a sample"). https://www.graphpad.com/guides/prism/latest/statistics/stat_semandsdnotsame.htm . Also Çetinkaya-Rundel M, Hardin J. Introduction to Modern Statistics, 2nd ed. OpenIntro; section 5.4 ("how much a sample mean varies from one sample to the next"). https://openintro-ims.netlify.app/explore-numerical
- **Checked:** 16.11.2026, passage read
- **Notes:** Fully supported, all three sentences. Could not open Altman and Bland's Statistics Note "Standard deviations and standard errors" (BMJ 2005;331:903); bmj.com and PubMed Central blocked automated access.

### `smd`

**Standardized mean difference (SMD).** The difference between two groups' means, divided by the standard deviation. It has no units and does not depend on the sample size, so in a Table 1 it shows how far apart two groups are on each baseline characteristic. Cohen's d and Hedges' g are versions of it.

- **Source:** Austin PC. An introduction to propensity score methods for reducing the effects of confounding in observational studies. Multivariate Behavioral Research, 2011;46(3):399–424; section "Balance diagnostics"
- **URL:** <https://pmc.ncbi.nlm.nih.gov/articles/PMC3144483/>
- **Supports:** The standardized difference compares the difference in means in units of the pooled standard deviation, is not influenced by sample size, and lets variables in different units be compared.
- **Also:** Higgins JPT, Li T, Deeks JJ (editors). Chapter 6: Choosing effect measures and computing estimates of effect. In: Cochrane Handbook for Systematic Reviews of Interventions, version 6.5. Cochrane, 2024; section 6.5.1.2 "The standardized mean difference" (the SMD expresses the effect relative to the between-participant variability; the version used in Cochrane reviews is Hedges' adjusted g): https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-06
- **Checked:** 16.11.2026, passage read
- **Notes:** Defined for the site's main use, balance in Table 1 (page 2). Austin also defines it for yes/no variables (difference between two proportions, standardized the same way); the definition leaves that out to stay short. The site's 0.1 rule of thumb is in Austin ("less than 0.1 has been taken to indicate a negligible difference", with no universally agreed threshold) and is left to the page.

### `statistical-significance`

**Statistically significant.** A result is called statistically significant when its p-value is below a threshold fixed before the analysis, the significance level or alpha, which is almost always 0.05 (the 5% level). It means the null hypothesis is rejected because data like these would be unusual if it were true. It does not mean that the difference is large or clinically important. A result that is not statistically significant does not show that there is no difference; the confidence interval shows which differences remain compatible with the data.

- **Source:** Motulsky HJ. "Statistical hypothesis testing". GraphPad Statistics Guide (Prism 11). GraphPad Software; accessed 16.11.2026
- **URL:** <https://www.graphpad.com/guides/prism/latest/statistics/statistical_hypothesis_testing.htm>
- **Supports:** Motulsky: define a threshold P value (alpha, almost always 0.05) before the experiment; if the P value is less than the threshold, reject the null hypothesis and call the difference statistically significant.
- **Also:** Harrell FE. Glossary of Statistical Terms. Vanderbilt University School of Medicine, Department of Biostatistics, 26.04.2025; entry "significance level" ("A preset value of alpha against which P-values are judged in order to reject H0"). https://hbiostat.org/glossary/ Also Motulsky HJ. "Interpreting results: P values from contingency tables". GraphPad Statistics Guide (Prism 11). GraphPad Software; accessed 16.11.2026 ("statistically significant" is not the same as "scientifically important"). https://www.graphpad.com/guides/prism/latest/statistics/stat_interpreting_results_contingen_2_2.htm
- **Checked:** 16.11.2026, passage read; 20.11.2026, two sentences added from these passages, both read: Greenland S, Senn SJ, Rothman KJ, Carlin JB, Poole C, Goodman SN, Altman DG. Statistical tests, P values, confidence intervals, and power: a guide to misinterpretations. Eur J Epidemiol 2016;31(4):337 to 350. doi:10.1007/s10654-016-0149-3, misinterpretation 6 ("it is a mistake to conclude from P > 0.05 that a study found 'no association' or 'no evidence' of an effect"), misinterpretation 4 (a nonsignificant result does not mean the test hypothesis is true), section on confidence intervals (they "allow one to shift focus away from the null hypothesis, toward the full range of effect sizes compatible with the data") and "The terms 'significance level' and 'alpha level' (α) are often used to refer to the cut-off", full text via Europe PMC, https://pmc.ncbi.nlm.nih.gov/articles/PMC4877414/ ; Altman DG, Bland JM. Absence of evidence is not evidence of absence. BMJ 1995;311(7003):485. doi:10.1136/bmj.311.7003.485 ("This term wrongly implies that the study has shown that there is no difference, whereas usually all that has been shown is an absence of evidence of a difference"), read for the content review (docs/audits/2026-11-20-content-review/sources.md, section 17)
- **Notes:** Covers 'significant', 'significance', 'significance level', 'the 5% level' and '0.05 threshold'. 'Clinically important' is this site's wording for Motulsky's 'scientifically important'. Harrell's entry on type I probability adds that declaring 'statistical significance' is 'not recommended', and GraphPad has a page advising to avoid the concept where possible; the definition explains the term without endorsing it. 'Alpha' was added to the name of the significance level and the last sentence on 20.11.2026 (content review B8); Motulsky's page also calls the threshold alpha.

### `stepwise-selection`

**Stepwise selection.** An automatic way to choose a model's predictors: software adds or removes one predictor at a time according to its p-value until none is left to add or remove. Its results are unreliable: the p-values of the final model come out too small, its confidence intervals can't be trusted, and predictors that are only noise often get in.

- **Source:** Harrell FE. Regression Modeling Strategies (course notes). hbiostat.org; chapter 4, section 4.3 (Variable selection)
- **URL:** <https://hbiostat.org/rmsc/multivar.html>
- **Supports:** Variable selection gives biased R-squared, coefficients and standard errors and P-values that are too small; confidence intervals after stepwise selection are not meaningful, and final models often contain noise.
- **Also:** The procedure: Penn State Eberly College of Science. STAT 501: Regression Methods (online course notes); Lesson 10, section 10.2 (Stepwise regression): predictors are entered and removed one at a time by their t-test p-values until no more can be (https://online.stat.psu.edu/stat501/Lesson10.html)
- **Checked:** 16.11.2026, passage read
- **Notes:** Sources disagree on whether to use it. Harrell rejects it, and pages 12 and 14 follow him. Penn State teaches it with a list of limitations, and Schneider et al. (Dtsch Arztebl Int 2010) recommend running forward and backward selection and trusting a model on which both agree, which Harrell calls fruitless (citing Wiegand 2010). Page 12's 'results that won't replicate' is the site's summary; Harrell's notes say the final model 'represented noise' 20% to 74% of the time in Derksen and Keselman's simulations.

### `stratification`

**Stratification.** Dividing the patients into groups (strata) that share a characteristic, such as the same surgical approach or the same matched set, and comparing only within each group before combining the results. A stratified Cox regression gives each stratum its own baseline hazard, so it gives no hazard ratio for the variable that defines the strata.

- **Source:** Bradburn MJ, Clark TG, Love SB, Altman DG. Survival analysis part II: multivariate data analysis – an introduction to concepts and methods. Br J Cancer 2003;89(3):431–436. doi:10.1038/sj.bjc.6601119; section "Stratified survival analysis"
- **URL:** <https://pmc.ncbi.nlm.nih.gov/articles/PMC2394368/>
- **Supports:** Groups are "compared within each stage of disease (the 'strata')" and "the differences within each stratum are then combined to give an overall comparison".
- **Also:** Therneau T. R survival package, help page coxph, version 3.8-6 ("A strata term identifies a stratified Cox model; separate baseline hazard functions are fit for each strata"), https://stat.ethz.ch/R-manual/R-devel/library/survival/html/coxph.html. Bradburn MJ, Clark TG, Love SB, Altman DG. Survival analysis part III: multivariate data analysis – choosing a model and assessing its adequacy and fit. Br J Cancer 2003;89(4):605–611. doi:10.1038/sj.bjc.6601120; section "Assessing whether PH is appropriate" (the stratifying covariate "has no estimated effect size"), https://pmc.ncbi.nlm.nih.gov/articles/PMC2376927/. Bellera CA, MacGrogan G, Debled M, Tunon de Lara C, Brouste V, Mathoulin-Pélissier S. Variables with time-varying effects and the Cox model: some statistical concepts illustrated with a prognostic factor study in breast cancer. BMC Med Res Methodol 2010;10:20. doi:10.1186/1471-2288-10-20 ("Each stratum k has a distinct baseline hazard but common values for the coefficient vector β"), https://pmc.ncbi.nlm.nih.gov/articles/PMC2846954/
- **Checked:** 16.11.2026, passage read
- **Notes:** The sources describe strata as the levels of a categorical variable (tumor stage in their example). Matched sets and patients as strata are the site's use (pages 7, 9 and 14); no source opened here discusses matched sets with a stratified Cox model. The site uses the word only for Cox regression and the log-rank setting, not for stratified randomization. Primary source read in full text.

### `sum-of-squares`

**Sum of squares.** A measure of variation: take the distance of each value from a mean, square it, and add up the squares. ANOVA splits the total sum of squares into a part between the groups and a part within the groups. A sum of squares divided by its degrees of freedom is a mean square, which is a variance.

- **Source:** GraphPad Software. GraphPad Prism 11 Statistics Guide; page 'Interpreting results: One-way ANOVA'; sections 'Sum-of-squares' and 'Mean squares'
- **URL:** <https://www.graphpad.com/guides/prism/latest/statistics/f_ratio_and_anova_table_(one-way_anova).htm>
- **Supports:** The total sum of squares is the sum of squared differences between each value and the grand mean; it splits into within-group and between-group parts, and each divided by its degrees of freedom gives a mean square, which can be thought of as a variance.
- **Also:** NIST/SEMATECH e-Handbook of Statistical Methods, section 7.4.3.1 'One-way ANOVA overview', https://www.itl.nist.gov/div898/handbook/prc/section4/prc431.htm ; Bewick V, Cheek L, Ball J. Statistics review 9: One-way analysis of variance. Crit Care 2004;8(2):130-136. doi:10.1186/cc2836 ('mean squares ... are obtained by dividing the sums of squares by their degrees of freedom'), https://pmc.ncbi.nlm.nih.gov/articles/PMC420045/
- **Checked:** 16.11.2026, passage read
- **Notes:** Covers 'mean square' as the scope note asks.

### `survival`

**Survival (survivorship).** The probability of not yet having had the event at a given time after the starting point, such as the date of surgery. When the event is revision, it is the share of implants still unrevised, also called survivorship. A survival curve plots this probability against time.

- **Source:** Clark TG, Bradburn MJ, Love SB, Altman DG. Survival analysis part I: basic concepts and first analyses. Br J Cancer 2003;89(2):232–238. doi:10.1038/sj.bjc.6601118; sections "Survival and hazard" and "Kaplan–Meier survival estimate"
- **URL:** <https://pmc.ncbi.nlm.nih.gov/articles/PMC2394262/>
- **Supports:** The survival probability "is the probability that an individual survives from the time origin (e.g. diagnosis of cancer) to a specified future time".
- **Checked:** 16.11.2026, passage read
- **Notes:** Clark et al. use "survivorship" as a plain synonym of survival ("the overall estimate of the survivorship"); that it is the usual word for implants is the site's wording (page 13, #survivorship), not a claim taken from the source. "Survival curve" is backed by the source's "a plot of the KM survival probability against time". "Revision-free survival" is the same thing with revision as the event. Primary source read in full text.

### `symmetric`

**Symmetric.** Looking the same on both sides of the center: the values lie about equally far below and above the middle. In a symmetric distribution the mean and the median sit in the same place, so the mean is a fair summary. The opposite is skewed.

- **Source:** NIST/SEMATECH. e-Handbook of Statistical Methods. National Institute of Standards and Technology, 2012; section 1.3.5.11 Measures of Skewness and Kurtosis
- **URL:** <https://www.itl.nist.gov/div898/handbook/eda/section3/eda35b.htm>
- **Supports:** "A distribution, or data set, is symmetric if it looks the same to the left and right of the center point"; skewness measures "the lack of symmetry".
- **Also:** Harrell FE. Glossary of Statistical Terms. Vanderbilt University, 26.04.2025; entry "mean" ("When the data distribution is symmetric, the population mean and median are the same"). https://hbiostat.org/glossary/
- **Checked:** 16.11.2026, passage read
- **Notes:** Both passages read in this session. The site always writes "roughly symmetric": real data are never exactly symmetric, and the entry can be linked from that phrase. "So the mean is a fair summary" is the site's own teaching conclusion (pages 2 and 4); the sources support it only through mean = median.

### `t-score`

**T-score.** A score rescaled so that the average of a reference population is 50 and the standard deviation is 10. PROMIS scores are T-scores, for most measures with the US general population as the reference, so a patient at 40 is 1 standard deviation below that average. It is unrelated to the t test.

- **Source:** HealthMeasures (Northwestern University). Interpret Scores, and Reference Populations. healthmeasures.net, page updated 2026
- **URL:** <https://healthmeasures.net/interpret-scores/>
- **Supports:** "A T-score transforms raw response scores into a scale with an average (mean) of 50 and standard deviation (SD) of 10"; 40 is one SD below the reference population's mean.
- **Also:** HealthMeasures. PROMIS Physical Function User Manual and Scoring Instructions, 24 Nov 2025; sections Direction of Scores, Reference Populations and T-score. https://healthmeasures.net/pdfs/PROMIS%20Physical%20Function%20User%20Manual%20and%20Scoring%20Instructions_24Nov2025.pdf ; reference populations (PROMIS adult measures: a sample representing the 2000 US census): https://healthmeasures.net/interpret-scores/reference-populations/
- **Checked:** 16.11.2026, passage read
- **Notes:** HealthMeasures is the official documentation of the PROMIS instruments (the brief's category 3, documentation for the method). Agrees with the site (page 9: "50 is the average of the US general population"). Not every PROMIS measure uses the general population (some use a clinical sample), hence "for most measures"; Physical Function does. The manual also says a higher T-score means more of the concept measured, so higher is better for function but worse for pain.

### `t-test`

**t test.** A test that compares means: one group's mean with a hypothetical value (one-sample t test), the means of two separate groups (unpaired t test), or two paired measurements (paired t test). Its test statistic, t, is the difference divided by its standard error: the further t is from 0, the smaller the p-value. Student's t test is also a name for t tests in general, but on this site it means the unpaired t test that assumes equal variances; the site's unpaired t tests are Welch's version, which does not make that assumption.

- **Source:** Whitley E, Ball J. Statistics review 5: Comparison of means. Crit Care 2002;6(5):424-428. doi:10.1186/cc1548; abstract and the sections on a single mean, paired data and unpaired data
- **URL:** <https://pmc.ncbi.nlm.nih.gov/articles/PMC137324/>
- **Supports:** The t-test compares a single mean with a hypothesized value, two paired means, or two unpaired means; t is the number of standard errors separating the two, and larger t gives smaller P.
- **Also:** GraphPad Software. GraphPad Prism 11 Statistics Guide; page 'Interpreting results: Unpaired t' (t ratio = difference between means divided by the standard error of the difference), https://www.graphpad.com/guides/prism/latest/statistics/how_the_unpaired_t_test_works2.htm ; Kim TK. T test as a parametric statistic. Korean J Anesthesiol 2015;68(6):540-546. doi:10.4097/kjae.2015.68.6.540 ('A t test is also known as Student's t test'), https://pmc.ncbi.nlm.nih.gov/articles/PMC4667138/
- **Checked:** 16.11.2026, passage read; 20.11.2026, the site's use checked in its own pages: Tests A–Z ("Student's t test: like the unpaired t test, but assumes equal spreads; use Welch's instead"), page 6 ("Student's or Welch's?"), the `equal-variances` and `welch-test` entries; no page runs `t.test(..., var.equal = TRUE)` or `equal_var=True` (searched in `en/`), and page 6 runs `t.test()` with R's default (Welch) and `ttest_ind(..., equal_var=False)`
- **Notes:** The name Student's t test is used in two ways: for t tests in general (Kim 2015; R's help page for t.test is titled 'Student's t-Test') and, when contrasted with Welch's, for the unpaired version that assumes equal variances. The site's Tests A-Z page uses the second sense. Until 20.11.2026 the definition gave only the general one ("Also called Student's t test"), which contradicted the site's other entries (content review C9); it now keeps the general use (Kim 2015) and says how this site uses the name, a statement about the site checked in its pages. For the paired test, 'the difference' is the mean of the within-pair differences (GraphPad, 'Interpreting results: Paired t', read).

### `table-1`

**Table 1.** The first table of most clinical papers, which describes the patients who were studied: age, sex and other characteristics, usually as recorded at baseline and shown for each group. It lets readers judge whether the patients resemble their own and how alike the groups were.

- **Source:** Hayes-Larson E, Kezios KL, Mooney SJ, Lovasi G. Who is in this study, anyway? Guidelines for a useful Table 1. J Clin Epidemiol, 2019;114:125; sections 1 and 2
- **URL:** <https://pmc.ncbi.nlm.nih.gov/articles/PMC6773463/>
- **Supports:** Papers often include a table describing the study sample, commonly the first table, colloquially called "Table 1"; it helps readers assess applicability and bias.
- **Also:** Vandenbroucke JP, von Elm E, Altman DG, et al. Strengthening the Reporting of Observational Studies in Epidemiology (STROBE): Explanation and Elaboration. PLoS Med, 2007;4(10):e297; item 14a (give the characteristics of study participants, by group; readers need them to judge generalisability). https://doi.org/10.1371/journal.pmed.0040297
- **Checked:** 16.11.2026, passage read
- **Notes:** Read through the PubMed full-text service (PMC6773463, doi 10.1016/j.jclinepi.2019.06.011). "At baseline" is the site's own point (page 2: Table 1 "usually holds the characteristics measured before surgery"); the paper speaks of "baseline demographics" but also allows other rows, hence "usually".

### `test-statistic`

**Test statistic.** A single number, such as t, U or χ², that a test calculates from the data to measure how far they are from "no difference".

- **Source:** Greenland S, Senn SJ, Rothman KJ, Carlin JB, Poole C, Goodman SN, Altman DG. Statistical tests, P values, confidence intervals, and power: a guide to misinterpretations. Eur J Epidemiol 2016;31(4):337 to 350; section "Statistical tests, P values, and confidence intervals: a caustic primer"
- **URL:** <https://doi.org/10.1007/s10654-016-0149-3>
- **Supports:** "the distance between the data and the model prediction is measured using a test statistic (such as a t-statistic or a Chi squared statistic)".
- **Also:** GraphPad Software. GraphPad Prism 11 Statistics Guide (the guide the brief lists as Motulsky's); page "Interpreting results: Mann-Whitney test" (U: "If the null hypothesis is true, then the value of U should be about half that value", the number of comparisons). https://www.graphpad.com/guides/prism/latest/statistics/how_the_mann-whitney_test_works.htm . Also Harrell FE. Glossary of Statistical Terms. Vanderbilt University School of Medicine, Department of Biostatistics, version of 26.04.2025, entry "P-value" ("a result (e.g., t or χ² statistics) as or more extreme than the observed statistic"). https://hbiostat.org/glossary/
- **Checked:** 16.11.2026, passage read
- **Notes:** Fully supported. One nuance for the examples: χ² grows the further the data are from "no difference", but t counts as far in either direction from 0, and U is far when it is well away from half the number of comparisons (GraphPad reports the smaller U, so a small U is the extreme one). "Measures how far" is right for all three; "larger means further" would not be.

### `theil-sen`

**Theil-Sen slope.** A slope calculated as the median of the slopes of the lines through every pair of points. It is a robust way to fit a line: a few outliers change it little. Sen's confidence interval is the confidence interval that goes with it.

- **Source:** The SciPy community. scipy.stats.theilslopes. SciPy v1.18.0 Manual; summary, Returns and Notes
- **URL:** <https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.theilslopes.html>
- **Supports:** theilslopes "implements a method for robust linear regression. It computes the slope as the median of all slopes between paired values"; it returns a confidence interval on the slope and follows Sen (1968).
- **Also:** Sen PK. Estimates of the regression coefficient based on Kendall's tau. Journal of the American Statistical Association, 1968;63:1379 to 1389 (the original paper, cited by the SciPy page; not opened).
- **Checked:** 16.11.2026, passage read
- **Notes:** The SciPy page was read; Sen's paper and Theil's (1950) were not opened, and their details are taken from the SciPy reference list. "A few outliers change it little" is my plain reading of SciPy's "robust linear regression"; the page shows an example with added outliers but does not put the claim in words. The site's statement that the confidence interval "comes from ranks" (page 11) fits the title of Sen's paper (Kendall's tau is a rank statistic) but was not checked against the paper itself.

### `tidy-data`

**Tidy data.** Data laid out so that every variable is a column, every observation is a row and every cell holds one value, with each kind of thing observed (patients, visits) in a table of its own. This standard layout is the one statistics software works with most easily.

- **Source:** Wickham H. Tidy Data. Journal of Statistical Software, 2014;59(10); abstract
- **URL:** <https://doi.org/10.18637/jss.v059.i10>
- **Supports:** "each variable is a column, each observation is a row, and each type of observational unit is a table"; tidy datasets are easy to manipulate, model and visualize.
- **Also:** Wickham H. Tidy data (vignette of the R package tidyr; the paper's text, kept current): each variable is a column, each observation is a row, each value is a cell. https://tidyr.tidyverse.org/articles/tidy-data.html
- **Checked:** 16.11.2026, passage read
- **Notes:** Only the abstract of the 2014 paper was read (on jstatsoft.org); the rules and the reasons were read in full in the tidyr vignette. Page 1 of the site gives the 2014 rules (third rule: each kind of observational unit gets its own table). The current tidyr vignette and R for Data Science (2nd edition, chapter 5) give the third rule as "each value is a cell" and treat one table per observational unit as a tidying step. The definition holds both, so it agrees with page 1 and with the current wording.

### `ties`

**Ties.** Two or more observations with exactly the same value. Rank-based tests give tied values the average of the ranks they share and then correct the test statistic for the ties. In survival analysis, tied times are events recorded at the same time, which Cox regression handles with an approximation such as Efron's method.

- **Source:** Motulsky HJ. "Interpreting results: Mann-Whitney test". GraphPad Statistics Guide (Prism 11). GraphPad Software; accessed 16.11.2026; section "Tied values in the Mann-Whitney test"
- **URL:** <https://www.graphpad.com/guides/prism/latest/statistics/how_the_mann-whitney_test_works.htm>
- **Supports:** Motulsky: when two or more values are the same they tie for the same rank and are assigned the average of the ranks for which they tie; the software corrects the statistic for ties.
- **Also:** Therneau T. survival package version 3.8-6, R documentation for coxph, argument ties and section "Ties" (three choices for handling tied event times; the Efron approximation is the default and more accurate with many ties). https://stat.ethz.ch/R-manual/R-devel/library/survival/html/coxph.html Same wording on ties for Kruskal-Wallis in Motulsky HJ. "Interpreting results: Kruskal-Wallis test". GraphPad Statistics Guide (Prism 11). GraphPad Software; accessed 16.11.2026. https://www.graphpad.com/guides/prism/latest/statistics/how_the_kruskal-wallis_test_works.htm
- **Checked:** 16.11.2026, passage read
- **Notes:** Covers 'tie(s)', 'tied values', 'tied scores' and 'tied times'. See the note under exact-test: the site's statements that R needs 'no ties' for an exact Wilcoxon p-value do not match R 4.6.

### `time-to-event`

**Time-to-event (survival) data.** Data that record how long it took until an event happened, such as the years from surgery to revision; the event need not be death. Some patients are censored, so their true time is unknown, and that is why these data need their own methods, together called survival analysis.

- **Source:** Clark TG, Bradburn MJ, Love SB, Altman DG. Survival analysis part I: basic concepts and first analyses. Br J Cancer 2003;89(2):232–238. doi:10.1038/sj.bjc.6601118; section Introduction
- **URL:** <https://pmc.ncbi.nlm.nih.gov/articles/PMC2394262/>
- **Supports:** The outcome is the time to an event; it is called survival time even when the event is relapse; unknown times at the end of follow-up make survival analysis necessary.
- **Also:** Austin PC, Lee DS, Fine JP. Introduction to the analysis of survival data in the presence of competing risks. Circulation 2016;133(6):601–609. doi:10.1161/CIRCULATIONAHA.115.017719; introduction ("We use the term survival data to refer to data in which the outcome variable denotes the time to the occurrence of the event of interest. Others refer to such data as time-to-event data"). https://pmc.ncbi.nlm.nih.gov/articles/PMC4741409/
- **Checked:** 16.11.2026, passage read
- **Notes:** Clark et al. give a second reason for special methods (the times are skewed); left out to keep the entry short. Covers the surface forms "survival analysis" and "survival data". Primary source read in full text.

### `tukey-hsd`

**Tukey's HSD.** Tukey's honestly significant difference test: a post-hoc test used after ANOVA that compares every pair of group means. Its p-values and confidence intervals are adjusted for all the pairs at once. It assumes that the groups have similar spreads.

- **Source:** GraphPad Software. GraphPad Prism 11 Statistics Guide; page 'Tukey and Dunnett tests in Prism'
- **URL:** <https://www.graphpad.com/guides/prism/latest/statistics/stat_the_methods_of_tukey_and_dunne.htm>
- **Supports:** "The Tukey test compares every mean with every other mean"; it is only a follow-up to ANOVA, its confidence intervals account for multiple comparisons, and it assumes populations with the same standard deviation.
- **Also:** NIST/SEMATECH e-Handbook of Statistical Methods, section 7.4.7.1 Tukey's method ("applies simultaneously to the set of all pairwise comparisons"), https://www.itl.nist.gov/div898/handbook/prc/section4/prc471.htm; R Core Team, TukeyHSD {stats} (intervals "with the specified family-wise probability of coverage"), https://stat.ethz.ch/R-manual/R-devel/library/stats/html/TukeyHSD.html; Lee S, Lee DK. What is the proper way to apply the multiple comparison test? Korean J Anesthesiol 2018;71(5):353–360, https://pmc.ncbi.nlm.nih.gov/articles/PMC6193594/
- **Checked:** 16.11.2026, passage read
- **Notes:** R's help calls it the 'Honest Significant Difference'; Lee & Lee and page 15 say 'honestly significant difference', which the definition follows. Tukey's original work was not consulted.

### `two-sided`

**Two-sided (and one-sided).** A two-sided (two-tailed) test counts a difference in either direction as evidence against the null hypothesis. A one-sided (one-tailed) test counts one direction only, which must be chosen before the data are seen; when the difference lies in that direction, its p-value is usually half the two-sided one. A one-sided confidence interval gives only a lower or only an upper limit.

- **Source:** Motulsky HJ. "One-tail vs. two-tail P values". GraphPad Statistics Guide (Prism 11). GraphPad Software; accessed 16.11.2026
- **URL:** <https://www.graphpad.com/guides/prism/latest/statistics/one-tail_vs__two-tail_p_values.htm>
- **Supports:** Motulsky: a two-tailed P value counts a difference with either group larger; a one-tail P value requires predicting the direction before collecting data and is half the two-tailed value with most tests; one-sided and two-sided mean the same as one- and two-tail.
- **Also:** Harrell FE. Glossary of Statistical Terms. Vanderbilt University School of Medicine, Department of Biostatistics, 26.04.2025; entries "two-sided test" and "one-sided test" (non-directional versus directional hypothesis; two-sided P-values are double the one-sided if the distribution of the test statistic is symmetric). https://hbiostat.org/glossary/ One-sided intervals: Motulsky HJ. "One sided confidence intervals". GraphPad Statistics Guide (Prism 11). GraphPad Software; accessed 16.11.2026 (expressed in only one direction, to either the lower or the upper confidence limit). https://www.graphpad.com/guides/prism/latest/statistics/one_sided_confidence_intervals.htm
- **Checked:** 16.11.2026, passage read
- **Notes:** The halving holds when the observed difference lies in the predicted direction (Motulsky) and the statistic's distribution is symmetric (Harrell); 'usually' stands for both conditions. Bland and Altman's BMJ note 'One and two sided tests of significance' (1994;309:248) would be a natural second source, but PubMed Central holds it only as a scanned page image and bmj.com returned 403, so it was not read.

### `unit-of-analysis`

**Unit of analysis.** The thing that counts as one observation in an analysis, usually one row of the data: a patient, a hip or knee, or a visit. When one patient supplies several rows, such as both knees, those rows are related, and an analysis that counts them as separate patients gives confidence intervals that are too narrow.

- **Source:** Higgins JPT, Li T, Deeks JJ (editors). Chapter 6: Choosing effect measures and computing estimates of effect. In: Cochrane Handbook for Systematic Reviews of Interventions, version 6.5. Cochrane, 2024; sections 6.2.1 and 6.2.7, MECIR Box 6.2.a
- **URL:** <https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-06>
- **Supports:** Several observations per person (repeated measurements, different body parts) are clustered; ignoring that gives confidence intervals that are too narrow.
- **Also:** Bryant D, Havey TC, Roberts R, Guyatt G. How many patients? How many limbs? Analysis of patients or limbs in the orthopaedic literature: a systematic review. J Bone Joint Surg Am, 2006;88(1):41 (abstract: two limbs or several joints of one person, analyzed as independent, give "false precision"). https://doi.org/10.2106/JBJS.E.00272 . Cochrane Community. Glossary. Cochrane; archived copy of community.cochrane.org/glossary (Internet Archive snapshot of 01.07.2019); entry "Unit of analysis error". https://web.archive.org/web/20190701142620/https://community.cochrane.org/glossary
- **Checked:** 16.11.2026, passage read
- **Notes:** No source opened gives a one-line definition of the term itself: Cochrane defines the error and discusses it for randomized trials (the analysis must match the unit that was randomized), and the first sentence is my plain-words reading of that plus Wickham's "an observation contains all values measured on the same unit (like a person, or a day, or a race)" (tidyr tidy-data vignette), which also covers "observational unit" on page 1. Only the abstract of Bryant 2006 was read (PubMed). The classic note, Altman DG, Bland JM. Units of analysis. BMJ 1997;314:1874, could not be opened (scanned PDF; bmj.com and the PMC PDF refuse automated access), so it is not cited as read.

### `variable`

**Variable.** A characteristic that is recorded for every patient and can differ from one patient to the next, such as age, sex or a score. In a data table each variable is one column.

- **Source:** Harrell FE. Glossary of Statistical Terms. Vanderbilt University School of Medicine, Department of Biostatistics, 2025 (hbiostat.org); entry "variable"
- **URL:** <https://hbiostat.org/glossary/>
- **Supports:** "variable: a characteristic of interest that you measure, record, and analyze."
- **Also:** Çetinkaya-Rundel M, Hardin J. Introduction to Modern Statistics, 2nd ed. OpenIntro, 2024; section 1.2.1 ("each column is referred to as a variable"). https://openintro-ims.netlify.app/data-hello ; Penn State Eberly College of Science. STAT 200: Elementary Statistics (online notes), Lesson 1: Collecting Data, Definition 1.2 ("Characteristic of cases that can take on different values"). https://online.stat.psu.edu/stat200/Lesson01
- **Checked:** 16.11.2026, passage read

### `variance`

**Variance.** The standard deviation squared. Tests such as ANOVA compare two variances, and the variances of separate sources of variation, such as differences between patients and measurement error, can be added up to give the total.

- **Source:** GraphPad Software. GraphPad Prism 11 Statistics Guide (the guide the brief lists as Motulsky's); page "Interpreting results: One-way ANOVA" (F ratio and ANOVA table), sections "Sum-of-squares" and "Mean squares"
- **URL:** <https://www.graphpad.com/guides/prism/latest/statistics/f_ratio_and_anova_table_(one-way_anova).htm>
- **Supports:** "the variance is the square of the standard deviation"; the sums of squares within and between groups add up to the total, but the two mean squares do "not add up".
- **Also:** NIST/SEMATECH e-Handbook of Statistical Methods; section 3.2.3.1, One-Way ANOVA (the test works "by comparing the within-level variancs to the between-level variance"), https://www.itl.nist.gov/div898/handbook/ppc/section2/ppc231.htm , and section 7.4.4, What are variance components? (the batch variance and the error variance are added to give the total variance: 11.71 ÷ (1.800 + 11.71) = 86.7%), https://www.itl.nist.gov/div898/handbook/prc/section4/prc44.htm
- **Checked:** 16.11.2026, passage read
- **Revised:** this entry existed before the source check; its wording was changed on that date to match the source.
- **Notes:** Sentence 1 is supported (GraphPad, NIST 1.3.5.6). In sentence 2, "ANOVA compares variances" is supported (NIST 3.2.3.1; GraphPad: the mean squares "can be thought of as variances"), but the reason given is not. GraphPad says what adds up in ANOVA is the sums of squares (within + between = total), and that the two variances the test compares, the mean squares, do "not add up to equal the total mean-square". What can be added up are the variances of separate sources of variation (NIST 7.4.4; page 16 adds 78.1 between knees and 73.5 within a knee). None of the sources I opened gives additivity as the reason ANOVA compares variances. "Sum of squares" is a glossary entry in this expansion.

### `wald-interval`

**Wald confidence interval.** The simplest kind of CI: the estimate plus and minus about 2 standard errors (1.96 for a 95% CI). For a ratio, such as an odds ratio or a hazard ratio, the calculation is done on the logarithm of the ratio and the limits are then converted back.

- **Source:** Harrell FE. Regression Modeling Strategies (course notes). Chapter 9, Overview of Maximum Likelihood Estimation; section 9.5, Confidence Intervals
- **URL:** <https://hbiostat.org/rmsc/mle.html>
- **Supports:** "The interval based on the Wald test is given by" the coefficient ± z × its standard error; likelihood ratio and score intervals "are computationally more intensive".
- **Also:** R Core Team. R documentation, help page "confint" (stats): "The default method is based on inverting the Wald test, assuming approximate normality of the estimator." https://stat.ethz.ch/R-manual/R-devel/library/stats/html/confint.html . Also Harrell FE. Biostatistics for Biomedical Research, section 6.10.1 ("Wald test is the easiest to compute but P-values and confidence intervals from it are not as accurate"). https://hbiostat.org/bbr/prop.html . Also Higgins JPT, Li T, Deeks JJ (editors). Chapter 6: Choosing effect measures and computing estimates of effect. In: Cochrane Handbook for Systematic Reviews of Interventions, version 6.5. Cochrane, 2024; sections 6.3.1 (a 95% CI is 2 × 1.96 = 3.92 standard errors wide) and 6.3.2 ("Analyses of ratio measures are performed on the natural log scale"). https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-06
- **Checked:** 16.11.2026, passage read
- **Revised:** this entry existed before the source check; its wording was changed on that date to match the source.
- **Notes:** Supported as written for a mean, a difference or a proportion (pages 4 and 6): simplest to compute, estimate ± 1.96 standard errors. Incomplete for the other place the site links it, the Wald CIs of odds ratios on pages 11 and 12 (and of hazard ratios). In Harrell's formula the estimate is the regression coefficient, which is the logarithm of the odds ratio, and Cochrane 6.3.2 says ratio measures are analyzed on the log scale: the ± is applied to the log and the limits are converted back, so the CI is not the odds ratio ± 2 standard errors (page 11: 1.22 to 1.86 is not symmetric around the odds ratio). Harrell's glossary makes the same point: CIs for odds ratios and other ratios are asymmetric. "Logarithm" is a glossary entry in this expansion. Could not open Brown, Cai and DasGupta 2001 or Agresti and Coull 1998 (the usual citations for the Wald interval of a proportion); Project Euclid and CORE blocked automated access.

### `wald-test`

**Wald test.** A test built from an estimate and its standard error: in its simplest form, the estimate divided by its standard error, compared with a normal distribution. The z and the p-value printed beside each coefficient of a logistic or Cox model are Wald tests. A Wald test can also test several coefficients at once.

- **Source:** Penn State Eberly College of Science. STAT 501: Regression Methods (online course notes); Lesson 13, section 13.2, 'Wald test'
- **URL:** <https://online.stat.psu.edu/stat501/Lesson13.html>
- **Supports:** The Wald test is the test of significance for individual coefficients in logistic regression: the estimate divided by its standard error, with a p-value from the standard normal curve.
- **Also:** Cox, and several coefficients at once: R survival package, help page summary.coxph (each coefficient's 'Wald statistic, and P value'; 'the overall likelihood ratio, score, and Wald test statistics for the model') (https://stat.ethz.ch/R-manual/R-devel/library/survival/html/summary.coxph.html). Harrell FE. Regression Modeling Strategies (course notes). hbiostat.org; chapter 9 (by Chiara Di Gravio), section 9.2 (https://hbiostat.org/rmsc/mle.html)
- **Checked:** 16.11.2026, passage read
- **Notes:** The Wald confidence interval keeps its existing entry (wald-interval). Harrell and the R help page coxph both warn that the Wald test fails when a coefficient is very large or infinite, while the likelihood ratio and score tests stay valid; not in the definition, but the pages could use it.

### `welch-test`

**Welch's t test.** A version of the unpaired t test that does not assume the two groups have equal variances (the same spread), as the classic version does. Its degrees of freedom are worked out from the data, so they are usually not a whole number. Welch's ANOVA does the same for three or more groups.

- **Source:** GraphPad Software. GraphPad Prism 11 Statistics Guide; page 'The unequal variance Welch t test'
- **URL:** <https://www.graphpad.com/guides/prism/latest/statistics/stat_the_unequal_variance_welch_t_t.htm>
- **Supports:** The Welch test does not assume the two populations have the same variance; its df come from a formula using both variances and are usually not an integer.
- **Also:** Welch's ANOVA: GraphPad Software. GraphPad Prism 11 Statistics Guide; page 'Interpreting results: Welch and Brown-Forsythe tests', https://www.graphpad.com/guides/prism/latest/statistics/interpreting_welch_browne-forsythe_tests.htm ; R Core Team. R documentation, stats::oneway.test (the Welch (1951) method 'generalizes the commonly known 2-sample Welch test to the case of arbitrarily many samples'), https://stat.ethz.ch/R-manual/R-devel/library/stats/html/oneway.test.html ; original paper, not opened: Welch BL. The generalisation of 'Student's' problem when several different population variances are involved. Biometrika 1947;34(1-2):28-35. doi:10.1093/biomet/34.1-2.28
- **Checked:** 16.11.2026, passage read
- **Notes:** Welch 1947 could not be opened; its citation was confirmed in PubMed (PMID 20287819) and the definition rests on the GraphPad and R pages, which were read. GraphPad also recommends Welch's test as the default, which matches the site's advice.

### `wilcoxon-signed-rank-test`

**Wilcoxon signed-rank test.** A rank-based (nonparametric) test that compares one group with a hypothetical value, or two paired measurements. It ranks the distances from the value (or the paired differences) by size, ignoring their direction, then compares the sum of the ranks above with the sum of the ranks below. It is not the Wilcoxon rank-sum test, which is another name for the Mann-Whitney test.

- **Source:** GraphPad Software. GraphPad Prism 11 Statistics Guide; page 'Interpreting results: Wilcoxon signed rank test', with the pages 'Results: Wilcoxon matched pairs test' and '"The Wilcoxon test" can refer to several statistical tests'
- **URL:** <https://www.graphpad.com/guides/prism/latest/statistics/stat_interpreting_results_wilcoxon_.htm>
- **Supports:** The test ranks the distances from the hypothetical median regardless of direction and sums the positive and the negative ranks; the matched-pairs version does the same with the paired differences.
- **Also:** Whitley E, Ball J. Statistics review 6: Nonparametric methods. Crit Care 2002;6(6):509-513. doi:10.1186/cc1820; section 'The Wilcoxon signed rank test', https://pmc.ncbi.nlm.nih.gov/articles/PMC153434/ ; GraphPad pages https://www.graphpad.com/guides/prism/latest/statistics/how_the_wilcoxon_matched_pairs_test_works.htm and https://www.graphpad.com/guides/prism/latest/statistics/stat_the_wilcoxon_test_can_refer_to.htm
- **Checked:** 16.11.2026, passage read
- **Notes:** Covers both uses on the site (page 5: one group against a value; page 7: paired). GraphPad adds that the test assumes the values are spread symmetrically around the median, which agrees with the site's remark about the pseudomedian. Values equal to the hypothetical value (or pairs with no difference) are dropped in Wilcoxon's original method; left to the pages.

### `wilson-interval`

**Wilson interval.** A confidence interval for a proportion, also called the Wilson score interval. It collects every candidate value of the true proportion that a test would not rule out given the observed proportion, working out the standard error from each candidate instead of from the sample. Unlike the simple Wald interval, its lower limit cannot fall below 0, and it works well for almost any sample size and proportion.

- **Source:** NIST/SEMATECH e-Handbook of Statistical Methods; section 7.2.4.1 "Confidence intervals" (with the test in section 7.2.4)
- **URL:** <https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm>
- **Supports:** The Wilson method inverts the test whose standard error uses the hypothesized proportion; its worth does not strongly depend on n or p, and its lower limit cannot be negative.
- **Also:** R Core Team. R documentation, stats::prop.test (R 4.6) ("The confidence interval is computed by inverting the score test"): https://stat.ethz.ch/R-manual/R-devel/library/stats/html/prop.test.html . SciPy documentation, BinomTestResult.proportion_ci (method "wilson"): https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats._result_classes.BinomTestResult.proportion_ci.html . Original, not opened (as cited by NIST, R and SciPy): Wilson EB. Probable inference, the law of succession, and statistical inference. Journal of the American Statistical Association 1927;22(158):209–212.
- **Checked:** 16.11.2026, passage read
- **Notes:** Page 4 says the interval "can never go below 0% or above 100%" and is "pulled a little toward 50%". NIST states only that the lower limit cannot be negative; the upper limit and the pull toward 50% are not stated in the sources I could open (Brown, Cai and DasGupta 2001, which NIST cites, was not reachable), so the definition claims only the lower limit. Both statements are true of the formula, but unconfirmed against a source here.

### `z-statistic`

**z statistic (z score).** A z score says how many standard deviations a value lies above or below the mean. A z statistic does the same for an estimate: it is the estimate minus the value expected under the null hypothesis, divided by its standard error, and the normal distribution turns it into a p-value. A test that works this way is called a z test.

- **Source:** Penn State Department of Statistics. STAT 200: Elementary Statistics (online course notes), Lesson 7; section 7.1, "Standard Normal Distribution"; accessed 16.11.2026, and the box "General Form of a Test Statistic" in the same lesson
- **URL:** <https://online.stat.psu.edu/stat200/Lesson07.html>
- **Supports:** Penn State: z = (x - mean) / standard deviation, so a z score of 1.333 is "1.333 standard deviations above the mean"; test statistic = (sample statistic - null parameter) / standard error, with the p-value taken from the standard normal (z) distribution.
- **Also:** Penn State Department of Statistics. STAT 200: Elementary Statistics (online course notes), Lesson 8; section 8.1, "One Sample Proportion"; accessed 16.11.2026 (the "z-test statistic tells us how far our sample proportion is from the hypothesized population proportion in standard error units"). https://online.stat.psu.edu/stat200/Lesson08.html
- **Checked:** 16.11.2026, passage read
- **Notes:** Covers 'z', 'z statistic', 'z score', 'z test' and 'standardized value'. On the site the z tests are mostly Wald tests of regression coefficients (estimate divided by standard error, null value 0) and Dunn's test; both fit the general form. The definition says 'normal distribution' for the source's 'standard normal distribution' because only the former is a glossary entry.
