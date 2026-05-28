---
name: scripts-path-usage
description: |
  This skill provides guidance for teamwork agents on using SCRIPTS_PATH and accessing project data via scripts.
  Required knowledge for all teamwork agents (orchestrator, workers, verifiers).
---

# Scripts Path Usage

## What is SCRIPTS_PATH?

`SCRIPTS_PATH` is the expanded absolute path of `${CLAUDE_PLUGIN_ROOT}/src/scripts`.

Your prompt includes it like this:
```
SCRIPTS_PATH: /Users/name/.claude/plugins/cache/teamwork/0.20.0/src/scripts
```

Use this path to call Bun scripts.

## Core Rules

1. **JSON via scripts, Markdown via Read** - Use `project-get.js`, `task-get.js` for JSON access
2. **Always pass `--project` and `--team`** - Required for all teamwork scripts

## Quick Reference

| Data | Access Method |
|------|---------------|
| project.json | `bun "{SCRIPTS_PATH}/project-get.js" --project {PROJECT} --team {TEAM}` |
| tasks/*.json | `bun "{SCRIPTS_PATH}/task-get.js" --project {PROJECT} --team {TEAM} --id 1` |
| waves.json | `bun "{SCRIPTS_PATH}/wave-status.js" --project {PROJECT} --team {TEAM}` |
