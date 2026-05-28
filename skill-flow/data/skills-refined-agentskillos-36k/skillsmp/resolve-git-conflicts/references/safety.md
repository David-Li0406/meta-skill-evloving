# Safety Guidelines

## Core Principles

1. **Ask before resolving ambiguous conflicts** - When both sides have meaningful changes, never auto-pick
2. **Show before applying** - Always display the proposed resolution before writing
3. **Confirm destructive actions** - Abort, reset, checkout operations need explicit approval
4. **Preserve user's work** - When in doubt, err on the side of keeping changes

## Before Starting Resolution

Check for uncommitted work that could be lost:
```bash
git stash list
git status --porcelain
```

## Abort Procedures

### Merge Abort
```bash
git merge --abort
```
Safe: Returns to pre-merge state. No data loss.

### Rebase Abort
```bash
git rebase --abort
```
Safe: Returns to original branch state before rebase started.

### Cherry-pick Abort
```bash
git cherry-pick --abort
```
Safe: Returns to pre-cherry-pick state.

### Stash Conflicts
After `git stash pop` with conflicts, the stash is NOT dropped.
```bash
# Discard attempted apply (CONFIRM FIRST - loses working tree changes)
git checkout .

# Stash is still available
git stash list
```

## Data Loss Warnings

**Always warn user before:**
- `git checkout .` - Discards all unstaged changes
- `git checkout --ours/--theirs` - Overwrites one side's changes
- `git reset --hard` - Discards all uncommitted changes
- `git clean -fd` - Deletes untracked files
- `git rebase --skip` - Drops a commit entirely

## Recovery Options

If user accidentally lost work:

```bash
# Find lost commits
git reflog

# Recover a commit
git cherry-pick <sha>

# Recover to a previous state
git reset --hard <sha>
```

## Rerere Considerations

If `rerere.enabled` is true, Git may auto-resolve conflicts based on previous resolutions.

```bash
# Check what rerere did
git rerere status
git diff
```

Even if rerere resolved, still:
1. Show the resolution to user
2. Confirm it's correct for this context
3. Previous resolution may not apply to current situation

## When to Suggest Abort

Suggest aborting when:
- User is confused about which changes to keep
- Conflict is too complex and user needs to rethink approach
- User realizes they should have done something differently first
- Too many conflicts suggest branches diverged too much (consider alternative strategy)

## Alternative Strategies

If conflicts are overwhelming, suggest:
- Abort and sync with target branch more frequently
- Break feature into smaller PRs
- Use `git rerere` to remember resolutions
- Consider merge vs rebase tradeoffs
