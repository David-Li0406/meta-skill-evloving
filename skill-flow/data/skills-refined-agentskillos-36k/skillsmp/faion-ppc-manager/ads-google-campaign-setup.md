---
id: google-campaign-setup
name: "Google Ads Campaign Setup"
domain: ADS
skill: faion-marketing-manager
category: "advertising"
---

# Google Ads Campaign Setup

## Metadata

| Field | Value |
|-------|-------|
| **ID** | google-campaign-setup |
| **Name** | Google Ads Campaign Setup |
| **Category** | Ads API |
| **Difficulty** | Intermediate |
| **Agent** | faion-ads-agent |
| **Related** | google-keywords, google-creative, paid-acquisition |

---

## Problem

Google Ads can reach billions of people at the moment they're searching for your solution. But the platform is complex. Wrong settings burn through budget fast. Many advertisers never get past the learning phase.

This methodology covers the foundational setup to launch successful Google Ads campaigns.

---

## Framework

Google Ads has several campaign types:

```
SEARCH     -> Show ads when people search keywords
DISPLAY    -> Show image ads across websites
VIDEO      -> YouTube ads
SHOPPING   -> Product listings (e-commerce)
PMAX       -> AI-driven cross-channel
```

### Step 1: Set Up Conversion Tracking

**Before spending money:**

1. Create Google Ads account
2. Link to Google Analytics 4
3. Set up conversion actions
4. Install Google Tag (gtag.js)

**Conversion types:**

| Type | Use For |
|------|---------|
| Website purchase | E-commerce sales |
| Lead form submit | Lead generation |
| Sign up | SaaS trials |
| Phone call | Local businesses |
| App install | Mobile apps |

**Conversion setup:**
```
1. Tools & Settings → Conversions
2. Create new conversion
3. Select category (Purchase, Lead, etc.)
4. Set value (fixed or dynamic)
5. Set attribution window (30-day click)
6. Install tracking code
```

### Step 2: Choose Campaign Type

**Campaign type selection:**

| Goal | Campaign Type | When to Use |
|------|---------------|-------------|
| High intent leads | Search | People actively searching |
| Brand awareness | Display | Reach and frequency |
| Retargeting | Display | Re-engage visitors |
| Product sales | Shopping | E-commerce with feed |
| Video views | Video | YouTube content |
| Maximum reach | Performance Max | Trust AI, broad goals |

**For beginners: Start with Search.** It's most direct and easiest to optimize.

### Step 3: Campaign Settings

**Campaign setup:**

| Setting | Recommendation |
|---------|----------------|
| Campaign name | [Product]_[Type]_[Goal]_[Date] |
| Networks | Search Network only (uncheck Display) |
| Locations | Target your market specifically |
| Languages | Match your content |
| Bidding | Start with Maximize Conversions |
| Budget | $20-50/day minimum |

**Bidding strategies:**

| Strategy | When to Use |
|----------|-------------|
| Maximize Conversions | Starting out, need data |
| Target CPA | Have historical data, know CPA |
| Target ROAS | E-commerce, know value |
| Manual CPC | Full control, experienced |

### Step 4: Ad Group Structure

**Campaign structure:**
```
Campaign: [Product] Search
├── Ad Group 1: [Theme A]
│   ├── Keywords (10-20 related)
│   ├── Ad 1
│   └── Ad 2
├── Ad Group 2: [Theme B]
│   ├── Keywords (10-20 related)
│   ├── Ad 1
│   └── Ad 2
└── Ad Group 3: [Theme C]
```

**Ad group best practices:**
- One theme per ad group
- 10-20 keywords per group
- Keywords should share intent
- Ads match keyword theme

### Step 5: Create Search Ads

**Responsive Search Ads (RSA):**
- Up to 15 headlines
- Up to 4 descriptions
- Google tests combinations

**Headlines (30 chars each):**
- Include main keyword
- Highlight benefits
- Add social proof
- Include numbers
- Use CTAs

**Descriptions (90 chars each):**
- Expand on benefits
- Include differentiators
- Add urgency/offers
- Clear call to action

**Example RSA:**
```
Headlines:
H1: [Keyword] for Startups
H2: Trusted by 10,000+ Teams
H3: Start Free Trial Today
H4: Easy Setup in 5 Minutes
H5: Save 30% This Month

Descriptions:
D1: Get started in minutes. No credit card required.
    Join 10,000+ companies already using [Product].
D2: Automate your workflow and save 10+ hours per week.
    Rated #1 by G2 for ease of use. Try free.
```

### Step 6: Add Extensions

**Required extensions:**

| Extension | Purpose | Setup |
|-----------|---------|-------|
| Sitelinks | More links to click | 4-6 relevant pages |
| Callouts | Highlight benefits | "Free Trial" "24/7 Support" |
| Structured snippets | Feature categories | Types, features |
| Image | Visual element | Logo, product images |
| Call | Phone number | If phone leads valuable |

**Extension tips:**
- Use all relevant extensions
- More extensions = larger ads = higher CTR
- Keep them updated and relevant

---

## Templates

### Campaign Naming Convention

```
[Product]_[Type]_[Target]_[Date]

Examples:
- SaaS_Search_Branded_2026Q1
- Ecom_Shopping_Feed_Jan2026
- App_Video_Install_2026
```

### Search Campaign Checklist

```markdown
## Campaign: [Name]

### Settings
- [ ] Campaign type: Search
- [ ] Network: Search only
- [ ] Locations: [List]
- [ ] Languages: [List]
- [ ] Budget: $[X]/day
- [ ] Bidding: [Strategy]

### Ad Groups
- [ ] AG1: [Theme] - X keywords
- [ ] AG2: [Theme] - X keywords
- [ ] AG3: [Theme] - X keywords

### Ads
- [ ] 15 headlines per RSA
- [ ] 4 descriptions per RSA
- [ ] Include keywords in ads

### Extensions
- [ ] Sitelinks (4-6)
- [ ] Callouts (4-6)
- [ ] Structured snippets
- [ ] Images

### Tracking
- [ ] Conversion action set
- [ ] Google Tag installed
- [ ] Conversions firing
```

### Ad Copy Template

```markdown
## Ad Group: [Theme]

### Keywords Target
[Primary keyword]
[Secondary keyword]
[Related keywords]

### Headlines (15)
1. [Keyword]-focused
2. [Benefit 1]
3. [Benefit 2]
4. [Social proof]
5. [CTA]
6. [Offer/discount]
7. [Feature 1]
8. [Feature 2]
9. [Differentiator]
10. [Urgency]
11-15. [Variations of above]

### Descriptions (4)
1. [Expand on benefit + CTA]
2. [Features + social proof]
3. [Problem + solution]
4. [Offer + urgency]
```

---

## Examples

### Example 1: SaaS Lead Generation

**Campaign structure:**
```
Campaign: SaaS_Search_Demo_2026
├── AG: Project Management Software
│   ├── KW: project management software
│   ├── KW: project management tool
│   ├── KW: best project management app
│   └── Ads: 2 RSAs
├── AG: Team Collaboration Tools
│   ├── KW: team collaboration software
│   ├── KW: remote team tools
│   └── Ads: 2 RSAs
└── AG: Competitor Alternative
    ├── KW: [competitor] alternative
    ├── KW: [competitor] vs
    └── Ads: 2 RSAs
```

### Example 2: E-commerce

**Campaign structure:**
```
Campaign: Ecom_Search_Products
├── AG: Product Category A
├── AG: Product Category B
└── AG: Brand Terms

Campaign: Ecom_Shopping_All
├── Product Group: Category A
└── Product Group: Category B

Campaign: Ecom_PMax_Sales
└── Asset groups with products
```

---

## Implementation Checklist

### Pre-Launch
- [ ] Conversion tracking installed
- [ ] Test conversions firing
- [ ] Link to Google Analytics
- [ ] Create remarketing audience

### Campaign Setup
- [ ] Create campaign
- [ ] Set budget and bidding
- [ ] Configure location targeting
- [ ] Set up ad groups

### Ad Creation
- [ ] Write headlines (15 per ad)
- [ ] Write descriptions (4 per ad)
- [ ] Add all extensions
- [ ] Review ad strength

### Launch
- [ ] Review all settings
- [ ] Enable campaign
- [ ] Monitor first 24-48 hours
- [ ] Check for disapprovals

---

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|--------------|-----|
| No conversion tracking | Can't optimize | Install before launch |
| Display network on | Wasted spend | Uncheck in Search campaigns |
| Too broad keywords | Irrelevant clicks | Use exact/phrase match |
| One ad per group | No testing | 2-3 ads minimum |
| No extensions | Lower CTR | Add all relevant |
| Wrong bidding | Poor performance | Start with Maximize Conv. |

---

## Metrics to Understand

| Metric | Definition | Good Benchmark |
|--------|------------|----------------|
| Impressions | Times ad shown | Depends on budget |
| Clicks | Ad clicks | - |
| CTR | Click-through rate | 3%+ for search |
| Avg CPC | Cost per click | Industry varies |
| Conversions | Completed actions | - |
| Conv. rate | Conversions / Clicks | 3%+ |
| CPA | Cost per acquisition | Your target |
| Quality Score | 1-10 relevance | 7+ |

---

## Tools

| Purpose | Tools |
|---------|-------|
| Keyword research | Google Keyword Planner |
| Ad creation | Google Ads Editor |
| Tracking | Google Tag Manager |
| Analytics | GA4 |
| Reporting | Google Ads, Looker Studio |

---

## Related Methodologies

- **google-keywords:** Google Keywords (keyword research)
- **google-creative:** Google Creative (ad copy)
- **google-reporting:** Google Reporting
- **paid-acquisition:** Paid Acquisition Overview

---

*Methodology: google-campaign-setup | Ads API | faion-ads-agent*
