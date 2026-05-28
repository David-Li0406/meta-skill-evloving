---
name: prd-writing
description: Use this skill when you need to create structured Product Requirement Documents (PRDs) for software features.
---

# PRD Writing Skill

This skill is activated automatically when the user wants to define a new feature or create documentation for requirements.

## When to Use

- Define a new feature
- Document business requirements
- Specify expected behavior
- Create acceptance criteria

## Template

Use the template in `templates/prd-template.md` as a base.

## Process

1. **Understand the Problem**
   - What problem is being solved?
   - Who are the affected users?
   - What is the impact of not solving it?

2. **Define Functional Requirements**
   - What should the system do?
   - What are the inputs and outputs?
   - What validations are necessary?

3. **Define Non-Functional Requirements**
   - Expected performance
   - Required security
   - Required scalability

4. **Establish Acceptance Criteria**
   - How to validate that it is ready?
   - What tests are necessary?
   - Who approves the delivery?

## Outputs

- `.claude/plans/features/<name>/prd.md`

## Related Files

- `templates/prd-template.md` - Standard template