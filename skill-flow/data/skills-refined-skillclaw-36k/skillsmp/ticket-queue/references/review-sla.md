title: Review SLA Enforcement (15 minutes)

decision_tree:
  entrypoint: ENFORCE
  nodes[1]:
    - id: ENFORCE
      purpose: "Ensure both AI reviews (security + code quality) post a PR comment and update their status checks within 15 minutes. If reviewers stall, remediate quickly."
      steps[12]:
        - id: NOTE_VARIABLE_SUBSTITUTION
          action: "Replace <WORKTREE_PATH> and <TICKET_ID>. Replace <PR_URL> if known. Replace <SEC_PID>/<QUAL_PID>/<SEC_LOG>/<QUAL_LOG> once discovered."
        - id: GET_PR_URL
          action: command
          run: "bash -lc 'set -euo pipefail; cd \"<WORKTREE_PATH>\"; b=$(git branch --show-current); timeout 30s gh pr view \"$b\" --json url --jq .url'"
          capture_as: pr_url
        - id: RUN_CHECK_FOR_REMEDIATION
          action: command
          run: "bash -lc 'set -euo pipefail; cd \"<WORKTREE_PATH>\" && timeout 30s cargo xtask check'"
          capture_as: check_output
        - id: LOAD_REVIEWER_STATE
          action: command
          run: "python3 - <<'PY'\nimport json\nfrom pathlib import Path\np = Path.home()/'.apm2'/'reviewer_state.json'\ndata = json.loads(p.read_text())\nfor k,v in (data.get('reviewers') or {}).items():\n    print(f\"{k}\\tpid={v.get('pid')}\\tstarted_at={v.get('started_at')}\\tlog_file={v.get('log_file')}\\tpr_url={v.get('pr_url')}\")\nPY"
          capture_as: reviewer_state_summary
        - id: IDENTIFY_PIDS_AND_LOGS
          action: "From reviewer_state_summary, set <SEC_PID>/<SEC_LOG> for `security` and <QUAL_PID>/<QUAL_LOG> for `quality`. If entries are missing, reviews may not have been spawned (escalate implementer)."
        - id: INSPECT_REVIEWER_PROCESSES
          action: command
          run: "bash -lc 'set -euo pipefail; ps -p <SEC_PID> -o pid=,etime=,cmd= || true; ps -p <QUAL_PID> -o pid=,etime=,cmd= || true'"
          capture_as: reviewer_ps
        - id: CHECK_LOG_ACTIVITY
          action: command
          run: "bash -lc 'set -euo pipefail; stat -c \"%y %n\" <SEC_LOG> || true; stat -c \"%y %n\" <QUAL_LOG> || true'"
          capture_as: reviewer_log_mtime
        - id: TAIL_LOGS_FOR_ERRORS_AND_TOOL_CALLS
          action: command
          run: "bash -lc 'set -euo pipefail; echo \"--- security tail ---\"; tail -n 80 <SEC_LOG> || true; echo \"--- quality tail ---\"; tail -n 80 <QUAL_LOG> || true'"
          capture_as: reviewer_log_tail
        - id: ENFORCE_15_MINUTE_DEADLINE
          action: "Compute SLA from each reviewer entry's `started_at`. If now - started_at >= 900s and the corresponding GitHub status is still `pending`, you MUST treat this as an SLA breach and take corrective action immediately (restart reviews or switch to a manual/fallback review runner)."
        - id: RESTART_IF_UNHEALTHY
          action: "If either reviewer is STALE/DEAD or showing API/tool errors in logs, immediately run `cargo xtask check` again (it auto-remediates reviewers) and re-check within 60 seconds."
        - id: ESCALATE_IF_REVIEWS_NOT_RUNNING
          action: "If reviewer_state has no entries and `check_output` shows reviews pending, the review spawn likely failed. Escalate to implementer to re-run `cargo xtask push` (or `cargo xtask push --force-review` if available) and confirm reviewers start."
        - id: LOOP_UNTIL_RESOLVED
          action: "Loop: run `cargo xtask check` every 60s, tail reviewer logs, and restart/remediate until both reviews are no longer pending and merge can proceed."
      decisions[2]:
        - id: BACK_TO_MONITOR
          if: "reviews are no longer pending OR remediation was attempted"
          then:
            next_reference: references/dispatch-and-monitor-ticket.md
        - id: HARD_STOP_ON_NO_PROGRESS
          if: "SLA breached AND repeated remediation failed (>=3 attempts) OR gh/gemini APIs are unavailable"
          then:
            next_reference: references/stop-blocked-review-sla.md

