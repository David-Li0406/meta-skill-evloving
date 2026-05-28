# Schema: Assessment

**Document Type**: SPC (Specification)
**Temporal Class**: Standing
**Scope**: Project
**Status**: DRAFT
**Version**: 1

---

## Purpose

This schema defines the Assessment artifact type for the Dialogue Framework. Assessments capture structured evaluations at various points in the development lifecycle, from daily developer experience checks to phase transition readiness reviews.

**Framework grounding**:
- **C-6 (Hicks et al. 2024)**: Developer Thriving constructs—agency, motivation, learning culture, support
- **C-7 (Obi et al. 2024)**: "Bad Days" indicators—blockers, interruptions, context switching, unclear requirements
- **STS Theory**: Joint optimisation requires monitoring both human and technical system health

---

## Assessment Types

| Type | Purpose | Trigger | Framework Source |
|------|---------|---------|------------------|
| `DAILY_CHECK` | Developer experience snapshot | End of session (Stop hook) | C-6, C-7 |
| `STAKEHOLDER_ALIGNMENT` | Alignment across stakeholders | Phase transition, human-initiated | TMS, STS |
| `PROBLEM_FRAMING` | Problem definition quality | Phase 1-2 transitions | Naur Theory-Building |
| `TTKM` | Team tacit knowledge health | Periodic (monthly) | Ryan & O'Connor (C-5) |
| `PHASE_READINESS` | Phase transition composite | Phase transitions | Framework integration |

---

## Core Schema

All assessments share this structure:

```yaml
Assessment:
  id: string                    # ASSESS-YYYYMMDD-HHMMSS
  timestamp: ISO8601            # When assessment was recorded
  assessment_type: AssessmentType
  assessor: ActorReference      # "ai:claude" | "human:<id>"
  phase: number | null          # 1-7, optional
  task_ref: string | null       # Task reference (e.g., "FW-023"), optional
  responses: object             # Type-specific payload (see below)
  context: string | null        # Optional situational context
  tags: string[]                # Optional categorisation tags
```

### ID Format

Assessment IDs follow the framework's temporal ID pattern:

```
ASSESS-YYYYMMDD-HHMMSS
       └──┬───┘ └──┬──┘
         date     time (UTC)
```

Example: `ASSESS-20260122-143000`

---

## Type-Specific Schemas

### DAILY_CHECK

Lightweight end-of-session assessment based on C-6/C-7 constructs.

```yaml
DailyCheckResponses:
  # Good day indicators (C-6 Developer Thriving)
  made_progress: boolean        # Made meaningful progress on tasks
  learned_something: boolean    # Learned something new or deepened understanding
  felt_supported: boolean       # Had support when needed (human or AI)
  had_agency: boolean           # Had control over how to approach work

  # Bad day indicators (C-7 "Bad Days")
  experienced_blockers: boolean # Encountered blockers that impeded progress
  context_switching: boolean    # Excessive context switching disrupted flow
  unclear_requirements: boolean # Worked with unclear or ambiguous requirements

  # Overall
  session_quality: 1-5          # Overall session quality rating
  notes: string | null          # Free-text reflection (optional)
```

### STAKEHOLDER_ALIGNMENT

Stakeholder alignment assessment (5 dimensions, 1-5 scale).

```yaml
StakeholderAlignmentResponses:
  # Alignment dimensions
  goal_clarity: 1-5             # "We agree on what success looks like"
  priority_alignment: 1-5       # "We agree on what matters most"
  risk_awareness: 1-5           # "We share understanding of risks"
  communication_quality: 1-5    # "Information flows effectively"
  decision_authority: 1-5       # "We agree on who decides what"

  stakeholders_consulted: string[]  # List of stakeholder identifiers
  notes: string | null
```

### PROBLEM_FRAMING

Problem framing checklist (6 boolean elements).

```yaml
ProblemFramingResponses:
  # Checklist items
  problem_stated: boolean       # Problem is explicitly stated
  scope_bounded: boolean        # Scope boundaries are defined
  success_criteria: boolean     # Success criteria are measurable
  constraints_identified: boolean # Constraints are documented
  assumptions_explicit: boolean # Key assumptions are stated
  stakeholders_identified: boolean # Affected stakeholders are identified

  confidence: 1-5               # Overall confidence in framing
  gaps_identified: string | null # Any gaps noted

  # Recommendation (computed from checklist + confidence)
  recommendation: "PROCEED" | "PROCEED_WITH_CAUTION" | "ADDRESS_GAPS" | "RETURN_TO_DEFINITION"
```

**Recommendation logic**: Both confirmed count AND confidence must meet thresholds:
- 6/6 confirmed AND confidence >= 4 -> PROCEED
- 5+/6 confirmed AND confidence >= 3 -> PROCEED_WITH_CAUTION
- 4+/6 confirmed AND confidence >= 2 -> ADDRESS_GAPS
- Otherwise -> RETURN_TO_DEFINITION

**Note**: PROBLEM_FRAMING uses more specific recommendations than PHASE_READINESS because problem definition issues require different remediation guidance than phase transition gaps.

### TTKM

Team Tacit Knowledge Measure constructs (Ryan & O'Connor, 2013).

```yaml
TTKMResponses:
  # TTKM constructs (1-5 scale: 1=strongly disagree, 5=strongly agree)
  shared_understanding: 1-5     # "Team members understand each other's work"
  knowledge_location: 1-5       # "We know who knows what"
  knowledge_access: 1-5         # "We can easily get knowledge from each other"
  knowledge_integration: 1-5    # "We effectively combine our knowledge"
  knowledge_creation: 1-5       # "We create new knowledge together"

  team_size: number             # Number of team members assessed
  notes: string | null
```

### PHASE_READINESS

Composite assessment for phase transitions. Aggregates other assessment types.

```yaml
PhaseReadinessResponses:
  current_phase: 1-7
  target_phase: 2-7

  # Component assessment references (IDs of prerequisite assessments)
  component_assessments:
    problem_framing: string | null      # ASSESS-... ID
    stakeholder_alignment: string | null
    ttkm: string | null
    daily_checks: string[]              # Array of recent ASSESS-... IDs

  # Readiness scores (computed or assessed)
  documentation_readiness: 1-5          # Are artefacts complete?
  knowledge_transfer_readiness: 1-5     # Is knowledge documented/shared?
  stakeholder_readiness: 1-5            # Are stakeholders aligned?
  technical_readiness: 1-5              # Are technical prerequisites met?

  # Recommendation
  recommendation: "PROCEED" | "PROCEED_WITH_CAUTION" | "DEFER"
  rationale: string                     # Explanation for recommendation
  blockers: string[]                    # Any blocking issues
  risks: string[]                       # Identified risks to proceeding

  # DEFER remediation guidance (only present when recommendation is DEFER)
  defer_guidance:                       # Optional, only when DEFER
    primary_gap: "documentation" | "knowledge" | "stakeholder" | "technical"
    primary_gap_score: 1-5              # Score of the primary gap dimension
    secondary_gaps: string[]            # Other dimensions scoring <= 2
    phase_tacit_percentage: number      # Tacit % for current phase (30-75)
    recommended_approach: "DIALOGUE" | "MIXED" | "ARTIFACT"
    specific_actions: string[]          # Recommended remediation activities
    restart_point:
      phase: 1-7                        # Phase to restart from
      phase_name: string
      focus: string                     # What to address before re-assessment

  # Approval
  approved_by: ActorReference | null    # Human who approved (if applicable)
  approval_timestamp: ISO8601 | null
```

**DEFER Remediation Model**:

The `defer_guidance` block uses a two-factor model:

1. **Phase tacit percentage**: Determines remediation character
   - High tacit (55-75%): Remediation needs dialogue, elicitation, facilitation
   - Medium tacit (40-50%): Balanced dialogue + artifact review
   - Low tacit (30-35%): Remediation can focus on artifacts, process

2. **Gap dimension**: Determines remediation type
   - `documentation`: Formal gaps in artifacts
   - `knowledge`: Tacit understanding not transferred
   - `stakeholder`: Alignment or consensus issues
   - `technical`: Dependencies, blockers, feasibility

The combination determines `recommended_approach`:
- **DIALOGUE**: Convene sessions, elicit understanding, facilitate alignment
- **MIXED**: Combine dialogue with artifact review/creation
- **ARTIFACT**: Focus on documentation, specifications, technical resolution

---

## Recommendation Enums

Different assessment types use different recommendation enums based on their purpose:

### Phase-Agnostic Assessments

**PROBLEM_FRAMING** uses specific remediation guidance:

| Value | Meaning | Action |
|-------|---------|--------|
| `PROCEED` | Well-framed | Proceed to implementation |
| `PROCEED_WITH_CAUTION` | Mostly framed | Document gaps, proceed carefully |
| `ADDRESS_GAPS` | Gaps present | Address gaps before major work |
| `RETURN_TO_DEFINITION` | Poorly framed | Return to problem definition |

### Phase Transition Assessments

**PHASE_READINESS** uses gate-oriented recommendations:

| Value | Meaning | Action |
|-------|---------|--------|
| `PROCEED` | Ready to transition | Human approves, proceed |
| `PROCEED_WITH_CAUTION` | Minor gaps | Review gaps, may proceed with mitigations |
| `DEFER` | Not ready | Address blockers before transitioning |

### Design Rationale

Problem framing uses more specific recommendations because:
1. It occurs earlier in the lifecycle where course correction is cheaper
2. "ADDRESS_GAPS" and "RETURN_TO_DEFINITION" provide clearer guidance than "DEFER"
3. The checklist nature supports granular remediation advice

Phase readiness uses gate-oriented recommendations because:
1. It's a go/no-go decision point
2. The composite nature aggregates multiple signals
3. Human approval is the final arbiter

---

## Context Graph Integration

### Node Type

Assessments are ARTIFACT nodes:

```yaml
ArtifactNode:
  id: "ASSESS-20260122-143000"
  node_type: ARTIFACT
  metadata:
    artifact_type: ASSESSMENT
    assessment_type: DAILY_CHECK
    temporal_class: Ephemeral   # DAILY_CHECK, TTKM
                  | Dynamic     # STAKEHOLDER_ALIGNMENT, PROBLEM_FRAMING
                  | Standing    # PHASE_READINESS
    content_type: text/yaml
    title: "Daily Check - 2026-01-22"
    summary: "Session quality: 4/5, progress made, no blockers"
    location_hint: ".dialogue/logs/assessments/ASSESS-20260122-143000.yaml"
    assessor: "human:pidster"
  status: ACTIVE
```

### Edge Type: ASSESSES

New edge type for traceability:

```yaml
AssessesEdge:
  source: "ASSESS-20260122-143000"  # Assessment
  target: "FW-023"                  # Task, Phase, or other artifact
  edge_type: ASSESSES
  metadata:
    assessment_type: DAILY_CHECK
    dimension: string | null        # Optional: which aspect was assessed
  confidence: 1.0
```

---

## Validation Rules

1. `id` must match pattern `ASSESS-YYYYMMDD-HHMMSS`
2. `assessment_type` must be one of the defined enum values
3. `assessor` must follow actor reference format
4. `phase` if present must be 1-7
5. `responses` must conform to type-specific schema
6. Scale values (1-5) must be integers within range
7. Boolean values must be `true` or `false`
8. `PHASE_READINESS.recommendation` must be one of: PROCEED, PROCEED_WITH_CAUTION, DEFER

---

## Usage Patterns

### Daily Check Flow

1. Stop hook detects end of substantive session
2. Hook outputs reminder (non-blocking)
3. Human or AI invokes `dialogue-daily-check` skill
4. Skill collects responses via interactive prompts
5. Assessment logged to `.dialogue/logs/assessments/`
6. Graph node and CREATED edge created
7. Optional: ASSESSES edge to active task

### Phase Readiness Flow

1. Human initiates phase transition assessment
2. `dialogue-assess-phase` skill invoked
3. Skill checks for recent component assessments
4. Missing components prompted or flagged
5. Composite score computed
6. Recommendation generated
7. Human reviews and approves/defers
8. Assessment logged with approval metadata

---

*Assessments provide structured checkpoints for developer experience and phase transitions. The schema supports both lightweight daily checks (visibility focus) and comprehensive readiness reviews (decision focus).*
