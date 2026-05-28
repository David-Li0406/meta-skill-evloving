---
name: speckit-clarify
description: Use this skill to identify underspecified areas in the current feature spec by asking targeted clarification questions and encoding answers back into the spec.
---

## When to Use

Use this skill when the feature spec exists but needs targeted clarification before planning.

## Inputs

- The current feature spec in `specs/<feature>/spec.md`.
- The user's clarification intent or constraints from the request.

## Workflow

Goal: Detect and reduce ambiguity or missing decision points in the active feature specification and record the clarifications directly in the spec file.

Note: This clarification workflow is expected to run (and be completed) BEFORE the speckit-plan skill. If the user explicitly states they are skipping clarification (e.g., exploratory spike), you may proceed, but must warn that downstream rework risk increases.

### Execution Steps

1. **Check Prerequisites**: Run `.specify/scripts/bash/check-prerequisites.sh --json --paths-only` from repo root **once**. Parse minimal JSON payload fields:
   - `FEATURE_DIR`
   - `FEATURE_SPEC`
   - (Optionally capture `IMPL_PLAN`, `TASKS` for future chained flows.)
   - If JSON parsing fails, abort and instruct the user to re-run `/speckit.specify` or verify feature branch environment.

2. **Load Spec File**: Perform a structured ambiguity & coverage scan using the following taxonomy. For each category, mark status: Clear / Partial / Missing. Produce an internal coverage map used for prioritization (do not output raw map unless no questions will be asked).

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

3. **Generate Clarification Questions**: Create a prioritized queue of candidate clarification questions (maximum 5). Each question must be answerable with:
   - A short multiple-choice selection (2-5 distinct, mutually exclusive options), OR
   - A one-word / short-phrase answer (explicitly constrain: "Answer in <=5 words").

4. **Sequential Questioning Loop**:
   - Present EXACTLY ONE question at a time.
   - For multiple-choice questions, analyze all options and determine the most suitable option based on best practices. Present your recommended option prominently with clear reasoning.
   - After the user answers, validate the response and record it in working memory.

5. **Integration After Each Accepted Answer**:
   - Maintain an in-memory representation of the spec and ensure a `## Clarifications` section exists.
   - Append a bullet line immediately after acceptance: `- Q: <question> → A: <final answer>`.
   - Apply the clarification to the most appropriate section(s) in the spec.

6. **Validation**: Perform validation after each write plus a final pass to ensure:
   - Clarifications session contains exactly one bullet per accepted answer (no duplicates).
   - Total asked (accepted) questions ≤ 5.
   - Updated sections contain no lingering vague placeholders.

7. **Write Updated Spec**: Write the updated spec back to `FEATURE_SPEC`.

8. **Report Completion**: After the questioning loop ends or early termination, report:
   - Number of questions asked & answered.
   - Path to updated spec.
   - Sections touched (list names).
   - Coverage summary table listing each taxonomy category with Status.

### Behavior Rules

- If no meaningful ambiguities found, respond: "No critical ambiguities detected worth formal clarification." and suggest proceeding.
- If the spec file is missing, instruct the user to run `/speckit.specify` first.
- Never exceed 5 total asked questions.
- Respect user early termination signals ("stop", "done", "proceed").