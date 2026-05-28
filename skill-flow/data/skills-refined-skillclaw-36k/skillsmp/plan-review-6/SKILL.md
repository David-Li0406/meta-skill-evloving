---
name: plan-review
description: "Systematic project plan review toolkit. Evaluate architecture decisions, building block specifications, sprint plans, cost estimates, risk assessments, and implementation feasibility for comprehensive project plan validation."
allowed-tools: [Read, Write, Edit, Bash]
---

# Project Plan Review and Validation

## Overview

Plan review is a systematic process for evaluating project plans and specifications. Assess architecture decisions, building blocks, sprint plans, cost estimates, risk assessments, and implementation roadmaps. Apply this skill to validate project plans before implementation begins.

## When to Use This Skill

This skill should be used when:
- Reviewing completed project plans and specifications
- Validating architecture decisions and technology choices
- Assessing building block specifications for completeness
- Reviewing sprint plans and user stories for INVEST criteria
- Validating cost estimates and ROI projections
- Evaluating risk assessments and mitigation strategies
- Providing constructive feedback on implementation roadmaps

## Visual Enhancement with Project Diagrams

**When creating review documents, consider adding diagrams to enhance communication.**

Use the **project-diagrams** skill to generate:
- Architecture review diagrams highlighting concerns
- Dependency analysis visualizations
- Sprint timeline charts
- Risk heat maps
- Cost breakdown charts

```bash
python .claude/skills/project-diagrams/scripts/generate_schematic.py "diagram description" -o diagrams/output.png
```

---

## Plan Review Workflow

Conduct plan review systematically through the following stages.

### Stage 1: Initial Assessment

Begin with a high-level evaluation to determine the plan's scope, completeness, and overall quality.

**Key Questions:**
- What is the project's core objective and value proposition?
- Are all major deliverables and milestones identified?
- Is the scope realistic for the proposed timeline and resources?
- Are there any immediate major gaps or inconsistencies?

**Output:** Brief summary (2-3 sentences) capturing the plan's essence and initial impression.

### Stage 2: Architecture Review

Evaluate the system architecture and technology decisions.

#### Technology Stack Assessment
- **Appropriateness:** Is the stack suitable for the project's requirements?
- **Maturity:** Are chosen technologies production-ready and well-supported?
- **Team Skills:** Does the team have expertise with the chosen stack?
- **Scalability:** Can the architecture handle projected growth?
- **Cost:** Are there hidden costs or vendor lock-in risks?

#### Architecture Decision Records (ADRs)
- Are major decisions documented with context and rationale?
- Are alternatives considered and trade-offs discussed?
- Are decisions traceable to requirements?

#### Component Design
- Is the system properly decomposed into logical components?
- Are component boundaries clear and responsibilities well-defined?
- Are interfaces between components specified?
- Are there circular dependencies or tight coupling concerns?

### Stage 3: Building Block Specification Review

Evaluate each building block for completeness and buildability.

**For each building block, verify:**

#### Specification Completeness
- [ ] Clear name and description
- [ ] Type identified (frontend, backend, infrastructure, integration, shared)
- [ ] Responsibilities listed (specific, not vague)
- [ ] Dependencies documented
- [ ] Interfaces defined (API endpoints, events, data contracts)
- [ ] Complexity estimate (S, M, L, XL)
- [ ] Estimated hours/story points
- [ ] Test criteria specified

#### Buildability Assessment
- Can Claude Code build this block independently?
- Are all prerequisites and dependencies available?
- Is the scope small enough for incremental delivery?
- Are acceptance criteria testable?

#### Interface Contracts
- Are API endpoints RESTful with proper HTTP methods?
- Are request/response schemas defined?
- Are error responses specified?
- Are events and messages well-documented?

### Stage 4: Sprint Plan Review

Evaluate sprint plans for feasibility and INVEST criteria.

#### Sprint Structure
- **Goals:** Are sprint goals clear, measurable, and achievable?
- **Duration:** Is the sprint duration realistic (typically 1-2 weeks)?
- **Scope:** Is the sprint scope appropriate for the team capacity?
- **Dependencies:** Are inter-sprint dependencies identified?

#### User Stories Assessment (INVEST Criteria)

| Criterion | Question |
|-----------|----------|
| **Independent** | Can this story be delivered without other stories? |
| **Negotiable** | Is the scope flexible based on feedback? |
| **Valuable** | Does it deliver value to users or stakeholders? |
| **Estimable** | Can effort be reasonably estimated? |
| **Small** | Can it be completed within a sprint? |
| **Testable** | Are acceptance criteria clear and testable? |

#### Story Quality Checklist
- [ ] Clear "As a... I want... So that..." format
- [ ] Acceptance criteria are specific and measurable
- [ ] Story points are assigned
- [ ] Building block association is specified
- [ ] Dependencies are identified
- [ ] Priority is assigned

### Stage 5: Cost Analysis Review

Evaluate cost estimates and financial projections.

#### Service Cost Verification
- Are estimates based on current pricing (not outdated)?
- Are pricing sources documented?
- Are usage assumptions realistic?
- Are low/mid/high scenarios provided?

#### Cost Categories to Verify
- [ ] Infrastructure costs (compute, storage, networking)
- [ ] Third-party service costs (APIs, SaaS)
- [ ] Development tool costs (CI/CD, monitoring)
- [ ] Licensing costs
- [ ] Personnel costs (if applicable)
- [ ] Contingency buffer (typically 15-25%)

#### ROI Assessment
- Are revenue projections realistic and justified?
- Is the payback period calculated correctly?
- Are growth assumptions documented?
- Are comparable market data referenced?

### Stage 6: Risk Assessment Review

Evaluate risk identification and mitigation strategies.

#### Risk Register Completeness
- [ ] Risks categorized (technical, business, resource, external, security)
- [ ] Likelihood assessed (low, medium, high)
- [ ] Impact assessed (low, medium, high)
- [ ] Risk scores calculated
- [ ] Mitigation strategies defined
- [ ] Contingency plans documented
- [ ] Risk owners assigned

#### Risk Coverage Assessment
**Verify these common risk categories are addressed:**

| Category | Example Risks |
|----------|--------------|
| Technical | Integration failures, scalability issues, technical debt |
| Security | Data breaches, authentication vulnerabilities |
| Resource | Key person dependency, skill gaps, turnover |
| External | Third-party API changes, regulatory changes |
| Business | Market changes, competitor actions, budget cuts |
| Timeline | Scope creep, dependency delays, underestimation |

#### Mitigation Quality
- Are mitigations actionable and specific?
- Are contingency plans realistic?
- Is residual risk acceptable?

### Stage 7: Timeline and Milestone Review

Evaluate the implementation timeline.

#### Timeline Realism
- Are duration estimates realistic based on complexity?
- Is there adequate buffer for uncertainties (20-30%)?
- Are holidays and team availability considered?
- Are external dependencies factored in?

#### Critical Path Analysis
- Is the critical path identified?
- Are bottlenecks recognized?
- Are parallel workstreams maximized?
- Are milestone dependencies clear?

#### Milestone Quality
- [ ] Milestones are measurable and verifiable
- [ ] Deliverables are clearly defined
- [ ] Success criteria are specified
- [ ] Review gates are planned

## Structuring Plan Review Reports

Organize feedback in a hierarchical structure.

### Summary Statement

Provide a concise overall assessment (1-2 paragraphs):
- Brief synopsis of the project plan
- Overall recommendation (approve, minor revisions, major revisions, significant rework)
- Key strengths (2-3 bullet points)
- Key concerns (2-3 bullet points)
- Bottom-line assessment of implementation readiness

### Critical Issues

List issues that must be resolved before implementation:
- Missing critical specifications
- Unrealistic estimates or timelines
- Major architectural flaws
- Unaddressed high-impact risks
- Budget insufficiencies

**For each critical issue:**
1. Clearly state the issue
2. Explain why it's critical
3. Suggest specific resolution
4. Indicate blocking nature

### Major Recommendations

List important issues that should be addressed:
- Specification gaps
- Unclear interfaces
- Missing test criteria
- Questionable technology choices
- Incomplete risk coverage

### Minor Suggestions

List improvements for plan quality:
- Documentation clarifications
- Diagram additions
- Minor specification enhancements
- Alternative approaches to consider

### Questions for Clarification

List specific questions needing answers:
- Unclear requirements
- Ambiguous decisions
- Missing context
- Assumption verification

## Review Checklist by Plan Component

### Project Specification Review
- [ ] Problem statement is clear
- [ ] Target users defined
- [ ] Core features prioritized
- [ ] Success metrics specified
- [ ] Constraints documented

### Technical Specification Review
- [ ] Architecture diagram included
- [ ] Technology stack justified
- [ ] Data model complete
- [ ] API specification defined
- [ ] Security considerations addressed
- [ ] Performance requirements stated

### Building Blocks Review
- [ ] All functionality covered
- [ ] No overlapping responsibilities
- [ ] Dependencies form DAG (no cycles)
- [ ] Interfaces are consistent
- [ ] Complexity estimates reasonable

### Sprint Plan Review
- [ ] All building blocks assigned to sprints
- [ ] Dependencies respected in ordering
- [ ] Capacity is realistic per sprint
- [ ] Stories are properly decomposed
- [ ] Acceptance criteria are testable

### Cost Analysis Review
- [ ] All services identified
- [ ] Current pricing used
- [ ] Usage assumptions documented
- [ ] Scenarios provided (low/mid/high)
- [ ] ROI calculated with realistic assumptions

### Risk Assessment Review
- [ ] Major risk categories covered
- [ ] High-impact risks have mitigations
- [ ] Contingency plans exist
- [ ] Risk owners assigned
- [ ] Monitoring approach defined

## Tone and Approach

Maintain a constructive, professional tone throughout.

**Best Practices:**
- **Be constructive:** Frame concerns as opportunities for improvement
- **Be specific:** Reference specific sections, blocks, or estimates
- **Be balanced:** Acknowledge strengths alongside concerns
- **Be actionable:** Provide concrete suggestions
- **Be thorough:** Cover all plan components systematically

**Avoid:**
- Vague criticism without specifics
- Dismissing plans without justification
- Imposing personal preferences over best practices
- Scope creep in recommendations
- Perfectionism that delays implementation

## Final Checklist

Before finalizing the review, verify:

- [ ] Summary clearly conveys overall assessment
- [ ] Critical issues are justified and actionable
- [ ] All plan components reviewed
- [ ] Recommendations are specific and feasible
- [ ] Questions are clear and answerable
- [ ] Tone is constructive throughout
- [ ] Review is proportionate to plan scope
- [ ] Recommendation is consistent with issues identified
