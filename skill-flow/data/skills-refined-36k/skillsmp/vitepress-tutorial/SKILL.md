---
name: vitepress-tutorial
description: Generate VitePress documentation sites for source code learning and analysis. Use when creating tutorials that explain how a codebase is implemented internally.
---

# VitePress Source Tutorial Generator

Generate VitePress documentation sites for source code learning and analysis.

## Overview

This skill creates standalone VitePress tutorial sites that teach developers how a codebase works internally. Unlike user documentation that explains "how to use", these tutorials explain "how it's implemented".

## Usage

```
/vitepress-tutorial [source-path] [output-path]
```

**Examples:**
- `/vitepress-tutorial ./apps/runner ./tutorials/runner-guide`
- `/vitepress-tutorial ./pkg/sandbox`

## Workflow

### Phase 1: Analysis

1. Explore the specified source directory
2. Identify key components, patterns, and architecture
3. Map dependencies and data flows
4. Output: Module inventory and architecture overview

**User checkpoint**: Confirm scope and focus areas

### Phase 2: Planning

1. Generate tutorial outline based on analysis
2. Determine chapter structure and navigation
3. Identify code sections to highlight
4. Output: Tutorial structure document

**User checkpoint**: Approve outline before generation

### Phase 3: Generation

1. Create VitePress project skeleton using @project-structure.md
2. Configure VitePress using @config-template.md
3. Generate tutorial content following @content-guidelines.md
4. Build and verify

## Output Structure

```
{output-path}/
├── package.json
├── docs/
│   ├── .vitepress/
│   │   └── config.ts
│   ├── index.md              # Homepage
│   ├── introduction/
│   │   ├── overview.md       # Project overview
│   │   └── architecture.md   # Architecture diagram
│   └── {modules}/            # One directory per module
│       ├── index.md
│       └── {topics}.md
└── README.md
```

## Features

- **Source References**: Auto-generate `Source: path/to/file.go:123` annotations
- **Mermaid Diagrams**: Architecture, sequence, and flow diagrams
- **Code Highlighting**: Go, TypeScript, Python with line highlighting
- **Chinese-first**: Content in Chinese, code comments in English
- **Standalone Deploy**: Ready for Vercel, Netlify, or GitHub Pages

## Configuration

The skill reads project context to customize output:

| Context | Effect |
|---------|--------|
| Go project | Uses Go code blocks, references `.go` files |
| TypeScript | Uses TS blocks, references `.ts/.tsx` files |
| Monorepo | Detects `apps/`, `packages/` structure |

## Instructions

When executing this skill:

1. **Always explore first** - Read source files before writing tutorials
2. **Reference actual code** - Include real code snippets with file paths
3. **Use Mermaid for architecture** - Visual diagrams aid understanding
4. **Keep chapters focused** - One concept per file, ~200-400 lines
5. **Link between chapters** - Use VitePress prev/next navigation
6. **Include API tables** - Summarize endpoints, functions, types
