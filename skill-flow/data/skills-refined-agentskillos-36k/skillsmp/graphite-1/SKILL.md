---
name: graphite
description: "Manage Git branches and PRs using Graphite CLI (gt) instead of raw git commands. Use this skill when committing code changes, amending commits, creating branches, or submitting pull requests. Triggers on git commit, git push, creating PRs, amending changes, stacking branches, or any version control workflow."
---

# Graphite CLI

Use `gt` commands instead of raw git for all branch and PR operations.

## Core Workflow

### Create a branch with changes

```bash
gt create -m "description"           # Create branch with staged changes
gt create --all -m "description"     # Stage all files and create branch
gt create                            # Interactive: prompts for message
```

### Modify current branch

```bash
gt modify                            # Amend staged changes to current commit
gt modify --all                      # Stage all and amend
gt modify -m "new message"           # Amend with new commit message
gt modify --commit                   # Add new commit instead of amending
```

### Submit PR to GitHub

```bash
gt submit --no-interactive           # Push and create/update PR
gt submit --no-interactive --stack   # Submit entire stack
gt submit --no-interactive --draft   # Create as draft PR
```

## Common Patterns

**New feature:**
```bash
gt create --all -m "Add user authentication"
gt submit --no-interactive
```

**Fix after code review:**
```bash
gt modify --all
gt submit --no-interactive
```

**Multiple related changes (stacking):**
```bash
gt create --all -m "Add auth middleware"
gt submit --no-interactive
gt create --all -m "Add login endpoint"
gt submit --no-interactive --stack
```

## Key Flags

| Flag | Commands | Effect |
|------|----------|--------|
| `--all`, `-a` | create, modify | Stage all changes including untracked |
| `--message`, `-m` | create, modify | Set commit message |
| `--no-interactive` | submit | Skip prompts, use defaults |
| `--stack`, `-s` | submit | Include descendant branches |
| `--draft`, `-d` | submit | Create PR as draft |

## Navigation

```bash
gt checkout [branch]    # Switch branch (interactive if no arg)
gt up / gt down         # Move up/down the stack
gt log                  # Show stack structure
gt sync                 # Sync with remote, clean merged branches
```

## Conflict Resolution

```bash
gt continue             # Continue after resolving conflicts
gt abort                # Abort current operation
gt restack              # Rebase stack to fix parent history
```

## Resources

See [references/commands.md](references/commands.md) for full command reference.
