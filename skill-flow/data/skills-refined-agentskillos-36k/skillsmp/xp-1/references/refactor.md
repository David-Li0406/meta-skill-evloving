# Refactor

## Core Rules (Non-Negotiable)

1. **NEVER change behaviour** — refactoring preserves existing functionality
2. **All tests must pass** before and after refactoring
3. **Small incremental changes** — one transformation at a time
4. **Run tests after every change** — catch regressions immediately

## The Refactor Cycle

```
✅ VERIFY   → Run all tests, confirm green state
🔍 ANALYSE  → Identify code smell or improvement opportunity
🔵 REFACTOR → Apply ONE transformation
✅ VERIFY   → Run all tests, confirm still green
🔁 REPEAT   → Continue until goal achieved
```

## Goals & Techniques

| Goal | Techniques |
|------|------------|
| Eliminate duplication | Extract method, extract variable, pull up method |
| Improve clarity | Rename, inline temp, introduce explaining variable |
| Simplify conditionals | Decompose conditional, consolidate conditional |
| Improve structure | Extract class, move method, replace inheritance with delegation |

## Code Smells to Address

- **Duplication** — same code in multiple places
- **Long methods** — do too much, hard to understand
- **Large classes** — too many responsibilities
- **Long parameter lists** — difficult to call correctly
- **Feature envy** — method uses another class more than its own
- **Primitive obsession** — using primitives instead of small objects

## What Refactoring Is NOT

- Adding new features
- Fixing bugs (unless the fix is purely structural)
- Changing external APIs

## Announcing Changes

```
🔵 REFACTOR → [smell]: [transformation]
```

Examples:

- `🔵 REFACTOR → duplication: Extract method calculateTotal`
- `🔵 REFACTOR → long method: Split processOrder into validate and execute`

## Safety Checklist

Before starting:

- [ ] All tests pass
- [ ] Understand the code being refactored

After each change:

- [ ] Tests still pass
- [ ] Behaviour unchanged
- [ ] Code is cleaner/clearer
