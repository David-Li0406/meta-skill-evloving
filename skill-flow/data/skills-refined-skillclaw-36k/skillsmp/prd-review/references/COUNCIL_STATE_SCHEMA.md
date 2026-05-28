# Council State Schema

YAML schema definitions for council session state. All council sessions persist state to enable inter-cycle communication and post-hoc analysis.

## Session File Location

```
evidence/prd/{PRD_ID}/reviews/council_session_{timestamp}.yaml
```

Timestamp format: `YYYYMMDD-HHMMSS` (filesystem-safe)

---

## Schema: Council Session

```yaml
# council_session_{timestamp}.yaml
schema_version: "1.0.0"
session_id: "COUNCIL-{PRD_ID}-{timestamp}"
prd_id: "PRD-XXXX"
initiated_at: "2026-01-26T10:00:00Z"
completed_at: null  # Set on CONVERGE or terminal state
terminal_state: null  # CONVERGED | DEADLOCKED | ABORTED

# Subagent declarations (populated in INIT phase)
subagents:
  - agent_id: "SA-1"
    emergent_role: null  # Auto-generated from mode cluster, e.g., "Formal Rigorist"
    selected_modes:
      - mode_id: 1
        mode_name: "Deductive reasoning"
        selection_rationale: "PRD contains logical preconditions requiring formal verification"
      - mode_id: 7
        mode_name: "Type-theoretic reasoning"
        selection_rationale: "API contracts benefit from type-level analysis"
      # ... (5 modes total)
    mode_cluster_signature: "formal-constructive"  # Hash of mode categories

  - agent_id: "SA-2"
    emergent_role: null
    selected_modes: []
    mode_cluster_signature: null

  - agent_id: "SA-3"
    emergent_role: null
    selected_modes: []
    mode_cluster_signature: null

# North Star context (loaded once, referenced throughout)
north_star:
  oath_affirmed: true
  phase_context:
    current_phase: 1
    phase_1_progress: 0.4  # Estimated progress toward exit criteria
    phase_2_readiness: 0.1
    phase_3_readiness: 0.0
    phase_4_readiness: 0.0
    phase_5_readiness: 0.0

# Cycle state (one entry per cycle)
cycles:
  - cycle_number: 1
    cycle_name: "BROAD"
    started_at: "2026-01-26T10:01:00Z"
    completed_at: null

    # Raw findings from each subagent
    subagent_findings:
      SA-1:
        findings: []  # Array of Finding objects
        north_star_assessment:
          phase_scores: [0.0, 0.0, 0.0, 0.0, 0.0]
          strategic_recommendations: []
      SA-2:
        findings: []
        north_star_assessment:
          phase_scores: [0.0, 0.0, 0.0, 0.0, 0.0]
          strategic_recommendations: []
      SA-3:
        findings: []
        north_star_assessment:
          phase_scores: [0.0, 0.0, 0.0, 0.0, 0.0]
          strategic_recommendations: []

    # Aggregated cycle outputs
    merged_findings: []  # Deduplicated findings with attribution
    contested_items: []  # Findings where subagents disagree

    # Onboarding notes for next cycle
    onboarding_notes:
      focus_areas: []  # Areas requiring deeper analysis
      mode_recommendations: []  # Suggested mode emphasis for next cycle
      unresolved_questions: []  # Questions to address in next cycle

  # Cycle 2 and 3 follow same structure
  - cycle_number: 2
    cycle_name: "REMEDIATE"
    # ...

  - cycle_number: 3
    cycle_name: "CONVERGE"
    # ...

# Final outputs (populated on terminal state)
final_outputs:
  verdict: null  # PASSED | FAILED | NEEDS_REMEDIATION | NEEDS_ADJUDICATION
  verdict_reason: null

  # Consensus findings (after quorum)
  consensus_findings: []

  # Findings that failed to reach quorum
  deadlocked_findings: []

  # North Star final assessment
  north_star_assessment:
    phase_scores: [0.0, 0.0, 0.0, 0.0, 0.0]
    primary_phase_alignment: null
    strategic_recommendations: []
    violations: []  # Any PHASE_REGRESSION, PHASE_SKIP, etc.

  # Council metadata
  council_metadata:
    total_findings_generated: 0
    findings_after_dedup: 0
    contested_items_count: 0
    quorum_achieved: false
    cycles_completed: 0
    budget_consumed_tokens: 0
    elapsed_time_seconds: 0
```

---

## Schema: Finding Object

```yaml
# Individual finding within council session
finding_id: "FND-{PRD_ID}-{NNN}"
source_agent: "SA-1"
source_cycle: 1
source_mode: 7  # Which reasoning mode generated this finding

category: "SPEC_DEFECT"
subcategory: "AMBIGUOUS_REQUIREMENT"
severity: "MAJOR"

location: "documents/prds/PRD-XXXX/requirements/REQ-0001.yaml:acceptance_criteria[0]"
location_type: "REQUIREMENT"

description: "Acceptance criterion lacks quantitative bound"
remediation: "Add latency threshold: 'p99 < 200ms under 1000 RPS'"

# Council-specific fields
agreement_status: "UNANIMOUS" | "MAJORITY" | "CONTESTED" | "PENDING"
supporting_agents: ["SA-1", "SA-2"]
dissenting_agents: ["SA-3"]
dissent_rationale: "SA-3 argues the implicit bound from SLA is sufficient"

# Signature for deduplication
signature: "blake3({category, subcategory, location})[:16]"
```

---

## Schema: Onboarding Notes

```yaml
# Generated after each cycle (except final)
cycle_source: 1
generated_at: "2026-01-26T10:15:00Z"

focus_areas:
  - area: "Security requirements"
    rationale: "Multiple findings related to authentication gaps"
    suggested_modes: [49, 79]  # Robust/worst-case, Adversarial
    priority: "HIGH"

  - area: "Performance constraints"
    rationale: "Latency bounds missing from 3 requirements"
    suggested_modes: [19, 48]  # Fermi estimation, Optimization
    priority: "MEDIUM"

mode_recommendations:
  - agent_id: "SA-2"
    current_modes: [13, 14, 15, 37, 43]
    recommended_emphasis: [37, 43]  # Focus on causal modes
    rationale: "Root cause analysis needed for contested findings"

unresolved_questions:
  - question: "Is eventual consistency acceptable for user-facing reads?"
    relevant_findings: ["FND-PRD-XXXX-003", "FND-PRD-XXXX-007"]
    decision_required_by: "AUTH_PRODUCT"

contested_items_summary:
  - finding_id: "FND-PRD-XXXX-005"
    supporters: ["SA-1", "SA-3"]
    dissenters: ["SA-2"]
    core_disagreement: "Whether the caching strategy introduces staleness risk"
    suggested_resolution: "Request evidence artifact demonstrating cache invalidation"
```

---

## Schema: Subagent Mode Selection

```yaml
# Mode selection declaration for a subagent
agent_id: "SA-1"
selection_timestamp: "2026-01-26T10:00:30Z"

# Affinity signals extracted from PRD
prd_affinity_signals:
  - signal: "Contains API contract definitions"
    affinity_modes: [1, 7, 8]  # Deductive, Type-theoretic, Counterexample
  - signal: "Mentions 'latency' and 'performance'"
    affinity_modes: [19, 48, 49]  # Fermi, Optimization, Robust
  - signal: "References external dependencies"
    affinity_modes: [43, 55]  # Systems thinking, Game-theoretic

# Mode selection with rationale
selected_modes:
  - mode_id: 1
    mode_name: "Deductive reasoning"
    category: "Formal"
    selection_rationale: "API contracts require formal precondition verification"
    affinity_score: 0.9

  - mode_id: 7
    mode_name: "Type-theoretic reasoning"
    category: "Formal"
    selection_rationale: "Type-level analysis catches interface mismatches"
    affinity_score: 0.85

  - mode_id: 43
    mode_name: "Systems thinking"
    category: "Causal & Explanatory"
    selection_rationale: "Multiple interacting components require holistic view"
    affinity_score: 0.8

  - mode_id: 75
    mode_name: "Meta-reasoning"
    category: "Meta-Level"
    selection_rationale: "Required: at least one META_LEVEL mode per council"
    affinity_score: 0.7

  - mode_id: 49
    mode_name: "Robust / worst-case reasoning"
    category: "Practical"
    selection_rationale: "Performance requirements need boundary analysis"
    affinity_score: 0.75

# Overlap penalty (penalize if modes overlap with other subagents)
overlap_with_other_agents:
  - agent_id: "SA-2"
    overlapping_modes: [43]
    penalty_applied: 0.1

# Emergent role derivation
mode_categories_present:
  - "Formal": 2
  - "Causal & Explanatory": 1
  - "Meta-Level": 1
  - "Practical": 1

emergent_role: "Formal Systems Analyst"
role_derivation: "Plurality in Formal category (2/5 modes)"
```

---

## Schema: North Star Assessment

```yaml
# North Star assessment at cycle or session level
assessed_at: "2026-01-26T10:20:00Z"
assessor: "SA-1" | "COUNCIL"  # Individual or collective

phase_scores:
  phase_1:
    score: 0.7
    direct_contribution: 0.8
    enabling_contribution: 0.6
    no_harm: 0.9
    rationale: "PRD directly improves code generation quality (Phase 1 objective)"

  phase_2:
    score: 0.3
    direct_contribution: 0.2
    enabling_contribution: 0.5
    no_harm: 1.0
    rationale: "Infrastructure work enables future innovation but not directly novel"

  phase_3:
    score: 0.1
    direct_contribution: 0.0
    enabling_contribution: 0.2
    no_harm: 1.0
    rationale: "No direct commercial impact; enables future productization"

  phase_4:
    score: 0.0
    direct_contribution: 0.0
    enabling_contribution: 0.1
    no_harm: 1.0
    rationale: "Too early for partnership relevance"

  phase_5:
    score: 0.0
    direct_contribution: 0.0
    enabling_contribution: 0.0
    no_harm: 1.0
    rationale: "No life sciences connection"

primary_phase_alignment: 1
secondary_phase_alignment: [2]

strategic_recommendations:
  - recommendation: "Add extensibility hooks for future ML model integration"
    target_phase: 2
    effort: "LOW"
    impact: "MEDIUM"

  - recommendation: "Consider API design that could support external licensing"
    target_phase: 3
    effort: "MEDIUM"
    impact: "HIGH"

violations: []  # Empty if none detected
# Example violation:
# - violation_type: "PHASE_SKIP"
#   description: "PRD assumes Phase 2 capabilities not yet achieved"
#   severity: "BLOCKER"
#   remediation: "Scope PRD to Phase 1 objectives; defer advanced features"
```

---

## Validation Rules

### Session State Invariants

1. **Mode Count:** Each subagent MUST have exactly 5 selected modes
2. **Meta-Level Requirement:** At least one subagent MUST include a mode from range 75-80
3. **Cycle Progression:** Cycles MUST complete in order: 1 → 2 → 3
4. **Findings Attribution:** Every finding MUST have `source_agent` and `source_cycle`
5. **Quorum Calculation:** Quorum = 2/3 agreement (2 of 3 subagents)
6. **Terminal State:** Session MUST end in CONVERGED, DEADLOCKED, or ABORTED

### Mode Selection Constraints

1. **No Duplicates:** A subagent cannot select the same mode twice
2. **Affinity Minimum:** At least 3 of 5 modes MUST have affinity_score ≥ 0.5
3. **Overlap Penalty:** Total overlap across all subagents SHOULD be ≤ 5 modes
4. **Category Diversity:** Each subagent SHOULD have modes from ≥ 3 categories

### Onboarding Note Requirements

1. **Timing:** Notes MUST be generated after Cycle 1 and Cycle 2
2. **Consumption:** Notes from Cycle N MUST be referenced in Cycle N+1 findings
3. **Focus Areas:** At least 1 focus area MUST be identified per cycle
4. **Mode Recommendations:** At least one mode recommendation per subagent
