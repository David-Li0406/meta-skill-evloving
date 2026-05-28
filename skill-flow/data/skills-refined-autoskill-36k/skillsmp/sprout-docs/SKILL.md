---
name: sprout-docs
description: Generate folder-scoped README documentation for codebase exploration
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Task, TodoWrite
---

# Sprout Docs Skill

Generate navigable documentation for every folder in a repository. Output goes to a gitignored `sprout-docs/` folder for local exploration.

## Usage

```
/sprout-docs [path] [options]

Options:
  --depth <n>       Max folder depth (default: unlimited)
  --skip <pattern>  Additional folders to skip (comma-separated)
  --dry-run         Show what would be created without writing
```

## Overview

1. Creates `sprout-docs/` folder (gitignored)
2. Generates a doc file for each folder with navigation and contents
3. Tracks state in `sprout-docs/.state.json` for incremental updates

## Quick Reference

Runbook: `runbook/sprout-docs.md` in your knowledge base.

## Why Ephemeral?

- **No merge conflicts** - docs stay local, never committed
- **Zero maintenance** - regenerate anytime, delete when done
- **Exploration focused** - helps navigate unfamiliar codebases

## Progress Display

```
SPROUT DOCS: 15/23 folders
━━━━━━━━━━━━━━━━━━━━━░░░░░░░░ 65%

  ✓ src/components/
  ✓ src/utils/
  → src/hooks/
```
