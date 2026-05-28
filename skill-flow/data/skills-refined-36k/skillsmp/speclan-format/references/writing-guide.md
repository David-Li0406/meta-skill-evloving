# SPECLAN Writing Guide

Best practices for writing effective, maintainable specifications.

## Core Principles

### 1. User-Focused

Write specifications from the user's perspective, not the developer's.

**Good:**
```markdown
Users can filter pets by health status to quickly find animals
ready for sale.
```

**Avoid:**
```markdown
The filterPets() function accepts a status parameter and queries
the database with a WHERE clause.
```

### 2. Implementation-Agnostic

Describe WHAT the system should do, not HOW it should be implemented.

**Good:**
```markdown
The system prevents sale of pets in quarantine or medical hold status.
```

**Avoid:**
```markdown
Add a check in the CartService.addItem() method that throws
ValidationException if pet.status is QUARANTINE or MEDICAL_HOLD.
```

### 3. Testable

Every requirement should have clear, measurable acceptance criteria.

**Good:**
```markdown
Given a pet with status QUARANTINE
When a user attempts to add it to cart
Then the system displays error "Pet not available for sale"
And the cart remains unchanged
```

**Avoid:**
```markdown
The system should handle quarantined pets appropriately.
```

### 4. Traceable

Maintain clear links between entities in the hierarchy.

```
Goal G-087 (Animal Welfare)
  └── Feature F-049 (Pet Management)
        └── Requirement R-0001 (No quarantine sales)
              └── Scenario S-0001 (Cart add attempt)
                    └── AC-0001 (Error displayed)
                          └── Test T-0001 (Automated check)
```

---

## Writing Goals

Goals define strategic business objectives.

### Structure

```markdown
---
[YAML frontmatter]
---

## Overview
[1-2 paragraphs explaining the goal's purpose and business value]

## Strategic Context
[Why this goal matters, market/business drivers]

## Success Criteria
[Measurable outcomes that indicate goal achievement]

## Contributing Features
[List of features that help achieve this goal]
```

### Tips

- Focus on business outcomes, not technical solutions
- Include quantifiable metrics where possible
- Link to all contributing features
- Keep goals broad enough to encompass multiple features

### Example

```markdown
## Overview
Enable pet stores to maintain healthy, well-cared-for animals while
ensuring compliance with local animal welfare regulations.

## Success Criteria
- **Compliance Rate**: 100% compliance with health check schedules
- **Incident Reduction**: 50% reduction in animal health incidents
- **Customer Satisfaction**: 90%+ positive feedback on pet health
```

---

## Writing Features

Features describe capabilities that deliver user value.

### Structure

```markdown
---
[YAML frontmatter]
---

# [Feature Title]

## Overview
[Brief description of what this feature does and why]

## User Story
As a **[user role]**, I want **[capability]** so that **[benefit]**.

## Scope

### In Scope
- [Key capability 1]
- [Key capability 2]

### Out of Scope
- [Explicitly excluded items]

## Key Business Rules
| Rule ID | Description |
|---------|-------------|
| [ID] | [Rule description] |

## Related Entities
- **[Entity]**: [How it relates to this feature]
```

### Tips

- One clear user story per feature
- Explicitly state what's out of scope
- Reference business rules by ID
- For parent features, describe how children relate

### Leaf vs Parent Features

**Parent features** (have child features):
- Describe the organizing container
- List child features in scope
- May have fewer requirements directly attached

**Leaf features** (no children):
- More detailed specifications
- Direct requirements attached
- Specific acceptance criteria

---

## Writing Requirements

Requirements specify conditions that must be satisfied.

### Structure

```markdown
---
[YAML frontmatter]
---

[One-line requirement statement]

## Rationale
[Why this requirement exists, what problem it solves]

## Business Rule Reference
- **[Rule ID]**: [Rule description]

## Acceptance Criteria

### Scenario 1: [Scenario name]
**Given** [initial state]
**When** [action]
**Then** [expected outcome]

### Scenario 2: [Scenario name]
**Given** [initial state]
**When** [action]
**Then** [expected outcome]

## Edge Cases
- [Edge case 1 and expected behavior]
- [Edge case 2 and expected behavior]

## Related
### Goals
- [Link to related goals]

### Features
- [Link to related features]
```

### Tips

- Start with a clear, one-line requirement statement
- Use Given/When/Then format for scenarios
- Document edge cases explicitly
- Include rationale to explain the "why"

### Good Requirement Statements

```markdown
Pets in quarantine or medical hold status cannot be sold.

Users receive email notification within 5 minutes of order placement.

The system retains transaction history for a minimum of 7 years.
```

### Avoid

```markdown
The system should handle pet status appropriately.  # Too vague

Implement validation in the checkout flow.  # Implementation detail

Make sure pets can't be sold when they shouldn't be.  # Ambiguous
```

---

## Writing Scenarios

Scenarios describe specific situations for validation.

### Structure

```markdown
---
[YAML frontmatter]
---

## Context
[Background context for this scenario]

## Steps

**Given** [precondition 1]
**And** [precondition 2]

**When** [action taken]
**And** [additional action if needed]

**Then** [expected outcome 1]
**And** [expected outcome 2]

## Test Data
| Field | Value |
|-------|-------|
| [field] | [value] |

## Notes
[Additional context or edge case considerations]
```

### Tips

- One scenario per specific situation
- Use concrete test data
- Keep steps atomic and testable
- Reference any required preconditions

---

## Writing Acceptance Criteria

Acceptance criteria define specific conditions for scenario success.

### Structure

```markdown
---
[YAML frontmatter]
---

## Criterion
[Clear, testable statement of what must be true]

## Verification Method
[How this criterion will be verified]

## Expected Behavior
| Condition | Expected Result |
|-----------|-----------------|
| [condition] | [result] |
```

### Tips

- One clear condition per criterion
- Must be objectively verifiable
- Include expected behavior table for complex criteria

---

## Writing Tests

Tests document verification procedures.

### Structure

```markdown
---
[YAML frontmatter]
---

## Test Description
[What this test verifies]

## Prerequisites
- [Prerequisite 1]
- [Prerequisite 2]

## Test Steps
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Expected Results
- [Expected result 1]
- [Expected result 2]

## Code Reference
[Link to automated test if applicable]
```

### Automated vs Manual

**Automated tests:**
- Include `kind: automated` in frontmatter
- Reference test file and selector
- Document test framework

**Manual tests:**
- Include `kind: manual` in frontmatter
- Detailed step-by-step instructions
- Clear pass/fail criteria

---

## Common Mistakes

### 1. Mixing Requirements and Implementation

**Wrong:**
```markdown
Add a validatePetStatus() method that checks the database
and throws an error if status is invalid.
```

**Right:**
```markdown
The system validates pet status before allowing sale transactions.
```

### 2. Vague Acceptance Criteria

**Wrong:**
```markdown
The system should respond quickly.
```

**Right:**
```markdown
The system responds to search queries within 500ms for 95th percentile.
```

### 3. Missing Traceability

**Wrong:**
```markdown
# Requirement without linking to feature or scenarios
```

**Right:**
```yaml
feature: F-049
scenarios:
  - S-0001
  - S-0002
```

### 4. Incomplete Edge Cases

**Wrong:**
```markdown
Users can add pets to cart.
```

**Right:**
```markdown
Users can add available pets to cart.

## Edge Cases
- Quarantined pets: Display error, block addition
- Reserved pets: Display warning, allow waitlist
- Out of stock: Display availability date
```

---

## Terminology Consistency

Maintain consistent terminology across specifications:

| Term | Use For | Avoid |
|------|---------|-------|
| User | End user of the system | Customer, Client (unless specific) |
| System | The software being specified | Application, App, Platform |
| Display | Show on screen | Render, Output, Print |
| Store | Persist data | Save, Write, Commit |
| Retrieve | Fetch data | Get, Load, Read, Query |

Create a project glossary for domain-specific terms.

---

## Review Checklist

Before finalizing a specification:

- [ ] Uses user-focused, non-technical language
- [ ] Implementation-agnostic (describes WHAT, not HOW)
- [ ] All required YAML fields present
- [ ] Linked to parent/child entities
- [ ] Acceptance criteria are testable
- [ ] Edge cases documented
- [ ] Consistent terminology
- [ ] No ambiguous words (should, might, could, appropriate)
- [ ] Dates and timestamps in ISO-8601 format
- [ ] File naming follows convention
