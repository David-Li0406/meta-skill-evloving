---
id: competitor-analysis
name: "Competitor Analysis"
domain: RES
skill: faion-researcher
category: "research"
---

# Competitor Analysis

## Metadata

| Field | Value |
|-------|-------|
| **ID** | (semantic) |
| **Category** | Research |
| **Difficulty** | Beginner |
| **Tags** | #research, #competitors, #analysis |
| **Domain Skill** | faion-researcher |
| **Agents** | faion-competitor-analyzer-agent |

---

## Problem

Entrepreneurs either ignore competitors ("We're unique!") or obsess over them. Common issues:
- Not knowing who the real competitors are
- Copying instead of differentiating
- Missing indirect competitors
- No systematic tracking of competitor moves

**The root cause:** No structured framework for competitive intelligence.

---

## Framework

### What is Competitor Analysis?

Competitor analysis is the systematic study of businesses that compete for the same customers. It helps you find gaps, position your offering, and learn from others' mistakes.

### The Competitor Analysis Framework

#### Step 1: Identify Competitors

**Three types:**

| Type | Definition | Example (for CRM) |
|------|------------|-------------------|
| Direct | Same product, same audience | Salesforce, HubSpot |
| Indirect | Different product, same problem | Spreadsheets, Notion |
| Future | Emerging or could pivot | AI startups, big tech |

**Where to find:**
- Google "[problem] solution"
- Product Hunt: search category
- G2/Capterra: browse category
- "Alternatives to [known competitor]"
- Reddit: "What do you use for [problem]?"
- Ask target customers what they use

**Target:** 5-10 direct, 3-5 indirect, 2-3 future

#### Step 2: Map Competitor Landscape

**Positioning Matrix:**

```
                    Premium
                       |
    Specialized    |   Enterprise
    (High Value)   |   (High Price)
    ---------------|----------------
    Niche          |   Mass Market
    (Underserved)  |   (Crowded)
                       |
                    Budget
       Narrow ---------|--------- Broad
                   Feature Set
```

**Your goal:** Find empty quadrants or underserved positions.

#### Step 3: Analyze Each Competitor

**Key dimensions:**

| Dimension | Questions |
|-----------|-----------|
| Product | What features? What's missing? |
| Pricing | What model? What tiers? |
| Positioning | Who do they target? What's the message? |
| Technology | What stack? What integrations? |
| Traction | How many users? Revenue estimate? |
| Team | Size? Expertise? Funding? |
| Marketing | Channels? Content? Ads? |
| Weaknesses | Bad reviews? Gaps? Slow? |

#### Step 4: Identify Opportunities

**Gap analysis:**

| Category | Competitor A | Competitor B | Your Opportunity |
|----------|-------------|-------------|------------------|
| Feature X | Yes | No | Differentiate |
| Feature Y | Weak | Yes | Do better |
| Audience Z | No | No | Blue ocean |
| Price point | $99/mo | $49/mo | $19/mo tier |

**Opportunity types:**
1. **Feature gap** - They don't have it
2. **Quality gap** - They do it poorly
3. **Audience gap** - They don't serve this segment
4. **Price gap** - They're too expensive for some
5. **Experience gap** - UX/onboarding is painful

#### Step 5: Define Your Differentiation

**Positioning statement:**

```
For [target audience]
Who [need/problem]
[Product name] is a [category]
That [key benefit]
Unlike [competitors]
We [key differentiator]
```

**Example:**
```
For solo freelancers
Who need simple project tracking
TaskLite is a project management tool
That focuses on single-person workflows
Unlike Asana or Monday
We have no team features, just personal productivity
```

---

## Templates

### Competitor Analysis Report

```markdown
## Competitor Analysis: [Your Product]

### Market Overview
- **Category:** [X]
- **Total competitors identified:** [X]
- **Date:** [X]

### Competitor Map

| Competitor | Type | Founded | Funding | Est. Users |
|------------|------|---------|---------|------------|
| [Name] | Direct | YYYY | $X | X |
| [Name] | Indirect | YYYY | $X | X |

### Detailed Analysis

#### [Competitor 1]
**Overview:** [Brief description]
**Website:** [URL]

**Product:**
- Core features: [List]
- Unique features: [List]
- Missing features: [List]

**Pricing:**
| Tier | Price | Features |
|------|-------|----------|
| Free | $0 | [X] |
| Pro | $X/mo | [X] |

**Target audience:** [Who]
**Positioning:** [Message]

**Strengths:**
1. [X]
2. [X]

**Weaknesses:**
1. [X]
2. [X]

**Notable reviews:**
- Good: "[Quote]"
- Bad: "[Quote]"

---

#### [Competitor 2]
...

### Positioning Matrix

[Draw or describe the matrix position of each competitor]

### Gap Analysis

| Gap Type | Opportunity | Competitors Missing | Priority |
|----------|-------------|---------------------|----------|
| Feature | [X] | A, B, C | High |
| Audience | [X] | All | Medium |
| Price | [X] | A, B | High |

### Our Differentiation

**Positioning:**
For [audience] who [need], we are [category] that [benefit].
Unlike [competitors], we [differentiator].

**Key differentiators:**
1. [X]
2. [X]
3. [X]

### Ongoing Monitoring

| Competitor | Track What | Frequency |
|------------|------------|-----------|
| [Name] | Pricing, features | Monthly |
| [Name] | Content, messaging | Weekly |
```

### Quick Competitor Snapshot

```markdown
## [Competitor Name] Snapshot

**Website:** [URL]
**Founded:** [Year]
**Employees:** ~[X]
**Funding:** $[X]

### Product
**What it does:** [1 sentence]
**Key features:** [3-5 bullets]

### Pricing
| Tier | Price | Main Features |
|------|-------|---------------|
| [X] | $X | [X] |

### Strengths
1. [X]
2. [X]

### Weaknesses
1. [X]
2. [X]

### Opportunity for Us
[What can we do better?]
```

---

## Examples

### Example 1: Competitor Analysis for Note-Taking App

**Market:** Personal knowledge management

**Competitors analyzed:**
- Direct: Notion, Obsidian, Roam Research
- Indirect: Apple Notes, Google Docs
- Future: AI writing tools

**Key findings:**

| Competitor | Strength | Weakness | Opportunity |
|------------|----------|----------|-------------|
| Notion | All-in-one | Slow, complex | Speed, simplicity |
| Obsidian | Local-first, plugins | Steep learning | Easier onboarding |
| Roam | Backlinks | Expensive, dated UI | Better UX at lower price |

**Positioning:**
"For busy professionals who want fast, simple notes with linking.
Unlike Notion, we're single-purpose and lightning fast.
Unlike Obsidian, we work great out of the box."

### Example 2: Competitor Analysis for Email Marketing

**Market:** Email marketing for solopreneurs

**Gap discovered:**
- All tools price by subscriber count
- Solopreneurs hit paywalls early
- No tool focuses on <1000 subscribers

**Opportunity:**
"Generous free tier (5000 subscribers), solo-focused features, no team complexity"

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Only direct competitors | Include indirect and future |
| Surface-level analysis | Dig into reviews, pricing pages, features |
| Copying competitors | Find gaps to differentiate |
| One-time analysis | Set up ongoing monitoring |
| Competitor obsession | Focus on customers, not competitors |
| Ignoring weaknesses | Your differentiation is their weakness |

---

## Related Methodologies

- **niche-evaluation:** Niche Evaluation
- **market-research-tam-sam-som:** Market Research (TAM/SAM/SOM)
- **pricing-research:** Pricing Research
- **mvp-scoping:** MVP Scoping
- **gtm-strategy:** GTM Strategy

---

## Agent

**faion-competitor-analyzer-agent** helps analyze competition. Invoke with:
- "Analyze competitors in [market]"
- "Find competitors for [product idea]"
- "What are the weaknesses of [competitor]?"
- "How should I differentiate from [competitor]?"

---

*Methodology | Research | Version 1.0*
