---
name: prd-review
description: Refine and review PRDs from multiple angles with formal gates, evidence contracts, and recurrence prevention.
argument-hint: "[create | review] PRD-XXXX"
---

orientation: "You are a PRD review/refinement agent. Your job is to help authors produce PRDs that (a) pass trusted gates, (b) are testable and evidence-backed, and (c) avoid cousin abstractions by forcing reuse-by-default thinking."

title: PRD Review & Refinement
protocol:
  id: PRD-REVIEW
  version: 1.0.0
  type: executable_specification
  inputs[2]:
    - MODE_OPTIONAL
    - PRD_ID
  outputs[2]:
    - FindingsBundle
    - Verdict

variables:
  MODE_OPTIONAL: "$1"
  PRD_ID: "$2"

references[16]:
  - path: references/prd-review-workflow.md
    purpose: "Primary decision tree for mode selection and input validation."
  - path: references/create-mode.md
    purpose: "Logic for drafting a new PRD from template."
  - path: references/review-mode.md
    purpose: "Logic for formal gate execution, depth computation, and iterative refinement."
  - path: references/REVIEW_RUBRIC.md
    purpose: "Formal gate definitions and evidence contracts."
  - path: references/ANGLE_PROMPTS.md
    purpose: "Multi-angle content review prompts."
  - path: references/FINDING_CATEGORIES.md
    purpose: "Deterministic finding taxonomy and severity rules."
  - path: references/CREATE_PRD_PROMPT.md
    purpose: "Detailed drafting guidance and Falsifiability Standard."
  - path: references/ADVERSARIAL_REVIEW_PROMPT.md
    purpose: "Adversarial meta-review protocol for DEEP reviews."
  - path: references/COUNCIL_PROTOCOL.md
    purpose: "Multi-agent deliberation protocol for COUNCIL reviews."
  - path: `documents/strategy/NORTH_STAR.md`
    purpose: "5-phase vision document for council alignment."
  - path: references/FEEDBACK_LOOPS.md
    purpose: "Recursive improvement mechanisms and SNR checks."
  - path: references/reconciliation.md
    purpose: "Post-merge variance detection (GATE-PRD-RECONCILIATION)."
  - path: references/COUNTERMEASURE_PATTERNS.md
    purpose: "Patterns for preventing defect recurrence."
  - path: references/commands.md
    purpose: "CLI command reference."
  - path: ../agent-native-software/SKILL.md
    purpose: "REQUIRED READING: First principles of agent-native software engineering."
  - path: ../../security/AGENTS.md
    purpose: "REQUIRED READING: Security policy, threat models, and incident response."

decision_tree:
  entrypoint: WORKFLOW
  nodes[1]:
    - id: WORKFLOW
      action: invoke_reference
      reference: references/prd-review-workflow.md

## Verdict Rules

- **PASSED**: All gates passed.
- **FAILED**: Any gate failed with BLOCKER findings.
- **NEEDS_REMEDIATION**: Only MAJOR/MINOR findings remain.
- **NEEDS_ADJUDICATION**: A required decision is missing or confidence is LOW.

## Meta-Review Protocol

Use Gemini as a second-pass reviewer for `GATE-PRD-CONTENT` and for improving the PRD review process itself. For `DEEP` reviews, use the protocol in `references/ADVERSARIAL_REVIEW_PROMPT.md`. Follow the constraints in `references/META_IMPROVEMENT_PROMPT.md` when proposing skill updates.