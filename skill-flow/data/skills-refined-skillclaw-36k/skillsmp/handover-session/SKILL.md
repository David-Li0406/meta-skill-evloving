---
name: handover_session
description: AIモデル間や作業セッション間での円滑な引継ぎのためのドキュメント・プロンプトを作成する
---

# Handover Session Skill

Create handover prompts and documentation to prevent loss of context and ensure smooth continuation of work when handing over tasks between AI coding tools or different LLM models.

## Components of a Handover Package

A high-quality handover prompt should encompass the following information:

### 1. Current Status and Accomplishments
- Progress relative to the plan (e.g., Phase X completed).
- List of files recently created or modified.
- Status of physics verification and tests.

### 2. References to Materials and Resources
- **Plans**: Latest plan path under `docs/developers/plans/`.
- **Work Reports**: Most recent report path under `docs/developers/reports/`.
- **Issues and Pending Tasks**: Unchecked items in the plan or newly discovered bugs.

### 3. Specific Instructions for the Next Worker (Model)
- Files to be created or modified next.
- Test commands to be executed.
- Implementation constraints or pitfalls encountered by the predecessor.

### 4. Shared Debug Information
- Logs of recently failed tests (if any).
- Details of remaining Lint errors.

## Handover Workflow

1.  **Consolidate Information**: Execute `archive_work` to summarize the latest state in a report.
2.  **Construct Prompt**:
    *   Create a section titled `### Handover Instructions for the Next Model`.
    *   Fill in the information according to the "Components" outlined above.
3.  **Adjustment Based on Model Characteristics**:
    *   For models strong in logical reasoning (Claude Opus/Thinking), emphasize "Verification of physical/mathematical consistency."
    *   For models strong in rapid/high-volume code generation (GPT/Codex/Flash), instruct on "Mass production of test cases" or "Standard refactoring."

## Example Handover Prompt

```markdown
### Handover Instructions for [Model Name]

**1. Reference Materials**
- Plan: `/path/to/plan_2026MMDD.md`
- Work Report: `/path/to/report_2026MMDD.md`

**2. Current State**
- Phase 1 & 2 implementation complete. Physics verification script `verify_*.py` passed all checks.
- Currently, two `AttributeError`s occur when running `tests/test_foo.py`, and the fix is in progress.

**3. Tasks**
- Fix the errors in `tests/test_foo.py` according to the new properties in ScalarField.
- Once fixed, run the entire `pytest` suite to verify coverage.
- Finally, commit the changes to finalize the task.
```

## Critical Rule: Exclusive Coding Task Control

To prevent environment inconsistency and conflicts during handover, strictly adhere to the following rules:

-   **Halt Work**: **Do not resume coding tasks unilaterally** (creating, modifying, or deleting files) until it is explicitly stated that the successor's coding work is finished.
-   **Permitted Concurrent Tasks**: Tasks other than coding can still be performed while waiting.
    -   Discussion/Requirement elicitation with the user.
    -   Codebase analysis/research.
    -   Creating/updating/organizing agent skills.
    -   Reviewing/refining documentation.

This separation allows for improving agent capabilities and deepening understanding in parallel without disrupting the context of the main coding worker.
