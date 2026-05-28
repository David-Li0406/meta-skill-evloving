---
name: product-strategy
description: Write product strategy documents for Viya TMS product teams. Uses Playing to Win framework, cascading from company strategy to team-level strategic choices.
---

# Product Strategy Skill

Write product strategy documents for Viya TMS product teams. Cascades company-level strategy (Playing to Win framework) into actionable team-level strategies with clear choices, trade-offs, and success metrics.

## Trigger

When user asks to:
- Write a product strategy for a team/product area
- Define strategic choices for a product
- Create a product vision and strategy document
- Cascade company strategy to product teams
- Review or improve an existing product strategy

## Context: Viya TMS

Viya is a cloud-based Transportation Management System (TMS) for B2B shippers.

### Company Strategy (Playing to Win)

| Component | Definition |
|-----------|------------|
| **Winning Aspiration** | €12M ARR in Europe, improve daily work lives of 10,000 logistics professionals |
| **Where to Play** | Enterprise (€10M+ transport spend), Mid-market (50+ employees), European B2B shippers, general cargo, manufacturing/spare-parts/life sciences |
| **How to Win** | Human-centred design, automation without complexity, customer journey exception handling, European cross-border expertise |
| **Core Capabilities** | Automation & workflow engine, UX & design, analytics, integrations, cross-border expertise, customer success |

### Product Teams

| Team | Audience | Focus |
|------|----------|-------|
| **Shipping / Consignment** | Warehouse / Logistics Analyst | Make complex shipping flows easy |
| **Visibility / Tracking / Reporting** | Customer Service / Logistics Manager | Exception handling and insights |
| **Freight Settlement / Rates** | Financial Manager / Logistics Analyst | Cost optimization and accuracy |
| **Carrier Portal** | Carriers | Easier collaboration with Viya |

## Process

### Step 1: Identify the Product Area

Confirm with user:
1. **Product team**: Which of the four teams (or a new area)?
2. **Scope**: Full strategy | Strategy refresh | Specific section
3. **Current state**: Starting fresh | Has existing vision | Has partial strategy

If unclear, ask:
> "Which product area are we creating a strategy for? (Shipping/Consignment, Visibility/Tracking, Freight Settlement, or Carrier Portal)"

### Step 2: Gather Strategic Context

**2a. Load company strategy**
Read the company strategy to ensure alignment:
- `knowledgebase/strategy/Strategy 2025-2030*.md`
- `knowledgebase/vision/Mission & Vision.md`

**2b. Check existing research**
```javascript
memory({ mode: "search", query: "<product area> strategy", tags: ["product-strategy"] })
```

**2c. Understand current state**
Ask about:
- Current product vision (if any)
- Key customer segments served
- Main competitors/alternatives
- Recent customer feedback or pain points
- Team composition and capabilities

### Step 3: Facilitate Strategic Choices

Guide the user through each strategic choice using Socratic questions:

**3a. Product Vision**
> "In 3 years, what future state does [product area] create for users? Complete this: 'A world where logistics professionals can...'"

**3b. Target Users & Problems**
> "Who are the 2-3 specific user personas? What are their top 3 pain points that keep them up at night?"

**3c. Strategic Bets**
> "If you could only solve 3 problems in the next year, which would have the biggest impact on the company's winning aspiration?"

**3d. How to Win**
> "What would make users choose Viya's [product area] over alternatives? What's hard for competitors to copy?"

**3e. What We're NOT Doing**
> "What requests or ideas are you explicitly saying no to? What adjacent problems will you NOT solve?"

### Step 4: Apply Strategy Frameworks

Use these frameworks to strengthen the strategy:

**Playing to Win Cascade**
Ensure each product choice reinforces the company-level choices:
- Does the product's "where to play" fit within company segments?
- Does "how to win" leverage company capabilities?
- Do capabilities build on existing strengths?

**DHM Model (Delight + Hard-to-Copy + Margin)**
For each strategic bet, ask:
- How does this **delight** users? (What's the "wow"?)
- Why is this **hard to copy**? (Moat: brand, network effects, data, technology, switching costs)
- Does this protect or improve **margin**?

**The "Opposite Test"**
For each strategic choice, check: "Is the opposite a viable strategy someone else might choose?"
- If yes: It's a real strategic choice
- If no: It's not strategy, it's a goal (reframe it)

### Step 5: Write the Strategy Document

Create file: `docs/strategy/<product-area>-strategy.md`

Use this template:

```markdown
---
title: [Product Area] Strategy
product_team: [team name]
owner: [PM name if known]
version: 1.0
last_updated: YYYY-MM-DD
status: draft | review | approved
---

# [Product Area] Strategy

## Product Vision

[2-3 sentences describing the future state this product creates]

**North Star Metric**: [Single metric that best indicates success]

## Link to Company Strategy

| Company Choice | How We Contribute |
|----------------|-------------------|
| Winning Aspiration: €12M ARR, 10K professionals | [How this product contributes] |
| Where to Play | [Which segments we serve] |
| How to Win | [Which differentiators we enable] |

## Target Users

### Primary Persona: [Role Name]

**Who they are**: [Description]

**Pain points**:
1. [Pain point with evidence/quotes]
2. [Pain point with evidence/quotes]
3. [Pain point with evidence/quotes]

**Jobs to be done**:
- [Outcome they're trying to achieve]
- [Outcome they're trying to achieve]

### Secondary Persona: [Role Name]

[Same structure]

## Strategic Bets

We are making [N] strategic bets for the next [timeframe]:

### Bet 1: [Name]

**What we believe**: If we [action], then [outcome] because [rationale].

**Success metrics**:
- [Metric]: [Current] → [Target] by [Date]
- [Metric]: [Current] → [Target] by [Date]

**Key initiatives**:
1. [Initiative]
2. [Initiative]

**Risks & mitigations**:
- Risk: [Description] → Mitigation: [How we address it]

### Bet 2: [Name]

[Same structure]

### Bet 3: [Name]

[Same structure]

## How We Win

| Differentiator | How It Delights Users | Why It's Hard to Copy |
|----------------|----------------------|----------------------|
| [Capability] | [User benefit] | [Competitive moat] |
| [Capability] | [User benefit] | [Competitive moat] |
| [Capability] | [User benefit] | [Competitive moat] |

## What We're NOT Doing

We are explicitly deprioritizing:

| Not Doing | Rationale |
|-----------|-----------|
| [Feature/market/segment] | [Why it doesn't fit our strategy] |
| [Feature/market/segment] | [Why it doesn't fit our strategy] |
| [Feature/market/segment] | [Why it doesn't fit our strategy] |

## Dependencies & Capabilities

### Capabilities We Need

| Capability | Current State | Gap | Plan to Close |
|------------|--------------|-----|---------------|
| [Skill/technology] | [Assessment] | [Gap] | [Action] |

### Cross-Team Dependencies

| Dependency | Team | What We Need | Timeline |
|------------|------|--------------|----------|
| [Dependency] | [Team] | [Requirement] | [When] |

## Key Metrics

| Metric | Current | Target | Rationale |
|--------|---------|--------|-----------|
| [KPI] | [Baseline] | [Goal] | [Why it matters to strategy] |
| [KPI] | [Baseline] | [Goal] | [Why it matters to strategy] |
| [KPI] | [Baseline] | [Goal] | [Why it matters to strategy] |

## Review Cadence

- **Weekly**: [What's reviewed]
- **Monthly**: [What's reviewed]
- **Quarterly**: [Full strategy review with leadership]

## Appendix

### Competitive Landscape

| Competitor | Positioning | Our Differentiation |
|------------|-------------|---------------------|
| [Competitor] | [Their approach] | [Why we're different] |

### Customer Evidence

[Quotes, data points, or research that informed this strategy]

### Open Questions

- [ ] [Question for further research]
- [ ] [Question for further research]
```

### Step 6: Validate the Strategy

Run these quality checks:

**Coherence Check**
- Do all bets support the product vision?
- Does the product strategy align with company strategy?
- Are the "not doing" items consistent with the bets?

**Clarity Check**
- Could a new team member understand the priorities?
- Are metrics specific and measurable?
- Are success criteria well-defined?

**Courage Check**
- Are there genuine trade-offs (not just "do good things")?
- Would a competitor choose the opposite of any choice?
- Is the "not doing" list uncomfortable but correct?

### Step 7: Store in Memory

After creating the strategy:
```javascript
memory({
  mode: "add",
  content: "Product Strategy: [product area] - [key bets summary]. North star: [metric]. Not doing: [key exclusions]",
  scope: "project",
  tags: ["product-strategy", "viya", "<product-area>"]
})
```

## Output to User

After completing the strategy, provide:
1. The complete strategy document
2. Summary of key strategic choices made
3. Suggested file location
4. Recommended next steps (e.g., customer validation, team alignment, OKR mapping)
5. Any gaps that need further input

## Facilitation Tips

**If user struggles with vision**:
- Ask about the current biggest pain point for users
- Ask what users would say in a testimonial if the product was wildly successful
- Reference company vision for inspiration

**If user struggles with trade-offs ("everything is important")**:
- Ask: "If you could only do ONE of these, which would it be?"
- Use forced ranking: "Stack rank these 5 options"
- Ask: "What would you tell a customer asking for [deprioritized thing]?"

**If user struggles with differentiation**:
- Ask: "What do customers say when asked why they chose Viya?"
- Ask: "What would be painful for a competitor to copy?"
- Reference Gibson Biddle's 7 Powers for moat ideas

**If user is unsure about metrics**:
- Start with leading indicators (can influence) vs lagging indicators (measure outcomes)
- Ask: "How would you know if this bet is working? What would you observe?"
- Reference company KPIs and map product metrics to them

## Framework Quick Reference

### Playing to Win (5 Choices)
1. Winning Aspiration - What is our purpose?
2. Where to Play - Target markets, customers, channels
3. How to Win - Value proposition, competitive advantage
4. Capabilities - Activities required to win
5. Management Systems - Metrics and processes

### DHM Model
- **Delight**: What unique value creates "wow"?
- **Hard-to-copy**: Brand, network effects, scale, technology, switching costs, data
- **Margin**: Does this protect or improve profitability?

### SVPG Four Pillars
1. **Focus**: Few critical objectives
2. **Insights**: Learning from data, customers, technology, industry
3. **Actions**: Team objectives with strategic context
4. **Management**: Active servant leadership

## Error Handling

If information is incomplete:
- Mark sections with `[TODO: needs input on X]`
- List specific questions at the end
- Provide example answers to guide thinking

If strategy conflicts with company direction:
- Flag the conflict explicitly
- Recommend discussing with leadership
- Document the tension and potential resolutions

## Related Resources

- Company Strategy: `knowledgebase/strategy/Strategy 2025-2030*.md`
- Company Vision: `knowledgebase/vision/Mission & Vision.md`
- Research: `research/product-strategy/2026-01-13-writing-product-strategy.md`
