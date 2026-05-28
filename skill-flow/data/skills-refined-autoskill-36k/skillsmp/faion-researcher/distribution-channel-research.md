---
id: distribution-channel-research
name: "Distribution Channel Research"
domain: RES
skill: faion-researcher
category: "research"
---

# Distribution Channel Research

## Metadata

| Field | Value |
|-------|-------|
| **ID** | (semantic) |
| **Category** | Research |
| **Difficulty** | Intermediate |
| **Tags** | #research, #distribution, #channels |
| **Domain Skill** | faion-researcher |
| **Agents** | faion-market-researcher-agent |

---

## Problem

"If you build it, they will come" is a myth. Common distribution failures:
- No clear channel strategy
- Trying all channels at once
- Picking channels based on preference, not fit
- No understanding of channel economics

**The root cause:** Not researching how customers actually discover and adopt products.

---

## Framework

### What is Distribution Channel Research?

Distribution channel research is identifying and evaluating the pathways to reach customers. It answers: "How will people find and start using this?"

### Channel Categories

#### 1. Organic Channels

| Channel | Description | Timeline | Cost |
|---------|-------------|----------|------|
| SEO | Search engine rankings | 6-12 months | Low |
| Content marketing | Blog, video, podcast | 3-6 months | Low-Med |
| Social media organic | Building following | 3-6 months | Low |
| Community building | Forum, Discord, Slack | 6+ months | Low |
| Word of mouth | Customer referrals | Ongoing | Free |
| Product-led growth | In-product virality | Varies | Low |

**Best for:** Long-term sustainable growth, lower CAC

#### 2. Paid Channels

| Channel | Description | Timeline | Cost |
|---------|-------------|----------|------|
| Search ads | Google, Bing | Immediate | High |
| Social ads | Meta, LinkedIn, Twitter | Immediate | Med-High |
| Display/programmatic | Banner ads | Immediate | Medium |
| Influencer | Sponsored content | 1-4 weeks | Varies |
| Affiliate | Revenue share | 1-2 months | Variable |
| Sponsorships | Podcast, newsletter | 1-4 weeks | Med-High |

**Best for:** Fast testing, scaling proven models

#### 3. Sales-Led Channels

| Channel | Description | Timeline | Cost |
|---------|-------------|----------|------|
| Outbound sales | Cold email/call | Immediate | High |
| Partnerships | Co-marketing, integrations | 2-6 months | Medium |
| Conferences | Events, booths | 1-3 months | High |
| Webinars | Educational sales | 1-2 weeks | Low-Med |

**Best for:** High-value B2B, complex products

#### 4. Viral/Network Channels

| Channel | Description | Timeline | Cost |
|---------|-------------|----------|------|
| Referral program | Incentivized sharing | 1-2 months | Variable |
| Integrations | App marketplaces | 2-4 months | Medium |
| Embeds | Widgets, badges | 1-2 months | Low |
| User-generated content | Templates, showcases | 2-4 months | Low |

**Best for:** Products with network effects

### Channel Research Process

#### Step 1: Map Customer Discovery

**Research questions:**
- Where does your target audience hang out online?
- What do they read/watch/listen to?
- How did they find current solutions?
- What influences their decisions?

**Data sources:**
- Customer interviews: "How did you hear about us?"
- Survey: "Where do you discover new tools?"
- Analytics: "What's our traffic source?"
- Competitor analysis: "Where do they advertise?"

#### Step 2: Evaluate Channel Fit

**Channel-Product Fit Matrix:**

| Factor | Weight | Score (1-5) |
|--------|--------|-------------|
| Audience presence | 25% | |
| Competitors using | 15% | |
| Cost to test | 20% | |
| Time to results | 15% | |
| Scalability | 15% | |
| Team capability | 10% | |

**Score each channel, prioritize highest scorers.**

#### Step 3: Model Channel Economics

**Per channel:**
```
Cost per impression: $X
Click-through rate: X%
Cost per click: $X
Conversion rate: X%
Cost per acquisition: $X
Customer lifetime value: $X
LTV:CAC: X:1
```

**Viable channel:** LTV:CAC > 3:1

#### Step 4: Test and Validate

**Testing framework:**
1. **Micro-test:** $100-500, 1-2 weeks
2. **Validate:** Did we get signal?
3. **Scale test:** $1-5K, 1 month
4. **Optimize:** Improve conversion
5. **Scale:** Increase budget

**Success criteria:**
- CAC within target
- Quality of leads acceptable
- Channel is scalable

#### Step 5: Build Channel Mix

**Portfolio approach:**

| Stage | Focus |
|-------|-------|
| 0-$10K MRR | 1 channel, master it |
| $10-50K MRR | 2-3 channels |
| $50K+ MRR | Diversified mix |

**Rule:** 80% effort on 1-2 proven channels, 20% on experiments.

---

## Templates

### Channel Research Report

```markdown
## Channel Research: [Product]

### Customer Discovery Research

**Interview insights (N=X):**
- "I found [competitor] via [channel]"
- "I usually discover tools through [source]"

**Top discovery sources:**
1. [Channel 1]: [X]% of customers
2. [Channel 2]: [X]% of customers
3. [Channel 3]: [X]% of customers

### Channel Evaluation

| Channel | Audience | Cost | Time | Scale | Fit | Score |
|---------|----------|------|------|-------|-----|-------|
| [Ch 1] | 5 | 4 | 3 | 4 | 5 | 4.2 |
| [Ch 2] | 4 | 3 | 4 | 3 | 4 | 3.6 |
| [Ch 3] | 3 | 5 | 5 | 2 | 3 | 3.4 |

### Channel Economics (Estimated)

| Channel | CAC Est. | LTV:CAC | Time to ROI |
|---------|----------|---------|-------------|
| [Ch 1] | $X | X:1 | X weeks |
| [Ch 2] | $X | X:1 | X months |

### Competitor Channel Analysis

| Competitor | Primary Channel | Secondary | Notes |
|------------|-----------------|-----------|-------|
| [Comp 1] | [Channel] | [Channel] | [Observation] |
| [Comp 2] | [Channel] | [Channel] | [Observation] |

### Recommended Channel Strategy

**Phase 1 (Months 1-3):**
- Primary: [Channel]
- Test budget: $[X]
- Success metric: [X]

**Phase 2 (Months 4-6):**
- Add: [Channel 2]
- Scale: [Channel 1] if working

### Testing Plan

| Channel | Test Budget | Duration | Success Criteria |
|---------|-------------|----------|------------------|
| [Ch 1] | $X | X weeks | CAC < $X |
| [Ch 2] | $X | X weeks | X signups |
```

### Channel Test Report

```markdown
## Channel Test: [Channel Name]

### Test Parameters
- **Budget:** $[X]
- **Duration:** [X] days
- **Targeting:** [Audience]
- **Creative:** [Description]

### Results

| Metric | Target | Actual |
|--------|--------|--------|
| Impressions | [X] | [X] |
| Clicks | [X] | [X] |
| CTR | [X]% | [X]% |
| Signups | [X] | [X] |
| Conversion rate | [X]% | [X]% |
| CPC | $[X] | $[X] |
| CAC | $[X] | $[X] |

### Analysis
- **What worked:** [Observation]
- **What didn't:** [Observation]
- **Learnings:** [Key insights]

### Recommendation
[ ] Scale (increase budget to $X)
[ ] Optimize (adjust targeting/creative)
[ ] Pause (channel not viable)
[ ] Kill (move to other channels)

### Next Steps
1. [Action]
2. [Action]
```

---

## Examples

### Example 1: B2B SaaS Tool

**Customer research findings:**
- 60% discover via Google search
- 25% via peer recommendations
- 15% via LinkedIn

**Channel strategy:**
1. **SEO (Primary):** Content for "how to [problem]" keywords
2. **LinkedIn (Secondary):** Thought leadership + ads
3. **Referral (Tertiary):** In-product referral program

**Economics:**
- SEO CAC: $20 (after 6 months)
- LinkedIn CAC: $150
- Referral CAC: $30

### Example 2: Consumer Mobile App

**Customer research findings:**
- 45% from App Store search
- 30% from friend recommendation
- 25% from Instagram/TikTok

**Channel strategy:**
1. **ASO (Primary):** App Store optimization
2. **Viral loops (Secondary):** Shareable content/results
3. **TikTok organic (Tertiary):** Viral content attempts

**Economics:**
- ASO: Free (organic installs)
- Viral: $5 CAC (referral incentive)
- TikTok ads: $2 CPI

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Trying all channels | Focus on 1-2 initially |
| No testing budget | Allocate $500-2K for experiments |
| Copying competitor channels | Validate fit for your product |
| Ignoring economics | Calculate CAC before scaling |
| Giving up too early | Give channels 4-6 weeks minimum |
| No tracking | Set up attribution from day one |

---

## Related Methodologies

- **competitor-analysis:** Competitor Analysis
- **business-model-research:** Business Model Research
- **gtm-strategy:** GTM Strategy
- **seo-fundamentals:** SEO Fundamentals
- **aarrr-pirate-metrics:** AARRR Pirate Metrics

---

## Agent

**faion-market-researcher-agent** helps with channel research. Invoke with:
- "What channels should I use for [product]?"
- "Analyze distribution channels for [market]"
- "Design a channel test for [audience]"
- "Calculate channel economics for [numbers]"

---

*Methodology | Research | Version 1.0*
