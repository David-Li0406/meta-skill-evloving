---
name: testing-standards
description: Write comprehensive tests following TDD and best practices. Use when generating unit tests, integration tests, or end-to-end tests for any code.
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

---

## Credits

**Author:** [Michel Abboud](https://github.com/michelabboud)  
**AI Assistance:** Created with the help of Claude Code (Anthropic)  
**License:** Apache-2.0  

💡 **Want more?** Explore [claude-code-helper](https://github.com/michelabboud/claude-code-helper) for 30+ agents, 13+ skills, 9 MCP servers, and comprehensive guides.