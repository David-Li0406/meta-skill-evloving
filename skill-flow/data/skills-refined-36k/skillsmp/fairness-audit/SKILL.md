---
name: fairness-audit
description: Validates True Positive Rate and False Positive Rate gaps across demographics using AgentDB metrics
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: clinical-pipeline
---

## What I do

I validate that the risk assessment meets fairness standards by checking TPR (True Positive Rate) and FPR (False Positive Rate) gaps across demographic groups. I ensure the model performs equitably regardless of skin tone.

## When to use me

Use this when:

- Risk assessment is complete and you need fairness validation
- You need to verify TPR/FPR gaps are within acceptable thresholds
- You're ensuring the model doesn't exhibit demographic bias

## Key Concepts

- **TPR Gap**: Difference in true positive rates across groups
- **FPR Gap**: Difference in false positive rates across groups
- **Fairness Thresholds**: Maximum acceptable gaps (typically 0.1)
- **fairness_validated**: State flag after audit complete

## Source Files

- `services/agentDB.ts`: Fairness metrics storage
- `services/goap.ts`: Fairness validation action

## Code Patterns

- Query AgentDB for demographic performance metrics
- Calculate TPR and FPR gaps between groups
- Fail validation if gaps exceed thresholds

## Operational Constraints

- TPR and FPR gaps MUST be within acceptable thresholds
- If fairness validation fails, diagnosis is not web-verified
- Must maintain demographic parity in performance metrics
