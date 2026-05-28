---
id: procurement-management
name: "Procurement Management"
domain: PM
skill: faion-project-manager
category: "project-management"
---

# Procurement Management

## Metadata
- **Category:** Project Management Framework / Delivery Performance Domain
- **Difficulty:** Intermediate
- **Tags:** #methodology #pmbok #procurement #vendors #contracts #project-management
- **Agent:** faion-pm-agent

---

## Problem

You need external help but do not know how to engage vendors properly. Contracts are vague, leading to disputes. Vendors underdeliver or overcharge. You are locked into bad agreements. Procurement delays hold up the entire project.

Without procurement management:
- Poor vendor selection
- Unclear deliverables
- Cost overruns
- Legal disputes
- Dependency on unreliable suppliers

---

## Framework

### Step 1: Make-or-Buy Decision

For each need, decide: build internally or buy externally?

| Factor | Make (Internal) | Buy (External) |
|--------|-----------------|----------------|
| **Cost** | Higher fixed cost | Variable cost |
| **Control** | Full control | Less control |
| **Speed** | May be slower | Often faster |
| **Expertise** | Limited to team | Access to specialists |
| **Risk** | Internal risk | Shared/transferred risk |

### Step 2: Define Requirements

Write a clear Statement of Work (SOW):

| Element | Description |
|---------|-------------|
| **Scope** | What exactly is needed |
| **Deliverables** | Tangible outputs |
| **Timeline** | Start date, milestones, end date |
| **Acceptance criteria** | How to verify completion |
| **Constraints** | Limitations and requirements |

### Step 3: Select Contract Type

| Type | Description | Risk | When to Use |
|------|-------------|------|-------------|
| **Fixed Price** | Set price for defined scope | Buyer risk low | Clear requirements |
| **Time & Materials** | Pay for hours + expenses | Buyer risk high | Unclear scope |
| **Cost Plus** | Cost + agreed margin | Buyer risk very high | Research, innovation |

### Step 4: Source Vendors

**Sourcing methods:**
- Request for Information (RFI) - gather market info
- Request for Proposal (RFP) - formal proposals with solutions
- Request for Quote (RFQ) - price quotes for defined work
- Sole source - direct engagement (if justified)

**Evaluation criteria:**

| Criterion | Weight | Vendor A | Vendor B |
|-----------|--------|----------|----------|
| Price | 30% | 85 | 90 |
| Experience | 25% | 90 | 80 |
| Technical approach | 25% | 85 | 85 |
| Timeline | 10% | 80 | 90 |
| References | 10% | 90 | 75 |
| **Weighted Total** | 100% | **86.5** | **84.5** |

### Step 5: Negotiate and Contract

**Key contract elements:**
- Scope and deliverables
- Price and payment terms
- Timeline and milestones
- Change process
- Acceptance criteria
- Warranties and guarantees
- Termination clauses
- Intellectual property rights
- Confidentiality

### Step 6: Manage Vendors

**Ongoing activities:**
- Track deliverables against plan
- Review invoices and payments
- Conduct regular status meetings
- Address issues promptly
- Document changes formally
- Evaluate performance

---

## Templates

### Statement of Work (SOW) Template

```markdown
# Statement of Work: [Project/Service Name]

**Version:** [X.X]
**Date:** [Date]
**Buyer:** [Company]
**Contract Reference:** [Number]

## 1. Background
[Context and reason for this work]

## 2. Scope of Work
[Detailed description of what is required]

### In Scope
- [Item 1]
- [Item 2]

### Out of Scope
- [Exclusion 1]
- [Exclusion 2]

## 3. Deliverables

| ID | Deliverable | Description | Due Date |
|----|-------------|-------------|----------|
| D1 | [Name] | [Description] | [Date] |
| D2 | [Name] | [Description] | [Date] |

## 4. Acceptance Criteria
[How each deliverable will be evaluated]

## 5. Timeline

| Milestone | Date | Deliverables |
|-----------|------|--------------|
| Kickoff | [Date] | - |
| [Milestone] | [Date] | D1 |
| Completion | [Date] | All |

## 6. Assumptions
- [Assumption 1]
- [Assumption 2]

## 7. Dependencies
- [Buyer will provide X]
- [Access to Y required]

## 8. Payment Terms
[Payment schedule tied to milestones]
```

### Vendor Evaluation Matrix

```markdown
# Vendor Evaluation: [Procurement Name]

**Date:** [Date]
**Evaluators:** [Names]

## Scoring Scale
1 = Poor, 2 = Below Average, 3 = Average, 4 = Good, 5 = Excellent

## Evaluation

| Criterion | Weight | Vendor A | Vendor B | Vendor C |
|-----------|--------|----------|----------|----------|
| Technical Capability | 25% | | | |
| Relevant Experience | 20% | | | |
| Price | 25% | | | |
| Timeline | 15% | | | |
| Team Quality | 10% | | | |
| References | 5% | | | |
| **Weighted Score** | 100% | | | |

## Recommendation
[Which vendor and why]

## Risks
[Identified risks with recommended vendor]
```

---

## Examples

### Example 1: Development Agency Selection

**Need:** Mobile app development (iOS and Android)

**SOW highlights:**
- Deliverables: Design mockups, working app, source code
- Timeline: 12 weeks
- Acceptance: App Store approval, 95% crash-free

**Evaluation result:**

| Vendor | Score | Strengths | Weaknesses |
|--------|-------|-----------|------------|
| Agency A | 88 | Strong portfolio, local | Highest price |
| Agency B | 82 | Lowest price | Limited iOS experience |
| Agency C | 79 | Fast timeline | Poor references |

**Decision:** Agency A selected for quality and reliability.

### Example 2: Cloud Hosting Contract

**Contract type:** Time & Materials with cap

**Terms:**
- Hourly rate: $150 for senior, $100 for junior
- Monthly cap: $15,000
- Scope: Infrastructure setup and ongoing support
- Change process: Written approval for scope changes

---

## Common Mistakes

1. **Vague SOW** - Leads to scope disputes
2. **Lowest price wins** - Ignoring quality and risk
3. **No change process** - Scope creep without control
4. **Poor vendor management** - Set and forget
5. **Missing exit clause** - Trapped with bad vendor

---

## Contract Types Deep Dive

### Fixed Price
```
Total cost: $50,000
Payment: 25% at start, 50% at milestone, 25% at completion
Risk: Vendor bears cost overrun risk
Best for: Well-defined scope, clear deliverables
```

### Time and Materials
```
Rate: $100/hour
Estimate: 400-500 hours
Cap: $55,000 (optional)
Risk: Buyer bears cost risk
Best for: Unclear scope, evolving requirements
```

### Cost Plus Fixed Fee
```
Cost: Actual expenses
Fee: $10,000 fixed
Risk: Buyer bears all cost risk
Best for: Research, highly uncertain work
```

---

## Next Steps

After procurement planning:
1. Get legal/finance review of contracts
2. Establish vendor communication protocols
3. Set up invoice processing
4. Schedule regular check-ins
5. Connect to Lessons Learned methodology

---

## References

- Project Management Framework Guide 7th Edition - Delivery Performance Domain
- PM industry practice standard for Project Procurement Management
