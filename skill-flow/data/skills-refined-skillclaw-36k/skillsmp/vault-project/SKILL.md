---
name: vault-project
description: >
  Use when user wants to start a new project or create project structure.
  Triggered when intention involves beginning organized work with clear goals.
  Creates project folder with CLAUDE.md and _index.md.
---

# Vault Project

## Behavior

1. Get project name from user (or infer from context)
2. Generate project ID: lowercase, hyphenated (e.g., `marketing-campaign`)
3. Create folder: `01_Projects/{project-id}/`
4. Create `_index.md` using template from `${CLAUDE_PLUGIN_ROOT}/templates/tpl-project.md`
5. Create `CLAUDE.md` using template from `${CLAUDE_PLUGIN_ROOT}/templates/tpl-project-claude.md`

## Project ID Rules

- Lowercase letters and hyphens only
- Max 30 characters
- Descriptive but concise
- Examples: `website-redesign`, `q1-marketing`, `learn-rust`

## Frontmatter for _index.md

```yaml
---
type: project
project: {project-id}
status: active
created: {YYYY-MM-DD}
due:
tags: []
---
```

## Project Structure

```
01_Projects/{project-id}/
├── CLAUDE.md      # Project-specific context for Claude
├── _index.md      # Project overview and status
└── (future notes)
```

## After Creation

- Confirm project structure created
- Show the created files
- Ask for:
  - Project objective ("What does done look like?")
  - Key results or milestones
  - Due date if applicable
  - Initial context Claude should know

## Project CLAUDE.md Content

Include:
- Project overview
- Definition of done
- Key files description
- Project-specific conventions
- Related resources or areas
