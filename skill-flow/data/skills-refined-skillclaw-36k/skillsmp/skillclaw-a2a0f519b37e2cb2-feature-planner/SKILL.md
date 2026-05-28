---
name: feature-planner
description: Use this skill when planning features, organizing work, breaking down tasks, creating roadmaps, or structuring development strategy with a focus on phase-based delivery and quality gates.
---

# Feature Planner

## Purpose
Generate structured, phase-based plans where:
- Each phase delivers complete, runnable functionality.
- Quality gates enforce validation before proceeding.
- User approves the plan before any work begins.
- Progress is tracked via markdown checkboxes.
- Each phase is 1-4 hours maximum.

## Planning Workflow

### Step 1: Requirements Analysis
1. Read relevant files to understand codebase architecture.
2. Identify dependencies and integration points.
3. Assess complexity and risks.
4. Determine appropriate scope (small/medium/large).

### Step 2: Phase Breakdown with TDD Integration
Break the feature into 3-7 phases where each phase:
- **Test-First**: Write tests BEFORE implementation.
- Delivers working, testable functionality.
- Takes 1-4 hours maximum.
- Follows the Red-Green-Refactor cycle.
- Has measurable test coverage requirements.
- Can be rolled back independently.
- Has clear success criteria.

**Phase Structure**:
- **Phase Name**: Clear deliverable.
- **Goal**: What working functionality this produces.
- **Test Strategy**: What test types, coverage target, test scenarios.
- **Tasks** (ordered by TDD workflow):
  1. **RED Tasks**: Write failing tests first.
  2. **GREEN Tasks**: Implement minimal code to make tests pass.
  3. **REFACTOR Tasks**: Improve code quality while tests stay green.
- **Quality Gate**: TDD compliance + validation criteria.
- **Dependencies**: What must exist before starting.
- **Coverage Target**: Specific percentage or checklist for this phase.

### Step 3: Plan Document Creation
Use `plan-template.md` to generate: `docs/plans/PLAN_<feature-name>.md`.

Include:
- Overview and objectives.
- Architecture decisions with rationale.
- Complete phase breakdown with checkboxes.
- Quality gate checklists.
- Risk assessment table.
- Rollback strategy per phase.
- Progress tracking section.
- Notes & learnings area.

### Step 4: User Approval
**CRITICAL**: Use AskUserQuestion to get explicit approval before proceeding.

Ask:
- "Does this phase breakdown make sense for your project?"
- "Any concerns about the proposed approach?"
- "Should I proceed with creating the plan document?"

Only create the plan document after user confirmation.