---
name: systematic-debugging
description: This skill should be used when the user reports a "bug", "not working", "fix this", "debug", "test failing", or when investigating unexpected behavior. Four-phase framework ensuring root cause understanding before attempting solutions.
allowed-tools: Read, Bash, Grep, Skill, mcp__plugin_serena_serena, mcp__plugin_serena_serena_*
---

# Systematic Debugging

**Announce at start:** "I'm using the systematic-debugging skill to investigate this issue."

Random fixes waste time and create new bugs. Quick patches mask underlying issues.

**Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

**Violating the letter of this process is violating the spirit of debugging.**

## The Iron Law

```text
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1, you cannot propose fixes.

## The Four Phases

### Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:**

1. **Read error messages carefully** - They often contain the solution
2. **Reproduce consistently** - If not reproducible, gather more data
3. **Check recent changes** - Git diff, new dependencies, config changes
4. **Trace data flow** - Where does bad value originate?

For deep call stack errors, use **root-cause-tracing** skill.

For multi-component systems, add diagnostic instrumentation at each boundary before proposing fixes.

### Phase 2: Pattern Analysis

1. **Find working examples** - Similar working code in same codebase
2. **Compare against references** - Read reference implementation completely
3. **Identify differences** - List every difference, however small
4. **Understand dependencies** - What settings, config, environment?

### Phase 3: Hypothesis and Testing

1. **Form single hypothesis** - "I think X is the root cause because Y"
2. **Test minimally** - Smallest possible change, one variable at a time
3. **Verify before continuing** - Didn't work? Form NEW hypothesis

### Phase 4: Implementation

**Fix the root cause, not the symptom:**

1. **Create failing test case**
   - Simplest possible reproduction
   - Use **dev-workflow:test-driven-development** skill
   - MUST have before fixing

2. **Implement single fix**
   - Address the root cause identified
   - ONE change at a time
   - No "while I'm here" improvements
   - No bundled refactoring

3. **Verify fix**
   - Test passes now?
   - No other tests broken?
   - Issue actually resolved?

4. **If fix doesn't work**
   - STOP
   - Count: How many fixes have you tried?
   - If < 3: Return to Phase 1, re-analyze with new information
   - **If ≥ 3: STOP and question the architecture (see below)**
   - DON'T attempt Fix #4 without architectural discussion

## Red Flags - STOP

When catching these thoughts:

- "Quick fix for now, investigate later"
- "Just try changing X and see"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- Proposing solutions before tracing data flow
- "Here are the main problems: [lists fixes without investigation]"
- **"One more fix attempt" (when already tried 2+)**
- **Each fix reveals new problem in different place**

**All mean: STOP. Return to Phase 1.**

**If 3+ fixes failed:** Question the architecture (see below).

## Quick Reference

| Phase             | Key Activities                 | Success Criteria            |
| ----------------- | ------------------------------ | --------------------------- |
| 1. Root Cause     | Read errors, reproduce, trace  | Understand WHAT and WHY     |
| 2. Pattern        | Find working examples, compare | Identify differences        |
| 3. Hypothesis     | Form theory, test minimally    | Confirmed or new hypothesis |
| 4. Implementation | Create test, fix, verify       | Bug resolved, tests pass    |

## When 3+ Fixes Failed: Question Architecture

**Pattern indicating architectural problem:**

- Each fix reveals new shared state/coupling/problem in different place
- Fixes require "massive refactoring" to implement
- Each fix creates new symptoms elsewhere

**This is NOT a failed hypothesis - this is a wrong architecture.**

**STOP and question fundamentals:**

```text
BEFORE attempting Fix #4:

1. Have I tried 3+ fixes for this issue?
   If YES → STOP

2. Does each fix reveal a new problem?
   If YES → Architecture problem, not bug

3. Questions to ask:
   - Is this pattern fundamentally sound?
   - Are we "sticking with it through sheer inertia"?
   - Should we refactor architecture vs. continue fixing symptoms?

4. Discuss with human partner before attempting more fixes
```

**Do NOT:**
- "One more fix might work"
- Keep adding patches
- Assume the architecture is correct

**DO:**
- Present findings: "3 fix attempts, each revealed new problem"
- Propose architectural discussion
- Wait for guidance before proceeding

## Additional Resources

### Reference Files

For detailed guidance:

- **`references/phase-details.md`** - Expanded phase procedures
- **`references/rationalizations.md`** - Common excuses and rebuttals

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Issue is simple, don't need process" | Simple issues have root causes too. Process is fast for simple bugs. |
| "Emergency, no time for process" | Systematic debugging is FASTER than guess-and-check thrashing. |
| "Just try this first, then investigate" | First fix sets the pattern. Do it right from the start. |
| "I'll write test after confirming fix works" | Untested fixes don't stick. Test first proves it. |
| "Multiple fixes at once saves time" | Can't isolate what worked. Causes new bugs. |
| "I see the problem, let me fix it" | Seeing symptoms ≠ understanding root cause. |
| "One more fix attempt" (after 2+ failures) | 3+ failures = architectural problem. Question pattern, don't fix again. |

## Real-World Impact

| Approach | Outcome |
|----------|---------|
| Systematic debugging | 15-30 minutes to fix |
| Random fixes approach | 2-3 hours of thrashing |
| First-time fix rate (systematic) | 95% |
| First-time fix rate (random) | 40% |
| New bugs introduced (systematic) | Near zero |
| New bugs introduced (random) | Common |

**The math is clear:** Systematic beats random every time.

## Integration

- **dev-workflow:root-cause-tracing** - REQUIRED for deep call stack errors (Phase 1)
- **dev-workflow:test-driven-development** - REQUIRED for failing test case (Phase 4)
- **dev-workflow:defense-in-depth** - Add validation layers after fix
- **dev-workflow:verification-before-completion** - Verify fix before claiming success
