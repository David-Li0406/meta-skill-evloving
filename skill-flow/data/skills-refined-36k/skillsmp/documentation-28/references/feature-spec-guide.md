# Feature Specification Writing Guide

## Overview

Feature specifications document what needs to be built, why, and how success is measured. They serve as contracts between stakeholders and implementers.

---

## Purpose of Feature Specs

### For Product/Planning
- Define scope and boundaries
- Prioritize based on value
- Track progress

### For Development
- Understand requirements
- Know when done (acceptance criteria)
- Make informed technical decisions

### For Testing
- Clear acceptance criteria to verify
- Edge cases documented
- Expected behavior defined

### For Documentation
- Source of truth for feature behavior
- User-facing docs derive from specs
- Historical record of decisions

---

## Feature Spec Structure

### 1. Header Section

```markdown
# Feature Name

> One-line description of what this feature does.

**Module:** [Program] / [Module]
**Status:** Planned | In Progress | Complete
**Started:** YYYY-MM-DD
**Completed:** YYYY-MM-DD
**GitHub Issue:** #123
```

The header provides quick context:
- **Feature Name**: Clear, action-oriented (e.g., "Create Weekly Meal Plan")
- **One-liner**: Explains the feature in one sentence
- **Module**: Where this feature belongs
- **Status**: Current state (Planned → In Progress → Complete)
- **Dates**: When work started/finished
- **Issue**: Link to tracking issue

---

### 2. User Story

```markdown
## User Story

**As a** [user type],
**I want** [action/capability],
**So that** [benefit/outcome].
```

The user story:
- Identifies who benefits
- Describes what they want to do
- Explains why it matters

**Examples:**

```markdown
**As a** home cook,
**I want** to generate a weekly meal plan,
**So that** I can save time and eat more variety.

**As a** team lead,
**I want** to see my team's availability,
**So that** I can schedule meetings efficiently.
```

---

### 3. Overview

```markdown
## Overview

[2-3 paragraphs describing the feature in detail]

### Basic Scenario

1. User does X
2. System responds with Y
3. User sees Z
```

The overview:
- Expands on the user story
- Describes typical use case
- Shows the happy path flow

**Example:**

```markdown
## Overview

The meal plan generator creates a week's worth of meals based on user preferences,
dietary restrictions, and available ingredients. Users can customize the plan,
swap meals, and regenerate individual days.

### Basic Scenario

1. User clicks "Generate Meal Plan"
2. System analyzes preferences and generates 7 days of meals
3. User reviews the plan and optionally swaps meals
4. User confirms and saves the plan
```

---

### 4. Acceptance Criteria

```markdown
## Acceptance Criteria

- [ ] Criterion 1 (testable)
- [ ] Criterion 2 (testable)
- [ ] Criterion 3 (testable)
```

Acceptance criteria are **testable conditions** that define "done."

**Good Criteria:**
- Specific and measurable
- Written as checkboxes
- One condition per item
- Cover happy path AND edge cases

**Example:**

```markdown
## Acceptance Criteria

### Core Functionality
- [ ] User can generate a 7-day meal plan
- [ ] Plan respects dietary restrictions (vegetarian, vegan, gluten-free)
- [ ] Plan avoids ingredients marked as "disliked"
- [ ] Each day includes breakfast, lunch, dinner

### User Control
- [ ] User can swap any meal with an alternative
- [ ] User can regenerate a single day
- [ ] User can lock meals they want to keep

### Data
- [ ] Plan is saved to user's account
- [ ] User can view past meal plans
- [ ] Shopping list is generated from the plan

### Edge Cases
- [ ] System handles when no recipes match restrictions
- [ ] System handles when ingredient database is incomplete
```

---

### 5. Data Model

```markdown
## Data Model

### MealPlan

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Unique identifier |
| user_id | UUID | Owner of the plan |
| week_start | Date | First day of the plan |
| meals | MealDay[] | Array of daily meals |
| created_at | DateTime | When created |
```

Include data model when:
- Feature involves new data structures
- Existing data is modified
- API contracts need definition

---

### 6. Technical Notes

```markdown
## Technical Notes

### Approach
[How this will be implemented]

### Dependencies
- [Service/API X]
- [Library Y]

### Performance Considerations
[Any performance requirements or concerns]

### Standards Checklist
- [ ] Code Quality: Tests written first (TDD)
- [ ] Code Quality: 3-tier architecture followed
- [ ] Architecture: Module boundaries respected
- [ ] Design: Design tokens used
- [ ] Security: Input validation implemented
- [ ] Documentation: This spec complete
```

Technical notes help developers:
- Understand the approach
- Know dependencies
- Consider constraints
- Verify standards compliance

---

### 7. Open Questions

```markdown
## Open Questions

- [ ] **Open:** Should we limit plans to 7 days or allow custom lengths?
- [x] **Resolved:** How to handle conflicting dietary restrictions? → User sets priority order
```

Open questions:
- Track unknowns during planning
- Document decisions when resolved
- Use checkboxes to show status

---

### 8. Related Features

```markdown
## Related Features

- [Recipe Management](./recipe-management.md)
- [Shopping List](./shopping-list.md)
- [Dietary Preferences](./dietary-preferences.md)
```

Link to related features for context.

---

## Writing Tips

### Be Specific

```markdown
# ❌ Vague
- [ ] System is fast

# ✅ Specific
- [ ] Page loads in under 2 seconds on 3G connection
- [ ] Search returns results in under 500ms
```

### Be Testable

```markdown
# ❌ Untestable
- [ ] User experience is good

# ✅ Testable
- [ ] User can complete task in under 3 clicks
- [ ] Error messages explain how to fix the issue
```

### Cover Edge Cases

```markdown
# ❌ Only happy path
- [ ] User can upload image

# ✅ Includes edge cases
- [ ] User can upload image (jpg, png, gif)
- [ ] System rejects files over 10MB with clear error
- [ ] System rejects unsupported file types with clear error
- [ ] Upload works on slow connections (shows progress)
```

### Use Active Voice

```markdown
# ❌ Passive
- [ ] Meal plan is displayed to the user

# ✅ Active
- [ ] System displays the meal plan to the user
- [ ] User can view the generated meal plan
```

---

## Feature Lifecycle

```
1. Planned    → Spec written, reviewed, prioritized
2. In Progress → Development started
3. Complete   → All acceptance criteria met, deployed
```

### Status Updates

When status changes:
1. Update status in feature file
2. Update dates (started/completed)
3. Update module explainer table
4. Update project roadmap if milestone affected

---

## Review Checklist

Before finalizing a spec:

- [ ] **Header complete** — All fields filled
- [ ] **User story clear** — Follows As/Want/So format
- [ ] **Overview helpful** — Explains the feature well
- [ ] **Criteria testable** — Each can be verified
- [ ] **Criteria complete** — Covers happy path and edge cases
- [ ] **Technical notes present** — Approach documented
- [ ] **Standards checklist** — All items addressed
- [ ] **Questions tracked** — Open items documented
- [ ] **Related features linked** — Context provided
