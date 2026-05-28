---
name: judge
description: Evaluate any item using CYNIC's 25-dimension judgment system. Use when asked to judge, evaluate, assess, rate, score, or analyze the quality of code, tokens, decisions, patterns, or any content. Returns Q-Score (0-100), verdict (HOWL/WAG/GROWL/BARK), and dimension breakdown.
user-invocable: true
---

# /judge - CYNIC Judgment

*"φ distrusts φ"* - Max confidence 61.8%

## Quick Start

```
/judge <item to evaluate>
```

## What It Does

Evaluates any item across **25 dimensions** grouped into **4 axioms**:

| Axiom | Dimensions | Weight |
|-------|------------|--------|
| **PHI** | Golden ratios, mathematical harmony | 38.2% |
| **VERIFY** | Source credibility, fact-checking | 23.6% |
| **CULTURE** | Pattern alignment, ecosystem fit | 23.6% |
| **BURN** | Simplicity, no bloat, efficiency | 14.6% |

## Output

- **Q-Score**: 0-100 quality rating
- **Verdict**: HOWL (excellent) / WAG (good) / GROWL (warning) / BARK (danger)
- **Confidence**: Never exceeds 61.8% (φ⁻¹)
- **Breakdown**: Per-axiom and per-dimension scores

## Examples

### Judge Code
```
/judge this authentication function for security
```

### Judge a Token
```
/judge $BONK token quality
```

### Judge a Decision
```
/judge our choice to use PostgreSQL over MongoDB
```

## Implementation

Use the `brain_cynic_judge` MCP tool:

```javascript
brain_cynic_judge({
  item: {
    type: "code|token|decision|pattern|content",
    content: "<the item to judge>",
    // Optional: provide explicit scores
    scores: { PHI: 0.7, VERIFY: 0.8 }
  },
  context: {
    source: "<where it came from>",
    type: "<category>"
  }
})
```

## Refinement

For important judgments, use `brain_cynic_refine` to self-critique:

```javascript
brain_cynic_refine({
  judgmentId: "jdg_abc123",
  maxIterations: 3
})
```

## See Also

- [dimensions.md](dimensions.md) - Full 25-dimension breakdown
- `/learn` - Provide feedback on judgments
- `/trace` - Trace judgment to blockchain
