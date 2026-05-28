---
name: code-review
description: Get quality code reviews from Claude Code - PR workflows, review prompts, checklists
version: 1.0.0
author: Claude Code SDK
tags: [review, pr, quality, feedback]
---

# Code Review with Claude Code

Get thorough, actionable code reviews from Claude Code for any codebase.

## Quick Reference

| Review Type | When to Use | Prompt Pattern |
|-------------|-------------|----------------|
| General | New features, refactors | "Review @file for issues" |
| Security | Auth, data handling | "Security review @file" |
| Performance | Hot paths, loops | "Performance review @file" |
| Style | Consistency, standards | "Style review against @.eslintrc" |
| Architecture | Design decisions | "ultrathink about @src/module/" |

## Review Request Patterns

### Basic Review

```
Review @src/api/users.ts for issues.

Focus on:
- Logic errors
- Edge cases
- Error handling
- Code clarity
```

### Targeted Review

```
Review @src/auth/login.ts specifically for:
- SQL injection vulnerabilities
- Password handling
- Session management

Ignore styling issues.
```

### Comparative Review

```
Review this change:
@git:diff src/api/

Compare against:
- Our patterns in @src/api/orders.ts
- Best practices for REST APIs
```

## Review Types

### Security Review

```
Security review @src/auth/ @src/api/

Check for:
- Input validation
- SQL injection
- XSS vulnerabilities
- Auth/authz issues
- Secrets exposure
- CSRF protection

Rate each finding: critical/high/medium/low
```

### Performance Review

```
Performance review @src/services/search.ts

Analyze:
- Time complexity
- Memory usage
- Database queries (N+1?)
- Caching opportunities
- Async patterns
```

### Style Review

```
Style review @src/components/ against:
@.eslintrc.js
@.prettierrc

Report:
- Naming conventions
- File organization
- Import ordering
- Component patterns
```

### Architecture Review

```
ultrathink about the architecture of @src/orders/

Evaluate:
- Separation of concerns
- Dependency direction
- Coupling/cohesion
- Testability
- Extensibility
```

## Getting Better Reviews

### Provide Context

Include related files and history:

```
Review @src/api/payments.ts

Context:
- @src/types/payment.ts (types)
- @src/services/stripe.ts (integration)
- This replaces the old PayPal flow
- Must handle refunds within 30 days
```

### Specify Your Concerns

```
Review @src/auth/session.ts

I'm specifically worried about:
1. Race conditions in token refresh
2. Session fixation attacks
3. Memory leaks from unclosed sessions

Less concerned about:
- Code style (will run linter)
- Test coverage (separate pass)
```

### Request Actionable Feedback

```
Review @src/utils/parser.ts

For each issue found:
1. Explain the problem
2. Show the problematic code
3. Provide a fix
4. Rate severity
```

## Review Output Format

Request structured output for complex reviews:

```
Review @src/api/ and format findings as:

## Critical
- [Issue]: [Location]: [Description]

## Improvements
- [Suggestion]: [Location]: [Benefit]

## Questions
- [Question]: [Context]

## Positive
- What's done well
```

## Iterative Reviews

### Multi-Pass Approach

```
# Pass 1: High-level
Review @src/orders/ for architectural issues.
Don't look at implementation details yet.

# Pass 2: After addressing Pass 1
Now review the implementation in @src/orders/service.ts
Focus on business logic correctness.

# Pass 3: Final
Security and performance review of @src/orders/
```

### Review and Fix

```
Review @src/api/upload.ts for security issues.

For each critical issue:
1. Explain it
2. Fix it immediately
3. Add a test case
```

## Thinking Keywords for Reviews

| Keyword | Review Type | Example |
|---------|-------------|---------|
| `think` | General review | "think about issues in @file" |
| `think harder` | Edge cases | "think harder about edge cases" |
| `ultrathink` | Security/arch | "ultrathink about security of @auth/" |
| `megathink` | Critical systems | "megathink about @payment/ risks" |

## Review Checklists

Quick prompts for standard checks:

```
Run through @CHECKLIST.md for @src/api/users.ts
```

See [CHECKLIST.md](./CHECKLIST.md) for complete checklists.

## PR-Specific Reviews

```
Review PR #123

gh pr diff 123

Focus on:
- Does it match the PR description?
- Are tests adequate?
- Any breaking changes?
- Documentation updated?
```

See [PR-WORKFLOWS.md](./PR-WORKFLOWS.md) for complete PR review workflows.

## Review Comment Templates

### Issue Found

```
Issue: [Brief description]
Location: [file:line]
Severity: [critical|high|medium|low]

Problem:
[Explanation of what's wrong]

Current:
[code snippet]

Suggested:
[fixed code snippet]

Why: [Reason this matters]
```

### Suggestion

```
Suggestion: [Brief description]
Location: [file:line]
Impact: [performance|readability|maintainability]

Current approach:
[what code does now]

Alternative:
[better approach]

Benefit: [Why this is better]
```

## Common Review Prompts

### API Endpoint

```
Review @src/api/users.ts for:
- Input validation completeness
- Error response consistency
- Auth/authz checks
- Rate limiting consideration
- Logging adequacy
```

### React Component

```
Review @src/components/UserCard.tsx for:
- Props validation
- Render optimization
- Hook usage
- Accessibility
- Error boundaries
```

### Database Code

```
Review @src/repositories/user.ts for:
- SQL injection (even with ORM)
- N+1 query patterns
- Transaction handling
- Index usage
- Connection management
```

### Utility Functions

```
Review @src/utils/validation.ts for:
- Edge case handling
- Type safety
- Error messages clarity
- Reusability
- Test coverage gaps
```

## Reference Files

| File | Contents |
|------|----------|
| [REVIEW-PROMPTS.md](./REVIEW-PROMPTS.md) | Detailed prompts by review type |
| [PR-WORKFLOWS.md](./PR-WORKFLOWS.md) | Pull request review workflows |
| [CHECKLIST.md](./CHECKLIST.md) | Code review checklists |

## Validation

After a review, verify quality:

- [ ] All critical issues addressed
- [ ] Fixes don't introduce new issues
- [ ] Tests added for bugs found
- [ ] Review comments resolved
- [ ] Code compiles and tests pass
