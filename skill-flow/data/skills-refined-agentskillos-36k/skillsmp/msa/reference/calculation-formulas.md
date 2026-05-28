# MSA Calculation Formulas Reference

## Gage R&R - X-bar/R Method

### Study Constants

#### K₁ - Repeatability Factor (Based on Trials)

| Trials (r) | K₁ |
|------------|-----|
| 2 | 4.56 |
| 3 | 3.05 |

#### K₂ - Reproducibility Factor (Based on Operators)

| Operators (o) | K₂ |
|---------------|-----|
| 2 | 3.65 |
| 3 | 2.70 |

#### K₃ - Part Variation Factor (Based on Parts)

| Parts (n) | K₃ |
|-----------|-----|
| 5 | 2.08 |
| 6 | 1.93 |
| 7 | 1.82 |
| 8 | 1.74 |
| 9 | 1.67 |
| 10 | 1.62 |

---

### Step-by-Step Calculations

#### Step 1: Calculate Ranges

For each part and operator:
```
Range = Max(trials) - Min(trials)
```

Example for Part 1, Operator A with 3 trials (5.2, 5.3, 5.1):
```
Range = 5.3 - 5.1 = 0.2
```

#### Step 2: Calculate Average Range (R̄)

```
R̄ = Sum of all ranges / (n × o)

Where:
n = number of parts
o = number of operators
```

#### Step 3: Calculate Repeatability (EV)

```
EV = R̄ × K₁

Where:
K₁ = factor based on number of trials
```

#### Step 4: Calculate Operator Averages

```
X̄_operator = Sum of all measurements by operator / (n × r)

Where:
n = number of parts
r = number of trials
```

#### Step 5: Calculate X̄_diff

```
X̄_diff = Max(X̄_operators) - Min(X̄_operators)
```

#### Step 6: Calculate Reproducibility (AV)

```
AV = √[(X̄_diff × K₂)² - (EV²/(n×r))]

Where:
K₂ = factor based on number of operators
n = number of parts
r = number of trials

NOTE: If the value under the square root is negative, AV = 0
```

#### Step 7: Calculate GR&R

```
GR&R = √(EV² + AV²)
```

#### Step 8: Calculate Part Averages

```
X̄_part = Sum of all measurements for part / (o × r)

Where:
o = number of operators
r = number of trials
```

#### Step 9: Calculate Part Range (R_p)

```
R_p = Max(X̄_parts) - Min(X̄_parts)
```

#### Step 10: Calculate Part Variation (PV)

```
PV = R_p × K₃

Where:
K₃ = factor based on number of parts
```

#### Step 11: Calculate Total Variation (TV)

```
TV = √(GR&R² + PV²)
```

#### Step 12: Calculate Percentages

```
%EV = (EV / TV) × 100
%AV = (AV / TV) × 100
%GR&R = (GR&R / TV) × 100
%PV = (PV / TV) × 100

Note: %EV² + %AV² + %PV² ≈ 100%
      %GR&R² + %PV² = 100%
```

#### Step 13: Calculate ndc

```
ndc = 1.41 × (PV / GR&R)

Round down to integer
```

---

## Gage R&R - ANOVA Method

### ANOVA Table Structure

| Source | DF | SS | MS | F | Variance |
|--------|----|----|----|----|----------|
| Part | n-1 | SS_P | MS_P | MS_P/MS_PO | σ²_P |
| Operator | o-1 | SS_O | MS_O | MS_O/MS_PO | σ²_O |
| Part×Operator | (n-1)(o-1) | SS_PO | MS_PO | MS_PO/MS_E | σ²_PO |
| Repeatability | no(r-1) | SS_E | MS_E | | σ²_E |
| Total | nor-1 | SS_T | | | |

### Sum of Squares Formulas

```
SS_Total = Σ(x_ijk - X̄...)²

SS_Part = or × Σ(X̄_i.. - X̄...)²

SS_Operator = nr × Σ(X̄_.j. - X̄...)²

SS_Part×Operator = r × ΣΣ(X̄_ij. - X̄_i.. - X̄_.j. + X̄...)²

SS_Repeatability = ΣΣΣ(x_ijk - X̄_ij.)²

Where:
i = part index
j = operator index
k = trial index
```

### Mean Squares

```
MS = SS / DF
```

### Variance Components

```
σ²_Repeatability = MS_E

σ²_Part×Operator = (MS_PO - MS_E) / r
   If negative, set to 0

σ²_Operator = (MS_O - MS_PO) / (n × r)
   If negative, set to 0

σ²_Part = (MS_P - MS_PO) / (o × r)
   If negative, set to 0

σ²_Reproducibility = σ²_Operator + σ²_Part×Operator

σ²_GR&R = σ²_Repeatability + σ²_Reproducibility

σ²_Total = σ²_Part + σ²_GR&R
```

### Standard Deviations and Percentages

```
σ_component = √(σ²_component)

Study Variation = 6 × σ_component (for 99.73% coverage)

%Contribution = (σ²_component / σ²_Total) × 100

%Study Variation = (6σ_component / 6σ_Total) × 100
                 = (σ_component / σ_Total) × 100
```

---

## %GR&R vs Tolerance

Alternative calculation using tolerance:

```
%GR&R_tolerance = (6 × σ_GR&R / Tolerance) × 100

Or equivalently:

%GR&R_tolerance = (GR&R / (Tolerance/6)) × 100
```

---

## Attribute Agreement Formulas

### Within Appraiser Agreement

```
Within Agreement_j = (# samples where all trials match) / n × 100

Overall Within = Average of all appraiser within agreements
```

### Between Appraiser Agreement

```
Between Agreement = (# samples where all appraisers agree) / n × 100
```

### Appraiser vs Standard

```
Effectiveness_j = (# correct decisions) / (n × r) × 100

Where:
j = appraiser
n = samples
r = trials

Overall Effectiveness = Average of all appraiser effectiveness
```

### Kappa Calculation

For single appraiser vs. standard:

```
         Observed Agreement - Expected Agreement
Kappa = ─────────────────────────────────────────
              1 - Expected Agreement

Where:
Observed Agreement (P_o) = (a + d) / N
Expected Agreement (P_e) = [(a+b)(a+c) + (c+d)(b+d)] / N²

From 2x2 contingency table:
              Standard
              Good    Bad
Appraiser Good  a      b
          Bad   c      d

N = a + b + c + d
```

### Fleiss' Kappa (Multiple Appraisers)

For overall agreement among multiple appraisers:

```
         P̄ - P̄_e
κ = ──────────────
       1 - P̄_e

Where P̄ and P̄_e are computed across all appraisers
```

---

## Bias Calculation

```
Bias = X̄_observed - Reference Value

% Bias = (|Bias| / Process Variation) × 100

t-statistic = Bias / (s / √n)

Where:
s = standard deviation of measurements
n = number of measurements
```

---

## Linearity Calculation

```
Bias_i = X̄_i - Reference_i

Linearity = |Slope| × Process Variation

% Linearity = (Linearity / Process Variation) × 100

Regression: Bias = a + b × Reference
Where:
a = y-intercept
b = slope
```

---

## Quick Reference Formulas

### Repeatability (EV)
```
EV = R̄ × K₁
```

### Reproducibility (AV)
```
AV = √[(X̄_diff × K₂)² - (EV²/nr)]
```

### GR&R
```
GR&R = √(EV² + AV²)
```

### Part Variation (PV)
```
PV = R_p × K₃
```

### Total Variation (TV)
```
TV = √(GR&R² + PV²)
```

### %GR&R
```
%GR&R = (GR&R / TV) × 100
```

### ndc
```
ndc = 1.41 × (PV / GR&R)
```

---

## Example Calculation

**Given:**
- 3 operators, 10 parts, 3 trials
- R̄ = 0.034
- X̄_diff = 0.012
- R_p = 0.187

**Solution:**

```
EV = 0.034 × 3.05 = 0.1037

AV = √[(0.012 × 2.70)² - (0.1037²/(10×3))]
   = √[0.001050 - 0.000359]
   = √0.000691
   = 0.0263

GR&R = √(0.1037² + 0.0263²) = √0.01144 = 0.1070

PV = 0.187 × 1.62 = 0.303

TV = √(0.1070² + 0.303²) = √0.1033 = 0.321

%GR&R = (0.1070 / 0.321) × 100 = 33.3%

ndc = 1.41 × (0.303 / 0.1070) = 3.99 ≈ 3
```

**Conclusion:** %GR&R = 33.3% (Unacceptable), ndc = 3 (Marginal)
