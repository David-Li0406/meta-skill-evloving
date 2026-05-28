# Market Research Playbook

## When to Use
- Entering new markets
- Content strategy planning
- Competitive landscape mapping
- Investor presentations
- Strategic planning

## Research Depths

### Quick Scan (15 minutes)
For a fast market overview:
```
web_search("[market/topic] market size")
web_search("[market/topic] trends 2024")
g2_scrape(category_slug)
reddit_search("[topic]", subreddit="SaaS")
```

### Standard Research (1 hour)
For solid market understanding:
- Quick scan +
- Top 5 competitor analysis
- Customer pain point mapping
- Trend identification

### Deep Dive (4+ hours)
For strategic decisions:
- Standard research +
- TAM/SAM/SOM calculation
- Full competitive matrix
- Customer interview synthesis
- Regulatory/compliance review

## Market Sizing Framework

### TAM (Total Addressable Market)
The total market demand for a product/service.

**How to calculate:**
1. Top-down: Industry reports × relevant segment %
2. Bottom-up: # of potential customers × average deal size

**Sources:**
- Industry analyst reports (Gartner, Forrester, IDC)
- Government data (Census, BLS)
- Trade associations
- Public company filings

### SAM (Serviceable Addressable Market)
The portion of TAM you can serve with your product.

**How to calculate:**
TAM × (% that matches your ICP)

**Consider:**
- Geographic limitations
- Company size fit
- Industry fit
- Technical requirements

### SOM (Serviceable Obtainable Market)
The realistic portion you can capture.

**How to calculate:**
SAM × realistic market share % (usually 1-5% for new entrants)

**Factors:**
- Current market share
- Go-to-market capacity
- Competitive intensity
- Brand awareness

## Market Analysis Template

```markdown
# Market Analysis: [Market Name]

## Executive Summary
[2-3 sentences: What is this market, how big, why it matters]

## Market Definition
**What's included:**
- [Segment 1]
- [Segment 2]

**What's excluded:**
- [Adjacent market 1]
- [Adjacent market 2]

## Market Size
| Metric | Value | Source |
|--------|-------|--------|
| TAM | $X | [Source] |
| SAM | $X | Calculated |
| SOM | $X | Calculated |
| Growth Rate | X% CAGR | [Source] |

## Market Drivers
1. **Driver 1:** [Description]
2. **Driver 2:** [Description]
3. **Driver 3:** [Description]

## Market Challenges
1. **Challenge 1:** [Description]
2. **Challenge 2:** [Description]

## Competitive Landscape

### Market Leaders
| Company | Est. Share | Strengths |
|---------|------------|-----------|
| | | |

### Emerging Players
| Company | Funding | Differentiation |
|---------|---------|-----------------|
| | | |

### Competitive Dynamics
- [Key competitive theme 1]
- [Key competitive theme 2]

## Customer Landscape

### Buyer Segments
| Segment | Size | Willingness to Pay | Our Fit |
|---------|------|-------------------|---------|
| | | | |

### Common Pain Points
1. [Pain point with evidence]
2. [Pain point with evidence]
3. [Pain point with evidence]

### Buying Process
- **Typical buyer:** [Role]
- **Decision makers:** [Roles involved]
- **Evaluation criteria:** [Top 3]
- **Deal cycle:** [Typical length]

## Trends & Predictions

### Short-term (1 year)
- [Trend 1]
- [Trend 2]

### Medium-term (2-3 years)
- [Trend 1]
- [Trend 2]

### Long-term (5+ years)
- [Trend 1]
- [Trend 2]

## Opportunities for Us
1. **Opportunity 1:** [Description + why we can win]
2. **Opportunity 2:** [Description + why we can win]

## Threats to Consider
1. **Threat 1:** [Description + mitigation]
2. **Threat 2:** [Description + mitigation]

## Recommendations
1. [Strategic recommendation 1]
2. [Strategic recommendation 2]
3. [Strategic recommendation 3]

## Sources
- [Source 1]
- [Source 2]
```

## Research Tool Sequences

### For Market Size
```
web_search("[market] market size 2024")
web_search("[market] TAM SAM")
web_search("[market] industry report")
firecrawl_scrape(industry_report_url)
```

### For Competitive Landscape
```
g2_scrape(category_slug)
web_search("[market] competitors landscape")
web_search("top [market] companies")
```

### For Customer Pain Points
```
reddit_search("[market] problems OR frustrating OR hate")
reddit_search("[market] wish OR need OR want")
g2_scrape(competitor) # Look at negative reviews
capterra_scrape(competitor)
```

### For Trends
```
web_search("[market] trends 2024 2025")
web_search("[market] future predictions")
web_search("[market] emerging technology")
reddit_search("[market] changing OR new OR future", subreddit="relevant_sub")
```

## Pain Point Mining

### Reddit Queries
```
"[product category] sucks"
"[product category] frustrating"
"hate [product category]"
"wish [product category] would"
"looking for [product category] alternative"
"[competitor] problems"
```

### G2/Capterra Mining
Look for patterns in 1-3 star reviews:
- Missing features
- Usability complaints
- Support issues
- Pricing concerns
- Integration gaps

### Signal Phrases in Reviews
**High pain:**
- "Dealbreaker"
- "Had to switch"
- "Wasted hours/days"
- "Cost us money"

**Moderate pain:**
- "Wish it had"
- "Would be nice if"
- "Annoying that"

**Low pain:**
- "Minor issue"
- "Not a big deal"
- "Would be cool"

## Trend Identification Framework

### PESTLE Analysis
| Factor | Current State | Trend Direction | Impact on Market |
|--------|---------------|-----------------|------------------|
| **P**olitical | | | |
| **E**conomic | | | |
| **S**ocial | | | |
| **T**echnological | | | |
| **L**egal | | | |
| **E**nvironmental | | | |

### Technology Adoption Curve
Where is the market?
- [ ] Innovators (2.5%)
- [ ] Early Adopters (13.5%)
- [ ] Early Majority (34%)
- [ ] Late Majority (34%)
- [ ] Laggards (16%)

### Market Maturity Signals
**Emerging Market:**
- Few established players
- Rapid growth
- Undefined categories
- Education-heavy sales

**Growth Market:**
- Clear category leaders emerging
- Many new entrants
- Consolidation beginning
- Feature competition

**Mature Market:**
- Established leaders
- Price competition
- Commoditization
- Innovation at edges

## Quality Checklist

Before delivering market research:

- [ ] Market clearly defined (what's in/out)
- [ ] TAM/SAM/SOM calculated with sources
- [ ] At least 3 market drivers identified
- [ ] At least 5 competitors mapped
- [ ] Customer pain points backed by evidence
- [ ] Trends have supporting data
- [ ] All claims have sources
- [ ] Recommendations are actionable
