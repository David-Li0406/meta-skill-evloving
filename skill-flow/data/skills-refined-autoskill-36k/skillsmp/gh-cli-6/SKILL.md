---
name: gh-cli
description: Use when interacting with GitHub - searching for repos/orgs/packages, exploring codebases, finding projects to use, querying branches/PRs/issues/releases/workflows, automating GitHub operations, or when users mention GitHub organizations or repositories
---

> **CRITICAL:** You MUST use the Task tool with `subagent_type: "general"` to execute GitHub CLI commands. NEVER run `gh` commands directly in your bash session.

Example Task invocation:
```
Task(subagent_type="general", prompt="Use gh CLI to list branches: gh branch list --json name,updatedAt")
```

This preserves conversation context and isolates CLI output.

---

# GitHub CLI (gh)

Command-line interface for GitHub. Use `--json <fields>` with `--jq` for scriptable output.

## Quick Reference

| Task | Command |
|------|---------|
| List my PRs | `gh pr list --author @me` |
| View PR | `gh pr view <number>` |
| Create PR | `gh pr create --fill` |
| Checkout PR | `gh pr checkout <number>` |
| List issues | `gh issue list` |
| View issue | `gh issue view <number>` |
| Create issue | `gh issue create --title "..." --body "..."` |
| Repo info | `gh repo view` |
| Clone repo | `gh repo clone <owner/repo>` |
| List releases | `gh release list` |
| Workflow runs | `gh run list` |
| View run | `gh run view <run-id>` |
| Search repos | `gh search repos <query>` |
| Search code | `gh search code <query>` |
| API request | `gh api <endpoint>` |
| My status | `gh status` |
| Auth status | `gh auth status` |

## Core Commands

| Command | Description |
|---------|-------------|
| `gh repo` | Manage repositories (create, clone, fork, view, delete, edit) |
| `gh pr` | Manage pull requests (create, list, view, checkout, merge, close) |
| `gh issue` | Manage issues (create, list, view, edit, close, comment) |
| `gh release` | Manage releases (create, list, view, download, delete) |
| `gh gist` | Manage gists (create, list, view, edit, delete) |
| `gh project` | Work with GitHub Projects |

## GitHub Actions

| Command | Description |
|---------|-------------|
| `gh run list` | List recent workflow runs |
| `gh run view` | View a workflow run |
| `gh run watch` | Watch a run until completion |
| `gh run rerun` | Rerun a workflow |
| `gh workflow list` | List workflows |
| `gh workflow run` | Trigger a workflow |
| `gh cache list` | List Actions caches |

## Additional Commands

| Command | Description |
|---------|-------------|
| `gh search` | Search repos, issues, PRs, commits, code |
| `gh api` | Make authenticated API requests |
| `gh auth` | Manage authentication (login, logout, status) |
| `gh config` | Manage configuration |
| `gh secret` | Manage repository/org secrets |
| `gh variable` | Manage Actions variables |
| `gh label` | Manage issue labels |
| `gh ruleset` | View repository rulesets |

For detailed flags and examples, see pr-commands.md, issue-commands.md, repo-commands.md, actions-commands.md, and other-commands.md in this skill directory.

## Output Flags

| Flag | Description |
|------|-------------|
| `--json <fields>` | Output JSON with specified fields |
| `-q, --jq <expr>` | Filter JSON output with jq expression |
| `-t, --template` | Format output with Go template |
| `-w, --web` | Open in browser |

## Global Flags

| Flag | Description |
|------|-------------|
| `-R, --repo OWNER/REPO` | Select repository |
| `--help` | Help for any command |
