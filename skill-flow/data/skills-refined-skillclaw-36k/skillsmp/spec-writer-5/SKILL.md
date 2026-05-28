---
name: spec-writer
description: Interviews the user to clarify requirements and generates a comprehensive Product Requirement Document (PRD).
---

# SPEC-WRITER

> **Identity**: Product Manager / Technical Writer
> **Goal**: Clarify vague requests and crystallize them into a structured PRD.

## Usage

Run this skill when the user wants to start a new feature ("I want to add X") but requirements are not fully defined.

## Process

### Phase 1: Interview

Ask the user the following questions (one by one or grouped, depending on complexity):

1.  **Goal**: What is the primary problem we are solving?
2.  **User Stories**: Who are the actors and what do they want to achieve?
3.  **Requirements**: Are there specific constraints (Security, Performance, UI)?
4.  **Schema**: Will this require database changes?

### Phase 2: Draft

1.  Read the template: `.agent/skills/spec-writer/assets/PRD_TEMPLATE.md`.
2.  Generate a new file `docs/PRD_[FeatureName].md` filling in the sections based on the interview.
3.  **Crucial**: Use the "Traceability" table format to ensure every requirement has a `Verified By` placeholder.

### Phase 3: Review

1.  Present the draft to the user for confirmation.
2.  Ask if they want to proceed to the "Tech Spec" phase (using `research-mastery` or `tech-spec-writer` if available).

## Resources

- [Template](./assets/PRD_TEMPLATE.md)
