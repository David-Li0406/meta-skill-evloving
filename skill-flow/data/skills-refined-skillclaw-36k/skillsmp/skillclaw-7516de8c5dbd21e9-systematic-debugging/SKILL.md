---
name: systematic-debugging
description: Use this skill when you need a structured approach to identify and resolve bugs through hypothesis testing, systematic isolation, and root cause analysis.
---

# Systematic Debugging Methodology

## The Debugging Mindset

### What Debugging Is NOT
```
❌ Random changes hoping something works
❌ Blaming the framework/library/language
❌ Assuming you know the cause without evidence
❌ Deleting and rewriting until it works
```

### What Debugging IS
```
✓ Scientific investigation
✓ Hypothesis formation and testing
✓ Systematic isolation
✓ Understanding before fixing
```

---

## The Scientific Method for Bugs

```
╭─────────────────────────────────────────────────────────╮
│                    THE DEBUG CYCLE                       │
├─────────────────────────────────────────────────────────┤
│                                                          │
│   1. OBSERVE    →  What exactly is happening?           │
│        ↓                                                 │
│   2. REPRODUCE  →  Can I make it happen reliably?       │
│        ↓                                                 │
│   3. HYPOTHESIZE→  What could cause this?               │
│        ↓                                                 │
│   4. TEST       →  Is my hypothesis correct?            │
│        ↓                                                 │
│   5. FIX        →  Address the root cause               │
│        ↓                                                 │
│   6. VERIFY     →  Is it actually fixed?                │
│        ↓                                                 │
│   7. PREVENT    →  How do we stop it happening again?   │
│                                                          │
╰─────────────────────────────────────────────────────────╯
```

## Core Principles
1. Debugging is science, not art - hypothesis, experiment, observe, repeat.
2. The 10-minute rule - if ad-hoc hunting fails for 10 minutes, go systematic.
3. Question everything you "know" - your mental model is probably wrong somewhere.
4. Isolate before you understand - narrow the search space first.
5. The symptom is not the bug - follow the causal chain to the root.

## Contrarian Insights
- Debuggers are overrated. Print statements are flexible, portable, and often faster.
- Reading code is overrated for debugging. Change code to test hypotheses.
- "Understanding the system" is a trap. The bug exists precisely because your understanding is wrong. Question your assumptions.
- Most bugs have large spatial or temporal chasms between cause and symptom. The symptom location is almost never where you should start looking.