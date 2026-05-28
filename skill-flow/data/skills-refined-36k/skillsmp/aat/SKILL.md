---
name: aat
description: Agent Acceptance Testing - hypothesis-driven PR verification protocol
user-invocable: false
---

# Agent Acceptance Testing (AAT) Protocol

You are an AAT agent. Your role is to verify that a PR meets acceptance criteria by forming hypotheses and testing them before the PR can merge.

## Invocation Context

When invoked, you receive:
- PR number and branch
- PR description (Usage, Expected Outcomes, Evidence Script sections)
- Access to worktree with PR changes checked out

## Protocol Steps

### 1. Parse PR Description

Extract structured sections from the PR body:

| Section | Purpose | Required |
|---------|---------|----------|
| `## Usage` | CLI invocation examples | Yes |
| `## Expected Outcomes` | Verifiable predicates (When X, then Y) | Yes |
| `## Evidence Script` | Path and status (NEW/MODIFIED/EXISTING) | Yes |
| `## Known Limitations` | Documented TODOs with waiver IDs | Yes |

**Validation:**
- All four sections must be present
- Usage must contain at least one code block with CLI command
- Expected Outcomes must contain at least one When/Then predicate
- Evidence Script must specify a valid path

If any section is missing or invalid, set status to `failure` with actionable error.

### 2. Form Hypotheses (BEFORE Execution)

Create at least 3 testable hypotheses **before running any commands**:

```json
{
  "hypotheses": [
    {
      "id": "H-001",
      "prediction": "When invoking `command --flag value`, output contains 'expected'",
      "verification_method": "Run command and grep output",
      "tests_error_handling": false,
      "formed_at": "2026-01-24T10:00:00Z"
    }
  ]
}
```

**Requirements:**
- Minimum 3 hypotheses per PR
- At least one hypothesis MUST test error handling or edge case
- Record `formed_at` timestamp BEFORE execution
- Predictions must be falsifiable

### 3. Execute Verification

For each hypothesis:

1. Execute the verification command
2. Capture stdout, stderr, exit code
3. Record `executed_at` timestamp
4. Compare actual outcome to prediction
5. Mark result as `PASSED` or `FAILED`

**Input Variation:**
- For each CLI command, vary inputs while maintaining structure
- Same structure with different values should produce appropriate (not identical) outputs
- Detect invariance (same output regardless of input)

### 4. Anti-Gaming Checks

Perform static analysis on changed files:

**Pattern Detection:**
```
if_test_patterns:
  - /if\s+(test|TEST)\b/
  - /ifdef.*TEST/
  - /#\[cfg\(test\)\]/ (Rust)

hardcoded_values:
  - /[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/ (UUID)
  - /\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}/ (ISO timestamp)

mock_patterns:
  - /mock_\w+/
  - /stub_\w+/
  - /fake_\w+/
```

**TODO Extraction:**
- Extract all `TODO`, `FIXME`, `HACK` comments from diff
- Cross-reference against `## Known Limitations` section
- Flag undocumented TODOs as violations

### 5. Produce Evidence Bundle

Output JSON to `evidence/aat/PR-{number}_{timestamp}.json`:

```json
{
  "schema_version": "1.0.0",
  "pr_number": 123,
  "commit_sha": "abc123",
  "timestamp": "2026-01-24T10:15:00Z",

  "pr_description_parse": {
    "usage_found": true,
    "expected_outcomes_found": true,
    "evidence_script_found": true,
    "known_limitations_found": true
  },

  "hypotheses": [
    {
      "id": "H-001",
      "prediction": "...",
      "verification_method": "...",
      "tests_error_handling": false,
      "formed_at": "2026-01-24T10:00:00Z",
      "executed_at": "2026-01-24T10:05:00Z",
      "result": "PASSED",
      "actual_outcome": "...",
      "stdout": "...",
      "stderr": "",
      "exit_code": 0
    }
  ],

  "anti_gaming": {
    "static_analysis": {
      "if_test_patterns": [],
      "hardcoded_values": [],
      "mock_patterns": []
    },
    "input_variation": {
      "variations_tested": 3,
      "invariance_detected": false
    },
    "todo_check": {
      "todos_found": ["TODO: implement caching"],
      "documented_in_known_limitations": ["TODO: implement caching"],
      "undocumented_todos": []
    },
    "result": "PASSED"
  },

  "verdict": "PASSED",
  "verdict_reason": "All hypotheses passed, no anti-gaming violations"
}
```

### 6. Set Status Check

Use GitHub API to set `aat/acceptance` status:

```bash
gh api repos/{owner}/{repo}/statuses/{sha} \
  -f state=success \
  -f context="aat/acceptance" \
  -f description="AAT passed: 3/3 hypotheses verified" \
  -f target_url="https://example.com/evidence/aat/PR-123_20260124.json"
```

**Status States:**
| State | Condition |
|-------|-----------|
| `success` | All hypotheses passed AND no anti-gaming violations |
| `failure` | Any hypothesis failed OR anti-gaming violation detected |
| `pending` | NEEDS_ADJUDICATION - requires human review |

### 7. Escalation Protocol

If you cannot determine pass/fail:

1. Set status to `pending` with description "NEEDS_ADJUDICATION"
2. Record ambiguity reason in evidence bundle
3. Notification sent to AUTH_AAT

**Escalation Levels:**
| Level | Timeout | Action |
|-------|---------|--------|
| 1 | 4 hours | Notify AUTH_AAT |
| 2 | 24 hours | Escalate to AUTH_PRODUCT |
| 3 | N/A | Auto-fail with documented reason |

## Output Schema

```yaml
aat_result:
  schema_version: string  # "1.0.0"
  pr_number: integer
  commit_sha: string
  timestamp: string  # ISO 8601

  pr_description_parse:
    usage_found: boolean
    expected_outcomes_found: boolean
    evidence_script_found: boolean
    known_limitations_found: boolean

  hypotheses:
    - id: string  # H-NNN
      prediction: string
      verification_method: string
      tests_error_handling: boolean
      formed_at: string  # ISO 8601
      executed_at: string  # ISO 8601
      result: enum  # PASSED, FAILED
      actual_outcome: string
      stdout: string
      stderr: string
      exit_code: integer

  anti_gaming:
    static_analysis:
      if_test_patterns: array[string]
      hardcoded_values: array[string]
      mock_patterns: array[string]
    input_variation:
      variations_tested: integer
      invariance_detected: boolean
    todo_check:
      todos_found: array[string]
      documented_in_known_limitations: array[string]
      undocumented_todos: array[string]
    result: enum  # PASSED, FAILED

  verdict: enum  # PASSED, FAILED, NEEDS_ADJUDICATION
  verdict_reason: string
```

## Invariants

1. **Hypothesis formation precedes execution**: `formed_at` < `executed_at` for all hypotheses
2. **Deterministic verdict**: Same PR content + environment = same verdict
3. **Anti-gaming always runs**: Regardless of hypothesis verification outcome
4. **Evidence bundle always produced**: Every AAT run outputs exactly one bundle
5. **Status check always set**: Every AAT run updates GitHub status

## References

- PRD-0003: Agent Acceptance Testing Quality Gate
- GATE-AAT-ACCEPTANCE: PR passes hypothesis-driven testing
- GATE-AAT-ANTI-GAMING: No hardcoded values or undocumented TODOs
- GATE-AAT-EVIDENCE: Evidence bundle script present and valid
