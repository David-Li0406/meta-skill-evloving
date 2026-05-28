---
name: systematic-debugging
description: Use this skill when encountering any bug, test failure, or unexpected behavior, before proposing fixes.
---

# Systematic Debugging

## Overview

Random fixes waste time and create new bugs. Quick patches mask underlying issues.

**Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

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
   - Read stack traces completely and note line numbers, file paths, error codes.

2. **Reproduce Consistently**
   - Can you trigger it reliably? Document the exact steps that trigger the failure.
   - If not reproducible → gather more data, don't guess.

3. **Check Recent Changes**
   - Review recent commits, new dependencies, configuration changes, and environmental differences.

4. **Gather Evidence in Multi-Component Systems**
   - Add diagnostic instrumentation at each component boundary to identify where it breaks.

5. **Trace Data Flow**
   - Follow the data flow backward from the error to find the source of the bad value.

### Phase 2: Pattern Analysis

**Find the pattern before fixing:**

1. **Find Working Examples**
   - Locate similar working code in the same codebase.

2. **Compare Against References**
   - Read reference implementations thoroughly to understand their dependencies and settings.

3. **Identify Differences**
   - List every difference between working and broken code.

4. **Understand Dependencies**
   - Identify what other components are needed and what assumptions are made.

### Phase 3: Hypothesis and Testing

**Scientific method:**

1. **Form Single Hypothesis**
   - State clearly: "I think X is the root cause because Y."

2. **Test Minimally**
   - Make the SMALLEST possible change to test the hypothesis.

3. **Verify Before Continuing**
   - Did it work? If not, form a new hypothesis.

4. **When You Don't Know**
   - Acknowledge your uncertainty and seek help or research more.

### Phase 4: Implementation

**Fix the root cause, not the symptom:**

1. **Create Failing Test Case**
   - Ensure you have a test that reproduces the issue before fixing it.

2. **Implement Single Fix**
   - Address the root cause identified with one change at a time.

3. **Verify Fix**
   - Ensure the test passes and no other tests are broken.

4. **If Fix Doesn't Work**
   - Count how many fixes you've tried. If ≥ 3, question the architecture.

5. **If 3+ Fixes Failed: Question Architecture**
   - Discuss with your human partner before attempting more fixes.

## Red Flags - STOP and Follow Process

If you catch yourself thinking:
- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "I don't fully understand but this might work"

**ALL of these mean: STOP. Return to Phase 1.**

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Issue is simple, don't need process" | Simple issues have root causes too. |
| "Emergency, no time for process" | Systematic debugging is FASTER than guess-and-check thrashing. |
| "Just try this first, then investigate" | First fix sets the pattern. Do it right from the start. |

## Quick Reference

| Phase | Key Activities | Success Criteria |
|-------|---------------|------------------|
| **1. Root Cause** | Read errors, reproduce, check changes, gather evidence | Understand WHAT and WHY |
| **2. Pattern** | Find working examples, compare | Identify differences |
| **3. Hypothesis** | Form theory, test minimally | Confirmed or new hypothesis |
| **4. Implementation** | Create test, fix, verify | Bug resolved, tests pass |

## When Process Reveals "No Root Cause"

If systematic investigation reveals the issue is truly environmental or external:
1. Document what you investigated.
2. Implement appropriate handling (retry, timeout, error message).
3. Add monitoring/logging for future investigation.

**But:** 95% of "no root cause" cases are incomplete investigation.

## Supporting Techniques

- **`root-cause-tracing.md`** - Trace bugs backward through the call stack.
- **`defense-in-depth.md`** - Add validation at multiple layers after finding root cause.
- **`condition-based-waiting.md`** - Replace arbitrary timeouts with condition polling.

**Related skills:**
- **superpowers:test-driven-development** - For creating failing test cases.
- **superpowers:verification-before-completion** - Verify fix worked before claiming success.

## Real-World Impact

From debugging sessions:
- Systematic approach: 15-30 minutes to fix.
- Random fixes approach: 2-3 hours of thrashing.
- First-time fix rate: 95% vs 40%.
- New bugs introduced: Near zero vs common.