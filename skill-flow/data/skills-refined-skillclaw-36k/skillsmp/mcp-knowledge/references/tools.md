# MCP Tool Development

## Table of Contents

- [🚨 MANDATORY: Read BEFORE Development](#mandatory-read-before-development)
- [Tool Fundamentals](#tool-fundamentals)
- [Tool Schema Definition](#tool-schema-definition)
- [Implementation Examples](#implementation-examples)
- [Error Handling](#error-handling)
- [Advanced Patterns](#advanced-patterns)
- [Annotations](#annotations)
- [Naming Conventions](#naming-conventions)
- [Testing Tools](#testing-tools)
- [Best Practices](#best-practices)
- [Common Patterns](#common-patterns)
- [Next Steps](#next-steps)

Create custom MCP tools with proper schemas, validation, and error handling.

## 🚨 MANDATORY: Read BEFORE Development

**CRITICAL**: You MUST read and understand these URLs:

### Primary Documentation (MUST READ)
- **[MUST READ] MCP Specification**: https://modelcontextprotocol.io/
  - **Tool**: `mcp__simplewebfetch__simpleWebFetch`
  - **When to Read**: Before any MCP tool development
  - **Content**: Tool schemas, input/output validation, protocol requirements
  - **Cache**: 15 minutes minimum

- **[MUST READ] Official MCP Guide**: https://code.claude.com/docs/en/mcp
  - **Tool**: `mcp__simplewebfetch__simpleWebFetch`
  - **When to Read**: Before implementing MCP servers
  - **Content**: Integration patterns, best practices
  - **Cache**: 15 minutes minimum

### ⚠️ BLOCKING RULES
- **DO NOT proceed** without understanding MCP primitives
- **MUST validate** schemas before implementation
- **REQUIRED** to understand security considerations

## Tool Fundamentals

### What Are MCP Tools?
Callable functions exposed by MCP servers with:
- Named functions with input/output schemas
- Type-safe parameter validation
- Structured error handling
- Clear descriptions for discovery

### Tool Format
Format: `ServerName:tool_name`

Example: `github:create_issue`, `database:query`

## Tool Schema Definition

### Input Schema Structure
```json
{
  "name": "tool_name",
  "description": "Clear description of what this tool does",
  "inputSchema": {
    "type": "object",
    "properties": {
      "parameter_name": {
        "type": "string",
        "description": "Parameter description",
        "minLength": 1,
        "maxLength": 200
      }
    },
    "required": ["parameter_name"]
  }
}
```

### Parameter Types
- `string`: Text data
- `number`: Numeric values
- `boolean`: True/false values
- `array`: Lists of items
- `object`: Nested objects

### Best Practices
- Use specific types (not `any`)
- Include descriptions for all fields
- Set appropriate constraints (min/max length)
- Mark required fields clearly
- Provide examples in descriptions

## Implementation Examples

### Python Implementation
```python
from mcp import Server
from mcp.types import Tool

server = Server("my-server")

@server.list_tools()
async def handle_list_tools():
    return [
        Tool(
            name="search_web",
            description="Search the web for information",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query string",
                        "minLength": 1,
                        "maxLength": 200
                    },
                    "limit": {
                        "type": "number",
                        "description": "Maximum number of results",
                        "minimum": 1,
                        "maximum": 50,
                        "default": 10
                    }
                },
                "required": ["query"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name, arguments):
    if name == "search_web":
        query = arguments["query"]
        limit = arguments.get("limit", 10)

        # Tool implementation
        results = await search(query, limit)

        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Found {len(results)} results"
                }
            ]
        }
```

### TypeScript Implementation
```typescript
import { Server } from '@modelcontextprotocol/sdk/server/index.js';

const server = new Server('my-server', { version: '1.0.0' });

server.setRequestHandler('tools/list', async () => ({
  tools: [
    {
      name: 'search_web',
      description: 'Search the web for information',
      inputSchema: {
        type: 'object',
        properties: {
          query: {
            type: 'string',
            description: 'Search query string',
            minLength: 1,
            maxLength: 200
          },
          limit: {
            type: 'number',
            description: 'Maximum number of results',
            minimum: 1,
            maximum: 50,
            defaultValue: 10
          }
        },
        required: ['query']
      }
    }
  ]
}));

server.setRequestHandler('tools/call', async (request) => {
  const { name, arguments: args } = request.params;

  if (name === 'search_web') {
    const query = args.query;
    const limit = args.limit ?? 10;

    // Tool implementation
    const results = await search(query, limit);

    return {
      content: [
        {
          type: 'text',
          text: `Found ${results.length} results`
        }
      ]
    };
  }
});
```

## Error Handling

### Structured Error Responses
```typescript
async function executeTool(args) {
  try {
    const result = await externalAPI.call(args);
    return {
      content: [{ type: 'text', text: result }],
      isError: false
    };
  } catch (error) {
    return {
      content: [{
        type: 'text',
        text: `Error: ${error.message}`
      }],
      isError: true
    };
  }
}
```

### Validation Errors
```typescript
function validateToolInput(name, args) {
  // Validate tool name
  if (!isValidToolName(name)) {
    throw new Error('Invalid tool name');
  }

  // Validate arguments against schema
  if (!validateArguments(name, args)) {
    throw new Error('Invalid arguments');
  }

  return true;
}
```

## Advanced Patterns

### Tool Composition
```typescript
@server.call_tool()
async function handleCallTool(name, arguments) {
  switch (name) {
    case 'analyze_code':
      // Use multiple operations together
      const ast = await parseCode(arguments.code);
      const issues = await analyzeAST(ast);
      const suggestions = await generateSuggestions(issues);

      return formatResult(suggestions);

    default:
      throw new Error(`Unknown tool: ${name}`);
  }
}
```

### Pagination Support
```json
{
  "name": "list_items",
  "description": "List items with pagination",
  "inputSchema": {
    "type": "object",
    "properties": {
      "page": {
        "type": "number",
        "description": "Page number (1-based)",
        "minimum": 1,
        "default": 1
      },
      "limit": {
        "type": "number",
        "description": "Items per page",
        "minimum": 1,
        "maximum": 100,
        "default": 20
      }
    }
  }
}
```

### Resource Caching
```typescript
const toolCache = new Map();

@server.call_tool()
async function handleCallTool(name, arguments) {
  const cacheKey = `${name}:${JSON.stringify(arguments)}`;

  if (toolCache.has(cacheKey)) {
    return toolCache.get(cacheKey);
  }

  const result = await executeTool(name, arguments);
  toolCache.set(cacheKey, result);

  return result;
}
```

## Annotations

### Use Annotations for Better UX
```typescript
{
  "name": "delete_file",
  "description": "Delete a file from the system",
  "inputSchema": { ... },
  "annotations": {
    "readOnlyHint": false,
    "destructiveHint": true,
    "idempotentHint": false,
    "openWorldHint": false
  }
}
```

**Available Annotations**:
- `readOnlyHint`: Tool doesn't modify state
- `destructiveHint`: Tool performs destructive operations
- `idempotentHint`: Multiple calls have same effect
- `openWorldHint`: Tool accesses external systems

## Naming Conventions

### Tool Names
- Use descriptive, action-oriented names
- Prefix with server name: `github_create_issue`
- Use underscores for multi-word names
- Keep names concise but clear

### Parameter Names
- Use camelCase
- Be descriptive but concise
- Match parameter purpose

## Testing Tools

### MCP Inspector
```bash
# Test with MCP Inspector
npx @modelcontextprotocol/inspector
```

### Manual Testing
```bash
# Test server directly
node server.js

# Verify tool discovery
# Check tool schemas
# Test error handling
```

## Best Practices

### DO ✅
- Use official MCP SDKs
- Validate all inputs
- Implement proper error handling
- Document tools clearly
- Use type-safe schemas
- Cache when appropriate
- Follow naming conventions

### DON'T ❌
- Don't expose sensitive data
- Don't skip input validation
- Don't use unencrypted HTTP
- Don't hardcode credentials
- Don't ignore errors
- Don't expose internal APIs

## Common Patterns

### API Integration
```typescript
{
  "name": "api_call",
  "description": "Call external API endpoint",
  "inputSchema": {
    "type": "object",
    "properties": {
      "endpoint": {
        "type": "string",
        "description": "API endpoint URL"
      },
      "method": {
        "type": "string",
        "enum": ["GET", "POST", "PUT", "DELETE"],
        "description": "HTTP method"
      }
    }
  }
}
```

### Database Query
```typescript
{
  "name": "query_database",
  "description": "Execute SQL query",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "SQL query string"
      },
      "params": {
        "type": "array",
        "description": "Query parameters"
      }
    },
    "required": ["query"]
  }
}
```

## Next Steps

After tool development:
- See **[servers.md](servers.md)** to configure servers
- See **[resources.md](resources.md)** for resources and prompts
- Test thoroughly with MCP Inspector
- Create comprehensive evaluations
