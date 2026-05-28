---
name: systematic-debugging
description: Use this skill when encountering bugs or unexpected behavior to methodically identify and fix the root cause.
---

# Systematic Debugging

## Core Principle

Debug methodically, not randomly. Follow a systematic process to identify and fix the root cause, not just symptoms.

## When to Use This Skill

- Encountering bugs or errors
- Unexpected behavior in applications
- Tests failing
- Production issues
- User-reported problems
- "It worked yesterday" situations

## The Iron Law

**NEVER "try random things until it works."** That's not debugging, it's luck.

## The 5-Step Debugging Process

### Step 1: REPRODUCE

**Goal**: Get the bug to happen consistently.

- Capture exact commands, inputs, and environment.
- Document reproduction steps and conditions.

### Step 2: ISOLATE

**Goal**: Narrow down where the problem occurs.

- Use techniques like binary search, logging, and minimal test cases to identify the location of the issue.

### Step 3: IDENTIFY

**Goal**: Find the root cause, not just where the error occurs.

- Investigate error messages, logs, and recent changes to determine the underlying issue.

### Step 4: FIX

**Goal**: Fix the root cause, not symptoms.

- Apply the smallest fix that addresses the root cause and document the changes made.

### Step 5: VERIFY

**Goal**: Confirm the fix works and doesn't break anything else.

- Re-run the reproduction steps, relevant tests, and check for regressions.

## Debugging Techniques

- **Rubber Duck Debugging**: Explain the problem out loud to clarify your thoughts.
- **Divide and Conquer**: Break down the problem into smaller parts to isolate the issue.
- **Time Travel (Git Bisect)**: Use git bisect to find the commit that introduced the bug.
- **Minimal Reproduction**: Create a minimal test case to isolate the bug.

## Common Debugging Scenarios

1. **Intermittent Bug**: Analyze patterns and conditions under which the bug occurs.
2. **"Works on My Machine"**: Compare environments and configurations to identify discrepancies.
3. **The Bug That Makes No Sense**: Question assumptions and add extensive logging to uncover hidden issues.

## Debugging Tools

- **Debugger**: Step through code and inspect variables.
- **Logging**: Use strategic logging to track the flow of execution and state.
- **Browser DevTools**: Inspect network requests, console errors, and JavaScript execution.

## Red Flags (Bad Debugging)

- Trying random changes without understanding
- Skipping reproduction steps
- Fixing symptoms instead of root causes
- Not verifying the fix

## Your Commitment

When debugging:
- [ ] I will reproduce the bug reliably first
- [ ] I will isolate where the problem occurs
- [ ] I will identify the root cause, not just symptoms
- [ ] I will fix the root cause
- [ ] I will verify the fix completely
- [ ] I will add tests to prevent regression

---

**Bottom Line**: Systematic debugging finds root causes quickly. Random debugging wastes time and creates more bugs. Follow the process: Reproduce → Isolate → Identify → Fix → Verify.