---
id: decision-analysis
name: "Decision Analysis"
domain: BA
skill: faion-business-analyst
category: "business-analysis"
---

# Decision Analysis

## Metadata
- **Category:** BA Framework / Requirements Analysis and Design Definition
- **Difficulty:** Intermediate
- **Tags:** #methodology #babok #decision #analysis #business-analysis
- **Agent:** faion-ba-agent

---

## Problem

Decisions are made based on gut feeling. Options are not properly evaluated. Important criteria are overlooked. Stakeholders disagree because there is no common framework. After implementation, people question why one option was chosen over another.

Without decision analysis:
- Subjective decisions
- Missed alternatives
- No decision justification
- Stakeholder disagreement

---

## Framework

### What is Decision Analysis?

Decision Analysis provides structured approaches to evaluate options and make informed choices. It removes bias and ensures all relevant factors are considered.

### Decision Analysis Steps

```
Define Decision → Identify Options → Define Criteria → Evaluate Options → Make Decision → Document
```

### Step 1: Define the Decision

Clarify what needs to be decided:

| Element | Description |
|---------|-------------|
| **Decision statement** | What specifically is being decided |
| **Objectives** | What we want to achieve |
| **Constraints** | Limitations on options |
| **Decision maker** | Who has authority |
| **Timeline** | When decision is needed |

### Step 2: Identify Options

Generate alternatives:

**Option generation techniques:**
- Brainstorming
- Research (market, competitors)
- Expert consultation
- Past project review
- Stakeholder input

**Include:**
- Obvious options
- Do nothing option
- Innovative alternatives

### Step 3: Define Evaluation Criteria

What matters for this decision?

| Criterion Type | Examples |
|----------------|----------|
| **Cost** | Initial, ongoing, total cost of ownership |
| **Time** | Implementation time, time to value |
| **Risk** | Technical, business, implementation |
| **Capability** | Features, functionality, flexibility |
| **Strategic fit** | Alignment with goals |
| **Operational** | Ease of use, maintenance, support |

**Weighting criteria:**
1. List all criteria
2. Rank by importance
3. Assign weights (total = 100%)

### Step 4: Evaluate Options

Score options against criteria:

| Criterion | Weight | Option A | Option B | Option C |
|-----------|--------|----------|----------|----------|
| Cost | 25% | 4 | 3 | 5 |
| Time | 20% | 3 | 5 | 3 |
| Risk | 20% | 4 | 4 | 2 |
| Features | 20% | 5 | 3 | 4 |
| Support | 15% | 3 | 4 | 4 |
| **Weighted Total** | 100% | 3.85 | 3.70 | 3.55 |

**Scoring scale:** 1 (poor) to 5 (excellent)

### Step 5: Make Recommendation

Based on analysis:
- Present findings
- Highlight key differentiators
- State recommendation with rationale
- Identify risks of recommendation
- Note close alternatives

### Step 6: Document Decision

Record for future reference:
- Decision made
- Options considered
- Criteria and weights
- Evaluation results
- Rationale for selection
- Decision maker and date

---

## Templates

### Decision Analysis Document

```markdown
# Decision Analysis: [Decision Topic]

**Version:** [X.X]
**Date:** [Date]
**Analyst:** [Name]
**Decision Maker:** [Name]
**Decision Needed By:** [Date]

## 1. Decision Context

### Decision Statement
[What specific decision needs to be made]

### Objectives
- [Objective 1]
- [Objective 2]

### Constraints
- [Constraint 1]
- [Constraint 2]

### Background
[Context and why this decision is needed]

## 2. Options Considered

### Option 1: [Name]
- **Description:** [What this option involves]
- **Pros:** [Benefits]
- **Cons:** [Drawbacks]
- **Cost Estimate:** [Range]
- **Timeline:** [Duration]

### Option 2: [Name]
[Same structure]

### Option 3: Do Nothing
- **Description:** Maintain current state
- **Pros:** [Benefits]
- **Cons:** [Drawbacks]

## 3. Evaluation Criteria

| Criterion | Weight | Definition | Scale |
|-----------|--------|------------|-------|
| [Criterion] | [X%] | [What it means] | [How to score] |

## 4. Evaluation Matrix

| Criterion | Weight | Option 1 | Option 2 | Option 3 |
|-----------|--------|----------|----------|----------|
| [Criterion 1] | [X%] | [Score] | [Score] | [Score] |
| [Criterion 2] | [X%] | [Score] | [Score] | [Score] |
| **Weighted Total** | 100% | **[Total]** | **[Total]** | **[Total]** |

## 5. Analysis

### Key Findings
- [Finding 1]
- [Finding 2]

### Sensitivity Analysis
[How results change if weights change]

### Risks

| Option | Key Risks | Mitigation |
|--------|-----------|------------|
| [Option] | [Risks] | [Mitigation] |

## 6. Recommendation

**Recommended Option:** [Option X]

**Rationale:**
[Why this option is recommended]

**Key Advantages:**
- [Advantage 1]
- [Advantage 2]

**Key Risks:**
- [Risk 1 and mitigation]
- [Risk 2 and mitigation]

## 7. Approval

| Role | Name | Decision | Date |
|------|------|----------|------|
| Decision Maker | | Approve/Reject | |

**Final Decision:** [What was decided]
```

### Simple Decision Matrix

```markdown
# Decision Matrix: [Topic]

**Decision:** [What is being decided]
**Date:** [Date]

## Options
1. [Option 1]
2. [Option 2]
3. [Option 3]

## Criteria and Weights
| Criterion | Weight | Why Important |
|-----------|--------|---------------|
| [Criterion] | [%] | [Reason] |

## Evaluation (1-5 scale)

| Criterion | Wt | Opt 1 | Opt 2 | Opt 3 |
|-----------|----|-------|-------|-------|
| | | | | |
| **Total** | | **X.XX** | **X.XX** | **X.XX** |

## Decision
**Selected:** [Option]
**Reason:** [Brief rationale]
```

---

## Examples

### Example 1: CRM Selection

**Decision:** Select CRM platform for sales team

**Options:**
1. Salesforce - Enterprise, full-featured
2. HubSpot - Mid-market, marketing integration
3. Pipedrive - Sales-focused, simple

**Criteria and Evaluation:**

| Criterion | Weight | Salesforce | HubSpot | Pipedrive |
|-----------|--------|------------|---------|-----------|
| Features | 25% | 5 | 4 | 3 |
| Cost (inverse) | 25% | 2 | 4 | 5 |
| Ease of use | 20% | 3 | 4 | 5 |
| Integration | 15% | 5 | 4 | 3 |
| Support | 15% | 4 | 4 | 3 |
| **Total** | 100% | **3.55** | **4.00** | **3.85** |

**Recommendation:** HubSpot - best balance of features, cost, and usability

### Example 2: Build vs Buy

**Decision:** Build custom solution or buy commercial product?

**Criteria:**
- Time to market (30%)
- Total cost 3-year (25%)
- Customization needs (25%)
- Risk (20%)

**Analysis:**

| Factor | Build | Buy |
|--------|-------|-----|
| Time to market | 12 months | 3 months |
| 3-year cost | $400K | $300K |
| Customization | Full control | Limited |
| Risk | Higher (new dev) | Lower (proven) |

**Decision:** Buy - faster time to market outweighs customization limitations

---

## Common Mistakes

1. **Predetermined conclusion** - Analysis done to justify decision already made
2. **Missing options** - Not considering all alternatives
3. **Equal weights** - All criteria treated same importance
4. **No documentation** - Decision rationale lost
5. **Ignoring risks** - Only looking at benefits

---

## Decision Analysis Techniques

| Technique | Best For |
|-----------|----------|
| **Decision matrix** | Multiple options, multiple criteria |
| **Pros/cons list** | Simple decisions, quick analysis |
| **Cost-benefit analysis** | Financial decisions |
| **Decision tree** | Sequential decisions, uncertainty |
| **Pugh matrix** | Comparing to baseline option |
| **SWOT** | Strategic options |

---

## Sensitivity Analysis

Test how robust your decision is:

1. Change weights (+/- 10%)
2. Recalculate scores
3. Check if recommendation changes

If small weight changes flip the recommendation, decision is sensitive and needs more analysis.

---

## Next Steps

After decision analysis:
1. Present to decision maker
2. Get formal decision
3. Document rationale
4. Communicate decision
5. Connect to Use Case Modeling methodology

---

## References

- BA Framework Guide v3 - Requirements Analysis and Design Definition
- BA industry Decision Analysis Guidelines
