# Code Review Guide

## Review Areas

### 1. Security Issues

- Input validation and sanitization
- Authentication and authorization
- Data exposure risks
- Injection vulnerabilities

### 2. Performance & Efficiency

- Algorithm complexity
- Memory usage patterns
- Database query optimization
- Unnecessary computations

### 3. Code Quality

- Adherence to best practices
- Readability and maintainability
- Proper naming conventions
- Function/class size and responsibility
- Code duplication

### 4. Architecture & Design

- Design pattern usage
- Separation of concerns
- Dependency management
- Error handling strategy

### 5. Testing & Documentation

- Test coverage and quality
- Documentation completeness
- Comment clarity and necessity

## Output Format

Provide feedback as:

- **Critical Issues** - Must fix before merge
- **Suggestions** - Improvements to consider
- **Good Practices** - What's done well

For each issue include:

1. Specific line references
2. Clear explanation of the problem
3. Suggested solution with code example
4. Rationale for the change

Be constructive and helpful in your feedback.
