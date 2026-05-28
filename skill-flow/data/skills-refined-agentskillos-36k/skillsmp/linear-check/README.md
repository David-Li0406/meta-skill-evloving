# linear-check Skill

Queries Linear API to verify planning/implementation status of components/features using issue tracking data.

## Overview

This skill checks Linear for issue tracking evidence to determine component status. It queries:

1. **Issues** - Open, in-progress, completed issues mentioning the component
2. **Workflow States** - Triage, Backlog, Todo, In Progress, In Review, Done, Canceled
3. **Assignees** - Who is working on what
4. **Updates** - Recent activity on issues

## Status Levels

| Status | Evidence Required |
|--------|-------------------|
| Done | Issue in completed state |
| In Review | Issue in started state with "Review" in name |
| In Progress | Issue in started state |
| Todo | Issue in unstarted state (scheduled) |
| Backlog | Issue in backlog state |
| Triage | Issue in triage state (needs review) |
| Canceled | Issue in canceled state |
| Unknown | No Linear issue found |

## When to Use

- Directly: `/linear-check authentication`
- Automatically invoked by `/project-status` when Linear is configured

## Prerequisites

1. **Linear MCP authenticated** (preferred):
   ```bash
   # Check MCP connection
   claude /mcp
   ```

2. **Or Linear configuration** in `.entourage/repos.json`:
   ```json
   {
     "linear": {
       "token": "lin_api_...",
       "teamId": "TEAM",
       "workspace": "my-workspace"
     }
   }
   ```

## Testing the Skill

### Running Evaluations

1. Navigate to your context database:
   ```bash
   cd ~/my-context
   ```

2. Start Claude Code with the plugin:
   ```bash
   # From the plugin directory
   claude --plugin-dir .

   # Or specify the path
   claude --plugin-dir ~/your-plugin
   ```

3. Test directly:
   ```
   /linear-check authentication
   /linear-check user-dashboard payments
   ```

### Example Test Queries

| Test Case | Query |
|-----------|-------|
| Single component | `/linear-check auth` |
| Multiple components | `/linear-check auth dashboard payments` |
| Non-existent component | `/linear-check nonexistent-feature` |

### Expected Output Format

```markdown
## Linear Scan: auth

| Issue | Status | State | Assignee | Last Updated |
|-------|--------|-------|----------|--------------|
| TEAM-123 | In Progress | In Progress | @alice | 2025-01-10 |

### Linear Details

**TEAM-123:** "Implement authentication flow"
- Status: In Progress
- State: In Progress (started)
- Assignee: @alice
- Updated: Jan 10, 2025
- URL: https://linear.app/my-workspace/issue/TEAM-123
```

## Authentication

The skill prefers Linear MCP for authentication. If unavailable, falls back to token in `.entourage/repos.json`:

### Option 1: Linear MCP (Recommended)

Configure in `.mcp.json`:
```json
{
  "mcpServers": {
    "linear": {
      "type": "sse",
      "url": "https://mcp.linear.app/sse"
    }
  }
}
```

### Option 2: API Token (Fallback)

```json
{
  "linear": {
    "token": "lin_api_...",
    "teamId": "TEAM",
    "workspace": "my-workspace"
  }
}
```

Generate a token at: https://linear.app/settings/api

## Error Handling

| Error | Behavior |
|-------|----------|
| MCP not configured, no token | Returns configuration instructions |
| Authentication failed | Reports token issue |
| Rate limited | Reports rate limit, suggests try later |
| Team not found | Reports team not found, check config |

## Evaluation Logs

This skill is typically invoked by `/project-status`. Evaluation logs are stored with project-status results:

```
~/my-context/evaluations/project-status/
```

## Test Cases

See `evaluations/evaluation.json` for the full test suite covering:
- Issue status detection (all workflow states)
- Multiple issue handling
- Authentication scenarios (MCP, token fallback)
- Error handling
- Multi-component queries

## See Also

- `/github-repo-check` - GitHub evidence gathering
- `/local-repo-check` - Local repository scanning
- `/project-status` - Orchestrates all evidence sources
