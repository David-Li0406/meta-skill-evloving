# Tool Inventory

Current MCP tools in the Hub with their registration status.

## Registered Tools (services/hub/src/tools/registry.cjs)

| Tool | Category | Description |
|------|----------|-------------|
| `ping` | Meta | Test connectivity |
| `list_tools` | Meta | Discover available tools |
| `get_service_health` | Meta | Check service status |
| `invoke_notion_tool` | Notion | Proxy to Notion API |
| `list_notion_tools` | Notion | List Notion operations |
| `n8n_list_workflows` | n8n | List workflows |
| `n8n_get_workflow` | n8n | Get workflow details |
| `n8n_create_workflow` | n8n | Create new workflow |
| `n8n_execute_workflow` | n8n | Execute via webhook |
| `slack_post_message` | Slack | Post to channel |
| `slack_get_channel_history` | Slack | Get message history |
| `agent_execute` | Agent | Run autonomous tasks |

## Tool Categories

| Category | Service | Config Required |
|----------|---------|-----------------|
| Meta | Hub | None |
| Notion | Notion Wrapper | `NOTION_TOKEN` |
| n8n | n8n Instance | `N8N_*` vars |
| Slack | Slack API | `SLACK_*` vars |
| Agent | Agent Worker | `ANTHROPIC_API_KEY_LIMITED` |

## Adding New Tools

See `SKILL.md` for the complete guide on:
1. Creating tool definition in `services/hub/src/tools/`
2. Registering in `registry.cjs`
3. Adding to user whitelists in `clients/`

## Customization

When forking this boilerplate:
1. Remove tools you don't need from registry
2. Add your own tools following the patterns
3. Update user configs with appropriate permissions

## Maintenance

Update this file when adding/removing tools.
