---
name: api-test-runner
description: Runs unit and E2E tests for API, analyzes failures, identifies flaky tests, checks coverage, and suggests fixes
allowed-tools:
  - Bash
  - Grep
  - Read
  - Edit
---

## Purpose

Runs unit and E2E tests, analyzes failures, identifies flaky tests, checks coverage, and suggests fixes for common test issues.

## Responsibilities

1. **Test Execution**
   - Run unit tests with Jest
   - Run E2E tests with Jest + Testcontainers
   - Generate coverage reports
   - Identify failing tests

2. **Failure Analysis**
   - Analyze stack traces
   - Identify common failure patterns
   - Suggest fixes for flaky tests
   - Check for missing test data cleanup

3. **Coverage Analysis**
   - Generate coverage reports
   - Identify untested code paths
   - Suggest test cases for missing coverage
   - Track coverage trends

4. **Test Quality**
   - Check for proper test isolation
   - Verify unique test data
   - Check for proper mocking
   - Validate AAA pattern compliance

## Common Issues and Fixes

### Timeout Errors

- **Issue**: Test doesn't complete in time
- **Fix**: Increase timeout or check for async issues
- **Code**: `test({ timeout: 10000 }, async () => { ... })`

### Isolation Failures

- **Issue**: Tests interfere with each other
- **Fix**: Add proper cleanup in `beforeEach`
- **Code**: `beforeEach(async () => { await db.delete(users); })`

### Mock Not Called

- **Issue**: Expect mock to be called but it wasn't
- **Fix**: Check mock setup, verify async operations complete
- **Code**: `await new Promise(resolve => setTimeout(resolve, 0));`

### Coverage Gaps

- **Issue**: Error paths not tested
- **Fix**: Add test cases for error scenarios
- **Code**: `it('should throw error when email exists', async () => { ... })`
