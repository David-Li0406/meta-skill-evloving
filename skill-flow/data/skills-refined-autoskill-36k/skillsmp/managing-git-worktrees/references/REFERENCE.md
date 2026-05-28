# Git Worktree Command Reference

## Table of Contents
- [Command Reference](#command-reference)
- [Error Handling](#error-handling)
- [Monitoring and Maintenance](#monitoring-and-maintenance)

## Command Reference

### Creating Worktrees

**Create worktree from existing branch:**
```bash
git worktree add <path> <existing-branch>
```
Example:
```bash
git worktree add ../my-project-hotfix hotfix/metadata-bug
```

**Create worktree with new branch:**
```bash
git worktree add -b <new-branch> <path>
```
Example:
```bash
git worktree add -b feature/search ../my-project-search
```

**Create worktree with new branch from specific commit:**
```bash
git worktree add -b <new-branch> <path> <commit-sha>
```
Example:
```bash
git worktree add -b fix/rollback ../my-project-rollback abc1234
```

### Listing Worktrees

**List all worktrees:**
```bash
git worktree list
```

**List with porcelain format (for scripting):**
```bash
git worktree list --porcelain
```

### Removing Worktrees

**Remove a worktree:**
```bash
git worktree remove <path>
```

**Force remove (even with uncommitted changes):**
```bash
git worktree remove --force <path>
```

### Moving Worktrees

**Move a worktree to new location:**
```bash
git worktree move <old-path> <new-path>
```

### Maintenance

**Remove stale worktree references:**
```bash
git worktree prune
```

**Dry run to see what would be pruned:**
```bash
git worktree prune --dry-run
```

**Lock a worktree (prevent removal/pruning):**
```bash
git worktree lock <path>
```

**Unlock a worktree:**
```bash
git worktree unlock <path>
```

## Error Handling

### Error: "fatal: 'branch' is already checked out"

**Cause:** The branch is already checked out in another worktree.

**Diagnosis:**
```bash
git worktree list | grep <branch-name>
```

**Solutions:**

1. **Use a different branch name:**
```bash
git worktree add -b feature/search-v2 ../my-project-search-v2
```

2. **Remove existing worktree first:**
```bash
git worktree remove <existing-path>
git worktree add ../my-project-new <branch-name>
```

3. **Create from the same branch:**
```bash
# Create new branch from existing one
git worktree add -b feature/search-copy ../my-project-search feature/search
```

**Ask user which approach to take.**

### Error: "fatal: invalid reference"

**Cause:** The branch doesn't exist.

**Solution:** Use `-b` flag to create branch and worktree together:
```bash
git worktree add -b <new-branch> <path>
```

**Example:**
```bash
# This will fail if branch doesn't exist:
git worktree add ../my-project-test feature/nonexistent

# This will succeed:
git worktree add -b feature/new-feature ../my-project-test
```

### Error: Directory already exists

**Cause:** The target path is already occupied.

**Diagnosis:**
```bash
ls -la <path>
```

**Solutions:**

1. **Use a different path:**
```bash
git worktree add ../my-project-search-v2
```

2. **Remove existing directory (with user approval):**
```bash
rm -rf <path>
git worktree add -b <branch> <path>
```

3. **If it's a stale worktree:**
```bash
git worktree prune
git worktree add -b <branch> <path>
```

**Always get user approval before deleting directories.**

### Error: "fatal: '<path>' is already a registered worktree"

**Cause:** Git still has a reference to this worktree path.

**Solution:**
```bash
# Check for stale references
git worktree prune --dry-run

# Remove stale references
git worktree prune

# Try creating worktree again
git worktree add -b <branch> <path>
```

### Stale Worktree References

**Symptoms:**
- `git worktree list` shows worktrees that don't exist on disk
- Can't create new worktree at old path

**Diagnosis:**
```bash
git worktree prune --dry-run
```

**Solution:**
```bash
git worktree prune
```

**Prevention:**
- Always use `git worktree remove` instead of manually deleting directories
- Run `git worktree prune` periodically as maintenance

### Error: "fatal: '<path>' is not a working tree"

**Cause:** Trying to remove a path that isn't a worktree.

**Diagnosis:**
```bash
git worktree list
```

**Solution:** Verify the correct path and use `git worktree list` to find valid worktrees.

### Error: Uncommitted changes prevent removal

**Full error:**
```
fatal: '<path>' contains modified or untracked files, use --force to delete it
```

**Diagnosis:**
```bash
cd <path>
git status
```

**Solutions:**

1. **Commit the changes:**
```bash
cd <path>
git add .
git commit -m "Save work in progress"
cd ../main-worktree
git worktree remove <path>
```

2. **Stash the changes:**
```bash
cd <path>
git stash
cd ../main-worktree
git worktree remove <path>
```

3. **Force remove (with user confirmation):**
```bash
git worktree remove --force <path>
```

**Always ask user which approach to take, especially for --force.**

## Monitoring and Maintenance

### Check Status of All Worktrees

**List all worktrees with branch info:**
```bash
git worktree list
```

**Check for uncommitted changes across all worktrees:**
```bash
for wt in $(git worktree list --porcelain | grep worktree | cut -d' ' -f2); do
    echo "=== $wt ==="
    cd "$wt" && git status -s
done
```

**Check disk space used by worktrees:**
```bash
for wt in $(git worktree list --porcelain | grep worktree | cut -d' ' -f2); do
    echo "=== $wt ==="
    du -sh "$wt"
done
```

### Periodic Cleanup

**Monthly maintenance routine:**
```bash
# 1. Check for stale worktrees
git worktree prune --dry-run

# 2. Clean up stale references
git worktree prune

# 3. List merged branches (safe to delete)
git branch --merged main | grep -v "^\*" | grep -v "main"

# 4. Delete merged branches (with confirmation)
git branch --merged main | grep -v "^\*" | grep -v "main" | xargs -r git branch -d
```

**Check for orphaned node_modules:**
```bash
find .. -maxdepth 2 -name "node_modules" -type d -exec du -sh {} \;
```

### Verify Worktree Integrity

**Check Git database for issues:**
```bash
git fsck --full
```

**Verify all worktrees are accessible:**
```bash
git worktree list --porcelain | grep -A 3 "worktree" | while read line; do
    if [[ $line == worktree* ]]; then
        path=$(echo $line | cut -d' ' -f2)
        if [ -d "$path" ]; then
            echo "✓ $path exists"
        else
            echo "✗ $path missing (stale reference)"
        fi
    fi
done
```

### Recovering from Issues

**If worktree list shows wrong information:**
```bash
# Prune stale references
git worktree prune

# Verify
git worktree list
```

**If you accidentally deleted a worktree directory:**
```bash
# Prune the stale reference
git worktree prune

# Recreate if needed
git worktree add -b <branch> <path>
```

**If you lost commits from a removed worktree:**
```bash
# Check reflog
git reflog

# Find the lost commit
git log --all --oneline | grep "your commit message"

# Create new branch from lost commit
git branch recovery-branch <commit-sha>

# Create worktree from recovery branch
git worktree add ../my-project-recovery recovery-branch
```

## Advanced Commands

### Working with Remote Branches

**Create worktree from remote branch:**
```bash
# Fetch latest
git fetch origin

# Create worktree tracking remote branch
git worktree add ../my-project-feature origin/feature/search
```

**Create worktree for PR review:**
```bash
# Fetch PR
git fetch origin pull/123/head:pr-123

# Create worktree
git worktree add ../my-project-pr-123 pr-123
```

### Batch Operations

**Create multiple worktrees:**
```bash
# From a list of branches
for branch in feature/search feature/download fix/metadata; do
    dir_name="../my-project-${branch//\//-}"
    git worktree add -b "$branch" "$dir_name"
    cd "$dir_name" && npm install && cd -
done
```

**Remove all worktrees except main:**
```bash
git worktree list --porcelain | grep "^worktree" | cut -d' ' -f2 | \
while read wt; do
    if [[ "$wt" != "$(git rev-parse --show-toplevel)" ]]; then
        echo "Removing: $wt"
        git worktree remove "$wt"
    fi
done
```

## Best Practices for Error Prevention

1. **Always use `git worktree remove`** instead of manually deleting directories
2. **Run `git worktree prune`** regularly to clean stale references
3. **Use `git worktree list`** to verify before creating new worktrees
4. **Commit or stash changes** before removing worktrees
5. **Use descriptive branch names** to avoid confusion
6. **Document active worktrees** in team environments
7. **Clean up merged branches** promptly after merging

## Troubleshooting Checklist

When encountering issues:

- [ ] Run `git worktree list` to see current state
- [ ] Run `git worktree prune --dry-run` to check for stale references
- [ ] Check `git status` in the problematic worktree
- [ ] Verify directory exists: `ls -la <path>`
- [ ] Check for uncommitted changes: `git status -s`
- [ ] Run `git fsck` if database corruption is suspected
- [ ] Check disk space: `df -h`
- [ ] Review recent git operations: `git reflog`
