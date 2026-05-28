---
name: systematic-debugging
description: Use this skill when encountering any bug, test failure, or unexpected behavior, before proposing fixes. It provides a four-phase framework (root cause investigation, pattern analysis, hypothesis testing, implementation) to ensure understanding before attempting solutions.
---

# Systematic Debugging

## Overview

Random fixes waste time and create new bugs. Quick patches mask underlying issues.

**Core principle:** ALWAYS find the root cause before attempting fixes. Symptom fixes are a failure.

**The Iron Law:**

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
   - Read stack traces completely and note line numbers, file paths, and error codes.

2. **Reproduce Consistently**
   - Can you trigger it reliably? What are the exact steps?
   - Does it happen every time? If not reproducible, gather more data, don't guess.

3. **Check Recent Changes**
   - What changed that could cause this? Review Git diffs, recent commits, new dependencies, and config changes.

4. **Gather Evidence in Multi-Component Systems**
   - When the system has multiple components (e.g., CI → build → signing, API → service → database), add diagnostic instrumentation:
   ```
   For EACH component boundary:
     - Log what data enters the component
     - Log what data exits the component
     - Verify environment/config propagation
     - Check state at each layer
   ```

   Run once to gather evidence showing WHERE it breaks, then analyze.

### Phase 2: Pattern Analysis

- Identify patterns in the data collected during Phase 1.
- Look for commonalities in failures or behaviors.

### Phase 3: Hypothesis Testing

- Formulate hypotheses based on the patterns identified.
- Test each hypothesis systematically to confirm or refute.

### Phase 4: Implementation

- Once the root cause is identified and a solution is confirmed, implement the fix.
- Monitor the system to ensure the issue is resolved and no new issues arise.