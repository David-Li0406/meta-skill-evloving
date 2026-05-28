---
name: code-reviewer
description: Review code for quality, bugs, and best practices. Use when the user says "review this code", "check my implementation", "code quality", "is this code ready", or asks for feedback on specific code. For comprehensive automated reviews that populate REVIEW.md, use the code-auditor agent instead.
---

# Code Reviewer

Provide inline code review feedback during normal conversation. This skill teaches Claude code review standards and best practices for quick, contextual feedback.

## When to Use

- Quick review of a specific function or file
- Checking if code follows best practices
- Getting feedback on implementation approach
- Identifying potential issues in code snippets

## Quick Review Checklist

When reviewing code, check for:

### Correctness
- Does the code do what it's supposed to do?
- Are edge cases handled?
- Are error conditions handled properly?

### Security
- Input validation present?
- No hardcoded secrets or credentials?
- Safe handling of user data?

### Performance
- Obvious inefficiencies?
- Unnecessary loops or allocations?
- Appropriate data structures?

### Maintainability
- Clear naming and structure?
- Appropriate comments for complex logic?
- No excessive duplication?

### Testing
- Are tests present or needed?
- Are edge cases covered?

## Review Format

When providing feedback, organize by severity:

**Critical** (must fix):
- Security vulnerabilities
- Logic errors causing incorrect behavior
- Data loss or corruption risks

**Warning** (should fix):
- Missing error handling
- Performance issues
- Missing tests for critical paths

**Suggestion** (nice to have):
- Code style improvements
- Refactoring opportunities
- Documentation additions

For detailed checklist, see [checklist.md](checklist.md).
For common anti-patterns, see [patterns.md](patterns.md).
