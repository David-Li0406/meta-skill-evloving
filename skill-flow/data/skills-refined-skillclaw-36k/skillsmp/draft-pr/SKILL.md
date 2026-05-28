---
name: draft-pr
description: Commits staged changes using smart-commit workflow, publishes the branch to remote, and opens a draft pull request using repository PR templates. Use when you want to quickly create a draft PR from local changes.
---

# Draft PR

## Overview

This skill automates the complete workflow from local changes to draft pull request by:
1. Using smart-commit to commit staged changes (creates feature branch if on main/master)
2. Publishing the branch to remote
3. Opening a draft PR using repository PR templates

## Quick Start

Use this skill when you need to:
- Commit local changes and immediately create a draft PR
- Follow smart-commit best practices (auto-branching from main)
- Use existing PR templates from the repository
- Quickly share work-in-progress for early feedback

## Workflow

### 1. Smart Commit

First, follow the smart-commit skill to:
- Check if on main/master → create feature branch (`johnmog-<area>-<change>`)
- Commit staged changes with concise message (≤52 chars)
- Stay on current branch if not on main/master

See the smart-commit skill for detailed commit message guidelines.

### 2. Publish Branch

Push the current branch to remote:
```bash
git push -u origin <branch-name>
```

If branch already exists remotely:
```bash
git push
```

### 3. Find PR Template

Look for PR templates in common locations:
- `.github/pull_request_template.md`
- `.github/PULL_REQUEST_TEMPLATE.md`
- `.github/PULL_REQUEST_TEMPLATE/*.md` (multiple templates)
- `docs/pull_request_template.md`
- `PULL_REQUEST_TEMPLATE.md` (root)

If multiple templates exist, use the default or ask user which to use.

### 4. Create Draft PR

Use `gh` CLI to create draft PR:
```bash
gh pr create --draft --template <template-path>
```

If no template exists:
```bash
gh pr create --draft --title "<commit-message>" --body ""
```

The PR will:
- Use the branch name and commit message as context
- Be marked as draft (allows merging later without review requirements)
- Include template sections if template exists

## Examples

### Example 1: Create Draft PR from Main

**User Request:** "Draft PR"

**Current State:**
```bash
$ git branch --show-current
main

$ git status
Changes to be committed:
  modified:   src/auth/login.js
```

**Actions:**
1. Smart commit:
   - Create branch: `johnmog-auth-validation`
   - Commit: `add user authentication validation`
2. Publish: `git push -u origin johnmog-auth-validation`
3. Find template: `.github/pull_request_template.md` exists
4. Create PR: `gh pr create --draft --template .github/pull_request_template.md`

**Output:**
```
Created branch: johnmog-auth-validation
Committed: add user authentication validation
Published branch to remote
Created draft PR: https://github.com/owner/repo/pull/123
```

### Example 2: Draft PR from Existing Branch

**User Request:** "Create a draft PR"

**Current State:**
```bash
$ git branch --show-current
johnmog-cache-fix

$ git status
Changes to be committed:
  modified:   src/utils/cache.js
```

**Actions:**
1. Smart commit: `fix cache undefined access`
2. Publish: `git push -u origin johnmog-cache-fix`
3. No template found
4. Create PR: `gh pr create --draft --title "fix cache undefined access" --body ""`

**Output:**
```
Committed: fix cache undefined access
Published branch to remote
Created draft PR: https://github.com/owner/repo/pull/124
```

### Example 3: Multiple PR Templates

**User Request:** "Draft PR for bug fix"

**Template Selection:**
```
Found multiple PR templates:
1. .github/PULL_REQUEST_TEMPLATE/bug_fix.md
2. .github/PULL_REQUEST_TEMPLATE/feature.md
3. .github/PULL_REQUEST_TEMPLATE/docs.md

Which template? bug_fix
```

**Actions:**
1. Smart commit workflow
2. Publish branch
3. Create PR: `gh pr create --draft --template .github/PULL_REQUEST_TEMPLATE/bug_fix.md`

## Error Handling

**No staged changes:**
```
Error: No changes staged for commit.
Please stage changes with: git add <files>
```

**Branch already published:**
```
Branch already exists on remote. Pushing latest changes...
```

**PR already exists:**
```
Error: Pull request already exists for this branch.
View it at: https://github.com/owner/repo/pull/123
```

**Not authenticated with gh:**
```
Error: Not authenticated with GitHub CLI.
Please run: gh auth login
```

**No remote configured:**
```
Error: No remote 'origin' configured.
Please add remote: git remote add origin <url>
```

## Prerequisites

- Git repository with remote configured
- GitHub CLI (`gh`) installed and authenticated
- Staged changes ready to commit

## Best Practices

1. **Review before committing**: Check `git diff --cached`
2. **Keep commits atomic**: One logical change per commit
3. **Use draft status**: Mark incomplete work as draft
4. **Add description**: Fill out PR template sections after creation
5. **Link issues**: Reference related issues in PR body

## Integration with Smart Commit

This skill extends smart-commit by:
- Using same branch naming conventions
- Following same commit message guidelines
- Automatically handling main/master branching
- Adding publish and PR creation steps

## Related Skills

- **smart-commit**: Core commit workflow
- **code-reviewer**: Review changes before creating PR
