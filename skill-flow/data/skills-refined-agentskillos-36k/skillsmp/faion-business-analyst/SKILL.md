---
name: faion-business-analyst
user-invocable: false
description: "BA Domain Skill: Business Analysis Framework orchestrator. 6 Knowledge Areas (Planning, Elicitation, Analysis, Traceability, Evaluation, Management), requirements engineering, stakeholder analysis, process modeling, use cases, user stories. 24 methodologies."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(ls:*), Task, AskUserQuestion, TodoWrite
---

# BA Domain Skill

## Agents

| Agent | When to Use |
|-------|-------------|
| `faion-ba-agent` | Execute Business Analysis Framework methodologies for business analysis |

**Communication: User's language. Docs/code: English.**

---

## Purpose

Orchestrates business analysis activities following Business Analysis Framework standards. Core focus: understanding stakeholder needs and translating them into actionable requirements.

**Philosophy:** "Requirements are the foundation of successful solutions"

---

## 3-Layer Architecture

```
Layer 1: Domain Skills (this) → orchestrators
    ↓ call
Layer 2: Agents (faion-ba-agent) → executors
    ↓ use
Layer 3: Technical Skills → tools
```

---

## Decision Trees

### Main Decision Tree: What BA Task?

```
START: What is your BA task?
    │
    ├─► Planning/Setup?
    │   └─► Knowledge Area 1: BA Planning and Monitoring
    │       ├─► Need BA approach? → ba-planning
    │       ├─► Need stakeholder map? → stakeholder-analysis
    │       └─► Need governance? → references/methodologies-detail.md#governance
    │
    ├─► Gathering Information?
    │   └─► Knowledge Area 2: Elicitation and Collaboration
    │       ├─► Preparing for elicitation? → elicitation-techniques (preparation)
    │       ├─► Conducting sessions? → elicitation-techniques
    │       └─► Communication planning? → references/methodologies-detail.md#communication
    │
    ├─► Managing Requirements?
    │   └─► Knowledge Area 3: Requirements Lifecycle Management
    │       ├─► Tracking relationships? → requirements-traceability
    │       ├─► Maintaining/versioning? → requirements-lifecycle
    │       ├─► Prioritizing? → requirements-prioritization
    │       └─► Assessing changes? → references/methodologies-detail.md#change-impact
    │
    ├─► Strategic Planning?
    │   └─► Knowledge Area 4: Strategy Analysis
    │       ├─► Current state analysis? → strategy-analysis
    │       ├─► Future state definition? → strategy-analysis
    │       ├─► Risk analysis? → references/methodologies-detail.md#risk-analysis
    │       └─► Change strategy? → references/methodologies-detail.md#change-strategy
    │
    ├─► Requirements Analysis?
    │   └─► Knowledge Area 5: Requirements Analysis and Design
    │       ├─► Modeling requirements? → use-case-modeling OR user-story-mapping
    │       ├─► Data requirements? → data-analysis
    │       ├─► Process requirements? → business-process-analysis
    │       ├─► Interface requirements? → interface-analysis
    │       ├─► Business rules? → decision-analysis
    │       ├─► Validation? → requirements-validation
    │       └─► Acceptance criteria? → acceptance-criteria
    │
    └─► Solution Evaluation?
        └─► Knowledge Area 6: Solution Evaluation
            ├─► Assessing solution? → solution-assessment
            └─► Recommending improvements? → solution-assessment
```

### Requirements Modeling Decision Tree

```
What type of requirements?
    │
    ├─► Functional (user interactions)?
    │   ├─► Detailed flows needed? → use-case-modeling
    │   ├─► Agile/iterative? → user-story-mapping
    │   └─► Both? Start with user stories, detail with use cases
    │
    ├─► Data requirements?
    │   └─► data-analysis (ERD, data dictionary)
    │
    ├─► Process/workflow?
    │   └─► business-process-analysis (BPMN)
    │
    ├─► Business rules/decisions?
    │   └─► decision-analysis (decision tables/trees)
    │
    ├─► Interface/integration?
    │   └─► interface-analysis
    │
    └─► Non-functional?
        └─► requirements-documentation (NFR section)
```

### Elicitation Technique Selection

```
What information needed?
    │
    ├─► Deep understanding from individuals
    │   └─► Interviews (structured/semi-structured)
    │
    ├─► Consensus/group decisions
    │   └─► Workshops (facilitated)
    │
    ├─► Broad input from many
    │   └─► Surveys/Questionnaires
    │
    ├─► Process understanding
    │   └─► Observation (active/passive)
    │
    ├─► Existing state/documentation
    │   └─► Document Analysis
    │
    ├─► UI/UX validation
    │   └─► Prototyping
    │
    └─► Idea generation
        └─► Brainstorming
```

### Prioritization Technique Selection

```
What context?
    │
    ├─► Quick initial triage
    │   └─► MoSCoW (Must/Should/Could/Won't)
    │
    ├─► Product backlog scoring
    │   └─► RICE (Reach, Impact, Confidence, Effort)
    │
    ├─► Sprint planning
    │   └─► Value vs Effort Matrix
    │
    ├─► Customer satisfaction focus
    │   └─► Kano Model (Basic/Performance/Delighters)
    │
    └─► Complex multi-criteria
        └─► Weighted Scoring
```

---

## 6 Knowledge Areas (Overview)

### KA-1: Business Analysis Planning and Monitoring

**Purpose:** Define approach, identify stakeholders, plan governance.

| Task | Description | Key Output |
|------|-------------|------------|
| Plan BA Approach | Define how BA will be performed | BA approach document |
| Plan Stakeholder Engagement | Identify and plan work with stakeholders | Stakeholder engagement approach |
| Plan Governance | Define decision-making for requirements | Governance approach |
| Plan Information Management | Define how BA info stored/accessed | Information management approach |
| Identify Improvements | Assess BA performance, recommend improvements | BA performance improvements |

**Methodologies:** ba-planning, stakeholder-analysis

---

### KA-2: Elicitation and Collaboration

**Purpose:** Obtain information from stakeholders and confirm results.

| Task | Description | Key Output |
|------|-------------|------------|
| Prepare for Elicitation | Understand scope, select techniques | Elicitation activity plan |
| Conduct Elicitation | Draw out relevant information | Elicitation results (unconfirmed) |
| Confirm Results | Verify understanding with stakeholders | Elicitation results (confirmed) |
| Communicate BA Info | Ensure shared understanding | BA communication |
| Manage Collaboration | Encourage stakeholders to work together | Updated stakeholder engagement |

**Methodologies:** elicitation-techniques

---

### KA-3: Requirements Lifecycle Management

**Purpose:** Manage and maintain requirements throughout solution lifecycle.

| Task | Description | Key Output |
|------|-------------|------------|
| Trace Requirements | Ensure alignment at different levels | Requirements (traced) |
| Maintain Requirements | Keep accurate and consistent | Requirements (maintained) |
| Prioritize Requirements | Rank by importance | Requirements (prioritized) |
| Assess Changes | Evaluate proposed changes | Change assessment |
| Approve Requirements | Obtain agreement and approval | Requirements (approved) |

**Methodologies:** requirements-traceability, requirements-lifecycle, requirements-prioritization

---

### KA-4: Strategy Analysis

**Purpose:** Define future state needed to address business needs.

| Task | Description | Key Output |
|------|-------------|------------|
| Analyze Current State | Understand existing environment | Current state description |
| Define Future State | Define goals and objectives | Future state description |
| Assess Risks | Identify uncertainties and impacts | Risk assessment results |
| Define Change Strategy | Develop approach to achieve future state | Change strategy |

**Methodologies:** strategy-analysis

---

### KA-5: Requirements Analysis and Design Definition

**Purpose:** Structure, specify, model, verify, and validate requirements.

| Task | Description | Key Output |
|------|-------------|------------|
| Specify/Model Requirements | Analyze and refine into requirements | Requirements (specified/modeled) |
| Verify Requirements | Ensure quality standards met | Requirements (verified) |
| Validate Requirements | Ensure alignment with business goals | Requirements (validated) |
| Define Architecture | Ensure requirements support each other | Requirements architecture |
| Define Design Options | Define solution approaches | Design options |
| Analyze Value/Recommend | Assess options, recommend solution | Solution recommendation |

**Methodologies:** use-case-modeling, user-story-mapping, data-analysis, business-process-analysis, decision-analysis, interface-analysis, requirements-validation, acceptance-criteria, requirements-documentation

---

### KA-6: Solution Evaluation

**Purpose:** Assess solution performance and value delivered.

| Task | Description | Key Output |
|------|-------------|------------|
| Measure Performance | Define how performance measured | Solution performance measures |
| Analyze Measures | Examine data against expected value | Performance analysis |
| Assess Solution Limitations | Investigate problems and causes | Solution limitations |
| Assess Enterprise Limitations | Investigate enterprise factor impacts | Enterprise limitations |
| Recommend Actions | Identify actions to increase value | Value improvement recommendations |

**Methodologies:** solution-assessment

---

## Methodology Summary Table

| # | Methodology | Knowledge Area | When to Use | File |
|---|-------------|----------------|-------------|------|
| 1 | BA Planning | KA-1 Planning | Define BA approach and deliverables | [ba-planning](references/ba-planning.md) |
| 2 | Stakeholder Analysis | KA-1 Planning | Identify and analyze stakeholders | [stakeholder-analysis](references/stakeholder-analysis.md) |
| 3 | Elicitation Techniques | KA-2 Elicitation | Gather requirements from stakeholders | [elicitation-techniques](references/elicitation-techniques.md) |
| 4 | Requirements Documentation | KA-5 Analysis | Document requirements formally | [requirements-documentation](references/requirements-documentation.md) |
| 5 | Requirements Traceability | KA-3 Lifecycle | Track requirement relationships | [requirements-traceability](references/requirements-traceability.md) |
| 6 | Strategy Analysis | KA-4 Strategy | Analyze current/future state | [strategy-analysis](references/strategy-analysis.md) |
| 7 | Requirements Lifecycle | KA-3 Lifecycle | Manage requirements over time | [requirements-lifecycle](references/requirements-lifecycle.md) |
| 8 | Solution Assessment | KA-6 Evaluation | Evaluate solution performance | [solution-assessment](references/solution-assessment.md) |
| 9 | Business Process Analysis | KA-5 Analysis | Model and analyze processes | [business-process-analysis](references/business-process-analysis.md) |
| 10 | Data Analysis | KA-5 Analysis | Analyze data requirements | [data-analysis](references/data-analysis.md) |
| 11 | Decision Analysis | KA-5 Analysis | Model business rules/decisions | [decision-analysis](references/decision-analysis.md) |
| 12 | Use Case Modeling | KA-5 Analysis | Model user-system interactions | [use-case-modeling](references/use-case-modeling.md) |
| 13 | User Story Mapping | KA-5 Analysis | Agile requirements as user stories | [user-story-mapping](references/user-story-mapping.md) |
| 14 | Acceptance Criteria | KA-5 Analysis | Define done criteria (Given-When-Then) | [acceptance-criteria](references/acceptance-criteria.md) |
| 15 | Requirements Validation | KA-5 Analysis | Validate against business goals | [requirements-validation](references/requirements-validation.md) |
| 16 | Requirements Prioritization | KA-3 Lifecycle | Rank requirements (MoSCoW, RICE) | [requirements-prioritization](references/requirements-prioritization.md) |
| 17 | Interface Analysis | KA-5 Analysis | Analyze system interfaces | [interface-analysis](references/interface-analysis.md) |
| 18 | Knowledge Areas Overview | Framework | BA Framework knowledge areas summary | [knowledge-areas-overview](references/knowledge-areas-overview.md) |

---

## Modern BA Practices (2025-2026)

| Topic | File | Key Focus |
|-------|------|-----------|
| AI-Enabled BA | [ai-enabled-business-analysis](references/ai-enabled-business-analysis.md) | GenAI, agentic AI, AI requirements |
| Agile BA Frameworks | [agile-ba-frameworks](references/agile-ba-frameworks.md) | Scrum, scaled agile, Agile Analysis Certification |
| Process Mining | [process-mining-automation](references/process-mining-automation.md) | RPA, automation assessment |
| Data-Driven Requirements | [data-driven-requirements](references/data-driven-requirements.md) | Analytics-informed prioritization |
| Modern BA Framework | [modern-ba-framework](references/modern-ba-framework.md) | BA Framework 2025-2026 updates |
| BA Strategic Partnership | [ba-strategic-partnership](references/ba-strategic-partnership.md) | Innovation leadership |

---

## BA Framework Techniques Quick Reference

| Category | Techniques |
|----------|------------|
| **Elicitation** | Interviews, Workshops, Observation, Document Analysis, Surveys, Prototyping, Brainstorming, Focus Groups |
| **Analysis** | Data Modeling, Process Modeling, Use Cases, User Stories, Decision Tables, Business Rules, SWOT |
| **Strategy** | Business Model Canvas, Balanced Scorecard, SWOT, Capability Analysis, Gap Analysis |
| **Prioritization** | MoSCoW, RICE, Kano Model, Value vs Effort, Weighted Scoring |
| **Validation** | Reviews, Walkthroughs, Acceptance Criteria, Prototyping |
| **Management** | Traceability Matrix, Version Control, Change Control, Item Tracking |

---

## Embedded Framework Reference

Detailed embedded methodology content (templates, examples, step-by-step guides) is available in:
- [methodologies-detail.md](references/methodologies-detail.md) - Governance, communication, risk, change impact

---

## Underlying Competencies

| Category | Competencies |
|----------|--------------|
| **Analytical** | Creative thinking, decision making, systems thinking, problem solving |
| **Behavioral** | Ethics, accountability, trustworthiness, adaptability |
| **Business** | Business acumen, industry knowledge, organization knowledge |
| **Communication** | Verbal, written, listening, non-verbal |
| **Interaction** | Facilitation, leadership, teamwork, negotiation |

---

## Directory Structure

```
~/.claude/skills/faion-business-analyst/
├── SKILL.md                          # Main skill file
├── CLAUDE.md                         # Navigation
├── ref-CLAUDE.md                     # References overview
├── ba-planning.md
├── stakeholder-analysis.md
├── elicitation-techniques.md
├── requirements-documentation.md
├── requirements-traceability.md
├── strategy-analysis.md
├── requirements-lifecycle.md
├── solution-assessment.md
├── business-process-analysis.md
├── data-analysis.md
├── decision-analysis.md
├── use-case-modeling.md
├── user-story-mapping.md
├── acceptance-criteria.md
├── requirements-validation.md
├── requirements-prioritization.md
├── interface-analysis.md
├── knowledge-areas-overview.md
├── methodologies-detail.md           # Embedded templates
├── ai-enabled-business-analysis.md
├── agile-ba-frameworks.md
├── process-mining-automation.md
├── data-driven-requirements.md
├── modern-ba-framework.md
├── ba-strategic-partnership.md
└── ba-trends-summary.md
```

---

*BA Domain Skill v2.0*
*Based on Business Analysis Framework (Guide to Business Analysis Body of Knowledge)*
*24 Methodologies | 6 Knowledge Areas | Decision Trees*
