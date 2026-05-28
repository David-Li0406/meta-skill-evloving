---
name: cognitive-artifacts-builder
description: Build CADSL-based cognitive artifacts for SEA-Forge™ including checklists, planners, decision trees, kanban boards, and mind maps. Use for generating interactive, semantically-anchored artifacts that support knowledge work and collaborative decision-making. Aligns with Cognitive Architecture patterns and Knowledge Graph integration.
license: Complete terms in LICENSE.txt
---

# Cognitive Artifacts Builder

Generate CADSL (Cognitive Artifact DSL) artifacts for SEA-Forge™ to support knowledge work. CADSL artifacts are declarative, semantically-rich, and platform-agnostic definitions that can be rendered across multiple interfaces (web, mobile, voice).

**For reference:** [Cognitive Architecture Handbook](../../../docs/handbooks/Cognitive_Architecture_Handbook/README.md) | [CADSL Specification](../../../docs/specs/cognitive-extension/reference/001-cadsl-language-specification.md)

---

## When to Use This Skill

Use cognitive-artifacts-builder when:

1. **Organizing Knowledge**: User needs structured representation of complex information
2. **Supporting Decisions**: User is evaluating options or making strategic choices
3. **Tracking Work**: User needs to manage tasks, projects, or workflows
4. **Facilitating Collaboration**: Team needs shared artifact for alignment
5. **Visualizing Relationships**: User wants to see connections between concepts

---

## Artifact Type Catalog

### 1. Checklist

**Purpose**: Track completion of sequential or independent tasks

**Elements**: Heading, Checkbox, Label, ProgressBar

**Use Cases**:
- Pre-flight checklists before deployment
- Quality assurance verification
- Onboarding task lists
- Compliance requirements

**CADSL Example**:
\`\`\`yaml
artifactType: Checklist
metadata:
  title: "Production Deployment Checklist"
  semanticRefs:
    - conceptId: "sea:Deployment"
    - conceptId: "sea:QualityGate"
  provenance:
    generatedBy: "cognitive-artifacts-builder"
    timestamp: "2026-01-06T12:00:00Z"

sections:
  - id: "pre-deploy"
    heading: "Pre-Deployment"
    items:
      - id: "test-pass"
        checkbox: true
        completed: false
        label: "All tests passing"
      - id: "review-complete"
        checkbox: true
        completed: false
        label: "Code review approved"
\`\`\`

---

### 2. Decision Tree / Planner

**Purpose**: Guide users through conditional decision-making paths

**Elements**: Heading, Section, RadioButton, Button, Arrow, Conditional

**Use Cases**:
- Architecture decision records (ADR)
- Troubleshooting guides
- Policy routing (which team handles this?)
- Feature selection wizards

---

### 3. Kanban Board

**Purpose**: Visualize workflow states and move items through stages

**Elements**: Panel, Section, DragAndDropArea, Card, Badge, ProgressIndicator

**Use Cases**:
- Sprint planning
- Case management (CMMN artifact pipeline)
- Content workflow (draft → review → published)
- Support ticket triage

---

### 4. Mind Map / Concept Map

**Purpose**: Visualize hierarchical or networked relationships between concepts

**Elements**: Canvas, Node (circle/box), Line, Arrow, Label, Grouping

**Use Cases**:
- Brainstorming sessions
- System architecture overview
- Knowledge Graph visualization
- Dependency mapping

---

### 5. Timeline / Roadmap

**Purpose**: Chronological representation of events, milestones, or plans

**Elements**: Timeline, Calendar, Schedule, ProgressBar, Badge

**Use Cases**:
- Project roadmaps
- Release planning
- Historical event tracking
- Compliance deadline tracking

---

## Workflow: Generating CADSL Artifacts

### Step 1: Analyze Context

Extract from user conversation:
- **Task/Goal**: What is the user trying to accomplish?
- **Information Structure**: Linear? Hierarchical? Networked? Temporal?
- **Interaction Needs**: View-only? Editable? Collaborative?
- **Semantic Context**: Related concepts from Knowledge Graph

### Step 2: Recommend Artifact Type

Based on analysis, suggest most appropriate artifact type:

| User Need | Recommended Artifact |
|-----------|---------------------|
| Track completion of tasks | Checklist |
| Choose between options | Decision Tree / Planner |
| Manage workflow stages | Kanban Board |
| Explore concept relationships | Mind Map |
| Plan over time | Timeline / Roadmap |

**Explicitly ask**: "Would a [ARTIFACT_TYPE] help with [TASK]? Here's what it would include..."

### Step 3: Generate CADSL Definition

Create YAML artifact following specification:

**Required metadata**:
\`\`\`yaml
metadata:
  title: "<descriptive title>"
  semanticRefs:
    - conceptId: "<sea:ConceptId>"  # Link to Knowledge Graph
  provenance:
    generatedBy: "cognitive-artifacts-builder"
    timestamp: "<ISO-8601>"
\`\`\`

**Semantic Anchoring**:
- Every artifact MUST include \`semanticRefs\` linking to Knowledge Graph concepts
- Use \`conceptId\` format: \`sea:<ConceptName>\` or \`<context>:<ConceptName>\`
- Enables discoverability, traceability, and semantic reasoning

### Step 4: Present Artifact

1. **Show CADSL definition** in code block
2. **Explain structure**: Walk through sections and key elements
3. **Highlight semantic links**: Point out Knowledge Graph connections
4. **Suggest interactions**: "You can edit...", "I can update...", "This links to..."

### Step 5: Iterate

Support refinement:
- "Add a new column to the kanban board"
- "Change this checklist item priority to critical"
- "Link this decision tree node to ADR-034"

**Use precise updates**: Modify specific sections of YAML rather than regenerating entire artifact.

---

## Integration Points

### Knowledge Graph (DomainForge™)

**Purpose**: Semantic anchoring and concept resolution

**Pattern**:
\`\`\`yaml
semanticRefs:
  - conceptId: "sea:BoundedContext"
    uri: "http://sea-forge.org/ontology#BoundedContext"
\`\`\`

**Query Knowledge Graph** to:
- Validate \`conceptId\` exists
- Retrieve related concepts for suggestions
- Check SHACL constraints on artifact structure

### Case Management (CMMN)

**Purpose**: Artifacts as first-class case items

**Pattern**:
\`\`\`yaml
metadata:
  caseId: "case-2026-001"
  stage: "planning"  # CMMN stage
\`\`\`

**Integration**:
- Artifacts move through CMMN artifact pipeline stages
- PM-Agent can trigger artifact generation
- Artifact state changes emit events to NATS

### Observability (OpenTelemetry)

**Purpose**: Track artifact usage and effectiveness

**Telemetry**:
- Artifact generation events
- User interactions (edits, completions)
- Semantic reference lookups

---

## Quality Guidelines

### 1. Semantic Richness

❌ **Bad**: Generic labels without context
\`\`\`yaml
heading: "Items"
items:
  - label: "Task 1"
\`\`\`

✅ **Good**: Descriptive, semantically linked
\`\`\`yaml
heading: "Pre-Deployment Quality Gates"
semanticRefs:
  - conceptId: "sea:QualityGate"
items:
  - label: "All tests passing (CI/CD)"
    semanticRefs:
      - conceptId: "sea:ContinuousIntegration"
\`\`\`

### 2. Provenance Tracking

Always include:
- \`generatedBy\`: Tool/agent that created artifact
- \`timestamp\`: When artifact was created
- \`sourceDoc\`: Optional reference to originating specification

### 3. Actionability

Artifacts should enable action, not just display:
- Buttons with \`command\` or \`link\` properties
- Interactive elements (checkboxes, drag-and-drop)
- Clear next steps

---

## References

- [Cognitive Architecture Handbook](../../../docs/handbooks/Cognitive_Architecture_Handbook/README.md)
- [CADSL Language Specification](../../../docs/specs/cognitive-extension/reference/001-cadsl-language-specification.md)
- [SDS-005: Artifact Engine Service](../../../docs/specs/cognitive-extension/sds/005-artifact-engine-service.md)
- [Case Management Handbook](../../../docs/handbooks/ProjectCase_Mgmt_Handbook/README.md)
