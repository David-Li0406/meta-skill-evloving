# Mathematical Formulation: Adaptive Walk-Forward Epoch Selection

## 1. Walk-Forward Efficiency (WFE)

### Definition

```
WFE = SR_OOS / SR_IS
```

Where SR is the Sharpe Ratio:

```
SR = (μ - r_f) / σ
```

- μ = Mean return
- r_f = Risk-free rate (typically 0 for crypto)
- σ = Standard deviation of returns

### Statistical Properties

#### Sharpe Ratio Distribution (Lo, 2002)

Under normality assumptions:

```
SR ~ N(SR*, √((1 + SR*²/2) / T))
```

Where:

- SR\* = True Sharpe ratio
- T = Number of observations

#### Standard Error of Sharpe Ratio

```
SE(SR) ≈ √((1 + 0.5 × SR²) / T)
```

#### WFE Variance (Delta Method)

For WFE as ratio of two correlated random variables:

```
Var(WFE) ≈ WFE² × [Var(SR_OOS)/SR_OOS² + Var(SR_IS)/SR_IS² - 2×Cov(SR_OOS, SR_IS)/(SR_OOS × SR_IS)]
```

Assuming independence between IS and OOS:

```
Var(WFE) ≈ (SR_OOS/SR_IS)² × [(1 + 0.5×SR_OOS²)/T_OOS + (1 + 0.5×SR_IS²)/T_IS]
```

### Bias Characteristics

**WFE is NOT unbiased.**

1. **Ratio Bias**: E[X/Y] ≠ E[X]/E[Y] (Jensen's inequality)
2. **Selection Bias**: IS_Sharpe is inflated due to optimization
3. **Net Direction**: Typically downward bias (denominator inflated)

**First-Order Bias Correction**:

```
WFE_corrected ≈ WFE × (1 + Var(SR_IS) / SR_IS²)
```

## 2. WFE Aggregation Methods

### Method 1: Pooled WFE

```
WFE_pooled = Σ(T_OOS_i × SR_OOS_i) / Σ(T_IS_i × SR_IS_i)
```

**Properties**:

- Weights by sample size (precision)
- More stable than arithmetic mean
- Handles varying fold sizes well

### Method 2: Median WFE

```
WFE_median = median(WFE_1, WFE_2, ..., WFE_K)
```

**Properties**:

- Robust to outliers
- Breakdown point = 0.5
- Loses information from distribution tails

### Method 3: Inverse-Variance Weighted Mean

```
WFE_weighted = Σ(w_i × WFE_i) / Σ(w_i)

where w_i = 1 / Var(WFE_i) ≈ T_OOS_i × T_IS_i / (T_OOS_i + T_IS_i)
```

**Properties**:

- Optimal efficiency under homoscedasticity
- Downweights noisy estimates

## 3. WFE Distribution Under Null (No Skill)

Under H₀: SR_true = 0, both SR_IS and SR_OOS are sampling noise:

```
SR_IS ~ N(0, 1/√T_IS)
SR_OOS ~ N(0, 1/√T_OOS)
```

**WFE Distribution Under Null**:

The ratio of two independent standard normals follows a **Cauchy distribution**:

```
WFE | H₀ ~ Cauchy(0, √(T_IS/T_OOS))
```

**Critical Properties**:

- No defined mean or variance
- Heavy tails (extreme values common)
- Makes arithmetic mean unreliable

## 4. Deflated Sharpe Ratio (DSR)

### Formula

```
DSR = Φ[(SR - SR₀) × √(N-1) / √(1 + 0.5×SR² - γ₃×SR + (γ₄-3)/4×SR²)]
```

Where:

- Φ = Standard normal CDF
- SR₀ = Expected maximum Sharpe under null
- N = Sample size
- γ₃ = Skewness
- γ₄ = Kurtosis

### Expected Maximum Under Null

For K independent trials (Bailey & López de Prado, 2014):

```
SR₀ = √(2 × ln(K)) × (1 - γ / √(2 × ln(K)) - ln(ln(K) + ln(4π)) / (2 × √(2 × ln(K))))
```

Where γ ≈ 0.5772 (Euler-Mascheroni constant).

**Simplified approximation**:

```
SR₀ ≈ √(2 × ln(K)) - (γ + ln(π/2)) / √(2 × ln(K))
```

### Application to Epoch Selection

Total trials = K_epochs × F_folds

For 4 epochs × 31 folds = 124 trials:

```python
import math

K = 124
gamma = 0.5772  # Euler-Mascheroni

sr0 = math.sqrt(2 * math.log(K))
sr0 -= (gamma + math.log(math.pi / 2)) / math.sqrt(2 * math.log(K))
sr0 *= 0.3  # Typical SE(SR)

# sr0 ≈ 0.75
```

## 5. Efficient Frontier Formulation

### Pareto Dominance

Epoch A **dominates** Epoch B if:

```
WFE(A) ≥ WFE(B) AND Time(A) ≤ Time(B)
```

with at least one strict inequality.

### Efficient Frontier Set

```
Frontier = {e ∈ Epochs : ∄ e' ∈ Epochs s.t. e' dominates e}
```

### Selection from Frontier

**Weighted Score Method**:

```
Score(e) = w_wfe × norm(WFE(e)) + w_time × (1 - norm(Time(e)))
```

Where:

- norm(x) = (x - min) / (max - min) (min-max normalization)
- w_wfe = Weight for WFE (default: 1.0)
- w_time = Weight for time (default: 0.1)

**Knee-Point Method**:

Find epoch where marginal WFE gain per unit time decreases most sharply.

```
Knee = argmax_e |∂²WFE/∂Time²|
```

## 6. Stability Penalty Formulation

### Penalty Function

```
AdjustedWFE(e_t) = WFE(e_t) - λ × I(e_t ≠ e_{t-1})
```

Where:

- λ = Stability penalty coefficient (default: 0.1 × WFE_mean)
- I(·) = Indicator function (1 if condition true, 0 otherwise)

### Selection Rule

```
e_t* = argmax_e [WFE(e) - λ × I(e ≠ e_{t-1}*)]
```

Only change epochs if improvement exceeds penalty threshold.

### Alternative: Bayesian Shrinkage

```
e_t* = α × argmax_e WFE(e) + (1-α) × e_{t-1}*
```

With α ∈ [0, 1] controlling adaptation speed.

## 7. Effective Sample Size (N_eff)

### Reduction from Epoch Selection

```
N_eff = N_samples × selection_factor × correlation_factor
```

Where:

- selection_factor = 1 / √K_epochs
- correlation_factor = (1 - ρ) / (1 + ρ) (Kish's formula)
- ρ = Autocorrelation from carry-forward

### Example Calculation

For 31 folds, 4 epochs, autocorrelation 0.3:

```python
n_samples = 31
n_epochs = 4
autocorr = 0.3

selection_factor = 1 / math.sqrt(n_epochs)  # 0.5
correlation_factor = (1 - autocorr) / (1 + autocorr)  # 0.54

n_eff = n_samples * selection_factor * correlation_factor
# n_eff ≈ 8.4
```

**31 folds provide ~8 effective independent observations.**

## 8. Minimum Sample Size Requirements

### For Reliable WFE

For SE(WFE) < target precision ε:

```
T_OOS ≥ (1 + 0.5×SR²) / (ε/WFE)² - T_IS×(1 + 0.5×SR²) / T_IS
```

### Practical Minimums (20% precision)

| SR_IS | T_IS | Minimum T_OOS |
| ----- | ---- | ------------- |
| 0.5   | 252  | 47 days       |
| 1.0   | 252  | 56 days       |
| 1.5   | 252  | 69 days       |
| 2.0   | 252  | 88 days       |

### Rule of Thumb

- **Minimum**: T_OOS ≥ 63 trading days (1 quarter)
- **Recommended**: T_OOS ≥ 126 trading days (6 months)
- **Robust**: T_OOS ≥ 252 trading days (1 year)

## 9. Confidence Intervals for WFE

### Fieller's Method (Exact)

For WFE = SR_OOS / SR_IS:

```
CI = [WFE × (1 - z_α × CV_IS²) ± z_α × SE_ratio] / (1 - z_α² × CV_IS²)
```

Where:

- CV_IS = SE(SR_IS) / SR_IS
- SE_ratio = WFE × √(CV_OOS² + CV_IS² - 2×ρ×CV_OOS×CV_IS)

### Bootstrap Method (Recommended)

```python
def bootstrap_wfe_ci(
    returns_is,
    returns_oos,
    n_bootstrap=10000,
    alpha=0.05,
    annualization_factor=None,  # Use AWFESConfig.get_annualization_factor()
    is_threshold=None,          # Use compute_is_sharpe_threshold()
):
    """Bootstrap confidence interval for WFE.

    Args:
        annualization_factor: sqrt(periods_per_year). Use:
            - sqrt(365) for crypto_24_7 daily
            - sqrt(252) for equity/session-filtered daily
            - Or get from AWFESConfig.get_annualization_factor()
        is_threshold: Minimum IS Sharpe. Use compute_is_sharpe_threshold(n).
    """
    # Default to equity convention if not specified
    ann_factor = annualization_factor or np.sqrt(252)
    min_is = is_threshold or 0.1

    wfe_samples = []
    for _ in range(n_bootstrap):
        is_sample = np.random.choice(returns_is, size=len(returns_is), replace=True)
        oos_sample = np.random.choice(returns_oos, size=len(returns_oos), replace=True)

        sr_is = is_sample.mean() / is_sample.std() * ann_factor
        sr_oos = oos_sample.mean() / oos_sample.std() * ann_factor

        if sr_is > min_is:
            wfe_samples.append(sr_oos / sr_is)

    return np.percentile(wfe_samples, [100*alpha/2, 100*(1-alpha/2)])
```

## 10. Summary: Key Formulas

| Concept           | Formula                               |
| ----------------- | ------------------------------------- |
| WFE               | SR_OOS / SR_IS                        |
| SE(SR)            | √((1 + 0.5×SR²) / T)                  |
| Pooled WFE        | Σ(T_OOS × SR_OOS) / Σ(T_IS × SR_IS)   |
| DSR SR₀           | √(2×ln(K)) - (γ + ln(π/2))/√(2×ln(K)) |
| N_eff             | N × (1/√K) × ((1-ρ)/(1+ρ))            |
| Stability penalty | WFE - λ × I(change)                   |
