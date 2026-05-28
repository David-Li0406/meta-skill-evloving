---
name: github
description: GitHub workflow best practices using gh CLI and git. Use when working with GitHub repositories, pull requests, issues, or GitHub interactions.
---
# GitHub

- Prefer using `gh` CLI commands for all GitHub operations including viewing issues, PRs, repos, and discussions.
- Use `gh issue view`, `gh pr view`, `gh repo view` to inspect GitHub resources instead of web search.
- When given a GitHub URL (e.g., https://github.com/user/repo/issues/123), extract the info and use `gh` to fetch the issue/PR data.
- Use `gh api` for advanced GitHub API interactions that are not natively supported by `gh` commands.
- Always assume GitHub URLs may refer to private repositories and use `gh` for authentication.
- Use `git` for all local git operations (clone, branch, commit, push, etc.).

## When to Use gh CLI

Use `gh` for:
- Viewing issues: `gh issue view <number> --repo owner/repo`
- Viewing PRs: `gh pr view <number> --repo owner/repo`
- Searching issues/PRs: `gh issue list --repo owner/repo --search "query"`
- Viewing repository info: `gh repo view owner/repo`
- Creating PRs: `gh pr create`
- Creating issues: `gh issue create`
- Checking CI status: `gh run list`, `gh run view`
- Viewing workflows: `gh workflow list`, `gh workflow view`
- Creating releases: `gh release create`

## Workflows

### Pull Request

- You must `git push` a branch before creating a pull request with `gh pr create`.
- Use `gh pr create` with appropriate flags for title, body, reviewers, etc.

### Viewing Issues from URLs

When given a GitHub issue URL like `https://github.com/owner/repo/issues/123`:
1. Extract owner, repo, and issue number
2. Run `gh issue view 123 --repo owner/repo`
3. Use the issue data instead of web search

### Viewing PRs from URLs

When given a GitHub PR URL like `https://github.com/owner/repo/pull/456`:
1. Extract owner, repo, and PR number
2. Run `gh pr view 456 --repo owner/repo`
3. Use the PR data instead of web search

### Searching Issues

Use `gh issue list` to search:
```bash
gh issue list --repo owner/repo --search "bug"
gh issue list --repo owner/repo --search "is:open label:enhancement"
```

### Searching PRs

Use `gh pr list` to search:
```bash
gh pr list --repo owner/repo --search "is:open"
gh pr list --repo owner/repo --search "base:main"
```

## Common Commands

### Repository Info
```bash
gh repo view owner/repo
gh repo view owner/repo --json name,description,topics,stars
```

### Issues
```bash
gh issue list --repo owner/repo
gh issue view 123 --repo owner/repo
gh issue create --repo owner/repo --title "Title" --body "Body"
```

### Pull Requests
```bash
gh pr list --repo owner/repo
gh pr view 456 --repo owner/repo
gh pr create --base main --title "Title" --body "Body"
```

### CI/Workflows
```bash
gh workflow list --repo owner/repo
gh run list --repo owner/repo
gh run view run-id --repo owner/repo --log
```

## Keywords
GitHub, issue, pull request, PR, repository, repo, gh, git, GitHub CLI, GitHub API, workflow, release, CI/CD
