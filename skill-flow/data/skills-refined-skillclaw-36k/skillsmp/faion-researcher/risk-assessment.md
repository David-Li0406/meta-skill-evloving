---
id: risk-assessment
name: "Risk Assessment"
domain: RES
skill: faion-researcher
category: "research"
---

# Risk Assessment

## Metadata

| Field | Value |
|-------|-------|
| **ID** | (semantic) |
| **Category** | Research |
| **Difficulty** | Intermediate |
| **Tags** | #research, #risk, #planning |
| **Domain Skill** | faion-researcher |
| **Agents** | faion-market-researcher-agent |

---

## Problem

Entrepreneurs are often blindly optimistic or paralyzed by fear. Common issues:
- Not identifying risks until they hit
- No contingency plans
- Underestimating probability or impact
- Overcomplicating risk management

**The root cause:** No structured process for identifying and managing business risks.

---

## Framework

### What is Risk Assessment?

Risk assessment is identifying, analyzing, and planning for potential threats to your business. It answers: "What could go wrong and how do we handle it?"

### Risk Categories

#### 1. Market Risks

| Risk | Description | Examples |
|------|-------------|----------|
| Demand | No one wants it | Market too small, poor timing |
| Competition | Others win | Incumbent copies, well-funded rival |
| Pricing | Can't make money | Commoditization, price war |
| Trend | Market shifts | Technology obsolescence |

#### 2. Product Risks

| Risk | Description | Examples |
|------|-------------|----------|
| Technical | Can't build it | Complexity, dependencies |
| Usability | Users can't use it | Poor UX, learning curve |
| Value | Doesn't solve problem | Feature gaps, wrong solution |
| Quality | Doesn't work well | Bugs, performance issues |

#### 3. Team Risks

| Risk | Description | Examples |
|------|-------------|----------|
| Skills | Lack capabilities | Missing expertise |
| Capacity | Not enough bandwidth | Founder burnout, solo limits |
| Alignment | Different goals | Co-founder conflict |
| Dependency | Key person risk | Single point of failure |

#### 4. Financial Risks

| Risk | Description | Examples |
|------|-------------|----------|
| Runway | Running out of money | Cash burn too high |
| Revenue | Can't generate income | Monetization fails |
| Costs | Expenses too high | Infrastructure, CAC |
| External | Economic downturn | Recession, funding winter |

#### 5. Operational Risks

| Risk | Description | Examples |
|------|-------------|----------|
| Vendor | Dependency fails | API discontinued, pricing change |
| Legal | Compliance issues | GDPR, copyright, licensing |
| Security | Data breach | Hack, data loss |
| Scale | Can't handle growth | Infrastructure breaks |

### Risk Assessment Process

#### Step 1: Identify Risks

**Brainstorming questions:**
- What could stop us from succeeding?
- What assumptions are we making?
- What's happened to similar businesses?
- What keeps me up at night?
- What do skeptics say?

**Use categories above as a checklist.**

#### Step 2: Analyze Each Risk

**Risk matrix:**

```
          IMPACT
          High     Medium    Low
    High │  RED    │ ORANGE │ YELLOW │
PROB Med │ ORANGE  │ YELLOW │ GREEN  │
    Low  │ YELLOW  │ GREEN  │ GREEN  │
```

**Scoring:**

| Probability | Score | Meaning |
|-------------|-------|---------|
| High | 3 | >50% chance |
| Medium | 2 | 20-50% chance |
| Low | 1 | <20% chance |

| Impact | Score | Meaning |
|--------|-------|---------|
| High | 3 | Existential threat |
| Medium | 2 | Major setback |
| Low | 1 | Minor inconvenience |

**Risk Score = Probability × Impact**

#### Step 3: Plan Responses

**Response strategies:**

| Strategy | Description | When to Use |
|----------|-------------|-------------|
| Avoid | Eliminate the risk | High prob, high impact |
| Mitigate | Reduce prob or impact | Medium risks |
| Transfer | Shift to someone else | Insurance, contracts |
| Accept | Live with it | Low risks |

#### Step 4: Create Contingency Plans

**For high-priority risks:**
```
Risk: [Description]
Trigger: [When do we know it's happening]
Response: [What we'll do]
Owner: [Who's responsible]
Resources: [What we need]
```

#### Step 5: Monitor and Review

**Review cadence:**
- Weekly: Top 3 risks
- Monthly: Full risk register
- Quarterly: Deep review, update assumptions

---

## Templates

### Risk Register

```markdown
## Risk Register: [Product/Business]

### Last Updated: [Date]
### Review Cadence: [Frequency]

### High Priority Risks

| ID | Risk | Category | Prob | Impact | Score | Status |
|----|------|----------|------|--------|-------|--------|
| R1 | [Risk] | [Cat] | H | H | 9 | Mitigating |
| R2 | [Risk] | [Cat] | H | M | 6 | Monitoring |

### Medium Priority Risks

| ID | Risk | Category | Prob | Impact | Score | Status |
|----|------|----------|------|--------|-------|--------|
| R3 | [Risk] | [Cat] | M | M | 4 | Accepted |

### Low Priority Risks

| ID | Risk | Category | Prob | Impact | Score | Status |
|----|------|----------|------|--------|-------|--------|
| R4 | [Risk] | [Cat] | L | L | 1 | Accepted |

### Risk Matrix View

```
          IMPACT
          High     Med      Low
    High │ R1     │ R2     │        │
PROB Med │        │ R3     │        │
    Low  │        │        │ R4     │
```

### Response Plans

#### R1: [Risk Name]
**Strategy:** [Avoid/Mitigate/Transfer/Accept]
**Actions:**
1. [Action 1] - Owner: [Name] - Due: [Date]
2. [Action 2] - Owner: [Name] - Due: [Date]

**Contingency Plan:**
- Trigger: [What signals this is happening]
- Response: [What we'll do]
- Resources needed: [What we'll need]

**Progress:** [Current status]

---

#### R2: [Risk Name]
...
```

### Pre-Mortem Template

```markdown
## Pre-Mortem: [Project/Launch]

### Setup
Imagine it's [future date] and this project has FAILED completely.

### What Went Wrong?

**Each participant writes independently (5 min):**
[What caused the failure?]

### Consolidated Failure Modes

| Failure Mode | Mentioned By | Category |
|--------------|--------------|----------|
| [Mode 1] | [X] people | [Cat] |
| [Mode 2] | [X] people | [Cat] |

### Risk Conversion

| Failure Mode | Risk Statement | Prob | Impact |
|--------------|----------------|------|--------|
| [Mode 1] | [As risk] | [H/M/L] | [H/M/L] |

### Mitigation Actions

| Risk | Mitigation | Owner |
|------|------------|-------|
| [Risk] | [Action] | [Name] |

### Go/No-Go Decision
After review:
[ ] Proceed with mitigations
[ ] Delay until [condition]
[ ] Cancel project
```

---

## Examples

### Example 1: SaaS Startup Risks

**Top risks identified:**

| Risk | Prob | Impact | Response |
|------|------|--------|----------|
| No product-market fit | H | H | Intensive customer development |
| Key engineer leaves | M | H | Documentation, equity vesting |
| AWS costs spike | M | M | Cost monitoring, reserved instances |
| Competitor launches | M | M | Speed to market, differentiation |
| GDPR non-compliance | L | H | Legal review, privacy by design |

**Contingency for R1 (No PMF):**
- Trigger: <20 paying customers after 6 months
- Response: Pivot to adjacent problem or different segment
- Runway needed: 3 months buffer

### Example 2: Content Business Risks

**Top risks identified:**

| Risk | Prob | Impact | Response |
|------|------|--------|----------|
| Platform algorithm change | H | H | Email list building, diversification |
| Creator burnout | M | H | Batch content, hire support |
| Payment processor drops us | L | H | Multiple payment options |
| Piracy/content theft | M | L | Watermarking, community value |

**Contingency for R1 (Platform change):**
- Trigger: >30% drop in organic reach
- Response: Shift budget to email, community, paid ads
- Resources: 3 months content backlog, ad budget

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Ignoring risks | Schedule regular risk reviews |
| Too many risks | Focus on top 5-10 |
| No contingencies | Every high risk needs a plan |
| Static assessment | Update monthly minimum |
| Optimism bias | Get outside perspectives |
| Paralysis | Accept some risks, take action |
| Not tracking | Assign owners, review progress |

---

## Related Methodologies

- **niche-evaluation:** Niche Evaluation
- **business-model-research:** Business Model Research
- **mvp-scoping:** MVP Scoping
- **risk-management:** Risk Management
- **quality-gates-confidence:** Quality Gates & Confidence

---

## Agent

**faion-market-researcher-agent** helps with risk assessment. Invoke with:
- "What are the risks for [business idea]?"
- "Create a risk register for [project]"
- "Run a pre-mortem for [launch]"
- "How should I mitigate [risk]?"

---

*Methodology | Research | Version 1.0*
