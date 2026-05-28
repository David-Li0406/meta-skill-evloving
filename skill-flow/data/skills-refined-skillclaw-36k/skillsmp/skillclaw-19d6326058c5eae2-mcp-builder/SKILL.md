---
name: mcp-builder
description: Use this skill when creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools, resources, and prompts.
---

# MCP Server Development Guide

## Overview

Create MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. The quality of an MCP server is measured by how well it enables LLMs to accomplish real-world tasks safely, reliably, and with predictable outputs.

## High-Level Workflow

Creating a high-quality MCP server involves several main phases:

### Phase 1: Research and Planning

#### Understand Modern MCP Design

- **API Coverage vs. Workflow Tools:** Balance comprehensive API endpoint coverage with specialized workflow tools. Workflow tools can be more convenient for specific tasks, while comprehensive coverage gives agents flexibility to compose operations.
- **Tool Naming and Discoverability:** Use clear, descriptive tool names with consistent prefixes (e.g., `github_create_issue`, `github_list_repos`) to help agents find the right tools quickly.
- **Context Management:** Design tools that return focused, relevant data and provide actionable error messages to guide agents toward solutions.

#### Study MCP Protocol Documentation

- Start with the sitemap to find relevant pages: `https://modelcontextprotocol.io/sitemap.xml`
- Key pages to review include the specification overview, transport mechanisms, and tool definitions.

### Phase 2: Implementation

#### Recommended Stack

- **Language:** TypeScript (best SDK support) or Python (FastMCP).
- **Transport:** Streamable HTTP for remote, stdio for local.

#### Project Structure

```
my-mcp-server/
├── src/
│   ├── index.ts      # Server entry point
│   ├── tools/        # Tool implementations
│   └── utils/        # Shared utilities
├── package.json
└── tsconfig.json
```

#### Tool Implementation Pattern

```typescript
server.registerTool({
  name: "github_create_issue",
  description: "Create a new GitHub issue",
  inputSchema: z.object({
    repo: z.string().describe("Repository name (owner/repo)"),
    title: z.string().describe("Issue title"),
    body: z.string().optional().describe("Issue body")
  }),
  outputSchema: z.object({
    id: z.number(),
    url: z.string()
  }),
  annotations: {
    readOnlyHint: false,
    destructiveHint: false,
    idempotentHint: false
  },
  handler: async (input) => {
    // Implementation
    return { id: 123, url: "https://..." };
  }
});
```

### Phase 3: Testing

Run relevant checks to ensure compliance and functionality:

```bash
# TypeScript
npm run build
npx @modelcontextprotocol/inspector

# Python
python -m py_compile your_server.py
```

### Phase 4: Create Evaluations

Develop complex, realistic questions to test your MCP server:

```xml
<evaluation>
  <qa_pair>
    <question>Find all open issues labeled 'bug' in the repo</question>
    <answer>5</answer>
  </qa_pair>
</evaluation>
```

## Tool Design Best Practices

- Use Zod (TS) or Pydantic (Python) for schemas.
- Include constraints and ensure structured outputs for better discoverability and usability.
- Follow compliance with the latest MCP specifications and industry standards.