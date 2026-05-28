---
name: generate-tests
description: Generate comprehensive unit tests for selected code
agent: agent
tools: ['search', 'edit', 'read']
---

# Generate Unit Tests

Generate comprehensive unit tests for the selected code following our team patterns.

## Context

- **File**: ${file}
- **Selection**: ${selection}
- **Test Framework**: Detect from project (pytest/unittest/jest/mocha/junit)

## Requirements

Follow the patterns defined in [testing-patterns](../instructions/testing-patterns.instructions.md).

## Analysis Steps

1. Identify all testable functions/methods in the selection
2. Determine input parameters and return types
3. List dependencies that need mocking
4. Identify edge cases and error conditions

## Output

Create a test file with:

### Happy Path Tests

- Test normal operation with valid inputs
- Verify expected return values
- Check side effects (database writes, API calls)

### Edge Case Tests  

- Empty inputs (empty string, empty list, None)
- Boundary values (0, 1, max values)
- Invalid inputs (wrong types, out of range)

### Error Handling Tests

- Expected exceptions are raised
- Error messages are informative
- Cleanup happens on failure

### Fixtures

- Use existing fixtures from conftest.py where available
- Create new fixtures for test-specific data
- Follow [fixture patterns](../references/TEST-FIXTURES.md)

## File Naming

| Source File | Test File |
|-------------|-----------|
| `order_service.py` | `test_order_service.py` |
| `OrderService.java` | `OrderServiceTest.java` |
| `orderService.ts` | `orderService.test.ts` |
