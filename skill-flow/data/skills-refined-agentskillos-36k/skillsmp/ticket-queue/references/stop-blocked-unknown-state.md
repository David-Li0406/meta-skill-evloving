title: Blocked — Unknown Queue State

decision_tree:
  entrypoint: STOP
  nodes[1]:
    - id: STOP
      purpose: "Stop when the queue state cannot be classified with the available evidence."
      steps[3]:
        - id: OUTPUT_BLOCKER
          action: "Output a BlockerReport describing what could not be classified (missing gh, unexpected command output, etc.). Include the last commands run and their outputs."
        - id: SUGGEST_DEBUG
          action: "Suggestion: rerun `timeout 30s gh pr list --state merged --limit 500 --json headRefName` and `git branch --list \"*ticket/*TCK-*\"` and include outputs."
        - id: STOP
          action: "Stop the workflow."
