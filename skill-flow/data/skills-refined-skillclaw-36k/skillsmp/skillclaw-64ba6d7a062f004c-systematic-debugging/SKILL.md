---
name: systematic-debugging
description: Use this skill when encountering any bug, test failure, or unexpected behavior, before proposing fixes.
---

# Systematic Debugging

## Overview

Random fixes waste time and create new bugs. Quick patches mask underlying issues. The core principle is to **always find the root cause before attempting fixes**. Symptom fixes are failures.

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed the root cause investigation, you cannot propose fixes.

## When to Use

Use for any technical issue:
- Test failures
- Bugs in production
- Unexpected behavior
- Performance problems
- Build failures
- Integration issues

**Especially valuable when:**
- Under time pressure (emergencies make guessing tempting)
- "Just one quick fix" seems obvious
- Previous attempts haven't worked
- You don't fully understand the issue

**Don't skip when:**
- The issue seems simple (simple bugs have root causes too)
- You're in a hurry (rushing guarantees rework)
- A manager wants it fixed immediately (systematic is faster than thrashing)

## The Four Phases

You must complete each phase before proceeding to the next.

### Phase 1: Root Cause Investigation

**Before attempting any fix:**

1. **Read Error Messages Carefully**
   - Don't skip past errors or warnings; they often contain the exact solution.
   - Read stack traces completely and note line numbers, file paths, and error codes.

2. **Reproduce Consistently**
   - Can you trigger it reliably? What are the exact steps?
   - If not reproducible, gather more data instead of guessing.

3. **Check Recent Changes**
   - What changed that could cause this? Review recent commits, new dependencies, and configuration changes.

4. **Gather Evidence in Multi-Component Systems**
   - For systems with multiple components, add diagnostic instrumentation:
   ```
   For each component boundary:
     - Log what data enters and exits the component.
     - Verify environment/config propagation.
     - Check state at each layer.
   ```

### Phase 2: Trace the Problem
- Follow the data flow backward from the error to identify the source of the problem.

### Phase 3: Compare with Working Code
- Find similar code that works correctly and compare systematically.

### Phase 4: Test Understanding
- Form a clear hypothesis about the cause of the problem and test with minimal changes.

### Implement Fix
- Create a test that reproduces the issue before fixing it to ensure understanding and verify the fix works.

By following these steps, you can systematically debug issues and implement effective solutions.