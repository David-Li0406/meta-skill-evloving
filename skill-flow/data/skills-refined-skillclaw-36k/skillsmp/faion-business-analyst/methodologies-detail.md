---
id: methodologies-detail
name: "BA Methodologies - Detailed Reference"
domain: BA
skill: faion-business-analyst
category: "business-analysis"
---

# BA Methodologies - Detailed Reference

This file contains detailed methodology content extracted from the original SKILL.md. Includes templates, step-by-step guides, and examples for methodologies not covered in individual reference files.

---

## Table of Contents

1. [Governance Framework](#governance)
2. [Communication Planning](#communication)
3. [Elicitation Preparation](#elicitation-preparation)
4. [Requirements Maintenance](#requirements-maintenance)
5. [Change Impact Analysis](#change-impact)
6. [Current State Analysis](#current-state-analysis)
7. [Future State Definition](#future-state-definition)
8. [Risk Analysis](#risk-analysis)
9. [Change Strategy Planning](#change-strategy)
10. [Requirements Architecture](#requirements-architecture)
11. [Solution Options Analysis](#solution-options-analysis)
12. [Solution Limitation Assessment](#solution-limitation-assessment)

---

<a name="governance"></a>
## 1. Governance Framework

### Problem
How to establish decision-making processes for requirements?

### Framework

1. **Define Decision Rights**
   - Who can approve requirements?
   - Escalation paths
   - Consensus vs authority

2. **Establish Change Control**
   - Change request process
   - Impact assessment requirements
   - Approval thresholds

3. **Set Prioritization Rules**
   - Criteria for prioritization
   - Weighting factors
   - Tie-breaking rules

4. **Document Approval Process**
   - Sign-off requirements
   - Documentation standards
   - Audit trail

### Template

```markdown
## Governance Framework

### Decision Authority Matrix
| Decision Type | Authority Level | Escalation |
|---------------|-----------------|------------|
| New requirement | BA Lead | PM |
| Scope change | Steering Committee | Sponsor |
| Priority change | Product Owner | PM |

### Change Control Process
1. Submit change request
2. Impact assessment (T-shirt sizing)
3. Review by {authority}
4. Approve/Reject/Defer
5. Update requirements baseline
```

---

<a name="communication"></a>
## 2. Communication Planning

### Problem
How to ensure effective communication of BA information?

### Framework

1. **Audience Analysis**
   - Who needs what information?
   - Preferred format and channel
   - Frequency requirements

2. **Message Design**
   - Key points to convey
   - Level of detail
   - Supporting materials

3. **Channel Selection**
   - Formal vs informal
   - Written vs verbal
   - Synchronous vs asynchronous

4. **Feedback Mechanism**
   - How to confirm understanding
   - Follow-up process
   - Issue resolution

### Template

```markdown
## Communication Plan

### Audience Matrix
| Audience | Information | Format | Frequency | Channel |
|----------|-------------|--------|-----------|---------|
| Sponsor | Status, risks | Summary | Weekly | Email |
| Dev team | Detailed reqs | Full doc | Per sprint | Jira |

### Key Messages
1. {message 1}
2. {message 2}
```

---

<a name="elicitation-preparation"></a>
## 3. Elicitation Preparation

### Problem
How to prepare effectively for elicitation activities?

### Framework

1. **Define Scope**
   - What information is needed?
   - What decisions will be made?
   - What is out of scope?

2. **Select Techniques**
   - Match technique to information type
   - Consider stakeholder preferences
   - Plan technique combinations

3. **Prepare Logistics**
   - Schedule sessions
   - Book resources
   - Prepare environment

4. **Create Materials**
   - Question guides
   - Visual aids
   - Prototypes/mockups

### Technique Selection Guide

| Information Type | Recommended Techniques |
|-----------------|------------------------|
| Current state | Observation, Document analysis |
| Pain points | Interviews, Focus groups |
| Requirements | Workshops, Prototyping |
| Validation | Reviews, Walkthroughs |

---

<a name="requirements-maintenance"></a>
## 4. Requirements Maintenance

### Problem
How to keep requirements accurate and useful over time?

### Framework

1. **Version Control**
   - Baseline management
   - Change history tracking
   - Branch/merge strategies

2. **Attribute Management**
   - Status (draft, approved, implemented)
   - Priority
   - Owner
   - Source

3. **Quality Monitoring**
   - Periodic reviews
   - Consistency checks
   - Completeness validation

4. **Archival Strategy**
   - When to archive
   - What to retain
   - Access policies

---

<a name="change-impact"></a>
## 5. Change Impact Analysis

### Problem
How to assess the impact of proposed requirement changes?

### Framework

1. **Scope Assessment**
   - What requirements are affected?
   - What designs are affected?
   - What tests are affected?

2. **Effort Assessment**
   - Development effort
   - Testing effort
   - Documentation updates

3. **Risk Assessment**
   - Technical risks
   - Schedule risks
   - Quality risks

4. **Stakeholder Impact**
   - Who is affected?
   - Training needs
   - Communication needs

5. **Decision Support**
   - Options analysis
   - Recommendation
   - Trade-offs

### Template

```markdown
## Change Impact Analysis

### Change Request: {CR-ID}
**Description:** {change description}

### Impact Assessment
| Area | Impact | Effort |
|------|--------|--------|
| Requirements | {count} reqs affected | {hours} |
| Design | {components} | {hours} |
| Code | {modules} | {hours} |
| Tests | {test cases} | {hours} |
| **Total** | | **{total hours}** |

### Risks
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| {risk} | H/M/L | H/M/L | {action} |

### Recommendation
{Accept/Reject/Defer} because {rationale}
```

---

<a name="current-state-analysis"></a>
## 6. Current State Analysis

### Problem
How to understand the existing environment and identify needs?

### Framework

1. **Business Context**
   - Organizational structure
   - Business processes
   - Strategic goals

2. **Capability Assessment**
   - Current capabilities
   - Capability gaps
   - Maturity levels

3. **Technology Landscape**
   - Current systems
   - Integration points
   - Technical debt

4. **Stakeholder Landscape**
   - Key players
   - Pain points
   - Success metrics

5. **SWOT Analysis**
   - Strengths
   - Weaknesses
   - Opportunities
   - Threats

### Template

```markdown
## Current State Assessment

### Business Context
- Organization: {description}
- Core processes: {list}
- Strategic alignment: {goals}

### Capability Assessment
| Capability | Current State | Target State | Gap |
|------------|--------------|--------------|-----|
| {cap} | {level 1-5} | {level 1-5} | {delta} |

### Pain Points
1. {pain point 1}
2. {pain point 2}

### SWOT
| Strengths | Weaknesses |
|-----------|------------|
| {s1} | {w1} |

| Opportunities | Threats |
|---------------|---------|
| {o1} | {t1} |
```

---

<a name="future-state-definition"></a>
## 7. Future State Definition

### Problem
How to define the desired future state?

### Framework

1. **Vision Statement**
   - Clear, compelling description
   - Stakeholder-aligned
   - Measurable outcomes

2. **Goals and Objectives**
   - SMART criteria
   - Aligned with strategy
   - Prioritized

3. **New Capabilities**
   - Required capabilities
   - Capability improvements
   - Capability retirements

4. **Success Metrics**
   - KPIs definition
   - Baseline vs target
   - Measurement approach

5. **Constraints and Assumptions**
   - Budget limitations
   - Timeline constraints
   - Technical constraints
   - Assumptions to validate

### Template

```markdown
## Future State Vision

### Vision Statement
{compelling description of future state}

### Goals and Objectives
| Goal | Objective | Metric | Target |
|------|-----------|--------|--------|
| {G1} | {O1} | {KPI} | {value} |

### Capability Roadmap
| Capability | Current | Future | Timeline |
|------------|---------|--------|----------|
| {cap} | Level 2 | Level 4 | Q3 2026 |

### Constraints
- Budget: {amount}
- Timeline: {deadline}
- Technology: {constraints}

### Assumptions
1. {assumption 1} - Validated: Yes/No
2. {assumption 2} - Validated: Yes/No
```

---

<a name="risk-analysis"></a>
## 8. Risk Analysis

### Problem
How to identify and assess risks to the change initiative?

### Framework

1. **Risk Identification**
   - Technical risks
   - Business risks
   - Organizational risks
   - External risks

2. **Risk Assessment**
   - Probability (1-5)
   - Impact (1-5)
   - Risk score = P x I

3. **Risk Response**
   - Avoid, Mitigate, Transfer, Accept
   - Response owner
   - Contingency plan

4. **Risk Monitoring**
   - Triggers
   - Status tracking
   - Escalation criteria

### Template

```markdown
## Risk Register

| ID | Risk | Category | P | I | Score | Response | Owner |
|----|------|----------|---|---|-------|----------|-------|
| R-001 | {description} | Technical | 4 | 5 | 20 | Mitigate | {name} |
| R-002 | {description} | Business | 2 | 3 | 6 | Accept | {name} |

## Risk Matrix

High Impact
    |
    | Accept    |  Mitigate/
    | with      |  Avoid
    | Reserve   |
    |-----------|----------
    | Accept    |  Monitor
    |           |  Closely
Low Impact --- Low Prob --- High Prob
```

---

<a name="change-strategy"></a>
## 9. Change Strategy Planning

### Problem
How to develop the optimal approach for achieving the future state?

### Framework

1. **Gap Analysis**
   - Current vs future state delta
   - Capability gaps
   - Process gaps
   - Technology gaps

2. **Solution Options**
   - Build vs buy vs partner
   - Phased vs big bang
   - Scope variations

3. **Transition Planning**
   - Milestones and phases
   - Dependencies
   - Resource requirements

4. **Readiness Assessment**
   - Organizational readiness
   - Technical readiness
   - Stakeholder readiness

5. **Business Case**
   - Expected benefits
   - Total cost of ownership
   - ROI calculation

### Template

```markdown
## Change Strategy

### Gap Analysis
| Dimension | Current | Future | Gap | Priority |
|-----------|---------|--------|-----|----------|
| Process | {state} | {state} | {gap} | H/M/L |
| Technology | {state} | {state} | {gap} | H/M/L |

### Solution Options
| Option | Description | Pros | Cons | Est. Cost |
|--------|-------------|------|------|-----------|
| A | Build in-house | Control | Time | $500K |
| B | Buy COTS | Speed | Fit | $300K |

### Recommendation
Option {X} because {rationale}

### Transition Roadmap
Phase 1 (Q1): {scope}
Phase 2 (Q2): {scope}
Phase 3 (Q3): {scope}
```

---

<a name="requirements-architecture"></a>
## 10. Requirements Architecture

### Problem
How to organize requirements into a coherent structure?

### Framework

1. **Viewpoints**
   - Business perspective
   - User perspective
   - Technical perspective
   - Operational perspective

2. **Decomposition**
   - Hierarchical breakdown
   - Parent-child relationships
   - Abstraction levels

3. **Dependencies**
   - Prerequisite relationships
   - Conflict identification
   - Synergy identification

4. **Completeness Check**
   - Coverage analysis
   - Gap identification
   - Consistency validation

### Template

```markdown
## Requirements Architecture

### Viewpoints
| Viewpoint | Stakeholders | Key Concerns |
|-----------|--------------|--------------|
| Business | Sponsor, Execs | ROI, Strategy |
| User | End users | Usability, Features |
| Technical | Developers | Feasibility, Architecture |

### Requirement Hierarchy
- BR-001: Business Requirement
  - SR-001: Stakeholder Requirement
    - FR-001: Functional Requirement
    - FR-002: Functional Requirement
  - SR-002: Stakeholder Requirement
    - FR-003: Functional Requirement

### Dependencies
| Requirement | Depends On | Enables |
|-------------|------------|---------|
| FR-001 | - | FR-003, FR-004 |
| FR-002 | FR-001 | FR-005 |
```

---

<a name="solution-options-analysis"></a>
## 11. Solution Options Analysis

### Problem
How to evaluate and recommend the best solution option?

### Framework

1. **Options Identification**
   - Generate alternatives
   - Include "do nothing" baseline
   - Consider combinations

2. **Evaluation Criteria**
   - Strategic fit
   - Technical feasibility
   - Financial viability
   - Organizational impact
   - Risk profile

3. **Scoring Method**
   - Weighted criteria
   - Scoring scale (1-5)
   - Sensitivity analysis

4. **Recommendation**
   - Best option selection
   - Justification
   - Conditions and caveats

### Template

```markdown
## Solution Options Analysis

### Options
| # | Option | Description |
|---|--------|-------------|
| A | {name} | {description} |
| B | {name} | {description} |
| C | {name} | {description} |

### Evaluation Criteria
| Criterion | Weight |
|-----------|--------|
| Strategic fit | 25% |
| Technical feasibility | 20% |
| Cost | 20% |
| Time to value | 20% |
| Risk | 15% |

### Scoring Matrix
| Criterion | Weight | Opt A | Opt B | Opt C |
|-----------|--------|-------|-------|-------|
| Strategic fit | 25% | 4 | 3 | 5 |
| Technical | 20% | 5 | 4 | 3 |
| Cost | 20% | 3 | 4 | 2 |
| Time | 20% | 3 | 5 | 2 |
| Risk | 15% | 4 | 4 | 3 |
| **Weighted Score** | | **3.75** | **3.95** | **3.10** |

### Recommendation
**Option B** is recommended because {rationale}

### Conditions
- Requires {condition}
- Assumes {assumption}
```

---

<a name="solution-limitation-assessment"></a>
## 12. Solution Limitation Assessment

### Problem
How to identify and address solution limitations?

### Framework

1. **Defect Identification**
   - Functional gaps
   - Performance issues
   - Usability problems

2. **Root Cause Analysis**
   - Technical causes
   - Process causes
   - Organizational causes

3. **Impact Assessment**
   - Business impact
   - User impact
   - Operational impact

4. **Remediation Options**
   - Quick fixes
   - Workarounds
   - Permanent solutions
   - Accept limitations

### Template

```markdown
## Solution Limitation Assessment

### Identified Limitations
| ID | Limitation | Category | Severity |
|----|------------|----------|----------|
| L-001 | {description} | Functional | High |
| L-002 | {description} | Performance | Medium |

### Root Cause Analysis
| Limitation | Root Cause | Evidence |
|------------|------------|----------|
| L-001 | {cause} | {evidence} |

### Impact Assessment
| Limitation | Business Impact | User Impact | Frequency |
|------------|-----------------|-------------|-----------|
| L-001 | {impact} | {impact} | Daily |

### Remediation Recommendations
| Limitation | Option | Effort | Recommendation |
|------------|--------|--------|----------------|
| L-001 | A: Fix in v2 | 3 sprints | Accept for now |
| L-001 | B: Workaround | 2 days | Implement |
```

---

## BA Framework 50 Techniques Reference

| # | Technique | Primary Use Cases |
|---|-----------|-------------------|
| 1 | Acceptance and Evaluation Criteria | Requirements validation |
| 2 | Backlog Management | Agile requirements |
| 3 | Balanced Scorecard | Strategy analysis |
| 4 | Benchmarking and Market Analysis | Current state analysis |
| 5 | Brainstorming | Elicitation |
| 6 | Business Capability Analysis | Strategy analysis |
| 7 | Business Cases | Change strategy |
| 8 | Business Model Canvas | Strategy analysis |
| 9 | Business Rules Analysis | Requirements analysis |
| 10 | Collaborative Games | Elicitation |
| 11 | Concept Modelling | Requirements modeling |
| 12 | Data Dictionary | Data requirements |
| 13 | Data Flow Diagrams | Process analysis |
| 14 | Data Mining | Analysis |
| 15 | Data Modelling | Data requirements |
| 16 | Decision Analysis | Solution evaluation |
| 17 | Decision Modelling | Business rules |
| 18 | Document Analysis | Elicitation |
| 19 | Estimation | Planning |
| 20 | Financial Analysis | Business case |
| 21 | Focus Groups | Elicitation |
| 22 | Functional Decomposition | Requirements architecture |
| 23 | Glossary | Communication |
| 24 | Interface Analysis | Requirements analysis |
| 25 | Interviews | Elicitation |
| 26 | Item Tracking | Requirements management |
| 27 | Lessons Learned | Improvement |
| 28 | Metrics and KPIs | Performance measurement |
| 29 | Mind Mapping | Elicitation, analysis |
| 30 | Non-Functional Requirements Analysis | Requirements analysis |
| 31 | Observation | Elicitation |
| 32 | Organizational Modelling | Current state |
| 33 | Prioritization | Requirements management |
| 34 | Process Analysis | Current state |
| 35 | Process Modelling | Requirements modeling |
| 36 | Prototyping | Elicitation, validation |
| 37 | Reviews | Verification |
| 38 | Risk Analysis and Management | Strategy, evaluation |
| 39 | Roles and Permissions Matrix | Requirements analysis |
| 40 | Root Cause Analysis | Problem analysis |
| 41 | Scope Modelling | Strategy analysis |
| 42 | Sequence Diagrams | Requirements modeling |
| 43 | Stakeholder List, Map, or Personas | Stakeholder analysis |
| 44 | State Modelling | Requirements modeling |
| 45 | Survey or Questionnaire | Elicitation |
| 46 | SWOT Analysis | Current state |
| 47 | Use Cases and Scenarios | Requirements modeling |
| 48 | User Stories | Agile requirements |
| 49 | Vendor Assessment | Solution evaluation |
| 50 | Workshops | Elicitation |

---

*Extracted from BA Domain Skill v1.0*
*Reference document for detailed methodology content*
