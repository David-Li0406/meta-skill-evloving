---
name: review
description: Review uncommitted changes for issues, regressions, and optimization opportunities
---

# Code Review

Review all uncommitted changes in the current repository.

## Workflow

### 1. Get Uncommitted Changes

```bash
git diff HEAD
git diff --cached
git status --short
```

### 2. Analyze Each Changed File

For each modified file:
- Read the full file for context (not just the diff)
- Understand the purpose of the changes
- Check imports and dependencies affected

### 3. Check for Issues

Look for:
- Logic errors or bugs introduced
- Edge cases not handled
- Null/undefined access risks
- Error handling gaps
- Type safety issues
- Security vulnerabilities (exposed secrets, injection risks)

### 4. Check for Regressions

Identify:
- Breaking changes to existing APIs or contracts
- Removed functionality that may be needed
- Changed behavior that could affect callers
- Test coverage for modified code paths

### 5. Optimize Implementation

Find opportunities for:
- Redundant code that can be removed
- Duplicate logic that should be consolidated
- Unnecessary complexity that can be simplified
- Performance issues (N+1 queries, excessive loops, memory leaks)

### 6. Verify Code Quality

Run lint and build commands to check for errors.

### 7. Fix Simple Issues

If there are only a few issues (≤5) or they are straightforward:
- Apply the fixes directly without asking

For complex issues requiring design decisions: report and recommend

### 8. Report Findings

Group by severity:
- 🔴 Critical
- 🟠 Warning
- 🟡 Suggestion

Format:
```
✅ Fixed: [Category] filename:line
   Was: <description>
   Now: <what was changed>

🔴/🟠/🟡 [Category] filename:line
   Problem: <description>
   Fix: <recommendation>
```

End with summary: fixed count, remaining issues by severity, overall assessment.
