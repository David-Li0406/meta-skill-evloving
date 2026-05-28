---
name: understand-project-structure
description: Load project context before making changes. Use when starting work to check available element kinds, relationship types, and tags.
---

# Understand Project Structure

Use this skill when starting work on a LikeC4 project or before making significant changes.

## C4 Framework Foundation

Before understanding the project, familiarize yourself with the C4 model:
- Read the `c4-modeling-process` skill to understand the methodology
- Understand how architecture is organized: C1 Context → C2 Container → C3 Component
- This project follows these conventions for all models

## Workspace Structure

- **Shared specifications:** `projects/shared/spec-*.c4` - Source of truth for element kinds, relationship types, and tags
- **MCP servers (REQUIRED):** Use LikeC4 MCP and Context7 MCP for context gathering
- **ADR documentation:** `ADR/` directory - System architecture decisions using standard ADR format

## Steps

1. **C4 Context (REQUIRED):** Read `c4-modeling-process` skill to understand design hierarchy
2. **Use LikeC4 MCP (REQUIRED):** `list-projects` or `read-project-summary` to get project overview
3. Read `likec4.config.json` to understand includes and image aliases
4. Check `projects/shared/spec-*.c4` for available element kinds, relationship types, and tags
5. Review existing model files to understand current C1/C2/C3 architecture
6. **Use Context7 MCP:** Query LikeC4 documentation if uncertain about syntax or features

## Output

- Understanding of C4 framework and top-to-bottom design approach
- Complete understanding of project structure and architecture
- Available element kinds, relationship types, and tags
- Current C1/C2/C3 architecture organization
