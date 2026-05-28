---
name: linear-management
description: Use this skill when managing issues, projects, and teams in Linear, including creating, updating, and querying tasks.
---

# Linear Management

Tools and workflows for managing issues, projects, and teams in Linear.

## Tool Selection

Choose the right tool for the task:

1. **MCP Tools (mcp__linear)** - Use for simple operations (create/update/query single issues, basic filters).
2. **Linear CLI** - Use if MCP tools are not available; always accessible via Bash.
3. **Helper Scripts** - For complex operations involving loops, mapping, or bulk updates.

## Conventions

### Issue Status

When creating issues, set the appropriate status based on assignment:

- **Assigned to me** (`assignee: "me"`): Set `state: "Todo"`
- **Unassigned**: Set `state: "Backlog"`

Example:
```typescript
// Issue for myself
await linear.create_issue({
  team: "ENG",
  title: "Fix authentication bug",
  assignee: "me",
  state: "Todo"
})

// Unassigned issue
await linear.create_issue({
  team: "ENG",
  title: "Research API performance",
  state: "Backlog"
})
```

### Querying Issues

Use `assignee: "me"` to filter issues assigned to the authenticated user:

```typescript
// My issues
await linear.list_issues({ assignee: "me" })

// Team backlog
await linear.list_issues({ team: "ENG", state: "Backlog" })
```

### Labels

You can use label names directly in `create_issue` and `update_issue` - no need to look up IDs:

```typescript
await linear.create_issue({
  team: "ENG",
  title: "Update documentation",
  labels: ["documentation", "high-priority"]
})
```

**Label Lookup**: Labels can exist at the workspace level or team level. When searching for labels, check both:

1. Workspace labels: `list_issue_labels()` (no team filter)
2. Team labels: `list_issue_labels({ team: "TEAM" })`

If a label isn't found at the workspace level, check the team before concluding it doesn't exist.

## CLI Commands

If MCP tools are not available, use the Linear CLI via Bash:

```bash
# View an issue
linear issues view ENG-123

# Create an issue
linear issues create --title "Issue title" --description "Description"

# Update issue status (get state IDs first)
linear issues update ENG-123 -s "STATE_ID"

# Add a comment
linear issues comment add ENG-123 -m "Comment text"

# List issues
linear issues list
```

## Security: Varlock Integration

**CRITICAL**: Never expose API keys in terminal output or context.

### Safe Commands (Always Use)

```bash
# Validate LINEAR_API_KEY is set (masked output)
varlock load 2>&1 | grep LINEAR

# Run commands with secrets injected
varlock run -- npx tsx scripts/query.ts "query { viewer { name } }"
```

### Setup for New Projects

1. Create `.env.schema` with `@sensitive` annotation:
   ```bash
   # @type=string(startsWith=lin_api_) @required @sensitive
   LINEAR_API_KEY=
   ```

2. Add `LINEAR_API_KEY` to `.env` (never commit this file).

3. Configure MCP to use the environment variable:
   ```json
   {
     "mcpServers": {
       "linear": {
         "env": { "LINEAR_API_KEY": "${LINEAR_API_KEY}" }
       }
     }
   }
   ```

4. Use `varlock load` to validate before operations.

## Quick Start (First-Time Users)

### 1. Check Your Setup

Run the setup check to verify your configuration:

```bash
npx tsx ~/.claude/skills/linear/scripts/setup.ts
```

This will check:
- LINEAR_API_KEY is set and valid
- @linear/sdk is installed
- Linear CLI availability (optional)
- MCP configuration