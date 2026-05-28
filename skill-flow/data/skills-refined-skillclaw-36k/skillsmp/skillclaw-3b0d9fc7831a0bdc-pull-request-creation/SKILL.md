---
name: pull-request-creation
description: Use this skill when you need to create a pull request with a standardized format and quality checks.
---

# Skill body

## Overview

This skill provides a comprehensive workflow for creating pull requests (PRs) with consistent formatting and configurable quality checks. It is designed to ensure that every PR includes complete context for reviewers and adheres to best practices.

## Workflow Steps

### 1. Verify Prerequisites

Ensure the following conditions are met before creating a PR:

| Check | Required |
|-------|----------|
| Not on main/master | ✅ |
| Branch pushed to origin | ✅ |
| Has commits since main | ✅ |

### 2. Identify Target Branch

Determine the target branch for the PR. You can either prompt the user or detect the default branch:

```bash
# Method 1: Ask user
read -p "Enter target branch (main/develop/staging/etc.): " TARGET_BRANCH

# Method 2: Detect default
if [ -z "$TARGET_BRANCH" ]; then
  TARGET_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD | sed 's@^refs/remotes/origin/@@')
fi
```

### 3. Draft PR Title

**Format:** `type(scope): brief description`

Use the suggested type from context, or override based on commits:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `refactor`: Code restructuring

### 4. Draft PR Description

Use the following template for the PR description:

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

### 5. Run Quality Checks

Execute any configured quality checks (linting, building, testing) before creating the PR.

### 6. Create PR

Use the following command to create the PR:

```bash
gh pr create --title "type(scope): desc" --body "$(cat <<'EOF'
[body content]
EOF
)"
```

### 7. Report Result

After creating the PR, report the result:

```markdown
## ✅ Pull Request Created

**PR:** #XXX - [Title]
**URL:** https://github.com/owner/repo/pull/XXX
**Branch:** feature → main

CI checks will run automatically.
```

## Safety Rules

### NEVER:
- Create PR from the main branch
- Create PR without commits
- Skip the test plan section
- Push --force without permission

### ALWAYS:
- Verify the branch is pushed first
- Include a complete test plan
- Link related issues
- Follow conventional commit format

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

## Success Metrics

- ✅ All PRs follow a consistent format
- ✅ Reviewers have complete context for the changes