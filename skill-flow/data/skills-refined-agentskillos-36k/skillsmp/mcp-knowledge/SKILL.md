---
name: mcp-knowledge
description: "Complete guide to Model Context Protocol (MCP) for project-scoped integration via .mcp.json. Use when configuring project-level MCP servers, creating custom tools, or managing resources/prompts. Do not use for standalone plugin MCP configuration."
user-invocable: true
---

# MCP Knowledge Base

Complete Model Context Protocol (MCP) knowledge base for project-scoped Claude Code integration. Access comprehensive guides for MCP integration, server configuration in `.mcp.json`, tool development, and resources/prompts creation.

## 🚨 MANDATORY: Read BEFORE MCP Integration

**CRITICAL**: You MUST read and understand these URLs:

### Primary Documentation (MUST READ)
- **[MUST READ] Official MCP Guide**: https://code.claude.com/docs/en/mcp
  - **Tool**: `mcp__simplewebfetch__simpleWebFetch`
  - **When to Read**: Before any MCP integration
  - **Content**: MCP integration patterns, tools, resources, prompts
  - **Cache**: 15 minutes minimum

- **[MUST READ] MCP Specification**: https://modelcontextprotocol.io/
  - **Tool**: `mcp__simplewebfetch__simpleWebFetch`
  - **When to Read**: Before implementing MCP servers
  - **Content**: Protocol definition, transport mechanisms, primitives
  - **Cache**: 15 minutes minimum

### ⚠️ BLOCKING RULES
- **DO NOT proceed** until you've fetched and reviewed Primary Documentation
- **MUST validate** all URLs are accessible before MCP integration
- **REQUIRED** to understand MCP primitives before server creation

## Progressive Disclosure Knowledge Base

This skill provides complete MCP knowledge through progressive disclosure:

### Tier 1: Quick Overview
This SKILL.md provides the decision framework and quick reference.

### Tier 2: Comprehensive Guides
Load full guides on demand:
- **[integration.md](references/integration.md)** - Decision guide for MCP usage
- **[servers.md](references/servers.md)** - Server configuration and deployment
- **[tools.md](references/tools.md)** - Tool development and schemas
- **[resources.md](references/resources.md)** - Resources and prompts implementation

### Tier 3: Deep Reference
Individual reference files provide complete implementation details.

## Quick Start

### New to MCP?
Start with **[integration.md](references/integration.md)** to determine if MCP is right for your use case.

### Need to Configure Servers?
See **[servers.md](references/servers.md)** for official servers (Context7, DeepWiki, DuckDuckGo) and custom server setup.

### Building Custom Tools?
Check **[tools.md](references/tools.md)** for tool schemas, validation, and implementation patterns.

### Creating Resources/Prompts?
Review **[resources.md](references/resources.md)** for resource and prompt development.

## MCP Primitives Quick Reference

| Primitive | Purpose | Use When |
| --------- | ------- | -------- |
| **Tools** | Callable functions | Need to expose operations or actions |
| **Resources** | Read-only data | Need to provide data access |
| **Prompts** | Reusable workflows | Need predefined prompt templates |

## Transport Mechanisms

### stdio
Local process execution via standard input/output
- Use for: Local MCP server implementation
- Best for: Development, testing, single-user scenarios

### Streamable HTTP
Hosted services with bidirectional streaming
- Use for: Cloud-based servers, production deployments
- Best for: Multi-user, shared instances, high availability

## Key Takeaways

1. **Use MCP** for shareable, protocol-standardized integrations
2. **Use skills** for project-specific, direct integrations
3. **Use native tools** for basic file operations
4. **Choose transport** based on deployment needs
5. **Start with official servers** before building custom

## Project-Scoped MCP Configuration

**Target File**: `${CLAUDE_PROJECT_DIR}/.mcp.json`

**Use Project MCP When**:
- Adding web search to current project
- Integrating external APIs for project use
- Configuring project-specific tools
- Local development MCP servers

**Configuration Example**:
```json
{
  "mcpServers": {
    "my-server": {
      "transport": {
        "type": "stdio",
        "command": "node",
        "args": ["path/to/server.js"]
      }
    }
  }
}
```

**Safety**: Always merge new servers into existing `.mcp.json` to preserve current configuration.

## Layer Selection Decision

```
Need external service integration?
├─ Yes → Use MCP
│  ├─ Decision guide → [integration.md](references/integration.md)
│  ├─ Configure servers → [servers.md](references/servers.md)
│  ├─ Build tools → [tools.md](references/tools.md)
│  └─ Create resources → [resources.md](references/resources.md)
└─ No → Use skills or native tools
```

## Next Steps

Choose your path:

1. **[Determine if MCP is needed](references/integration.md)** - Decision framework
2. **[Configure MCP servers](references/servers.md)** - Setup and deployment
3. **[Develop MCP tools](references/tools.md)** - Custom tool creation
4. **[Build resources/prompts](references/resources.md)** - Data access and workflows
