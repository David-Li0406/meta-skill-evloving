---
name: plugin-management
description: Use this skill when creating, managing, and distributing Claude Code plugins, including their structure, manifests, and marketplace integration.
---

# Plugin Management

## Purpose

This skill provides workflows for creating, managing, and distributing Claude Code plugins. It covers the necessary structure, manifest generation, and marketplace configuration.

## When to Use

Activate this skill when discussing:
- Plugin creation and management
- Bundling and packaging plugins
- Understanding plugin structure and manifest files
- Distributing skills, commands, agents, and hooks to a marketplace

## Getting Started

### Create New Plugin

To create a new plugin structure, use the following command:

```bash
python scripts/create_plugin.py <plugin-name> \
  --marketplace-root /path/to/marketplace \
  --author-name "Your Name" \
  --author-email "your.email@example.com" \
  --description "Plugin description" \
  --keywords "keyword1,keyword2" \
  --category "productivity"
```

This command will:
- Create the necessary directory structure
- Generate the `plugin.json` manifest
- Create a README template

### Plugin Manifest

The `plugin.json` file is essential for defining your plugin. Here’s a basic structure:

```json
{
  "name": "<plugin-name>",
  "version": "0.1.0",
  "description": "Plugin description",
  "author": {
    "name": "Your Name",
    "email": "your.email@example.com"
  },
  "keywords": ["keyword1", "keyword2"]
}
```

### Validate Plugin

After creating or modifying a plugin, always validate it:

```bash
uv run .claude/skills/meta-plugin-creator/scripts/validate-plugin.py path/to/<plugin-name>
```

This will check for required fields and correct structure.

## Core Operations

### 1. Create Plugin Structure

To create a plugin structure manually, follow these steps:

1. Create the main plugin directory and manifest:
   ```bash
   mkdir -p <plugin-name>/.claude-plugin
   echo '{"name": "<plugin-name>", "version": "0.1.0"}' > <plugin-name>/.claude-plugin/plugin.json
   ```

2. Create component directories:
   ```bash
   mkdir -p <plugin-name>/{commands,skills,hooks,agents}
   ```

### 2. Bundle Components

To bundle components by a prefix (e.g., "git"), follow these steps:

1. Use glob patterns to find matching files:
   ```bash
   commands/**/{prefix}-*.md
   skills/**/{prefix}-*/**
   ```

2. Create the plugin structure and copy matched components into it.

### 3. Create Marketplace Config

To create a `marketplace.json` file, use the following template:

```json
{
  "name": "MARKETPLACE",
  "owner": {
    "name": "OWNER"
  },
  "plugins": [
    {
      "name": "<plugin-name>",
      "source": "./path",
      "description": "Plugin description"
    }
  ]
}
```

### 4. Validate Plugin Structure

To validate the plugin structure, ensure:
- The `plugin.json` file exists and is valid JSON.
- Required fields like `name` and `version` are present.
- All component directories exist and contain the correct file types.

### 5. Pack for Distribution

To prepare a plugin for distribution:
1. Validate the plugin.
2. Optionally remove files specified in `.gitignore`.
3. Create a tarball if needed:
   ```bash
   tar -czf <plugin-name>.tar.gz -C <plugin-name> .
   ```

## Common Mistakes

- Ensure components are not placed inside the `.claude-plugin/` directory.
- Use relative paths in manifests.
- Validate plugins before distribution.

## References

- Official Plugins Reference: [code.claude.com/docs/en/plugins-reference](https://code.claude.com/docs/en/plugins-reference)
- Discover Plugins: [code.claude.com/docs/en/discover-plugins](https://code.claude.com/docs/en/discover-plugins)
- Plugin Marketplaces: [code.claude.com/docs/en/plugin-marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)