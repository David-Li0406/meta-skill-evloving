# Statistical Analysis - Sharp Edges

## Shapiro-Wilk Paradox: Fails When You Need It Most

### **Id**
small-sample-normality
### **Severity**
critical
### **Summary**
Normality tests lack power for small samples - exactly when normality matters
### **Symptoms**
  - Shapiro-Wilk p > 0.05 with n=15
  - Using t-test because 'normality passed'
  - Non-significant test treated as proof of normality
### **Why**
  With small n, normality tests have low power - they often
  fail to reject even clearly non-normal data. With large n,
  they reject trivial deviations that don't affect t-test validity.
  
### **Gotcha**
  data = np.random.exponential(1, 20)  # Clearly non-normal
  stat, p = stats.shapiro(data)
  if p > 0.05:
      print("Data is normal!")  # WRONG - test has no power
  
### **Solution**
  1. Use Q-Q plots for visual inspection
  2. For small n, prefer robust/non-parametric methods
  3. For large n, visual check matters more than test
  4. Non-significant ≠ evidence of normality
  
### **Detection Pattern**
shapiro.*if.*p.*>|normaltest.*>.*0\.05

## Hidden Confounders in Every Correlation

### **Id**
correlation-causation
### **Severity**
critical
### **Summary**
High correlations can be entirely spurious due to confounding
### **Symptoms**
  - High correlation between X and Y
  - Recommending intervention on X to change Y
  - No consideration of confounding variables
### **Why**
  Shoe size correlates with reading ability (r≈0.7).
  Cause: Age affects both. In complex systems, confounders
  are often unmeasured or unknown.
  
### **Solution**
  1. Draw causal diagram (DAG) before analysis
  2. For causal claims, use experimental designs
  3. For observational data, use causal inference methods
  4. State limitations explicitly
  
### **Detection Pattern**
corr.*cause|correlation.*recommend

## Wrong Test Type: Paired vs Independent

### **Id**
paired-vs-independent
### **Severity**
high
### **Summary**
Using independent test on paired data loses power; vice versa inflates errors
### **Symptoms**
  - Pre-post measurements analyzed as independent
  - Same subjects in both conditions analyzed independently
### **Gotcha**
  before = measure_subjects(subjects)
  after = measure_subjects(subjects)  # SAME subjects
  ttest_ind(before, after)  # WRONG - loses power
  
### **Solution**
  Same subject at different times → Paired (ttest_rel)
  Random samples from populations → Independent (ttest_ind)
  
### **Detection Pattern**
ttest_ind.*before.*after

## ANOVA Says 'Different' But Not 'Which Ones'

### **Id**
anova-without-posthoc
### **Severity**
high
### **Summary**
Significant ANOVA requires post-hoc tests to identify which pairs differ
### **Symptoms**
  - ANOVA p < 0.05, then directly comparing specific pairs
  - Multiple t-tests after ANOVA without correction
### **Solution**
  Use post-hoc tests: Tukey HSD, Bonferroni, or Dunnett
  from statsmodels.stats.multicomp import pairwise_tukeyhsd
  
### **Detection Pattern**
f_oneway.*ttest_ind

## Regression Extrapolation: Monsters Beyond the Data

### **Id**
regression-extrapolation
### **Severity**
high
### **Summary**
Predictions outside observed range can be wildly wrong
### **Symptoms**
  - Predicting beyond range of training data
  - Model used for forecasting far into future
### **Solution**
  1. Only predict within observed data range
  2. If extrapolation needed, use uncertainty bounds
  3. Consider non-linear models that asymptote appropriately
  
### **Detection Pattern**
predict.*outside|forecast.*beyond

## Simpson's Paradox: Aggregation Reverses Effect

### **Id**
simpson-paradox
### **Severity**
high
### **Summary**
A trend in aggregated data can reverse when stratified
### **Symptoms**
  - Treatment looks better overall but worse in every subgroup
  - Opposite conclusions from aggregate vs stratified analysis
### **Solution**
  1. Always stratify by potential confounders
  2. Use regression to control for confounders
  3. Report both aggregate and stratified results
  
### **Detection Pattern**
groupby.*mean(?!.*stratif)

## Base Rate Neglect: The Prosecutor's Fallacy

### **Id**
base-rate-neglect
### **Severity**
medium
### **Summary**
P(A|B) ≠ P(B|A) - ignoring base rates gives wrong probabilities
### **Symptoms**
  - Confusing sensitivity with positive predictive value
  - Test 99% accurate → 99% confident in positive result
### **Why**
  99% accurate test for 1/1000 disease: positive predictive
  value is only ~9%, not 99%. Most positives are false positives.
  
### **Solution**
  Use Bayes' theorem. Report PPV and NPV, not just sensitivity.
  
### **Detection Pattern**
sensitivity.*accurate

## Relative vs Absolute Risk Confusion

### **Id**
ratio-interpretation
### **Severity**
medium
### **Summary**
50% relative risk reduction can be 0.1% absolute reduction
### **Symptoms**
  - Drug reduces risk by 50%!
  - Ignoring baseline risk in relative measures
### **Solution**
  Always report absolute risk and NNT alongside relative risk.
  
### **Detection Pattern**
relative.*risk.*without