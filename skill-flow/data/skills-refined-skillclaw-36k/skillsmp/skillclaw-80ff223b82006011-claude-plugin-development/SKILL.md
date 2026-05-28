---
name: claude-plugin-development
description: Use this skill when creating, validating, and distributing Claude Code plugins, especially when dealing with "plugin.json", "marketplace", or related commands.
---

# Claude Plugin Development

This skill covers the complete lifecycle for developing, validating, and distributing Claude Code plugins.

## Quick Start

```bash
# 1. Scaffold plugin
./scripts/scaffold-plugin.sh my-plugin --with-commands

# 2. Add components (commands, agents, hooks, skills)
# 3. Test locally
/plugin marketplace add ./my-plugin
/plugin install my-plugin@my-plugin

# 4. Distribute
git push origin main --tags
```

## Lifecycle Overview

```
Discovery -> Init -> Components -> Validate -> Distribute -> Marketplace
    |         |          |            |            |             |
    v         v          v            v            v             v
 Purpose   Scaffold   Commands    Structure    Package      Catalog
  Scope    plugin.json  Agents     Testing     Version      Publish
  Type      README      Hooks      Quality     Release       Share
```

## Phase 1: Discovery

Before creating a plugin, clarify:

| Question | Impact |
|----------|--------|
| What problem does this solve? | Plugin scope and features |
| Who will use it? | Distribution method |
| What components are needed? | Commands, agents, hooks, MCP servers |
| Where will it live? | Personal, project, or marketplace |

## Phase 2: Initialization

### Plugin Structure

#### Standalone Plugin Structure

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json      # Required: metadata
├── README.md            # Required for distribution
└── commands/            # Optional components
```

#### Marketplace Structure

```
my-marketplace/
├── .claude-plugin/
│   └── marketplace.json # Defines all plugins
├── plugin-a/            # No .claude-plugin/ here
│   └── commands/
├── plugin-b/
```

### plugin.json (Required)

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "Brief description of what this plugin does",
  "author": {
    "name": "Your Name",
    "email": "you@example.com"
  },
  "license": "MIT"
}
```

### Using the Scaffold Script

```bash
./scripts/scaffold-plugin.sh my-plugin \
  --author "Your Name" \
  --with-commands \
  --with-agent \
  --with-hooks
```

## Phase 3: Components

Add components based on plugin needs. For detailed component authoring, refer to the relevant documentation.