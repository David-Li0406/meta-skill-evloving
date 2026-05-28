# {{FEATURE_NAME}}

> {{ONE_LINE_DESCRIPTION}}

**Module:** {{PROGRAM}} / {{MODULE}}
**Status:** Planned
**Started:** —
**Completed:** —
**GitHub Issue:** #{{ISSUE_NUMBER}}

---

## User Story

**As a** {{USER_TYPE}},
**I want** {{ACTION_OR_CAPABILITY}},
**So that** {{BENEFIT_OR_OUTCOME}}.

---

## Overview

{{DETAILED_DESCRIPTION}}

### Basic Scenario

1. {{STEP_1}}
2. {{STEP_2}}
3. {{STEP_3}}

---

## Acceptance Criteria

### Core Functionality

- [ ] {{CRITERION_1}}
- [ ] {{CRITERION_2}}
- [ ] {{CRITERION_3}}

### User Experience

- [ ] {{UX_CRITERION_1}}
- [ ] {{UX_CRITERION_2}}

### Edge Cases

- [ ] {{EDGE_CASE_1}}
- [ ] {{EDGE_CASE_2}}

---

## Data Model

_If this feature involves new data structures, define them here._

### {{MODEL_NAME}}

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Unique identifier |
| {{FIELD_1}} | {{TYPE_1}} | {{DESCRIPTION_1}} |
| {{FIELD_2}} | {{TYPE_2}} | {{DESCRIPTION_2}} |
| created_at | DateTime | When created |
| updated_at | DateTime | When last modified |

---

## Technical Notes

### Approach

{{IMPLEMENTATION_APPROACH}}

### Dependencies

- {{DEPENDENCY_1}}
- {{DEPENDENCY_2}}

### Performance Considerations

{{PERFORMANCE_NOTES}}

### Standards Checklist

Before marking this feature complete, verify:

#### Code Quality
- [ ] Tests written first (TDD red-green-refactor)
- [ ] All tests pass
- [ ] 3-tier architecture followed (presentation → logic → data)
- [ ] No reverse imports (data → logic forbidden)
- [ ] Functions/classes follow naming conventions
- [ ] Docstrings on all public APIs

#### Architecture
- [ ] Module boundaries respected
- [ ] No circular dependencies introduced
- [ ] Single index.ts entry point (if new module)
- [ ] Dependencies are explicit

#### Design
- [ ] Design tokens used (no hardcoded values)
- [ ] Semantic HTML used
- [ ] All interactive states implemented (hover, focus, active, disabled)
- [ ] Accessible (keyboard nav, screen reader support)

#### Security
- [ ] Input validation implemented
- [ ] No hardcoded secrets
- [ ] Authorization checks in place
- [ ] Errors don't leak sensitive info

#### Documentation
- [ ] This feature spec is complete
- [ ] Acceptance criteria all checked
- [ ] Open questions resolved
- [ ] Module explainer updated

---

## Open Questions

- [ ] **Open:** {{QUESTION_1}}
- [ ] **Open:** {{QUESTION_2}}

---

## Related Features

- [{{RELATED_FEATURE_1}}](./{{related-feature-1}}.md)
- [{{RELATED_FEATURE_2}}](./{{related-feature-2}}.md)

---

## Revision History

| Date | Author | Change |
|------|--------|--------|
| {{DATE}} | {{AUTHOR}} | Initial spec |
