---
name: mcp-architect
description: "Project-scoped .mcp.json router for external tools and service integrations. Use for creating, auditing, or refining MCP servers in current project root. Routes to mcp-knowledge for configuration details. Do not use for standalone plugin MCP configuration."
disable-model-invocation: true
---

# MCP Architect

Domain router for project-scoped Model Context Protocol (MCP) integrations via `.mcp.json`.

## MANDATORY: Read Before Creating MCP Integrations

- **MUST READ**: [Official MCP Guide](https://code.claude.com/docs/en/mcp)
  - **Tool**: `mcp__simplewebfetch__simpleWebFetch`
  - **Cache**: 15 minutes minimum
  - **Content**: MCP integration patterns, tools, resources, prompts, transport mechanisms

- **MUST READ**: [MCP Specification](https://modelcontextprotocol.io/)
  - **Tool**: `mcp__simplewebfetch__simpleWebFetch`
  - **Cache**: 15 minutes minimum
  - **Content**: Protocol definition, JSON-RPC 2.0 message format, security principles

**BLOCKING RULES**:
- **DO NOT proceed** without understanding MCP protocol and primitives
- **REQUIRED** to validate URLs are accessible before MCP integration
- **MUST understand** Tools, Resources, Prompts primitives before server creation

## Actions

### create
**Creates/edits MCP configuration** in `.mcp.json`

**Target File**: `${CLAUDE_PROJECT_DIR}/.mcp.json`

**Router Logic**:
1. Load: mcp-knowledge for implementation details
2. Determine MCP component:
   - Tools - API wrappers
   - Resources - Data access
   - Prompts - Templates
   - Servers - Full integration
3. **Safely merge** new server into existing .mcp.json:
   - Read existing .mcp.json
   - Parse as JSON
   - Add/merge new server configuration
   - Validate JSON syntax
   - Write back to .mcp.json
4. Validate: Protocol compliance

**Output Contract**:
```
## MCP Server Added: {server_name}

### Location
- File: .mcp.json
- Transport: {transport}
- Existing Servers Preserved: ✅

### Server Configuration
- Tools: {count}
- Resources: {count}
- Prompts: {count}
```

### audit
**Audits MCP integrations** for protocol compliance

**Router Logic**:
1. **Load: mcp-knowledge/references/integration.md**
2. Check:
   - Protocol adherence
   - Transport configuration (stdio, http)
   - Tool/resource/prompt validity
   - Security considerations
3. Generate audit with compliance scoring

**Output Contract**:
```
## MCP Audit: {component_name}

### Protocol Compliance
- Specification: {version}
- Adherence: {score}/10

### Components
- Tools: {tool_count} ({valid_count} valid)
- Resources: {resource_count} ({valid_count} valid)
- Prompts: {prompt_count} ({valid_count} valid)

### Transport
- Type: {transport}
- Configuration: ✅/❌

### Issues
- {issue_1}
- {issue_2}
```

### refine
**Improves MCP integrations** based on audit findings

**Router Logic**:
1. **Load: mcp-knowledge** for implementation patterns
2. Enhance:
   - Protocol compliance
   - Transport optimization
   - Component validation
   - Security hardening
3. Validate improvements

**Output Contract**:
```
## MCP Refined: {component_name}

### Protocol Improvements
- {improvement_1}
- {improvement_2}

### Component Enhancements
- {enhancement_1}
- {enhancement_2}

### Compliance Score: {old_score} → {new_score}/10
```

## MCP Components

**Tools**:
- External API wrappers
- Service integrations
- Data transformation

**Resources**:
- Data access patterns
- File system access
- Network resources

**Prompts**:
- Template management
- Dynamic generation
- Context injection

**Servers**:
- Full MCP server implementation
- Multi-component integration
- Transport management

## Routing Criteria

**For Tool Creation**: Load mcp-knowledge/references/tools.md
- API wrapper patterns
- Tool schemas and validation
- Service integration examples

**For Resource/Prompt Creation**: Load mcp-knowledge/references/resources.md
- Data access patterns
- File system resources
- Template management
- Context injection

**For Server Configuration**: Load mcp-knowledge/references/servers.md
- Transport setup (stdio, http)
- Official servers (Context7, DeepWiki, DuckDuckGo)
- Custom server deployment
- Plugin MCP (.mcp.json or plugin.json)

**For Integration Guidance**: Load mcp-knowledge/references/integration.md
- Architecture patterns
- Decision framework
- Security considerations
- Configuration management

## 2026 MCP Features

- **Tool Search**: Auto-enabled when tools exceed 10% of context
- **MCP Resources**: Referenced via `@server:protocol://resource/path` syntax
- **MCP Prompts**: Available as `/mcp__servername__promptname` commands
- **Plugin MCP**: Plugins bundle MCP servers via `.mcp.json` or `plugin.json`
- **Dynamic Tool Updates**: Supports `list_changed` notifications
- **MCP Output Limits**: Default 25,000 tokens, configurable via `MAX_MCP_OUTPUT_TOKENS`
- **Environment Variables**: `${CLAUDE_PLUGIN_ROOT}` for plugin paths

## Transport Mechanisms

### stdio (Local)
- Local process execution via standard input/output
- Use for: Development, testing, single-user scenarios
- Configuration: `claude mcp add --transport stdio <name> -- <command> [args...]`

### http (Remote)
- Hosted services with bidirectional streaming (recommended for cloud)
- Use for: Production deployments, multi-user, high availability
- Configuration: `claude mcp add --transport http <name> <url>`

### sse (Deprecated)
- Server-Sent Events transport is deprecated
- Use http instead for new implementations

## MCP Primitives Quick Reference

See mcp-knowledge for complete primitives table and decision framework.

| Primitive | Purpose | Use When |
| --------- | ------- | -------- |
| **Tools** | Callable functions | Need to expose operations or actions |
| **Resources** | Read-only data | Need to provide data access |
| **Prompts** | Reusable workflows | Need predefined prompt templates |
