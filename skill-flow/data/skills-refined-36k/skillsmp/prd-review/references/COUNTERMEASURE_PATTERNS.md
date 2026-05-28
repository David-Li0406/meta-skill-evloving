# Countermeasure Patterns

Patterns for preventing recurrence of PRD defects. Countermeasures improve the factory (templates, schemas, lint rules) rather than fixing individual instances.

---

## Countermeasure Types

| Type | Target | Trigger |
|------|--------|---------|
| LINT_RULE_ADDITION | `standards/lint/LINT_SPEC.yaml` | Recurring FORMAT_DEFECT or structural SPEC_DEFECT |
| SCHEMA_CONSTRAINT | `standards/schemas/*.schema.yaml` | Recurring SCHEMA_VIOLATION or missing fields |
| TEMPLATE_ENHANCEMENT | `documents/prds/template/*` | Recurring INCOMPLETENESS |
| RUBRIC_ENHANCEMENT | `references/REVIEW_RUBRIC.md` | Content quality issues not caught by gates |
| SKILL_ENHANCEMENT | `SKILL.md` or references | Defects from user misunderstanding |

---

## Lifecycle

`IDENTIFIED → DESIGNED → IMPLEMENTED → VALIDATED → DEPLOYED → MONITORED`

| State | Entry Trigger | Exit Trigger |
|-------|---------------|--------------|
| IDENTIFIED | Finding signature reaches 3 occurrences | Countermeasure designed |
| DESIGNED | Solution documented with target file | Implementation PR created |
| IMPLEMENTED | PR merged to target file | Validation testing begins |
| VALIDATED | Corpus replay shows 100% detection, <5% false positives | Approval from AUTH_PRODUCT |
| DEPLOYED | Released to production | Monitoring period begins (30 days) |
| MONITORED | Deployed | Recurrence rate confirms < 1/month (then remove from active tracking) |

---

## Record Schema (minimal)

```yaml
countermeasure:
  id: "CM-XXXX"
  status: "DEPLOYED"
  trigger:
    finding_signature: "a1b2c3d4e5f67890"
    category: "SPEC_DEFECT"
    subcategory: "UNTESTABLE"
    occurrence_count: 5
  type: "LINT_RULE_ADDITION"
  target: "standards/lint/LINT_SPEC.yaml"
  validation:
    baseline_occurrences: 5
    post_implementation_occurrences: 0
```

---

## Validation

Before deployment, validate via corpus replay:
1. Collect PRDs with the defect
2. Run current review, count occurrences (baseline)
3. Apply countermeasure
4. Re-run review, verify reduction

**Acceptance:** Detection rate 100%, false positive rate <5%.

---

## Selection Guide

**When to create a countermeasure:** When a finding signature reaches the thresholds defined in `FINDING_CATEGORIES.md#recurrence-thresholds`:
- 3 occurrences: Flag for consideration
- 5 occurrences: Auto-create countermeasure work item
- 10 occurrences: Escalate to AUTH_PRODUCT

| Finding Category | Recommended Countermeasure |
|------------------|---------------------------|
| FORMAT_DEFECT.* | LINT_RULE_ADDITION or SCHEMA_CONSTRAINT |
| SPEC_DEFECT.INCOMPLETENESS | TEMPLATE_ENHANCEMENT |
| SPEC_DEFECT.AMBIGUITY | RUBRIC_ENHANCEMENT |
| TRACEABILITY_DEFECT.* | LINT_RULE_ADDITION |
| EVIDENCE_DEFECT.MISSING_* | SCHEMA_CONSTRAINT |
| QUALITY_DEFECT.UNCOVERED | TEMPLATE_ENHANCEMENT |
| GOVERNANCE_DEFECT.* | SCHEMA_CONSTRAINT |

---

## Metrics

| Metric | Target |
|--------|--------|
| Recurrence rate (post-deploy) | < 1/month |
| Detection rate | > 95% |
| False positive rate | < 5% |
| Time to deployment | < 14 days |
