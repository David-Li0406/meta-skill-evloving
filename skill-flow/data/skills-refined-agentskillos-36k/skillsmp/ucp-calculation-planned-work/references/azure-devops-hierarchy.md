# Azure DevOps Work Item Hierarchy for UCP

## Standard Hierarchy

```
Epic (Strategic Goal - Quarters)
  ↓
Feature (Functional Area - 2-3 Sprints)
  ↓
User Story (Use Case - 1 Sprint) ← COUNT THIS FOR UCP
  ↓
Task (Implementation Step - Days)
```

## Decision Matrix

| Work Item Type | Use for UCP? | Accuracy | Calibration | When to Use |
|---------------|--------------|----------|-------------|-------------|
| **User Story** | ✅ Best | 95-98% | None | Always preferred |
| **Feature** | ⚠️ Acceptable | 80-90% | 1.8x | When no User Stories |
| **Epic** | ❌ No | N/A | N/A | Strategic planning only |
| **Task** | ❌ No | N/A | N/A | Sprint execution only |

## Why User Stories Are Correct Level

✅ Right granularity (4-7 transactions)
✅ Implementation-focused
✅ Testable acceptance criteria
✅ Actor-identifiable
✅ Sprint-sized (1-2 sprints)

## Calibration Factors

**If using Features:**
- High-quality Features (detailed deliverables): 1.8x multiplier
- Typical Features (high-level): 2.0x multiplier
- Expected accuracy: ±15-25%

**If missing User Stories:**
- Add 25-30% for untracked infrastructure work
- Check for missing categories: health monitoring, error handling, logging, testing, deployment
