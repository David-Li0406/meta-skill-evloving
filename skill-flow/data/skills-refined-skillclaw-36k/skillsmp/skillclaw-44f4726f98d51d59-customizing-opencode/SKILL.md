---
name: customizing-opencode
description: Use this skill when setting up or modifying OpenCode configuration through various files and settings.
---

# Customizing OpenCode

Configure OpenCode behavior through `opencode.json`, agents, commands, and extensions.

## Config File Locations

| Location | Path | Purpose |
|----------|------|---------|
| Global | `~/.config/opencode/opencode.json` | User-wide preferences |
| Project | `./opencode.json` | Project-specific settings |
| Custom | `$OPENCODE_CONFIG` env var | Override path |

**Precedence** (later overrides earlier): Remote `.well-known/opencode` < Global < Custom < Project

## Quick Reference

| Task | Where | Reference |
|------|-------|-----------|
| Set theme, model, autoupdate | `opencode.json` | [config-schema.md](references/config-schema.md) |
| Define specialized agents | `.opencode/agents/*.md` or config | [agents.md](references/agents.md) |
| Create slash commands | `.opencode/commands/*.md` or config | [commands.md](references/commands.md) |
| Add external tools via MCP | `opencode.json` `mcp` section | [mcp-servers.md](references/mcp-servers.md) |
| Write custom tool functions | `.opencode/tools/*.ts` | [custom-tools.md](references/custom-tools.md) |
| Extend with plugins/hooks | `.opencode/plugins/*.ts` or npm | [plugins.md](references/plugins.md) |
| Control tool access | `opencode.json` `permission` section | [permissions.md](references/permissions.md) |
| Customize keyboard shortcuts | `opencode.json` `keybinds` section | [keybinds.md](references/keybinds.md) |
| Change colors/appearance | `opencode.json` `theme` or custom JSON | [themes.md](references/themes.md) |

## Directory Structure

```
~/.config/opencode/           # Global config
├── opencode.json
├── AGENTS.md                 # Global rules
├── agents/                   # Global agents
├── commands/                 # Global commands
├── plugins/                  # Global plugins
├── skills/                   # Global skills
├── tools/                    # Global custom tools
└── themes/                   # Global custom themes

.opencode/                    # Project config (same structure)
├── agents/
├── commands/
├── plugins/
├── skills/
├── tools/
└── themes/
```

## When to Use What

| Need | Solution |
|------|----------|
| Change model/theme for all projects | Global `opencode.json` |
| Project-specific agent behavior | Project `.opencode/agents/*.md` |
| Add custom commands | Project `.opencode/commands/*.md` |
| Extend functionality with plugins | Project `.opencode/plugins/*.ts` |
| Control access to tools | `opencode.json` `permission` section |
| Customize keyboard shortcuts | `opencode.json` `keybinds` section |
| Change appearance | `opencode.json` `theme` or custom JSON |