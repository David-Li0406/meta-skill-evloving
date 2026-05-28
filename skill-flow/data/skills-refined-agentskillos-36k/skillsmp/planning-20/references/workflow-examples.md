# Planning Skill Examples

## Example 1: Create PRD for Advanced Filtering

### Input
```
User: "Create a PRD for adding advanced filtering to the prompts page.
Users need to filter by multiple criteria: model, provider, date range, tags, and favorites."
```

### Process
1. Extract feature name: "Advanced Filtering"
2. Determine category: "features"
3. Generate PRD using template
4. Structure sections:
   - Problem: Users can only filter by single criteria
   - Goals: Multi-criteria filtering, saved filter sets
   - Requirements: UI for filter builder, backend filter query support
   - Phases: Phase 1 (Backend), Phase 2 (Frontend), Phase 3 (Saved Filters)

### Output

**File**: `docs/project_plans/PRDs/features/advanced-filtering-v1.md`

```markdown
# Advanced Filtering - PRD

**Feature Name**: Advanced Filtering
**Date**: 2025-11-11
**Author**: Claude (Sonnet 4.5)
**Related**: Filtering guides, search ADRs

## 1. Executive Summary
Enable users to filter prompts by multiple criteria simultaneously
(model, provider, date range, tags, favorites) with the ability to
save and reuse filter sets.

## 2. Context & Background
Current filtering supports single criteria only. Users frequently
need to filter by combinations (e.g., "OpenAI models from last
week tagged 'production'").

... (full PRD structure)
```

---

## Example 2: Create Implementation Plan with Phase Breakout

### Input
```
User: "Create implementation plan for
docs/project_plans/PRDs/features/advanced-filtering-v1.md"
```

### Process
1. Read PRD, extract requirements
2. Plan 7 phases following MP architecture
3. Generate task breakdown with estimates
4. Assign subagents to each task
5. Calculate total: 1100 lines → needs breakout
6. Create phase files:
   - phase-1-3-backend.md (500 lines)
   - phase-4-5-frontend.md (400 lines)
   - phase-6-7-validation.md (300 lines)
7. Update parent plan with links (200 lines)

### Output

**Main Plan**: `docs/project_plans/implementation_plans/features/advanced-filtering-v1.md` (200 lines)

```markdown
# Implementation Plan: Advanced Filtering

## Phase Overview
| Phase | Title | Effort | Files |
|-------|-------|--------|-------|
| 1-3 | Backend Implementation | 18 pts | [Details](./advanced-filtering-v1/phase-1-3-backend.md) |
| 4-5 | Frontend Implementation | 12 pts | [Details](./advanced-filtering-v1/phase-4-5-frontend.md) |
| 6-7 | Validation & Deployment | 8 pts | [Details](./advanced-filtering-v1/phase-6-7-validation.md) |

... (executive summary, strategy)
```

**Phase Files Created**:

`advanced-filtering-v1/phase-1-3-backend.md` (500 lines)
- Phase 1: Database (filter_sets table, indexes)
- Phase 2: Repository (query builder, filter sets repo)
- Phase 3: Service (filter validation, DTO mapping)

`advanced-filtering-v1/phase-4-5-frontend.md` (400 lines)
- Phase 4: API (filter endpoints, saved sets API)
- Phase 5: UI (filter builder component, saved sets UI)

`advanced-filtering-v1/phase-6-7-validation.md` (300 lines)
- Phase 6: Testing (unit, integration, E2E)
- Phase 7: Deployment (feature flags, monitoring)

---

## Example 3: Optimize Existing Long Plan

### Input
```
User: "Optimize docs/project_plans/implementation_plans/harden-polish/sidebar-polish-v1.md
- it's 1200 lines"
```

### Process
1. Read plan: 8 phases, ~150 lines each
2. Determine breakout: Group 1-3 (backend), 4-5 (frontend), 6-8 (validation)
3. Create phase files
4. Update parent plan: Keep summary, add links (200 lines)

### Output

**Updated**: `sidebar-polish-v1.md` (200 lines)

**Created Phase Files**:

`sidebar-polish-v1/phase-1-3-backend.md` (450 lines)
- Phase 1: Database - Sidebar state, user preferences
- Phase 2: Repository - State management, RLS
- Phase 3: Service - Preference sync, DTOs

`sidebar-polish-v1/phase-4-5-frontend.md` (400 lines)
- Phase 4: API - Endpoints for sidebar state
- Phase 5: UI - Sidebar component, animations

`sidebar-polish-v1/phase-6-8-validation.md` (350 lines)
- Phase 6: Testing - Unit, integration, visual
- Phase 7: Documentation - Component docs, API docs
- Phase 8: Deployment - Feature flags, rollout

**Token Efficiency**: 67% reduction for targeted queries

---

## Example 4: Full Feature Planning Flow

### Input
```
User: "Plan the complete user analytics dashboard feature"
```

### Full Flow

**Step 1: Create PRD**
```
Output: docs/project_plans/PRDs/features/analytics-dashboard-v1.md
```

**Step 2: Create Implementation Plan**
```
Output: docs/project_plans/implementation_plans/features/analytics-dashboard-v1.md
Phase files (if needed):
- analytics-dashboard-v1/phase-1-3-backend.md
- analytics-dashboard-v1/phase-4-5-frontend.md
- analytics-dashboard-v1/phase-6-8-validation.md
```

**Step 3: Create Progress Tracking (via artifact-tracking)**
```
Output: .claude/progress/analytics-dashboard/all-phases-progress.md
```

**Result**: Complete planning documentation with progressive disclosure

[Return to Planning Skill](../SKILL.md)
