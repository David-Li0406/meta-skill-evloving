---
id: statistical-significance
name: "Statistical Significance"
domain: GRO
skill: faion-marketing-manager
category: "growth"
---

# Statistical Significance

## Metadata

| Field | Value |
|-------|-------|
| **ID** | statistical-significance |
| **Name** | Statistical Significance |
| **Category** | Growth |
| **Difficulty** | Intermediate |
| **Agent** | faion-growth-agent |
| **Related** | ab-testing-framework, multivariate-testing, cohort-analysis |

---

## Problem

You ran an A/B test. Variant B had a 5.2% conversion rate, Variant A had 5.0%. Is B really better, or did you just get lucky with the random sample?

Statistical significance answers: "How confident can I be that this difference is real?"

Without understanding significance, you will:
- Ship changes that do not actually help
- Kill changes that would have worked
- Waste time running tests too short or too long

---

## Framework

### Key Concepts

#### 1. The Null Hypothesis

The null hypothesis (H0) assumes there is NO difference between variants. Your test tries to disprove this.

```
H0: Conversion rate A = Conversion rate B (no difference)
H1: Conversion rate A ≠ Conversion rate B (there IS a difference)
```

#### 2. P-Value

The p-value is the probability of seeing your results (or more extreme) IF the null hypothesis were true.

```
p-value = 0.03 means:
"If there were truly no difference, there is a 3% chance
 we would see this result by random chance."
```

**Lower p-value = stronger evidence that the difference is real.**

#### 3. Significance Level (Alpha)

The threshold you set BEFORE the test to determine when to reject H0.

```
Standard: alpha = 0.05 (95% confidence)

If p-value < alpha → Statistically significant → Reject H0
If p-value >= alpha → Not significant → Cannot reject H0
```

#### 4. Confidence Level

Confidence level = 1 - alpha

```
Alpha = 0.05 → 95% confidence
Alpha = 0.01 → 99% confidence
```

"95% confidence" means: If you ran this test 100 times with no real difference, you would incorrectly conclude there IS a difference about 5 times.

#### 5. Statistical Power

Power is the probability of detecting a real difference when one exists.

```
Standard: 80% power

80% power means:
- If there IS a real difference
- You have 80% chance of detecting it
- 20% chance of missing it (Type II error)
```

### Type I and Type II Errors

| Error | Name | Meaning | Controlled By |
|-------|------|---------|---------------|
| Type I | False Positive | Conclude difference exists when it does not | Significance level (alpha) |
| Type II | False Negative | Conclude no difference when one exists | Statistical power |

```
                     Reality
                 ┌─────────┬─────────┐
                 │ No Diff │  Diff   │
   ┌─────────────┼─────────┼─────────┤
   │ Conclude    │  Type I │ Correct │
Your│ Difference │  Error  │ (True+) │
Test├─────────────┼─────────┼─────────┤
   │ Conclude No │ Correct │ Type II │
   │ Difference  │ (True-) │  Error  │
   └─────────────┴─────────┴─────────┘
```

### Confidence Intervals

A confidence interval gives a range of plausible values for the true difference.

```
Example:
Conversion A: 5.0%
Conversion B: 5.8%
Difference: +0.8%
95% CI: [0.2%, 1.4%]

Interpretation:
We are 95% confident the true difference is between 0.2% and 1.4%.
Since 0 is not in this range, the difference is statistically significant.
```

**Wider CI = more uncertainty (need more data)**
**Narrower CI = more precision**

---

## Calculating Statistical Significance

### For Conversion Rates (Proportions)

Use a two-proportion z-test.

**Inputs:**
- n1 = sample size for A
- n2 = sample size for B
- x1 = conversions in A
- x2 = conversions in B
- p1 = x1/n1 (conversion rate A)
- p2 = x2/n2 (conversion rate B)

**Pooled proportion:**
```
p_pooled = (x1 + x2) / (n1 + n2)
```

**Standard error:**
```
SE = sqrt(p_pooled × (1 - p_pooled) × (1/n1 + 1/n2))
```

**Z-score:**
```
z = (p2 - p1) / SE
```

**P-value:**
Look up z-score in standard normal table (or use calculator).

### Example Calculation

```
Variant A: 1,000 visitors, 50 conversions (5.0%)
Variant B: 1,000 visitors, 62 conversions (6.2%)

p1 = 50/1000 = 0.050
p2 = 62/1000 = 0.062

p_pooled = (50 + 62) / (1000 + 1000) = 112/2000 = 0.056

SE = sqrt(0.056 × 0.944 × (1/1000 + 1/1000))
   = sqrt(0.056 × 0.944 × 0.002)
   = sqrt(0.0001057)
   = 0.0103

z = (0.062 - 0.050) / 0.0103 = 1.17

p-value (two-tailed) ≈ 0.24

Result: NOT statistically significant (p > 0.05)
```

---

## Sample Size Calculation

### Formula

```
n = 2 × [(Z_alpha/2 + Z_beta)² × p × (1-p)] / (MDE)²

Where:
- Z_alpha/2 = 1.96 for 95% confidence
- Z_beta = 0.84 for 80% power
- p = baseline conversion rate
- MDE = minimum detectable effect (absolute)
```

### Simplified Formula

```
n per variant ≈ 16 × p × (1-p) / MDE²
```

### Sample Size Table

| Baseline | 5% Relative MDE | 10% Relative MDE | 20% Relative MDE |
|----------|-----------------|------------------|------------------|
| 1% | 314,000 | 78,500 | 19,600 |
| 2% | 156,000 | 39,000 | 9,800 |
| 5% | 61,500 | 15,400 | 3,850 |
| 10% | 28,800 | 7,200 | 1,800 |
| 20% | 12,800 | 3,200 | 800 |
| 50% | 3,200 | 800 | 200 |

*Sample size per variant at 95% confidence, 80% power*

---

## Templates

### Significance Calculation Template

```markdown
# Statistical Significance Check

## Test: [Name]

## Raw Data
| Variant | Sample Size | Conversions | Rate |
|---------|-------------|-------------|------|
| A (Control) | | | |
| B (Treatment) | | | |

## Difference
- Absolute: B rate - A rate = _____%
- Relative: (B - A) / A × 100 = _____%

## Statistical Test
- Test type: Two-proportion z-test
- Z-score: _____
- P-value: _____
- 95% CI for difference: [_____, _____]

## Conclusion
[ ] p < 0.05 → Statistically significant
[ ] p >= 0.05 → NOT significant

## Recommendation
[Ship B / Keep A / Need more data]
```

### Pre-Test Power Analysis Template

```markdown
# Sample Size Calculation

## Inputs
- Baseline conversion rate: ____%
- Minimum detectable effect: _____% relative (_____% absolute)
- Significance level: 95%
- Power: 80%

## Calculation
n = 16 × p × (1-p) / MDE²
n = 16 × _____ × _____ / _____²
n = _____ per variant

## Total Sample Needed
- Per variant: _____
- Total (both variants): _____

## Duration Estimate
- Daily traffic: _____
- Days needed: Total / Daily = _____ days
```

---

## Examples

### Example 1: Significant Result

**Test:** New checkout button color

| Variant | Visitors | Purchases | Rate |
|---------|----------|-----------|------|
| A: Gray | 15,000 | 450 | 3.00% |
| B: Green | 15,000 | 525 | 3.50% |

**Calculation:**
- p_pooled = 975/30000 = 0.0325
- SE = 0.0129
- z = (0.035 - 0.030) / 0.0129 = 2.93
- p-value = 0.003

**Result:**
- p < 0.05 → Statistically significant
- 95% CI: [0.17%, 0.83%]
- Confident B is better

**Decision:** Ship green button

### Example 2: Not Significant (Need More Data)

**Test:** Headline change

| Variant | Visitors | Signups | Rate |
|---------|----------|---------|------|
| A: "Save Time" | 2,000 | 100 | 5.0% |
| B: "Work Smarter" | 2,000 | 110 | 5.5% |

**Calculation:**
- p_pooled = 0.0525
- SE = 0.0158
- z = 0.32
- p-value = 0.75

**Result:**
- p > 0.05 → NOT significant
- 95% CI: [-2.6%, +3.6%]
- CI includes 0 → cannot conclude difference

**Decision:** Need ~10,000 per variant to detect this difference

### Example 3: Underpowered Test

**Setup:**
- Expected baseline: 10%
- Expected lift: 5% relative (0.5% absolute)
- Actual sample: 500 per variant

**Power calculation:**
- Needed sample: 16 × 0.10 × 0.90 / 0.005² = 57,600 per variant
- Actual sample: 500
- Actual power: ~6%

**Problem:** Only 6% chance of detecting a real effect. Test was essentially useless.

---

## Common Mistakes

| Mistake | Why It's Wrong | Fix |
|---------|---------------|-----|
| Peeking and stopping early | Inflates false positive rate | Pre-commit to sample size |
| Using one-tailed tests | Biases toward expected direction | Use two-tailed tests |
| Ignoring practical significance | Statistical ≠ meaningful | Check if lift matters for business |
| Not correcting for multiple tests | More tests = more false positives | Use Bonferroni correction |
| Confusing CI and credible interval | Different interpretations | Understand frequentist vs Bayesian |
| "Not significant" = "no effect" | Absence of evidence ≠ evidence of absence | Say "insufficient evidence" |

---

## Significance Calculator

```
INPUTS:
─────────────────────────────────────────
Sample A (n1):           _____
Conversions A (x1):      _____
Conversion rate A (p1):  _____%

Sample B (n2):           _____
Conversions B (x2):      _____
Conversion rate B (p2):  _____%

CALCULATIONS:
─────────────────────────────────────────
Difference = p2 - p1 = _____%

Pooled rate = (x1 + x2) / (n1 + n2) = _____

SE = sqrt(pooled × (1-pooled) × (1/n1 + 1/n2))
   = sqrt(_____ × _____ × _____)
   = _____

Z-score = Difference / SE = _____

P-value (two-tailed) = _____

95% CI = Difference ± 1.96 × SE
       = [_____, _____]

RESULT:
─────────────────────────────────────────
[ ] Significant (p < 0.05)
[ ] Not significant (p >= 0.05)
```

---

## Bayesian Alternative

Frequentist statistics (p-values) can be counterintuitive. Bayesian A/B testing gives direct probability statements.

**Frequentist:** "If there's no difference, there's a 3% chance of seeing this result"

**Bayesian:** "There's a 97% probability that B is better than A"

| Approach | Pros | Cons |
|----------|------|------|
| Frequentist | Standard, simple tools | Counterintuitive interpretation |
| Bayesian | Intuitive, allows early stopping | Requires prior assumptions |

---

## Quick Reference

| Situation | Interpretation |
|-----------|---------------|
| p < 0.01 | Strong evidence of difference |
| 0.01 ≤ p < 0.05 | Moderate evidence |
| 0.05 ≤ p < 0.10 | Weak evidence, consider more data |
| p ≥ 0.10 | Insufficient evidence |

---

## Tools

| Purpose | Tools |
|---------|-------|
| Calculators | Evan Miller, ABTestGuide |
| Analysis | Python (scipy.stats), R |
| Testing platforms | Optimizely, VWO, Statsig |
| Bayesian | Optimizely Stats Engine, VWO SmartStats |

---

## Related Methodologies

- **ab-testing-framework:** A/B Testing Framework (how to run tests)
- **multivariate-testing:** Multivariate Testing (testing multiple variables)
- **cohort-analysis:** Cohort Analysis (segmenting results)

---

*Methodology: statistical-significance | Growth | faion-growth-agent*
