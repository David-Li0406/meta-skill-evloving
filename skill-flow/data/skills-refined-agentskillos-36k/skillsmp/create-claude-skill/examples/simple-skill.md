# Example: Simple Skill

This example shows a minimal but complete skill structure.

## Skill: Code Review

A skill that helps Claude perform thorough code reviews.

### Directory Structure

```
.claude/skills/code-review/
├── SKILL.md
└── checklists/
    ├── security.md
    └── performance.md
```

### SKILL.md

```markdown
---
name: Code Review
description: Perform thorough code reviews. Use when user says "review this code", "check my PR", or "code review".
---

# Code Review

You are an expert code reviewer. Your task is to provide thorough, actionable feedback on code quality, security, and performance.

## When to Use This Skill

Use this skill when:
- User asks to review code or a PR
- User wants feedback on implementation quality
- User asks about potential issues in their code

## Review Process

### Step 1: Understand Context

Before reviewing:
1. Identify the language and framework
2. Understand the purpose of the code
3. Note any constraints mentioned by the user

### Step 2: Review for Correctness

Check:
- Logic errors
- Edge cases
- Error handling
- Input validation

### Step 3: Review for Quality

Check:
- Code organization
- Naming clarity
- DRY violations
- Unnecessary complexity

### Step 4: Review for Security

For detailed security checklist:
Read: .claude/skills/code-review/checklists/security.md

### Step 5: Review for Performance

For detailed performance checklist:
Read: .claude/skills/code-review/checklists/performance.md

### Step 6: Provide Feedback

Format feedback as:
1. **Summary**: Overall assessment (1-2 sentences)
2. **Critical Issues**: Must-fix problems
3. **Suggestions**: Improvements to consider
4. **Positive Notes**: What's done well

## Quick Reference

| Issue Type | Priority |
|------------|----------|
| Security vulnerability | Critical |
| Logic error | Critical |
| Performance issue | High |
| Code style | Low |

## BEGIN

When reviewing code:
1. Read the code completely before commenting
2. Understand intent before critiquing
3. Provide specific, actionable feedback
4. Include code examples for suggestions
```

### checklists/security.md

```markdown
# Security Review Checklist

## Input Validation
- [ ] All user inputs are validated
- [ ] Input length limits are enforced
- [ ] Special characters are sanitized

## Authentication
- [ ] Authentication is required where needed
- [ ] Passwords are hashed (not stored in plain text)
- [ ] Session management is secure

## Authorization
- [ ] Access controls are enforced
- [ ] Users can only access their own data
- [ ] Admin functions are protected

## Data Protection
- [ ] Sensitive data is encrypted
- [ ] No secrets in code
- [ ] Logs don't expose sensitive info

## Common Vulnerabilities
- [ ] No SQL injection risks
- [ ] No XSS vulnerabilities
- [ ] No command injection
- [ ] CSRF protection in place
```

### checklists/performance.md

```markdown
# Performance Review Checklist

## Database
- [ ] Queries are efficient (no N+1)
- [ ] Indexes are used appropriately
- [ ] Unnecessary data isn't fetched

## Memory
- [ ] No memory leaks
- [ ] Large objects are cleaned up
- [ ] Caching is used where appropriate

## Network
- [ ] API calls are minimized
- [ ] Responses are appropriately sized
- [ ] Pagination is used for large datasets

## Complexity
- [ ] No unnecessary loops
- [ ] Algorithms are appropriate
- [ ] Early returns where possible
```

---

## Key Takeaways

1. **YAML frontmatter** defines when the skill activates
2. **Main SKILL.md** contains the core workflow
3. **Supporting files** provide detailed checklists loaded on demand
4. **Progressive disclosure** keeps context lean
5. **Clear instructions** tell Claude exactly what to do
