---
name: obsidian-vault-management
description: Use this skill when you need to efficiently manage and manipulate Markdown documents within an Obsidian vault, leveraging LSP features for search, backlink exploration, and document organization.
---

# Skill body

## Overview

This skill is designed for managing Markdown documents in an Obsidian vault. It utilizes the markdown-oxide LSP for efficient searching, backlink exploration, and document organization.

## Core Features

### 1. LSP-Based Search (markdown-oxide)

When connected to the markdown-oxide MCP server, you can utilize the following features:

- **Find References**: Locate all notes that reference a specific note.
- **Go to Definition**: Navigate to the actual file from a `[[link]]`.
- **Tag Search**: Search for all instances of a `#tag`.
- **Completion**: Use auto-completion for links, tags, and headings.
- **Diagnostics**: Identify broken links and non-existent notes.

### 2. Vault Structure Understanding

Before starting any work, familiarize yourself with the vault structure:

```bash
# Check directory structure
ls -la

# Find MOC (Map of Content) notes
find . -name "*MOC*" -o -name "*Index*" -o -name "*목차*"

# Check recently modified notes
find . -name "*.md" -mtime -7
```

### 3. Efficient Token Access

For bulk document operations, follow a hierarchical approach:

1. Read MOC/Index notes first.
2. Identify related notes using LSP.
3. Load only the necessary notes.
4. After completing tasks, use `/compact` to optimize.

## Usage Guidelines

### Searching Notes

```
1. Use LSP find_references first (if available).
2. If LSP is unavailable, use Grep to search for [[note-name]] patterns.
3. For tag searches: grep -r "#tag-name" --include="*.md"
```

### Analyzing Link Relationships

```
1. Identify outgoing links from the target note (extract [[link]] within the note).
2. Identify incoming links (backlinks) using LSP or grep.
3. If visualization is needed, create a Mermaid diagram.
```

### Modifying Documents

```
1. Check backlinks before making modifications (to understand impact).
2. Update all references when renaming files.
3. Verify anchor links ([[note#heading]]) when changing headings.
```

### Daily Notes Management

```
1. Confirm the format of daily notes (e.g., YYYY-MM-DD.md).
2. Perform date-based searches: find . -name "2025-01-*.md".
3. Batch process notes for specific periods.
```

## Obsidian-Specific Syntax

### Supported Syntax

| Syntax            | Description   | Example                  |
|-------------------|---------------|--------------------------|
| `[[link]]`        | Internal link | `[[Note Title]]`        |
| `[[link|alias]]`  | Alias link    | `[[Long Title|Short Name]]` |
| `[[link#heading]]` | Heading link  | `[[Note#Section]]`      |
| `![[embed]]`      | Note embed    | `![[Note to Include]]`  |
| `#tag`            | Tag           | `#project/active`       |
| `#tag/subtag`     | Nested tag    | `#status/in-progress`   |

### Frontmatter Handling

```yaml
---
title: Note Title
created: 2025-01-13
tags:
  - tag1
  - tag2
aliases:
  - alias1
  - alias2
---
```

- `aliases`: Allows linking with alternative names.
- `tags`: Recognizes both frontmatter and inline tags.

## MCP Server Setup

Connecting to the markdown-oxide MCP server is required.

### Setup Instructions

```bash
# Install markdown-oxide
brew install markdown-oxide
# or
cargo install --locked markdown-oxide

# Add MCP server
claude mcp add-json "markdown-oxide" '{
  "type": "stdio",
  "command": "npx",
  "args": ["tritlo/lsp-mcp", "markdown", "markdown-oxide"]
}'
```

### Environment Variables

```bash
export ENABLE_LSP_TOOL=1
```

For detailed setup, refer to the official documentation.