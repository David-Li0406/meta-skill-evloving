---
name: manage-stacked-prs
description: Use this skill to manage stacked pull requests and Git branches using the Graphite CLI (gt) for efficient version control workflows.
---

# Managing Stacked Pull Requests with Graphite

Graphite enables the management of stacked pull requests (PRs) on GitHub, allowing for incremental code changes that can be tested, reviewed, and merged independently. This skill provides a comprehensive guide for creating, modifying, and submitting stacked PRs using the `gt` CLI.

## Core Workflow

### Creating a Stacked PR

1. **Start from the main branch:**
   ```bash
   gt checkout main
   ```

2. **Create the first branch in the stack:**
   ```bash
   gt create --all -m "feat(api): Add new API method"  # Stages all changes, creates a branch, and commits
   ```

3. **Submit the PR:**
   ```bash
   gt submit
   ```

4. **Create subsequent branches in the stack:**
   ```bash
   gt create --all -m "feat(frontend): Load and show users"
   ```

5. **Submit the entire stack:**
   ```bash
   gt submit --stack
   ```

### Modifying Current Branch

- **Amend last commit and restack:**
  ```bash
  gt modify -a
  ```

- **Create a new commit and restack:**
  ```bash
  gt modify --commit --message "Feedback"
  ```

### Syncing and Restacking

- **Sync with the latest changes:**
  ```bash
  gt sync  # Pull latest, rebase open PRs, clean merged branches
  ```

- **Continue after resolving conflicts:**
  ```bash
  gt continue
  ```

### Navigation Commands

- **Move to parent branch:**
  ```bash
  gt up
  ```

- **Move to child branch:**
  ```bash
  gt down
  ```

- **View stack structure:**
  ```bash
  gt log short  # Condensed view of the stack
  ```

## Best Practices

- **Keep PRs small:** Aim for 100-200 lines per PR for easier review.
- **Test locally before submitting:** Ensure all tests pass to avoid CI failures.
- **Plan your stack structure:** Present the intended stack structure before coding.
- **Use descriptive commit messages:** Clearly describe the purpose of each change.

## Common Patterns

### New Feature Development

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

### Keeping Your Stack Updated

```bash
gt sync        # Daily sync with main
# Resolve any conflicts
gt continue
```

## Troubleshooting

- **If `gt` commands fail:** Save your work with `git add .` and `git commit -m "wip: saving progress"`, then push using `git push origin HEAD`.
- **For merge conflicts:** Use `gt sync` to pull the latest changes and resolve conflicts.

## Conclusion

Utilize the Graphite CLI to streamline your version control workflow, manage stacked PRs effectively, and maintain high code quality through structured development practices.