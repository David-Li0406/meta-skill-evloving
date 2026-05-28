# Journaling

This reference describes how to document decisions, deviations, and progress through journal entries.

## When to Journal

- **Decisions** - Architectural choices, technology selections
- **Deviations** - Changes from the original plan
- **Blockers** - Issues preventing progress (with resolution)
- **Notes** - Important observations during implementation
- **Status changes** - Task completions (automatic with `task action="complete"`)

## Adding Journal Entries

```bash
# Document a decision
mcp__plugin_foundry_foundry-mcp__journal action="add" spec_id={spec-id} title="Decision Title" content="Explanation of decision and rationale" task_id={task-id} entry_type="decision"

# Document a deviation from the plan
mcp__plugin_foundry_foundry-mcp__journal action="add" spec_id={spec-id} title="Deviation: Changed Approach" content="Created separate service file instead of modifying existing. Improves separation of concerns." task_id={task-id} entry_type="deviation"

# Document a blocker
mcp__plugin_foundry_foundry-mcp__journal action="add" spec_id={spec-id} title="Blocker: External API" content="Third-party API is down. Waiting for resolution." task_id={task-id} entry_type="blocker"

# Document a note
mcp__plugin_foundry_foundry-mcp__journal action="add" spec_id={spec-id} title="Implementation Note" content="Using Redis for session storage as discussed." task_id={task-id} entry_type="note"

# Document task completion (automatic with task action="complete")
mcp__plugin_foundry_foundry-mcp__journal action="add" spec_id={spec-id} title="Task Completed: Implement Auth" content="Successfully implemented authentication with JWT tokens. All tests passing." task_id={task-id} entry_type="status_change"
```

## Entry Types

| Type | Purpose |
|------|---------|
| `decision` | Architectural or design decisions |
| `deviation` | Changes from original plan |
| `blocker` | Issues preventing progress |
| `note` | General observations |
| `status_change` | Task status updates |

## Listing Journal Entries

```bash
# List all entries for a spec
mcp__plugin_foundry_foundry-mcp__journal action="list" spec_id={spec-id}

# List entries for a specific task
mcp__plugin_foundry_foundry-mcp__journal action="list" spec_id={spec-id} task_id={task-id}

# Filter by entry type
mcp__plugin_foundry_foundry-mcp__journal action="list" spec_id={spec-id} entry_type="decision"
```

## Automatic Journaling

The `task action="complete"` command automatically creates journal entries:
- Records what was accomplished
- Timestamps the completion
- Links to the specific task

Parent nodes (phases, groups) are also journaled automatically when they auto-complete.

## Best Practices

1. **Document WHY** - Rationale is more valuable than just what changed
2. **Be specific** - Vague notes aren't helpful later
3. **Journal immediately** - Don't batch updates; context is lost over time
4. **Link to tasks** - Always include `task_id` when relevant
5. **Use appropriate types** - Helps with filtering and review
