---
name: clarify
description: Clarify underspecified areas in specifications - recommended before planning phase
---

# Clarify - Specification Clarification

## Overview

Systematically identify and clarify underspecified areas in functional specifications before moving to technical planning.

**Announce at start:** "I'm using the clarify skill to identify and resolve specification gaps."

## When to Use

- After creating functional specification (`SpecKit/specify`)
- Before creating technical plan (`SpecKit/plan`)
- When specification has ambiguous or missing details
- When requirements need further refinement

## The Process

### Step 1: Review Specification

1. Read the specification file (`specs/<feature-id>/spec.md`)
2. Identify areas that are:
   - Ambiguous or unclear
   - Missing details
   - Inconsistent
   - Potentially problematic

### Step 2: Structured Clarification

Use sequential, coverage-based questioning:

**Categories to Cover:**

1. **Data Model**
   - What data structures are needed?
   - What are the relationships?
   - What are the constraints?

2. **User Interactions**
   - What are all possible user actions?
   - What happens in each case?
   - What are the edge cases?

3. **Business Rules**
   - What are the validation rules?
   - What are the business constraints?
   - What are the error scenarios?

4. **Performance & Scale**
   - What are the expected volumes?
   - What are the performance requirements?
   - What are the scalability needs?

5. **Integration Points**
   - What external systems are involved?
   - What are the integration requirements?
   - What are the API contracts?

### Step 3: Record Clarifications

Add a **Clarifications** section to the specification:

```markdown
## Clarifications

### Data Model
**Q:** What data structures are needed for albums?
**A:** Albums contain: id, name, date, photos array, created_at timestamp.

### User Interactions
**Q:** What happens when user drags album to invalid location?
**A:** Album returns to original position, show error message "Albums cannot be nested".
...
```

### Step 4: Update Specification

- Update `spec.md` with clarifications
- Revise affected sections if needed
- Ensure consistency across document

### Step 5: Validate Completeness

Ask user:
- Are all questions answered?
- Are there any remaining ambiguities?
- Is specification ready for planning phase?

## Example Usage

```
/speckit.clarify
```

The skill will:
1. Review the specification
2. Ask questions one at a time
3. Record answers in Clarifications section
4. Update specification as needed

## Optional: Free-Form Refinement

After structured clarification, you can add free-form refinements:

```
For each sample project, there should be a variable number of tasks between 5 and 15 
tasks randomly distributed into different states of completion. Make sure that there's 
at least one task in each stage of completion.
```

## Key Principles

- **One question at a time**: Don't overwhelm with multiple questions
- **Coverage-based**: Systematically cover all areas
- **Record answers**: Document clarifications in specification
- **Update spec**: Revise specification based on clarifications
- **Validate**: Ensure specification is complete before planning

## When to Skip Clarification

You can skip clarification if:
- Specification is intentionally vague (spike/exploratory prototype)
- Requirements are already very detailed
- User explicitly requests to skip

In this case, explicitly state: "Skipping clarification phase as specification is intentionally exploratory."

## Integration with Other Skills

- **Before**: Use `SpecKit/specify` to create specification
- **After**: Use `SpecKit/plan` to create technical implementation plan
- **Alternative**: Use `Superpowers/brainstorming` for design exploration
