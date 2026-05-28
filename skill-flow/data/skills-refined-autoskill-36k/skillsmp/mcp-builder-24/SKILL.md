---
name: mcp-builder
description: Use when building MCP servers or integrating external APIs/services via MCP (TypeScript or Python).
allowed-tools: ["shell", "read_file", "write_file", "apply_patch", "update_plan"]
metadata:
  short-description: Build MCP servers and tools
---

# MCP Server Development Guide

## Overview

Create MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. The quality of an MCP server is measured by how well it enables real-world tasks.

---

# Process

## Phase 1: Deep Research and Planning

### 1.1 Understand Modern MCP Design

**API Coverage vs. Workflow Tools:**
Balance comprehensive endpoint coverage with specialized workflow tools. When uncertain, prefer comprehensive coverage.

**Tool Naming and Discoverability:**
Use clear, consistent, action-oriented tool names.

**Context Management:**
Keep tool descriptions concise; support filtering/pagination.

**Actionable Error Messages:**
Errors should guide agents toward resolution with specific next steps.

### 1.2 Study MCP Protocol Documentation

Start with the sitemap and fetch markdown pages using `web.run`:
- `https://modelcontextprotocol.io/sitemap.xml`
- `https://modelcontextprotocol.io/specification/draft.md`

Review architecture, transports, tool/resource/prompt definitions.

### 1.3 Study Framework Documentation

**Recommended stack:**
- Language: TypeScript
- Transport: Streamable HTTP for remote servers; stdio for local servers

**Load framework documentation:**
- MCP Best Practices: `reference/mcp_best_practices.md`
- TypeScript SDK: `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md`
- TypeScript Guide: `reference/node_mcp_server.md`
- Python SDK: `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md`
- Python Guide: `reference/python_mcp_server.md`

### 1.4 Plan Your Implementation

- Review API docs to identify endpoints, auth, and data models
- Prioritize common operations and ensure pagination support

---

## Phase 2: Implementation

### 2.1 Set Up Project Structure

See language-specific guides in `reference/`.

### 2.2 Implement Core Infrastructure

- Authenticated API client
- Error handling helpers
- Response formatting
- Pagination utilities

### 2.3 Implement Tools

**Input Schema:** Zod (TS) or Pydantic (Python) with constraints and examples

**Output Schema:** Define `outputSchema` where possible; return structured content

**Annotations:**
- `readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`

---

## Phase 3: Review and Test

### 3.1 Code Quality

- DRY, consistent error handling, type coverage, clear descriptions

### 3.2 Build and Test

**TypeScript:**
- `npm run build`
- `npx @modelcontextprotocol/inspector`

**Python:**
- `python -m py_compile your_server.py`
- MCP Inspector

---

## Phase 4: Create Evaluations

Load `reference/evaluation.md` and create 10 realistic, stable, read-only evaluation questions with verifiable answers.

---

# Reference Files

These files are bundled with this skill under the local `reference/` directory:
- `reference/mcp_best_practices.md`
- `reference/node_mcp_server.md`
- `reference/python_mcp_server.md`
- `reference/evaluation.md`

## Arguments

Target: ${ARGUMENTS}
