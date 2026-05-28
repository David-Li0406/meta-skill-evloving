---
name: graphite
description: Manage stacked pull requests using Graphite CLI (gt). Use when creating PRs, working with git branches in a stack, submitting changes for review, syncing branches, or when the user mentions Graphite, stacked PRs, or the gt command.
allowed-tools:
  - Bash(gt:*)
  - Bash(git:*)
---

# Graphite CLI (gt) - Stacked Pull Requests

Graphite manages stacked pull requests on GitHub. A stack is a sequence of PRs, each building off its parent, enabling incremental code changes that can be tested, reviewed, and merged independently.

## Core Commands

### Creating Stacked PRs

```bash
# Start from main branch
gt checkout main

# Create first branch in stack
gt create --all --message "feat(api): Add new API method"
# This stages all changes, creates a branch, and commits

# Submit the PR
gt submit

# Create next branch in stack (builds on previous)
gt create --all --message "feat(frontend): Load and show users"

# Submit entire stack
gt submit --stack
```

### Navigation

```bash
gt up          # Move to parent branch
gt down        # Move to child branch
gt checkout    # Interactive branch picker
gt top         # Go to top of stack
gt bottom      # Go to bottom of stack
gt log         # View stack structure (detailed)
gt log short   # View stack structure (condensed)
```

### Modifying Branches

```bash
gt modify -a                              # Amend last commit and restack
gt modify --commit --message "Feedback"   # New commit and restack
gt split                                  # Split branch into multiple
```

### Syncing & Restacking

```bash
gt sync       # Pull latest, rebase open PRs, clean merged branches
gt continue   # Resume after resolving conflicts
gt reorder    # Reorder branches in stack
gt move       # Move commits between branches
```

### Merging

```bash
gt top        # Go to top of stack first
gt pr         # Open PR in Graphite web UI for merging
gt merge      # Or merge from CLI
```

## Key Concepts

1. **Stacking**: Each PR builds on the previous one
2. **Restacking**: Auto-rebases dependent branches when parent changes
3. **Fall-through**: Unrecognized commands pass to git (`gt status` = `git status`)

## Common Workflows

### Creating a Feature Stack

```bash
gt checkout main
gt create --all -m "feat: Add database schema"
gt submit
gt create --all -m "feat: Add API endpoints"
gt submit
gt create --all -m "feat: Add UI components"
gt submit --stack
```

### Addressing Review Feedback

```bash
gt checkout <branch-name>
# Make changes
gt modify -a   # Amend and restack
gt submit
```

### Keeping Stack Updated

```bash
gt sync        # Daily sync with main
# Resolve any conflicts
gt continue
```

## Tips

- Use `gt create -m "description"` for descriptive branch names
- Keep PRs small (100-200 lines ideally)
- Sync regularly to avoid large rebases
- Use `gt log short` to visualize stack state
- `--all` flag stages all changes automatically
