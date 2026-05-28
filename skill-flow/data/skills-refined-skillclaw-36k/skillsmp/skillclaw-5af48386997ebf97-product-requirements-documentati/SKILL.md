---
name: product-requirements-documentation
description: Use this skill when creating and managing Product Requirements Documents (PRDs) to ensure clear communication of feature specifications and requirements.
---

# Skill body

## Overview

This skill helps create comprehensive Product Requirements Documents (PRDs) for feature planning and development. A PRD outlines user stories, acceptance criteria, and technical specifications to align stakeholders and guide implementation.

## When to Use

- Planning a new feature or product
- Documenting requirements before development
- Aligning stakeholders on scope and priorities
- Creating technical specifications for handoff

## PRD Structure

1. **Project Metadata**
   - `project`: Name of the project
   - `branchName`: Git branch for this feature (prefix with `ralph/`)
   - `description`: Short description of the feature

2. **User Stories**
   - Each user story should be small and focused, ideally completable in one context window.
   - Format:
     ```json
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
     ```

3. **Acceptance Criteria**
   - Define clear, verifiable outcomes for each user story.

4. **Prioritization**
   - Set priorities for implementation order based on dependencies and importance.

## Quick Start

1. Create/edit `agents/prd.json` in the project.
2. Define user stories with acceptance criteria.
3. Track progress by updating `passes: false` to `true` when completed.

## Best Practices

- **Small, focused stories**: Each story should fit in one iteration.
- **Clear acceptance criteria**: Ensure they are testable and verifiable.
- **Priority ordering**: Consider dependencies and importance.
- **Documentation**: Keep all relevant information organized and accessible.

## Example Output

```json
{
  "project": "MyApp",
  "branchName": "ralph/feature-name",
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