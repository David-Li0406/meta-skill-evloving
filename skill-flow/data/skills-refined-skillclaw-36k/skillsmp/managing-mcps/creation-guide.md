# MCP Server Creation Guide

Step-by-step instructions for building Model Context Protocol servers.

## Prerequisites

**Required Knowledge:**
- JSON-RPC protocol basics
- Async/await programming patterns
- Environment variable management

**Required Tools:**
- Node.js 18+ (for TypeScript/JavaScript servers) OR
- Python 3.10+ (for Python servers)
- npm or pip package manager
- Text editor or IDE

## Language Choice

**TypeScript/JavaScript:**
- Official SDK: `@modelcontextprotocol/sdk`
- Best for: Node.js integrations, npm ecosystem tools
- Transport: stdio, SSE built-in

**Python:**
- Official SDK: `mcp` package
- Best for: Data science, ML tools, Python ecosystem integrations
- Transport: stdio built-in

**Other Languages:**
- Implement protocol manually from specification
- Requires JSON-RPC 2.0 implementation
- Requires transport layer implementation

## TypeScript Server Creation

### Step 1: Project Initialization

```bash
mkdir my-mcp-server
cd my-mcp-server
npm init -y
npm install @modelcontextprotocol/sdk
npm install -D typescript @types/node
```

Create `tsconfig.json`:
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "Node16",
    "moduleResolution": "Node16",
    "outDir": "./build",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true
  }
}
```

Update `package.json`:
```json
{
  "type": "module",
  "bin": {
    "my-mcp-server": "./build/index.js"
  },
  "scripts": {
    "build": "tsc",
    "prepare": "npm run build"
  }
}
```

### Step 2: Basic Server Structure

Create `src/index.ts`:
```typescript
#!/usr/bin/env node
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

// Server instance
const server = new Server(
  {
    name: "my-mcp-server",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Tool definitions
const tools = [
  {
    name: "example-tool",
    description: "Demonstrates basic tool functionality",
    inputSchema: {
      type: "object",
      properties: {
        message: {
          type: "string",
          description: "Message to process",
        },
      },
      required: ["message"],
    },
  },
];

// List tools handler
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools,
}));

// Call tool handler
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  if (name === "example-tool") {
    const message = args.message as string;
    return {
      content: [
        {
          type: "text",
          text: `Processed: ${message}`,
        },
      ],
    };
  }

  throw new Error(`Unknown tool: ${name}`);
});

// Connect transport
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch((error) => {
  console.error("Server error:", error);
  process.exit(1);
});
```

### Step 3: Build and Test

```bash
npm run build
npx @modelcontextprotocol/inspector node ./build/index.js
```

Inspector opens browser interface to test server interactively.

### Step 4: Add Tools

Extend tool implementations:

```typescript
interface ToolImplementation {
  name: string;
  execute: (args: Record<string, unknown>) => Promise<ToolResult>;
}

const toolImplementations: ToolImplementation[] = [
  {
    name: "example-tool",
    execute: async (args) => {
      // Validate inputs
      if (typeof args.message !== "string") {
        throw new Error("message must be string");
      }

      // Perform operation
      const result = processMessage(args.message);

      // Return structured result
      return {
        content: [
          {
            type: "text",
            text: result,
          },
        ],
      };
    },
  },
];

// Update CallTool handler
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  const tool = toolImplementations.find((t) => t.name === name);
  if (!tool) {
    throw new Error(`Unknown tool: ${name}`);
  }

  try {
    return await tool.execute(args);
  } catch (error) {
    return {
      content: [
        {
          type: "text",
          text: `Error: ${error.message}`,
        },
      ],
      isError: true,
    };
  }
});
```

### Step 5: Add Resources (Optional)

```typescript
import {
  ListResourcesRequestSchema,
  ReadResourceRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

// Update server capabilities
const server = new Server(
  { name: "my-mcp-server", version: "1.0.0" },
  {
    capabilities: {
      tools: {},
      resources: {},
    },
  }
);

// Resource definitions
server.setRequestHandler(ListResourcesRequestSchema, async () => ({
  resources: [
    {
      uri: "file:///data/example.txt",
      name: "Example Data",
      description: "Sample resource",
      mimeType: "text/plain",
    },
  ],
}));

// Resource reading
server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const { uri } = request.params;

  if (uri === "file:///data/example.txt") {
    return {
      contents: [
        {
          uri,
          mimeType: "text/plain",
          text: "Resource content here",
        },
      ],
    };
  }

  throw new Error(`Unknown resource: ${uri}`);
});
```

### Step 6: Add Prompts (Optional)

```typescript
import {
  ListPromptsRequestSchema,
  GetPromptRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

// Update capabilities
const server = new Server(
  { name: "my-mcp-server", version: "1.0.0" },
  {
    capabilities: {
      tools: {},
      prompts: {},
    },
  }
);

// Prompt definitions
server.setRequestHandler(ListPromptsRequestSchema, async () => ({
  prompts: [
    {
      name: "analysis-prompt",
      description: "Analyze data with context",
      arguments: [
        {
          name: "data",
          description: "Data to analyze",
          required: true,
        },
        {
          name: "context",
          description: "Analysis context",
          required: false,
        },
      ],
    },
  ],
}));

// Prompt generation
server.setRequestHandler(GetPromptRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  if (name === "analysis-prompt") {
    const data = args?.data as string;
    const context = (args?.context as string) || "general";

    return {
      messages: [
        {
          role: "user",
          content: {
            type: "text",
            text: `Analyze this data in ${context} context: ${data}`,
          },
        },
      ],
    };
  }

  throw new Error(`Unknown prompt: ${name}`);
});
```

### Step 7: Environment Configuration

Add environment variable support:

```typescript
interface Config {
  apiKey?: string;
  endpoint?: string;
  timeout?: number;
}

function loadConfig(): Config {
  return {
    apiKey: process.env.API_KEY,
    endpoint: process.env.API_ENDPOINT || "https://default.example.com",
    timeout: parseInt(process.env.TIMEOUT || "30000"),
  };
}

const config = loadConfig();

// Use in tool implementations
async function callExternalAPI(data: string) {
  if (!config.apiKey) {
    throw new Error("API_KEY environment variable required");
  }

  // Use config.apiKey, config.endpoint, etc.
}
```

### Step 8: Error Handling

Robust error handling:

```typescript
class ToolError extends Error {
  constructor(
    message: string,
    public readonly code: number = -32001
  ) {
    super(message);
    this.name = "ToolError";
  }
}

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    // Validate tool exists
    const tool = toolImplementations.find((t) => t.name === name);
    if (!tool) {
      throw new ToolError(`Unknown tool: ${name}`, -32601);
    }

    // Validate inputs
    validateInputs(name, args);

    // Execute
    return await tool.execute(args);
  } catch (error) {
    // Log error
    console.error(`Tool ${name} error:`, error);

    // Return error response
    return {
      content: [
        {
          type: "text",
          text: error instanceof ToolError ? error.message : "Internal error",
        },
      ],
      isError: true,
    };
  }
});
```

### Step 9: Logging

Add structured logging:

```typescript
import {
  LoggingMessageNotificationSchema,
} from "@modelcontextprotocol/sdk/types.js";

function log(level: "info" | "warning" | "error", message: string, data?: unknown) {
  // Console logging for development
  console[level === "error" ? "error" : level === "warning" ? "warn" : "log"](
    message,
    data
  );

  // Send to client
  server.notification({
    method: "notifications/message",
    params: {
      level,
      logger: "my-mcp-server",
      data: JSON.stringify({ message, ...data }),
    },
  });
}

// Use in tool implementations
log("info", "Tool executed", { tool: name, duration: 123 });
```

### Step 10: Testing

Create test file `src/test.ts`:

```typescript
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

async function test() {
  const transport = new StdioClientTransport({
    command: "node",
    args: ["./build/index.js"],
  });

  const client = new Client(
    {
      name: "test-client",
      version: "1.0.0",
    },
    {
      capabilities: {},
    }
  );

  await client.connect(transport);

  // Test tool listing
  const tools = await client.request(
    { method: "tools/list" },
    ListToolsRequestSchema
  );
  console.log("Tools:", tools);

  // Test tool calling
  const result = await client.request(
    {
      method: "tools/call",
      params: {
        name: "example-tool",
        arguments: { message: "test" },
      },
    },
    CallToolRequestSchema
  );
  console.log("Result:", result);

  await client.close();
}

test().catch(console.error);
```

## Python Server Creation

### Step 1: Project Setup

```bash
mkdir my-mcp-server
cd my-mcp-server
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install mcp
```

Create `pyproject.toml`:
```toml
[project]
name = "my-mcp-server"
version = "0.1.0"
dependencies = ["mcp"]

[project.scripts]
my-mcp-server = "my_mcp_server:main"
```

### Step 2: Basic Server

Create `my_mcp_server/__init__.py`:
```python
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

app = Server("my-mcp-server")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="example-tool",
            description="Demonstrates basic tool functionality",
            inputSchema={
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Message to process"
                    }
                },
                "required": ["message"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "example-tool":
        message = arguments["message"]
        return [TextContent(type="text", text=f"Processed: {message}")]

    raise ValueError(f"Unknown tool: {name}")

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

### Step 3: Install and Test

```bash
pip install -e .
python -m mcp.cli my-mcp-server
```

### Step 4: Add Resources

```python
from mcp.types import Resource, ResourceContents

@app.list_resources()
async def list_resources() -> list[Resource]:
    return [
        Resource(
            uri="file:///data/example.txt",
            name="Example Data",
            description="Sample resource",
            mimeType="text/plain"
        )
    ]

@app.read_resource()
async def read_resource(uri: str) -> ResourceContents:
    if uri == "file:///data/example.txt":
        return ResourceContents(
            uri=uri,
            mimeType="text/plain",
            text="Resource content here"
        )

    raise ValueError(f"Unknown resource: {uri}")
```

### Step 5: Add Prompts

```python
from mcp.types import Prompt, PromptMessage, GetPromptResult

@app.list_prompts()
async def list_prompts() -> list[Prompt]:
    return [
        Prompt(
            name="analysis-prompt",
            description="Analyze data with context",
            arguments=[
                {"name": "data", "description": "Data to analyze", "required": True},
                {"name": "context", "description": "Analysis context", "required": False}
            ]
        )
    ]

@app.get_prompt()
async def get_prompt(name: str, arguments: dict) -> GetPromptResult:
    if name == "analysis-prompt":
        data = arguments["data"]
        context = arguments.get("context", "general")

        return GetPromptResult(
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(
                        type="text",
                        text=f"Analyze this data in {context} context: {data}"
                    )
                )
            ]
        )

    raise ValueError(f"Unknown prompt: {name}")
```

### Step 6: Environment Configuration

```python
import os

class Config:
    api_key = os.getenv("API_KEY")
    endpoint = os.getenv("API_ENDPOINT", "https://default.example.com")
    timeout = int(os.getenv("TIMEOUT", "30"))

config = Config()

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if not config.api_key:
        raise ValueError("API_KEY environment variable required")

    # Use config values
```

### Step 7: Error Handling

```python
from mcp.types import TextContent

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    try:
        if name == "example-tool":
            # Validate inputs
            if "message" not in arguments:
                raise ValueError("message parameter required")

            message = arguments["message"]
            if not isinstance(message, str):
                raise TypeError("message must be string")

            # Execute
            result = process_message(message)

            return [TextContent(type="text", text=result)]

        raise ValueError(f"Unknown tool: {name}")

    except Exception as e:
        # Log error
        print(f"Tool {name} error: {e}")

        # Return error
        return [TextContent(
            type="text",
            text=f"Error: {str(e)}",
            isError=True
        )]
```

## Common Patterns

### Input Validation

```typescript
function validateInputs(toolName: string, args: Record<string, unknown>) {
  const schema = tools.find((t) => t.name === toolName)?.inputSchema;
  if (!schema) return;

  // Use JSON Schema validator
  const valid = ajv.validate(schema, args);
  if (!valid) {
    throw new ToolError(`Invalid inputs: ${ajv.errorsText()}`);
  }
}
```

### Async Operations

```typescript
async function longRunningOperation(progressToken?: string) {
  const total = 100;

  for (let i = 0; i < total; i++) {
    // Do work
    await doWork();

    // Report progress
    if (progressToken) {
      server.notification({
        method: "notifications/progress",
        params: {
          progressToken,
          progress: i,
          total,
        },
      });
    }
  }
}
```

### Resource Caching

```typescript
const resourceCache = new Map<string, { data: string; timestamp: number }>();
const CACHE_TTL = 60000; // 1 minute

async function readResourceCached(uri: string): Promise<string> {
  const cached = resourceCache.get(uri);
  if (cached && Date.now() - cached.timestamp < CACHE_TTL) {
    return cached.data;
  }

  const data = await fetchResource(uri);
  resourceCache.set(uri, { data, timestamp: Date.now() });
  return data;
}
```

### Tool Chaining

```typescript
// Tool 1: Fetch data
{
  name: "fetch-data",
  execute: async (args) => {
    const data = await fetchFromAPI(args.endpoint);
    return {
      content: [{
        type: "resource",
        uri: "temp://fetched-data",
        mimeType: "application/json"
      }]
    };
  }
}

// Tool 2: Process data from resource
{
  name: "process-data",
  execute: async (args) => {
    const data = await readResource(args.resourceUri);
    const result = processData(data);
    return {
      content: [{ type: "text", text: result }]
    };
  }
}
```

## Deployment

### Local Development

```bash
npm run build && npx @modelcontextprotocol/inspector node ./build/index.js
```

### Claude Code Integration

Add to `~/.claude/config.json`:
```json
{
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["/absolute/path/to/build/index.js"],
      "env": {
        "API_KEY": "secret-key"
      }
    }
  }
}
```

### npm Package

```bash
npm publish
```

Users install: `npm install -g my-mcp-server`

Config becomes:
```json
{
  "mcpServers": {
    "my-server": {
      "command": "npx",
      "args": ["-y", "my-mcp-server"]
    }
  }
}
```

### Docker Container

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --production
COPY build ./build
CMD ["node", "build/index.js"]
```

## Troubleshooting

**Server won't start:**
- Check Node.js/Python version
- Verify SDK installed: `npm list @modelcontextprotocol/sdk`
- Check for syntax errors in server code

**Tools not appearing:**
- Verify ListToolsRequest handler registered
- Check tool schema validity
- Restart Claude Code after config changes

**Tool execution fails:**
- Add try-catch around tool implementation
- Check input validation
- Verify environment variables set
- Check logs in Claude Code console

**Inspector not working:**
- Ensure server runs standalone: `node build/index.js`
- Check for console errors
- Verify stdio transport configured

## Reference Documentation

**Getting Started:**
- https://modelcontextprotocol.io/docs/getting-started/intro
- https://modelcontextprotocol.io/docs/develop/build-server

**SDK Documentation:**
- https://modelcontextprotocol.io/docs/sdk
- TypeScript: https://github.com/modelcontextprotocol/typescript-sdk
- Python: https://github.com/modelcontextprotocol/python-sdk

**Examples:**
- https://github.com/modelcontextprotocol/servers (official examples)
- https://github.com/punkpeye/awesome-mcp-servers (community examples)

**Testing:**
- https://modelcontextprotocol.io/docs/tools/inspector
