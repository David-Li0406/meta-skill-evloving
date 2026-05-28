---
name: generating-spec
description: > 
  Writes the specification with problem definition, solution outline, and acceptance criteria.
  To be used to specify a feature, bug correction, or enhancement.
---

# Generating Specs Skill

## Role

Act as a software analyst. 

## Task

Write the specification to implement a feature, bug correction, or enhancement.
Do not write any code or tests, just the specification.

## Context

The feature, bug correction, or enhancement must be provided in the input.

If not, ask for it before proceeding.

Types of specifications to generate include:
- New or current feature : `feat`
- Bug correction : `bug`
- Enhancement or refactor : `chore`

## Steps to follow:

1. **Capture inputs**:
  - Confirm feat/bug/chore to specify; if missing, ask.
  - Draft the issue title from the request; if unclear, ask.
2. **Review PRD (if applicable)**:
  - Check if the feature, bug correction, or enhancement is already in PRD.
  - If it is, use that information to help you write the specification.
  - If not, update the PRD documentation with it.
2. **Define the Problem**: 
  - Clearly outline the problem that we aim to solve.
3. **List User Stories**: 
  - Up to 3 US that describe the problem from the user's perspective.
4. **Outline the Solution**: 
  - Describe the simplest approach without technical details for:
    - User/App interface
    - Model and logic
    - Persistence
5. **Set Acceptance Criteria**: 
  - Up to 9 criteria in EARS format that define when the spec is complete.
  - Follow the [EARS format guide](./EARS.md).
6. **Generate an spec-slug-id**:
  - Create a short-name identifier for the spec based on the type and title.
  - Example: `feat-booking-management`.
7. **Write the Specification**: 
  - Use short sentences and bullet points where possible.
  - Keep the specification concise but complete.
  - Follow the [spec template](spec.md)
  - Write it in markdown format at `specs/<spec-slug-id>.spec.md`.