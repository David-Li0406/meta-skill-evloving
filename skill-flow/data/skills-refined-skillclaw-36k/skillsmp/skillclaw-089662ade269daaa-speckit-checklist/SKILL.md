---
name: speckit-checklist
description: Use this skill when you need a requirements-quality checklist tailored to a feature or domain.
---

# Checklist Purpose: "Unit Tests for English"

**CRITICAL CONCEPT**: Checklists are **UNIT TESTS FOR REQUIREMENTS WRITING** - they validate the quality, clarity, and completeness of requirements in a given domain.

**NOT for verification/testing**:
- NOT "Verify the button clicks correctly"
- NOT "Test error handling works"
- NOT "Confirm the API returns 200"
- NOT checking if code/implementation matches the spec

**FOR requirements quality validation**:
- "Are visual hierarchy requirements defined for all card types?" (completeness)
- "Is 'prominent display' quantified with specific sizing/positioning?" (clarity)
- "Are hover state requirements consistent across all interactive elements?" (consistency)
- "Are accessibility requirements defined for keyboard navigation?" (coverage)
- "Does the spec define what happens when logo image fails to load?" (edge cases)

**Metaphor**: If your spec is code written in English, the checklist is its unit test suite. You're testing whether the requirements are well-written, complete, unambiguous, and ready for implementation - NOT whether the implementation works.

## Execution Steps

1. **Setup**: Run `.specify/scripts/bash/check-prerequisites.sh --json` from repo root and parse JSON for FEATURE_DIR and AVAILABLE_DOCS list.
   - All file paths must be absolute.
   - For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Clarify intent (dynamic)**: Derive up to THREE initial contextual clarifying questions (no pre-baked catalog). They MUST:
   - Be generated from the user's phrasing + extracted signals from spec/plan/tasks
   - Only ask about information that materially changes checklist content
   - Be skipped individually if already unambiguous in the user's request
   - Prefer precision over breadth

3. **Understand user request**: Combine user input with clarifying answers to derive checklist theme (e.g., security, review, deploy, UX) and consolidate explicit must-have items mentioned by the user.