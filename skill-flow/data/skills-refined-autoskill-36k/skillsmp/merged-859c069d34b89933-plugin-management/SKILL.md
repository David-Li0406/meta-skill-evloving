---
name: plugin-management
description: Use this skill for creating, managing, and maintaining Claude Code plugins, including their structure, manifests, and marketplace integration.
---

# Plugin Management

## Purpose

This skill provides workflows for creating, validating, and managing Claude Code plugins, including their directory structure, manifest files, and integration with the marketplace.

## When to Use

- Creating new plugins for a marketplace
- Adding or modifying plugin components (skills, commands, agents, hooks)
- Updating plugin versions
- Working with plugin or marketplace manifests
- Validating plugin structure and compliance
- Managing the marketplace registry

## Getting Started

### Create New Plugin

Use the following commands to generate the plugin structure:

```bash
mkdir -p plugins/<plugin-name>/.claude-plugin
mkdir -p plugins/<plugin-name>/skills
mkdir -p plugins/<plugin-name>/agents
mkdir -p plugins/<plugin-name>/commands
```

Create the `plugin.json` manifest:

```json
{
  "name": "<plugin-name>",
  "version": "1.0.0",
  "description": "<Brief description>",
  "author": {
    "name": "Your Name",
    "url": "https://github.com/yourusername"
  },
  "repository": "https://github.com/yourusername/<plugin-name>",
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"]
}
```

### Validate Plugin Structure

After creating or modifying a plugin, validate its structure:

```bash
uv run .claude/skills/meta-plugin-creator/scripts/validate-plugin.py path/to/plugins/<plugin-name>
```

### Bump Version

To update versions in both manifests, use:

```bash
./scripts/bump-version.sh <plugin-name> major|minor|patch
```

### Add Skills, Agents, and Commands

#### Skills

Create a skill in `plugins/<plugin-name>/skills/<skill-name>/SKILL.md`:

```markdown
---
name: <skill-name>
description: <When to use this skill - triggers on keywords/contexts>
---

# Skill Title

## Content

<Skill content - commands, templates, workflows, etc.>
```

#### Agents

Create an agent in `plugins/<plugin-name>/agents/<agent-name>.md`:

```markdown
---
name: <agent-name>
description: <Agent purpose>
model: haiku  # optional
---

# Agent instructions

<Agent system prompt and behavior>
```

#### Commands

Create a command in `plugins/<plugin-name>/commands/<command>.md`:

```markdown
---
name: <command>
description: <What the command does>
---

# Command instructions

<What to do when command is invoked>
```

### Create Marketplace Configuration

Add your plugin to the marketplace by updating the `marketplace.json` file located in `.claude-plugin/`:

```json
{
  "name": "<plugin-name>",
  "version": "1.0.0",
  "description": "<Brief description>",
  "source": "./plugins/<plugin-name>",
  "author": {
    "name": "Your Name",
    "url": "https://github.com/yourusername"
  },
  "keywords": ["keyword1", "keyword2"]
}
```

### Common Commands

- **Create Plugin**: Follow the steps above to create a new plugin.
- **Validate Plugin**: Use the validation command to ensure compliance.
- **Bump Version**: Use the version management script to update plugin versions.
- **Add Components**: Create and add skills, agents, and commands as needed.

## Reference Documentation

- **Plugin Structure**: Follow the directory layout and manifest schema outlined in the documentation.
- **Validation Rules**: Ensure your plugin meets all required standards before publishing.
- **Marketplace Management**: Understand how to manage the marketplace registry and plugin visibility.

## Important Notes

- Always validate your plugin after making changes.
- Use semantic versioning for version management.
- Ensure all components are correctly structured and documented.