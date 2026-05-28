---
name: mcp-builder
description: Guide for creating MCP (Model Context Protocol) servers in TypeScript or Python. Use when building MCP servers to integrate external APIs or services.
---

# MCP Server Development Guide

## Overview

Create MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. The quality of an MCP server is measured by how well it enables LLMs to accomplish real-world tasks.

---

## High-Level Workflow

Creating a high-quality MCP server involves four main phases:

### Phase 1: Deep Research and Planning

#### 1.1 Understand Modern MCP Design

**API Coverage vs. Workflow Tools:**
Balance comprehensive API endpoint coverage with specialized workflow tools. Workflow tools can be more convenient for specific tasks, while comprehensive coverage gives agents flexibility to compose operations. When uncertain, prioritize comprehensive API coverage.

**Tool Naming and Discoverability:**
Clear, descriptive tool names help agents find the right tools quickly. Use consistent prefixes (e.g., `github_create_issue`, `github_list_repos`) and action-oriented naming.

**Context Management:**
Agents benefit from concise tool descriptions and the ability to filter/paginate results. Design tools that return focused, relevant data.

**Actionable Error Messages:**
Error messages should guide agents toward solutions with specific suggestions and next steps.

#### 1.2 Study MCP Protocol Documentation

**Navigate the MCP specification:**

Start with the sitemap: `https://modelcontextprotocol.io/sitemap.xml`

Then fetch specific pages with `.md` suffix for markdown format (e.g., `https://modelcontextprotocol.io/specification/draft.md`).

Key pages to review:
- Specification overview and architecture
- Transport mechanisms (streamable HTTP, stdio)
- Tool, resource, and prompt definitions

#### 1.3 Study Framework Documentation

**Recommended stack:**
- **Language**: TypeScript (high-quality SDK support, good compatibility, static typing)
- **Transport**: Streamable HTTP for remote servers (stateless JSON), stdio for local servers

**SDK Documentation:**
- **TypeScript SDK**: `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md`
- **Python SDK**: `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md`

#### 1.4 Plan Your Implementation

**Understand the API:**
Review the service's API documentation to identify key endpoints, authentication requirements, and data models.

**Tool Selection:**
Prioritize comprehensive API coverage. List endpoints to implement, starting with the most common operations.

---

### Phase 2: Implementation

#### 2.1 Set Up Project Structure

**TypeScript project:**
```
my-mcp-server/
├── src/
│   ├── index.ts        # Entry point
│   ├── tools/          # Tool implementations
│   └── utils/          # Shared utilities
├── package.json
├── tsconfig.json
└── README.md
```

**Python project:**
```
my-mcp-server/
├── src/
│   └── my_mcp_server/
│       ├── __init__.py
│       ├── server.py   # Entry point
│       ├── tools/      # Tool implementations
│       └── utils/      # Shared utilities
├── pyproject.toml
└── README.md
```

#### 2.2 Implement Core Infrastructure

Create shared utilities:
- API client with authentication
- Error handling helpers
- Response formatting (JSON/Markdown)
- Pagination support

#### 2.3 Implement Tools

For each tool:

**Input Schema:**
- Use Zod (TypeScript) or Pydantic (Python)
- Include constraints and clear descriptions
- Add examples in field descriptions

**Output Schema:**
- Define `outputSchema` where possible for structured data
- Use `structuredContent` in tool responses (TypeScript SDK feature)
- Helps clients understand and process tool outputs

**Tool Description:**
- Concise summary of functionality
- Parameter descriptions
- Return type schema

**Implementation:**
- Async/await for I/O operations
- Proper error handling with actionable messages
- Support pagination where applicable
- Return both text content and structured data when using modern SDKs

**Annotations:**
- `readOnlyHint`: true/false
- `destructiveHint`: true/false
- `idempotentHint`: true/false
- `openWorldHint`: true/false

---

### Phase 3: Review and Test

#### 3.1 Code Quality

Review for:
- No duplicated code (DRY principle)
- Consistent error handling
- Full type coverage
- Clear tool descriptions

#### 3.2 Build and Test

**TypeScript:**
```bash
npm run build          # Verify compilation
npx @modelcontextprotocol/inspector  # Test with MCP Inspector
```

**Python:**
```bash
python -m py_compile your_server.py  # Verify syntax
# Test with MCP Inspector
```

---

### Phase 4: Create Evaluations

After implementing your MCP server, create comprehensive evaluations to test its effectiveness.

#### 4.1 Understand Evaluation Purpose

Use evaluations to test whether LLMs can effectively use your MCP server to answer realistic, complex questions.

#### 4.2 Create 10 Evaluation Questions

Process:
1. **Tool Inspection**: List available tools and understand their capabilities
2. **Content Exploration**: Use READ-ONLY operations to explore available data
3. **Question Generation**: Create 10 complex, realistic questions
4. **Answer Verification**: Solve each question yourself to verify answers

#### 4.3 Evaluation Requirements

Ensure each question is:
- **Independent**: Not dependent on other questions
- **Read-only**: Only non-destructive operations required
- **Complex**: Requiring multiple tool calls and deep exploration
- **Realistic**: Based on real use cases humans would care about
- **Verifiable**: Single, clear answer that can be verified by string comparison
- **Stable**: Answer won't change over time

#### 4.4 Output Format

Create an XML file with this structure:

```xml
<evaluation>
  <qa_pair>
    <question>Find discussions about AI model launches with animal codenames. One model needed a specific safety designation that uses the format ASL-X. What number X was being determined for the model named after a spotted wild cat?</question>
    <answer>3</answer>
  </qa_pair>
<!-- More qa_pairs... -->
</evaluation>
```

---

## TypeScript Implementation Patterns

### Server Setup

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";

const server = new McpServer({
  name: "my-server",
  version: "1.0.0",
});

server.tool(
  "list_items",
  {
    description: "List items with optional filtering",
    inputSchema: z.object({
      filter: z.string().optional().describe("Filter by name"),
      limit: z.number().default(10).describe("Max items to return"),
    }),
  },
  async ({ filter, limit }) => {
    const items = await fetchItems(filter, limit);
    return {
      content: [{ type: "text", text: JSON.stringify(items, null, 2) }],
    };
  }
);
```

### Error Handling

```typescript
server.tool("get_item", { /* schema */ }, async ({ id }) => {
  try {
    const item = await fetchItem(id);
    if (!item) {
      return {
        content: [{ type: "text", text: `Item ${id} not found. Try list_items to see available items.` }],
        isError: true,
      };
    }
    return { content: [{ type: "text", text: JSON.stringify(item) }] };
  } catch (error) {
    return {
      content: [{ type: "text", text: `Failed to fetch item: ${error.message}. Check your API key.` }],
      isError: true,
    };
  }
});
```

---

## Python Implementation Patterns

### Server Setup

```python
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

mcp = FastMCP("my-server")

class ListItemsInput(BaseModel):
    filter: str | None = Field(None, description="Filter by name")
    limit: int = Field(10, description="Max items to return")

@mcp.tool()
async def list_items(input: ListItemsInput) -> str:
    """List items with optional filtering."""
    items = await fetch_items(input.filter, input.limit)
    return json.dumps(items, indent=2)
```

### Error Handling

```python
@mcp.tool()
async def get_item(id: str) -> str:
    """Get item by ID."""
    try:
        item = await fetch_item(id)
        if not item:
            raise ValueError(f"Item {id} not found. Try list_items to see available items.")
        return json.dumps(item)
    except Exception as e:
        raise ValueError(f"Failed to fetch item: {e}. Check your API key.")
```

---

## Best Practices

### Server Naming
- Use lowercase with hyphens: `github-mcp-server`
- Be descriptive: `slack-workspace-tools` not `slack`

### Tool Naming
- Use consistent prefixes: `github_create_issue`, `github_list_repos`
- Use action verbs: `list_`, `get_`, `create_`, `update_`, `delete_`
- Be specific: `search_issues_by_label` not `search`

### Response Format
- Use JSON for structured data that will be processed
- Use Markdown for human-readable summaries
- Include pagination info when returning lists

### Pagination
- Default to reasonable limits (10-50 items)
- Return cursor/offset for next page
- Include total count when available

### Security
- Never log sensitive data (API keys, tokens)
- Validate all inputs
- Use environment variables for credentials
- Document required permissions
