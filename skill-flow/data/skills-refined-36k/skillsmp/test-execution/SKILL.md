---
name: test-execution
description: Run unit and integration tests, generate coverage reports, and view results. Use to validate code changes before committing or merging.
license: MIT
compatibility: Requires Node.js test runner (vitest, jest) or project-specific test framework
metadata:
  author: ximplicity
  version: "1.0"
  category: testing
---

# Test Execution Skill

Run and manage automated tests.

## Allowed Operations

- Run unit tests
- Run integration tests
- Run specific test files
- Run tests by pattern
- Generate coverage reports
- View test results

## Forbidden Operations

- Modify test files during execution
- Skip tests without documentation
- Disable coverage thresholds
- Run tests against production
- Commit test snapshots without review

## Constraints

- Tests must run in isolated environment
- No network calls to external services (use mocks)
- Test timeout: 30 seconds per test
- Coverage minimum: 80%

## Test Categories

| Type | Speed | Dependencies | When to Run |
|------|-------|--------------|-------------|
| Unit | Fast | Mocked | Every commit |
| Integration | Medium | Test fixtures | Before merge |
| E2E | Slow | Full stack | Before release |

## Quick Commands

```bash
# Run all tests
npm test

# Run with coverage
npm run test:coverage

# Run specific file
npm test -- path/to/test.ts

# Run by pattern
npm test -- --grep "auth"
```

For detailed test patterns, see [TEST-PATTERNS.md](references/TEST-PATTERNS.md).

For coverage configuration, see [COVERAGE-GUIDE.md](references/COVERAGE-GUIDE.md).

## Output Format

```json
{
  "passed": 42,
  "failed": 0,
  "skipped": 2,
  "duration": 1234,
  "coverage": {
    "lines": 85.5,
    "branches": 80.2
  }
}
```

## Failure Handling

- Capture full error output
- Include stack traces
- Show relevant code context
- Suggest potential fixes if obvious

## Example Usage

```
Run all unit tests
Run tests matching "auth"
Run tests with coverage report
Show results of last test run
```
