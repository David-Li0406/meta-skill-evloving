---
name: plugin-creator
description: Guide for creating Claude Code plugins. Use when user asks to "create a plugin", "build a plugin", "develop a plugin", "understand plugin structure", "implement commands/agents/skills/hooks", or "troubleshoot plugin issues". Covers component structure, best practices, validation, and common patterns for production-ready plugins.
---

# Plugin Creator

Comprehensive guide for creating high-quality Claude Code plugins.

## Quick Start

### Option 1: Use Helper Scripts (Recommended)

```bash
# Initialize a new plugin
python skills/plugin-creator/scripts/init_plugin.py my-plugin

# Validate your plugin
python skills/plugin-creator/scripts/validate_plugin.py my-plugin

# Package for distribution
python skills/plugin-creator/scripts/package_plugin.py my-plugin
```

### Option 2: Manual Setup

```bash
mkdir my-plugin
cd my-plugin
# Create required files
touch .plugin.json README.md
mkdir -p commands agents skills hooks
```

## Plugin Components

A Claude Code plugin consists of:

- **.plugin.json**: Plugin manifest (required)
- **README.md**: User documentation (required)
- **Commands/**: User-invoked slash commands (optional)
- **Agents/**: Autonomous task handlers (optional)
- **Skills/**: Specialized knowledge domains (optional)
- **Hooks/**: Event-driven automation (optional)

## Core Workflow

### 1. Create Manifest (.plugin.json)

```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "Brief plugin description",
  "commands": ["command1", "command2"],
  "agents": ["agent1"],
  "skills": ["skill1"],
  "hooks": {
    "PreToolUse": ["hook1"],
    "PostToolUse": ["hook2"]
  }
}
```

**Required fields:** `name`, `version`, `description`

### 2. Implement Components

Choose component types based on needs. See [COMPONENTS.md](references/COMPONENTS.md) for complete templates.

**Quick Templates:**

- **Commands** (commands/command-name.md): User-invoked actions
  - Use for: Code generation, analysis, quick actions

- **Agents** (agents/agent-name.md): Complex autonomous tasks
  - Use for: Multi-file operations, analysis workflows

- **Skills** (skills/skill-name.md): Specialized knowledge
  - Use for: Domain expertise, best practices, patterns

- **Hooks** (hooks/event-type/hook-name.md): Event automation
  - Use for: Validation, logging, cleanup

### 3. Naming Conventions

- Plugin names: `kebab-case`, descriptive
- Command names: Verb-based (`commit`, not `create-commit`)
- Agent names: Role-based (`code-reviewer`)
- Skill names: Domain-based (`react-patterns`)

### 4. Validation & Packaging

Use helper scripts:

```bash
# Validate plugin structure and content
python skills/plugin-creator/scripts/validate_plugin.py my-plugin

# Package plugin for distribution
python skills/plugin-creator/scripts/package_plugin.py my-plugin ./dist
```

Or manually:

```bash
# Validate JSON
python3 -m json.tool .plugin.json

# Check structure
ls -R

# Test installation
cp -r my-plugin ~/.claude/plugins/
```

## Reference Documentation

For detailed guides, see [references/README.md](references/README.md) for a complete index.

**Quick links:**
- **[COMPONENTS.md](references/COMPONENTS.md)** - Complete templates with examples
- **[PATTERNS.md](references/PATTERNS.md)** - Common patterns
- **[TROUBLESHOOTING.md](references/TROUBLESHOOTING.md)** - Debug guide

## Advanced Features

### MCP Server Integration

Integrate external tools via `.mcp.json`:

```json
{
  "mcpServers": {
    "server-name": {
      "type": "sse",
      "url": "http://localhost:3000/sse"
    }
  }
}
```

See [MCP.md](references/MCP.md) for server types and configuration.

### Plugin Configuration

Use `.local.md` files for user settings:

```yaml
---
setting1: value1
enabled: true
---
```

Read from: `${CLAUDE_PLUGIN_ROOT}/../plugin-name.local.md`

## Component Templates

### Command Template

```markdown
---
description: [Brief action description, max 100 chars]
args:
  - name: arg_name
    description: What this argument does
    required: false
---

# Command Title

[Clear instructions for what Claude should do]

## Process

1. First step
2. Second step
3. Final step

## Examples

- `command-name arg1` - What happens
- `command-name arg1 --flag` - With flag
```

### Agent Template

```markdown
---
description: When to trigger this agent (be specific)
color: blue
tools:
  - Read
  - Write
  - Bash
examples:
  - trigger: "User asks to..."
    action: "Launch this agent to..."
---

# Agent Name

You are a specialized agent for [purpose].

## Your Process

### Phase 1: Analysis
[Detailed steps]

### Phase 2: Execution
[Detailed steps]
```

### Hook Template

```markdown
---
description: What this hook does and when
---

# Hook Title

Instructions for event handling.

## Behavior

[What the hook should do]

## Conditions

[When to act - optional]
```

See [COMPONENTS.md](references/COMPONENTS.md) for detailed templates with strict/flexible examples.

## Common Patterns

See [PATTERNS.md](references/PATTERNS.md) for:
- Command + Agent pattern
- Skill + Command pattern
- Hook + Validation pattern
- Multi-component plugins
- And more

## Troubleshooting

See [TROUBLESHOOTING.md](references/TROUBLESHOOTING.md) for:
- Plugin not loading
- Command/agent/hook not working
- YAML frontmatter errors
- Common issues and solutions

## Best Practices

- Keep descriptions under 100 characters
- Use imperative form in instructions
- Include practical examples
- Validate all JSON/YAML syntax
- Test all components before distribution
- Handle errors gracefully

## Validation Checklist

- [ ] .plugin.json valid and complete
- [ ] README.md with installation steps
- [ ] All declared components exist
- [ ] YAML frontmatter valid
- [ ] Names follow conventions
- [ ] Components tested
- [ ] Examples provided

## Resources

- Official docs: https://code.claude.com/docs/zh-CN/plugins
- Built-in examples: `~/.claude/plugins/`
- Community plugins: GitHub search "claude-code-plugin"
