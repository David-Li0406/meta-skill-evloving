# MCP Architecture Overview

Comprehensive reference for Model Context Protocol structure, concepts, and protocol mechanics.

## Protocol Fundamentals

**Current Specification**: 2025-06-18

**Core Concept**: MCP is client-server protocol where:
- **Client**: AI application (Claude Code) that initiates connections
- **Server**: Service providing capabilities (tools, resources, prompts)
- **Host**: Application controlling client behavior

**Communication**: JSON-RPC 2.0 messages over transport layer

## Architecture Layers

### 1. Transport Layer

Handles message exchange between client and server.

**Available Transports:**

**stdio (Standard Input/Output)**
- Most common for local servers
- Server runs as child process
- Messages via stdin/stdout
- Lifecycle tied to process
- Best for: Command-line tools, local integrations
- Configuration: `{"command": "node", "args": ["server.js"]}`

**SSE (Server-Sent Events)**
- HTTP-based for remote servers
- Long-lived HTTP connection
- Unidirectional server→client events
- Client requests via separate HTTP calls
- Best for: Web services, cloud deployments
- Configuration: `{"url": "https://server.example/sse"}`

**Custom Transports**
- Implement transport interface
- WebSocket, named pipes, etc.
- Requires custom client/server code

### 2. Protocol Layer

JSON-RPC 2.0 message structure.

**Message Types:**

**Request** (client → server):
```json
{
  "jsonrpc": "2.0",
  "id": "unique-id",
  "method": "tools/call",
  "params": {
    "name": "tool-name",
    "arguments": {}
  }
}
```

**Response** (server → client):
```json
{
  "jsonrpc": "2.0",
  "id": "same-id",
  "result": {
    "content": [{"type": "text", "text": "Result"}]
  }
}
```

**Notification** (either direction, no response expected):
```json
{
  "jsonrpc": "2.0",
  "method": "notifications/message",
  "params": {"level": "info", "message": "Status update"}
}
```

**Error**:
```json
{
  "jsonrpc": "2.0",
  "id": "same-id",
  "error": {
    "code": -32600,
    "message": "Invalid request",
    "data": {}
  }
}
```

### 3. Capability Layer

Functional capabilities servers expose.

## Server Capabilities

### Tools

Functions AI can invoke to perform actions.

**Structure:**
```typescript
interface Tool {
  name: string;                // Unique identifier
  description: string;         // Natural language purpose
  inputSchema: JSONSchema;     // Parameter validation
}
```

**Lifecycle:**
1. Server registers tools via `ListToolsRequest` handler
2. Client discovers available tools
3. Client invokes tool via `CallToolRequest`
4. Server executes and returns result

**Tool Result Format:**
```typescript
{
  content: [
    {type: "text", text: "Result text"},
    {type: "image", data: "base64...", mimeType: "image/png"},
    {type: "resource", uri: "file:///path", mimeType: "text/plain"}
  ],
  isError?: boolean
}
```

**Best Practices:**
- Atomic operations (one clear purpose)
- Idempotent when possible
- Clear error messages
- Validate all inputs against schema
- Return structured data when appropriate

### Resources

Data sources AI can read.

**Structure:**
```typescript
interface Resource {
  uri: string;                 // Unique identifier (URI format)
  name: string;                // Human-readable name
  description?: string;        // Purpose
  mimeType?: string;           // Content type
}
```

**URI Patterns:**
- `file:///path/to/resource` - File system
- `db://database/table/id` - Database records
- `api://service/endpoint` - API data
- Custom schemes for domain-specific resources

**Lifecycle:**
1. Server registers resources via `ListResourcesRequest` handler
2. Client discovers available resources
3. Client reads resource via `ReadResourceRequest`
4. Server returns content

**Resource Templates:**
Dynamic URIs with variables:
- `file:///{path}` - User-specified path
- `db://database/{table}/{id}` - Dynamic database query

**Subscriptions:**
Client can subscribe to resource changes:
1. Client sends `SubscribeRequest` with URI
2. Server sends notifications when resource changes
3. Client re-reads resource on notification

### Prompts

Reusable prompt templates with arguments.

**Structure:**
```typescript
interface Prompt {
  name: string;                // Unique identifier
  description?: string;        // Purpose
  arguments?: Array<{          // Template variables
    name: string;
    description?: string;
    required?: boolean;
  }>;
}
```

**Lifecycle:**
1. Server registers prompts via `ListPromptsRequest` handler
2. Client discovers available prompts
3. Client gets prompt via `GetPromptRequest` with arguments
4. Server returns formatted messages

**Prompt Message Format:**
```typescript
{
  messages: [
    {
      role: "user" | "assistant",
      content: {
        type: "text" | "image" | "resource",
        text?: string,
        data?: string,
        mimeType?: string
      }
    }
  ]
}
```

## Protocol Lifecycle

### 1. Initialization

**Client initiates:**
```json
{
  "method": "initialize",
  "params": {
    "protocolVersion": "2025-06-18",
    "capabilities": {
      "roots": {"listChanged": true},
      "sampling": {}
    },
    "clientInfo": {
      "name": "claude-code",
      "version": "1.0.0"
    }
  }
}
```

**Server responds:**
```json
{
  "result": {
    "protocolVersion": "2025-06-18",
    "capabilities": {
      "tools": {},
      "resources": {"subscribe": true},
      "prompts": {}
    },
    "serverInfo": {
      "name": "my-server",
      "version": "1.0.0"
    }
  }
}
```

**Client confirms:**
```json
{
  "method": "notifications/initialized"
}
```

### 2. Operation

**Capability Discovery:**
- Client: `tools/list` → Server returns tool definitions
- Client: `resources/list` → Server returns available resources
- Client: `prompts/list` → Server returns prompt templates

**Capability Usage:**
- Client: `tools/call` → Server executes tool
- Client: `resources/read` → Server returns resource content
- Client: `prompts/get` → Server returns formatted prompt

**Dynamic Updates:**
- Server: `notifications/tools/list_changed` → Client re-lists tools
- Server: `notifications/resources/updated` → Client re-reads resource

### 3. Utilities

**Progress Tracking:**
```json
{
  "method": "notifications/progress",
  "params": {
    "progressToken": "token-from-request",
    "progress": 50,
    "total": 100
  }
}
```

**Logging:**
```json
{
  "method": "notifications/message",
  "params": {
    "level": "info" | "warning" | "error",
    "logger": "component-name",
    "data": "Log message"
  }
}
```

**Cancellation:**
Client can cancel long-running operations:
```json
{
  "method": "notifications/cancelled",
  "params": {
    "requestId": "id-to-cancel",
    "reason": "User cancelled"
  }
}
```

### 4. Shutdown

**Graceful:**
- Client closes transport
- Server cleans up resources
- Process exits (stdio) or connection closes (SSE)

**Error:**
- Transport failure detected
- Both sides clean up
- Client may retry connection

## Client Capabilities

Servers can invoke client capabilities (when authorized):

### Sampling

Request LLM completion from client:
```json
{
  "method": "sampling/createMessage",
  "params": {
    "messages": [...],
    "modelPreferences": {
      "hints": [{"name": "claude-3-5-sonnet-20241022"}]
    },
    "maxTokens": 1024
  }
}
```

**Use Cases:**
- Chain-of-thought reasoning
- Multi-step analysis
- Content generation

### Roots

Access to client's filesystem roots:
```json
{
  "method": "roots/list",
  "params": {}
}
```

**Response:**
```json
{
  "result": {
    "roots": [
      {"uri": "file:///workspace", "name": "Project"}
    ]
  }
}
```

## Error Codes

Standard JSON-RPC codes:
- `-32700` Parse error
- `-32600` Invalid request
- `-32601` Method not found
- `-32602` Invalid params
- `-32603` Internal error

MCP-specific codes:
- `-32001` Tool execution failed
- `-32002` Resource not found
- `-32003` Prompt not found

## Security Model

**Isolation:**
- Server runs in separate process (stdio)
- Server has own permission scope
- No direct filesystem/network access from client

**Authorization:**
- Optional OAuth 2.0 for remote servers
- Environment variable secrets
- Request validation

**Input Validation:**
- JSON Schema enforcement
- Parameter sanitization
- Path traversal prevention

**Rate Limiting:**
- Server-side request throttling
- Resource usage quotas
- Connection limits

## SDK Usage Patterns

**Server Setup (TypeScript):**
```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new Server({
  name: "my-server",
  version: "1.0.0"
}, {
  capabilities: {
    tools: {},
    resources: {},
    prompts: {}
  }
});

// Register handlers
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [...]
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => ({
  content: [...]
}));

// Connect transport
const transport = new StdioServerTransport();
await server.connect(transport);
```

**Server Setup (Python):**
```python
from mcp.server import Server
from mcp.server.stdio import stdio_server

app = Server("my-server")

@app.list_tools()
async def list_tools():
    return [...]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    return [...]

async def main():
    async with stdio_server() as streams:
        await app.run(
            streams[0],
            streams[1],
            app.create_initialization_options()
        )
```

## Performance Considerations

**Connection Overhead:**
- stdio: Low (local process)
- SSE: Higher (network latency)

**Message Size:**
- Keep tool results concise
- Use resource references for large data
- Stream large responses when possible

**Concurrency:**
- Servers should handle concurrent requests
- Use async/await patterns
- Implement request queuing if needed

**Caching:**
- Cache expensive operations
- Invalidate on resource updates
- Consider client-side caching

## Versioning

**Protocol Version Format:** `YYYY-MM-DD`

**Current:** `2025-06-18`

**Compatibility:**
- Servers declare supported version in initialization
- Clients choose compatible version
- Breaking changes require new version
- Servers should support multiple versions

**Migration:**
- Check changelog for breaking changes
- Update SDK to latest version
- Test with MCP Inspector
- Update capability declarations

## Claude Code Integration

Claude Code-specific features and patterns for MCP usage.

### Transport Recommendations

**Preference order for new servers:**

1. **HTTP (Recommended)**: Cloud-based services, standard web protocols
   - Use for: Remote APIs, cloud deployments, production services
   - Configuration: `claude mcp add --transport http name https://api.example.com/mcp`

2. **stdio**: Local processes, direct system access
   - Use for: Local tools, development servers, filesystem operations
   - Configuration: `claude mcp add --transport stdio name -- node /path/to/server.js`

3. **SSE (Deprecated)**: Legacy remote servers only
   - Avoid for new implementations
   - Use HTTP instead

### Configuration Methods

**Primary: CLI commands**
```bash
claude mcp add --transport [stdio|http|sse] [--scope local|project|user] [--env KEY=VALUE] [--header "Name: Value"] [name] [command/url]
claude mcp list
claude mcp get [name]
claude mcp remove [name]
claude mcp add-json [json-string]
claude mcp add-from-claude-desktop
claude mcp reset-project-choices
claude mcp serve
```

**Key flags:**
- `--scope local|project|user` - Set configuration scope
- `--env KEY=VALUE` - Pass environment variables (repeatable)
- `--header "Name: Value"` - Add HTTP headers for http/sse (repeatable)
- `--` - Separates Claude flags from server command (stdio only)

**Alternative: Direct file manipulation**
- File: `.mcp.json` in project root
- Structure: `{"mcpServers": {"name": {...}}}`
- Requires Claude Code restart after changes

### Scope Levels

Three configuration tiers:

1. **Local** (highest priority): Session-specific, temporary
2. **Project**: `.mcp.json` in project root, team-shared
3. **User** (lowest priority): Cross-project personal

**Resolution:** Local > Project > User

### In-Conversation Features

**Check server status:**
```
/mcp
```

Shows connected servers, authentication status, available capabilities.

**Reference MCP resources:**
```
@server:protocol://resource/path
```

Examples:
- `@github:api://repo/owner/name/issues`
- `@filesystem:file:///workspace/file.txt`
- `@database:db://table/id`

Claude Code fetches resource and injects content into conversation.

**Invoke MCP prompts:**
```
/mcp__servername__promptname [arguments]
```

MCP prompts exposed as slash commands with tab completion.

### Authentication

**OAuth 2.0 flow:**
1. Configure server (CLI or .mcp.json)
2. Start Claude Code
3. User types `/mcp` in conversation
4. Follow OAuth prompts
5. Tokens stored securely, auto-refresh

**No manual token management required.**

### Environment Variables

**Expansion syntax:**
- `${VAR}` - Expands from system environment
- `${VAR:-default}` - Uses default if VAR not set

**Example:**
```json
{
  "env": {
    "API_KEY": "${API_KEY}",
    "LOG_LEVEL": "${LOG_LEVEL:-info}"
  }
}
```

### Output Limits

**Token limits:**
- Warning threshold: 10,000 tokens
- Default maximum: 25,000 tokens
- Configurable: `MAX_MCP_OUTPUT_TOKENS` environment variable

**Timeouts:**
- Server startup timeout: Configurable via `MCP_TIMEOUT` (milliseconds)
- Default: System-dependent

**Configure behavior:**
```bash
MAX_MCP_OUTPUT_TOKENS=50000 claude  # Increase output limit
MCP_TIMEOUT=10000 claude            # Set 10s startup timeout
```

Large outputs truncated automatically.

### Enterprise Deployment

**Managed MCP servers** (system-wide, admin-controlled):

- **macOS**: `/Library/Application Support/ClaudeCode/managed-mcp.json`
- **Windows**: `C:\ProgramData\ClaudeCode\managed-mcp.json`
- **Linux**: `/etc/claude-code/managed-mcp.json`

Managed configs override user/project/local settings.

### Popular Integrations

**40+ remote MCP servers available:**

- **Project Management**: Asana, Jira, Linear, Notion, Monday
- **Payments**: PayPal, Stripe, Square, Plaid
- **Design**: Figma, Canva, Cloudinary
- **Infrastructure**: Cloudflare, Netlify, Vercel
- **Data**: Airtable, HubSpot, Daloopa
- **Automation**: Zapier, Workato

Connect via HTTP transport, authenticate with `/mcp` command.

### Tool Usage Patterns

**When configuring MCP:**
- Use Bash for CLI commands: `claude mcp add ...`
- Use Read/Edit for `.mcp.json` when CLI unavailable
- User must restart Claude Code (cannot automate)

**When verifying connection:**
- Use Bash: `claude mcp list`, `claude mcp get name`
- Direct user to type `/mcp` in conversation

**When troubleshooting:**
- Use Bash with Inspector: `npx @modelcontextprotocol/inspector ...`
- Use Bash to test server standalone
- Use Read to examine `.mcp.json` configuration

## Reference Documentation

**Claude Code MCP:**
- https://code.claude.com/docs/en/mcp
- https://docs.claude.com/en/docs/agents-and-tools/mcp-connector
- https://docs.claude.com/en/docs/agents-and-tools/remote-mcp-servers

**Core Specs:**
- https://modelcontextprotocol.io/specification/2025-06-18
- https://modelcontextprotocol.io/specification/2025-06-18/architecture
- https://modelcontextprotocol.io/specification/2025-06-18/basic

**Capabilities:**
- https://modelcontextprotocol.io/specification/2025-06-18/server/tools
- https://modelcontextprotocol.io/specification/2025-06-18/server/resources
- https://modelcontextprotocol.io/specification/2025-06-18/server/prompts

**Advanced:**
- https://modelcontextprotocol.io/specification/2025-06-18/client/sampling
- https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization
- https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices
