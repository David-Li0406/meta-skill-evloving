---
name: create-prd
description: Use this skill when you need to create a Product Requirements Document (PRD) that outlines the end state of a feature, including its purpose, scope, and success criteria.
---

# PRD Creation Skill

Create Product Requirements Documents suitable for RFC review by Principal Engineers, Designers, and Product Owners. The PRD describes WHAT to build and WHY, not HOW or in WHAT ORDER.

## Workflow

1. User requests: "Load the create-prd skill and create a PRD for [feature]"
2. **Ask clarifying questions** to build full understanding.
3. **Explore codebase** to understand patterns, constraints, and dependencies.
4. Generate markdown PRD to `prd-<feature-name>.md` in project root.

## Clarifying Questions

Ask questions across these domains:

### Problem & Motivation
- What problem does this solve? Who experiences it?
- What's the cost of NOT solving this? (user pain, revenue, tech debt)
- Why now? What triggered this work?

### Users & Stakeholders
- Who are the primary users? Secondary users?

### End State & Success
- What does "done" look like? How will users interact with it?

### Scope & Boundaries
- What's explicitly OUT of scope?
- What's deferred to future iterations?
- Are there adjacent features that must NOT be affected?

### Constraints & Requirements
- Performance requirements?
- Security requirements? (auth, data sensitivity, compliance)
- Compatibility requirements? (browsers, versions, APIs)
- Accessibility requirements? (WCAG level, screen readers)

### Risks & Dependencies
- What could go wrong? Technical risks?
- External service dependencies?
- What decisions are still open/contentious?

Keep questions concise. 5-7 at most.

## Output Format

Save to `prd-<feature-name>.md` (project root):

```markdown
# PRD: <Feature Name>

**Date:** <YYYY-MM-DD>

---

## Problem Statement

### What problem are we solving?
Clear description of the problem. Include user impact and business impact.

### Why now?
What triggered this work? Cost of inaction?

### Who is affected?
- **Primary users:** Description
- **Secondary users:** Description

---

## Proposed Solution

### Overview
One paragraph describing what this feature does when complete.

### User Experience (if applicable)
<!-- Include for user-facing features -->
How will users interact with this feature? Include user flows for primary scenarios.

#### User Flow: <Scenario Name>
1. User does X
2. System responds with Y
3. User sees Z

### Design Considerations
```