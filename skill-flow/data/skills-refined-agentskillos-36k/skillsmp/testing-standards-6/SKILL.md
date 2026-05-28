---
name: testing-standards
description: Write comprehensive tests following TDD and best practices. Use when generating unit tests, integration tests, or end-to-end tests for any code
dependencies:
  - jest
  - @testing-library/react
---

# Testing Standards Skill

## Test Structure (AAA Pattern)

```javascript
describe('Component/Function Name', () => {
  it('should do something specific', () => {
    // Arrange - Set up test data
    const input = { foo: 'bar' }
    
    // Act - Execute the code
    const result = functionUnderTest(input)
    
    // Assert - Verify results
    expect(result).toEqual(expectedOutput)
  })
})
```

## Test Categories

### Unit Tests
- Test single functions/methods
- Mock all dependencies
- Fast (<100ms per test)
- High coverage (80%+)

### Integration Tests
- Test component interactions
- Use test database
- Moderate speed
- Focus on critical paths

### E2E Tests
- Test complete user flows
- Use real browser
- Slower execution
- Test happy paths only

## Best Practices

1. **Descriptive Names**: `it('should return 401 when token is expired')`
2. **One Assert Per Concept**: Test one thing at a time
3. **Independent Tests**: No shared state between tests
4. **Use Factories**: Create test data with factories
5. **Mock External Services**: APIs, databases, file system
