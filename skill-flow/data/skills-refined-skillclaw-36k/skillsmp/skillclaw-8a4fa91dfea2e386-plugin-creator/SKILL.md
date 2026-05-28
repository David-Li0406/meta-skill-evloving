---
name: plugin-creator
description: Use this skill when creating, managing, or validating Claude Code plugins, including their structure, manifests, and marketplace integration.
---

# Skill body

## Purpose

This skill helps you create, manage, and validate Claude Code plugins with the correct structure, including manifests and marketplace integration.

## When to Use

- Creating new plugins for a marketplace
- Adding or modifying plugin components (commands, skills, agents, hooks)
- Updating plugin versions
- Working with plugin or marketplace manifests
- Validating existing plugins against standards
- Setting up local plugin testing
- Publishing plugins

## Getting Started

### Create New Plugin

To generate a plugin structure, use the following command:

```bash
python scripts/create_plugin.py plugin-name \
  --marketplace-root /path/to/marketplace \
  --author-name "Your Name" \
  --author-email "your.email@example.com" \
  --description "Plugin description" \
  --keywords "keyword1,keyword2" \
  --category "productivity"
```

This command will automatically:
- Create the plugin directory structure
- Generate the `plugin.json` manifest
- Create a README template
- Update the `marketplace.json`

### Bump Version

To update versions in both manifests, use:

```bash
python scripts/bump_version.py plugin-name major|minor|patch \
  --marketplace-root /path/to/marketplace
```

### Plugin Structure

The basic structure of a plugin should look like this:

```
plugin-name/
  .claude-plugin/
    plugin.json
  commands/
  skills/
  hooks/
  agents/
```

### Plugin Manifest

The `plugin.json` file should include the following required fields:

```json
{
  "name": "plugin-name",
  "version": "0.1.0",
  "description": "Plugin description",
  "author": {
    "name": "Your Name",
    "email": "your.email@example.com"
  },
  "keywords": ["keyword1", "keyword2"]
}
```

### Validate Plugin Structure

Always validate your plugin after creating or modifying it:

```bash
uv run .claude/skills/meta-plugin-creator/scripts/validate-plugin.py path/to/plugin-name
```

Fix any errors before publishing.

### Register in Marketplace

Update the `marketplace.json` file as follows:

```json
{
  "name": "plugin-name",
  "source": "./plugins/plugin-name",
  "description": "Plugin description",
  "version": "0.1.0",
  "keywords": ["keyword1", "keyword2"],
  "category": "productivity"
}
```

## Important Notes

- Ensure that the `name` field in the manifest is in kebab-case with no spaces.
- Use Agent Skills instead of slash commands for new plugins, as slash commands are being deprecated.
- This skill is not intended for debugging plugin behavior at runtime or writing plugin code directly; it focuses on structure and organization.