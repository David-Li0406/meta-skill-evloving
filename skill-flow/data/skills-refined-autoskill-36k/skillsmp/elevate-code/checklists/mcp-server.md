# MCP Server Checklist

Complete validation checklist for Model Context Protocol (MCP) servers.

Based on official Anthropic MCP documentation.

---

## Project Structure

```
my-mcp-server/
├── package.json           # or pyproject.toml
├── src/
│   ├── index.ts           # Entry point
│   ├── server.ts          # MCP server setup
│   ├── tools/             # Tool implementations
│   │   ├── index.ts
│   │   └── <tool-name>.ts
│   ├── resources/         # Resource providers
│   │   └── index.ts
│   └── prompts/           # Prompt templates
│       └── index.ts
├── tests/
├── README.md
├── CLAUDE.md
└── mcp.json               # MCP configuration
```

---

## MCP Fundamentals

### Server Setup
- [ ] MCP SDK installed (`@modelcontextprotocol/sdk` or `mcp`)
- [ ] Server properly initialized
- [ ] Transport configured (stdio, HTTP, WebSocket)
- [ ] Error handling for connection issues
- [ ] Graceful shutdown handler

### Capabilities Declaration
- [ ] Tools declared with schemas
- [ ] Resources declared (if applicable)
- [ ] Prompts declared (if applicable)
- [ ] Version information provided

---

## The Triad (Adapted for MCP)

### Health (Doctor)
- [ ] Server validates dependencies on startup
- [ ] Clear error messages for missing configuration
- [ ] Required environment variables documented
- [ ] Connection test capability

### Safety (Safety Net)
- [ ] Destructive tools require confirmation parameter
- [ ] Dry-run option for file/data modifications
- [ ] Undo capability where appropriate
- [ ] Audit logging for tool invocations

### Resilience (Statekeeper)
- [ ] Long operations provide progress updates
- [ ] Interruption handling (cancelation tokens)
- [ ] State persistence for multi-step operations
- [ ] Retry logic for external service calls

---

## Tool Implementation

### Tool Definition
```typescript
{
  name: "my_tool",
  description: "Clear description of what the tool does",
  inputSchema: {
    type: "object",
    properties: {
      param1: {
        type: "string",
        description: "What this parameter does"
      },
      confirm: {
        type: "boolean",
        description: "Confirm destructive action",
        default: false
      }
    },
    required: ["param1"]
  }
}
```

### Tool Checklist
- [ ] Clear, descriptive name (snake_case)
- [ ] Comprehensive description
- [ ] JSON Schema for input validation
- [ ] All parameters documented
- [ ] Required vs optional clearly marked
- [ ] Default values where appropriate
- [ ] Error responses are structured

### Tool Implementation
- [ ] Input validation before processing
- [ ] Clear success/error responses
- [ ] Progress updates for long operations
- [ ] Handles edge cases gracefully
- [ ] No silent failures

---

## Resources

### Resource Definition
```typescript
{
  uri: "myserver://resource/{id}",
  name: "Resource Name",
  description: "What this resource provides",
  mimeType: "application/json"
}
```

### Resource Checklist
- [ ] URI scheme is consistent (`myserver://...`)
- [ ] Resources are discoverable via list
- [ ] Content type declared
- [ ] Pagination for large collections
- [ ] Error handling for missing resources

---

## Prompts

### Prompt Definition
```typescript
{
  name: "my_prompt",
  description: "When to use this prompt",
  arguments: [
    {
      name: "context",
      description: "Additional context",
      required: false
    }
  ]
}
```

### Prompt Checklist
- [ ] Clear use case in description
- [ ] Arguments well documented
- [ ] Prompt generates useful context
- [ ] Handles missing arguments gracefully

---

## Error Handling

### Error Response Format
```typescript
{
  isError: true,
  content: [
    {
      type: "text",
      text: "ERROR: What failed\nREASON: Why it failed\nFIX: How to fix it"
    }
  ]
}
```

### Error Checklist
- [ ] All errors include helpful messages
- [ ] Error format is consistent
- [ ] Actionable fix suggestions
- [ ] No stack traces in production
- [ ] Errors logged for debugging

---

## Configuration

### mcp.json
```json
{
  "name": "my-mcp-server",
  "version": "1.0.0",
  "description": "Server description",
  "tools": ["tool1", "tool2"],
  "resources": ["resource1"],
  "prompts": ["prompt1"]
}
```

### Environment Variables
- [ ] All required vars documented
- [ ] Sensible defaults where possible
- [ ] Validation on startup
- [ ] No secrets in code

---

## Security

- [ ] Input sanitization on all tools
- [ ] File operations restricted to safe paths
- [ ] No arbitrary code execution
- [ ] Secrets handled securely
- [ ] Rate limiting if appropriate
- [ ] Audit logging for sensitive operations

---

## Testing

- [ ] Unit tests for tool logic
- [ ] Integration tests with MCP client
- [ ] Error scenario coverage
- [ ] Mock external dependencies
- [ ] Schema validation tests

---

## Documentation

### README.md
- [ ] Installation instructions
- [ ] Configuration requirements
- [ ] Available tools with examples
- [ ] Available resources
- [ ] Available prompts
- [ ] Troubleshooting guide

### CLAUDE.md
- [ ] Architecture overview
- [ ] Key files and their purposes
- [ ] Adding new tools guide
- [ ] Testing instructions

---

## Deployment

### Claude Desktop Integration
```json
// claude_desktop_config.json
{
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["/path/to/server/dist/index.js"],
      "env": {
        "API_KEY": "your-key"
      }
    }
  }
}
```

### Checklist
- [ ] Server starts reliably
- [ ] Configuration documented
- [ ] Environment variables documented
- [ ] Error logs accessible
- [ ] Version management

---

## Quick Validation

```bash
# Check MCP structure
ls src/tools/ src/resources/ src/prompts/

# Check tool definitions
grep -rE "name:|description:|inputSchema:" src/tools/

# Check error handling
grep -rE "isError:|content:" src/

# Test server startup
node dist/index.js --help
```
