# Mercurial Basic Operations

This guide covers the daily basic operations of Mercurial.

## Initialization and Cloning

### Initialize New Repository

```bash
hg init project-name
cd project-name
```

### Clone Remote Repository

```bash
# Standard clone
hg clone https://example.com/repo

# Clone to specific directory
hg clone https://example.com/repo my-directory

# Do not update to the latest changeset (just clone)
hg clone -U https://example.com/repo

# Shallow clone (pull only the latest n changesets)
hg clone -r tip https://example.com/repo
```

### Share Repository (Git worktree equivalent)

The `hg share` command creates a new working directory that shares its history with another repository. This is similar to Git's `git worktree` and allows working on different branches or changes in parallel without the associated cost in terms of disk space.

```bash
# Enable share extension (add to ~/.hgrc)
[extensions]
share =

# Create shared working directory
hg share /path/to/original /path/to/share

# Share without updating to tip
hg share -U /path/to/original /path/to/share

# Share with bookmarks
hg share -B /path/to/original /path/to/share

# Share with relative path
hg share --relative ../original my-share

# Unshare - convert shared repository to normal
hg unshare
```

**Important Notes:**
- Shared repositories share the same store (`.hg/store`), saving disk space
- Using `rollback` or extensions that modify history (mq, rebase, etc.) can cause considerable confusion with shared clones
- If you upgrade storage format in one repository, ensure related configs are set in the shares
- Setting `format.exp-share-safe = True` enables sharing configs and requirements

**Automatic Pooled Storage:**
```bash
# Configure shared pool in ~/.hgrc
[share]
pool = /path/to/share/pool
poolnaming = identity  # or "remote"
```

## File Status

### View Status

```bash
# Basic status
hg status

# Show all files (including untracked)
hg status -A

# Show modified files and their status
hg status -mard

# Show copies and renames
hg status -C
```

### Status Codes Explained

| Code | Meaning |
|------|---------|
| M | Modified |
| A | Added - added but not committed |
| R | Removed |
| ! | Missing - file deleted but not removed from repo |
| ? | Untracked |
| I | Ignored |

### View Differences

```bash
# View all changes
hg diff

# View specific file
hg diff file.txt

# View difference between working directory and specific revision
hg diff -r 1234 file.txt

# View difference between two revisions
hg diff -r 1234:1235

# Ignore whitespace
hg diff -w

# Show unified context lines
hg diff -U 5
```

## Add and Remove Files

### Add Files

```bash
# Add single file
hg add file.txt

# Add multiple files
hg add file1.txt file2.txt

# Add all files
hg add

# Add files matching pattern
hg add -I "*.cpp"
```

### Remove Files

```bash
# Remove file (keep file copy)
hg remove file.txt

# Remove file and delete
hg remove -f file.txt

# Remove all deleted files
hg remove -A
```

## Commit Changes

### Basic Commit

```bash
# Commit all added files
hg commit -m "Commit message"

# Commit specific files
hg commit -m "Commit message" file1.txt file2.txt

# Add and commit all changes
hg commit -A -m "Commit message"
```

### Commit Options

```bash
# Do not open editor
hg commit -m "Commit message"

# Open editor to enter commit message
hg commit

# Use specified username
hg commit -u "Username <email@example.com>"

# Add date
hg commit -d "2024-01-01 12:00:00 +0800"

# Amend last commit (not recommended)
hg commit --amend
```

## View History

### Basic History

```bash
# Short history
hg log

# Graphical history
hg log -G

# Detailed history
hg log -v

# Minimal history (hash and message only)
hg log --template "{node|short}: {desc}\n"

# Limit number of entries
hg log -l 10

# Start from specific revision
hg log -r 1000:tip
```

### Filter by Condition

```bash
# Specify author
hg log -u "Author Name"

# Specify date range
hg log -d "2024-01-01 to 2024-01-31"

# Specify file
hg log path/to/file

# Search commit message
hg log -k "keyword"

# Show all branches
hg log --all
```

### History Template

```bash
# Custom template
hg log --template "{rev}:{node|short} | {author} | {date|isodate}\n{desc}\n\n"

# Common placeholders
# {rev}  - Revision number
# {node} - Full hash
# {node|short} - Short hash
# {author} - Author
# {date} - Date
# {desc} - Commit message
# {bookmarks} - bookmarks
# {branches} - Branch name
```

## Pull and Push

### Pull Updates

```bash
# Pull remote updates
hg pull

# Update working directory after pull
hg pull -u

# Pull remote updates to specific changeset
hg pull -r 1234

# View incoming changes but do not pull
hg incoming

# Pull from specific remote
hg pull https://other-repo.example.com
```

### Push Changes

> **Warning**: Always exercise caution with any push operation. Use `hg outgoing` to review the changes before pushing, and ensure you only push the intended changesets.

```bash
# Push local changes
hg push

# Push to specific remote
hg push https://other-repo.example.com

# Push specific changeset
hg push -r 1234

# View outgoing changes
hg outgoing

# Force push (create new remote head)
hg push -f
```

## Update Working Directory

### Update to Specific Revision

```bash
# Update to latest
hg update

# Update to specific revision number
hg update 1234

# Update to tip
hg update tip

# Update to specific changeset
hg update abc123def456
```

### Update Options

```bash
# Discard local changes
hg update -C

# Update to another bookmark
hg update bookmark-name

# Update but do not keep backup
hg update --clean
```

## Undo Operations

### Revert Files

```bash
# Revert file to last commit state
hg revert file.txt

# Revert all files
hg revert --all

# Revert to specific revision
hg revert -r 1234 file.txt

# Revert but do not create backup
hg revert --no-backup file.txt
```

### Backout Commit

```bash
# Backout specific commit (create new commit)
hg backout 1234

# Backout and merge
hg backout 1234 --merge

# Do not open editor
hg backout 1234 -m "Backout explanation"
```

### Delete Commit (requires mq extension)

```bash
# Strip specific commit and all following commits
hg strip 1234

# Keep backup
hg strip --keep 1234

# Strip up to specific commit (exclusive)
hg strip -r 1234:
```

## Search and Grep

### Search Commits

```bash
# Search commit message
hg log -k "keyword"

# Search code changes
hg grep "keyword"

# Search in specific file
hg grep "keyword" path/to/file

# Show matching commits
hg grep --all "keyword"
```

## Export and Import

### Export Patch

```bash
# Export single commit
hg export 1234 > patch.diff

# Export multiple commits
hg export -o patch-%n.diff 1234:1236

# Export all outgoing commits
hg export -o patch-%n.diff `hg out -q`
```

### Import Patch

```bash
# Apply patch
hg import patch.diff

# Apply patch but do not commit
hg import --no-commit patch.diff

# Specify commit message
hg import -m "Description" patch.diff
```

## Ignore Files

Create `.hgignore` file:

```
# Lines starting with # are comments

# glob mode
syntax: glob
*.pyc
*.o
*.so
build/
dist/

# regexp mode
syntax: regexp
^\.git/
```

## Common Aliases

Add to `~/.hgrc`:

```ini
[alias]
st = status
ci = commit
co = update
br = branches
heads = heads
logg = log --graph --template "{rev}:{node|short} {desc|firstline}\n"
```
