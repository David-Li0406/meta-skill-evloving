---
name: idea-memo
description: Save and retrieve ideas, insights, and notes during conversation. Use when user mentions ideas worth remembering or asks to recall past ideas.
---

# Idea Memo - External Memory for Ideas

This is `${CLAUDE_PLUGIN_ROOT}/skills/idea-memo/SKILL.md`
Scripts: `${CLAUDE_PLUGIN_ROOT}/skills/idea-memo/scripts/`
Data: `~/.local/share/idea-storage/ideas/`

## Overview

An external memory system for storing and retrieving ideas, insights, plans, and notes.
Automatically records noteworthy items from conversations and makes them searchable.

## Data Structure

```
~/.local/share/idea-storage/
├── ideas/
│   ├── YYYY-MM-DD/
│   │   └── YYYY-MM-DDTHH-MM-SS-{slug}.md
│   └── index.json  # Searchable index
└── config.json     # User preferences
```

## Idea File Format

```markdown
---
id: {uuid}
title: {title}
created: {ISO8601}
updated: {ISO8601}
tags: [tag1, tag2]
status: draft|active|archived
---

{content}
```

## Scripts

| Script | Description |
|--------|-------------|
| `save.sh <title> [tags...]` | Save new idea (reads content from stdin) |
| `list.sh [-n N] [-t tag] [-s status]` | List ideas with filters |
| `search.sh <query>` | Full-text search ideas |
| `get.sh <id-or-slug>` | Get idea by ID or slug |
| `update.sh <id> [--status S] [--tags T]` | Update idea metadata |

## Usage Guidelines

1. **When to save**: User mentions "idea", "remember this", "note to self", or discusses plans
2. **Auto-tagging**: Infer tags from context (project names, topics, etc.)
3. **Title generation**: Create concise, searchable titles from content
4. **Status flow**: draft → active → archived

## Example Workflow

```bash
# Save a new idea
echo "Consider using SQLite for local caching" | \
  bash ${CLAUDE_PLUGIN_ROOT}/skills/idea-memo/scripts/save.sh \
    "SQLite local cache" project:myapp performance

# Search ideas
bash ${CLAUDE_PLUGIN_ROOT}/skills/idea-memo/scripts/search.sh "cache"

# List recent ideas
bash ${CLAUDE_PLUGIN_ROOT}/skills/idea-memo/scripts/list.sh -n 5
```
