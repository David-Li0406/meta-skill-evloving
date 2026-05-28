---
name: code-review
description: Systematic code review checklist for quality and security
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: review
---

## What I Do

- Provide systematic review checklist
- Identify security, performance, and maintainability issues
- Ensure consistent review quality
- Focus on what matters most

## When to Use Me

Use this skill when:
- Reviewing pull requests
- Self-reviewing before submitting
- Auditing existing code
- Onboarding to a new codebase

## Review Checklist

### 1. Correctness

- [ ] Does the code do what it's supposed to do?
- [ ] Are edge cases handled?
- [ ] Are error conditions handled gracefully?
- [ ] Are there any obvious bugs?

### 2. Security

- [ ] Input validation present?
- [ ] No SQL injection vulnerabilities?
- [ ] No XSS vulnerabilities?
- [ ] Sensitive data not logged or exposed?
- [ ] Authentication/authorization correct?
- [ ] No hardcoded secrets?

### 3. Performance

- [ ] No N+1 queries?
- [ ] Appropriate caching?
- [ ] No unnecessary loops or iterations?
- [ ] Large data sets paginated?
- [ ] Async operations where appropriate?

### 4. Maintainability

- [ ] Code is readable and self-documenting?
- [ ] Functions are small and focused?
- [ ] No code duplication?
- [ ] Naming is clear and consistent?
- [ ] Comments explain WHY, not WHAT?

### 5. Testing

- [ ] Tests exist for new functionality?
- [ ] Edge cases tested?
- [ ] Tests are readable and maintainable?
- [ ] No flaky tests?

### 6. Architecture

- [ ] Follows existing patterns?
- [ ] Appropriate separation of concerns?
- [ ] Dependencies are reasonable?
- [ ] No circular dependencies?

## Review Feedback Format

**For issues:**
```
[SEVERITY] File:Line - Description

Problem: What's wrong
Impact: Why it matters  
Suggestion: How to fix
```

**Severity levels:**
- `[BLOCKER]` - Must fix before merge
- `[MAJOR]` - Should fix, significant issue
- `[MINOR]` - Nice to fix, small improvement
- `[NIT]` - Optional, style preference

## Good Review Practices

1. **Be constructive** - Suggest solutions, not just problems
2. **Be specific** - Point to exact lines
3. **Be kind** - Review the code, not the person
4. **Be thorough** - Don't just skim
5. **Be timely** - Review within 24 hours

## Self-Review Checklist

Before submitting a PR, verify:
- [ ] I've reviewed my own diff
- [ ] Tests pass locally
- [ ] No debug code left in
- [ ] No commented-out code
- [ ] Commit messages are clear
- [ ] PR description explains the change
