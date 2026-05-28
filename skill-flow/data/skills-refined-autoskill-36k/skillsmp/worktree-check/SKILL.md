---
name: worktree-check
description: "Use before git write operations (commit, push, merge, rebase) to verify you are in a git worktree. Guides worktree setup if missing. Keywords: worktree, isolation, git commit, git push."
---

# Worktree Check

Ensure git write operations happen inside an isolated worktree.

## When to Use
- Before `git commit`, `git push`, `git merge`, or `git rebase`
- When unsure if you are in a worktree

## Verify Worktree

```bash
# Worktree indicators
[ -f .git ] && echo "worktree"

git rev-parse --git-dir 2>/dev/null | grep -q "/worktrees/" && echo "worktree"
```

If neither check confirms a worktree, create one before proceeding.

## Create Worktree (Recommended)

```bash
# Prefer .worktrees/ if present
ls -d .worktrees worktrees 2>/dev/null

# Ensure gitignored
git check-ignore -q .worktrees || echo ".worktrees/" >> .gitignore

# Create and enter worktree
branch="feature/your-branch"
git worktree add .worktrees/your-branch -b "$branch"
cd .worktrees/your-branch
```

## Proceed Safely

Re-run the git command from inside the worktree once it is created.

## Notes
- If the user asks to proceed without a worktree, confirm explicitly before running git write operations.
