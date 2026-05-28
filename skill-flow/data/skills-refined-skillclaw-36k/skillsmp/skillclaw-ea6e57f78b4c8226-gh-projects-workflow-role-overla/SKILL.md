---
name: gh-projects-workflow-role-overlay
description: Use this skill when you need to manage GitHub Projects in different roles, such as project manager, coder, or reviewer, ensuring tasks are appropriately handled based on your role.
---

# Skill body

## Overview
This skill provides role overlays for managing GitHub Projects. Depending on your role, you will perform different actions related to project management, coding, or reviewing.

## Roles

### Project Manager
- Capture ideas as draft items.
- Refine or split tasks as necessary.
- Convert drafts to issues in the appropriate repository/project.
- Manage priorities and keep project status accurate.

### Coder
- Pick up an existing issue assigned to you.
- Implement the solution and link your pull requests (PRs) to the issue.
- Add brief progress notes to the issue.
- Update the status of the issue through the workflow: Todo → In Progress → In Review → Done.
- Avoid backlog shaping unless explicitly requested.

### Reviewer
- Review pull requests for assigned issues.
- Validate the issue’s verification plan and results.
- Leave actionable feedback on the PR.
- Update the status of the issue: keep it In Review, move back to In Progress if changes are requested, and mark it Done only when merged.