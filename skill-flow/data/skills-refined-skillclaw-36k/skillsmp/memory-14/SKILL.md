---
name: memory
description: Manage long-term memories using date-based files. Allows creating, listing, and reading memories.
---

# Memory Skill

This skill allows you to manage long-term memories in `docs/memories/`.
It uses the `scripts/memory.py` utility.

## Commands

### Create Memory
Create a new memory file.
Command: `python3 scripts/memory.py create "<title>" "<content>" [--tags "tag1,tag2"] [--format json]`

### List Memories
List recent memories, optionally filtered by tag.
Command: `python3 scripts/memory.py list [--tag <tag>] [--limit <limit>] [--format json]`

### Read Memory
Read a specific memory file.
Command: `python3 scripts/memory.py read <filename_or_slug> [--format json]`

## Usage Instructions
- Use `create` to store important architectural decisions, lessons learned, or long-term context.
- Use `list` to recall past memories.
- Use `read` to get the full content of a memory.
- Memories are stored as Markdown files with YAML frontmatter.
