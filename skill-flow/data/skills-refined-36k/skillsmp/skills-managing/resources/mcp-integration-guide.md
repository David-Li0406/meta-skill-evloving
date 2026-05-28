# MCP Integration Guide
*Model Context Protocol for ASE*

**Purpose**: Guide for integrating MCP Servers into ASE Skills logic. This allows Agents to use external tools (Databases, APIs, Browser) via standard protocols.

## What is MCP?
Model Context Protocol (MCP) connects AI models to external systems. In ASE, we can define skills that *know usage patterns* for specific MCP servers.

## Integration Patterns

### 1. The Wrapper Pattern
Create a skill that teaches the Agent how to *use* a specific set of MCP tools.

**Example: `postgres-expert`**
- **Trigger**: "Query database", "Check schema"
- **Knowledge**:
  - Knows which tools exist (`query_db`, `list_tables`)
  - Knows best practices ("Always limit queries to 10 rows first")
  - Knows error handling ("If connection fails, check VPN")

### 2. The Setup Pattern
Create a skill that helps the user *configure* an MCP server.

**Example: `setup-github-mcp`**
- **Action**: Writes the config file for the user.
- **Knowledge**:
  - Knows JSON schema for `.mcp.json` or equivalent config.
  - Knows required Environment Variables (`GITHUB_TOKEN`).

## Standard MCP config (Reference)

```json
{
  "mcpServers": {
    "sqlite": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "mcp/sqlite"],
      "env": {}
    }
  }
}
```

## Best Practices
1.  **Portable Paths**: If referencing local scripts, use standard relative paths or project root variables.
2.  **Security**: Never hardcode API keys in the Skill. Instruct users to use `.env`.
3.  **Validation**: Teach the Agent to run a "health check" tool (if available) before complex operations.
