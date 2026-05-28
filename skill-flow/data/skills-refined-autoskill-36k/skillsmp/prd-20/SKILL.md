---
name: prd
description: Creates Product Requirements Documents (PRDs) for features with user stories in Ralph-compatible format. Use when asked to create a PRD, write requirements, plan a feature, or generate user stories.
---

# PRD Skill

Generates detailed Product Requirements Documents with user stories structured for autonomous Ralph execution.

## Workflow

1. **Gather Requirements**: Ask clarifying questions about the feature
2. **Generate PRD**: Create comprehensive markdown PRD
3. **Save Output**: Write to `tasks/prd-[feature-name].md`

## Clarifying Questions

Before generating a PRD, ask these questions (adapt based on context):

1. **Feature Name**: What should we call this feature?
2. **Problem Statement**: What problem does this solve? Who has this problem?
3. **Success Criteria**: How do we know when this is done? What metrics matter?
4. **Scope**: What's in scope? What's explicitly out of scope?
5. **User Roles**: Who uses this feature? Are there different user types?
6. **Key Workflows**: What are the main user journeys?
7. **Technical Constraints**: Any specific tech requirements or limitations?
8. **Dependencies**: Does this depend on other features or systems?
9. **Priority**: Is this high/medium/low priority? Any deadline?

## PRD Template

Generate PRDs with this structure:

```markdown
# PRD: [Feature Name]

## Overview
Brief description of the feature and its purpose.

## Problem Statement
What problem this solves and for whom.

## Goals
- Primary goal
- Secondary goals

## Non-Goals (Out of Scope)
- What we're explicitly NOT doing

## User Stories

### [US-001] [Story Title]
**As a** [user type]
**I want** [capability]
**So that** [benefit]

**Acceptance Criteria:**
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

**Technical Notes:**
- Implementation hints
- Dependencies

---

### [US-002] [Next Story Title]
...

## Technical Requirements
- API endpoints needed
- Database changes
- External integrations

## UI/UX Requirements
- Wireframes or descriptions
- User flow diagrams

## Testing Requirements
- Unit test coverage
- Integration test scenarios
- E2E test cases

## Success Metrics
- KPIs to track
- Definition of success

## Timeline
- Estimated effort
- Milestones
```

## User Story Guidelines

Each story must be:
- **Small**: Completable in one Amp context window (one iteration)
- **Independent**: Can be implemented without other incomplete stories
- **Testable**: Has clear acceptance criteria that can be verified

### Right-Sized Stories
- Add a database column and migration
- Create a single UI component
- Implement one API endpoint
- Add validation logic to a form

### Too Big (Split These)
- "Build the dashboard" → Split into individual widgets/sections
- "Add authentication" → Split into login, signup, password reset, etc.
- "Refactor the API" → Split into specific endpoints/modules

## Output Format

After gathering requirements, create the PRD file:

```
tasks/prd-[feature-name].md
```

Use kebab-case for the feature name (e.g., `prd-user-authentication.md`).

## Converting to Ralph Format

After creating the PRD, remind the user to convert it to Ralph format:

```
Load the ralph skill and convert tasks/prd-[feature-name].md to prd.json
```

This creates the `prd.json` file that Ralph uses for autonomous execution.
