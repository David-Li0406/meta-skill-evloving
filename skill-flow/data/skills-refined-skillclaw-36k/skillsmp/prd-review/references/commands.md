# PRD Review Commands

commands[3]:
  - name: create
    command: "/prd-review create PRD-XXXX"
    purpose: "Draft a new PRD from template."
  - name: review
    command: "/prd-review review PRD-XXXX"
    purpose: "Consolidated review and refinement. Checks for existing evidence, runs gates, remediates findings, and emits a new evidence bundle."
  - name: implicit-review
    command: "/prd-review PRD-XXXX"
    purpose: "Runs the consolidated review mode for the given PRD."
