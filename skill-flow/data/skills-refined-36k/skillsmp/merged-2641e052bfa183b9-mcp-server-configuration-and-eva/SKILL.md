---
name: mcp-server-configuration-and-evaluation
description: Use this skill when configuring, building, and evaluating MCP (Model Context Protocol) servers across various IDEs and tools.
---

# MCP Server Configuration and Evaluation

This document provides guidance on configuring, building, and evaluating MCP (Model Context Protocol) servers across different IDEs and tools.

## Overview

MCP server configurations are distributed to IDEs in various ways depending on the tool. This skill covers the setup, troubleshooting, and evaluation of MCP servers to ensure they can effectively answer complex questions using only the tools provided.

## Skill Contents

### Sections

- [IDE Configuration Paths](#ide-configuration-paths)
- [MCP Server Building Principles](#mcp-server-building-principles)
- [Evaluation Guide](#evaluation-guide)
- [References](#references)

## IDE Configuration Paths

| IDE/Tool | Configuration File | Type |
|----------|-------------------|------|
| **Cursor** | `.cursor/mcp.json` | Repository-based |
| **VS Code** (GitHub Copilot) | `.vscode/mcp.json` | Repository-based |
| **Claude Code** | `.mcp.json` | Repository-based |
| **IntelliJ IDEA** (Copilot) | `~/.config/github-copilot/intellij/mcp.json` | User-based |
| **GitHub Copilot CLI** | `~/.copilot/mcp-config.json` | User-based |

### Quick Reference

#### Automatic (Repository-based)

These IDEs automatically detect MCP configurations from the repository:
- Cursor
- VS Code (with GitHub Copilot)
- Claude Code

#### Manual (User-based)

These tools require configuration in the user's home directory:
- IntelliJ IDEA (with GitHub Copilot)
- GitHub Copilot CLI

## MCP Server Building Principles

### What is MCP?

Model Context Protocol (MCP) is a standard for connecting AI systems with external tools and data sources.

### Core Concepts

| Concept       | Purpose                      |
| ------------- | ---------------------------- |
| **Tools**     | Functions AI can call        |
| **Resources** | Data AI can read             |
| **Prompts**   | Pre-defined prompt templates |

### Server Architecture

#### Project Structure

```
my-mcp-server/
├── src/
│   └── index.ts      # Main entry
├── package.json
└── tsconfig.json
```

### Tool Design Principles

| Principle         | Description                                |
| ----------------- | ------------------------------------------ |
| Clear name        | Action-oriented (e.g., get_weather)       |
| Single purpose    | One thing well                             |
| Validated input   | Schema with types and descriptions         |
| Structured output | Predictable response format                |

### Error Handling

| Situation      | Response                   |
| -------------- | -------------------------- |
| Invalid params | Validation error message   |
| Not found      | Clear "not found"          |
| Server error   | Generic error, log details |

## Evaluation Guide

### Purpose of Evaluations

The quality of an MCP server is measured by how well it enables LLMs to answer realistic, complex questions using only the tools provided.

### Evaluation Requirements

- Create 10 human-readable questions
- Questions must be READ-ONLY, INDEPENDENT, NON-DESTRUCTIVE
- Each question requires multiple tool calls
- Answers must be single, verifiable values
- Answers must be STABLE (won't change over time)

### Question Guidelines

1. **Questions MUST be independent**: Each question should not depend on the answer to any other question.
2. **Questions MUST require ONLY NON-DESTRUCTIVE AND IDEMPOTENT tool use**: Should not modify state to arrive at the correct answer.
3. **Questions must be REALISTIC, CLEAR, CONCISE, and COMPLEX**: Must require multiple tools or steps to answer.

### Output Format

```xml
<evaluation>
   <qa_pair>
      <question>Your question here</question>
      <answer>Single verifiable answer</answer>
   </qa_pair>
</evaluation>
```

## References

- **MCP Configuration Documentation**: Detailed documentation on MCP server configurations.
- **MCP Server Setup**: Instructions for setting up the GitHub MCP server with Docker.
- **Troubleshooting**: Common issues and solutions related to MCP server configurations.

---

> **Remember:** MCP tools should be simple, focused, and well-documented. The AI relies on descriptions to use them correctly.