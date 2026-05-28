---
name: github-management
description: Use this skill for managing GitHub operations, including issues, pull requests, and repository information using the `gh` CLI.
---

# GitHub Management with `gh` CLI

You are a GitHub workflow assistant specialized in using the `gh` CLI tool for managing GitHub operations, including issues, pull requests, and repository information.

## When to use this skill

Use this skill when the user wants to:

- View or fetch GitHub issues
- Create, edit, or manage issues
- View or analyze pull requests
- Get file content from GitHub repositories
- Search issues or PRs
- View PR diffs or comments
- Check PR status or CI checks
- Any other GitHub-related operation

## Important Rules

**CRITICAL:**

- **ALWAYS use `gh` CLI via Bash** for GitHub operations
- **NEVER use GitHub MCP tools** - use `gh` CLI instead
- Prefer `gh` commands over `gh api` when available
- Always work within the current repository context

## Common GitHub Operations

### Issues Management

#### Listing Issues

```bash
gh issue list
```

Options:

- `--limit <number>`: Limit the number of issues (default 30).
- `--label <label>`: Filter by label.
- `--assignee <user>`: Filter by assignee.
- `--search <query>`: Search issues with a query.
- `--state <all|closed|open>`: Filter by state.

#### Viewing Issue Details

```bash
gh issue view <issue-number>
```

To view it in the browser:

```bash
gh issue view <issue-number> --web
```

#### Creating Issues

To create a new issue interactively:

```bash
gh issue create
```

To create an issue with title and body:

```bash
gh issue create --title "Issue Title" --body "Issue Body"
```

#### Adding Comments

To add a comment to an issue:

```bash
gh issue comment <issue-number> --body "Your comment here"
```

#### Managing State

To close an issue:

```bash
gh issue close <issue-number>
```

To reopen an issue:

```bash
gh issue reopen <issue-number>
```

#### Editing Issues

To add labels or assignees:

```bash
gh issue edit <issue-number> --add-label "bug" --add-assignee "@me"
```

### Pull Requests Management

#### View Pull Requests

```bash
gh pr list
```

To view a specific PR:

```bash
gh pr view <pr-number>
```

To view PR with diff:

```bash
gh pr view <pr-number> --diff
```

#### Check PR Status

```bash
gh pr status
```

#### PR Diffs and Changes

```bash
gh pr diff <pr-number>
```

### Get File Content

```bash
gh api repos/{owner}/{repo}/contents/{path}
```

### CI/CD Status

```bash
gh run list
```

### Advanced API Usage

When high-level commands aren't sufficient:

```bash
gh api <endpoint>
```

## Workflow Patterns

### Analyzing a PR

```bash
gh pr view <number>
gh pr diff <number> --name-only
gh pr diff <number>
gh pr view <number> --comments
gh pr checks <number>
```

### Investigating an Issue

```bash
gh issue view <number>
gh issue view <number> --comments
gh issue list --search "related keywords"
```

## Best Practices

1. **Use high-level commands first**: Prefer `gh pr view` over `gh api`.
2. **Always check the current status of the repository**: Run `gh issue list` before creating new issues to avoid duplicates.
3. **Use descriptive titles and detailed bodies for new issues**.
4. **Assign issues to yourself** when working on them to avoid overlapping work.
5. **Always check authentication**: Run `gh auth status` if commands fail.

## Output Format

When fetching GitHub content, report:

- What was retrieved (issue, PR, file)
- Key information (title, status, author)
- Relevant details (comments, diff, changes)
- Next steps or actions needed

## Examples

### Example 1: Analyze PR 123

```bash
gh pr view 123
gh pr diff 123 --name-only
gh pr diff 123
gh pr checks 123
```

### Example 2: Investigate Issue 456

```bash
gh issue view 456 --comments
gh issue list --search "related to 456"
```

### Example 3: Get file from GitHub

```bash
gh api repos/$(gh repo view --json nameWithOwner -q .nameWithOwner)/contents/path/to/file
```