---
id: paid-acquisition
name: "Paid Acquisition Overview"
domain: MKT
skill: faion-marketing-manager
category: "marketing"
---

# Paid Acquisition Overview

## Metadata

| Field | Value |
|-------|-------|
| **ID** | paid-acquisition |
| **Name** | Paid Acquisition Overview |
| **Category** | Marketing |
| **Difficulty** | Intermediate |
| **Agent** | faion-ads-agent |
| **Related** | meta-campaign-setup, google-campaign-setup, gtm-strategy |

---

## Problem

Organic growth is slow. You want customers now. Paid advertising can accelerate growth, but most founders burn money without results. They target wrong audiences, create boring ads, and don't track properly.

Paid acquisition works when you understand unit economics, test systematically, and scale what works. It's a skill that compounds.

---

## Framework

Paid acquisition follows a test-and-scale approach:

```
CALCULATE -> Know your numbers first
TEST      -> Small budget, multiple variations
ANALYZE   -> What's working, what's not
SCALE     -> Increase spend on winners
OPTIMIZE  -> Continuous improvement
```

### Step 1: Know Your Numbers

**Before spending $1, calculate:**

| Metric | Formula | Example |
|--------|---------|---------|
| **LTV** | ARPU x Avg. lifetime | $50/mo x 12 mo = $600 |
| **Target CAC** | LTV / 3 (SaaS rule) | $600 / 3 = $200 |
| **Conversion rate** | Historical or estimate | 3% of trials |
| **Max CPA** | Target CAC x Conv. rate | $200 x 0.03 = $6 |

**The golden ratio:**
```
LTV : CAC should be at least 3:1

If LTV = $300, CAC should be ≤$100
If you can't hit this, fix product/pricing first
```

### Step 2: Choose Your Channels

**Platform comparison:**

| Platform | Best For | Starting Budget | Learning Curve |
|----------|----------|-----------------|----------------|
| **Google Ads** | High intent, search | $500/mo | Medium |
| **Meta Ads** | B2C, broad targeting | $500/mo | Medium |
| **LinkedIn Ads** | B2B, professional | $1000/mo | Low |
| **Twitter/X Ads** | Tech, niche | $300/mo | Low |
| **Reddit Ads** | Niche communities | $200/mo | Low |
| **TikTok Ads** | Young, viral | $500/mo | High |

**Start with ONE channel.** Master it before adding more.

**Channel selection criteria:**
- Where does your audience spend time?
- What's your budget?
- What's your creative capability?
- What's your conversion type (purchase, signup, lead)?

### Step 3: Campaign Structure

**Standard structure:**

```
Campaign (budget level)
├── Ad Set 1 (audience A)
│   ├── Ad 1
│   ├── Ad 2
│   └── Ad 3
├── Ad Set 2 (audience B)
│   ├── Ad 1
│   ├── Ad 2
│   └── Ad 3
└── Ad Set 3 (audience C)
    ├── Ad 1
    ├── Ad 2
    └── Ad 3
```

**Testing framework:**
1. Start with 3-5 audiences
2. Run 3-5 ad variations per audience
3. Give each ad $20-50 before judging
4. Kill underperformers after 1000 impressions
5. Scale winners

### Step 4: Create High-Converting Ads

**Ad elements:**

| Element | Purpose | Best Practices |
|---------|---------|----------------|
| **Headline** | Stop the scroll | Problem or outcome focused |
| **Visual** | Attention grab | Real photos > stock, faces work |
| **Copy** | Convince to click | Benefit-focused, social proof |
| **CTA** | Drive action | Clear, specific action |

**Copy formulas:**

```
PAS (Problem-Agitate-Solve):
"Tired of [problem]? [Make it worse]. [Product] solves this by [benefit]."

Before/After:
"Before [Product]: [Pain state]. After: [Desired state]."

Social Proof:
"Join 5,000+ [audience] who [benefit]."
```

### Step 5: Tracking & Attribution

**Essential tracking:**

| Tool | Purpose |
|------|---------|
| **Pixel** | Track website events |
| **UTM parameters** | Identify traffic source |
| **Conversion API** | Server-side tracking |
| **Analytics** | Full funnel visibility |

**UTM structure:**
```
?utm_source=meta
&utm_medium=paid
&utm_campaign=campaign_name
&utm_content=ad_variation
```

**Conversion events to track:**
1. Page view
2. Lead (signup, form submit)
3. Trial start
4. Purchase
5. Subscription (if applicable)

### Step 6: Optimization Loop

**Weekly routine:**

| Day | Activity |
|-----|----------|
| Monday | Review last week's performance |
| Tuesday | Pause underperformers, increase winners |
| Wednesday | Create new ad variations |
| Thursday | Test new audiences |
| Friday | Analyze and plan next week |

**When to kill an ad:**
- CTR < 0.5% after 1000 impressions
- CPA > 2x target after $50 spend
- No conversions after 5x expected CPA spend

**When to scale:**
- CPA < target for 3+ days
- Consistent conversion volume
- Creative fatigue not visible

---

## Templates

### Campaign Planning Template

```markdown
## Campaign: [Name]

### Goals
- Objective: [Awareness/Traffic/Conversions]
- Target CPA: $[X]
- Daily budget: $[X]
- Test duration: [X] days

### Audience
- Demographics: [Age, location, gender]
- Interests: [List]
- Behaviors: [List]
- Lookalikes: [Source audience]

### Creative
- Format: [Image/Video/Carousel]
- Ad count: [X] variations
- Copy angles: [List]
- CTAs: [List]

### Tracking
- Pixel: [Installed]
- UTMs: [Structure]
- Conversion event: [Event name]

### Success Criteria
- Minimum data: [X] conversions
- Decision date: [Date]
```

### Weekly Ads Report

```markdown
## Week of [Date] Ads Report

### Summary
- Spend: $[X]
- Conversions: [X]
- CPA: $[X]
- ROAS: [X]:1

### By Campaign
| Campaign | Spend | Conv. | CPA | Status |
|----------|-------|-------|-----|--------|
| [Name]   | $X    | X     | $X  | Scale/Hold/Kill |

### Key Learnings
- [What worked]
- [What didn't]

### Next Week
- [ ] [Action 1]
- [ ] [Action 2]
- [ ] [Action 3]
```

---

## Examples

### Example 1: B2C SaaS

**Product:** Budget tracking app ($10/mo)

**Approach:**
- Platform: Meta Ads
- Targeting: Age 25-45, interest in personal finance
- Creative: Before/after screenshots
- Offer: 14-day free trial

**Results:**
- $2,000 spend over 30 days
- 400 trial signups ($5 CPA)
- 80 paid conversions (20% trial-to-paid)
- Effective CAC: $25 vs LTV $120

### Example 2: B2B Lead Gen

**Product:** Enterprise software (demo request)

**Approach:**
- Platform: LinkedIn Ads
- Targeting: Job titles + company size
- Creative: Customer testimonial video
- Offer: Free demo

**Results:**
- $5,000 spend over 30 days
- 50 demo requests ($100 CPL)
- 10 closed deals (20% close rate)
- CAC: $500 vs LTV $10,000

---

## Implementation Checklist

### Before Starting
- [ ] Calculate LTV and target CAC
- [ ] Install tracking pixels
- [ ] Set up conversion events
- [ ] Create UTM structure
- [ ] Prepare landing page

### Campaign Launch
- [ ] Choose one platform
- [ ] Define 3-5 audiences
- [ ] Create 3-5 ad variations
- [ ] Set daily budget ($20-50)
- [ ] Launch campaign

### Weekly Management
- [ ] Review performance data
- [ ] Kill underperformers
- [ ] Scale winners
- [ ] Create new variations
- [ ] Test new audiences

---

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|--------------|-----|
| No tracking | Can't measure ROI | Set up before spending |
| Too broad targeting | Wasted spend | Start narrow, expand |
| Too few creatives | Can't test | 3-5 minimum |
| Judging too early | Insufficient data | Wait for significance |
| Scaling too fast | Performance drops | 20-30% budget increases |
| Ignoring unit economics | Unprofitable | Calculate LTV:CAC first |

---

## Metrics to Track

| Metric | Definition | Good Benchmark |
|--------|------------|----------------|
| CTR | Clicks / Impressions | 1%+ |
| CPC | Cost / Clicks | Varies by platform |
| CVR | Conversions / Clicks | 2-5% |
| CPA | Cost / Conversions | < LTV/3 |
| ROAS | Revenue / Ad Spend | 3:1+ |

---

## Tools

| Purpose | Tools |
|---------|-------|
| Ad platforms | Meta Ads, Google Ads, LinkedIn |
| Analytics | GA4, Mixpanel, Amplitude |
| Landing pages | Unbounce, Webflow, Carrd |
| Creative | Canva, Figma, CapCut |
| Attribution | Triple Whale, Rockerbox |

---

## Related Methodologies

- **meta-campaign-setup:** Meta Campaign Setup (Facebook/Instagram)
- **google-campaign-setup:** Google Campaign Setup (Search/Display)
- **landing-page-design:** Landing Page Design (conversion)
- **ab-testing-ads:** A/B Testing Ads (optimization)

---

*Methodology: paid-acquisition | Marketing | faion-ads-agent*
