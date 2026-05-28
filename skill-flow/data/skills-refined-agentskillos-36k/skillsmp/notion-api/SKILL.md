---
name: notion-api
description: Interact with Notion project boards via the Notion API. Use when Claude needs to list, read, create, or update tickets/items on a Notion project board, change ticket status, or filter items by state or project. Supports querying databases, reading page content, updating properties, and creating new items.
---

# Notion API Skill

Interact with Notion project boards to manage tickets and tasks.

## Prerequisites

- `NOTION_API_KEY` environment variable set with an integration token from https://www.notion.so/my-integrations
- `tsx` in PATH (install globally: `pnpm add -g tsx`)
- The integration must be connected to the workspace containing the target databases

## Vessel Workspace Databases

| Database | ID                                 | Description                 |
| -------- | ---------------------------------- | --------------------------- |
| Tasks    | `a5a500207a95402fad259d6487646cef` | Main tasks/tickets database |

### Quick Commands for Vessel Tasks

```bash
# List tasks in a project
~/.claude/skills/notion-api/scripts/list-items.ts --database a5a500207a95402fad259d6487646cef --project "Autonomous Reporting Extraction"

# List tasks by status
~/.claude/skills/notion-api/scripts/list-items.ts --database a5a500207a95402fad259d6487646cef --status "Not Started"

# Read a specific task (accepts URL or ID)
~/.claude/skills/notion-api/scripts/read-item.ts --page 'https://www.notion.so/vesselfunds/Task-Name-abc123'
```

## Available Scripts

All scripts are in `~/.claude/skills/notion-api/scripts/` and directly executable (require `tsx` in PATH).

**All scripts accept Notion URLs or raw IDs** - they auto-extract the ID from URLs.

| Script              | Purpose                                |
| ------------------- | -------------------------------------- |
| `list-items.ts`     | List/filter items from a database      |
| `read-item.ts`      | Read full content of a page            |
| `create-item.ts`    | Create new item in database            |
| `update-item.ts`    | Update page properties                 |
| `change-status.ts`  | Change status of an item               |
| `delete-item.ts`    | Delete (archive) a page                |
| `append-content.ts` | Add markdown content to a page         |
| `manage-blocks.ts`  | List/delete/update page blocks         |
| `add-comment.ts`    | Add a comment to a page                |
| `batch.ts`          | Batch operations (export, status)      |
| `page-to-md.ts`     | Save page as markdown file             |
| `append-task.ts`    | Create task with due date              |
| `search-pages.ts`   | Search pages by keyword                |
| `sync-changes.ts`   | Sync pages to local markdown folder    |
| `export-db.ts`      | Export database as CSV/MD/JSON         |
| `clone-page.ts`     | Deep clone page content                |
| `track-progress.ts` | Summarize status of database items     |
| `quick-note.ts`     | Rapidly create page with title+content |

## Quick Reference

### List items with filters

```bash
~/.claude/skills/notion-api/scripts/list-items.ts --database <DB_ID|URL> [--status "Done"] [--project "SOC 2"] [--limit 20]
```

### Read item content

```bash
~/.claude/skills/notion-api/scripts/read-item.ts --page <PAGE_ID|URL>
```

### Update item properties

```bash
~/.claude/skills/notion-api/scripts/update-item.ts --page <PAGE_ID|URL> --property Status --value "Done"
~/.claude/skills/notion-api/scripts/update-item.ts --page <PAGE_ID|URL> --title "New title"
```

### Create new item

```bash
~/.claude/skills/notion-api/scripts/create-item.ts --database <DB_ID|URL> --title "Task name" [--status "Not Started"] [--assign "Person Name"]
```

### Change status

```bash
~/.claude/skills/notion-api/scripts/change-status.ts --page <PAGE_ID|URL> --status "Done"
```

### Delete a page

```bash
~/.claude/skills/notion-api/scripts/delete-item.ts --page <PAGE_ID|URL>
```

### Add a comment

```bash
~/.claude/skills/notion-api/scripts/add-comment.ts --page <PAGE_ID|URL> "Your comment text"
```

### Append content to a page (markdown)

```bash
# Inline markdown (positional argument)
~/.claude/skills/notion-api/scripts/append-content.ts --page <PAGE_ID|URL> "# Hello World"

# From a file
~/.claude/skills/notion-api/scripts/append-content.ts --page <PAGE_ID|URL> --file content.md

# Pipe via stdin (NO --file flag, just pipe directly)
echo '# Heading' | ~/.claude/skills/notion-api/scripts/append-content.ts --page <PAGE_ID|URL>

# Heredoc via stdin (NO --file flag)
~/.claude/skills/notion-api/scripts/append-content.ts --page <PAGE_ID|URL> << 'EOF'
# Heading
- Bullet 1
- Bullet 2
EOF
```

**IMPORTANT:** Do NOT use `--file -` for stdin. The script auto-reads stdin when no `--file` or positional content is provided.

Supported markdown: `# h1`, `## h2`, `### h3`, `- bullets`, `1. numbered`, `> quotes`, `---` dividers, `code blocks`

### Manage page blocks

```bash
# List all blocks with their IDs
~/.claude/skills/notion-api/scripts/manage-blocks.ts --page <PAGE_ID|URL> --action list

# Delete a block
~/.claude/skills/notion-api/scripts/manage-blocks.ts --page <PAGE_ID|URL> --action delete --block <BLOCK_ID>

# Update block text
~/.claude/skills/notion-api/scripts/manage-blocks.ts --page <PAGE_ID|URL> --action update --block <BLOCK_ID> --text "New text"
```

### Batch operations

```bash
# Export all items to JSON
~/.claude/skills/notion-api/scripts/batch.ts export --database <DB_ID|URL> --output backup.json

# Mark filtered items as done
~/.claude/skills/notion-api/scripts/batch.ts mark-done --database <DB_ID|URL> --filter-status "In Progress"

# Count items by status
~/.claude/skills/notion-api/scripts/batch.ts count --database <DB_ID|URL>
```

### Page to Markdown

```bash
# Save to file
~/.claude/skills/notion-api/scripts/page-to-md.ts --page <PAGE_ID|URL> --output notes.md

# Include properties in output
~/.claude/skills/notion-api/scripts/page-to-md.ts --page <PAGE_ID|URL> --include-properties > page.md
```

### Append Task (with due date)

```bash
~/.claude/skills/notion-api/scripts/append-task.ts --database <DB_ID|URL> --title "Review PR" --due 2025-01-15

# With date range
~/.claude/skills/notion-api/scripts/append-task.ts -d <DB_ID> -t "Sprint" --due "2025-01-20 to 2025-01-24" --status "Not Started"
```

### Search Pages

```bash
~/.claude/skills/notion-api/scripts/search-pages.ts --query "meeting notes"

# Filter by type
~/.claude/skills/notion-api/scripts/search-pages.ts --query "Q4 planning" --filter page --limit 20
```

### Sync to Local

```bash
# Sync a page and subpages to local folder
~/.claude/skills/notion-api/scripts/sync-changes.ts --page <PAGE_ID|URL> --local ./docs

# Sync entire database
~/.claude/skills/notion-api/scripts/sync-changes.ts --database <DB_ID|URL> --local ./wiki --depth 3
```

### Export Database

```bash
# CSV export
~/.claude/skills/notion-api/scripts/export-db.ts --database <DB_ID|URL> --format csv --output tasks.csv

# Markdown export with content
~/.claude/skills/notion-api/scripts/export-db.ts --database <DB_ID|URL> --format md --output ./docs --include-content

# JSON export
~/.claude/skills/notion-api/scripts/export-db.ts --database <DB_ID|URL> --format json > backup.json
```

### Clone Page

```bash
# Clone to another database
~/.claude/skills/notion-api/scripts/clone-page.ts --page <PAGE_ID|URL> --target-db <DB_ID|URL>

# Clone as child of another page
~/.claude/skills/notion-api/scripts/clone-page.ts --page <PAGE_ID|URL> --target-page <PAGE_ID|URL>
```

### Track Progress

```bash
# Summary by status
~/.claude/skills/notion-api/scripts/track-progress.ts --database <DB_ID|URL>

# Group by different property
~/.claude/skills/notion-api/scripts/track-progress.ts --database <DB_ID|URL> --group-by "Priority"
```

### Quick Note

```bash
# Create in database
~/.claude/skills/notion-api/scripts/quick-note.ts --database <DB_ID|URL> --title "Meeting Notes" "Discussed roadmap"

# Create under page
~/.claude/skills/notion-api/scripts/quick-note.ts --page <PAGE_ID|URL> --title "Ideas" "Random thoughts"

# Pipe content
echo "Long content here" | ~/.claude/skills/notion-api/scripts/quick-note.ts -d <DB_ID> -t "From stdin"
```

## URL Handling

Scripts automatically extract IDs from Notion URLs:

```bash
# All of these work:
~/.claude/skills/notion-api/scripts/read-item.ts --page abc123def456
~/.claude/skills/notion-api/scripts/read-item.ts --page 'https://www.notion.so/workspace/Page-Title-abc123def456'
~/.claude/skills/notion-api/scripts/read-item.ts --page 'https://www.notion.so/workspace/Parent-Page-xxx?p=abc123def456'
```

## Property Types Reference

See [references/property-types.md](references/property-types.md) for handling different Notion property types when updating.

## Common Patterns

### Filter by multiple criteria

```bash
~/.claude/skills/notion-api/scripts/list-items.ts --database $DB_ID --status "Not Started" --project "SOC 2"
```

### Batch status update (using zx)

```typescript
import { $ } from "zx";
const pages = ["id1", "id2", "id3"];
for (const id of pages) {
  await $`~/.claude/skills/notion-api/scripts/change-status.ts --page ${id} --status "Done"`;
}
```

## Error Handling

Scripts exit with code 1 on error and print JSON error details. Common issues:

- `401`: Invalid or missing API key
- `404`: Page/database not found or not shared with integration
- `400`: Invalid property name or value format
