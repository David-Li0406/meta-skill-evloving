---
name: github-issue-creator
description: |
  Generate comprehensive GitHub issues for ROLESENSE.ai sprints by leveraging project documentation.
  Use when: (1) Creating sprint epic issues, (2) Creating feature/FR issues with subtasks,
  (3) Creating bug or task issues, (4) Preparing issues for PR and code review workflow.
  Triggers: "create issue", "github issue", "open issue", "sprint issue", "FR issue", "feature issue".
  References docs/ folder structure: PRD, FRD, epics, workflows, sprints, UI-UX-Design-Spec.
---

# GitHub Issue Creator for ROLESENSE.ai

Generate GitHub issues that leverage project documentation for complete context, enabling smooth PR and code review workflows.

## Documentation Structure

The project documentation follows this structure:

```
docs/
├── PRD.md                      # Product Requirements
├── FRD.md                      # Functional Requirements
├── architecture.md             # System Architecture
├── UI-UX-Design-Spec.md        # UI/UX Design Specifications
├── Technology-Stack.md         # Tech Stack Reference
├── project_sprint_plan.md      # Master Sprint Roadmap
├── epics/                      # Epic definitions (EPIC-*.md)
│   ├── EPIC-SYS-01.md
│   ├── EPIC-ING-01.md
│   ├── EPIC-JOB-01.md
│   ├── EPIC-TLR-01.md
│   └── EPIC-EXP-01.md
├── workflows/                  # Workflow definitions (WF-*.md)
│   └── WF-XX-XXX-*.md
└── sprint-{N}/                 # Sprint folders
    ├── sprint-plan.md          # Sprint overview and goals
    ├── backlog.md              # Detailed task backlog
    ├── issue-description.md    # Sprint issue summary
    ├── FR-*-*.md               # Functional requirement specs
    └── github-issues/          # Ready-to-use issue templates
```

## Issue Creation Workflow

### Step 1: Gather Context

Before creating any issue, read the relevant documentation:

1. **For Sprint Epic Issues:**
   - `docs/project_sprint_plan.md` - Overall roadmap context
   - `docs/sprint-{N}/sprint-plan.md` - Sprint goals and scope
   - `docs/sprint-{N}/issue-description.md` - Sprint summary
   - `docs/epics/EPIC-*.md` - Related epic details

2. **For Feature/FR Issues:**
   - `docs/sprint-{N}/FR-*-*.md` - Detailed FR specification
   - `docs/sprint-{N}/backlog.md` - Task breakdown
   - `docs/workflows/WF-*.md` - Related workflow
   - `docs/UI-UX-Design-Spec.md` - UI/UX requirements (if frontend)

3. **For Bug/Task Issues:**
   - Relevant sprint and FR documentation
   - `docs/architecture.md` - Technical context

### Step 2: Create Issue Using Template

Use the appropriate template from `references/issue-templates.md`:

- **Epic Issue** - For sprint-level tracking
- **Feature Issue** - For FR implementation with subtasks
- **Task Issue** - For individual work items
- **Bug Issue** - For defect tracking

### Step 3: Add Documentation References

Every issue MUST include a References section linking to:

```markdown
## 📎 References

| Document | Link |
|----------|------|
| Sprint Plan | `docs/sprint-{N}/sprint-plan.md` |
| Epic | `docs/epics/EPIC-*.md` |
| Workflow | `docs/workflows/WF-*.md` |
| FR Spec | `docs/sprint-{N}/FR-*-*.md` |
| UI/UX | `docs/UI-UX-Design-Spec.md` |
```

### Step 4: Define Subtasks for PRs

Break down issues into subtasks that map to individual PRs:

- **Backend subtasks** - API endpoints, services, models
- **Frontend subtasks** - Components, composables, stores
- **Test subtasks** - Unit, integration, E2E tests
- **Infra subtasks** - Config, Docker, CI/CD

## Branch Naming Convention

```
{Sprint}-{Feature-Name}
```

Examples:
- `Sprint2-Resume-Ingestion`
- `Sprint3-LinkedIn-Import`
- `Sprint4-Match-Scoring`

## Label Standards

| Label | Usage |
|-------|-------|
| `epic` | Sprint-level tracking issues |
| `feature` | New functionality |
| `bug` | Defect fixes |
| `enhancement` | Improvements |
| `sprint-{N}` | Sprint association |
| `priority:high/medium/low` | Priority level |
| `backend` | Backend work |
| `frontend` | Frontend work |
| `tests` | Testing work |
| `EPIC-*` | Epic association |

## PR and Code Review Workflow

Issues created with this skill support the PR workflow:

1. **Issue Created** → Developer assigned
2. **Branch Created** → From main, named per convention
3. **Development** → Commits reference issue number
4. **PR Created** → Links to issue, includes checklist
5. **Code Review** → Reviewers check against acceptance criteria
6. **Merge** → PR merged, issue closed

### PR Description Template

```markdown
## Summary
Brief description of changes

## Related Issue
Closes #{issue_number}

## Changes
- Change 1
- Change 2

## Checklist
- [ ] Code follows project style
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] UI matches design spec (if applicable)

## Screenshots (if UI changes)
```

## Quick Reference

### Create Sprint Epic Issue

```bash
# 1. Read sprint documentation
Read: docs/project_sprint_plan.md
Read: docs/sprint-{N}/sprint-plan.md
Read: docs/sprint-{N}/issue-description.md

# 2. Generate issue using Epic template
# 3. Create branch: Sprint{N}-{Feature-Name}
```

### Create FR Issue with Subtasks

```bash
# 1. Read FR specification
Read: docs/sprint-{N}/FR-*-*.md
Read: docs/sprint-{N}/backlog.md
Read: docs/UI-UX-Design-Spec.md (if frontend)

# 2. Generate issue using Feature template
# 3. Create subtask issues for each work area
```

## Reference Files

For detailed templates and patterns, see:

- `references/issue-templates.md` - Complete issue templates
- `references/documentation-map.md` - Documentation navigation guide
- `references/pr-workflow.md` - PR and review process details
