title: Follow Up on Existing PR

decision_tree:
  entrypoint: FOLLOW_UP_EXISTING_PR
  nodes[1]:
    - id: FOLLOW_UP_EXISTING_PR
      purpose: "Continue work on an existing PR, addressing the latest feedback and improvements."
      steps[11]:
        - id: NOTE_VARIABLE_SUBSTITUTION
          action: "References do not interpolate variables; replace <TICKET_ID>, <RFC_ID>, and <PR_URL> with values extracted from start-ticket output."
        - id: READ_TICKET_CONTEXT
          action: "Read ticket definition and requirements."
          context_files[2]:
            - path: "documents/work/tickets/<TICKET_ID>.yaml"
            - path: "documents/rfcs/<RFC_ID>/06_ticket_decomposition.yaml"
        - id: READ_LOCAL_INVARIANTS
          action: "Read AGENTS.md and relevant code/tests for touched modules."
        - id: FETCH_LATEST_FEEDBACK
          action: command
          run: "gh pr view <PR_URL> --json reviews,reviewThreads --jq '{latest_review: (.reviews[-1].body // \"N/A\"), unresolved_threads: [.reviewThreads[]? | select(.isResolved == false) | {path: .path, body: .comments[-1].body}]}'"
          capture_as: latest_feedback
        - id: READ_PR_DIFF
          action: command
          run: "gh pr diff <PR_URL>"
          capture_as: diff_content
        - id: IMPLEMENT_AND_TEST
          action: "Address the latest feedback and improve correctness. Apply relevant Rust Textbook frameworks (Ownership, Async, Errors, etc.)."
        - id: UPDATE_DOCS_AND_AGENTS
          action: "Update documentation and AGENTS.md files to reflect changes and new invariants."
        - id: FIX_FORMATTING
          action: command
          run: "cargo fmt"
        - id: VERIFY_AND_COMMIT
          action: command
          run: "cargo xtask commit \"Addressing review feedback and improving implementation\""
        - id: PUSH_CHANGES
          action: command
          run: "cargo xtask push"
        - id: FINISH
          action: "Task complete. The ticket-queue will monitor for further updates."
      decisions[1]:
        - id: MERGED
          if: "status indicates merged"
          then:
            next_reference: references/post-merge-cleanup.md
