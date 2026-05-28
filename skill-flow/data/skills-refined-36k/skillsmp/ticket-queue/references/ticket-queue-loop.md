title: Ticket Queue — Main Loop

decision_tree:
  entrypoint: SNAPSHOT_AND_CLASSIFY
  nodes[1]:
    - id: SNAPSHOT_AND_CLASSIFY
      purpose: "Compute ticket state (completed/in-progress/incomplete), pick exactly one ticket to process next, and dispatch work."
      steps[7]:
        - id: NOTE_VARIABLE_SUBSTITUTION
          action: "References do not interpolate variables; replace <START_TARGET_OPTIONAL> with $1 (or empty). Replace <TICKET_ID>/<WORKTREE_PATH>/<BRANCH_NAME> when routed."
        - id: LIST_ALL_TICKETS
          action: command
          run: "ls documents/work/tickets/TCK-*.yaml | rg -o \"TCK-[0-9]{5}\" | sort -u"
          capture_as: all_ticket_ids
        - id: LIST_COMPLETED
          action: command
          run: "timeout 30s gh pr list --state merged --limit 500 --json headRefName | rg -o \"TCK-[0-9]{5}\" | sort -u"
          capture_as: completed_ticket_ids
        - id: LIST_IN_PROGRESS
          action: command
          run: "bash -lc 'set -euo pipefail; completed=$(timeout 30s gh pr list --state merged --limit 500 --json headRefName | rg -o \"TCK-[0-9]{5}\" | sort -u || true); branches=$( (git branch --list \"*ticket/*TCK-*\"; git branch -r --list \"*ticket/*TCK-*\") | rg -o \"TCK-[0-9]{5}\" | sort -u || true); comm -23 <(printf \"%s\\n\" \"$branches\") <(printf \"%s\\n\" \"$completed\")'"
          capture_as: in_progress_ticket_ids
        - id: COMPUTE_INCOMPLETE
          action: command
          run: "bash -lc 'set -euo pipefail; all=$(ls documents/work/tickets/TCK-*.yaml | rg -o \"TCK-[0-9]{5}\" | sort -u); completed=$(timeout 30s gh pr list --state merged --limit 500 --json headRefName | rg -o \"TCK-[0-9]{5}\" | sort -u || true); comm -23 <(printf \"%s\\n\" \"$all\") <(printf \"%s\\n\" \"$completed\")'"
          capture_as: incomplete_ticket_ids
        - id: ASSERT_SEQUENTIAL
          action: "If in_progress_ticket_ids has >1 ticket, you MUST still process tickets one-by-one: pick the lowest ID first and ignore the rest until it is merged."
        - id: ROUTE_NEXT
          action: "Route to the correct next step based on the snapshot."
      decisions[4]:
        - id: ALL_DONE
          if: "incomplete_ticket_ids is empty"
          then:
            next_reference: references/stop-all-tickets-merged.md
        - id: HAS_IN_PROGRESS
          if: "in_progress_ticket_ids is non-empty"
          then:
            next_reference: references/process-in-progress-ticket.md
        - id: NO_IN_PROGRESS_BUT_INCOMPLETE
          if: "in_progress_ticket_ids is empty AND incomplete_ticket_ids is non-empty"
          then:
            next_reference: references/start-and-process-next-ticket.md
        - id: FALLBACK_STOP
          if: "unable to classify state"
          then:
            next_reference: references/stop-blocked-unknown-state.md

