# Workflow: Create Implementation Plan from PRD

**Input**: Path to existing PRD or newly created PRD

## Process

### 1. Analyze PRD

- Read full PRD content
- Extract key requirements
- Identify architectural layers needed
- Determine phase breakdown strategy

### 2. Plan Phase Structure

Follow MP layered architecture: routers → services → repositories → DB

**Common Phase Sequence**:
- Database → Repository → Service → API → UI → Testing → Docs → Deployment

**Grouping Strategy**:
- Group related tasks into phases
- Consider parallel work opportunities
- Identify critical path

### 3. Generate Task Breakdown

- Use template: `../templates/implementation-plan-template.md`
- Create tasks for each phase
- Format: Task tables with ID, Name, Description, Acceptance Criteria, Estimate
- Include quality gates for each phase

### 4. Assign Subagents

Reference: `../references/subagent-assignments.md`

**Assignment by task type**:
- Database: `data-layer-expert`
- Backend API: `python-backend-engineer`, `backend-architect`
- Frontend: `ui-engineer-enhanced`, `frontend-developer`
- UI Components: `ui-designer`, `ui-engineer`
- Testing: appropriate testing agents
- Docs: `documentation-writer`, `documentation-complex`

**Format**: Add to each task: "Assigned Subagent(s): agent-1, agent-2"

### 5. Optimize for Token Efficiency

**If total plan >800 lines**: Break into phase-specific files

- Pattern: `[feature-name]-v1/phase-[N]-[name].md`
- Parent plan links to phase files
- Each phase file <800 lines
- See `../references/optimization-patterns.md`

### 6. Generate Files

**Main plan**: `docs/project_plans/implementation_plans/[category]/[feature-name]-v1.md`

**Phase files (if needed)**: `docs/project_plans/implementation_plans/[category]/[feature-name]-v1/phase-[N]-[name].md`

## Output

- Implementation Plan at determined location
- Phase breakdown with subagent assignments
- Linked phase files if plan >800 lines
- Quality gates and success criteria per phase

## Example

**Input PRD**: `docs/project_plans/PRDs/features/realtime-collaboration-v1.md`

**Output**:

Main Plan: `docs/project_plans/implementation_plans/features/realtime-collaboration-v1.md`

**Phase Breakdown**:
| Phase | Title | Assignees |
|-------|-------|-----------|
| 1 | Database Layer (websocket_sessions, edit_locks) | data-layer-expert |
| 2 | Repository Layer (session, lock management) | python-backend-engineer |
| 3 | Service Layer (operational transforms, conflict resolution) | backend-architect |
| 4 | API Layer (WebSocket endpoints, presence API) | python-backend-engineer |
| 5 | UI Layer (collaborative editor, presence indicators) | ui-engineer-enhanced |
| 6 | Testing (unit, integration, E2E conflict scenarios) | testing agents |
| 7 | Documentation (API docs, user guides) | documentation-writer |
| 8 | Deployment (feature flags, monitoring) | DevOps |

**Phase Files (if plan >800 lines)**:
- `realtime-collaboration-v1/phase-1-3-backend.md`
- `realtime-collaboration-v1/phase-4-5-frontend.md`
- `realtime-collaboration-v1/phase-6-8-validation.md`

[Return to Planning Skill](../SKILL.md)
