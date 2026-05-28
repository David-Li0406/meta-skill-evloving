---
name: atlas
description: Use this skill when you need to execute tasks systematically, leveraging fresh contexts for complex implementations while tracking state persistently.
---

# Atlas - Task Execution Engine

Atlas is an autonomous agent loop designed for implementing tasks. It picks tasks from TodoWrite and executes them systematically, using fresh sub-agent contexts for complex work to prevent context degradation.

## Overview

```
Pick ready task -> Decide inline vs sub-agent -> Implement -> Validate -> Commit -> Repeat
```

**Memory persists via:**
- **git commits** - Work history
- **STATE.md** - Current position + context notes
- **progress.txt** - Short-term learnings (current feature)
- **CLAUDE.md / AGENTS.md** - Long-term memory (codebase patterns)

## When to Use Atlas

| Scenario | Use |
|----------|-----|
| Tasks already planned (TodoWrite populated) | `run atlas` or `/atlas` |
| After `compound-engineering` plan phase | `run atlas` |
| After `build-feature` approval gate | Automatic |
| Need to plan first | Use `compound-engineering` or `build-feature` instead |

## Execution Loop

### Step 0: Read Current State

```bash
cat .claude/atlas/current-feature.txt
cat .claude/atlas/STATE.md
cat .claude/atlas/progress.txt
```
Check TodoWrite for current tasks and their status.

### Step 1: Find Ready Tasks

From TodoWrite, find tasks that are:
- `status: "pending"`
- All dependencies completed (earlier tasks in list are done)

**Skip container/parent tasks** - only work on leaf tasks.

### Step 2: If No Ready Tasks

Check if all tasks are completed:
- **If yes:** Signal completion (see Completion section)
- **If blocked:** Report which tasks are blocked and why

### Step 3: Execute Ready Task

**Pick the next task:**
- Prefer tasks related to what was just completed (same module/area)
- If no prior context, pick the first ready task

#### Decide: Inline vs Sub-Agent

**Run inline (same context) when:**
- Rename/move files
- Add/remove imports
- Fix typos or small bugs
- < ~15 lines changed
- Running npm commands
- Simple file edits

**Spawn sub-agent (fresh 200k context) when:**
- New component or file
- Significant logic changes (>15 lines)
- Multi-file changes
- Task requires understanding patterns from other files
- Complex implementation

### Step 4a: Inline Execution

For simple tasks:

1. **Mark as in_progress** via TodoWrite
2. **Implement directly** - Make the changes
3. **Validate** the changes
4. **Commit** the changes to the repository
5. **Update** the task status in TodoWrite