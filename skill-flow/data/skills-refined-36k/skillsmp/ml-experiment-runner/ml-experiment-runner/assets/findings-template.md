# [Experiment ID]: [Experiment Name] - Findings

## Status: [COMPLETED/FAILED] | Recommendation: [PROCEED/PIVOT]

## Summary

[2-3 sentences summarizing: What did we test? What did we learn? What's the recommendation?]

---

## Key Metrics

| Metric | Value | Target | Acceptable | Failure | Result |
|--------|-------|--------|------------|---------|--------|
| [metric_1] | [X.XXX] | [target] | [acceptable] | [failure] | [Pass/Fail] |
| [metric_2] | [X.XXX] | [target] | [acceptable] | [failure] | [Pass/Fail] |
| [metric_3] | [X.XXX] | [target] | [acceptable] | [failure] | [Pass/Fail] |

**Overall Assessment:** [X/Y] metrics meet acceptable thresholds.

---

## Sub-experiment Results

### [E_X_1]: [Sub-experiment Name]

**Objective:** [What this sub-experiment tested]

**Method:** [Brief description of approach]

**Results:**
- [Key finding 1 with specific numbers]
- [Key finding 2 with specific numbers]

**Artifacts:**
- `artifacts/[filename].png` - [Description]

---

### [E_X_2]: [Sub-experiment Name]

**Objective:** [What this sub-experiment tested]

**Method:** [Brief description of approach]

**Results:**
- [Key finding 1]
- [Key finding 2]

**Artifacts:**
- `artifacts/[filename].png` - [Description]

---

## Analysis

### What Worked

1. **[Finding]**: [Explanation with numbers]
2. **[Finding]**: [Explanation with numbers]

### What Didn't Work

1. **[Finding]**: [Explanation of why, with numbers]
2. **[Finding]**: [Explanation of why, with numbers]

### Unexpected Findings

- **[Finding]**: [Why it was unexpected, what it might mean]

---

## Implications for Hypothesis

[How do these results affect confidence in the main hypothesis?]

[What does this mean for the next phase of research?]

---

## Confidence Assessment

**Confidence:** [High/Medium/Low]

**Rationale:**
- Sample size: [n=X]
- Consistency: [Results across Y runs had std of Z]
- Margin: [X% above/below threshold]
- Agreement: [N/M sub-experiments support conclusion]

---

## Next Steps

1. **[Action]**: [Why this is recommended]
2. **[Action]**: [Why this is recommended]
3. **[Action]**: [Why this is recommended]

---

## Appendix: Raw Data

### Configuration

```yaml
experiment_id: [id]
model: [model name]
dataset: [dataset name]
samples: [n]
device: [GPU type]
```

### W&B Run

- **Run URL**: [link]
- **Artifacts**: [link to artifacts]

---

*Generated: [DATE]*
*Status: [completed/failed]*
*Recommendation: [proceed/pivot]*
