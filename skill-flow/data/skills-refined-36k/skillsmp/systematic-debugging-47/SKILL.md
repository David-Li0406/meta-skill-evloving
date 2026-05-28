---
name: systematic-debugging
description: Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes - four-phase framework (root cause investigation, pattern analysis, hypothesis testing, implementation) that ensures understanding before attempting solutions
context: fork
---

# Systematic Debugging

## Quick Reference

For detailed patterns and troubleshooting, see:
- [DEBUG-PATTERNS.md](DEBUG-PATTERNS.md) - Multi-component diagnostics, data flow tracing, hypothesis testing
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Red flags, common mistakes, architectural issues

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1, you cannot propose fixes.

**Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

## When to Use

Use for ANY technical issue: test failures, bugs, unexpected behavior, performance problems, build failures.

**Use ESPECIALLY when:**
- Under time pressure (emergencies make guessing tempting)
- "Just one quick fix" seems obvious
- You've already tried multiple fixes

## The Four Phases

### Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:**

1. **Read Error Messages Carefully**
   - Don't skip past errors or warnings
   - Read stack traces completely
   - Note line numbers, file paths, error codes

2. **Reproduce Consistently**
   - Can you trigger it reliably?
   - If not reproducible → gather more data, don't guess

3. **Check Recent Changes**
   - Git diff, recent commits
   - New dependencies, config changes

4. **Gather Evidence** (see DEBUG-PATTERNS.md for multi-component systems)

5. **Trace Data Flow** - Where does bad value originate?

### Phase 2: Pattern Analysis

1. Find working examples in same codebase
2. Compare against references - read COMPLETELY
3. Identify ALL differences between working and broken
4. Understand dependencies and assumptions

### Phase 3: Hypothesis and Testing

1. **Form Single Hypothesis** - "I think X is root cause because Y"
2. **Test Minimally** - SMALLEST possible change, one variable
3. **Verify** - Did it work? If not, form NEW hypothesis (don't stack fixes)

### Phase 4: Implementation

1. **Create Failing Test Case** - MUST have before fixing
2. **Implement Single Fix** - ONE change, no bundled improvements
3. **Verify Fix** - Tests pass, no regressions

**If Fix Doesn't Work:**
- Count fixes attempted
- If < 3: Return to Phase 1
- If ≥ 3: STOP and question architecture (see TROUBLESHOOTING.md)

## Quick Reference Table

| Phase | Key Activities | Success Criteria |
|-------|---------------|------------------|
| **1. Root Cause** | Read errors, reproduce, check changes, gather evidence | Understand WHAT and WHY |
| **2. Pattern** | Find working examples, compare | Identify differences |
| **3. Hypothesis** | Form theory, test minimally | Confirmed or new hypothesis |
| **4. Implementation** | Create test, fix, verify | Bug resolved, tests pass |
