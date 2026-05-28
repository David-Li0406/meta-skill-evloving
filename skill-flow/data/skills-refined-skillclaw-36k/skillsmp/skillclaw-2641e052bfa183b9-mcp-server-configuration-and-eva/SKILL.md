---
name: mcp-server-configuration-and-evaluation
description: Use this skill when you need to configure, build, and evaluate MCP (Model Context Protocol) servers across various IDEs and tools.
---

# MCP Server Configuration and Evaluation

This skill provides comprehensive guidance on configuring, building, and evaluating MCP servers, ensuring they are set up correctly and can effectively respond to complex queries.

## Overview

MCP (Model Context Protocol) servers facilitate the connection between AI systems and external tools. This skill covers the configuration paths for different IDEs, principles for building MCP servers, and guidelines for evaluating their effectiveness.

## Skill Contents

### 1. IDE Configuration Paths

| IDE/Tool | Configuration File | Type |
|----------|-------------------|------|
| **Cursor** | `.cursor/mcp.json` | Repository-based |
| **VS Code** (GitHub Copilot) | `.vscode/mcp.json` | Repository-based |
| **Claude Code** | `.mcp.json` | Repository-based |
| **IntelliJ IDEA** (Copilot) | `~/.config/github-copilot/intellij/mcp.json` | User-based |
| **GitHub Copilot CLI** | `~/.copilot/mcp-config.json` | User-based |

### 2. Building MCP Servers

#### Core Concepts

- **Tools**: Functions AI can call.
- **Resources**: Data AI can read.
- **Prompts**: Pre-defined prompt templates.

#### Server Architecture

Example project structure:
```
my-mcp-server/
├── src/
│   └── index.ts      # Main entry
├── package.json
└── tsconfig.json
```

#### Tool Design Principles

- **Clear name**: Action-oriented (e.g., `get_weather`).
- **Single purpose**: Each tool should perform one function well.
- **Validated input**: Use schemas to define input types and descriptions.
- **Structured output**: Ensure predictable response formats.

### 3. Evaluation of MCP Servers

#### Evaluation Requirements

- Create 10 human-readable, independent, non-destructive questions.
- Each question should require multiple tool calls and yield a single, verifiable answer.

#### Output Format
```xml
<evaluation>
   <qa_pair>
      <question>Your question here</question>
      <answer>Single verifiable answer</answer>
   </qa_pair>
</evaluation>
```

### 4. Error Handling

- **Invalid params**: Return a validation error message.
- **Not found**: Provide a clear "not found" response.

## Conclusion

This skill serves as a comprehensive guide for configuring, building, and evaluating MCP servers, ensuring they are effective and reliable for AI interactions.