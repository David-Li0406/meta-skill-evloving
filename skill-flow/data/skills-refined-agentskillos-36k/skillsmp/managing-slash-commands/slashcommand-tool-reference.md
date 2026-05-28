# SlashCommand Tool, Plugin Commands, and MCP Commands Reference

Advanced reference for programmatic command invocation and ecosystem integration features.

## SlashCommand Tool

The SlashCommand tool allows Claude Code to execute custom slash commands programmatically during conversations. This gives Claude the ability to invoke slash commands on your behalf when appropriate.

### Supported Commands

SlashCommand tool only supports:
- **User-defined custom slash commands** (built-in commands like `/compact` and `/init` are not supported)
- **Commands with description frontmatter field** (description is required and used in context)

Commands can be enabled/disabled for programmatic invocation using the `disable-model-invocation` frontmatter field.

### Enabling SlashCommand Execution

To encourage Claude to trigger the SlashCommand tool:

Add command references to your prompts, CLAUDE.md, or skill instructions:

```markdown
Run /write-unit-test when you are about to start writing tests.
Use /analyze-coverage to generate coverage reports.
```

Claude will see SlashCommand tool metadata in context (up to character budget limit) and may invoke commands when appropriate.

### Disabling SlashCommand Invocation

**Disable all commands** via permissions:
```
/permissions
# Add to deny rules: SlashCommand
```

This removes all slash command metadata from context.

**Disable specific commands** via frontmatter:
```yaml
---
description: My command
disable-model-invocation: true
---
```

This removes the command from SlashCommand tool context while keeping it available for manual invocation.

### Permission Rules

SlashCommand tool supports two permission patterns:

**Exact match**: Allow only specific command with no arguments
```
SlashCommand:/commit
```

**Prefix match**: Allow command with any arguments
```
SlashCommand:/review-pr:*
```

### Character Budget Limit

The SlashCommand tool includes a character budget to limit size of command descriptions shown to Claude, preventing token overflow with many commands.

- **Default limit**: 15,000 characters
- **Custom limit**: Set via `SLASH_COMMAND_TOOL_CHAR_BUDGET` environment variable

When budget exceeded, Claude sees only subset of available commands. In `/context`, a warning shows "M of N commands".

**Optimization**: Keep command descriptions concise to fit more commands within budget.

---

## Plugin Commands

Plugins can provide custom slash commands that distribute through plugin marketplaces.

### Plugin Command Structure

**Location**: `commands/` directory in plugin root

**File Format**: Markdown files with frontmatter (identical to personal/project commands)

**Features**: Support all command features (arguments, frontmatter, bash execution, file references)

### Plugin Command Namespacing

Commands use format:
- **Direct** (when no conflicts): `/command-name`
- **Plugin-prefixed** (when disambiguation needed): `/plugin-name:command-name`

Plugin prefix shown in help: `(plugin:plugin-name)`

### Examples

**Single command from plugin**:
```
/my-command
```

**Multiple commands with namespacing**:
```
/analyze (plugin:analytics)
/generate (plugin:templates)
/check (plugin:validators)
```

### Plugin Command Invocation

Commands appear in `/help` once plugin installed and enabled.

Full command feature set available:
- **Arguments**: Use `$1`, `$2`, `$ARGUMENTS` placeholders
- **Subdirectories**: Organize with namespacing (shown in help)
- **Bash integration**: Execute shell scripts via `!` prefix
- **File references**: Include file contents with `@` prefix
- **Frontmatter**: Use all standard fields (description, allowed-tools, argument-hint, model, disable-model-invocation)

### Cross-Plugin Conflicts

When commands have same name in multiple plugins:
- Both available with plugin-prefixed names
- Manual invocation requires prefix: `/plugin-name:command-name`
- SlashCommand tool may have disambiguation rules

**Recommendation**: Use descriptive prefixed names or avoid naming conflicts through design.

---

## MCP Commands

MCP (Model Context Protocol) servers expose prompts as slash commands that become available in Claude Code through dynamic discovery.

### MCP Command Format

MCP commands follow pattern:
```
/mcp__<server-name>__<prompt-name> [arguments]
```

### Examples

**Without arguments**:
```
/mcp__github__list_prs
```

**With arguments**:
```
/mcp__github__pr_review 456
/mcp__jira__create_issue "Bug title" high
```

### Dynamic Discovery

MCP commands are automatically available when:
- MCP server is connected and active
- Server exposes prompts through MCP protocol
- Prompts successfully retrieved during connection

**Setup**: Use `/mcp` command to:
- View all configured MCP servers
- Check connection status
- Authenticate with OAuth-enabled servers
- Clear authentication tokens
- View available tools and prompts from each server

### Naming Normalization

MCP server and prompt names are normalized:
- Spaces and special characters become underscores
- Names lowercased for consistency
- Resulting command: `/mcp__<normalized-server>__<normalized-prompt>`

### MCP Permissions

When configuring permissions for MCP commands, note wildcards are **not supported**:

**Correct**:
- `mcp__github` (approves ALL tools from github server)
- `mcp__github__get_issue` (approves specific tool)

**Incorrect**:
- `mcp__github__*` (wildcards not supported)

To approve all MCP commands from a server, use server name only. For specific commands, list each individually.

### When to Use MCP Commands

Use MCP commands when:
- Integrating with external services (GitHub, Jira, etc.)
- Leveraging domain-specific prompt libraries from MCP servers
- Dynamic command discovery is beneficial
- Server handles complex logic (authentication, API calls)

Advantages over custom commands:
- No file creation needed
- Automatic updates from MCP server
- Centralized authentication
- Extensible through MCP ecosystem

### MCP Command Best Practices

1. **Prefix Understanding**: Always include `/mcp__` prefix in documentation or instructions
2. **Server Configuration**: Ensure MCP server is properly configured and connected before relying on commands
3. **Permission Management**: Configure appropriate permission rules for your use case
4. **Argument Validation**: Document which arguments each MCP command accepts (varies by server)
5. **Error Handling**: MCP commands may fail if server unavailable—have fallback plans

---

## Comparing Command Types

| Aspect | Personal/Project | Plugin | MCP |
|--------|------------------|--------|-----|
| **Location** | `.claude/commands/` or `~/.claude/commands/` | Plugin `commands/` directory | Connected MCP server |
| **File Based** | Yes (markdown) | Yes (markdown) | No (dynamic) |
| **Distribution** | Git repository | Plugin marketplace | MCP server configuration |
| **Invocation** | `/command-name` | `/command-name` or `/plugin:command-name` | `/mcp__server__prompt` |
| **Authentication** | N/A | N/A | MCP server OAuth (optional) |
| **Maintenance** | Manual updates | Plugin maintainer | MCP server owner |
| **Arguments** | `$ARGUMENTS`, `$1-$9` | `$ARGUMENTS`, `$1-$9` | Server-defined |
| **Bash Execution** | Yes (`!` prefix) | Yes (`!` prefix) | Server-dependent |
| **SlashCommand Tool** | Yes | Yes | Yes |

---

## Choosing Command Architecture

### Use Personal/Project Commands When

- Creating team-specific prompts
- Quick experimentation or prototyping
- Commands tightly integrated with your codebase
- Full control over updates desired
- No external service dependency needed

### Use Plugin Commands When

- Distributing reusable command sets
- Sharing with broader community
- Bundling with other skills/tools
- Maintaining standardized library

See **managing-plugins** skill for detailed plugin command creation.

### Use MCP Commands When

- Integrating with external services
- Leveraging domain-specific tools
- Dynamic prompt discovery beneficial
- Server handles authentication/logic
- Infrastructure managed by external team

See **managing-mcps** skill for MCP server setup and prompt exposure.

---

## Advanced Patterns

### Combining Command Types

You can use multiple command types together:

**Pattern: Local + MCP**
- Local commands for team workflows
- MCP commands for external service integration
- Same prompt may reference both

**Pattern: Plugin + Programmatic**
- Plugin provides commands
- SlashCommand tool invokes them programmatically
- Enables workflow automation

**Pattern: MCP + Local Wrapper**
- MCP server provides raw prompt
- Local command wraps with additional context
- Adapts MCP capabilities to team needs

---

## Reference Summary

| Feature | Section |
|---------|---------|
| Programmatic invocation | SlashCommand Tool |
| Managing command execution | SlashCommand Tool → Disabling/Permissions |
| Distributing commands | Plugin Commands |
| Plugin command naming conflicts | Plugin Commands → Cross-Plugin Conflicts |
| External service integration | MCP Commands |
| Permission configuration | MCP Commands → MCP Permissions |
| Architecture decision | Choosing Command Architecture |
