# Mercurial Queues (MQ)

This guide covers the usage of the Mercurial MQ (Mercurial Queues) extension.

## Enable MQ Extension

Add to `~/.hgrc`:

```ini
[extensions]
mq =
```

## Basic Concepts

MQ uses a stack to manage patches:

```
Top
------------
Patch 3
------------
Patch 2
------------
Patch 1
------------
Bottom
```

- **Applied patches**: Patches that are applied (in the stack)
- **Unapplied patches**: Patches that are not applied (in the queue)
- **Popped**: Patches removed from the stack
- **Pushed**: Patches applied to the stack

## Create Patch Queue

### Initialize MQ

```bash
# Enable MQ in existing repository
hg qinit

# View queue status
hg qseries
```

### Create First Patch

```bash
# Create patch from current working directory
hg qnew -m "Initial commit" my-first-patch

# Edit patch message
hg qnew my-first-patch
# This opens editor to enter patch message
```

## Patch Management

### Create Patch

```bash
# Create new patch
hg qnew feature-patch

# Create patch from existing commit
hg qimport -r 1234

# Create patch from diff file
hg qimport existing.patch

# Create patch with message
hg qnew -m "Add login feature" login-feature
```

### Apply and Remove Patches

```bash
# Apply next patch
hg qpush

# Apply multiple patches
hg qpush -a

# Apply specific patch
hg qpush my-patch

# Remove top patch
hg qpop

# Remove all patches
hg qpop -a

# Remove down to specific patch
hg qpop my-patch
```

### View Patches

```bash
# List all patches
hg qseries

# List applied patches
hg qapplied

# List unapplied patches
hg qunapplied

# View current patch
hg qtop

# View patch content
hg qdiff

# View specfic patch content
hg qdiff -r "qparent::qtip"
```

## Edit Patch

### Modify Current Patch

```bash
# Edit patch message
hg qrefresh -m "Updated message"

# Add changes to current patch
hg qrefresh

# Add specific files to patch
hg qrefresh file1.txt file2.txt

# Edit patch content
hg qedit
```

### Reorder Patches

```bash
# Move patch position
hg qreorder patch1 patch2

# View patch order
hg qseries
```

### Import and Export Patches

```bash
# Export all patches
hg qexport

# Export specific patch
hg qexport my-patch

# Export with custom filename
hg qexport -o custom-name.patch my-patch
```

## Advanced Operations

### Fold Patches

```bash
# Fold multiple patches into one
hg qfold -m "Folded patch" patch1 patch2 patch3

# Fold into current patch
hg qfold patch1 patch2
```

### Delete Patch

```bash
# Delete current patch
hg qdelete

# Delete specific patch
hg qdelete my-patch

# Delete patch but keep files
hg qdelete -k my-patch

# Delete unapplied patches
hg qdelete -a
```

### Reapply Patch

```bash
# Reapply all patches
hg qpush -a -f

# Reapply and resolve conflicts
hg qpush --reapply

# Force apply patch
hg qpush -f
```

## Patch Conflict Resolution

### View Conflict

```bash
# Try to apply patch
hg qpush

# If conflict exists, view conflict files
hg qdiff

# View conflict markers
grep -r "<<<<<<" .
```

### Resolve Conflict

```bash
# After manual resolution
hg resolve --mark

# Mark patch as resolved
hg qrefresh

# Continue to next patch
hg qpush
```

### Discard Conflicting Patch

```bash
# Discard changes of current patch
hg qpop

# Delete patch from queue
hg qdelete my-patch
```

## Patch Queue Management

### Create Multiple Queues

```bash
# Create new queue
hg qqueue --create new-queue

# Switch queue
hg qqueue new-queue

# List all queues
hg qqueue

# Delete queue (must switch to another queue first)
hg qqueue --delete old-queue

# Rename queue
hg qqueue --rename old-name new-name
```

### Queue Status

```bash
# View active queue
hg qqueue --active

# View all queues
hg qqueue
```

## Workflows

### Feature Development Workflow

```bash
# 1. Start new feature
hg qnew -m "Start new feature" feature-xyz

# 2. Develop
# Edit files...

# 3. Refresh patch
hg qrefresh

# 4. Continue development
# More edits...

# 5. Final refresh
hg qrefresh

# 6. Finish patch
hg qfinish -a

# This converts patch to permanent commit
```

### Multi-patch Workflow

```bash
# 1. Create multiple patches
hg qnew -m "Patch 1" patch1
hg qrefresh
hg qnew -m "Patch 2" patch2
hg qrefresh
hg qnew -m "Patch 3" patch3
hg qrefresh

# 2. View patch order
hg qseries
# patch1
# patch2
# patch3

# 3. Apply all patches
hg qpush -a

# 4. Finish all patches
hg qfinish -a
```

### Temporary Patch Workflow

```bash
# 1. Create temporary patch
hg qnew temp-patch

# 2. Make experimental changes
hg qrefresh

# 3. If successful, keep patch
hg qfinish

# 4. If unsuccessful, delete patch
hg qpop
hg qdelete temp-patch
```

## Interaction with Regular Workflow

### Working on Patch Queue

```bash
# Pull updates when having patch queue
hg pull

# Update to patch base
hg update qparent

# Merge updates into current patch
hg qpop -a
hg update tip
hg merge qparent
hg commit -m "Merge upstream updates"
hg qnew patch-after-merge
hg qpush -a
```

### Convert Patches to Commits

```bash
# Convert all patches to commits
hg qfinish -a

# Convert specific patch to commit
hg qfinish my-patch

# Convert multiple patches to commits
hg qfinish patch1 patch2
```

## MQ Configuration Options

### Configure in ~/.hgrc

```ini
[mq]
# Directory to save patches
patches = .hg/patches

# Auto refresh patches
auto-refresh = False

# Auto apply patches
auto-push = False

# Sign patches
sign = False

# Keep original patches
keep-originals = True
```

### Patch Naming Pattern

```ini
[mq]
# Patch naming format
# %n - Sequence number
# %b - Branch name
# %h - Short hash
# %r - Revision number
# %R - Remote repo name
# %u - User
patch-dir = .hg/patches
```

## Troubleshooting

### Patch Application Failed

```bash
# Try to reapply
hg qpush -f

# Or manual resolution
hg qpush
# Resolve conflicts
hg resolve --mark
hg qrefresh
```

### Patch Conflict

```bash
# View conflict
hg qdiff

# Discard patch
hg qpop
hg qdelete conflicted-patch

# Or continue after resolution
hg resolve --mark
hg qrefresh
```

### Lost Patches

```bash
# Recover patch from history
hg qimport -r 1234

# Recover patch from file
hg qimport /path/to/saved.patch
```

## MQ Best Practices

### Naming Conventions

```bash
# Feature patches
feature-user-auth
feature-dashboard

# Bugfix patches
fix-login-bug
fix-performance-issue

# Experimental patches
experiment-new-algorithm
wip-work-in-progress
```

### Patch Granularity

```bash
# Good: Small and focused patches
hg qnew -m "Add user model" user-model
hg qnew -m "Implement user auth" user-auth
hg qnew -m "Add login UI" login-ui

# Bad: Large and messy patch
hg qnew -m "Add user features including model, auth, UI etc" everything
```

### Finish Patches Regularly

```bash
# Don't let patches stay in queue for too long
hg qfinish -a

# Sync upstream regularly
hg pull -u
hg qpop -a
# Reapply patches
hg qpush -a
```

## MQ Command Quick Reference

| Command | Description |
|---------|-------------|
| `hg qinit` | Initialize MQ |
| `hg qnew` | Create new patch |
| `hg qpush` | Apply patch |
| `hg qpop` | Remove patch |
| `hg qrefresh` | Refresh patch |
| `hg qseries` | List all patches |
| `hg qapplied` | List applied patches |
| `hg qunapplied` | List unapplied patches |
| `hg qtop` | View top patch |
| `hg qdiff` | View patch diff |
| `hg qdelete` | Delete patch |
| `hg qfold` | Fold patches |
| `hg qfinish` | Finish patch |
| `hg qqueue` | Manage queues |
| `hg qimport` | Import patch |
| `hg qexport` | Export patch |
| `hg qreorder` | Reorder patches |
