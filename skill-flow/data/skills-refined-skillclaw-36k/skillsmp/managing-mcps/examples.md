# MCP Server Examples

Reference implementations and patterns from official and community MCP servers.

## Official Examples

### Filesystem Server

**Repository**: https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem

**Capabilities**: File operations (read, write, list, search)

**Key Features:**
- Path validation and security
- Async file operations
- Directory traversal
- File search with patterns

**Tool Examples:**
```typescript
{
  name: "read_file",
  description: "Read complete contents of a file",
  inputSchema: {
    type: "object",
    properties: {
      path: {
        type: "string",
        description: "Path to file"
      }
    },
    required: ["path"]
  }
}

{
  name: "write_file",
  description: "Write content to a file",
  inputSchema: {
    type: "object",
    properties: {
      path: {
        type: "string",
        description: "Path to file"
      },
      content: {
        type: "string",
        description: "Content to write"
      }
    },
    required: ["path", "content"]
  }
}

{
  name: "search_files",
  description: "Search for files matching pattern",
  inputSchema: {
    type: "object",
    properties: {
      path: {
        type: "string",
        description: "Base directory"
      },
      pattern: {
        type: "string",
        description: "Glob pattern"
      }
    },
    required: ["path", "pattern"]
  }
}
```

**Configuration:**
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/allowed/path"]
    }
  }
}
```

**Security Pattern:**
```typescript
// Validate path within allowed directory
const allowedDir = process.argv[2];

function validatePath(requestedPath: string): string {
  const normalized = path.normalize(requestedPath);
  const absolute = path.resolve(allowedDir, normalized);

  if (!absolute.startsWith(allowedDir)) {
    throw new Error("Access denied");
  }

  return absolute;
}
```

### GitHub Server

**Repository**: https://github.com/modelcontextprotocol/servers/tree/main/src/github

**Capabilities**: GitHub API operations, repository management

**Key Features:**
- OAuth authentication
- Issue/PR management
- Repository operations
- Search functionality

**Tool Examples:**
```typescript
{
  name: "create_issue",
  description: "Create a new issue in a repository",
  inputSchema: {
    type: "object",
    properties: {
      owner: {
        type: "string",
        description: "Repository owner"
      },
      repo: {
        type: "string",
        description: "Repository name"
      },
      title: {
        type: "string",
        description: "Issue title"
      },
      body: {
        type: "string",
        description: "Issue description"
      }
    },
    required: ["owner", "repo", "title"]
  }
}

{
  name: "search_code",
  description: "Search code across repositories",
  inputSchema: {
    type: "object",
    properties: {
      query: {
        type: "string",
        description: "Search query"
      },
      owner: {
        type: "string",
        description: "Filter by owner"
      }
    },
    required: ["query"]
  }
}
```

**Configuration:**
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

**Authentication Pattern:**
```typescript
import { Octokit } from "@octokit/rest";

const octokit = new Octokit({
  auth: process.env.GITHUB_TOKEN
});

async function createIssue(owner: string, repo: string, title: string, body: string) {
  const response = await octokit.rest.issues.create({
    owner,
    repo,
    title,
    body
  });

  return {
    content: [{
      type: "text",
      text: `Created issue #${response.data.number}: ${response.data.html_url}`
    }]
  };
}
```

### Slack Server

**Repository**: https://github.com/modelcontextprotocol/servers/tree/main/src/slack

**Capabilities**: Slack messaging, channel management, user operations

**Key Features:**
- Bot token authentication
- Message sending
- Channel listing
- User lookups

**Tool Examples:**
```typescript
{
  name: "send_message",
  description: "Send a message to a Slack channel",
  inputSchema: {
    type: "object",
    properties: {
      channel: {
        type: "string",
        description: "Channel ID or name"
      },
      text: {
        type: "string",
        description: "Message text"
      },
      thread_ts: {
        type: "string",
        description: "Thread timestamp for replies"
      }
    },
    required: ["channel", "text"]
  }
}

{
  name: "list_channels",
  description: "List all Slack channels",
  inputSchema: {
    type: "object",
    properties: {
      types: {
        type: "string",
        description: "Channel types (public_channel, private_channel)",
        default: "public_channel"
      }
    }
  }
}
```

**Configuration:**
```json
{
  "mcpServers": {
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}"
      }
    }
  }
}
```

**Rate Limiting Pattern:**
```typescript
import { WebClient } from "@slack/web-api";

const client = new WebClient(process.env.SLACK_BOT_TOKEN, {
  retryConfig: {
    retries: 3,
    factor: 2
  }
});

// Slack has rate limits, SDK handles automatically
async function sendMessage(channel: string, text: string) {
  try {
    const result = await client.chat.postMessage({
      channel,
      text
    });

    return {
      content: [{
        type: "text",
        text: `Message sent: ${result.ts}`
      }]
    };
  } catch (error) {
    if (error.code === "rate_limited") {
      throw new Error("Rate limit exceeded, retry after delay");
    }
    throw error;
  }
}
```

### Google Drive Server

**Repository**: https://github.com/modelcontextprotocol/servers/tree/main/src/gdrive

**Capabilities**: Google Drive file operations

**Key Features:**
- OAuth 2.0 authentication
- File upload/download
- Folder management
- Search functionality

**Tool Examples:**
```typescript
{
  name: "upload_file",
  description: "Upload file to Google Drive",
  inputSchema: {
    type: "object",
    properties: {
      name: {
        type: "string",
        description: "File name"
      },
      content: {
        type: "string",
        description: "File content"
      },
      folderId: {
        type: "string",
        description: "Parent folder ID"
      }
    },
    required: ["name", "content"]
  }
}

{
  name: "search_files",
  description: "Search files in Google Drive",
  inputSchema: {
    type: "object",
    properties: {
      query: {
        type: "string",
        description: "Search query"
      },
      mimeType: {
        type: "string",
        description: "Filter by MIME type"
      }
    },
    required: ["query"]
  }
}
```

**Configuration:**
```json
{
  "mcpServers": {
    "gdrive": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-gdrive"],
      "env": {
        "GOOGLE_CLIENT_ID": "${GOOGLE_CLIENT_ID}",
        "GOOGLE_CLIENT_SECRET": "${GOOGLE_CLIENT_SECRET}",
        "GOOGLE_REFRESH_TOKEN": "${GOOGLE_REFRESH_TOKEN}"
      }
    }
  }
}
```

## AWS MCP Servers

**Repository**: https://github.com/awslabs/mcp

### AWS Bedrock Agent Core MCP Server

**Repository**: https://github.com/awslabs/amazon-bedrock-agent-samples/tree/main/examples/amazon-bedrock-agentcore-mcp-server

**Capabilities**: AWS Bedrock integration with memory, runtime, and gateway services

**Architecture Pattern:**

This server demonstrates production-ready MCP architecture with:
- **Modular design**: Separate modules for memory, runtime, gateway, docs
- **FastMCP framework**: Uses `mcp.server.fastmcp.FastMCP` for rapid development
- **Type safety**: Python type hints throughout
- **AWS integration**: Bedrock Agent Core SDK integration

**Code Structure:**
```
amazon-bedrock-agentcore-mcp-server/
├── server.py           # Main server entry point
├── memory.py           # Memory management module
├── runtime.py          # Runtime execution module
├── gateway.py          # API gateway module
├── docs.py             # Documentation module
└── requirements.txt    # Python dependencies
```

**Tool Implementation Pattern (from runtime.py):**
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("bedrock-runtime")

@mcp.tool()
def invoke_agent(
    agent_id: str,
    session_id: str,
    prompt: str
) -> dict:
    """Invoke a Bedrock agent with the given prompt."""
    # Implementation here
    return {
        "agent_id": agent_id,
        "response": response_text,
        "trace": trace_data
    }
```

**Key Patterns:**
1. **Decorator-based tool registration**: `@mcp.tool()` makes function an MCP tool
2. **Type hints**: Parameters and return types clearly defined
3. **Docstrings**: Become tool descriptions in MCP protocol
4. **Structured returns**: Dictionary responses with clear keys
5. **Error handling**: Try-except blocks with informative error messages

**Server Startup:**
```python
def main():
    mcp.run()

if __name__ == "__main__":
    main()
```

**Configuration:**
```json
{
  "mcpServers": {
    "bedrock": {
      "command": "python",
      "args": ["server.py"],
      "env": {
        "AWS_REGION": "us-east-1",
        "AWS_ACCESS_KEY_ID": "${AWS_ACCESS_KEY_ID}",
        "AWS_SECRET_ACCESS_KEY": "${AWS_SECRET_ACCESS_KEY}"
      }
    }
  }
}
```

**Benefits of This Pattern:**
- Clean separation of concerns (modules per domain)
- FastMCP handles protocol complexity
- Easy to add new tools (just add decorated functions)
- Type safety catches errors early
- AWS SDK integration straightforward

### AWS Knowledge Base Server

**Capabilities**: Query AWS documentation and knowledge bases

**Tool Examples:**
```typescript
{
  name: "query_knowledge_base",
  description: "Query AWS Knowledge Base",
  inputSchema: {
    type: "object",
    properties: {
      knowledgeBaseId: {
        type: "string",
        description: "Knowledge Base ID"
      },
      query: {
        type: "string",
        description: "Search query"
      },
      maxResults: {
        type: "number",
        description: "Maximum results",
        default: 5
      }
    },
    required: ["knowledgeBaseId", "query"]
  }
}
```

**Configuration:**
```json
{
  "mcpServers": {
    "aws-kb": {
      "command": "npx",
      "args": ["-y", "@aws/aws-kb-retrieval-mcp-server"],
      "env": {
        "AWS_REGION": "us-east-1",
        "AWS_ACCESS_KEY_ID": "${AWS_ACCESS_KEY_ID}",
        "AWS_SECRET_ACCESS_KEY": "${AWS_SECRET_ACCESS_KEY}"
      }
    }
  }
}
```

### AWS Bedrock Server

**Capabilities**: Access AWS Bedrock LLMs

**Tool Examples:**
```typescript
{
  name: "invoke_model",
  description: "Invoke AWS Bedrock model",
  inputSchema: {
    type: "object",
    properties: {
      modelId: {
        type: "string",
        description: "Bedrock model ID"
      },
      prompt: {
        type: "string",
        description: "Input prompt"
      },
      maxTokens: {
        type: "number",
        description: "Maximum tokens"
      }
    },
    required: ["modelId", "prompt"]
  }
}
```

## Microsoft MCP Servers

**Repository**: https://github.com/microsoft/mcp

### Playwright MCP

**Repository**: https://github.com/microsoft/playwright-mcp

**Capabilities**: Browser automation and testing

**Tool Examples:**
```typescript
{
  name: "navigate",
  description: "Navigate to URL",
  inputSchema: {
    type: "object",
    properties: {
      url: {
        type: "string",
        description: "URL to navigate to"
      }
    },
    required: ["url"]
  }
}

{
  name: "screenshot",
  description: "Take screenshot of page",
  inputSchema: {
    type: "object",
    properties: {
      fullPage: {
        type: "boolean",
        description: "Capture full page",
        default: false
      }
    }
  }
}

{
  name: "execute_script",
  description: "Execute JavaScript in page",
  inputSchema: {
    type: "object",
    properties: {
      script: {
        type: "string",
        description: "JavaScript code"
      }
    },
    required: ["script"]
  }
}
```

**Configuration:**
```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp"]
    }
  }
}
```

**Browser Automation Pattern:**
```typescript
import { chromium } from "playwright";

let browser: Browser;
let page: Page;

async function initBrowser() {
  browser = await chromium.launch();
  page = await browser.newPage();
}

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  if (!page) await initBrowser();

  if (name === "navigate") {
    await page.goto(args.url);
    return {
      content: [{ type: "text", text: `Navigated to ${args.url}` }]
    };
  }

  if (name === "screenshot") {
    const screenshot = await page.screenshot({
      fullPage: args.fullPage
    });

    return {
      content: [{
        type: "image",
        data: screenshot.toString("base64"),
        mimeType: "image/png"
      }]
    };
  }
});

// Cleanup on shutdown
process.on("SIGTERM", async () => {
  await browser?.close();
});
```

## Community Examples

### Database Server

**Pattern**: Generic database query server

**Tool Examples:**
```typescript
{
  name: "query",
  description: "Execute SQL query",
  inputSchema: {
    type: "object",
    properties: {
      sql: {
        type: "string",
        description: "SQL query (SELECT only)"
      },
      params: {
        type: "array",
        description: "Query parameters",
        items: { type: "string" }
      }
    },
    required: ["sql"]
  }
}

{
  name: "list_tables",
  description: "List all tables",
  inputSchema: {
    type: "object",
    properties: {}
  }
}
```

**Security Pattern:**
```typescript
import { Pool } from "pg";

const pool = new Pool({
  connectionString: process.env.DATABASE_URL
});

async function query(sql: string, params: any[] = []) {
  // Validate SELECT-only
  const normalized = sql.trim().toLowerCase();
  if (!normalized.startsWith("select")) {
    throw new Error("Only SELECT queries allowed");
  }

  // Prevent multiple statements
  if (sql.includes(";") && !sql.trim().endsWith(";")) {
    throw new Error("Multiple statements not allowed");
  }

  // Execute with timeout
  const client = await pool.connect();
  try {
    await client.query("SET statement_timeout = 30000");
    const result = await client.query(sql, params);

    return {
      content: [{
        type: "text",
        text: JSON.stringify(result.rows, null, 2)
      }]
    };
  } finally {
    client.release();
  }
}
```

### HTTP API Server

**Pattern**: Generic HTTP API client

**Tool Examples:**
```typescript
{
  name: "get",
  description: "HTTP GET request",
  inputSchema: {
    type: "object",
    properties: {
      url: {
        type: "string",
        description: "URL"
      },
      headers: {
        type: "object",
        description: "Request headers"
      }
    },
    required: ["url"]
  }
}

{
  name: "post",
  description: "HTTP POST request",
  inputSchema: {
    type: "object",
    properties: {
      url: {
        type: "string",
        description: "URL"
      },
      body: {
        type: "object",
        description: "Request body"
      },
      headers: {
        type: "object",
        description: "Request headers"
      }
    },
    required: ["url", "body"]
  }
}
```

**Rate Limiting and Caching Pattern:**
```typescript
import { RateLimiter } from "limiter";

const limiter = new RateLimiter({
  tokensPerInterval: 10,
  interval: "minute"
});

const cache = new Map<string, { data: any; timestamp: number }>();
const CACHE_TTL = 60000;

async function get(url: string, headers: Record<string, string> = {}) {
  // Check cache
  const cached = cache.get(url);
  if (cached && Date.now() - cached.timestamp < CACHE_TTL) {
    return {
      content: [{
        type: "text",
        text: JSON.stringify(cached.data)
      }]
    };
  }

  // Rate limit
  await limiter.removeTokens(1);

  // Fetch
  const response = await fetch(url, { headers });
  const data = await response.json();

  // Cache
  cache.set(url, { data, timestamp: Date.now() });

  return {
    content: [{
      type: "text",
      text: JSON.stringify(data, null, 2)
    }]
  };
}
```

### RSS Feed Server

**Pattern**: RSS feed reader

**Resource Examples:**
```typescript
server.setRequestHandler(ListResourcesRequestSchema, async () => ({
  resources: [
    {
      uri: "rss://feeds.example.com/news",
      name: "News Feed",
      mimeType: "application/rss+xml"
    }
  ]
}));

server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const { uri } = request.params;
  const feedUrl = uri.replace("rss://", "https://");

  const response = await fetch(feedUrl);
  const xml = await response.text();

  return {
    contents: [{
      uri,
      mimeType: "application/rss+xml",
      text: xml
    }]
  };
});
```

**Resource Subscription Pattern:**
```typescript
const subscriptions = new Map<string, Set<string>>();

server.setRequestHandler(SubscribeRequestSchema, async (request) => {
  const { uri } = request.params;

  if (!subscriptions.has(uri)) {
    subscriptions.set(uri, new Set());

    // Poll for changes
    setInterval(async () => {
      const changed = await checkForChanges(uri);
      if (changed) {
        server.notification({
          method: "notifications/resources/updated",
          params: { uri }
        });
      }
    }, 60000);
  }

  return {};
});
```

## Common Patterns

### Tool Result Formatting

**Text result:**
```typescript
return {
  content: [{ type: "text", text: "Result message" }]
};
```

**Structured data:**
```typescript
return {
  content: [{
    type: "text",
    text: JSON.stringify({ key: "value" }, null, 2)
  }]
};
```

**Image result:**
```typescript
return {
  content: [{
    type: "image",
    data: base64ImageData,
    mimeType: "image/png"
  }]
};
```

**Resource reference:**
```typescript
return {
  content: [{
    type: "resource",
    uri: "file:///path/to/result.json",
    mimeType: "application/json"
  }]
};
```

**Error result:**
```typescript
return {
  content: [{ type: "text", text: "Error message" }],
  isError: true
};
```

### Progress Reporting

```typescript
async function longOperation(progressToken?: string) {
  const steps = 100;

  for (let i = 0; i < steps; i++) {
    await doWork();

    if (progressToken) {
      server.notification({
        method: "notifications/progress",
        params: {
          progressToken,
          progress: i,
          total: steps
        }
      });
    }
  }
}
```

### Cancellation Handling

```typescript
const activeOperations = new Map<string, AbortController>();

server.setNotificationHandler("notifications/cancelled", (notification) => {
  const { requestId } = notification.params;
  const controller = activeOperations.get(requestId);

  if (controller) {
    controller.abort();
    activeOperations.delete(requestId);
  }
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const controller = new AbortController();
  activeOperations.set(request.id, controller);

  try {
    const result = await fetch(url, { signal: controller.signal });
    return processResult(result);
  } finally {
    activeOperations.delete(request.id);
  }
});
```

## FastMCP Quick Start Pattern

Based on AWS Bedrock example, here's a minimal MCP server template:

```python
#!/usr/bin/env python3
from mcp.server.fastmcp import FastMCP

# Initialize server with name
mcp = FastMCP("my-server")

# Define tools using decorator
@mcp.tool()
def example_tool(param: str) -> dict:
    """
    Tool description shown to Claude.

    Args:
        param: Parameter description

    Returns:
        Dictionary with results
    """
    # Implementation
    result = f"Processed: {param}"
    return {"result": result, "status": "success"}

# Add more tools as needed
@mcp.tool()
def another_tool(value: int) -> dict:
    """Another tool description."""
    return {"value": value * 2}

# Entry point
def main():
    mcp.run()

if __name__ == "__main__":
    main()
```

**Key Advantages:**
- Minimal boilerplate (FastMCP handles protocol)
- Decorator pattern for tool registration
- Type hints provide automatic validation
- Docstrings become tool descriptions
- Quick development iteration

**Use FastMCP when:**
- Building Python-based MCP servers
- Want rapid prototyping
- Need production-ready framework
- Prefer decorator pattern

## Reference Links

**Official Examples:**
- https://github.com/modelcontextprotocol/servers
- https://github.com/awslabs/mcp
- https://github.com/awslabs/amazon-bedrock-agent-samples (AWS Bedrock MCP examples)
- https://github.com/microsoft/mcp
- https://github.com/microsoft/playwright-mcp

**Community Examples:**
- https://github.com/punkpeye/awesome-mcp-servers

**Tutorial:**
- https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/tutorials/building-mcp-with-llms.mdx

**FastMCP Documentation:**
- https://github.com/modelcontextprotocol/python-sdk (includes FastMCP)
