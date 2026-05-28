---
name: gh-cli
description: Use this skill when working with GitHub from the command line for operations involving repositories, pull requests, issues, workflows, releases, and API interactions.
---

# GitHub CLI (gh) Reference

The `gh` CLI is GitHub's official command-line tool, allowing seamless interaction with GitHub repositories, pull requests, issues, workflows, and more.

## Quick Start

```bash
# Authenticate
gh auth login

# Check authentication status
gh auth status
```

## Command Reference

### Authentication (`gh auth`)

| Command | Description |
|---------|-------------|
| `gh auth login` | Authenticate with GitHub |
| `gh auth logout` | Log out of GitHub |
| `gh auth refresh` | Refresh stored credentials |
| `gh auth setup-git` | Configure git to use gh as credential helper |
| `gh auth status` | View authentication status |
| `gh auth switch` | Switch between accounts |
| `gh auth token` | Print or manage auth tokens |

### Pull Requests (`gh pr`)

| Command | Description |
|---------|-------------|
| `gh pr create` | Create a pull request |
| `gh pr list` | List pull requests |
| `gh pr view [number]` | View PR details |
| `gh pr checkout <number>` | Check out a PR branch |
| `gh pr merge [number]` | Merge a PR |
| `gh pr close [number]` | Close a PR |
| `gh pr reopen [number]` | Reopen a PR |
| `gh pr edit [number]` | Edit PR title, body, labels, etc. |
| `gh pr comment [number]` | Add a comment |
| `gh pr review [number]` | Submit a review |
| `gh pr diff [number]` | View PR diff |
| `gh pr status` | Show PR status for current branch |

**Common PR Workflows:**

```bash
# Create PR interactively
gh pr create --fill

# View and checkout
gh pr list
gh pr view [NUMBER]
gh pr checkout NUMBER

# Review and merge
gh pr review NUMBER --approve
gh pr merge --squash --delete-branch
```

### Issues (`gh issue`)

| Command | Description |
|---------|-------------|
| `gh issue create` | Create an issue |
| `gh issue list` | List issues |
| `gh issue view <number>` | View issue details |
| `gh issue close <number>` | Close an issue |
| `gh issue reopen <number>` | Reopen an issue |
| `gh issue edit <number>` | Edit issue |
| `gh issue comment <number>` | Add a comment |
| `gh issue delete <number>` | Delete an issue |
| `gh issue develop <number>` | Create linked branch |

**Common Issue Workflows:**

```bash
# Create issue interactively
gh issue create --title "Bug" --body "Description here"

# List open issues assigned to me
gh issue list --assignee @me
```

### Repositories (`gh repo`)

| Command | Description |
|---------|-------------|
| `gh repo create` | Create a repository |
| `gh repo clone <repo>` | Clone a repository |
| `gh repo fork [repo]` | Fork a repository |
| `gh repo view [repo]` | View repo details |
| `gh repo list [owner]` | List repositories |
| `gh repo edit` | Edit repo settings |
| `gh repo delete <repo>` | Delete a repository |

**Common Repo Workflows:**

```bash
# Create new repo from current directory
gh repo create --source=. --push

# Clone and cd into repo
gh repo clone owner/repo
```

### Workflows & Actions (`gh workflow`, `gh run`)

| Command | Description |
|---------|-------------|
| `gh workflow list` | List workflows |
| `gh workflow view [id]` | View workflow details |
| `gh workflow run <workflow>` | Trigger a workflow |
| `gh run list` | List recent runs |
| `gh run view [id]` | View run details |
| `gh run watch [id]` | Watch run in real-time |

### Releases (`gh release`)

| Command | Description |
|---------|-------------|
| `gh release create <tag>` | Create a release |
| `gh release list` | List releases |
| `gh release view [tag]` | View release details |
| `gh release delete <tag>` | Delete a release |

### Search (`gh search`)

| Command | Description |
|---------|-------------|
| `gh search repos <query>` | Search repositories |
| `gh search issues <query>` | Search issues |
| `gh search prs <query>` | Search pull requests |

### Codespaces (`gh codespace`)

| Command | Description |
|---------|-------------|
| `gh codespace create` | Create a codespace |
| `gh codespace list` | List codespaces |
| `gh codespace code` | Open in VS Code |
| `gh codespace ssh` | SSH into codespace |

### API (`gh api`)

Make authenticated requests to GitHub's REST or GraphQL API.

```bash
gh api <endpoint> [flags]
```

**Key flags:**

| Flag | Description |
|------|-------------|
| `-X, --method` | HTTP method (GET, POST, etc.) |
| `-f, --raw-field` | Add string parameter |
| `-H, --header` | Add HTTP header |
| `-q, --jq` | Filter response with jq |

## Global Flags

These work with most commands:

| Flag | Description |
|------|-------------|
| `-R, --repo [HOST/]OWNER/REPO` | Target a specific repository |
| `--help` | Show help |
| `--version` | Show version |

## Environment Variables

| Variable | Description |
|----------|-------------|
| `GH_TOKEN` | Authentication token |
| `GH_REPO` | Default repository (OWNER/REPO format) |
| `GH_EDITOR` | Preferred editor for interactive commands |

## Tips

1. **Use `--web`** to open in browser: `gh pr view --web`
2. **Use `@me`** for current user: `gh issue list --assignee @me`
3. **Use jq filtering** for JSON output: `gh api user -q '.login'`
4. **Tab completion** - run `gh completion` and follow instructions
5. **Aliases** - create shortcuts: `gh alias set pv 'pr view'`

## Resources

- [Official Manual](https://cli.github.com/manual/)
- [GitHub Docs](https://docs.github.com/en/github-cli)