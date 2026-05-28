---
name: refactoring
description: Use this skill when improving code structure without changing behavior through test-preserving transformations in small steps, running tests between each change.
---

# Safe Refactoring

## Overview

Refactoring changes code structure without changing behavior. Tests must stay green throughout, or you're rewriting, not refactoring.

**Core principle:** Change → Test → Commit. Repeat until complete. Tests green at every step.

**Announce at start:** "I'm using gambit:refactoring to restructure this code safely."

## Rigidity Level

MEDIUM FREEDOM - Follow the change→test→commit cycle strictly. Adapt specific refactoring patterns to your language and codebase. Never proceed with failing tests.

## Quick Reference

| Step | Action | STOP If |
|------|--------|---------|
| 1 | Verify tests pass BEFORE starting | Any test fails |
| 2 | Create refactoring Task | - |
| 3 | Make ONE small change | Doesn't compile |
| 4 | Run tests immediately | Any test fails |
| 5 | Commit with descriptive message | - |
| 6 | Repeat 3-5 until complete | Tests fail → undo |
| 7 | Final verification & close Task | - |

**Core cycle:** Change → Test → Commit (repeat)

## When to Use

- Improving code structure without changing functionality
- Extracting duplicated code into shared utilities
- Renaming for clarity
- Reorganizing file/module structure
- Simplifying complex code while preserving behavior

**Don't use for:**
- Changing functionality (use feature development)
- Fixing bugs (use debugging)
- Adding features while restructuring (do separately)
- Code without tests (write tests first using test-driven development)

## The Process

### Step 1: Verify Tests Pass

**BEFORE any refactoring:**

```bash
# Use test-runner agent to keep context clean
Dispatch hyperpowers:test-runner agent: "Run: go test ./..."
```

**Verify:** ALL tests pass. If any fail, fix them FIRST, then refactor.

**Why:** Failing tests mean you can't detect if refactoring breaks things.

---

### Step 2: Create Refactoring Task

Track the refactoring work:

```bash
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
    - [ ] All existing tests still pass
    - [ ] No behavior changes
    - [ ] Code is cleaner/simpler
    - [ ] Each commit is small and safe

    ## Anti-patterns
    - ❌ Changing behavior while refactoring
    - ❌ Multiple transformations before testing
    - ❌ "While I'm here" improvements
```

---

### Step 3: Make ONE Small Change

The smallest transformation that compiles.

**Examples of "small":**
- Extract one method
- Rename one variable
- Move one function to different file
- Inline one constant
- Extract one interface

**NOT small:**
- Extracting multiple methods at once
- Renaming + moving + restructuring
- "While I'm here" improvements

**Example transformation:**

```go
// BEFORE
func createUser(name, email string) (*User, error) {
    if email == "" {
        return nil, errors.New("email required")
    }
    if !strings.Contains(email, "@") {
        return nil, errors.New("invalid email")
    }
    // ... rest of function
}

// AFTER - ONE small change (extract email validation)
func createUser(name, email string) (*User, error) {
    if err := validateEmail(email); err != nil {
        return nil, err
    }
    // ... rest of function
}

func validateEmail(email string) error {
    if email == "" {
        return errors.New("email required")
    }
    if !strings.Contains(email, "@") {
        return errors.New("invalid email")
    }
    return nil
}
```

---

### Step 4: Run Tests Immediately

After EVERY small change:

```bash
Dispatch hyperpowers:test-runner agent: "Run: go test ./..."
```

**Verify:** ALL tests still pass.

**If tests fail:**
1. STOP
2. Undo the change: `git restore src/file.go`
3. Understand why it broke
4. Make smaller change
5. Try again

**Never proceed with failing tests.**

---

### Step 5: Commit the Small Change

Commit each safe transformation:

```bash
Dispatch hyperpowers:test-runner agent: "Run: git add src/user.go && git commit -m 'refactor: extract email validation to function

No behavior change. All tests pass.'"
```

**Why commit so often:**
- Easy to undo if next step breaks
- Clear history of transformations
- Can review each step independently
- Proves tests passed at each point

---

### Step 6: Repeat Until Complete

Repeat steps 3-5 for each small transformation:

```
1. Extract validateEmail() ✓ (committed)
2. Extract validateName() ✓ (committed)
3. Create UserValidator struct ✓ (committed)
4. Move validations into UserValidator ✓ (committed)
5. Update createUser to use validator ✓ (committed)
6. Remove old inline validations ✓ (committed)
```

**Pattern:** change → test → commit (repeat)

---

### Step 7: Final Verification

After all transformations complete:

```bash
Dispatch hyperpowers:test-runner agent: "Run: go test ./... && golangci-lint run"
```

**Checklist:**
- [ ] All tests pass
- [ ] No new warnings
- [ ] No behavior changes
- [ ] Code is cleaner/simpler
- [ ] Each commit is small and safe

**Close Task:**

```bash
TaskUpdate
  taskId: "[task-id]"
  description: |
    [Original description]

    ## Completed
    - [List of transformations made]
    - All tests pass (verified)
    - No behavior changes
    - N small transformations, each tested
  status: "completed"
```

---

## Refactor vs Rewrite

### When to Refactor
- Tests exist and pass
- Changes are incremental
- Business logic stays the same
- Can transform in small, safe steps
- Each step independently valuable

### When to Rewrite
- No tests exist (write tests first, then refactor)
- Fundamental architecture change needed
- Easier to rebuild than modify
- Requirements changed significantly
- After 3+ failed refactoring attempts

**Rule:** If you need to change test assertions (not just add tests), you're rewriting, not refactoring.

### Strangler Fig Pattern (Hybrid)

**When to use:**
- Need to replace a system but can't tolerate downtime
- Want incremental migration with monitoring
- System too large to refactor in one go

**How it works:**

```
Legacy: Monolithic UserService (5000 LOC)
Goal: Extract into separate module

Step 1 (Transform):
- Create new UserValidator module
- Implement validation logic
- Tests pass in isolation

Step 2 (Coexist):
- Add routing layer (facade)
- Route validation calls to new module
- Route other calls to legacy
- Monitor both

Step 3 (Eliminate):
- Once confident, migrate more functionality
- Remove from legacy
- Repeat until legacy empty
```

**Benefits:**
- Incremental replacement reduces risk
- Legacy continues operating during transition
- Can pause/rollback at any point
- Each step independently valuable

---

## Critical Rules

### Rules That Have No Exceptions

1. **Tests must stay green** throughout → If they fail, you changed behavior (stop and undo)
2. **Commit after each small change** → Large commits hide which change broke what
3. **One transformation at a time** → Multiple changes = impossible to debug failures
4. **Run tests after EVERY change** → Delayed testing doesn't tell you which change broke it
5. **If tests fail 3+ times, question approach** → Might need to rewrite instead, or add tests first

### Common Excuses

All of these mean: **STOP. Return to the change→test→commit cycle.**

| Excuse | Reality |
|--------|---------|
| "Small refactoring, don't need tests between steps" | Small changes can break things. Test every step. |
| "I'll test at the end" | Can't identify which change broke what |
| "Tests are slow, I'll run once at the end" | Slow tests → run targeted tests between steps |
| "Just fixing bugs while refactoring" | Bug fixes = behavior changes = not refactoring |
| "Easier to do all at once" | Easier to debug one change than ten |
| "Tests will fail temporarily but I'll fix them" | Tests must stay green. No exceptions. |
| "While I'm here, I'll also..." | Scope creep during refactoring = disaster |

---

## Verification Checklist

Before marking refactoring complete:

- [ ] Verified all tests passed BEFORE starting
- [ ] Created Task tracking the refactoring
- [ ] Made ONE small change at a time
- [ ] Ran tests after EVERY change
- [ ] Committed each safe transformation
- [ ] Undid changes when tests failed
- [ ] No behavior changes introduced
- [ ] Code is cleaner/simpler than before
- [ ] Each commit in history is small and safe
- [ ] Final verification: all tests pass, no warnings
- [ ] Task documents what was done and why
- [ ] Task marked complete

**Can't check all boxes?** Return to process and fix before closing Task.

---

## Integration

**This skill requires:**
- Tests exist (use test-driven development to write tests first if none exist)
- Verification before completion
- test-runner agent (for running tests without context pollution)

**This skill is called when:**
- Improving code structure after features complete
- Preparing code for new features
- Reducing duplication
- Simplifying complex code

**Workflow:**
```
Want to improve code structure
    ↓
gambit:refactoring (this skill)
    ↓
Step 1: Verify tests pass
    ↓
Step 2: Create Task
    ↓
Step 3-6: Change → Test → Commit (repeat)
    ↓
Step 7: Final verification
    ↓
Code improved, tests still green
```

---

## Resources

**Common refactoring patterns:**
- Extract Method: Pull code into new function
- Extract Class: Pull related methods into new type
- Inline: Replace function call with body
- Rename: Make names clearer
- Move: Relocate code to better location
- Replace Conditional with Polymorphism: Use interfaces

**When stuck:**
- Tests fail after change → Undo (git restore), make smaller change
- 3+ failures → Question if refactoring is right approach
- No tests exist → Use test-driven development to write tests first
- Unsure how small → If it touches more than one function/file, too big
- Behavior needs to change → Stop refactoring, do feature work separately