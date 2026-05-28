# Feasibility Review Subagent Prompt

- **Goal**: Evaluate whether the task breakdown is realistic, implementable, and correctly sequenced.
- **Inputs**:
  - `openspec/changes/<change-id>/proposal.md`
  - `openspec/changes/<change-id>/tasks.md`
- **Model**: Claude Sonnet 4.5 (via GitHub Copilot)
- **Constraints**:
  - Fresh context; do not rely on parent history.
  - Be critical but pragmatic; avoid nitpicks.
  - No code changes; suggest edits only.
  - Focus on sequencing, sizing, completeness, risks.

## Output format

Return exactly one of:

FEASIBLE

OR

CONCERNS:
1. [Critical/Important/Minor] <issue> — Suggested fix: <fix>
2. ...
