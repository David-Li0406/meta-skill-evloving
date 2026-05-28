---
name: testing-patterns
description: TDD workflows, test generation, and coverage strategies with Claude Code. Use when writing tests, implementing TDD, analyzing coverage gaps, or generating quality unit/integration/e2e tests. Covers Jest, Vitest, pytest, and mocking patterns.
version: 1.0.0
author: Claude Code SDK
tags: [testing, tdd, coverage, quality]
---

# Testing Patterns

Systematic approaches for test-driven development, test generation, and coverage optimization with Claude Code.

## Quick Reference

| Pattern | When to Use | Key Benefit |
|---------|-------------|-------------|
| TDD Workflow | New features | Design emerges from tests |
| Test Generation | Existing code | Rapid test creation |
| Coverage Analysis | Before release | Find untested paths |
| Edge Case Testing | Critical paths | Prevent regressions |

## TDD Workflow Summary

The red-green-refactor cycle with Claude:

```
1. Write Failing Test  -->  2. Implement Minimum  -->  3. Refactor
   (You describe)           (Claude implements)        (Both review)
```

### Quick TDD Prompt

```
Write a failing test for [feature]. The function should:
- Accept [inputs]
- Return [outputs]
- Throw [errors] when [conditions]

Do NOT implement the function yet.
```

After test fails:

```
Now implement the minimum code to make this test pass.
```

See [TDD-WORKFLOW.md](./TDD-WORKFLOW.md) for complete patterns.

## Test Generation Commands

### Generate Tests for Existing Code

```
Write comprehensive tests for src/utils/validation.ts covering:
- Happy path scenarios
- Edge cases (empty, null, undefined)
- Error conditions
- Boundary values
```

### Generate Tests from Specification

```
Given this API specification:
[paste spec]

Generate integration tests that verify:
- All endpoints return correct status codes
- Response bodies match schema
- Error responses are properly formatted
```

### Generate E2E Tests

```
Write Playwright tests for the user registration flow:
1. Navigate to /register
2. Fill form with valid data
3. Submit and verify redirect to /dashboard
4. Verify welcome message shows username
```

See [TEST-GENERATION.md](./TEST-GENERATION.md) for framework-specific patterns.

## Coverage Strategy

### Quick Coverage Analysis

```bash
# JavaScript/TypeScript (Jest)
bun test --coverage

# JavaScript/TypeScript (Vitest)
bun test --coverage

# Python
pytest --cov=src --cov-report=html
```

### Prompt for Coverage Gaps

```
Analyze this coverage report and identify:
1. Untested functions
2. Untested branches
3. Edge cases not covered

[paste coverage report]

Then generate tests to cover the gaps.
```

See [COVERAGE.md](./COVERAGE.md) for detailed strategies.

## Framework Quick Reference

### Jest (JavaScript/TypeScript)

```typescript
describe('UserService', () => {
  beforeEach(() => {
    // Setup
  });

  it('should create user with valid data', async () => {
    const result = await userService.create(validData);
    expect(result).toMatchObject({ id: expect.any(String) });
  });

  it('should throw on duplicate email', async () => {
    await userService.create(validData);
    await expect(userService.create(validData))
      .rejects.toThrow('Email already exists');
  });
});
```

### Vitest (JavaScript/TypeScript)

```typescript
import { describe, it, expect, beforeEach, vi } from 'vitest';

describe('UserService', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should create user with valid data', async () => {
    const result = await userService.create(validData);
    expect(result).toMatchObject({ id: expect.any(String) });
  });
});
```

### pytest (Python)

```python
import pytest

class TestUserService:
    @pytest.fixture(autouse=True)
    def setup(self):
        # Setup
        pass

    def test_create_user_with_valid_data(self, user_service):
        result = user_service.create(valid_data)
        assert result['id'] is not None

    def test_raise_on_duplicate_email(self, user_service):
        user_service.create(valid_data)
        with pytest.raises(ValueError, match='Email already exists'):
            user_service.create(valid_data)
```

## Mocking Patterns

### Mock External Services

```
Mock the following for testing:
- API calls to /api/users
- Database queries
- File system operations
- Date/time functions

Use [framework] mocking utilities.
```

### Jest Mock Example

```typescript
// Mock module
jest.mock('./database', () => ({
  query: jest.fn().mockResolvedValue([{ id: 1, name: 'Test' }])
}));

// Mock specific function
const mockFetch = jest.spyOn(global, 'fetch')
  .mockResolvedValue(new Response(JSON.stringify({ data: 'test' })));

// Verify mock called
expect(mockFetch).toHaveBeenCalledWith('/api/users', expect.any(Object));
```

### Vitest Mock Example

```typescript
import { vi } from 'vitest';

// Mock module
vi.mock('./database', () => ({
  query: vi.fn().mockResolvedValue([{ id: 1, name: 'Test' }])
}));

// Mock specific function
const mockFetch = vi.spyOn(global, 'fetch')
  .mockResolvedValue(new Response(JSON.stringify({ data: 'test' })));
```

## Test Organization

### File Structure

```
src/
  utils/
    validation.ts
    validation.test.ts      # Co-located unit tests
tests/
  integration/
    api.test.ts             # Integration tests
  e2e/
    user-flow.spec.ts       # E2E tests
  fixtures/
    users.json              # Test data
```

### Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| Unit test | `*.test.ts` | `validation.test.ts` |
| Integration | `*.integration.test.ts` | `api.integration.test.ts` |
| E2E | `*.spec.ts` or `*.e2e.ts` | `login.spec.ts` |

## Edge Case Checklist

Ask Claude to test these scenarios:

- [ ] Empty inputs (empty string, empty array, empty object)
- [ ] Null and undefined values
- [ ] Boundary values (0, -1, MAX_INT)
- [ ] Invalid types (string where number expected)
- [ ] Unicode and special characters
- [ ] Very large inputs
- [ ] Concurrent operations
- [ ] Network failures
- [ ] Timeout scenarios
- [ ] Permission errors

## Prompting Best Practices

### Be Specific About Expectations

**Good:**
```
Test that createUser:
- Returns user object with id, email, createdAt
- Sets createdAt to current timestamp
- Hashes password before storage
- Throws ValidationError for invalid email format
```

**Avoid:**
```
Test the createUser function
```

### Specify Test Framework

**Good:**
```
Using Jest with TypeScript, write tests for...
```

**Avoid:**
```
Write tests for...
```

### Request Assertions

**Good:**
```
Include assertions for:
- Return value structure
- Side effects (database calls)
- Error messages
```

## Common Workflows

### Workflow: Add Tests to Untested Code

1. Ask Claude to analyze the function
2. Request test cases covering all branches
3. Review generated tests for completeness
4. Run tests and verify they pass
5. Check coverage report

### Workflow: Fix Failing Test

1. Share failing test and error
2. Ask Claude to diagnose the issue
3. Implement fix
4. Verify test passes
5. Check for regressions

### Workflow: Increase Coverage

1. Generate coverage report
2. Share report with Claude
3. Request tests for uncovered lines
4. Review and run new tests
5. Re-check coverage

## Reference Files

| File | Contents |
|------|----------|
| [TDD-WORKFLOW.md](./TDD-WORKFLOW.md) | Test-driven development patterns |
| [TEST-GENERATION.md](./TEST-GENERATION.md) | Generating quality tests |
| [COVERAGE.md](./COVERAGE.md) | Coverage strategies and analysis |

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Testing implementation | Brittle tests | Test behavior, not internals |
| Over-mocking | Tests pass, code fails | Mock only external deps |
| No assertions | Tests always pass | Require explicit expects |
| Shared state | Flaky tests | Isolate test data |
| Ignoring edge cases | Bugs in production | Use edge case checklist |
