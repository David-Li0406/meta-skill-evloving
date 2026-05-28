---
name: mgrep-code-search
description: Use this skill when you need to perform semantic code searches across large codebases, allowing for natural language queries to find features and understand implementation details.
---

# mgrep Code Search

## Overview

mgrep is a semantic search tool that enables natural language queries across code, text, PDFs, and images. It is particularly effective for exploring larger or complex codebases where traditional pattern matching falls short.

## When to Use This Skill

Use mgrep when:
- The codebase contains more than 30 non-gitignored files.
- There are nested directory structures.
- Searching for concepts, features, or intent rather than exact strings.
- Exploring an unfamiliar codebase.
- You need to understand "where" or "how" something is implemented.

Use traditional grep/ripgrep when:
- Searching for exact patterns or symbols.
- Performing regex-based refactoring.
- Tracing specific function or variable names.

## Quick Start

### Indexing

Before searching, start the watcher to index the repository:

```bash
bunx @mixedbread/mgrep watch
```

The `watch` command indexes the repository and maintains synchronization with file changes. It respects `.gitignore` and `.mgrepignore` patterns.

### Searching

To perform a search, use the following command:

```bash
bunx @mixedbread/mgrep "your natural language query" [path]
```

## Search Commands

### Basic Search Examples

```bash
bunx @mixedbread/mgrep "where is authentication configured?"
bunx @mixedbread/mgrep "how do we handle errors in API calls?" src/
bunx @mixedbread/mgrep "database connection setup" src/lib
```

### Search Options

| Option          | Description                              |
| --------------- | ---------------------------------------- |
| `-m <count>`    | Maximum results (default: 10)            |
| `-c, --content` | Display full result content              |
| `-a, --answer`  | Generate AI-powered synthesis of results |
| `-s, --sync`    | Update index before searching            |
| `--no-rerank`   | Disable relevance optimization           |

### Examples with Options

```bash
# Get more results
bunx @mixedbread/mgrep -m 25 "user authentication flow"

# Show full content of matches
bunx @mixedbread/mgrep -c "error handling patterns"

# Get an AI-synthesised answer
bunx @mixedbread/mgrep -a "how does the caching layer work?"

# Sync index before searching
bunx @mixedbread/mgrep -s "payment processing" src/services
```