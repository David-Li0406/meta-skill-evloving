---
name: code-refactoring
description: Use this skill when you need to improve code structure, reduce complexity, or enhance maintainability without changing behavior.
---

# Code Refactoring

## Core Principle

**Refactoring changes code structure without changing behavior.** It is about making code easier to understand, maintain, and extend. Every refactoring should be:

- **Safe** — Behavior remains unchanged
- **Testable** — Tests verify behavior preservation
- **Incremental** — Small steps, frequent commits
- **Reversible** — Can roll back if needed

## When to Refactor

### Good Times to Refactor
- Before adding a feature
- During code review
- When you touch existing code
- When you see duplication
- When code is hard to test
- When you struggle to understand code

### Bad Times to Refactor
- While debugging
- Near a deadline
- Without tests
- In unfamiliar code
- Just because

## Common Code Smells and Refactoring Patterns

| Smell | Refactoring |
|-------|-------------|
| Long method (>20 lines) | Extract Method |
| Large class | Extract Class |
| Long parameter list (>3) | Introduce Parameter Object |
| Duplicated code | Extract Method/Class |
| Complex conditional | Decompose Conditional |
| Magic numbers | Named Constants |
| Nested loops | Replace Loop with Pipeline |

## Refactoring Techniques

### 1. Extract Method
Identify a code block that does one thing and move it to a new method with a descriptive name.

### 2. Replace Conditional with Polymorphism
Use polymorphic classes instead of conditionals to handle different types.

### 3. Introduce Parameter Object
Replace long parameter lists with a single object that encapsulates the parameters.

### 4. Replace Magic Numbers with Constants
Use named constants instead of unexplained numeric literals.

### 5. Simplify Conditional Logic
Use early returns or guard clauses to reduce nesting in conditionals.

### 6. Improve Naming
Use descriptive names for functions and variables to clarify their purpose.

### 7. Split Large Classes
Extract responsibilities into focused classes to adhere to the Single Responsibility Principle.

## Safe Refactoring Process

1. **Ensure tests exist** - Write tests if they don't.
2. **Make small changes** - One refactoring at a time.
3. **Run tests after each change** - Catch regressions immediately.
4. **Commit frequently** - Easy to revert if something breaks.
5. **Review the diff** - Ensure behavior hasn't changed.

## Refactoring Workflow

### Step 1: Ensure Tests Exist
Run existing tests before refactoring. If tests are missing, write them first.

### Step 2: Make One Small Change
Keep refactorings atomic; avoid combining multiple changes.

### Step 3: Run Tests After Each Change
Verify that tests still pass after each refactoring step.

### Step 4: Commit Frequently
Commit after each successful refactoring with a clear message.

### Step 5: Review Before Pushing
Ensure all tests pass and that the code is simpler and clearer.

## Integration with Other Skills

- **With Code Review**: Refactor before requesting a review.
- **With Testing Strategy**: Write tests before refactoring if missing.
- **With Git Hygiene**: Commit refactorings separately from features.

## Common Pitfalls

- Refactoring without tests
- Big bang refactoring
- Refactoring while adding features
- Refactoring for perfection

**Remember:** Refactoring is about making code better without changing what it does. Keep changes small, test frequently, and commit often.