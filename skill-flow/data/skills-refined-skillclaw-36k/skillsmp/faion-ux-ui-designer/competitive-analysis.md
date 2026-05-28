---
id: competitive-analysis
name: "Competitive Analysis"
domain: UX
skill: faion-ux-ui-designer
category: "ux-design"
---

# Competitive Analysis

## Metadata
- **Category:** UX / Research Methods
- **Difficulty:** Beginner
- **Tags:** #methodology #ux #research #competitive-analysis #benchmarking
- **Agent:** faion-ux-researcher-agent

---

## Problem

You design in a vacuum without knowing what exists. Users have expectations from other products you don't know about. You reinvent solutions that already exist. You miss opportunities competitors haven't addressed. Stakeholders ask "what do others do?" and you can't answer.

Without competitive analysis:
- Reinventing existing solutions
- Missing user expectations
- Unknown industry standards
- Missed opportunities

---

## Framework

### What is Competitive Analysis?

Competitive analysis systematically examines competitor products to understand their strengths, weaknesses, and approaches. For UX, this focuses on design patterns, user experience, and feature implementation.

### Types of Competitors

| Type | Definition | Example |
|------|------------|---------|
| **Direct** | Same problem, same user | Uber vs Lyft |
| **Indirect** | Same problem, different approach | Uber vs public transit |
| **Partial** | Overlap in some features | Google Maps vs Waze |
| **Aspirational** | Best-in-class to learn from | Not a competitor, inspiration |

### Analysis Dimensions

| Dimension | What to examine |
|-----------|-----------------|
| **Features** | What can users do? |
| **User flows** | How do users accomplish goals? |
| **UI patterns** | What design patterns are used? |
| **Information architecture** | How is content organized? |
| **Content** | What messaging and tone? |
| **Accessibility** | How accessible is it? |

---

## Process

### Step 1: Define Scope

**Questions to answer:**
- What product/feature are we analyzing?
- Who are our competitors?
- What aspects matter most?
- How will we use findings?

**Select competitors:**
- 3-5 direct competitors
- 2-3 indirect competitors
- 1-2 aspirational examples

### Step 2: Create Evaluation Criteria

Based on your research questions:

```
Example criteria for checkout flow:
- Number of steps
- Required information
- Guest checkout option
- Payment methods
- Error handling
- Mobile experience
- Accessibility
```

### Step 3: Gather Data

**Methods:**
- Use the product yourself
- Take screenshots/recordings
- Create accounts if needed
- Complete key user flows
- Document observations

### Step 4: Document Findings

Create consistent documentation:
- Screenshots with annotations
- Flow diagrams
- Feature comparison tables
- Notes on strengths/weaknesses

### Step 5: Analyze Patterns

Look for:
- What do most competitors do? (baseline)
- What does nobody do? (opportunity)
- What works well? (best practices)
- What problems exist? (avoid)

### Step 6: Generate Insights

Convert observations to recommendations:
- "We should..." (things to adopt)
- "We could differentiate by..." (opportunities)
- "We should avoid..." (problems seen)

---

## Templates

### Competitive Analysis Plan

```markdown
# Competitive Analysis Plan

**Product/Feature:** [What we're analyzing]
**Date:** [Date]
**Analyst:** [Name]

## Objective
[What we want to learn from this analysis]

## Competitors

| Company | Type | Why included |
|---------|------|--------------|
| [Name] | Direct | [Reason] |
| [Name] | Indirect | [Reason] |
| [Name] | Aspirational | [Reason] |

## Evaluation Criteria

| Criterion | Why it matters |
|-----------|----------------|
| [Criterion 1] | [Reason] |
| [Criterion 2] | [Reason] |
| [Criterion 3] | [Reason] |

## User Flows to Analyze

1. [Flow 1: e.g., Sign up process]
2. [Flow 2: e.g., Complete purchase]
3. [Flow 3: e.g., Get support]

## Deliverables
- [ ] Feature comparison matrix
- [ ] Flow diagrams for each competitor
- [ ] Annotated screenshots
- [ ] Summary report with recommendations

## Timeline
- Research: [Date range]
- Analysis: [Date]
- Report: [Date]
```

### Feature Comparison Matrix

```markdown
# Feature Comparison Matrix

| Feature | Our Product | Competitor A | Competitor B | Competitor C |
|---------|-------------|--------------|--------------|--------------|
| **Core Features** |
| [Feature 1] | Yes | Yes | No | Yes |
| [Feature 2] | No | Yes | Yes | Partial |
| **User Experience** |
| [UX aspect 1] | Good | Excellent | Poor | Good |
| [UX aspect 2] | [Rating] | [Rating] | [Rating] | [Rating] |
| **Technical** |
| Mobile app | Yes | Yes | No | Yes |
| Accessibility | AA | A | None | AAA |

## Legend
- Yes: Feature present
- No: Feature absent
- Partial: Limited implementation
- Ratings: Excellent / Good / Fair / Poor
```

### Individual Competitor Profile

```markdown
# Competitor Profile: [Company Name]

**Website:** [URL]
**Type:** Direct / Indirect / Aspirational
**Analyzed:** [Date]

## Overview
[Brief description of product and positioning]

## Target Users
[Who they seem to target]

## Key Screens

### [Screen Name]
[Screenshot]

**Observations:**
- [What works]
- [What doesn't]
- [Notable pattern]

### [Screen Name]
[Same structure]

## User Flows

### [Flow Name: e.g., Onboarding]

**Steps:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Friction points:**
- [Where users might struggle]

**Good practices:**
- [What they do well]

## Strengths
- [Strength 1]
- [Strength 2]

## Weaknesses
- [Weakness 1]
- [Weakness 2]

## Opportunities for Us
- [What we could do better]
- [What they're missing]
```

### Summary Report Template

```markdown
# Competitive Analysis Report

**Date:** [Date]
**Scope:** [What was analyzed]
**Competitors:** [List]

## Executive Summary

[2-3 paragraph overview of key findings]

## Key Findings

### 1. Industry Standards
[What most competitors do - baseline expectations]

### 2. Best Practices
[What top performers do well]

### 3. Common Problems
[Issues seen across competitors]

### 4. Opportunities
[Gaps no one is filling]

## Feature Comparison

[Insert comparison matrix]

## UX Pattern Analysis

### Navigation
[How competitors handle navigation]

### Forms
[Common form patterns]

### Error Handling
[How errors are communicated]

[Continue for relevant patterns]

## Recommendations

### Must Have (Table stakes)
- [Feature/pattern users expect]

### Should Have (Competitive parity)
- [What we need to match competitors]

### Could Differentiate (Opportunity)
- [Where we can stand out]

### Avoid
- [What to not do based on competitor failures]

## Appendix
- Competitor profiles
- Screenshots
- Flow diagrams
```

---

## Examples

### Example 1: E-commerce Checkout

**Finding:** All 5 competitors offer guest checkout

**Insight:** Guest checkout is table stakes. Not having it would be a competitive disadvantage.

**Finding:** Only 1 competitor shows estimated delivery on product page

**Insight:** Opportunity to differentiate by showing delivery estimate earlier.

### Example 2: SaaS Onboarding

| Competitor | Onboarding Steps | Time to Value |
|------------|------------------|---------------|
| A | 8 | 15 minutes |
| B | 3 | 2 minutes |
| C | 5 | 8 minutes |

**Insight:** Competitor B's minimal onboarding correlates with highest ratings. Consider reducing our steps.

---

## Analysis Frameworks

### SWOT Per Competitor

```
Strengths:     Weaknesses:
[List]         [List]

Opportunities: Threats:
[For us]       [From them]
```

### Feature Prioritization

Based on competitive landscape:

| Priority | Feature Type | Action |
|----------|--------------|--------|
| High | Table stakes | Must have, match best |
| Medium | Differentiators | Invest to stand out |
| Low | Nice-to-have | Consider later |

### Gap Analysis

```
        Feature Present
              ↑
    Them:Yes  │  Us: Yes
    Us: No    │  Them: No
   ──────────────────────→
              │           Feature Value
    Them:Yes  │  Us: Yes
    Us: Yes   │  Them: Yes
              ↓
```

---

## Common Mistakes

1. **Only analyzing direct competitors** - Miss inspiration from other industries
2. **Copying without understanding** - Don't know why competitor made choices
3. **One-time analysis** - Market changes, update regularly
4. **Surface-level review** - Need to actually use products, not just look
5. **No action from findings** - Analysis without implementation

---

## Tips for Effective Analysis

### Go Deep

```
Don't just look - use the product:
- Create a real account
- Complete full user flows
- Try edge cases
- Contact support
- Use on mobile
- Test accessibility
```

### Stay Objective

```
Avoid bias:
- Document before judging
- Use consistent criteria
- Acknowledge strengths
- Don't rationalize our weaknesses
- Let data inform conclusions
```

### Keep Updated

```
Schedule regular reviews:
- Major: Annually or after launches
- Minor: Quarterly check-ins
- Triggered: When competitors update
```

---

## Tools

| Tool | Use Case |
|------|----------|
| **Screenshots** | Loom, CloudApp, Screenshots folder |
| **Flow diagrams** | Miro, FigJam, Whimsical |
| **Comparison tables** | Notion, Airtable, Sheets |
| **Feature tracking** | Productboard, dedicated tracker |
| **Updates** | Competitor newsletters, Owler |

---

## Checklist

Before starting:
- [ ] Scope defined
- [ ] Competitors identified
- [ ] Criteria established
- [ ] Flows to analyze listed

During analysis:
- [ ] Used each product thoroughly
- [ ] Screenshots captured
- [ ] Flows documented
- [ ] Patterns noted
- [ ] Strengths/weaknesses recorded

After analysis:
- [ ] Comparison matrix completed
- [ ] Patterns identified
- [ ] Recommendations developed
- [ ] Report shared
- [ ] Follow-up scheduled

---

## References

- Just Enough Research by Erika Hall
- Competitive Strategy by Michael Porter
- UX research community: Competitive Usability Evaluations