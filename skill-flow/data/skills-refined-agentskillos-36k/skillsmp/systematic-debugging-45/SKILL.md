---
name: systematic-debugging
description: Use when encountering bugs, test failures, unexpected behavior, or performance issues before proposing fixes.
allowed-tools: ["shell", "read_file", "apply_patch", "update_plan"]
metadata:
  short-description: Root-cause-first debugging workflow
---

# Systematic Debugging

**Read these references:**
- `~/.config/agent/core/behavior.md` - Evidence-based reasoning
- `~/.config/agent/core/methodology.md` - Problem-solving framework
- `~/.config/agent/domain/testing/unit.md` - Test strategy

## Overview

Random fixes waste time. Always find the root cause before fixing symptoms.

**Core principle:** Root-cause investigation before fixes.

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

## Phase 1: Root Cause Investigation

1. **Read errors carefully** (stack traces, line numbers, error codes)
2. **Reproduce consistently** (steps, frequency, exact conditions)
3. **Check recent changes** (diffs, dependency changes, env changes)
4. **Gather evidence across boundaries** (log inputs/outputs between layers)
5. **Trace data flow** (use `root-cause-tracing.md`)

## Phase 2: Pattern Analysis

1. Find working examples in the codebase
2. Compare against references completely
3. List every difference (no assumptions)
4. Identify dependencies and assumptions

## Phase 3: Hypothesis & Testing

1. Form a single, explicit hypothesis
2. Test minimally (one variable at a time)
3. Verify before proceeding
4. If uncertain, pause and ask

## Phase 4: Implementation

1. **Create a failing repro test** when feasible
   - Prefer automated tests; one-off scripts if needed
   - If strict TDD is required, invoke `tdd-enforce`
2. Implement a single fix for the root cause
3. Verify the fix (re-run tests, check regressions)
4. If 3+ fixes fail, stop and question architecture

## Red Flags — STOP

- “Quick fix now, investigate later”
- Multiple fixes at once
- Guessing without evidence
- Skipping the repro test when feasible

## Supporting Techniques

- `root-cause-tracing.md` - Trace bugs backward to source
- `defense-in-depth.md` - Layered validation after root cause found
- `condition-based-waiting.md` - Replace arbitrary sleeps with conditions

## Arguments

Target: ${ARGUMENTS}
