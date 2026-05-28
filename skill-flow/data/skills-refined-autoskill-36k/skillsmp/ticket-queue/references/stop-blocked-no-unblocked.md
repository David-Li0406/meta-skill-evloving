title: Blocked — No Unblocked Tickets (Dependencies)

decision_tree:
  entrypoint: STOP
  nodes[1]:
    - id: STOP
      purpose: "Stop when `cargo xtask start-ticket` reports no unblocked tickets (dependency deadlock or unmet prerequisites)."
      steps[5]:
        - id: OUTPUT_BLOCKER
          action: "Output a BlockerReport: `cargo xtask start-ticket` reported no unblocked tickets due to dependencies."
        - id: INCLUDE_EVIDENCE
          action: "Include the exact `cargo xtask start-ticket` output snippet that explains the dependency block."
        - id: LIST_BLOCKED_TICKETS
          action: "List the blocked tickets and their unmet dependencies exactly as reported."
        - id: NOTE_SEQUENTIAL_BLOCK
          action: "Note: sequential merge policy means the queue cannot proceed until dependencies are resolved (or tickets are reclassified/unblocked)."
        - id: STOP
          action: "Stop the workflow."
