---
name: debug
description: "Use when encountering bugs, test failures, or unexpected behavior. Hypothesis-driven debugging."
---

# Systematic Debugging

**Iron Law:** NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST.

## The Process

```
1. REPRODUCE  -> Trigger consistently
2. INVESTIGATE -> Gather evidence, trace data flow
3. HYPOTHESIZE -> Form ONE specific theory
4. TEST       -> Minimal change to verify
5. FIX        -> Address root cause
6. VERIFY     -> Confirm with test
```

## Step 1: Reproduce

```bash
npm test -- --testPathPattern="auth"
# Document: exact steps, expected vs actual, full error message
```

**Cannot reproduce?** Gather more data. Don't guess.

## Step 2: Investigate

1. **Read error messages completely** - line numbers, stack traces, error codes
2. **Check recent changes:** `git diff HEAD~5`
3. **Trace data flow:** Add logging at component boundaries

```bash
echo "=== Input to component: $INPUT ==="
# component does its thing
echo "=== Output: $OUTPUT ==="
```

**Goal:** Find WHERE it breaks, not just WHAT breaks.

## Step 3: Hypothesize

**Form ONE specific theory:**

```
"Token is null because login returns before API response completes."
```

Not: "Something's wrong with auth" (too vague)

## Step 4: Test Hypothesis

**Smallest possible change:**

```typescript
console.log('Token before return:', token);
```

- Confirmed? Proceed to fix.
- Wrong? Form NEW hypothesis. Return to Step 3.

## Step 5: Fix Root Cause

| Symptom | Wrong Fix | Right Fix |
|---------|-----------|-----------|
| Null pointer | Add null check | Fix why it's null |
| Timeout | Increase timeout | Fix why it's slow |

## Step 6: Verify

Write test that fails before fix, passes after. Proves fix works.

## Decision Criteria

| Situation | Action |
|-----------|--------|
| Cannot reproduce | More data. Don't guess. |
| 3+ failed attempts | Question architecture. Discuss with user. |
| "Quick fix" obvious | STOP. Follow process anyway. |

## Red Flags

- "Let me just try..." -> STOP. Investigate first.
- "Quick fix for now" -> Root cause first.
- Multiple fixes at once -> One hypothesis at a time.

## Integration

**Pairs with:** tdd (write failing test), verification (prove fix works)
