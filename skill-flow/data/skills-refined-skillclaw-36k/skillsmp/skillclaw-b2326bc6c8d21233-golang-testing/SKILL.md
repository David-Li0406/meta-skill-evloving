---
name: golang-testing
description: Use this skill when writing comprehensive test suites in Go, including unit tests, mocking, and performance benchmarking.
---

# Go Testing Standards and Strategies

## Overview

Go provides a robust built-in testing framework (`testing` package) that emphasizes simplicity and developer productivity. Combined with community tools like Testify and GoMock, Go testing enables comprehensive test coverage with minimal boilerplate.

## Key Features

- **Table-Driven Tests**: The idiomatic way to write tests in Go, allowing for multiple inputs in a single function.
- **Subtests (`t.Run`)**: Organize related tests for better reporting.
- **Parallel Usage**: Use `t.Parallel()` for independent tests to speed up execution.
- **Mock Interfaces**: Mock dependencies through interfaces using tools like GoMock and Testify.
- **Benchmarking**: Built-in performance testing to ensure efficiency.
- **Race Detector**: Verify thread safety in concurrent code.
- **Coverage Reporting**: Native coverage reporting and enforcement for quality assurance.
- **CI Integration**: Test caching and parallel execution for continuous integration pipelines.

## When to Use This Skill

Activate this skill when:
- Writing test suites for Go libraries or applications.
- Setting up testing infrastructure for new projects.
- Mocking external dependencies (databases, APIs, services).
- Benchmarking performance-critical code paths.
- Ensuring thread-safe concurrent implementations.
- Integrating tests into CI/CD pipelines.

## Core Testing Principles

1. **Simplicity Over Magic**: Prefer the standard library when possible.
2. **Table-Driven Tests**: Use this pattern to test multiple scenarios efficiently.
3. **Mocking**: Use interface-based mocking to isolate tests.
4. **Test File Naming**: Use `*_test.go` for test files and `func TestName(t *testing.T)` for test functions.
5. **Avoid Anti-Patterns**: Do not use sleeping in tests; instead, utilize channels or waitgroups.

## Tools

- **Stdlib**: The `testing` package is usually sufficient.
- **Testify**: Provides readable assertions and mocks.
- **GoMock**: A popular mocking framework for type-safe interface mocking.

## Quick Start

1. Structure tests using the table-driven pattern.
2. Use Testify for assertions.
3. Mock interfaces with GoMock.
4. Benchmark critical paths.
5. Integrate coverage in CI/CD pipelines.

## References

- [Table-Driven Tests](references/table-driven-tests.md)
- [Mocking Strategies](references/mocking-strategies.md)