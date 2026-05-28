---
name: deepwiki-exploration
description: Use this skill when you need to explore GitHub repository documentation, understand library APIs, or ask questions about open-source projects using DeepWiki.
---

# DeepWiki Exploration

## Overview

This skill enables exploration of GitHub repository documentation using the DeepWiki API or MCP server. It provides AI-generated documentation and Q&A capabilities for any GitHub repository.

## When to Use This Skill

- Researching GitHub repository documentation
- Understanding library or framework APIs
- Asking specific questions about open-source projects
- Exploring repository structure and architecture
- Learning how to use unfamiliar libraries

## Available Tools

### Read Wiki Structure

Get a list of documentation topics for a GitHub repository.

**Endpoint:**
```
GET https://api.deepwiki.com/wiki/{owner}/{repo}/structure
```

**Example:**
```bash
curl -s "https://api.deepwiki.com/wiki/microsoft/vscode/structure" | jq '.'
```

### Read Wiki Contents

View comprehensive documentation about a GitHub repository.

**Endpoint:**
```
GET https://api.deepwiki.com/wiki/{owner}/{repo}/contents
```

**Example:**
```bash
curl -s "https://api.deepwiki.com/wiki/xtermjs/xterm.js/contents" | jq '.'
```

### Ask Question

Ask any question about a GitHub repository and get AI-powered answers.

**Endpoint:**
```
POST https://api.deepwiki.com/wiki/{owner}/{repo}/ask
```

**Example:**
```bash
curl -s -X POST "https://api.deepwiki.com/wiki/microsoft/vscode/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "How does the terminal handle PTY integration?"}'
```

## Common Workflows

### Research a New Library

1. Get wiki structure to understand available topics.
2. Read full documentation for comprehensive understanding.
3. Ask specific questions about implementation details.

### Understand VS Code Implementation

```bash
curl -s -X POST "https://api.deepwiki.com/wiki/microsoft/vscode/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "How does VS Code implement terminal session persistence?"}'
```

### Explore xterm.js API

```bash
curl -s -X POST "https://api.deepwiki.com/wiki/xtermjs/xterm.js/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "What addons are available and how do I use them?"}'
```

## Best Practices

1. **Start with structure**: Use the `Read Wiki Structure` endpoint to identify available topics before diving into the contents or asking questions.
2. **Use specific questions**: When asking questions, be as specific as possible to get the most relevant answers.

## Notes

- No API key is required for public repositories.
- Rate limits may apply.
- Responses are AI-generated based on repository documentation.