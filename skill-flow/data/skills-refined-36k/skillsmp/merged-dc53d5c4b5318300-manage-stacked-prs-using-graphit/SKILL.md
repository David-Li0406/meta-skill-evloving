---
name: manage-stacked-prs-using-graphite
description: Use this skill to manage Git branches and pull requests with Graphite CLI, especially when working with stacked pull requests and ensuring code quality through CI checks.
---

# Managing Stacked PRs with Graphite CLI

Graphite enables efficient management of Git branches and pull requests (PRs) using the `gt` CLI. This skill is essential for creating and managing stacked PRs, which are chains of dependent PRs that build on each other, making it easier to handle large changes.

## Core Workflow

### Assess Current State

Before starting, check if Graphite is active and understand your current stack:

```bash
bash skills/use-graphite/scripts/graphite-detect.sh   # Check if Graphite is active
gt log short                                           # View current stack structure
git status                                             # Check for uncommitted changes
```

### Creating a Branch with Changes

To create a new branch with staged changes, use:

```bash
gt create -m "description"           # Create branch with staged changes
gt create --all -m "description"     # Stage all files and create branch
```

### Modifying the Current Branch

To amend changes to the current commit:

```bash
gt modify                            # Amend staged changes to current commit
gt modify --all                      # Stage all and amend
gt modify -m "new message"           # Amend with new commit message
```

### Submitting a Pull Request

To submit a PR to GitHub:

```bash
gt submit --no-interactive           # Push and create/update PR
gt submit --no-interactive --stack   # Submit entire stack
```

### Stacked Pull Requests

When working with large features, break them into smaller, logical PRs:

1. **Plan Your Stack Structure**: Present the intended stack structure for confirmation before coding.
2. **Ensure Atomic and CI-Passing**: Each PR must be atomic and pass CI checks before submission.
3. **Create Each Branch**: Use `gt create` for each step in the stack.
4. **Submit the Stack**: Use `gt submit --stack` to submit all PRs in the stack.

### Keeping the Stack in Sync

To keep your stack aligned with the base branch:

```bash
gt stack sync --no-interactive
```

### Best Practices

- **Test Before Submit**: Always run tests locally to ensure CI will pass.
- **Keep PRs Small and Atomic**: Each PR should represent a single logical change.
- **Use `gt` Commands**: Prefer `gt create` and `gt submit` over raw git commands to maintain stack integrity.
- **Sync Regularly**: Use `gt stack sync` to avoid merge conflicts.

### Troubleshooting

If you encounter issues:

- **Stack Structure Incorrect**: Use `gt restack --no-interactive` to reorganize.
- **Merge Conflicts**: Sync with the base branch and resolve conflicts.
- **Need to Modify Earlier PR**: Check out the branch, make changes, and restack.

## Command Reference

| Command | Purpose |
|---------|---------|
| `gt create --no-interactive` | Create a commit and branch with automatic dependencies |
| `gt submit --no-interactive` | Submit the current branch and downstack to Graphite |
| `gt stack submit --no-interactive` | Submit the entire stack as PRs |
| `gt stack sync --no-interactive` | Sync the stack with the base branch |

## Conclusion

Using Graphite CLI streamlines the process of managing stacked PRs, ensuring that changes are logical, reviewable, and maintain high code quality. Always plan your stack structure, verify CI checks, and utilize `gt` commands for optimal results.