---
name: mcp-skill-generator
description: Convert MCP servers to Claude Code skills with progressive disclosure. Use when creating a skill from an MCP server, updating an existing MCP skill, or converting MCP documentation to skill format. Accepts MCP documentation URLs, npm package names, or direct connection info.
allowed-tools: Bash, Read, Write, Edit, Glob, WebFetch
---

# MCP Skill Generator

Convert MCP servers into Claude Code skills with progressive disclosure pattern.

## Before You Start

Read https://code.claude.com/docs/en/skills for the latest skill best practices.

## Workflow

### 1. Get MCP Server Info

Ask user for: documentation URL, package name, or direct connection info (stdio command or HTTP URL).

### 2. Version Locking (When Possible)

Version locking prevents supply chain attacks, but **only applies when the MCP server supports it**:

| Server Type | Can Lock? |
|-------------|-----------|
| Package (npm, pip, cargo, etc.) | ✅ Yes - use package manager's version syntax |
| Remote HTTP service | ⚠️ Maybe - only if API supports versioning |
| Local binary/service | ❌ No |

**If lockable**, record the version in config.toml (`version` and `versionLockedAt` fields).

**If package but not lockable**, STOP and warn user loudly:

> ⚠️ **SECURITY WARNING**
>
> Cannot lock version for this package. The package maintainer could push malicious updates at any time.
>
> **Do you trust the publisher of `<package-name>`?**
>
> Only proceed if you fully trust them. Type "yes I trust" to continue.

**If remote service**, no extra warning needed - user implicitly trusts it by choosing to convert.

### 3. Extract Schema

Run from this skill's directory (use subshell to preserve pwd):

```bash
(cd /path/to/mcp-skill-generator && node ./scripts/schema-extractor.mjs --stdio "npx <package>@<version> <args>")
# or
(cd /path/to/mcp-skill-generator && node ./scripts/schema-extractor.mjs --http "<url>")
```

### 4. Generate Skill

Create directory structure:

```
~/.claude/skills/mcp-[server-name]/
├── SKILL.md              # Overview (use templates/SKILL.md.template)
├── tools/                # One file per tool (use templates/tool.md.template)
├── config.toml           # Connection config (see docs/config-format.md)
├── resources.md          # Resource docs (if server has resources)
├── prompts.md            # Prompt docs (if server has prompts)
└── scripts/
    ├── mcp-transport.mjs # Transport layer
    ├── mcp-caller.mjs    # CLI interface
    └── api.mjs           # Programmatic API for batch/parallel calls
```

### 5. Ask Save Location

- Project: `.claude/skills/mcp-[name]/`
- Personal: `~/.claude/skills/mcp-[name]/`

### 6. Copy Scripts

```bash
mkdir -p <target>/scripts
cp -f /path/to/mcp-skill-generator/scripts/mcp-transport.mjs <target>/scripts/
cp -f /path/to/mcp-skill-generator/scripts/mcp-caller.mjs <target>/scripts/
cp -f /path/to/mcp-skill-generator/scripts/api.mjs <target>/scripts/
```

**Only copy these 3 runtime files.** Do NOT copy files not needed at runtime (e.g., `schema-extractor.mjs`).

### 7. Show Summary

Display: tools/resources/prompts count, save location, locked version, usage instructions.

## Updating Existing Skills

1. Read existing config.toml
2. Check for newer version: `npm view <package> version`
3. Extract fresh schema
4. Compare changes: "3 new tools, 1 removed, 2 modified"
5. Regenerate files (preserve user customizations)
6. Always overwrite scripts/

## Reference

- [Design document](./docs/DESIGN.md) - Architecture, design decisions, and trade-offs
- [config.toml format](./docs/config-format.md) - Configuration examples and environment variables
- [templates/](./templates/) - SKILL.md and tool.md templates
