# Context Gathering Best Practices

## DO: Use MCP Tools for Spec Data

Always use MCP tools to access specification data:

```bash
# Get next actionable task with full context
mcp__plugin_foundry_foundry-mcp__task action="prepare" spec_id={spec-id}

# Query tasks by status or parent
mcp__plugin_foundry_foundry-mcp__task action="query" spec_id={spec-id} status="pending"
mcp__plugin_foundry_foundry-mcp__task action="query" spec_id={spec-id} parent="phase-1"

# Get detailed task information
mcp__plugin_foundry_foundry-mcp__task action="info" spec_id={spec-id} task_id={task-id}
```

## DON'T: Read Spec Files Directly

Never use these approaches for spec data:

```bash
# BAD - Wastes context tokens and bypasses validation
Read("specs/active/my-spec.json")
cat specs/active/my-spec.json
jq '.phases' specs/active/my-spec.json
grep "task-1" specs/active/my-spec.json
```

## Context Efficiency

| Approach | Context Cost | Reliability |
|----------|--------------|-------------|
| MCP `task action="prepare"` | Low | High |
| MCP `task action="info"` | Low | High |
| Read spec file directly | High | Low |
| Bash + jq parsing | High | Medium |

## Anti-Patterns

1. **Reading full spec files** - Inflates context with JSON structure
2. **Bash loops over tasks** - Use `task action="query"` instead
3. **Creating temp scripts** - Unnecessary complexity
4. **Parsing JSON with grep/sed** - Fragile and error-prone
