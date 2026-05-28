# Cleanup a Ticket Worktree

Removes a git worktree and cleans up associated branches.

## Input

User may provide:
- Ticket ID: `TDE-7379`
- Worktree name: `TDE-7379-optimize-lytics-loading`
- Nothing (show list of worktrees)

## Steps

### 1. List Worktrees (if no input)

```bash
cd ~/Vuori/cascade && git worktree list
```

Show worktrees under `~/Vuori/cascade-worktrees/` and ask which to clean up.

### 2. Find the Worktree

```bash
ls ~/Vuori/cascade-worktrees/ | grep TDE-7379
```

### 3. Check Branch Status

```bash
cd ~/Vuori/cascade-worktrees/<worktree-name>
git log --oneline -1  # Last commit
git status --short    # Uncommitted changes
```

### 4. Warn About Uncommitted Changes

If uncommitted changes exist:
- List changed files
- Ask if user wants to proceed (changes will be lost)
- Suggest committing or stashing first

### 5. Check if Merged

```bash
cd ~/Vuori/cascade
git fetch origin
git branch --merged origin/main | grep <branch-name>
```

Inform user if branch has unmerged changes.

### 6. Remove Worktree

```bash
cd ~/Vuori/cascade
git worktree remove ~/Vuori/cascade-worktrees/<worktree-name>
```

With uncommitted changes (after user confirms):
```bash
git worktree remove --force ~/Vuori/cascade-worktrees/<worktree-name>
```

### 7. Delete Local Branch

If merged, offer to delete:
```bash
git branch -d <branch-name>
```

If not merged but user wants to delete:
```bash
git branch -D <branch-name>
```

### 8. Provide Summary

```
Cleaned up TDE-7379:
- Removed worktree: ~/Vuori/cascade-worktrees/TDE-7379-optimize-lytics-loading
- Deleted branch: feat/TDE-7379-optimize-lytics-loading (was merged to main)

Remaining worktrees:
- TDE-7358-optimize-elevar-loading
- TDE-6053-optimize-product-info-provider
```
