---
id: product-lifecycle
name: "Product Lifecycle Management"
domain: PRD
skill: faion-product-manager
category: "product"
---

# Product Lifecycle Management

## Metadata

| Field | Value |
|-------|-------|
| **ID** | (semantic) |
| **Category** | Product |
| **Difficulty** | Intermediate |
| **Tags** | #product, #lifecycle, #strategy |
| **Domain Skill** | faion-product-manager |
| **Agents** | faion-mlp-impl-planner-agent |

---

## Problem

Products are managed the same way regardless of maturity stage. Issues:
- Growth tactics applied to declining products
- Maturity investments in early products
- No exit strategy for end-of-life
- Resource misallocation

**The root cause:** No recognition that different lifecycle stages require different strategies.

---

## Framework

### Product Lifecycle Stages

```
Revenue
   ↑
   │                    ┌─────────┐
   │                   /           \
   │                  /    Maturity \
   │                 /               \
   │         Growth /                 \ Decline
   │               /                   \
   │   Introduction                     \
   │  ──────────────                     ────────
   └──────────────────────────────────────────────→ Time
```

### Stage Characteristics

#### 1. Introduction

**Characteristics:**
- Low revenue, negative profit
- Early adopters only
- High uncertainty
- Frequent pivots

**Focus:**
- Product-market fit
- Learning and iteration
- Core feature refinement
- User feedback

**Metrics:**
- Activation rate
- Retention (early)
- NPS from early users

#### 2. Growth

**Characteristics:**
- Rapidly increasing revenue
- Market acceptance
- Competition increasing
- Scaling challenges

**Focus:**
- Customer acquisition
- Feature expansion
- Team growth
- Infrastructure scaling

**Metrics:**
- Growth rate
- CAC, LTV
- Market share
- Revenue

#### 3. Maturity

**Characteristics:**
- Stable/slowing revenue
- Market saturation
- Intense competition
- Optimization focus

**Focus:**
- Efficiency
- Retention
- Incremental improvements
- Cost optimization

**Metrics:**
- Profitability
- Churn
- NPS
- Efficiency ratios

#### 4. Decline

**Characteristics:**
- Decreasing revenue
- Technology shift
- Customer migration
- Resource reallocation

**Focus:**
- Cash harvesting
- Managed decline
- Migration support
- Sunset planning

**Metrics:**
- Cash flow
- Migration rate
- Support cost
- Timeline to sunset

### Stage-Appropriate Strategies

| Stage | Product | Marketing | Operations |
|-------|---------|-----------|------------|
| Intro | MVP, iteration | Awareness | Lean |
| Growth | Features, scale | Acquisition | Build team |
| Maturity | Optimize, extend | Retention | Efficiency |
| Decline | Maintenance | Migration | Wind down |

### Lifecycle Management Process

#### Step 1: Assess Current Stage

**Indicators:**

| Stage | Growth Rate | Profitability | Competition |
|-------|-------------|---------------|-------------|
| Intro | Low/negative | Negative | Low |
| Growth | 20%+ YoY | Improving | Increasing |
| Maturity | <10% YoY | Peak | High |
| Decline | Negative | Declining | Shifting |

#### Step 2: Validate Stage

- Review metrics trends (3+ quarters)
- Compare to market
- Consider external factors
- Get team alignment

#### Step 3: Apply Stage Strategy

**Match activities to stage:**
- Right investments
- Right metrics
- Right team focus
- Right expectations

#### Step 4: Plan Transitions

**Anticipate:**
- What triggers next stage?
- What needs to change?
- What new capabilities needed?
- What to stop doing?

---

## Templates

### Lifecycle Assessment

```markdown
## Lifecycle Assessment: [Product]

### Current Metrics

| Metric | Last Year | Current | Trend |
|--------|-----------|---------|-------|
| Revenue | $X | $Y | +/- X% |
| Growth rate | X% | Y% | +/- |
| Profitability | X% | Y% | +/- |
| Market share | X% | Y% | +/- |
| NPS | X | Y | +/- |

### Stage Indicators

| Indicator | Intro | Growth | Maturity | Decline |
|-----------|-------|--------|----------|---------|
| Growth rate | | [X] | | |
| Profitability | | | [X] | |
| Competition | | [X] | | |
| Innovation | [X] | | | |

### Assessed Stage: [Stage]

**Confidence:** [High/Medium/Low]
**Rationale:** [Why this stage]

### Stage-Appropriate Actions

**Should do:**
- [Action aligned with stage]
- [Action aligned with stage]

**Should stop:**
- [Action not appropriate for stage]
- [Action not appropriate for stage]

### Transition Planning

**Next stage trigger:** [What signals transition]
**Timeline estimate:** [When expected]
**Preparation needed:** [What to build/change]
```

### Stage Strategy Guide

```markdown
## Strategy: [Stage] Stage

### Focus Areas
1. [Primary focus]
2. [Secondary focus]
3. [Tertiary focus]

### Key Metrics
| Metric | Current | Target | Timeframe |
|--------|---------|--------|-----------|
| [Metric] | [X] | [Y] | [When] |

### Investment Priorities
| Area | Level | Rationale |
|------|-------|-----------|
| Product dev | [High/Med/Low] | [Why] |
| Marketing | [High/Med/Low] | [Why] |
| Sales | [High/Med/Low] | [Why] |
| Support | [High/Med/Low] | [Why] |

### Risks to Manage
- [Stage-specific risk]
- [Stage-specific risk]

### Success Criteria
[How we know this stage is successful]

### Transition Triggers
[What signals move to next stage]
```

---

## Examples

### Example 1: SaaS Product in Growth

**Assessment:**
- 40% YoY growth
- Just reached profitability
- 3 new competitors entered market
- Stage: **Growth**

**Strategy:**
- Accelerate customer acquisition
- Expand feature set for enterprise
- Build sales team
- Invest in infrastructure

**Transition trigger:** Growth slows to <15% YoY

### Example 2: Legacy Product in Decline

**Assessment:**
- -10% YoY revenue
- Customers migrating to new platform
- Technology becoming outdated
- Stage: **Decline**

**Strategy:**
- Maintain core functionality only
- Help customers migrate
- Reduce support costs
- Plan sunset timeline

**End goal:** Complete migration in 18 months

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Ignoring lifecycle stage | Regular assessment |
| Growth tactics in decline | Match strategy to stage |
| No transition planning | Anticipate next stage |
| Same metrics for all | Stage-appropriate KPIs |
| Emotional attachment | Data-driven decisions |
| Sudden changes | Gradual transitions |
| No sunset plan | Plan end-of-life early |

---

## Related Methodologies

- **roadmap-design:** Roadmap Design
- **trend-analysis:** Trend Analysis
- **business-model-research:** Business Model Research
- **aarrr-pirate-metrics:** AARRR Pirate Metrics
- **gtm-strategy:** GTM Strategy

---

## Agent

**faion-mlp-impl-planner-agent** helps with lifecycle. Invoke with:
- "What lifecycle stage is [product] in?"
- "What strategy fits [lifecycle stage]?"
- "Plan transition from [stage] to [stage]"
- "Create a sunset plan for [product]"

---

*Methodology | Product | Version 1.0*
