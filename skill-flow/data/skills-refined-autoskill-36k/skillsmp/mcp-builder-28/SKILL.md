---
name: mcp-builder
description: 'Build Model Context Protocol (MCP) servers. Guide step-by-step từ specification đến implementation, testing, deployment.'
---

# MCP Builder Skill

Skill này guide bạn through the process of building MCP (Model Context Protocol) servers, cho phép AI models interact với external systems.

## Khi Nào Sử Dụng

- Build custom MCP server cho specific service
- Expose APIs/databases cho AI consumption
- Create tool integrations
- Build agentic workflows
- Connect AI với external data sources

---

## MCP Overview

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Client    │────▶│ MCP Server  │────▶│  External   │
│  (Claude)   │◀────│   (Your)    │◀────│   Service   │
└─────────────┘     └─────────────┘     └─────────────┘
    JSON-RPC         Your Logic          API/DB/etc
```

### Core Concepts

| Concept | Description |
|---------|-------------|
| **Tools** | Functions AI có thể call |
| **Resources** | Data AI có thể read |
| **Prompts** | Reusable prompt templates |
| **Transport** | stdio hoặc HTTP |

---

## Quick Start (TypeScript)

### 1. Project Setup
```bash
mkdir my-mcp-server
cd my-mcp-server
npm init -y
npm install @modelcontextprotocol/sdk zod
npm install -D typescript @types/node tsx
```

### 2. TypeScript Config
```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "outDir": "./dist",
    "strict": true,
    "esModuleInterop": true
  },
  "include": ["src/**/*"]
}
```

### 3. Package.json Scripts
```json
{
  "type": "module",
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js",
    "dev": "tsx src/index.ts"
  },
  "bin": {
    "my-mcp-server": "./dist/index.js"
  }
}
```

### 4. Basic Server
```typescript
// src/index.ts
#!/usr/bin/env node

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

// Create server
const server = new McpServer({
  name: "my-mcp-server",
  version: "1.0.0",
});

// Define tools
server.tool(
  "hello",
  "Say hello to someone",
  {
    name: z.string().describe("Name to greet"),
  },
  async ({ name }) => {
    return {
      content: [
        {
          type: "text",
          text: `Hello, ${name}!`,
        },
      ],
    };
  }
);

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("MCP server running on stdio");
}

main().catch(console.error);
```

---

## Tool Patterns

### Simple Tool
```typescript
server.tool(
  "get_weather",
  "Get current weather for a city",
  {
    city: z.string().describe("City name"),
  },
  async ({ city }) => {
    const weather = await fetchWeather(city);
    return {
      content: [{ type: "text", text: JSON.stringify(weather) }],
    };
  }
);
```

### Tool with Multiple Parameters
```typescript
server.tool(
  "search",
  "Search for items with filters",
  {
    query: z.string().describe("Search query"),
    limit: z.number().optional().default(10).describe("Max results"),
    category: z.enum(["all", "products", "users"]).optional(),
  },
  async ({ query, limit, category }) => {
    const results = await searchService.search(query, { limit, category });
    return {
      content: [{ type: "text", text: JSON.stringify(results) }],
    };
  }
);
```

### Tool with Error Handling
```typescript
server.tool(
  "create_item",
  "Create a new item",
  {
    name: z.string().min(1).describe("Item name"),
    price: z.number().positive().describe("Item price"),
  },
  async ({ name, price }) => {
    try {
      const item = await db.create({ name, price });
      return {
        content: [{ type: "text", text: `Created item: ${item.id}` }],
      };
    } catch (error) {
      return {
        content: [{ type: "text", text: `Error: ${error.message}` }],
        isError: true,
      };
    }
  }
);
```

---

## Resource Patterns

### Static Resource
```typescript
server.resource(
  "config",
  "config://app",
  async () => ({
    contents: [
      {
        uri: "config://app",
        mimeType: "application/json",
        text: JSON.stringify({ version: "1.0", env: "prod" }),
      },
    ],
  })
);
```

### Dynamic Resource List
```typescript
server.resource(
  "users",
  "users://{id}",
  async (uri) => {
    const id = uri.pathname.replace("/", "");
    const user = await db.getUser(id);
    return {
      contents: [
        {
          uri: uri.href,
          mimeType: "application/json",
          text: JSON.stringify(user),
        },
      ],
    };
  }
);
```

---

## Prompt Templates

```typescript
server.prompt(
  "analyze_code",
  "Analyze code quality",
  {
    code: z.string().describe("Code to analyze"),
    language: z.string().describe("Programming language"),
  },
  async ({ code, language }) => ({
    messages: [
      {
        role: "user",
        content: {
          type: "text",
          text: `Analyze this ${language} code for quality issues:\n\n\`\`\`${language}\n${code}\n\`\`\``,
        },
      },
    ],
  })
);
```

---

## Testing

### Manual Testing
```bash
# Run server
npm run dev

# In another terminal, test with example input
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | npm run dev
```

### Integration with Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["/absolute/path/to/dist/index.js"]
    }
  }
}
```

---

## Common Integrations

### Database (SQLite)
```typescript
import Database from "better-sqlite3";

const db = new Database("app.db");

server.tool("query", "Run SQL query", {
  sql: z.string(),
}, async ({ sql }) => {
  // Only allow SELECT
  if (!sql.trim().toLowerCase().startsWith("select")) {
    return { content: [{ type: "text", text: "Only SELECT allowed" }], isError: true };
  }
  const results = db.prepare(sql).all();
  return { content: [{ type: "text", text: JSON.stringify(results) }] };
});
```

### REST API
```typescript
server.tool("fetch_api", "Fetch from API", {
  endpoint: z.string(),
}, async ({ endpoint }) => {
  const response = await fetch(`https://api.example.com${endpoint}`, {
    headers: { Authorization: `Bearer ${process.env.API_KEY}` },
  });
  const data = await response.json();
  return { content: [{ type: "text", text: JSON.stringify(data) }] };
});
```

### File System
```typescript
import { readFile, writeFile } from "fs/promises";

server.tool("read_file", "Read a file", {
  path: z.string(),
}, async ({ path }) => {
  // Validate path is in allowed directory
  const content = await readFile(path, "utf-8");
  return { content: [{ type: "text", text: content }] };
});
```

---

## Best Practices

### Security
- [ ] Validate all inputs với Zod
- [ ] Sanitize file paths
- [ ] Use environment variables for secrets
- [ ] Limit scope of operations
- [ ] Log all actions

### Error Handling
- [ ] Return meaningful error messages
- [ ] Use `isError: true` for failures
- [ ] Don't expose internal details
- [ ] Handle timeouts

### Performance
- [ ] Cache when appropriate
- [ ] Set reasonable timeouts
- [ ] Batch operations when possible
- [ ] Stream large responses

### Design
- [ ] Clear, descriptive tool names
- [ ] Detailed parameter descriptions
- [ ] Consistent response formats
- [ ] Document all tools

---

## Deployment

### npm Package
```bash
npm login
npm publish
```

### Docker
```dockerfile
FROM node:20-slim
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY dist ./dist
CMD ["node", "dist/index.js"]
```

### Claude Desktop Config
```json
{
  "mcpServers": {
    "my-server": {
      "command": "npx",
      "args": ["-y", "my-published-mcp-server"],
      "env": {
        "API_KEY": "xxx"
      }
    }
  }
}
```

---

## Debugging

### Enable Logging
```typescript
server.onerror = (error) => {
  console.error("[MCP Error]", error);
};
```

### Check Claude Desktop Logs
```bash
# macOS
tail -f ~/Library/Logs/Claude/mcp*.log
```

---

## Resources

| Resource | URL |
|----------|-----|
| MCP Spec | modelcontextprotocol.io |
| SDK Docs | github.com/modelcontextprotocol/typescript-sdk |
| Examples | github.com/modelcontextprotocol/servers |
