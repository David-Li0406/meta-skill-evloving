---
name: deepwiki-exploration
description: Use this skill when exploring GitHub repository documentation, understanding library APIs, or asking questions about open-source projects.
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

**API Endpoint:**
```
GET https://api.deepwiki.com/wiki/{owner}/{repo}/structure
```

**MCP Tool:** `mcp__deepwiki__read_wiki_structure`

**Parameters:**
- `repoName` (required): GitHub repository in "owner/repo" format

**Example Usage:**
```bash
curl -s "https://api.deepwiki.com/wiki/microsoft/vscode/structure" | jq '.'
```
or
```
mcp__deepwiki__read_wiki_structure({ repoName: "microsoft/vscode" })
```

### Read Wiki Contents

Get full documentation content for a repository.

**API Endpoint:**
```
GET https://api.deepwiki.com/wiki/{owner}/{repo}/contents
```

**MCP Tool:** `mcp__deepwiki__read_wiki_contents`

**Parameters:**
- `repoName` (required): GitHub repository in "owner/repo" format

**Example Usage:**
```bash
curl -s "https://api.deepwiki.com/wiki/xtermjs/xterm.js/contents" | jq '.'
```
or
```
mcp__deepwiki__read_wiki_contents({ repoName: "xtermjs/xterm.js" })
```

### Ask Question

Ask a question about a repository and get AI-generated answers.

**API Endpoint:**
```
POST https://api.deepwiki.com/wiki/{owner}/{repo}/ask
```

**MCP Tool:** `mcp__deepwiki__ask_question`

**Parameters:**
- `repoName` (required): GitHub repository in "owner/repo" format
- `question` (required): The question to ask about the repository

**Example Usage:**
```bash
curl -s -X POST "https://api.deepwiki.com/wiki/microsoft/vscode/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "How does the terminal handle PTY integration?"}'
```
or
```
mcp__deepwiki__ask_question({
  repoName: "microsoft/vscode",
  question: "How does the terminal extension handle PTY integration?"
})
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

1. **Start with structure**: Use `read_wiki_structure` first to understand available topics.
2. **Be specific with questions**: Provide context in questions for better answers.
3. **Use full repo path**: Always use the complete "owner/repo" format.
4. **Combine with local code**: Use DeepWiki insights together with local codebase exploration.

## Notes

- No API key required for public repositories.
- Rate limits may apply.
- Responses are AI-generated based on repository content.

## References

For detailed tool parameters, see `references/tools.md`.