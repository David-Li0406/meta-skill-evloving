title: No Unblocked Ticket After Start Attempt

decision_tree:
  entrypoint: CLASSIFY
  nodes[1]:
    - id: CLASSIFY
      purpose: "Handle the case where `cargo xtask start-ticket` did not start a new ticket."
      steps[1]:
        - id: NOTE
          action: "Inspect the `cargo xtask start-ticket` output and classify whether: (a) all tickets are complete/in-progress, or (b) you are blocked by dependencies (no unblocked tickets)."
      decisions[3]:
        - id: BACK_TO_LOOP_IN_PROGRESS
          if: "start-ticket output indicates 'All tickets are complete or in progress' (or equivalent)"
          then:
            next_reference: references/ticket-queue-loop.md
        - id: BLOCKED_BY_DEPENDENCIES
          if: "start-ticket output indicates 'No unblocked tickets found' (or equivalent dependency block)"
          then:
            next_reference: references/stop-blocked-no-unblocked.md
        - id: UNKNOWN
          if: "otherwise"
          then:
            next_reference: references/stop-blocked-unknown-state.md
