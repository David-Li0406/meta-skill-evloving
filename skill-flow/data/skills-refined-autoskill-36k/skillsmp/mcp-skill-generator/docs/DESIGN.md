# MCP Skill Generator - Design Document

## Project Goal

Convert MCP (Model Context Protocol) servers into Claude Code skills using **progressive disclosure** pattern to reduce context consumption.

### Why This Exists

MCP servers configured directly in Claude Code consume significant context - all tool definitions are loaded into the system prompt immediately. This skill converts MCP servers to Skills, which use lazy loading:
- Minimal context at startup (just tool names and descriptions)
- Detailed docs loaded on demand (from `tools/` directory)

## Design Principles

### 1. Zero Runtime Dependencies

All scripts use pure Node.js built-in modules only. No npm dependencies at runtime.
- `mcp-transport.mjs` - stdio/HTTP transport layer
- `mcp-caller.mjs` - CLI interface
- `api.mjs` - programmatic API

### 2. Security: Version Locking When Possible

Version locking prevents supply chain attacks, but not all MCP servers support it:

| Server Type | Can Lock? | Action |
|-------------|-----------|--------|
| Package (npm, pip, etc.) | Usually yes | Lock version in command args |
| Remote HTTP service | Maybe | Only if API supports versioning |
| Local binary/service | No | N/A |

**Key design decision**: If a package cannot be version-locked, the generator STOPS and requires explicit user confirmation ("yes I trust") before proceeding. This happens during generation, not after - we don't want to create a skill the user hasn't consciously accepted the risk for. Remote services don't need this warning - user implicitly trusts them by choosing to convert.

### 3. Environment Variable Isolation

Use unified prefix `MCP_<SKILL_NAME>_<VAR_NAME>` to avoid conflicts:
- Between different MCP skills
- With user's existing environment variables
- With other Claude Code skills

Example: `MCP_CONTEXT7_API_KEY`, `MCP_GITHUB_TOKEN`

### 4. Optional Authentication

Environment variables in `[headers]` and `[env]` sections are optional:
- If not set, the entire entry is skipped (not sent as empty value)
- Allows skills to work without credentials (lower rate limits) or with credentials (higher limits)

**Key design decision**: When `Bearer ${VAR}` has an unset VAR, we remove the entire header rather than sending `Bearer ` (which would cause auth errors).

### 5. AI-Friendly API

The `api.mjs` module provides a simple interface for AI agents:

```javascript
import { callTool, listTools } from './scripts/api.mjs';

// Parallel calls - AI can batch operations
const results = await Promise.all([
  callTool('tool1', { arg: 'value1' }),
  callTool('tool2', { arg: 'value2' }),
]);
```

**Design decisions**:
- Lazy initialization: Connection established on first call
- Shared client: Subsequent calls reuse the same connection
- Simple exports: No need to handle config parsing, transport setup, or MCP handshake

### 6. Script Management

Generated skills include 3 runtime scripts that are auto-managed:
- Scripts have `⚠️ AUTO-GENERATED FILE - DO NOT EDIT` headers
- Updates always overwrite these files (bug fixes propagate automatically)
- Only runtime files are copied (not `schema-extractor.mjs`)

### 7. Progressive Disclosure in Documentation

Following Claude Code skill best practices:
- `SKILL.md` stays concise (~100 lines max)
- Detailed references in `docs/` and `templates/`
- Each tool has its own `tools/<name>.md` file

### 8. Preserve Working Directory

CLI examples use subshell to avoid changing pwd:
```bash
(cd /path/to/skill && node ./scripts/mcp-caller.mjs call ...)  # Good
cd /path/to/skill && node ./scripts/mcp-caller.mjs call ...    # Bad - changes pwd
```

## Architecture

```
mcp-skill-generator/
├── SKILL.md                    # Concise workflow (load first)
├── docs/
│   ├── DESIGN.md               # This file - design rationale
│   └── config-format.md        # Detailed config reference (load on demand)
├── templates/
│   ├── SKILL.md.template       # Template for generated skills
│   └── tool.md.template        # Template for tool docs
└── scripts/
    ├── schema-extractor.mjs    # Generation-time only (NOT copied)
    ├── mcp-transport.mjs       # Runtime - transport layer (copied)
    ├── mcp-caller.mjs          # Runtime - CLI interface (copied)
    └── api.mjs                 # Runtime - AI-friendly API (copied)
```

## Key Bug Fixes (2026-01-20)

### 1. Optional Auth - Empty Value Bug
**Problem**: `${VAR}` replaced with empty string when unset, causing `Bearer ` to be sent.
**Fix**: Return `REMOVE_VALUE` symbol to skip entire header.

### 2. Optional Auth - Nested Key Bug
**Problem**: `substituteEnvVarsInObject` lost "optional" context when recursing into `headers.Authorization`.
**Fix**: Pass `isOptional` boolean that propagates through the subtree.

### 3. Import Execution Bug
**Problem**: `mcp-caller.mjs` called `main()` unconditionally, causing execution when imported by `api.mjs`.
**Fix**: Added execution guard: `if (import.meta.url === \`file://${process.argv[1]}\`) { main(); }`

## Trade-offs

### TOML vs JSON for config
**Choice**: TOML
**Rationale**: More readable, saves tokens in context, comments supported.

### Single connection vs connection-per-call
**Choice**: Single shared connection (lazy init)
**Rationale**: Performance - MCP handshake takes ~100-200ms per connection.

### Strict vs optional environment variables
**Choice**: Optional for `[headers]` and `[env]`, required elsewhere
**Rationale**: Balance between security (don't fail silently on missing critical vars) and flexibility (allow anonymous access with lower rate limits).

## Future Considerations

1. **Real SSE streaming**: Currently we parse SSE responses but don't maintain persistent connections for server-pushed notifications.

2. **Credential management**: Currently relies on shell environment variables. Could integrate with system keychain.

3. **Schema validation**: Could validate tool arguments against inputSchema before calling.
