---
name: sdd-workflow-management
description: Use this skill to manage the entire Software Design Document (SDD) workflow, from requirements definition to implementation and review.
---

# Skill body

## Overview

This skill orchestrates the entire SDD workflow, integrating various sub-skills to ensure a cohesive process from requirements definition to implementation and maintenance.

## Main Functions
- Manage the creation and maintenance of SDD documents, including requirements, design, and tasks.
- Execute tasks as defined in the SDD and perform reverse reviews to ensure consistency.
- Handle troubleshooting and document management throughout the project lifecycle.

## When to Use This Skill
- When starting a new project that requires a complete set of SDD documents.
- To ensure consistency across requirements, design, and task documentation.
- During the implementation phase to execute tasks and conduct reverse reviews.
- For troubleshooting issues and analyzing root causes in the system.
- To manage and archive completed tasks and documents.

## Workflow

### New Development Flow

```text
1. Initialize → Create the docs/ directory structure
      ↓
2. requirements-defining → Create docs/requirements/
      ↓ User confirmation and approval
3. software-designing → Create docs/design/
      ↓ User confirmation and approval
4. task-planning → Create docs/tasks/
      ↓ User confirmation and approval
5. task-executing → Execute tasks as per docs/tasks/
      ↓
6. sdd-troubleshooting → Analyze issues and propose fixes
      ↓
7. sdd-document-management → Archive completed tasks and documents
```

## Task Execution Management

### Task Status Management

```text
TODO → IN_PROGRESS → DONE
         ↓
      BLOCKED (if issues arise)
```

### Update Timing

| Timing          | Status        | Action                                      |
|----------------|---------------|---------------------------------------------|
| At task start  | `IN_PROGRESS` | Update task file and index.md, commit      |
| At task end    | `DONE`       | Add completion summary, update, commit     |
| If issues arise | `BLOCKED`    | Document the reason for blocking            |

### Pre-completion Checklist

Before marking a task as DONE, analyze the task content and identify relevant categories, then confirm using the checklist.

### Checklist Application Rules

1. **Analyze Task Content**: Identify relevant categories from the task description and acceptance criteria.
2. **Present Checklist**: Show checklists for all identified categories.
3. **Conduct Confirmation**: Ask the user if each item has been confirmed.
4. **Warning for Unconfirmed Items**: Display a warning if there are unconfirmed items and hold completion.

### Specific Conditions

- **UI Changes**: Confirm visual checks in actual browsers and across different screen sizes.
- **External System Integration**: Verify functionality in actual systems, not mocks.
- **Data Operations**: Check behavior with edge cases and boundary values.

This skill consolidates the task execution and SDD documentation processes, ensuring a streamlined workflow for software development projects.