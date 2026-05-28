---
name: obsidian-markdown-vault
description: Use this skill for efficient management and analysis of Markdown documents within an Obsidian vault, leveraging LSP features for backlinks, tag searches, and document structure exploration.
---

# Obsidian Markdown Vault Skill

This skill facilitates efficient operations on Markdown documents within an Obsidian vault, utilizing the markdown-oxide LSP for various tasks.

## Core Features

### 1. LSP-Based Search (markdown-oxide)

When connected to the markdown-oxide MCP server, the following features are available:

- **Find References**: Locate all backlinks referencing a specific note.
- **Go to Definition**: Navigate to the actual file from `[[link]]`.
- **Tag Search**: Search all instances of `#tag`.
- **Completion**: Utilize auto-completion for links, tags, and headings.
- **Diagnostics**: Detect broken links and non-existent notes.

### 2. Vault Structure Understanding

Before starting any task, familiarize yourself with the vault structure:

```bash
# Check directory structure
ls -la

# Find MOC (Map of Content) notes
find . -name "*MOC*" -o -name "*Index*" -o -name "*목차*"

# Check recently modified notes
find . -name "*.md" -mtime -7
```

### 3. Token Efficient Access

For bulk document operations, follow a hierarchical approach:

1. Read MOC/Index notes first.
2. Identify related notes using LSP.
3. Selectively load only the necessary notes.
4. After completing tasks, run `/compact`.

## Task Guidelines

### Note Searching

```
1. Use LSP find_references first (if available).
2. If LSP is unavailable, search for [[note_name]] using Grep.
3. For tag searches: grep -r "#tag_name" --include="*.md".
```

### Link Relationship Analysis

```
1. Identify outgoing links from the target note (extract [[link]] within the note).
2. Identify incoming links (backlinks) using LSP or grep.
3. Create a visualization diagram using Mermaid if needed.
```

### Document Editing

```
1. Check backlinks before editing (to understand the impact).
2. Update all references when renaming files.
3. Verify anchor links ([[note#heading]]) when changing headings.
```

### Daily Notes Management

```
1. Confirm the format of Daily notes (e.g., YYYY-MM-DD.md).
2. Search by date: find . -name "2025-01-*.md".
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
| `#tag/subtag`     | Nested tag    | `#status/in-progress`    |

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

### Environment Variable

```bash
export ENABLE_LSP_TOOL=1
```

Refer to the detailed setup in the relevant documentation.

## Cautionary Notes

1. **Limit Bulk File Loads**: Process no more than 10 files at a time.
2. **Be Cautious with Archive Folder**: Access archived notes only when necessary.
3. **Token Management**: Run `/compact` after completing tasks.
4. **Prioritize LSP**: Use LSP features over text searches whenever possible.

## Related Files

- Reference documentation for detailed setup and advanced features.
- Troubleshooting guide for resolving issues.