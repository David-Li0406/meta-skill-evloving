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
**Problem:** Long function doing multiple things  
**Solution:** Extract logical blocks into named functions

### 2. Replace Conditional with Polymorphism
**Problem:** Using conditionals to determine behavior  
**Solution:** Use polymorphic classes

### 3. Introduce Parameter Object
**Problem:** Too many parameters in a function  
**Solution:** Group parameters into an object

### 4. Replace Magic Numbers with Constants
**Problem:** Unexplained numeric literals throughout code  
**Solution:** Use named constants

### 5. Simplify Conditional Logic
**Problem:** Nested or complex conditionals  
**Solution:** Use early returns or guard clauses

### 6. Improve Naming
**Problem:** Unclear or misleading names  
**Solution:** Use descriptive, intention-revealing names

### 7. Split Large Classes
**Problem:** Class doing too many things  
**Solution:** Extract responsibilities into focused classes

## Safe Refactoring Process

1. **Ensure tests exist** - Write tests if they don't
2. **Make small changes** - One refactoring at a time
3. **Run tests after each change** - Catch regressions immediately
4. **Commit frequently** - Easy to revert if something breaks
5. **Review the diff** - Ensure behavior hasn't changed

## Refactoring Checklist

- [ ] Tests pass before starting
- [ ] Each change is small and focused
- [ ] Tests pass after each change
- [ ] No behavior changes (only structure)
- [ ] Code is more readable than before
- [ ] Commit message explains the refactoring

## Integration with Other Skills

- **With Code Review:** Refactor before requesting review
- **With Testing Strategy:** Write tests before refactoring
- **With Git Hygiene:** Commit refactorings separately from features

## Common Pitfalls

- Refactoring without tests
- Big bang refactoring
- Refactoring while adding features
- Refactoring for perfection

**Remember:** Refactoring is about making code better without changing what it does. Keep changes small, test frequently, commit often. If tests fail after refactoring, you changed behavior—revert and try again.