---
name: root-cause-tracing
description: Use this skill when errors occur deep in execution and you need to trace back to find the original trigger by systematically tracing bugs backward through the call stack.
---

# Root Cause Tracing

## Overview

Bugs often manifest deep in the call stack (e.g., git init in the wrong directory, file created in the wrong location, database opened with the wrong path). Your instinct is to fix where the error appears, but that's treating a symptom.

**Core principle:** Trace backward through the call chain until you find the original trigger, then fix at the source.

This skill is a specialized technique within the systematic-debugging workflow, typically applied during Phase 1 (Root Cause Investigation) when dealing with deep call stacks.

## When to Use This Skill

**Use root-cause-tracing when:**
- An error happens deep in execution (not at the entry point).
- The stack trace shows a long call chain.
- It is unclear where invalid data originated.
- You need to find which test or code triggers the problem.
- A symptom appears far from the actual cause.

## The Tracing Process

### 1. Observe the Symptom

Identify the error message and the failed operation.

### 2. Find Immediate Cause

Determine what code directly causes the error.

### 3. Ask: What Called This?

Trace one level up the call stack to find the caller.

### 4. Keep Tracing Up

Continue tracing until you find the original trigger.

### 5. Fix at Source + Add Defense

Address the root cause and implement validation at each layer after fixing the source.

## Key Principles

1. **Trace Backward**: Follow the call chain from symptom to source.
2. **Find Original Trigger**: Identify where bad data or state originated.
3. **Fix at Source**: Address the root cause, not just the symptom.
4. **Defense-in-Depth**: Add validation at each layer after fixing the source.

## Quick Start

### The 5-Step Trace Process

1. **Observe the Symptom**: What error message? What failed operation?
2. **Find Immediate Cause**: What code directly causes this error?
3. **Ask What Called This**: Trace one level up the call stack.
4. **Keep Tracing Up**: Continue until you find the original trigger.
5. **Fix at Source + Defense**: Fix the root cause and add layer validation.

### Decision Tree

```
Error appears deep in stack?
  → Yes: Start tracing backward
    → Can identify caller? → Trace one level up → Repeat
    → Cannot identify caller? → Add instrumentation
  → No: May not need tracing (error at entry point)
```

## Stack Trace Tips

- Use `console.error()` for debugging in tests (logger may be suppressed).
- Log before the dangerous operation, not after it fails.
- Include context: directory, cwd, environment variables, timestamps.
- Capture stack traces using `new Error().stack` to show the complete call chain.

## Real-World Impact

From a debugging session (2025-10-03):
- Found root cause through a 5-level trace.
- Fixed at source (getter validation).
- Added 4 layers of defense.
- 1847 tests passed, zero pollution.
- Time saved: 3+ hours vs. symptom-fix approach.

**Bottom line:** Tracing takes 15-30 minutes. Symptom fixes take hours of whack-a-mole.

## Red Flags - STOP

STOP when thinking:
- "I'll just add validation here" (without finding the source).
- "This will prevent the error" (symptom fix).
- "Too hard to trace back" (add instrumentation instead).
- "Quick fix for now" (creates technical debt).

**ALL of these mean: Continue tracing to find the root cause.**

## Integration with Other Skills

- **systematic-debugging**: Use root-cause-tracing during Phase 1.
- **defense-in-depth**: Add after finding the root cause.
- **verification-before-completion**: Verify the fix worked at the source.
- **test-driven-development**: Write tests for the root cause, not the symptom.

For detailed information, refer to the following:
- **[Tracing Techniques](references/tracing-techniques.md)**: Complete tracing methodology, patterns, and decision trees.
- **[Examples](references/examples.md)**: Real-world debugging scenarios with full trace chains.
- **[Advanced Techniques](references/advanced-techniques.md)**: Stack traces, instrumentation, test pollution detection.
- **[Integration](references/integration.md)**: How to use with systematic-debugging and other skills.