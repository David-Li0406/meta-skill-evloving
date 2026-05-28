---
name: test-driven-development
description: Use this skill when implementing code changes to ensure quality and reliability through a structured testing process.
---

# Test-Driven Development

Test-Driven Development (TDD) is a fundamental practice where every line of production code is written in response to a failing test. This skill outlines the TDD workflow, which is essential for all code changes, including features, bug fixes, and refactoring.

## RED-GREEN-REFACTOR Cycle

### RED: Write Failing Test First
- Do not write any production code until you have a failing test.
- The test should describe the desired behavior, not the implementation.
- Ensure the test fails for the correct reason.

### GREEN: Minimum Code to Pass
- Write only enough code to make the test pass.
- Avoid adding any functionality that is not required by the test.
- Commit immediately after achieving a passing test.

### REFACTOR: Assess Improvements
- Assess potential improvements after each green phase, but only refactor if it adds value.
- Commit before refactoring.
- Ensure all tests pass after refactoring.

## TDD Evidence in Commit History

### Default Expectation
The commit history should clearly show a RED → GREEN → REFACTOR progression.

**Ideal progression example:**
```
commit abc123: test: add failing test for user authentication
commit def456: feat: implement user authentication to pass test
commit ghi789: refactor: extract validation logic for clarity
```

### Rare Exceptions
TDD evidence may not always be linearly visible in commits in the following cases:

1. **Multi-Session Work**
   - The feature spans multiple development sessions.
   - TDD is applied in each session, but commits are organized for clarity rather than strict TDD phases.
   - **Evidence**: All tests exist and pass, with implementation matching test requirements.

2. **Context Continuation**
   - Resuming work from a previous session.
   - The original RED phase was completed in a prior commit.
   - **Evidence**: Reference to the RED commit in the PR description.

3. **Refactoring Commits**
   - Large refactors occur after the GREEN phase.
   - Multiple small refactors may be combined into a single commit.
   - **Evidence**: Commit message indicates "refactor only, no behavior change."

### Documenting Exceptions in PRs
When exceptions apply, document them in the PR description:

```markdown
## TDD Evidence

RED phase: commit c925187 (added failing tests for shopping cart)
GREEN phase: commits 5e0055b, 9a246d0 (implementation + bug fixes)
REFACTOR: commit 11dbd1a (test isolation improvements)

Test Evidence:
✅ 4/4 tests passing (7.7s with 4 workers)
```

**Important**: Documenting exceptions is crucial for maintaining clarity in the TDD process.