---
name: github-cli
description: Interact with GitHub via the command line (PRs, Issues, Releases).
---

# GitHub CLI Skill

## Prerequisite
- **Local Path**: Ensure `gh` is in your PATH.
- **Usage**: Run `gh` commands directly (e.g., `gh issue list`).
- **Auth**: Ensure you are authenticated. Run `gh auth status`. If not, run `gh auth login`.

## Pull Requests
- **Create PR**:
  ```bash
  gh pr create --title "type(scope): description" --body "Detailed description"
  ```
- **View PR**: `gh pr view [number|url] --web`
- **Check Status**: `gh pr status`
- **Checkout PR**: `gh pr checkout [number]`
- **List PRs**: `gh pr list`

## Issues
- **List Issues**: `gh issue list`
- **Create Issue**: `gh issue create --title "..." --body "..."`

## Actions
- **List Runs**: `gh run list`
- **Watch Run**: `gh run watch [run-id]`

## Best Practices
- **Non-Interactive**: Use flags (`--title`, `--body`, `--yes`) to avoid interactive prompts when running from scripts/agent.
- **Web Flag**: Use `--web` when asking the user to review something in the browser.
- **JSON Output**: Use `--json [fields]` to get machine-readable output.
