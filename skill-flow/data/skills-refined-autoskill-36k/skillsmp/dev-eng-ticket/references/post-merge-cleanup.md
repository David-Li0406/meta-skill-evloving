title: Post-Merge Cleanup

steps[2]:
  - id: FINISH_WORKTREE
    action: command
    run: "cargo xtask finish"
  - id: CONTINUE
    action: "If more tickets remain, return to the main workflow and run start-ticket again."
