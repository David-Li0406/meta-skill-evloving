---
name: pr-workflow
description: "Use when creating PRs, managing stacked PRs, or completing feature branches."
---

# PR Workflow

**Goal:** Clean PRs that are easy to review and merge.

## Workflow

```
PREPARE -> Verify tests, clean commits
PUSH    -> git push -u origin branch
CREATE  -> gh pr create with description
RESPOND -> Address review feedback
MERGE   -> gh pr merge --squash
CLEANUP -> Delete branch, pull main
```

## Create PR

```bash
# Prepare
npm test && npm run build && git status

# Push and create
git push -u origin feature/auth
gh pr create --title "Add authentication" --body "$(cat <<'EOF'
## Summary
- Add login/logout endpoints
- Implement JWT handling

## Test Plan
- [ ] Login with valid credentials
- [ ] Protected routes require token
EOF
)"
```

## Respond to Review

| Severity | Action |
|----------|--------|
| Critical | Fix immediately |
| Important | Fix before approval |
| Minor | Fix or discuss |

## Merge and Cleanup

```bash
gh pr merge --squash
git checkout main && git pull
git branch -d feature/auth
```

## Stacked PRs

```bash
# PR 1: Base
git checkout -b feature/auth-db && gh pr create --base main

# PR 2: Depends on PR 1
git checkout -b feature/auth-api && gh pr create --base feature/auth-db

# Merge bottom-up, rebase each after merge
```

## Decision Criteria

| Situation | Action |
|-----------|--------|
| Tests failing | Don't create. Fix first. |
| Large change | Split into stacked PRs |
| Approved + CI green | Merge immediately |

**Pairs with:** code-review, commit-discipline, verification
