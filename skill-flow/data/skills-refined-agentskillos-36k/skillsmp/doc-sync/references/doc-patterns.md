# Tech-Docs Taxonomy Reference

Standardized documentation structure used across all projects.

## Canonical Structure

```
docs/tech-docs/
├── README.md                        # Index with priority-sorted tables
├── _archive/                        # Historical docs (issues, lessons, solutions)
│   ├── issues/
│   ├── lessons-learned/
│   └── solutions/
├── architecture/
│   ├── overview.md                  # High-level architecture and data flow
│   ├── component-strategy.md        # Component patterns (Server vs Client, etc.)
│   └── decisions/                   # Architecture Decision Records (ADRs)
│       ├── README.md                # Decision log/index
│       └── NNN-<topic>.md           # Individual ADRs (001-use-nextjs.md)
├── design/
│   ├── design-system.md             # Complete design system reference
│   ├── tokens.md                    # Color, typography, spacing tokens
│   └── concepts/                    # Design concept explorations
├── features/
│   └── <feature-name>.md            # Per-feature implementation docs
├── guides/
│   ├── creating-pages.md            # How to add new pages/routes
│   ├── styling.md                   # Design tokens and CSS patterns
│   └── deployment.md                # Production deployment workflow
├── quick-reference/
│   ├── before-you-start.md          # Essential setup and conventions
│   ├── decision-trees.md            # Quick decision guides
│   ├── common-patterns.md           # Frequently used code patterns
│   └── file-locations.md            # Where to find/place code
└── reference/
    ├── tech-stack.md                # Technologies and dependencies
    └── scripts-commands.md          # npm scripts and CLI tools
```

---

## Frontmatter Standard

Every doc MUST have YAML frontmatter:

```yaml
---
title: Document Title
description: One-line description of what this doc covers
priority: CRITICAL | HIGH | MEDIUM
last_updated: YYYY-MM-DD
status: IMPLEMENTED | PLANNED | DEPRECATED # Optional, for features
related_docs: # Optional
  - ../path/to/related.md
---
```

### Priority Levels

| Priority | Badge | Meaning                                                |
| -------- | ----- | ------------------------------------------------------ |
| CRITICAL | 🔴    | Breaking if wrong/outdated - keep current at all costs |
| HIGH     | 🟡    | Frequently referenced - should be accurate             |
| MEDIUM   | 🟢    | Occasional reference - update when convenient          |

### Status Values (for features)

| Status      | Meaning                          |
| ----------- | -------------------------------- |
| PLANNED     | Designed but not yet implemented |
| IMPLEMENTED | Complete and in production       |
| DEPRECATED  | Still works but being phased out |

**Critical rule:** A doc with `status: PLANNED` for an implemented feature is a
documentation bug.

---

## Category Definitions

### quick-reference/

**Purpose:** Fast-lookup guides for active development. Keep open while coding.

| Doc                 | Contents                                       |
| ------------------- | ---------------------------------------------- |
| before-you-start.md | Setup, conventions, project structure          |
| decision-trees.md   | Quick decision guides (Server vs Client, etc.) |
| common-patterns.md  | Copy-paste code patterns                       |
| file-locations.md   | Where to find and place code                   |

**When to update:** Any change to project conventions, patterns, or structure.

### architecture/

**Purpose:** System design and structural decisions.

| Doc                   | Contents                                              |
| --------------------- | ----------------------------------------------------- |
| overview.md           | High-level architecture, data flow, system boundaries |
| component-strategy.md | Component patterns specific to the tech stack         |
| decisions/\*.md       | ADRs documenting why decisions were made              |

**When to update:** New integrations, structural changes, major refactors.

### architecture/decisions/ (ADRs)

**Purpose:** Historical context for key technical decisions.

**Naming:** `NNN-<topic>.md` (e.g., `001-use-nextjs.md`, `002-use-supabase.md`)

**Template:**

```markdown
---
title: "ADR-NNN: Decision Title"
description: Brief description
priority: MEDIUM
last_updated: YYYY-MM-DD
status: Accepted | Proposed | Deprecated | Superseded
---

# ADR-NNN: Decision Title

## Problem

What problem are we solving?

## Decision

What did we decide?

## Why

Why this approach? What were the key factors?

## Alternatives Considered

What else did we consider? Why not those?

## Trade-offs

What are the downsides of this decision?

## References

- Links to relevant docs, issues, discussions
```

**When to create:** New database, new major dependency, new architectural
pattern, significant infrastructure change.

### design/

**Purpose:** Design system documentation.

| Doc              | Contents                                                            |
| ---------------- | ------------------------------------------------------------------- |
| design-system.md | Complete design reference (colors, typography, spacing, components) |
| tokens.md        | Design token definitions                                            |
| concepts/\*.md   | Design explorations and rationale                                   |

**When to update:** New colors, typography changes, component additions, design
pattern changes.

### features/

**Purpose:** Implementation details for specific application features.

**Naming:** `<feature-name>.md` (e.g., `blog-system.md`, `auth.md`, `search.md`)

**Template:**

```markdown
---
title: Feature Name
description: What this feature does
priority: HIGH | MEDIUM
last_updated: YYYY-MM-DD
status: IMPLEMENTED | PLANNED
related_docs:
  - ../architecture/decisions/NNN-relevant.md
---

# Feature Name

## Overview

Brief description of what this feature provides.

## Routes

| Route   | Description          |
| ------- | -------------------- |
| `/path` | What this route does |

## Key Files

| File                       | Purpose             |
| -------------------------- | ------------------- |
| `src/app/feature/page.tsx` | Main page component |
| `src/lib/feature.ts`       | Core logic          |

## Data Model

Database tables, types, or schemas used.

## API Functions

### `functionName(params)`

What it does, what it returns.

## Implementation Notes

Any gotchas, patterns, or important details.
```

**When to update:** New routes, new API functions, schema changes, significant
behavior changes.

### guides/

**Purpose:** Step-by-step instructions for common workflows.

| Doc               | Contents                                  |
| ----------------- | ----------------------------------------- |
| creating-pages.md | How to add new pages and routes           |
| styling.md        | How to use design tokens and CSS patterns |
| deployment.md     | Production deployment workflow            |

**When to update:** Workflow changes, new capabilities, tooling updates.

### reference/

**Purpose:** Complete API and configuration documentation.

| Doc                 | Contents                          |
| ------------------- | --------------------------------- |
| tech-stack.md       | All technologies and dependencies |
| scripts-commands.md | npm scripts and CLI tools         |

**When to update:** New dependencies, version bumps, new scripts.

### tech-stack.md Format

```markdown
## Category Name

### Package Name

**Version:** x.y.z (or "latest" if floating) **Purpose:** What it's used for
**Key files:** Where it's configured/used **Docs:** Link to official docs
```

Categories:

- Framework (Next.js, React)
- Styling (Tailwind, CSS)
- Animation (Framer Motion)
- UI Components (shadcn/ui)
- Data Layer (Supabase, database clients)
- Content Processing (markdown parsers)
- Development Tools (ESLint, TypeScript)

### \_archive/

**Purpose:** Historical documentation preserved for reference.

| Folder           | Contents                                |
| ---------------- | --------------------------------------- |
| issues/          | Past issue investigations               |
| lessons-learned/ | Incident retrospectives                 |
| solutions/       | Historical solutions that may be useful |

**When to use:** Move docs here when superseded, don't delete.

---

## Index README.md Format

The main `docs/tech-docs/README.md` serves as the navigation hub:

```markdown
## Category Name

Description of what this category contains.

| Priority    | Document                  | Description          |
| ----------- | ------------------------- | -------------------- |
| 🔴 CRITICAL | [Doc Title](./path/to.md) | One-line description |
| 🟡 HIGH     | [Doc Title](./path/to.md) | One-line description |
| 🟢 MEDIUM   | [Doc Title](./path/to.md) | One-line description |
```

**Maintenance:** When adding new docs, add them to the appropriate table in
README.md.

---

## Change-to-Doc Mapping (Quick Reference)

| Code Change       | Update These Docs                                                  |
| ----------------- | ------------------------------------------------------------------ |
| New route/page    | features/\*.md, file-locations.md                                  |
| New component     | component-strategy.md (if pattern), design-system.md (if reusable) |
| New dependency    | tech-stack.md, possibly new ADR                                    |
| Database change   | features/\*.md (schema section), new ADR                           |
| New integration   | New ADR, architecture/overview.md                                  |
| Design tokens     | design/tokens.md, design-system.md                                 |
| New script        | reference/scripts-commands.md                                      |
| Convention change | quick-reference/\*.md                                              |

---

## Doc-Sync Detection Rules

### Status Drift Detection

- Feature implemented → `status: PLANNED` still in frontmatter = **High priority
  gap**
- ADR referenced in code but doesn't exist = **High priority gap**

### Staleness Detection

- `last_updated` > 30 days old + related code changed = **Medium priority**
- Index README.md missing entry for existing doc = **Low priority**

### Missing Doc Detection

- New `src/app/*/page.tsx` with no features/\*.md = **High priority**
- New entry in package.json dependencies with no tech-stack.md entry = **Medium
  priority**
- New `src/lib/*.ts` core utility with no architecture mention = **Medium
  priority**
