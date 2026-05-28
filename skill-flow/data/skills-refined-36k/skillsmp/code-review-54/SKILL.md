---
name: code-review
description: Review code for quality, security, and best practices
version: 1.0.0
author: AI Team
tags: [review, security, quality]
---

# Code Review

Comprehensive code review covering quality, security, and best practices.

## When to Use

- Reviewing pull requests
- Pre-commit code quality check
- Security audit of new code
- Learning code review practices

## Available Operations

1. **Quality Review**: Code style, patterns, readability
2. **Security Review**: OWASP vulnerabilities, input validation
3. **Performance Review**: Efficiency, resource usage
4. **Full Review**: All of the above

## Instructions

### Step 1: Identify Files to Review

Determine scope:

- Single file: Direct review
- Multiple files: Prioritize by change size
- PR: Focus on changed files

### Step 2: Quality Review

Check against `references/best_practices.md`:

- Code organization
- Naming conventions
- Error handling
- Documentation

### Step 3: Security Review

Check against `references/security_checklist.md`:

- Input validation
- Authentication/Authorization
- Data exposure
- Injection vulnerabilities

### Step 4: Anti-Pattern Detection

Check against `references/common_antipatterns.md`:

- Code smells
- Design anti-patterns
- Language-specific issues

### Step 5: Generate Report

Format findings by severity:

- **Critical**: Must fix before merge
- **Warning**: Should fix, not blocking
- **Info**: Suggestions for improvement

## Resources

Load these Level 3 resources based on review type:

- `references/best_practices.md` - Load for quality reviews
- `references/security_checklist.md` - Load for security audits
- `references/common_antipatterns.md` - Load for anti-pattern detection

**Note:** Only load the resource relevant to the current task to conserve tokens.

## Examples

### Example 1: Security-Focused Review

**User asks:** "Review this authentication code for security issues"

**Response:**

1. Load `references/security_checklist.md`
2. Check against OWASP Top 10
3. Verify input validation
4. Check token handling
5. Report findings with severity

### Example 2: Quality Review

**User asks:** "Review this PR for code quality"

**Response:**

1. Load `references/best_practices.md`
2. Check naming conventions
3. Verify error handling
4. Assess test coverage
5. Report findings

## Output Format

```markdown
## Code Review Summary

**Files Reviewed:** N
**Issues Found:** N (Critical: N, Warning: N, Info: N)

### Critical Issues
- `file.go:123` - Description
  - **Fix:** Suggested solution

### Warnings
- `file.go:45` - Description

### Suggestions
- Consider refactoring X for clarity

### Positive Observations
- Good error handling in Y
- Comprehensive test coverage
```

## Notes

- Always load specific reference based on review type
- Don't load all references at once (token efficiency)
- Prioritize critical issues over style nits
- Consider project-specific patterns from .claude/rules/
