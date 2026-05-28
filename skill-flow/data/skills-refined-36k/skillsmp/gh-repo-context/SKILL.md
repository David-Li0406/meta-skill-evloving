---
name: gh-repo-context
description: Get GitHub repository context including owner, repo name, available issue types, labels, and linked projects. Use when you need to fetch repo metadata or discover available options for issues/projects.
allowed-tools: Bash, Read
---

# GitHub Repository Context

Provides scripts to dynamically fetch repository information. All scripts auto-detect the current repo.

## Available Scripts

### get-repo-info.sh
Returns owner, repo name, and default branch.
```bash
~/.claude/skills/gh-repo-context/scripts/get-repo-info.sh
```

### get-issue-types.sh
Returns available issue types with their IDs.
```bash
~/.claude/skills/gh-repo-context/scripts/get-issue-types.sh
```

### get-labels.sh
Returns available labels for the repo.
```bash
~/.claude/skills/gh-repo-context/scripts/get-labels.sh
```

### get-projects.sh
Returns linked projects with their numbers.
```bash
~/.claude/skills/gh-repo-context/scripts/get-projects.sh
```

## Usage

Run scripts directly to get JSON output:
```bash
bash ~/.claude/skills/gh-repo-context/scripts/get-issue-types.sh
```

All scripts require being in a git repo with a GitHub remote.
