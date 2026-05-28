---
name: go-testing
description: Go testing patterns. Routes to specific patterns.
---

# Testing

## Route by Pattern
- Table-driven tests → see [table/](table/)
- Subtests with t.Run → see [subtests/](subtests/)
- Test helpers → see [helpers/](helpers/)
- Benchmarks → see [benchmarks/](benchmarks/)

## Quick Check
- [ ] Tests named Test_Function_Scenario
- [ ] Table tests for >2 cases
- [ ] Helpers call t.Helper()
- [ ] Parallel tests capture loop vars

## Common Patterns

**Basic test structure:**
```go
func Test_Function_Scenario(t *testing.T) {
    // Arrange
    input := "test"

    // Act
    result := Function(input)

    // Assert
    if result != expected {
        t.Errorf("got %v, want %v", result, expected)
    }
}
```
