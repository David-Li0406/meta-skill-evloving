---
name: systematic-debugging
description: Use when encountering any bug, test failure, or unexpected behavior before proposing fixes
---

# Systematic Debugging

Random fixes waste time and create new bugs. Quick patches mask underlying issues.

**Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

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

**Use ESPECIALLY when:**
- Under time pressure (emergencies make guessing tempting)
- "Just one quick fix" seems obvious
- You've already tried multiple fixes
- Previous fix didn't work

## The Four Phases

Complete each phase before proceeding to the next.

### Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:**

1. **Read Error Messages Carefully**
   - Don't skip past errors or warnings
   - They often contain the exact solution
   - Read stack traces completely
   - Note line numbers, file paths, error codes

2. **Reproduce Consistently**
   - Can you trigger it reliably?
   - What are the exact steps?
   - Does it happen every time?
   - If not reproducible → gather more data, don't guess

3. **Check Recent Changes**
   - What changed that could cause this?
   - Git diff, recent commits
   - New dependencies, config changes
   - Environmental differences

4. **Gather Evidence**
   - Add diagnostic logging if needed
   - Check each component boundary
   - Verify data at each layer

### Phase 2: Hypothesis Formation

Only after gathering evidence:

1. Form a specific hypothesis about the root cause
2. Predict what fixing it would change
3. Identify how to verify the hypothesis

### Phase 3: Minimal Fix

1. Fix the ROOT CAUSE, not symptoms
2. Make the smallest change possible
3. Don't refactor while fixing
4. One fix at a time

### Phase 4: Verification

1. Confirm the original issue is resolved
2. Run full test suite
3. Check for regressions
4. Verify the fix addresses the hypothesis

## After 3 Consecutive Failures

1. **STOP** all further edits immediately
2. **REVERT** to last known working state
3. **DOCUMENT** what was attempted and what failed
4. **CONSULT** Oracle with full failure context
5. If Oracle cannot resolve → **ASK USER**

## Anti-Patterns (NEVER DO)

- Shotgun debugging (random changes hoping something works)
- Fixing symptoms without understanding cause
- Multiple simultaneous changes
- Deleting failing tests to "pass"
- Leaving code in broken state
