title: Blocked — Review SLA Breach

decision_tree:
  entrypoint: STOP
  nodes[1]:
    - id: STOP
      purpose: "Stop when AI reviews fail to complete within the 15-minute SLA after repeated remediation."
      steps[5]:
        - id: OUTPUT_BLOCKER
          action: "Output a BlockerReport: AI reviews did not complete within 15 minutes and remediation attempts failed."
        - id: INCLUDE_EVIDENCE
          action: "Include: PR URL, HEAD SHA, reviewer_state.json summary, reviewer PIDs, last 80 lines of each reviewer log, and the timestamps showing the SLA breach."
        - id: SUGGEST_FALLBACK
          action: "Suggest manual recovery: rerun reviews synchronously (`cargo xtask review security <PR_URL>`, `cargo xtask review quality <PR_URL>`) or run an alternative review runner, then update status checks."
        - id: NOTE_SEQUENTIAL_BLOCK
          action: "Note: sequential merge policy means the queue cannot proceed until this PR merges."
        - id: STOP
          action: "Stop the workflow."
