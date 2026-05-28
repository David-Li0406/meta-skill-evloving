---
name: undercity
description: Dispatch tasks to the undercity orchestrator for autonomous batch execution. Use when adding tasks, checking status, or running parallel work. Ideal for multi-task workloads that benefit from autonomous verification.
allowed-tools: Bash(undercity:*)
---

# Undercity Task Orchestrator

Dispatch work to undercity for autonomous, parallel execution with built-in verification (typecheck, test, lint).

## When to Use Undercity

**Good fit:**
- Multi-step tasks that can run independently
- Batch refactoring across many files
- Work that benefits from verification loops
- Tasks to run overnight/in background

**Skip undercity for:**
- Single quick fixes (do directly)
- Questions/explanations
- Exploratory debugging

## Commands

### Add a Task

```bash
undercity add "task description"
```

Examples:
```bash
undercity add "Fix all TypeScript strict null check errors in src/"
undercity add "Add JSDoc comments to all exported functions"
undercity add "Migrate deprecated API calls to v2"
```

### Add Task with Context (Handoff)

Pass context to help workers start with relevant information:

```bash
# Pass files you've already analyzed
undercity add "Refactor auth module" --files-read "src/auth.ts,src/types.ts"

# Pass notes about decisions or constraints
undercity add "Fix validation bug" --notes "Issue is in validateInput(), not the schema"
```

### Check Task Board

```bash
# All tasks
undercity tasks

# Only pending
undercity tasks --status pending

# Only completed
undercity tasks --status complete
```

### Mark Tasks Complete

```bash
# Mark task as complete
undercity complete <task-id>

# With resolution notes
undercity complete <task-id> --resolution "Fixed in commit abc"

# With reason (for closures without implementation)
undercity complete <task-id> --reason "Already implemented"
```

### Start Autonomous Execution

```bash
# Process all pending tasks
undercity grind

# Limit concurrent workers
undercity grind --parallel 2

# Process specific number of tasks
undercity grind -n 5
```

### Proactive PM (Task Generation)

```bash
# Generate tasks from codebase analysis
undercity pm --propose

# Research a topic via web search
undercity pm "topic" --research

# Full ideation: research + propose
undercity pm "topic" --ideate

# Add generated tasks to board
undercity pm "topic" --ideate --add
```

### Monitor Progress

```bash
# Live TUI dashboard
undercity watch

# Current status snapshot
undercity status
```

## Task Description Guidelines

Write clear, actionable task descriptions:

**Good:**
- "Fix TypeScript error TS2345 in src/api/client.ts"
- "Add input validation to all POST endpoints in src/routes/"
- "Replace deprecated lodash _.pluck with _.map"

**Vague (avoid):**
- "Fix bugs" (which bugs?)
- "Improve performance" (where? how?)
- "Clean up code" (too broad)

## How It Works

1. Tasks execute in isolated git worktrees (no conflicts)
2. All changes verified (typecheck, test, lint) before commit
3. Tasks merge to main serially
4. Failed tasks retry with model escalation (haiku -> sonnet -> opus)

## Task Board Location

Tasks are stored in `.undercity/tasks.json` (tracked in git for team visibility).

Runtime state files (knowledge, metrics, recovery) are in `.undercity/` but gitignored.
