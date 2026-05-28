# Obsidian MCP API Reference

## API Methods

### read_note
Read a note from the vault with parsed frontmatter.

**Request:**
```json
{
  "name": "read_note",
  "arguments": {
    "path": "project-ideas.md",
    "prettyPrint": false
  }
}
```

**Response:**
```json
{
  "fm": {
    "title": "Project Ideas",
    "tags": ["projects", "brainstorming"],
    "created": "2023-01-15T10:30:00.000Z"
  },
  "content": "# Project Ideas\n\n## AI Tools\n- MCP server for Obsidian\n- Voice note transcription\n\n## Web Apps\n- Task management system"
}
```

### write_note
Write a note to the vault with optional frontmatter and write mode.

**Modes:**
- `overwrite` (default): Replace entire file content
- `append`: Add content to the end of existing file
- `prepend`: Add content to the beginning of existing file

**Request (Overwrite):**
```json
{
  "name": "write_note",
  "arguments": {
    "path": "meeting-notes.md",
    "content": "# Team Meeting\n\n## Agenda\n- Project updates\n- Next milestones",
    "frontmatter": {
      "title": "Team Meeting Notes",
      "date": "2023-12-01",
      "tags": ["meetings", "team"]
    },
    "mode": "overwrite"
  }
}
```

**Request (Append):**
```json
{
  "name": "write_note",
  "arguments": {
    "path": "daily-log.md",
    "content": "\n\n## 3:00 PM Update\n- Completed project review\n- Started new feature",
    "mode": "append"
  }
}
```

### patch_note
Efficiently update specific parts of a note.

**Request:**
```json
{
  "name": "patch_note",
  "arguments": {
    "path": "Physics/Relativity.md",
    "oldString": "## Energy and Mass",
    "newString": "## Energy and Mass\n\nE = mc²",
    "prettyPrint": false
  }
}
```

### list_directory
List files and directories in the vault.

**Request:**
```json
{
  "name": "list_directory",
  "arguments": {
        "path": "Projects",
    "prettyPrint": false
  }
}
```

### delete_note
Delete a note from the vault (requires confirmation).

**Request:**
```json
{
  "name": "delete_note",
  "arguments": {
    "path": "old-draft.md",
    "confirmPath": "old-draft.md"
  }
}
```

### manage_tags
Add, remove, or list tags in a note.

**Request (Add):**
```json
{
  "name": "manage_tags",
  "arguments": {
    "path": "research-notes.md",
    "operation": "add",
    "tags": ["machine-learning", "ai", "important"]
  }
}
```

### search_notes
Search for notes in the vault by content or frontmatter.

**Request:**
```json
{
  "name": "search_notes",
  "arguments": {
    "query": "machine learning",
    "limit": 5,
    "searchContent": true,
    "searchFrontmatter": false,
    "caseSensitive": false,
    "prettyPrint": false
  }
}
```

### move_note
Move or rename a note in the vault.

**Request:**
```json
{
  "name": "move_note",
  "arguments": {
    "oldPath": "drafts/article.md",
    "newPath": "published/article.md",
    "overwrite": false
  }
}
```

### read_multiple_notes
Read multiple notes in a batch (maximum 10 files).

**Request:**
```json
{
  "name": "read_multiple_notes",
  "arguments": {
    "paths": ["note1.md", "note2.md", "note3.md"],
    "includeContent": true,
    "includeFrontmatter": true,
    "prettyPrint": false
  }
}
```

### update_frontmatter
Update frontmatter of a note without changing content.

**Request:**
```json
{
  "name": "update_frontmatter",
  "arguments": {
    "path": "research-note.md",
    "frontmatter": {
      "status": "completed",
      "updated": "2025-09-23"
    },
    "merge": true
  }
}
```
