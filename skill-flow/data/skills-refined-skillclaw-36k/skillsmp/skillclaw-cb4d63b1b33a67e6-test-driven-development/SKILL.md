---
name: test-driven-development
description: Use this skill when implementing features with Test-Driven Development (TDD), writing tests first, or refactoring with test coverage.
---

# Test-Driven Development

Write tests first, implement minimal code to pass, refactor systematically.

<when_to_use>

- New features with TDD methodology
- Complex business logic requiring coverage
- Critical paths: auth, payments, data integrity
- Bug fixes: reproduce with test, fix, verify
- Refactoring: ensure behavior preservation
- API design: tests define the interface

NOT for: exploratory coding, UI prototypes, static config, trivial glue code

</when_to_use>

<phases>

Track with task management. Advance through RED-GREEN-REFACTOR cycle.

| Phase | Trigger | activeForm |
|-------|---------|------------|
| Red | Session start / cycle restart | "Writing failing test" |
| Green | Test written and failing | "Implementing code" |
| Refactor | Tests passing | "Refactoring code" |
| Verify | Refactor complete | "Verifying implementation" |

Task format:

```text
- Write failing test for { feature }
- Implement { feature } to pass tests
- Refactor { aspect }
- Verify { what's being checked }
```

Workflow:
- Start: Create "Red" phase `in_progress`
- Transition: Mark current `completed`, add next `in_progress`
- After each phase: Run tests before advancing
- Multiple cycles: Return to "Red" for next feature

Edge cases:
- Good existing tests: Start at "Refactor" after confirming pass
- Bug fix: Start at "Red" with failing test reproducing bug
- No regression: Tests must continue passing through all phases

</phases>

<cycle>

```
RED --> GREEN --> REFACTOR --> RED --> ...
 |       |          |
Test   Impl      Improve
Fails  Passes   Quality
```

Each cycle: 5-15 min. Longer = step too large, decompose.

Philosophy:
- Red-Green-Refactor as primary workflow
- Test quality over quantity - behavior, not implementation
- Incremental progress - small focused cycles
- Type safety throughout - tests as type-safe as production

</cycle>

<red_phase>

Write tests defining desired behavior before implementation exists.

Guidelines:
- 3-5 related tests fully specifying one feature
- Type system makes invalid states unrepresentable
- Each test = one specific behavior
- Run tests, verify fail for right reason
- Descriptive names forming sentences

TypeScript:

```typescript
import { describe, test, expect } from 'your-testing-library';

describe('Feature', () => {
  test('should do something', () => {
    // Arrange
    // Act
    // Assert
  });
});
```

</red_phase>