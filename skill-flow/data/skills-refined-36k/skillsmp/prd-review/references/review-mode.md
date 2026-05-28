# REVIEW Mode

decision_tree:
  entrypoint: REVIEW_AND_REFINE
  nodes[1]:
    - id: REVIEW_AND_REFINE
      purpose: "Execute formal review gates with iterative refinement and emit findings."
      steps[7]:
        - id: ITERATIVE_GATE_EXECUTION
          action: |
            For each gate in the invariant order (1-7):
            1. Execute gate (SCHEMA -> LINT -> TRACEABILITY -> CCP-MAPPING -> QUALITY -> EVIDENCE -> CONTENT).
            2. If gate FAILS with BLOCKER/MAJOR findings:
               a. PROPOSE_EDITS: Generate remediations (BOUND_ADDED, EVIDENCE_LINKED, etc.).
               b. APPLY_EDITS: Modify PRD if substance test passes.
               c. DELTA_QUALITY_CHECK: Verify fix is not PROSE_ONLY.
               d. RE-RUN: Repeat gate check once to verify fix.
            3. Record final findings for the gate.
        - id: COMPUTE_DEPTH
          action: "Compute impact vector based on requirements, dependencies, abstractions, data classification, and blast radius."
          logic: |
            Impact Vector Computation:
            - requirement_count: ≤3 (Low), 4-10 (Medium), >10 (High)
            - external_dependencies: 0 (Low), 1-2 (Medium), >2 (High)
            - net_new_abstractions: 0 (Low), 1 (Medium), >1 (High)
            - data_classification: public (Low), internal (Medium), pii/confidential (High)
            - blast_radius: single_component (Low), cross_component (Medium), system_wide (High)

            Depth Algorithm:
            - LIGHT: all dimensions = low
            - STANDARD: any dimension = medium, none = high
            - DEEP: any dimension = high
            - COUNCIL: blast_radius = system_wide AND (net_new_abstractions > 2 OR north_star_alignment_requested)
        - id: CONTENT_REVIEW
          action: invoke_reference
          reference: references/ANGLE_PROMPTS.md
          purpose: "Execute required and optional review angles based on computed depth."
        - id: ADVERSARIAL_PASS
          action: invoke_reference
          reference: references/ADVERSARIAL_REVIEW_PROMPT.md
          condition: "depth is DEEP or 20% random sample of STANDARD"
        - id: COUNCIL_PROTOCOL
          action: invoke_reference
          reference: references/COUNCIL_PROTOCOL.md
          condition: "depth is COUNCIL"
        - id: EMIT_BUNDLE
          action: |
            Produce NEW prd_review_{timestamp}.json evidence bundle.
            Note: Always emit a new bundle even if all gates pass initially.
      decisions[2]:
        - id: CRITICAL_FAILURE
          if: "any gate status is FAILED after refinement"
          then:
            stop: true
        - id: COMPLETED
          if: "all gates executed and refined"
          then:
            stop: true
