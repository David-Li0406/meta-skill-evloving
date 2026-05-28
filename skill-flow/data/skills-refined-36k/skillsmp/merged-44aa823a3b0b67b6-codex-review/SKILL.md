---
name: codex-review
description: Use this skill for comprehensive code reviews and analysis using OpenAI Codex CLI to identify bugs, security vulnerabilities, performance issues, and code quality problems.
---

# Codex Review Skill

This skill utilizes OpenAI Codex CLI to perform automated code reviews that identify issues and suggest improvements. It is a **read-only** analysis skill.

## When to Use

- User asks to "review" code
- User wants to check for bugs or issues
- User mentions "security", "performance", or "quality"
- Before committing code
- During pull request review
- User asks "what's wrong with this code?"

## Prerequisites

Verify Codex CLI is available:

```bash
codex --version  # Should display installed version
```

## Command

```bash
codex --sandbox=read-only exec "<request>"
```

## Parameters

| Parameter             | Description                         |
| --------------------- | ----------------------------------- |
| `--sandbox=read-only` | Read-only sandbox for safe analysis |
| `"<request>"`         | Request content                     |

## Execution Steps

1. Receive request from user
2. Identify scope of review (e.g., uncommitted changes, specific files, last commit, pull request, entire codebase)
3. Execute Codex with the command format above
4. Present findings organized by severity

## Example Reviews

### Review Uncommitted Changes

```bash
codex --sandbox=read-only exec "Review all uncommitted changes for:
- Bugs and logic errors
- Security vulnerabilities
- Performance issues
- Code quality problems
- Missing error handling
Do NOT modify code."
```

### Security-Focused Review

```bash
codex --sandbox=read-only exec "Security review of src/auth/*.ts:
- SQL injection vulnerabilities
- XSS vulnerabilities
- Authentication bypass
- Authorization flaws
- Secrets in code
- Input validation gaps
Provide severity level and fix suggestions. Do NOT modify code."
```

### Pre-Commit Review

```bash
codex --sandbox=read-only exec "Quick review of staged changes for:
- console.log statements
- Commented-out code
- Unused imports
- TODO comments
- Missing error handling
- Type errors
Exit with error if critical issues found. Do NOT modify code."
```

## Output Format

Structure review results:

````markdown
# Code Review: [Scope]

## Summary

- Files reviewed: 3
- Issues found: 5 (Critical: 1, Important: 2, Suggestions: 2)
- Estimated fix time: 2 hours

## 🔴 Critical Issues (Fix Immediately)

### src/auth/login.ts:45 - SQL Injection Vulnerability

**Severity:** Critical
**Category:** Security

**Problem:**
Direct string interpolation in SQL query allows SQL injection.

**Why it matters:**
Attacker can execute arbitrary SQL commands, steal data, or drop tables.

**How to fix:**
Use parameterized queries:

```typescript
// Before (vulnerable)
db.query(`SELECT * FROM users WHERE email = '${email}'`);

// After (safe)
db.query("SELECT * FROM users WHERE email = ?", [email]);
```
````

## Best Practices

✅ **DO:**
- Categorize by severity (Critical/Important/Suggestion)
- Include specific file paths and line numbers
- Explain WHY something is a problem
- Provide clear fix suggestions
- Note positive observations too

❌ **DON'T:**
- Make code modifications (use codex-exec for that)
- Skip verification of findings
- Report false positives without investigation
- Be purely negative without noting good practices

## Verification

After getting Codex's review:
1. Verify file paths and line numbers are correct
2. Check if issues are real (not false positives)
3. Assess severity appropriately
4. Add context from your knowledge of the code

## Error Handling

**If Codex not found:**
```
Codex CLI is not available. Ensure it's installed and in your PATH.
```

**If too many issues:**
- Focus on critical issues first
- Group related issues
- Break into multiple focused reviews

**If false positives:**
- Manually verify each issue
- Filter out non-issues
- Clarify with more specific review scope

## Integration Patterns

### Pre-Commit Hook
```bash
#!/bin/bash
# .git/hooks/pre-commit
codex --sandbox=read-only exec "Quick review of staged changes for critical issues" --yes
exit $?
```

### CI/CD Pipeline

```yaml
# GitHub Actions example
- name: Codex Review
  run: |
    codex --sandbox=read-only exec "Review PR changes for security and quality" > review.md
```

## Limitations

- Static analysis only (cannot run code)
- May generate false positives
- Cannot understand business logic
- Cannot test runtime behavior
- Limited by context window size

---

**Remember**: This skill is READ-ONLY. To fix issues found, use the `codex-exec` skill.