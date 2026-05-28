---
name: code-review
description: Use this skill when reviewing code changes to ensure quality, security, and adherence to best practices.
---

# Code Review Skill

This skill helps you perform thorough code reviews for quality, security, and performance.

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
- [ ] Follows project style guidelines

### 3. Performance

- [ ] No unnecessary re-renders (for UI frameworks)
- [ ] Database queries are optimized
- [ ] No N+1 query problems
- [ ] Caching used appropriately
- [ ] Bundle size impact considered

### 4. Security

- [ ] No SQL injection vulnerabilities
- [ ] No XSS vulnerabilities
- [ ] Input validation present
- [ ] Authentication/authorization checked
- [ ] Secrets not committed
- [ ] CORS configured properly

### 5. Design Principles

- [ ] Changes fit the intended architecture and structure
- [ ] Avoid hacks or special cases
- [ ] Use existing utilities and libraries
- [ ] Follow established design patterns

## How to Provide Feedback

- Be specific about what needs to change
- Explain why, not just what
- Suggest alternatives when possible

## Automation Tools

Before starting a manual review, run lint checks to quickly identify common issues:

```bash
.agent/skills/code-review/scripts/lint-check.sh .
```

## Common Issues to Look For

### Anti-Patterns

**❌ Magic Numbers**
```typescript
// Bad
if (user.age > 18) {
  allowAccess();
}

// Good
const LEGAL_AGE = 18;
if (user.age >= LEGAL_AGE) {
  allowAccess();
}
```

**❌ Deep Nesting**
```typescript
// Bad
if (user) {
  if (user.isActive) {
    if (user.hasPermission) {
      if (resource.isAvailable) {
        // do something
      }
    }
  }
}

// Good
if (!user || !user.isActive || !user.hasPermission || !resource.isAvailable) {
  return;
}
// do something
```