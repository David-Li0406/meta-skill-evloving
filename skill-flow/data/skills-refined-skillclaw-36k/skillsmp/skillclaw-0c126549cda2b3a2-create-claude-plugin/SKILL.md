---
name: create-claude-plugin
description: Use this skill when you need to create a new Claude plugin from scratch with the standard directory structure and necessary files.
---

# Create Claude Plugin

## When to Use This Skill

Use this skill when:
- Creating a new Claude Code plugin from scratch
- Setting up the standard plugin directory structure
- Adding a new plugin to the ClaudeKit marketplace

**Trigger phrases:**
- "create a new plugin"
- "scaffold a plugin for X"
- "add a plugin called X"

## Instructions

1. Use the `Glob` tool to check if the plugin already exists.
2. Use the Ask Question Tool to confirm overwriting if the plugin already exists.
3. Create a new directory for the plugin.
4. Create a minimal plugin structure.
5. Update the plugin metadata file (`plugin.json`) with basic information:
    ```json
    {
        "name": "plugin-name",
        "version": "0.1.0",
        "description": "A brief description of the plugin",
        "author": {
            "name": "Author Name"
        }
    }
    ```
6. Update the root `README.md` to include the new plugin.
7. Update `.claude-plugin/marketplace.json` to include the new plugin.
8. Update the release configuration to include the new plugin.

## Plugin Structure

```
|- .claude-plugin/
    |- plugin.json
|- commands/ # Omit if no commands
    |- example.md
|- agents/ # Omit if no agents
    |- example-agent.md
|- skills/ # Omit if no skills
    |- example-skill/
        |- SKILL.md
|- hooks/ # Omit if no hooks
    |- hooks.json
|- src/ # Omit if no hook script is needed
    |- example.ts
|- dist/ # Auto-generated, omit
    |- example.js
|- README.md
|- rolldown.config.js # Omit if no src
|- package.json # Omit if no src
|- tsconfig.json # Omit if no src
```

## Reference

For detailed information on creating Claude plugins, refer to the following documentation:

- [Claude Plugin Reference](https://docs.claude.com/en/docs/claude-code/plugins-reference)
- [Claude Hook Reference](https://docs.claude.com/en/docs/claude-code/hooks)
- [Claude Agent](https://docs.claude.com/en/docs/claude-code/sub-agents)
- [Claude Agent Skill](https://docs.claude.com/en/docs/claude-code/skills)