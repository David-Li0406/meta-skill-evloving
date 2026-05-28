# Finding Categories

Taxonomy for deterministic finding classification. Enables FindingSignature computation, recurrence tracking, and automated countermeasure recommendations.

---

## SPEC_DEFECT

| Subcategory | Description | Source Angle |
|-------------|-------------|--------------|
| AMBIGUITY | Requirement can be interpreted multiple ways | COHERENCE_CONSISTENCY |
| INCOMPLETENESS | Requirement missing necessary detail | COHERENCE_CONSISTENCY |
| INCONSISTENCY | Requirement contradicts another | COHERENCE_CONSISTENCY |
| UNTESTABLE | Cannot write pass/fail test | VERIFIABILITY |
| UNDERSPECIFIED | Lacks measurable criteria | VERIFIABILITY |
| INFEASIBLE | Requirement cannot be implemented as specified | TECHNICAL_FEASIBILITY |
| STACK_MISMATCH | Requirement conflicts with system architecture | TECHNICAL_FEASIBILITY |
| PERF_IMPOSSIBLE | Performance target violates theoretical limits | TECHNICAL_FEASIBILITY |
| WEAK_CUSTOMER | Customer segment is too vague or generic | CUSTOMER_VALUE |
| PROBLEM_UNTESTABLE | Problem statement cannot be validated | CUSTOMER_VALUE |
| GOAL_DISCONNECTED | Goals don't address stated problem | CUSTOMER_VALUE |
| UNMITIGATED_RISK | Known risk without documented mitigation | IMPLEMENTATION_RISK |
| MISSING_FALLBACK | Critical path without degradation strategy | IMPLEMENTATION_RISK |
| IMPLICIT_DEPENDENCY | Undeclared dependency on external system | IMPLEMENTATION_RISK |
| MISSING_ROLLBACK | No rollback strategy for deployment | OPERATIONAL_READINESS |
| NAIVE_OPTIMIZATION | Claims "best" without tradeoff analysis | TRADEOFF_ANALYSIS |
| HIDDEN_COST | Tradeoff downsides are not acknowledged | TRADEOFF_ANALYSIS |
| UNSTABLE_FEEDBACK | Design creates reinforcing feedback loops | SYSTEM_DYNAMICS |
| SECOND_ORDER_HARM | Negative consequences on wider system | SYSTEM_DYNAMICS |

---

## TRACEABILITY_DEFECT

| Subcategory | Description | Source Angle |
|-------------|-------------|--------------|
| ORPHAN_REQ | Requirement not linked to customer need | - |
| ORPHAN_EVID | Evidence not referenced by any requirement | - |
| MISSING_CHAIN | Gap in Customer→Problem→Goal→REQ→EVID | - |
| CIRCULAR_REF | Circular dependency in references | - |
| BROKEN_REF | Reference to non-existent artifact | - |
| COUSIN_ABSTRACTION | Requirement duplicates existing abstraction | REUSE_POTENTIAL |
| IGNORED_EXTENSION_POINT | Existing extension point not leveraged | REUSE_POTENTIAL |
| UNGROUNDED_SOLUTION | Solution Overview does not map to CCP | REUSE_POTENTIAL |

---

## EVIDENCE_DEFECT

| Subcategory | Description | Source Angle |
|-------------|-------------|--------------|
| INSUFFICIENT | Evidence doesn't adequately demonstrate requirement | - |
| NON_REPRODUCIBLE | Evidence cannot be independently reproduced | - |
| MISSING_CAPTURE | No capture.paths specified | - |
| NETWORK_UNDEFINED | Command doesn't declare network_access | - |
| STALE_EVIDENCE | Evidence older than requirement modification | - |
| INVALID_NETWORK_ACCESS | network_access not valid enum value | - |
| MISSING_DATA_CLASS | Missing data.classification or data.redaction | SECURITY_POSTURE |
| CRITERION_VAGUE | Acceptance criterion uses subjective terms | VERIFIABILITY |
| EVIDENCE_WEAK | Evidence cannot falsify the requirement | VERIFIABILITY |
| COVERAGE_GAP | Significant scenarios lack test coverage | VERIFIABILITY |
| NO_OBSERVABILITY | Missing metrics, logging, or tracing requirements | OPERATIONAL_READINESS |
| UNDEFINED_NETWORK | Network boundaries not specified | SECURITY_POSTURE |

---

## QUALITY_DEFECT

| Subcategory | Description |
|-------------|-------------|
| UNCOVERED | Quality dimension not addressed (missing from framework) |
| INVALID_EXCEPTION | DOES_NOT_APPLY without proper exception (missing `exception.requested: true`, `exception.rationale`, or `exception.required_signoffs`) |
| MISSING_GUARDRAILS | Dimension with `disposition: DELEGATED_WITH_GUARDRAILS` but empty `delegation.guardrails` array |
| WEAK_EVIDENCE | Evidence category in `delegation.required_evidence_categories` not linked to actual evidence |
| MISSING_SIGNOFFS | Exception missing `required_signoffs` list (must have at least one authority) |

---

## GOVERNANCE_DEFECT

| Subcategory | Description |
|-------------|-------------|
| MISSING_GATE | Required gate not present in review |
| INVALID_AUTHORITY | Signoff from unauthorized authority |
| WAIVER_EXPIRED | Waiver past expiration_date |
| WAIVER_MISSING | WAIVED status but no waiver_id |
| SCOPE_MISMATCH | Waiver scope doesn't cover gate |

---

## FORMAT_DEFECT

| Subcategory | Description |
|-------------|-------------|
| PARSE_ERROR | YAML fails to parse |
| SCHEMA_VIOLATION | Document doesn't match schema |
| ID_FORMAT | ID doesn't match canonical pattern |
| SORT_ORDER | Lists not lexicographically sorted |
| DUPLICATE_ID | Same ID used twice |
| TAB_CHARACTER | File contains tab characters |

---

## FindingSignature

Deterministic signature for recurrence tracking. Computed as `blake3(json({category, subcategory, rule_id, location_type}))[:16]`.

**Fields:**
- `category`: One of the six categories above (e.g., SPEC_DEFECT)
- `subcategory`: Specific defect type within category (e.g., AMBIGUITY)
- `rule_id`: The lint rule or gate check that detected it (e.g., LINT-0007, or empty if no rule)
- `location_type`: The type of file where finding occurred: `META`, `CUSTOMER`, `PROBLEM`, `GOALS`, `SOLUTION`, `REQUIREMENT`, `EVIDENCE`, `QUALITY`, `TRACEABILITY`, or `GOVERNANCE`

**Properties:** Deterministic, content-based (not instance-based), stable across location changes within same location_type.

---

## Recurrence Thresholds

| Occurrences | Action |
|-------------|--------|
| 3 | Flag for countermeasure consideration |
| 5 | Auto-create countermeasure work item |
| 10 | Escalate to AUTH_PRODUCT |

---

## Severity Assignment Rules

Severity is determined by category and subcategory combination.

| Category | Subcategory | Default Severity | Source Angle |
|----------|-------------|------------------|--------------|
| SPEC_DEFECT | AMBIGUITY | MAJOR | COHERENCE_CONSISTENCY |
| SPEC_DEFECT | GOAL_DISCONNECTED | BLOCKER | CUSTOMER_VALUE |
| SPEC_DEFECT | IMPLICIT_DEPENDENCY | MAJOR | IMPLEMENTATION_RISK |
| SPEC_DEFECT | INCOMPLETENESS | MAJOR | COHERENCE_CONSISTENCY |
| SPEC_DEFECT | INCONSISTENCY | BLOCKER | COHERENCE_CONSISTENCY |
| SPEC_DEFECT | INFEASIBLE | BLOCKER | TECHNICAL_FEASIBILITY |
| SPEC_DEFECT | MISSING_FALLBACK | MAJOR | IMPLEMENTATION_RISK |
| SPEC_DEFECT | MISSING_ROLLBACK | MAJOR | OPERATIONAL_READINESS |
| SPEC_DEFECT | PERF_IMPOSSIBLE | BLOCKER | TECHNICAL_FEASIBILITY |
| SPEC_DEFECT | PROBLEM_UNTESTABLE | MAJOR | CUSTOMER_VALUE |
| SPEC_DEFECT | STACK_MISMATCH | MAJOR | TECHNICAL_FEASIBILITY |
| SPEC_DEFECT | UNDERSPECIFIED | MAJOR | VERIFIABILITY |
| SPEC_DEFECT | UNMITIGATED_RISK | MAJOR | IMPLEMENTATION_RISK |
| SPEC_DEFECT | UNTESTABLE | MAJOR | VERIFIABILITY |
| SPEC_DEFECT | WEAK_CUSTOMER | MAJOR | CUSTOMER_VALUE |
| SPEC_DEFECT | HIDDEN_COST | MAJOR | TRADEOFF_ANALYSIS |
| SPEC_DEFECT | NAIVE_OPTIMIZATION | MAJOR | TRADEOFF_ANALYSIS |
| SPEC_DEFECT | SECOND_ORDER_HARM | MAJOR | SYSTEM_DYNAMICS |
| SPEC_DEFECT | UNSTABLE_FEEDBACK | BLOCKER | SYSTEM_DYNAMICS |
| TRACEABILITY_DEFECT | BROKEN_REF | BLOCKER | - |
| TRACEABILITY_DEFECT | CIRCULAR_REF | BLOCKER | - |
| TRACEABILITY_DEFECT | COUSIN_ABSTRACTION | MAJOR | REUSE_POTENTIAL |
| TRACEABILITY_DEFECT | IGNORED_EXTENSION_POINT | MINOR | REUSE_POTENTIAL |
| TRACEABILITY_DEFECT | MISSING_CHAIN | BLOCKER | - |
| TRACEABILITY_DEFECT | ORPHAN_EVID | MINOR | - |
| TRACEABILITY_DEFECT | ORPHAN_REQ | MAJOR | - |
| TRACEABILITY_DEFECT | UNGROUNDED_SOLUTION | MAJOR | REUSE_POTENTIAL |
| EVIDENCE_DEFECT | COVERAGE_GAP | MAJOR | VERIFIABILITY |
| EVIDENCE_DEFECT | CRITERION_VAGUE | MAJOR | VERIFIABILITY |
| EVIDENCE_DEFECT | EVIDENCE_WEAK | MAJOR | VERIFIABILITY |
| EVIDENCE_DEFECT | INSUFFICIENT | MAJOR | - |
| EVIDENCE_DEFECT | INVALID_NETWORK_ACCESS | MAJOR | - |
| EVIDENCE_DEFECT | MISSING_CAPTURE | MAJOR | - |
| EVIDENCE_DEFECT | MISSING_DATA_CLASS | MAJOR | SECURITY_POSTURE |
| EVIDENCE_DEFECT | NETWORK_UNDEFINED | MAJOR | - |
| EVIDENCE_DEFECT | NO_OBSERVABILITY | MAJOR | OPERATIONAL_READINESS |
| EVIDENCE_DEFECT | NON_REPRODUCIBLE | MAJOR | - |
| EVIDENCE_DEFECT | STALE_EVIDENCE | MINOR | - |
| EVIDENCE_DEFECT | UNDEFINED_NETWORK | MAJOR | SECURITY_POSTURE |
| QUALITY_DEFECT | INVALID_EXCEPTION | BLOCKER | - |
| QUALITY_DEFECT | MISSING_GUARDRAILS | MAJOR | - |
| QUALITY_DEFECT | MISSING_SIGNOFFS | BLOCKER | - |
| QUALITY_DEFECT | UNCOVERED | BLOCKER | - |
| QUALITY_DEFECT | WEAK_EVIDENCE | MINOR | - |
| GOVERNANCE_DEFECT | INVALID_AUTHORITY | BLOCKER | - |
| GOVERNANCE_DEFECT | MISSING_GATE | BLOCKER | - |
| GOVERNANCE_DEFECT | SCOPE_MISMATCH | BLOCKER | - |
| GOVERNANCE_DEFECT | WAIVER_EXPIRED | BLOCKER | - |
| GOVERNANCE_DEFECT | WAIVER_MISSING | BLOCKER | - |
| FORMAT_DEFECT | DUPLICATE_ID | BLOCKER | - |
| FORMAT_DEFECT | ID_FORMAT | MAJOR | - |
| FORMAT_DEFECT | PARSE_ERROR | BLOCKER | - |
| FORMAT_DEFECT | SCHEMA_VIOLATION | BLOCKER | - |
| FORMAT_DEFECT | SORT_ORDER | MINOR | - |
| FORMAT_DEFECT | TAB_CHARACTER | MINOR | - |

---

## References

- [ANGLE_PROMPTS.md](ANGLE_PROMPTS.md) - Multi-angle analysis framework
- [FEEDBACK_LOOPS.md](FEEDBACK_LOOPS.md) - Recurrence-driven improvement
