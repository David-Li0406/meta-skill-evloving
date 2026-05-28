# PRD Review Workflow

decision_tree:
  entrypoint: VALIDATE_AND_CLASSIFY
  nodes[1]:
    - id: VALIDATE_AND_CLASSIFY
      purpose: "Validate inputs and branch to the correct mode."
      steps[5]:
        - id: VALIDATE_ID
          action: "Ensure PRD_ID matches /^PRD-[0-9]{4}$/. If invalid, reject with error."
        - id: LOCATE_INPUTS
          action: "Set default PRD root to documents/prds/{PRD_ID}/. Allow interactive override."
        - id: CHECK_EXISTING_EVIDENCE
          action: |
            For PRD-XXXX targets:
            - Search `evidence/prd/{PRD_ID}/prd_review_*.json`
            - If found, load the latest bundle to identify previously failed gates and unresolved findings.
        - id: SELECT_MODE
          action: "If mode is not provided, default to REVIEW (or CREATE if PRD does not exist)."
        - id: GATE_INVARIANT
          action: "Note fixed gate order: 1. SCHEMA, 2. LINT, 3. TRACEABILITY, 4. CCP-MAPPING, 5. QUALITY, 6. EVIDENCE, 7. CONTENT."
      decisions[2]:
        - id: MODE_CREATE
          if: "mode is CREATE"
          then:
            next_reference: references/create-mode.md
        - id: MODE_REVIEW
          if: "mode is REVIEW"
          then:
            next_reference: references/review-mode.md
