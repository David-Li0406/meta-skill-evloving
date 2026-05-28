---
name: github-cli
description: Use this skill when you need to interact with GitHub from the command line, managing repositories, pull requests, issues, and more using the GitHub CLI (gh).
---

# GitHub CLI (gh) Reference

The GitHub CLI (gh) is the official command-line tool for GitHub, allowing you to manage repositories, pull requests, issues, and other GitHub operations directly from your terminal.

## Prerequisites

### Installation

```bash
# macOS
brew install gh

# Linux
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh

# Windows
winget install --id GitHub.cli

# Verify installation
gh --version
```

### Authentication

```bash
# Authenticate with GitHub
gh auth login

# Check authentication status
gh auth status

# Logout
gh auth logout
```

## Common Commands

### Pull Requests

```bash
# Create a pull request
gh pr create --title "Title" --body "Description"

# List pull requests
gh pr list

# View a pull request
gh pr view [NUMBER]

# Checkout a pull request
gh pr checkout [NUMBER]

# Merge a pull request
gh pr merge [NUMBER] --squash
```

### Issues

```bash
# Create an issue
gh issue create --title "Title" --body "Description"

# List issues
gh issue list

# View an issue
gh issue view [NUMBER]

# Close an issue
gh issue close [NUMBER]
```

## Additional Features

- Use `gh <command> --help` for help on specific commands.
- Use `gh <command> --web` to open a command in the browser.
- Use tab completion to explore available commands and flags.

For comprehensive documentation, visit [GitHub CLI Manual](https://cli.github.com/manual).