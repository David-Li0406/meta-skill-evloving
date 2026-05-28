# Statistical Analysis - Validations

## T-test Without Assumption Verification

### **Id**
ttest-without-assumption-check
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ttest_ind.*(?![\s\S]{0,300}shapiro|levene|normaltest)
  - ttest_rel.*(?![\s\S]{0,300}shapiro)
### **Message**
T-tests assume normality and equal variances. Verify assumptions.
### **Fix Action**
  Check assumptions:
  stats.shapiro(data)  # Normality
  stats.levene(group1, group2)  # Equal variances
  Or use Welch's t-test (default in scipy) or non-parametric alternatives.
  
### **Applies To**
  - **/*.py

## Statistical Test Without Effect Size

### **Id**
no-effect-size-reported
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ttest.*pvalue(?![\s\S]{0,200}cohen|effect|hedges)
  - mannwhitney.*pvalue(?![\s\S]{0,200}effect|rank)
### **Message**
Report effect sizes (Cohen's d, r, etc.) alongside p-values.
### **Fix Action**
  def cohens_d(g1, g2):
      return (g1.mean() - g2.mean()) / np.sqrt(((len(g1)-1)*g1.var() + (len(g2)-1)*g2.var()) / (len(g1)+len(g2)-2))
  
### **Applies To**
  - **/*.py

## Multiple Statistical Tests Without Correction

### **Id**
multiple-tests-no-correction
### **Severity**
error
### **Type**
regex
### **Pattern**
  - for.*ttest|ttest.*\n.*ttest.*\n.*ttest
  - p_values\.append.*for
### **Message**
Multiple tests inflate false positive rate. Apply correction.
### **Fix Action**
  from statsmodels.stats.multitest import multipletests
  reject, adjusted_p, _, _ = multipletests(p_values, method='fdr_bh')
  
### **Applies To**
  - **/*.py

## ANOVA Without Post-hoc Tests

### **Id**
anova-no-posthoc
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - f_oneway.*(?![\s\S]{0,500}tukey|bonferroni|posthoc)
### **Message**
Significant ANOVA requires post-hoc tests to identify which groups differ.
### **Fix Action**
  from statsmodels.stats.multicomp import pairwise_tukeyhsd
  tukey = pairwise_tukeyhsd(data, groups, alpha=0.05)
  
### **Applies To**
  - **/*.py

## Correlation Interpreted as Causation

### **Id**
correlation-as-causation
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - corr.*cause|correlation.*therefore
  - corr.*recommend.*intervention
### **Message**
Correlation does not imply causation. Consider confounders.
### **Applies To**
  - **/*.py
  - **/*.md

## Point Estimate Without Confidence Interval

### **Id**
no-confidence-interval
### **Severity**
info
### **Type**
regex
### **Pattern**
  - mean\(\).*print(?![\s\S]{0,100}ci|interval|±)
### **Message**
Report confidence intervals to show estimate precision.
### **Fix Action**
  from scipy import stats
  ci = stats.t.interval(0.95, len(data)-1, loc=np.mean(data), scale=stats.sem(data))
  
### **Applies To**
  - **/*.py

## Parametric Test With Small Sample

### **Id**
small-sample-parametric
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - len.*<.*20.*ttest|n.*=.*1\d.*ttest
### **Message**
Small samples may not meet parametric assumptions. Consider non-parametric tests.
### **Applies To**
  - **/*.py

## One-tailed Test Without Justification

### **Id**
wrong-test-direction
### **Severity**
info
### **Type**
regex
### **Pattern**
  - alternative.*=.*['"]less|alternative.*=.*['"]greater
### **Message**
One-tailed tests require a priori directional hypothesis. Document justification.
### **Applies To**
  - **/*.py

## Regression Without Diagnostics

### **Id**
regression-no-diagnostics
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - OLS.*fit\(\)(?![\s\S]{0,500}resid|heteroscedasticity|vif)
### **Message**
Check regression assumptions: normality, homoscedasticity, multicollinearity.
### **Fix Action**
  # Check residuals
  from statsmodels.stats.diagnostic import het_breuschpagan
  from statsmodels.stats.outliers_influence import variance_inflation_factor
  
### **Applies To**
  - **/*.py