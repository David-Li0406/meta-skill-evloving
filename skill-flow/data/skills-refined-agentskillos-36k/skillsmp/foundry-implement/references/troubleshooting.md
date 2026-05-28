# Troubleshooting

## Task Not Found

**Error:** MCP tool returns "task not found"

**Causes:**
- Incorrect task_id format
- Task in different spec
- Spec not in active/ folder

**Resolution:**
```bash
# List all tasks to find correct ID
mcp__plugin_foundry_foundry-mcp__task action="query" spec_id={spec-id}

# Check spec location
mcp__plugin_foundry_foundry-mcp__spec action="find" spec_id={spec-id}
```

## Spec Not Active

**Error:** Spec found in pending/ not active/

**Resolution:**
```bash
# Activate the spec first
mcp__plugin_foundry_foundry-mcp__lifecycle action="activate" spec_id={spec-id}
```

## Circular Dependencies

**Error:** Task blocked by task that depends on it

**Resolution:**
1. Check dependency graph with `task action="info"`
2. Identify circular reference
3. Use `Skill(foundry:foundry-spec)` to fix spec (includes modify capabilities)

## Context Limit Warnings

**Symptom:** `[CONTEXT X%]` warnings appearing

**Resolution:**
1. Complete current task
2. Mark task complete with journal
3. Run `/clear`
4. Resume with `foundry-implement`

## MCP Tools Not Responding

**Error:** MCP tools not responding

**Resolution:**
1. Check foundry-mcp is installed: `python -m foundry_mcp.server --help`
2. Restart Claude Code
3. Run `foundry-implement` again

## Quick Reference

### Core Commands

```bash
# Task preparation (primary)
mcp__plugin_foundry_foundry-mcp__task action="prepare" spec_id={spec-id}

# Task status update
mcp__plugin_foundry_foundry-mcp__task action="start" spec_id={spec-id} task_id={task-id}

# Task completion (atomic status + journal)
mcp__plugin_foundry_foundry-mcp__task action="complete" spec_id={spec-id} task_id={task-id} completion_note="..."

# Blocking
mcp__plugin_foundry_foundry-mcp__task action="block" spec_id={spec-id} task_id={task-id} reason="..."

# Unblocking
mcp__plugin_foundry_foundry-mcp__task action="unblock" spec_id={spec-id} task_id={task-id} resolution="..."
```

### Decision Tree

```
Start Task
    |
    +-- Dependencies met?
    |       |
    |       +-- No --> Block or choose different task
    |       |
    |       +-- Yes --> Continue
    |
    +-- Clear instructions?
    |       |
    |       +-- No --> Ask user or explore
    |       |
    |       +-- Yes --> Implement
    |
    +-- Implementation complete?
    |       |
    |       +-- No --> Continue or block
    |       |
    |       +-- Yes --> Run tests
    |
    +-- Tests passing?
    |       |
    |       +-- No --> Fix or block
    |       |
    |       +-- Yes --> Mark complete
    |
    +-- Surface next task
```
