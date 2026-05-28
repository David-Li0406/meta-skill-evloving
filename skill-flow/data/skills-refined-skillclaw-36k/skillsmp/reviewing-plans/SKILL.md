---
name: reviewing-plans
description: Review methodology for implementation plans. Use when evaluating plan quality, completeness, or risk.
---

# Reviewing Plans

Evaluate plans across five weighted dimensions.

## Dimensions

| Dimension | Weight | Focus |
|-----------|--------|-------|
| Completeness | 25% | Requirements coverage, missing steps, edge cases |
| Correctness | 25% | Technical soundness, logical flaws, assumptions |
| Feasibility | 20% | Implementability, realistic assumptions |
| Risk | 15% | Security, performance, scalability concerns |
| Clarity | 15% | Actionability, ambiguity |

## Severity Levels

| Level | Impact |
|-------|--------|
| P1 | Critical — fundamental flaws, implementation failure |
| P2 | Major — significant issues affecting success |

Only report P1 and P2 findings.

## Output Format

```
VERDICT: [APPROVE|REVISE|BLOCK]

## Findings

### [P1] Title
**Dimension**: <dimension>
**Issue**: <description>
**Recommendation**: <fix>

## Summary
<2-3 sentences>
```

## Verdict Rules

- BLOCK: Any P1 findings
- REVISE: P2 findings, no P1
- APPROVE: No P1 or P2
