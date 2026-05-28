# Domain-Driven Development with Context7 Integration

> Module: ANALYZE-PRESERVE-IMPROVE DDD cycle with Context7 patterns and AI-powered testing
> Complexity: Advanced
> Time: 25+ minutes
> Dependencies: Python/TypeScript, test frameworks, Context7 MCP

## Overview

DDD Context7 integration provides a comprehensive domain-driven development workflow with AI-powered test generation, Context7-enhanced testing patterns, and automated best practices enforcement.

### Key Features

- **AI-Powered Test Generation**: Generate comprehensive test suites from specifications
- **Context7 Integration**: Access latest testing patterns and best practices
- **ANALYZE-PRESERVE-IMPROVE Cycle**: Complete DDD workflow implementation
- **Advanced Testing**: Property-based testing, mutation testing, continuous testing
- **Test Patterns**: Comprehensive library of testing patterns and fixtures

---

## Quick Start

### Basic DDD Cycle

```typescript
// Step 1: ANALYZE - Understand existing code
// Use Context7 to get best practices for analysis
// mcp__context7__query-docs: "refactoring patterns", libraryId: "/refactoring"

// Step 2: PRESERVE - Create characterization tests
// Capture existing behavior before making changes
describe('ExistingBehavior', () => {
  it('should preserve current calculation logic', () => {
    const result = existingFunction(input);
    expect(result).toMatchSnapshot();
  });
});

// Step 3: IMPROVE - Refactor with test safety net
// Make changes while keeping tests green
```

---

## Core Components

### DDD Cycle Phases

**1. ANALYZE Phase: Understand existing code**

- Analyze existing code structure and patterns
- Identify current behavior through code reading
- Document dependencies and side effects
- Map test coverage gaps

**2. PRESERVE Phase: Create characterization tests**

- Write characterization tests for existing behavior
- Capture current behavior as the "golden standard"
- Ensure tests pass with current implementation
- Create behavior snapshots for complex outputs

**3. IMPROVE Phase: Refactor with behavior preservation**

- Refactor code while keeping tests green
- Make small, incremental changes
- Run tests after each change
- Maintain behavior preservation

**4. REVIEW Phase: Verify and commit**

- Verify all characterization tests still pass
- Review code quality and documentation
- Check for any behavior changes
- Commit changes with clear messages

---

## Context7 Integration

### Pattern Loading

Use Context7 to access latest testing patterns:

```typescript
// Resolve library for testing patterns
// mcp__context7__resolve-library-id: "vitest testing patterns"

// Query specific documentation
// mcp__context7__query-docs: "mocking best practices", libraryId: resolved_id
```

### Best Practices Retrieval

Query Context7 for language-specific testing patterns:

| Language | Query Example |
|----------|---------------|
| TypeScript | "vitest typescript testing patterns" |
| Python | "pytest best practices" |
| Go | "go testing patterns" |
| Rust | "rust testing cargo" |

---

## Common Use Cases

### Behavior Preservation

```typescript
// Characterization test specification
describe('Calculate Sum - Existing Behavior', () => {
  it('should preserve existing sum calculation', () => {
    // Arrange
    const input = { a: 10, b: 20 };

    // Act
    const result = calculateSum(input);

    // Assert - Document actual behavior
    expect(result).toBe(30);
  });

  it('should handle edge cases as before', () => {
    expect(calculateSum({ a: 0, b: 0 })).toBe(0);
    expect(calculateSum({ a: -5, b: 5 })).toBe(0);
    expect(calculateSum({ a: Number.MAX_SAFE_INTEGER, b: 1 })).toBe(Number.MAX_SAFE_INTEGER + 1);
  });
});
```

### Refactoring with Tests

```typescript
// Integration test specification for refactoring
describe('DatabaseService - Refactoring', () => {
  it('should preserve database behavior during refactoring', async () => {
    // Preserve: Capture current behavior
    const originalResult = await dbService.query('SELECT * FROM users');

    // This test ensures any refactoring maintains identical behavior
    expect(originalResult).toMatchSnapshot();
  });

  it('should handle connection failure as before', async () => {
    // Characterize error handling behavior
    await expect(dbService.query('INVALID SQL'))
      .rejects.toThrow('Syntax error');
  });
});
```

### Exception Behavior Preservation

```typescript
// Exception test specification
describe('Division - Existing Error Handling', () => {
  it('should preserve division by zero exception', () => {
    // Document existing error behavior
    expect(() => divide(10, 0)).toThrow('Division by zero');
  });

  it('should preserve error message format', () => {
    try {
      divide(10, 0);
    } catch (e) {
      expect(e.message).toBe('Division by zero');
      expect(e.code).toBe('MATH_ERROR');
    }
  });
});
```

---

## Best Practices

### Test Design

1. **Characterization First**: Write tests that capture existing behavior before changing code
2. **Descriptive Names**: Test names should clearly describe what behavior is being preserved
3. **Arrange-Act-Assert**: Structure tests with this pattern for clarity
4. **Independent Tests**: Tests should not depend on each other
5. **Fast Execution**: Keep tests fast for quick feedback

### Context7 Integration

1. **Pattern Loading**: Load Context7 patterns for latest best practices
2. **Edge Case Detection**: Use Context7 to identify missing edge cases
3. **Test Suggestions**: Leverage AI suggestions for test improvements
4. **Quality Analysis**: Use Context7 for test quality analysis

### DDD Workflow

1. **Analyze First**: Always understand existing behavior before changing code
2. **Preserve with Tests**: Create characterization tests before refactoring
3. **Keep Tests Green**: Never commit failing tests
4. **Small Increments**: Make small, incremental changes
5. **Continuous Testing**: Run tests after every change

---

## Advanced Features

### Property-Based Testing

Use Hypothesis (Python) or fast-check (TypeScript) for property-based testing:

```typescript
import * as fc from 'fast-check';

describe('Addition Properties', () => {
  it('should be commutative', () => {
    fc.assert(fc.property(
      fc.integer(), fc.integer(),
      (a, b) => add(a, b) === add(b, a)
    ));
  });

  it('should be associative', () => {
    fc.assert(fc.property(
      fc.integer(), fc.integer(), fc.integer(),
      (a, b, c) => add(add(a, b), c) === add(a, add(b, c))
    ));
  });
});
```

### Mutation Testing

Verify test suite quality by introducing code mutations:

```bash
# TypeScript with Stryker
npx stryker run

# Python with mutmut
mutmut run
```

### Continuous Testing

Implement watch mode for automatic test execution:

```json
// package.json
{
  "scripts": {
    "test:watch": "vitest --watch",
    "test:coverage": "vitest --coverage"
  }
}
```

---

## Performance Considerations

- **Test Execution**: Use parallel test execution for faster feedback
- **Test Isolation**: Ensure tests are isolated to prevent interference
- **Mock External Dependencies**: Mock external services for fast, reliable tests
- **Optimize Setup**: Use fixtures and test factories for efficient test setup

---

## Troubleshooting

### Common Issues

**1. Tests Failing Intermittently**

- Check for shared state between tests
- Verify test isolation
- Add proper cleanup in fixtures

**2. Slow Test Execution**

- Use parallel test execution
- Mock external dependencies
- Optimize test setup

**3. Context7 Integration Issues**

- Verify Context7 MCP configuration
- Check network connectivity
- Use default patterns as fallback

---

## Integration with DDD Workflow

### Workflow Integration Points

```
/jikime:2-run (DDD Mode)
       │
       ▼
┌──────────────────────┐
│    ANALYZE Phase     │
│  • Context7 patterns │
│  • Code analysis     │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│    PRESERVE Phase    │
│  • Characterization  │
│  • Snapshot tests    │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│    IMPROVE Phase     │
│  • Refactoring       │
│  • Continuous tests  │
└──────────────────────┘
```

### Agent Integration

| Agent | DDD Role |
|-------|----------|
| manager-ddd | Orchestrates DDD cycle |
| test-guide | Creates characterization tests |
| refactorer | Implements improvements |
| manager-quality | Validates behavior preservation |

---

## Related Modules

- [Vitest Testing](./vitest.md) - TypeScript testing with Vitest
- [Playwright E2E](./playwright.md) - End-to-end testing
- [Quality Gates](./quality-gates.md) - Quality validation

---

Module: `modules/ddd-context7.md`
Version: 1.0.0
Last Updated: 2026-01-22
