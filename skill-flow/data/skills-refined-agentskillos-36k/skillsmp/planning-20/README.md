# Planning Skill - Quick Reference

## Overview

The Planning Skill generates and optimizes Product Requirements Documents (PRDs) and Implementation Plans as AI artifacts optimized for AI agent consumption.

**Primary Use Cases**:
- Generate PRDs from feature requests
- Create phased Implementation Plans with subagent assignments
- Optimize long planning docs by breaking into phase-specific files

---

## Quick Start

### Generate PRD
```
User: "Create a PRD for advanced filtering on prompts"
→ Output: docs/project_plans/PRDs/features/advanced-filtering-v1.md
```

### Generate Implementation Plan
```
User: "Create implementation plan for docs/project_plans/PRDs/features/advanced-filtering-v1.md"
→ Output: Main plan + phase files (if >800 lines)
```

### Optimize Existing Plan
```
User: "Optimize docs/project_plans/implementation_plans/harden-polish/sidebar-polish-v1.md"
→ Breaks 1200-line plan into summary + 3 phase files (50-70% token reduction)
```

---

## Skill Structure

```
planning/
├── SKILL.md                          # Main skill (190 lines)
├── README.md                         # This file
├── workflows/                        # Detailed workflow guides
│   ├── create-prd.md                 # Workflow 1: Create PRD
│   ├── create-implementation-plan.md # Workflow 2: Create Plan
│   ├── optimize-existing-plans.md    # Workflow 3: Optimize
│   └── create-progress-tracking.md   # Workflow 4: Progress
├── templates/                        # Document templates
│   ├── prd-template.md
│   ├── implementation-plan-template.md
│   └── phase-breakdown-template.md
├── references/                       # Reference documentation
│   ├── subagent-assignments.md       # Task → subagent mapping
│   ├── file-structure.md             # Directory conventions
│   ├── optimization-patterns.md      # Token efficiency patterns
│   ├── best-practices.md             # Planning guidelines
│   └── workflow-examples.md          # Detailed examples
└── scripts/                          # Automation (placeholder)
```

---

## Core Workflows

| Workflow | Purpose | Details |
|----------|---------|---------|
| Create PRD | Generate PRD from feature request | [workflows/create-prd.md](workflows/create-prd.md) |
| Create Plan | Generate implementation plan from PRD | [workflows/create-implementation-plan.md](workflows/create-implementation-plan.md) |
| Optimize | Break large plans into phase files | [workflows/optimize-existing-plans.md](workflows/optimize-existing-plans.md) |
| Progress | Create tracking artifacts | [workflows/create-progress-tracking.md](workflows/create-progress-tracking.md) |

---

## Key Concepts

### Token Efficiency (Progressive Disclosure)

- **Target**: ~800 lines max per file
- **Strategy**: Summary in parent → Details in linked files
- **Result**: 50-70% token reduction for most queries

### Subagent Integration

Every task assigned to appropriate specialist:
- Database → data-layer-expert
- Backend → python-backend-engineer, backend-architect
- Frontend → ui-engineer-enhanced, frontend-developer
- Testing → testing specialists
- Docs → documentation-writer

---

## File Output Structure

```
docs/project_plans/
├── PRDs/[category]/
│   └── feature-name-v1.md
└── implementation_plans/[category]/
    ├── feature-name-v1.md (parent)
    └── feature-name-v1/ (phase files if >800 lines)
        ├── phase-1-3-backend.md
        ├── phase-4-5-frontend.md
        └── phase-6-8-validation.md
```

---

## Quick Tips

**Creating PRDs**: Be specific about requirements and include user stories

**Creating Plans**: Follow 8-phase MP architecture, assign subagents to every task

**Optimizing**: Group related phases (1-3, 4-5, 6-8), keep summary in parent

---

**Version**: 3.0 (Progressive Disclosure Optimization)
**Last Updated**: 2025-12-30
**Skill Location**: `.claude/skills/planning/`
