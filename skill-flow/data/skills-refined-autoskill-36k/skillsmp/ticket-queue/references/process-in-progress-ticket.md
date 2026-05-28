title: Process In-Progress Ticket (Resume and Merge)

decision_tree:
  entrypoint: RESUME
  nodes[1]:
    - id: RESUME
      purpose: "Select the next in-progress ticket, ensure a worktree exists, and delegate to an implementer subagent; then monitor until merged."
      steps[8]:
        - id: NOTE_VARIABLE_SUBSTITUTION
          action: "Replace <TICKET_ID> with the lowest ID from in_progress_ticket_ids. Replace <BRANCH_NAME> by finding the matching `ticket/.../<TICKET_ID>` branch. Replace <WORKTREE_PATH> with the worktree path (prefer existing)."
        - id: PICK_LOWEST_IN_PROGRESS
          action: "Pick the lowest ticket ID from the in-progress list (lexicographic works for TCK-00001..TCK-99999). Set it as <TICKET_ID>."
        - id: FIND_BRANCH_NAME
          action: command
          run: "git branch --all --format='%(refname:short)' | rg \"^(remotes/origin/)?ticket/.*/<TICKET_ID>$\" | head -n 1"
          capture_as: branch_name_maybe
        - id: NORMALIZE_BRANCH_NAME
          action: "If branch_name_maybe starts with `remotes/origin/`, strip that prefix. The result is <BRANCH_NAME>."
        - id: ENSURE_LOCAL_BRANCH
          action: command
          run: "bash -lc 'set -euo pipefail; if git show-ref --verify --quiet \"refs/heads/<BRANCH_NAME>\"; then echo \"local branch ok\"; else timeout 30s git fetch origin \"<BRANCH_NAME>:<BRANCH_NAME>\"; fi'"
          capture_as: ensure_local_branch_result
        - id: ENSURE_WORKTREE
          action: command
          run: "bash -lc 'set -euo pipefail; root=$(git rev-parse --show-toplevel); parent=$(dirname \"$root\"); wt=\"$parent/apm2-<TICKET_ID>\"; if [ -d \"$wt\" ]; then echo \"$wt\"; else git worktree add \"$wt\" \"<BRANCH_NAME>\"; echo \"$wt\"; fi'"
          capture_as: worktree_path
        - id: UPDATE_PR_IF_BEHIND
          action: command
          run: "bash -lc 'set -euo pipefail; status=$(gh pr view \"<BRANCH_NAME>\" --json mergeStateStatus --jq .mergeStateStatus || echo \"UNKNOWN\"); if [ \"$status\" == \"BEHIND\" ]; then echo \"PR is behind main; updating...\"; gh pr update-branch \"<BRANCH_NAME>\"; else echo \"PR status is $status; no update needed.\"; fi'"
        - id: DISPATCH_IMPLEMENTER
          action: "Dispatch an implementer subagent in <WORKTREE_PATH> to get the PR into a mergeable state (CI + reviews). The queue orchestrator MUST NOT modify code."
        - id: MONITOR_TO_MERGE
          action: "Proceed to monitoring (CI + reviews + SLA) until merged, then cleanup."
      decisions[1]:
        - id: MONITOR
          if: "always"
          then:
            next_reference: references/dispatch-and-monitor-ticket.md

