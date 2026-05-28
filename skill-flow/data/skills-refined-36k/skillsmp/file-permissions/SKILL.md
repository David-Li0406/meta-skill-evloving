---
name: file-permissions
description: File read/write permissions for all Ralph agents
category: orchestration
depends-on: [ralph-core]
---

# File Permissions

> "Single-writer principle prevents race conditions."

## Core Principle

Each file has a **primary owner** to avoid conflicts. Only the owner may write to that file.

## File Ownership

| File | Primary Owner | Other Agents |
|------|---------------|--------------|
| `coordinator-state.json` | PM | Workers may update their own `agents.{role}.*` fields only |
| `current-task.json` | PM (creates) | Workers may update `status`, `completedAt`, `commit`, `retryCount`, `bugNotes` |
| `prd.json` | PM (fields) | QA may update `passes`, `validationResults`, `bugs` |
| `session.log` | All agents | All append-only |
| `coordinator-progress.txt` | PM | All append-only |
| `developer-progress.txt` | Developer | PM may append notes |
| `qa-progress.txt` | QA | PM may append notes |

## Permission Rules

1. **Read-modify-write atomically** - see [atomic-updates.md](atomic-updates.md)
2. **Only update fields you own** - never overwrite another agent's data
3. **Append-only for logs** - never delete or reorder entries
4. **Retry on conflict** - if write fails, re-read and retry once
5. **Use per-agent files** for frequently updated data to reduce contention

## What Each Agent CAN Write To

### PM Coordinator
- ✅ `.claude/session/*` - All session files
- ✅ `prd.json` - ONLY task status fields: `passes`, `status`, `assignedAt`, `assignedTo`, `completedAt`
- ✅ `coordinator-progress.txt` - Full ownership
- ✅ `developer-progress.txt` - May append notes
- ✅ `qa-progress.txt` - May append notes
- ❌ Source code files (`src/`, `server/`, `public/`)
- ❌ Test files
- ❌ Configuration files

### Developer Worker
- ✅ `.claude/session/session.log` - Append log entries
- ✅ `.claude/session/developer-progress.txt` - Full ownership
- ✅ `current-task.json` - May update: `status`, `completedAt`, `commit`, `question`, `questionType`
- ✅ Source code files (`src/`, etc.) - Full ownership
- ❌ `prd.json` - Read-only
- ❌ `coordinator-progress.txt` - Read-only (PM manages this)
- ❌ `qa-progress.txt` - Read-only

### QA Worker
- ✅ `.claude/session/session.log` - Append log entries
- ✅ `.claude/session/qa-progress.txt` - Full ownership
- ✅ `current-task.json` - May update: `status`, `validatedAt`, `validationResults`, `bugs`
- ✅ `prd.json` - May update: `passes`, `validationResults`, `bugs`
- ❌ Source code files - Read-only (validates only, doesn't edit)
- ❌ `coordinator-progress.txt` - Read-only
- ❌ `developer-progress.txt` - Read-only

### Game Designer Worker
- ✅ `.claude/session/session.log` - Append log entries
- ✅ `.claude/session/gamedesigner-progress.txt` - Full ownership
- ✅ `docs/design/` - Full ownership of all design artifacts
- ✅ Design artifacts in project root
- ❌ Source code files - Read-only
- ❌ `prd.json` task descriptions - Read-only (PM only)

### Tech Artist Worker
- ✅ `.claude/session/session.log` - Append log entries
- ✅ `.claude/session/techartist-progress.txt` - Full ownership
- ✅ `src/assets/` - All 3D models, textures, materials
- ✅ `src/components/**/*.{materials,shaders,effects}*` - Visual components
- ✅ `src/styles/` - UI styles and visual themes
- ✅ `src/vfx/` - Particle systems and effects
- ❌ Core game logic (store/, hooks/, utils/) - Read-only
- ❌ Network code (server/) - Read-only
- ❌ `prd.json` task descriptions - Read-only (PM only)

## Commit Permissions

**ALL agents MUST commit their file changes** following the Ralph commit format.

| Agent | Must Commit | Commit Scope |
|-------|-------------|--------------|
| **PM** | ✅ Yes | `prd.json`, `.claude/session/coordinator-progress.txt`, skill files, retrospective artifacts |
| **Developer** | ✅ Yes | Source files, tests, own progress files |
| **Tech Artist** | ✅ Yes | Asset files, visual components, shaders, styles |
| **QA** | ✅ Yes | `prd.json` (validation fields), bug reports, own progress files |
| **Game Designer** | ✅ Yes | `docs/design/`, GDD, design artifacts, own progress files |

**Commit Format:**
```
[ralph] [{{AGENT}}] {{TASK_ID}}: {{Brief description}}

- Change 1
- Change 2

PRD: {{TASK_ID}} | Agent: {{AGENT}} | Iteration: {{N}}
```

**No Commit Exceptions:**
- Heartbeat updates (coordinator-state.json timestamps)
- Temporary/pending message files (deleted after processing)

> See [ralph-core.md](ralph-core.md#universal-commit-rule-all-agents) for complete commit rules.

## Concurrency Rules

1. **Never overwrite entire files** - update specific fields only
2. **Use atomic updates** - read-modify-write to temp file, then rename
3. **Check file locks** - if `.lock` file exists, wait or retry
4. **Additive updates** - for logs, append only (never delete except by PM archiving)
5. **Field-level ownership** - multiple agents can update different fields in same file

## Atomic Update Pattern

```bash
# Read
STATE=$(cat file.json)
# Modify
NEW_STATE=$(echo "$STATE" | jq '.field = "value"')
# Write atomically
echo "$NEW_STATE" > file.json.tmp && mv file.json.tmp file.json
```

## Logging Best Practices

- **Use structured logs** - JSON format where possible
- **Include timestamps** - ISO 8601 format
- **Include agent identifier** - who made the change
- **Append only** - never rewrite log files
- **Archive, don't delete** - PM may archive old logs

## Conflict Resolution

If you encounter a write conflict:

1. **Re-read the file** - get the latest state
2. **Re-apply your changes** - on top of the new state
3. **Write again** - using atomic pattern
4. **If still conflicts** - log the issue and wait 30 seconds

## File Locking

The system uses `.lock` files to prevent concurrent writes:

- `{file}.lock` - Created before writing, removed after
- Stale locks (>30s) are automatically removed
- Use `Invoke-WithFileLock` (PowerShell) for custom critical sections

## Reference

- [ralph-core.md](ralph-core.md) — Session structure and file ownership table
- [atomic-updates.md](atomic-updates.md) — Atomic update patterns
