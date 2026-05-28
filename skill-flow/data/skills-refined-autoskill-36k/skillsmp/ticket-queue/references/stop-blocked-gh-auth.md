title: Blocked — GitHub CLI Not Authenticated

decision_tree:
  entrypoint: STOP
  nodes[1]:
    - id: STOP
      purpose: "Stop when GitHub CLI auth is missing; ticket-queue cannot proceed without PR/merge access."
      steps[3]:
        - id: OUTPUT_BLOCKER
          action: "Output a BlockerReport: `gh auth status` failed or indicates no auth. Ticket queue cannot proceed without GitHub access (PR status + merges)."
        - id: INSTRUCTION
          action: "Ask the operator to run `gh auth login` (or configure a token) and then re-run the ticket-queue skill."
        - id: STOP
          action: "Stop the workflow."
