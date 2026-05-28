---
name: better-icons
description: Use this skill when you need to search and retrieve SVG icons from Iconify libraries for UI/UX projects or codebases.
---

# Better Icons

Search and retrieve icons from 200+ libraries via Iconify.

## When to Use

- You need SVG icons quickly from Iconify libraries.
- You want consistent icon families across UI or documentation.
- You need to batch fetch or sync icons into a project file.
- You want to use the MCP tools from an agent.

## Inputs

- **Search query** (string) and optional **collection prefix**.
- **Icon ID** (`prefix:name`).
- Optional **size** and **color** (use design tokens when available).
- **Output target path** (if writing a file).
- **Framework target** for `sync_icon` (e.g., React, Vue, Svelte).

## Outputs

- SVG output to stdout or a file.
- Search results (JSON list of icon IDs).
- Updated project icon file (when syncing).
- Collections list (when listing libraries).

## Constraints / Safety

- Redact sensitive file paths, project names, or proprietary terms from logs by default.
- Do not overwrite existing files without explicit confirmation.
- If icons are used for interactive controls, ensure a minimum 44x44 hit-area and align spacing/breakpoints to design tokens where applicable.

## Anti-Patterns

- Mixing icon styles (stroke vs solid) within the same UI surface.
- Using icons without text labels for critical actions.
- Hardcoding colors that ignore the design system.
- Fetching excessive icons without narrowing by prefix or use case.

## Procedure

1. Confirm the use case and icon style constraints.
2. Search by query (optionally with a prefix).
3. Select icon IDs that match the family and style.
4. Fetch SVGs with token-aligned size/color.
5. Sync into the project if needed.
6. Validate output and usage context.

## CLI Commands

```bash
# Search icons
better-icons search <query> [--prefix <prefix>] [--limit <n>] [--json]

# Get icon SVG (outputs to stdout)
better-icons get <icon-id> [--color <color>] [--size <px>] [--json]

# Setup MCP server for AI agents
better-icons setup [-a cursor,claude-code] [-s global|project]
```

## Examples

```bash
better-icons search arrow --limit 10
better-icons get lucide:home > icon.svg
better-icons get mdi:home --color '#333' --json
```

## Popular Collections

`lucide`, `mdi`, `heroicons`, `tabler`, `ph`, `ri`, `solar`, `iconamoon`