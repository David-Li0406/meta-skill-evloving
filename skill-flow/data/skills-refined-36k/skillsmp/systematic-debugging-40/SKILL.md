---
name: systematic-debugging
description: Structured debugging process for bugs. Reproduces, isolates, hypothesizes, tests, fixes minimally, and documents learnings.
---

# Systematic Debugging

## Core Purpose

Debug issues through a structured process rather than random changes. Reproduce the bug, isolate the cause, form a hypothesis, write a failing test, make a minimal fix, and document what was learned.

## Operating Philosophy

### What This Skill IS

- **Methodical investigator** who follows evidence systematically
- **Hypothesis tester** who validates theories before fixing
- **Minimal fixer** who makes the smallest change that works
- **Knowledge capturer** who documents for future reference
- **Test writer** who captures the bug in a test first

### What This Skill IS NOT

- A random code changer who tries things until they work
- A perfectionist who refactors while debugging
- A scope creeper who fixes "related" issues
- A cowboy who fixes without tests

## Activation Protocol

When activated:

1. **Gather symptoms** - What's the observable problem?
2. **Reproduce** - Can we trigger it reliably?
3. **Isolate** - Narrow to smallest failing case
4. **Hypothesize** - Form theory about root cause
5. **Test** - Write failing test that captures the bug
6. **Fix** - Minimal change to pass the test
7. **Verify** - Run full test suite
8. **Document** - Record learnings if significant

---

## Phase 1: Gather Symptoms

### Collect All Available Information

| Category  | Questions to Answer                          |
| --------- | -------------------------------------------- |
| What      | What's the observed vs expected behavior?    |
| When      | When did it start? What changed recently?    |
| Where     | Which file/function/line? Which environment? |
| Who       | Which users/inputs/scenarios trigger it?     |
| Frequency | Always, sometimes, or rarely?                |

### Read Error Context

- Full error message and stack trace
- Relevant logs (before and after the error)
- Input data that triggered the bug
- Environment details (versions, config)

---

## Phase 2: Reproduce

### Establish Reliable Reproduction

**Goal:** Trigger the bug consistently on demand.

**Steps:**

1. Start with the reported reproduction steps
2. Simplify - remove anything that doesn't affect the bug
3. Document the minimal reproduction case
4. Verify it fails consistently (run 3+ times)

**If bug is intermittent:**

- Look for race conditions
- Check for timing dependencies
- Log more context to understand patterns
- Add timestamps to narrow window

### Document Reproduction

```markdown
## Reproduction

**Environment:** [Node version, OS, etc.]

**Steps:**

1. [Step]
2. [Step]
3. [Step]

**Expected:** [What should happen]
**Actual:** [What happens instead]

**Reproduction rate:** [X/X attempts]
```

---

## Phase 3: Isolate

### Narrow the Scope

**Binary search approach:**

1. Identify the boundaries of potentially affected code
2. Split in half - is the bug in the first or second half?
3. Repeat until you've found the specific location

**Isolation techniques:**

| Technique               | When to Use                                |
| ----------------------- | ------------------------------------------ |
| Binary search           | Large area, unclear location               |
| Divide and conquer      | Multiple components interacting            |
| Minimal input           | Simplest data that still triggers bug      |
| Environment elimination | Works in some envs, not others             |
| Git bisect              | Bug introduced recently, known good commit |

### Key Questions

- What's the smallest input that triggers the bug?
- What's the smallest code path that reproduces it?
- Can we trigger it in isolation (unit) or only integration?
- Which specific line of code produces the wrong behavior?

---

## Phase 4: Hypothesize

### Form a Theory

Based on gathered evidence, form a clear hypothesis:

```markdown
## Hypothesis

**Root cause:** [Specific explanation of what's wrong]

**Why this explains the symptoms:**

- [How it accounts for observation 1]
- [How it accounts for observation 2]

**Prediction:** If this hypothesis is correct, then:

- [Testable prediction 1]
- [Testable prediction 2]
```

### Common Bug Patterns

Check for these common causes:

| Pattern        | Symptoms                      | Where to Look                         |
| -------------- | ----------------------------- | ------------------------------------- |
| Off-by-one     | Works except at boundaries    | Loop conditions, array indices        |
| Null/undefined | Random crashes                | Optional chaining, default values     |
| Race condition | Intermittent failures         | Async code, shared state              |
| Type coercion  | Unexpected comparisons        | String/number mixing, equality checks |
| State mutation | Works first time only         | Object references, caching            |
| Missing await  | Partial execution             | Async functions, promises             |
| Wrong scope    | Variable has unexpected value | Closures, hoisting                    |

---

## Phase 5: Test-First Fix

### Write a Failing Test

**Before fixing anything**, write a test that:

1. Reproduces the bug
2. Fails with current code
3. Will pass when the bug is fixed
4. Guards against regression

```typescript
// Example test structure
describe('bugfix: [brief description]', () => {
  it('should [expected behavior] when [condition that caused bug]', () => {
    // Arrange - set up the buggy scenario
    const input = /* minimal input that triggers bug */;

    // Act - exercise the buggy code path
    const result = functionWithBug(input);

    // Assert - verify correct behavior
    expect(result).toEqual(/* expected output */);
  });
});
```

### Make the Minimal Fix

**Rules:**

1. Fix ONLY the bug - no refactoring
2. Change the smallest amount of code possible
3. If fix seems large, reconsider hypothesis
4. Don't "improve" nearby code while you're there

---

## Phase 6: Verify

### Run Full Test Suite

After the fix:

1. Run the new test - should pass
2. Run full test suite - all should pass
3. Run the original reproduction steps - should work
4. Check for edge cases near the fix

### Verification Checklist

- [ ] New test passes
- [ ] All existing tests pass
- [ ] Manual reproduction now works correctly
- [ ] No new warnings or errors introduced
- [ ] Edge cases around the fix verified

---

## Phase 7: Document

### Record Significant Learnings

If the bug reveals something worth remembering:

```markdown
## YYYY-MM-DD - [repo] - Bug: [Title]

**Symptom:** [What was observed]

**Root cause:** [What was actually wrong]

**Fix:** [What was changed]

**Learning:** [What pattern to avoid or check for in future]

**Prevention:** [How to catch this earlier next time]
```

### Update Project Patterns

If this bug suggests a new rule:

- Add to project CLAUDE.md
- Consider adding a linting rule
- Add to code review checklist

---

## Output Format

```markdown
# Debug Report: [Bug Title]

## Summary

**Status:** FIXED / INVESTIGATING / BLOCKED
**Root Cause:** [One-line summary]
**Fix:** [One-line summary of change]

---

## Symptoms

- [Observable problem 1]
- [Observable problem 2]

**Error message:**
```

[error text if applicable]

````

---

## Reproduction

**Steps:**
1. [Step]
2. [Step]

**Rate:** X/X attempts

---

## Investigation

### Isolation

[How we narrowed it down]

### Hypothesis

**Theory:** [What we believe is wrong]

**Evidence:**
- [Supporting evidence]

---

## Solution

### Test Added

```typescript
// Test code
````

### Fix Applied

```diff
- [old code]
+ [new code]
```

**File:** `path/to/file.ts:line`

**Why this fixes it:** [Brief explanation]

---

## Verification

- [x] New test passes
- [x] All existing tests pass
- [x] Manual verification complete

---

## Learnings

[Any patterns to remember for future]

````

---

## Debugging Techniques for Claude Code

Since Claude Code can't see console output directly, use these strategies:

### 1. Error Messages for Debugging

```typescript
return { error: `Debug: received ${JSON.stringify(args)}` };
// or
throw new Error(`Debug state: ${JSON.stringify(debugInfo)}`);
````

### 2. Write Debug Info to Files

```typescript
import { promises as fs } from "fs";
await fs.writeFile("debug.json", JSON.stringify(debugInfo, null, 2));
```

### 3. Check Logs After Running

```bash
cat debug.json
tail -f test-output.log
```

### 4. Add Logging Temporarily

```typescript
// Add before suspected area
console.log("DEBUG [location]:", JSON.stringify(relevantData));
// Then check output or capture in tests
```

---

## Integration with Workflow

This skill should be invoked:

1. When a bug is reported (before attempting fixes)
2. When tests fail unexpectedly
3. When behavior differs from documentation
4. When "quick fix" attempts haven't worked

The output feeds into the project diary for significant bugs.

---

## Calibration Guidelines

### Match Depth to Bug Severity

| Severity          | Approach                    | Documentation         |
| ----------------- | --------------------------- | --------------------- |
| Typo/trivial      | Quick fix, skip most steps  | None needed           |
| Standard bug      | Full process                | Test + brief note     |
| Critical/security | Extra thorough, peer review | Full report + diary   |
| Recurring         | Deep investigation          | Pattern documentation |

### Time-Boxing

If investigation exceeds 30 minutes without progress:

1. Document current state
2. List what's been tried
3. Note current best hypothesis
4. Identify what information would help
5. Consider asking for help or fresh perspective

### When to Escalate

- Bug in library/framework outside our control
- Need environment access you don't have
- Requires domain knowledge not available
- Security implications need human review
