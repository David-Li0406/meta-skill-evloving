---
description: Automated code review before push
---

# Code Review

รัน automated code review ก่อน push code

## Usage

```
/review
```

## Instructions

### Step 1: Get Changed Files

```bash
echo "=== Changed Files ==="
git diff --name-only HEAD
git diff --cached --name-only

echo "=== Diff Stats ==="
git diff --stat HEAD
```

### Step 2: Run Code Review

ใช้ Task tool กับ subagent_type="general-purpose" เพื่อ review code:

```
Prompt:
"Review the code changes in this branch compared to main.

Check for:
1. **Code Quality**: Best practices, clean code, naming conventions
2. **Bugs**: Potential bugs, logic errors, edge cases
3. **Security**: SQL injection, XSS, command injection, secrets exposure
4. **Performance**: N+1 queries, memory leaks, inefficient algorithms
5. **Tests**: Test coverage, missing tests, test quality

For each finding, provide:
- Severity: CRITICAL / WARNING / INFO
- File and line number
- Description of the issue
- Suggested fix

Output format:
## Review Summary

### Critical Issues (must fix)
- [ ] Issue description

### Warnings (should fix)
- [ ] Issue description

### Info (nice to have)
- [ ] Issue description

### Overall Assessment
Pass / Fail with reason"
```

### Step 3: Report Results

**ถ้ามี CRITICAL issues:**

```markdown
## Code Review Failed ❌

### Critical Issues Found

[list of critical issues]

### Action Required
แก้ไข critical issues ก่อน push

### Commands
- แก้ไข code
- รัน `/review` อีกครั้ง
```

**ถ้าไม่มี CRITICAL issues:**

```markdown
## Code Review Passed ✅

### Summary
- Critical: 0
- Warnings: [count]
- Info: [count]

### Warnings (should fix)
[list if any]

### Ready to Push
Code is ready for `/td` or manual push
```

## Review Checklist

| Category | What to Check |
|----------|---------------|
| **Code Quality** | Naming, formatting, comments, DRY |
| **Bugs** | Null checks, error handling, edge cases |
| **Security** | Input validation, auth, secrets |
| **Performance** | Queries, loops, memory |
| **Tests** | Coverage, quality, assertions |

## Severity Levels

| Level | Description | Action |
|-------|-------------|--------|
| CRITICAL | Security vulnerability, data loss, crash | Must fix before push |
| WARNING | Bug risk, bad practice, missing test | Should fix |
| INFO | Style, optimization, suggestion | Nice to have |

## Integration with /td

`/td` command จะเรียก `/review` โดยอัตโนมัติใน Step 4

ถ้า review fail → `/td` จะหยุดและแจ้งให้แก้ไขก่อน

## Examples

### Example Output (Pass)

```markdown
## Code Review Passed ✅

### Summary
- Critical: 0
- Warnings: 2
- Info: 3

### Warnings
1. ⚠️ `internal/auth/service.go:45` - Missing error check on database call
2. ⚠️ `internal/user/handler.go:78` - No input validation for email

### Info
1. ℹ️ `internal/auth/service.go:12` - Consider using constants for magic numbers
2. ℹ️ `internal/user/model.go:5` - Add godoc comment for exported type
3. ℹ️ `tests/auth_test.go:30` - Consider adding edge case test

### Ready to Push ✅
```

### Example Output (Fail)

```markdown
## Code Review Failed ❌

### Critical Issues Found

1. 🔴 `internal/db/query.go:23` - SQL Injection vulnerability
   ```go
   query := "SELECT * FROM users WHERE id = " + userId
   ```
   **Fix:** Use parameterized queries
   ```go
   query := "SELECT * FROM users WHERE id = $1"
   db.Query(query, userId)
   ```

2. 🔴 `config/secrets.go:5` - Hardcoded API key exposed
   ```go
   const API_KEY = "sk-1234567890"
   ```
   **Fix:** Use environment variables

### Action Required
แก้ไข critical issues ก่อน push
```

## Related Commands

| Command | Purpose |
|---------|---------|
| `/td` | จบ session (เรียก review อัตโนมัติ) |
| `/commit` | Atomic commits |
| `/review` | Manual code review (คุณอยู่ที่นี่) |
