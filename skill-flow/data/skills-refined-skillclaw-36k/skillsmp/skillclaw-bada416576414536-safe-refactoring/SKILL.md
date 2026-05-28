---
name: safe-refactoring
description: Use this skill when you need to improve code structure without changing its behavior, ensuring that tests remain green throughout the process.
---

# Skill body

## Overview

Refactoring changes code structure without altering behavior. It is crucial to keep tests passing at every step; otherwise, you are not refactoring but rewriting.

**Core principle:** Change → Test → Commit. Repeat until complete. Ensure tests are green at every step.

## Rigidity Level

MEDIUM FREEDOM - Adhere strictly to the change→test→commit cycle while adapting specific refactoring patterns to your language and codebase. Never proceed with failing tests.

## Quick Reference

| Step | Action | STOP If |
|------|--------|---------|
| 1 | Verify tests pass BEFORE starting | Any test fails |
| 2 | Create a refactoring task | - |
| 3 | Make ONE small change | Doesn't compile |
| 4 | Run tests immediately | Any test fails |
| 5 | Commit with a descriptive message | - |
| 6 | Repeat steps 3-5 until complete | Tests fail → undo |
| 7 | Final verification & close the task | - |

**Core cycle:** Change → Test → Commit (repeat)

**If tests fail:** STOP. Undo the change. Make a smaller change. Try again.

## When to Use

- Improving code structure without changing functionality
- Extracting duplicated code into shared utilities
- Renaming for clarity
- Reorganizing file/module structure
- Simplifying complex code while preserving behavior

**Don't use for:**
- Changing functionality (use a different skill for feature development)
- Fixing bugs (use a debugging skill)
- Adding features while restructuring (do this separately)
- Code without tests (write tests first using test-driven development)

## The Process

### Step 1: Verify Tests Pass

**BEFORE any refactoring:**

```bash
# Run the full test suite
Dispatch hyperpowers:test-runner agent: "Run: go test ./..."
```

**Verify:** ALL tests pass.

**Decision tree:**
- All pass? → Go to Step 2
- Any fail? → **STOP. Fix failing tests FIRST, then refactor.**

**Why:** Failing tests mean you can't detect if refactoring breaks things.

---

### Step 2: Create Refactoring Task

Track the refactoring work:

```bash
# Create a task for refactoring
TaskCreate
  subject: "Refactor: [specific goal]"
  description: |
    ## Goal
    [What structure change you're making]

    ## Why
    - [Reason 1: duplication, complexity, etc.]
    - [Reason 2]

    ## Approach
    1. [Transformation 1]
    2. [Transformation 2]
    3. [Transformation 3]

    ## Success Criteria
    - [ ] All tests still pass
```

This structured approach ensures clarity and accountability throughout the refactoring process.