---
name: code-review
description: Use this skill to perform comprehensive code reviews, checking for bugs, style issues, security vulnerabilities, performance problems, and adherence to best practices when reviewing pull requests or analyzing code quality.
---

# Code Review Skill

This skill assists in conducting thorough code reviews to ensure quality, security, and performance.

## When to Use This Skill

- Before creating pull requests
- Reviewing complex changes
- Checking for security vulnerabilities
- Identifying performance issues
- Ensuring code quality standards
- Mentoring junior developers

## Code Review Checklist

### 1. Correctness

- [ ] Code does what it's supposed to do
- [ ] Edge cases are handled
- [ ] Error handling is appropriate
- [ ] No obvious bugs
- [ ] Logic is correct and efficient

### 2. Code Quality

- [ ] Code is readable and maintainable
- [ ] Functions are small and focused
- [ ] Variable names are descriptive
- [ ] No code duplication
- [ ] Follows DRY principle
- [ ] Comments explain "why", not "what"

### 3. Type Safety

- [ ] No use of `any` (or justified with comment)
- [ ] Proper TypeScript types
- [ ] No type assertions without reason
- [ ] Interfaces/types are well-defined
- [ ] Generics used appropriately

### 4. Testing

- [ ] New code has tests
- [ ] Tests cover edge cases
- [ ] Tests are meaningful
- [ ] No flaky tests
- [ ] Test names are descriptive

### 5. Performance

- [ ] No unnecessary re-renders (React)
- [ ] Database queries are optimized
- [ ] No N+1 query problems
- [ ] Caching used appropriately
- [ ] Bundle size impact considered

### 6. Security

- [ ] No SQL injection vulnerabilities
- [ ] No XSS vulnerabilities
- [ ] Input validation present
- [ ] Authentication/authorization checked
- [ ] Secrets not committed
- [ ] CORS configured properly

## Review Process

1. **Understand the Change**: Review the diff and commit history.
2. **Check Code Quality**: Run linter and type checker.
3. **Check for Common Issues**: Search for anti-patterns and security issues.
4. **Review Database Changes**: Check migration files and SQL.
5. **Check Dependencies**: Review package changes and security vulnerabilities.

## How to Provide Feedback

- Be specific about what needs to change
- Explain why, not just what
- Suggest alternatives when possible

## Review Comments

### Constructive Feedback

- **Must Fix**: Critical issues that block merge
- **Should Fix**: Important but not blocking
- **Suggestion**: Nice to have improvements
- **Learning**: Educational comments
- **Question**: Asking for clarification

## Automated Review Tools

- **TypeScript Compiler**: Check types across workspace.
- **Biome Linter**: Lint all files and check for specific issues.
- **Tests**: Run all tests and check coverage.

## Best Practices

1. **Be Constructive**: Focus on improvement, not criticism.
2. **Explain Why**: Don't just say "wrong", explain the issue.
3. **Suggest Solutions**: Provide alternatives when possible.
4. **Prioritize**: Mark critical issues vs suggestions.
5. **Be Timely**: Review PRs promptly.
6. **Ask Questions**: Seek to understand before judging.
7. **Praise Good Code**: Acknowledge well-written code.
8. **Stay Professional**: Keep feedback objective and respectful.

## References

- TypeScript Best Practices: https://typescript-eslint.io/rules/
- React Best Practices: https://react.dev/learn
- Security: OWASP Top 10
- Related files:
  - Code style guidelines
  - Linting rules