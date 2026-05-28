---
name: jujutsu-version-control
description: Use this skill when managing version control with Jujutsu (jj), including committing changes, viewing history, and syncing with remote repositories.
---

# Jujutsu Version Control

## Core Principles

- **Change IDs** (immutable) vs **Commit IDs** (content-based hashes that change on edit)
- **No staging area**: All changes in the working directory are automatically part of the current change.
- **Automatic snapshots**: The working copy is automatically snapshotted.
- **Immutable history**: By default, only "mutable" commits can be modified.
- **Conflicts don't block**: Resolve later.

## Essential Commands

### Status and Inspection
```bash
jj status                          # View current status
jj log                             # View history
jj diff                            # View changes
jj diff --git                      # Use Git-compatible diff format
jj show -r <rev>                   # Show revision details
```

### Making Changes
```bash
jj new [-A] <base>                 # Create a new change
jj edit <rev>                       # Switch to editing revision
jj describe -m "commit message"     # Set description
jj commit -m "commit message"       # Commit current change
jj squash                           # Squash into parent
```

### Branch Operations
```bash
jj branch create <name>             # Create a new branch
jj rebase -d <destination>          # Rebase onto another branch
```

### Remote Operations
```bash
jj git fetch                        # Fetch from remote
jj git push                         # Push changes to remote
jj push-new                         # Create a new bookmark and push it
```

## Agent Guidelines

1. **Use jj exclusively**: Do not use Git commands.
2. **Always use `-m` flag**: For commands like `jj describe`, `jj commit`, and `jj squash` to avoid opening an editor.
3. **Use `--ignore-working-copy`**: For read operations when you don't need the latest snapshot.
4. **Use Git-compatible formats**: For easier parsing of diffs and conflicts.

## For More Information

For detailed documentation, command references, and templates, refer to the Jujutsu documentation or invoke the `/jj` command.