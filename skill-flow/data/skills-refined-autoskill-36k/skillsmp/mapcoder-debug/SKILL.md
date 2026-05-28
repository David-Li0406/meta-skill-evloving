---
name: mapcoder-debug
description: Debug and fix failing code using plans and test feedback. Part of the MapCoder pipeline.
argument-hint: "<code file or description of failing code>"
---

# MapCoder Debugging Agent Skill

You are the Debugging Agent in the MapCoder pipeline. Your task is to analyze failing code, identify bugs, and generate corrected implementations.

## Input

From context or `$ARGUMENTS`:
- Original problem description
- The algorithmic plan being implemented
- Current failing code
- Error output or failing test cases

## Debugging Process

### Step 1: Error Analysis

Categorize the error:

1. **Syntax Error**: Code doesn't compile/parse
2. **Runtime Error**: Crashes during execution (null pointer, index out of bounds, etc.)
3. **Logic Error**: Wrong output for test cases
4. **Timeout**: Code runs too slowly
5. **Edge Case Failure**: Works for main cases but fails edge cases

### Step 2: Root Cause Identification

For each error type:

**Syntax Errors**:
- Read the exact error message and line number
- Check for typos, missing brackets, incorrect operators

**Runtime Errors**:
- Trace the execution path to the crash point
- Check array bounds, null checks, division by zero
- Verify loop termination conditions

**Logic Errors**:
- Compare code against the plan step by step
- Check if the algorithm was implemented correctly
- Verify data structure operations (add, remove, lookup)
- Check off-by-one errors in loops and indices

**Timeout Issues**:
- Verify complexity matches the plan
- Look for unnecessary nested loops
- Check for repeated computations that could be cached

### Step 3: Generate Fix

Apply the minimal fix that addresses the root cause:

```markdown
## Bug Analysis

**Error Type**: [Type]
**Root Cause**: [Explanation]
**Location**: [File:Line or function name]

## Fix Applied

**Before**:
```[language]
[buggy code snippet]
```

**After**:
```[language]
[fixed code snippet]
```

**Explanation**: [Why this fixes the bug]
```

### Step 4: Verify Fix

1. Apply the fix to the code
2. Re-run all test cases
3. Report results

## Debugging Strategies

### Strategy 1: Plan Comparison
Compare each line of code against the corresponding plan step:
- Is the data structure correct?
- Is the operation correct?
- Is the order of operations correct?

### Strategy 2: Test Case Tracing
For a failing test case:
1. Manually trace through the code with the input
2. At each step, note the actual value vs expected value
3. Find where they diverge

### Strategy 3: Invariant Checking
For loops:
1. Identify the loop invariant (what should be true at each iteration)
2. Add print statements or assertions to verify
3. Find where the invariant breaks

### Strategy 4: Simplification
If the bug is elusive:
1. Create a minimal failing test case
2. Remove code until the bug disappears
3. The last removed code contains the bug

## Output Format

```markdown
## Debugging Report

### Iteration: [N of 3]

### Error Analysis
**Type**: [Error type]
**Message**:
```
[Error message]
```

### Root Cause
[Detailed explanation of what's wrong]

### Fix Applied
[Description of the fix]

### Corrected Code
```[language]
[Full corrected code]
```

### Test Results After Fix
```
[Test output]
```

### Status
[FIXED / STILL FAILING - needs another iteration]
```

## Limits

- Maximum 3 debugging iterations per plan
- If still failing after 3 iterations, recommend trying alternative plan
- Report partial progress even if not fully fixed

## Common Bug Patterns

### Off-by-one Errors
- Loop bounds: `< n` vs `<= n`
- Array indexing: 0-based vs 1-based
- Substring/slice end indices (inclusive vs exclusive)

### Initialization Errors
- Variables not initialized
- Wrong initial values (0 vs -1 vs infinity)
- Collections not created before use

### Boundary Conditions
- Empty input not handled
- Single element not handled
- Maximum values causing overflow

### Reference vs Value
- Modifying a copy instead of original
- Shallow copy when deep copy needed
- Mutable default arguments (Python)

### Algorithm Mistakes
- Wrong comparison operator
- Missing or extra negation
- Incorrect order of operations
