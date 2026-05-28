---
name: test
description: Run the test suite. Use when running tests, checking test coverage, or validating code changes.
allowed-tools: Bash, Read, Glob, Grep
---

# Test - argus

Run the project test suite.

## Command

```bash
go test ./...
```

## Description

Run all tests

## Test Examples

Reference these files for test patterns:
- `internal/detector/architecture_test.go`
- `internal/detector/cli_test.go`
- `internal/detector/codepatterns_test.go`

## On Failure

- Analyze the failing test output
- Identify the root cause of the failure
- Check if it's a test issue or a code issue
- Suggest fixes for the failing tests

## Options

- Add `-run TestName` to run specific test files
- Add `-v` for verbose output

## Success Criteria

- All tests pass
- No skipped tests without reason
- Coverage meets project standards (if applicable)
