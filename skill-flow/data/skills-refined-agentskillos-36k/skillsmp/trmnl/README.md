# TRMNL MCP Server

MCP server for managing [TRMNL](https://usetrmnl.com) e-ink displays from Claude Code.

## Setup

1. Get your API key from https://usetrmnl.com (Account settings, starts with `user_`)
2. Store with deep-env: `deep-env store TRMNL_API_KEY "user_xxxxx"`

## Available Tools

| Tool | Description |
|------|-------------|
| `trmnl_list_devices` | List all your TRMNL devices |
| `trmnl_get_device` | Get device details (battery, signal, etc.) |
| `trmnl_update_device` | Update sleep mode settings |
| `trmnl_get_current_screen` | See what's currently displayed |
| `trmnl_advance_screen` | Move to next screen in playlist |
| `trmnl_list_playlist` | List playlist items |
| `trmnl_toggle_playlist_item` | Show/hide playlist items |
| `trmnl_list_plugins` | List plugin settings |
| `trmnl_get_plugin_data` | Get plugin data/variables |
| `trmnl_update_plugin_data` | Update plugin data |
| `trmnl_push_webhook` | Push custom content to display |
| `trmnl_get_webhook_content` | Get current webhook content |
| `trmnl_get_account` | Get account info |
| `trmnl_delete_plugin` | Delete a plugin |

## Example Usage

```
# List your devices
"Show me my TRMNL devices"

# Push custom content
"Push a message to my TRMNL that says 'Focus: Building feature X'"

# Check what's displayed
"What's currently showing on my TRMNL?"
```

## Rate Limits

- Webhook pushes: 12x/hour (standard) or 30x/hour (TRMNL+)
- Data size: 2kb (standard) or 5kb (TRMNL+)
