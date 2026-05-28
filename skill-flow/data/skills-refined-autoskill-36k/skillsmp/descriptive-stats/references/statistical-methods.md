# Statistical Methods Reference

Detailed reference for statistical methods used in descriptive analysis.

## Table of Contents

- [Measures of Central Tendency](#measures-of-central-tendency)
- [Measures of Dispersion](#measures-of-dispersion)
- [Distribution Shape](#distribution-shape)
- [Normality Tests](#normality-tests)
- [Outlier Detection Methods](#outlier-detection-methods)
- [Group Comparison Tests](#group-comparison-tests)
- [Effect Sizes](#effect-sizes)

## Measures of Central Tendency

### Mean (Arithmetic Average)

**Formula:** μ = Σx / N (population) or x̄ = Σx / n (sample)

**When to use:**
- Data is normally distributed
- No extreme outliers
- Data is measured on interval or ratio scale

**Advantages:**
- Uses all data points
- Mathematically tractable
- Most efficient estimator for normal distributions

**Disadvantages:**
- Sensitive to extreme values
- Not appropriate for skewed distributions

**Python Implementation:**
```python
mean = series.mean()
```

### Median

**Definition:** The middle value when data is sorted (50th percentile)

**When to use:**
- Skewed distributions
- Presence of outliers
- Ordinal data

**Advantages:**
- Robust to outliers
- Appropriate for skewed data
- Always exists for real data

**Disadvantages:**
- Doesn't use all data information
- Less efficient for normal distributions
- Less mathematically tractable

**Python Implementation:**
```python
median = series.median()
```

### Mode

**Definition:** The most frequently occurring value(s)

**When to use:**
- Categorical/nominal data
- Discrete data
- Describing "typical" values

**Advantages:**
- Works with any data type
- Intuitive interpretation
- Actual observed value

**Disadvantages:**
- May not exist (all values unique)
- May have multiple modes
- Doesn't use all data information

**Python Implementation:**
```python
mode = series.mode()[0]  # First mode if multiple
```

### Geometric Mean

**Formula:** GM = (Πx)^(1/n)

**When to use:**
- All values are positive
- Data is multiplicative (growth rates, ratios)
- Log-normal distributions

**Python Implementation:**
```python
from scipy.stats import gmean
geometric_mean = gmean(series)
```

### Harmonic Mean

**Formula:** HM = n / Σ(1/x)

**When to use:**
- Rates and speeds
- Reciprocal data
- Average of ratios

**Python Implementation:**
```python
from scipy.stats import hmean
harmonic_mean = hmean(series)
```

## Measures of Dispersion

### Standard Deviation

**Formula:** σ = √(Σ(x-μ)²/N) (population) or s = √(Σ(x-x̄)²/(n-1)) (sample)

**When to use:**
- Normally distributed data
- With mean as measure of center
- Comparative analysis

**Interpretation:**
- Approximately 68% of data falls within μ ± 1σ
- Approximately 95% within μ ± 2σ
- Approximately 99.7% within μ ± 3σ

**Python Implementation:**
```python
std = series.std()  # Sample std (ddof=1)
std_pop = series.std(ddof=0)  # Population std
```

### Variance

**Formula:** σ² = Σ(x-μ)²/N or s² = Σ(x-x̄)²/(n-1)

**Interpretation:** Average squared deviation from the mean

**When to use:**
- ANOVA calculations
- When you need squared units
- Statistical inference

**Python Implementation:**
```python
variance = series.var()
```

### Range

**Formula:** Range = Max - Min

**Advantages:**
- Easy to calculate and understand
- Uses only two values

**Disadvantages:**
- Very sensitive to outliers
- Doesn't use information about distribution

**Python Implementation:**
```python
data_range = series.max() - series.min()
```

### Interquartile Range (IQR)

**Formula:** IQR = Q3 - Q1 (75th percentile - 25th percentile)

**When to use:**
- Skewed distributions
- With median as measure of center
- Outlier detection

**Advantages:**
- Robust to outliers
- Represents middle 50% of data

**Python Implementation:**
```python
from scipy.stats import iqr
iqr_value = iqr(series)
# Or:
iqr_value = series.quantile(0.75) - series.quantile(0.25)
```

### Coefficient of Variation (CV)

**Formula:** CV = (σ/μ) × 100%

**When to use:**
- Comparing variability across different datasets
- Different units of measurement
- Assessing relative variability

**Interpretation:**
- CV < 15%: Low variability
- CV 15-30%: Moderate variability
- CV > 30%: High variability

**Python Implementation:**
```python
cv = (series.std() / series.mean()) * 100
```

## Distribution Shape

### Skewness

**Definition:** Measure of asymmetry in the distribution

**Formula (Fisher's moment coefficient):**
```
Skewness = Σ(x-μ)³ / (n×σ³)
```

**Interpretation:**
- Skewness = 0: Symmetric distribution
- Skewness > 0: Right-skewed (positive skew, tail to right)
- Skewness < 0: Left-skewed (negative skew, tail to left)

**Guidelines:**
- |skewness| < 0.5: Approximately symmetric
- 0.5 ≤ |skewness| < 1: Moderately skewed
- |skewness| ≥ 1: Highly skewed

**Python Implementation:**
```python
from scipy.stats import skew
skewness = skew(series)
```

### Kurtosis

**Definition:** Measure of "tailedness" or "peakedness"

**Formula (Fisher's excess kurtosis):**
```
Kurtosis = Σ(x-μ)⁴ / (n×σ⁴) - 3
```

**Interpretation (excess kurtosis):**
- Kurtosis = 0: Normal distribution (mesokurtic)
- Kurtosis > 0: Heavy tails, sharp peak (leptokurtic)
- Kurtosis < 0: Light tails, flat peak (platykurtic)

**Python Implementation:**
```python
from scipy.stats import kurtosis
kurtosis_value = kurtosis(series, fisher=True)  # Excess kurtosis
```

## Normality Tests

### Shapiro-Wilk Test

**Best for:** Small to medium samples (n < 5000)

**Hypotheses:**
- H0: Data is normally distributed
- H1: Data is not normally distributed

**Test statistic:** W (ranges from 0 to 1, closer to 1 indicates normality)

**Interpretation:**
- p < α: Reject H0, data is not normally distributed
- p ≥ α: Fail to reject H0, data may be normally distributed

**Python Implementation:**
```python
from scipy.stats import shapiro
statistic, p_value = shapiro(series)
```

### Kolmogorov-Smirnov Test

**Best for:** Large samples (n ≥ 50)

**Hypotheses:**
- H0: Data follows specified distribution (e.g., normal)
- H1: Data does not follow specified distribution

**Advantages:**
- Works with any distribution
- Good for large samples

**Disadvantages:**
- Less powerful than Shapiro-Wilk for normality
- Sensitive to sample size

**Python Implementation:**
```python
from scipy.stats import kstest
statistic, p_value = kstest(series, 'norm', args=(series.mean(), series.std()))
```

### Anderson-Darling Test

**Best for:** Detecting deviations in distribution tails

**Hypotheses:**
- H0: Data comes from specified distribution
- H1: Data does not come from specified distribution

**Advantages:**
- More sensitive to tail differences
- More powerful than K-S test

**Python Implementation:**
```python
from scipy.stats import anderson
result = anderson(series, dist='norm')
# Compare statistic to critical_values at desired significance level
```

### D'Agostino's K² Test

**Best for:** Medium to large samples (n ≥ 20)

**Hypotheses:**
- H0: Data comes from a normally distributed population
- H1: Data does not come from a normally distributed population

**How it works:**
- Tests for skewness and kurtosis jointly
- More comprehensive than individual tests

**Python Implementation:**
```python
from scipy.stats import normaltest
statistic, p_value = normaltest(series)
```

## Outlier Detection Methods

### IQR Method

**Formula:**
- Lower bound = Q1 - k×IQR
- Upper bound = Q3 + k×IQR

**Common values for k:**
- k = 1.5: Mild outliers
- k = 3.0: Extreme outliers

**When to use:**
- Skewed distributions
- Non-normal data
- Robust outlier detection

**Python Implementation:**
```python
Q1 = series.quantile(0.25)
Q3 = series.quantile(0.75)
IQR = Q3 - Q1
lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR
outliers = series[(series < lower) | (series > upper)]
```

### Z-Score Method

**Formula:**
- Z = (x - μ) / σ
- Outlier if |Z| > threshold

**Common thresholds:**
- 2.5: Moderate
- 3.0: Standard (~99.7% confidence)
- 3.5: Conservative

**When to use:**
- Normally distributed data
- Mean as measure of center

**Limitations:**
- Sensitive to outliers themselves
- Assumes normality

**Python Implementation:**
```python
from scipy.stats import zscore
z_scores = np.abs(zscore(series))
outliers = series[z_scores > 3]
```

### Modified Z-Score Method

**Formula:**
- Modified Z = 0.6745 × (x - median) / MAD
- Where MAD = median(|x - median|)

**Advantages:**
- More robust than standard Z-score
- Uses median instead of mean
- Better for non-normal data

**Python Implementation:**
```python
median = series.median()
mad = np.median(np.abs(series - median))
modified_z_scores = 0.6745 * (series - median) / mad
outliers = series[np.abs(modified_z_scores) > 3.5]
```

## Group Comparison Tests

### Choosing the Right Test

```
                    2 Groups                    |                3+ Groups
---------------------------------------------------|----------------------------------------------
Normal distribution  |  Independent t-test       |        One-way ANOVA
Homogeneous variance |                           |
---------------------------------------------------|----------------------------------------------
Normal distribution  |  Welch's t-test           |        Welch's ANOVA
Heterogeneous variance |                          |
---------------------------------------------------|----------------------------------------------
Non-normal          |  Mann-Whitney U test      |        Kruskal-Wallis test
---------------------------------------------------|----------------------------------------------
Paired data         |  Paired t-test            |        Repeated measures ANOVA
---------------------------------------------------|----------------------------------------------
Categorical data    |  Chi-square test          |        Chi-square test
```

### Independent t-test

**Assumptions:**
1. Normality (both groups)
2. Homogeneity of variance (Levene's test)
3. Independence of observations

**Hypotheses:**
- H0: μ1 = μ2 (no difference in means)
- H1: μ1 ≠ μ2 (means differ)

**Python Implementation:**
```python
from scipy.stats import ttest_ind
statistic, p_value = ttest_ind(group1, group2, equal_var=True)
```

### Welch's t-test

**Assumptions:**
1. Normality (both groups)
2. Independence of observations
3. Does NOT assume equal variances

**When to use:**
- Normal distributions
- Variances are unequal (Levene's test significant)

**Python Implementation:**
```python
from scipy.stats import ttest_ind
statistic, p_value = ttest_ind(group1, group2, equal_var=False)
```

### Mann-Whitney U Test

**Assumptions:**
1. Independent observations
2. Ordinal or continuous data
3. Similar shaped distributions

**Hypotheses:**
- H0: Distributions are equal
- H1: Distributions differ

**Python Implementation:**
```python
from scipy.stats import mannwhitneyu
statistic, p_value = mannwhitneyu(group1, group2, alternative='two-sided')
```

### One-way ANOVA

**Assumptions:**
1. Normality (all groups)
2. Homogeneity of variance
3. Independence of observations

**Hypotheses:**
- H0: μ1 = μ2 = ... = μk (all means equal)
- H1: At least one mean differs

**Python Implementation:**
```python
from scipy.stats import f_oneway
statistic, p_value = f_oneway(group1, group2, group3)
```

### Kruskal-Wallis Test

**Assumptions:**
1. Independent observations
2. Ordinal or continuous data
3. Similar shaped distributions

**Hypotheses:**
- H0: All group distributions are equal
- H1: At least one distribution differs

**Python Implementation:**
```python
from scipy.stats import kruskal
statistic, p_value = kruskal(group1, group2, group3)
```

### Levene's Test

**Purpose:** Test for equality of variances (homoscedasticity)

**Hypotheses:**
- H0: All variances are equal
- H1: At least one variance differs

**Python Implementation:**
```python
from scipy.stats import levene
statistic, p_value = levene(group1, group2, group3)
```

## Effect Sizes

### Cohen's d

**Formula:** d = (μ1 - μ2) / σpooled

**Interpretation:**
- d = 0.2: Small effect
- d = 0.5: Medium effect
- d = 0.8: Large effect

**When to use:**
- Comparing two group means
- With t-tests

**Python Implementation:**
```python
import numpy as np
from scipy.stats import ttest_ind

def cohens_d(group1, group2):
    n1, n2 = len(group1), len(group2)
    var1, var2 = group1.var(), group2.var()
    pooled_std = np.sqrt(((n1-1)*var1 + (n2-1)*var2) / (n1+n2-2))
    return (group1.mean() - group2.mean()) / pooled_std
```

### Eta-Squared (η²)

**Formula:** η² = SSbetween / SStotal

**Interpretation:**
- η² = 0.01: Small effect
- η² = 0.06: Medium effect
- η² = 0.14: Large effect

**When to use:**
- ANOVA results
- Proportion of variance explained

### R (for Mann-Whitney)

**Formula:** r = Z / √N

**Interpretation:**
- r = 0.1: Small effect
- r = 0.3: Medium effect
- r = 0.5: Large effect

## References

- Field, A. (2013). Discovering statistics using IBM SPSS statistics.
- Shapiro, S. S., & Wilk, M. B. (1965). An analysis of variance test for normality.
- Cohen, J. (1988). Statistical power analysis for the behavioral sciences.
