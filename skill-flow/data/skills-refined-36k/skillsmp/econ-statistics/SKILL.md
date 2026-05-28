---
name: econ-statistics
description: Econometric analysis, statistical inference, and empirical economics. Use for regression, causal inference, IV, DID, RDD, time series, panel data, or hypothesis testing.
allowed-tools:
  - Read
  - Bash
  - Write
  - Edit
---

# Econometrics & Statistics

## Method Selection Decision Tree

```
Is treatment randomly assigned?
├── Yes → Simple comparison of means (RCT)
└── No → Is there a discontinuity?
    ├── Yes → RDD (regression discontinuity)
    └── No → Is there a policy change over time?
        ├── Yes → DID (difference-in-differences)
        └── No → Is there an instrument?
            ├── Yes → IV/2SLS
            └── No → Selection on observables?
                ├── Yes → Matching/Propensity score
                └── No → Bounds/Sensitivity analysis
```

## Regression Methods

### OLS
$$\hat{\beta} = (X'X)^{-1}X'y$$
- Assumes: $E[\varepsilon|X] = 0$ (exogeneity)
- Use: Descriptive analysis, correlations

### Instrumental Variables (IV/2SLS)
- **First stage**: $X = Z\pi + v$
- **Second stage**: $Y = X\hat{\beta} + \varepsilon$
- **Relevance**: $Cov(Z, X) \neq 0$ (F > 10)
- **Exclusion**: $Cov(Z, \varepsilon) = 0$

### GMM (Generalized Method of Moments)
$$\hat{\theta} = \arg\min_\theta g(\theta)' W g(\theta)$$
- Use: Over-identified models, panel data

## Causal Inference Checklist

### Difference-in-Differences (DID)
1. **Parallel trends**: Pre-treatment trends similar
2. **No anticipation**: Treatment effect starts at treatment
3. **SUTVA**: No spillovers between groups
4. **Common shocks**: Both groups affected equally by other factors

### Regression Discontinuity (RDD)
1. **Running variable**: Continuous, no manipulation
2. **Bandwidth selection**: Optimal vs robust
3. **Polynomial order**: Local linear preferred
4. **Density test**: McCrary test for sorting

### Synthetic Control
1. **Pre-treatment fit**: Good match in pre-period
2. **Donor pool**: Similar untreated units
3. **Placebo tests**: In-time and in-space

## Standard Errors Guide

| Data Structure | SE Type | Stata | Python (statsmodels) |
|----------------|---------|-------|----------------------|
| Cross-section | Robust (HC) | `robust` | `cov_type='HC3'` |
| Panel | Clustered | `cluster(id)` | `cov_type='cluster'` |
| Time series | HAC (Newey-West) | `newey` | `cov_type='HAC'` |
| Spatial | Conley | Custom | Custom |

### When to Cluster
- **Rule**: Cluster at the level of treatment assignment
- **Conservative**: Cluster at highest reasonable level
- **Few clusters (<50)**: Use wild bootstrap

## Hypothesis Testing

### Standard Tests
| Test | Null | Use |
|------|------|-----|
| t-test | $\beta = 0$ | Single coefficient |
| F-test | $R\beta = r$ | Joint hypothesis |
| Wald | $g(\theta) = 0$ | Nonlinear restrictions |
| LR | Restricted = Unrestricted | Model comparison |
| Hausman | RE consistent | FE vs RE |

### Multiple Testing Corrections
- **Bonferroni**: $\alpha/m$ (conservative)
- **Holm**: Step-down Bonferroni
- **FDR (BH)**: Controls false discovery rate
- **Westfall-Young**: Resampling-based

## Reporting Standards

### Regression Tables
1. Dependent variable clearly labeled
2. Sample size (N) for each column
3. R-squared or pseudo-R-squared
4. Standard errors in parentheses with type noted
5. Significance stars with legend (* p<0.1, ** p<0.05, *** p<0.01)
6. Control variables listed or noted

### Key Statistics to Report
- Point estimate and SE
- 95% confidence interval
- First-stage F (for IV)
- Pre-trend test p-value (for DID)
- Bandwidth and kernel (for RDD)

## Common Mistakes

1. **Forgetting to cluster**: Understates SEs
2. **p-hacking**: Pre-register analyses
3. **Weak instruments**: Check first-stage F
4. **Bad controls**: Don't control for post-treatment variables
5. **Wrong functional form**: Check linearity assumption
