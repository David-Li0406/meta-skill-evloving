---
name: github-cli-automation
description: Automate GitHub operations using the `gh` CLI for managing repositories, issues, pull requests, releases, and workflows.
---

# GitHub CLI Automation

This skill helps you manage GitHub operations using the `gh` CLI, including repositories, issues, pull requests, releases, and GitHub Actions workflows.

## Prerequisites

Ensure `gh` CLI is installed and authenticated:
```bash
gh auth status
```

## Core Capabilities

- **Repositories**: Create, clone, fork, view, and manage repositories.
- **Issues**: Create, list, view, close, comment, and label issues.
- **Pull Requests**: Create, review, merge, list, and comment on pull requests.
- **Releases**: Create releases and manage tags.
- **Workflows**: View and manage GitHub Actions.
- **Search**: Search repositories, issues, pull requests, code, and users.

## Common Operations

### Repository Operations
```bash
# View repository
gh repo view <owner>/<repo>

# Clone repository
gh repo clone <owner>/<repo>

# Create a new repository
gh repo create <name> --public/--private

# List repositories for an owner
gh repo list <owner>
```

### Issue Operations
```bash
# List issues
gh issue list --repo <owner>/<repo>

# Create an issue
gh issue create --repo <owner>/<repo> --title "Title" --body "Body"

# View a specific issue
gh issue view <number> --repo <owner>/<repo>

# Close an issue
gh issue close <number> --repo <owner>/<repo>

# Comment on an issue
gh issue comment <number> --repo <owner>/<repo> --body "Comment"
```

### Pull Request Operations
```bash
# List pull requests
gh pr list --repo <owner>/<repo>

# Create a pull request
gh pr create --repo <owner>/<repo> --title "Title" --body "Body"

# View a specific pull request
gh pr view <number> --repo <owner>/<repo>

# Merge a pull request
gh pr merge <number> --repo <owner>/<repo>

# Review a pull request
gh pr review <number> --repo <owner>/<repo> --approve/--comment/--request-changes
```

### Release Operations
```bash
# List releases
gh release list --repo <owner>/<repo>

# Create a release
gh release create <tag> --repo <owner>/<repo> --title "Title" --notes "Notes"
```

### Workflow Operations
```bash
# List workflow runs
gh run list --repo <owner>/<repo>

# View a specific workflow run
gh run view <run-id> --repo <owner>/<repo>

# List workflows
gh workflow list --repo <owner>/<repo>
```

## Automation Scripts

### Auto-Reply Fixed Issues
Automatically find and reply to issues fixed since the last release:
```bash
# Preview (dry-run)
python scripts/auto-reply-fixed-issues.py --dry-run

# Post comments
python scripts/auto-reply-fixed-issues.py

# Specific repo
python scripts/auto-reply-fixed-issues.py --repo owner/repo
```

## Guidelines

- Always specify `--repo <owner>/<repo>` when not in a cloned repository.
- For destructive operations (delete, close, merge), confirm with the user first.
- Use `--json` flag when you need to parse output programmatically.
- Handle errors gracefully and suggest fixes.
- When creating issues/PRs, use clear titles and descriptive bodies.

## Output Format

When listing items, format clearly:
```
#123 - Issue title (open/closed) - @author
#456 - PR title (open/merged/closed) - @author
```

When creating items, always report:
- The created item's number/ID
- Direct URL to the item
- Any relevant status information

## Examples

**Create an issue:**
```bash
gh issue create --repo <owner>/<repo> --title "Bug: Login fails" --body "Steps to reproduce..."
```

**List open PRs awaiting review:**
```bash
gh pr list --repo <owner>/<repo> --state open --search "review:required"
```

**Get PR details as JSON:**
```bash
gh pr view <number> --repo <owner>/<repo> --json title,state,reviews,checks
```

## Additional Resources

- **Command Reference**: See the official [GitHub CLI documentation](https://cli.github.com/manual/) for complete command reference.
- **GitHub API Access**: Use `gh api` for direct REST/GraphQL access with built-in authentication.

**Remember**: The GitHub CLI is a powerful tool - use it wisely to automate your GitHub workflows and boost your productivity! 🚀