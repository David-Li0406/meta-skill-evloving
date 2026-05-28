# Sample Prompt: Sprint 2 GitHub Issue Creation

Use this prompt template to leverage the `github-issue-creator` skill for creating Sprint 2 issues.

---

## Full Sprint 2 Prompt

Copy and paste the following prompt to create all Sprint 2 GitHub issues:

```
Using the @agent/skills/github-issue-creator skill, please create GitHub issues for Sprint 2 - Resume Ingestion.

## Context
Review the following documentation to understand Sprint 2 scope:
- @docs/sprint-2/sprint-plan.md - Sprint goals and timeline
- @docs/sprint-2/backlog.md - Detailed task breakdown
- @docs/epics/EPIC-ING-01.md - Resume Ingestion epic
- @docs/sprint-2/FR-ING-001-Multi-Format-Resume-Upload.md - Upload FR spec
- @docs/sprint-2/FR-ING-002-Resume-Parsing-Structure.md - Parsing FR spec (to be created)
- @docs/workflows/WF-01-001-resume-upload-parsing.md - Upload workflow
- @docs/UI-UX-Design-Spec.md (sections 4A.3, 4A.4, 6.1.1) - UI specifications

## Deliverables

### 1. Epic Issue
Create the Sprint Epic issue:
- Title: "Sprint 2 – Resume Ingestion v1"
- Include sprint goal, scope table, DoD checklist
- Link to child feature issues
- Branch: `Sprint2-Resume-Ingestion`

### 2. Feature Issues
Create feature issues for:

**FR-ING-001: Multi-Format Resume Upload**
- User story, acceptance criteria (Gherkin format)
- Subtasks for: backend, frontend, tests, infra/config
- Reference UI-UX-Design-Spec.md sections 4A.3, 6.1.1
- Estimate: ~40h total

**FR-ING-002: Resume Parsing & Structure**
- User story, acceptance criteria (Gherkin format)
- Subtasks for: backend, frontend, tests
- Reference workflow WF-01-001
- Estimate: ~34h total

### 3. Subtask Issues
Create individual subtask issues for each PR:

For FR-ING-001:
- `[FR-ING-001] backend - Setup MinIO and upload endpoint`
- `[FR-ING-001] backend - File validation service`
- `[FR-ING-001] frontend - Upload UI with drag-and-drop`
- `[FR-ING-001] tests - Unit and integration tests`
- `[FR-ING-001] infra - Docker config and env variables`

For FR-ING-002:
- `[FR-ING-002] backend - PDF/DOCX text extraction`
- `[FR-ING-002] backend - JSON Resume schema mapping`
- `[FR-ING-002] frontend - Parsed resume preview`
- `[FR-ING-002] tests - Parser unit tests`

## Output Format
For each issue, provide:
1. Issue title
2. Complete issue body (ready to paste into GitHub)
3. Labels to apply
4. Milestone: Sprint 2
```

---

## Shorter Prompts for Specific Tasks

### Create Epic Only

```
Using @docs/.skills/github-issue-creator, create the Sprint 2 Epic issue.

Reference:
- @docs/sprint-2/sprint-plan.md
- @docs/epics/EPIC-ING-01.md

Title: "Sprint 2 – Resume Ingestion v1"
Branch: `Sprint2-Resume-Ingestion`
Include: Goal, scope table, DoD, child issue placeholders
```

### Create Single Feature Issue

```
Using @docs/.skills/github-issue-creator, create the feature issue for FR-ING-001.

Reference:
- @docs/sprint-2/FR-ING-001-Multi-Format-Resume-Upload.md
- @docs/workflows/WF-01-001-resume-upload-parsing.md
- @docs/UI-UX-Design-Spec.md (sections 4A.3, 6.1.1)
- @docs/sprint-2/backlog.md (FR-ING-001 tasks)

Include:
- User story
- Acceptance criteria (Gherkin)
- Subtasks for backend, frontend, tests, infra
- Documentation references
- Estimate breakdown
```

### Create Subtask Issues

```
Using @docs/.skills/github-issue-creator, create subtask issues for FR-ING-001.

Reference:
- @docs/sprint-2/backlog.md
- @docs/sprint-2/FR-ING-001-Multi-Format-Resume-Upload.md

Create these subtasks:
1. `[FR-ING-001] backend - Setup MinIO container and boto3 client` (4h)
2. `[FR-ING-001] backend - Create upload endpoint with validation` (6h)
3. `[FR-ING-001] frontend - Upload UI with drag-and-drop` (8h)
4. `[FR-ING-001] tests - Unit and integration tests` (6h)
5. `[FR-ING-001] infra - File size limits and MIME config` (3h)

Each subtask should include:
- Clear scope description
- Technical details from FR spec
- Acceptance criteria
- Parent issue reference
```

---

## Quick Reference: Key Documentation for Sprint 2

| Document | Path | Use For |
|----------|------|---------|
| Sprint Plan | `docs/sprint-2/sprint-plan.md` | Goals, timeline, deliverables |
| Backlog | `docs/sprint-2/backlog.md` | Task breakdown, estimates |
| Epic Spec | `docs/epics/EPIC-ING-01.md` | Epic-level requirements |
| FR-ING-001 | `docs/sprint-2/FR-ING-001-*.md` | Upload feature details |
| FR-ING-002 | `docs/sprint-2/FR-ING-002-*.md` | Parsing feature details |
| Workflow | `docs/workflows/WF-01-001-*.md` | End-to-end flow |
| UI/UX Spec | `docs/UI-UX-Design-Spec.md` | Design requirements |
| └─ Section 4A.3 | Resume Creation Modal | Upload modal design |
| └─ Section 4A.4 | New Scan Interface | Scan page design |
| └─ Section 6.1.1 | Run Free Scan Flow | User flow steps |

---

## Expected Output Structure

When the skill processes the prompt, expect output like:

```
## Epic Issue: Sprint 2 – Resume Ingestion v1

**Labels:** `epic`, `sprint-2`, `priority: high`
**Milestone:** Sprint 2

[Full issue body...]

---

## Feature Issue: FR-ING-001 - Multi-Format Resume Upload

**Labels:** `type: feature`, `component: backend`, `component: frontend`, `priority: critical`, `sprint-2`
**Milestone:** Sprint 2
**Parent:** #{epic_number}

[Full issue body...]

---

## Subtask: [FR-ING-001] backend - Setup MinIO container and boto3 client

**Labels:** `type: subtask`, `component: backend`, `component: infra`, `sprint-2`
**Milestone:** Sprint 2
**Parent:** #{feature_number}

[Full issue body...]
```

---

## Tips for Best Results

1. **Reference specific doc sections** - Point to exact sections in UI-UX-Design-Spec.md (e.g., "section 4A.3")

2. **Include estimate hints** - Mention expected hours from backlog.md

3. **Specify output format** - Ask for "ready to paste into GitHub" format

4. **Request labels explicitly** - Ensure proper categorization

5. **Link parent issues** - Maintain traceability with `#{issue_number}` placeholders

6. **One prompt per scope** - For complex sprints, break into Epic → Features → Subtasks
