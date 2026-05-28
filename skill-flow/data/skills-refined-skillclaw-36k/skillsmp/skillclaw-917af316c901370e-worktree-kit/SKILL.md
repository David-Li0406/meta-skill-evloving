---
name: worktree-kit
description: Use this skill to manage git worktrees, allowing for parallel feature work, isolated reviews, and maintaining a clean workspace.
---

# Worktree kit

Use the manager script for all worktree actions.

```bash
ROOT="$(git rev-parse --show-toplevel)"
PLUGIN_ROOT="$ROOT/.opencode/skill"
bash "$PLUGIN_ROOT/worktree-kit/scripts/worktree.sh" <command> [args]
```

Commands:
- `create <name> [base]`
- `list`
- `switch <name>` (prints path)
- `cleanup`
- `copy-env <name>`

Safety notes:
- `create` does not change the current branch.
- `cleanup` does not force-remove worktrees and does not delete branches; it deletes the worktree directory (including ignored files) and removal fails if the worktree is not clean.
- `.env*` files are copied with no overwrite (symlinks skipped).
- The script refuses to operate if `.worktrees/` or any worktree path component is a symlink.
- `copy-env` only targets registered worktrees.
- Fetch from `origin` is optional; local base refs are allowed.
- Fetch from `origin` only when the base looks like a branch.
- Worktrees are managed under `.worktrees/`.