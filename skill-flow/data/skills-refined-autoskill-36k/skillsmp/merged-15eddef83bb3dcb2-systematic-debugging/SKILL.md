---
name: systematic-debugging
description: Use this skill when encountering bugs, test failures, or unexpected behavior to systematically trace root causes and validate fixes.
---

# Systematic Debugging

**Iron Law:** "NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST"

## When to Use

Use this skill when:
- A test fails and you need to understand why.
- An error is thrown and you need to find the cause.
- A feature behaves unexpectedly.
- Performance degrades and you need to identify bottlenecks.
- Data corruption occurs and you need to trace the source.
- A bug reappears after "fixing" it.

## Red Flags (Violation Indicators)

Detect these patterns that indicate skipping root cause investigation:
- **Fix without understanding** - "I'll just add a null check" (why is it null?)
- **Skip to solution** - "Let me try wrapping this in setTimeout" (why does timing matter?)
- **Restart tools** - "Let me restart the dev server" (what state is corrupted?)
- **Clear cache** - "Let me clear the cache" (what cache entry is stale?)
- **Change multiple things** - "Let me update these 3 files" (which one fixes it?)
- **Shouldn't cause problem** - "This change shouldn't affect that" (but it does, why?)
- **Assume cause** - "Must be a race condition" (what evidence supports this?)

## Key Concepts

### 1. Root Cause vs. Symptom

**Symptom:** What you observe (test fails, error thrown, wrong output)  
**Root Cause:** Why it happens (null value, wrong condition, missing await)

**Example:**
```
Symptom: "TypeError: Cannot read property 'name' of undefined"
Root Cause: API returns null when user not found, but code expects object
```

### 2. Data Flow Tracing

**Principle:** Follow data from source to error point

**Steps:**
1. Identify error location (stack trace line number).
2. Identify data involved (variable name, object property).
3. Trace backwards: Where does this data come from?
4. Find divergence: Where does actual differ from expected?

### 3. Hypothesis-Driven Debugging

**Principle:** Form hypothesis, test with evidence, refine

**Process:**
1. **Observe:** What is the symptom? (error message, wrong output)
2. **Hypothesize:** What could cause this? (list 2-3 possibilities)
3. **Predict:** If hypothesis is true, what else should I see?
4. **Test:** Add logging, check state, run minimal reproduction.
5. **Conclude:** Does evidence support hypothesis? If no, try next hypothesis.

### 4. Fix Verification

**Principle:** Verify fix addresses root cause, not just symptom

**Checklist:**
- [ ] Test that was failing now passes.
- [ ] Test passes for the reason you expect (not coincidence).
- [ ] Test fails if you revert the fix (confirms fix is necessary).
- [ ] Related tests still pass (no regressions).
- [ ] Root cause is addressed in fix (not just symptom).

## 4-Phase Debugging Process

### Phase 1: TRACE DATA FLOW

**Objective:** Identify where actual diverges from expected

**Steps:**
1. Read error message (what failed?).
2. Read stack trace (where failed?).
3. Identify data involved (what value is wrong?).
4. Trace backwards from error to source.
5. Log intermediate values to find divergence point.

### Phase 2: IDENTIFY DIVERGENCE

**Objective:** Determine why actual differs from expected

**Questions:**
- What is the expected value? (from spec, test, documentation)
- What is the actual value? (from logs, debugger, state inspection)
- Where does the divergence occur? (which function, which line)
- What changed recently? (git diff, recent commits)

### Phase 3: HYPOTHESIZE ROOT CAUSE

**Objective:** Form testable hypothesis about why divergence occurred

**Hypothesis Template:**
```
"I believe [divergence] occurs because [root cause].
If this is true, I should see [evidence].
I can test this by [action]."
```

### Phase 4: VERIFY FIX

**Objective:** Confirm fix addresses root cause

**Verification Steps:**
1. Write test that reproduces the bug (fails before fix).
2. Apply fix.
3. Run test (should pass).
4. Explain why fix works (addresses root cause).
5. Run regression tests (no side effects).

## Debugging Strategies by Problem Type

### Test Fails

**Strategy:** Identify assertion, trace data, find divergence.

### Performance Slow

**Strategy:** Profile execution, identify bottleneck.

### Data Corruption

**Strategy:** Trace data mutations, find unexpected write.

### Error Thrown

**Strategy:** Read stack trace, identify throw location, trace backwards.

### Feature Broken

**Strategy:** Identify last working state, compare changes.

## Common Root Causes

### Type Issues
- **Null/undefined:** Value is null when code expects object.
- **String vs. number:** "42" treated as string, not number.
- **Array vs. object:** Iterating object as array.
- **Promise vs. value:** Forgot to await async function.

### Async Issues
- **Race condition:** Two async operations modify same state.
- **Promise not awaited:** Code continues before async completes.
- **Callback hell:** Nested callbacks lose error context.
- **Event ordering:** Events fire in unexpected order.

### Data Issues
- **Validation failed:** Input doesn't match expected format.
- **Format changed:** API response structure changed.
- **Stale cache:** Cached data is outdated.
- **Encoding mismatch:** UTF-8 vs. ASCII, JSON vs. string.

### Logic Issues
- **Wrong condition:** if (x > 5) should be if (x >= 5).
- **Early return:** Function returns before reaching correct code.
- **Off-by-one:** Loop iterates n-1 or n+1 times.
- **Short-circuit:** && or || causes early exit.

### Environment Issues
- **Env var not set:** Missing API_KEY environment variable.
- **Service not running:** Database or API server is down.
- **Version mismatch:** Dependency version incompatibility.
- **Permission denied:** File or directory not accessible.

## Integration with Other Skills

### With verification-before-completion
After debugging and fixing, confirm:
- Test that was failing now passes.
- Root cause is addressed in fix.
- No regressions introduced.

### With test-driven-development
When debugging reveals a bug:
1. Write test that reproduces the bug (RED phase).
2. Debug to find root cause (this skill).
3. Implement fix (GREEN phase).
4. Refactor if needed (REFACTOR phase).

### With agent-coordination-discipline
For complex debugging requiring multiple investigations:
- Use agent delegation when debugging spans multiple services.
- Define clear success criteria: "Find root cause of timeout".

## Enforcement Checklist

Before marking debugging task complete:
- [ ] Root cause identified (not just symptom).
- [ ] Data flow traced from source to error.
- [ ] Hypothesis tested with evidence.
- [ ] Fix verified to address root cause.
- [ ] Test added to prevent regression.
- [ ] Related tests still pass (no side effects).
- [ ] Can explain WHY fix works (not just THAT it works).

**If any checkbox is unchecked, continue debugging. Do not apply fix until root cause is understood.**