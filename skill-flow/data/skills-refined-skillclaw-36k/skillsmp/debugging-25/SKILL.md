---
name: debugging
description:
  Systematically debug and diagnose code issues. Use this skill when investigating bugs, analyzing
  error messages, tracing code paths, or understanding unexpected behavior. Provides structured
  approaches to find and fix problems efficiently.
---

# Debugging Best Practices

This skill provides systematic approaches to finding and fixing bugs efficiently.

## When This Skill Applies

- Investigating bug reports
- Analyzing error messages and stack traces
- Understanding unexpected behavior
- Tracing code execution paths
- Diagnosing performance issues

## The Scientific Method for Debugging

Treat debugging as hypothesis testing:

1. **Observe**: Gather information about the bug
2. **Hypothesize**: Form a theory about the cause
3. **Predict**: What would we expect if the hypothesis is true?
4. **Test**: Verify the prediction
5. **Iterate**: Refine hypothesis based on results

## Step-by-Step Debugging Process

### 1. Reproduce the Bug

Before debugging, ensure you can reliably reproduce the issue:

- What are the exact steps?
- What environment? (OS, browser, versions)
- What input data triggers it?
- Is it consistent or intermittent?

**If you can't reproduce it, you can't fix it.**

### 2. Gather Information

Collect all available data:

- Error messages and stack traces
- Log files around the time of failure
- User reports and screenshots
- Recent code changes (git log, blame)
- System state (memory, CPU, disk)

### 3. Isolate the Problem

Narrow down the scope:

- **Binary search**: Disable half the code, see if bug persists
- **Minimal reproduction**: Strip away unrelated code
- **Input reduction**: Find the smallest input that triggers the bug
- **Environment isolation**: Does it happen in dev? staging? only prod?

### 4. Understand Before Fixing

Resist the urge to immediately change code:

- Read the code carefully
- Trace the execution path
- Understand why the current behavior happens
- Identify the root cause, not just symptoms

### 5. Fix and Verify

- Make the smallest change that fixes the issue
- Write a test that catches the bug
- Verify the fix in the reproduction case
- Check for similar bugs elsewhere

## Debugging Techniques

### Print/Log Debugging

Simple but effective:

```python
print(f"DEBUG: user_id={user_id}, status={status}")
```

Use structured logging for production:

```python
logger.debug("Processing request", extra={"user_id": user_id, "status": status})
```

### Interactive Debuggers

Use breakpoints to pause execution:

- **Python**: `breakpoint()` or `import pdb; pdb.set_trace()`
- **JavaScript**: `debugger;` statement
- **Go**: Delve debugger
- **Rust**: `rust-lldb` or VS Code debugger

### Binary Search (Git Bisect)

Find the commit that introduced a bug:

```bash
git bisect start
git bisect bad HEAD
git bisect good v1.0.0
# Git checks out middle commit
# Test and mark as good/bad
git bisect good  # or git bisect bad
# Repeat until found
git bisect reset
```

### Rubber Duck Debugging

Explain the problem out loud (or in writing):

1. Describe what the code should do
2. Describe what it actually does
3. Walk through the code line by line
4. Often, the act of explaining reveals the bug

## Common Bug Patterns

### Off-by-One Errors

- Array index out of bounds
- Loop iterates one too many/few times
- Fence post errors (counting vs. gaps)

### Null/Undefined References

- Accessing properties on null objects
- Forgetting to handle empty arrays
- Async data not loaded yet

### Race Conditions

- Shared mutable state accessed concurrently
- Async operations completing in unexpected order
- Time-dependent behavior

### State Management

- Stale state after updates
- Incorrect initial state
- State not reset between operations

### Type Coercion

- Implicit type conversions
- String vs number comparisons
- Truthy/falsy edge cases

## Error Message Analysis

Read error messages carefully—they usually contain:

1. **Error type**: What category of error
2. **Message**: Description of what went wrong
3. **Stack trace**: Where it happened
4. **Context**: Variable values, request details

### Stack Trace Reading

- Read bottom-up: your code is usually at the bottom
- Ignore framework internals initially
- Look for your file names and line numbers
- The actual bug is often a few frames before the crash

## Performance Debugging

For slow code:

1. **Measure first**: Use profilers, not intuition
2. **Find the hotspot**: What's taking the most time?
3. **Understand why**: I/O? CPU? Memory?
4. **Optimize the bottleneck**: Not random code

Tools:

- **JavaScript**: Chrome DevTools Performance tab
- **Python**: `cProfile`, `py-spy`
- **Go**: `pprof`
- **Rust**: `perf`, `flamegraph`

## When You're Stuck

- Take a break—fresh eyes help
- Ask a colleague (rubber duck)
- Search for the exact error message
- Check recent changes (what changed?)
- Question your assumptions
- Sleep on it—seriously
