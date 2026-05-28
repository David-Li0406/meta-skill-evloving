# Generate Phase Guide

**Purpose**: Creation - AI writes code following TDD

## Key Process

**RED → GREEN → REFACTOR**

1. **RED**: Write a failing test first
2. **GREEN**: Write minimal code to make it pass
3. **REFACTOR**: Improve code while tests stay green

## Critical Rules

- One task per session (prevents context pollution)
- Tests MUST be written BEFORE implementation
- 80% minimum test coverage (90% for critical paths)
- No skipped tests

## Structured Prompts

When starting a task, provide:

1. **Context**: Relevant background, related code, dependencies
2. **Task**: Clear description of what to implement
3. **Criteria**: Acceptance criteria from Refine phase
4. **Format**: Expected output format, coding standards

## TDD Cycle

```
┌─────────────────────────────────────────┐
│  1. Write failing test (RED)            │
│     - Test describes expected behavior  │
│     - Run test, confirm it fails        │
├─────────────────────────────────────────┤
│  2. Write minimal code (GREEN)          │
│     - Just enough to pass the test      │
│     - No premature optimization         │
├─────────────────────────────────────────┤
│  3. Refactor (REFACTOR)                 │
│     - Improve code quality              │
│     - Tests must stay green             │
│     - Repeat cycle for next test        │
└─────────────────────────────────────────┘
```

## One Task Per Session

Why? Context pollution causes:
- AI mixing up requirements from different tasks
- Conflicting implementations
- Lost focus on acceptance criteria

Start fresh for each task with:
- Relevant context from earlier phases
- Clear task description
- Specific acceptance criteria

## Quality Gates

Before marking a task complete:
- [ ] All tests passing
- [ ] Coverage meets minimum threshold
- [ ] No linting errors
- [ ] Code follows project conventions

## Completion Checklist

- [ ] Tests written before implementation
- [ ] All tests passing
- [ ] Coverage threshold met
- [ ] Code review completed
- [ ] Integration verified

## Common Mistakes

- Writing code before tests
- Too many tasks in one session
- Skipping the refactor step
- Not running tests after changes

## Next Phase

When Generate is complete, advance to **Evaluate** where you verify output matches intent.
