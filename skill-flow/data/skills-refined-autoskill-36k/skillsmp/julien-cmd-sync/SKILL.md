---
name: julien-cmd-sync
description: Sync core skills, commands, and scripts from marketplace to ~/.claude/
author: Julien
version: 1.0.0
category: infrastructure
type: command
triggers:
  - sync skills
  - synchronize marketplace
  - update global skills
  - sync core
  - mettre à jour les skills
  - synchroniser le marketplace
  - sync commands
  - sync scripts
  - marketplace sync
---

# Sync Marketplace to Global

Synchronize skills, commands, and scripts from the marketplace to your global `~/.claude/` folder.

## What to sync

Read `registry/sync-config.json` for the list of:
- `home_files_to_sync`: Files to copy to `~/.claude/` root (settings.json)
- `skills_to_sync`: Skills to copy to `~/.claude/skills/`
- `commands_to_sync`: Commands to copy to `~/.claude/commands/`
- `scripts_to_sync`: Scripts to copy to `~/.claude/scripts/`
- `configs_to_sync`: Configs to copy to `~/.claude/registry/`

## Execute

```bash
# 0. Generate skill-triggers.json from SKILL.md YAML frontmatter
python scripts/generate-triggers.py && echo "✓ triggers regenerated"

# 1. Create directories
mkdir -p ~/.claude/skills ~/.claude/commands ~/.claude/scripts ~/.claude/configs

# 2. Sync skills
for skill in $(cat registry/sync-config.json | jq -r '.skills_to_sync[]'); do
  cp -r "skills/$skill" ~/.claude/skills/ 2>/dev/null && echo "✓ skill: $skill"
done

# 3. Sync commands
for cmd in $(cat registry/sync-config.json | jq -r '.commands_to_sync[]'); do
  cp ".claude/commands/$cmd" ~/.claude/commands/ 2>/dev/null && echo "✓ cmd: $cmd"
done

# 4. Sync scripts
for script in $(cat registry/sync-config.json | jq -r '.scripts_to_sync[]'); do
  cp "scripts/$script" ~/.claude/scripts/ 2>/dev/null && echo "✓ script: $script"
done

# 5. Sync configs
for cfg in $(cat registry/sync-config.json | jq -r '.configs_to_sync[]'); do
  cp "registry/$cfg" ~/.claude/registry/ 2>/dev/null && echo "✓ config: $cfg"
done

# 6. Sync home files (settings.json, etc.)
for file in $(cat registry/sync-config.json | jq -r '.home_files_to_sync[]'); do
  cp "home/$file" ~/.claude/ 2>/dev/null && echo "✓ home: $file"
done
```

## After sync

- Skills available globally in all projects
- Commands available with `/sync` and `/list-resources`
- Scripts available for hooks (semantic-router, tracking)
- MCP registry available for `discover-mcps.py` and `mcp-auto-install.py`

## MCP Management

After syncing, you can use these MCP tools:

```bash
# Discover installed vs available MCPs
python ~/.claude/scripts/discover-mcps.py

# Install a specific MCP globally
python ~/.claude/scripts/mcp-auto-install.py notion

# Install in project only
python ~/.claude/scripts/mcp-auto-install.py playwright --project

# Install all recommended MCPs
python ~/.claude/scripts/mcp-auto-install.py --recommended

# List available MCPs
python ~/.claude/scripts/mcp-auto-install.py --list
```
