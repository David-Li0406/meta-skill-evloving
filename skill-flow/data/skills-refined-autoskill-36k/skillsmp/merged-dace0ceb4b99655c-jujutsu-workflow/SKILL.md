---
name: jujutsu-workflow
description: Use this skill when working with Jujutsu (jj) for version control, providing guidance on commands, workflows, and best practices.
---

# Jujutsu (jj) Version Control Workflow

## Overview

Jujutsu (jj) is a Git-compatible version control system that emphasizes a different workflow compared to traditional Git. This skill provides comprehensive guidance on using jj commands, managing changes, and understanding the unique features of jujutsu.

## Key Differences from Git

- **No Staging Area**: All changes in the working directory are automatically part of the current change.
- **Changes vs Commits**: Jujutsu uses "changes" identified by change IDs rather than traditional commits.
- **Automatic Snapshots**: The working copy is automatically snapshotted.
- **Immutable History**: By default, only mutable changes can be modified.

## Core Principles

- **Change IDs**: Immutable identifiers for changes.
- **Operations Log**: Every operation can be undone progressively.
- **No Conflicts Block**: Conflicts can be resolved later without blocking operations.
- **Lightweight Commits**: Commits are easy to edit and manage.

## Common Workflow Commands

| Task                          | Command                                      |
|-------------------------------|----------------------------------------------|
| See current status            | `jj status`                                  |
| View diff                     | `jj diff --git`                             |
| Commit current change         | `jj commit -m "message"`                    |
| Set/update description        | `jj describe -m "message"`                  |
| Squash into parent            | `jj squash`                                  |
| Create new change             | `jj new`                                     |
| Push to remote                | `jj git push`                               |
| Fetch from remote             | `jj git fetch`                              |
| Cleanup empty commits         | `/cleanup`                                   |

## Best Practices

1. **Use jj, Not Git**: All version control operations should use jj commands exclusively.
2. **Always Use `-m` Flag**: For `jj describe`, `jj commit`, and `jj squash` to avoid opening an editor.
3. **Use `--ignore-working-copy`**: For read operations like `jj log` and `jj diff` when you don't need the latest snapshot.
4. **Use `--git` for Diffs**: `jj diff --git` produces standard unified diff format.

## Common Jujutsu Operations

### Navigating Changes

- **Check Current Status**: 
  ```bash
  jj status
  ```

- **View Commit History**: 
  ```bash
  jj log
  ```

- **Show Changes**: 
  ```bash
  jj diff
  ```

### Managing Changes

- **Create a New Change**: 
  ```bash
  jj new
  ```

- **Describe Current Change**: 
  ```bash
  jj describe -m "Your message here"
  ```

- **Squash Changes**: 
  ```bash
  jj squash
  ```

### Undoing Changes

- **Undo Last Operation**: 
  ```bash
  jj undo
  ```

- **Redo Undone Operation**: 
  ```bash
  jj redo
  ```

## Troubleshooting

### Common Pitfalls

- **Accidentally Run Git Commands**: If you accidentally run a git command in a jujutsu repository, use:
  ```bash
  jj undo
  ```

- **Conflicts During Rebase**: Jujutsu handles conflicts gracefully. Use:
  ```bash
  jj status
  jj diff
  ```

## References

For detailed jj documentation, command references, revset syntax, and templates, refer to the official Jujutsu documentation or invoke the `/jj` command for more information.