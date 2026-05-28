---
id: niche-evaluation
name: "Niche Evaluation"
domain: RES
skill: faion-researcher
category: "research"
---

# Niche Evaluation

## Metadata

| Field | Value |
|-------|-------|
| **ID** | (semantic) |
| **Category** | Research |
| **Difficulty** | Beginner |
| **Tags** | #research, #niche, #evaluation |
| **Domain Skill** | faion-researcher |
| **Agents** | faion-niche-evaluator-agent |

---

## Problem

After generating ideas, solopreneurs struggle to evaluate which niche is worth pursuing. Common issues:
- Picking niches too broad (competing with giants)
- Picking niches too small (no revenue potential)
- Choosing based on gut feeling, not data
- Ignoring competition until it's too late

**The root cause:** No systematic criteria for evaluating niche viability.

---

## Framework

### What is Niche Evaluation?

Niche evaluation is the process of analyzing a market segment to determine if it's viable for your business. A good niche is specific enough to dominate but large enough to sustain revenue.

### The Niche Evaluation Framework

#### Step 1: Define the Niche Precisely

Use this formula:
```
[Product Type] for [Specific Audience] who [Specific Problem]
```

**Bad:** "Project management software"
**Good:** "Task tracking for freelance designers who struggle with client deadlines"

#### Step 2: Market Size Assessment

Calculate potential:

| Metric | How to Find | Target |
|--------|-------------|--------|
| TAM | Industry reports | $1B+ |
| SAM | Your geography/segment | $100M+ |
| SOM | Realistic capture | $1M+ |

**Quick validation:**
- Google Trends: Is interest growing?
- Keyword volume: Are people searching?
- Reddit/Community size: Are people talking?

#### Step 3: Competition Analysis

Map competitors on this matrix:

```
                Quality
                  High
                   |
    Opportunity  |  Premium
    Zone         |  Competitors
    ------------.------------
    Race to     |  Crowded
    Bottom      |  Market
                   |
                  Low
       Low -------|-------- High
              Number of Players
```

**Best position:** High quality, few competitors.

#### Step 4: Audience Accessibility

Answer these:

| Question | Score (1-5) |
|----------|-------------|
| Can I reach them organically (Reddit, Twitter, etc.)? | |
| Do they hang out in specific communities? | |
| Are there podcasts/blogs in this niche? | |
| Can I buy ads to reach them? | |
| Do they have money to spend? | |

**Target:** Average score > 3.5

#### Step 5: Monetization Potential

Evaluate revenue models:

| Model | Fit | Price Point | Recurring? |
|-------|-----|-------------|------------|
| SaaS | ? | $X/mo | Yes |
| Course | ? | $X once | No |
| Templates | ? | $X once | No |
| Consulting | ? | $X/hr | Varies |
| Ads | ? | CPM | Yes |

**Question:** Can you charge $50+/month or $200+ one-time?

#### Step 6: Personal Fit Assessment

Rate honestly:

| Factor | Score (1-5) |
|--------|-------------|
| I understand this audience | |
| I have skills relevant to the problem | |
| I'm excited to work on this daily | |
| I can create content about this | |
| I have connections in this space | |

**Rule:** If personal fit < 3, reconsider even if market is great.

### Niche Scoring Formula

```
Niche Score = (Market × 0.25) + (Competition × 0.20) +
              (Accessibility × 0.15) + (Monetization × 0.20) +
              (Personal Fit × 0.20)
```

**Thresholds:**
- Score > 4.0: Excellent, proceed immediately
- Score 3.5-4.0: Good, validate further
- Score 3.0-3.5: Risky, improve weak areas
- Score < 3.0: Reconsider or pivot

---

## Templates

### Niche Evaluation Scorecard

```markdown
## Niche: [Name]

### Definition
[Product Type] for [Specific Audience] who [Specific Problem]

### 1. Market Size (Weight: 25%)

| Metric | Value | Source |
|--------|-------|--------|
| TAM | $X | [source] |
| SAM | $X | [source] |
| SOM | $X | [calculation] |

Google Trends: [Growing/Stable/Declining]
Keyword Volume: [X searches/month]

**Score: [1-5]**

### 2. Competition (Weight: 20%)

| Competitor | Pricing | Strengths | Weaknesses |
|------------|---------|-----------|------------|
| [Name] | $X | | |
| [Name] | $X | | |

Position on Matrix: [Opportunity/Premium/Crowded/Race to Bottom]

**Score: [1-5]**

### 3. Audience Accessibility (Weight: 15%)

| Channel | Present? | Size |
|---------|----------|------|
| Reddit | Y/N | X members |
| Twitter/X | Y/N | X accounts |
| Podcasts | Y/N | X shows |
| Blogs | Y/N | X sites |
| Paid Ads | Y/N | CPM $X |

**Score: [1-5]**

### 4. Monetization Potential (Weight: 20%)

| Model | Viable? | Price Point |
|-------|---------|-------------|
| SaaS | Y/N | $X/mo |
| Course | Y/N | $X |
| Templates | Y/N | $X |
| Consulting | Y/N | $X/hr |

Willingness to Pay: [Evidence]

**Score: [1-5]**

### 5. Personal Fit (Weight: 20%)

| Factor | Score |
|--------|-------|
| Audience understanding | [1-5] |
| Relevant skills | [1-5] |
| Daily excitement | [1-5] |
| Content creation ability | [1-5] |
| Network connections | [1-5] |

**Average Score: [X]**

### Final Calculation

| Factor | Weight | Score | Weighted |
|--------|--------|-------|----------|
| Market Size | 25% | X | X |
| Competition | 20% | X | X |
| Accessibility | 15% | X | X |
| Monetization | 20% | X | X |
| Personal Fit | 20% | X | X |
| **TOTAL** | 100% | | **X** |

### Decision
[ ] Proceed with validation
[ ] Needs improvement in: [areas]
[ ] Reconsider/pivot
```

---

## Examples

### Example 1: Evaluating "AI Writing Tools for Lawyers"

**Definition:** AI-powered contract drafting tool for solo lawyers who waste hours on repetitive documents.

**Scores:**
- Market Size: 4 (legal tech $30B+, solo lawyers 350K+ in US)
- Competition: 4 (few specialized tools, mostly generic AI)
- Accessibility: 3 (legal communities exist but gatekept)
- Monetization: 5 (lawyers have money, $200+/mo viable)
- Personal Fit: 3 (knows AI, not law)

**Total: 3.85** - Good, but needs domain expertise partner.

### Example 2: Evaluating "Habit Tracking for Gamers"

**Definition:** Gamified habit tracker for PC gamers who want to build healthy routines.

**Scores:**
- Market Size: 3 (niche within productivity)
- Competition: 3 (habit apps exist, not gaming-focused)
- Accessibility: 5 (Reddit, Twitch, Discord easily reachable)
- Monetization: 2 (gamers resist subscriptions)
- Personal Fit: 5 (is a gamer, understands culture)

**Total: 3.4** - Risky due to monetization. Consider one-time purchase model.

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Niche too broad | Add "for [specific audience]" qualifier |
| Ignoring competition | Always map at least 5 competitors |
| Overweighting passion | Passion matters but won't compensate for bad market |
| Skipping market size | Even small niches should be quantified |
| Not talking to audience | Validation requires actual conversations |

---

## Related Methodologies

- **idea-generation:** Idea Generation
- **problem-validation:** Problem Validation
- **market-research-tam-sam-som:** Market Research (TAM/SAM/SOM)
- **competitor-analysis:** Competitor Analysis
- **mvp-scoping:** MVP Scoping

---

## Agent

**faion-niche-evaluator-agent** helps assess niche viability. Invoke with:
- "Evaluate this niche: [description]"
- "Compare these niches: [list]"
- "Find market size for [niche]"
- "Score my niche: [details]"

---

*Methodology | Research | Version 1.0*
