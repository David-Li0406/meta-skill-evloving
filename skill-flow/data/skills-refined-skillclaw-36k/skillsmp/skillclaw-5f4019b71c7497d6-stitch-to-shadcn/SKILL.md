---
name: stitch-to-shadcn
description: Use this skill to convert Google Stitch HTML exports into reusable shadcn/ui React components when provided with HTML file paths from stitch.withgoogle.com.
---

# Stitch HTML to shadcn/ui Component Converter

Convert Google Stitch design exports into production-ready, reusable React components using shadcn/ui as the foundation.

## Prerequisites

Before starting conversion:
1. **shadcn MCP must be available** - Query it before implementing ANY shadcn component.
2. **Project has shadcn/ui installed** - Components will import from `@/components/ui`.
3. **cn() utility exists** - From `@/lib/utils` (tailwind-merge + clsx).

## Quick Start

```
User: Convert this Stitch HTML at ./exports/dashboard.html to shadcn components
```

1. Read the HTML file at the provided path.
2. Run the 4-phase workflow below.
3. Output organized TypeScript components.

## Workflow Overview

| Phase | Focus | Output |
|-------|-------|--------|
| 0. Extract | Theme tokens, icons, custom CSS | `globals.css`, icon inventory |
| 1. Audit | Analyze HTML, identify patterns | Component inventory |
| 2. Atoms | Smallest units (buttons, inputs) | `@/components/ui/*` |
| 3. Molecules | Composed atoms (cards, form fields) | `@/components/*` |
| 4. Organisms | Complex sections (sidebars, tables) | `@/components/*` |

---

## Phase 0: Theme & Asset Extraction

**Objective:** Extract design tokens before component work.

### Steps

1. **Parse Tailwind config** - Find `<script id="tailwind-config">` block, extract custom colors.
2. **Map to CSS variables** - Convert Stitch colors to shadcn theme tokens in `globals.css`.
3. **Inventory icons** - List all `material-symbols-outlined` icons, map to Lucide equivalents.
4. **Extract custom CSS** - Move `<style>` block utilities to `globals.css` or Tailwind config.

### Theme Token Mapping

```css
/* globals.css - map Stitch colors to shadcn tokens */
:root {
  --background: 222.2 84% 4.9%;      /* Stitch: background-main */
  --foreground: 210 40% 98%;         /* Stitch: text-main */
  --primary: 142 71% 45%;            /* Stitch: primary */
  --muted-foreground: 215 20% 65%;   /* Stitch: text-dim */
  --border: 217 33% 17%;              /* Stitch: border */
}
```

## Phase 1: Audit

1. Scan HTML for repeating patterns.
2. Classify using atomic design principles.
3. Output an inventory table:

```
| Pattern | Count | Classification | shadcn Mapping |
|---------|-------|----------------|----------------|
```

## Phase 2: Build Atoms

- Query shadcn MCP first.
- Use CVA for variants.
- Forward `className` via `cn()`.
- Use `React.forwardRef` for DOM access.
- `"use client"` only if interactive.

## Phase 3: Build Molecules

- Compose atoms from `@/components/ui`.
- Use generic props, no hardcoded data.
- Create compound patterns for multi-part components.

## Phase 4: Build Organisms

- Compose molecules/atoms.
- Use generic interfaces with `<T>`.
- Manage internal UI state only (no data fetching).
- Support loading/error/empty states.

## Batch Processing

**CRITICAL:** Scan ALL files before creating ANY component.

### Phase A: Global Audit

1. List all HTML files.
2. Scan each → extract patterns + variants + theme.
3. Build a **master inventory** with deduplication:

```
| Component | Variants | Files | Action |
|-----------|----------|-------|--------|
| Button | default, ghost, outline | file1, file2, file3 | CREATE |
```

### Phase B: Theme Consolidation

Merge all Tailwind configs into a single `globals.css`.

### Phase C: Deduplicated Creation

Before each component creation, ensure no duplicates exist.