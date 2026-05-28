# Council Protocol

Full orchestration instructions for the COUNCIL depth level. This protocol governs how 3 subagents coordinate across 3 iterative review cycles to produce a consensus assessment grounded in the North Star vision.

## Overview

The COUNCIL protocol is a multi-agent deliberation process that:
1. Spawns 3 subagents with emergent specializations
2. Each subagent selects 5 reasoning modes from the 80 available
3. Subagents execute 3 review cycles with inter-cycle onboarding notes
4. Findings converge through quorum voting (2/3 agreement)
5. Final assessment includes North Star alignment scoring

---

## State Machine

```
┌─────────┐
│  INIT   │ ── Initialize session, spawn subagents, select modes
└────┬────┘
     │
     ▼
┌─────────┐
│ CYCLE_1 │ ── BROAD: Cast wide net, all modes applied independently
│ (BROAD) │
└────┬────┘
     │ Generate onboarding notes
     ▼
┌─────────┐
│ CYCLE_2 │ ── REMEDIATE: Focus on BLOCKER/MAJOR, propose fixes
│(REMEDIATE)│
└────┬────┘
     │ Generate onboarding notes
     ▼
┌─────────┐
│ CYCLE_3 │ ── CONVERGE: Vote on contested findings, reach quorum
│(CONVERGE)│
└────┬────┘
     │
     ▼
   ┌───┴───┐
   │       │
   ▼       ▼
┌──────┐ ┌──────────┐ ┌─────────┐
│CONVERGED│ │DEADLOCKED│ │ ABORTED │
└──────┘ └──────────┘ └─────────┘
```

### State Transitions

| From | To | Trigger |
|------|----|---------|
| INIT | CYCLE_1 | All 3 subagents have selected 5 modes |
| CYCLE_1 | CYCLE_2 | All subagents completed broad review |
| CYCLE_2 | CYCLE_3 | All subagents completed remediation review |
| CYCLE_3 | CONVERGED | All blockers resolved AND quorum achieved |
| CYCLE_3 | DEADLOCKED | Quorum failed on ≥1 contested finding |
| ANY | ABORTED | Timeout (1 hour) OR budget exhausted |

---

## INIT Phase

### Step 1: Session Initialization

```yaml
session_id: "COUNCIL-{PRD_ID}-{timestamp}"
state: "INIT"
```

1. Create session file at `evidence/prd/{PRD_ID}/reviews/council_session_{timestamp}.yaml`
2. Load PRD content into context
3. Load `references/NORTH_STAR.md` and affirm oath

### Step 2: Spawn Subagents

Spawn 3 subagents (SA-1, SA-2, SA-3) with the following context:
- Full PRD content
- North Star vision document
- Modes-of-reasoning skill (all 80 modes)
- Council state schema

### Step 3: Mode Selection

Each subagent executes the mode selection algorithm:

#### 3.1 Extract PRD Affinity Signals

Scan PRD for signals that indicate mode affinity:

| Signal Pattern | Affinity Modes |
|----------------|----------------|
| API contracts, interfaces | 1, 7, 8 (Formal) |
| Performance, latency, throughput | 19, 48, 49 (Practical) |
| Security, authentication, authorization | 49, 79 (Robust, Adversarial) |
| Dependencies, integrations | 43, 55 (Systems, Game-theoretic) |
| User experience, personas | 56, 62 (Theory-of-mind, Narrative) |
| Data models, schemas | 4, 6, 7 (Algebraic, Constraint, Type) |
| Uncertainty, risk | 11, 21, 22 (Bayesian, Imprecise, Evidential) |
| Process, workflow | 47, 66 (Planning, Temporal) |
| Compliance, policy | 65, 71 (Deontic, Legal) |
| Trade-offs, decisions | 45, 46, 50 (Decision-theoretic, MCDA, Minimax) |

#### 3.2 Compute Affinity Scores

For each mode, compute:
```
affinity_score = base_relevance * signal_match_count / max_signals
```

#### 3.3 Apply Selection Constraints

1. **Meta-Level Requirement:** At least one subagent MUST select a mode from 75-80
2. **Overlap Penalty:** Penalize modes already selected by other subagents
3. **Category Diversity:** Prefer modes from different categories

#### 3.4 Select Top 5 Modes

Each subagent selects the 5 modes with highest adjusted affinity scores.

#### 3.5 Generate Emergent Role

Derive role label from mode cluster:

```python
def derive_emergent_role(selected_modes):
    categories = count_categories(selected_modes)
    dominant = max(categories, key=categories.get)

    role_map = {
        "Formal": ["Formal Rigorist", "Logic Guardian", "Proof Architect"],
        "Ampliative": ["Pattern Synthesizer", "Evidence Weaver", "Inference Engine"],
        "Uncertainty": ["Risk Assessor", "Uncertainty Navigator", "Probability Sage"],
        "Vagueness": ["Boundary Analyst", "Gradient Thinker", "Fuzzy Reasoner"],
        "Inconsistency & Defaults": ["Conflict Resolver", "Default Challenger", "Belief Auditor"],
        "Causal & Explanatory": ["Causal Detective", "Systems Thinker", "Root Cause Analyst"],
        "Practical": ["Pragmatic Optimizer", "Decision Engineer", "Solution Architect"],
        "Strategic & Social": ["Strategic Analyst", "Game Theorist", "Stakeholder Modeler"],
        "Dialectical & Rhetorical": ["Dialectician", "Narrative Analyst", "Frame Builder"],
        "Modal & Temporal": ["Modal Reasoner", "Temporal Analyst", "Possibility Explorer"],
        "Domain-Specific": ["Domain Expert", "Specialist Reviewer", "Context Maven"],
        "Meta-Level": ["Meta-Reasoner", "Epistemic Auditor", "Calibration Sentinel"]
    }

    return random.choice(role_map[dominant])
```

### Step 4: Validate Mode Selection

Before proceeding to CYCLE_1:
- [ ] Each subagent has exactly 5 modes
- [ ] At least one subagent has a mode in range 75-80
- [ ] Total mode overlap ≤ 5 across all subagents
- [ ] Each subagent has modes from ≥ 3 categories

---

## CYCLE_1: BROAD

**Purpose:** Cast a wide net. All 3 subagents apply all 5 of their modes independently.

### Execution

For each subagent:
1. Load PRD content and North Star context
2. For each selected mode (5 total):
   a. Apply mode-specific reasoning to PRD
   b. Generate findings using that mode's lens
   c. Tag each finding with `source_mode`
3. Generate North Star assessment
4. Record all findings in session state

### Cycle 1 Output Requirements

Each subagent produces:
- 0-N findings (no minimum, no maximum)
- 1 North Star assessment with phase scores
- Each finding MUST include:
  - `source_agent`
  - `source_cycle: 1`
  - `source_mode` (which of the 5 modes generated it)
  - `agreement_status: PENDING`

### Aggregation

After all subagents complete:
1. Merge findings, deduplicate by signature
2. For each finding, check if multiple subagents raised it:
   - If raised by ≥2 subagents: `agreement_status: MAJORITY`
   - If raised by all 3: `agreement_status: UNANIMOUS`
   - If raised by only 1: `agreement_status: PENDING`
3. Identify contested items (conflicting assessments)

### Onboarding Note Generation

Generate onboarding notes for Cycle 2:

```yaml
focus_areas:
  - Identify clusters of related findings
  - Highlight areas with BLOCKER/MAJOR severity
  - Note where subagents disagree

mode_recommendations:
  - Suggest which modes each subagent should emphasize
  - Recommend de-emphasizing low-yield modes

unresolved_questions:
  - List questions that emerged from review
  - Identify decisions requiring human input
```

---

## CYCLE_2: REMEDIATE

**Purpose:** Focus on severity. Re-examine BLOCKER/MAJOR findings and propose remediations.

### Pre-Cycle Loading

Each subagent loads:
- Cycle 1 onboarding notes
- Merged findings from Cycle 1
- Contested items list

### Execution

For each subagent:
1. Review BLOCKER findings first, then MAJOR
2. For each BLOCKER/MAJOR finding:
   a. Apply relevant modes to assess validity
   b. If finding is valid: propose specific remediation
   c. If finding is invalid: provide counter-argument
3. Re-examine contested items from Cycle 1
4. Generate new findings if discovered
5. Update North Star assessment

### Cycle 2 Output Requirements

Each subagent produces:
- Remediation proposals for BLOCKER/MAJOR findings
- Validity assessments for contested items
- Updated North Star assessment
- New findings (if any)

### Aggregation

After all subagents complete:
1. Merge remediation proposals
2. For contested items, tally support/dissent
3. Identify items still contested

### Onboarding Note Generation

Generate onboarding notes for Cycle 3:

```yaml
focus_areas:
  - Items requiring quorum vote
  - Remaining BLOCKER findings without remediation
  - North Star alignment gaps

convergence_targets:
  - Specific findings to resolve in Cycle 3
  - Questions requiring final decision

consensus_candidates:
  - Findings with majority agreement (ready for quorum)
```

---

## CYCLE_3: CONVERGE

**Purpose:** Reach consensus. Vote on contested findings using 2/3 quorum.

### Pre-Cycle Loading

Each subagent loads:
- Cycle 2 onboarding notes
- Current state of all findings
- Contested items requiring resolution

### Execution

For each contested finding:
1. Each subagent casts vote: SUPPORT or OPPOSE
2. Optionally provide final rationale
3. If 2/3 (2 of 3) agree: finding status = RESOLVED
4. If not: finding status = DEADLOCKED

For each unresolved BLOCKER:
1. Final attempt to propose remediation
2. If no remediation possible: escalate to AUTH_PRODUCT

### Quorum Rules

```python
def apply_quorum(finding, votes):
    support_count = sum(1 for v in votes if v == "SUPPORT")
    oppose_count = sum(1 for v in votes if v == "OPPOSE")

    if support_count >= 2:
        finding.agreement_status = "QUORUM_SUPPORT"
        finding.in_consensus = True
    elif oppose_count >= 2:
        finding.agreement_status = "QUORUM_OPPOSE"
        finding.in_consensus = False
    else:
        finding.agreement_status = "DEADLOCKED"
        # Escalate to DEADLOCKED terminal state
```

### Final North Star Assessment

Aggregate North Star assessments from all 3 subagents:

```python
def aggregate_north_star(assessments):
    final = {}
    for phase in range(1, 6):
        scores = [a.phase_scores[phase].score for a in assessments]
        final[phase] = {
            "score": mean(scores),
            "variance": variance(scores),
            "consensus": variance(scores) < 0.1  # Low variance = consensus
        }
    return final
```

---

## Terminal States

### CONVERGED

Conditions:
- All BLOCKER findings resolved (remediated or dismissed by quorum)
- Quorum achieved on all contested findings
- North Star assessment complete

Outputs:
- `verdict`: Based on remaining findings
- `consensus_findings`: All findings with quorum agreement
- `north_star_assessment`: Aggregated phase scores
- `council_metadata`: Session statistics

### DEADLOCKED

Conditions:
- Quorum failed on ≥1 contested finding after Cycle 3
- OR: BLOCKER finding unresolved with no remediation consensus

Outputs:
- `verdict`: NEEDS_ADJUDICATION
- `deadlocked_findings`: Findings that failed quorum
- `escalation_target`: AUTH_PRODUCT
- `council_metadata`: Session statistics

### ABORTED

Conditions:
- Session duration exceeds 1 hour
- OR: Token budget exhausted

Outputs:
- `verdict`: ABORTED
- `partial_findings`: All findings generated before abort
- `abort_reason`: TIMEOUT or BUDGET_EXHAUSTED
- `cycles_completed`: How many cycles finished

---

## Evidence Bundle Output

Council sessions produce an enhanced evidence bundle:

```json
{
  "schema_version": "1.0.0",
  "prd_id": "PRD-XXXX",
  "review_timestamp": "2026-01-26T10-00-00Z",
  "review_depth": "COUNCIL",

  "gates": [...],
  "findings": [...],
  "verdict": "PASSED",
  "verdict_reason": "Council reached consensus",

  "council_metadata": {
    "session_id": "COUNCIL-PRD-XXXX-20260126-100000",
    "subagents": [
      {
        "agent_id": "SA-1",
        "emergent_role": "Formal Rigorist",
        "selected_modes": [1, 7, 8, 43, 75]
      },
      ...
    ],
    "cycles_completed": 3,
    "total_findings_generated": 24,
    "findings_after_dedup": 15,
    "contested_items_resolved": 4,
    "quorum_achieved": true,
    "elapsed_time_seconds": 1847
  },

  "north_star_assessment": {
    "phase_scores": [0.7, 0.3, 0.1, 0.0, 0.0],
    "primary_phase_alignment": 1,
    "strategic_recommendations": [...],
    "violations": []
  }
}
```

---

## Mode Reference

The 80 reasoning modes are defined in `documents/skills/modes-of-reasoning/SKILL.md`.

### Mode Categories

| Category | Mode Range | Count |
|----------|------------|-------|
| Formal | 1-8 | 8 |
| Ampliative | 9-19 | 11 |
| Uncertainty | 20-24 | 5 |
| Vagueness | 25-29 | 5 |
| Inconsistency & Defaults | 30-36 | 7 |
| Causal & Explanatory | 37-43 | 7 |
| Practical | 44-54 | 11 |
| Strategic & Social | 55-58 | 4 |
| Dialectical & Rhetorical | 59-63 | 5 |
| Modal & Temporal | 64-67 | 4 |
| Domain-Specific | 68-74 | 7 |
| Meta-Level | 75-80 | 6 |

### Meta-Level Modes (Required Coverage)

At least one subagent MUST select from:
- 75: Meta-reasoning
- 76: Calibration and epistemic humility
- 77: Reflective equilibrium
- 78: Transcendental reasoning
- 79: Adversarial / red-team reasoning
- 80: Debiasing / epistemic hygiene reasoning

---

## Timeout and Budget

### Timeout

- Default: 1 hour (3600 seconds)
- Measured from INIT to terminal state
- On timeout: Abort with partial findings

### Token Budget

- Estimated budget: ~100K tokens per council session
- Monitor cumulative usage across all subagents
- On budget exhaustion: Abort with partial findings

### Budget Allocation

Approximate allocation per cycle:
- INIT + Mode Selection: ~5K tokens
- CYCLE_1 (BROAD): ~35K tokens
- CYCLE_2 (REMEDIATE): ~30K tokens
- CYCLE_3 (CONVERGE): ~25K tokens
- Final assembly: ~5K tokens

---

## Error Handling

### Subagent Failure

If a subagent fails during any cycle:
1. Log failure reason
2. Continue with remaining subagents
3. Adjust quorum requirement (2/2 if one fails)
4. Note degraded mode in final bundle

### Mode Selection Failure

If mode selection constraints cannot be satisfied:
1. Relax overlap penalty
2. Allow duplicate categories
3. Log constraint relaxation

### Convergence Failure

If Cycle 3 fails to reach quorum:
1. Record deadlocked findings
2. Emit partial consensus
3. Escalate to AUTH_PRODUCT with context
