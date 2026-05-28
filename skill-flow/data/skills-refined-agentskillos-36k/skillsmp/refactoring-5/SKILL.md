---
name: refactoring
description: Use when improving code structure without changing behavior - test-preserving transformations in small steps, running tests between each change
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

**If tests fail:** STOP. Undo change. Make smaller change. Try again.

## When to Use

- Improving code structure without changing functionality
- Extracting duplicated code into shared utilities
- Renaming for clarity
- Reorganizing file/module structure
- Simplifying complex code while preserving behavior

**Don't use for:**
- Changing functionality (use `gambit:execute-plan`)
- Fixing bugs (use `gambit:debugging`)
- Adding features while restructuring (do separately)
- Code without tests (write tests first using `gambit:tdd`)

## The Process

### Step 1: Verify Tests Pass

**BEFORE any refactoring:**

```
Task
  subagent_type: "hyperpowers:test-runner"
  prompt: "Run: go test ./..."
```

**Verify:** ALL tests pass.

**Decision tree:**
- All pass? → Go to Step 2
- Any fail? → **STOP. Fix failing tests FIRST, then refactor.**

**Why:** Failing tests mean you can't detect if refactoring breaks things.

---

### Step 2: Create Refactoring Task

Track the refactoring work:

```
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
  activeForm: "Refactoring code"
```

```
TaskUpdate
  taskId: "[task-id]"
  status: "in_progress"
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
- Touching more than 2-3 files

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

```
Task
  subagent_type: "hyperpowers:test-runner"
  prompt: "Run: go test ./..."
```

**Verify:** ALL tests still pass.

**Decision tree:**
- All pass? → Go to Step 5
- Any fail? → **STOP. Undo and try smaller change.**

**If tests fail:**

```bash
# Undo the change
git restore src/file.go

# Or if multiple files
git checkout -- .
```

Then:
1. Understand why it broke
2. Make smaller change
3. Try again

**Never proceed with failing tests.**

---

### Step 5: Commit the Small Change

Commit each safe transformation:

```bash
git add src/user.go
git commit -m "$(cat <<'EOF'
refactor: extract email validation to function

No behavior change. All tests pass.

Task: [task-id]

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
EOF
)"
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

```
Task
  subagent_type: "hyperpowers:test-runner"
  prompt: "Run: go test ./... && golangci-lint run"
```

**Checklist:**
- [ ] All tests pass
- [ ] No new warnings
- [ ] No behavior changes
- [ ] Code is cleaner/simpler
- [ ] Each commit is small and safe

**Review the changes:**

```bash
# See all refactoring commits
git log --oneline | head -10

# Review full diff from start
git diff [start-sha]..HEAD
```

**Close Task:**

```
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
- Business logic stays same
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
- Need to replace system but can't tolerate downtime
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

## Examples

### Bad: Big-Bang Refactoring

```
# Changes made all at once:
- Renamed 15 functions across 5 files
- Extracted 3 new classes
- Moved code between 10 files
- Reorganized module structure

# Then runs tests
$ go test ./...
... 23 test failures ...

# Now what? Which change broke what?
# Can't identify. Must revert everything.
# 3 hours of work lost.
```

**Why it fails:**
- Can't identify which change broke tests
- Reverting means losing ALL work
- Fixing requires debugging entire refactoring

### Good: Incremental Refactoring

```
# Step 1
Extract validateEmail() → test → commit ✓

# Step 2
Extract validateName() → test → commit ✓

# Step 3 (test fails!)
Move validation to new file → test → FAIL
Undo: git restore .
Try smaller: Just move one function → test → pass → commit ✓

# Step 4
Move second function → test → commit ✓

# Result: 4 commits, each reviewable, each safe
# If step 3 had broken something, knew exactly which change
```

### Bad: Changing Behavior While "Refactoring"

```go
// Original
func validateEmail(email string) error {
    if email == "" {
        return errors.New("email required")
    }
    if !strings.Contains(email, "@") {
        return errors.New("invalid email")
    }
    return nil
}

// "Refactored" - but added behavior!
func validateEmail(email string) error {
    if email == "" {
        return errors.New("email required")
    }
    if !strings.Contains(email, "@") {
        return errors.New("invalid email")
    }
    // NEW: Added validation
    if !strings.Contains(email, ".") {
        return errors.New("invalid email domain")
    }
    return nil
}
```

**Why it fails:**
- This changes behavior (now rejects emails like "user@localhost")
- Tests might pass if they don't cover this case
- Not refactoring - this is modifying functionality
- Do separately: refactor first, then add feature

### Bad: Refactoring Without Tests

```go
// Legacy code with no tests
func processPayment(amount float64, userID int64) error {
    // 200 lines of complex payment logic
    // Multiple edge cases
    // No tests exist
}

// Developer refactors without tests:
// - Extracts 5 methods
// - Renames variables
// - Simplifies conditionals
// - "Looks good to me!"

// Deploys to production
// Payments fail for amounts over $1000
// Edge case handling was accidentally changed
```

**Why it fails:**
- No tests to verify behavior preserved
- Complex logic has hidden edge cases
- Subtle behavior changes go unnoticed
- Breaks in production, not development

### Good: Write Tests First, Then Refactor

```go
// BEFORE refactoring: Write tests documenting current behavior

func TestProcessPayment_ValidAmount(t *testing.T) { ... }
func TestProcessPayment_ZeroAmount(t *testing.T) { ... }
func TestProcessPayment_LargeAmount(t *testing.T) { ... }  // The $1000+ case!
func TestProcessPayment_NegativeAmount(t *testing.T) { ... }
func TestProcessPayment_InvalidUser(t *testing.T) { ... }

// Run tests → all pass (documenting current behavior)

// NOW refactor with tests as safety net:
// Extract method → test → commit
// Rename → test → commit
// Simplify → test → commit

// Tests catch any behavior changes immediately
```

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
- Tests exist (use `gambit:tdd` to write tests first if none exist)
- `gambit:verify` (for final verification)
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
- No tests exist → Use `gambit:tdd` to write tests first
- Unsure how small → If it touches more than one function/file, too big
- Behavior needs to change → Stop refactoring, do feature work separately
