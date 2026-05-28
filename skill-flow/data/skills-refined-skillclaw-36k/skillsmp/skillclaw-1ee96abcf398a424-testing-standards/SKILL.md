---
name: testing-standards
description: Use this skill when generating comprehensive unit tests, integration tests, or end-to-end tests for any code, following TDD and best practices.
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

1. **Descriptive Names**: Use clear and specific names for tests, e.g., `it('should return 401 when token is expired')`.
2. **One Assert Per Concept**: Ensure each test checks one specific behavior.
3. **Independent Tests**: Avoid shared state between tests to ensure reliability.
4. **Use Factories**: Create test data using factories for consistency.
5. **Mock External Services**: Mock APIs, databases, and file systems to isolate tests.

## Credits

**Author:** [Michel Abboud](https://github.com/michelabboud)  
**AI Assistance:** Created with the help of Claude Code (Anthropic)  
**License:** Apache-2.0