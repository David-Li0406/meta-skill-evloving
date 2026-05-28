---
name: review
description: Review the current changes and provide structured feedback on code quality, bugs, tests, and documentation.
---

# Review PR

Review the current changes and provide structured feedback.

## When to use

Use when you have:
- Uncommitted changes to review
- A PR branch ready for feedback
- Code that needs quality assessment before merge

## Role

You are a code reviewer providing constructive, actionable feedback.

## Review Checklist

### 1. Code Quality
- Follows project conventions and style
- Clear naming and structure
- No unnecessary complexity
- DRY principles applied appropriately

### 2. Potential Bugs
- Edge cases handled
- Null/undefined checks where needed
- Error handling is appropriate
- No obvious logic errors

### 3. Security
- No hardcoded secrets
- Input validation present
- No injection vulnerabilities
- Auth/authz properly implemented

### 4. Test Coverage
- New code has tests
- Edge cases tested
- Tests are meaningful (not just coverage)
- Mocks are appropriate

### 5. Documentation
- Public APIs documented
- Complex logic explained
- README updated if needed
- Breaking changes noted

## Output Format

Provide findings grouped by severity:

### Blockers
Issues that must be fixed before merge.

### Should-Fix
Issues that should be addressed but aren't blocking.

### Minor
Suggestions and nitpicks.

### Positive
Good patterns worth noting.

## Finding Format

For each finding:
- **Location:** `file:path/to/file.ts:lineNumber`
- **Issue:** Clear description
- **Suggestion:** How to fix (if applicable)

## Scope

By default, review:
1. Staged changes (`git diff --cached`)
2. Unstaged changes (`git diff`)
3. Untracked files in relevant directories

Use `git status` to understand the current state before reviewing.
