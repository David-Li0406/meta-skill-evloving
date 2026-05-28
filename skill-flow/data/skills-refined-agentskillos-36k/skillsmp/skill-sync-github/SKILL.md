---
name: skill-sync-github
description: Synchronizes OpenCode skills with GitHub repository
metadata:
  short-description: Sync skills with GitHub
---

# Sync Skills

## Description
Synchronizes local OpenCode skills with the GitHub repository. Fetches remote changes, commits local changes, and pushes to GitHub.

## Usage
```
skill sync-skills
```

## What it does
1. Fetches latest changes from GitHub
2. Commits any local changes (skills, opencode.jsonc)
3. Pushes to GitHub
4. Pulls remote changes with rebase
