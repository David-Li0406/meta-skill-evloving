---
name: meta-unify-core
description: Core configuration engine for meta-unify plugin. Parses user configuration requests, translates between Claude and Codex formats, and generates appropriate configuration files for both systems. Invoked by meta-unify commands to handle MCP servers, skills, hooks, rules, and instructions.
user-invocable: false
---

# Meta-Unify Core Skill

This skill provides the parsing, translation, and generation logic that powers the meta-unify plugin. It is not invoked directly by users but is called by meta-unify commands to perform configuration operations.

## Core Capabilities

### What This Skill Does

1. **Parses Configuration Requests**: Interprets natural language or structured requests for adding/modifying MCP servers, skills, hooks, rules, or instructions
2. **Translates Between Formats**: Converts configuration syntax between Claude Code and Codex formats
3. **Generates Configuration Files**: Creates or modifies the appropriate files for both systems
4. **Validates Output**: Ensures generated configurations are syntactically correct before writing

### Configuration Types Handled

| Type | Description |
|------|-------------|
| MCP Servers | Model Context Protocol server definitions (STDIO and HTTP transports) |
| Skills | Reusable capability bundles with assets, scripts, and references |
| Hooks | Event-triggered actions (Claude only) |
| Rules | Permission and constraint definitions |
| Instructions | System-wide or project-scoped behavioral guidelines |
| Plugins | Complete Claude Code plugin scaffolding and generation |

---

## File Location Mappings

### Quick Reference Table

| Config Type | Claude User Scope | Claude Project Scope | Codex User Scope | Codex Project Scope |
|-------------|-------------------|---------------------|------------------|---------------------|
| MCP servers | `~/.claude.json` | `.mcp.json` | `~/.codex/config.toml` | N/A |
| Skills | `~/.claude/skills/` | `.claude/skills/` | `~/.codex/skills/` | `.codex/skills/` |
| Hooks | `~/.claude/settings.json` | `.claude/settings.json` | N/A | N/A |
| Rules | `~/.claude/settings.json` (permissions) | `.claude/settings.json` | `~/.codex/rules/*.rules` | N/A |
| Instructions | `~/.claude/CLAUDE.md` | `.claude/CLAUDE.md` | `~/.codex/AGENTS.md` | `AGENTS.md` |

### Notes on Scope Differences

- **Codex MCP**: Only supports user-scope configuration in `config.toml`
- **Codex Hooks**: Not supported; use rules for command-level control
- **Codex Rules**: Starlark-based files in `~/.codex/rules/` directory

---

## Format Translation Rules

### MCP Servers

**Claude (JSON) → Codex (TOML)**

```json
// Claude (.mcp.json or ~/.claude.json)
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["@package/server"],
      "env": { "KEY": "value" }
    }
  }
}
```

```toml
# Codex (~/.codex/config.toml)
[mcp_servers.server-name]
command = "npx"
args = ["@package/server"]

[mcp_servers.server-name.env]
KEY = "value"
```

**HTTP Transport**

```json
// Claude
{
  "mcpServers": {
    "remote-server": {
      "url": "https://api.example.com/mcp"
    }
  }
}
```

```toml
# Codex
[mcp_servers.remote-server]
url = "https://api.example.com/mcp"
```

### Skills

Both systems use SKILL.md with YAML frontmatter. Key differences:

| Property | Claude | Codex |
|----------|--------|-------|
| Name | `name` (max 64 chars) | `name` (max 100 chars) |
| Description | `description` (max 1024 chars) | `description` (max 500 chars) |
| User-callable | `user-invocable: true/false` | Always invocable via `$skill-name` |
| Extra fields | `allowed-tools`, `model`, `context` | `metadata.short-description` |

**Translation**: Claude-specific fields are omitted from Codex version silently.

### Permissions / Rules

**Claude (settings.json permissions)**

```json
{
  "permissions": {
    "allow": ["Bash(npm run:*)"],
    "ask": ["Bash(git push:*)"],
    "deny": ["Bash(rm -rf:*)"]
  }
}
```

**Codex (Starlark .rules file)**

```python
prefix_rule(
    pattern = ["npm", "run"],
    decision = "allow",
)

prefix_rule(
    pattern = ["git", "push"],
    decision = "prompt",
)

prefix_rule(
    pattern = ["rm", "-rf"],
    decision = "forbidden",
)
```

### Instructions

**Claude (CLAUDE.md)** and **Codex (AGENTS.md)** use the same markdown format.

**Special sections:**
- `## Claude Only` → Only in CLAUDE.md
- `## Codex Only` → Only in AGENTS.md

---

## Parsing Heuristics

### Transport Type Detection

| Pattern | Inferred Transport |
|---------|-------------------|
| `npx @package/...` | STDIO |
| `node script.js` | STDIO |
| `python -m module` | STDIO |
| Any executable command | STDIO |
| `https://` or `http://` URL | HTTP |

### Skill Structure Suggestions

| Keyword in Request | Suggested Structure |
|-------------------|---------------------|
| "guidelines", "docs", "reference", "API" | `references/` directory |
| "deploy", "build", "run", "validate" | `scripts/` directory |
| "template", "scaffold", "generate" | `assets/` directory |

### Environment Variable Patterns

| Pattern | Action |
|---------|--------|
| `API_KEY`, `TOKEN`, `SECRET` | Warn about sensitive data |
| `${VAR}` or `$VAR` | Preserve as env var reference |

---

## Validation Requirements

### Before Writing Configuration

1. **JSON Validation** (Claude configs)
   - Valid JSON syntax
   - Required keys present
   - Correct structure

2. **TOML Validation** (Codex configs)
   - Valid TOML syntax
   - Required sections present

3. **Starlark Validation** (Codex rules)
   - Valid Python-like syntax
   - prefix_rule() calls are correct

4. **Command Existence Check** (STDIO MCP)
   - Verify command exists in PATH
   - Warn if not found

---

## Error Handling

### Partial Failure Protocol

When one system succeeds but the other fails:

1. Do NOT roll back the successful write
2. Report clearly which system succeeded and which failed
3. Show the error from the failed system
4. Ask user how to proceed:
   - Keep successful changes
   - Retry failed system
   - Abort and restore

### Error Message Format

```
[meta-unify] ERROR: Failed to write Codex config
  File: ~/.codex/config.toml
  Reason: Invalid TOML syntax - unclosed string at line 15
  Action: Please check the configuration and retry
```

---

## Reference Documentation

For detailed format specifications, see:

- `references/claude-formats.md` - Complete Claude Code configuration schemas
- `references/codex-formats.md` - Complete Codex configuration schemas
- `references/plugin-formats.md` - Claude Code plugin structure and manifest formats

---

## Integration Notes

### Called By

- `/meta-unify:add-mcp` - Adding MCP servers
- `/meta-unify:add-skill` - Creating new skills
- `/meta-unify:add-hook` - Adding hooks (Claude only)
- `/meta-unify:add-rule` - Adding permission rules
- `/meta-unify:add-plugin` - Creating new Claude Code plugins
- `/meta-unify:sync` - Synchronizing configs between systems

### Limitations

- Codex hooks are not supported; suggests rule-based alternatives
- Cannot migrate complex Starlark rules to Claude permissions automatically
- Does not validate MCP server functionality, only syntax
