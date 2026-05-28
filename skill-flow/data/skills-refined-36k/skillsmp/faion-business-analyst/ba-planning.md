---
id: ba-planning
name: "Business Analysis Planning"
domain: BA
skill: faion-business-analyst
category: "business-analysis"
---

# Business Analysis Planning

## Metadata
- **Category:** BA Framework / Business Analysis Planning and Monitoring
- **Difficulty:** Beginner
- **Tags:** #methodology #babok #planning #business-analysis
- **Agent:** faion-ba-agent

---

## Problem

Business analysis happens ad-hoc without structure. Requirements are gathered inconsistently. Stakeholders do not know when they will be involved. BA activities take longer than necessary or miss important areas. There is no clear approach to how analysis will be conducted.

Without BA planning:
- Inconsistent analysis approach
- Missed stakeholders
- Uncoordinated activities
- Unclear deliverables

---

## Framework

### What is BA Planning?

BA Planning defines how business analysis work will be performed, including:
- Approach and methodology
- Stakeholders to involve
- Activities and timing
- Deliverables to produce

### Step 1: Understand the Context

Before planning, understand:

| Question | Purpose |
|----------|---------|
| What is the initiative? | Scope of BA effort |
| What type of change? | New system, process, strategy |
| What is the organization culture? | Formal vs. informal |
| What constraints exist? | Time, budget, resources |

### Step 2: Select the Approach

Choose analysis approach based on context:

| Approach | When to Use | Characteristics |
|----------|-------------|-----------------|
| **Plan-Driven** | Clear scope, stable requirements | Upfront planning, sequential |
| **Change-Driven** | Uncertain, evolving requirements | Iterative, adaptive |
| **Hybrid** | Mix of characteristics | Combine approaches |

### Step 3: Identify Stakeholders

List all parties involved in or affected by the change:

| Category | Examples |
|----------|----------|
| **Sponsors** | Executive funding the initiative |
| **Users** | People who will use the solution |
| **Implementers** | Team building the solution |
| **Regulators** | Compliance bodies |
| **Support** | Operations, help desk |

### Step 4: Plan Elicitation Activities

Define how requirements will be gathered:

| Technique | When to Use | Stakeholders |
|-----------|-------------|--------------|
| Interviews | Deep understanding | Individuals |
| Workshops | Consensus building | Groups |
| Surveys | Broad input | Many stakeholders |
| Observation | Process understanding | Users |
| Document Analysis | Existing state | Documents |

### Step 5: Define BA Deliverables

Specify what will be produced:

| Deliverable | Purpose | When |
|-------------|---------|------|
| Stakeholder List | Identify parties | Early |
| Requirements Document | Capture needs | Throughout |
| Process Models | Visualize flows | As needed |
| Decision Log | Track decisions | Ongoing |

### Step 6: Establish Governance

Define how BA work will be managed:

- Who approves requirements
- How changes are handled
- Review and sign-off process
- Escalation path

---

## Templates

### BA Approach Document

```markdown
# Business Analysis Approach: [Initiative Name]

**Version:** [X.X]
**Date:** [Date]
**Business Analyst:** [Name]

## 1. Initiative Overview
[Brief description of the change initiative]

## 2. Analysis Approach

**Selected Approach:** [Plan-Driven / Change-Driven / Hybrid]
**Rationale:** [Why this approach]

## 3. Stakeholders

| Name/Role | Category | Involvement | Availability |
|-----------|----------|-------------|--------------|
| [Name] | [Category] | [How involved] | [When available] |

## 4. Elicitation Plan

| Activity | Technique | Participants | Timing |
|----------|-----------|--------------|--------|
| [Activity] | [Technique] | [Who] | [When] |

## 5. Deliverables

| Deliverable | Description | Target Date |
|-------------|-------------|-------------|
| [Deliverable] | [Description] | [Date] |

## 6. Governance

**Requirements Approval:** [Who approves]
**Change Process:** [How changes handled]
**Review Cadence:** [Frequency]

## 7. Risks and Constraints

| Risk/Constraint | Impact | Mitigation |
|-----------------|--------|------------|
| [Item] | [Impact] | [Action] |

## 8. Timeline

| Phase | Activities | Duration |
|-------|------------|----------|
| [Phase] | [Activities] | [Duration] |
```

### BA Activity Plan

```markdown
# BA Activity Plan: [Initiative Name]

**Week of:** [Date]
**Business Analyst:** [Name]

## Planned Activities

| Day | Activity | Stakeholders | Duration | Deliverable |
|-----|----------|--------------|----------|-------------|
| Mon | [Activity] | [Who] | [Time] | [Output] |
| Tue | [Activity] | [Who] | [Time] | [Output] |
| Wed | [Activity] | [Who] | [Time] | [Output] |

## Dependencies
- [Dependency 1]
- [Dependency 2]

## Blockers/Risks
- [Issue 1]
- [Issue 2]
```

---

## Examples

### Example 1: Agile BA Planning

**Context:** New mobile app, uncertain requirements

**Approach:** Change-Driven

**Elicitation Plan:**
- Sprint 0: User interviews (10), competitor analysis
- Each sprint: Backlog refinement, user story mapping
- Ongoing: Prototype testing, feedback sessions

**Deliverables:**
- Product backlog (living document)
- User personas (Sprint 0)
- Acceptance criteria (each sprint)

### Example 2: Waterfall BA Planning

**Context:** ERP implementation, well-defined scope

**Approach:** Plan-Driven

**Phases:**
1. Discovery (4 weeks): Current state analysis
2. Requirements (6 weeks): Detailed requirements
3. Design Review (2 weeks): Validate with stakeholders
4. Support (ongoing): Clarification during build

**Deliverables:**
- Business Requirements Document
- Process Flow Diagrams
- Data Dictionary
- Traceability Matrix

---

## Common Mistakes

1. **No approach defined** - Ad-hoc analysis
2. **Missing stakeholders** - Key voices not heard
3. **Too detailed too early** - Planning without context
4. **No governance** - Unclear approval process
5. **Static plan** - Never updating as situation changes

---

## Planning Considerations

| Factor | Plan-Driven | Change-Driven |
|--------|-------------|---------------|
| Requirements clarity | High | Low |
| Stakeholder availability | Limited, scheduled | Continuous |
| Risk tolerance | Low | Higher |
| Documentation | Extensive | Just enough |
| Change frequency | Low | High |

---

## Next Steps

After BA planning:
1. Communicate plan to stakeholders
2. Schedule initial elicitation sessions
3. Set up deliverable templates
4. Begin stakeholder engagement
5. Connect to Stakeholder Analysis methodology

---

## References

- BA Framework Guide v3 - Business Analysis Planning and Monitoring
- BA industry Standards
