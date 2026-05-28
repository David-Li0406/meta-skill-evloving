---
name: vault
description: Use this skill when you want to read and write notes in your Obsidian vault for task logs, knowledge capture, and building context.
---

# Skill body

## Location
`~/Documents/Notes/`

## Principles
1. **Obsidian vault for documents** - Detailed notes, task logs, project context.
2. **Unix tools for fast search** - Use `ripgrep` (rg), `fd`, or `mdfind` for efficient content searching.
3. **WikiLinks for connections** - Build a traversable knowledge graph.
4. **ALWAYS**: New tasks should be in an `open` state.

## Templates
- `templates/knowledge-note.md` - For knowledge notes.
- `templates/task.md` - For new tasks.

## Bash Commands
```bash
# List in-progress tasks
rg --type md -l "^status:\s*in-progress" ~/Documents/Notes/Projects/*/Tasks

# Find project directory (handles YYYY[-MM] prefix)
fd -t d -d 1 -i "<project>" ~/Documents/Notes/Projects

# List project task files
fd -e md . ~/Documents/Notes/Projects/*<project>*/Tasks

# Find files by name
fd -e md -i "<name>" ~/Documents/Notes

# Recently modified (last 7 days)
fd -e md --changed-within 7d ~/Documents/Notes

# Find with Spotlight index
mdfind -interpret -onlyin ~/Documents/Notes "<concept>"
```

## Timestamps
Always use real timestamps, never placeholders:
```bash
# For task filename: YYYY-MM-DD HHMMSS
date +"%Y-%m-%d %H%M%S"

# For log entry header: YYYY-MM-DD HH:MM
date +"%Y-%m-%d %H:%M"

# For frontmatter (ISO-8601)
date -Iseconds
```

## Task File Path
`~/Documents/Notes/Projects/<YYYY[-MM] Project>/Tasks/<YYYY-MM-DD HHMMSS> <Title>.md`

## Linking Strategy
> Link if it improves the note, not just because it matches a term.

### What to search for
| Search for | Example (if writing about "Unison abilities") |
|------------|-----------------------------------------------|
| Direct terms | "abilities", "Unison abilities" |
| Parent concepts | "effect handlers", "functional programming" |
| Sibling techniques | "monads", "algebraic effects" |
| Tools/tech used | "UCM", "Jit" |

### Linking workflow
1. **Semantic discovery** — Use `mdfind -interpret` for related concepts.
2. **Backlinks** — Use `rg "\[\[<concept>"` to find what links to your topics.
3. **Tags overlap** — Use `rg "^  - <tag>$"` for notes sharing tags.
4. Add discovered notes as WikiLinks using breadcrumb pattern: `[[Parent]] | [[Related]]`.

## Capture Heuristics
**Worth capturing when:**
| Marker | Trigger |
|--------|---------|
| 📋 | Principle applies across multiple contexts |
| 🤔 | Caused debugging time or surprised me |
| ⚙️ | Method that... |