---
name: sdd-workflow-management
description: Use this skill to manage the entire Software Design Document (SDD) workflow, from requirements definition to implementation and review.
---

# SDD Workflow Management Skill

This skill orchestrates the creation, management, and implementation of Software Design Documents (SDD), covering all phases from requirements definition to implementation and maintenance.

## Overview

This skill integrates the following sub-skills to manage the entire process:

| Sub-skill                     | Role                                      | Output                     |
|-------------------------------|-------------------------------------------|----------------------------|
| **requirements-defining**     | Define requirements using EARS notation    | docs/requirements/         |
| **software-designing**        | Design technical architecture              | docs/design/               |
| **task-planning**             | Decompose tasks for AI agents             | docs/tasks/                |
| **task-executing**            | Execute tasks and conduct reverse reviews | Implementation code        |
| **sdd-troubleshooting**       | Analyze issues and formulate fixes        | docs/troubleshooting/, docs/tasks/ |
| **sdd-document-management**   | Manage and maintain documentation          | docs/archive/, docs/reports/ |

## When to Use This Skill

### Initialization
- When a new project requires a complete set of SDD documents.

### Overall Management
- To verify the consistency among the three documents.
- To conduct reverse reviews (tasks → design → requirements).

### Implementation Phase
- When implementing according to docs/tasks/.
- When a reverse review is needed after implementation.

### Troubleshooting
- When system malfunctions or issues are reported.
- To analyze root causes and formulate corrective actions.

### Document Management
- To detect and resolve inconsistencies between documents.
- To confirm synchronization between implementation and documentation.
- To archive completed tasks and organize bloated files.

### Individual Tasks
- For executing specific processes, each sub-skill can be used directly:
  - Requirements only → `requirements-defining`
  - Design only → `software-designing`
  - Task planning only → `task-planning`
  - Implementation only → `task-executing`
  - Issue analysis only → `sdd-troubleshooting`
  - Document management only → `sdd-document-management`

## Workflow

### New Development Flow

```text
1. Initialization → Create docs/ directory structure
      ↓
2. requirements-defining → docs/requirements/
      ↓ User confirmation and approval
3. software-designing → docs/design/
      ↓ User confirmation and approval
4. task-planning → docs/tasks/
      ↓ User confirmation and approval
5. Document reverse review
      ↓
6. task-executing → Implementation code
      ↓
7. Implementation reverse review → Completion
```

### Troubleshooting Flow

```text
1. Confirm issue occurrence
      ↓
2. Analyze root cause
      ↓
3. Cross-check with specifications (docs/requirements/, docs/design/)
      ↓
4. Formulate corrective action
      ↓
5. ★ User approval ★ (mandatory gate)
      ↓
6. Decompose tasks → Add to docs/tasks/
      ↓
7. task-executing → Implement fixes
```

## Best Practices

1. **Always update status at task start**: Change to IN_PROGRESS before committing.
2. **Adhere to commit templates**: Always include references to related documents.
3. **Confirm all acceptance criteria**: Do not mark as complete if any are unmet.
4. **Do not skip reverse reviews**: Early detection of issues through consistency checks.
5. **Avoid using emojis**: Prohibited in commit messages and documents.

## Resources

### References
- Workflow guide: `references/workflow_guide_ja.md`
- Verification checklist: `references/checklist_ja.md`

### Sub-skills
- Requirements definition: `requirements-defining/SKILL.md`
- Design: `software-designing/SKILL.md`
- Task planning: `task-planning/SKILL.md`
- Task execution: `task-executing/SKILL.md`
- Troubleshooting: `sdd-troubleshooting/SKILL.md`
- Document management: `sdd-document-management/SKILL.md`