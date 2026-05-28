# Mercurial Branch Management

This guide covers Mercurial branch management operations, including named branches and bookmarks.

## Concept Comparison

| Feature | Named Branches | Bookmarks |
|---------|----------------|-----------|
| Persistence | Permanently exists in history | Movable, similar to Git branches |
| Naming | Arbitrary name | Arbitrary name |
| Visibility | Always visible in history | Visible only when referenced |
| Recommended Scenario | Long-term feature branches, release branches | Daily development, temporary branches |
| Close | Can be closed | Just delete it |

## Bookmarks (Recommended for Daily Development)

### Create and List Bookmarks

```bash
# Create bookmark
hg bookmark my-feature

# Force create/update bookmark at current location
hg bookmark -f my-feature

# List all bookmarks
hg bookmarks
```

### Switch and Update

```bash
# Switch to bookmark
hg update my-feature

# Update current bookmark
hg bookmarks -f

# Rename bookmark
hg bookmark -m old-name new-name

# Delete bookmark
hg bookmark -d my-feature
```

### Push and Pull Bookmarks

```bash
# Push specify bookmark
hg push -B my-feature

# Pull remote bookmark
hg pull -B my-feature

# Delete remote bookmark
hg bookmark -d my-feature
hg push -B my-feature
```

## Named Branches

### Create Branch

```bash
# Create and switch to new branch
hg branch feature-xyz

# Commit branch creation
hg commit -m "Create feature branch"
```

### List and Switch Branch

```bash
# List all branches
hg branches

# Switch to existing branch
hg update stable

# Update and discard local changes if any
hg update --clean stable
```

### Close Branch

```bash
# Switch to branch to be closed
hg update feature-xyz

# Close current branch
hg commit --close-branch -m "Close feature branch"
```

### Push Branch

> **Warning**: Always exercise caution with any push operation. Use `hg outgoing` to review the changes before pushing, and ensure you only push the intended changesets.

```bash
# Push current branch
hg push

# Push all branches
hg push --all-branches

# Push specific branch
hg push -b feature-xyz
```

## View Branch Information

```bash
# View current branch
hg branch

# View all branches
hg branches

# View all branch heads
hg heads

# View active heads
hg heads -t

# View specific branch
hg heads feature-xyz

# Graphically view branches
hg log -G
```

## Branch Strategies

### Feature Branch Workflow (Using Bookmarks)

```bash
# 1. Create feature branch from main/master
hg update master
hg bookmark feature/login

# 2. Develop feature
hg commit -m "Add login UI"
hg commit -m "Implement login logic"

# 3. Merge back to main branch
hg update master
hg merge feature/login
hg commit -m "Merge login feature"

# 4. Delete feature bookmark
hg bookmark -d feature/login
```

### Release Branch Workflow (Using Named Branches)

```bash
# 1. Create release branch
hg branch release-1.0
hg commit -m "Start 1.0 release"

# 2. Prepare for release
hg commit -m "Update version number"
hg commit -m "Fix release issues"

# 3. Close branch after release
hg commit --close-branch -m "Release 1.0"
```

### Maintenance Branch Workflow

```bash
# 1. Create maintenance bookmark from release branch
hg update release-1.0
hg bookmark maintain-1.0

# 2. Fix bug
hg commit -m "Fix critical bug"

# 3. Merge back to release branch
hg update release-1.0
hg merge maintain-1.0
hg commit -m "Merge maintenance fixes"
```

## Branch Management Best Practices

### When to Use Bookmarks

- Daily feature development
- Temporary experimental branches
- Personal development branches
- Branches needing frequent creation and deletion

### When to Use Named Branches

- Long-term feature branches
- Release version branches
- Branches needing permanent record in history
- Interoperability with Git repositories (using bookmarks)

### Branch Naming Conventions

```bash
# Feature branches
feature/user-auth
feature/new-dashboard

# Bugfix branches
fix/login-bug
hotfix/critical-security

# Release branches
release/1.0.0
release/1.1.0-beta

# Maintenance branches
maintain/1.0.x
maintain/2.x
```

## Advanced Branch Operations

### List Branch Relationships

```bash
# View branch inheritance relationship
hg log -G --template "{branch}: {node|short} {desc|firstline}\n"

# View history of specific branch
hg log -b feature-xyz

# View unmerged changesets
hg log -b feature-xyz -r "not ancestors('default')"
```

### Find Branch Origin

```bash
# Find divergence point of two branches
hg debugancestor feature-xyz default

# Find start point of bookmark
hg log -r "bookmark('my-feature')~1"
```

### Batch Operations

```bash
# Delete all inactive bookmarks
for b in `hg bookmarks -q`; do hg bookmark -d $b; done

# List all unclosed branches (default)
hg branches

# List all branches including closed
hg branches --closed
```
