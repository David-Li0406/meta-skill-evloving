title: Start and Process Next Unblocked Ticket

decision_tree:
  entrypoint: START
  nodes[1]:
    - id: START
      purpose: "Start the next unblocked ticket (creates worktree + branch), then delegate to implementer subagent and monitor until merged."
      steps[7]:
        - id: NOTE_VARIABLE_SUBSTITUTION
          action: "Replace <START_TARGET_OPTIONAL> with $1 (or empty). This controls the initial selection only; you MUST continue until all tickets are merged."
        - id: START_TICKET
          action: command
          run: "cargo xtask start-ticket <START_TARGET_OPTIONAL>"
          capture_as: start_ticket_output
        - id: EXTRACT_TICKET_ID
          action: parse_text
          from: start_ticket_output
          extract[2]:
            - TICKET_ID
            - WORKTREE_PATH
        - id: ENTER_WORKTREE
          action: command
          run: "cd \"<WORKTREE_PATH>\""
          capture_as: entered_worktree
        - id: ASSERT_ON_TICKET_BRANCH
          action: command
          run: "git branch --show-current"
          capture_as: branch_name
        - id: DISPATCH_IMPLEMENTER
          action: "Dispatch an implementer subagent in <WORKTREE_PATH> to implement the ticket and open/update the PR. The queue orchestrator MUST NOT modify code."
        - id: MONITOR_TO_MERGE
          action: "Proceed to monitoring (CI + reviews + SLA) until merged, then cleanup."
      decisions[2]:
        - id: NO_TICKET_AVAILABLE
          if: "start_ticket_output indicates all tickets are complete OR no unblocked tickets exist"
          then:
            next_reference: references/stop-or-blocked-no-unblocked.md
        - id: MONITOR
          if: "a ticket was started and <WORKTREE_PATH> is known"
          then:
            next_reference: references/dispatch-and-monitor-ticket.md

