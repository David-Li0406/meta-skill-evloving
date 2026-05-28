# Planning Structure

## Directory Layout

```
./planning/{YYYYMMDD}_{project}/
├── PROJECT.md                    # Status dashboard
├── requirements/
│   ├── PRODUCT-REQUIREMENTS.md   # Phase 1
│   ├── TECHNICAL-REQUIREMENTS.md # Phase 2
│   └── TRACEABILITY.md           # Phase 3
├── diagrams/                     # Phase 4-5 (use diagrams-kroki skill)
│   ├── architecture/
│   ├── behavior/
│   └── data/
├── design/
│   ├── ARCHITECTURE.md           # Phase 5
│   └── INTERFACES.md             # Phase 6
└── epics/{E###}_{name}/
    ├── EPIC.md
    └── stories/{S###}_{name}/
        ├── STORY.md
        └── tasks/{T###}_{name}.md
```

## Naming Conventions

| Element | Format | Example |
|---------|--------|---------|
| Project | `{YYYYMMDD}_{kebab-case}` | `20260116_user-auth` |
| Epic | `{E###}_{kebab-case}` | `E001_user-management` |
| Story | `{S###}_{kebab-case}` | `S001_registration` |
| Task | `{T###}_{kebab-case}.md` | `T001_user-model.md` |

## PROJECT.md Template

```markdown
# Project: {Name}

**Created**: {YYYY-MM-DD}
**Status**: 🟡 In Progress

## Overview
{Brief description}

## Phase Progress

| Phase | Status | Approved |
|-------|--------|----------|
| 1. Product Requirements | ⚪ | - |
| 2. Technical Requirements | ⚪ | - |
| 3. Requirements Integration | ⚪ | - |
| 4. Diagrams & Artifacts | ⚪ | - |
| 5. Architecture & Design | ⚪ | - |
| 6. Interface Contracts | ⚪ | - |
| 7. Code Scaffolding | ⚪ | - |
| 8. Test Development | ⚪ | - |
| 9. Implementation | ⚪ | - |
| 10. Simulation Testing | ⚪ | - |

## Epics

| ID | Epic | Progress |
|----|------|----------|
| E001 | {Name} | ░░░░░░░░░░ 0% |
```

## EPIC.md Template

```markdown
# Epic: {Name}

**ID**: E{###}
**Status**: ⚪ Not Started
**Priority**: 🟠 High

## User Value
**As a** {persona}
**I want** {capability}
**So that** {benefit}

## Stories

| ID | Story | Status |
|----|-------|--------|
| S001 | {Name} | ⚪ |
```

## STORY.md Template

```markdown
# Story: {Name}

**ID**: S{###}
**Epic**: {Epic Name}
**Status**: ⚪ Not Started

## User Story
**As a** {persona}
**I want to** {action}
**So that** {benefit}

## Acceptance Criteria
- [ ] {Criterion 1}
- [ ] {Criterion 2}

## Tasks

| ID | Task | Status |
|----|------|--------|
| T001 | {Name} | ⚪ |

## Definition of Done
- [ ] Tests passing
- [ ] Code reviewed
- [ ] Documentation updated
```

## Task Template

```markdown
# Task: {Name}

**ID**: T{###}
**Story**: {Story Name}
**Status**: ⚪ Not Started
**Estimate**: {X}h

## Description
{What needs to be done}

## Subtasks
- [ ] {Subtask 1}
- [ ] {Subtask 2}

## Files to Modify
| File | Action |
|------|--------|
| `path/to/file` | Create/Modify |
```

## Status Icons

| Icon | Meaning |
|------|---------|
| ⚪ | Not Started |
| 🟡 | In Progress |
| 🟢 | Complete |
| 🔴 | Blocked |

## Progress Bars

```
[░░░░░░░░░░] 0%
[██░░░░░░░░] 20%
[█████░░░░░] 50%
[████████░░] 80%
[██████████] 100%
```
