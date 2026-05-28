# Company Research Playbook

## When to Use
- Preparing for outbound outreach
- Qualifying inbound leads
- Partnership evaluation
- Competitive landscaping
- Investment/M&A research

## Quick Research (5 minutes)

For a fast company scan, gather:

1. **What they do** (homepage headline)
2. **Size** (employee count)
3. **Stage** (funding)
4. **Key person** (target contact)

Tool sequence:
```
web_search("[company] company" )
clearbit_company(domain)
apollo_people_search(company, title="VP Marketing")
```

## Deep Research (30 minutes)

For comprehensive company intelligence:

### Step 1: Foundation (Web + Enrichment)
```
web_search("[company] company overview")
web_search("[company] funding news")
clearbit_company(domain)
crunchbase_lookup(company)
```

### Step 2: Digital Presence
```
firecrawl_scrape(homepage_url)
firecrawl_scrape(pricing_url)  
firecrawl_scrape(about_url)
firecrawl_screenshot(homepage_url)
```

### Step 3: Technology
```
builtwith_lookup(domain)
```

### Step 4: People
```
apollo_people_search(company, titles=["CEO", "CTO", "VP Marketing", "Head of Growth"])
proxycurl_linkedin(ceo_linkedin_url)
proxycurl_linkedin(target_contact_linkedin_url)
```

### Step 5: Reviews & Sentiment
```
g2_scrape(company_or_product)
reddit_search("[company] review OR experience")
```

### Step 6: Recent Activity
```
web_search("[company] news 2024")
web_search("[company] product launch")
web_search("[company] announces")
```

## Research Checklist

### Company Basics
- [ ] One-line description
- [ ] Founded year
- [ ] Headquarters
- [ ] Employee count
- [ ] Industry/category

### Business Model
- [ ] Target customer (B2B/B2C, size, industry)
- [ ] Pricing model (subscription, usage, one-time)
- [ ] Pricing tiers (if public)
- [ ] Primary revenue stream

### Funding & Financials
- [ ] Total funding raised
- [ ] Last round (amount, date, investors)
- [ ] Key investors
- [ ] Revenue (if available)

### Technology
- [ ] Core tech stack
- [ ] Key integrations
- [ ] Platform dependencies

### People
- [ ] CEO/Founder
- [ ] Leadership team
- [ ] Target contact(s) for our outreach
- [ ] Recent hires (growth signals)

### Market Position
- [ ] Key competitors
- [ ] Differentiators
- [ ] Market share (if known)
- [ ] Key customers

### Recent Activity
- [ ] News in last 90 days
- [ ] Product launches
- [ ] Blog posts/content themes
- [ ] Job postings (growth areas)

## Outreach Angle Development

After gathering data, identify angles:

### Trigger-Based Angles
| Trigger | Angle |
|---------|-------|
| Recent funding | "Congrats on the raise — often a good time to invest in [our solution area]" |
| New hire in our area | "Saw you just hired [role] — they might find [our tool] useful for [specific task]" |
| Product launch | "Saw the [product] launch — curious how you're handling [related challenge]" |
| Expansion | "Noticed you're expanding into [market] — [our solution] helped [similar company] with that" |

### Pain-Point Angles
| Signal | Angle |
|--------|-------|
| Hiring for roles we automate | "Saw you're hiring [role] — some teams use [our tool] to [outcome] instead" |
| Using competitor | "Noticed you're using [competitor] — curious if [common pain point] is an issue" |
| Tech stack gap | "Saw you're using [tool A] and [tool B] but not [category we're in]" |
| Rapid growth | "Growing fast often breaks [process we help with]" |

### Personalization Angles
| Data Point | Angle |
|------------|-------|
| Founder background | Reference shared experience or industry |
| Recent content | Reference specific post or article |
| Company mission | Align our value to their mission |
| Shared connection | Mention mutual contact |

## Output Quality Checklist

Before delivering company research:

- [ ] All data points have sources
- [ ] Employee count is recent (note if from LinkedIn vs Clearbit)
- [ ] Funding data includes date of last round
- [ ] At least 2 actionable outreach angles
- [ ] Contact list includes verified emails
- [ ] Recent news is from last 90 days
