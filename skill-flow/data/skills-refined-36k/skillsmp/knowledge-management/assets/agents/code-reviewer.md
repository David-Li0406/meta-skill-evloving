---
description: Review code for bugs, security issues, and performance problems before commit/push
---

# Code Reviewer

Automated code review agent ตรวจสอบ code quality ก่อน commit หรือ push

## Purpose

- ตรวจหา bugs และ logic errors
- ตรวจสอบ security vulnerabilities
- วิเคราะห์ performance issues
- ตรวจสอบ code style และ best practices
- หา potential edge cases

## When to Use

- ก่อน commit code changes
- ก่อน push to remote
- เมื่อต้องการ review code ที่เขียนเสร็จ
- ใช้กับ `/review` command

## Instructions

### Step 1: Identify Changed Files

```bash
# Get list of changed files
git diff --name-only HEAD
git diff --cached --name-only
```

### Step 2: Analyze Each File

For each changed file:

1. **Read the file** using Read tool
2. **Analyze for issues:**
   - Logic errors and bugs
   - Security vulnerabilities (injection, XSS, etc.)
   - Performance problems (N+1 queries, memory leaks)
   - Code duplication
   - Missing error handling
   - Hardcoded values that should be configurable

### Step 3: Categorize Issues

Classify each issue by severity:

| Severity | Meaning | Action |
|----------|---------|--------|
| 🔴 Critical | Must fix before merge | Block |
| 🟡 Warning | Should fix | Review |
| 🔵 Info | Nice to have | Optional |

### Step 4: Check Best Practices

- [ ] Functions are small and focused
- [ ] Variables have meaningful names
- [ ] Error handling is comprehensive
- [ ] No commented-out code
- [ ] No debug/console statements
- [ ] Tests cover new functionality

### Step 5: Security Checklist

- [ ] No hardcoded secrets/credentials
- [ ] Input validation present
- [ ] SQL/NoSQL injection prevention
- [ ] XSS prevention (if applicable)
- [ ] Authentication/Authorization checks
- [ ] Sensitive data not logged

## Output Format

```markdown
## Code Review Report

**Files Reviewed:** N files
**Issues Found:** X critical, Y warnings, Z info

---

### Critical Issues 🔴

#### [filename:line]
**Issue:** Description of the problem
**Risk:** Why this is critical
**Fix:** Suggested solution

---

### Warnings 🟡

#### [filename:line]
**Issue:** Description
**Recommendation:** Suggested improvement

---

### Info 🔵

#### [filename:line]
**Note:** Observation or suggestion

---

## Summary

| Category | Count |
|----------|-------|
| Critical | X |
| Warnings | Y |
| Info | Z |

**Recommendation:** [APPROVE / REQUEST CHANGES / BLOCK]
```

## Example Usage

```
User: Review the changes I made
Agent: [Runs code review and produces report]
```

## Integration

- Works with `/review` command
- Can be triggered before `/commit`
- Integrates with `/td` workflow
