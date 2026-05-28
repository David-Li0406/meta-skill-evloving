---
name: case-management
description: Manage knowledge work using CMMN (Case Management Model and Notation) primitives including Cases, Stages, Tasks, and Artifacts. Use for discretionary workflows, research projects, consulting engagements, creative work, or any knowledge-intensive work requiring flexible orchestration. Integrates with PM-Agent for AI-driven case lifecycle management.
license: Complete terms in LICENSE.txt
---

# Case Management (CMMN)

Orchestrate knowledge-intensive work using SEA-Forge™'s case-based approach. Cases adapt to reality rather than forcing reality into rigid plans, making them ideal for research, consulting, creative projects, and complex discretionary workflows.

**For reference:** [Case Management Handbook](../../../docs/handbooks/ProjectCase_Mgmt_Handbook/README.md) | [SDS-012: Case Management Service](../../../docs/specs/cognitive-extension/sds/012-case-management-service.md)

---

## When to Use This Skill

Use case-management when:

1. **Discretionary Work**: Outcome is clear but path is uncertain (research, design)
2. **Knowledge Reification**: Raw notes need to become formal specifications or assets
3. **Hybrid Teams**: Coordinating mix of human experts and AI specialists
4. **Complex Workflows**: Multiple stages with event-driven transitions
5. **Asset Formation**: Work products should become reusable organizational capital

---

## Core Concepts

### CMMN Primitives

| Primitive | Purpose | Example |
|-----------|---------|---------|
| **Case** | Container for knowledge work | "Market Research Q1", "Feature X Design" |
| **Stage** | Logical grouping of tasks | "Discovery", "Analysis", "Recommendations" |
| **Task** | Unit of work (discretionary or mandatory) | "Interview stakeholders", "Write spec" |
| **Sentry** | Event-driven conditional trigger | "When 3 interviews complete, activate analysis" |
| **Milestone** | Observable achievement | "Discovery complete", "Spec approved" |

### Artifact Pipeline (Four Reification Stages)

```
Cognitive Artifact → Intellectual Artifact → Information Product → Intellectual Capital
(notes, sketches) → (specs, designs)      → (software, reports) → (organizational assets)
```

**Key Principle**: Artifacts must **progress through stages in order**. No "teleportation" – every transition requires provenance via TransitionTokens.

### PM-Agent Orchestration

The **Project Manager Agent** (PM-Agent) serves as conductor for hybrid human-AI teams:
- Activates discretionary tasks when sentries fire
- Assigns tasks to appropriate specialists (human or AI)
- Tracks artifact pipeline progression
- Enforces governance (Sovereign Gates for high-impact decisions)

---

## Workflow: Creating a Case

### Step 1: Define Desired Outcome

Every case starts with a clear goal:

**Template**:
```yaml
case:
  id: "case-2026-001"
  title: "<Brief descriptive title>"
  desiredOutcome: "<What success looks like>"
  context: "<Why this case exists>"
  stakeholders:
    - name: "<Stakeholder>"
      role: "<Their role>"
```

**Example**:
```yaml
case:
  id: "case-2026-001"
  title: "Optimize Skills Architecture"
  desiredOutcome: "All skills whitelabeled, cognitive-artifacts-builder created, handbooks aligned"
  context: "Current skills reference Claude; need SEA-Forge branding and CADSL integration"
  stakeholders:
    - name: "Architecture Team"
      role: "Owner"
    - name: "Documentation Team"
      role: "Contributor"
```

### Step 2: Define Stages

Break case into logical phases:

**Stage Types**:
- **Discretionary**: Can be skipped if not needed
- **Mandatory**: Must be completed
- **Repeatable**: Can occur multiple times

**Template**:
```yaml
stages:
  - id: "<stage-id>"
    name: "<Stage Name>"
    type: "discretionary|mandatory|repeatable"
    entryCriteria:  # Sentry conditions
      - "<condition>"
    exitCriteria:   # Milestones
      - "<achievement>"
```

**Example**:
```yaml
stages:
  - id: "analysis"
    name: "Current State Analysis"
    type: "mandatory"
    entryCriteria:
      - "Case activated"
    exitCriteria:
      - "All skills inventoried"
      - "Brand references identified"

  - id: "whitelabeling"
    name: "Whitelabeling"
    type: "mandatory"
    entryCriteria:
      - "Analysis complete"
    exitCriteria:
      - "5 skills whitelabeled"

  - id: "transformation"
    name: "Transformation"
    type: "mandatory"
    entryCriteria:
      - "Whitelabeling complete"
    exitCriteria:
      - "cognitive-artifacts-builder created"
      - "CADSL examples included"
```

### Step 3: Define Tasks

Tasks are the atomic units of work:

**Task Types**:
- **Human Task**: Requires human judgment
- **Process Task**: Can be automated
- **Case Task**: Nested sub-case

**Template**:
```yaml
tasks:
  - id: "<task-id>"
    name: "<Task name>"
    type: "human|process|case"
    stage: "<stage-id>"
    assignedTo: "<member-id>"
    isDiscretionary: true|false
    activationSentry:
      conditions:
        - "<condition>"
```

**Example**:
```yaml
tasks:
  - id: "task-001"
    name: "Inventory all skills"
    type: "process"
    stage: "analysis"
    assignedTo: "agent-specialist-analysis"
    isDiscretionary: false

  - id: "task-002"
    name: "Identify Claude references"
    type: "process"
    stage: "analysis"
    assignedTo: "agent-specialist-analysis"
    isDiscretionary: false
    activationSentry:
      conditions:
        - "task-001 completed"

  - id: "task-003"
    name: "Whitelabel web-artifacts-builder"
    type: "process"
    stage: "whitelabeling"
    assignedTo: "agent-specialist-refactor"
    isDiscretionary: false
    activationSentry:
      conditions:
        - "analysis stage complete"
```

### Step 4: Configure PM-Agent

PM-Agent manages case lifecycle:

**Configuration**:
```yaml
pmAgent:
  caseId: "case-2026-001"
  capabilities:
    - taskActivation: true
    - artifactTracking: true
    - sovereignGateEnforcement: true

  rules:
    # Activate discretionary tasks when conditions met
    - trigger: "sentry-fired"
      action: "activate-task"

    # Track artifact pipeline transitions
    - trigger: "artifact-created"
      action: "record-transition-token"

    # Require human approval for capital formation
    - trigger: "capitalization-flow"
      action: "request-sovereign-signature"
```

### Step 5: Track Artifacts

As work progresses, artifacts move through pipeline:

**Artifact Tracking**:
```yaml
artifacts:
  - id: "artifact-001"
    name: "Skills Analysis Report"
    stage: "IntellectualArtifact"  # Formal spec
    case: "case-2026-001"
    createdBy: "agent-specialist-analysis"
    provenance:
      - transition: "CognitiveArtifact → IntellectualArtifact"
        transitionToken: "token-001"
        timestamp: "2026-01-06T10:00:00Z"

  - id: "artifact-002"
    name: "cognitive-artifacts-builder Skill"
    stage: "InformationProduct"  # Executable work product
    case: "case-2026-001"
    createdBy: "agent-specialist-refactor"
    provenance:
      - transition: "IntellectualArtifact → InformationProduct"
        transitionToken: "token-002"
        timestamp: "2026-01-06T12:00:00Z"
```

---

## Common Case Patterns

### Research Case

**Stages**: Literature Review → Hypothesis Formation → Experiments → Analysis → Publication

**Key Sentries**:
- Activate experiments when 10+ papers reviewed
- Activate analysis when 3+ experiments complete
- Activate publication when findings validated

**Artifacts**:
- Literature notes (Cognitive) → Research design (Intellectual) → Paper draft (Product) → Published paper (Capital)

### Development Case (Spec-First)

**Stages**: Ideation → Specification → Implementation → Testing → Deployment

**Key Sentries**:
- Activate implementation when ADR + PRD + SDS approved
- Activate testing when code generation complete
- Activate deployment when all tests pass

**Artifacts**:
- Design notes (Cognitive) → ADR/PRD/SDS (Intellectual) → Generated code (Product) → Released feature (Capital)

### Consulting Case

**Stages**: Discovery → Analysis → Recommendations → Presentation → Handoff

**Key Sentries**:
- Activate analysis when 5+ stakeholder interviews complete
- Activate recommendations when analysis validated
- Activate presentation when recommendations approved

**Artifacts**:
- Interview notes (Cognitive) → Analysis doc (Intellectual) → Recommendation deck (Product) → Client asset (Capital)

---

## Integration Points

### Cognitive Artifacts (CADSL)

Cases can use cognitive artifacts (checklists, decision trees, kanban) for visualization:

```yaml
case:
  id: "case-2026-001"
  artifacts:
    - type: "Kanban"
      artifactId: "kanban-001"
      columns: ["Backlog", "In Progress", "Review", "Done"]

    - type: "Checklist"
      artifactId: "checklist-001"
      items: ["Whitelabel skills", "Create new skills", "Update handbooks"]
```

**Use cognitive-artifacts-builder skill** to generate these visualizations.

### Knowledge Graph (DomainForge™)

Link cases and artifacts to semantic concepts:

```yaml
case:
  semanticRefs:
    - conceptId: "sea:KnowledgeWork"
    - conceptId: "sea:DiscretionaryWorkflow"

artifacts:
  - id: "artifact-001"
    semanticRefs:
      - conceptId: "sea:Specification"
      - conceptId: "sea:IntellectualArtifact"
```

### Internal Federated Ledger (IFL)

Every case state transition creates immutable TransitionToken:

```yaml
transitionTokens:
  - id: "token-001"
    case: "case-2026-001"
    transition: "Created → Active"
    timestamp: "2026-01-06T09:00:00Z"
    ifl:hash: "sha256:abc123..."

  - id: "token-002"
    case: "case-2026-001"
    transition: "Stage[analysis] → Complete"
    timestamp: "2026-01-06T11:00:00Z"
    ifl:hash: "sha256:def456..."
```

**No Teleportation Policy**: Artifacts cannot skip stages. Every transition must have provenance token.

### Observability (OpenTelemetry)

Track case metrics:

```
cmmn_cases_active_total{type="research"}
cmmn_stages_completed_total{case_id="case-2026-001"}
cmmn_artifacts_reified_total{stage="IntellectualCapital"}
cmmn_sovereign_gates_triggered_total
```

---

## Governance Policies

### Single Agent Control

**Policy**: AI members must be managed exclusively by PM-Agent

**Enforcement**: Case members cannot self-assign tasks or activate stages

### No Teleportation

**Policy**: Artifacts must progress through pipeline in order

**Example Violation**:
```yaml
# ❌ VIOLATION: Skipping IntellectualArtifact stage
artifact:
  stage: "InformationProduct"
  provenance: []  # No IntellectualArtifact transition token
```

**Valid**:
```yaml
# ✅ VALID: Complete provenance chain
artifact:
  stage: "InformationProduct"
  provenance:
    - transition: "CognitiveArtifact → IntellectualArtifact"
      token: "token-001"
    - transition: "IntellectualArtifact → InformationProduct"
      token: "token-002"
```

### Sovereign Gate

**Policy**: High-impact capital conversions require human signature

**Trigger**: When artifact transitions to IntellectualCapital

**Action**: PM-Agent requests SignatureToken from human sovereign

---

## PM-Agent Configuration

### Role Assignment

PM-Agent assigns tasks based on capability matching:

```yaml
members:
  - id: "agent-specialist-analysis"
    type: "ai"
    capabilities: ["analysis", "research", "synthesis"]

  - id: "agent-specialist-refactor"
    type: "ai"
    capabilities: ["code-generation", "refactoring"]

  - id: "human-architect"
    type: "human"
    capabilities: ["architecture-decisions", "sovereign-approval"]

taskAssignment:
  rules:
    - taskType: "analysis"
      assignTo: "agent-specialist-analysis"

    - taskType: "refactoring"
      assignTo: "agent-specialist-refactor"

    - taskType: "sovereign-gate"
      assignTo: "human-architect"
```

### Sentry Evaluation

PM-Agent continuously evaluates sentries:

```yaml
sentries:
  - id: "activate-analysis"
    conditions:
      - "task-001.status == 'complete'"
      - "task-002.status == 'complete'"
    action:
      - "activate-stage('analysis')"
      - "notify-members(['agent-specialist-analysis'])"
```

---

## Examples by Domain

### Software Development

```yaml
case:
  title: "Implement CADSL Renderer"
  stages:
    - Ideation (brainstorm, spike)
    - Specification (ADR, SDS, SEA™)
    - Implementation (codegen)
    - Testing (unit, integration)
    - Deployment (CI/CD)
```

### Research Project

```yaml
case:
  title: "LLM as Idiolect Study"
  stages:
    - Literature Review
    - Hypothesis Formation
    - Experiment Design
    - Data Collection
    - Analysis
    - Publication
```

### Consulting Engagement

```yaml
case:
  title: "Digital Transformation Roadmap"
  stages:
    - Discovery (stakeholder interviews)
    - Current State Analysis
    - Future State Design
    - Recommendations
    - Presentation
```

---

## Quality Guidelines

### 1. Clear Desired Outcomes

❌ **Bad**: Vague or unachievable
```yaml
desiredOutcome: "Make things better"
```

✅ **Good**: Specific and measurable
```yaml
desiredOutcome: "All 17 skills whitelabeled with SEA-Forge branding; 3 new skills created; handbooks aligned with skills"
```

### 2. Proper Sentry Design

❌ **Bad**: Missing conditions
```yaml
sentry:
  action: "activate-stage('analysis')"
  # No conditions specified
```

✅ **Good**: Explicit conditions
```yaml
sentry:
  conditions:
    - "task-inventory.status == 'complete'"
    - "task-analysis.status == 'complete'"
  action: "activate-stage('whitelabeling')"
```

### 3. Complete Provenance

Always track artifact transitions:

```yaml
artifact:
  id: "spec-001"
  provenance:
    - stage: "CognitiveArtifact"
      timestamp: "2026-01-05T14:00:00Z"
      token: "token-001"
    - stage: "IntellectualArtifact"
      timestamp: "2026-01-06T10:00:00Z"
      token: "token-002"
```

---

## References

- [Case Management Handbook](../../../docs/handbooks/ProjectCase_Mgmt_Handbook/README.md)
- [SDS-012: Case Management Service](../../../docs/specs/cognitive-extension/sds/012-case-management-service.md)
- [CMMN Reference Guide](../../../docs/handbooks/ProjectCase_Mgmt_Handbook/Technical/cmmn_reference_guide.md)
- [Artifact Pipeline Management](../../../docs/handbooks/ProjectCase_Mgmt_Handbook/Technical/artifact_pipeline_management.md)
- [PM-Agent Orchestration](../../../docs/handbooks/ProjectCase_Mgmt_Handbook/Technical/pm_agent_orchestration.md)
