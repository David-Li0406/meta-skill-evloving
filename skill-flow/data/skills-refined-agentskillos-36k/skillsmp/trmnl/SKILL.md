---
name: trmnl
description: Manage TRMNL e-ink displays - push messages, control playlists, check device status. Use when user mentions TRMNL, e-ink display, or wants to push content to their display.
triggers:
  - TRMNL display management
  - Push content to display
  - Check what's showing on display
  - E-ink display control
---

# TRMNL MCP Server

Manage TRMNL e-ink displays from Claude Code via MCP.

## When to Use

Use this skill when:
- User wants to push a message or content to their TRMNL display
- User asks what's currently showing on their display
- User wants to manage display playlists or plugins
- User mentions "TRMNL", "e-ink display", or display management

## Available MCP Tools

| Tool | Description |
|------|-------------|
| `trmnl_list_devices` | List all TRMNL devices |
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

## Common Workflows

### Push a Custom Message
```
1. Use trmnl_push_webhook with title and optional body
2. The display updates at its next refresh interval
```

### Check Current Display
```
1. Use trmnl_get_current_screen to see what's showing
2. Use trmnl_list_playlist to see the full rotation
```

### Manage Playlist
```
1. Use trmnl_list_playlist to see all items
2. Use trmnl_toggle_playlist_item to enable/disable specific items
3. Use trmnl_advance_screen to skip to next item
```

## Rate Limits

Be aware of TRMNL's rate limits:
- **Webhook pushes**: 12x/hour (standard) or 30x/hour (TRMNL+)
- **Data size**: 2kb (standard) or 5kb (TRMNL+)

Don't exceed these limits when pushing content.

## Setup

Credentials are stored via deep-env:
```bash
deep-env store TRMNL_API_KEY "user_xxxxx"
```

## Example Usage

**Push a focus message:**
"Push a message to my TRMNL that says 'Focus: Building feature X'"

**Check display status:**
"What's currently showing on my TRMNL?"

**List devices:**
"Show me my TRMNL devices"
