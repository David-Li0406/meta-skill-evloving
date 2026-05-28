---
name: mcp-server-development
description: Use this skill when creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools, resources, and prompts.
---

# MCP Server Development Guide

## Overview

Create MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. The quality of an MCP server is measured by how well it enables LLMs to accomplish real-world tasks safely, reliably, and with predictable outputs.

## High-Level Workflow

Creating a high-quality MCP server involves four main phases:

### Phase 1: Deep Research and Planning

#### 1.1 Understand Modern MCP Design

- **API Coverage vs. Workflow Tools:** Balance comprehensive API endpoint coverage with specialized workflow tools. Prioritize comprehensive API coverage when uncertain.
- **Tool Naming and Discoverability:** Use clear, descriptive tool names with consistent prefixes (e.g., `github_create_issue`, `github_list_repos`) to help agents find the right tools quickly.
- **Context Management:** Design tools that return focused, relevant data and support filtering/pagination.
- **Actionable Error Messages:** Provide error messages that guide agents toward solutions with specific suggestions.

#### 1.2 Study MCP Protocol Documentation

- **Navigate the MCP specification:** Start with the sitemap at `https://modelcontextprotocol.io/sitemap.xml` and review key pages such as the specification overview, transport mechanisms, and tool definitions.

#### 1.3 Study Framework Documentation

- **Recommended stack:** Use TypeScript for high-quality SDK support and good compatibility, or Python for FastMCP. Choose streamable HTTP for remote servers and stdio for local servers.

#### 1.4 Plan Your Implementation

- **Understand the API:** Review the service's API documentation to identify key endpoints, authentication requirements, and data models.
- **Tool Selection:** Prioritize comprehensive API coverage and list endpoints to implement, starting with the most common operations.

---

### Phase 2: Implementation

#### 2.1 Set Up Project Structure

Use the `init_mcp.py` script to create a properly structured MCP server:

```bash
# Python MCP server
scripts/init_mcp.py my-server --path ./servers --lang python

# TypeScript MCP server
scripts/init_mcp.py my-server --path ./servers --lang typescript
```

This creates the necessary directories and files for your server.

#### 2.2 Implement Core Infrastructure

Create shared utilities:
- API client with authentication
- Error handling helpers
- Response formatting (JSON/Markdown)
- Pagination support

#### 2.3 Implement Tools

For each tool:
- **Input Schema:** Use Zod (TypeScript) or Pydantic (Python) to define input schemas with constraints and clear descriptions.
- **Output Schema:** Define `outputSchema` for structured data and use `structuredContent` in tool responses.
- **Tool Description:** Provide a concise summary of functionality, parameter descriptions, and return type schema.
- **Implementation:** Use async/await for I/O operations, proper error handling, and support pagination where applicable.

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

Follow the process outlined in the evaluation guide:
1. **Tool Inspection:** List available tools and understand their capabilities.
2. **Content Exploration:** Use READ-ONLY operations to explore available data.
3. **Question Generation:** Create 10 complex, realistic questions.
4. **Answer Verification:** Solve each question yourself to verify answers.

#### 4.3 Evaluation Requirements

Ensure each question is:
- **Independent:** Not dependent on other questions.
- **Read-only:** Only non-destructive operations required.
- **Complex:** Requiring multiple tool calls and deep exploration.
- **Realistic:** Based on real use cases humans would care about.
- **Verifiable:** Single, clear answer that can be verified by string comparison.
- **Stable:** Answer won't change over time.

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

## Reference Files

### 📚 Documentation Library

Load these resources as needed during development:

- **MCP Protocol:** Start with sitemap at `https://modelcontextprotocol.io/sitemap.xml`.
- **MCP Best Practices:** Core guidelines for server and tool naming conventions, response format guidelines, pagination best practices, and security standards.
- **SDK Documentation:** Fetch from the respective SDK repositories for TypeScript and Python.

### Additional Resources

- **Evaluation Guide:** Complete evaluation creation guide with question creation guidelines and answer verification strategies.
- **mKit Boilerplate Guide:** For implementing or extending the mKit MCP boilerplate.

## When to Use

Use this skill when the task matches its description and triggers. If the request is outside scope, route to the referenced skill.

## Inputs

User request details and any relevant files/links.

## Outputs

A structured response or artifact appropriate to the skill. Include `schema_version: 1` if outputs are contract-bound.

## Constraints

Redact secrets/PII by default. Avoid destructive operations without explicit user direction.

## Validation

Run any relevant checks or scripts when available. Fail fast and report errors before proceeding.

## Philosophy

Favor clarity, explicit tradeoffs, and verifiable outputs.