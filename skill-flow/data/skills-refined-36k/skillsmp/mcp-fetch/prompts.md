# Prompts

This MCP server provides the following prompts:

## fetch

Fetch a URL and extract its contents as markdown.

**Arguments:**
- `url` (required): URL to fetch

**Usage:**

```bash
node ./scripts/mcp-caller.mjs prompt fetch '{"url": "https://example.com"}'
```

This prompt provides a convenient way to fetch and extract web content as markdown.
