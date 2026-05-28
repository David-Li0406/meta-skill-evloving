---
name: plugin-creator
description: Use this skill when you need to automatically create new Claude Code plugins with the proper structure, validation, and marketplace integration.
---

# Plugin Creator

## Purpose
Automatically scaffolds new Claude Code plugins with a complete directory structure, required files, proper formatting, and marketplace catalog integration, specifically optimized for the claude-code-plugins repository.

## Trigger Keywords
- "create plugin"
- "new plugin"
- "plugin from template"
- "scaffold plugin"
- "generate plugin"
- "add new plugin to marketplace"

## Plugin Creation Process

When activated, I will:

1. **Gather Requirements**
   - Plugin name (kebab-case)
   - Category (productivity, security, devops, etc.)
   - Type (commands, agents, skills, MCP, or combination)
   - Description and keywords
   - Author information

2. **Create Directory Structure**
   ```
   plugins/[category]/[plugin-name]/
   ├── .claude-plugin/
   │   └── plugin.json
   ├── README.md
   ├── LICENSE
   └── [commands|agents|skills|hooks|mcp]/
   ```

3. **Generate Required Files**
   - **plugin.json** with proper schema (name, version, description, author)
   - **README.md** with comprehensive documentation
   - **LICENSE** (MIT by default)
   - Component files based on type

4. **Add to Marketplace Catalog**
   - Update `.claude-plugin/marketplace.extended.json`
   - Run `npm run sync-marketplace` automatically
   - Validate catalog schema

5. **Validate Everything**
   - Run `./scripts/validate-all.sh` on the new plugin
   - Check JSON syntax with `jq`
   - Verify frontmatter in markdown files
   - Ensure scripts are executable

## Plugin Types Supported

### Commands Plugin
- Creates `commands/` directory
- Generates example command with proper frontmatter
- Includes `/demo-command` example

### Agents Plugin
- Creates `agents/` directory
- Generates example agent with capabilities
- Includes model specification

### Skills Plugin
- Creates `skills/skill-name/` directory
- Generates SKILL.md with proper format
- Includes trigger keywords and allowed-tools

### MCP Plugin
- Creates `src/`, `dist/`, `mcp/` directories
- Generates TypeScript boilerplate
- Includes package.json with MCP SDK
- Adds to pnpm workspace

### Full Plugin
- Combines all types
- Creates complete example structure
- Ready for customization