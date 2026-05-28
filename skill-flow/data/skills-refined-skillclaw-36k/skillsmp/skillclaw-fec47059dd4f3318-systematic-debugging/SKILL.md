---
name: systematic-debugging
description: Use this skill when encountering bugs, errors, failing tests, or unexpected behavior. It provides a structured approach to debugging through evidence-based root cause investigation using a four-phase framework.
---

# Systematic Debugging

Evidence-based investigation -> root cause -> verified fix.

<when_to_use>

- Bugs, errors, exceptions, crashes
- Unexpected behavior or wrong results
- Failing tests (unit, integration, e2e)
- Intermittent or timing-dependent failures
- Performance issues (slow, memory leaks, high CPU)
- Integration failures (API, database, external services)

NOT for: obvious fixes, feature requests, architecture planning

</when_to_use>

<iron_law>

**NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST**

Never propose solutions or "try this" without understanding root cause through systematic investigation.

</iron_law>

<phases>

| Phase | Trigger | activeForm |
|-------|---------|------------|
| Collect Evidence | Session start | "Collecting evidence" |
| Isolate Variables | Evidence gathered | "Isolating variables" |
| Formulate Hypotheses | Problem isolated | "Formulating hypotheses" |
| Test Hypothesis | Hypothesis formed | "Testing hypothesis" |
| Verify Fix | Fix identified | "Verifying fix" |

**Situational** (insert when triggered):
- Iterate -> Hypothesis disproven, loops back with new hypothesis

**Workflow:**
- Start: "Collect Evidence" as `in_progress`
- Transition: Mark current `completed`, add next `in_progress`
- Failed hypothesis: Add "Iterate" task
- Quick fixes: If root cause obvious from error, skip to "Verify Fix" (still create failing test)
- Need more evidence: Add new evidence task (don't regress phases)
- Circuit breaker: After 3 failed hypotheses -> escalate

</phases>

<quick_start>

1. Create "Collect Evidence" todo as `in_progress`
2. Reproduce - exact steps to trigger consistently
3. Investigate - gather evidence about what's happening
4. Analyze - compare working vs broken, find differences
5. Test hypothesis - single specific hypothesis, minimal test
6. Implement - failing test first, then fix
7. Update todos on phase transitions

</quick_start>

<phase_1_root_cause>

Goal: Understand what's actually happening.

Transition: Mark complete when you have reproduction steps and initial evidence.

**Read error messages completely**
- Stack traces top to bottom
- Note file paths, line numbers, variable names

</phase_1_root_cause>