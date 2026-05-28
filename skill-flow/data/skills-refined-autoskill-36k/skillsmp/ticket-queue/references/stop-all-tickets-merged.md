title: Stop Condition — All Tickets Merged

decision_tree:
  entrypoint: STOP
  nodes[1]:
    - id: STOP
      purpose: "Terminate the queue when all tickets under documents/work/tickets are merged to main."
      steps[4]:
        - id: VERIFY_NO_INCOMPLETE
          action: command
          run: "bash -lc 'set -euo pipefail; all=$(ls documents/work/tickets/TCK-*.yaml | rg -o \"TCK-[0-9]{5}\" | sort -u); completed=$(timeout 30s gh pr list --state merged --limit 500 --json headRefName | rg -o \"TCK-[0-9]{5}\" | sort -u); missing=$(comm -23 <(printf \"%s\\n\" \"$all\") <(printf \"%s\\n\" \"$completed\") || true); if [ -n \"$missing\" ]; then echo \"MISSING_TICKETS:\"; echo \"$missing\"; exit 1; fi; echo \"ALL_TICKETS_MERGED\"'"
          capture_as: verify_output
        - id: EMIT_TICKET_MERGE_LEDGER
          action: "Output a final TicketMergeLedger summarizing tickets processed (ticket ID -> PR URL -> merged). Keep it concise."
        - id: OUTPUT_DONE
          action: "Output 'Done' and nothing else."
        - id: STOP
          action: "Stop the workflow."
