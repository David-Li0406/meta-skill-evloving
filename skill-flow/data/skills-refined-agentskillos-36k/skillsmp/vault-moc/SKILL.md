---
name: vault-moc
description: >
  Use when user wants to structure or organize knowledge on a topic.
  Triggered when intention involves creating overview, index, or knowledge map.
  Creates or updates Map of Content in 05_MOC.
---

# Vault MOC

## Behavior

1. Identify topic from user request
2. Search for related notes:
   - By tag (e.g., `ai/agents`)
   - By folder (e.g., `03_Resources/AI/`)
   - By content keywords
3. Create or update MOC file: `05_MOC/{topic}-MOC.md`
4. Organize found notes into logical structure

## Frontmatter

```yaml
---
type: moc
topic: {topic}
scope: {folders/tags covered}
last_generated: {YYYY-MM-DD}
tags: []
---
```

## MOC Structure Template

```markdown
# {Topic} MOC

## Overview
{What this topic covers and why it matters}

## Core Concepts
- [[note1]] - brief description
- [[note2]] - brief description

## Key Notes
### {Subtopic 1}
- [[note]] - description

### {Subtopic 2}
- [[note]] - description

## Questions to Explore
- {Open questions or gaps in knowledge}

## Related MOCs
- [[other-MOC]]
```

## Organization Logic

1. **Group by subtopic** - cluster related notes
2. **Order by importance** - core concepts first
3. **Add descriptions** - brief context for each link
4. **Identify gaps** - note missing areas

## Linking Format

Use Obsidian wiki-link format:
- `[[note-name]]` for same folder
- `[[folder/note-name]]` for cross-folder

## Update vs Create

- If MOC exists: update with new notes, preserve manual edits
- If new: create fresh structure
- Always update `last_generated` date
