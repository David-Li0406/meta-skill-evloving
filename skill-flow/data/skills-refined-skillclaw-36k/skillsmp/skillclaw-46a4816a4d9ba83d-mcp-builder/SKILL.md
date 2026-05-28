---
name: mcp-builder
description: Use this skill when you need to create a high-quality MCP (Model Context Protocol) server that enables LLMs to interact with external services through well-designed tools.
---

# MCP Server Development Guide

## Overview

This guide provides a comprehensive approach to building a high-quality MCP (Model Context Protocol) server, allowing LLMs to effectively interact with external services and APIs. The quality of an MCP server is determined by how well it enables LLMs to accomplish real-world tasks.

## Process

### 🚀 High-Level Workflow

Creating a high-quality MCP server involves four main phases:

#### Phase 1: Research and Planning

1. **Understand Modern MCP Design**
   - Balance API coverage with workflow tools. Prioritize comprehensive API endpoints for flexibility.
   - Use clear, descriptive tool names to enhance discoverability.
   - Design tools that return focused, relevant data, optimizing for the limited context available to agents.

2. **Study the MCP Protocol Documentation**
   - Navigate the MCP specifications and guidelines to understand the transport mechanisms and tool definitions.

3. **Research Framework Documentation**
   - Recommended tech stack:
     - **TypeScript**: Excellent SDK support and type safety.
     - **Python**: Rich ecosystem and ease of use.
   - Use streamable HTTP for remote servers and stdio for local tools.

4. **Plan Your Implementation**
   - Review the service's API documentation to identify key endpoints and authentication requirements.
   - List the endpoints to implement, starting with the most common operations.

#### Phase 2: Implementation

1. **Set Up Project Structure**
   - Follow specific language guidelines for project setup:
     - **TypeScript**: Organize files in a clear structure with `src/`, `package.json`, and `tsconfig.json`.
     - **Python**: Use a similar structure with `src/my_mcp_server/`, `__init__.py`, and `pyproject.toml`.

2. **Implement Core Infrastructure**
   - Create shared utilities such as an authenticated API client, error handling helpers, and response formatting.

3. **Implement Tools**
   - Define input and output schemas using Zod (TypeScript) or Pydantic (Python).
   - Ensure tools have clear descriptions, parameter definitions, and structured output where applicable.
   - Implement error handling with actionable messages and support for pagination.

### Best Practices

- **Single Responsibility**: Each tool should perform one task.
- **Clear Naming**: Use a verb-noun format for tool names.
- **Consistent Error Handling**: All errors should follow the same format.
- **Support for Pagination**: Large datasets must support pagination.

### Reference Resources

- [MCP Official Documentation](https://modelcontextprotocol.io/)
- [TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [Python SDK](https://github.com/modelcontextprotocol/python-sdk)