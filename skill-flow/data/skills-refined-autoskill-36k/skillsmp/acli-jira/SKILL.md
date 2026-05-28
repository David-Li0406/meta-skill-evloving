---
name: acli-jira
description: Full API reference for acli Jira interface. Use when working with Jira workitems, projects, or boards.
---

# ACLI Jira Interface

TypeScript interface for Jira automation via the `acli` CLI.

```typescript
import { acli } from "./agent-scripts";
```

## Workitems

### Search

```typescript
const result = await acli.workitem.search({ jql: "project = TEAM" });
const result = await acli.workitem.search({
  jql: "assignee = currentUser() AND status != Done",
});
```

### View

```typescript
const issue = await acli.workitem.view("TEAM-123");
// Returns: { key, summary, status, assignee, description, ... }
```

### Create

```typescript
await acli.workitem.create({
  project: "TEAM",
  type: "Task", // Task, Bug, Story, Epic, etc.
  summary: "Issue title",
  descriptionMarkdown: "# Overview\n\nThis is **bold** text.",
  // Optional fields:
  assignee: "username",
  labels: ["label1", "label2"],
  parent: "TEAM-100", // For subtasks
});
```

### Edit

```typescript
await acli.workitem.edit({
  key: "TEAM-123", // or ["TEAM-123", "TEAM-124"] for batch
  summary: "Updated title",
  descriptionMarkdown: "Updated description with *italic* text.",
  assignee: "newuser",
  labelsToAdd: ["new-label"],
  labelsToRemove: ["old-label"],
});
```

### Transition

```typescript
await acli.workitem.transition({ key: "TEAM-123", status: "In Progress" });
await acli.workitem.transition({ key: "TEAM-123", status: "Done" });
```

### Comments

```typescript
// Create a comment
await acli.workitem.comment.create({
  key: "TEAM-123",
  bodyMarkdown: "- Item 1\n- Item 2\n- Item 3",
});

// List comments
const comments = await acli.workitem.comment.list({ key: "TEAM-123" });
```

### Link Workitems

```typescript
await acli.workitem.link({
  key: "TEAM-123",
  targetKey: "TEAM-456",
  linkType: "blocks", // blocks, is blocked by, relates to, etc.
});
```

## Projects

```typescript
// List all projects
const projects = await acli.project.list();

// View project details
const project = await acli.project.view("TEAM");
```

## Boards

```typescript
// Search boards
const boards = await acli.board.search({ project: "TEAM" });

// View board details
const board = await acli.board.view(123);
```

## Markdown to ADF

All `descriptionMarkdown` and `bodyMarkdown` fields auto-convert markdown to Atlassian Document Format. You can also use the converter directly:

```typescript
import { markdownToAdf } from "./agent-scripts";

const adf = markdownToAdf("# Hello\n\n**bold** text");
```

### Supported Markdown

- Headings (`# H1` through `###### H6`)
- Bold (`**text**`), italic (`*text*`), strikethrough (`~~text~~`)
- Code (inline and fenced blocks with language)
- Lists (ordered and unordered, nested)
- Links (`[text](url)`)
- Blockquotes (`> quote`)
- Horizontal rules (`---`)
- Tables

## Source Files

For implementation details and types, read:

- `agent-scripts/lib/acli/index.ts` - Main exports
- `agent-scripts/lib/acli/workitem.ts` - Workitem operations
- `agent-scripts/lib/acli/project.ts` - Project operations
- `agent-scripts/lib/acli/board.ts` - Board operations
- `agent-scripts/lib/md-to-adf.ts` - Markdown converter
