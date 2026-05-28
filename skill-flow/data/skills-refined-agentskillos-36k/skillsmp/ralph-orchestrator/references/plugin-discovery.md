# Plugin Discovery for Ralph

Ralph loops can leverage other installed Claude Code plugins and MCP servers to enhance capabilities. This reference explains how to discover and expose available integrations.

## Discovery Sources

### 1. MCP Servers (Project-Level)

Check for `.mcp.json` in the project root and subdirectories:

```bash
find . -name ".mcp.json" -type f 2>/dev/null | head -5
```

Parse each file to find configured MCP servers:
```json
{
  "mcpServers": {
    "ServerName": {
      "url": "https://..."
    }
  }
}
```

**Common MCP Servers and Their Uses**:
| Server | Task Types | Capabilities |
|--------|------------|--------------|
| Sentry | investigation, implementation | Error tracking, issue details, stack traces |
| Trello | all | Task management, card updates, status tracking |
| Toggl | all | Time tracking, project logging |
| GitHub | implementation | PR creation, issue management |

### 2. Available MCP Tools

Use the `ListMcpResourcesTool` tool to discover available MCP resources:
```
ListMcpResourcesTool()
```

This returns all resources from configured MCP servers.

### 3. Installed Plugins

Check `~/.claude/plugins/installed_plugins.json` for installed plugins:

```bash
cat ~/.claude/plugins/installed_plugins.json 2>/dev/null | head -100
```

**Key Plugin Categories for Ralph**:
| Plugin Pattern | Task Types | Use Case |
|----------------|------------|----------|
| `sentry@*` | investigation | Pull Sentry issues, errors |
| `code-review@*` | implementation | Review code changes |
| `debugging-toolkit@*` | investigation | Debug assistance |
| `incident-response@*` | investigation | Incident handling |
| `error-diagnostics@*` | investigation | Error analysis |

## Integration in Plan/PRD

When discovering plugins, add them to the plan:

### In plan.json / prd.json

Add an `available_integrations` field:
```json
{
  "available_integrations": {
    "mcp_servers": [
      {
        "name": "Sentry",
        "type": "mcp",
        "capabilities": ["error_tracking", "issue_details"]
      }
    ],
    "plugins": [
      {
        "name": "sentry@claude-plugins-official",
        "type": "plugin",
        "capabilities": ["sentry_issues", "error_analysis"]
      }
    ]
  }
}
```

### In PLAN.md / PRD.md

Add an "Available Integrations" section:
```markdown
## Available Integrations

The following tools are available during this Ralph loop:

### MCP Servers
- **Sentry** - Use for error tracking and issue investigation
  - Tools: `mcp__sentry__*`

### Plugins
- **code-review** - Use for reviewing implementation changes
  - Skills: `/review-pr`
```

## Task-Type-Specific Recommendations

### Implementation Tasks
Recommend these integrations:
- Code review plugins
- Test runners
- Type checkers
- Sentry (for monitoring new code)

### Documentation Tasks
Recommend these integrations:
- Document generation plugins
- SEO plugins (for public docs)

### Investigation Tasks
Recommend these integrations:
- Sentry (error details, stack traces)
- Debugging toolkit
- Error diagnostics
- Incident response
- Logging plugins

## Discovery During Plan Creation

Add this step to `/ralph-freeform` and `/prd`:

```markdown
### Step: Discover Available Integrations

Before generating phases/stories, check for available integrations:

1. **Find MCP configs**:
   ```bash
   find . -name ".mcp.json" -type f 2>/dev/null
   ```

2. **List MCP tools**:
   ```
   ListMcpResourcesTool()
   ```

3. **Suggest relevant integrations** based on task type:
   - If investigation: "I see you have Sentry configured. Should I include Sentry issue lookup in the investigation phases?"
   - If implementation: "I see you have code-review plugin. Should I add a review phase at the end?"

4. **Record in plan** for the Ralph loop to use
```

## During Ralph Loop Execution

When building the master prompt, include discovered integrations:

```markdown
## Available Tools

In addition to standard tools, you have access to:

### MCP Servers
- **Sentry**: Use `mcp__sentry__get_issues` to fetch error details
- **Toggl**: Use `mcp__toggl__start_timer` for time tracking

### Plugin Skills
- **code-review**: Run `/review-pr` after implementation phases

Use these tools when relevant to the current phase.
```

## Example: Investigation Task with Sentry

If Sentry MCP is configured and task_type is `investigation`:

1. Plan creation suggests: "Use Sentry to gather error details in Phase 1"
2. Phase 1 steps include: "Fetch Sentry issues related to the problem"
3. Master prompt includes: "You have access to Sentry MCP tools"
4. Loop can autonomously query Sentry for error context
