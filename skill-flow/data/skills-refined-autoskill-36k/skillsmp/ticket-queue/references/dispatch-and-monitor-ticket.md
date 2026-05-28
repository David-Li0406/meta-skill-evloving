title: Dispatch Implementer and Monitor Until Merge

decision_tree:
  entrypoint: DISPATCH
  nodes[1]:
    - id: DISPATCH
      purpose: "Ensure an implementer subagent is active for this ticket, supervise its progress, enforce review SLA, and keep looping until the PR is merged and cleaned up."
      steps[9]:
        - id: NOTE_VARIABLE_SUBSTITUTION
          action: "Replace <TICKET_ID> and <WORKTREE_PATH>. If known, replace <IMPLEMENTER_LOG_FILE> and <IMPLEMENTER_PID> for out-of-band supervision."
        - id: ESTABLISH_IMPLEMENTER_CONTRACT
          action: "Create/confirm an implementer subagent (separate process/session) that is allowed to edit code. Give it the `dev-eng-ticket` workflow and the specific <TICKET_ID>/<WORKTREE_PATH>. Require it to: implement, `cargo xtask commit`, `cargo xtask push`, respond to failures, and get to green."
        - id: REQUIRE_DEDICATED_LOG
          action: "The implementer MUST run with a durable log you can tail out-of-band. Prefer the exact commands in `references/commands.md` (`start-claude-implementer-with-log` or `start-codex-implementer-with-json-log`). Record PID + log path."
        - id: CHECK_CADENCE
          action: "While implementer is running: follow `references/subagent-supervision.md` (3-minute cadence; STUCK threshold 5 minutes; restart on no-progress)."
        - id: STATUS_POLL
          action: command
          run: "bash -lc 'set -euo pipefail; cd \"<WORKTREE_PATH>\" && timeout 30s cargo xtask check'"
          capture_as: check_output
        - id: REVIEW_SLA_ENFORCEMENT
          action: "If AI reviews are pending, enforce the 15-minute SLA using reviewer PIDs + logs. Do not allow pending reviews to persist beyond 15 minutes."
        - id: MERGE_WAIT
          action: "If CI/reviews are passing and auto-merge is enabled, keep polling until merged."
        - id: CLEANUP_AFTER_MERGE
          action: "When merged, run `cargo xtask finish` in the worktree to clean up, then return to the main loop."
        - id: LOOP
          action: "Repeat STATUS_POLL + supervision until a stop/branch condition triggers."
      decisions[5]:
        - id: MERGED
          if: "check_output indicates PR merged"
          then:
            next_reference: references/post-merge-cleanup.md
        - id: NO_PR
          if: "check_output indicates no PR exists or branch not pushed"
          then:
            next_reference: references/escalate-to-implementer.md
        - id: CI_FAILED
          if: "check_output indicates CI failed"
          then:
            next_reference: references/escalate-to-implementer.md
        - id: CHANGES_REQUESTED
          if: "check_output indicates changes requested or review denied"
          then:
            next_reference: references/escalate-to-implementer.md
        - id: REVIEWS_PENDING_OR_STUCK
          if: "check_output indicates reviews pending OR reviewer health is stale/dead OR SLA risk"
          then:
            next_reference: references/review-sla.md
