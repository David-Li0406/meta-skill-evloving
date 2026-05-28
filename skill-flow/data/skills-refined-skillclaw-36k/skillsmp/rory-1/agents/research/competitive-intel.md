# Competitive Intelligence Playbook

## When to Use
- Creating battle cards for sales
- Positioning/messaging development
- Product roadmap input
- Pricing strategy
- Win/loss analysis

## Competitor Categories

### Direct Competitors
Same product, same buyer, same problem.
→ Deep analysis required

### Indirect Competitors
Different product, same buyer, same budget.
→ Positioning awareness needed

### Alternatives
Different approach to same problem (including "do nothing").
→ Understand for objection handling

## Quick Competitive Scan (10 minutes)

For fast competitor overview:

```
web_search("[competitor] vs [us/category]")
firecrawl_scrape(competitor_homepage)
g2_scrape(competitor_product)
```

Output: One-paragraph summary + key differentiators

## Deep Competitive Analysis (1 hour)

### Phase 1: Product Intelligence

**Website Analysis**
```
firecrawl_scrape(homepage_url)
firecrawl_scrape(features_url)
firecrawl_scrape(pricing_url)
firecrawl_scrape(integrations_url)
firecrawl_screenshot(homepage_url)
firecrawl_screenshot(pricing_url)
```

**Key Questions:**
- What's their primary value prop (homepage headline)?
- What features do they emphasize?
- What's their pricing model and tiers?
- Who are their integration partners?

**Product Documentation**
```
firecrawl_scrape(docs_url)
firecrawl_scrape(changelog_url)
```

**Key Questions:**
- What features have they launched recently?
- What's their release velocity?
- What gaps exist in their docs?

### Phase 2: Market Position

**Review Mining**
```
g2_scrape(product_name)
capterra_scrape(product_name)
web_search("[competitor] reviews reddit")
reddit_search("[competitor] review OR experience OR alternative")
```

**Extract:**
- Overall rating + review count
- Top 3 things customers love
- Top 3 things customers complain about
- Common comparison competitors
- Buyer personas from reviews

**G2 Comparison Data**
```
g2_scrape("[competitor] vs [other competitor]")
g2_scrape("[competitor] alternatives")
```

### Phase 3: Company Intelligence

```
clearbit_company(domain)
crunchbase_lookup(company)
web_search("[competitor] funding")
web_search("[competitor] acquisition")
builtwith_lookup(domain)
```

**Key Questions:**
- How big are they? (employees, revenue if available)
- How much runway do they have?
- Who are their investors?
- What's their growth trajectory?

### Phase 4: Content & SEO

```
web_search("site:[competitor.com] blog")
firecrawl_scrape(blog_url)
web_search("[competitor] [key topic]")
```

**Key Questions:**
- What topics do they create content about?
- What keywords are they targeting?
- What's their content quality?
- Who writes for them?

### Phase 5: Sales & GTM

```
firecrawl_scrape(demo_page)
firecrawl_scrape(free_trial_page)
web_search("[competitor] sales process")
web_search("[competitor] customer success")
```

**Key Questions:**
- Self-serve or sales-led?
- Free trial or demo-first?
- What's their typical deal cycle?
- How do they onboard customers?

## Analysis Frameworks

### Feature Comparison Matrix

| Feature | Us | Competitor A | Competitor B |
|---------|----|--------------|--------------| 
| Feature 1 | ✅ | ✅ | ❌ |
| Feature 2 | ✅ | ⚠️ Limited | ✅ |
| Feature 3 | ❌ Roadmap | ✅ | ✅ |

Legend:
- ✅ Full support
- ⚠️ Limited/partial
- ❌ Not available
- 🔜 On roadmap

### Positioning Map

```
                    HIGH PRICE
                        │
          Enterprise    │    Premium
          (Competitor A)│    (Us?)
                        │
    ────────────────────┼────────────────────
                        │
          Budget        │    Value
          (Competitor C)│    (Competitor B)
                        │
                    LOW PRICE
    
    LESS ◄──────────────┼──────────────► MORE
    FEATURES            │            FEATURES
```

### SWOT Analysis

| | Strengths | Weaknesses |
|---|-----------|------------|
| **Internal** | What they do well | Where they struggle |
| **External** | Opportunities they have | Threats they face |

### Win/Loss Themes

| We Win When... | We Lose When... |
|----------------|-----------------|
| [Scenario 1] | [Scenario 1] |
| [Scenario 2] | [Scenario 2] |

## Battle Card Template

```markdown
# Battle Card: [Competitor Name]

## Quick Facts
- **What they do:** [One sentence]
- **Founded:** [Year]
- **HQ:** [Location]
- **Size:** [Employees]
- **Funding:** [Amount/Stage]
- **Pricing:** [Model/Range]

## Their Pitch
"[Their tagline/headline]"

## Target Customer
[Who they sell to]

## Key Strengths (Where They Win)
1. [Strength 1]
2. [Strength 2]
3. [Strength 3]

## Key Weaknesses (Where We Win)
1. [Weakness 1]
2. [Weakness 2]
3. [Weakness 3]

## Feature Comparison
| Feature | Us | Them |
|---------|-------|------|
| [Feature] | ✅ | ❌ |

## Pricing Comparison
| Tier | Us | Them |
|------|-------|------|
| Starter | $X | $Y |
| Pro | $X | $Y |

## Common Objections & Responses

**"[Competitor] has [feature]"**
> [Our response]

**"[Competitor] is cheaper"**
> [Our response]

**"[Competitor] integrates with [tool]"**
> [Our response]

## Landmines to Plant
Questions to ask that expose their weaknesses:
1. "How do you handle [thing we do better]?"
2. "What's their approach to [our strength area]?"

## Proof Points
- [Customer who switched from them]
- [Metric where we outperform]
- [Review quote highlighting their weakness]

## Red Flags (When to Walk Away)
- [Scenario where they're better fit]
```

## Review Mining Guide

### G2 Review Analysis

Look for patterns in:

**5-Star Reviews (What they do well)**
- Features mentioned positively
- Use cases that work well
- Customer types who love them

**1-3 Star Reviews (Weaknesses)**
- Common complaints
- Missing features
- Support issues
- Bugs/reliability
- Pricing complaints

**Review Titles** (Quick sentiment scan)
- Extract top 10 positive titles
- Extract top 10 negative titles

### Reddit Analysis

Search queries:
```
reddit_search("[competitor] review")
reddit_search("[competitor] vs [alternative]")
reddit_search("[competitor] problems OR issues OR hate")
reddit_search("[competitor] love OR great OR recommend")
reddit_search("alternative to [competitor]")
```

Look for:
- Unfiltered opinions
- Edge cases and power user issues
- Migration stories (why people switched)
- Recommendations for alternatives

## Competitive Monitoring

### Weekly Tasks
- [ ] Check competitor blog for new posts
- [ ] Search news for competitor mentions
- [ ] Review G2/Capterra for new reviews
- [ ] Check LinkedIn for new hires/job posts

### Monthly Tasks
- [ ] Full pricing page screenshot comparison
- [ ] Feature page comparison
- [ ] Social media content themes
- [ ] SEO ranking changes

### Quarterly Tasks
- [ ] Full competitive analysis refresh
- [ ] Battle card updates
- [ ] Win/loss analysis review
- [ ] Positioning review

## Output Checklist

Before delivering competitive intel:

- [ ] All pricing is current (note date captured)
- [ ] Review data includes volume + rating
- [ ] Screenshots captured for visual comparison
- [ ] At least 3 "how to win" tactics
- [ ] Objection handling for top 3 objections
- [ ] Sources cited for all claims
