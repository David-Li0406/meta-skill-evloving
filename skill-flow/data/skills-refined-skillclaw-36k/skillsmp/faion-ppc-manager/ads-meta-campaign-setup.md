---
id: meta-campaign-setup
name: "Meta Campaign Setup"
domain: ADS
skill: faion-marketing-manager
category: "advertising"
---

# Meta Campaign Setup

## Metadata

| Field | Value |
|-------|-------|
| **ID** | meta-campaign-setup |
| **Name** | Meta Campaign Setup |
| **Category** | Ads API |
| **Difficulty** | Beginner |
| **Agent** | faion-ads-agent |
| **Related** | meta-targeting, meta-creative, paid-acquisition |

---

## Problem

You want to run Facebook/Instagram ads but the Ads Manager is overwhelming. There are dozens of options, campaign types, and settings. One wrong choice wastes your entire budget.

This methodology walks you through setting up your first campaign correctly.

---

## Framework

Meta campaigns follow a three-tier structure:

```
CAMPAIGN      -> Objective (what you want)
  └── AD SET  -> Targeting (who to reach)
      └── AD  -> Creative (what they see)
```

### Step 1: Install the Meta Pixel

**Before running any ads:**

1. Go to Events Manager
2. Create a new Pixel (if needed)
3. Install on your website
4. Verify events are tracking

**Standard events to track:**
- PageView (automatic)
- ViewContent
- AddToCart (e-commerce)
- InitiateCheckout
- Purchase
- Lead
- CompleteRegistration

**Verification:**
- Use Meta Pixel Helper Chrome extension
- Test conversion events manually
- Check Events Manager for data

### Step 2: Choose Campaign Objective

**Objectives mapped to goals:**

| Your Goal | Objective | Optimize For |
|-----------|-----------|--------------|
| Brand awareness | Awareness | Reach, impressions |
| Website traffic | Traffic | Link clicks, landing page views |
| Engagement | Engagement | Post interactions |
| Lead collection | Leads | Lead form submissions |
| App installs | App Installs | Installs |
| Sales/signups | Sales | Purchases, registrations |

**For most startups: Start with Sales or Leads objective.**

### Step 3: Campaign Settings

**Campaign structure:**
```
Campaign: [Product/Goal] - [Objective]
├── Ad Set: [Audience description]
│   ├── Ad 1: [Creative description]
│   ├── Ad 2: [Creative description]
│   └── Ad 3: [Creative description]
├── Ad Set: [Audience description]
│   └── ...
```

**Budget options:**

| Type | Best For | Setting |
|------|----------|---------|
| Campaign Budget Optimization (CBO) | Testing multiple ad sets | Campaign level |
| Ad Set Budget | Control per audience | Ad set level |

**Start with:** CBO, $20-50/day minimum

**Bidding:**
- Start with "Lowest Cost" (automatic)
- Move to "Cost Cap" once you know your target CPA

### Step 4: Ad Set Configuration

**Location and demographics:**
- Start with your primary market
- Age range based on customer data
- Language settings

**Detailed targeting:**
- Interests related to your product
- Behaviors (purchase history, device use)
- Demographics (job titles for B2B)

**Audience size:**
- 500K - 5M for interest targeting
- Too narrow = high CPMs, limited learning
- Too broad = irrelevant traffic

**Placements:**
- Start with Advantage+ Placements (automatic)
- Or manually select: Feed, Stories, Reels

### Step 5: Create Your First Ads

**Minimum creative set:**
- 3-5 ad variations per ad set
- Mix of formats (image, video, carousel)
- Different hooks and angles

**Ad components:**
- Primary text (125 chars shown, 125+ "See more")
- Headline (40 chars ideal)
- Description (optional, under headline)
- CTA button (Learn More, Sign Up, Shop Now)
- Image/Video

### Step 6: Launch and Monitor

**Pre-launch checklist:**
- [ ] Pixel verified and firing
- [ ] Conversion event selected
- [ ] Budget set
- [ ] Schedule set (or run continuously)
- [ ] Tracking parameters (UTMs)

**Learning phase:**
- Meta needs ~50 conversions per ad set per week
- Don't edit during learning phase (3-7 days)
- Performance may be volatile initially

---

## Templates

### Campaign Naming Convention

```
[Product]_[Objective]_[Audience]_[Date]

Examples:
- SaaS_Leads_Interests_2026Q1
- Course_Sales_Lookalike_Jan2026
- App_Installs_RetargetingCart_2026
```

### Ad Set Naming Convention

```
[Audience Type]_[Demographics]_[Placement]

Examples:
- Interest_25-45_Auto
- LAL_Website_Feed
- Retarget_ViewContent_AllPlacements
```

### Campaign Setup Checklist

```markdown
## Campaign: [Name]

### Objective
- [ ] Objective selected: [___]
- [ ] Conversion event: [___]

### Budget
- [ ] Daily budget: $[___]
- [ ] Start date: [___]
- [ ] End date: [___ or ongoing]

### Ad Sets
- [ ] Audience 1: [Description]
- [ ] Audience 2: [Description]

### Ads
- [ ] 3+ creatives per ad set
- [ ] Primary text variations
- [ ] Headline variations

### Tracking
- [ ] Pixel installed
- [ ] UTM parameters set
- [ ] Conversion tracking verified
```

---

## Examples

### Example 1: SaaS Lead Generation

**Setup:**
```
Campaign: SaaS_Leads_CBO
├── Budget: $50/day
├── Objective: Leads
├── Conversion: Lead (form submit)
│
├── Ad Set 1: Interests_Founders
│   ├── Targeting: Startup, SaaS, Entrepreneur interests
│   ├── Age: 25-45
│   ├── Location: US
│   └── Ads: 4 variations
│
├── Ad Set 2: Interests_Marketers
│   └── Targeting: Marketing Manager, Growth interests
│
└── Ad Set 3: LAL_Website_1%
    └── Targeting: 1% lookalike of website visitors
```

### Example 2: E-commerce Sales

**Setup:**
```
Campaign: Ecom_Sales_CBO
├── Budget: $100/day
├── Objective: Sales
├── Conversion: Purchase
│
├── Ad Set 1: Interests_Fitness
├── Ad Set 2: Interests_Health
├── Ad Set 3: Retarget_AddToCart_7days
└── Ad Set 4: LAL_Purchasers_1%
```

---

## Implementation Checklist

### Before Setup
- [ ] Install Meta Pixel
- [ ] Verify events in Events Manager
- [ ] Define conversion event
- [ ] Set target CPA

### Campaign Creation
- [ ] Choose objective
- [ ] Set budget (CBO recommended)
- [ ] Name campaign clearly

### Ad Set Creation
- [ ] Define audience
- [ ] Set locations
- [ ] Choose placements
- [ ] Set optimization goal

### Ad Creation
- [ ] Upload 3+ creatives
- [ ] Write primary text
- [ ] Write headlines
- [ ] Set UTM parameters
- [ ] Preview on all placements

### Launch
- [ ] Review everything
- [ ] Publish campaign
- [ ] Monitor learning phase
- [ ] Don't edit for 3-7 days

---

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|--------------|-----|
| No pixel | Can't track conversions | Install before running ads |
| Wrong objective | Optimizing for wrong action | Match objective to goal |
| Too narrow audience | Limited learning | 500K+ audience |
| Too few creatives | Can't find winners | 3-5 per ad set |
| Editing during learning | Resets learning | Wait 3-7 days |
| No UTM tracking | Can't attribute in analytics | Always add UTMs |

---

## Metrics to Understand

| Metric | Definition | Good Benchmark |
|--------|------------|----------------|
| CPM | Cost per 1000 impressions | $5-20 |
| CPC | Cost per click | $0.50-2.00 |
| CTR | Click-through rate | 1%+ |
| CVR | Conversion rate | 2%+ |
| CPA | Cost per acquisition | Your target |
| ROAS | Return on ad spend | 3:1+ |

---

## Tools

| Purpose | Tools |
|---------|-------|
| Campaign management | Meta Ads Manager |
| Pixel verification | Meta Pixel Helper |
| Creative design | Canva, Figma |
| Landing pages | Webflow, Unbounce |
| Analytics | GA4, Mixpanel |

---

## Related Methodologies

- **meta-targeting:** Meta Targeting (audience setup)
- **meta-creative:** Meta Creative (ad creation)
- **meta-reporting:** Meta Reporting (analysis)
- **paid-acquisition:** Paid Acquisition Overview

---

*Methodology: meta-campaign-setup | Ads API | faion-ads-agent*
