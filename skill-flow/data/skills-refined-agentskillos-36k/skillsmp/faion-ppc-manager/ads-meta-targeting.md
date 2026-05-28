---
id: meta-targeting
name: "Meta Targeting & Audiences"
domain: ADS
skill: faion-marketing-manager
category: "advertising"
---

# Meta Targeting & Audiences

## Metadata

| Field | Value |
|-------|-------|
| **ID** | meta-targeting |
| **Name** | Meta Targeting & Audiences |
| **Category** | Ads API |
| **Difficulty** | Intermediate |
| **Agent** | faion-ads-agent |
| **Related** | meta-campaign-setup, meta-creative, paid-acquisition |

---

## Problem

Your ads reach the wrong people. You're paying to show ads to people who will never buy. Targeting is the difference between 2% and 0.2% conversion rates - a 10x impact on your CAC.

The key is building audiences that match your customer profile and iterating based on performance.

---

## Framework

Meta offers three audience types:

```
CORE      -> Interest, demographic, behavior targeting
CUSTOM    -> Your own data (website, email, engagement)
LOOKALIKE -> Meta finds similar people to your best customers
```

### Step 1: Core Audiences (Cold Traffic)

**Core audience components:**

| Component | Examples |
|-----------|----------|
| **Location** | Countries, cities, radius |
| **Age** | 18-65+ in ranges |
| **Gender** | All, Men, Women |
| **Languages** | Match content language |
| **Interests** | Hobbies, brands, topics |
| **Behaviors** | Purchase behavior, device use |
| **Demographics** | Job title, education, life events |

**Interest targeting strategy:**
- Start with 5-10 related interests
- Layer with behaviors when possible
- Exclude irrelevant segments

**Finding interests:**
- Competitor brands
- Industry publications
- Related tools they use
- Communities they belong to

### Step 2: Custom Audiences (Warm Traffic)

**Custom audience sources:**

| Source | Use Case | Minimum Size |
|--------|----------|--------------|
| Website visitors | Retargeting | 1,000+ |
| Email list | Re-engage customers | 1,000+ |
| App users | App remarketing | 1,000+ |
| Video viewers | Engaged prospects | Any |
| Lead form openers | High-intent leads | Any |
| Instagram/FB engaged | Social proof seekers | Any |

**Website custom audiences:**
```
All visitors (180 days)    -> Broad retargeting
Visited pricing (30 days)  -> High intent
Added to cart (7 days)     -> Hot leads
Purchasers (180 days)      -> Upsell/cross-sell
```

**Exclusions:**
- Always exclude recent purchasers from acquisition
- Exclude leads from lead gen campaigns
- Create exclusion audiences

### Step 3: Lookalike Audiences (Scale)

**Lookalike basics:**
- Based on a source audience
- Meta finds similar users
- Percentages: 1%, 2%, 5%, 10%

**Best source audiences (ranked):**
1. Purchasers/customers
2. High-value customers
3. Leads who converted
4. Website visitors with action
5. Email subscribers

**Lookalike strategy:**
```
LAL_Purchasers_1%    -> Best quality, smallest
LAL_Purchasers_2-3%  -> Balance of quality/scale
LAL_Purchasers_5-10% -> Scale, lower quality
```

**Minimum source size:**
- 1,000 people minimum
- Ideal: 2,000-10,000
- More data = better matching

### Step 4: Audience Layering

**Combine audiences for precision:**

```
Example: B2B SaaS targeting

Interests: SaaS, Startup, Entrepreneur
AND
Job Titles: Founder, CEO, Marketing Manager
AND
Behaviors: Business page admins
```

**Exclude to focus:**
```
Include: Website visitors last 30 days
Exclude: Purchasers last 180 days
= Active prospects who haven't bought
```

### Step 5: Testing Framework

**Audience testing approach:**

1. **Start broad:** Test 3-5 audience types
2. **Find winners:** Which has lowest CPA?
3. **Expand winners:** More segments in winning type
4. **Create lookalikes:** From best performers

**Testing structure:**
```
Campaign: Audience Testing
├── Ad Set: Interest_A (same ads)
├── Ad Set: Interest_B (same ads)
├── Ad Set: LAL_1% (same ads)
├── Ad Set: LAL_2-3% (same ads)
└── Ad Set: Retarget (same ads)

Keep ads identical to isolate audience performance
```

### Step 6: Advantage+ Audiences

**Meta's AI targeting:**
- Advantage+ Audience: Meta finds best people
- Audience suggestions: Starting point for Meta
- Use when: Large budgets, broad appeal products

**When to use each:**

| Targeting Type | Best For |
|----------------|----------|
| Manual/Core | Niche products, small budgets |
| Custom | Retargeting, existing customers |
| Lookalike | Scaling proven audiences |
| Advantage+ | Large scale, broad appeal |

---

## Templates

### Custom Audience Library

```markdown
## Website Audiences
- [ ] All visitors (180 days)
- [ ] All visitors (30 days)
- [ ] Pricing page (30 days)
- [ ] Blog visitors (60 days)
- [ ] Checkout visitors (7 days)
- [ ] Purchasers (180 days)

## Engagement Audiences
- [ ] Video viewers (25% watched)
- [ ] Video viewers (75% watched)
- [ ] Lead form openers
- [ ] Instagram engaged (90 days)
- [ ] Facebook engaged (90 days)

## Customer Audiences
- [ ] All customers (email upload)
- [ ] High-value customers
- [ ] Recent purchasers (30 days)
- [ ] Churned customers

## Exclusion Audiences
- [ ] Purchasers (180 days) - for acquisition
- [ ] Email subscribers - for list building
```

### Audience Testing Log

```markdown
## Test: [Name]

| Audience | Spend | Impressions | Clicks | Conversions | CPA |
|----------|-------|-------------|--------|-------------|-----|
| Interest A | $X | X | X | X | $X |
| Interest B | $X | X | X | X | $X |
| LAL 1% | $X | X | X | X | $X |

**Winner:** [Audience]
**Next steps:** [Action]
```

---

## Examples

### Example 1: SaaS Product

**Audience strategy:**
```
Cold (60% budget):
- Interests: SaaS, Startup tools, Competitors
- LAL 1%: Website leads

Warm (30% budget):
- Retarget: Pricing page visitors (14 days)
- Retarget: Demo request started, not completed

Hot (10% budget):
- Retarget: Trial users who didn't convert
```

### Example 2: E-commerce

**Audience strategy:**
```
Prospecting:
- LAL 1%: Purchasers
- LAL 2-3%: Add to cart
- Interests: Related products/brands

Retargeting:
- View content (7 days) - exclude purchasers
- Add to cart (3 days) - exclude purchasers
- Purchasers (30-90 days) - upsell

Loyalty:
- Purchasers 2+ times - new product launch
```

---

## Implementation Checklist

### Setup
- [ ] Create website custom audiences
- [ ] Upload customer email list
- [ ] Create engagement audiences
- [ ] Build exclusion audiences

### Lookalike Creation
- [ ] Create LAL from purchasers (1%, 2-3%)
- [ ] Create LAL from leads (1%, 2-3%)
- [ ] Create LAL from website visitors (1%, 2-3%)

### Testing
- [ ] Design test structure
- [ ] Keep creatives identical
- [ ] Set sufficient budget per audience
- [ ] Run for 7+ days

### Optimization
- [ ] Analyze performance by audience
- [ ] Scale winners
- [ ] Pause losers
- [ ] Create new variations of winners

---

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|--------------|-----|
| Too narrow | Not enough reach | 500K+ for interests |
| Too broad | Wasted spend | Layer targeting |
| No exclusions | Show to wrong people | Exclude customers |
| Stale audiences | Audience fatigue | Refresh regularly |
| Wrong LAL source | Poor quality matches | Use best customers |
| Testing too many | Can't get significance | 3-5 audiences max |

---

## Audience Size Guidelines

| Audience Type | Minimum | Ideal |
|---------------|---------|-------|
| Core/Interest | 500K | 1-5M |
| Custom (source) | 1,000 | 5,000+ |
| Lookalike | 500K | 1-2M |
| Retargeting | 1,000 | 10,000+ |

---

## Tools

| Purpose | Tools |
|---------|-------|
| Audience building | Meta Audiences tool |
| Email upload | Meta Custom Audiences |
| Pixel events | Events Manager |
| Competitor research | Meta Ad Library |
| Analytics | Meta Insights |

---

## Related Methodologies

- **meta-campaign-setup:** Meta Campaign Setup
- **meta-creative:** Meta Creative
- **retargeting:** Retargeting
- **paid-acquisition:** Paid Acquisition Overview

---

*Methodology: meta-targeting | Ads API | faion-ads-agent*
