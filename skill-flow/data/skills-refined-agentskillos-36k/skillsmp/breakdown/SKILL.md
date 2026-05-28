---
name: breakdown
description: |
  Break down epics and features into concrete backlog tasks with dependencies.
  Use when planning work, decomposing large features, or organizing sprints.
  Trigger with "break down", "decompose", "plan feature", "create subtasks".
model: sonnet
allowed-tools: Read, Grep, Glob, Bash, Task
---

# Breakdown - Epic Decomposition

Patterns for breaking down large features into concrete, parallelizable tasks.

## Decomposition Patterns

### New Feature Pattern

```
1. Infrastructure
   └── Types, contexts, schemas, state management

2. Core Implementation
   └── Main components, business logic

3. Integration
   └── Connect pieces, wire up routes

4. Polish
   └── Edge cases, error handling, UX improvements

5. Validation
   └── Tests, documentation updates
```

**Example: Dark Mode**
1. Infrastructure: Theme context, CSS variables
2. Core: Theme toggle component, styled components
3. Integration: Apply to all pages
4. Polish: System preference detection, smooth transitions
5. Validation: Visual regression tests

### Refactor Pattern

```
1. Create New
   └── Build new pattern alongside old

2. Migrate
   └── Move components one at a time

3. Cleanup
   └── Remove old pattern, dead code

4. Verify
   └── Update tests, ensure no regressions
```

**Example: Move to React Query**
1. Create: Set up React Query provider
2. Migrate: Convert hooks one by one
3. Cleanup: Remove old fetch utilities
4. Verify: Update tests for new patterns

### Bug Fix Pattern

```
1. Investigate (if complex)
   └── Reproduce, identify root cause

2. Fix
   └── Implement the solution

3. Verify
   └── Add regression test
```

**Most bugs don't need decomposition** - only create subtasks for complex bugs requiring investigation.

## Task Sizing

| Size | Lines Changed | Files | Time | Example |
|------|---------------|-------|------|---------|
| XS | <20 | 1 | Minutes | Fix typo, add import |
| S | 20-100 | 1-2 | <1hr | Add helper function |
| M | 100-300 | 2-5 | Hours | Add component |
| L | 300+ | 5+ | Day | Feature module |
| XL | 1000+ | 10+ | Days | Architecture change |

**Target: S-M tasks.** XS is too granular, L-XL should be broken down.

## Dependency Patterns

### Sequential (A → B → C)
```
A: Create database schema
B: Implement API endpoint (blocked by A)
C: Add frontend form (blocked by B)
```

### Fan-out (A → B, C, D in parallel)
```
A: Create shared context
B: Use in Header (blocked by A)
C: Use in Footer (blocked by A)
D: Use in Sidebar (blocked by A)
```

### Fan-in (B, C, D → E)
```
B, C, D: Independent features
E: Integration testing (blocked by B, C, D)
```

### File Conflict Sequencing
```
B: Update styles.css for Header
C: Update styles.css for Footer (blocked by B)
```
Even though B and C are conceptually parallel, they touch the same file.

## Identifying File Overlaps

Common conflict points:
- Shared styles (`styles.css`, `theme.ts`)
- Route configuration (`routes.tsx`, `App.tsx`)
- State management (`store.ts`, `context.tsx`)
- Shared types (`types.ts`, `interfaces.ts`)
- Test utilities (`testUtils.ts`, `fixtures.ts`)

**When detected**: Add dependency between tasks to sequence them.

## Wave Planning

Group tasks into waves:

```markdown
## Wave 1 (Ready Now)
Tasks with no blockers - start immediately

## Wave 2 (After Wave 1)
Tasks blocked by Wave 1 - becomes ready when Wave 1 completes

## Wave 3 (After Wave 2)
Final integration, polish tasks
```

**Max 3-5 tasks per wave** for manageability.

## Quality Checks

Before finalizing breakdown:

1. **Is each task concrete?** Should be implementable without further planning
2. **Are dependencies correct?** No circular deps, no unnecessary sequencing
3. **Are file conflicts handled?** Same-file tasks sequenced
4. **Is it parallelizable?** Maximize concurrent work
5. **Is it right-sized?** No XS or XL tasks

## References

- [dependencies.md](references/dependencies.md) - Dependency patterns
- [epics.md](references/epics.md) - Epic management
