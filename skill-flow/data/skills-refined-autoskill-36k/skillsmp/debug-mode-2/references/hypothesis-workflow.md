# Hypothesis Workflow Guide

Detailed methodology for generating, testing, and evaluating debugging hypotheses.

## Why Hypotheses Matter

Without hypotheses:
- Debugging becomes random trial-and-error
- Logs lack focus and miss critical data
- Fixes address symptoms, not root causes

With hypotheses:
- Each log has a purpose
- Evidence directly confirms or rejects theories
- Fixes are targeted and reliable

## Generating Effective Hypotheses

### Hypothesis Categories

When facing a bug, consider these categories:

| Category | Example Hypothesis | What to Log |
|----------|-------------------|-------------|
| **Input Validation** | Parameters are null/undefined/wrong type | Parameter values and types at entry |
| **Logic Errors** | Conditional uses wrong operator | Values before condition, which branch executes |
| **State Issues** | Variable mutated unexpectedly | State before/after each mutation |
| **Async/Timing** | Race condition between operations | Timestamps, execution order |
| **Edge Cases** | Boundary values not handled | Input values, especially 0, empty, null |
| **Type Coercion** | Implicit type conversion causes bug | Types before/after operations |
| **Memory/References** | Object reference vs copy issue | Object IDs, mutation traces |

### Writing Testable Hypotheses

**Good hypothesis:**
> "Hypothesis B: The `calculateTotal` function returns NaN when the `items` array contains an object with a missing `price` property."

- Specific location (`calculateTotal`)
- Specific condition (`items` with missing `price`)
- Specific outcome (`returns NaN`)
- Can be tested with targeted logs

**Bad hypothesis:**
> "Something is wrong with the calculation."

- Too vague
- No specific condition to test
- Cannot determine what to log

### Template for Hypotheses

```
Hypothesis [A-E]: The [function/component] [incorrect behavior]
when [specific condition] because [suspected cause].
```

Examples:
- `Hypothesis A: The login function returns undefined when username is empty because the early return skips the validation step.`
- `Hypothesis B: The fetchData function hangs when called twice rapidly because the abort controller is shared between calls.`
- `Hypothesis C: The formatDate function returns "Invalid Date" when timezone is GMT+0 because the offset calculation divides by zero.`

## Instrumentation Strategy

### Log Placement per Hypothesis

For each hypothesis, place logs at:

1. **Entry point** - Capture initial state
2. **Decision point** - Capture values before condition
3. **Each branch** - Confirm which path executed
4. **Exit point** - Capture final result

### Example: Testing Input Validation Hypothesis

```
Hypothesis A: Parameters are passed as strings instead of numbers
```

Instrumentation:
```javascript
function calculate(a, b) {
  // Log 1: Entry - capture types
  // #region agent log - Hypothesis A
  fetch(..., { body: JSON.stringify({
    location: 'calc.js:5',
    message: 'calculate entry',
    data: { a, b, aType: typeof a, bType: typeof b },
    hypothesisId: 'A'
  })});
  // #endregion

  // If strings detected, hypothesis confirmed
  // If numbers detected, hypothesis rejected
}
```

## Evaluation Criteria

### CONFIRMED

Use when logs **prove** the hypothesis is the root cause:

```
Hypothesis B: The function returns undefined when a === 0

Evidence:
- Log #4: a=0, b=5 (input received)
- Log #5: condition "a === 0" evaluated to TRUE
- Log #6: returned undefined

Status: CONFIRMED - Logs prove the a===0 condition causes undefined return
```

### REJECTED

Use when logs **prove** the hypothesis is NOT the cause:

```
Hypothesis A: Parameters are wrong type

Evidence:
- Log #1: a=5, typeof a="number"
- Log #2: b=3, typeof b="number"
- Log #3: a=0, typeof a="number"

Status: REJECTED - All inputs are correct number type
```

### INCONCLUSIVE

Use when logs don't provide enough data:

```
Hypothesis D: Race condition between API calls

Evidence:
- Log #1: First call started at t=1000
- Log #2: First call completed at t=1050
- (No logs from second call)

Status: INCONCLUSIVE - Need to add logging to second API call
```

## Iteration Process

When all hypotheses are INCONCLUSIVE or REJECTED but bug persists:

### Step 1: Analyze What We Learned

What did the logs reveal?
- Which code paths executed?
- What values were unexpected?
- What wasn't logged that should have been?

### Step 2: Generate New Hypotheses

Based on insights, create 3-5 new hypotheses:

```
Round 2 Hypotheses:

Hypothesis F: The bug is in the cache layer, not the calculation
(Because calculation logs showed correct values)

Hypothesis G: The bug occurs during serialization
(Because function return was correct but API response was wrong)

Hypothesis H: A middleware modifies the response
(Because we haven't logged the middleware layer)
```

### Step 3: Add Targeted Instrumentation

Focus on the newly suspected areas.

### Step 4: Reproduce Again

Request user to trigger the bug with new instrumentation.

## Evaluation Table Format

Always present findings in this format:

```markdown
## Hypothesis Evaluation - Round 1

| Hypothesis | Status | Evidence |
|------------|--------|----------|
| A: Wrong param types | REJECTED | Log #1-3: All params are numbers |
| B: a===0 returns undefined | CONFIRMED | Log #5-6: Condition true, returns undefined |
| C: Calculation error | REJECTED | Log #4: 5+3=8 is correct |
| D: Async timing | INCONCLUSIVE | No async operations logged |

**Root Cause:** Hypothesis B confirmed.

**Next Steps:** Apply fix to remove incorrect a===0 check.
```

## Common Pitfalls

### Pitfall 1: Too Few Hypotheses

Problem: Only 1-2 hypotheses means you might miss the real cause.

Solution: Always generate 3-5 hypotheses across different categories.

### Pitfall 2: Overlapping Hypotheses

Problem: Hypotheses that test the same thing waste instrumentation.

Solution: Ensure each hypothesis tests a distinct failure mode.

### Pitfall 3: Unfalsifiable Hypotheses

Problem: "Something is wrong" cannot be rejected by logs.

Solution: Write hypotheses with specific testable conditions.

### Pitfall 4: Premature Fixing

Problem: Fixing after 1 round when evidence is inconclusive.

Solution: Only fix when a hypothesis is CONFIRMED with clear evidence.

## Session Management

Use consistent session IDs across a debugging session:

```
sessionId: "debug-{uuid}"     # Unique per debug session
runId: "initial"              # First reproduction
runId: "post-fix"             # After fix applied
runId: "round-2"              # Second iteration if needed
```

This allows comparing logs across reproduction attempts.
