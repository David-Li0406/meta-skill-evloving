---
name: risk-assessment
description: "Project risk assessment toolkit. Identify technical, business, resource, and external risks, score likelihood and impact, define mitigation strategies and contingency plans for comprehensive risk management."
allowed-tools: [Read, Write, Edit, Bash]
---

# Risk Assessment

## Overview

Risk assessment is a systematic process for identifying, analyzing, and planning responses to project risks. Evaluate technical, business, resource, and external risks, score by likelihood and impact, and define mitigation strategies and contingency plans to manage project uncertainty.

## When to Use This Skill

This skill should be used when:
- Identifying risks in new project plans
- Assessing technical and architectural risks
- Evaluating business and market risks
- Planning risk mitigations and contingencies
- Creating risk registers for projects
- Monitoring and updating risk status

## Visual Enhancement with Project Diagrams

**When documenting risk assessments, include visualizations.**

Use the **project-diagrams** skill to generate:
- Risk heat maps (likelihood vs. impact matrix)
- Risk category breakdown charts
- Mitigation timeline diagrams
- Decision trees for contingency plans

```bash
python .claude/skills/project-diagrams/scripts/generate_schematic.py "diagram description" -o diagrams/output.png
```

---

## Risk Assessment Framework

### Risk Categories

| Category | Description | Examples |
|----------|-------------|----------|
| **Technical** | Technology and implementation risks | Integration failures, scalability issues, technical debt |
| **Security** | Data and system security risks | Breaches, vulnerabilities, compliance failures |
| **Resource** | Team and capacity risks | Key person dependency, skill gaps, turnover |
| **External** | Third-party and environmental risks | API changes, vendor reliability, regulatory changes |
| **Business** | Market and financial risks | Competition, market changes, budget cuts |
| **Timeline** | Schedule and delivery risks | Scope creep, estimation errors, dependencies |
| **Operational** | Production and support risks | Downtime, incident response, maintenance |

### Risk Scoring Matrix

**Likelihood Scale:**

| Score | Level | Description |
|-------|-------|-------------|
| 1 | Rare | < 10% probability, unlikely to occur |
| 2 | Unlikely | 10-30% probability, could occur |
| 3 | Possible | 30-50% probability, might occur |
| 4 | Likely | 50-80% probability, will probably occur |
| 5 | Almost Certain | > 80% probability, expected to occur |

**Impact Scale:**

| Score | Level | Description |
|-------|-------|-------------|
| 1 | Negligible | Minor inconvenience, easily absorbed |
| 2 | Minor | Some disruption, workaround available |
| 3 | Moderate | Significant impact, requires response |
| 4 | Major | Serious impact, threatens objectives |
| 5 | Critical | Catastrophic, project failure possible |

**Risk Score Calculation:**
```
Risk Score = Likelihood × Impact

1-4:   Low risk (green)
5-9:   Medium risk (yellow)
10-15: High risk (orange)
16-25: Critical risk (red)
```

### Risk Heat Map

```
           Impact
           1    2    3    4    5
        ┌────┬────┬────┬────┬────┐
      5 │ 5  │ 10 │ 15 │ 20 │ 25 │
L       ├────┼────┼────┼────┼────┤
i     4 │ 4  │ 8  │ 12 │ 16 │ 20 │
k       ├────┼────┼────┼────┼────┤
e     3 │ 3  │ 6  │ 9  │ 12 │ 15 │
l       ├────┼────┼────┼────┼────┤
i     2 │ 2  │ 4  │ 6  │ 8  │ 10 │
h       ├────┼────┼────┼────┼────┤
o     1 │ 1  │ 2  │ 3  │ 4  │ 5  │
o       └────┴────┴────┴────┴────┘
d
```

## Risk Specification Schema

```yaml
risk:
  # Identity
  id: "RISK-NNN"
  title: "Short descriptive title"

  # Classification
  category: "technical | security | resource | external | business | timeline | operational"

  # Description
  description: |
    What is the risk? What could go wrong?

  cause: |
    What could cause this risk to materialize?

  effect: |
    What would be the impact if this risk materializes?

  # Scoring
  likelihood: 1-5
  likelihood_rationale: "Why this likelihood score"

  impact: 1-5
  impact_rationale: "Why this impact score"

  risk_score: N  # likelihood × impact
  risk_level: "low | medium | high | critical"

  # Response
  response_strategy: "avoid | mitigate | transfer | accept"

  mitigation:
    actions:
      - "Specific action to reduce likelihood or impact"
    responsible: "Team or person"
    deadline: "YYYY-MM-DD"
    cost: "Estimated cost if applicable"

  contingency:
    trigger: "What indicates this risk has materialized"
    actions:
      - "Action to take if risk occurs"
    responsible: "Team or person"

  # Tracking
  status: "identified | mitigating | monitoring | closed | materialized"
  owner: "Person responsible for tracking"

  # Metadata
  identified_date: "YYYY-MM-DD"
  last_reviewed: "YYYY-MM-DD"
  related_risks: ["RISK-XXX"]
```

### Response Strategies

| Strategy | When to Use | Example |
|----------|-------------|---------|
| **Avoid** | Eliminate the risk entirely | Change technology, remove feature |
| **Mitigate** | Reduce likelihood or impact | Add redundancy, implement safeguards |
| **Transfer** | Shift risk to third party | Insurance, outsourcing, SLAs |
| **Accept** | Acknowledge and monitor | Low-impact risks, cost-effective |

## Common Risks by Category

### Technical Risks

```yaml
risks:
  - id: "RISK-T001"
    title: "Integration Complexity"
    category: "technical"
    description: |
      Third-party API integrations prove more complex than estimated,
      requiring additional development time.
    cause: |
      - Poor API documentation
      - Undocumented edge cases
      - Version incompatibilities
    effect: |
      - Sprint delays
      - Increased development cost
      - Technical debt
    likelihood: 3
    impact: 3
    risk_score: 9
    risk_level: "medium"
    response_strategy: "mitigate"
    mitigation:
      actions:
        - "Prototype integrations in Sprint 1"
        - "Create abstraction layer for external dependencies"
        - "Document fallback approaches"
      responsible: "Tech Lead"
      deadline: "End of Sprint 1"
    contingency:
      trigger: "Integration spike takes >3 days"
      actions:
        - "Evaluate alternative providers"
        - "Adjust timeline and communicate to stakeholders"
    status: "identified"

  - id: "RISK-T002"
    title: "Scalability Issues"
    category: "technical"
    description: |
      System architecture cannot handle projected user growth,
      requiring significant rearchitecture.
    cause: |
      - Underestimated traffic growth
      - Inefficient database queries
      - Synchronous processing bottlenecks
    effect: |
      - Performance degradation
      - User experience impact
      - Costly emergency fixes
    likelihood: 2
    impact: 4
    risk_score: 8
    risk_level: "medium"
    response_strategy: "mitigate"
    mitigation:
      actions:
        - "Design for 10x expected load"
        - "Implement caching layer from start"
        - "Plan load testing in Sprint 3"
    contingency:
      trigger: "Response times exceed 2 seconds at 50% projected load"
      actions:
        - "Emergency scale-up infrastructure"
        - "Activate CDN for static assets"
        - "Implement request queuing"
    status: "identified"
```

### Security Risks

```yaml
risks:
  - id: "RISK-S001"
    title: "Data Breach"
    category: "security"
    description: |
      Unauthorized access to user data due to security vulnerability.
    cause: |
      - Unpatched vulnerabilities
      - Weak authentication
      - SQL injection or XSS
    effect: |
      - Regulatory fines (GDPR)
      - Reputation damage
      - Legal liability
    likelihood: 2
    impact: 5
    risk_score: 10
    risk_level: "high"
    response_strategy: "mitigate"
    mitigation:
      actions:
        - "Security audit before launch"
        - "Implement WAF and rate limiting"
        - "Enable encryption at rest and in transit"
        - "Conduct penetration testing"
      responsible: "Security Team"
      cost: "$5,000-10,000"
    contingency:
      trigger: "Detection of unauthorized access"
      actions:
        - "Activate incident response plan"
        - "Isolate affected systems"
        - "Notify affected users within 72 hours"
        - "Engage forensic investigation"
    status: "identified"
```

### Resource Risks

```yaml
risks:
  - id: "RISK-R001"
    title: "Key Person Dependency"
    category: "resource"
    description: |
      Critical project knowledge concentrated in one team member,
      creating single point of failure.
    cause: |
      - Complex domain expertise
      - Specialized technical skills
      - Insufficient documentation
    effect: |
      - Project delays if person unavailable
      - Knowledge loss if person leaves
      - Bottleneck in decision making
    likelihood: 3
    impact: 4
    risk_score: 12
    risk_level: "high"
    response_strategy: "mitigate"
    mitigation:
      actions:
        - "Document all architectural decisions (ADRs)"
        - "Pair programming on critical components"
        - "Cross-train at least 2 team members"
      responsible: "Engineering Manager"
    contingency:
      trigger: "Key person unavailable > 1 week"
      actions:
        - "Activate backup assignee"
        - "Prioritize documentation catch-up"
        - "Consider contractor for specialized skills"
    status: "identified"
```

### External Risks

```yaml
risks:
  - id: "RISK-E001"
    title: "Third-Party API Deprecation"
    category: "external"
    description: |
      Critical third-party API announces deprecation or breaking changes
      during project timeline.
    cause: |
      - Vendor business changes
      - Technology evolution
      - Acquisition or shutdown
    effect: |
      - Forced migration effort
      - Timeline delays
      - Potential feature loss
    likelihood: 2
    impact: 3
    risk_score: 6
    risk_level: "medium"
    response_strategy: "mitigate"
    mitigation:
      actions:
        - "Abstract all external dependencies"
        - "Identify alternative providers"
        - "Monitor vendor announcements"
      responsible: "Tech Lead"
    contingency:
      trigger: "Deprecation announcement or breaking change"
      actions:
        - "Assess migration timeline"
        - "Evaluate alternative providers"
        - "Adjust project timeline if needed"
    status: "identified"
```

### Timeline Risks

```yaml
risks:
  - id: "RISK-TL001"
    title: "Scope Creep"
    category: "timeline"
    description: |
      Requirements expand beyond original scope, consuming budget
      and extending timeline.
    cause: |
      - Unclear initial requirements
      - Stakeholder additions
      - "Just one more feature" syndrome
    effect: |
      - Budget overrun
      - Timeline extension
      - Team burnout
    likelihood: 4
    impact: 3
    risk_score: 12
    risk_level: "high"
    response_strategy: "mitigate"
    mitigation:
      actions:
        - "Document scope in detail before starting"
        - "Implement change request process"
        - "Regular scope reviews in sprint planning"
        - "Prioritize MVP features ruthlessly"
      responsible: "Product Owner"
    contingency:
      trigger: "Scope increases by >20% from baseline"
      actions:
        - "Formal change request required"
        - "Adjust timeline or budget"
        - "Deprioritize lower-value features"
    status: "identified"
```

## Risk Register Template

```yaml
risk_register:
  project: "[Project Name]"
  last_updated: "YYYY-MM-DD"

  summary:
    total_risks: N
    critical: N
    high: N
    medium: N
    low: N

  risks:
    - id: "RISK-001"
      title: "..."
      category: "..."
      # ... full specification

    # ... more risks

  review_schedule:
    frequency: "Every sprint"
    next_review: "YYYY-MM-DD"
    reviewer: "Project Manager"
```

## Risk Assessment Report Structure

```markdown
# Risk Assessment Report: [Project Name]

## Executive Summary
- Total risks identified: N
- Critical/High risks: N (requiring immediate attention)
- Primary risk areas: [Categories]
- Overall risk level: [Low/Medium/High]

## Risk Heat Map
[Visual representation of risks by likelihood/impact]

## Critical and High Risks

### RISK-001: [Title]
**Score:** [N] (Critical/High)
**Category:** [Category]

**Description:** [What could go wrong]

**Mitigation:**
- [Action 1]
- [Action 2]

**Contingency:** [If risk materializes]

**Owner:** [Person responsible]

---

[Repeat for each critical/high risk]

## Medium and Low Risks

| ID | Title | Category | Score | Status |
|----|-------|----------|-------|--------|
| RISK-X | Title | Category | N | Status |

## Risk Monitoring Plan

| Risk ID | Metric to Monitor | Review Frequency | Trigger |
|---------|-------------------|------------------|---------|
| | | | |

## Recommendations
1. [Key action to reduce overall risk]
2. [Key action to reduce overall risk]
3. [Key action to reduce overall risk]

## Appendix: Full Risk Register
[Complete risk specifications]
```

## Risk Assessment Process

### Phase 1: Risk Identification

**Techniques:**
1. **Brainstorming** - Team session to identify risks
2. **Checklist Review** - Use category checklists
3. **Assumption Analysis** - Challenge assumptions
4. **Expert Interviews** - Consult domain experts
5. **Historical Review** - Learn from past projects

**Questions to Ask:**
- What could go wrong?
- What assumptions are we making?
- What dependencies do we have?
- What has failed in similar projects?
- What keeps you up at night?

### Phase 2: Risk Analysis

**For each identified risk:**
1. Describe the risk clearly
2. Identify root causes
3. Assess potential effects
4. Score likelihood (1-5)
5. Score impact (1-5)
6. Calculate risk score
7. Determine risk level

### Phase 3: Risk Response Planning

**For high and critical risks:**
1. Choose response strategy
2. Define specific mitigation actions
3. Assign ownership
4. Set deadlines
5. Define contingency plans
6. Identify trigger conditions

### Phase 4: Risk Monitoring

**Ongoing activities:**
- Review risk register each sprint
- Update scores based on new information
- Track mitigation action completion
- Monitor trigger conditions
- Add new risks as identified
- Close risks that are no longer relevant

## Quality Checklist

Before completing risk assessment:

- [ ] All risk categories considered
- [ ] Risks clearly described with cause and effect
- [ ] Likelihood and impact scored with rationale
- [ ] High/Critical risks have mitigation plans
- [ ] Contingency plans defined with triggers
- [ ] Risk owners assigned
- [ ] Review schedule established
- [ ] Risk heat map generated
- [ ] Stakeholders aware of critical risks

## Best Practices

### Do's
- Involve the whole team in risk identification
- Be specific about causes and effects
- Update risk register regularly
- Track mitigation action completion
- Learn from risks that materialize
- Communicate risks transparently

### Don'ts
- Don't ignore "unlikely" risks with high impact
- Don't set and forget the risk register
- Don't underestimate security risks
- Don't assume risks are someone else's problem
- Don't let risk assessment become checkbox exercise
- Don't panic - plan and respond systematically
