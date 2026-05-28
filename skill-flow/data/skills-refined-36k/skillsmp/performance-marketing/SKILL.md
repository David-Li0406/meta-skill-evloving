---
name: performance-marketing
description: Set up, optimize, and scale paid social campaigns on Meta (Facebook/Instagram), Google Ads, and TikTok. Master test budgets, creative testing, audience targeting, funnel metrics, and budget scaling strategies for maximum ROAS.
---

# Performance Marketing

Complete workflow for running profitable paid social campaigns from test budgets to scaled spend.

## When to Use

- Launching new paid campaigns (Meta, Google, TikTok)
- Testing creative variations and audiences
- Optimizing underperforming campaigns
- Scaling winning campaigns without killing performance
- Setting up tracking and attribution
- Analyzing funnel metrics (CPM, CTR, CPA, ROAS)
- Troubleshooting campaign issues

## Core Principles

```
TEST SMALL → FIND WINNERS → SCALE GRADUALLY

1. Start with $20-50/day test budgets
2. Test creative first, then audiences
3. Let data decide, not hunches
4. Scale winners, kill losers fast
5. Creative fatigue is your enemy
```

**Priority Hierarchy:**
```
1. CREATIVE (biggest impact - 70%)
2. AUDIENCE (20%)
3. PLACEMENT (7%)
4. BIDDING (3%)
```

---

## Workflow

### Step 1: Campaign Setup & Tracking

**Pre-Launch Checklist:**
```markdown
## Campaign Setup: [Campaign Name]

### Tracking Foundation
- [ ] Pixel/SDK installed and firing
- [ ] Conversion events defined (add-to-cart, purchase, signup, etc.)
- [ ] UTM parameters configured
- [ ] Attribution window chosen (7-day click, 1-day view standard)
- [ ] Test purchase/conversion to verify tracking

### Campaign Structure
- **Objective**: [ ] Awareness / [ ] Traffic / [ ] Conversions / [ ] App Installs
- **Campaign Budget Optimization (CBO)**: [ ] Yes / [ ] No
- **Daily budget**: $[X]
- **Test duration**: [X] days (minimum 3-5 days)
```

**Meta Ads Structure:**
```
CAMPAIGN (Objective)
└── AD SET (Audience + Budget + Placement)
    └── ADS (Creative variations)

RECOMMENDED:
├── 1 Campaign (Conversions objective)
├── 3-5 Ad Sets (Different audiences, $20-50/day each)
└── 3-5 Ads per set (Creative variations)
```

### Step 2: Audience Targeting Strategy

**Audience Testing Framework:**

**1. Lookalike Audiences** (Best for scaling)
```
Source Data:
- Top 1% of customers by LTV
- Recent purchasers (last 30 days)
- Email list of engaged users

Variations to Test:
- 1% LAL (most similar, smallest reach)
- 2-3% LAL (broader, more scale)
- 5-10% LAL (broad, testing only)
```

**2. Interest Targeting** (Discovery phase)
```
Strategy:
- Stack 3-5 related interests per ad set
- Avoid overlap between ad sets
- Test competitor interests
- Combine interests + behaviors

Example:
Ad Set 1: [Competitor A] + [Industry Publication]
Ad Set 2: [Behavior: Online shoppers] + [Interest: Your category]
Ad Set 3: [Related hobby] + [Job title]
```

**3. Broad Targeting** (Let algorithm optimize)
```
When to Use:
- You have 50+ conversions/week (algo has data)
- Pixel is mature (installed 30+ days)
- Testing new creative angles

Setup:
- Age + Gender + Geo ONLY
- No interests or behaviors
- Let Meta's AI find your audience
```

**Audience Testing Template:**
```markdown
## Audience Test: [Test Name]

**Objective**: Find best-performing audience
**Creative**: [Use proven winner - don't test both]
**Budget**: $30/day per audience x 5 days = $150/audience

| Audience Name | Targeting | Size | Hypothesis |
|---------------|-----------|------|------------|
| LAL 1% Buyers | Top customers | 200K | Most similar to best customers |
| Interest Stack | [List] | 1M | Topic relevance |
| Broad 25-45 | Age/geo only | 10M+ | Let algo find audience |

**Success Metric**: CPA under $[X]
**Duration**: 5 days
**Decision**: Scale winner, kill losers
```

### Step 3: Creative Testing (Most Important)

**Creative Testing Hierarchy:**
```
TEST IN THIS ORDER:
1. Hook (first 3 seconds) - biggest impact
2. Format (video vs static vs carousel)
3. Messaging angle (pain vs solution vs social proof)
4. Visual style (UGC vs polished vs animation)
5. CTA (learn more vs shop now vs sign up)
```

**Creative Test Template:**
```markdown
## Creative Test: [Test Name]

**Hypothesis**: [What you're testing - e.g., "Pain-focused hook will outperform benefit-focused"]
**Variable**: [Hook / Format / Angle / Style]
**Audience**: [Use consistent audience - don't test both]
**Budget**: $40/day x 3 creatives x 5 days = $600

**Control (Current Best)**:
- Hook: [Exact copy]
- Format: [Video/Static]
- CPA: $[X]

**Variant A**:
- Change: [What's different]
- Hypothesis: [Why this might win]

**Variant B**:
- Change: [What's different]
- Hypothesis: [Why this might win]

**Success Criteria**:
- Winner = 20%+ lower CPA than control
- Minimum 30 conversions per variant for significance

**Results**:
| Variant | Spend | Conv | CPA | CTR | Winner? |
|---------|-------|------|-----|-----|---------|
| Control | $200  |  10  | $20 | 1.5%|         |
| A       | $200  |  15  | $13 | 2.1%| ✅      |
| B       | $200  |  8   | $25 | 1.2%| ❌      |

**Decision**: Scale Variant A, kill B, iterate on A's angle
```

**Creative Brief for Ad Production:**
```markdown
## Ad Creative Brief

### Campaign Context
- **Product**: [What you're promoting]
- **Target audience**: [Demographics + psychographics]
- **Objective**: [Awareness / Traffic / Conversions]
- **Platform**: [Meta / TikTok / Google]

### Message
- **Key benefit**: [Single most important thing]
- **Pain point**: [Problem you're solving]
- **Proof point**: [Social proof, stats, testimonials]
- **CTA**: [Specific action]

### Creative Direction
- **Format**: [ ] Video (15s/30s) / [ ] Static / [ ] Carousel
- **Style**: [ ] UGC / [ ] Polished / [ ] Animation / [ ] Motion graphics
- **Hook concepts** (test 3):
  1. [Pain-focused]: "Tired of [problem]?"
  2. [Solution-focused]: "Finally, a way to [benefit]"
  3. [Social proof]: "Join [X] customers who [result]"

### Specifications
- **Aspect ratios**: 9:16 (Stories), 1:1 (Feed), 4:5 (Feed optimal)
- **File size**: Under 4GB
- **Text overlay**: Keep under 20% of image
- **Length**: 15-30s for best performance
```

### Step 4: Funnel Metrics Analysis

**Key Metrics by Funnel Stage:**

**Awareness (Top Funnel)**
```
CPM (Cost per 1,000 impressions)
├── Benchmark: $5-$15 (varies by industry/geo)
├── High CPM = Audience saturation or poor relevance score
└── Low CPM ≠ good if CTR is also low

Reach & Frequency
├── Frequency <3 = Healthy
├── Frequency 3-5 = Monitor for fatigue
└── Frequency >5 = Creative fatigue, refresh needed
```

**Consideration (Middle Funnel)**
```
CTR (Click-Through Rate)
├── Benchmark: 1-3% (social ads)
├── <1% = Hook/creative not resonating
└── >3% = Strong creative, test scaling

CPC (Cost Per Click)
├── Benchmark: $0.50-$3.00
├── High CPC + High CTR = Expensive audience
└── Low CPC + Low CTR = Low-quality clicks
```

**Conversion (Bottom Funnel)**
```
CVR (Conversion Rate)
├── Landing page: 10-30% (varies by offer)
├── <10% = Landing page issue, not ad issue
└── >30% = Excellent message match

CPA (Cost Per Acquisition)
├── Must be < Customer LTV
├── Target: CPA < (LTV * 0.33) for 3:1 ratio
└── Track by cohort, not blended

ROAS (Return on Ad Spend)
├── Benchmark: 2-4x for profitability
├── <2x = Unprofitable, fix or kill
└── >4x = Scale opportunity
```

**Funnel Health Dashboard:**
```markdown
## Campaign Metrics: [Campaign Name]

### Awareness
- Impressions: [X]
- CPM: $[X] (vs benchmark $10)
- Reach: [X unique users]
- Frequency: [X] (target <3)

### Consideration
- Clicks: [X]
- CTR: [X]% (benchmark 2%)
- CPC: $[X] (benchmark $1.50)
- Landing page views: [X]

### Conversion
- Conversions: [X]
- CVR: [X]% (benchmark 15%)
- CPA: $[X] (target $[X])
- ROAS: [X]x (target 3x)

### Diagnosis
- Bottleneck: [Awareness / Consideration / Conversion]
- Action: [What to optimize]
```

### Step 5: Budget Scaling Playbook

**When to Scale (All Must Be True):**
```
SCALE SIGNALS:
✅ CPA stable for 3-5 days
✅ CTR and CVR consistent (not declining)
✅ Sufficient conversion volume (50+/week minimum)
✅ Creative not fatiguing (frequency <4)
✅ ROAS above target
```

**How to Scale:**

**Option A: Vertical Scaling (Safer, Slower)**
```
METHOD: Increase budget gradually
├── Increase budget 20% every 2-3 days
├── Monitor CPA daily
├── Pause if CPA rises >30%
└── Takes 2-3 weeks to 3-5x budget

WHEN TO USE:
- Single winning ad set
- Limited total budget
- Risk-averse approach
```

**Option B: Horizontal Scaling (Faster, Riskier)**
```
METHOD: Duplicate winning elements
├── Duplicate ad set to new audience (LAL 2-3%)
├── Expand to new placements (Stories, Reels)
├── Add new geo/age ranges
└── Can scale 5-10x in 1 week

RISKS:
- Audience overlap
- Budget fragmentation
- Higher CPMs
```

**Option C: Creative Expansion (Best Long-Term)**
```
METHOD: Create new winning creative angles
├── Iterate on winning hook
├── Test new formats (video if static won, vice versa)
├── Different value props
└── Sustainable scaling through fresh creative

PROCESS:
1. Analyze what made winner work
2. Create 3 new variations on that angle
3. Test at original budget
4. Scale new winners
```

**Scaling Checklist:**
```markdown
## Scale Decision: [Campaign Name]

**Current Performance**:
- Daily spend: $[X]
- CPA: $[X] (stable [X] days)
- ROAS: [X]x
- Frequency: [X]
- Conversion volume: [X]/week

**Scale Approach**:
- [ ] Vertical: Increase budget 20% to $[X]/day
- [ ] Horizontal: Duplicate to LAL 2-3% audience
- [ ] Creative: Launch [X] new creative variations
- [ ] Geo: Expand to [new markets]

**Monitoring Plan**:
- Check CPA daily for [X] days
- Pause if CPA > $[X] (30% increase)
- Review creative fatigue (frequency) every 3 days
- Prepare new creative if frequency >4

**Rollback Plan**:
- If CPA increases >30%, reduce budget back to $[X]
- If performance doesn't stabilize in 3 days, pause scale
```

### Step 6: Troubleshooting Guide

**Problem: High CPM, Low CTR**
```
DIAGNOSIS: Creative not resonating
├── Audience sees ads but doesn't engage
└── Poor relevance score

FIXES:
1. Test new hooks (biggest impact)
2. Try different ad formats
3. Check audience relevance (too broad?)
4. Refresh creative
5. Check placement (turn off Audience Network if on)
```

**Problem: Good CTR, Low CVR**
```
DIAGNOSIS: Landing page issue
├── Ad promise doesn't match landing page
└── Conversion flow broken

FIXES:
1. Check page load speed (<3 seconds)
2. Ensure message match (ad copy = landing page headline)
3. Simplify conversion flow (fewer form fields)
4. A/B test landing pages
5. Check mobile experience (80% of traffic)
```

**Problem: Unstable CPA (Spikes Daily)**
```
DIAGNOSIS: Insufficient data or learning phase
├── Budget too low for algorithm to optimize
└── Not enough conversions per week

FIXES:
1. Increase budget for more conversion volume
2. Consolidate ad sets (fewer = more data per set)
3. Wait for learning phase to exit (50 conversions)
4. Expand conversion window (7-day vs 1-day)
5. Consider value optimization vs conversion optimization
```

**Problem: Creative Fatigue**
```
DIAGNOSIS: Frequency too high (>5)
├── Same people seeing ad too often
└── CTR declining over time

FIXES:
1. Launch new creative variations
2. Expand audience size
3. Add exclusions (purchasers, recent site visitors)
4. Reduce budget to slow delivery
5. Pause ad set, refresh creative
```

---

## Campaign Templates

### Template 1: New Product Launch

```markdown
## Campaign: [Product Name] Launch

**Objective**: Drive sales
**Budget**: $500 test ($50/day x 10 days)
**Structure**:
- 1 Campaign (Conversions)
- 2 Ad Sets: Warm traffic + Cold traffic
- 6 Ads: 3 creative variations x 2 messaging angles

**Ad Set 1: Warm Traffic** ($30/day)
- Audience: Website visitors (30 days), Email list LAL 1%
- Creative: Direct CTA, "You've been waiting for this"
- Expected CPA: $15-25

**Ad Set 2: Cold Traffic** ($20/day)
- Audience: Interest targeting + LAL 1% customers
- Creative: Problem-focused hook, educational
- Expected CPA: $30-50

**Success**: CPA under $40, 10+ purchases
```

### Template 2: Retargeting Campaign

```markdown
## Campaign: Retargeting - Abandoned Carts

**Objective**: Conversions
**Budget**: $200/week
**Audience**: Added to cart, no purchase (7 days)

**Creative Strategy**:
- Reminder: "You left something in your cart"
- Urgency: "Limited stock" or "Offer expires"
- Incentive: Free shipping or 10% off code
- Social proof: "[X] customers bought this week"

**Expected Metrics**:
- CTR: 3-5% (warm audience)
- CVR: 20-40%
- ROAS: 5-10x
```

---

## Common Mistakes

| Don't | Do |
|-------|-----|
| Test creative and audience simultaneously | Test one variable at a time |
| Scale too fast (2x overnight) | Scale 20% every 2-3 days |
| Run too many ad sets (<$20/day each) | Consolidate for more data per set |
| Wait too long to kill losers (weeks) | Kill after 3-5 days if not performing |
| Ignore creative fatigue | Refresh creative when frequency >4 |
| Optimize for clicks on conversion campaigns | Optimize for your actual goal (purchases) |
| Set it and forget it | Check daily, especially first week |
| Only run one creative | Always have 3-5 variations testing |
| Copy exact settings from other campaigns | Every audience/product is different |

---

## Tools & Resources

**Campaign Planning:**
- Meta Business Suite (Ads Manager)
- Google Ads Editor
- TikTok Ads Manager

**Analytics:**
- Meta Pixel Helper (Chrome extension)
- Google Analytics 4
- Triple Whale or Northbeam (attribution)

**Creative Testing:**
- Meta A/B Test feature (built-in)
- Creative reporting (breakdown by creative)

**Benchmarking:**
- Meta Ads Library (see competitors' ads)
- WordStream Industry Benchmarks
- Your own historical data (best source)

---

## Related Skills

- `/ugc-content-creator` - Creating ad creative that performs
- `/copywriter` - Writing ad copy and CTAs
- `/social-media-ops` - Organic content that can scale to ads

---

**Last Updated**: 2026-01-22
