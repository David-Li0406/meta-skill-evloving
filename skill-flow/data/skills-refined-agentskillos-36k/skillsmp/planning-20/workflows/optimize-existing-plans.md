# Workflow: Optimize Existing Plans

**Input**: Path to existing PRD or Implementation Plan that's >800 lines

## Process

### 1. Analyze Plan

- Read full plan
- Count total lines
- Identify natural break points (phases, sections)
- Determine optimal split strategy

### 2. Determine Breakout Strategy

**Primary**: Break by phase (most common)
**Secondary**: Break by domain (backend vs frontend)
**Tertiary**: Break by task type (implementation vs testing)

**Goal**: Each file <800 lines, logically cohesive

### 3. Create Breakout Files

**Pattern**: `[plan-name]/phase-[N]-[name].md`
**Alternative**: `[plan-name]/[domain]-tasks.md`

**Each file includes**:
- Phase/section overview
- Relevant tasks with subagent assignments
- Quality gates for that section
- Links back to parent plan

### 4. Update Parent Plan

- Add table of contents linking to breakout files
- Keep executive summary and overview in parent
- Replace detailed sections with links:

```markdown
## Phase 2: Repository Layer
See [Phase 2 Implementation Details](./[plan-name]/phase-2-repository.md)
```

- Maintain quality gates summary in parent

### 5. Validate Optimization

Checklist:
- [ ] Each file <800 lines
- [ ] All content preserved
- [ ] Links work correctly
- [ ] Logical grouping maintained
- [ ] Progressive disclosure achieved

## Output

- Optimized parent plan (summary + links)
- Breakout files for detailed content
- Improved token efficiency (95%+ reduction in single-load context)

## Example

**Input**: `docs/project_plans/implementation_plans/harden-polish/sidebar-polish-v1.md` (1200 lines)

**Analysis**:
- 8 phases, ~150 lines each
- Can group related phases: 1-3 (backend), 4-5 (frontend), 6-8 (validation)

**Output**:

```
sidebar-polish-v1.md (200 lines - summary + links)
├── sidebar-polish-v1/
│   ├── phase-1-3-backend.md (450 lines)
│   │   - Phase 1: Database - Sidebar state, user preferences
│   │   - Phase 2: Repository - State management, RLS
│   │   - Phase 3: Service - Preference sync, DTOs
│   ├── phase-4-5-frontend.md (400 lines)
│   │   - Phase 4: API - Endpoints for sidebar state
│   │   - Phase 5: UI - Sidebar component, animations
│   └── phase-6-8-validation.md (350 lines)
│       - Phase 6: Testing - Unit, integration, visual
│       - Phase 7: Documentation - Component docs, API docs
│       - Phase 8: Deployment - Feature flags, rollout
```

**Token Efficiency**: 67% reduction for targeted queries

[Return to Planning Skill](../SKILL.md)
