# M13: Severity and Verdict

```yaml
module_id: M13
domain: verdict_computation
inputs: [Finding[]]
outputs: [EvidenceBundle]
```

---

## Severity Rubric

```yaml
BLOCKER:
  description: "Fails status check; merge blocked"
  triggers:
    - "unsafe code without local safety proof"
    - "soundness risk (UAF, double-free, aliasing, pointer stability)"
    - "QCP changes without adequate tests/evidence"
    - "public API footgun making misuse likely and catastrophic"
    - "semver hazard without justification and migration"
    - "concurrency safety risk (incorrect Send/Sync, ordering, locking)"
    - "MSRV violation or undefined MSRV in foundational crate"
    - "promised no_std broken"
    - "license compliance failure"
    - "uncovered cfg branches"

MAJOR:
  description: "Usually fails; pass only with explicit waiver"
  triggers:
    - "complexity increase without abstraction"
    - "panic risk in plausible production paths"
    - "poor invariant encoding pushing burden to callers"
    - "likely performance regression without measurement"
    - "incomplete documentation for public API"
    - "macro hygiene failures"
    - "missing property tests for allocators"

MINOR:
  description: "Must fix soon; can pass if tightly scoped"
  triggers:
    - "naming inconsistencies"
    - "missing docs for non-critical items"
    - "ergonomic improvements needed"
    - "non-idiomatic patterns"

NIT:
  description: "Non-blocking polish"
  triggers:
    - "formatting nits (should be CI-caught)"
    - "micro-idiom preferences"
```

---

## Verdict Computation

```mermaid
flowchart TD
    A[Collect Findings] --> B[Count by Severity]
    B --> C{blocker_count > 0?}
    C -->|YES| D[verdict = FAIL]
    C -->|NO| E{blocked_by_stop_condition?}
    E -->|YES| F[verdict = BLOCKED]
    E -->|NO| G{qcp AND major_count > 0?}
    G -->|YES| H[verdict = FAIL (presumptive)]
    G -->|NO| I[verdict = PASS]
```

```yaml
reducer:
  inputs:
    findings: Finding[]
    qcp: boolean
    stop_conditions: StopCondition[]

  computation:
    blocker_count: findings.filter(f => f.severity == "BLOCKER").length
    major_count: findings.filter(f => f.severity == "MAJOR").length
    minor_count: findings.filter(f => f.severity == "MINOR").length
    nit_count: findings.filter(f => f.severity == "NIT").length

  verdict_logic:
    IF blocker_count > 0:
      verdict = FAIL
    ELSE IF stop_conditions.length > 0:
      verdict = BLOCKED
    ELSE IF qcp AND major_count > 0:
      verdict = FAIL  # presumptive for QCP
    ELSE:
      verdict = PASS

  no_narrative_judgment: true
```

---

## Evidence Bundle Assembly

```yaml
output_schema:
  evidence_bundle:
    findings: Finding[]
    counts:
      blocker: int
      major: int
      minor: int
      nit: int
    verdict: PASS | FAIL | BLOCKED
    qcp: boolean
    qcp_categories: QCPCategory[]
    ci_evidence_verified: CICheck[]
    invariant_map_coverage: float
```

---

## Required Output Format

```yaml
review_notes_structure:
  - qcp_status:
      format: "QCP = YES/NO"
      justification: "one sentence"

  - scope_reviewed:
      - subsystems_touched: string[]
      - public_api_changes: boolean
      - unsafe_surfaces: boolean
      - concurrency_surfaces: boolean
      - performance_surfaces: boolean

  - evidence_verified:
      - ci_checks_passed: string[]
      - coverage_gaps: string[]

  - findings_list:
      FOR EACH finding:
        - severity: Severity
        - location: "file:line:symbol"
        - issue: "one paragraph"
        - remediation: "specific action"
        - proof_required: "test/bench/doc/invariant"

  - verdict:
      value: PASS | FAIL | BLOCKED
      justification: "based on findings"

rule:
  every_finding_has_proof_clause: true
  no_vague_guidance: true
```

---

## Output Schema

```typescript
interface EvidenceBundle {
  findings: Finding[];
  blocker_count: number;
  major_count: number;
  minor_count: number;
  nit_count: number;
  verdict: "PASS" | "FAIL" | "BLOCKED";
  qcp: boolean;
  qcp_categories: QCPCategory[];
}

interface ReviewNotes {
  qcp_status: {
    value: boolean;
    justification: string;
  };
  scope: ScopeReviewed;
  evidence: CIEvidenceVerified;
  findings: FindingSummary[];
  verdict: VerdictDecision;
}
```
