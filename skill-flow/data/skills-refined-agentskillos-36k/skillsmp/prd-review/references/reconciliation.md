# Post-Merge Reconciliation (GATE-PRD-RECONCILIATION)

**Trigger:** After any PR referencing `PRD-XXXX` is merged to main.

decision_tree:
  entrypoint: RECONCILIATION
  nodes[1]:
    - id: RECONCILIATION
      purpose: "Detect variance between implementation and PRD specification after merge."
      steps[3]:
        - id: EXTRACT_SYMBOLS
          action: "Extract new public symbols (functions, structs, traits, types) from merged PR diff."
        - id: VERIFY_MAPPING
          action: "Verify all new symbols map to the PRD's CCP projection."
        - id: REPORT_VARIANCE
          action: "If a symbol introduces a net-new abstraction not in the PRD, emit VARIANCE_EVENT."
          logic: |
            ```yaml
            variance_id: VAR-{PRD_ID}-{NNN}
            pr_ref: "PR#123"
            symbol: "crate::new_retry::CustomRetry"
            expected_mapping: "core/retry.rs::RetryPolicy"
            variance_type: "UNDOCUMENTED_ABSTRACTION"
            ```
            - Auto-create ticket: "PRD-XXXX Variance: Reconcile {symbol} with specification"
            - Add variance pattern to references/COUNTERMEASURE_PATTERNS.md
      decisions[1]:
        - id: DONE
          if: "always"
          then:
            stop: true
