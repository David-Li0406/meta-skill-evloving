---
name: systematic-debugging
description: Use this skill when encountering any bug, test failure, or unexpected behavior, to ensure understanding before proposing fixes through a structured four-phase framework.
---

# Systematic Debugging

## Overview

Random fixes waste time and create new bugs. Quick patches mask underlying issues. This skill guides you through a systematic process of identifying, reproducing, and fixing bugs.

## When To Use

- Users report a bug
- You encounter an unexpected error
- Tests are failing inexplicably
- Any technical issue, including performance problems and integration issues

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1, you cannot propose fixes.

## The Four Phases

You MUST complete each phase before proceeding to the next.

### Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:**

1. **Read Error Messages Carefully**
   - Don't skip past errors or warnings; they often contain the exact solution.
   - Read stack traces completely and note line numbers, file paths, and error codes.

2. **Reproduce Consistently**
   - Can you trigger it reliably? What are the exact steps?
   - If not reproducible, gather more data instead of guessing.

3. **Check Recent Changes**
   - What changed that could cause this? Review recent commits and environmental differences.

4. **Gather Evidence in Multi-Component Systems**
   - For systems with multiple components, log data entering and exiting each component to identify where it breaks.

5. **Trace Data Flow**
   - If the error is deep in the call stack, trace back to find the source of the bad value.

### Phase 2: Pattern Analysis

**Find the pattern before fixing:**

1. **Find Working Examples**
   - Locate similar working code in the same codebase.

2. **Compare Against References**
   - Read reference implementations completely to understand the pattern fully.

3. **Identify Differences**
   - List every difference between working and broken code.

4. **Understand Dependencies**
   - Identify other components, settings, and assumptions related to the issue.

### Phase 3: Hypothesis and Testing

**Scientific method:**

1. **Form Single Hypothesis**
   - Clearly state your hypothesis about the root cause.

2. **Test Minimally**
   - Make the smallest possible change to test your hypothesis.

3. **Verify Before Continuing**
   - Confirm whether your hypothesis was correct before proceeding.

4. **When You Don't Know**
   - Acknowledge gaps in understanding and seek help or conduct further research.

### Phase 4: Implementation

**Fix the root cause, not the symptom:**

1. **Create Failing Test Case**
   - Develop the simplest possible reproduction of the issue.

2. **Implement Single Fix**
   - Address the identified root cause with one change at a time.

3. **Verify Fix**
   - Ensure that the fix resolves the issue without breaking other tests.

4. **If Fix Doesn't Work**
   - If multiple fixes have failed, return to Phase 1 and re-analyze the situation.

## Red Flags - STOP and Follow Process

If you catch yourself thinking:
- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "Skip the test, I'll manually verify"

**ALL of these mean: STOP. Return to Phase 1.**

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Issue is simple, don't need process" | Simple issues have root causes too. |
| "Emergency, no time for process" | Systematic debugging is FASTER than guess-and-check. |
| "Just try this first, then investigate" | First fix sets the pattern. Do it right from the start. |

## Real-World Impact

From debugging sessions:
- Systematic approach: 15-30 minutes to fix
- Random fixes approach: 2-3 hours of thrashing
- First-time fix rate: 95% vs 40%
- New bugs introduced: Near zero vs common

## Integration with Other Skills

This skill requires using:
- **root-cause-tracing** for deep call stack errors
- **test-driven-development** for creating failing test cases

Complementary skills include:
- **defense-in-depth** for validation at multiple layers
- **verification-before-completion** to ensure fixes are effective