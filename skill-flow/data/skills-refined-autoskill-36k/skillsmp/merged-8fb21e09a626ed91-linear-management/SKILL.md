---
name: linear-management
description: Use this skill for managing Linear issues, projects, and teams, including creating, updating, and querying tasks.
---

# Linear Management

Tools and workflows for managing issues, projects, and teams in Linear.

## Tool Selection

Choose the right tool for the task:

| Tool | When to Use |
|------|-------------|
| **MCP Tools (mcp__linear)** | Most operations - PREFERRED |
| **Linear CLI (`linear-cli`)** | Always available via Bash |
| **Helper Scripts** | For complex operations |
| **GraphQL API** | Operations not supported by MCP/CLI |

## Quick Start

### Setup Check

Run the setup check to verify your configuration:

```bash
npx tsx ~/.claude/skills/linear/scripts/setup.ts
```

### Common Operations

```bash
# Create an issue
linear-cli i create "Bug: Login fails" -t Engineering -p 2

# Update issue status
linear-cli i update LIN-123 -s Done

# Start working on an issue
linear-cli i start LIN-123 --checkout

# List all issues
linear-cli i list
```

## Managing Issues

### Listing Issues

```bash
# List all issues
linear-cli i list

# Filter by team
linear-cli i list -t Engineering

# Filter by status
linear-cli i list -s "In Progress"

# Get JSON output
linear-cli i list --output json
```

### Viewing Issue Details

```bash
# View issue details
linear-cli i get LIN-123

# Get as JSON
linear-cli i get LIN-123 --output json
```

### Creating Issues

```bash
# Create issue with status
linear-cli i create "Feature request" -t ENG -s "Backlog"
```

### Updating Issues

```bash
# Update status
linear-cli i update LIN-123 -s Done

# Update priority
linear-cli i update LIN-123 -p 1
```

### Starting and Stopping Work

```bash
# Start working on an issue
linear-cli i start LIN-123 --checkout

# Stop working on an issue
linear-cli i stop LIN-123
```

### Comments

```bash
# List comments
linear-cli cm list LIN-123

# Add comment
linear-cli cm create LIN-123 -b "Fixed in latest commit"
```

## Project Management

### Creating Projects and Linking Initiatives

1. **Create the project**:
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

### Updating Project Status

```bash
npx tsx scripts/linear-ops.ts project-status "Phase X" in-progress
```

## Conventions

### Issue Status

- **Assigned to me**: Set `state: "Todo"`
- **Unassigned**: Set `state: "Backlog"`

### Labels

Use domain-based label taxonomy. Key rules include:
- ONE Type label: `feature`, `bug`, etc.
- 1-2 Domain labels: `security`, `backend`, etc.

## SDK Automation Scripts

For complex operations involving loops or bulk updates, write TypeScript scripts using `@linear/sdk`. 

## GraphQL API

Use when operations aren't supported by MCP or CLI. See the API documentation for complete details.

## Reference

| Document | Purpose |
|----------|---------|
| [api.md](api.md) | GraphQL API reference |
| [sdk.md](sdk.md) | SDK automation patterns |
| [projects.md](projects.md) | Project & initiative management |
| [troubleshooting.md](troubleshooting.md) | Common issues, MCP debugging |

**External:** [Linear MCP Documentation](https://linear.app/docs/mcp.md)