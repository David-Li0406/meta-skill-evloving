---
name: checkpoint-workflow
description: Manage workflow checkpoints for issue tracking. Use when starting work on an issue, logging actions, logging commits, changing workflow phase, or checking workflow status during /work-on-issue or /auto-issue workflows.
allowed-tools: Bash, Read
---

# Checkpoint Workflow Skill

Manage workflow state persistence for issue-based development workflows.

## When to Use

- Starting work on a GitHub issue
- Logging gate passages and actions
- Recording commits made during implementation
- Transitioning between workflow phases
- Checking if a workflow exists for an issue
- Resuming interrupted workflows

## MCP Tools (Preferred)

When the MCP server is available, use native tools:

| Tool                         | Purpose                                   |
| ---------------------------- | ----------------------------------------- |
| `checkpoint_workflow_find`   | Check if workflow exists for an issue     |
| `checkpoint_workflow_create` | Start tracking a new workflow             |
| `checkpoint_workflow_update` | Update phase, status, log actions/commits |

These tools are automatically available when claude-knowledge MCP server is running.

## CLI Reference (Fallback)

When MCP tools are unavailable, use the checkpoint CLI:

```bash
bun run checkpoint workflow <command> [args...]
```

## Commands

### Find Existing Workflow

Check if a workflow exists for an issue:

```bash
bun run checkpoint workflow find <issue-number>
```

Returns JSON with workflow state or error if not found.

### Create New Workflow

Start tracking a new workflow:

```bash
bun run checkpoint workflow create <issue-number> "<branch-name>"
```

Returns JSON with the new workflow including its `id` for subsequent commands.

### Get Workflow Details

Retrieve full workflow state including actions and commits:

```bash
bun run checkpoint workflow get "<workflow-id>"
```

### Set Workflow Phase

Update the current phase:

```bash
bun run checkpoint workflow set-phase "<workflow-id>" "<phase>"
```

Valid phases: `research`, `implement`, `review`, `finalize`, `planning`, `execute`, `merge`, `cleanup`

### Set Workflow Status

Update the workflow status:

```bash
bun run checkpoint workflow set-status "<workflow-id>" "<status>"
```

Valid statuses: `running`, `paused`, `completed`, `failed`

### Log an Action

Record an action taken during the workflow:

```bash
bun run checkpoint workflow log-action "<workflow-id>" "<action-name>" "<result>" '{"optional": "metadata"}'
```

Results: `success`, `failed`, `pending`

Example actions:

- `gate-1-issue-reviewed`
- `gate-2-plan-approved`
- `research-complete`
- `implementation-complete`
- `review-agents-complete`
- `pr-created`

### Log a Commit

Record a commit made during implementation:

```bash
bun run checkpoint workflow log-commit "<workflow-id>" "<sha>" "<commit-message>"
```

### List Active Workflows

See all running workflows:

```bash
bun run checkpoint workflow list-active
```

### Delete Workflow

Remove a workflow record:

```bash
bun run checkpoint workflow delete "<workflow-id>"
```

## Workflow Phases

| Phase       | Description                        |
| ----------- | ---------------------------------- |
| `research`  | Analyzing issue, creating dev plan |
| `implement` | Writing code, making commits       |
| `review`    | Running review agents              |
| `finalize`  | Creating PR, cleanup               |

## Example: Starting a New Workflow

```bash
# 1. Check for existing workflow
bun run checkpoint workflow find 394

# 2. If not found, create new
bun run checkpoint workflow create 394 "feat/issue-394-tree-sitter"

# 3. Store the workflow ID from output for subsequent commands
# Example output: {"id": "workflow-394-1768147000000-abc123", ...}
```

## Example: Logging Progress

**IMPORTANT:** Each command is a separate Bash tool call. Replace `<workflow-id>` with the actual ID from the create command output. Never use shell variables like `$WORKFLOW_ID`.

```bash
# Log gate passage
bun run checkpoint workflow log-action "<workflow-id>" "gate-1-issue-reviewed" "success"
```

```bash
# Transition to implement phase
bun run checkpoint workflow set-phase "<workflow-id>" "implement"
```

To log a commit, first get the SHA:

```bash
git rev-parse HEAD
```

Then use the SHA value from that output:

```bash
bun run checkpoint workflow log-commit "<workflow-id>" "<sha>" "feat(module): add new feature"
```

```bash
# Mark workflow complete
bun run checkpoint workflow set-status "<workflow-id>" "completed"
```
