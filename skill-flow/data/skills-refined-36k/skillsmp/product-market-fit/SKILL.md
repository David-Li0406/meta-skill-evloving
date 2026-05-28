---
name: product-market-fit
description: Measure and diagnose product-market fit using retention cohorts, user surveys, engagement metrics, and qualitative signals. Systematic framework for B2C, B2B SaaS, and marketplace products to understand if you've achieved PMF.
---

# Product-Market Fit Measurement

Systematically measure, diagnose, and improve product-market fit using quantitative metrics and qualitative signals.

## When to Use

- Wondering if you've achieved product-market fit
- Preparing for fundraising (investors will ask about PMF)
- Deciding whether to scale or pivot
- Diagnosing why growth has stalled
- Prioritizing feature work (fix retention vs. add features)
- Setting team goals and OKRs around PMF

## Core Concept

**PMF is not binary** - it's a spectrum from "no PMF" to "strong PMF". Most products exist somewhere in between.

**Key Insight:** PMF is **dynamic, not static**. You can lose it as markets shift, competitors emerge, or user expectations evolve.

**What PMF Feels Like:**
- Users are pulling the product from you (not pushing on them)
- Retention curves flatten (users stick around)
- Organic growth happens (word of mouth, virality)
- Usage is habitual (users return without prompts)
- You're struggling to keep up with demand

---

## Workflow

### Step 1: Choose Your PMF Metrics (By Product Type)

**B2C Consumer Products:**

```markdown
## B2C PMF Metrics

**PRIMARY METRIC: Retention Cohorts**
- Day 1, Day 7, Day 30 retention rates
- When cohorts flatten = PMF signal
- Look for 40%+ D30 retention (B2C benchmark)

**SECONDARY METRICS:**
1. **Engagement Depth**
   - DAU/MAU ratio (>20% is strong)
   - Session frequency (how often users return)
   - Time spent per session

2. **Organic Growth**
   - Virality coefficient (K-factor)
   - Referral rate
   - Word-of-mouth attribution

3. **NPS Score**
   - Survey: "How likely to recommend?" (0-10 scale)
   - >50 NPS = strong PMF
   - 30-50 = moderate
   - <30 = weak

**QUALITATIVE SIGNALS:**
- Users complain when feature breaks
- Users request new features (engagement signal)
- Users create content about your product
- Users hack together workarounds for missing features
```

**B2B SaaS Products:**

```markdown
## B2B SaaS PMF Metrics

**PRIMARY METRIC: Net Revenue Retention (NRR)**
- Track cohort revenue over time
- >100% NRR = PMF (upsells > churn)
- 90-100% = moderate PMF
- <90% = weak PMF

**SECONDARY METRICS:**
1. **Logo Retention**
   - % of customers retained year-over-year
   - >90% logo retention = strong PMF

2. **Time to Value**
   - Days from signup to first value milestone
   - Faster = stronger PMF

3. **Sales Velocity**
   - Average deal size × win rate / sales cycle length
   - Increasing velocity = PMF improving

4. **40% Rule**
   - Growth rate + profit margin ≥ 40%
   - Public market benchmark for healthy SaaS

**QUALITATIVE SIGNALS:**
- Sales cycle shortening (buyers convinced faster)
- Champions emerge inside customer orgs
- Customers renew without negotiation
- Inbound leads increasing
```

**Marketplace / Platform Products:**

```markdown
## Marketplace PMF Metrics

**PRIMARY METRIC: Liquidity**
- Supply-side: % of suppliers getting transactions
- Demand-side: % of buyers finding what they want
- Match rate: successful transactions / attempts
- >60% match rate = strong liquidity

**SECONDARY METRICS:**
1. **Repeat Rate**
   - % of users who transact 2+ times
   - >40% repeat rate = PMF signal

2. **Cross-Side Network Effects**
   - Does adding supply increase demand?
   - Does adding demand increase supply?
   - Measure elasticity of each side

3. **Take Rate Sustainability**
   - Can you charge commission without disintermediation?
   - Are users willingly paying your fee?

**QUALITATIVE SIGNALS:**
- Suppliers asking to join (supply pull)
- Buyers returning frequently
- Low disintermediation (off-platform transactions)
```

---

### Step 2: The Sean Ellis Test (40% Rule)

**The Question:**
> "How would you feel if you could no longer use [product]?"
> - Very disappointed
> - Somewhat disappointed
> - Not disappointed

**Benchmark:**
- **≥40% "Very disappointed"** = Strong PMF
- 25-40% = Moderate PMF (keep improving)
- <25% = Weak PMF (major work needed)

**How to Run:**
1. Survey recent active users (used product in last 2 weeks)
2. Minimum 40-50 responses for statistical significance
3. Segment results by user type, use case, cohort
4. Ask follow-up: "What's the primary benefit you get from [product]?"

**Interpretation:**

```markdown
## Sean Ellis Test Results

| Score | Interpretation | Action |
|-------|---------------|---------|
| >50% | **Strong PMF** | Scale channels, optimize funnel |
| 40-50% | **Good PMF** | Nail positioning, improve retention |
| 25-40% | **Moderate PMF** | Double down on core users, cut features |
| <25% | **Weak/No PMF** | Pivot or major rework needed |

**Warning:** If >60% say "Very disappointed" but retention is still weak, you have a retention problem (not lack of love).
```

---

### Step 3: Retention Cohort Analysis

**What to Measure:**

```markdown
## Retention Cohort Framework

**STEP 1: Define "Retained User"**
Examples by product:
- Social app: opened app and viewed content
- SaaS tool: logged in and performed core action
- Marketplace: browsed listings or made inquiry
- Content platform: consumed 1+ piece of content

**STEP 2: Build Cohort Table**
Rows = Signup week/month
Columns = Time periods (Day 0, Day 1, Day 7, Day 30, etc.)
Cells = % of cohort still retained

Example:
| Cohort    | D0   | D1   | D7   | D30  | D60  | D90  |
|-----------|------|------|------|------|------|------|
| Week 1    | 100% | 40% | 25% | 15% | 13% | 12% |
| Week 2    | 100% | 45% | 30% | 18% | 16% | 15% |
| Week 3    | 100% | 50% | 35% | 22% | 20% | 19% |

**STEP 3: Look for Flattening**
- When curve flattens = natural retention floor
- Improving cohorts over time = PMF getting stronger
- If curve never flattens = churn problem

**BENCHMARKS:**
| Product Type | Good D30 Retention | Strong D30 Retention |
|--------------|-------------------|---------------------|
| Social/Content | 20-30% | >40% |
| Productivity | 30-40% | >50% |
| B2B SaaS | 50-70% | >80% |
| Marketplace | 15-25% | >35% |
```

**Diagnostic Questions:**

```markdown
## Retention Diagnostic

**If retention is WEAK (<15% D30):**
❌ Core value prop not resonating
❌ Onboarding not working (users don't get to "aha" moment)
❌ Product is nice-to-have, not must-have
❌ Wrong target audience

→ Action: Fix onboarding, talk to churned users, consider pivot

**If retention STARTS strong then drops:**
❌ Initial novelty wears off
❌ No habit formation (no trigger to return)
❌ Feature set too shallow (users exhaust value)
❌ Competing alternatives pulled them away

→ Action: Build engagement loops, add depth, improve notifications

**If retention is IMPROVING over cohorts:**
✅ PMF is getting stronger
✅ Product improvements are working
✅ Targeting is getting better

→ Action: Keep doing what you're doing, start scaling
```

---

### Step 4: Qualitative PMF Signals

**Strong PMF Signals:**

```markdown
## Qualitative PMF Checklist

✅ **User Pull (not push)**
- Users ask "When is [feature] coming?"
- Users complain loudly when things break
- Users create content/tutorials about your product
- Users recruit friends/colleagues without prompting

✅ **Organic Growth**
- Word-of-mouth referrals increasing
- Direct traffic growing (not just paid)
- Press/influencers covering you unsolicited
- Waitlist building organically

✅ **Habit Formation**
- Users return multiple times per week without prompts
- Usage integrated into existing workflows
- Users describe product as "essential" or "can't live without"

✅ **Market Pull**
- Inbound sales leads increasing
- Sales cycle shortening
- Customers closing themselves (low-touch sales)
- Buyers citing specific features/benefits (know what they want)

✅ **Team Focus**
- Engineering struggling to keep up with user demand
- Support tickets are mostly "how do I do X?" not "this is broken"
- Roadmap driven by user requests, not guesses

❌ **Weak PMF Signals:**
- You're chasing users for feedback
- Users say "nice tool" but don't use it
- Growth only happens when you pay for it
- Sales cycles are long and complex
- Users need heavy handholding to get value
```

---

### Step 5: PMF Stage Diagnosis

**Use this framework to diagnose where you are:**

```markdown
## PMF Stages

### Stage 0: No PMF
**Symptoms:**
- Retention <10% D30
- Sean Ellis <15%
- No organic growth
- Users ghost you after initial trial

**What to Do:**
1. Talk to 10-20 churned users (why did you leave?)
2. Identify if problem is positioning, product, or audience
3. Consider pivot or major rework
4. Do NOT scale marketing (throwing good money after bad)

---

### Stage 1: Weak PMF (10-25% "Very disappointed")
**Symptoms:**
- Some users love it, most don't
- Retention 10-20% D30
- Growth is slow and requires heavy push
- High variance in user satisfaction

**What to Do:**
1. Segment users: Who are the lovers vs. meh?
2. Double down on the lovers (ignore the rest)
3. Find 10 more users exactly like the lovers
4. Narrow positioning to that specific segment
5. Cut features that don't serve core users

---

### Stage 2: Moderate PMF (25-40% "Very disappointed")
**Symptoms:**
- Core users love it, retention flattening at 20-30% D30
- Some organic growth
- Clear positioning working for specific segment
- Founders still heavily involved in sales/support

**What to Do:**
1. Nail the positioning message (you've found product, now nail market)
2. Optimize onboarding (get more users to "aha" moment)
3. Build engagement loops (habit formation)
4. Scale channels that are already working (don't experiment yet)
5. Improve product for core use case (go deep, not wide)

---

### Stage 3: Strong PMF (40-50% "Very disappointed")
**Symptoms:**
- Retention >30% D30 and flattening
- Organic growth via word-of-mouth
- Inbound leads increasing
- Sales/support becoming repeatable
- Users vocally advocate for product

**What to Do:**
1. Scale acquisition channels aggressively
2. Build moats (network effects, data advantages)
3. Expand to adjacent segments carefully
4. Invest in infrastructure/team to handle growth
5. Maintain product quality (don't break what's working)

---

### Stage 4: Very Strong PMF (>50% "Very disappointed")
**Symptoms:**
- Retention >40% D30
- NRR >120% (B2B) or strong virality (B2C)
- Struggle to keep up with demand
- Competitors copying you

**What to Do:**
1. Scale aggressively (you've earned it)
2. Expand product surface area to capture more value
3. Geographic expansion
4. Platform / API opportunities
5. Don't get complacent (PMF can erode)
```

---

### Step 6: Common PMF Mistakes

```markdown
## Anti-Patterns

❌ **Mistake 1: Scaling Before PMF**
"We have 10K users, so let's run ads!"
→ Problem: Pouring water into leaky bucket. Fix retention first.
→ Test: If you stopped all paid acquisition, would you still grow?

❌ **Mistake 2: Building Features Users Don't Use**
"Users asked for [X], so we built it, but no one uses it"
→ Problem: Users don't know what they want. Watch behavior, not words.
→ Test: Do 10+ users use this feature weekly?

❌ **Mistake 3: Confusing Engagement with PMF**
"Our DAU/MAU is 40%!"
→ Problem: Engagement ≠ PMF. Could be novelty, not habit.
→ Test: Are cohorts flattening or still declining?

❌ **Mistake 4: Ignoring Churn to Chase Growth**
"We're growing 20% MoM but churn is 15%"
→ Problem: Treadmill growth. Not sustainable.
→ Test: What's net growth after churn?

❌ **Mistake 5: Averaging Across Segments**
"Average retention is 25%, so we're moderate PMF"
→ Problem: Could be 50% retention for one segment, 10% for another.
→ Test: Segment by user type, use case, acquisition channel.

❌ **Mistake 6: Declaring PMF Too Early**
"We hit $1M ARR, so we have PMF!"
→ Problem: Revenue ≠ PMF. Could be custom deals, not repeatable.
→ Test: Is sales motion repeatable? Is NRR >100%?
```

---

## PMF Tracking Dashboard

**Build a simple dashboard tracking:**

```markdown
## Weekly PMF Check-In

**QUANTITATIVE (Update Weekly):**
- [ ] Cohort retention (latest cohort D7, D30)
- [ ] DAU/MAU ratio (engagement)
- [ ] NRR (B2B) or virality coefficient (B2C)
- [ ] Organic vs. paid user split
- [ ] Sean Ellis score (run monthly)

**QUALITATIVE (Review Weekly):**
- [ ] Support ticket themes (problems vs. requests)
- [ ] Sales call feedback (objections vs. enthusiasm)
- [ ] User interviews (2-3 per week minimum)
- [ ] Social mentions / community activity
- [ ] Team gut check (do we feel PMF improving?)

**RED FLAGS (Review Weekly):**
- [ ] Retention declining cohort-over-cohort
- [ ] Churn accelerating
- [ ] Sales cycle lengthening
- [ ] Competitors winning deals
- [ ] Team morale dropping (sign of PMF eroding)
```

---

## Output Format

**When using this skill, provide:**

```markdown
## PMF Assessment for [Product]

### 1. Current PMF Stage
[No PMF / Weak / Moderate / Strong / Very Strong]

### 2. Key Metrics
- Sean Ellis Score: X% "Very disappointed"
- D30 Retention: X%
- [Product-specific metric]: X

### 3. Diagnosis
[What's working / What's not working]

### 4. Recommendations (Prioritized)
1. [Top priority action]
2. [Second priority]
3. [Third priority]

### 5. Red Flags
[Any warning signs to watch]

### 6. Next Milestone
[What metric needs to hit what number to move to next stage?]
```

---

## Related Skills

- `/retention-engagement` - Deep dive on retention strategies
- `/user-onboarding` - Fix onboarding to improve D1/D7 retention
- `/growth-loops` - Build organic growth mechanisms
- `/user-interviews` - Talk to users to diagnose PMF issues
- `/north-star-metrics` - Align team around PMF-related metric

---

**Last Updated**: 2026-01-22
