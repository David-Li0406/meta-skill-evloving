# Issue Document Templates

This file contains the detailed templates for each type of issue document.

## Bug Report / Technical Issue

```markdown
---
date: YYYY-MM-DD
type: Bug
severity: Critical | High | Medium | Low | N/A
status: Resolved | In Progress | Investigating
---

# [Concise Title]

## Problem
[What broke? What is the impact? Be specific.]

## Root Cause
[Why did it happen? Trace to origin.]

## Solution
[How was it fixed? Show code before/after.]

## Lessons Learned
- [Actionable takeaway]

## Prevention
- [ ] [Checklist item]
```

## Feature Plan

```markdown
---
date: YYYY-MM-DD
type: Feature Plan
severity: Critical | High | Medium | Low | N/A
status: Draft | Proposed | In Progress | Accepted
---

# [Feature Name]

## Goal
[What are we building and why? Value proposition.]

## Requirements
- [ ] User Story 1
- [ ] User Story 2

## Proposed Implementation
[High-level technical approach. Components involved.]

## Risks & Considerations
- [Potential blockers or edge cases]
```

## RFC (Request for Comments)

```markdown
---
date: YYYY-MM-DD
type: RFC
severity: Critical | High | Medium | Low | N/A
status: Open for Comment | Proposed | Accepted | In Progress
---

# RFC: [Topic]

## Summary
[One paragraph explanation.]

## Motivation
[Why do we need this? What problem does it solve?]

## Detailed Design
[How will it work? API changes, data models, etc.]

## Alternatives Considered
- [Option A]: [Why rejected?]

## Unresolved Questions
- [ ] Question 1?
```

## ADR (Architecture Decision Record)

```markdown
---
date: YYYY-MM-DD
type: ADR
severity: N/A
status: Proposed
author: Name <email>
tags:
  - architecture
  - decision
related:
  - 251201_arch-decision.md
---

# ADR: [Decision Title]

## Context
[The situation and constraints leading to this decision.]

## Decision
[The change that we are proposing or have agreed to.]

## Consequences
**Positive:**
- [Benefit 1]

**Negative:**
- [Trade-off 1]
```

## Task

```markdown
---
date: YYYY-MM-DD
type: Task
severity: Critical | High | Medium | Low | N/A
status: Draft | Proposed | In Progress | Accepted
---

# Task: [Task Name]

## Objective
[What needs to be done?]

## Tasks
- [ ] Step 1
- [ ] Step 2

## Acceptance Criteria
- [ ] Criteria 1
- [ ] Criteria 2

## References
- [Link to code or docs]
```

## Retrospective

```markdown
---
date: YYYY-MM-DD
type: Retrospective
severity: N/A
status: Documented | Reviewed | Implemented
---

# Lesson: [Concise Title]

## Context
[What happened? Brief background on the incident, problem, or project.]

## What Went Well
- [Positive aspects or successes]

## What Didn't Go Well
- [Challenges, mistakes, or areas for improvement]

## Key Lessons Learned
- [Actionable insights and takeaways]
- [What we learned about processes, tools, or team dynamics]

## Actions Taken
- [Immediate fixes or changes implemented]

## Future Prevention / Improvements
- [ ] [Checklist item for preventing recurrence]
- [ ] [Recommendations for similar situations]
```