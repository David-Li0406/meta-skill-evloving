---
name: systematic-debugging
description: Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes
---

# Systematic Debugging

**Core principle:** ALWAYS find root cause before attempting fixes.

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

## The Four Phases

### Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:**

1. **Read Error Messages Carefully** - Stack traces, line numbers, error codes
2. **Reproduce Consistently** - Exact steps, every time?
3. **Check Recent Changes** - Git diff, new deps, config changes
4. **Gather Evidence in Multi-Component Systems** - Log data at each component boundary, run once, analyze WHERE it breaks

### Phase 2: Pattern Analysis

1. **Find Working Examples** - Similar working code in same codebase
2. **Compare Against References** - Read reference implementation COMPLETELY
3. **Identify Differences** - List every difference, however small

### Phase 3: Hypothesis and Testing

1. **Form Single Hypothesis** - "I think X is the root cause because Y"
2. **Test Minimally** - SMALLEST possible change, one variable at a time
3. **Verify Before Continuing** - Didn't work? Form NEW hypothesis, don't stack fixes

### Phase 4: Implementation

1. **Create Failing Test Case** - MUST have before fixing
2. **Implement Single Fix** - ONE change at a time, no "while I'm here" improvements
3. **Verify Fix** - Test passes? No other tests broken?
4. **If 3+ Fixes Failed** - STOP. Question the architecture, discuss with human partner

## Red Flags - STOP and Return to Phase 1

- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "I don't fully understand but this might work"
- Proposing solutions before tracing data flow
- Each fix reveals new problem in different place

## Quick Reference

| Phase             | Key Activity                          | Success Criteria            |
| ----------------- | ------------------------------------- | --------------------------- |
| 1. Root Cause     | Read errors, reproduce, check changes | Understand WHAT and WHY     |
| 2. Pattern        | Find working examples, compare        | Identify differences        |
| 3. Hypothesis     | Form theory, test minimally           | Confirmed or new hypothesis |
| 4. Implementation | Create test, fix, verify              | Bug resolved, tests pass    |
