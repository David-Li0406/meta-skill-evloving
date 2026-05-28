title: Post-Merge Cleanup and Continue

decision_tree:
  entrypoint: CLEANUP
  nodes[1]:
    - id: CLEANUP
      purpose: "After a PR merges, run cleanup (`cargo xtask finish`) and return to the main queue loop."
      steps[2]:
        - id: NOTE_VARIABLE_SUBSTITUTION
          action: "Replace <WORKTREE_PATH> and <TICKET_ID>."
        - id: FINISH
          action: command
          run: "bash -lc 'set -euo pipefail; cd \"<WORKTREE_PATH>\" && cargo xtask finish'"
          capture_as: finish_output
      decisions[1]:
        - id: NEXT
          if: "always"
          then:
            next_reference: references/ticket-queue-loop.md
