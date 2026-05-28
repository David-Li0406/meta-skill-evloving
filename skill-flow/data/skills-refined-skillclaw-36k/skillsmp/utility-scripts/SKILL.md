---
name: utility-scripts
description: |
  Comprehensive guide for ultrawork agents on using session, task, and context management scripts.
  Covers all common script patterns with $SCRIPTS_PATH variable usage.
  Required for explorer, planner, worker, verifier, and reviewer agents.
---

# Ultrawork Utility Scripts

> **IMPORTANT: Placeholder Notation**
>
> This document uses `{SCRIPTS_PATH}` and `${CLAUDE_SESSION_ID}` as **text placeholders** that represent values provided in your agent prompt.
>
> - `{SCRIPTS_PATH}` → Replace with the actual `SCRIPTS_PATH` value from your prompt
> - `${CLAUDE_SESSION_ID}` → Replace with the actual `CLAUDE_SESSION_ID` value from your prompt
>
> These are NOT bash environment variables (not `$SCRIPTS_PATH` or `${CLAUDE_SESSION_ID}`).
> When you see `bun "{SCRIPTS_PATH}/script.js"`, substitute the actual path like:
> ```bash
> bun "/Users/name/.claude/plugins/.../src/scripts/script.js"
> ```

## What is SCRIPTS_PATH?

`SCRIPTS_PATH` is the expanded absolute path to ultrawork scripts directory.

Your prompt includes it like this:
```
SCRIPTS_PATH: /Users/name/.claude/plugins/cache/hardworker-marketplace/ultrawork/0.26.0/src/scripts
```

Use `{SCRIPTS_PATH}` as a placeholder (substitute with actual value from your prompt) when calling Bun scripts in bash commands.

---

## Session Management Scripts

### Get Session Data

```bash
# Get full session JSON
bun "{SCRIPTS_PATH/session-get.js" --session ${CLAUDE_SESSION_ID}

# Get specific field (more efficient)
bun "{SCRIPTS_PATH/session-get.js" --session ${CLAUDE_SESSION_ID} --field phase
bun "{SCRIPTS_PATH/session-get.js" --session ${CLAUDE_SESSION_ID} --field goal
bun "{SCRIPTS_PATH/session-get.js" --session ${CLAUDE_SESSION_ID} --field working_dir

# Get session directory path (direct variable)
SESSION_DIR=~/.claude/ultrawork/sessions/${CLAUDE_SESSION_ID}
```

### Update Session State

```bash
# Update session phase
bun "{SCRIPTS_PATH/session-update.js" --session ${CLAUDE_SESSION_ID} --phase EXECUTION
bun "{SCRIPTS_PATH/session-update.js" --session ${CLAUDE_SESSION_ID} --phase VERIFICATION
bun "{SCRIPTS_PATH/session-update.js" --session ${CLAUDE_SESSION_ID} --phase COMPLETE

# Mark plan approved
bun "{SCRIPTS_PATH/session-update.js" --session ${CLAUDE_SESSION_ID} --plan-approved

# Update exploration stage
bun "{SCRIPTS_PATH/session-update.js" --session ${CLAUDE_SESSION_ID} --exploration-stage complete
```

---

## Task Management Scripts

### Create Tasks

```bash
# Create standard task
bun "{SCRIPTS_PATH/task-create.js" --session ${CLAUDE_SESSION_ID} \
  --id "1" \
  --subject "Add authentication middleware" \
  --description "Implement JWT-based auth in src/middleware/auth.ts" \
  --complexity standard \
  --criteria "Middleware created|Tests pass 5/5|Handles invalid tokens"

# Create complex task (uses Opus model)
bun "{SCRIPTS_PATH/task-create.js" --session ${CLAUDE_SESSION_ID} \
  --id "2" \
  --subject "Design API architecture" \
  --complexity complex \
  --criteria "Architecture documented|Security review passed"

# Create TDD task
bun "{SCRIPTS_PATH/task-create.js" --session ${CLAUDE_SESSION_ID} \
  --id "3" \
  --subject "Validate user input" \
  --approach tdd \
  --criteria "Test created first|Test failed|Implementation passes"

# Create task with dependencies
bun "{SCRIPTS_PATH/task-create.js" --session ${CLAUDE_SESSION_ID} \
  --id "4" \
  --subject "Update frontend" \
  --blocked-by "1,2,3" \
  --criteria "UI updated|Tests pass"
```

### Get Task Details

```bash
# Get full task JSON
bun "{SCRIPTS_PATH/task-get.js" --session ${CLAUDE_SESSION_ID} --id 1

# Get specific field (more efficient)
bun "{SCRIPTS_PATH/task-get.js" --session ${CLAUDE_SESSION_ID} --id 1 --field status
bun "{SCRIPTS_PATH/task-get.js" --session ${CLAUDE_SESSION_ID} --id 1 --field evidence

# Alias: --task-id or --task also work
bun "{SCRIPTS_PATH/task-get.js" --session ${CLAUDE_SESSION_ID} --task 1
```

### List Tasks

```bash
# List all tasks
bun "{SCRIPTS_PATH/task-list.js" --session ${CLAUDE_SESSION_ID}

# Filter by status
bun "{SCRIPTS_PATH/task-list.js" --session ${CLAUDE_SESSION_ID} --status open
bun "{SCRIPTS_PATH/task-list.js" --session ${CLAUDE_SESSION_ID} --status resolved

# Output format
bun "{SCRIPTS_PATH/task-list.js" --session ${CLAUDE_SESSION_ID} --format json
bun "{SCRIPTS_PATH/task-list.js" --session ${CLAUDE_SESSION_ID} --format table
```

### Update Tasks

```bash
# Mark task resolved
bun "{SCRIPTS_PATH/task-update.js" --session ${CLAUDE_SESSION_ID} --id 1 \
  --status resolved

# Add evidence
bun "{SCRIPTS_PATH/task-update.js" --session ${CLAUDE_SESSION_ID} --id 1 \
  --add-evidence "Created src/middleware/auth.ts"

# Combine status and evidence
bun "{SCRIPTS_PATH/task-update.js" --session ${CLAUDE_SESSION_ID} --id 1 \
  --status resolved \
  --add-evidence "Tests pass: 5/5" \
  --add-evidence "Exit code: 0"

# Update verify task
bun "{SCRIPTS_PATH/task-update.js" --session ${CLAUDE_SESSION_ID} --id verify \
  --status resolved \
  --add-evidence "VERDICT: PASS"

# Alias: --task-id or --task also work
bun "{SCRIPTS_PATH/task-update.js" --session ${CLAUDE_SESSION_ID} --task 1 --status resolved
```

---

## Context Management Scripts

### Initialize Context

```bash
# Initialize with expected explorers
bun "{SCRIPTS_PATH/context-init.js" --session ${CLAUDE_SESSION_ID} \
  --expected "overview,exp-auth,exp-api"
```

### Add Explorer Summaries

```bash
# Add exploration summary
bun "{SCRIPTS_PATH/context-add.js" --session ${CLAUDE_SESSION_ID} \
  --explorer-id "overview" \
  --summary "Next.js 14 app with TypeScript, using App Router" \
  --key-files "app/layout.tsx,src/lib/auth.ts"

# Add targeted exploration
bun "{SCRIPTS_PATH/context-add.js" --session ${CLAUDE_SESSION_ID} \
  --explorer-id "exp-auth" \
  --summary "Found NextAuth.js setup in app/api/auth/"
```

### Get Context Data

```bash
# Get full context JSON
bun "{SCRIPTS_PATH/context-get.js" --session ${CLAUDE_SESSION_ID}

# Get specific field
bun "{SCRIPTS_PATH/context-get.js" --session ${CLAUDE_SESSION_ID} --field explorers
bun "{SCRIPTS_PATH/context-get.js" --session ${CLAUDE_SESSION_ID} --field key_files

# Get AI-friendly markdown summary
bun "{SCRIPTS_PATH/context-get.js" --session ${CLAUDE_SESSION_ID} --summary
```

---

## Common Patterns

### Worker Pattern

```bash
# 1. Get task details
bun "{SCRIPTS_PATH/task-get.js" --session ${CLAUDE_SESSION_ID} --id {TASK_ID}

# 2. Mark in progress
bun "{SCRIPTS_PATH/task-update.js" --session ${CLAUDE_SESSION_ID} --id {TASK_ID} \
  --add-evidence "Starting implementation at $(date -u +%Y-%m-%dT%H:%M:%SZ)"

# 3. Implement and collect evidence
# ... (use Read, Write, Edit, Bash tools)

# 4. Mark resolved with evidence
bun "{SCRIPTS_PATH/task-update.js" --session ${CLAUDE_SESSION_ID} --id {TASK_ID} \
  --status resolved \
  --add-evidence "Created src/feature.ts" \
  --add-evidence "npm test: 10/10 passed, exit 0"
```

### Planner Pattern

```bash
# 1. Read session goal
bun "{SCRIPTS_PATH/session-get.js" --session ${CLAUDE_SESSION_ID} --field goal

# 2. Read exploration context
bun "{SCRIPTS_PATH/context-get.js" --session ${CLAUDE_SESSION_ID} --summary

# 3. Create tasks
bun "{SCRIPTS_PATH/task-create.js" --session ${CLAUDE_SESSION_ID} --id "1" ...
bun "{SCRIPTS_PATH/task-create.js" --session ${CLAUDE_SESSION_ID} --id "2" ...

# 4. Update session phase
bun "{SCRIPTS_PATH/session-update.js" --session ${CLAUDE_SESSION_ID} --phase EXECUTION
```

### Verifier Pattern

```bash
# 1. List tasks
bun "{SCRIPTS_PATH/task-list.js" --session ${CLAUDE_SESSION_ID}

# 2. Get task evidence
bun "{SCRIPTS_PATH/task-get.js" --session ${CLAUDE_SESSION_ID} --id 1 --field evidence

# 3. Run verification tests
# ... (use Bash tool)

# 4. Update verify task
bun "{SCRIPTS_PATH/task-update.js" --session ${CLAUDE_SESSION_ID} --id verify \
  --status resolved \
  --add-evidence "VERDICT: PASS"

# 5. Update session phase
bun "{SCRIPTS_PATH/session-update.js" --session ${CLAUDE_SESSION_ID} --phase COMPLETE
```

### Explorer Pattern

```bash
# 1. Read exploration context
bun "{SCRIPTS_PATH/context-get.js" --session ${CLAUDE_SESSION_ID}

# 2. Explore and write findings to markdown
# Write("$SESSION_DIR/exploration/exp-{id}.md", findings)

# 3. Add summary to context
bun "{SCRIPTS_PATH/context-add.js" --session ${CLAUDE_SESSION_ID} \
  --explorer-id "exp-{id}" \
  --summary "Brief summary of findings" \
  --key-files "path/to/file1.ts,path/to/file2.ts"
```

---

## Core Rules

1. **JSON via scripts, Markdown via Read** - Use scripts for session.json, context.json, tasks/*.json
2. **Use `--field` for efficiency** - Extract only needed data instead of full JSON
3. **Use `{SCRIPTS_PATH}` placeholder** - Substitute with actual path from your prompt
4. **Direct path for SESSION_DIR** - No script needed: `~/.claude/ultrawork/sessions/${CLAUDE_SESSION_ID}`

---

## Quick Reference

| Data | Access Method |
|------|---------------|
| session.json | `bun "{SCRIPTS_PATH/session-get.js" --session ${CLAUDE_SESSION_ID}` |
| context.json | `bun "{SCRIPTS_PATH/context-get.js" --session ${CLAUDE_SESSION_ID}` |
| tasks/*.json | `bun "{SCRIPTS_PATH/task-get.js" --session ${CLAUDE_SESSION_ID} --id N` |
| task list | `bun "{SCRIPTS_PATH/task-list.js" --session ${CLAUDE_SESSION_ID}` |
| exploration/*.md | `Read("~/.claude/ultrawork/sessions/${CLAUDE_SESSION_ID}/exploration/file.md")` |

---

## Why Scripts Over Direct Read?

1. **Token efficiency**: JSON wastes tokens on structure (`{`, `"key":`, etc.)
2. **Field extraction**: Scripts return only needed data
3. **Consistent error handling**: Validation and error messages
4. **Abstraction**: Storage format changes don't affect agents
