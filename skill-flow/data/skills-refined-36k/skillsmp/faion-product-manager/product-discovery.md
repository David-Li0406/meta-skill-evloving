---
id: product-discovery
name: "Product Discovery"
domain: PRD
skill: faion-product-manager
category: "product"
---

# Product Discovery

## Metadata

| Field | Value |
|-------|-------|
| **ID** | (semantic) |
| **Category** | Product |
| **Difficulty** | Intermediate |
| **Tags** | #product, #discovery, #validation |
| **Domain Skill** | faion-product-manager |
| **Agents** | faion-idea-generator-agent |

---

## Problem

Teams jump from idea to building without validating assumptions. Issues:
- Building features nobody wants
- Wasted engineering time
- Discovering problems after launch
- No learning culture

**The root cause:** No structured process to de-risk ideas before committing resources.

---

## Framework

### What is Product Discovery?

Product discovery is the process of identifying and validating what to build BEFORE building it. It answers four key questions:

1. **Value Risk:** Will customers buy/use it?
2. **Usability Risk:** Can customers figure it out?
3. **Feasibility Risk:** Can we build it?
4. **Business Viability Risk:** Does it work for our business?

### Discovery vs Delivery

| Discovery | Delivery |
|-----------|----------|
| Find the right thing to build | Build the thing right |
| Reduce risk | Execute efficiently |
| Fast experimentation | Quality implementation |
| Cheap to fail | Expensive to change |
| Output: Validated ideas | Output: Working software |

**Rule:** Spend 20-30% of capacity on discovery.

### Discovery Techniques

#### For Value Risk

| Technique | Effort | Confidence | When to Use |
|-----------|--------|------------|-------------|
| Customer interviews | Low | Medium | Early ideas |
| Surveys | Low | Low | Large scale validation |
| Fake door tests | Low | Medium | Testing demand |
| Concierge MVP | Medium | High | Service-based products |
| Wizard of Oz | Medium | High | Complex features |
| Prototype testing | Medium | Medium | UX validation |
| Landing page | Low | Medium | Market interest |

#### For Usability Risk

| Technique | Effort | Confidence | When to Use |
|-----------|--------|------------|-------------|
| Paper prototypes | Low | Low | Early concepts |
| Clickable prototypes | Medium | Medium | Flow validation |
| Usability testing | Medium | High | Design validation |
| A/B testing | High | Very High | Optimization |

#### For Feasibility Risk

| Technique | Effort | Confidence | When to Use |
|-----------|--------|------------|-------------|
| Technical spike | Low-Med | High | Unknown tech |
| Architecture review | Low | Medium | System impact |
| Proof of concept | Medium | High | Critical features |
| Vendor evaluation | Low | Medium | Third-party dependencies |

#### For Business Risk

| Technique | Effort | Confidence | When to Use |
|-----------|--------|------------|-------------|
| Financial modeling | Low | Medium | Revenue impact |
| Competitive analysis | Low | Medium | Market fit |
| Stakeholder interviews | Low | Medium | Internal alignment |
| Pilot program | High | Very High | Major investments |

### Discovery Process

#### Step 1: Identify Assumptions

List everything you're assuming:
- Users have this problem
- Users will pay for solution
- We can build it in X time
- It won't break existing features

**Template:**
```
Assumption: [Statement]
Risk level: [High/Medium/Low]
Validation method: [How to test]
```

#### Step 2: Prioritize Risks

**Focus on:**
- High-risk assumptions
- Things that would kill the idea if wrong
- Things that are easy to test

#### Step 3: Design Experiments

**Experiment template:**
```
Hypothesis: [If we do X, we expect Y]
Test: [How we'll test]
Success criteria: [What number means success]
Timeline: [How long to run]
Resources: [What we need]
```

#### Step 4: Run and Learn

- Execute experiments
- Collect data
- Make decisions
- Document learnings

#### Step 5: Decide

| Signal | Decision |
|--------|----------|
| All risks addressed | Proceed to delivery |
| Critical risk not validated | Pivot or kill |
| Partial validation | More discovery needed |

---

## Templates

### Discovery Kickoff

```markdown
## Discovery: [Feature/Product Name]

### Context
**Opportunity:** [What we're exploring]
**Trigger:** [Why now]
**Timeline:** [Discovery period]

### Team
- Product: [Name]
- Design: [Name]
- Engineering: [Name]

### Core Questions
1. [Key question about value]
2. [Key question about usability]
3. [Key question about feasibility]
4. [Key question about business]

### Assumptions to Test

| Assumption | Risk | Method | Owner |
|------------|------|--------|-------|
| [Assumption 1] | High | [Method] | [Name] |
| [Assumption 2] | Medium | [Method] | [Name] |

### Success Criteria
Discovery is successful when we can answer:
- [ ] [Question 1]
- [ ] [Question 2]
- [ ] [Question 3]

### Schedule
- Week 1: [Activities]
- Week 2: [Activities]
- Week 3: [Decision meeting]
```

### Experiment Report

```markdown
## Experiment: [Name]

### Hypothesis
We believe [assumption].
We will test by [method].
We'll know we're right when [metric].

### Setup
- **Duration:** [X days]
- **Sample size:** [N users]
- **Method:** [Details]

### Results

| Metric | Target | Actual | Result |
|--------|--------|--------|--------|
| [Metric 1] | [X] | [Y] | Pass/Fail |
| [Metric 2] | [X] | [Y] | Pass/Fail |

### Observations
- [Observation 1]
- [Observation 2]

### Learnings
- [Key insight 1]
- [Key insight 2]

### Decision
[ ] Validated - proceed to build
[ ] Invalidated - pivot
[ ] Unclear - need more data

### Next Steps
- [Action 1]
- [Action 2]
```

---

## Examples

### Example 1: New Feature Discovery

**Feature idea:** AI-powered writing assistant

**Assumptions tested:**
| Assumption | Test | Result |
|------------|------|--------|
| Users struggle with writing | 10 interviews | Validated (8/10) |
| Users would use AI for help | Fake door test | 15% click rate (validated) |
| We can build accurate AI | Technical spike | Possible but 2 months work |
| Users will pay for it | Pricing survey | $10/mo acceptable |

**Decision:** Proceed with MVP, target 4-week delivery.

### Example 2: Market Expansion Discovery

**Opportunity:** Enter German market

**Assumptions tested:**
| Assumption | Test | Result |
|------------|------|--------|
| Same product works in DE | Customer interviews | Needs localization |
| Payment methods work | Technical research | Need local payment options |
| Support can handle German | Team assessment | Need German-speaking agent |
| Market size justifies effort | Market research | $5M SAM, viable |

**Decision:** Proceed with localization plan, 8-week timeline.

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Skipping discovery | Budget 20-30% for discovery |
| Only asking customers | Combine methods for confidence |
| Confirmation bias | Seek disconfirming evidence |
| Taking too long | Timebox discovery (1-4 weeks) |
| Not documenting | Write up all learnings |
| Discovery theater | Focus on decisions, not process |
| Building during discovery | Keep experiments cheap |

---

## Related Methodologies

- **problem-validation:** Problem Validation
- **feature-discovery:** Feature Discovery
- **mvp-scoping:** MVP Scoping
- **usability-testing:** Usability Testing
- **ab-testing-framework:** A/B Testing Framework

---

## Agent

**faion-idea-generator-agent** helps with discovery. Invoke with:
- "Plan discovery for [feature idea]"
- "What assumptions should I test for [product]?"
- "Design an experiment for [hypothesis]"
- "Help me analyze [experiment results]"

---

*Methodology | Product | Version 1.0*
