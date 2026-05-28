title: New Ticket Flow (No Existing PR)

decision_tree:
  entrypoint: NEW_TICKET_FLOW
  nodes[1]:
    - id: NEW_TICKET_FLOW
      purpose: "Implement a ticket from scratch and open a new PR."
      steps[11]:
        - id: NOTE_VARIABLE_SUBSTITUTION
          action: "References do not interpolate variables; replace <TICKET_ID> and <RFC_ID> with values extracted from start-ticket output."
        - id: READ_TICKET_CONTEXT
          action: "Read ticket definition and requirements."
          context_files[2]:
            - path: "documents/work/tickets/<TICKET_ID>.yaml"
            - path: "documents/rfcs/<RFC_ID>/06_ticket_decomposition.yaml"
        - id: READ_LOCAL_INVARIANTS
          action: "Read AGENTS.md and relevant code/tests for touched modules."
        - id: SELECT_RELEVANT_RUST_FRAMEWORKS
          action: "Based on the planned changes, select relevant Rust Textbook frameworks (Ownership, Async, Errors, etc.)."
        - id: PLAN_TESTS
          action: "Define a test strategy covering happy paths, edge cases, and failure modes."
        - id: IMPLEMENT
          action: "Implement the change following Textbook quality standards."
        - id: UPDATE_DOCS_AND_AGENTS
          action: "Update documentation and AGENTS.md if public behavior or module invariants change."
        - id: FIX_FORMATTING
          action: command
          run: "cargo fmt"
        - id: VERIFY_AND_COMMIT
          action: command
          run: "cargo xtask commit \"Initial implementation of <TICKET_ID>\""
        - id: PUSH_CREATE_PR
          action: command
          run: "cargo xtask push"
        - id: FINISH
          action: "Task complete. The ticket-queue will monitor for review feedback."
      decisions[1]:
        - id: MERGED
          if: "status indicates merged"
          then:
            next_reference: references/post-merge-cleanup.md
