# Reproduction Strategies

Reference guide for establishing verifiable reproduction environments.

## Strategy 1: Minimal Test Case

```
Goal: Smallest code that reproduces the issue

Steps:
1. Start with failing scenario
2. Remove unrelated code
3. Simplify data
4. Isolate the trigger
```

**When to use:** Logic bugs, calculation errors, data transformation issues

## Strategy 2: Logging Injection

```
Goal: Understand execution flow

Steps:
1. Add entry/exit logs to suspect functions
2. Log state at key points
3. Include timestamps for timing issues
4. Log error contexts
```

**When to use:** Timing issues, state bugs, intermittent failures

## Strategy 3: Binary Search (Git Bisect)

```
Goal: Find the breaking change

Steps:
1. Find a known-good state (commit, version)
2. Find the current bad state
3. Check midpoint
4. Repeat until found
```

**When to use:** Regressions, "it worked before" situations

---

## Anti-Patterns to Avoid

### 1. Shotgun Debugging

**Wrong:** Making multiple changes hoping one works
**Right:** Understand the problem, make one targeted change

### 2. Copy-Paste Fixing

**Wrong:** Copying a fix from elsewhere without understanding
**Right:** Understand why it works, adapt appropriately

### 3. Suppressing Symptoms

**Wrong:** Catching errors and ignoring them
**Right:** Fix the error source, handle edge cases properly
