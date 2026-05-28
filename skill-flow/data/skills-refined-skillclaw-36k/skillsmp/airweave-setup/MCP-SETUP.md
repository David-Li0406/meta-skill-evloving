# Airweave MCP Server Setup

Configure the Airweave MCP server to enable AI assistants to search your data.

## Prerequisites

1. An Airweave account with API key
2. A collection with synced data
3. Node.js 18+ (for local mode)

## Deployment Modes

### 1. Local Mode (Claude Desktop, Cursor)

For desktop AI assistants that run MCP servers locally.

#### Installation via npx (Recommended)

No installation required—runs directly:

```bash
npx airweave-mcp-search
```

#### Configuration for Cursor

Create or edit `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "airweave-search": {
      "command": "npx",
      "args": ["airweave-mcp-search"],
      "env": {
        "AIRWEAVE_API_KEY": "your-api-key-here",
        "AIRWEAVE_COLLECTION": "your-collection-readable-id",
        "AIRWEAVE_BASE_URL": "https://api.airweave.ai"
      }
    }
  }
}
```

#### Configuration for Claude Desktop

Add to `~/.config/claude/claude_desktop_config.json` (macOS/Linux) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "airweave-search": {
      "command": "npx",
      "args": ["airweave-mcp-search"],
      "env": {
        "AIRWEAVE_API_KEY": "your-api-key-here",
        "AIRWEAVE_COLLECTION": "your-collection-readable-id",
        "AIRWEAVE_BASE_URL": "https://api.airweave.ai"
      }
    }
  }
}
```

#### Local Development (Self-Hosted Airweave)

For testing with a local Airweave instance:

```json
{
  "mcpServers": {
    "airweave-search": {
      "command": "node",
      "args": ["/path/to/airweave/mcp/build/index.js"],
      "env": {
        "AIRWEAVE_API_KEY": "your-local-api-key",
        "AIRWEAVE_COLLECTION": "your-collection-id",
        "AIRWEAVE_BASE_URL": "http://localhost:8001"
      }
    }
  }
}
```

### 2. Hosted Mode (Cloud AI Platforms)

For cloud-based AI platforms like OpenAI Agent Builder.

- **URL**: `https://mcp.airweave.ai`
- **Transport**: Streamable HTTP (MCP 2025-03-26)

Pass your API key via headers:
- `Authorization: Bearer YOUR_API_KEY`
- or `X-API-Key: YOUR_API_KEY`

## Available Tools

Once configured, the MCP server exposes these tools:

### `search-{collection}`

Search within your Airweave collection.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | string | (required) | Search query text |
| `response_type` | "raw" \| "completion" | "raw" | Return results or AI answer |
| `limit` | number | 100 | Max results (1-1000) |
| `offset` | number | 0 | Skip results for pagination |
| `recency_bias` | number | - | 0-1, favor recent (1=most recent) |
| `score_threshold` | number | - | 0-1, minimum similarity score (deprecated, may be ignored) |
| `search_method` | string | "hybrid" | "hybrid", "neural", "keyword" |
| `expansion_strategy` | string | "auto" | "auto", "llm", "no_expansion" |
| `enable_reranking` | boolean | true | AI reranking for relevance |
| `enable_query_interpretation` | boolean | true | Extract filters from query |

**Example Usage:**

The AI assistant can call the tool like this:

```
search-my-collection({
  query: "customer complaints about shipping delays",
  limit: 10,
  recency_bias: 0.7
})
```

### `get-config`

Shows current server configuration.

```
get-config()
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `AIRWEAVE_API_KEY` | Yes | - | Your Airweave API key |
| `AIRWEAVE_COLLECTION` | Yes | - | Collection readable ID |
| `AIRWEAVE_BASE_URL` | No | `https://api.airweave.ai` | API base URL |

## Usage Examples

Once the MCP server is configured, you can ask your AI assistant:

**Basic Searches:**
- "Search for customer feedback about pricing"
- "Find documents related to API documentation"
- "Look up information about data privacy policies"

**With Parameters:**
- "Search for bug reports from the last week" (uses recency_bias)
- "Find high-quality results about authentication" (uses enable_reranking)
- "Give me a summary of our refund policy" (uses response_type: completion)

**Natural Language Mapping:**
- "Find the first 5 results" → `limit: 5`
- "Show me results 11-20" → `limit: 10, offset: 10`
- "Find the most recent documents" → `recency_bias: 0.8`
- "Use keyword search" → `search_method: "keyword"`

## Troubleshooting

### "Error: AIRWEAVE_API_KEY environment variable is required"

Ensure the API key is set in your MCP configuration. Verify the key is valid at https://app.airweave.ai.

### "Error: AIRWEAVE_COLLECTION environment variable is required"

Set the collection's readable ID (find it in your Airweave dashboard or via the API).

### "Airweave API error (404)"

- Verify the collection ID is correct
- Check the collection exists and you have access

### "Airweave API error (401)"

- Check your API key is valid and not expired
- Ensure the API key has permissions for this collection

### MCP Server Not Appearing

1. Restart your AI client (Cursor/Claude Desktop)
2. Check the MCP config file for JSON syntax errors
3. Verify the npx command works: `npx airweave-mcp-search --version`

### Debug Mode

The server logs to stderr. Check logs for:
- "Airweave MCP Search Server started"
- "Collection: your-collection-id"
- "Base URL: https://api.airweave.ai"

## Multiple Collections

To search multiple collections, configure multiple MCP servers:

```json
{
  "mcpServers": {
    "airweave-engineering": {
      "command": "npx",
      "args": ["airweave-mcp-search"],
      "env": {
        "AIRWEAVE_API_KEY": "your-api-key",
        "AIRWEAVE_COLLECTION": "engineering-docs-abc123"
      }
    },
    "airweave-support": {
      "command": "npx",
      "args": ["airweave-mcp-search"],
      "env": {
        "AIRWEAVE_API_KEY": "your-api-key",
        "AIRWEAVE_COLLECTION": "support-tickets-xyz789"
      }
    }
  }
}
```

Each collection will have its own search tool: `search-engineering-docs-abc123` and `search-support-tickets-xyz789`.

