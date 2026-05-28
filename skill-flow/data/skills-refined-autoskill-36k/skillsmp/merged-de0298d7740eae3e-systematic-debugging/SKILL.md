---
name: systematic-debugging
description: Use this skill when encountering any bug, test failure, or unexpected behavior, ensuring root cause investigation before proposing fixes.
---

# Systematic Debugging

## Overview

Random fixes waste time and create new bugs. Quick patches mask underlying issues.

**Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

**Violating the letter of this process is violating the spirit of debugging.**

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1, you cannot propose fixes.

## When to Use

Use for ANY technical issue:

- Test failures
- Bugs in production
- Unexpected behavior
- Performance problems
- Build failures
- Integration issues

**Use this ESPECIALLY when:**

- Under time pressure (emergencies make guessing tempting)
- "Just one quick fix" seems obvious
- You've already tried multiple fixes
- Previous fix didn't work
- You don't fully understand the issue

**Don't skip when:**

- Issue seems simple (simple bugs have root causes too)
- You're in a hurry (rushing guarantees rework)
- Manager wants it fixed NOW (systematic is faster than thrashing)

## The Four Phases

You MUST complete each phase before proceeding to the next.

### Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:**

1. **Read Error Messages Carefully**
   - Don't skip past errors or warnings; they often contain the exact solution.
   - Read stack traces completely and note line numbers, file paths, error codes.

2. **Reproduce Consistently**
   - Can you trigger it reliably? What are the exact steps?
   - If not reproducible → gather more data, don't guess.

3. **Check Recent Changes**
   - What changed that could cause this? Check Git diff, recent commits, new dependencies, config changes, and environmental differences.

4. **Gather Evidence in Multi-Component Systems**
   - For EACH component boundary, log what data enters and exits, verify environment/config propagation, and check state at each layer.
   - Run once to gather evidence showing WHERE it breaks, then analyze to identify the failing component.

5. **Trace Data Flow**
   - Where does the bad value originate? What called this with the bad value? Keep tracing up until you find the source and fix at the source, not at the symptom.

### Phase 2: Pattern Analysis

**Find the pattern before fixing:**

1. **Find Working Examples**
   - Locate similar working code in the same codebase.

2. **Compare Against References**
   - If implementing a pattern, read the reference implementation COMPLETELY.

3. **Identify Differences**
   - What's different between working and broken? List every difference, however small.

4. **Understand Dependencies**
   - What other components does this need? What settings, config, environment? What assumptions does it make?

### Phase 3: Hypothesis and Testing

**Scientific method:**

1. **Form Single Hypothesis**
   - State clearly: "I think X is the root cause because Y." Write it down.

2. **Test Minimally**
   - Make the SMALLEST possible change to test the hypothesis. One variable at a time.

3. **Verify Before Continuing**
   - Did it work? Yes → Phase 4. Didn't work? Form NEW hypothesis.

4. **When You Don't Know**
   - Say "I don't understand X." Don't pretend to know; ask for help or research more.

### Phase 4: Implementation

**Fix the root cause, not the symptom:**

1. **Create Failing Test Case**
   - Simplest possible reproduction; automated test if possible.

2. **Implement Single Fix**
   - Address the root cause identified. ONE change at a time.

3. **Verify Fix**
   - Test passes now? No other tests broken? Issue actually resolved?

4. **If Fix Doesn't Work**
   - STOP. Count how many fixes you've tried. If < 3: Return to Phase 1. If ≥ 3: STOP and question the architecture.

5. **If 3+ Fixes Failed: Question Architecture**
   - Each fix reveals new shared state/coupling/problem in different places. Discuss with your human partner before attempting more fixes.

## Red Flags - STOP and Follow Process

If you catch yourself thinking:

- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "Skip the test, I'll manually verify"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- "One more fix attempt" (when already tried 2+)

**ALL of these mean: STOP. Return to Phase 1.**

## Common Rationalizations

| Excuse                                       | Reality                                                                 |
| -------------------------------------------- | ----------------------------------------------------------------------- |
| "Issue is simple, don't need process"        | Simple issues have root causes too. Process is fast for simple bugs.    |
| "Emergency, no time for process"             | Systematic debugging is FASTER than guess-and-check thrashing.          |
| "Just try this first, then investigate"      | First fix sets the pattern. Do it right from the start.                 |
| "I'll write test after confirming fix works" | Untested fixes don't stick. Test first proves it.                       |
| "Multiple fixes at once saves time"          | Can't isolate what worked. Causes new bugs.                             |

## Quick Reference

| Phase                 | Key Activities                                         | Success Criteria            |
| --------------------- | ------------------------------------------------------ | --------------------------- |
| **1. Root Cause**     | Read errors, reproduce, check changes, gather evidence | Understand WHAT and WHY     |
| **2. Pattern**        | Find working examples, compare                         | Identify differences        |
| **3. Hypothesis**     | Form theory, test minimally                            | Confirmed or new hypothesis |
| **4. Implementation** | Create test, fix, verify                               | Bug resolved, tests pass    |

## When Process Reveals "No Root Cause"

If systematic investigation reveals issue is truly environmental, timing-dependent, or external:

1. You've completed the process.
2. Document what you investigated.
3. Implement appropriate handling (retry, timeout, error message).
4. Add monitoring/logging for future investigation.

**But:** 95% of "no root cause" cases are incomplete investigation.

## Integration with Other Skills

This skill works with:

- skills/root-cause-tracing - How to trace back through call stack
- skills/defense-in-depth - Add validation after finding root cause
- skills/testing/condition-based-waiting - Replace timeouts identified in Phase 2
- skills/verification-before-completion - Verify fix worked before claiming success

## Real-World Impact

From debugging sessions:

- Systematic approach: 15-30 minutes to fix
- Random fixes approach: 2-3 hours of thrashing
- First-time fix rate: 95% vs 40%
- New bugs introduced: Near zero vs common