title: Dev Ticket Workflow Decision Tree

decision_tree:
  entrypoint: INIT_AND_CLASSIFY
  nodes[1]:
    - id: INIT_AND_CLASSIFY
      purpose: "Initialize worktree and choose the correct workflow path."
      context_files[6]:
        - path: README.md
          purpose: "Root-level module index, documentation discovery, and repository-wide constraints."
        - path: documents/skills/rust-textbook/SKILL.md
          purpose: "Rust quality guidance; choose relevant sections later."
        - path: documents/security/AGENTS.md
          purpose: "Security documentation index and quick reference."
        - path: documents/security/SECURITY_POLICY.md
          purpose: "Security invariants and modes."
        - path: documents/skills/holonic-agent-network/SKILL.md
          purpose: "Core philosophy and constraints."
      steps[5]:
        - id: READ_BASELINE_CONTEXT
          action: "Read the context files listed above and note global constraints."
        - id: NOTE_ARGUMENT_SUBSTITUTION
          action: "If this runner does not interpolate $1 in references, replace $1 manually with the ticket ID or omit it to auto-select the next unblocked ticket."
        - id: START_TICKET
          action: command
          run: "cargo xtask start-ticket $1"
          capture_as: start_ticket_output
        - id: ENTER_WORKTREE
          action: command
          run: "cd \"$(cargo xtask start-ticket $1 --print-path)\""
          capture_as: worktree_path
        - id: EXTRACT_CONTEXT
          action: parse_text
          from: start_ticket_output
          extract[4]:
            - TICKET_ID
            - RFC_ID
            - PR_URL
            - WORKTREE_PATH
      decisions[3]:
        - id: NO_TICKET_AVAILABLE
          if: "start_ticket_output indicates no unblocked tickets or no ticket selected"
          then:
            next_reference: references/no-ticket-available.md
        - id: EXISTING_PR
          if: "PR_URL is present"
          then:
            next_reference: references/follow-up-existing-pr.md
        - id: NEW_TICKET
          if: "PR_URL is empty"
          then:
            next_reference: references/new-ticket-flow.md
