# Feedback Loops

Recursive improvement mechanisms connecting downstream execution signals back to PRD template and process refinement.

---

## Overview

The PRD review system improves over time through four feedback loops. Each loop captures signals from downstream execution and routes them to specific improvement targets.

| Loop ID | Signal Source | Feedback Target | Automation Level |
|---------|---------------|-----------------|------------------|
| LOOP-TICKET | Ticket completion | PRD template enhancement | Automated (Variance-Triggered) |
| LOOP-AAT | AAT verification | Verifiability rubric | Semi-automated |
| LOOP-RECURRENCE | FindingSignature counts | Countermeasure creation | Automated |
| LOOP-IMPACT | Impact map grounding | REUSE_POTENTIAL angle | Manual |

---

## Signal-to-Noise Ratio (SNR) Check

After every review, compute the Signal-to-Noise Ratio to ensure review depth calibration:

```
SNR = (BLOCKER + MAJOR findings) / (total findings)
```

- If SNR < 0.5 (more than half are MINOR/INFO), the review depth was **miscalibrated**.
- Emit `REVIEW_CALIBRATION_WARNING` and record for depth algorithm tuning.
- This prevents "Alert Fatigue" — the Pragmatist's concern.

---

## LOOP-TICKET: Ticket Completion Feedback

**Signal Source:** Completed engineering tickets derived from PRD requirements

**Feedback Target:** PRD template structure and drafting guidance

### Signal Schema

```yaml
ticket_completion_signal:
  ticket_id: "TCK-XXXXX"
  prd_id: "PRD-XXXX"
  requirement_ids: ["REQ-XXXX", "REQ-YYYY"]
  completion_timestamp: "2026-01-25T10:00:00Z"

  # Deviation report - requirements discovered during implementation
  deviation_report:
    discovered_requirements:
      - description: "Need to handle rate limiting from external API"
        severity: MAJOR
        should_have_been: "REQ in original PRD"
        category: IMPLEMENTATION_RISK

    scope_changes:
      - original: "Support 3 payment providers"
        actual: "Support 2 providers (one deprecated during implementation)"
        reason: "Provider sunset announcement after PRD approval"

    estimate_variance:
      original_points: 8
      actual_points: 13
      variance_reason: "Undocumented legacy system integration required"

  # Implementation learnings
  learnings:
    - pattern: "External API integrations always need fallback"
      recommendation: "Add IMPLEMENTATION_RISK checklist item"
    - pattern: "Legacy system constraints often undocumented"
      recommendation: "Add discovery step to PRD template"
```

### Feedback Processing

1. **Collect:** Aggregate deviation reports from completed tickets
2. **Analyze:** Identify patterns in discovered requirements
3. **Categorize:** Map patterns to PRD template sections
4. **Propose:** Create template enhancement proposals

### Template Enhancement Schema

```yaml
template_enhancement:
  enhancement_id: "ENH-XXXX"
  triggered_by:
    signal_type: TICKET_COMPLETION
    ticket_ids: ["TCK-00123", "TCK-00145", "TCK-00167"]
    pattern: "External API fallback requirements consistently discovered"

  target:
    template_file: "documents/prds/template/requirements/REQ-0001.yaml"
    section: "acceptance_criteria"

  proposed_change:
    type: ADD_CHECKLIST_ITEM
    content: |
      - id: AC-FALLBACK
        criterion: "For external API calls, fallback behavior MUST be specified"
        verification_method: "Review requirement for fallback clause"

  evidence:
    occurrence_count: 3
    ticket_references:
      - ticket_id: "TCK-00123"
        deviation: "Rate limiting fallback not specified"
      - ticket_id: "TCK-00145"
        deviation: "Timeout handling not specified"
      - ticket_id: "TCK-00167"
        deviation: "Retry policy not specified"
```

### Thresholds

| Metric | Threshold | Action |
|--------|-----------|--------|
| Same deviation pattern | 3 occurrences | Flag for consideration |
| Same deviation pattern | 5 occurrences | Auto-create enhancement proposal |
| Estimate variance > 50% | 3 occurrences | Flag PRD estimation guidance |

---

## LOOP-AAT: AAT Verification Feedback

**Signal Source:** Agent Acceptance Testing hypothesis results

**Feedback Target:** Verifiability angle rubric and evidence requirements

### Signal Schema

```yaml
aat_verification_signal:
  aat_run_id: "AAT-XXXXX"
  prd_id: "PRD-XXXX"
  pr_id: "PR-XXXX"
  verification_timestamp: "2026-01-25T10:00:00Z"

  # Hypothesis outcomes
  hypotheses:
    - hypothesis_id: "HYP-001"
      requirement_id: "REQ-0003"
      evidence_id: "EVID-0003"

      # Did evidence actually verify the requirement?
      verdict: PASSED | FAILED | INCONCLUSIVE

      # Gaming detection
      gaming_analysis:
        detected: false
        indicators: []
        # OR
        detected: true
        indicators:
          - type: "NARROW_COVERAGE"
            description: "Test only covers happy path, ignores error cases"
          - type: "SELF_FULFILLING"
            description: "Evidence command checks same code that implements feature"

    - hypothesis_id: "HYP-002"
      requirement_id: "REQ-0005"
      evidence_id: "EVID-0005"
      verdict: FAILED
      failure_analysis:
        root_cause: "Criterion was subjective, no objective pass/fail possible"
        criterion_text: "System should perform acceptably under load"
        recommendation: "Add measurable threshold: p99 < 200ms at 1000 RPS"

  # Evidence sufficiency assessment
  evidence_assessment:
    total_requirements: 12
    fully_verified: 8
    partially_verified: 2
    not_verifiable: 2
    coverage_ratio: 0.67

  # Recommendations for verifiability improvement
  verifiability_recommendations:
    - requirement_id: "REQ-0005"
      current_score: NOT_VERIFIABLE
      recommended_changes:
        - "Replace subjective term 'acceptably' with measurable threshold"
        - "Add specific load profile (concurrent users, RPS)"
        - "Define measurement method (what tool, what metric)"
```

### Feedback Processing

1. **Collect:** Aggregate AAT results across PRD implementations
2. **Identify:** Find patterns in verification failures and gaming attempts
3. **Refine:** Update VERIFIABILITY angle prompts and rubrics
4. **Strengthen:** Add anti-gaming patterns to evidence requirements

### Verifiability Rubric Update Schema

```yaml
verifiability_rubric_update:
  update_id: "VRU-XXXX"
  triggered_by:
    signal_type: AAT_VERIFICATION
    aat_run_ids: ["AAT-00234", "AAT-00256", "AAT-00278"]
    pattern: "Subjective performance criteria consistently fail verification"

  target:
    file: "documents/skills/prd-review/references/ANGLE_PROMPTS.md"
    section: "VERIFIABILITY"

  proposed_change:
    type: ADD_ANTI_PATTERN
    content: |
      ### Anti-Pattern: Subjective Performance Terms

      **Pattern:** Criteria using "acceptable", "reasonable", "fast", "responsive"
      **Problem:** Cannot be objectively measured, gaming-prone
      **Mitigation:** Replace with specific metric + threshold + measurement method

      | Bad | Good |
      |-----|------|
      | "performs acceptably" | "p99 latency < 200ms" |
      | "responds quickly" | "response time < 100ms for 99% of requests" |
      | "handles reasonable load" | "sustains 1000 RPS with error rate < 0.1%" |
```

### Thresholds

| Metric | Threshold | Action |
|--------|-----------|--------|
| Same gaming pattern | 2 occurrences | Add to anti-gaming checklist |
| Same verification failure pattern | 3 occurrences | Update angle rubric |
| Coverage ratio < 0.8 | 3 PRDs | Flag evidence standards gap |

---

## LOOP-RECURRENCE: Finding Signature Tracking

**Signal Source:** FindingSignature occurrence counts across PRD reviews

**Feedback Target:** Countermeasure creation and template fixes

### Signal Schema

```yaml
recurrence_signal:
  signature: "abc123..."  # blake3 hash
  signature_components:
    category: "SPEC_DEFECT"
    subcategory: "AMBIGUITY"
    rule_id: "LINT-0007"
    location_type: "REQUIREMENT"

  occurrences:
    count: 5
    prd_ids: ["PRD-0001", "PRD-0003", "PRD-0004", "PRD-0005", "PRD-0006"]
    first_seen: "2025-11-15T10:00:00Z"
    last_seen: "2026-01-25T10:00:00Z"

  trend:
    direction: INCREASING | STABLE | DECREASING
    velocity: 0.5  # occurrences per week
```

### Feedback Processing

1. **Track:** Maintain running counts of FindingSignature occurrences
2. **Threshold:** Trigger actions when counts exceed thresholds
3. **Create:** Generate countermeasure proposals automatically
4. **Verify:** Track whether countermeasures reduce recurrence

### Countermeasure Schema

```yaml
countermeasure:
  countermeasure_id: "CM-XXXX"
  triggered_by:
    signature: "abc123..."
    occurrence_count: 5
    threshold_triggered: AUTO_CREATE

  target_finding:
    category: "SPEC_DEFECT"
    subcategory: "AMBIGUITY"
    typical_description: "Requirement uses ambiguous quantifier without threshold"

  intervention:
    type: TEMPLATE_FIX | LINT_RULE | GUIDANCE_UPDATE | TRAINING

    # For TEMPLATE_FIX
    template_change:
      file: "documents/prds/template/requirements/REQ-0001.yaml"
      change: "Add comment enforcing explicit thresholds"

    # For LINT_RULE
    lint_rule:
      rule_id: "LINT-0010"
      description: "Quantifiers MUST have explicit bounds"
      pattern: "/(many|few|some|several|often|rarely)/"

    # For GUIDANCE_UPDATE
    guidance_update:
      file: "documents/skills/prd-review/references/CREATE_PRD_PROMPT.md"
      section: "Writing Requirements"
      addition: "Avoid ambiguous quantifiers: many, few, some, several"

  effectiveness_tracking:
    pre_intervention_rate: 0.5  # occurrences per week
    post_intervention_rate: null  # measured after deployment
    reduction_target: 0.8  # 80% reduction
```

### Thresholds

| Occurrences | Action |
|-------------|--------|
| 3 | Flag for countermeasure consideration (manual review) |
| 5 | Auto-create countermeasure ticket |
| 10 | Escalate to AUTH_PRODUCT for priority intervention |

### Recurrence Dashboard Schema

```yaml
recurrence_dashboard:
  generated_at: "2026-01-25T10:00:00Z"
  period: "2026-01-01 to 2026-01-25"

  top_recurring_findings:
    - signature: "abc123..."
      category: "SPEC_DEFECT"
      subcategory: "AMBIGUITY"
      count: 8
      status: COUNTERMEASURE_DEPLOYED
      countermeasure_id: "CM-0003"

    - signature: "def456..."
      category: "EVIDENCE_DEFECT"
      subcategory: "CRITERION_VAGUE"
      count: 6
      status: FLAGGED_FOR_REVIEW

    - signature: "ghi789..."
      category: "TRACEABILITY_DEFECT"
      subcategory: "ORPHAN_REQ"
      count: 4
      status: UNDER_THRESHOLD

  countermeasure_effectiveness:
    - countermeasure_id: "CM-0001"
      deployed: "2025-12-01"
      pre_rate: 0.8
      post_rate: 0.1
      reduction: 0.875
      status: EFFECTIVE

    - countermeasure_id: "CM-0002"
      deployed: "2025-12-15"
      pre_rate: 0.5
      post_rate: 0.4
      reduction: 0.2
      status: INEFFECTIVE
      recommendation: "Review and strengthen intervention"
```

---

## LOOP-IMPACT: Impact Map Grounding

**Signal Source:** Impact map analysis during RFC creation

**Feedback Target:** REUSE_POTENTIAL angle refinement

### Signal Schema

```yaml
impact_map_signal:
  rfc_id: "RFC-XXXX"
  prd_id: "PRD-XXXX"
  analysis_timestamp: "2026-01-25T10:00:00Z"

  # Reuse analysis
  reuse_analysis:
    total_requirements: 15
    net_new_requirements: 8
    extension_requirements: 5
    reuse_requirements: 2

    net_new_ratio: 0.53  # 8/15

    # Unmappable requirements - couldn't determine reuse category
    unmappable:
      - requirement_id: "REQ-0007"
        reason: "Unclear if existing RetryPolicy applies"
        recommendation: "PRD should specify whether to reuse or create new"

    # Missed reuse opportunities
    missed_reuse:
      - requirement_id: "REQ-0004"
        existing_abstraction: "core/validation.rs:Validator"
        similarity_score: 0.85
        recommendation: "Should extend existing Validator trait"

    # Cousin abstractions detected
    cousin_abstractions:
      - requirement_id: "REQ-0009"
        existing: "core/cache.rs:CachePolicy"
        proposed: "New caching strategy in requirement"
        overlap: 0.7
        recommendation: "Unify into single caching abstraction"

  # Architecture impact
  architecture_impact:
    components_affected: 5
    new_components: 2
    modified_components: 3

    extension_points_used:
      - extension_point: "core/plugins.rs:Plugin"
        used_by: ["REQ-0003"]

    extension_points_ignored:
      - extension_point: "core/middleware.rs:Middleware"
        could_apply_to: ["REQ-0006"]
        reason: "Requirement specifies custom middleware instead"
```

### Feedback Processing

1. **Collect:** Aggregate impact map analyses across RFCs
2. **Identify:** Find patterns in missed reuse and cousin abstractions
3. **Enhance:** Improve REUSE_POTENTIAL angle prompts
4. **Update:** Maintain extension point registry for future PRDs

### REUSE_POTENTIAL Enhancement Schema

```yaml
reuse_potential_enhancement:
  enhancement_id: "RPE-XXXX"
  triggered_by:
    signal_type: IMPACT_MAP_GROUNDING
    rfc_ids: ["RFC-0005", "RFC-0007", "RFC-0009"]
    pattern: "Caching requirements frequently miss existing CachePolicy"

  target:
    file: "documents/skills/prd-review/references/ANGLE_PROMPTS.md"
    section: "REUSE_POTENTIAL"

  proposed_change:
    type: ADD_KNOWN_ABSTRACTION
    content: |
      ### Known Abstraction: CachePolicy

      **Location:** `core/cache.rs:CachePolicy`
      **Capabilities:** TTL, LRU eviction, cache-aside, write-through
      **When to Check:** Any requirement mentioning caching, memoization, or
      performance optimization through data reuse

      **Question to Ask:** Does this requirement need custom caching, or can
      it use CachePolicy with appropriate configuration?
```

### Thresholds

| Metric | Threshold | Action |
|--------|-----------|--------|
| Net-new ratio > 0.7 | 3 PRDs | Flag for reuse analysis review |
| Same missed abstraction | 2 occurrences | Add to known abstractions list |
| Same unmappable pattern | 3 occurrences | Update PRD template guidance |

---

## Feedback Loop Orchestration

### Priority Order

When multiple loops produce updates targeting the same artifact, apply in priority order:

1. **LOOP-RECURRENCE** (highest) - Direct countermeasures for recurring defects
2. **LOOP-AAT** - Evidence and verification improvements
3. **LOOP-IMPACT** - Reuse pattern updates
4. **LOOP-TICKET** (lowest) - General template enhancements

### Conflict Resolution

```yaml
conflict_resolution:
  scenario: "Two loops propose changes to same template section"
  resolution:
    - Merge non-conflicting changes
    - For conflicts, prefer higher-priority loop
    - Flag for human review if both are same priority
    - Document conflict in enhancement record
```

### Feedback Cycle

```
PRD Draft → PRD Review → RFC → Tickets → Implementation → AAT
    ↑                                                       │
    │                                                       │
    └───────── FEEDBACK LOOPS ─────────────────────────────┘
```

---

## References

- [FINDING_CATEGORIES.md](FINDING_CATEGORIES.md) - FindingSignature computation
- [ANGLE_PROMPTS.md](ANGLE_PROMPTS.md) - Angle definitions updated by feedback
- [COUNTERMEASURE_PATTERNS.md](COUNTERMEASURE_PATTERNS.md) - Countermeasure templates
