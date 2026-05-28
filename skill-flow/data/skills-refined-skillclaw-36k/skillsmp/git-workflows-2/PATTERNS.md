# Git Patterns

Advanced git workflows including branching strategies, hotfixes, releases, conflict resolution, and recovery patterns.

## Branching Strategies

### Feature Branch Workflow

Standard workflow for most teams:

```
main
  └── feature/user-auth
        ├── commit 1
        ├── commit 2
        └── commit 3 → PR → merge to main
```

**Steps:**

```bash
# 1. Create feature branch from main
git checkout main
git pull origin main
git checkout -b feature/my-feature

# 2. Work on feature
# ... make changes ...
git add <files>
git commit -m "feat: implement feature"

# 3. Push and create PR
git push -u origin feature/my-feature
gh pr create --title "feat: my feature" --body "..."

# 4. After approval, merge
gh pr merge --squash --delete-branch
```

### Trunk-Based Development

All work happens on main/trunk with short-lived branches:

```
main ──●──●──●──●──●──●──●──
         ↑     ↑     ↑
      feat  feat  fix
      (1d) (2d)  (1d)
```

**Rules:**
- Branches live < 1-2 days
- Feature flags for incomplete work
- Frequent small merges
- Main always deployable

**Steps:**

```bash
# 1. Create short-lived branch
git checkout main && git pull
git checkout -b quick-fix

# 2. Make minimal change
# ... one focused change ...
git commit -m "fix: quick fix for issue"

# 3. Push and merge quickly
git push -u origin quick-fix
gh pr create --title "fix: quick fix" --body "..."
gh pr merge --rebase --delete-branch  # After quick review
```

### GitFlow

Structured workflow with multiple branch types:

```
main ─────────────●─────────────●────
                  ↑             ↑
release/1.0 ──────┤   release/1.1 ──
                  ↑             ↑
develop ──●──●──●─┴──●──●──●──●─┴──●──
            ↑          ↑
         feature    feature
```

**Branches:**

| Branch | Purpose | Merges To |
|--------|---------|-----------|
| `main` | Production releases | - |
| `develop` | Integration branch | `main` via release |
| `feature/*` | New features | `develop` |
| `release/*` | Release preparation | `main` and `develop` |
| `hotfix/*` | Production fixes | `main` and `develop` |

**Feature Branch:**

```bash
git checkout develop
git checkout -b feature/new-thing

# ... work ...

git push -u origin feature/new-thing
gh pr create --base develop --title "feat: new thing"
```

**Release Branch:**

```bash
git checkout develop
git checkout -b release/1.2.0

# ... version bumps, final fixes ...

gh pr create --base main --title "Release 1.2.0"
# After merge to main, also merge to develop
```

## Hotfix Procedures

### Standard Hotfix

For urgent production fixes:

```bash
# 1. Create hotfix branch from main
git checkout main
git pull origin main
git checkout -b hotfix/critical-bug

# 2. Make minimal fix
# ... only the fix, nothing else ...
git add <files>
git commit -m "$(cat <<'EOF'
fix(critical): resolve production crash

Emergency fix for null pointer in payment processing.
Root cause: missing validation on optional field.

Fixes #999
EOF
)"

# 3. Push and create PR
git push -u origin hotfix/critical-bug
gh pr create --title "hotfix: critical production fix" --body "$(cat <<'EOF'
## Summary
Emergency fix for production crash in payment flow.

## Root cause
Missing null check on optional user field.

## Test plan
- [ ] Verify payment flow works
- [ ] Check no regression in related flows
- [ ] Monitor error rates after deploy

## Rollback plan
Revert this commit if issues arise.
EOF
)"

# 4. Get expedited review and merge
gh pr merge --merge  # Preserve commit for easy revert
```

### Hotfix with Cherry-Pick

When the fix needs to go to multiple branches:

```bash
# 1. Make fix on main
git checkout main
git checkout -b hotfix/fix
# ... make fix ...
git commit -m "fix: critical issue"
git push -u origin hotfix/fix
gh pr create --title "hotfix: ..." --body "..."
# Merge to main
gh pr merge --merge

# 2. Cherry-pick to release branch
git checkout release/1.0
git cherry-pick <commit-sha>
git push origin release/1.0

# 3. Cherry-pick to develop
git checkout develop
git cherry-pick <commit-sha>
git push origin develop
```

### Hotfix Checklist

- [ ] Branch from production (main)
- [ ] Minimal changes only
- [ ] Clear commit message with "fix" type
- [ ] Include rollback plan in PR
- [ ] Expedited review process
- [ ] Deploy immediately after merge
- [ ] Monitor after deployment
- [ ] Cherry-pick to other branches if needed

## Release Management

### Creating a Release

```bash
# 1. Create release branch (GitFlow) or tag (trunk-based)
git checkout main
git pull origin main

# Option A: Release branch
git checkout -b release/1.2.0

# Option B: Direct tag
git tag -a v1.2.0 -m "Release version 1.2.0"
git push origin v1.2.0

# 2. Create GitHub release
gh release create v1.2.0 --title "v1.2.0" --notes "$(cat <<'EOF'
## What's New
- Feature 1 description
- Feature 2 description

## Bug Fixes
- Fix 1 description
- Fix 2 description

## Breaking Changes
- None

## Upgrade Guide
No special steps required.
EOF
)"
```

### Semantic Versioning

Format: `MAJOR.MINOR.PATCH`

| Increment | When |
|-----------|------|
| MAJOR | Breaking changes |
| MINOR | New features (backward compatible) |
| PATCH | Bug fixes (backward compatible) |

Examples:
- `1.0.0` → `2.0.0`: Breaking API change
- `1.0.0` → `1.1.0`: New feature added
- `1.0.0` → `1.0.1`: Bug fix

### Version Bump Commit

```bash
git commit -m "$(cat <<'EOF'
chore(release): bump version to 1.2.0

Prepare release with:
- Version update in package.json
- CHANGELOG update
- Documentation refresh
EOF
)"
```

## Conflict Resolution

### Understanding Conflicts

Conflicts occur when:
- Same line modified in both branches
- File deleted in one branch, modified in other
- File renamed differently in both branches

### Conflict Markers

```
<<<<<<< HEAD
Your changes (current branch)
=======
Their changes (incoming branch)
>>>>>>> branch-name
```

### Resolution Workflow

```bash
# 1. Update your branch
git fetch origin
git merge origin/main  # or rebase

# 2. See conflict status
git status              # Shows conflicting files

# 3. Open conflicting files
# Look for <<<<<<< markers
# Decide what to keep

# 4. Edit to resolve
# Remove all conflict markers
# Keep correct code

# 5. Mark as resolved
git add <resolved-files>

# 6. Complete merge
git commit -m "Merge main into feature, resolve conflicts"
# OR for rebase
git rebase --continue
```

### Conflict Resolution Strategies

**Keep Ours (current branch):**
```bash
git checkout --ours <file>
git add <file>
```

**Keep Theirs (incoming branch):**
```bash
git checkout --theirs <file>
git add <file>
```

**Manual Merge:**
Edit file to combine both changes appropriately.

**Use Merge Tool:**
```bash
git mergetool            # Opens configured tool
```

### Abort Merge/Rebase

If resolution gets too complex:
```bash
git merge --abort        # Abort merge
git rebase --abort       # Abort rebase
```

## Stash and Restore

### Basic Stash

```bash
# Save current changes
git stash

# List stashes
git stash list

# Apply most recent
git stash pop            # Apply and remove
git stash apply          # Apply and keep

# Apply specific stash
git stash apply stash@{2}
```

### Named Stash

```bash
# Stash with message
git stash push -m "WIP: user authentication"

# Find by message
git stash list
# stash@{0}: On main: WIP: user authentication
```

### Stash Specific Files

```bash
# Stash only specific files
git stash push -m "partial work" src/feature.ts src/feature.test.ts

# Stash untracked files too
git stash push -u -m "include untracked"
```

### Stash Workflow Example

```bash
# 1. Working on feature, need to switch branches
git stash push -m "WIP: feature work"

# 2. Switch and do other work
git checkout main
# ... do urgent fix ...
git checkout feature-branch

# 3. Restore work
git stash pop
# Continue working
```

### Drop Stash

```bash
git stash drop           # Drop most recent
git stash drop stash@{2} # Drop specific
git stash clear          # Drop all stashes
```

## Recovery Patterns

### Undo Last Commit (Keep Changes)

```bash
git reset HEAD~1 --soft
# Changes are staged, commit is gone
```

### Undo Last Commit (Discard Changes)

```bash
git reset HEAD~1 --hard
# WARNING: Changes are lost
```

### Recover Deleted Branch

```bash
# Find the commit
git reflog
# Look for: HEAD@{n}: checkout: moving from branch-name

# Recreate branch
git checkout -b branch-name <commit-sha>
```

### Recover Dropped Stash

```bash
# Find lost stash commit
git fsck --no-reflog | grep commit

# Apply the found commit
git stash apply <commit-sha>
```

### Undo Pushed Commit

```bash
# Create reverting commit (safe)
git revert <commit-sha>
git push

# Never force push to shared branches!
```

### Fix Commit to Wrong Branch

```bash
# 1. Note the commit hash
git log -1  # Copy the SHA

# 2. Undo commit on wrong branch
git reset HEAD~1 --soft
git stash

# 3. Switch to correct branch
git checkout correct-branch
git stash pop
git commit -m "original message"
```

### Recover from Detached HEAD

```bash
# See where you are
git status  # "HEAD detached at..."

# Option 1: Create branch from here
git checkout -b recovery-branch

# Option 2: Return to branch
git checkout main
```

## Working with Remotes

### Add Remote

```bash
git remote add upstream https://github.com/original/repo.git
```

### Sync Fork with Upstream

```bash
# Fetch upstream changes
git fetch upstream

# Merge to local main
git checkout main
git merge upstream/main

# Push to fork
git push origin main
```

### Track Remote Branch

```bash
git checkout --track origin/feature-branch
# OR
git checkout -b feature-branch origin/feature-branch
```

### Push to Different Remote

```bash
git push upstream feature-branch
```

## Git Aliases (Useful Shortcuts)

```bash
# Add useful aliases
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
git config --global alias.last 'log -1 HEAD'
git config --global alias.unstage 'reset HEAD --'
git config --global alias.visual '!gitk'
```

## Safety Commands Reference

### Safe Commands (Always OK)

```bash
git status
git diff
git log
git show
git branch -a
git remote -v
git stash list
git fetch
```

### Careful Commands (Review First)

```bash
git add .           # Might add unwanted files
git commit          # Verify message/content
git push            # Verify branch/remote
git merge           # May cause conflicts
git rebase          # Rewrites history
git stash pop       # May cause conflicts
```

### Dangerous Commands (Avoid on Shared Branches)

```bash
git push --force    # Overwrites remote history
git reset --hard    # Loses uncommitted changes
git clean -fd       # Deletes untracked files
git rebase -i       # Interactive mode unsupported
```

## Decision Tree: Which Pattern to Use?

```
Need to commit changes?
├── Yes → See COMMITS.md
└── No
    ↓
Need to create PR?
├── Yes → See PULL-REQUESTS.md
└── No
    ↓
What's the situation?
├── Production bug → Hotfix procedure
├── New feature → Feature branch workflow
├── Multiple release versions → GitFlow
├── Fast iteration → Trunk-based development
├── Merge conflicts → Conflict resolution
├── Need to switch context → Stash workflow
├── Made a mistake → Recovery patterns
└── Syncing fork → Working with remotes
```
