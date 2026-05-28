---
id: audience-segmentation
name: "Audience Segmentation"
domain: RES
skill: faion-researcher
category: "research"
---

# Audience Segmentation

## Metadata

| Field | Value |
|-------|-------|
| **ID** | (semantic) |
| **Category** | Research |
| **Difficulty** | Intermediate |
| **Tags** | #research, #segmentation, #audience |
| **Domain Skill** | faion-researcher |
| **Agents** | faion-persona-builder-agent |

---

## Problem

"Everyone is my customer" leads to weak positioning and wasted marketing spend. Issues:
- Messaging too generic to resonate
- Features built for nobody in particular
- Marketing scattered across channels
- Pricing that fits nobody well

**The root cause:** No segmentation strategy to identify and prioritize target groups.

---

## Framework

### What is Audience Segmentation?

Audience segmentation is dividing your potential market into distinct groups that have different needs, behaviors, or characteristics. It answers: "Which specific groups should we focus on?"

### Segmentation Criteria

#### 1. Demographic Segmentation

| Variable | Examples |
|----------|----------|
| Age | 18-24, 25-34, 35-44 |
| Income | <$50K, $50-100K, $100K+ |
| Education | High school, Bachelor's, Masters+ |
| Occupation | Developer, marketer, founder |
| Company size | Solo, 1-10, 11-50, 51-200 |
| Industry | SaaS, E-commerce, Consulting |

**Best for:** B2B targeting, pricing tiers

#### 2. Behavioral Segmentation

| Variable | Examples |
|----------|----------|
| Usage frequency | Daily, weekly, monthly |
| Purchase history | Free, paid, churned |
| Feature usage | Core only, power user |
| Engagement | Active, passive, dormant |
| Buying stage | Aware, considering, ready |

**Best for:** Product development, retention strategies

#### 3. Psychographic Segmentation

| Variable | Examples |
|----------|----------|
| Values | Quality over price, innovation |
| Attitudes | Risk-tolerant, skeptical |
| Lifestyle | Work-life balance, hustle culture |
| Motivations | Status, security, creativity |
| Pain tolerance | "Just make it work" vs perfectionists |

**Best for:** Messaging, brand positioning

#### 4. Needs-Based Segmentation

| Variable | Examples |
|----------|----------|
| Problem severity | Critical, moderate, nice-to-have |
| Current solution | DIY, competitor, nothing |
| Budget | Limited, flexible, money is no object |
| Speed priority | Need it yesterday, can wait |
| Support needs | Self-serve, guided, white-glove |

**Best for:** Product tiers, pricing strategy

### Segmentation Process

#### Step 1: Gather Data

**Sources:**

| Source | What to Extract |
|--------|-----------------|
| Customer interviews | Qualitative patterns |
| CRM data | Demographics, behavior |
| Analytics | Usage patterns |
| Survey responses | Preferences, attitudes |
| Sales conversations | Objections, needs |

#### Step 2: Identify Dimensions

Choose 2-3 most meaningful variables:

```
Dimension 1: [Most important differentiator]
Dimension 2: [Second most important]
(Optional) Dimension 3: [Third most important]
```

**Example:**
- Dimension 1: Company size (Solo, Small, Medium)
- Dimension 2: Tech sophistication (Low, Medium, High)

#### Step 3: Create Segments

**2×2 Matrix (simplest):**

```
                    Dimension 1
                Low           High
           |              |
Dimension  | Segment A    | Segment B
2  High    |              |
           |--------------|-------------
           | Segment C    | Segment D
   Low     |              |
```

**Example for project management tool:**

```
                    Company Size
                Solo          Team (5-20)
           |              |
Tech       | "The         | "The Scale-Up"
Savvy High | Hacker"      | Needs: Collaboration
           |--------------|-------------
           | "The         | "The Traditional"
   Low     | Overwhelmed" | Needs: Simple + Training
```

#### Step 4: Evaluate Segments

**Segment attractiveness criteria:**

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Size | 20% | How many people? |
| Growth | 15% | Is it growing? |
| Reachability | 20% | Can we access them? |
| Profitability | 20% | Will they pay enough? |
| Fit | 15% | Do we understand them? |
| Competition | 10% | How crowded? |

**Score each segment 1-5, calculate weighted total.**

#### Step 5: Select Target Segments

**Prioritization strategies:**

| Strategy | Description | When to Use |
|----------|-------------|-------------|
| Concentrated | Focus on one segment | Limited resources |
| Differentiated | Target 2-3 with different approaches | More resources |
| Niche | Deep focus on sub-segment | Crowded market |

**For solopreneurs:** Start with ONE segment until $10K+ MRR.

---

## Templates

### Segmentation Analysis

```markdown
## Audience Segmentation: [Product]

### Dimensions Selected
1. **Primary:** [Variable] - Why: [Reason]
2. **Secondary:** [Variable] - Why: [Reason]

### Segments Identified

#### Segment 1: [Name]

**Profile:**
- [Demographic 1]
- [Demographic 2]
- [Behavior]

**Needs:**
- [Primary need]
- [Secondary need]

**Current solutions:**
- [What they use now]

**Estimated size:** [N people/companies]
**Reachability:** [Where to find them]
**Willingness to pay:** $[X]/month

**Score:**
| Criterion | Score (1-5) |
|-----------|-------------|
| Size | |
| Growth | |
| Reachability | |
| Profitability | |
| Fit | |
| Competition | |
| **Weighted Total** | **X** |

---

#### Segment 2: [Name]
...

### Segment Comparison

| Segment | Size | WTP | Reach | Fit | Priority |
|---------|------|-----|-------|-----|----------|
| [Seg 1] | X | $X | Easy | High | 1 |
| [Seg 2] | X | $X | Medium | Medium | 2 |

### Target Strategy
[ ] Concentrated - Focus on [Segment X]
[ ] Differentiated - Target [Seg X] and [Seg Y]

### Implications

**Product:**
- [Feature priority]
- [Feature to skip]

**Marketing:**
- [Channel focus]
- [Messaging angle]

**Pricing:**
- [Tier structure]
```

### Segment Profile Card

```markdown
## Segment: [Name]

### In One Sentence
[Who they are and what they need]

### Demographics
- Role: [X]
- Company: [Size, type]
- Location: [Geography]
- Budget: [Range]

### Behaviors
- Tool usage: [Current stack]
- Buying process: [How they decide]
- Information sources: [Where they learn]

### Needs
1. [Primary need]
2. [Secondary need]
3. [Tertiary need]

### Pain Points
1. [Pain 1]
2. [Pain 2]

### Messaging That Works
- Hook: "[Attention grabber]"
- Promise: "[What we offer]"
- Proof: "[Evidence type they trust]"

### How to Reach Them
- Primary channel: [X]
- Secondary: [X]
- Communities: [X]

### Segment Size
- Total potential: [N]
- Addressable: [N]
- Reachable: [N]
```

---

## Examples

### Example 1: CRM Tool Segmentation

**Dimensions:**
- Team size: Solo, 2-5, 6-20, 20+
- Sales complexity: Transactional, Consultative

**Segments:**

| Segment | Size × Complexity | Needs | Price Point |
|---------|-------------------|-------|-------------|
| Freelancer | Solo × Transactional | Simple pipeline | $9/mo |
| Agency | 2-5 × Consultative | Deal tracking, proposals | $29/mo |
| Startup Sales | 6-20 × Transactional | Automation, reporting | $49/mo |
| Enterprise | 20+ × Consultative | Custom, integrations | Custom |

**Decision:** Focus on "Agency" segment - high WTP, underserved, reachable.

### Example 2: Online Course Segmentation

**Dimensions:**
- Learning goal: Career change, skill upgrade, hobby
- Time available: <5 hrs/week, 5-10 hrs, 10+ hrs

**Segments:**

| Segment | Goal × Time | Characteristics |
|---------|-------------|-----------------|
| Career Changers | Career × 10+ hrs | Committed, outcome-focused |
| Upskilling Pros | Upgrade × 5-10 hrs | Already working, busy |
| Hobbyists | Hobby × <5 hrs | Fun-focused, casual |

**Decision:** Focus on "Upskilling Pros" - pay for time savings, higher budgets.

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Too many segments | Start with 2-4 |
| Segments overlap | Ensure mutually exclusive |
| Only demographics | Include behavior/needs |
| Not validating size | Quantify each segment |
| Targeting everyone | Pick ONE primary segment |
| Static segmentation | Review quarterly |

---

## Related Methodologies

- **niche-evaluation:** Niche Evaluation
- **market-research-tam-sam-som:** Market Research (TAM/SAM/SOM)
- **persona-building:** Persona Building
- **mvp-scoping:** MVP Scoping
- **gtm-strategy:** GTM Strategy

---

## Agent

**faion-persona-builder-agent** helps with segmentation. Invoke with:
- "Segment my audience for [product]"
- "Evaluate these segments: [list]"
- "Which segment should I target first?"
- "Create segment profiles for [market]"

---

*Methodology | Research | Version 1.0*
