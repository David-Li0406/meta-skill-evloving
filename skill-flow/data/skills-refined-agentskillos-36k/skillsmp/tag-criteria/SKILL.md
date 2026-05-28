---
name: tag-criteria
description: This skill should be used when analyzing Obsidian notes for tagging, determining which tags apply to content, or understanding tag definitions and criteria. Provides the complete tag taxonomy with judgment criteria for the obsidian-tagger agent.
version: 0.2.0
---

# Obsidian Tag Criteria

Defines criteria for tagging Obsidian notes. Tags should only be assigned when content **clearly matches** the criteria.

## Judgment Rules

1. **Clarity Principle**: Only assign tags when content clearly matches the definition
2. **Multiple Tags Allowed**: Assign all applicable tags (e.g., arXiv paper -> #papers #arxiv)
3. **No Tag is OK**: Do not assign any tag if none clearly match
4. **Preserve Existing Tags**: Do not delete or modify existing tags
5. **Avoid Duplicates**: Do not add tags that already exist
6. **Folder Path Rule**: If the file path contains a folder name semantically matching a tag (e.g., `3d-reconstruction/`), automatically apply that tag
   - Match folder names to tag names (with or without `#` prefix, hyphens normalized)
   - When ambiguous, prefer the more specific tag or skip folder-based tagging
   - Examples:
     - `3d-reconstruction/note.md` -> `#3d-reconstruction`
     - `papers/summary.md` -> `#papers`
     - `ai-tools-info/guide.md` -> `#ai-tools`
