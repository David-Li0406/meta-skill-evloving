# MCP Server Examples

Complete working examples of MCP server implementations for different use cases.

## Example 1: Simple stdio Server (TypeScript)

A basic MCP server that provides a greeting tool.

### Setup

```bash
mkdir my-mcp-server && cd my-mcp-server
bun init -y
bun add @modelcontextprotocol/sdk
```

### Implementation

```typescript
// src/index.ts
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

const server = new Server(
  {
    name: "greeting-server",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// List available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "greet",
        description: "Generate a personalized greeting",
        inputSchema: {
          type: "object",
          properties: {
            name: {
              type: "string",
              description: "Name of the person to greet",
            },
            style: {
              type: "string",
              enum: ["formal", "casual", "enthusiastic"],
              description: "Style of greeting",
            },
          },
          required: ["name"],
        },
      },
    ],
  };
});

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "greet") {
    const { name, style = "casual" } = request.params.arguments as {
      name: string;
      style?: string;
    };

    let greeting: string;
    switch (style) {
      case "formal":
        greeting = `Good day, ${name}. It is a pleasure to make your acquaintance.`;
        break;
      case "enthusiastic":
        greeting = `Hey ${name}! So great to see you! This is AMAZING!`;
        break;
      default:
        greeting = `Hi ${name}! How are you doing?`;
    }

    return {
      content: [{ type: "text", text: greeting }],
    };
  }

  throw new Error(`Unknown tool: ${request.params.name}`);
});

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Greeting MCP server running on stdio");
}

main().catch(console.error);
```

### Package.json

```json
{
  "name": "greeting-mcp-server",
  "version": "1.0.0",
  "type": "module",
  "main": "src/index.ts",
  "bin": {
    "greeting-server": "./src/index.ts"
  },
  "scripts": {
    "start": "bun run src/index.ts"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.0.0"
  }
}
```

### Register with Claude Code

```bash
claude mcp add --transport stdio greeting -- bun run /path/to/my-mcp-server/src/index.ts
```

### Usage

```
> Use the greeting tool to greet Alice formally
Claude will call mcp__greeting__greet with {name: "Alice", style: "formal"}
```

## Example 2: HTTP Server with Authentication

An HTTP MCP server with API key authentication.

### Implementation

```typescript
// src/http-server.ts
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { HttpServerTransport } from "@modelcontextprotocol/sdk/server/http.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

const API_KEY = process.env.API_KEY;

const server = new Server(
  {
    name: "weather-server",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "get_weather",
        description: "Get current weather for a city",
        inputSchema: {
          type: "object",
          properties: {
            city: { type: "string", description: "City name" },
            units: {
              type: "string",
              enum: ["celsius", "fahrenheit"],
              default: "celsius",
            },
          },
          required: ["city"],
        },
      },
    ],
  };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "get_weather") {
    const { city, units = "celsius" } = request.params.arguments as {
      city: string;
      units?: string;
    };

    // In production, call actual weather API
    const temp = units === "celsius" ? "22C" : "72F";

    return {
      content: [
        {
          type: "text",
          text: JSON.stringify({
            city,
            temperature: temp,
            conditions: "Sunny",
            humidity: "45%",
          }),
        },
      ],
    };
  }

  throw new Error(`Unknown tool: ${request.params.name}`);
});

// HTTP server with auth middleware
const httpTransport = new HttpServerTransport({
  port: 8080,
  path: "/mcp",
  // Validate API key on each request
  onRequest: (req) => {
    const authHeader = req.headers.get("Authorization");
    if (!authHeader || authHeader !== `Bearer ${API_KEY}`) {
      throw new Error("Unauthorized");
    }
  },
});

async function main() {
  await server.connect(httpTransport);
  console.log("Weather MCP server running on http://localhost:8080/mcp");
}

main().catch(console.error);
```

### Running

```bash
API_KEY=your-secret-key bun run src/http-server.ts
```

### Register with Claude Code

```bash
claude mcp add --transport http weather http://localhost:8080/mcp \
  --header "Authorization: Bearer your-secret-key"
```

## Example 3: Database Connection Server

Connect Claude Code to PostgreSQL for natural language queries.

### Implementation

```typescript
// src/db-server.ts
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  ListResourcesRequestSchema,
  ReadResourceRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { Pool } from "pg";

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
});

const server = new Server(
  {
    name: "postgres-server",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
      resources: {},
    },
  }
);

// Tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "query",
        description: "Execute a read-only SQL query",
        inputSchema: {
          type: "object",
          properties: {
            sql: {
              type: "string",
              description: "SQL SELECT query to execute",
            },
            limit: {
              type: "number",
              description: "Max rows to return",
              default: 100,
            },
          },
          required: ["sql"],
        },
      },
      {
        name: "describe_table",
        description: "Get schema information for a table",
        inputSchema: {
          type: "object",
          properties: {
            table: { type: "string", description: "Table name" },
          },
          required: ["table"],
        },
      },
    ],
  };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  if (name === "query") {
    const { sql, limit = 100 } = args as { sql: string; limit?: number };

    // Safety: Only allow SELECT queries
    if (!sql.trim().toLowerCase().startsWith("select")) {
      return {
        content: [{ type: "text", text: "Error: Only SELECT queries allowed" }],
        isError: true,
      };
    }

    try {
      const result = await pool.query(`${sql} LIMIT ${limit}`);
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(result.rows, null, 2),
          },
        ],
      };
    } catch (error) {
      return {
        content: [{ type: "text", text: `Query error: ${error}` }],
        isError: true,
      };
    }
  }

  if (name === "describe_table") {
    const { table } = args as { table: string };
    const result = await pool.query(
      `SELECT column_name, data_type, is_nullable
       FROM information_schema.columns
       WHERE table_name = $1`,
      [table]
    );
    return {
      content: [{ type: "text", text: JSON.stringify(result.rows, null, 2) }],
    };
  }

  throw new Error(`Unknown tool: ${name}`);
});

// Resources - expose database schemas
server.setRequestHandler(ListResourcesRequestSchema, async () => {
  const result = await pool.query(
    "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
  );

  return {
    resources: result.rows.map((row) => ({
      uri: `postgres://schema/${row.table_name}`,
      name: row.table_name,
      description: `Schema for ${row.table_name} table`,
      mimeType: "application/json",
    })),
  };
});

server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const uri = request.params.uri;
  const match = uri.match(/postgres:\/\/schema\/(.+)/);

  if (!match) {
    throw new Error(`Invalid resource URI: ${uri}`);
  }

  const tableName = match[1];
  const result = await pool.query(
    `SELECT column_name, data_type, is_nullable, column_default
     FROM information_schema.columns
     WHERE table_name = $1`,
    [tableName]
  );

  return {
    contents: [
      {
        uri,
        mimeType: "application/json",
        text: JSON.stringify(result.rows, null, 2),
      },
    ],
  };
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("PostgreSQL MCP server running");
}

main().catch(console.error);
```

### Register

```bash
claude mcp add --transport stdio \
  --env DATABASE_URL="postgresql://user:pass@localhost:5432/mydb" \
  postgres -- bun run /path/to/db-server.ts
```

### Usage

```
> What tables do we have in the database?
> Show me the schema for the users table
> Query: Find users created in the last 7 days
> Analyze @postgres://schema/orders and suggest indexes
```

## Example 4: File System Server

Expose a sandboxed directory to Claude Code.

### Implementation

```typescript
// src/fs-server.ts
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import * as fs from "fs/promises";
import * as path from "path";

const SANDBOX_DIR = process.env.SANDBOX_DIR || "/tmp/mcp-sandbox";

// Ensure path stays within sandbox
function safePath(filePath: string): string {
  const resolved = path.resolve(SANDBOX_DIR, filePath);
  if (!resolved.startsWith(SANDBOX_DIR)) {
    throw new Error("Path traversal detected");
  }
  return resolved;
}

const server = new Server(
  {
    name: "filesystem-server",
    version: "1.0.0",
  },
  {
    capabilities: { tools: {} },
  }
);

server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "list_files",
        description: "List files in a directory",
        inputSchema: {
          type: "object",
          properties: {
            path: { type: "string", description: "Directory path (relative to sandbox)" },
          },
          required: ["path"],
        },
      },
      {
        name: "read_file",
        description: "Read file contents",
        inputSchema: {
          type: "object",
          properties: {
            path: { type: "string", description: "File path (relative to sandbox)" },
          },
          required: ["path"],
        },
      },
      {
        name: "write_file",
        description: "Write content to a file",
        inputSchema: {
          type: "object",
          properties: {
            path: { type: "string", description: "File path (relative to sandbox)" },
            content: { type: "string", description: "Content to write" },
          },
          required: ["path", "content"],
        },
      },
    ],
  };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    if (name === "list_files") {
      const dirPath = safePath((args as { path: string }).path);
      const entries = await fs.readdir(dirPath, { withFileTypes: true });
      const files = entries.map((e) => ({
        name: e.name,
        type: e.isDirectory() ? "directory" : "file",
      }));
      return { content: [{ type: "text", text: JSON.stringify(files, null, 2) }] };
    }

    if (name === "read_file") {
      const filePath = safePath((args as { path: string }).path);
      const content = await fs.readFile(filePath, "utf-8");
      return { content: [{ type: "text", text: content }] };
    }

    if (name === "write_file") {
      const { path: filePath, content } = args as { path: string; content: string };
      const safe = safePath(filePath);
      await fs.mkdir(path.dirname(safe), { recursive: true });
      await fs.writeFile(safe, content);
      return { content: [{ type: "text", text: `Written to ${filePath}` }] };
    }
  } catch (error) {
    return {
      content: [{ type: "text", text: `Error: ${error}` }],
      isError: true,
    };
  }

  throw new Error(`Unknown tool: ${name}`);
});

async function main() {
  // Ensure sandbox exists
  await fs.mkdir(SANDBOX_DIR, { recursive: true });

  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error(`Filesystem MCP server running (sandbox: ${SANDBOX_DIR})`);
}

main().catch(console.error);
```

### Register

```bash
claude mcp add --transport stdio \
  --env SANDBOX_DIR=/path/to/sandbox \
  filesystem -- bun run /path/to/fs-server.ts
```

## Example 5: API Wrapper Server

Wrap an external REST API as MCP tools.

### Implementation

```typescript
// src/api-wrapper.ts
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

const API_BASE = process.env.API_BASE || "https://api.example.com";
const API_KEY = process.env.API_KEY;

async function apiCall(
  method: string,
  endpoint: string,
  body?: object
): Promise<any> {
  const response = await fetch(`${API_BASE}${endpoint}`, {
    method,
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${API_KEY}`,
    },
    body: body ? JSON.stringify(body) : undefined,
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status} ${response.statusText}`);
  }

  return response.json();
}

const server = new Server(
  {
    name: "api-wrapper",
    version: "1.0.0",
  },
  {
    capabilities: { tools: {} },
  }
);

server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "list_items",
        description: "List items from the API",
        inputSchema: {
          type: "object",
          properties: {
            page: { type: "number", default: 1 },
            per_page: { type: "number", default: 20 },
            filter: { type: "string", description: "Filter query" },
          },
        },
      },
      {
        name: "get_item",
        description: "Get a single item by ID",
        inputSchema: {
          type: "object",
          properties: {
            id: { type: "string", description: "Item ID" },
          },
          required: ["id"],
        },
      },
      {
        name: "create_item",
        description: "Create a new item",
        inputSchema: {
          type: "object",
          properties: {
            name: { type: "string" },
            description: { type: "string" },
            tags: { type: "array", items: { type: "string" } },
          },
          required: ["name"],
        },
      },
      {
        name: "update_item",
        description: "Update an existing item",
        inputSchema: {
          type: "object",
          properties: {
            id: { type: "string" },
            name: { type: "string" },
            description: { type: "string" },
            tags: { type: "array", items: { type: "string" } },
          },
          required: ["id"],
        },
      },
      {
        name: "delete_item",
        description: "Delete an item",
        inputSchema: {
          type: "object",
          properties: {
            id: { type: "string" },
          },
          required: ["id"],
        },
      },
    ],
  };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    let result: any;

    switch (name) {
      case "list_items": {
        const { page = 1, per_page = 20, filter } = args as any;
        const query = new URLSearchParams({
          page: String(page),
          per_page: String(per_page),
          ...(filter && { filter }),
        });
        result = await apiCall("GET", `/items?${query}`);
        break;
      }

      case "get_item": {
        const { id } = args as { id: string };
        result = await apiCall("GET", `/items/${id}`);
        break;
      }

      case "create_item": {
        result = await apiCall("POST", "/items", args);
        break;
      }

      case "update_item": {
        const { id, ...data } = args as { id: string; [key: string]: any };
        result = await apiCall("PATCH", `/items/${id}`, data);
        break;
      }

      case "delete_item": {
        const { id } = args as { id: string };
        await apiCall("DELETE", `/items/${id}`);
        result = { success: true, message: `Item ${id} deleted` };
        break;
      }

      default:
        throw new Error(`Unknown tool: ${name}`);
    }

    return {
      content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
    };
  } catch (error) {
    return {
      content: [{ type: "text", text: `Error: ${error}` }],
      isError: true,
    };
  }
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("API wrapper MCP server running");
}

main().catch(console.error);
```

### Register

```bash
claude mcp add --transport stdio \
  --env API_BASE=https://api.example.com \
  --env API_KEY=your-key \
  myapi -- bun run /path/to/api-wrapper.ts
```

## Example 6: MCP Prompts

Expose reusable prompt templates.

### Implementation

```typescript
// src/prompts-server.ts
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  ListPromptsRequestSchema,
  GetPromptRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

const server = new Server(
  {
    name: "prompts-server",
    version: "1.0.0",
  },
  {
    capabilities: { prompts: {} },
  }
);

const prompts = {
  code_review: {
    name: "code_review",
    description: "Review code for best practices and potential issues",
    arguments: [
      { name: "language", description: "Programming language", required: true },
      { name: "focus", description: "Areas to focus on (security, performance, style)" },
    ],
  },
  explain_error: {
    name: "explain_error",
    description: "Explain an error message and suggest fixes",
    arguments: [
      { name: "error", description: "The error message", required: true },
      { name: "context", description: "Additional context" },
    ],
  },
  generate_tests: {
    name: "generate_tests",
    description: "Generate unit tests for code",
    arguments: [
      { name: "framework", description: "Test framework (jest, pytest, etc.)", required: true },
      { name: "coverage", description: "Coverage type (unit, integration, e2e)" },
    ],
  },
};

server.setRequestHandler(ListPromptsRequestSchema, async () => {
  return { prompts: Object.values(prompts) };
});

server.setRequestHandler(GetPromptRequestSchema, async (request) => {
  const { name, arguments: args = {} } = request.params;
  const prompt = prompts[name as keyof typeof prompts];

  if (!prompt) {
    throw new Error(`Unknown prompt: ${name}`);
  }

  let messages: Array<{ role: string; content: { type: string; text: string } }>;

  switch (name) {
    case "code_review":
      messages = [
        {
          role: "user",
          content: {
            type: "text",
            text: `Please review the following ${args.language} code.
${args.focus ? `Focus areas: ${args.focus}` : ""}

Check for:
- Code quality and readability
- Potential bugs or errors
- Security vulnerabilities
- Performance issues
- Best practices

Provide specific suggestions for improvement.`,
          },
        },
      ];
      break;

    case "explain_error":
      messages = [
        {
          role: "user",
          content: {
            type: "text",
            text: `Please explain this error and suggest how to fix it:

Error: ${args.error}

${args.context ? `Context: ${args.context}` : ""}

Please:
1. Explain what this error means
2. List possible causes
3. Provide step-by-step solutions
4. Show example code if applicable`,
          },
        },
      ];
      break;

    case "generate_tests":
      messages = [
        {
          role: "user",
          content: {
            type: "text",
            text: `Generate ${args.coverage || "unit"} tests using ${args.framework}.

Requirements:
- Cover edge cases
- Include positive and negative tests
- Use descriptive test names
- Follow ${args.framework} best practices`,
          },
        },
      ];
      break;

    default:
      throw new Error(`Unknown prompt: ${name}`);
  }

  return { messages };
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Prompts MCP server running");
}

main().catch(console.error);
```

### Usage in Claude Code

```
> /mcp__prompts__code_review typescript security
> /mcp__prompts__explain_error "TypeError: Cannot read property 'x' of undefined"
> /mcp__prompts__generate_tests jest unit
```

## Publishing Your Server

### npm Package Structure

```
my-mcp-server/
  package.json
  src/
    index.ts
  dist/
    index.js
  README.md
```

### package.json for Publishing

```json
{
  "name": "@yourorg/mcp-server",
  "version": "1.0.0",
  "type": "module",
  "main": "dist/index.js",
  "bin": {
    "mcp-server": "dist/index.js"
  },
  "files": ["dist"],
  "scripts": {
    "build": "tsc",
    "prepublishOnly": "npm run build"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.0.0"
  }
}
```

### Users Install With

```bash
claude mcp add --transport stdio myserver -- npx -y @yourorg/mcp-server
```
