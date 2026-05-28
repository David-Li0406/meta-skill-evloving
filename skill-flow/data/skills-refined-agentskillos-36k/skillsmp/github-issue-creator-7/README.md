# GitHub Issue Creator Skill

A specialized skill for generating comprehensive GitHub issues for ROLESENSE.ai development sprints by leveraging the project's documentation structure.

---

## Overview

This skill helps create well-structured GitHub issues that properly reference project documentation, enabling a smooth workflow from issue creation through PR, code review, and merge.

### When to Use This Skill

- Creating sprint epic issues
- Creating feature/FR issues with subtasks
- Creating individual subtask issues for PRs
- Creating bug reports with proper context
- Creating enhancement proposals

---

## Skill Files

### Core

| File | Description |
|------|-------------|
| [SKILL.md](./SKILL.md) | Main skill file with workflow steps, documentation structure overview, and quick-start guidance |

### References

| File | Description |
|------|-------------|
| [references/documentation-map.md](./references/documentation-map.md) | Complete navigation guide to all project documentation (~65 files), with reading strategies for different issue types |
| [references/issue-templates.md](./references/issue-templates.md) | Ready-to-use templates for Epic, Feature, Subtask, Bug, and Enhancement issues with label standards |
| [references/pr-workflow.md](./references/pr-workflow.md) | Full PR and code review workflow from branch creation through merge, including commit conventions |

### Examples

| File | Description |
|------|-------------|
| [examples/sprint-2-prompt.md](./examples/sprint-2-prompt.md) | Ready-to-use prompts for creating Sprint 2 GitHub issues |

### Directories

| Directory | Purpose |
|-----------|---------|
| `assets/` | Reserved for diagrams, images, and visual aids |
| `scripts/` | Reserved for future automation scripts |
| `examples/` | Sample prompts for different sprints |

---

## Quick Start

### 1. Creating a Sprint Epic Issue

```markdown
# Sprint {N} – {Sprint Name}

## 🎯 Goal
{One-sentence sprint goal from sprint-plan.md}

## 📋 Scope
| ID | Feature | Priority |
|----|---------|----------|
| FR-XXX-001 | Feature Name | P0 |

## ✅ Definition of Done
- [ ] All FR issues completed
- [ ] Tests passing (>80% coverage)
- [ ] Documentation updated
- [ ] Code reviewed and merged

## 🔗 Child Issues
- [ ] #{issue_number} - FR-XXX-001: Feature Name

## 📚 Documentation
- Sprint Plan: `docs/sprint-{n}/sprint-plan.md`
- Backlog: `docs/sprint-{n}/backlog.md`

## 🌿 Branch
`Sprint{N}-{Feature-Name}`
```

### 2. Creating a Feature Issue

```markdown
# FR-XXX-001: Feature Title

**Parent Epic:** #{epic_number}
**Priority:** P0 | **Estimate:** Xh | **Sprint:** N

## 📖 User Story
As a {user type}, I want to {action} so that {benefit}.

## ✅ Acceptance Criteria
- [ ] Given {context}, when {action}, then {result}

## 📋 Subtasks
- [ ] `[FR-XXX-001] backend - {task}`
- [ ] `[FR-XXX-001] frontend - {task}`
- [ ] `[FR-XXX-001] tests - {task}`

## 📚 Documentation
- FR Spec: `docs/sprint-{n}/FR-XXX-001-*.md` (or `docs/frd/FR-XXX-001-*.md` for cross-cutting FRs)
- Workflow: `docs/workflows/WF-XX-XXX-*.md`
- UI/UX: `docs/UI-UX-Design-Spec.md#section-X`
```

---

## Documentation Structure

The skill leverages ROLESENSE.ai's documentation hierarchy:

```
docs/
├── PRD.md                    # Product vision & features
├── FRD.md                    # Functional requirements index
├── UI-UX-Design-Spec.md      # Design specifications
├── workflows/                # Workflow definitions
├── epics/                    # Epic specifications
├── sprint-{n}/               # Sprint-specific docs
│   ├── sprint-plan.md
│   ├── backlog.md
│   ├── FR-XXX-001-*.md      # Sprint-specific FR specs
│   └── github-issues/
└── technical/                # Architecture & tech specs
```

See [documentation-map.md](./references/documentation-map.md) for complete details.

---

## Workflow Integration

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Issue     │───▶│   Branch    │───▶│     PR      │───▶│   Review    │───▶│   Merge     │
│  Created    │    │  Created    │    │  Created    │    │  Complete   │    │  to Main    │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

### Branch Naming

```
{Sprint}-{Feature-Name}
```

Example: `Sprint2-Resume-Ingestion`

### Commit Convention

```
{type}({scope}): {description}

Refs: #{issue_number}
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

See [pr-workflow.md](./references/pr-workflow.md) for complete details.

---

## Labels Reference

### Priority
- `priority: critical` - P0, blocks release
- `priority: high` - P1, sprint commitment
- `priority: medium` - P2, should have
- `priority: low` - P3, nice to have

### Type
- `type: feature` - New functionality
- `type: bug` - Defect fix
- `type: enhancement` - Improvement
- `type: docs` - Documentation
- `type: test` - Test coverage

### Component
- `component: backend` - FastAPI/Python
- `component: frontend` - Nuxt/Vue
- `component: infra` - DevOps/Config
- `component: ai` - LLM/OLLAMA

### Status
- `status: ready` - Ready to work
- `status: in-progress` - Being worked on
- `status: blocked` - Waiting on dependency
- `status: review` - In code review

See [issue-templates.md](./references/issue-templates.md) for complete label reference.

---

## Best Practices

1. **Always reference documentation** - Link to relevant FR specs, workflows, and UI/UX sections
2. **Use Gherkin for acceptance criteria** - Given/When/Then format ensures testability
3. **Break down into subtasks** - Each subtask should be a single PR
4. **Include estimates** - Help with sprint planning
5. **Link parent/child issues** - Maintain traceability
6. **Apply consistent labels** - Enable filtering and reporting

---

## Related Documentation

- [Project Sprint Plan](../project_sprint_plan.md) - Overall sprint roadmap
- [FRD Index](../FRD.md) - All functional requirements
- [UI/UX Design Spec](../UI-UX-Design-Spec.md) - Design specifications
- [Technical Architecture](../technical/) - System architecture docs

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-01-25 | Initial skill creation |
