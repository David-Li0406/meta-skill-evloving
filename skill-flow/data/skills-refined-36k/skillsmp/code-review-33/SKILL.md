---
name: code-review
description: Code review workflow using GitHub CLI. Use when reviewing pull requests, checking PR diffs, adding review comments, or approving/requesting changes on PRs.
allowed-tools:
  - Bash(gh pr list:*)
  - Bash(gh pr view:*)
  - Bash(gh pr diff:*)
  - Bash(gh pr checks:*)
  - Bash(gh pr checkout:*)
  - Bash(gh issue list:*)
  - Bash(gh issue view:*)
  - Bash(gh run list:*)
  - Bash(gh run view:*)
  - Bash(gh api:*)
  - Read
  - Grep
  - Glob
---

# Code Review Skill

## Rules

### Read-Only Operations
This skill only allows read-only GitHub operations.
Write operations require explicit user instruction outside this skill.

For `gh api`: GET requests only. No `-X POST/PUT/PATCH/DELETE` or `-f`/`-F` flags.

### Citation Required
Every issue raised MUST reference official documentation with URL or doc name.
Do not raise issues without documentation support.

## Workflow

1. **Get PR overview** - `gh pr view <number>`
2. **Review diff** - `gh pr diff <number>`
3. **Impact analysis** - Search callers of modified functions
4. **Check CI** - `gh pr checks <number>`
5. **Output findings** - Use format below

For detailed commands: See [references/gh-commands.md](references/gh-commands.md)

## Impact Analysis (REQUIRED)

When functions/methods/interfaces are modified:

1. Identify modified functions from diff
2. Search all callers: `rg "functionName" --type <lang>`
3. Verify caller compatibility
4. Report breaking changes

Check for: signature changes, return type changes, renamed functions, modified APIs.

## Output Format

```
## Review Summary

### Issues Found

#### [File: path/to/file.ext, Line: XX]
**Issue**: [Description]
**Reference**: [Official documentation URL]
**Suggestion**: [How to fix]

### Impact Analysis
- [Affected callers and compatibility status]

### Recommendation
- [ ] Approve / [ ] Request Changes / [ ] Comment Only
```

## Checklist

- [ ] Changes align with purpose
- [ ] Logic correct, edge cases handled
- [ ] All callers of modified functions identified
- [ ] No breaking changes to public APIs
- [ ] Security: input validation, no hardcoded secrets
- [ ] Tests added/updated, CI passing
