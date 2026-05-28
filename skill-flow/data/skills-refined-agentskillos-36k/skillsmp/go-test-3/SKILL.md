---
name: go-test
description: Generate high-quality Go unit tests for the given code or function.
metadata:
  short-description: Generate table-driven Go unit tests with strong coverage.
---

Generate Go unit tests for the provided code using Go testing best practices.

## Requirements
- Use **table-driven tests** for all testable functions.
- Each test case must:
    - Have a **clear and descriptive name**.
    - Explicitly define inputs, expected outputs, and error expectations.
- Use `testing.T` with `t.Run` for subtests.
- Use **stretchr/testify**:
    - `require` for fatal assertions (setup, preconditions, returned errors).
    - `assert` for value comparisons.
- Use **mocking** where appropriate:
    - Prefer `testify/mock` for interface dependencies.
    - Avoid real external dependencies (DB, network, filesystem).
- Focus on **test coverage**, including:
    - Success cases
    - Error cases
    - Edge cases
    - Boundary conditions
- Tests must be **deterministic** and **_translation-safe_** (no reliance on time, randomness, or global state unless mocked).
- Follow idiomatic Go conventions:
    - File name: `<file>_test.go`
    - Test name: `Test<FunctionName>`
- Always use **English** in test names and comments.
- Enforce minimum **package coverage of 80%**.
- Coverage must include:
    - At least one error path per public function (if applicable).
    - Boundary or edge cases where reasonable.

## Output expectations
- Generate complete, compilable test code.
- Include necessary imports.
- Clearly separate:
    - Arrange
    - Act
    - Assert
- Prefer readability to cleverness.
- Generated tests should realistically achieve ≥80% coverage when executed with: `go test -cover ./...`

## Additional guidelines
- Prefer **small, focused tests** over large monolithic ones.
- If a function is hard to test:
    - Explain briefly **why**
    - Suggest a **refactor** (e.g., dependency injection).
- Do not test private implementation details—test behavior.
- Avoid snapshot-style assertions unless explicitly requested.
- If achieving ≥80% coverage is not possible without testing private implementation details:
    - Explain the limitation briefly
    - Suggest a refactor (interface extraction, dependency injection)
- Avoid fake coverage (e.g. meaningless assertions).
