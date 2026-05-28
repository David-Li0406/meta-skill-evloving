# Competitor Intelligence Framework

## Purpose

Map the competitive landscape, identify gaps, and understand what you're up against. Answer: "Can I compete?"

---

## Competitor Identification

### Types of Competitors

| Type | Definition | Example |
|------|------------|---------|
| **Direct** | Same problem, same solution approach | Notion vs Coda |
| **Indirect** | Same problem, different approach | Notion vs physical notebook |
| **Adjacent** | Related problem, could expand | Slack could add docs |
| **Substitute** | Alternative ways to solve | Hiring a VA vs automation tool |

### Finding Competitors

**Search patterns:**
```
# Direct competitors
"{product type} alternatives"
"best {product type} 2024"
"{product type} vs"
"tools like {known competitor}"

# On comparison sites
site:g2.com "{product type}"
site:capterra.com "{product type}"
site:producthunt.com "{product type}"

# In communities
site:reddit.com "what do you use for {problem}"
site:news.ycombinator.com "{product type}"
```

**Places to check:**
- G2 (g2.com) - Enterprise/SMB software
- Capterra - Business software
- Product Hunt - New products
- AlternativeTo - Alternative finder
- Crunchbase - Funded competitors
- GitHub - Open source alternatives

---

## Competitor Analysis Template

### For Each Major Competitor

```markdown
## {Competitor Name}

**URL:** {website}
**Founded:** {year}
**Funding:** {amount or bootstrapped}
**Team Size:** {estimate}

### Positioning
**Tagline:** "{their tagline}"
**Target User:** {who they serve}
**Key Differentiator:** {what they emphasize}

### Product
**Core Features:**
1. {Feature 1}
2. {Feature 2}
3. {Feature 3}

**Notable Limitations:**
- {Limitation 1}
- {Limitation 2}

### Pricing
| Tier | Price | Key Features |
|------|-------|--------------|
| {tier} | ${X}/mo | {features} |

**Pricing Strategy:** {Freemium / Free trial / Paid only / Usage-based}

### Strengths
- {Strength 1}
- {Strength 2}

### Weaknesses
- {Weakness 1}
- {Weakness 2}

### User Sentiment
**What users love:** {from reviews}
**What users hate:** {from reviews}
**Common complaints:** {patterns}
```

---

## Competitive Landscape Mapping

### Market Positioning Matrix

Plot competitors on two axes relevant to your market:

```
                    HIGH PRICE
                        │
         Enterprise     │     Premium
         Solutions      │     Boutique
                        │
    ────────────────────┼────────────────────
    COMPLEX             │             SIMPLE
                        │
         Feature-rich   │     Emerging
         Legacy         │     Challengers
                        │
                    LOW PRICE
```

### Gap Analysis

**Questions to answer:**
1. Where is the white space on the map?
2. What user needs are underserved?
3. What price points are missing?
4. What use cases are ignored?

**Gap types:**
- **Feature gap** - Missing functionality
- **Price gap** - No option at certain price point
- **Segment gap** - User type not served
- **Experience gap** - Bad UX opportunity
- **Integration gap** - Doesn't connect to X

---

## Competitive Moat Assessment

### Types of Moats

| Moat Type | Description | Strength |
|-----------|-------------|----------|
| **Network Effects** | More users = more value | Very Strong |
| **Switching Costs** | Hard to leave | Strong |
| **Data Moat** | Unique data advantage | Strong |
| **Brand** | Trust and recognition | Medium |
| **Scale Economics** | Cost advantages at scale | Medium |
| **Regulatory** | Licensed, certified | Variable |
| **Speed** | First mover advantage | Temporary |

### Moat Vulnerabilities

**Even strong moats have weaknesses:**

| Moat | Vulnerability |
|------|---------------|
| Network effects | Can be bootstrapped in niches |
| Switching costs | Migrations tools can reduce |
| Data moat | New data sources emerge |
| Brand | Challenger brands can win segments |
| Scale | Focused products beat bloated ones |

### Solo Builder Advantage

You can compete by:
- **Focus** - Serve one segment extremely well
- **Speed** - Ship faster than committee-driven orgs
- **Experience** - Better UX than legacy products
- **Price** - Undercut or use different model
- **Service** - Personal touch at small scale
- **Positioning** - Own a niche they ignore

---

## Scraping Competitors

### Using Firecrawl

```javascript
// Get competitor landing page
mcp__firecrawl__firecrawl_scrape({
  url: "https://competitor.com",
  formats: ["markdown"]
})

// Extract pricing
mcp__firecrawl__firecrawl_extract({
  urls: ["https://competitor.com/pricing"],
  prompt: "Extract all pricing tiers, prices, and features",
  schema: {
    type: "object",
    properties: {
      tiers: {
        type: "array",
        items: {
          type: "object",
          properties: {
            name: { type: "string" },
            price: { type: "string" },
            features: { type: "array" }
          }
        }
      }
    }
  }
})

// Search for reviews
mcp__firecrawl__firecrawl_search({
  query: "{competitor} reviews complaints site:reddit.com",
  limit: 10
})
```

---

## Finding Weaknesses

### Review Mining

**Where to look:**
- G2 reviews (filter by 1-3 stars)
- Capterra reviews
- App Store / Play Store
- Trustpilot
- Reddit complaints
- Twitter/X mentions

**Search patterns:**
```
"{competitor} review"
"{competitor} terrible" OR "{competitor} frustrating"
"{competitor} alternative reddit"
"{competitor} vs {other}" site:reddit.com
"switching from {competitor}"
"left {competitor} for"
```

**What to extract:**
- Recurring complaints (pattern = opportunity)
- Feature requests (unmet needs)
- Support issues (experience gap)
- Pricing complaints (price gap)
- Complexity complaints (UX opportunity)

### Weakness Categories

| Category | Example Complaint | Your Opportunity |
|----------|-------------------|------------------|
| Price | "Too expensive for small teams" | Lower price tier |
| Complexity | "Takes forever to learn" | Simpler UX |
| Features | "Wish it could do X" | Build X |
| Support | "Can never reach anyone" | Personal service |
| Performance | "So slow and buggy" | Fast, reliable |
| Integration | "Doesn't work with Y" | Integrate with Y |

---

## Competitive Response Prediction

### How Will They React?

| Your Action | Likely Response | Counter |
|-------------|-----------------|---------|
| Undercut price | May ignore (too small), may match | Build value, not just price |
| New feature | May copy if validated | Move fast, iterate faster |
| Target their weakness | May try to fix | Establish position before they react |
| Niche focus | Usually ignore | Perfect - own the niche |

### Competitor Behavior Signals

**Slow-moving (good for you):**
- Infrequent product updates
- Old blog posts
- Legacy tech stack
- Large team, bureaucratic
- VC pressure for revenue over product

**Fast-moving (watch out):**
- Frequent releases
- Active community engagement
- Modern tech stack
- Small, focused team
- Product-led growth

---

## Output Format

```markdown
## Competitive Landscape

### Key Competitors

| Competitor | Type | Strength | Weakness | Threat Level |
|------------|------|----------|----------|--------------|
| {Name} | Direct | {strength} | {weakness} | High/Med/Low |
| {Name} | Indirect | {strength} | {weakness} | High/Med/Low |

### Positioning Map

{Description of where competitors sit and where gap exists}

### Gap Analysis

**Identified Gaps:**
1. **{Gap 1}** - {Description and opportunity}
2. **{Gap 2}** - {Description and opportunity}

### Competitive Moats

| Competitor | Primary Moat | Vulnerability |
|------------|--------------|---------------|
| {Name} | {moat type} | {how to overcome} |

### User Complaints (Opportunities)

| Complaint Pattern | Frequency | Opportunity |
|-------------------|-----------|-------------|
| "{complaint}" | Common | {how to address} |

### Your Potential Advantage

{Based on gaps and weaknesses, here's where you can win:}

1. {Advantage 1}
2. {Advantage 2}
3. {Advantage 3}
```

---

## Red Flags

- Dominant player with 60%+ market share and strong moat
- Well-funded competitors recently launched
- Commoditized market with race to bottom pricing
- Competitors have features you can't replicate
- Big tech actively investing in space
