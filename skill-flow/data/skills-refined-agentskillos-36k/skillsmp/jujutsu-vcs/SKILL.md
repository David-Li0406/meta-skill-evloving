---
name: jujutsu-vcs
description: Version control workflow using jujutsu (jj) exclusively. Use when managing version control, committing changes, viewing history, working with branches, or syncing with remote repositories. DO NOT use git commands - use jj commands instead.
---

# Jujutsu Version Control

**Critical Rule:** Use jujutsu exclusively. DO NOT make ANY git commands.

## Branch Management

When pushing a branch:

1. NEVER merge
2. Fetch main branch
3. Rebase onto it

```bash
jj git fetch
jj rebase -d main
jj git push
```

## Common Commands

**Status and Inspection:**

```bash
jj status          # View status
jj log             # View log
jj diff            # View diff
```

**Making Changes:**

```bash
jj describe -m "commit message"    # Describe changes
jj new                              # Create new change
jj edit                             # Edit a change
```

**Branch Operations:**

```bash
jj branch create <name>             # Create branch
jj rebase -d <destination>          # Rebase
```

**Remote Operations:**

```bash
jj git fetch                        # Fetch
jj git push                         # Push
```
