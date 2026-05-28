---
name: code-review
description: Thorough code review with focus on bugs, security, and best practices
triggers:
  - "(?i)review"
  - "(?i)code review"
  - "(?i)check.*code"
---

# Code Review Skill

When this skill is loaded, perform thorough code reviews focusing on:

## Review Checklist

### 1. Correctness
- Logic errors and edge cases
- Off-by-one errors
- Null/undefined handling
- Race conditions in async code

### 2. Security
- Input validation and sanitization
- SQL injection / XSS vulnerabilities
- Secrets/credentials exposure
- Authentication/authorization issues

### 3. Performance
- N+1 queries
- Unnecessary re-renders (React)
- Memory leaks
- Inefficient algorithms

### 4. Code Quality
- Clear naming and intent
- DRY violations
- Single responsibility
- Error handling

### 5. Testing
- Missing test coverage
- Edge cases not tested
- Mocking correctness

## Output Format

Provide review comments with:
1. **Location**: File and line reference
2. **Severity**: 🔴 Critical, 🟠 Warning, 🟡 Suggestion
3. **Issue**: Clear description
4. **Fix**: Concrete recommendation
