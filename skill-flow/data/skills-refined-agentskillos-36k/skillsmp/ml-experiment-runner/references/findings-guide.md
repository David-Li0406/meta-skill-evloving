# Writing Effective FINDINGS.md

## Purpose

FINDINGS.md documents what we learned from an experiment in plain language. It serves as:
- A record for future reference
- Communication to stakeholders
- Evidence for decision-making (proceed/pivot)

## Key Principles

### 1. Show Your Work

Don't just state conclusions—show the evidence:

```markdown
## Bad
The model performs well.

## Good
The model achieves 95% accuracy on the test set (n=1000), exceeding the 90% threshold.
Training converged after 50 epochs with final loss of 0.023.
```

### 2. Be Specific About Metrics

Always include:
- The actual value achieved
- The threshold/target
- Whether it passed or failed
- Sample sizes and conditions

```markdown
| Metric | Value | Target | Result |
|--------|-------|--------|--------|
| LPIPS | 0.264 | < 0.35 | Pass |
| SSIM | 0.943 | > 0.75 | Pass |
| Spatial IoU | 0.559 | > 0.60 | **Fail** |
```

### 3. Explain Unexpected Results

When results surprise you, explore why:

```markdown
## Unexpected Finding

Spatial IoU (0.559) failed despite strong LPIPS (0.264) and SSIM (0.943).

**Analysis:** The model preserves perceptual quality (textures, colors) but loses
precise spatial positioning. This suggests the 2x2 token merger destroys
positional information while preserving semantic content.
```

### 4. State Implications Clearly

Connect findings to the broader hypothesis:

```markdown
## Implications

This result indicates that VLM latents alone cannot support spatial tasks
requiring precise object localization. Alternative approaches needed:
- Hybrid encoder (DINOv2 + VLM)
- Skip connections from early VLM layers
- Separate spatial encoding pathway
```

## Experiment FINDINGS.md Template

```markdown
# [Experiment Name] - Findings

## Status: [COMPLETED/FAILED] | Recommendation: [PROCEED/PIVOT]

## Summary

[2-3 sentences: What did we test? What did we learn? What's the recommendation?]

## Key Metrics

| Metric | Value | Target | Acceptable | Result |
|--------|-------|--------|------------|--------|
| [metric1] | [value] | [target] | [acceptable] | [Pass/Fail] |
| [metric2] | [value] | [target] | [acceptable] | [Pass/Fail] |

## Sub-experiment Results

### [E1.1: Sub-experiment Name]

**Objective:** [What we tested]

**Method:** [How we tested it]

**Results:**
- [Key finding 1]
- [Key finding 2]

**Artifacts:** [Links to plots, data]

### [E1.2: Sub-experiment Name]
...

## Analysis

### What Worked
- [Finding that supports the hypothesis]

### What Didn't Work
- [Finding that challenges the hypothesis]

### Unexpected Findings
- [Surprising result and explanation]

## Implications for Hypothesis

[How do these results affect our confidence in the main hypothesis?
What should we do next?]

## Confidence Assessment

**Confidence:** [High/Medium/Low]
**Rationale:** [Why this confidence level?]

## Next Steps

1. [Recommended action 1]
2. [Recommended action 2]
```

## Project FINDINGS.md Updates

When updating the main research/FINDINGS.md:

### Add Summary Entry

```markdown
### [Experiment Name](experiments/<id>/FINDINGS.md) - [PROCEED/PIVOT]

**Question:** [What we tested]

**Answer:** [What we learned]

| Metric | Value | Threshold | Result |
|--------|-------|-----------|--------|
| [key metric] | [value] | [threshold] | [Pass/Fail] |

**Key Finding:** [One sentence insight]

→ [Full details](experiments/<id>/FINDINGS.md)
```

### Update Gate Status

```markdown
### Gate 1: [Gate Name]
**Status:** [PASSED/IN PROGRESS/BLOCKED]

| Experiment | Status | Recommendation |
|------------|--------|----------------|
| Q1 | Complete | **PROCEED** |
| P2 | Running | Pending |

**Gate Progress:** 1/2 proceed
```

## Showing Confidence Appropriately

### High Confidence
- Large sample sizes
- Consistent results across runs
- Clear margin above/below thresholds
- Multiple metrics agree

```markdown
**Confidence:** High
**Rationale:** Results consistent across 3 runs (std < 0.01), clear margin
above threshold (0.85 vs 0.70 target), all 4 sub-experiments agree.
```

### Medium Confidence
- Adequate sample sizes
- Some variance in results
- Close to thresholds
- Most metrics agree

```markdown
**Confidence:** Medium
**Rationale:** Single run, adequate sample (n=500), result close to threshold
(0.62 vs 0.60 target). Recommend additional validation.
```

### Low Confidence
- Small samples
- High variance
- Borderline results
- Metrics disagree

```markdown
**Confidence:** Low
**Rationale:** Small sample (n=50), high variance (std=0.15), borderline
result (0.61 vs 0.60 target). Strongly recommend human review and replication.
```

## Flagging for Human Review

Add this when confidence is low or results are unexpected:

```markdown
---
**REQUIRES HUMAN REVIEW**

Reason: [Borderline results / Unexpected finding / Low confidence / Pivot decision]

Specific questions:
1. [Question for human reviewer]
2. [Another question]
---
```
