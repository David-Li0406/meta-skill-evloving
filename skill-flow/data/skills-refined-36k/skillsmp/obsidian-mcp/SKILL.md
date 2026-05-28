---
name: obsidian-mcp
description: Guide for interacting with Obsidian vaults via MCP. Use when the user wants to read, write, search, manage tags, or organize notes within their Obsidian vault.
---

# Obsidian MCP Skill

This skill guides you in using the Obsidian MCP server to manage a user's vault. The server protects the vault by enforcing safe paths and validating frontmatter.

## Core Principles

1.  **Atomic Updates**: Prefer `patch_note` for making small changes to large files to avoid rewriting the entire content.
2.  **Frontmatter First**: Use `update_frontmatter` or `manage_tags` when only metadata needs changing.
3.  **Batch Operations**: Use `read_multiple_notes` when analyzing multiple related files (up to 10) to save roundtrips.
4.  **Confirm Destructive Actions**: `delete_note` requires a `confirmPath` argument that matches the `path`.

## API Reference

For detailed JSON schemas, argument lists, and return types, see [references/api.md](references/api.md).

## Common Workflows

### 1. Efficient Editing (Making targeted changes)

Use `patch_note` to replace specific text strings without rewriting the file.

**Goal**: Add an equation to a specific section.
**Tool**: `patch_note`

```json
{
  "path": "Physics/Relativity.md",
  "oldString": "## Energy and Mass",
  "newString": "## Energy and Mass\n\nE = mc²",
  "prettyPrint": false
}
```

### 2. Creating Notes (New content)

Use `write_note` (mode: `overwrite`) to create new files. The server handles directory creation automatically.

**Goal**: Create a meeting note.
**Tool**: `write_note`

```json
{
  "path": "Meetings/Team Sync.md",
  "content": "# Team Sync\n\n- Discussed Q1 goals\n- Action items assigned",
  "frontmatter": {
      "tags": ["meeting", "sync"],
      "date": "2025-10-24"
  },
  "prettyPrint": false
}
```

### 3. Reading Multiple Notes (Research/Summary)

Use `read_multiple_notes` to gather context from several files at once.

**Goal**: Summarize a list of book notes.
**Tool**: `read_multiple_notes`

```json
{
  "paths": [
    "Reading/The Phoenix Project.md",
    "Reading/Atomic Habits.md",
    "Reading/Deep Work.md"
  ],
  "prettyPrint": false
}
```

### 4. Managing Metadata (Tags/Status)

Use `update_frontmatter` or `manage_tags` to modify YAML metadata without touching the body content.

**Goal**: Update status and add tags.
**Tool**: `update_frontmatter`

```json
{
  "path": "Projects/Website Redesign.md",
  "frontmatter": {
    "tags": ["project", "web-design", "priority-high"],
    "status": "in-progress"
  },
  "merge": true,
  "prettyPrint": false
}
```

### 5. Searching Content

Use `search_notes` to find relevant information.

**Goal**: Find notes about "React hooks".
**Tool**: `search_notes`

```json
{
  "query": "React hooks",
  "limit": 10,
  "searchContent": true,
  "prettyPrint": false
}
```
