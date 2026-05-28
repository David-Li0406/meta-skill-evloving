---
name: linear-management
description: Use this skill for managing Linear issues, projects, and teams, including creating and updating issues, querying projects, and managing workflows.
---

# Linear Management

Tools and workflows for managing issues, projects, and teams in Linear.

## Tool Selection

Choose the right tool for the task:

| Tool | When to Use |
|------|-------------|
| **MCP Tools (mcp__linear)** | Most operations - PREFERRED |
| **Linear CLI (`linear` command)** | Always available via Bash |
| **Helper Scripts** | For complex operations |

**If MCP tools are NOT available**, use the Linear CLI via Bash:

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

## Conventions

### Issue Status

When creating issues, set the appropriate status based on assignment:

- **Assigned to me**: Set `state: "Todo"`
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

### Labels

You can use label names directly in `create_issue` and `update_issue` - no need to look up IDs:

```typescript
await linear.create_issue({
  team: "ENG",
  title: "Update documentation",
  labels: ["documentation", "high-priority"]
})
```

## Quick Start (First-Time Users)

### 1. Check Your Setup

Run the setup check to verify your configuration:

```bash
npx tsx ~/.claude/skills/linear/scripts/setup.ts
```

### 2. Get API Key (If Needed)

If setup reports a missing API key, create one in Linear and add it to your environment.

### 3. Test Connection

Verify everything works:

```bash
npx tsx ~/.claude/skills/linear/scripts/query.ts "query { viewer { name } }"
```

## Project Management Workflow

### Create Issues in the Correct Project from the Start

**Best Practice**: When planning a new phase or initiative, create the project and its issues together in a single planning session.

#### Recommended Workflow

1. **Create the project first**:
   ```bash
   npx tsx scripts/linear-ops.ts create-project "Phase X: Feature Name" "My Initiative"
   ```

2. **Set project state to Planned**:
   ```bash
   npx tsx scripts/linear-ops.ts project-status "Phase X: Feature Name" planned
   ```

3. **Create issues directly in the project**:
   ```bash
   npx tsx scripts/linear-ops.ts create-issue "Phase X: Feature Name" "Parent task" "Description"
   ```

4. **Update project state when work begins**:
   ```bash
   npx tsx scripts/linear-ops.ts project-status "Phase X: Feature Name" in-progress
   ```

## SDK Automation Scripts

**Use only when MCP tools are insufficient.** For complex operations involving loops, mapping, or bulk updates, write TypeScript scripts using `@linear/sdk`.

## GraphQL API

**Fallback only.** Use when operations aren't supported by MCP or SDK.

### Ad-Hoc Queries

Use `scripts/query.ts` to execute GraphQL queries:

```bash
LINEAR_API_KEY=lin_api_xxx node scripts/query.ts "query { viewer { id name } }"
```

## Reference

| Document | Purpose |
|----------|---------|
| [api.md](api.md) | GraphQL API reference |
| [sdk.md](sdk.md) | SDK automation patterns |
| [projects.md](projects.md) | Project & initiative management |
| [troubleshooting.md](troubleshooting.md) | Common issues, MCP debugging |
| [docs/labels.md](docs/labels.md) | Label taxonomy |

**External:** [Linear MCP Documentation](https://linear.app/docs/mcp.md)