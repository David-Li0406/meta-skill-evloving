# Git Workflow Patterns

| Field | Value |
|-------|-------|
| **Created** | 2026-01-14 |
| **Sources** | retrospectives (2026-01-09, 2026-01-14) |
| **Tags** | `git` `workflow` `branch` `stash` |

---

## Key Insight

> Always stash uncommitted changes before switching branches, verify changes before commit, and use `-u` flag when pushing new branches.

---

## The Problem

| Attempt | Result |
|---------|--------|
| `git checkout` with uncommitted changes | Changes lost or conflicts |
| `git commit` without checking | Empty commits or wrong files |
| `git push` without `-u` | No upstream tracking |
| Fast-forward merge on diverged branches | Merge fails |

---

## The Solution

### Pattern: Safe Branch Switch

```bash
# 1. Stash current changes with descriptive name
git stash push -m "wip-feature-x" -- path/to/files/

# 2. Switch branch
git checkout main
git pull origin main

# 3. Create new branch
git checkout -b feature/new-feature

# 4. Pop stash when ready
git stash pop
```

### Pattern: Safe Commit Flow

```bash
# 1. Check what will be committed
git status --short
git diff --cached

# 2. Verify there are changes to commit
if git diff --cached --quiet; then
  echo "No changes to commit"
  exit 0
fi

# 3. Commit with descriptive message
git commit -m "feat: description"

# 4. Verify commit was created
git log -1 --oneline
```

### Pattern: Push New Branch

```bash
# Always use -u for new branches
BRANCH=$(git branch --show-current)
git push -u origin "$BRANCH"

# This sets upstream tracking, enabling:
# - `git pull` without arguments
# - `git push` without arguments
# - PR creation knows the remote branch
```

### Pattern: Handle Diverged Branches

```bash
# When local and remote have diverged
git fetch origin

# Option 1: Reset to remote (discard local)
git reset --hard origin/main

# Option 2: Rebase local on remote
git rebase origin/main

# Option 3: Merge (creates merge commit)
git merge origin/main
```

### Pattern: Protected Branch Workflow

```bash
# Can't push directly to main? Create docs/feature branch

# 1. Stash changes
git stash push -m "docs-changes" -- docs/

# 2. Update main
git checkout main
git pull origin main

# 3. Create branch
git checkout -b docs/update-xyz

# 4. Pop stash
git stash pop

# 5. Commit and push
git add docs/
git commit -m "docs: update xyz"
git push -u origin docs/update-xyz

# 6. Create PR
gh pr create --base main --title "docs: update xyz"
```

**Why this works:**
- Stash prevents losing uncommitted work
- `-u` flag ensures proper upstream tracking
- Checking for changes prevents empty commits
- Fetch before reset ensures latest remote state

---

## Anti-Patterns

| Don't Do This | Do This Instead |
|---------------|-----------------|
| `git checkout` without stashing | `git stash push` first |
| `git push` new branch without `-u` | `git push -u origin branch` |
| `git commit` without checking | Check `git diff --cached` first |
| `git push --force` to shared branches | Use `--force-with-lease` or avoid |
| `git reset --hard` without fetch | `git fetch` then `reset` |

---

## When to Apply

### Use Stash
- Before switching branches with uncommitted work
- Before pulling when you have local changes
- When you need to temporarily save work

### Use `-u` Flag
- First push of any new branch
- After creating branch from stash workflow
- Ensures PR creation works correctly

### Use Reset
- Sync local with remote after PR merge
- Discard experimental local changes
- After diverged branch scenario

---

## Quick Reference

| Command | Use When |
|---------|----------|
| `git stash push -m "name" -- path/` | Save specific files |
| `git stash pop` | Restore most recent stash |
| `git push -u origin branch` | First push of branch |
| `git diff --cached --quiet` | Check for staged changes |
| `git reset --hard origin/main` | Sync to remote |
| `git fetch origin` | Get remote updates without merge |

---

## Related

### Source Retrospectives
- `docs/retrospective/2026-01/retrospective_2026-01-09_211600.md`
- `docs/retrospective/2026-01/retrospective_2026-01-14_032400.md`

### Code References
- `assets/commands/td.md` - Branch handling in /td command
- `assets/commands/pr.md` - PR creation workflow
