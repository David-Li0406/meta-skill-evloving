---
name: planning
description: Generate and optimize PRDs, Implementation Plans, and Progress Tracking documents optimized as AI artifacts for development agents. Use when creating new feature plans, breaking down long planning docs (>800 lines), or setting up progress tracking.
---

# Planning Skill

Generate and optimize Product Requirements Documents (PRDs) and Implementation Plans as AI artifacts - file-based context caches optimized for AI agent consumption.

## Purpose

- Generate comprehensive PRDs from feature requests
- Create phased Implementation Plans with subagent task assignments
- Optimize existing planning docs by breaking into token-efficient files
- Set up progress tracking (delegates to artifact-tracking skill)

## Key Benefits

| Benefit | Description |
|---------|-------------|
| Token Efficiency | Max ~800 lines per file for optimal AI context |
| Progressive Disclosure | Summary → Detail pattern with linked files |
| Subagent Integration | Automatic task assignment to specialists |
| MP Architecture | Plans follow layered architecture |

---

## Quick Start

### Create PRD
```bash
User: "Create a PRD for advanced filtering on the prompts page"
# Output: docs/project_plans/PRDs/[category]/advanced-filtering-v1.md
```

### Create Implementation Plan
```bash
User: "Create implementation plan for docs/project_plans/PRDs/features/advanced-filtering-v1.md"
# Output: Main plan + phase files (if >800 lines)
```

### Optimize Existing Plan
```bash
User: "Optimize docs/project_plans/implementation_plans/harden-polish/sidebar-polish-v1.md"
# Breaks 1200-line plan into summary + 3 phase files
```

### Create Progress Tracking
```bash
User: "Create progress tracking for data-layer-fixes PRD"
# Delegates to artifact-tracking skill
```

---

## Core Workflows

| # | Workflow | Input | Output | Details |
|---|----------|-------|--------|---------|
| 1 | Create PRD | Feature request | PRD file | Generates a comprehensive PRD from a feature request. |
| 2 | Create Implementation Plan | PRD path | Plan + phase files | Generates a detailed implementation plan from a PRD, including phase breakdowns. |
| 3 | Optimize Existing Plan | Plan path (>800 lines) | Optimized structure | Breaks down long plans into manageable phase-specific files. |
| 4 | Create Progress Tracking | PRD or Plan | Progress artifacts | Sets up progress tracking, delegating to the artifact-tracking skill. |

---

## File Organization

### PRDs
```
docs/project_plans/PRDs/[category]/[feature-name]-v1.md
Categories: harden-polish, features, enhancements, refactors
```

### Implementation Plans
```
docs/project_plans/implementation_plans/[category]/[feature-name]-v1.md
Phase files (if >800 lines): [feature-name]-v1/phase-[N]-[name].md
```

---

## Templates

| Template | Purpose | Location |
|----------|---------|----------|
| PRD | Standard PRD structure | [./templates/prd-template.md](./templates/prd-template.md) |
| Implementation Plan | Phased plan with tasks | [./templates/implementation-plan-template.md](./templates/implementation-plan-template.md) |
| Phase Breakdown | Individual phase file | [./templates/phase-breakdown-template.md](./templates/phase-breakdown-template.md) |

---

## References

| Reference | Purpose |
|-----------|---------|
| [Subagent Assignments](./references/subagent-assignments.md) | Task type to subagent mapping |
| [File Structure](./references/file-structure.md) | Directory and naming conventions |
| [Optimization Patterns](./references/optimization-patterns.md) | Strategies for breaking up large files |
| [Best Practices](./references/best-practices.md) | Guidelines for effective planning |
| [Workflow Examples](./references/workflow-examples.md) | Detailed usage examples |

---

## Subagent Integration

Plans integrate with 50+ project subagents. Key assignments:

| Domain | Primary Subagents |
|--------|-------------------|
| Database | data-layer-expert |
| Repository | python-backend-engineer, data-layer-expert |
| Service | backend-architect, python-backend-engineer |
| API | python-backend-engineer, backend-architect |
| Frontend | ui-engineer-enhanced, frontend-developer |
| Testing | testing specialist (varies by type) |
| Documentation | documentation-writer, documentation-complex |

---

## Token Efficiency

### Before Optimization
```
Load 1200-line plan for any query = 1200 lines context
```

### After Optimization
```
Overview query: Load 200-line summary only (83% reduction)
Phase query: Load 200 + 400-line phase = 600 lines (50% reduction)
```

---

## When to Use This Skill

| Scenario | Use This Skill |
|----------|---------------|
| Creating PRDs for new features | Yes |
| Generating implementation plans from PRDs | Yes |
| Breaking down long plans (>800 lines) | Yes |
| Setting up progress tracking | Yes (delegates to artifact-tracking) |
| Optimizing existing plans for AI consumption | Yes |

---

## Related Skills

| Skill | Purpose |
|-------|---------|
| artifact-tracking | Progress tracking and context artifacts |
| skill-builder | Create new custom skills |
| symbols | Token-efficient codebase indexing |
| codebase-explorer | Fast pattern discovery |

## Related Agents

| Agent | Purpose |
|-------|---------|
| lead-pm | SDLC orchestration |
| prd-writer | PRD creation |
| implementation-planner | Detailed planning |
| lead-architect | Architecture decisions |

---

## Version History

| Date | Changes |
|------|---------|
| 2026-01-06 | Added request-log integration for status updates via `/mc` commands |
| 2025-12-30 | Optimized for progressive disclosure; broke workflows into separate files |
| 2025-12-01 | Removed Tracking Creation; delegated to artifact-tracking skill |
| 2025-11-11 | Initial skill creation with 4 workflows |