---
name: product-requirements-documentation
description: Use this skill to create and manage comprehensive Product Requirements Documents (PRDs) for feature planning, ensuring alignment among stakeholders and guiding implementation.
---

# Product Requirements Documentation Skill

This skill assists in creating and managing Product Requirements Documents (PRDs) that outline user stories, acceptance criteria, and technical specifications for new features or enhancements.

## What is a PRD?

A **Product Requirements Document (PRD)** is a structured specification that:

1. Breaks a feature into **small, independent user stories**.
2. Defines **verifiable acceptance criteria** for each story.
3. Orders tasks by **dependency** (schema → backend → UI).

## When to Use

- Planning a new feature or product.
- Documenting requirements before development.
- Aligning stakeholders on scope and priorities.
- Creating technical specifications for handoff.

## Quick Start

1. Create/edit `agents/prd.json` in the project.
2. Define user stories with acceptance criteria.
3. Track progress by updating `passes: false` → `true`.

## PRD Structure

### Standard Template

```markdown
# [Feature Name] PRD

## Overview
**Author:** [Name]
**Status:** Draft | In Review | Approved
**Last Updated:** YYYY-MM-DD
**Target Release:** [Version/Quarter]

## Problem Statement
[2-3 sentences describing the problem]

## Goals & Success Metrics
| Goal | Metric | Target |
|------|--------|--------|
| Primary goal | How we measure | Success threshold |

## User Stories
### [Persona 1]
- As a [persona], I want to [action] so that [benefit]

## Requirements
### Functional Requirements
| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| FR-1 | Description | P0/P1/P2 | |

### Non-Functional Requirements
- Performance: [targets]
- Security: [requirements]
- Accessibility: [standards]

## Design
[Link to designs or embed key screens]

## Technical Approach
[High-level architecture, key decisions]

## Out of Scope
- [Explicitly excluded items]

## Dependencies
- [External dependencies]

## Risks & Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| | High/Med/Low | |

## Timeline
| Phase | Duration | Deliverable |
|-------|----------|-------------|
| | | |

## Open Questions
- [ ] Question 1
- [ ] Question 2
```

## Best Practices

- **Small, focused stories**: Each story should fit in one iteration.
- **Clear acceptance criteria**: Testable and verifiable outcomes.
- **Priority ordering**: Consider dependencies and importance.
- **AG4ONE compliance**: Ensure compatibility with autonomous development cycles.

## Example Output

```json
{
  "project": "MyApp",
  "branchName": "feature-name",
  "description": "Short description of the feature",
  "userStories": [
    {
      "id": "US-001",
      "title": "Add priority field to database",
      "description": "As a developer, I need to store task priority.",
      "acceptanceCriteria": [
        "Add priority column: 'high' | 'medium' | 'low'",
        "Generate and run migration",
        "Typecheck passes"
      ],
      "priority": 1,
      "passes": false,
      "notes": ""
    }
  ]
}
```

## Progress Tracking

Update `passes: true` when a story is complete. Use the `notes` field for runtime observations.

## Collaboration Workflow

1. **Draft Phase**: Create initial PRD with known information.
2. **Review Phase**: Stakeholder review and feedback.
3. **Approval Phase**: Final sign-off and create implementation tickets.
4. **Living Document**: Update as decisions are made and track changes.

## Important Reminders

- **Always** start with the problem, not the solution.
- **Always** define measurable success criteria.
- **Always** include an "Out of Scope" section.
- **Never** skip user stories—they drive acceptance criteria.
- **Ask** clarifying questions before drafting.

## Resources

For detailed documentation and templates, refer to `references/templates.md`.