---
name: gh-project-ops
description: GitHub Project operations including fetching project items, tracking status changes, and getting project fields. Use when working with GitHub Projects, checking progress, or building status reports.
allowed-tools: Bash, Read
---

# GitHub Project Operations

Provides scripts for GitHub Projects V2 operations. Uses config from `.claude/gh-config.json` if present.

## Config File

Scripts look for `.claude/gh-config.json` in the repo root:
```json
{
  "project": {
    "org": "orgname",
    "number": 1
  }
}
```

If not found, scripts will prompt or auto-detect.

## Available Scripts

### get-project-items.sh [project-number]
Returns all items in a project with their status.
```bash
~/.claude/skills/gh-project-ops/scripts/get-project-items.sh 1
```

### get-status-changes-today.sh [project-number]
Returns issues that had status changes today.
```bash
~/.claude/skills/gh-project-ops/scripts/get-status-changes-today.sh 1
```

### get-project-fields.sh [project-number]
Returns available fields and options for a project.
```bash
~/.claude/skills/gh-project-ops/scripts/get-project-fields.sh 1
```

## Usage

If `.claude/gh-config.json` exists, project number is optional:
```bash
bash ~/.claude/skills/gh-project-ops/scripts/get-project-items.sh
```

Otherwise, provide project number as argument.
