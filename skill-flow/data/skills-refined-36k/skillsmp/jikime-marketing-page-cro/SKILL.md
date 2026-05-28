---
name: jikime-marketing-page-cro
description: Page conversion rate optimization (CRO) specialist for analyzing and improving marketing pages including homepages, landing pages, pricing pages, and feature pages.
version: 1.0.0
tags: ["marketing", "cro", "conversion", "landing-page", "optimization"]
triggers:
  keywords: ["CRO", "conversion", "optimize page", "landing page", "not converting", "improve conversions", "전환율", "랜딩페이지", "최적화"]
  phases: ["plan", "run"]
  agents: ["frontend", "manager-strategy"]
  languages: []
# Progressive Disclosure Configuration
progressive_disclosure:
  enabled: true
  level1_tokens: ~100
  level2_tokens: ~6000
user-invocable: true
context: fork
agent: general-purpose
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - Task
  - TodoWrite
---

# Page Conversion Rate Optimization (CRO)

## Quick Reference (30 seconds)

Page CRO Specialist - Systematic approach to analyze and improve conversion rates on any marketing page.

Core Philosophy:
- **Data-Driven**: Always base recommendations on evidence, not assumptions
- **User-Centric**: Focus on what visitors need, not what you want to say
- **Prioritized Impact**: Address highest-impact issues first

Key Capabilities:
- Multi-page type analysis (Homepage, Landing, Pricing, Feature, Blog)
- 7-dimension CRO framework
- Experiment ideation with hypothesis templates
- Quick wins identification

Quick Commands:
- Analyze page: Provide URL or screenshot
- Generate test ideas: Request experiment hypotheses
- Review copy: Focus on messaging effectiveness

---

## Implementation Guide (5 minutes)

### Initial Assessment Framework

Before providing recommendations, identify:

```
┌─────────────────────────────────────────────────────────────────┐
│  1. PAGE TYPE          2. CONVERSION GOAL      3. TRAFFIC SOURCE │
│  ┌─────────┐          ┌─────────┐             ┌─────────┐       │
│  │Homepage │          │ Signup  │             │ Organic │       │
│  │Landing  │          │ Demo    │             │ Paid    │       │
│  │Pricing  │          │Purchase │             │ Social  │       │
│  │Feature  │          │Download │             │ Email   │       │
│  └─────────┘          └─────────┘             └─────────┘       │
└─────────────────────────────────────────────────────────────────┘
```

### The 7-Dimension CRO Analysis Framework

Analyze pages in order of impact:

| Priority | Dimension | Key Questions | Common Issues |
|----------|-----------|---------------|---------------|
| **1** | Value Proposition | Can visitors understand value in 5 seconds? | Feature-focused, too vague, jargon |
| **2** | Headline Effectiveness | Does it communicate core value? | Generic, clever over clear |
| **3** | CTA Hierarchy | Is there one clear primary action? | Weak copy, poor placement, no contrast |
| **4** | Visual Hierarchy | Can someone scanning get the message? | Wall of text, competing elements |
| **5** | Trust Signals | Is there social proof near decisions? | Missing logos, generic testimonials |
| **6** | Objection Handling | Are common concerns addressed? | No FAQ, missing guarantees |
| **7** | Friction Points | Are there unnecessary barriers? | Too many form fields, unclear steps |

### Dimension 1: Value Proposition Clarity (Highest Impact)

**5-Second Test Checklist:**
- [ ] What is this product/service?
- [ ] Who is it for?
- [ ] Why should I care?
- [ ] What makes it different?

**Strong Value Prop Patterns:**

```markdown
❌ Weak: "The best solution for your needs"
✅ Strong: "Cut your weekly reporting from 4 hours to 15 minutes"

❌ Weak: "Innovative platform for modern teams"
✅ Strong: "The project tracker that updates itself from your Git commits"
```

### Dimension 2: Headline Effectiveness

**Headline Formula Templates:**

| Pattern | Template | Example |
|---------|----------|---------|
| Outcome + Pain | `{Achieve X} without {Pain Y}` | "Get clear skin without harsh chemicals" |
| Specific Benefit | `{Number} {Audience} use {Product} to {Outcome}` | "10,000+ marketers use Acme to double email opens" |
| Direct Question | `{Pain point question}?` | "Tired of chasing approvals?" |
| How It Works | `The {opposite} way to {outcome}` | "The lazy way to stay fit" |

### Dimension 3: CTA Placement & Copy

**CTA Copy Strength Scale:**

| Level | Examples | Improvement |
|-------|----------|-------------|
| **Weak** | Submit, Sign Up, Learn More | Action only |
| **Medium** | Get Started, Try It Free | Some value hint |
| **Strong** | Start My Free Trial, Get My Report | Value + ownership |
| **Best** | See How It Works in 2 Minutes | Value + low commitment |

**CTA Placement Rules:**
- Above the fold (visible without scrolling)
- After each major benefit section
- After social proof
- At page bottom (final CTA)

### Output Format for CRO Analysis

Structure recommendations as:

```markdown
## Quick Wins (Implement Now)
- [Change]: [Expected impact] - [Why it works]

## High-Impact Changes (Prioritize)
- [Change]: [Expected impact] - [Implementation notes]

## Test Ideas (A/B Test)
**Hypothesis**: Because [observation], we believe [change] will [outcome].
**Metric**: [Primary metric to measure]

## Copy Alternatives
**Current**: [existing copy]
**Option A**: [alternative] — [rationale]
**Option B**: [alternative] — [rationale]
```

---

## Page-Specific Frameworks

### Homepage CRO

Homepages serve multiple audiences:

| Visitor Type | Need | Optimization Focus |
|--------------|------|-------------------|
| Ready to buy | Quick path to action | Prominent CTA, clear pricing link |
| Researching | Understand offering | Clear value prop, feature overview |
| Evaluating | Compare to alternatives | Differentiators, social proof |

**Homepage Experiments:**
- Hero headline variations (specific vs. abstract)
- CTA button text and color
- Social proof placement (above vs. below fold)
- Navigation simplification

### Landing Page CRO

Single-purpose pages require:

| Element | Optimization |
|---------|--------------|
| Message Match | Headline matches ad copy exactly |
| Single CTA | Remove navigation, one action only |
| Complete Argument | All info on one page |
| Urgency | Only if genuine (deadline, limited) |

### Pricing Page CRO

High-intent visitors need:

| Element | Best Practice |
|---------|---------------|
| Plan Comparison | Clear table, visual differentiation |
| Recommended Plan | "Most Popular" badge, visual emphasis |
| Feature Clarity | Checkmarks, not paragraphs |
| "Which is right?" | Use case descriptions per tier |

**Pricing Experiments:**
- Annual billing discount highlight
- "Most Popular" badge placement
- Feature comparison table format
- Money-back guarantee prominence

---

## Experiment Ideas Library

### Hero Section Tests

| Test | Control | Variant | Hypothesis |
|------|---------|---------|------------|
| Headline Specificity | "Grow Your Business" | "Increase sales 23% in 30 days" | Specific outcomes build confidence |
| Social Proof in Hero | No social proof | "Trusted by 10,000+ teams" | Immediate credibility increases engagement |
| CTA Button Copy | "Get Started" | "Start Free Trial" | Explicit value reduces friction |
| Hero Visual | Static image | Product demo GIF | Motion demonstrates value |

### Trust Building Tests

| Test | Control | Variant | Hypothesis |
|------|---------|---------|------------|
| Logo Placement | Below fold | In hero section | Earlier trust signals improve scroll depth |
| Testimonial Format | Text only | Photo + name + title | Attribution increases believability |
| Review Integration | No reviews | G2/Capterra badges | Third-party validation builds trust |

---

## CRO Checklist

```
Page CRO Validation:
- [ ] Value proposition clear within 5 seconds
- [ ] Headline specific and benefit-focused
- [ ] Primary CTA visible above the fold
- [ ] CTA copy communicates value, not just action
- [ ] Social proof placed near decision points
- [ ] Common objections addressed (FAQ, guarantee)
- [ ] Form fields minimized to essential only
- [ ] Mobile experience tested and optimized
- [ ] Page load time under 3 seconds
- [ ] Clear visual hierarchy guides the eye
```

---

## Works Well With

Skills:
- `jikime-marketing-copywriting` - For complete copy rewrites
- `jikime-marketing-ab-test` - For testing recommended changes
- `jikime-marketing-psychology` - For psychological principles
- `jikime-domain-frontend` - For implementation

---

Version: 1.0.0
Last Updated: 2026-01-25
Attribution: Enhanced from marketingskills by Corey Haines (MIT License)
