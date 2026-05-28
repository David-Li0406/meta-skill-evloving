---
name: systematic-debugging
description: Use this skill when investigating bugs, errors, unexpected behavior, or failed tests, emphasizing root cause analysis before applying fixes.
---

# Systematic Debugging

## Core Principle

**NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST.**

Never apply symptom-focused patches that mask underlying problems. Understand WHY something fails before attempting to fix it.

## The Four-Phase Framework

### Phase 1: Root Cause Investigation

Before touching any code:

1. **Read error messages thoroughly** - Every word matters.
2. **Reproduce the issue consistently** - If you can't reproduce it, you can't verify a fix.
3. **Examine recent changes** - What changed before this started failing?
4. **Gather diagnostic evidence** - Logs, stack traces, state dumps.
5. **Trace data flow** - Follow the call chain to find where bad values originate.

**Root Cause Tracing Technique:**

```
1. Observe the symptom - Where does the error manifest?
2. Find immediate cause - Which code directly produces the error?
3. Ask "What called this?" - Map the call chain upward.
4. Keep tracing up - Follow invalid data backward through the stack.
5. Find original trigger - Where did the problem actually start?
```

### Phase 2: Pattern Analysis

1. **Locate working examples** - Find similar code that works correctly.
2. **Compare implementations completely** - Don't just skim.
3. **Identify differences** - What's different between working and broken?
4. **Understand dependencies** - What does this code depend on?

### Phase 3: Hypothesis and Testing

Apply the scientific method:

1. **Formulate ONE clear hypothesis** - "The error occurs because X."
2. **Design minimal test** - Change ONE variable at a time.
3. **Predict the outcome** - What should happen if the hypothesis is correct?
4. **Run the test** - Execute and observe.
5. **Did it behave as predicted?**
6. **Iterate or proceed** - Refine hypothesis if wrong, implement if right.

### Phase 4: Implementation

1. **Create failing test case** - Captures the bug behavior.
2. **Implement single fix** - Address root cause, not symptoms.
3. **Verify test passes** - Confirms fix works.
4. **Run full test suite** - Ensure no regressions.
5. **If fix fails, STOP** - Re-evaluate hypothesis.

## Common Debugging Techniques

- Add logging at critical points.
- Use breakpoints and step-through debugging.
- Check input/output at boundaries.
- Review recent changes in version control.
- Compare working vs broken states.

## Adversary Gates

Three phases have adversary gates that challenge your work:

1. **HYPOTHESIZE** - Adversary challenges your hypothesis.
2. **PROVE** - Adversary verifies your proof.
3. **FIX** - Adversary checks if the fix matches proof.

## Instrumentation

```bash
# Log usage when using this skill
./scripts/log-skill.sh "systematic-debugging" "manual" "$$"
```