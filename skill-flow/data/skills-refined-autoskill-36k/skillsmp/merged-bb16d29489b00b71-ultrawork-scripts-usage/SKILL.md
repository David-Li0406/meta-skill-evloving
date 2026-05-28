---
name: ultrawork-scripts-usage
description: Use this skill when you need to manage sessions, tasks, and context in ultrawork using scripts.
---

# Ultrawork Scripts Usage

## What is SCRIPTS_PATH?

`SCRIPTS_PATH` is the expanded absolute path to the ultrawork scripts directory, typically formatted as follows:
```
SCRIPTS_PATH: /Users/name/.claude/plugins/cache/ultrawork/0.26.0/src/scripts
```
Use this path to call Bun scripts in your commands.

## ⚠️ WARNING: Placeholder vs Bash Variable Syntax

**CRITICAL: `{SCRIPTS_PATH}` and `${CLAUDE_SESSION_ID}` are TEXT PLACEHOLDERS, not bash environment variables!** Replace these placeholders with actual values from your prompt before executing commands.

### Correct Usage

Your prompt provides actual values:
```
SCRIPTS_PATH: /Users/mnthe/.claude/plugins/cache/hardworker-marketplace/ultrawork/0.26.1/src/scripts
CLAUDE_SESSION_ID: 76dfec2a-4187-48eb-8073-9435f4386466
```

**Use the literal values in bash commands:**

✅ **CORRECT:**
```bash
bun "/Users/mnthe/.claude/plugins/cache/hardworker-marketplace/ultrawork/0.26.1/src/scripts/session-get.js" --session 76dfec2a-4187-48eb-8073-9435f4386466
```

### Incorrect Usage

❌ **WRONG - Don't use placeholder syntax in actual commands:**
```bash
bun "{SCRIPTS_PATH}/session-get.js" --session ${CLAUDE_SESSION_ID}
```

## Core Rules

1. **JSON via scripts, Markdown via Read** - Use scripts for accessing session.json, context.json, and tasks/*.json.
2. **Use `--field` for efficiency** - Extract only needed data instead of full JSON.
3. **Use `{SCRIPTS_PATH}` placeholder** - Substitute with the actual path from your prompt.
4. **Direct path for SESSION_DIR** - Use `~/.claude/ultrawork/sessions/${CLAUDE_SESSION_ID}` directly.

## Session Management Scripts

### Get Session Data

```bash
# Get full session JSON
bun "{SCRIPTS_PATH}/session-get.js" --session ${CLAUDE_SESSION_ID}

# Get specific field (more efficient)
bun "{SCRIPTS_PATH}/session-get.js" --session ${CLAUDE_SESSION_ID} --field phase
```

### Update Session State

```bash
# Update session phase
bun "{SCRIPTS_PATH}/session-update.js" --session ${CLAUDE_SESSION_ID} --phase EXECUTION
```

## Task Management Scripts

### Create Tasks

```bash
# Create standard task
bun "{SCRIPTS_PATH}/task-create.js" --session ${CLAUDE_SESSION_ID} \
  --id "1" \
  --subject "Add authentication middleware" \
  --description "Implement JWT-based auth in src/middleware/auth.ts"
```

### Get Task Details

```bash
# Get full task JSON
bun "{SCRIPTS_PATH}/task-get.js" --session ${CLAUDE_SESSION_ID} --id 1
```

### List Tasks

```bash
# List all tasks
bun "{SCRIPTS_PATH}/task-list.js" --session ${CLAUDE_SESSION_ID}
```

### Update Tasks

```bash
# Mark task resolved
bun "{SCRIPTS_PATH}/task-update.js" --session ${CLAUDE_SESSION_ID} --id 1 --status resolved
```

## Context Management Scripts

### Initialize Context

```bash
# Initialize with expected explorers
bun "{SCRIPTS_PATH}/context-init.js" --session ${CLAUDE_SESSION_ID} --expected "overview,exp-auth,exp-api"
```

### Get Context Data

```bash
# Get full context JSON
bun "{SCRIPTS_PATH}/context-get.js" --session ${CLAUDE_SESSION_ID}
```

## Common Patterns

### Worker Pattern

```bash
# 1. Get task details
bun "{SCRIPTS_PATH}/task-get.js" --session ${CLAUDE_SESSION_ID} --id {TASK_ID}

# 2. Mark in progress
bun "{SCRIPTS_PATH}/task-update.js" --session ${CLAUDE_SESSION_ID} --id {TASK_ID} --add-evidence "Starting implementation at $(date -u +%Y-%m-%dT%H:%M:%SZ)"
```

### Planner Pattern

```bash
# 1. Read session goal
bun "{SCRIPTS_PATH}/session-get.js" --session ${CLAUDE_SESSION_ID} --field goal
```

### Verifier Pattern

```bash
# 1. List tasks
bun "{SCRIPTS_PATH}/task-list.js" --session ${CLAUDE_SESSION_ID}
```

### Explorer Pattern

```bash
# 1. Read exploration context
bun "{SCRIPTS_PATH}/context-get.js" --session ${CLAUDE_SESSION_ID}
```

## Quick Reference

| Data | Access Method |
|------|---------------|
| session.json | `bun "{SCRIPTS_PATH}/session-get.js" --session ${CLAUDE_SESSION_ID}` |
| context.json | `bun "{SCRIPTS_PATH}/context-get.js" --session ${CLAUDE_SESSION_ID}` |
| tasks/*.json | `bun "{SCRIPTS_PATH}/task-get.js" --session ${CLAUDE_SESSION_ID} --id N` |
| task list | `bun "{SCRIPTS_PATH}/task-list.js" --session ${CLAUDE_SESSION_ID}` |
| exploration/*.md | `Read("~/.claude/ultrawork/sessions/${CLAUDE_SESSION_ID}/exploration/file.md")` |

---

## Why Scripts Over Direct Read?

1. **Token efficiency**: JSON wastes tokens on structure.
2. **Field extraction**: Scripts return only needed data.
3. **Consistent error handling**: Validation and error messages.
4. **Abstraction**: Storage format changes don't affect agents.