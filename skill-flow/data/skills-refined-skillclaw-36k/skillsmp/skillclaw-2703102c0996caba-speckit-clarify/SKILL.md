---
name: speckit-clarify
description: Use this skill when the feature spec exists but needs targeted clarification to reduce ambiguity before planning.
---

# Skill body

## Inputs
- The current feature spec in `specs/<feature>/spec.md`.
- The user's clarification intent or constraints from the request.

## Workflow
Goal: Detect and reduce ambiguity or missing decision points in the active feature specification and record the clarifications directly in the spec file.

Note: This clarification workflow is expected to run (and be completed) BEFORE invoking the `/speckit.plan` skill. If the user explicitly states they are skipping clarification (e.g., exploratory spike), you may proceed, but must warn that downstream rework risk increases.

### Execution Steps:

1. **Check Prerequisites**: Run the following command from the repo root **once**:
   ```bash
   ./specify/scripts/bash/check-prerequisites.sh --json --paths-only
   ```
   - Parse minimal JSON payload fields:
     - `FEATURE_DIR`
     - `FEATURE_SPEC`
     - (Optionally capture `IMPL_PLAN`, `TASKS` for future chained flows.)
   - If JSON parsing fails, abort and instruct the user to re-run `/speckit.specify` or verify the feature branch environment.
   - For single quotes in arguments like "I'm Groot", use escape syntax: e.g., 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load Current Spec**: Load the current spec file and perform a structured ambiguity & coverage scan using the following taxonomy. For each category, mark status: Clear / Partial / Missing. Produce an internal coverage map used for prioritization (do not output raw map unless no questions will be asked).

   **Taxonomy Categories**:
   - Functional Scope & Behavior
   - Domain & Data Model
   - Interaction & UX Flow
   - Non-Functional Quality Attributes
   - Integration & External Dependencies
   - Edge Cases & Failure Handling
   - Constraints & Tradeoffs
   - Terminology & Consistency
   - Completion Signals
   - Misc / Placeholders

3. **Ask Clarification Questions**: Based on the ambiguity and coverage scan, ask up to 5 highly targeted clarification questions to the user.

4. **Record Answers**: Encode the answers back into the spec file.

5. **Save Q&A Decisions**: After completion, save the Q&A decisions:
   ```bash
   ./specify/scripts/memory-save --decisions "Clarified for {feature}: {key decisions}" --issues ""
   ```

## Constitution Alignment
This skill enforces project principles:
- **Testable Requirements**: Every requirement must be unambiguous and testable.
- **User-Focused**: Clarifications prioritize user value over technical details.