---
name: code-review
description: Perform a thorough code review
---

# Code Review

Perform a thorough code review of the provided code:

## Review Areas

### Correctness

- Does the code do what it's supposed to?
- Are edge cases handled?
- Are error conditions handled properly?

### Security

- Any injection vulnerabilities?
- Proper input validation?
- Sensitive data exposure?
- Authentication/authorization correct?

### Performance

- Any obvious inefficiencies?
- N+1 queries?
- Unnecessary computations?
- Memory concerns?

### Maintainability

- Is the code readable?
- Are functions focused (single responsibility)?
- Are names descriptive?
- Is complex logic documented?

### Testing

- Are there tests?
- Are edge cases covered?
- Are tests meaningful?

## Output Format

Provide feedback as:

**Critical Issues** (must fix)

- Issue, location, and recommended fix

**Suggestions** (should consider)

- Improvement and rationale

**Nits** (optional/minor)

- Small improvements

**What's Good**

- Highlight positive aspects

Be constructive and explain the "why" behind each suggestion.
