# File Structure Reference

## Directory Organization

### PRDs (Product Requirements Documents)

**Location**: `docs/project_plans/PRDs/[category]/[feature-name]-v1.md`

**Categories**:
- `harden-polish/` - Bug fixes, polish, hardening
- `features/` - New features
- `enhancements/` - Feature enhancements
- `refactors/` - Architecture refactors

**Naming Convention**:
- Format: `[feature-name]-v1.md`
- Use kebab-case (lowercase with hyphens)
- Include version number (-v1, -v2, etc.)
- Descriptive name (e.g., `advanced-filtering-v1.md`)

**Example**:
```
docs/project_plans/PRDs/
├── harden-polish/
│   ├── data-layer-fixes-filtering-v1.md
│   ├── prompt-modal-improvements-v1.md
│   └── sidebar-functionality-polish-v1.md
├── features/
│   ├── realtime-collaboration-v1.md
│   └── advanced-filtering-v1.md
├── enhancements/
│   └── search-improvements-v1.md
└── refactors/
    └── authentication-refactor-v1.md
```

---

### Implementation Plans

**Location**: `docs/project_plans/implementation_plans/[category]/[feature-name]-v1.md`

**Category**: Matches PRD category

**Naming Convention**:
- Format: `[feature-name]-v1.md` (matches PRD name)
- Version synchronized with PRD

**Phase Breakouts**: When plan >800 lines, create subdirectory

**Location**: `docs/project_plans/implementation_plans/[category]/[feature-name]-v1/`

**Phase File Naming**:
- Single phase: `phase-[N]-[name].md`
- Grouped phases: `phase-[N]-[M]-[name].md`
- Descriptive name: `database`, `backend`, `frontend`, `validation`

**Example**:
```
docs/project_plans/implementation_plans/
├── harden-polish/
│   ├── data-layer-fixes-filtering-v1.md       # Main plan (< 800 lines)
│   ├── prompt-modal-improvements-v1.md         # Main plan (summary + links)
│   └── prompt-modal-improvements-v1/           # Phase breakouts
│       ├── phase-1-3-backend.md                # Grouped phases
│       ├── phase-4-5-frontend.md
│       └── phase-6-8-validation.md
├── features/
│   ├── realtime-collaboration-v1.md
│   └── realtime-collaboration-v1/
│       ├── phase-1-database.md                 # Individual phases
│       ├── phase-2-repository.md
│       ├── phase-3-service.md
│       ├── phase-4-api.md
│       ├── phase-5-ui.md
│       ├── phase-6-testing.md
│       ├── phase-7-documentation.md
│       └── phase-8-deployment.md
└── enhancements/
    └── search-improvements-v1.md
```

---

## Naming Conventions Summary

### PRDs
```
Format: [feature-name]-v1.md
Example: data-layer-fixes-filtering-v1.md
Rules:
  - kebab-case (lowercase, hyphens)
  - descriptive name
  - version number (-v1, -v2)
```

### Implementation Plans
```
Format: [feature-name]-v1.md
Example: data-layer-fixes-filtering-v1.md
Rules:
  - matches PRD name exactly
  - same version as PRD
```

### Phase Files
```
Single Phase:
  Format: phase-[N]-[name].md
  Example: phase-1-database.md

Grouped Phases:
  Format: phase-[N]-[M]-[name].md
  Example: phase-1-3-backend.md

Rules:
  - sequential numbering
  - descriptive name (database, backend, frontend, validation)
  - lowercase, hyphens
```

---

## File Size Guidelines

### Optimal Sizes

| File Type | Target Size | Maximum Size | Action if Exceeded |
|-----------|-------------|--------------|-------------------|
| PRD | 400-600 lines | 800 lines | Move sections to appendices |
| Implementation Plan | 400-600 lines | 800 lines | Break into phase files |
| Phase File | 300-500 lines | 800 lines | Split into sub-phases |

### Breakout Strategy

**When to Break Out**:
- PRD >800 lines: Move detailed sections to appendices
- Implementation Plan >800 lines: Break into phase files
- Phase File >800 lines: Split into logical sub-sections

**How to Break Out**:
1. Identify natural boundaries (phases, domains, features)
2. Create subdirectory: `[feature-name]-v1/`
3. Create phase files with descriptive names
4. Update parent with table of contents linking to phase files
5. Keep summary in parent (200-300 lines)

---

## Cross-Linking Pattern

### From PRD to Implementation Plan

**In PRD**:
```markdown
## Implementation

See implementation plan: `docs/project_plans/implementation_plans/[category]/[feature-name]-v1.md`
```

### From PRD to Progress Tracking

**In PRD**:
```markdown
## Implementation

See progress tracking: `.claude/progress/[feature-name]/phase-{PHASE}-progress.md`
```

### From Implementation Plan to Phase Files

**In Parent Plan**:
```markdown
## Phase 2: Repository Layer

See [Phase 2 Implementation Details](./[feature-name]-v1/phase-2-repository.md)
```

### From Phase File to Parent

**At Bottom of Phase File**:
```markdown
[Return to Parent Plan](../[feature-name]-v1.md)
```

---

## YAML Frontmatter Requirements

### PRDs - Required

```yaml
---
title: "Feature Name - PRD"
description: "Brief summary (1-2 sentences)"
audience: [ai-agents, developers]
tags: [relevant, tags]
created: YYYY-MM-DD
updated: YYYY-MM-DD
category: "product-planning"
status: draft|published
related:
  - /docs/path/to/related.md
---
```

### Implementation Plans - Required

```yaml
---
title: "Feature Name - Implementation Plan"
description: "Brief implementation summary"
audience: [ai-agents, developers]
tags: [implementation, planning, phases]
created: YYYY-MM-DD
updated: YYYY-MM-DD
category: "product-planning"
status: draft|in-progress|published
related:
  - /docs/project_plans/PRDs/[category]/[feature-name]-v1.md
---
```

### Phase Files - Optional

Frontmatter optional for phase files (internal organization).

---

## Token Efficiency Through Structure

### Before Optimization

```
Single 1200-line implementation plan
│
└─ Load entire file for any query = 1200 lines context
```

### After Optimization

```
Parent plan (200 lines) + Phase files (400 lines each)
│
├─ Query about Phase 1 = Load 200 + 400 = 600 lines (50% reduction)
├─ Query about Phase 2 = Load 200 + 400 = 600 lines (50% reduction)
└─ Overview query = Load 200 lines only (83% reduction)
```

### Progressive Disclosure

1. **Level 1**: PRD summary (400 lines)
2. **Level 2**: Implementation plan summary (200 lines)
3. **Level 3**: Specific phase details (400 lines)
4. **Level 4**: Context files for deep dive (varies)

**Total context for targeted work**: ~1000 lines vs. 2000+ without structure

---

## Directory Tree Examples

### Small Feature (No Breakout)

```
project_plans/
├── PRDs/features/
│   └── small-feature-v1.md                     (400 lines)
└── implementation_plans/features/
    └── small-feature-v1.md                     (600 lines)

.claude/progress/
└── small-feature/
    └── all-phases-progress.md
```

### Medium Feature (Phase Breakout)

```
project_plans/
├── PRDs/features/
│   └── medium-feature-v1.md                    (500 lines)
└── implementation_plans/features/
    ├── medium-feature-v1.md                    (200 lines - summary)
    └── medium-feature-v1/
        ├── phase-1-3-backend.md                (500 lines)
        ├── phase-4-5-frontend.md               (400 lines)
        └── phase-6-8-validation.md             (300 lines)

.claude/
├── progress/
│   └── medium-feature/
│       └── all-phases-progress.md
└── worknotes/
    └── medium-feature/
        ├── phase-1-context.md
        └── phase-2-context.md
```

### Large Feature (Full Breakout)

```
project_plans/
├── PRDs/features/
│   └── large-feature-v1.md                     (600 lines)
└── implementation_plans/features/
    ├── large-feature-v1.md                     (250 lines - summary)
    └── large-feature-v1/
        ├── phase-1-database.md                 (400 lines)
        ├── phase-2-repository.md               (450 lines)
        ├── phase-3-service.md                  (500 lines)
        ├── phase-4-api.md                      (400 lines)
        ├── phase-5-ui.md                       (500 lines)
        ├── phase-6-testing.md                  (450 lines)
        ├── phase-7-documentation.md            (300 lines)
        └── phase-8-deployment.md               (250 lines)

.claude/
├── progress/
│   └── large-feature/
        ├── phase-1-progress.md
        ├── phase-2-progress.md
        ├── phase-3-progress.md
        ├── phase-4-progress.md
        └── phase-5-progress.md
└── worknotes/
    └── large-feature/
        ├── phase-1-context.md
        ├── phase-2-context.md
        ├── phase-3-context.md
        ├── phase-4-context.md
        └── phase-5-context.md
```

---

## Best Practices

1. **Match Names**: PRD, plan, and progress directory names should match
2. **Version Sync**: PRD and plan versions should match
3. **Logical Grouping**: Group related short phases (1-3, 4-5, 6-8)
4. **Token Efficiency**: Keep files <800 lines for optimal AI loading
5. **Progressive Disclosure**: Summary in parent, details in phase files
6. **Cross-Link**: Always link related documents
7. **Descriptive Names**: Use intention-revealing names for phase files
8. **Consistent Structure**: Follow templates for consistency

---

## Anti-Patterns to Avoid

❌ Generic phase names (`phase-1.md` instead of `phase-1-database.md`)
❌ Mismatched PRD/plan names
❌ Missing cross-links between documents
❌ Files >800 lines without breakout
❌ Deep nesting (keep structure flat)
❌ Version mismatches between PRD and plan
❌ Inconsistent naming conventions
