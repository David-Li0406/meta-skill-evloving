---
name: research-management
description: |
  Research and note management for Evernote. Use this skill when:
  - Saving research findings or web content
  - Searching for existing notes and references
  - Organizing notes into notebooks and with tags
  - Creating structured documentation
  - Managing knowledge bases and project notes
allowed-tools:
  - mcp__evernote__evernote_create_note
  - mcp__evernote__evernote_search_notes
  - mcp__evernote__evernote_get_note
  - mcp__evernote__evernote_update_note
  - mcp__evernote__evernote_delete_note
  - mcp__evernote__evernote_list_notebooks
  - mcp__evernote__evernote_create_notebook
  - mcp__evernote__evernote_list_tags
  - mcp__evernote__evernote_health_check
---

# Research Management Skill

Manage research and notes in Evernote using the **Capture-Organize-Retrieve** pattern.

## Phase 1: CAPTURE (Save Information)

### Create a Note

```javascript
mcp__evernote__evernote_create_note({
  title: "Research: [Topic] - YYYY-MM-DD",
  content: "## Summary\n\nKey findings here.\n\n## Details\n\n...",
  notebookGuid: "<notebook-guid>",  // optional
  tags: ["research", "topic", "2025-01"]
})
```

### Content Formatting

Evernote accepts Markdown which is converted to ENML:

```markdown
# Heading 1
## Heading 2

**Bold** and *italic* text

- Bullet list
- Another item

1. Numbered list
2. Second item

> Blockquote

`inline code`

    code block

[Link text](https://example.com)
```

### Save Web Research

When saving research from web sources:

```javascript
mcp__evernote__evernote_create_note({
  title: "[Article Title] - Web Clip",
  content: `## Source
[Original URL](https://example.com/article)

## Summary
Key points from the article...

## Quotes
> Important quote from the source

## My Notes
Personal observations and thoughts...`,
  tags: ["web-clip", "topic", "source-site"]
})
```

## Phase 2: ORGANIZE (Structure Knowledge)

### List Notebooks

```javascript
mcp__evernote__evernote_list_notebooks({})
```

Returns all notebooks with:

- GUID (for API operations)
- Name
- Stack (folder grouping)
- Note count

### Create Notebook

```javascript
mcp__evernote__evernote_create_notebook({
  name: "Project Alpha Research",
  stack: "Projects"  // optional folder grouping
})
```

### List Tags

```javascript
mcp__evernote__evernote_list_tags({})
```

### Update Note

Move notes between notebooks or update tags:

```javascript
mcp__evernote__evernote_update_note({
  guid: "<note-guid>",
  title: "Updated Title",
  content: "Updated content...",
  notebookGuid: "<new-notebook-guid>",
  tags: ["updated", "tags"]
})
```

## Phase 3: RETRIEVE (Find Information)

### Basic Search

```javascript
mcp__evernote__evernote_search_notes({
  query: "meeting notes project alpha",
  maxResults: 20,
  includeContent: true
})
```

### Advanced Search Syntax

Evernote supports powerful search operators:

```javascript
// Notes with specific tag
mcp__evernote__evernote_search_notes({
  query: "tag:project-alpha"
})

// Notes in specific notebook
mcp__evernote__evernote_search_notes({
  query: "notebook:Research important findings"
})

// Notes created in last week
mcp__evernote__evernote_search_notes({
  query: "created:week-1"
})

// Combine operators
mcp__evernote__evernote_search_notes({
  query: "tag:research notebook:Work created:month-1 machine learning"
})
```

### Search Operators Reference

| Operator | Example | Description |
| -------- | ------- | ----------- |
| `tag:` | `tag:work` | Notes with specific tag |
| `-tag:` | `-tag:archive` | Notes without tag |
| `notebook:` | `notebook:Personal` | Notes in notebook |
| `created:` | `created:day-7` | Created in timeframe |
| `updated:` | `updated:week-1` | Updated in timeframe |
| `intitle:` | `intitle:meeting` | Search title only |
| `source:` | `source:web.clip` | From specific source |
| `todo:` | `todo:true` | Notes with checkboxes |

### Get Full Note

```javascript
mcp__evernote__evernote_get_note({
  guid: "<note-guid>",
  includeContent: true
})
```

## Organization Best Practices

### Notebook Structure

```text
Notebooks/
├── Inbox/              # Quick capture, process later
├── Projects/
│   ├── Project Alpha/
│   ├── Project Beta/
│   └── Archive/
├── Reference/
│   ├── Technical/
│   ├── Personal/
│   └── Templates/
└── Journal/
```

### Tagging Strategy

Use consistent tag prefixes:

- `project-*` - Project names
- `type-*` - Note type (meeting, research, idea)
- `status-*` - Status (active, done, review)
- `YYYY-MM` - Date tags for temporal queries

### Note Title Format

```text
[Type] Topic - YYYY-MM-DD

Examples:
[Meeting] Product Roadmap Review - 2025-01-15
[Research] Machine Learning Best Practices - 2025-01-10
[Idea] New Feature Concept - 2025-01-08
```

## Health Check

Verify Evernote connection:

```javascript
mcp__evernote__evernote_health_check({})
```

## Best Practices

### Do

- Use consistent notebook and tag structure
- Add date tags for temporal searching
- Include source links in research notes
- Write summaries at the top of long notes
- Use headings to structure content
- Tag liberally for discoverability

### Don't

- Create deeply nested notebook hierarchies
- Use tags inconsistently
- Skip the summary on long research notes
- Store sensitive credentials in notes
- Let the Inbox pile up unprocessed
