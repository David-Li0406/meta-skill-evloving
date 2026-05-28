title: Blocked — Dirty Worktree

decision_tree:
  entrypoint: STOP
  nodes[1]:
    - id: STOP
      purpose: "Stop when the orchestrator worktree is dirty (uncommitted changes)."
      steps[3]:
        - id: OUTPUT_BLOCKER
          action: "Output a BlockerReport: repository worktree has uncommitted changes. Ticket queue requires a clean orchestrator worktree to avoid accidental edits."
        - id: INSTRUCTION
          action: "Ask the operator to commit/stash/discard changes, then re-run the ticket-queue skill."
        - id: STOP
          action: "Stop the workflow."
