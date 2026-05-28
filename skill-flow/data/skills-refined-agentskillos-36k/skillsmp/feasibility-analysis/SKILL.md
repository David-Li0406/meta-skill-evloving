---
name: feasibility-analysis
description: "Project feasibility analysis toolkit. Evaluate technical feasibility, resource requirements, market viability, risk factors, and implementation challenges for informed go/no-go decisions on software projects."
allowed-tools: [Read, Write, Edit, Bash]
---

# Project Feasibility Analysis

## Overview

Feasibility analysis is a systematic process for evaluating whether a proposed software project is viable and worth pursuing. Assess technical feasibility, resource requirements, market viability, risk factors, and implementation challenges. Apply this skill to make informed go/no-go decisions before committing resources.

## When to Use This Skill

This skill should be used when:
- Evaluating new project proposals for viability
- Assessing technical feasibility of proposed features
- Analyzing resource requirements and constraints
- Conducting market viability assessments
- Identifying potential blockers and deal-breakers
- Comparing multiple project options
- Preparing feasibility reports for stakeholders

## Visual Enhancement with Project Diagrams

**When creating feasibility documents, consider adding diagrams for clarity.**

Use the **project-diagrams** skill to generate:
- Feasibility decision trees
- Risk assessment matrices
- Resource requirement diagrams
- Technical architecture feasibility maps
- Market positioning charts

```bash
python .claude/skills/project-diagrams/scripts/generate_schematic.py "diagram description" -o diagrams/output.png
```

---

## Feasibility Analysis Framework

Conduct feasibility analysis systematically through multiple dimensions.

### 1. Technical Feasibility

Evaluate whether the project can be built with available technology and expertise.

#### Technology Readiness Assessment

| Readiness Level | Description | Risk |
|-----------------|-------------|------|
| **Mature** | Production-proven, widely used | Low |
| **Established** | Production-ready, growing adoption | Low-Medium |
| **Emerging** | Early adoption, limited production use | Medium |
| **Experimental** | Pre-production, research phase | High |
| **Theoretical** | Conceptual, not yet implemented | Very High |

**For each core technology, assess:**
- Current maturity level
- Community and vendor support
- Documentation quality
- Talent availability in market
- Long-term viability

#### Technical Complexity Assessment

**Complexity Factors:**

| Factor | Low | Medium | High |
|--------|-----|--------|------|
| Integration points | 1-3 | 4-7 | 8+ |
| Data sources | 1-2 | 3-5 | 6+ |
| Custom algorithms | None | Some | Significant |
| Real-time requirements | None | Partial | Critical |
| Scale requirements | <1K users | 1K-100K | >100K |
| Security requirements | Basic | Standard | Stringent |
| Compliance requirements | None | Industry | Regulatory |

**Complexity Score:** Sum factors and categorize:
- 0-7: Low complexity (straightforward implementation)
- 8-14: Medium complexity (manageable with expertise)
- 15-21: High complexity (significant challenges expected)
- 22+: Very high complexity (consider scope reduction)

#### Technical Risk Factors

**Identify and rate (1-5) these risks:**

- **Unproven architecture:** Novel patterns without precedent
- **Integration complexity:** Many external system dependencies
- **Performance uncertainty:** Unclear if requirements are achievable
- **Scalability concerns:** Uncertainty about growth handling
- **Security challenges:** Complex threat model or compliance needs
- **Data complexity:** Large, unstructured, or sensitive data
- **Algorithm novelty:** Custom ML/AI or complex logic required

**Risk Mitigation Questions:**
- Have similar systems been built successfully?
- Are there proven patterns we can follow?
- Can we prototype high-risk components early?
- What are fallback options if primary approach fails?

### 2. Resource Feasibility

Evaluate whether required resources (people, time, money) are available.

#### Team Capability Assessment

**Required Skills Inventory:**

| Skill Area | Required Level | Current Level | Gap |
|------------|---------------|---------------|-----|
| Frontend development | | | |
| Backend development | | | |
| DevOps/Infrastructure | | | |
| Database/Data engineering | | | |
| Security | | | |
| Domain expertise | | | |
| Project management | | | |

**Levels:** None, Basic, Intermediate, Advanced, Expert

**Gap Analysis:**
- Critical gaps (show-stoppers)
- Important gaps (require hiring/training)
- Minor gaps (manageable with learning)

#### Timeline Feasibility

**Timeline Estimation Factors:**

| Factor | Multiplier |
|--------|------------|
| Clear requirements | 1.0x |
| Partially defined requirements | 1.3x |
| Evolving requirements | 1.5x |
| Experienced team with stack | 1.0x |
| Team learning new technologies | 1.3x |
| Team new to domain | 1.5x |
| Greenfield project | 1.0x |
| Legacy integration | 1.3x |
| Legacy replacement | 1.5x |

**Timeline Reality Check:**
- Apply multipliers to initial estimates
- Add 20-30% buffer for unknowns
- Compare to similar past projects
- Identify hard deadlines and assess achievability

#### Budget Feasibility

**Cost Categories to Estimate:**

```yaml
cost_categories:
  development:
    - Personnel (internal team)
    - Contractors/consultants
    - Training and upskilling
  infrastructure:
    - Cloud services (compute, storage, networking)
    - Development environments
    - CI/CD tooling
  third_party:
    - SaaS subscriptions
    - API costs
    - Licensing fees
  operational:
    - Monitoring and observability
    - Support tooling
    - Security tools
  contingency:
    - Risk buffer (15-25%)
    - Scope buffer (10-20%)
```

**Budget Viability Assessment:**
- Total estimated cost vs. available budget
- Cash flow timing requirements
- Hidden costs identification
- Cost overrun scenarios

### 3. Market Feasibility

Evaluate whether the project addresses a real market need.

#### Market Need Assessment

**Key Questions:**
- Is there demonstrated demand for this solution?
- What problem does it solve, and how painful is that problem?
- Who are the target users, and can we reach them?
- What is the market size (TAM, SAM, SOM)?
- Is the market growing, stable, or declining?

#### Competitive Landscape Analysis

**Competitor Assessment Matrix:**

| Competitor | Strengths | Weaknesses | Our Differentiation |
|------------|-----------|------------|---------------------|
| | | | |

**Competitive Position Questions:**
- Who are the main competitors?
- What is our unique value proposition?
- Can we compete on features, price, or experience?
- Are there barriers to entry?
- Is there room for another player?

#### Market Timing Assessment

| Timing | Description | Implication |
|--------|-------------|-------------|
| **Too early** | Market not ready, user education needed | High risk, long runway required |
| **Early** | Market emerging, first-mover advantage possible | Medium risk, faster execution helps |
| **Right time** | Market established, clear demand | Lower risk, differentiation critical |
| **Late** | Market saturated, incumbents entrenched | High risk, disruption required |

### 4. Operational Feasibility

Evaluate whether the project can be successfully deployed and operated.

#### Organizational Readiness

**Assess the organization's ability to:**
- Adopt new technology and processes
- Support the solution post-launch
- Handle change management requirements
- Maintain the solution long-term

#### Operational Requirements

**Key Operational Factors:**

| Factor | Requirement | Current Capability | Gap |
|--------|-------------|-------------------|-----|
| 24/7 operations | | | |
| Incident response | | | |
| User support | | | |
| Data backup/recovery | | | |
| Security monitoring | | | |
| Performance monitoring | | | |
| Compliance reporting | | | |

#### Integration Feasibility

**For each required integration:**

| System | Integration Type | Complexity | Risk |
|--------|-----------------|------------|------|
| | API / File / DB / Event | Low/Med/High | |

**Integration Risk Factors:**
- API stability and documentation quality
- Authentication/authorization complexity
- Data format compatibility
- Rate limits and quotas
- Vendor reliability and support

### 5. Legal and Compliance Feasibility

Evaluate regulatory, legal, and compliance requirements.

#### Regulatory Requirements

**Common Compliance Frameworks:**

| Framework | Applicability | Effort |
|-----------|--------------|--------|
| GDPR | EU personal data | High |
| HIPAA | US healthcare data | Very High |
| SOC 2 | B2B SaaS | Medium-High |
| PCI-DSS | Payment card data | High |
| CCPA | California consumer data | Medium |

**Compliance Assessment:**
- Which regulations apply?
- What controls are required?
- What certifications are needed?
- What is the timeline and cost for compliance?

#### Intellectual Property Considerations

- Are there patent concerns?
- Are there licensing restrictions on dependencies?
- Do we have rights to required data?
- Are there trademark considerations?

## Feasibility Scoring

### Overall Feasibility Score

Rate each dimension (1-5):

| Dimension | Score | Weight | Weighted Score |
|-----------|-------|--------|----------------|
| Technical Feasibility | | 25% | |
| Resource Feasibility | | 25% | |
| Market Feasibility | | 20% | |
| Operational Feasibility | | 15% | |
| Legal/Compliance Feasibility | | 15% | |
| **Total** | | 100% | |

**Score Interpretation:**

| Total Score | Recommendation |
|-------------|----------------|
| 4.0-5.0 | **Strong Go** - Proceed with confidence |
| 3.0-3.9 | **Conditional Go** - Proceed with mitigations |
| 2.0-2.9 | **Caution** - Address significant concerns first |
| 1.0-1.9 | **No Go** - Major barriers, reconsider or pivot |

### Go/No-Go Decision Criteria

**Automatic No-Go Triggers:**
- Critical technology not available or unproven
- Required skills unavailable and unhirable
- Budget shortfall >50%
- Timeline impossible for hard deadline
- Regulatory showstopper
- Market doesn't exist

**Conditional Go Requirements:**
- All critical risks have mitigation plans
- Resource gaps have remediation paths
- Timeline achievable with buffer
- Budget within 20% of estimate
- Clear path to market

## Feasibility Report Structure

### Executive Summary
- Project overview (2-3 sentences)
- Overall feasibility score and recommendation
- Key strengths (2-3 bullets)
- Critical concerns (2-3 bullets)
- Go/No-Go recommendation with conditions

### Detailed Analysis

**For each feasibility dimension:**
1. Score and rationale
2. Key findings
3. Risks identified
4. Recommendations

### Risk Register

| Risk | Category | Likelihood | Impact | Score | Mitigation |
|------|----------|------------|--------|-------|------------|
| | | | | | |

### Recommendations

**If Go:**
- Required actions before starting
- Risk mitigations to implement
- Key success factors
- Monitoring metrics

**If No-Go:**
- Primary blockers
- What would need to change
- Alternative approaches to consider
- Potential pivot options

### Appendices
- Detailed cost estimates
- Technology assessment details
- Competitive analysis data
- Compliance requirements checklist

## Decision Framework Templates

### Technical Feasibility Decision Tree

```
Is core technology production-ready?
├── No → Can we use proven alternatives?
│        ├── No → HIGH RISK / Consider No-Go
│        └── Yes → Evaluate alternatives
└── Yes → Do we have required expertise?
          ├── No → Can we hire/train in time?
          │        ├── No → MEDIUM-HIGH RISK
          │        └── Yes → Add to resource plan
          └── Yes → Are there integration risks?
                    ├── Yes → Prototype integrations early
                    └── No → LOW TECHNICAL RISK
```

### Resource Feasibility Decision Tree

```
Is budget sufficient for scope?
├── No → Can scope be reduced?
│        ├── No → No-Go or find additional funding
│        └── Yes → Reprioritize features
└── Yes → Is team available?
          ├── No → Can we hire in time?
          │        ├── No → Extend timeline or reduce scope
          │        └── Yes → Add hiring to plan
          └── Yes → Is timeline realistic?
                    ├── No → Negotiate deadline or reduce scope
                    └── Yes → RESOURCE FEASIBLE
```

## Best Practices

### Do's
- Use real data and research, not assumptions
- Involve stakeholders in assessment
- Document all assumptions
- Consider multiple scenarios (optimistic, realistic, pessimistic)
- Update feasibility as new information emerges
- Be honest about uncertainties

### Don'ts
- Don't let confirmation bias drive conclusions
- Don't ignore red flags or inconvenient findings
- Don't rely on single points of failure
- Don't assume best-case scenarios
- Don't skip dimensions because they seem "obvious"
- Don't conflate feasibility with desirability

## Final Checklist

Before completing feasibility analysis:

- [ ] All five feasibility dimensions assessed
- [ ] Scores justified with evidence
- [ ] Critical risks identified
- [ ] Go/No-Go criteria applied
- [ ] Recommendations are actionable
- [ ] Assumptions documented
- [ ] Stakeholder input gathered
- [ ] Report reviewed for completeness
