title: Escalate Back to Implementer (Fix Required)

decision_tree:
  entrypoint: ESCALATE
  nodes[1]:
    - id: ESCALATE
      purpose: "Provide a concrete fix task to the implementer when the ticket is blocked (CI failed, reviews denied, missing PR, etc.)."
      steps[5]:
        - id: NOTE_VARIABLE_SUBSTITUTION
          action: "Replace <TICKET_ID>, <WORKTREE_PATH>, and <CHECK_OUTPUT_SNIPPET>."
        - id: PREPARE_ESCALATION
          action: "Summarize the blocking state and include <CHECK_OUTPUT_SNIPPET> plus the exact remediation command suggested by `cargo xtask check`."
        - id: ISSUE_IMPLEMENTER_TASK
          action: "Send the implementer subagent a fresh, short task: fix the blocker, run `cargo xtask commit`, run `cargo xtask push`, and report back when `cargo xtask check` is green."
        - id: SUPERVISE_PROGRESS
          action: "Monitor implementer log/activity every 3 minutes; restart if no progress for 5 minutes."
        - id: RECHECK
          action: command
          run: "bash -lc 'set -euo pipefail; cd \"<WORKTREE_PATH>\" && timeout 30s cargo xtask check'"
          capture_as: check_output
      decisions[1]:
        - id: BACK
          if: "always"
          then:
            next_reference: references/dispatch-and-monitor-ticket.md
