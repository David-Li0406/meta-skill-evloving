---
name: help
description: Show help for Vocal Bridge Claude Code plugin commands
---

# Vocal Bridge Plugin Commands

| Command | Description |
|---------|-------------|
| `/vocal-bridge:login [api_key]` | Authenticate with API key |
| `/vocal-bridge:status` | Check authentication status |
| `/vocal-bridge:agent` | Show agent information |
| `/vocal-bridge:logs [session_id]` | View call logs |
| `/vocal-bridge:download <session_id>` | Download call recording |
| `/vocal-bridge:stats` | Show call statistics |
| `/vocal-bridge:prompt [show\|set]` | Manage system prompt |
| `/vocal-bridge:config [show\|set\|edit\|options]` | Manage all agent settings |
| `/vocal-bridge:debug` | Stream debug events |
| `/vocal-bridge:setup` | Install CLI if needed |

## Getting Started

1. Get your API key from your agent detail page at https://vocalbridgeai.com
2. Run `/vocal-bridge:login vb_your_api_key` to authenticate
3. Use `/vocal-bridge:agent` to verify connection

## Examples

```
# Login with your API key
/vocal-bridge:login vb_abc123xyz

# Check connection status
/vocal-bridge:status

# View recent call logs
/vocal-bridge:logs

# View last 50 failed calls
/vocal-bridge:logs -n 50 --status failed

# View specific call transcript
/vocal-bridge:logs 550e8400-e29b-41d4-a716-446655440000

# Download call recording
/vocal-bridge:download 550e8400-e29b-41d4-a716-446655440000

# Show call statistics
/vocal-bridge:stats

# View current prompt
/vocal-bridge:prompt show

# View all agent settings
/vocal-bridge:config show

# Show valid options for a setting (ALWAYS do this before changing settings)
/vocal-bridge:config options voice
/vocal-bridge:config options "TTS Model"

# Update agent settings
/vocal-bridge:config set --debug-mode true

# Edit full config in editor
/vocal-bridge:config edit

# Stream debug events
/vocal-bridge:debug
```

## CLI Installation

The plugin automatically installs the CLI when needed. You can also install manually:

```bash
pip install vocal-bridge
```

Or download the standalone script:

```bash
curl -fsSL https://vocalbridgeai.com/cli/vb.py -o vb && chmod +x vb
```

## More Information

- Documentation: https://vocalbridgeai.com/docs/developer-guide
- Dashboard: https://vocalbridgeai.com
- GitHub: https://github.com/vocalbridgeai/vocal-bridge-claude-plugin
