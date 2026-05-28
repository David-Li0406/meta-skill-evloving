title: Implementer Subagent Supervision (Cadence + Tool-Call Congruency)

decision_tree:
  entrypoint: SUPERVISE
  nodes[1]:
    - id: SUPERVISE
      purpose: "Keep the implementer subagent moving, detect stalls early, and ensure tool calls are congruent with resolving blockers (CI failures, review feedback, security/quality issues)."
      steps[10]:
        - id: NOTE_VARIABLE_SUBSTITUTION
          action: "Replace <IMPLEMENTER_PID> and <IMPLEMENTER_LOG_FILE>. Replace <WORKTREE_PATH> and <TICKET_ID> if you include status context in a restart prompt."
        - id: CHECK_EVERY_3_MINUTES
          action: "At least every 3 minutes: check log mtime and tail the most recent tool-ish lines."
        - id: CHECK_LOG_ACTIVITY
          action: command
          run: "bash -lc 'set -euo pipefail; stat -c \"%y %n\" <IMPLEMENTER_LOG_FILE>; tail -n 120 <IMPLEMENTER_LOG_FILE> | rg -n \"tool|Tool|Bash\\(|Read\\(|Edit\\(|Write\\(|exec|command\" || true'"
          capture_as: implementer_recent_activity
        - id: CHECK_PROCESS_ALIVE
          action: command
          run: "ps -p <IMPLEMENTER_PID> -o pid=,etime=,cmd= || true"
          capture_as: implementer_ps
        - id: CONGRUENCY_EXPECTATIONS
          action: |
            Use the current blocker state to judge tool-call congruency:
            - If CI failed: expect `cargo fmt/clippy/test`, reading error logs, and targeted code edits.
            - If reviews failed: expect reading PR comments/diff, applying requested changes, re-running checks.
            - If reviews pending: expect `cargo xtask check` polling and reviewer log inspection (not random refactors).
            - If no PR: expect `cargo xtask push` (not more local-only edits).
        - id: STUCK_DEFINITION
          action: "Define STUCK as: (a) no log mtime change for >=5 minutes OR (b) repeated tool errors / API 4xx/5xx loops OR (c) repeated identical actions without new evidence."
        - id: STUCK_RESPONSE
          action: |
            If STUCK:
            1) Verify PID is really the subagent (ps cmdline contains `claude` or `codex`).
            2) Terminate it (TERM then KILL) and restart with a fresh, shorter prompt that includes:
               - the current `cargo xtask check` output snippet
               - the exact remediation command(s)
               - the ticket ID and worktree path
        - id: CONTEXT_EXHAUSTION_RESPONSE
          action: "If the subagent appears confused or out of context, restart it and include only the minimal necessary context plus concrete next commands."
        - id: DO_NOT_SELF_FIX
          action: "Even if you see the fix, do NOT edit code yourself. Always redirect the implementer with exact next commands and acceptance criteria."
        - id: RETURN
          action: "Return to references/dispatch-and-monitor-ticket.md."
      decisions[1]:
        - id: BACK
          if: "always"
          then:
            next_reference: references/dispatch-and-monitor-ticket.md

