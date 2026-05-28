# Planning Skill Best Practices

## File Size Management

**Guideline**: No file should exceed ~800 lines

**Rationale**:
- Optimal token efficiency for AI context loading
- Enables progressive disclosure pattern
- Reduces cognitive load for agents
- Faster file parsing and analysis

**Strategies**:
1. Break plans by phase when >800 lines
2. Group short related phases (1-3, 4-5)
3. Keep summaries in parent, details in phase files
4. Use links for cross-references

---

## Naming Conventions

### PRDs
- Format: `[feature-name]-v1.md`
- Use kebab-case (lowercase with hyphens)
- Include version number (-v1, -v2)
- Example: `advanced-filtering-v1.md`

### Implementation Plans
- Format: `[feature-name]-v1.md`
- Match PRD naming
- Same category as PRD
- Version synchronized with PRD

### Phase Files
- Format: `phase-[N]-[name].md`
- Sequential numbering (phase-1, phase-2)
- Can group: `phase-1-3-backend.md`
- Descriptive name (database, repository, frontend)

---

## Directory Organization

### PRDs
- Location: `docs/project_plans/PRDs/[category]/`
- Categories: `harden-polish`, `features`, `enhancements`, `refactors`

### Implementation Plans
- Location: `docs/project_plans/implementation_plans/[category]/`
- Match PRD category
- Phase breakouts in subdirectory: `[plan-name]/`

---

## Token Efficiency Tips

### Progressive Disclosure
1. Summary in parent plan (200 lines)
2. Link to detailed phase files (400 lines each)
3. Agent loads summary first, then specific phase as needed
4. 50-67% token reduction

### Structured References
- Link to ADRs instead of duplicating architecture info
- Reference existing docs rather than repeating
- Use relative paths for phase file links

### Chunk by Logical Units
- Keep related tasks together
- Don't split mid-phase
- Group short phases if logical
- Maintain quality gates with phases

---

## YAML Frontmatter

### PRDs
```yaml
---
title: "Feature Name - PRD"
description: "Brief summary (1-2 sentences)"
audience: [ai-agents, developers]
tags: [relevant, tags, for, search]
created: 2025-11-11
updated: 2025-11-11
category: "product-planning"
status: draft|published
related:
  - /docs/architecture/ADRs/relevant-adr.md
---
```

### Implementation Plans
```yaml
---
title: "Feature Name - Implementation Plan"
description: "Brief summary of implementation approach"
audience: [ai-agents, developers]
tags: [implementation, planning, phases]
created: 2025-11-11
updated: 2025-11-11
category: "product-planning"
status: draft|in-progress|published
related:
  - /docs/project_plans/PRDs/category/feature-name-v1.md
---
```

---

## Architecture Compliance

All plans follow MP layered architecture:
- **Routers** - HTTP + validation, return DTOs
- **Services** - Business logic, return DTOs only
- **Repositories** - All DB I/O, RLS enforcement, cursor pagination
- **ErrorResponse** - Envelope for all failures
- **Cursor Pagination** - `{ items, pageInfo }` format

---

## Documentation Policy

Follows CLAUDE.md documentation policy:
- PRDs are product-planning docs (allowed)
- Implementation Plans are product-planning docs (allowed)
- NO reports, summaries, etc unless explicitly requested
- One progress file per phase

---

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Generic phase names | `phase-1.md` unclear | Use `phase-1-database.md` |
| Mismatched names | PRD/plan names differ | Keep names synchronized |
| Missing cross-links | Lost navigation | Always link related docs |
| Files >800 lines | Token inefficiency | Break into phase files |
| Deep nesting | Hard to navigate | Keep structure flat |
| Version mismatch | Confusion | Sync PRD/plan versions |

[Return to Planning Skill](../SKILL.md)
