---
name: obsidian
description: Help with Obsidian Zettelkasten vault management - search, create, and organize notes in the user's personal knowledge base with 993+ notes. Use when the user asks about their Zettelkasten, vault, notes, or knowledge management. (project, gitignored)
---

# Obsidian Zettelkasten Skill

## Overview

Help user interact with their personal Zettelkasten vault - a knowledge management system with 993+ notes covering their learning, projects, and ideas.

## Vault Location

**Path**: `~/Documents/Zettelkasten/`

## Vault Structure

```
Zettelkasten/
├── copilot/          # AI copilot files
├── Files/            # Attachments, images, PDFs
├── Reference/        # Reference materials
├── Templates/        # Note templates
└── Zettelkasten/     # Main notes directory
```

**Total notes**: 993+ markdown files

## Common Operations

### Using Obsidian MCP Server

**IMPORTANT**: Always use the Obsidian MCP tools instead of direct file operations:

- `mcp__obsidian__obsidian_list_notes` - List notes in directories
- `mcp__obsidian__obsidian_read_note` - Read note content
- `mcp__obsidian__obsidian_global_search` - Search across vault
- `mcp__obsidian__obsidian_update_note` - Create/update notes
- `mcp__obsidian__obsidian_manage_frontmatter` - Manage YAML frontmatter
- `mcp__obsidian__obsidian_manage_tags` - Manage tags

### Searching Notes

Use the MCP global search tool:

```
mcp__obsidian__obsidian_global_search with query, pageSize, etc.
```

### Creating Notes

**CRITICAL**: When creating notes via MCP, ALWAYS add frontmatter using this template:

```yaml
---
created: YYYY-MM-DD
type: note
tags: [(relevant tags go here, comma separated)]
related:
aliases:
---
```

**Process for creating notes**:

1. Ask where it should go (usually `Zettelkasten/Notes/` or `Zettelkasten/Life/`)
2. Ask for the filename
3. **ALWAYS include frontmatter** in the content with:
   - `created`: Current date in YYYY-MM-DD format
   - `type: note` (always)
   - `tags:` Intelligently populate based on note content/topic
   - `related:` Leave empty for user to fill
   - `aliases:` Leave empty for user to fill
4. Use `mcp__obsidian__obsidian_update_note` with the full content including frontmatter

**Why**: The MCP bypasses Obsidian's Templater plugin, so you must manually add frontmatter to match the user's template structure found in `Templates/Note Template.md`

### Reading Notes

When user references a note:

- Search for it by name/keyword
- Read the file
- Understand context and links

## Obsidian Features Available

The vault has these plugins installed:

- **dataview**: Query notes with SQL-like syntax
- **templater**: Dynamic templates
- **obsidian-vimrc-support**: Vim keybindings
- **quickadd**: Quick note creation
- **calendar**: Calendar view
- **excalibrain**: Visual knowledge graph
- And 17 more plugins

## When to Use This Skill

Use this skill when user:

- Asks to search their Zettelkasten
- Wants to create a new note
- References existing notes
- Asks about their knowledge base
- Wants to query/analyze their notes

## Best Practices

1. **Always ask before creating notes** - Don't assume structure
2. **Use search first** - Check if similar notes exist
3. **Respect user's organization** - Follow their existing patterns
4. **Suggest connections** - Link related notes when relevant
5. **Use templates** - If user has templates, use them

## Examples

**User asks**: "Search my notes for information about fish shell"

```bash
rg -i "fish shell" ~/Documents/Zettelkasten --type md
```

**User asks**: "Create a note about today's fish migration"

- Ask: Where? (Zettelkasten/ or Reference/?)
- Ask: What filename?
- Create with proper frontmatter/structure

**User asks**: "Do I have any notes on tmux?"

```bash
find ~/Documents/Zettelkasten -name "*tmux*.md"
# or
rg -i "tmux" ~/Documents/Zettelkasten --type md -l
```

## Important Notes

- This is the user's **personal knowledge base**
- Treat it with care - these are their thoughts and learnings
- Don't make assumptions about structure without asking
- The vault is their long-term memory, not Claude's

## Integration with Other Skills

This skill is separate from Claude's memory system (see memory skill).

- **This vault**: User's personal knowledge
- **Memory skill**: Claude's context about the user
- **Different purposes**: Don't confuse the two!
