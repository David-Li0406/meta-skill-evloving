---
name: obsidian
description: DEPRECATED - Use the journal and notes skills instead
---

# Obsidian Integration (DEPRECATED)

**This skill is deprecated.** Use the new skill architecture instead:

- **`journal` skill** - For temporal/experiential entries with mood/energy tracking
- **`notes` skill** - For topical reference documentation and knowledge base

## What Changed

The old system mixed two types of content (temporal experiences + topical reference docs) in daily journal files. The new system separates them:

**Journal skill:**
- Captures how you felt, the experience of work, emotional context
- One file per day with time-stamped mood/energy entries
- Location: `~/dev/captains-log/journal/` ← **Still actively used**
- Temporal discovery: "How did I feel when..."

**Notes skill:**
- Captures what you know, technical details, reference material
- Topic-based files (no dates in filename)
- Location: `~/dev/captains-log/notes/` ← **New directory**
- Topical discovery: "What do I know about..."

Both skills support bidirectional linking for connecting experiences to knowledge.

## Legacy Folders

Old reference documentation exists in:
- `~/dev/captains-log/personal/` - Personal reference docs (no longer used)
- `~/dev/captains-log/zylo/` - Work reference docs (no longer used)

**These folders are deprecated.** New reference content goes in `notes/`.

The `journal/` folder continues to be actively used for daily journal entries.

## Migration

No immediate action needed. The new skills will create properly separated content going forward:
- Daily journal entries → `journal/` (journal skill)
- Reference documentation → `notes/` (notes skill)

Old reference docs in `personal/` and `zylo/` remain as reference but won't receive new content.
