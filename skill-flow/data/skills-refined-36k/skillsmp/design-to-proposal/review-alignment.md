# Alignment Review Subagent Prompt

- **Goal**: Verify the proposal accurately reflects the design intent and required scenarios.
- **Inputs**:
  - Design document
  - `openspec/changes/<change-id>/proposal.md`
  - `openspec/changes/<change-id>/tasks.md`
  - Spec deltas in `openspec/changes/<change-id>/specs/`
- **Model**: Claude Sonnet 4.5 (via GitHub Copilot)
- **Constraints**:
  - Fresh context; do not rely on parent history.
  - Be critical but pragmatic; avoid nitpicks.
  - No code changes; suggest edits only.
  - Focus on completeness, accuracy, scope discipline, scenario quality.

## Output format

Return exactly one of:

ALIGNED

OR

GAPS:
1. [Critical/Important/Minor] <issue> — Suggested fix: <fix>
2. ...
