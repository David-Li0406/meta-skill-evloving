---
name: resolve_canon_sources
description: Resolves the source hierarchy (Custom > Template)
version: 1.1.0
author: Antigravity
---

# Operational Instructions

## Trigger
- At the start of `tech_rag` (Step 0 Internal Context Discovery).
- At the start of `research_rag` (Step 0 Internal Canon Check).
- Whenever it's necessary to establish the "Gold Source" of truth.

## Inputs
- **Environment**: Local file system.
- **Constraints**: None.

## Steps
1. **Primary Check**: Verify existence of `docs_custom/SOURCES.md`.
2. **Fallback Check**: If Custom doesn't exist, use `.agent/docs/SOURCES.md`.
3. **Execution**:
   - Read the identified file (`view_file`).
   - If the topic is "Gold" (defined in the file), activate `markdownify` for deep reading.
   - Otherwise proceed with `brave_search` if necessary.

## Outputs
- **Path**: The path of the identified source file.
- **Content**: The content read to use as context.

## Suggested Commands
```bash
ls -F docs_custom/SOURCES.md 2>/dev/null || ls -F .agent/docs/SOURCES.md
```
