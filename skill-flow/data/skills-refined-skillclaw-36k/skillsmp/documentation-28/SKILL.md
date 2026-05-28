---
name: documentation
description: Documentation standards for changelogs, feature specs, and module documentation
user-invocable: false
---

# Documentation Skill

**Version:** 1.0
**Source:** Documentation Standards

> Non-negotiable documentation standards. Documentation ships with code, not after it.

---

## Core Principles

1. **Documentation Ships with Code** — Every feature includes updated documentation
2. **Single Source of Truth** — `/Documentation` folder is THE reference
3. **Agent Continuity** — Documentation enables agents to understand context
4. **Living Documents** — Keep documentation current, not stale

---

## The Documentation Feedback Loop

```
Agent reads /Documentation → Understands context → Does work → Updates /Documentation → Next agent reads
```

When you update `/Documentation`, you're helping the next agent (including future you) understand the project.

---

## Semantic Versioning (SemVer)

### Format

```
MAJOR.MINOR.PATCH
```

| Type | When to Bump | Examples |
|------|--------------|----------|
| **MAJOR** | Breaking change to behavior, inputs, outputs, or structure | API contract changes, removed features, renamed files |
| **MINOR** | New user-visible capability or workflow | New feature, new endpoint, new command |
| **PATCH** | Bug fixes, small improvements, no new capability | Fix typo, improve performance, formatting |

### Release Naming Convention

```
vX.Y.Z — [Program] / [Module]: [Feature]
```

| Component | Type | Description |
|-----------|------|-------------|
| **Program** | Noun | Major domain (e.g., Kitchen, Garden) |
| **Module** | Noun-phrase | Capability area (e.g., Planning, Tasks) |
| **Feature** | Verb/Noun-phrase | Specific action (e.g., Create meal plan) |

**Examples:**
- `v0.2.0 — Kitchen / Planning: Create weekly meal plan`
- `v0.3.0 — Garden / Tasks: Track watering routine`
- `v0.4.1 — Kitchen / Planning: Fix missing quantities`

### Scope Tags (Machine-Friendly)

```
scope: program.module.feature
```

**Examples:**
- `scope: kitchen.planning.generate-shopping-list`
- `scope: garden.tasks.track-watering-routine`

### Compatibility Rules

**MAJOR bump when ANY of these change in a breaking way:**
- File/folder paths or naming conventions
- Required inputs or workflow order
- Output contract (required sections, templates)

**MINOR bump when:**
- New workflow outcome added
- Module gains end-to-end feature
- Docs gain new non-breaking sections

**PATCH bump when:**
- Bug fixes, formatting, typos
- Performance improvements without contract change

---

## Folder Structure

```
/Documentation/
  project-roadmap.md       # Living plan + progress tracking
  architecture.md          # System design overview
  changelog.md             # Version history (Keep a Changelog)
  features/
    [program-name]/
      [module-name]/
        _[module-name].md  # Module explainer (underscore sorts first)
        feature-name-1.md  # Feature specification
        feature-name-2.md  # Feature specification
```

### Key Files

| File | Purpose |
|------|---------|
| `project-roadmap.md` | Strategic roadmap (v0.1 → v1.0), milestones |
| `architecture.md` | System design, data flow, key components |
| `changelog.md` | Version history (Keep a Changelog format) |
| `_*.md` (module) | Module overview, features list, dependencies |
| `*.md` (feature) | User story, acceptance criteria, tech notes |

---

## Feature Specifications

### Required Elements

Every feature file MUST include:

1. **One-line description**
2. **Module reference and status**
3. **User story** (As a / I want / So that)
4. **Overview and basic scenario**
5. **Acceptance criteria** (testable checkboxes)
6. **Data model** (if applicable)
7. **Technical notes with Standards Checklist**
8. **Open questions**
9. **Related features**

### Feature File Template

```markdown
# Feature Name

> One-line description of what this feature does.

**Module:** [Program] / [Module]
**Status:** Planned | In Progress | Complete
**Started:** YYYY-MM-DD
**Completed:** YYYY-MM-DD

---

## User Story

**As a** [user type],
**I want** [action/capability],
**So that** [benefit/outcome].

---

## Overview

[2-3 paragraph description of the feature]

### Basic Scenario

1. User does X
2. System responds with Y
3. User sees Z

---

## Acceptance Criteria

- [ ] Criterion 1 (testable)
- [ ] Criterion 2 (testable)
- [ ] Criterion 3 (testable)

---

## Data Model

[If applicable - tables, schemas, data structures]

---

## Technical Notes

### Approach

[Implementation approach]

### Standards Checklist

- [ ] Code Quality: Tests written first (TDD)
- [ ] Code Quality: 3-tier architecture followed
- [ ] Architecture: Module boundaries respected
- [ ] Design: Design tokens used (no hardcoded values)
- [ ] Security: Input validation implemented
- [ ] Documentation: Feature file complete

---

## Open Questions

- [ ] **Open:** Question 1?
- [x] **Resolved:** Question 2? → Answer

---

## Related Features

- [Related Feature 1](./related-1.md)
- [Related Feature 2](./related-2.md)
```

---

## Module Explainers

### Structure

```markdown
# Module Name

> One-line module description.

**Program:** [Program Name]
**Status:** 2/6 features complete

---

## Overview

[Module purpose and scope]

---

## Features

| Feature | Status | Description |
|---------|--------|-------------|
| [Feature 1](./feature-1.md) | ✅ | Description |
| [Feature 2](./feature-2.md) | 🔄 | Description |
| [Feature 3](./feature-3.md) | ⏳ | Description |

---

## Dependencies

- [Other Module](../other/other.md)
- External API X

---

## Architecture Notes

[How this module fits into the system]
```

---

## Changelog Format

Follow [Keep a Changelog](https://keepachangelog.com/) format:

```markdown
# Changelog

All notable changes to this project are documented here.

## [Unreleased]

### Added
- New feature X

### Changed
- Modified behavior Y

### Fixed
- Bug fix Z

---

## [0.2.0] — 2026-01-15 — Kitchen / Planning: Create weekly meal plan

### Added
- Weekly meal planning interface
- Recipe suggestion based on preferences

### Changed
- Updated planning algorithm

---

## [0.1.0] — 2026-01-01 — Initial Release

### Added
- Project scaffolding
- Basic infrastructure
```

### Change Types

| Type | Description |
|------|-------------|
| **Added** | New features |
| **Changed** | Changes in existing functionality |
| **Deprecated** | Soon-to-be removed features |
| **Removed** | Now removed features |
| **Fixed** | Bug fixes |
| **Security** | Vulnerability fixes |

---

## Status Formats

| Context | Format | Values |
|---------|--------|--------|
| `project-roadmap.md` | Emoji | ⏳ Planned, 🔄 In Progress, ✅ Complete, 🚫 Blocked |
| Feature/Module files | Text | Planned, In Progress, Complete |
| Open questions | Text | Open, Resolved |

**Rationale:** Emoji in roadmap for visual scanning. Text in feature files for AI parsing.

---

## Documentation Checklist

Before considering documentation complete:

### Feature Files
- [ ] One-line description present
- [ ] Status is current and accurate
- [ ] User story follows As/Want/So format
- [ ] Acceptance criteria are testable checkboxes
- [ ] Standards checklist is complete
- [ ] Open questions addressed or documented

### Module Explainers
- [ ] Feature table is current
- [ ] Status counts are accurate
- [ ] Dependencies listed

### Project-Level
- [ ] Roadmap reflects current state
- [ ] Changelog updated for release
- [ ] Architecture doc current

---

## References

- `references/semver-guide.md` — Complete semantic versioning guide
- `references/changelog-format.md` — Keep a Changelog format
- `references/feature-spec-guide.md` — Feature specification writing guide

## Assets

- `assets/feature-template.md` — Feature file template
- `assets/module-template.md` — Module explainer template
- `assets/changelog-template.md` — Changelog template

## Scripts

- `scripts/validate_docs.py` — Validate documentation structure
- `scripts/generate_feature.py` — Generate feature file from template
