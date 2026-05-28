---
name: jikime-marketing-psychology
description: Marketing psychology and mental models specialist for applying behavioral science principles to marketing decisions, customer behavior analysis, and ethical persuasion techniques.
version: 1.0.0
tags: ["marketing", "psychology", "mental-models", "persuasion", "behavioral-science"]
triggers:
  keywords: ["psychology", "mental model", "cognitive bias", "persuasion", "why people buy", "decision-making", "consumer behavior", "심리학", "설득", "행동심리", "구매심리"]
  phases: ["plan", "run"]
  agents: ["frontend", "manager-strategy", "architect"]
  languages: []
# Progressive Disclosure Configuration
progressive_disclosure:
  enabled: true
  level1_tokens: ~100
  level2_tokens: ~8000
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

# Marketing Psychology & Mental Models

## Quick Reference (30 seconds)

Marketing Psychology Specialist - Apply psychological principles and mental models to understand customer behavior and create more effective, ethical marketing.

Core Philosophy:
- **Understand First**: Know why people buy before trying to sell
- **Evidence-Based**: Use proven psychological principles, not assumptions
- **Ethical Application**: Influence behavior without manipulation

Key Capabilities:
- 70+ mental models for marketing decisions
- Buyer psychology and decision-making frameworks
- Persuasion techniques (Cialdini's principles)
- Pricing psychology patterns

---

## Mental Model Categories

```
┌─────────────────────────────────────────────────────────────────┐
│                    MENTAL MODEL FRAMEWORK                        │
├─────────────────────────────────────────────────────────────────┤
│  1. THINKING         2. BUYER            3. PERSUASION          │
│  ┌─────────────┐    ┌─────────────┐     ┌─────────────┐        │
│  │ Strategy    │    │ How people  │     │ Ethical     │        │
│  │ frameworks  │    │ decide and  │     │ influence   │        │
│  │ for better  │    │ behave      │     │ techniques  │        │
│  │ decisions   │    │             │     │             │        │
│  └─────────────┘    └─────────────┘     └─────────────┘        │
│                                                                  │
│  4. PRICING          5. DESIGN           6. GROWTH              │
│  ┌─────────────┐    ┌─────────────┐     ┌─────────────┐        │
│  │ Price       │    │ How to      │     │ How         │        │
│  │ perception  │    │ structure   │     │ marketing   │        │
│  │ psychology  │    │ experiences │     │ compounds   │        │
│  └─────────────┘    └─────────────┘     └─────────────┘        │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1. Foundational Thinking Models

Strategy frameworks for solving the right problems.

| Model | Principle | Marketing Application |
|-------|-----------|----------------------|
| **First Principles** | Break problems to basic truths, build from there | Don't copy competitors—ask why you need that channel |
| **Jobs to Be Done** | People hire products to accomplish outcomes | Frame around the job, not features ("hole, not drill") |
| **Circle of Competence** | Stay within areas of genuine expertise | Double down where you have competitive advantage |
| **Inversion** | Ask "What would guarantee failure?" | List campaign killers, then systematically prevent each |
| **Occam's Razor** | Simplest explanation usually correct | Check obvious causes first (broken form, slow page) |
| **Pareto Principle** | 80% results from 20% efforts | Find the 20% driving results, reduce the rest |
| **Theory of Constraints** | Find the one bottleneck limiting throughput | Fix traffic bottleneck before optimizing conversion |
| **Second-Order Thinking** | Consider effects of effects | Flash sale boosts revenue but may train discount waiting |

### Strategic Decision Framework

```
┌─────────────────────────────────────────────────────────────────┐
│  DECISION QUESTION                           MODEL TO USE       │
├─────────────────────────────────────────────────────────────────┤
│  "Why are we doing this?"                    First Principles   │
│  "What outcome does customer want?"          Jobs to Be Done    │
│  "Where should we focus?"                    Pareto Principle   │
│  "What's blocking growth?"                   Theory of Constraints│
│  "What could go wrong?"                      Inversion          │
│  "What are the long-term effects?"           Second-Order Thinking│
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Buyer Psychology Models

How customers think, decide, and behave.

### Cognitive Biases

| Bias | How It Works | Marketing Application |
|------|--------------|----------------------|
| **Mere Exposure Effect** | Familiarity breeds liking | Consistent brand presence builds preference |
| **Availability Heuristic** | Easy-to-recall = common | Case studies make success feel achievable |
| **Confirmation Bias** | Seek info confirming beliefs | Align with existing beliefs, don't fight them |
| **Mimetic Desire** | Want what others want | Show desirable people using your product |
| **Fundamental Attribution Error** | Blame character over situation | Examine your process before blaming customers |

### Ownership & Value Perception

| Model | Principle | Marketing Application |
|-------|-----------|----------------------|
| **Endowment Effect** | Value owned things more | Free trials create ownership feeling |
| **IKEA Effect** | Value self-created things | Let customers customize, invest effort |
| **Zero-Price Effect** | Free is psychologically different | Free tiers have disproportionate appeal |
| **Sunk Cost Fallacy** | Continue due to past investment | Know when to kill underperforming campaigns |

### Decision & Action Triggers

| Model | Principle | Marketing Application |
|-------|-----------|----------------------|
| **Hyperbolic Discounting** | Prefer immediate over future rewards | Emphasize "Start saving time today" |
| **Status-Quo Bias** | Prefer current state | Reduce switching friction, make it safe |
| **Default Effect** | Accept pre-selected options | Pre-select preferred plan |
| **Paradox of Choice** | Too many options paralyze | Limit to 3 pricing tiers, recommend one |
| **Goal-Gradient Effect** | Accelerate near goals | Show progress bars, "almost there" messaging |

### Experience & Memory

| Model | Principle | Marketing Application |
|-------|-----------|----------------------|
| **Peak-End Rule** | Judge by peak + end, not average | Design memorable peaks and strong endings |
| **Zeigarnik Effect** | Unfinished tasks occupy mind | "You're 80% done" creates pull to finish |
| **Pratfall Effect** | Flaws make competent more likable | "We're not cheapest, but..." builds trust |
| **Curse of Knowledge** | Can't imagine not knowing | Test copy with unfamiliar users |

---

## 3. Persuasion & Influence Models

Cialdini's principles and ethical influence techniques.

### Cialdini's 6+1 Principles

| Principle | Mechanism | Marketing Application |
|-----------|-----------|----------------------|
| **Reciprocity** | Return favors | Free content, tools create obligation |
| **Commitment** | Stay consistent with past actions | Small commitments lead to larger ones |
| **Social Proof** | Follow others | Show customer counts, testimonials |
| **Authority** | Defer to experts | Expert endorsements, certifications |
| **Liking** | Say yes to those we like | Relatable spokespeople, shared values |
| **Scarcity** | Limited = valuable | Genuine limited offers, exclusivity |
| **Unity** | "One of us" is powerful | Position as part of customer's tribe |

### Influence Techniques

| Technique | How It Works | Application |
|-----------|--------------|-------------|
| **Foot-in-the-Door** | Small request → large request | Free trial → paid → annual → enterprise |
| **Door-in-the-Face** | Large request → reasonable request | Show enterprise first, then starter plan |
| **Loss Aversion** | Losses hurt 2x more than gains | "Don't miss out" beats "You could gain" |
| **Anchoring** | First number influences judgment | Show higher price first to anchor |
| **Decoy Effect** | Inferior option makes another look better | Add decoy tier to favor preferred option |
| **Framing Effect** | Presentation changes perception | "90% success" beats "10% failure" |
| **Contrast Effect** | Comparison changes perception | Show clear before/after contrast |

### Commitment Escalation Ladder

```
┌─────────────────────────────────────────────────────────────────┐
│  LOW COMMITMENT ───────────────────────────── HIGH COMMITMENT   │
│                                                                  │
│  Newsletter  →  Free Tool  →  Free Trial  →  Paid  →  Annual   │
│  signup         download       activation    plan     contract  │
│                                                                  │
│  Each step builds on previous commitment                        │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. Pricing Psychology

How people perceive and respond to prices.

| Model | Principle | Application |
|-------|-----------|-------------|
| **Charm Pricing** | $99 feels much cheaper than $100 | Use .99 for value products |
| **Round Pricing** | $100 signals premium | Use round prices for premium |
| **Rule of 100** | Under $100: % off; Over $100: $ off | $80 product: "20% off" not "$16 off" |
| **Price Relativity** | Judged against options | Middle tier looks reasonable between extremes |
| **Mental Accounting** | Money framed differently | "$1/day" < "$30/month" (psychologically) |

### Price Framing Matrix

```
┌─────────────────────────────────────────────────────────────────┐
│  PRODUCT PRICE        DISCOUNT FRAMING           PRICE ENDING   │
├─────────────────────────────────────────────────────────────────┤
│  Under $100           Use percentage (20% off)   Use .99 / .95  │
│  Over $100            Use dollar amount ($50 off) Use round     │
│  Premium product      Any discount format        Use round      │
│  Value product        Percentage feels bigger    Use .99 / .97  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. Design & Delivery Models

How to structure effective marketing experiences.

| Model | Principle | Application |
|-------|-----------|-------------|
| **Hick's Law** | More options = slower decisions = abandonment | One clear CTA, fewer form fields |
| **AIDA Funnel** | Attention → Interest → Desire → Action | Structure pages through each stage |
| **Rule of 7** | ~7 touchpoints before conversion | Multi-touch campaigns, retargeting |
| **Nudge Theory** | Small presentation changes influence behavior | Defaults, ordering, friction reduction |

### Behavior Change Frameworks

| Framework | Components | Application |
|-----------|------------|-------------|
| **BJ Fogg Model** | Behavior = Motivation × Ability × Prompt | Design for all three factors |
| **EAST Framework** | Easy, Attractive, Social, Timely | Reduce friction, make appealing, show social proof, ask at right moment |
| **COM-B Model** | Capability, Opportunity, Motivation | Can they? Is path clear? Do they want to? |
| **Activation Energy** | Initial energy to start | Make first step trivially easy |

---

## 6. Growth & Scaling Models

How marketing compounds and scales.

| Model | Principle | Application |
|-------|-----------|-------------|
| **Feedback Loops** | Output becomes input | Build virtuous cycles (users → content → SEO → users) |
| **Compounding** | Small gains accumulate | Consistent efforts compound over time |
| **Network Effects** | Product improves with users | Design features that improve with adoption |
| **Flywheel Effect** | Momentum maintains itself | Content → traffic → leads → customers → content |
| **Switching Costs** | Cost of changing to competitor | Ethical stickiness via integrations, data |
| **Critical Mass** | Self-sustaining growth threshold | Focus on one segment before expanding |
| **Survivorship Bias** | Only see successes | Study failed campaigns too |

### Growth Flywheel Pattern

```
┌─────────────────────────────────────────────────────────────────┐
│                         FLYWHEEL                                 │
│                                                                  │
│                        ┌─────────┐                              │
│                        │ Content │                              │
│                        └────┬────┘                              │
│                             ↓                                    │
│    ┌─────────┐        ┌─────────┐        ┌─────────┐           │
│    │  More   │←───────│ Traffic │───────→│  Leads  │           │
│    │ content │        └─────────┘        └────┬────┘           │
│    └────┬────┘                                ↓                 │
│         ↑              ┌─────────┐        ┌─────────┐           │
│         └──────────────│  Case   │←───────│Customers│           │
│                        │ Studies │        └─────────┘           │
│                        └─────────┘                              │
│                                                                  │
│  Each element powers the next → momentum builds                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Quick Reference by Challenge

| Challenge | Relevant Models |
|-----------|-----------------|
| **Low conversions** | Hick's Law, Activation Energy, BJ Fogg, Friction |
| **Price objections** | Anchoring, Framing, Mental Accounting, Loss Aversion |
| **Building trust** | Authority, Social Proof, Reciprocity, Pratfall Effect |
| **Creating urgency** | Scarcity, Loss Aversion, Zeigarnik Effect |
| **Retention/churn** | Endowment Effect, Switching Costs, Status-Quo Bias |
| **Growth stalling** | Theory of Constraints, Local vs Global Optima, Compounding |
| **Decision paralysis** | Paradox of Choice, Default Effect, Nudge Theory |
| **Onboarding** | Goal-Gradient, IKEA Effect, Commitment & Consistency |

---

## Discovery Questions

Before applying models:

1. What specific behavior are you trying to influence?
2. What does your customer believe before encountering your marketing?
3. Where in the journey (awareness → consideration → decision) is this?
4. What's currently preventing the desired action?
5. Have you tested this with real customers?

---

## Ethical Application Guidelines

```
┌─────────────────────────────────────────────────────────────────┐
│  ETHICAL INFLUENCE CHECKLIST                                     │
├─────────────────────────────────────────────────────────────────┤
│  ✓ Would I be comfortable if customers knew the technique?      │
│  ✓ Does this genuinely help the customer make a better choice?  │
│  ✓ Is the scarcity/urgency real, not manufactured?              │
│  ✓ Are testimonials authentic and representative?               │
│  ✓ Am I informing, not manipulating?                            │
│  ✓ Would I apply this to my own family?                         │
└─────────────────────────────────────────────────────────────────┘
```

---

## Works Well With

Skills:
- `jikime-marketing-page-cro` - Apply psychology to page optimization
- `jikime-marketing-copywriting` - Write copy using psychological principles
- `jikime-marketing-pricing` - Price psychology and tier design
- `jikime-marketing-ab-test` - Test psychological hypotheses

---

Version: 1.0.0
Last Updated: 2026-01-25
Attribution: Enhanced from marketingskills by Corey Haines (MIT License)
