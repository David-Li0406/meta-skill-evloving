---
name: notes
description: Topical knowledge base with technical documentation and reference materials
---

# Knowledge Notes

Manages topical reference documentation and knowledge base content. Notes are time-invariant - organized by topic, not by date. They capture what you know, not when you learned it.

## Notes Location

```
~/dev/captains-log/notes/
```

Currently uses a flat directory structure. Can be organized into subdirectories if it becomes unmanageable.

## File Naming Convention

Note files are named with descriptive titles:

```
{Descriptive Title}.md
```

**Naming guidelines:**
- Use proper case with spaces (Obsidian standard)
- Time-invariant (no dates in filename)
- Descriptive and topic-focused
- Easy to search and discover

**Examples:**
- `PostgreSQL UUID7 Migration.md`
- `Docker Compose Version Migration.md`
- `Webhook Race Condition Debugging.md`
- `Audi A5 Maintenance Log.md`

## Note Format

Notes follow this structure:

```markdown
# {Note Title}

{Content sections - flexible based on content type}

---

## References

- [[{YYYY-MM-DD} - {Animal Name}#{HH:MM} - {Section Title}]]
- [[{YYYY-MM-DD} - {Animal Name}#{HH:MM} - {Section Title}]]

---

_Tags:_ #alphabetized #tags
```

**Content sections are flexible** - adapt to the type of knowledge:

### Technical Documentation
```markdown
# PostgreSQL UUID7 Migration

Brief overview of what this is about.

## Implementation

- Step 1
- Step 2

## Gotchas

- Thing to watch out for

## Benefits

- Why this approach
```

### Reference Logs (e.g., car maintenance)
```markdown
# Audi A5 Maintenance Log

## 2025-12-15 - Oil Change

- Mileage: 45,230
- Oil: 5W-40 synthetic
- Filter: OEM
- Shop: Local Mechanic

## 2025-11-03 - Tire Rotation

- Mileage: 43,100
- All tires rotated and balanced
```

### Learning Notes
```markdown
# React Server Components

## Key Concepts

- What they are
- How they differ from client components

## Use Cases

- When to use server components
- When client components are needed

## Gotchas

- Common pitfalls
```

## Bidirectional Linking

Notes are connected to journal entries through backlinks in the References section.

**When a journal entry links to a note:**

Journal: `See [[Docker Compose Version Migration]] for details.`

This note's References section should contain:

```markdown
## References

- [[2025-12-29 - Debugging Dragon#09:34 - Docker Compose Deprecation]]
```

**Backlink format:**
```markdown
[[{YYYY-MM-DD} - {Adjective Animal}#{HH:MM} - {Section Title}]]
```

**Backlink ordering:** Chronological (oldest first)

## Creating New Notes

When creating a new note:

1. **Check for similar existing notes** - Use `Glob` and `Grep` to see if a related note already exists
2. **Make judgment call:**
   - Create new note if topic is distinct
   - Add to existing note if closely related
   - Ask user if uncertain
3. **Infer tags from content** - Identify relevant topics, technologies, projects
4. **Alphabetize tags** - Always maintain alphabetical order
5. **Create References section** - If created from a journal entry, add that backlink immediately

**Initial note template:**

```markdown
# {Note Title}

{Content}

---

## References

- [[{Journal backlink if applicable}]]

---

_Tags:_ #alphabetized #tags
```

## Updating Existing Notes

When updating a note:

1. **Read the existing note** to understand structure and content
2. **Add new content** in appropriate section (or create new section)
3. **Update References** if being linked from a new journal entry
4. **Maintain chronological order** in References section
5. **Update tags** if new topics are covered (maintain alphabetical order)
6. **Preserve** all existing content

## Backlink Maintenance

**When journal skill creates a link to a note:**

The journal skill will attempt to update the note's References section. However, the notes skill should also verify backlinks are correct when creating or updating notes.

**To check for missing backlinks:**

1. Search journal entries for `[[{Note Name}]]` using `Grep`
2. Compare found references to the note's References section
3. Add any missing backlinks in chronological order

## Tag Inference

Infer tags from:
- Technology names (postgres, docker, react, typescript)
- Project names (zylo, tcgtoolbox)
- Topic categories (debugging, migration, maintenance)
- Work vs personal context

**Examples:**

`PostgreSQL UUID7 Migration.md` → `#database #migration #postgres #tcgtoolbox`

`Docker Compose Version Migration.md` → `#docker #docker-compose #migration`

`Audi A5 Maintenance Log.md` → `#audi #a5 #car #maintenance #personal`

## Querying Notes

To help the user find knowledge:

| Query Type | Approach |
| ---------- | -------- |
| Find by topic | `Grep` for keywords in note content |
| Find by tag | `Grep` for `_Tags:_` lines containing tag |
| Find by technology | `Grep` for tech names in titles or content |
| List all notes | `Glob` for `notes/*.md` |
| Find notes referencing a journal | `Grep` for journal date pattern in References |

## Decision Making: New Note vs Update Existing

**Create new note when:**
- Topic is distinct and won't be confused with existing notes
- Content is substantial enough to stand alone
- You're confident it's a separate concern

**Update existing note when:**
- Very closely related to existing note
- Adding details or new learnings to the same topic
- Note already exists with similar title

**Ask user when:**
- Multiple existing notes could be relevant
- Uncertain whether content should be merged
- Existing note structure would need significant refactoring

**To make good decisions:**
- Read existing notes in the notes/ directory at session start
- Use `Glob` and `Grep` to understand what exists
- Look for title similarities and topic overlap

## Example Workflow

**User says:** "Document the Docker Compose version property deprecation issue I just hit"

**Claude decides:**
1. Checks if similar notes exist (searches for "docker", "compose")
2. Sees no existing note about this specific issue
3. Creates new note with content

**Creates:** `notes/Docker Compose Version Migration.md`

```markdown
# Docker Compose Version Migration

The `version` property in docker-compose.yml is deprecated as of Compose V2.

## Old Format

```yaml
version: '3.8'
services:
  ...
```

## New Format

```yaml
# No version property needed
services:
  ...
```

---

## References

_No journal references yet_

---

_Tags:_ #docker #docker-compose #migration
```

**If this was created during a journal entry that linked to it**, the References section would contain:

```markdown
## References

- [[2025-12-29 - Debugging Dragon#09:34 - Docker Compose Deprecation]]
```

## When to Use This Skill

**Use notes skill when:**
- Documenting technical details, solutions, or learnings
- Creating reference material to look up later
- User says "document this" or "save this for later"
- Content is factual without emotional context
- Creating knowledge that transcends a specific moment

**Don't use notes skill when:**
- User is expressing feelings or emotional state (use journal skill)
- Content is primarily about the experience vs the knowledge
- Brief updates that don't need permanent reference

## Relationship with Journal Skill

The notes skill complements the journal skill:

- **Journal:** Captures the temporal/experiential (when, how you felt, the journey)
- **Notes:** Captures the topical/knowledge (what, the solution, the reference)

They work together through bidirectional linking:
- Journal entries link to notes for details
- Notes show References back to journal entries for temporal context

## Legacy Folders

Old reference content exists in:
- `~/dev/captains-log/personal/` - Personal reference docs (deprecated)
- `~/dev/captains-log/zylo/` - Work reference docs (deprecated)

These folders are no longer actively used. New reference content goes in `notes/`.
