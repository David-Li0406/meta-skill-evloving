# Mercurial Advanced Operations

This guide covers advanced Mercurial operations, including merging, conflict resolution, rebase, histedit, etc.

## Merge

### Basic Merge

```bash
# Merge specified branch into current branch
hg update default
hg merge feature-branch
hg commit -m "Merge feature branch"

# Check status after merge
hg status

# View merge diff
hg diff -r "p1()" -r "p2()"
```

### Merge Options

```bash
# Preview revisions to merge (no merge is performed)
hg merge -P

# Specify merge tool
hg merge --tool=vimdiff

# Preview possible merges
hg merge --preview

# Merge specific changeset
hg merge -r 1234
```

### Merge Conflict Resolution

```bash
# View conflicting files
hg resolve --list

# Resolve conflict (mark as resolved)
hg resolve --mark file.txt

# Unmark conflict (re-merge file)
hg resolve --unmark file.txt

# Abort merge
hg merge --abort
```

### View Merge History

```bash
# View all merge commits
hg log -m

# View recent merges
hg log -m -l 10

# View merges on specific branch
hg log -m -b default
```

## Rebase

**Note**: The rebase extension needs to be enabled:
```ini
[extensions]
rebase =
```

### Basic Rebase

```bash
# Rebase current branch to the latest version
hg update my-feature
hg rebase -d default

# Rebase specific changeset
hg rebase -s 1234 -d tip

# Rebase specific range
hg rebase -s 1234 -d 5678

# Rebase all unmerged changesets
hg rebase -d default
```

### Rebase Options

```bash
# Dry run rebase (do not execute)
hg rebase --dry-run

# Keep original author info
hg rebase --keepauthor

# Continue rebase (after resolving conflicts)
hg rebase --continue

# Abort rebase
hg rebase --abort
```

### Rebase Conflict Handling

```bash
# Continue after resolving conflicts
hg resolve --mark
hg rebase --continue

# Abort current rebase
hg rebase --abort
```

## History Editing (Histedit)

**Note**: The histedit extension needs to be enabled:
```ini
[extensions]
histedit =
```

### Edit History

```bash
# Edit the last n commits
hg histedit -r "tip~5"

# Edit specific changeset
hg histedit -r 1234

# Edit specific range
hg histedit -r 1234::1236
```

### Histedit Commands

In the histedit editor, each changeset can be assigned a command:

| Command | Description |
|---------|-------------|
| `pick` | Use this changeset (default) |
| `drop` | Discard this changeset |
| `edit` | Edit this changeset |
| `fold` | Fold this changeset into the previous one |
| `mess` | Edit commit message for this changeset |
| `base` | Use this changeset as base |

### Continue After Editing

```bash
# Continue after editing
hg histedit --continue

# Abort histedit
hg histedit --abort

# View changesets during edit
hg histedit --view-changesets
```

## Graft

**Note**: The graft extension needs to be enabled (usually built-in).

### Basic Graft

```bash
# Graft specific commit to current branch
hg update my-branch
hg graft 1234

# Graft multiple commits
hg graft 1234 1235 1236

# Graft a range of commits
hg graft -r 1234::1236

# Graft commits from specific branch
hg graft -r "ancestors('feature')"
```

### Graft Options

```bash
# Dry run (do not apply changes)
hg graft --dry-run

# Keep original author info
hg graft --user "Original Author"

# Specify commit message
hg graft -m "Custom commit message" 1234

# Use 3-way merge tool (helps with conflicts)
hg graft --tool internal:merge3
```

### Graft Conflict Handling

```bash
# Continue after resolving conflicts
hg resolve --mark
hg graft --continue

# Abort current graft
hg graft --abort
```

## Phases

### View Phases

```bash
# View phases of all changesets
hg phases

# View specific changeset phase
hg phase 1234

# View current working directory phase
hg phase -r .
```

### Modify Phases

```bash
# Set changeset to public
hg phase -p 1234

# Set changeset to draft
hg phase -d 1234

# Set changeset to secret
hg phase -s 1234

# Force modify phase
hg phase --force -p 1234
```

### Phase Rules

| Phase | Rebase/Modify | Description |
|-------|---------------|-------------|
| public | No | Published, immutable |
| draft | Yes | Local development |
| secret | Yes | Not pushed, private |

## Patch Operations

### Create Patch

```bash
# Create patch for working directory
hg diff > my-changes.patch

# Create patch for specific changeset
hg export 1234 > patch.diff

# Create patches for multiple changesets
hg export -o %R.patch 1234:1236
```

### Apply Patch

```bash
# Apply patch
hg import my-changes.patch

# Apply patch but do not commit
hg import --no-commit my-changes.patch

# Specify commit message
hg import -m "Apply patch" my-changes.patch

# Specify user
hg import -u "Author Name" my-changes.patch
```

## Modify History (Use with Caution)

### Collapse Commits

**Note**: The collapse extension needs to be enabled:
```ini
[extensions]
collapse =
```

```bash
# Collapse multiple commits into one
hg collapse -r 1234::1237

# Collapse and specify commit message
hg collapse -r 1234::1237 -m "Collapsed commit"
```

### Delete Commits

```bash
# Use mq extension to strip commits
hg strip 1234

# Strip up to specific commit (exclusive)
hg strip -r 1234:

# Strip but keep working directory changes
hg strip --keep 1234
```

## Query Changesets (Revsets)

### Basic Queries

```bash
# Query by author
hg log -u "author-name"

# Query by date range
hg log -d "2024-01-01 to 2024-12-31"

# Query by keyword
hg log -k "keyword"

# Query by file
hg log path/to/file
```

### Advanced Queries

```bash
# Query unmerged changesets (heads)
hg log -r "heads()"

# Query ancestors
hg log -r "ancestors(1234)"

# Query descendants
hg log -r "descendants(1234)"

# Query changes between two revisions
hg log -r "1234::tip"

# Query changes on specific branch
hg log -b feature-branch

# Query merge commits
hg log -m

# Query non-merge commits
hg log --no-merges
```

### Combined Queries

```bash
# Query commits by author in date range
hg log -u "author-name" -d "2024-01-01 to 2024-01-31"

# Query file but exclude branch
hg log path/to/file -b default

# Query last 5 non-merge commits
hg log --no-merges -l 5

# Query commits including specific file changes
hg log --include "*.cpp"
```

## File History and Blame

### View File History

```bash
# File revision history
hg log path/to/file

# File history graph
hg log -G path/to/file

# File annotate (blame)
hg annotate path/to/file

# File diff statistics
hg diffstat -r 1234:1235
```

### Trace File Origin

```bash
# Find last commit modifying file
hg log -r "file('path/to/file')"

# Trace file rename history
hg log --follow path/to/file

# Find file deletion
hg log --removed path/to/file
```

## Configure Merge Tools

### Configure Common Merge Tools

Configure in `~/.hgrc`:

```ini
[merge-tools]
vimdiff.executable = vim
vimdiff.args = -d $local $other $base $output
vimdiff.priority = 10

kdiff3.executable = kdiff3
kdiff3.args = $base $local $other -o $output
kdiff3.priority = 9

meld.executable = meld
meld.args = $local $base $other --output $output
meld.priority = 8
```

### Prioritize Specific Tool

```ini
[ui]
merge = vimdiff
```

### Interactive Merge

```bash
# Merge using specific tool
hg merge --tool=vimdiff

# Preview merge result
hg merge --tool=internal:merge3 --preview
```

## Advanced Export and Import

### Export to Git Format

```bash
# Use hg-git extension
hg gexport

# Export to specific directory
hg gexport --git-dir=/path/to/git-repo
```

### Import from Git

```bash
# Import Git repository
hg gimport

# Import from specific directory
hg gimport --git-dir=/path/to/git-repo
```

## Performance Optimization

### Index Optimization

```bash
# Rebuild index
hg debugrebuildfncache

# Verify index
hg verify

# Recover corrupted repository
hg recover
```
