---
name: review-pr
description: Comprehensive pull request review covering code quality, tests, security, and documentation. Use when reviewing PRs or when asked to review changes.
---

# Review PR

## Description
Comprehensive pull request review covering code quality, tests, security, and documentation.

## Inputs
- `pr`: PR number or URL (optional, defaults to current branch's PR)

## Steps

### 1. Gather PR Context
- Fetch PR diff, title, and description
- Identify all changed files
- Check PR size and scope

### 2. Code Quality Review
For each changed file:
- Logic correctness
- Error handling
- Edge cases covered
- Code clarity and readability
- Naming conventions
- DRY violations
- Unnecessary complexity

### 3. Architecture Review
- Does the change fit the existing architecture?
- Are there better patterns to use?
- Is the abstraction level appropriate?
- Any potential scaling concerns?

### 4. Security Review
- Input validation
- Authentication/authorization
- SQL injection, XSS, CSRF
- Secrets handling
- Dependency vulnerabilities

### 5. Test Review
- Are new paths tested?
- Test quality (not just coverage)
- Edge cases in tests
- Mocking appropriateness

### 6. Documentation
- Are public APIs documented?
- README updates needed?
- Breaking changes noted?

### 7. Generate Review
Output structured feedback:
- **Must Fix**: Blocking issues
- **Should Fix**: Important but not blocking
- **Consider**: Suggestions and improvements
- **Praise**: What was done well

## Example Usage
```
/review-pr 123
/review-pr https://github.com/org/repo/pull/123
/review-pr  # Reviews current branch's PR
```
