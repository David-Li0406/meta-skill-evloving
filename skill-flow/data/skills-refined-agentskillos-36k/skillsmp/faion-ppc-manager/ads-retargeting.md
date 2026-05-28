---
id: retargeting
name: "Retargeting"
domain: ADS
skill: faion-marketing-manager
category: "advertising"
---

# Retargeting

## Metadata

| Field | Value |
|-------|-------|
| **ID** | retargeting |
| **Name** | Retargeting |
| **Category** | Ads API |
| **Difficulty** | Beginner |
| **Agent** | faion-ads-agent |
| **Related** | meta-targeting, meta-campaign-setup, paid-acquisition |

---

## Problem

97% of website visitors leave without converting. You paid to get them there. Now they're gone. Without retargeting, you're starting from zero with every ad dollar.

Retargeting shows ads to people who already know you. They're warmer, more likely to convert, and cheaper to acquire.

---

## Framework

Retargeting follows the awareness-to-action path:

```
CAPTURE   -> Track website and engagement activity
SEGMENT   -> Group by behavior and intent
MESSAGE   -> Tailor ads to their stage
CONVERT   -> Drive them back to action
```

### Step 1: Set Up Tracking

**Required pixels:**

| Platform | Pixel | What It Tracks |
|----------|-------|----------------|
| Meta | Meta Pixel + CAPI | Page views, events |
| Google | Google Tag + Remarketing | Page views, conversions |
| LinkedIn | Insight Tag | Page views, conversions |
| Twitter | Twitter Pixel | Page views, events |

**Install before running any ads.**

**Standard events to track for retargeting:**
- Page views
- Content views (specific pages)
- Add to cart
- Begin checkout
- Form starts
- Video views
- Scroll depth

### Step 2: Create Audience Segments

**Segment by behavior and intent:**

| Segment | Definition | Intent Level |
|---------|------------|--------------|
| All visitors | Any page, last 180 days | Low |
| Blog readers | Blog pages, last 60 days | Low-Medium |
| Product viewers | Product pages, last 30 days | Medium |
| Pricing viewers | Pricing page, last 14 days | High |
| Cart abandoners | Added but didn't buy, last 7 days | Very High |
| Trial started | Started but didn't convert | Very High |
| Past customers | Purchased before | Warm (upsell) |

**Create segments in each platform:**

```
Meta Audiences:
├── Website visitors (180 days)
├── Blog visitors (60 days)
├── Product page (30 days)
├── Pricing page (14 days)
├── Add to cart (7 days)
├── Lead form opened (14 days)
└── Purchasers (180 days) - for exclusion
```

### Step 3: Match Messaging to Segment

**Messaging strategy by intent:**

| Segment | Message Focus | Offer |
|---------|---------------|-------|
| All visitors | Brand reminder, value prop | Content, free resource |
| Blog readers | Related content, expertise | More content, newsletter |
| Product viewers | Product benefits, features | Demo, free trial |
| Pricing viewers | Objection handling, comparison | Discount, extended trial |
| Cart abandoners | Urgency, reminder | Discount, free shipping |
| Past customers | New products, upgrades | Loyalty offer |

**Example ad copy by segment:**

**All visitors (awareness):**
```
Still thinking about [solving problem]?
Here's why [product] might be the answer.
[CTA: Learn More]
```

**Pricing visitors (high intent):**
```
Ready to get started?
Use code WELCOME for 20% off your first month.
[CTA: Start Free Trial]
```

**Cart abandoners (urgent):**
```
You left something behind!
Complete your order and get free shipping.
[CTA: Complete Order]
```

### Step 4: Set Frequency Caps

**Avoid ad fatigue:**

| Segment | Frequency Cap | Reasoning |
|---------|---------------|-----------|
| All visitors | 3/week | Don't overwhelm |
| High intent | 5/week | More touches OK |
| Cart abandoners | 7/week (first week) | Urgent window |

**Signs of fatigue:**
- CTR declining
- Frequency > 5
- Negative feedback increasing

**Refresh creative every 2-3 weeks.**

### Step 5: Exclude Converters

**Always exclude:**
- Recent purchasers (from acquisition)
- Current trials (from trial ads)
- Current subscribers

**Exclusion windows:**

| Conversion | Exclude For |
|------------|-------------|
| Purchase | 30-90 days (then upsell) |
| Trial start | Until trial ends |
| Lead form | Until sales follow-up complete |

### Step 6: Sequential Retargeting

**Tell a story over time:**

```
Stage 1 (Day 1-3):
"Did you see this?" - Reminder of what they viewed

Stage 2 (Day 4-7):
"Here's what you're missing" - Benefits focus

Stage 3 (Day 8-14):
"Others love it" - Social proof, testimonials

Stage 4 (Day 14+):
"Last chance" - Urgency, discount offer
```

---

## Templates

### Retargeting Audience Setup

```markdown
## Retargeting Audiences: [Product]

### Website Audiences
| Audience | Definition | Size | Status |
|----------|------------|------|--------|
| All visitors (180d) | Any page | X,XXX | Active |
| Blog readers (60d) | /blog/* | X,XXX | Active |
| Product page (30d) | /product/* | X,XXX | Active |
| Pricing (14d) | /pricing | XXX | Active |
| Cart abandon (7d) | add_to_cart, no purchase | XXX | Active |

### Exclusions
| Audience | Used To Exclude From |
|----------|---------------------|
| Purchasers (90d) | All prospecting |
| Trial users | Trial acquisition |

### Engagement Audiences
| Audience | Definition |
|----------|------------|
| Video viewers (50%) | Watched 50%+ |
| Lead form openers | Started form |
```

### Retargeting Campaign Structure

```markdown
## Retargeting Campaigns

### Campaign: Retargeting - Funnel

**Ad Set 1: Visitors (30-180 days)**
- Audience: All visitors, exclude recent
- Message: Brand reminder, value
- Budget: $X/day

**Ad Set 2: Engaged (7-30 days)**
- Audience: Product/pricing viewers
- Message: Benefits, social proof
- Budget: $X/day

**Ad Set 3: Hot (1-7 days)**
- Audience: Cart/form abandoners
- Message: Urgency, offer
- Budget: $X/day

### Exclusions Applied
- Purchasers (90d) excluded from all
- Each stage excludes higher-intent stages
```

---

## Examples

### Example 1: E-commerce Retargeting

**Audiences:**
- All visitors (30 days)
- Category viewers (14 days)
- Product viewers (7 days)
- Cart abandoners (3 days)

**Results:**
- Cart abandoner ROAS: 8:1
- Product viewer ROAS: 4:1
- All visitor ROAS: 2:1

**Insight:** Higher intent = higher ROAS. Allocate budget accordingly.

### Example 2: SaaS Retargeting

**Audiences:**
- Blog readers (60 days)
- Pricing page (14 days)
- Trial started, not converted (7 days)
- Demo requested, no show

**Results:**
- Pricing retargeting: $30 CPA (vs $80 cold)
- Trial retargeting: 20% conversion boost
- Blog retargeting: Good for brand, lower direct conversion

---

## Implementation Checklist

### Setup
- [ ] Install all tracking pixels
- [ ] Verify events firing
- [ ] Create website audiences
- [ ] Create engagement audiences
- [ ] Create exclusion audiences

### Campaigns
- [ ] Set up retargeting campaign
- [ ] Create ads for each segment
- [ ] Set frequency caps
- [ ] Apply exclusions

### Launch
- [ ] Start with small budget
- [ ] Monitor performance
- [ ] Adjust messaging based on results
- [ ] Refresh creative regularly

---

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|--------------|-----|
| Same message to everyone | Not relevant | Segment by intent |
| No frequency cap | Annoying users | Cap at 3-7/week |
| Not excluding converters | Wasted spend | Always exclude |
| Stale creative | Fatigue | Refresh every 2-3 weeks |
| Only cart abandoners | Missing others | Full-funnel retargeting |
| Too short window | Lose warm audience | 30-180 day windows |

---

## Retargeting Budget Guidelines

| Audience Size | Suggested Budget |
|---------------|------------------|
| <1,000 | $5-10/day |
| 1,000-5,000 | $10-25/day |
| 5,000-20,000 | $25-50/day |
| 20,000+ | $50-100/day |

**Rule of thumb:** Retargeting should be 20-30% of total ad spend.

---

## Metrics to Track

| Metric | Retargeting Benchmark | vs. Prospecting |
|--------|----------------------|-----------------|
| CTR | 0.7-1.5% | 2-3x higher |
| CVR | 3-8% | 2-4x higher |
| CPA | Varies | 40-70% lower |
| ROAS | 4-10:1 | 2-4x higher |

---

## Tools

| Purpose | Tools |
|---------|-------|
| Pixel installation | GTM, direct code |
| Audience building | Platform audience tools |
| Creative | Canva, Figma |
| Dynamic ads | Platform dynamic creative |

---

## Related Methodologies

- **meta-targeting:** Meta Targeting (audience building)
- **meta-campaign-setup:** Meta Campaign Setup
- **paid-acquisition:** Paid Acquisition Overview
- **email-marketing:** Email Marketing (email retargeting)

---

*Methodology: retargeting | Ads API | faion-ads-agent*
