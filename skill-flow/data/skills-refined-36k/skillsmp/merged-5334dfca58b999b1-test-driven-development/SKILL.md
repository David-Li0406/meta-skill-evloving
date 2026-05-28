---
name: test-driven-development
description: Use this skill when implementing Test-Driven Development (TDD) methodologies for software projects.
---

# Test-Driven Development (TDD)

## Description
This skill outlines the Test-Driven Development (TDD) methodology, emphasizing the importance of writing tests before code and ensuring high coverage during the development process.

## Details

**Core Principle: Write tests for the code you write.**

Follow the Red/Green/Verify cycle:

### 1. Red: Write a failing test first

- Write the test code that calls the new function.
- Add function declaration to the header file.
- Add a stub implementation that compiles but does nothing (e.g., `return OK(NULL);`).
- A compilation error is NOT a failing test; ensure the stub compiles and runs.
- Verify the test actually fails with assertion failures.

### 2. Green: Write minimal code to make the test pass

- Implement ONLY what the test requires.
- STOP immediately when the test passes.
- DO NOT write "helper functions" before they're called.
- DO NOT write code "because you'll need it later."

### 3. Verify: Run quality checks

- `make check` - All tests must pass.
- `make lint` - Code complexity under threshold.
- `make check-coverage` - **90% coverage is MANDATORY** during the coverage phase.

## Development Phase Focus

**Test what you build.** During development:

- Write tests for the happy path and obvious error cases.
- Cover the main functionality thoroughly.
- Keep momentum; don't get stuck on edge cases.

**Coverage gaps are acceptable during development** and should be addressed in a dedicated coverage phase before release.

**WARNING**: Writing code before tests wastes resources by generating unnecessary code and complicating debugging. 

**The test MUST come first. No exceptions.**

If writing a helper function, ask: "Does a passing test call this right now?" If no, DELETE IT.

If a branch is uncovered, ask: "Can I write a test for this?" If yes, WRITE IT.

**Hunt every branch** during the coverage phase:

- Test all error paths (use mocks to trigger failures).
- Test assertion violations.
- Test edge cases (empty, null, boundary conditions).
- Only use `LCOV_EXCL` markers when genuinely untestable.