---
name: vscode-tasks-organizer
description:
  Guide for creating or modifying VS Code tasks.json files with a focus on
  developer experience.
metadata:
  author: garnertb
  version: "1.1"
---

This skill helps you organize VS Code `tasks.json` files for consistency and
developer experience improvements.

## Analysis Steps

1. **Check for available scripts** Check for common task types: dev/run, build,
   test, lint, format in the language ecosystem (eg JavaScript/TypeScript check
   `package.json` scripts)
2. **Identify inconsistencies** in the task.json analyze property ordering,
   naming conventions, and missing properties. The output should be a list of
   recommended improvements to ensure consistency and enhance developer
   experience.
3. **Review task grouping** — VS Code supports `build`, `test`, or `none` groups

## Improvements to Apply

### Property Ordering

Standardize all tasks with consistent property order: `label` → `type` →
`command` → `group` → `icon` → `detail` → `options` → `problemMatcher`

### Naming Conventions

- Use consistent label format (e.g., `Title Case`)
- Match casing across all tasks

### Icons

All tasks should have an icon, if already present ensure consistency in style
and color (based on task category) and that the icon is appropriate and
intuitive.

If missing, add semantic icons with appropriate colors using these defaults:

- **Dev/Run tasks**: green (`terminal.ansiGreen`) with `run` or `globe` icons
- **Build tasks**: cyan (`terminal.ansiCyan`) with `tools` icon
- **Test tasks**: magenta (`terminal.ansiMagenta`) with `beaker`, `browser`, or
  `eye` icons
- **Lint tasks**: yellow (`terminal.ansiYellow`) with `search` icon
- **Format tasks**: blue (`terminal.ansiBlue`) with `symbol-color` or `wand`
  icons

### Details

Add descriptive `detail` text explaining each task's purpose

### Problem Matchers

Add appropriate problem matchers for error detection based on language ecosystem
and task type:

- JavaScript/TypeScript: `$tsc`, `$eslint-stylish`

### Cleanup

- Remove redundant `options.cwd` if defaulting to workspace folder
- Fix any JSON syntax errors (trailing commas, etc.)
