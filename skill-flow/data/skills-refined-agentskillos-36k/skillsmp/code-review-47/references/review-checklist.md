# Code Review Checklist

## General Code Quality

- [ ] **Naming**: Clear, descriptive names for variables, functions, classes
- [ ] **Readability**: Code is easy to understand without excessive comments
- [ ] **Comments**: Complex logic explained, WHY not WHAT
- [ ] **Formatting**: Consistent style, proper indentation
- [ ] **DRY**: No duplicated code
- [ ] **YAGNI**: No unnecessary features or abstractions

## Functions/Methods

- [ ] **Single Responsibility**: One clear purpose
- [ ] **Length**: ≤50 lines preferred
- [ ] **Parameters**: ≤5 parameters
- [ ] **Return Values**: Consistent, predictable
- [ ] **Side Effects**: Minimized and documented

## Performance

- [ ] **Complexity**: O(n) or better where possible
- [ ] **Loops**: No unnecessary nesting
- [ ] **Database**: Queries optimized, indexes used
- [ ] **Memory**: No obvious leaks
- [ ] **Caching**: Used appropriately

## Architecture

- [ ] **Modularity**: Well-organized, logical structure
- [ ] **Coupling**: Loose coupling between modules
- [ ] **Cohesion**: High cohesion within modules
- [ ] **Dependencies**: Minimal, well-justified
- [ ] **SOLID Principles**: Followed where applicable

## Error Handling

- [ ] **Exceptions**: Caught and handled appropriately
- [ ] **Edge Cases**: Considered and tested
- [ ] **Validation**: Input validated
- [ ] **Logging**: Errors logged with context

## Testing

- [ ] **Coverage**: Critical paths tested
- [ ] **Unit Tests**: Functions tested in isolation
- [ ] **Edge Cases**: Boundary conditions tested
- [ ] **Test Quality**: Tests are maintainable

## Security

- [ ] **Input Validation**: All inputs validated
- [ ] **SQL Injection**: Parameterized queries used
- [ ] **XSS**: Output sanitized
- [ ] **Authentication**: Properly implemented
- [ ] **Secrets**: No hardcoded secrets

## Documentation

- [ ] **API Docs**: Public interfaces documented
- [ ] **README**: Updated if needed
- [ ] **Change Log**: Significant changes noted
