---
name: code-simplifier
description: Refactor complex or duplicated code without changing behavior. Use for refactoring tasks, simplifying logic, or improving readability.
---

# Code Simplification

## Rules

- Do not change behavior.
- Prefer small, safe steps.
- Add or update tests if coverage is missing.

## Workflow

1. Read the target code and identify complexity drivers.
2. Plan minimal refactors (early returns, extraction, deduplication).
3. Apply changes incrementally and keep intent clear.
4. Run relevant tests and linters.

## Heuristics

- Keep functions ~20 lines when possible.
- Limit nesting depth to 3.
- Reduce argument count to 4 or fewer.
- Replace magic numbers with constants.

## Report format

```
## Code Simplification Report

### Target files
- path

### Issues found
1. [Type] function - description

### Changes made
1. file:line - before/after summary

### Follow-ups
- tests to run
```
