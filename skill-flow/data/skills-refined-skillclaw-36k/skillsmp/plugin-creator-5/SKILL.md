---
name: plugin-creator
description: Generate new Claude Code plugin scaffolds with configurable components. Use when users want to create a new plugin, start a plugin project, or scaffold plugin components.
---

# Plugin Creator

Generate well-structured Claude Code plugins following SideQuest marketplace patterns.

## When to Use This Skill

- User wants to create a new plugin
- User asks about plugin structure or scaffolding
- User mentions "new plugin", "create plugin", "plugin template"
- User wants to add components (commands, MCP server, hooks, skills) to a project

## Plugin Components

| Component | Purpose | Files Created |
|-----------|---------|---------------|
| commands | Slash commands users invoke | `commands/*.md` |
| mcp-server | Tools Claude can call | `mcp/{name}/index.ts` |
| hooks | Event handlers | `hooks/hooks.json` |
| skills | Autonomous capabilities | `skills/{name}/SKILL.md` |

## Implementation Types

| Type | Use Case | Structure |
|------|----------|-----------|
| Markdown only | Commands/skills are just prompts | No src/, stub scripts |
| TypeScript | CLI tools, utilities, testable logic | src/, full scripts |

**Note**: MCP server component auto-selects TypeScript (code required).

## Quick Reference

### Create Plugin
```
/plugin-template:create my-plugin
```
Then select:
1. Components (commands, mcp-server, hooks, skills)
2. Implementation type (markdown or typescript)

### Strip TypeScript
```
/plugin-template:strip my-plugin
```
Converts TypeScript plugin to markdown-only.

### Upgrade to TypeScript
```
/plugin-template:upgrade my-plugin
```
Adds TypeScript setup to markdown-only plugin.

### Plugin Naming
- Use kebab-case: `my-awesome-plugin`
- Lowercase letters, numbers, hyphens
- Must start with a letter

### Standard Structures

**Markdown Only:**
```
plugins/{name}/
├── .claude-plugin/plugin.json
├── package.json       ←(stub scripts)
├── commands/
└── skills/{name}/
```

**TypeScript:**
```
plugins/{name}/
├── .claude-plugin/plugin.json
├── package.json       ←(full scripts)
├── tsconfig.json
├── src/
│   ├── index.ts
│   └── index.test.ts
├── commands/
├── mcp/{name}/
├── hooks/
└── skills/{name}/
```

## Generation Workflow

1. **Validate** plugin name (kebab-case, no conflicts)
2. **Ask** which components to include
3. **Create** directory structure
4. **Generate** files from templates
5. **Register** in marketplace.json
6. **Install** dependencies with bun
7. **Verify** with tests

## Template Patterns

### package.json
- Namespace: `@sidequest/{name}`
- Scripts: test, typecheck, format, lint, check
- Uses Biome for formatting/linting

### MCP Server
- Uses `mcpez` library
- Export types for testing
- Zod schemas for input validation

### Commands
- YAML frontmatter with description
- argument-hint for usage hints
- allowed-tools for security

### Skills
- YAML frontmatter with name, description
- When to use section
- Quick reference table

## Post-Generation Steps

After generating a plugin:

1. **Navigate**: `cd plugins/{name}`
2. **Install**: `bun install`
3. **Test**: `bun test`
4. **Develop**: Add your logic to the generated files

## Examples

### Example 1: Create Simple Command Plugin
```
User: I want to create a plugin for managing todo lists
Assistant: I'll create a todo-manager plugin for you.
[Uses /plugin-template:create todo-manager]
[Selects commands component]
[Generates scaffold]
```

### Example 2: Create Full Plugin with MCP
```
User: Create a plugin that provides git statistics
Assistant: I'll scaffold a git-stats plugin with an MCP server.
[Uses /plugin-template:create git-stats]
[Selects commands, mcp-server, skills]
[Generates full structure]
```

### Example 3: Add Components to Existing Plugin
```
User: My plugin needs an MCP server now
Assistant: I'll add an MCP server to your existing plugin.
[Creates mcp/{name}/ directory]
[Generates index.ts and package.json]
[Updates .mcp.json]
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Name conflict | Choose different name or remove existing |
| Invalid name | Use kebab-case (lowercase, hyphens) |
| Bun install fails | Check network, run manually |
| Tests fail | Check generated code, fix issues |

## Related Commands

- `/plugin-template:create [name]` - Create new plugin
- `/plugin-template:strip [name]` - Remove TypeScript, convert to markdown-only
- `/plugin-template:upgrade [name]` - Add TypeScript to markdown-only plugin
- `/git:commit` - Commit your plugin changes
- `/para-brain:capture` - Document plugin ideas
