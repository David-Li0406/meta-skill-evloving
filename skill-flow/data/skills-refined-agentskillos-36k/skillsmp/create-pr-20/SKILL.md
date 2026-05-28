---
name: create-pr
description: Create a pull request from current git changes with auto-generated title and description
---

# Create PR

Create a pull request from current git changes with an auto-generated title and description.

## Workflow

### 1. Check Current State

```bash
git status --short
git branch --show-current
```

Verify:
- There are changes to commit (staged or unstaged)
- Not on main/master branch (create feature branch if needed)

### 2. If on main/master, Create Feature Branch

```bash
git diff --name-only HEAD
```

Generate a descriptive branch name from the changes (e.g., `feat/add-user-auth`, `fix/null-pointer-error`).

```bash
git checkout -b <branch-name>
```

### 3. Stage All Changes

```bash
git add -A
```

### 4. Analyze Changes for Commit Message

```bash
git diff --cached --stat
git diff --cached
```

Generate a conventional commit message:
- Type: `feat`, `fix`, `refactor`, `docs`, `style`, `test`, `chore`
- Scope: affected component/area (optional)
- Subject: imperative, lowercase, no period
- Body: what and why (not how)

### 5. Commit Changes

```bash
git commit -m "<type>(<scope>): <subject>

<body>"
```

### 6. Push Branch to Origin

```bash
git push -u origin HEAD
```

### 7. Generate PR Title and Description

Analyze the commits on this branch vs main:
```bash
git log main..HEAD --oneline
git diff main..HEAD --stat
```

**PR Title**: Clear, concise summary (use conventional commit style if single commit)

**PR Description** template:
```markdown
## Summary
<1-2 sentence overview of changes>

## Changes
- <bullet point per logical change>

## Testing
- <how changes were tested, or "Needs testing">

## Related Issues
- <link to issues if mentioned in commits, or "N/A">
```

### 8. Create the PR

```bash
gh pr create --title "<title>" --body "<description>"
```

Or for draft PR:
```bash
gh pr create --title "<title>" --body "<description>" --draft
```

### 9. Report Result

```
✅ PR created successfully

Branch: <branch-name>
PR: <pr-url>
Title: <title>

Commits: X
Files changed: Y
```

## Options

- "draft" → create as draft PR
- branch name → use specified branch name
- PR title → use as PR title instead of auto-generating

## Notes

- Always run build/lint checks before creating PR if commands are available
- If there are uncommitted changes AND existing commits, commit the changes first
- Never force push or modify history on shared branches
- If PR already exists for this branch, report the existing PR URL instead
