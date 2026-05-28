---
name: push-personal
description: Use this skill when the user asks to push to personal repository, push to personal account, push personal repo, push with account switch, or push to javierg1975. Switches GitHub accounts (javierg1975), pushes changes, and switches back to NYU account.
user-invocable: true
allowed-tools: Bash(git:*), Bash(gh:*)
---

# Push to Personal Repository

Push committed changes to the personal `javierg1975/zodiac-planner` repository with automatic GitHub account switching.

## Prerequisites Check

1. Verify there are no uncommitted changes:
```bash
git status
```

If there are uncommitted changes, inform the user they need to commit first and stop.

## Push Workflow

2. Switch to personal GitHub account:
```bash
gh auth switch --user javierg1975
```

3. Push to remote develop branch:
```bash
git push origin develop
```

4. Switch back to work account:
```bash
gh auth switch --user Javier-Gonzalez_NYULH
```

5. Confirm success to the user with the push result.

## Error Handling

If the push fails for any reason, still attempt to switch back to the NYU account before reporting the error.

## Session Information

Session ID: ${CLAUDE_SESSION_ID}
