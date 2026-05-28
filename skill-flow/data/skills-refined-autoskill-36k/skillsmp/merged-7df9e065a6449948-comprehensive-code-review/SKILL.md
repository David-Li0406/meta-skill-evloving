---
name: comprehensive-code-review
description: Use this skill for thorough code reviews, including security, performance, maintainability, and compliance checks before merging code.
---

# Comprehensive Code Review

> Orchestrate a multi-agent review process for in-depth code analysis and actionable feedback.

## When to Use

- After implementation and before merging code
- When requested for bug hunting, regression detection, or alternative implementation perspectives

## Instructions

### Step 1: Determine Review Scope

Identify what to review:

```bash
# Option A: Recent changes
git diff HEAD~1

# Option B: Staged changes  
git diff --staged

# Option C: Specific commit range
git log --oneline -10  # then select range

# Option D: Current working state
git status
```

### Step 2: Get Files to Review

```bash
git diff --name-only main...HEAD
```

### Step 3: Spawn Review Sub-Agents

Deploy parallel sub-agents with focused tasks:

| Sub-Agent | Task |
|-----------|------|
| **Security** | Check for OWASP Top 10 vulnerabilities, secrets, SQL injection, XSS |
| **Dev** | Evaluate against KISS principle, structure, error handling |
| **QA** | Assess test coverage, quality, and edge cases |
| **Performance** | Analyze algorithms, memory usage, and bundle size |

**Prompt each sub-agent with:**
> "Perform a comprehensive code review of [scope]. Investigate compliance, coding standards, and validate any API/library usage against current documentation. Report findings as actionable items."

### Step 4: Collect and Synthesize

Aggregate sub-agent reports into:

1. **Critical issues** requiring immediate fix
2. **Warnings** for non-blocking issues
3. **Recommendations** for improvement
4. **Metrics** on coverage and performance

## Output Format

```markdown
# Code Review Report

## Files Reviewed
- `path/to/file1.ts`
- `path/to/file2.ts`

### ✅ Passed Checks
- [List of passed checks]

### ⚠️ Warnings
- [Non-blocking issues]

### ❌ Issues Found
- **[CRITICAL]** [Issue] at [file:line]
  - Fix: [recommendation]

### 📊 Metrics
- Coverage: X% (target: Y%)
- Files: N changed

## Action Items
- [ ] Fix: [critical item]
- [ ] Consider: [recommendation]
- [ ] Verify: [needs validation]
```

## Quick Checklist

**Security:**
- [ ] No hardcoded secrets
- [ ] Input validation
- [ ] Auth checks in place

**Quality:**
- [ ] KISS principle
- [ ] No duplication
- [ ] Error handling
- [ ] Follows conventions

**Testing:**
- [ ] Coverage ≥ target
- [ ] Critical paths tested
- [ ] Edge cases covered

**Performance:**
- [ ] No N+1 queries
- [ ] Efficient algorithms
- [ ] No memory leaks

## Critical (Block Merge)

- Hardcoded secrets
- SQL injection / XSS
- Coverage < target
- Breaking changes without migration

---

**Remember:** Review improves code quality. Be constructive.