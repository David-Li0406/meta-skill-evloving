---
name: systematic-debugging
description: Use this skill when you need a structured approach to identify and resolve bugs through hypothesis testing, systematic investigation, and root cause analysis.
---

# Systematic Debugging: The Scientific Method

> *"Understanding precedes execution. Do not guess at the bug. Understand the system, and the bug reveals itself."*

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

## The Debug Cycle

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

## Step 1: Observe

### Gather the Facts
```
WHAT is happening?
- Exact error message (copy it!)
- Actual behavior vs. expected behavior
- What does "not working" mean specifically?

WHEN does it happen?
- Always, or intermittently?
- After a specific action?
- At a specific time?

WHERE does it happen?
- Which environment? (dev, staging, prod)
- Which browser/device/OS?
- Which user/account?

WHO does it affect?
- All users or specific users?
- New users or existing?
- Any pattern in affected users?
```

### The Bug Report Template
```markdown
## Bug: [Clear, specific title]

### Observed Behavior
[What actually happens]

### Expected Behavior
[What should happen]

### Steps to Reproduce
1. [Step 1]
2. [Step 2]
3. [Step 3]

### Environment
- Browser/Client:
- OS:
- Environment:
- User role:

### Error Messages
[Exact error text or screenshot]

### Frequency
[Always / Sometimes / Once]

### Impact
[Who is affected and how severely]
```

## Step 2: Reproduce

### The Reproduction Requirement
```
IF YOU CAN'T REPRODUCE IT, YOU CAN'T FIX IT
```

### Creating a Minimal Reproduction
```
1. Start with the full scenario
2. Remove one element at a time
3. Does the bug still occur?
4. Continue until you have the smallest case
```

### When You Can't Reproduce
```
Consider:
- Environment differences
- Timing/race conditions
- State dependencies
- User-specific data
- Cached vs. fresh state
- Network conditions
```

## Step 3: Hypothesize

### Generate Hypotheses
```
List possible causes without judgment:

"The bug could be caused by:"
1. [Hypothesis A]
2. [Hypothesis B]
3. [Hypothesis C]

Rank by:
- Likelihood (most to least likely)
- Testability (easiest to hardest to test)
```

### Common Bug Categories
```
STATE BUGS
LOGIC BUGS
DATA BUGS
TIMING BUGS
INTEGRATION BUGS
EDGE CASES
```

## Step 4: Test Hypotheses

### Isolation Techniques

#### Binary Search Debugging
```
1. Find the midpoint of the suspicious code
2. Add a log/breakpoint there
3. Is the state correct at that point?
4. If yes: bug is after that point
5. If no: bug is before that point
6. Repeat until found
```

#### Diff Debugging
```
1. Find last known working version
2. Compare with current version
3. What changed?
```

#### Rubber Duck Debugging
```
Explain the code line by line to:
- A rubber duck
- A colleague
- Yourself out loud
```

### Diagnostic Tools
```
LOGGING
BREAKPOINTS
ASSERTIONS
PROFILERS
```

## Step 5: Fix

### The Fix Principles
```
FIX THE ROOT CAUSE, NOT THE SYMPTOM
```

### Before Fixing
```
□ I understand WHY the bug occurs
□ I can explain the fix to someone else
□ The fix addresses root cause, not symptom
```

### The Minimal Fix
```
Change as little as possible.
One bug = one fix.
```

## Step 6: Verify

### Verification Checklist
```
□ Original bug is fixed
□ Bug cannot be reproduced anymore
□ All existing tests still pass
```

### The Regression Test
```
Write a test that:
1. Failed before the fix
2. Passes after the fix
```

## Step 7: Prevent

### Post-Mortem Questions
```
1. Why did this bug exist?
2. Why wasn't it caught earlier?
3. How can we prevent similar bugs?
```

### Prevention Strategies
```
ADD TESTS
IMPROVE CODE
IMPROVE PROCESS
```

## Quick Reference

### The Debug Checklist
```
□ Exact error message captured
□ Steps to reproduce documented
□ Minimal reproduction created
□ Hypotheses listed
□ Most likely hypothesis tested first
□ Root cause identified
□ Minimal fix applied
□ Fix verified
```

### When You're Stuck
```
1. Take a break
2. Explain it to someone else
3. Question your assumptions
```

*"The bug exists in the gap between what you think the code does and what it actually does. Close that gap with understanding."*