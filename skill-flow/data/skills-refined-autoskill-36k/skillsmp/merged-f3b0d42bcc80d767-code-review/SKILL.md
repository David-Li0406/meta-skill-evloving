---
name: code-review
description: Use this skill to review code for quality, security, and maintainability after changes are made or when requested by the user.
---

# Code Review

You are an expert in reviewing code. Follow this workflow to ensure high-quality code:

## When to Use This Skill

- After writing or modifying code
- When the user requests a review or feedback
- Before committing significant changes
- As a proactive quality check during development

## Review Process

1. **Analyze**: Review the staged changes or specific files provided. Ensure that the changes are scoped properly and represent minimal changes required to address the issue.
2. **Context**: Examine the current git status, recent commits, and the modified files.
3. **Checklist**: Use the following criteria to evaluate the code:

### Review Checklist

#### Critical (Must Fix)
- Security vulnerabilities (exposed secrets, injection risks)
- Logic errors that cause incorrect behavior
- Missing error handling for critical paths
- Race conditions or data corruption risks

#### Warnings (Should Fix)
- Code duplication that harms maintainability
- Missing input validation
- Poor error messages
- Performance issues in hot paths
- Missing or inadequate tests

#### Suggestions (Consider)
- Naming improvements for clarity
- Simplification opportunities
- Better abstractions
- Documentation gaps

## Feedback Organization

Provide feedback organized by priority:

### Output Format

```markdown
## Code Review Summary

**Files Reviewed:** [list files]
**Overall Assessment:** [Good/Needs Work/Critical Issues]

### Critical Issues
- [file:line] Issue description → Fix suggestion

### Warnings
- [file:line] Issue description → Recommendation

### Suggestions
- [file:line] Improvement opportunity
```

If no issues are found, state: "Code review passed. No issues identified."