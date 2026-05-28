---
name: github-cli
description: Use this skill when working with GitHub CLI (`gh`) for managing pull requests, issues, releases, and automating GitHub workflows from the command line.
---

# GitHub CLI (gh) Comprehensive Skill

Master the GitHub CLI (`gh`) to seamlessly work with GitHub from the command line. This skill covers all major GitHub operations including repository management, issues, pull requests, releases, authentication, and more.

## When to Use This Skill

Trigger this skill when the user asks to:
- "Create a PR/issue/release"
- "Manage GitHub repository"
- "Clone/fork/update a repo"
- "Check/authenticate with gh"
- "Work with GitHub Actions"
- "Manage codespaces"
- "Search repos/issues/PRs"
- Any GitHub CLI operation

## Prerequisites

### Installation & Authentication

**Check if gh is installed:**
```bash
gh --version
```

**Install gh (if not installed):**
```bash
# macOS
brew install gh

# Windows (winget)
winget install --id GitHub.cli

# Linux
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh
```

**Authenticate with GitHub:**
```bash
gh auth login
# Follow prompts:
# - GitHub.com
# - HTTPS protocol
# - Login with web browser OR token
```

**Verify authentication:**
```bash
gh auth status
```

## Core Command Categories

### 1. Repository Management

#### View Repository Info

```bash
# View current repository
gh repo view

# View specific repository
gh repo view owner/repo

# Open repository in browser
gh repo view --web
```

#### Clone Repository

```bash
# Clone current repository (if in directory)
gh repo clone

# Clone specific repository
gh repo clone owner/repo
```

#### Create Repository

```bash
# Create new repository (interactive)
gh repo create

# Create with specific settings
gh repo create my-repo --public --description "My awesome repository" --source=. --remote=origin --push
```

### 2. Issue Management

#### List Issues

```bash
# List issues in current repository
gh issue list

# List with filters
gh issue list --state open --author masx200 --label bug,enhancement --limit 20
```

#### Create Issue

```bash
# Create interactively
gh issue create

# Create with title and body
gh issue create --title "Bug in authentication" --body "Detailed description of the bug"
```

### 3. Pull Request Management

#### List Pull Requests

```bash
# List PRs in current repository
gh pr list

# List with filters
gh pr list --state open --author masx200 --base main --limit 20
```

#### Create Pull Request

```bash
# Create PR interactively
gh pr create

# Create with title and body
gh pr create --title "Add new feature" --body "Description of changes"
```

### 4. GitHub Actions Management

#### List Workflow Runs

```bash
# List recent workflow runs
gh run list

# List for specific workflow
gh run list --workflow "ci.yml"
```

#### View Run Details

```bash
# View run details
gh run view 123456789

# View with logs
gh run view 123456789 --log
```

### 5. Release Management

#### List Releases

```bash
# List releases
gh release list

# List with limit
gh release list --limit 20
```

#### Create Release

```bash
# Create release
gh release create v1.0.0 --title "Version 1.0.0" --notes "Release notes here"
```

### 6. Search & Browse

#### Search Repositories

```bash
# Search repositories
gh search repos "http proxy"
```

### 7. Authentication Management

#### Login/Logout

```bash
# Login
gh auth login

# Logout
gh auth logout
```

## Common Workflows & Examples

### Workflow 1: Complete PR Creation Flow

```bash
# 1. Update main branch
git checkout main
git pull

# 2. Create feature branch
git checkout -b feature/new-feature

# 3. Make changes and commit
git add .
git commit -m "feat: Add new feature"

# 4. Push to remote
git push -u origin feature/new-feature

# 5. Create PR with reviewers
gh pr create --title "Add new feature" --body "Detailed description" --reviewer username1,username2 --label enhancement

# 6. View PR status
gh pr status
```

### Workflow 2: Issue Triage

```bash
# 1. List open issues
gh issue list --state open --limit 50

# 2. View specific issue
gh issue view 123

# 3. Add label and assign
gh issue edit 123 --add-label "bug,priority-high" --add-assignee @me

# 4. Comment on issue
gh issue comment 123 --body "Working on this"
```

## Tips & Best Practices

### DO ✅

1. **Use aliases** for frequently used commands
2. **Enable shell completion** for better productivity
3. **Use JSON output** with `jq` for scripting
4. **Create templates** for common PR/issue descriptions

### DON'T ❌

1. **NEVER hardcode tokens** - let gh handle authentication
2. **DON'T ignore errors** - check exit codes and handle failures
3. **NEVER commit secrets** - use gh secret for sensitive data

## Troubleshooting

### Issue: "gh not found"

**Solution:**
```bash
# Check if gh is installed
which gh
```

### Issue: "gh: not logged in"

**Solution:**
```bash
gh auth login
gh auth status  # Verify
```

### Issue: "Permission denied"

**Solution:**
```bash
# Check permissions
gh repo view
```

## Additional Resources

- [Official GitHub CLI Documentation](https://cli.github.com/manual/)
- [GitHub Blog - Introducing gh CLI](https://github.blog/2020-09-17-introducing-github-cli/)

---

This skill provides a comprehensive guide to using the GitHub CLI for various operations, ensuring users can effectively manage their GitHub workflows from the command line.