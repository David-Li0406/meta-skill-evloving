---
name: tdd
description: Test-Driven Development skill for the ikigai project
---

# Test-Driven Development

## Description
TDD methodology for development phase. Focus on testing what you build.

## Details

**Core principle: Write tests for the code you write.**

Follow Red/Green/Verify cycle:

### 1. Red: Write a failing test first

- Write the test code that calls the new function
- Add function declaration to header file
- Add stub implementation that compiles but does nothing (e.g., `return OK(NULL);`)
- A compilation error is NOT a failing test - you need a stub that compiles and runs
- Verify the test actually fails with assertion failures

### 2. Green: Write minimal code to make the test pass

- Implement ONLY what the test requires
- STOP immediately when the test passes
- DO NOT write "helper functions" before they're called
- DO NOT write code "because you'll need it later"

### 3. Verify: Run quality checks

- `make check` - All tests must pass
- `make lint` - Code complexity under threshold

## Development Phase Focus

**Test what you build.** During development:

- Write tests for the happy path
- Write tests for obvious error cases
- Cover the main functionality thoroughly
- Keep momentum - don't get stuck on edge cases

**Coverage gaps are OK during development.** They will be closed in a dedicated coverage phase before release.

**The test should come first** - but don't let perfect coverage slow down feature development.

If writing a helper function, ask: "Does a passing test call this right now?" If no, DELETE IT.
