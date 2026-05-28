---
name: stitch-to-shadcn
description: Convert Google Stitch HTML exports into reusable shadcn/ui React components. Use when user provides HTML file paths exported from stitch.withgoogle.com and needs TypeScript React components with CVA variants, proper props interfaces, and atomic design organization. Supports single files OR batch processing. Triggers on "convert Stitch HTML", "Stitch to shadcn", or mentions of Google Stitch exports.
---

# Stitch HTML → shadcn/ui Converter

## Prerequisites

1. Query **shadcn MCP** before implementing ANY component
2. Project has shadcn/ui installed (`@/components/ui`)
3. `cn()` utility exists (`@/lib/utils`)

## Mode Selection

| Mode | Trigger | Workflow |
|------|---------|----------|
| **Single** | 1 HTML file | Phases 0→1→2→3→4 sequentially |
| **Batch** | Multiple files | Phase 0-1 on ALL files first, dedupe, then 2→3→4 |

---

## Single File Workflow

### Phase 0: Extract Theme
1. Find `<script id="tailwind-config">` → extract colors
2. Map to CSS variables in `globals.css`
3. List `material-symbols-outlined` icons → map to Lucide (see [component-mapping.md](references/component-mapping.md))

### Phase 1: Audit
1. Scan HTML for repeating patterns
2. Classify using [atomic-design.md](references/atomic-design.md)
3. Output inventory table:

```
| Pattern | Count | Classification | shadcn Mapping |
|---------|-------|----------------|----------------|
```

### Phase 2: Build Atoms
- Query shadcn MCP first
- Use CVA for variants (see [cva-patterns.md](references/cva-patterns.md))
- Forward `className` via `cn()`
- `React.forwardRef` for DOM access
- `"use client"` only if interactive

### Phase 3: Build Molecules
- Compose atoms from `@/components/ui`
- Generic props, no hardcoded data
- Compound pattern for multi-part components

### Phase 4: Build Organisms
- Compose molecules/atoms
- Generic interfaces with `<T>`
- Internal UI state only (no data fetching)
- Support loading/error/empty states

---

## Batch Workflow

**CRITICAL:** Scan ALL files before creating ANY component.

### Phase A: Global Audit
1. List all HTML files
2. Scan each → extract patterns + variants + theme
3. Build **master inventory** with deduplication:

```
| Component | Variants | Files | Action |
|-----------|----------|-------|--------|
| Button | default,ghost,outline | file1,file2,file3 | CREATE |
```

### Phase B: Theme Consolidation
Merge all tailwind configs → single `globals.css`

### Phase C: Deduplicated Creation
Before each component:
1. Check inventory → already marked CREATE?
2. Check filesystem → file exists?
3. If exists with same variants → **SKIP**
4. If exists with new variants → **EXTEND**
5. If doesn't exist → **CREATE**

### Deduplication Rules

| Scenario | Action |
|----------|--------|
| Doesn't exist | CREATE |
| Exists, same variants | SKIP |
| Exists, new variants | EXTEND existing |
| Similar, different purpose | CREATE with new name |

---

## Output Structure

```
src/components/
├── ui/           # Atoms
├── [molecules]   # Composed atoms
├── [organisms]   # Major sections
└── layouts/      # Page structures
```

---

## References

- [cva-patterns.md](references/cva-patterns.md) - CVA variant patterns
- [component-mapping.md](references/component-mapping.md) - HTML→shadcn mapping, icon conversion
- [atomic-design.md](references/atomic-design.md) - Classification rules
