# Tool Permission Patterns

## Permission Modes

### Blacklist (Admin)
All tools allowed except denied list.

```json
{
  "tools": {
    "mode": "blacklist",
    "allowed": [],
    "denied": []
  }
}
```

### Whitelist (User)
Only explicitly allowed tools.

```json
{
  "tools": {
    "mode": "whitelist",
    "allowed": ["ping", "list_tools", ...],
    "denied": ["admin_*"]
  }
}
```

## Common Patterns

### Full Admin (hermes-style)
```json
{
  "mode": "blacklist",
  "allowed": [],
  "denied": []
}
```
Access: Everything

### Standard User
```json
{
  "mode": "whitelist",
  "allowed": [
    "ping",
    "list_tools",
    "get_service_health",
    "n8n_list_workflows",
    "n8n_execute_workflow"
  ],
  "denied": ["admin_*"]
}
```
Access: Meta tools + n8n

### Notion-focused
```json
{
  "mode": "whitelist",
  "allowed": [
    "ping",
    "list_tools",
    "invoke_notion_tool",
    "list_notion_tools"
  ],
  "denied": ["admin_*"]
}
```
Access: Notion only

### Read-only User
```json
{
  "mode": "whitelist",
  "allowed": [
    "ping",
    "list_tools",
    "get_service_health"
  ],
  "denied": ["*_create*", "*_update*", "*_delete*", "*_execute*"]
}
```
Access: Read operations only

## Tool Categories

| Category | Tools |
|----------|-------|
| Meta | `ping`, `list_tools`, `get_service_health` |
| Notion | `invoke_notion_tool`, `list_notion_tools` |
| n8n | `n8n_list_workflows`, `n8n_get_workflow`, `n8n_create_workflow`, `n8n_execute_workflow` |
| Slack | `slack_post_message`, `slack_get_channel_history` |
| Agent | `agent_execute` |

## Wildcard Patterns

- `n8n_*` - All n8n tools
- `slack_*` - All Slack tools
- `admin_*` - All admin tools
- `*_create*` - All create operations
- `*_delete*` - All delete operations
- `*_execute*` - All execute operations
