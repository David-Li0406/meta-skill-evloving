---
name: claude-skills
description: Help with creating and managing Claude Code skills. Use when the user asks about creating skills, skill structure, or customizing Claude Code behavior.
---

# Claude Code Skills

## Overview

Skills are custom prompts that extend Claude Code's capabilities for specific tools, configurations, or workflows. They're project-specific or user-specific context that Claude can invoke when relevant.

## Skill Location

**User skills**: `~/.claude/skills/<skill-name>/SKILL.md`

Each skill is a directory containing a `SKILL.md` file.

## Skill Structure

```markdown
---
name: skill-name
description: Brief description of when to use this skill. Claude uses this to decide when to invoke the skill.
---

# Skill Title

## Overview
Brief explanation of what this skill helps with.

## Configuration Locations
Paths to relevant config files, if applicable.

## Key Concepts
Important information Claude should know.

## When Helping Users
Guidelines for how to approach tasks with this skill.

## Common Tasks
Examples of what users might ask for.

## Best Practices
Tips and recommendations.

## Troubleshooting
Common issues and solutions.
```

## Frontmatter Requirements

The YAML frontmatter at the top is critical:

```yaml
---
name: skill-name          # Must match directory name
description: When to use this skill. Be specific about triggers like "when user asks about X, Y, or Z"
---
```

The `description` field should:
- Be clear and specific
- Mention key terms that would trigger the skill
- Explain the scope (e.g., "configuration", "debugging", "setup")

## Creating a New Skill

1. **Create directory**:
   ```bash
   mkdir -p ~/.claude/skills/my-skill
   ```

2. **Create SKILL.md**:
   ```bash
   nvim ~/.claude/skills/my-skill/SKILL.md
   ```

3. **Add frontmatter and content**:
   - Start with YAML frontmatter
   - Include relevant paths, commands, and context
   - Reference official documentation when applicable
   - Add examples and common patterns

4. **Test the skill**:
   - Restart Claude or start a new conversation
   - Ask questions that should trigger the skill
   - Verify Claude has the right context

## Skill Examples

### aerospace skill
- **Purpose**: Help with AeroSpace window manager config
- **Includes**: Config locations, documentation links, TOML format help
- **Triggers**: "AeroSpace", "window management", "tiling"

### lazyvim skill
- **Purpose**: Help with LazyVim/Neovim configuration
- **Includes**: Plugin management, keybindings, LSP setup
- **Triggers**: "LazyVim", "Neovim", "plugins", "editor"

### tmux skill
- **Purpose**: Help with tmux/tmuxinator/sesh setup
- **Includes**: Template structure, session management, layouts
- **Triggers**: "tmux", "tmuxinator", "sessions", "terminal multiplexing"

## Best Practices

1. **Be specific in descriptions**: Help Claude know exactly when to use the skill
2. **Include file paths**: Direct paths make it easy to read/edit configs
3. **Reference documentation**: Link to official docs for authoritative info
4. **Add examples**: Show concrete examples of common patterns
5. **Keep it focused**: One skill per tool/domain
6. **Update regularly**: Keep skills current with your actual setup

## When to Create a Skill

Create a skill when:
- You have a complex tool configuration (e.g., tmux, vim, window manager)
- You want Claude to remember specific project patterns
- There are non-obvious conventions or workflows
- You frequently ask Claude about the same topic
- You have custom aliases, functions, or scripts

Don't create a skill for:
- Simple one-off tasks
- Standard tools without customization
- Information that's better in documentation

## Skill Scope

**Project skills** (if supported): Specific to a single project
**User skills**: Available across all Claude sessions for your user

User skills go in `~/.claude/skills/` and are always available.

## Invoking Skills

Claude automatically decides when to invoke skills based on:
- The skill's `description` field
- Keywords in the user's question
- Context of the conversation

You can also explicitly mention the tool/topic to trigger the skill.

## Debugging Skills

If a skill isn't being used:
1. Check the `description` field - is it specific enough?
2. Verify the YAML frontmatter is valid
3. Ensure `name:` matches the directory name
4. Try explicitly mentioning keywords from the description
5. Restart Claude or start a new conversation
