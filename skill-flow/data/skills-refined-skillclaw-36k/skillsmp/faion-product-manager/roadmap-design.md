---
id: roadmap-design
name: "Roadmap Design"
domain: PRD
skill: faion-product-manager
category: "product"
---

# Roadmap Design

## Metadata

| Field | Value |
|-------|-------|
| **ID** | (semantic) |
| **Category** | Product |
| **Difficulty** | Intermediate |
| **Tags** | #product, #roadmap, #planning |
| **Domain Skill** | faion-product-manager |
| **Agents** | faion-mlp-impl-planner-agent |

---

## Problem

Roadmaps either over-promise specific dates or are so vague they're useless. Common issues:
- Feature lists with dates that always slip
- No connection to strategy or goals
- Stakeholders interpret roadmap as commitment
- No flexibility for learning and change

**The root cause:** Wrong roadmap format for the audience and uncertainty level.

---

## Framework

### What is a Roadmap?

A roadmap is a strategic communication tool that shows what you plan to build and why. It answers: "Where are we going and how will we get there?"

**Key insight:** Roadmaps are about outcomes, not feature lists.

### Roadmap Types

| Type | Focus | Timeframe | Best For |
|------|-------|-----------|----------|
| Timeline | When things ship | Quarters/months | External, committed work |
| Now-Next-Later | Priority sequence | Flexible | Internal, early stage |
| Outcome-based | Goals to achieve | Themes | Strategic alignment |
| Kanban | Current work | Live | Internal teams |

### Roadmap Components

#### 1. Vision

**Where are we heading long-term?**
- 1-3 year vision statement
- Strategic pillars
- Success definition

#### 2. Objectives

**What outcomes are we targeting?**
- OKRs or goals
- Measurable targets
- Timeframes

#### 3. Themes

**What problem areas are we addressing?**
- Group related work
- Connect to objectives
- Provide flexibility

#### 4. Features/Initiatives

**What will we build?**
- High-level descriptions
- Tied to themes
- Confidence levels

### Roadmap Design Process

#### Step 1: Start with Strategy

**Inputs needed:**
- Company/product vision
- Business goals for the period
- User research insights
- Technical constraints

**Output:** Clear objectives for the roadmap period.

#### Step 2: Choose the Format

**Decision factors:**

| Factor | Timeline | Now-Next-Later | Outcome |
|--------|----------|----------------|---------|
| Uncertainty | Low | Medium | High |
| External sharing | Yes | Limited | Yes |
| Commitment level | High | Medium | Low |
| Team maturity | High | Any | Any |

#### Step 3: Define Themes

Group work into 3-5 themes:

**Template:**
```
Theme: [Name]
Objective: [What outcome it drives]
Why now: [Strategic rationale]
Example initiatives: [2-3 examples]
```

#### Step 4: Populate with Work

**For each time horizon/bucket:**
- What are we confident about?
- What are we exploring?
- What did we decide NOT to do?

**Confidence indicators:**
- High: Committed, scoped
- Medium: Planned, needs scoping
- Low: Exploring, tentative

#### Step 5: Add Context

**For stakeholder communication:**
- Why we chose this
- What we're NOT doing
- Dependencies and risks
- How we'll measure success

---

## Templates

### Now-Next-Later Roadmap

```markdown
## Product Roadmap: [Product Name]

### Vision
[1-2 sentence long-term vision]

### Current Focus
[What we're optimizing for this period]

---

## NOW (Current Quarter)

**Theme: [Theme Name]**
- [Initiative 1] - [Status: In Progress/Planned]
- [Initiative 2] - [Status]

**Theme: [Theme Name]**
- [Initiative 1] - [Status]

**Why:** [Strategic rationale]

---

## NEXT (Next Quarter)

**Theme: [Theme Name]**
- [Initiative 1] - Confidence: High
- [Initiative 2] - Confidence: Medium

**Theme: [Theme Name]**
- [Initiative 1] - Confidence: Medium

**Depends on:** [What needs to happen first]

---

## LATER (Future)

**Exploring:**
- [Idea 1]
- [Idea 2]

**Watching:**
- [Market trend]
- [Technology development]

**Not Doing:**
- [Explicit exclusion] - Reason: [Why]

---

### Success Metrics
| Objective | Metric | Target |
|-----------|--------|--------|
| [Goal 1] | [Metric] | [Target] |
| [Goal 2] | [Metric] | [Target] |

### Last Updated: [Date]
```

### Quarterly Outcome Roadmap

```markdown
## Q[X] Roadmap: [Product]

### Quarter Objectives
1. **[Objective 1]:** [Description]
   - Key Result: [Measurable outcome]

2. **[Objective 2]:** [Description]
   - Key Result: [Measurable outcome]

### Initiatives by Theme

#### Theme 1: [Name]
**Drives:** [Which objective]

| Initiative | Confidence | Effort | Owner |
|------------|------------|--------|-------|
| [Init 1] | High | M | [Name] |
| [Init 2] | Medium | L | [Name] |

#### Theme 2: [Name]
**Drives:** [Which objective]

| Initiative | Confidence | Effort | Owner |
|------------|------------|--------|-------|
| [Init 1] | High | S | [Name] |

### Explicitly Not Doing
| Item | Reason |
|------|--------|
| [Item 1] | [Rationale] |

### Risks & Dependencies
| Risk | Mitigation |
|------|------------|
| [Risk 1] | [Plan] |

### Review Schedule
- Mid-quarter check: [Date]
- EOQ review: [Date]
```

### External/Customer Roadmap

```markdown
## [Product] Direction - [Year]

### Our Vision
[Customer-facing vision statement]

### What We're Building

#### Currently Available
- [Feature 1] - [Benefit]
- [Feature 2] - [Benefit]

#### Coming Soon (Next Quarter)
- [Feature 1] - [Benefit]
- [Feature 2] - [Benefit]

#### On Our Radar (This Year)
- [Capability 1]
- [Capability 2]

### How We Prioritize
We focus on:
1. [Priority 1]
2. [Priority 2]
3. [Priority 3]

### Request a Feature
[Link to feedback channel]

---

*This roadmap represents our current plans and is subject to change.
Timing is approximate.*
```

---

## Examples

### Example 1: B2B SaaS Roadmap

**Now (Q1):**
- Onboarding improvements (reduce time to value)
- API v2 launch (enterprise requirement)
- Performance optimization (load times)

**Next (Q2):**
- Team collaboration features
- Slack integration
- Advanced permissions

**Later:**
- Mobile app (pending validation)
- AI-powered insights (exploring)

### Example 2: Solo Product Roadmap

**Now:**
- Core feature polish (MLP)
- Payment integration
- Basic analytics

**Next:**
- Email automation
- Template library
- Referral program

**Later:**
- Mobile app
- Team features
- Marketplace

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Feature list with dates | Focus on outcomes and themes |
| Overcommitting | Use confidence levels |
| No strategic connection | Link everything to objectives |
| Never updating | Review monthly minimum |
| Too detailed | Higher-level for further out |
| No "not doing" section | Explicitly state exclusions |
| Same roadmap for all audiences | Tailor to audience needs |

---

## Related Methodologies

- **feature-prioritization-rice:** Feature Prioritization (RICE)
- **feature-prioritization-moscow:** Feature Prioritization (MoSCoW)
- **okr-setting:** OKR Setting
- **backlog-grooming-roadmapping:** Backlog Grooming & Roadmapping
- **schedule-development:** Schedule Development

---

## Agent

**faion-mlp-impl-planner-agent** helps with roadmaps. Invoke with:
- "Create a roadmap for [product]"
- "What format should my roadmap use?"
- "Review my roadmap: [content]"
- "How should I communicate [roadmap] to [audience]?"

---

*Methodology | Product | Version 1.0*
