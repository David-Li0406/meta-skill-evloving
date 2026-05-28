---
name: fairness-bias-auditor
description: Evaluates machine learning models for demographic bias using the fairlearn library. Use this skill immediately after training any predictive model.
---

# Fairness & Bias Auditor

Automated decision systems in education can perpetuate inequality. Run this audit after training any predictive model.

## Audit Protocol

### 1. Metric Calculation

Use `fairlearn` to calculate:

- **Demographic Parity Difference**: Selection rates across groups
- **Equalized Odds**: True positive/false positive rates across groups

### 2. Protected Attributes

For higher education analytics, use:

- `PCTPELL` (Pell Grant rate) as socioeconomic proxy
- Racial demographics where available

### 3. Four-Fifths Rule

If selection rate ratio between privileged and unprivileged groups < **0.8**, flag as violation.

```python
from fairlearn.metrics import demographic_parity_ratio

ratio = demographic_parity_ratio(
    y_true,
    y_pred,
    sensitive_features=sensitive_group
)
if ratio < 0.8:
    print("WARNING: Four-fifths rule violation detected")
```

## Visualization Requirements

1. Generate disparity plots using CGI color palette
2. **Always** include the audit results visibly in deliverables
3. Document any mitigations applied (e.g., sample reweighting)

## Remediation Options

If bias detected:

1. Adjust sample weights to achieve demographic parity
2. Use `fairlearn.reductions.ExponentiatedGradient` for constrained optimization
3. Document the trade-off between accuracy and fairness
