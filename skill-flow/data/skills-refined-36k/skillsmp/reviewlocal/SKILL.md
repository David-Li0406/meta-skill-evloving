---
name: review:local
description: Local Code Review - analyzes code changes and provides structured feedback before commit
---

# Local Code Review

Performs a thorough code review of local changes before they are committed or pushed. Identifies potential issues, suggests improvements, and ensures code quality standards are met.

## When to use

Use this skill when the user needs to:
- Review changes before creating a commit
- Get feedback on code quality and potential issues
- Check for common mistakes and security concerns
- Validate code against best practices

## Instructions

### Step 1: Determine Review Scope

Check what the user wants to review. If arguments are provided, use them. Otherwise, auto-detect:

1. **Check for staged changes first:**
   ```bash
   git diff --cached --stat
   ```

2. **If no staged changes, check unstaged:**
   ```bash
   git diff --stat
   ```

3. **If nothing to review, check recent commits or ask user:**
   - Offer to review the last commit
   - Offer to compare current branch with main/master
   - Ask user to specify what to review

**Supported scopes:**
- `staged` - Review staged changes (default if available)
- `unstaged` - Review unstaged working directory changes
- `all` - Review all uncommitted changes
- `last` or `HEAD` - Review the last commit
- `branch` - Review all commits on current branch vs main
- `<file-path>` - Review specific file(s)
- `<commit-hash>` - Review specific commit

### Step 2: Gather Changes

Based on the determined scope, gather the diff:

```bash
# Staged changes
git diff --cached

# Unstaged changes
git diff

# All uncommitted
git diff HEAD

# Last commit
git show HEAD

# Branch diff
git diff main...HEAD
```

Also gather context:
- File types being modified
- Size of changes (lines added/removed)
- List of affected files

### Step 3: Analyze Code

Review the changes for the following categories:

| Category | What to check |
|----------|---------------|
| **Correctness** | Logic errors, edge cases, null handling, off-by-one errors |
| **Security** | Injection vulnerabilities, exposed secrets, unsafe operations |
| **Performance** | N+1 queries, unnecessary iterations, memory leaks |
| **Maintainability** | Code clarity, naming, duplication, complexity |
| **Best Practices** | Language idioms, framework conventions, project patterns |
| **Testing** | Missing tests, test coverage for new code |

For each issue found, note:
- Severity: 🔴 Critical, 🟠 Warning, 🟡 Suggestion
- Location: file path and line number
- Description: what the issue is
- Recommendation: how to fix it

### Step 4: Check Project Context

Before finalizing the review:
1. Look for existing patterns in the codebase
2. Check for project-specific conventions (linters, style guides)
3. Verify consistency with similar code in the project

### Step 5: Generate Review Report

Create a structured summary report:

```markdown
# Code Review Summary

**Scope:** [What was reviewed]
**Files:** [Number] files ([+lines added], [-lines removed])

---

## Overview

[1-2 sentence summary of the changes and overall assessment]

---

## 🔴 Critical Issues

> Issues that must be fixed before committing

### [Issue Title]
**File:** `path/to/file.ts:42`

[Description of the issue]

**Recommendation:**
```[language]
[Code suggestion]
```

---

## 🟠 Warnings

> Issues that should be addressed

- **[file:line]** — [Brief description]
- **[file:line]** — [Brief description]

---

## 🟡 Suggestions

> Optional improvements to consider

- [Suggestion 1]
- [Suggestion 2]

---

## ✅ What Looks Good

- [Positive observation 1]
- [Positive observation 2]

---

## Checklist Before Commit

- [ ] All critical issues resolved
- [ ] Tests added/updated for new functionality
- [ ] No debug code or console.logs left
- [ ] No hardcoded values that should be configurable
```

### Step 6: Handle Edge Cases

**No changes found:**
- Inform the user
- Suggest what they might want to review

**Very large diff (>500 lines):**
- Warn user about the size
- Offer to focus on specific files or categories
- Prioritize critical issues

**Binary files:**
- Note their presence but skip detailed review
- Warn if unexpected binary files are included

**Only deletions:**
- Verify nothing important is being removed
- Check for orphaned references

### Step 7: Offer Next Steps

After presenting the report, offer actions:

1. **Fix issues** — Help fix the identified problems
2. **Re-review** — Run the review again after changes
3. **Proceed anyway** — If issues are acceptable, continue to commit
4. **Explain** — Provide more details on any issue

## Review Guidelines

### Severity Levels

| Level | Criteria | Action |
|-------|----------|--------|
| 🔴 Critical | Bugs, security issues, data loss risks | Must fix |
| 🟠 Warning | Code smells, potential issues, missing tests | Should fix |
| 🟡 Suggestion | Style improvements, minor optimizations | Nice to have |

### Constructive Feedback

1. **Be specific** — Point to exact lines and provide examples
2. **Explain why** — Don't just say "bad", explain the consequence
3. **Suggest solutions** — Provide actionable recommendations
4. **Acknowledge good code** — Highlight what's done well
5. **Prioritize** — Focus on what matters most

### Security Checklist

Always check for:
- Hardcoded secrets, API keys, passwords
- SQL/NoSQL injection vulnerabilities
- XSS vulnerabilities in user input handling
- Insecure deserialization
- Path traversal in file operations
- Exposed sensitive data in logs

## Arguments

- `<args>` - Optional scope specification
  - `staged` - Review staged changes
  - `unstaged` - Review working directory changes
  - `all` - Review all uncommitted changes
  - `last` - Review the last commit
  - `branch` - Review current branch vs main
  - `path/to/file` - Review specific file
  - `abc123` - Review specific commit

Examples:
- `review:local` - Auto-detect and review available changes
- `review:local staged` - Review only staged changes
- `review:local src/auth/` - Review changes in auth directory
- `review:local last` - Review the last commit
- `review:local branch` - Review all branch changes vs main
