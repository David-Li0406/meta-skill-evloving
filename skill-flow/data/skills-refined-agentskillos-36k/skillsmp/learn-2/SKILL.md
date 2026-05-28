---
name: learn
description: Provide feedback on CYNIC judgments to improve future evaluations. Use when asked to correct a judgment, provide feedback, mark as correct/incorrect, or help CYNIC learn from mistakes.
user-invocable: true
---

# /learn - CYNIC Feedback Loop

*"φ learns from φ"*

## Quick Start

```
/learn <judgment_id> correct|incorrect [reason]
```

## What It Does

Provides feedback to improve CYNIC's judgment accuracy:
- Mark judgments as correct/incorrect/partial
- Explain why the judgment was wrong
- Suggest what the score should have been
- Trigger weight calibration

## Feedback Types

| Outcome | When to Use |
|---------|-------------|
| `correct` | Judgment was accurate |
| `incorrect` | Judgment was wrong |
| `partial` | Some parts right, some wrong |

## Examples

### Mark Correct
```
/learn jdg_abc123 correct
```

### Mark Incorrect with Reason
```
/learn jdg_abc123 incorrect "missed security vulnerability"
```

### Provide Score Correction
```
/learn jdg_abc123 incorrect --score 35 "should have been BARK not WAG"
```

## Implementation

Use the `brain_cynic_feedback` MCP tool:

```javascript
brain_cynic_feedback({
  judgmentId: "jdg_abc123",
  outcome: "correct|incorrect|partial",
  reason: "explanation of feedback",
  actualScore: 35  // What it should have been (0-100)
})
```

## Learning System

CYNIC uses feedback to:

1. **Calibrate Weights**: Adjust dimension weights
2. **Detect Biases**: Find systematic errors
3. **Improve Accuracy**: Learn from mistakes

Check learning state:
```javascript
brain_learning({ action: "state" })
```

View detected biases:
```javascript
brain_learning({ action: "biases" })
```

Trigger calibration:
```javascript
brain_learning({ action: "calibrate" })
```

## Impact

| Feedback Volume | Learning Effect |
|-----------------|-----------------|
| 10+ feedbacks | Initial calibration |
| 50+ feedbacks | Bias detection |
| 100+ feedbacks | Refined accuracy |

## See Also

- `/judge` - Create judgments to learn from
- `/patterns` - See learned patterns
- `/health` - Check learning system status
