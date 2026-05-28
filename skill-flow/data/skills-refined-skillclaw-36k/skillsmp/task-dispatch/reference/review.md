# Review Format

Implementation review tracking in `review.yaml`. Mirrors validation.yaml structure.

## Location

```
./specs/active/<spec-name>/review.yaml
```

## Schema

```yaml
# Review: ${SPEC_NAME}
# Machine + human readable implementation review tracking
#
# This file tracks batch reviews, accumulated issues, gate results, and
# final review status. Intended for both programmatic access (task-dispatch,
# task-continue) and human review.

metadata:
  spec_name: ${SPEC_NAME}
  spec_path: ./specs/active/${SPEC_NAME}
  branch: feat/${SPEC_NAME}
  created: ${DATE}
  last_updated: ${TIMESTAMP}
  total_batches: ${N}
  batches_reviewed: ${M}

# Review configuration (copied from validation.yaml)
# Variant format: {reasoning_effort}-medium (verbosity fixed at medium)
# Reasoning options: low | medium | high | xhigh (xhigh GPT-5.2 only)
review_config:
  reasoning_effort: ${REASONING_EFFORT}  # low | medium | high | xhigh
  reviewers:
    - type: claude
      model: ${CLAUDE_MODEL}  # opus
    - type: opencode
      model: ${OPENCODE_MODEL_1}
    - type: opencode
      model: ${OPENCODE_MODEL_2}

# Accumulated gate status across all batch reviews.
# Gate fails if ANY batch review failed it.
# Status values: pass | fail | pending
gates:
  correctness:
    status: ${STATUS}
    failed_batches: []  # [1, 3] if batches 1 and 3 failed this gate
  style:
    status: ${STATUS}
    failed_batches: []
  performance:
    status: ${STATUS}
    failed_batches: []
  security:
    status: ${STATUS}
    failed_batches: []
  architecture:
    status: ${STATUS}
    failed_batches: []

# Batch reviews record each review session.
# Written after Phase C of each batch.
batch_reviews:
  - batch: 1
    timestamp: ${TIMESTAMP}
    commit: ${SHA}
    tasks: [T001, T002]
    reviewers:
      - id: claude-opus
        status: completed
        gates:
          correctness: pass
          style: pass
          performance: pass
          security: pass
          architecture: pass
      - id: opencode-gpt5.2-codex
        status: completed
        gates:
          correctness: pass
          style: fail
          performance: pass
          security: pass
          architecture: pass
      - id: opencode-gemini-3-pro
        status: timeout  # or completed | failed
        gates: null
    synthesized:
      gates:
        correctness: pass
        style: fail
        performance: pass
        security: pass
        architecture: pass
      critical_issues: 0
      high_issues: 0
      medium_issues: 1
    outcome: approved  # or changes_requested
  # Additional batches follow same structure

# Accumulated issues across all batches.
# Grouped by severity, includes resolution status.
issues:
  critical:
    - id: C001
      batch: 2
      task: T003
      gate: security
      location: "src/auth/login.py:45"
      description: "SQL injection via unsanitized input"
      suggestion: "Use parameterized queries"
      found_by: [claude-opus, opencode-gemini-3-pro]
      status: resolved  # or open
      resolution:
        batch: 2
        commit: ${SHA}
        fix: "Added parameterized query"
  high:
    - id: H001
      batch: 1
      task: T001
      gate: correctness
      location: "src/models/user.py:23"
      description: "Missing null check before dereference"
      suggestion: "Add guard clause"
      found_by: [claude-opus]
      status: resolved
      resolution:
        batch: 1
        commit: ${SHA}
        fix: "Added None check"
  medium:
    - id: M001
      batch: 1
      task: T002
      gate: style
      location: "src/auth/auth.py:45"
      description: "Variable name 'x' is unclear"
      suggestion: "Rename to 'retry_count'"
      found_by: [opencode-gpt5.2-codex]
      status: deferred  # medium issues can be deferred
      resolution: null

# Deferred issues (medium severity, noted for later).
# Carried forward in checkpoints.
deferred_issues:
  - id: M001
    batch: 1
    description: "Variable naming in auth.py:45"
    gate: style
  # Additional deferred issues

# Final review (after all batches complete).
# Comprehensive review of entire implementation.
final_review:
  status: pending  # pending | in_progress | completed
  timestamp: null
  reviewers: []
  gates:
    correctness: pending
    style: pending
    performance: pending
    security: pending
    architecture: pending
  spec_compliance:
    all_tasks_complete: ${BOOL}
    acceptance_criteria_met: ${BOOL}
    edge_cases_handled: ${BOOL}
  issues: []
  strengths: []
  overall_assessment: null
  recommendation: null  # ready_to_merge | changes_requested

# Readiness checklist for merge/PR.
# All items must be true for implementation to be considered complete.
readiness:
  all_batches_reviewed: ${BOOL}
  critical_issues_resolved: ${BOOL}
  high_issues_resolved: ${BOOL}
  final_review_passed: ${BOOL}
  tests_passing: ${BOOL}

# Notes for additional context.
notes: |
  ${NOTES}
```

## Usage

### Writing review.yaml

**After each batch review (Phase C):**

1. Read existing review.yaml (or create if first batch)
2. Append new batch_reviews entry
3. Update accumulated gates
4. Add new issues to appropriate severity list
5. Update deferred_issues if medium issues noted
6. Write updated review.yaml
7. Include in batch commit

**After final review:**

1. Read review.yaml
2. Populate final_review section
3. Update readiness checklist
4. Write final review.yaml

### Reading review.yaml

**By task-continue:**
- Check last batch reviewed
- Load deferred issues
- Determine next batch

**By code-review (final mode):**
- Load all batch results
- Identify patterns across batches
- Complete final_review section

## Relationship to Other Files

| File | Purpose |
|------|---------|
| validation.yaml | Pre-implementation: spec quality, gates, markers |
| review.yaml | Post-implementation: code quality, batch reviews |
| checkpoint.yaml | Session state: progress, next batch |
| tasks.yaml | Task definitions and status |

## Gates

| Gate | What It Checks |
|------|----------------|
| correctness | Logic errors, edge cases, error handling, type safety |
| style | Naming conventions, formatting, readability, idioms |
| performance | Efficiency, data structures, unnecessary computation |
| security | Input validation, secrets exposure, injection risks |
| architecture | Design patterns, coupling, separation of concerns |
