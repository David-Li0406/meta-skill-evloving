---
name: pr-helper
description: Standardized Pull Request creation with consistent formatting. Use when user says "create pr" or "ready to merge".
version: 2.0.0
allowed-tools:
  - Read
  - Bash(git, gh)
  - Grep
plan_mode_required: false
trigger_keywords:
  - pull request
  - pr
  - create pr
  - open pr
  - ready to merge
---

# PR Helper

**Mission**: Clear Communication - every PR provides complete context for reviewers.

---

## Branch Context (Auto-Gathered)

```
!`bash .claude/skills/pr-helper/scripts/gather_info.sh 2>&1`
```

---

## PR Creation Workflow

Based on the context above:

### 1. Verify Prerequisites

| Check | Required |
|-------|----------|
| Not on main/master | ✅ |
| Branch pushed to origin | ✅ |
| Has commits since main | ✅ |

### 2. Draft PR Title

**Format:** `type(scope): brief description`

Use the suggested type from context, or override based on commits:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `refactor`: Code restructuring

### 3. Draft PR Description

Use template from [templates.md](reference/templates.md):

```markdown
## Summary
[2-3 sentences from commit messages]

### Key Changes
[From git diff --stat]

## Test Plan
- [ ] Tests pass
- [ ] Docs updated

https://claude.ai/code/session_ID
```

### 4. Create PR

```bash
gh pr create --title "type(scope): desc" --body "$(cat <<'EOF'
[body content]
EOF
)"
```

### 5. Report Result

```markdown
## ✅ Pull Request Created

**PR:** #XXX - [Title]
**URL:** https://github.com/owner/repo/pull/XXX
**Branch:** feature → main

CI checks will run automatically.
```

---

## Safety Rules

### NEVER:
- Create PR from main branch
- Create PR without commits
- Skip test plan section
- Push --force without permission

### ALWAYS:
- Verify branch is pushed first
- Include complete test plan
- Link related issues
- Follow conventional commit format

---

## Integration

```
Code complete → test-runner ✅ → security-checker ✅ → pr-helper ✅ → CI validates
```

**Prerequisite Skills:**
- test-runner: Verify tests pass
- security-checker: Scan for secrets
- doc-updater: Ensure docs current

---

## Quick Reference

```bash
# Create PR
gh pr create --title "..." --body "..."

# View PR
gh pr view $PR_NUMBER

# Check CI status
gh pr checks $PR_NUMBER --watch

# Merge when ready
gh pr merge $PR_NUMBER --squash --delete-branch
```

For full templates, see [templates.md](reference/templates.md)

---

## Success Metrics

- ✅ All PRs follow consistent format
- ✅ Reviewers have complete context
- ✅ PRs link to issues
- ✅ PR creation < 1 minute
