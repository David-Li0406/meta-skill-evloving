---
name: mcp-builder
description: Build MCP servers for integrating external APIs with AI agents
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: development
---

# MCP Server Builder

Create high-quality MCP (Model Context Protocol) servers that enable AI agents to interact with external services through well-designed tools.

## When to Use

- Building integrations for external APIs
- Creating tools for AI agent workflows
- Connecting LLMs to databases, services, or custom systems
- Extending Claude/OpenCode with new capabilities

## Key Principles

### Agent-Centric Design

1. **Build for workflows, not endpoints** - Group related operations
2. **Optimize for context windows** - Return concise, actionable data
3. **Actionable errors** - Tell the agent what to do next
4. **Natural subdivisions** - Match how tasks are mentally structured
5. **Evaluation-driven** - Test with real agent interactions

## Project Structure

### Python (FastMCP)

```
my-mcp-server/
├── pyproject.toml
├── src/
│   └── my_mcp_server/
│       ├── __init__.py
│       ├── server.py      # Main MCP server
│       ├── tools/         # Tool implementations
│       ├── utils/         # Shared utilities
│       └── schemas/       # Pydantic models
└── tests/
```

### TypeScript

```
my-mcp-server/
├── package.json
├── tsconfig.json
├── src/
│   ├── index.ts          # Main entry
│   ├── server.ts         # MCP server setup
│   ├── tools/            # Tool implementations
│   ├── utils/            # Shared utilities
│   └── types/            # Zod schemas
└── tests/
```

## Implementation Process

### Phase 1: Research & Plan

1. **Study the API**
   - Authentication requirements
   - Rate limits and pagination
   - Error response formats
   - Available endpoints

2. **Plan Tools**
   - Which operations are most useful for agents?
   - What workflows will agents perform?
   - What data format is most actionable?

### Phase 2: Build Core Infrastructure

```python
# Python example - shared utilities
from mcp.server import Server
from mcp.types import Tool, TextContent

class APIClient:
    """Handles auth, rate limiting, errors"""
    
    async def request(self, endpoint: str, **kwargs):
        # Retry logic, error handling
        pass

def format_response(data: dict) -> str:
    """Convert API response to agent-friendly format"""
    # Markdown or structured text
    pass
```

### Phase 3: Implement Tools

```python
from pydantic import BaseModel, Field

class SearchParams(BaseModel):
    """Input schema with validation"""
    query: str = Field(..., description="Search query")
    limit: int = Field(10, ge=1, le=100)

@server.tool()
async def search_items(params: SearchParams) -> str:
    """
    Search for items in the database.
    
    Use this when you need to find items matching specific criteria.
    Returns a list of matching items with their IDs and summaries.
    """
    results = await client.search(params.query, params.limit)
    return format_as_markdown(results)
```

### Phase 4: Add Tool Annotations

```python
@server.tool(
    annotations={
        "readOnlyHint": True,      # Doesn't modify data
        "destructiveHint": False,  # Safe operation
        "idempotentHint": True,    # Same result if repeated
        "openWorldHint": False     # Operates on known data
    }
)
async def get_item(item_id: str) -> str:
    ...
```

## Best Practices

### Input Design

| Do | Don't |
|----|-------|
| Use Pydantic/Zod schemas | Accept raw dicts |
| Add Field descriptions | Leave params undocumented |
| Set sensible defaults | Require all params |
| Validate at schema level | Validate in handler |

### Output Design

| Do | Don't |
|----|-------|
| Return markdown for readability | Return raw JSON blobs |
| Include actionable next steps | Leave agent guessing |
| Summarize large datasets | Dump everything |
| Format for quick scanning | Wall of text |

### Error Handling

```python
class MCPError(Exception):
    """Base error with agent-friendly message"""
    
    def __init__(self, message: str, suggestion: str = None):
        self.message = message
        self.suggestion = suggestion

# Usage
raise MCPError(
    "Item not found",
    suggestion="Try searching with `search_items` first"
)
```

## Testing

MCP servers run as long-lived processes. Test approaches:

1. **Unit tests** - Test tools in isolation
2. **Integration tests** - Run server, make tool calls
3. **Agent evaluation** - Real agent interactions

```bash
# Run server for testing
python -m my_mcp_server

# In another terminal, use MCP client to test
```

## Quality Checklist

- [ ] All tools have comprehensive docstrings
- [ ] Input schemas validate edge cases
- [ ] Errors include recovery suggestions
- [ ] Outputs are concise and scannable
- [ ] Rate limits are respected
- [ ] Authentication is secure
- [ ] Pagination is handled properly
- [ ] Tool annotations are accurate
