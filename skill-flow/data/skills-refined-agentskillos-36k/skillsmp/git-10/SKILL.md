---
name: git
description: Use for any git or GitHub operations including pull, sync, commit, push, PR, or when the user mentions git-related actions.
---

# Git & GitHub Workflows

This skill provides workflows for common git and GitHub operations.

## Quick Reference

| Action | Trigger phrases |
|--------|-----------------|
| Sync with remote | "pull", "sync", "update from main" |
| Commit changes | "commit", "save changes" |
| Create pull request | "PR it", "create a PR", "submit for review" |

## Workflow Composition

The workflows build on each other:

```
PR → Commit → Pull
```

- Creating a PR first commits changes
- Committing first pulls latest from main

---

## Pull Workflow

Pull latest changes and sync with remote.

### Scope

- **Single repo**: If the user mentions a specific repo or is clearly working in one repo, only pull that repo
- **All repos**: If the user says "all" or doesn't specify, pull all git repos in the workspace

### On `main` branch

- **Clean working directory**: `git pull origin main`
- **Has uncommitted changes**: `git stash && git pull origin main && git stash pop` — resolve any conflicts but do NOT push

### On a feature branch

1. Merge latest main: `git fetch origin && git merge origin/main`
2. Push the branch: `git push`

### Rules

- **Never force push**
- Summarize results for each repo at the end

---

## Commit Workflow

Commit changes to the current branch.

### Before Committing

1. **Pull latest** - Sync with main using the pull workflow above
2. **Run checks** - Run lint, format, and build/test as well as anything specific to this repository
3. **Fix issues** - Fix all warnings and errors from any of these commands

### Commit

1. Stage relevant changes
2. Write a clear, concise commit message focused on the "why"
3. Commit the changes

---

## PR Workflow

Create a PR against main with these changes.

### Before Creating PR

1. **Commit changes** - Apply the commit workflow above (which pulls latest and runs checks)
2. Create a new branch if needed

### Create the PR

1. Push to remote (with `-u` flag if new branch)
2. Create a PR using the `gh` CLI
3. Open a browser tab to the PR's `/files` page: `open <pr-url>/files`
4. Return the PR URL as a **clickable markdown link**: `[PR #N](url)`

### Output Format

Always format URLs as clickable markdown links in your response:
- PR link: `[PR #123](https://github.com/owner/repo/pull/123)`
- Any other URLs mentioned should also be linked

### Monitor CI

Use the `gh` CLI to monitor CI status. If CI fails:

1. Investigate the failure
2. Fix the issue
3. Push the fix
4. Repeat until CI passes
