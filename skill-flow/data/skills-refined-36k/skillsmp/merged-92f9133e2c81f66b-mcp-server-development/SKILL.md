---
name: mcp-server-development
description: Use this skill when building or upgrading MCP (Model Context Protocol) servers with TypeScript SDK, implementing tools, resources, or prompts, and ensuring compliance with the MCP specification.
---

# MCP Server Development Guide

## Overview

This guide provides comprehensive instructions for creating and maintaining MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. The quality of an MCP server is measured by how effectively it allows LLMs to accomplish real-world tasks.

## High-Level Workflow

Creating a high-quality MCP server involves four main phases:

### Phase 1: Deep Research and Planning

#### 1.1 Understand Modern MCP Design

- **API Coverage vs. Workflow Tools**: Balance comprehensive API endpoint coverage with specialized workflow tools. Prioritize comprehensive API coverage when uncertain.
- **Tool Naming and Discoverability**: Use clear, descriptive tool names with consistent prefixes (e.g., `github_create_issue`, `github_list_repos`).
- **Context Management**: Design tools that return focused, relevant data with concise descriptions.
- **Actionable Error Messages**: Provide error messages that guide users toward solutions.

#### 1.2 Study MCP Protocol Documentation

- Review the MCP specification, focusing on key pages such as the specification overview, transport mechanisms, and tool definitions.

#### 1.3 Study Framework Documentation

- Recommended stack: TypeScript for high-quality SDK support and static typing. Review SDK documentation for both TypeScript and Python.

#### 1.4 Plan Your Implementation

- Understand the service's API documentation to identify key endpoints and authentication requirements.

### Phase 2: Implementation

#### 2.1 Set Up Project Structure

**TypeScript Project Structure:**
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

**Python Project Structure:**
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

Create shared utilities for API client authentication, error handling, response formatting, and pagination support.

#### 2.3 Implement Tools

For each tool:
- **Input Schema**: Use Zod (TypeScript) or Pydantic (Python) for input validation.
- **Output Schema**: Define `outputSchema` for structured data.
- **Tool Description**: Provide a concise summary of functionality and parameter descriptions.
- **Implementation**: Use async/await for I/O operations, handle errors with actionable messages, and support pagination.

### Phase 3: Review and Test

#### 3.1 Code Quality

Ensure no duplicated code, consistent error handling, full type coverage, and clear tool descriptions.

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

### Phase 4: Create Evaluations

Create evaluations to test the effectiveness of your MCP server. Ensure each question is independent, read-only, complex, realistic, verifiable, and stable.

#### 4.1 Output Format

Create an XML file with the structure:
```xml
<evaluation>
  <qa_pair>
    <question>Your question here</question>
    <answer>Your answer here</answer>
  </qa_pair>
  <!-- More qa_pairs... -->
</evaluation>
```

## TypeScript Implementation Patterns

### Server Setup

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";

const server = new McpServer({
  name: "my-server",
  version: "1.0.0",
});

// Define tool with Zod schema
server.tool(
  "my_tool",
  "Tool description for LLM",
  { input: z.string().describe("Input parameter") },
  async (args) => ({
    content: [{ type: "text", text: `Result: ${args.input}` }],
    structuredContent: { result: args.input }
  })
);
```

### Error Handling

```typescript
function formatToolError(message: string, data: Record<string, unknown> = {}): CallToolResult {
  return {
    content: [{ type: "text", text: message }],
    structuredContent: { error: message, ...data },
    isError: true
  };
}
```

## Best Practices

- **Server Naming**: Use lowercase with hyphens for server names.
- **Tool Naming**: Use consistent prefixes and action verbs.
- **Response Format**: Use JSON for structured data and Markdown for human-readable summaries.
- **Security**: Validate all inputs and never log sensitive data.

## Common Mistakes

- Mixing framing formats: Always use Content-Length for output.
- Swallowing errors: Always propagate errors with context.
- Missing validation: Validate all inputs before processing.

## Remember

- **Content-Length always**: Output framing must be consistent.
- **Validate everything**: Never trust client input.
- **One handler, one tool**: Keep handlers focused.
- **Test error paths**: Most bugs hide in error handling.
- **Protocol compliance**: Follow JSON-RPC 2.0 exactly.