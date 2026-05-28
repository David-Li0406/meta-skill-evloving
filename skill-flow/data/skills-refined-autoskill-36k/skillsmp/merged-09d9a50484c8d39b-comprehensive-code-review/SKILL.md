---
name: comprehensive-code-review
description: Use this skill to perform a thorough code review focusing on quality, security, performance, and best practices.
---

# Comprehensive Code Review Skill

When conducting a code review, follow this structured approach to ensure a comprehensive evaluation of the code.

## Review Process

1. **Initial Scan**
   - Understand the purpose and context of the changes.
   - Identify the scope and affected components.
   - Note any breaking changes or major refactoring.

2. **Detailed Analysis**

### Core Review Areas

- **Security**
  - Check for input validation and sanitization.
  - Identify hardcoded secrets or sensitive data.
  - Look for vulnerabilities such as SQL injection and XSS.
  - Ensure proper authentication and authorization mechanisms are in place.

- **Performance**
  - Evaluate algorithm efficiency and memory usage.
  - Identify unnecessary computations or redundant operations.
  - Check for optimized database queries and caching strategies.

- **Code Quality**
  - Assess readability and maintainability of the code.
  - Ensure adherence to naming conventions and DRY principles.
  - Verify proper error handling and edge case management.
  - Check for appropriate use of design patterns and abstractions.

- **Testing**
  - Confirm comprehensive unit test coverage and quality.
  - Ensure edge cases and error scenarios are tested.
  - Review the organization and maintainability of tests.

- **Documentation**
  - Look for clear comments on complex logic.
  - Ensure public APIs are well-documented.
  - Check that the README and changelog are updated as necessary.

## Feedback Structure

Provide feedback in the following format:

```
## Summary
[Brief overall assessment]

## Critical Issues
- [List any security or major bugs]

## Suggestions for Improvement
- [List suggested improvements with specific examples]

## Good Practices Observed
- [List positive aspects of the code]
```

## Guidelines for Feedback

- Be specific about what needs to change and explain why.
- Provide actionable suggestions and alternatives when possible.
- Use clear line references and examples to illustrate points.

## Checklist for Review

### Correctness
- [ ] Code functions as intended.
- [ ] Edge cases are handled appropriately.
- [ ] Error handling is implemented.

### Security
- [ ] No hardcoded secrets or credentials.
- [ ] Input is validated and sanitized.
- [ ] No vulnerabilities present.

### Performance
- [ ] Efficient algorithms are used.
- [ ] Resource management is appropriate.

### Code Quality
- [ ] Code is readable and maintainable.
- [ ] Follows established coding standards.

### Testing
- [ ] Adequate test coverage is present.
- [ ] Tests are clear and maintainable.

### Documentation
- [ ] Code is well-commented.
- [ ] Documentation is complete and up-to-date.

Remember to be constructive and educational in your feedback, aiming to improve code quality while respecting the developer's work.