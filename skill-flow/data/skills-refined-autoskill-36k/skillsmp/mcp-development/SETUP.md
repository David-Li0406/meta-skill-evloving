# MCP Project Setup Guide

## Quick Start

```bash
# Create project
mkdir mcp-project && cd mcp-project
npm init -y

# Install dependencies
npm install @modelcontextprotocol/sdk zod
npm install -D typescript @types/node

# Initialize TypeScript
npx tsc --init

# Create structure
mkdir -p src/tools src/db src/utils
```

## Server Entry Point Template

**src/index.ts**
```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "mcp-server-name",
  version: "1.0.0",
});

// Health check tool
server.registerTool(
  "ping",
  {
    description: "Health check - returns pong with timestamp",
    inputSchema: z.object({}),
  },
  async () => ({
    content: [{
      type: "text",
      text: JSON.stringify({
        status: "ok",
        timestamp: new Date().toISOString()
      })
    }],
  })
);

// Start server
const transport = new StdioServerTransport();
server.connect(transport).catch((err) => {
  console.error("[MCP] Server error:", err);
  process.exit(1);
});

console.error("[MCP] Server started");
```

## Environment Variables

**.env.example**
```env
# Database
SQL_SERVER=localhost
SQL_DATABASE=mydb
SQL_USER=sa
SQL_PASSWORD=

# Server
LOG_LEVEL=info
```

**.gitignore**
```
node_modules/
build/
.env
*.log
.DS_Store
```

## Claude Desktop Configuration

**Location**: `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)

```json
{
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["/absolute/path/to/build/index.js"],
      "env": {
        "SQL_SERVER": "localhost",
        "SQL_DATABASE": "mydb",
        "SQL_USER": "sa",
        "SQL_PASSWORD": "password"
      }
    }
  }
}
```

## Build and Test

```bash
# Build
npm run build

# Test manually
node build/index.js

# Test with MCP Inspector
npx @modelcontextprotocol/inspector
```
