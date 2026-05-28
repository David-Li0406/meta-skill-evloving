---
name: config
description: View and update all agent configuration settings including style, capabilities, MCP servers, and more.
allowed-tools: Bash, Read, Write
---

Manage the voice agent's full configuration settings.

First ensure CLI is installed:

```bash
pip install --upgrade vocal-bridge
```

## Commands

### Discover valid options

**IMPORTANT**: Before updating settings, use `vb config options` to discover valid values. This prevents errors from invalid values.

```bash
# Show all available options for current agent style
vb config options

# Show options for a specific setting (by name or label)
vb config options voice
vb config options "TTS Model"

# Show all settings in a category
vb config options audio
vb config options realtime

# Output as JSON
vb config options --json
```

### Show all settings

```bash
vb config show
```

Shows all agent settings in a readable format including:
- Core settings (style, deploy targets)
- Capabilities (background AI, hold, hangup, debug mode)
- Greeting and system prompt
- Model settings
- MCP servers
- Post-processing configuration
- Built-in integrations

For JSON output:

```bash
vb config show --json
```

### Update individual settings

```bash
vb config set [OPTIONS]
```

Available options:
- `--name NAME` - Agent name
- `--style STYLE` - Agent style (Chatty, Focused, Gemini, Ultravox)
- `--greeting TEXT` - Greeting message (use '' to clear)
- `--prompt TEXT` - System prompt (use '' to clear)
- `--deploy-targets TARGET` - Deploy targets (phone, web, both)
- `--background-enabled true|false` - Enable background AI system
- `--hold-enabled true|false` - Enable hold capability
- `--hangup-enabled true|false` - Enable hangup capability
- `--debug-mode true|false` - Enable debug event streaming
- `--post-processing-prompt TEXT` - Post-processing prompt
- `--post-processing-mcp-url URL` - Post-processing MCP server URL
- `--model-settings-file FILE` - JSON file with model settings
- `--mcp-servers-file FILE` - JSON file with MCP servers array
- `--builtin-tools-file FILE` - JSON file with built-in tools config

Examples:

```bash
# Change agent style
vb config set --style Focused

# Enable debug mode
vb config set --debug-mode true

# Update multiple settings
vb config set --name "My Agent" --hold-enabled true --hangup-enabled true

# Set MCP servers from file
vb config set --mcp-servers-file mcp_servers.json
```

### Edit full configuration

Opens the full configuration in $EDITOR as JSON:

```bash
vb config edit
```

This allows editing all settings at once. Save and close the editor to apply changes.

## Based on $ARGUMENTS

Determine user intent from $ARGUMENTS:
- "options" or "valid" -> show valid options with `vb config options`
- "options <name>" -> show options for specific setting
- "show" or empty -> show all settings with `vb config show`
- "show --json" or "json" -> show as JSON
- "set" with options -> update specific settings
- "edit" -> open full config in editor
- Contains setting names -> first run `vb config options <setting>` to show valid values, then use `vb config set`

**Best Practice**: When user wants to change a setting, ALWAYS run `vb config options <setting>` first to show them valid values before making changes.

## Agent Styles

| Style | Description |
|-------|-------------|
| **Chatty** | Best for snappy, low-latency conversations. Ideal when most context fits in the system prompt and you only need 1-2 tools. |
| **Focused** | Best for information-heavy conversations like interviews, data collection, or surveys. More thorough responses. |
| **Gemini** | Powered by Google Gemini Live API. Great for natural, flowing conversations with multimodal capabilities. |
| **Ultravox** | Powered by Ultravox Realtime API. Optimized for voice-first interactions with native audio understanding. |

## JSON File Formats

### MCP Servers (mcp_servers.json)

```json
[
  {
    "url": "https://actions.zapier.com/mcp/...",
    "name": "Zapier",
    "tools": []
  }
]
```

### Model Settings (model_settings.json)

```json
{
  "stt_model": "nova-3",
  "tts_voice": "alloy",
  "temperature": 0.7
}
```

### Built-in Tools (builtin_tools.json)

```json
{
  "lever": {
    "enabled": true,
    "api_key": "...",
    "posting_id": "..."
  }
}
```
