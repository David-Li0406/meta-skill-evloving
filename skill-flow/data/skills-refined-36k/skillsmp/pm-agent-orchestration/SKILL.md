---
name: pm-agent-orchestration
description: Orchestrate PM-Agent workflows for case management, task delegation, and artifact pipeline coordination. Use when managing multi-step projects, delegating tasks to sub-agents, or tracking work through CMMN stages.
license: Complete terms in LICENSE.txt
---

# PM-Agent Orchestration

Coordinate project work through PM-Agent - the SEA-Forge™ orchestration layer for case management, task delegation, and artifact pipelines.

**For reference:** [Project/Case Management Handbook](../../../docs/handbooks/ProjectCase_Mgmt_Handbook/README.md) | [Case Management Skill](../case-management/SKILL.md)

---

## When to Use This Skill

Use pm-agent-orchestration when:

1. **Managing Complex Projects**: Work spanning multiple phases, teams, or dependencies
2. **Delegating to Sub-Agents**: Breaking work into tasks for specialized agents
3. **Tracking Artifact Pipelines**: Moving artifacts through CMMN stages
4. **Coordinating Handoffs**: Ensuring smooth transitions between stages
5. **Reporting Progress**: Generating status updates across cases

---

## PM-Agent Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        PM-Agent                              │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────────┐  │
│  │ Case Manager │  │ Task Router  │  │ Artifact Pipeline  │  │
│  └─────────────┘  └──────────────┘  └────────────────────┘  │
│          │                │                    │             │
│          ▼                ▼                    ▼             │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────────┐  │
│  │   NATS Bus   │◄─┤ Sub-Agents   │  │ Knowledge Graph    │  │
│  └─────────────┘  └──────────────┘  └────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## Core Workflows

### 1. Case Creation

Create a new case for a project or initiative:

```yaml
command: pm.case.create
payload:
  title: "SEA-Forge Skills Optimization"
  description: "Optimize skills, handbooks, and documentation"
  desiredOutcome: "All skills whitelabeled, new artifacts added, docs aligned"
  timeline:
    startDate: "2026-01-06"
    targetDate: "2026-01-20"
  semanticRefs:
    - conceptId: "sea:SkillDefinition"
    - conceptId: "sea:Documentation"
```

**Response:**
```yaml
caseId: "case-2026-001"
status: "created"
stage: "intake"
```

### 2. Task Breakdown

Break a case into delegatable tasks:

```yaml
command: pm.task.plan
payload:
  caseId: "case-2026-001"
  breakdown:
    strategy: "vertical-slice"  # or "horizontal", "milestone"
    maxParallelism: 3
```

**Generated Tasks:**
```yaml
tasks:
  - id: "task-001"
    name: "Whitelabel docx skill"
    stage: "execution"
    agent: "code-agent"
    dependencies: []
    
  - id: "task-002"
    name: "Add Notebook artifact type"
    stage: "execution"
    agent: "code-agent"
    dependencies: []
    
  - id: "task-003"
    name: "Create semantic-anchoring skill"
    stage: "execution"
    agent: "code-agent"
    dependencies: ["task-001", "task-002"]
```

### 3. Task Delegation

Delegate tasks to specialized sub-agents:

```yaml
command: pm.task.delegate
payload:
  taskId: "task-001"
  agent: "code-agent"
  context:
    files:
      - ".github/skills/docx/SKILL.md"
      - ".github/skills/docx/scripts/document.py"
    instructions: "Replace Claude references with SEA-Forge Agent"
    successCriteria:
      - "No Claude references remain"
      - "All tests pass"
```

**Agent Types:**
| Agent | Specialization |
|-------|----------------|
| `code-agent` | Code generation, refactoring |
| `review-agent` | Code review, PR analysis |
| `test-agent` | Test generation, verification |
| `doc-agent` | Documentation, handbooks |
| `research-agent` | Codebase exploration, analysis |

### 4. Progress Tracking

Monitor case and task progress:

```yaml
command: pm.case.status
payload:
  caseId: "case-2026-001"
```

**Response:**
```yaml
case:
  id: "case-2026-001"
  stage: "execution"
  progress:
    completed: 5
    inProgress: 2
    pending: 3
    total: 10
    percentage: 50
  timeline:
    onTrack: true
    estimatedCompletion: "2026-01-18"
  blockers: []
  recentActivity:
    - "task-001 completed: docx skill whitelabeled"
    - "task-002 completed: Notebook artifact added"
```

### 5. Artifact Pipeline

Move artifacts through CMMN stages:

```yaml
command: pm.artifact.advance
payload:
  artifactId: "artifact-2026-001"
  fromStage: "draft"
  toStage: "review"
  reviewer: "human"  # or "agent", "automated"
```

**Artifact Stages:**
```
draft → review → approved → published → archived
          ↓
       rejected → draft (revision)
```

---

## Event Integration (NATS)

PM-Agent publishes events for observability:

```yaml
# Case created
subject: "sea.pm.case.created"
payload:
  caseId: "case-2026-001"
  timestamp: "2026-01-06T12:00:00Z"

# Task completed
subject: "sea.pm.task.completed"
payload:
  taskId: "task-001"
  caseId: "case-2026-001"
  duration: "PT2H30M"
  result: "success"

# Stage transition
subject: "sea.pm.artifact.stage.changed"
payload:
  artifactId: "artifact-2026-001"
  from: "draft"
  to: "review"
```

---

## Delegation Patterns

### Sequential Execution

Tasks run one after another:

```yaml
execution:
  strategy: "sequential"
  tasks:
    - "task-001"  # Runs first
    - "task-002"  # Runs after task-001
    - "task-003"  # Runs after task-002
```

### Parallel Execution

Independent tasks run concurrently:

```yaml
execution:
  strategy: "parallel"
  maxConcurrency: 3
  tasks:
    - "task-001"  # All run
    - "task-002"  # simultaneously
    - "task-003"  # up to max
```

### DAG Execution

Tasks with dependencies:

```yaml
execution:
  strategy: "dag"
  tasks:
    - id: "task-001"
      dependencies: []
    - id: "task-002"
      dependencies: []
    - id: "task-003"
      dependencies: ["task-001", "task-002"]  # Waits for both
```

---

## Quality Guidelines

### 1. Clear Success Criteria

Every task must have measurable success criteria:

```yaml
successCriteria:
  - metric: "tests_passing"
    threshold: 100
    unit: "percent"
  - metric: "lint_errors"
    threshold: 0
    unit: "count"
```

### 2. Context Minimization

Provide only relevant context to sub-agents:

```yaml
# ❌ Too much context
context:
  files: ["**/*"]  # Entire repo

# ✅ Focused context
context:
  files:
    - ".github/skills/docx/SKILL.md"
    - ".github/skills/docx/scripts/document.py"
```

### 3. Atomic Tasks

Break work into atomic, verifiable units:

```yaml
# ❌ Too broad
tasks:
  - name: "Optimize all skills"

# ✅ Atomic
tasks:
  - name: "Whitelabel docx skill"
  - name: "Whitelabel skill-creator skill"
  - name: "Add Notebook artifact type"
```

---

## References

- [Project/Case Management Handbook](../../../docs/handbooks/ProjectCase_Mgmt_Handbook/README.md)
- [Case Management Skill](../case-management/SKILL.md)
- [SDS-010: PM-Agent Service](../../../docs/specs/orchestration/sds/010-pm-agent-service.md)
- [NATS Integration Handbook](../../../docs/handbooks/GenAIOps_Handbook/observability/README.md)
