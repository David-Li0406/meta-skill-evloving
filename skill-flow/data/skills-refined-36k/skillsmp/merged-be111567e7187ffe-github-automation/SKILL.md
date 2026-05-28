---
name: github-automation
description: Use this skill for comprehensive automation of GitHub operations via the `gh` CLI, including managing repositories, issues, pull requests, workflows, and more.
---

# GitHub Automation

This skill enables you to automate a wide range of GitHub operations using the `gh` CLI, covering repositories, issues, pull requests, releases, workflows, and more.

## Capabilities

- **Repositories**: Create, clone, fork, view, and manage repositories.
- **Issues**: Create, list, view, close, comment, and label issues.
- **Pull Requests**: Create, review, merge, list, and comment on pull requests.
- **Releases**: Create releases and manage tags.
- **Workflows**: View and manage GitHub Actions workflows.
- **Gists**: Create and manage gists.
- **Search**: Search repositories, issues, pull requests, code, and users.
- **Discussions**: Manage discussions within repositories.
- **Projects**: Create and manage projects and their items.
- **Notifications**: Manage notifications related to repositories and activities.
- **Security**: Handle code scanning alerts, dependabot alerts, and secret scanning alerts.

## Authentication

The `GITHUB_TOKEN` environment variable is pre-configured. Verify with:
```bash
gh auth status
```

## Instructions

### Phase 1: Understand the Request
1. Clarify what GitHub operation the user needs.
2. Identify the target repository (if not specified, ask).
3. Confirm any destructive operations before executing.

### Phase 2: Execute the Operation
Use `gh` CLI commands. Common patterns include:

**Repository Operations**
```bash
gh repo view <owner>/<repo>
gh repo clone <owner>/<repo>
gh repo create <name> --public/--private
gh repo list <owner>
```

**Issue Operations**
```bash
gh issue list --repo <owner>/<repo>
gh issue create --repo <owner>/<repo> --title "Title" --body "Body"
gh issue view <number> --repo <owner>/<repo>
gh issue close <number> --repo <owner>/<repo>
gh issue comment <number> --repo <owner>/<repo> --body "Comment"
```

**Pull Request Operations**
```bash
gh pr list --repo <owner>/<repo>
gh pr create --repo <owner>/<repo> --title "Title" --body "Body"
gh pr view <number> --repo <owner>/<repo>
gh pr merge <number> --repo <owner>/<repo>
gh pr review <number> --repo <owner>/<repo> --approve/--comment/--request-changes
```

**Workflow Operations**
```bash
gh workflow list --repo <owner>/<repo>
gh workflow run <workflow.yml> --repo <owner>/<repo>
```

**Release Operations**
```bash
gh release list --repo <owner>/<repo>
gh release create <tag> --repo <owner>/<repo> --title "Title" --notes "Notes"
```

## Guidelines

- Always specify `--repo <owner>/<repo>` when not in a cloned repository.
- For destructive operations (delete, close, merge), confirm with the user first.
- Use `--json` flag when you need to parse output programmatically.
- Handle errors gracefully and suggest fixes.
- When creating issues/PRs, use clear titles and descriptive bodies.

### Phase 3: Report Results
- Summarize what was done.
- Provide relevant links (PR URLs, issue numbers, etc.).
- Suggest next steps if applicable.

## Output Format

When listing items, format clearly:
```
#123 - Issue title (open/closed) - @author
#456 - PR title (open/merged/closed) - @author
```

When creating items, always report:
- The created item's number/ID.
- Direct URL to the item.
- Any relevant status information.

## Error Handling

### Common Errors and Solutions

| Error | Solution |
|-------|----------|
| `gh: command not found` | Install `gh` CLI: https://cli.github.com/ |
| `not logged in` | Run `gh auth login` |
| `HTTP 404` | Check repo/resource exists and you have access |
| `HTTP 403` | Check permissions/scopes, may need `gh auth refresh` |
| `HTTP 422` | Invalid parameters, check API docs |
| `rate limit exceeded` | Wait or authenticate for higher limits |

### Check Rate Limits
```bash
gh api rate_limit --jq '.resources.core | {limit: .limit, remaining: .remaining, reset: .reset}'
```

## Notes

- Always verify authentication before operations: `gh auth status`.
- Use `--json` flag for programmatic output.
- Use `--jq` for filtering JSON responses.
- Rate limits apply: 5000 requests/hour authenticated, 60/hour unauthenticated.