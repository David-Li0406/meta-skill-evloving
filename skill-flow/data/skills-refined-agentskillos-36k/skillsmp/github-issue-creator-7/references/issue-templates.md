# GitHub Issue Templates

## 1. Sprint Epic Issue Template

Use for sprint-level tracking that contains multiple feature issues.

```markdown
# Sprint {N} – {Sprint Name}

## 🎯 Goal

{One-sentence sprint goal from sprint-plan.md}

## 📋 Functional Requirements

| FR ID | Name | Priority |
|-------|------|----------|
| **{FR-ID-001}** | {FR Name} | P0 |
| **{FR-ID-002}** | {FR Name} | P0 |

## ✅ Sprint Checklist

### API
- [ ] {Endpoint 1} implemented
- [ ] {Endpoint 2} implemented
- [ ] Validation logic complete
- [ ] Integration tested

### UI
- [ ] {Component 1} wired
- [ ] {Component 2} wired
- [ ] Design tokens applied per UI-UX-Design-Spec.md

### Quality
- [ ] Unit tests written (>80% coverage)
- [ ] Integration tests complete
- [ ] E2E test for main flow
- [ ] Demo scenario passes

## 🧪 Demo Scenario

1. {Step 1}
2. {Step 2}
3. {Step 3}
4. {Expected outcome}

## 📎 References

| Document | Link |
|----------|------|
| Sprint Plan | `docs/sprint-{N}/sprint-plan.md` |
| Backlog | `docs/sprint-{N}/backlog.md` |
| Epic | `docs/epics/{EPIC-ID}.md` |
| Workflow | `docs/workflows/{WF-ID}.md` |
| UI/UX | `docs/UI-UX-Design-Spec.md` |

## 🏷️ Labels

`epic`, `sprint-{N}`, `priority:high`

## 📅 Milestone

Sprint {N}

---

## Child Issues

- [ ] {FR-ID-001} - {FR Name}
- [ ] {FR-ID-002} - {FR Name}

## Branch

`Sprint{N}-{Feature-Name}`
```

---

## 2. Feature/FR Issue Template

Use for functional requirement implementation with subtasks.

```markdown
# {FR-ID} - {FR Name}

## 📋 Description

{Brief description of the feature from FR spec}

## 🎯 User Story

> **As a** {user type},
> **I want to** {action},
> **So that** {benefit}.

## ✅ Acceptance Criteria

```gherkin
Scenario: {Happy path scenario}
  Given {precondition}
  And {additional precondition}
  When {action}
  Then {expected result}
  And {additional result}

Scenario: {Error scenario}
  Given {precondition}
  When {invalid action}
  Then {error handling}
```

## 📝 Technical Requirements

### API Endpoints

```
{METHOD} /api/v1/{resource}
Content-Type: application/json
Authorization: Bearer {jwt_token}

Response ({status}):
{
  "field": "value"
}
```

### UI Components (if applicable)

| Component | UI-UX-Design-Spec Section |
|-----------|---------------------------|
| {ComponentName}.vue | Section {X.X} |

### Database Changes (if applicable)

```sql
-- Table: {table_name}
-- Description: {purpose}
```

## ✅ Subtasks

### Backend
- [ ] `[{FR-ID}] backend - {Task description}`
- [ ] `[{FR-ID}] backend - {Task description}`

### Frontend
- [ ] `[{FR-ID}] frontend - {Task description}`
- [ ] `[{FR-ID}] frontend - {Task description}`

### Tests
- [ ] `[{FR-ID}] tests - {Test description}`
- [ ] `[{FR-ID}] tests - {Test description}`

### Infrastructure (if applicable)
- [ ] `[{FR-ID}] infra - {Task description}`

## 📎 References

| Document | Link |
|----------|------|
| FR Spec | `docs/sprint-{N}/{FR-ID}-{Name}.md` |
| Backlog | `docs/sprint-{N}/backlog.md` |
| Epic | `docs/epics/{EPIC-ID}.md` |
| Workflow | `docs/workflows/{WF-ID}.md` |
| UI/UX | `docs/UI-UX-Design-Spec.md` |
| FRD | `docs/FRD.md` (Section X.X) |

## 🏷️ Labels

`feature`, `sprint-{N}`, `priority:{level}`, `backend`, `frontend`, `{EPIC-ID}`

## 📅 Milestone

Sprint {N}

## 🔗 Parent Issue

Sprint {N} – {Sprint Name}

## ⏱️ Estimate

| Category | Hours |
|----------|-------|
| Backend | {X}h |
| Frontend | {X}h |
| Tests | {X}h |
| **Total** | **{X}h** |
```

---

## 3. Subtask Issue Template

Use for individual work items that belong to a feature issue.

```markdown
# [{FR-ID}] {area} - {Task Description}

## 📋 Description

{Detailed description of the task}

## ✅ Acceptance Criteria

- [ ] {Criterion 1}
- [ ] {Criterion 2}
- [ ] {Criterion 3}

## 📝 Implementation Notes

{Technical guidance, code patterns to follow, files to modify}

### Files to Create/Modify

- `{path/to/file1}`
- `{path/to/file2}`

### Dependencies

- {Dependency 1}
- {Dependency 2}

## 🧪 Testing Requirements

- [ ] Unit test: {test description}
- [ ] Integration test: {test description}

## 📎 References

- Parent Issue: #{parent_issue_number}
- FR Spec: `docs/sprint-{N}/{FR-ID}-{Name}.md`
- Relevant section: {Section reference}

## 🏷️ Labels

`task`, `sprint-{N}`, `{area}`, `{EPIC-ID}`

## ⏱️ Estimate

{X} hours
```

---

## 4. Bug Issue Template

Use for defect tracking.

```markdown
# 🐛 {Bug Title}

## 📋 Description

{Clear description of the bug}

## 🔄 Steps to Reproduce

1. {Step 1}
2. {Step 2}
3. {Step 3}

## ✅ Expected Behavior

{What should happen}

## ❌ Actual Behavior

{What actually happens}

## 🖼️ Screenshots/Logs

{Attach screenshots or relevant log output}

## 🔍 Environment

- **Browser**: {browser and version}
- **OS**: {operating system}
- **App Version**: {version or commit}

## 📝 Possible Cause

{If known, describe the suspected cause}

## ✅ Acceptance Criteria

- [ ] Bug is fixed
- [ ] Regression test added
- [ ] No new issues introduced

## 📎 References

- Related FR: `docs/sprint-{N}/{FR-ID}.md`
- Related Epic: `docs/epics/{EPIC-ID}.md`

## 🏷️ Labels

`bug`, `sprint-{N}`, `priority:{level}`, `{area}`

## ⏱️ Estimate

{X} hours
```

---

## 5. Enhancement Issue Template

Use for improvements to existing features.

```markdown
# ✨ {Enhancement Title}

## 📋 Description

{Description of the enhancement}

## 🎯 Motivation

{Why this enhancement is needed}

## 📝 Proposed Changes

{Detailed description of proposed changes}

## ✅ Acceptance Criteria

- [ ] {Criterion 1}
- [ ] {Criterion 2}
- [ ] {Criterion 3}

## 🔄 Impact

- **Affected Components**: {list}
- **Breaking Changes**: {yes/no, details}
- **Performance Impact**: {expected impact}

## 📎 References

- Related FR: {if applicable}
- UI/UX Spec: {section reference if applicable}

## 🏷️ Labels

`enhancement`, `sprint-{N}`, `priority:{level}`, `{area}`

## ⏱️ Estimate

{X} hours
```

---

## Label Reference

### Priority Labels
- `priority:high` - Must complete this sprint
- `priority:medium` - Should complete this sprint
- `priority:low` - Nice to have

### Type Labels
- `epic` - Sprint-level tracking
- `feature` - New functionality
- `bug` - Defect fix
- `enhancement` - Improvement
- `task` - Individual work item
- `documentation` - Doc updates

### Area Labels
- `backend` - Backend/API work
- `frontend` - Frontend/UI work
- `tests` - Testing work
- `infra` - Infrastructure/DevOps
- `database` - Database changes

### Sprint Labels
- `sprint-1`, `sprint-1.5`, `sprint-2`, etc.

### Epic Labels
- `EPIC-SYS-01`, `EPIC-ING-01`, `EPIC-JOB-01`, etc.

---

## Commit Message Convention

```
{type}({scope}): {description}

[optional body]

[optional footer]
Refs: #{issue_number}
```

### Types
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation
- `style` - Formatting
- `refactor` - Code restructure
- `test` - Tests
- `chore` - Maintenance

### Examples
```
feat(resume): add file upload endpoint

Implements POST /api/v1/resumes/upload with:
- Multipart form handling
- MIME type validation
- MinIO storage integration

Refs: #42
```
