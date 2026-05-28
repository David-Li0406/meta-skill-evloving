---
name: test-driven-development
description: Use this skill to guide development following Kent Beck's Test-Driven Development (TDD) methodology using the Red-Green-Refactor cycle. Ideal for writing tests first, implementing features, and refactoring after tests pass.
---

# Test-Driven Development (TDD)

## Instructions
Follow Kent Beck's Test-Driven Development (TDD) methodology precisely using the Red → Green → Refactor cycle.

### Core TDD Principles

#### The TDD Cycle
Always follow: **Red → Green → Refactor**

1. **RED**: Write a failing test
2. **GREEN**: Write minimal code to make it pass
3. **REFACTOR**: Improve structure while keeping tests green

### Test Writing Guidelines

#### Writing Tests
- Write the simplest failing test first that defines a small increment of functionality.
- Use meaningful test names that describe behavior (e.g., "shouldSumTwoPositiveNumbers").
- Ensure test failures are clear and informative.
- Write just enough code to make the test pass - no more.
- Always write one test at a time.

#### Test Execution
- Run tests to confirm they pass (Green).
- Always run all tests after every change.
- Once tests pass, consider if refactoring is needed.
- Repeat the cycle for new functionality.

#### Defect Fixing
When fixing a defect:
1. Write an API-level failing test.
2. Write the smallest possible test that replicates the problem.
3. Get both tests to pass.

### Implementation Guidelines

#### Minimum Implementation
- Implement the minimum code needed to make tests pass.
- Use the simplest solution that could possibly work.
- Write just enough code to make the test pass - no more.

#### Code Quality
- Eliminate duplication ruthlessly.
- Express intent clearly through naming and structure.
- Keep methods small and focused on a single responsibility.
- Minimize state and side effects.

### Refactoring in TDD

#### When to Refactor
- Refactor only when tests are passing (in the "Green" phase).
- Never refactor when tests are failing.

#### How to Refactor
- Use established refactoring patterns.
- Make one refactoring change at a time.
- Run tests after each refactoring step.
- Prioritize refactorings that remove duplication or improve clarity.

### TDD Workflow

#### Standard Feature Development
1. Write a simple failing test for a small part of the feature.
2. Implement the bare minimum to make it pass.
3. Run tests to confirm they pass (Green).
4. Make any necessary structural changes, running tests after each change.
5. Add another test for the next small increment of functionality.
6. Repeat until the feature is complete.

### Discipline
- Always write one test at a time.
- Make it run.
- Improve structure.
- Maintain high code quality throughout development.

### Commit Standards
Use small, frequent commits rather than large, infrequent ones. Only commit when:
1. ALL tests are passing.
2. ALL compiler/linter warnings have been resolved.
3. The change represents a single logical unit of work.

## Key Patterns
1. **Always write test first** - Never write production code without a failing test.
2. **Make smallest possible change** - Don't solve future problems.
3. **Run tests after every change** - Immediate feedback.
4. **Refactor only when green** - Safe to restructure.
5. **One test at a time** - Focus on single behavior.
6. **Separate commits** - Structural vs behavioral changes.